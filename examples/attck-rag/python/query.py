"""
ATT&CK RAG — 交互查询 CLI
=========================

全链路演示：混合检索 + 模型降级 + 渐进披露 + 质量度量

使用方式:
    python query.py "T1059 是什么"              # 单次查询
    python query.py                              # 交互模式

环境变量:
    DB_PATH     — SQLite 向量库路径 (默认 ../attck_vec.db)
    OLLAMA_HOST — Ollama 地址 (默认 http://localhost:11434)
    ATTCK_SRC   — 仅用于构建 FTS5 索引 (首次自动补建)
"""

import os, sys, re, sqlite3, json, logging
from pathlib import Path
from config import AttckRagConfig

logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper()),
    format="%(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

# 将项目根加入 path
sys.path.insert(0, str(Path(__file__).resolve().parent))

# ---------------------------------------------------------------------------
# Query Type Classification
# ---------------------------------------------------------------------------

EXACT_PATTERN = re.compile(r'(T\d{4}(?:\.\d{3})?|TA\d{4})', re.IGNORECASE)
FACTUAL_KEYWORDS = ["是什么", "定义", "含义", "编号", "包括哪些", "有哪些", "属于"]

def classify_query(query: str) -> tuple[str, int]:
    """
    分类查询 + 确定渐进披露深度

    返回: (query_type, disclosure_depth)
        exact:    TID 精确匹配 → depth=1 (仅目标文档)
        factual:  事实/定义查询 → depth=2 (战术+技术)
        analysis: 推理/分析 → depth=3 (全量)
    """
    if EXACT_PATTERN.search(query):
        return "exact", 1
    for kw in FACTUAL_KEYWORDS:
        if kw in query:
            return "factual", 2
    return "analysis", 3


# ---------------------------------------------------------------------------
# FTS5 全文索引 (在已有 SQLite 数据库中补建)
# ---------------------------------------------------------------------------

FTS5_SCHEMA_SQL = """
CREATE VIRTUAL TABLE IF NOT EXISTS attck_chunks_fts USING fts5(
    chunk_text,
    ta_id UNINDEXED,
    t_id UNINDEXED,
    sub_id UNINDEXED,
    level UNINDEXED,
    content='attck_chunks',
    content_rowid='rowid'
);
"""

FTS5_POPULATE_SQL = """
INSERT OR IGNORE INTO attck_chunks_fts(rowid, chunk_text, ta_id, t_id, sub_id, level)
SELECT rowid, chunk_text,
       json_extract(metadata, '$.ta_id'),
       json_extract(metadata, '$.t_id'),
       json_extract(metadata, '$.sub_id'),
       json_extract(metadata, '$.level')
FROM attck_chunks;
"""


# ---------------------------------------------------------------------------
# Progressive Disclosure Filter
# ---------------------------------------------------------------------------

def disclosure_filter(chunks: list, depth: int) -> list:
    """按渐进披露深度过滤

    depth=1 (精确 TID): 放行所有层级——用户明确知道要什么
    depth=2 (事实查询): 只保留 tactic + technique，隐藏 sub_technique 细节
    depth=3 (分析推理): 全量
    """
    if depth >= 3:
        return chunks
    if depth == 1:
        # 精确匹配：用户指明 TID，不限制层级
        return chunks
    allowed_levels = {2: {"tactic", "technique"}}
    return [c for c in chunks if c.get("level") in allowed_levels.get(depth, set())]


# ---------------------------------------------------------------------------
# Hybrid Search
# ---------------------------------------------------------------------------

def hybrid_search(conn: sqlite3.Connection, query: str, top_k: int, depth: int):
    """
    双路检索 + RRF 融合

    向量路: sqlite-vec 自定义函数 (需已加载扩展)
    全文路: FTS5 MATCH
    融合:   RRF (Reciprocal Rank Fusion)
    """
    try:
        import numpy as np
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer("BAAI/bge-small-zh-v1.5")
        query_emb = model.encode(query).tolist()
    except ImportError:
        logger.error("缺少 sentence-transformers: pip install sentence-transformers")
        return []

    # ---- 向量检索 ----
    vec_results = []
    try:
        cur = conn.execute(
            "SELECT rowid, chunk_text, metadata, "
            "  vec_distance_L2(embedding, ?) AS distance "
            "FROM attck_chunks "
            "ORDER BY distance LIMIT ?",
            (json.dumps(query_emb), top_k * 2),
        )
        for i, row in enumerate(cur):
            vec_results.append({
                "rowid": row[0], "text": row[1],
                "meta": json.loads(row[2]), "rank": i,
                "source": "vector",
            })
    except Exception as e:
        logger.warning(f"向量检索失败 (sqlite-vec 扩展未加载?): {e}")

    # ---- FTS5 检索 ----
    fts_results = []
    try:
        # 中文分词: 空格分隔单个字符作为简单分词
        fts_query = " ".join(query.strip())
        cur = conn.execute(
            "SELECT a.rowid, a.chunk_text, a.metadata, "
            "  rank "
            "FROM attck_chunks_fts f "
            "JOIN attck_chunks a ON f.rowid = a.rowid "
            "WHERE attck_chunks_fts MATCH ? "
            "ORDER BY rank LIMIT ?",
            (fts_query, top_k * 2),
        )
        for i, row in enumerate(cur):
            fts_results.append({
                "rowid": row[0], "text": row[1],
                "meta": json.loads(row[2]), "rank": i,
                "source": "fts",
            })
    except Exception as e:
        logger.warning(f"FTS5 检索失败: {e}")

    # ---- RRF 融合 ----
    RRF_K = 60
    scores = {}
    docs = {}

    for r in vec_results:
        rid = r["rowid"]
        scores[rid] = scores.get(rid, 0) + 1.0 / (RRF_K + r["rank"] + 1)
        docs[rid] = r
    for r in fts_results:
        rid = r["rowid"]
        scores[rid] = scores.get(rid, 0) + 1.0 / (RRF_K + r["rank"] + 1)
        if rid not in docs:
            docs[rid] = r

    sorted_docs = sorted(scores.items(), key=lambda x: -x[1])
    results = [docs[rid] for rid, _ in sorted_docs]

    # ---- Progressive Disclosure ----
    results = disclosure_filter(results, depth)

    return results[:top_k]


# ---------------------------------------------------------------------------
# Model Cascade
# ---------------------------------------------------------------------------

def query_ollama(question: str, context: list, query_type: str, cfg: AttckRagConfig):
    """调用 Ollama 模型生成回答"""
    import httpx

    # 绕过系统代理（仅限 Ollama 调用）
    _old_no_proxy = os.environ.get("NO_PROXY", "")
    os.environ["NO_PROXY"] = "localhost,127.0.0.1"

    model_map = {
        "exact": cfg.llm_exact,
        "factual": cfg.llm_factual,
        "analysis": cfg.llm_analysis,
    }
    model = model_map.get(query_type, cfg.llm_analysis)
    logger.debug("模型路由: %s → %s", query_type, model)

    # 构建上下文
    ctx_text = "\n\n---\n\n".join([
        f"[{c.get('meta', {}).get('level', '?')}] "
        f"TA:{c.get('meta', {}).get('ta_id', '?')} "
        f"T:{c.get('meta', {}).get('t_id', '?')} "
        f"{c['text'][:500]}"
        for c in context
    ])

    prompt_templates = {
        "exact": (
            "请根据以下 ATT&CK 知识库文档回答问题。"
            "只使用给定的上下文，不要添加外部知识。\n\n"
            "## 上下文\n{context}\n\n## 问题\n{question}"
        ),
        "factual": (
            "请根据以下 ATT&CK 知识库内容回答问题。\n\n"
            "## 上下文\n{context}\n\n## 问题\n{question}"
        ),
        "analysis": (
            "你是一个 MITRE ATT&CK 安全分析师。"
            "根据以下检索结果回答问题。\n\n"
            "## 检索结果\n{context}\n\n"
            "## 要求\n"
            "- 引用具体的 TID 编号\n"
            "- 标注信息来源的战术归属\n"
            "- 不确定的信息请说明\n\n"
            "## 问题\n{question}"
        ),
    }
    prompt = prompt_templates.get(query_type, prompt_templates["analysis"]).format(
        context=ctx_text, question=question
    )

    try:
        resp = httpx.post(
            f"{cfg.ollama_host}/api/chat",
            json={
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "stream": False,
                "options": {"temperature": 0.1},
            },
            timeout=180.0,
        )
        resp.raise_for_status()
        result = resp.json()["message"]["content"]
        return result
    except Exception as e:
        logger.error(f"Ollama 调用失败: {e}")
        return f"[Ollama 错误] {e}"
    finally:
        # 恢复 NO_PROXY（不干扰 HuggingFace 等外部连接）
        if _old_no_proxy:
            os.environ["NO_PROXY"] = _old_no_proxy
        else:
            os.environ.pop("NO_PROXY", None)


# ---------------------------------------------------------------------------
# Quality Metrics
# ---------------------------------------------------------------------------

def quality_report(answer: str, context: list, query_type: str) -> dict:
    """质量度量: TID 命中率、幻觉检测、深度匹配度"""
    cited_tids = set(re.findall(r'(T\d{4}(?:\.\d{3})?|TA\d{4})', answer))
    context_tids = set()
    for c in context:
        m = c.get("meta", {})
        for k in ("ta_id", "t_id", "sub_id"):
            v = m.get(k)
            if v and re.match(r'(T\d{4}(?:\.\d{3})?|TA\d{4})$', str(v)):
                context_tids.add(v)

    hallucinated = cited_tids - context_tids
    return {
        "query_type": query_type,
        "cited_tids": sorted(cited_tids),
        "context_tids": sorted(context_tids),
        "hallucinated_tids": sorted(hallucinated),
        "tid_hit_rate": f"{len(cited_tids & context_tids)}/{len(cited_tids) if cited_tids else 'N/A'}",
        "hallucination_count": len(hallucinated),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    cfg = AttckRagConfig()

    # 连接数据库
    db_path = cfg.db_path
    if not os.path.exists(db_path):
        logger.error(f"索引文件不存在: {db_path}")
        logger.info("请先运行: python index_builder.py --src <attck-knowledge/src> --db <db_path>")
        sys.exit(1)

    conn = sqlite3.connect(db_path)
    conn.enable_load_extension(True)

    # 尝试加载 sqlite-vec 扩展（通过 Python 包）
    try:
        import sqlite_vec
        sqlite_vec.load(conn)
        logger.debug("sqlite-vec 扩展已加载")
    except Exception as e:
        logger.warning(f"sqlite-vec 扩展未加载，向量检索将不可用: {e}")

    # 确保 FTS5 表存在
    try:
        conn.executescript(FTS5_SCHEMA_SQL)
        conn.executescript(FTS5_POPULATE_SQL)
        conn.commit()
        logger.debug("FTS5 全文索引就绪")
    except Exception as e:
        logger.warning(f"FTS5 初始化: {e}")

    # 交互或单次模式
    questions = sys.argv[1:] if len(sys.argv) > 1 else []
    interactive = len(questions) == 0

    if interactive:
        print("\n🔍 ATT&CK RAG 查询终端")
        print("输入问题查询，输入 'exit' 退出\n")
        while True:
            try:
                q = input(">>> ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                break
            if not q:
                continue
            if q.lower() in ("exit", "quit", "q"):
                break
            questions = [q]
            process_query(questions[0], conn, cfg)
    else:
        for q in questions:
            process_query(q, conn, cfg)


def process_query(question: str, conn: sqlite3.Connection, cfg: AttckRagConfig):
    """执行单次查询全流程"""
    print(f"\n{'='*60}")
    print(f"问题: {question}")
    print(f"{'='*60}")

    # 1. 查询分类 + 披露深度
    query_type, depth = classify_query(question)
    logger.debug("查询类型: %s, 披露深度: %d", query_type, depth)

    # 2. 混合检索
    results = hybrid_search(conn, question, cfg.top_k, depth)
    if not results:
        print("(未检索到相关内容)\n")
        return

    print(f"\n检索到 {len(results)} 条结果:")
    for i, r in enumerate(results, 1):
        meta = r.get("meta", {})
        tid = meta.get("t_id") or meta.get("sub_id") or meta.get("ta_id", "?")
        level = meta.get("level", "?")
        preview = r["text"][:120].replace("\n", " ")
        print(f"  [{i}] [{level}] {tid}: {preview}...")

    # 3. LLM 生成
    print("\n生成回答中...")
    answer = query_ollama(question, results, query_type, cfg)

    # 4. 输出
    print(f"\n{'─'*60}")
    print(f"回答 [{query_type}]:")
    print(f"{'─'*60}")
    print(answer)

    # 5. 质量报告
    qr = quality_report(answer, results, query_type)
    print(f"\n{'─'*40}")
    print(f"质量度量:")
    print(f"  TID 引用: {qr['cited_tids']}")
    if qr["hallucinated_tids"]:
        print(f"  ⚠️ 潜在幻觉 TID (不在上下文中): {qr['hallucinated_tids']}")
    print(f"  命中率: {qr['tid_hit_rate']}")
    print()


if __name__ == "__main__":
    main()
