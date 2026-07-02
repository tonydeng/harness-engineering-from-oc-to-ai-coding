"""
ATT&CK RAG — 索引构建与查询检索

适用：作为 attck-rag skill 的底层引擎，由 Agent 调用来完成：
  1. --build  从 attck-knowledge mdBook 源码构建 sqlite-vec 向量库
  2. --query  执行混合检索并输出上下文（Agent 据此生成回答）

依赖: pip install sentence-transformers sqlite-vec numpy
"""

import os, re, json, sqlite3, argparse, logging
from pathlib import Path
from typing import Iterator

logging.basicConfig(level=logging.INFO, format="%(name)s | %(levelname)s | %(message)s")
logger = logging.getLogger("attck-rag")

# 压制第三方库的 INFO/DEBUG 日志（sentence-transformers / transformers / huggingface_hub / httpx）
for lib_logger in ("transformers", "huggingface_hub", "sentence_transformers", "tokenizers", "httpx"):
    logging.getLogger(lib_logger).setLevel(logging.ERROR)

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_DB = str(SKILL_DIR / "attck_vec.db")


# ---------------------------------------------------------------------------
# Data Model
# ---------------------------------------------------------------------------

class AttckChunk:
    def __init__(self, text: str, level: str = None, ta_id: str = None,
                 ta_name: str = None, t_id: str = None, sub_id: str = None):
        self.text = text
        self.meta = {k: v for k, v in locals().items()
                     if k != "self" and k != "text" and v is not None}


# ---------------------------------------------------------------------------
# mdBook Parser
# ---------------------------------------------------------------------------

TA_RE = re.compile(r'(TA\d{4})')
T_RE  = re.compile(r'(T\d{4}(?:\.\d{3})?)')

def parse_mdbook(src_dir: str) -> Iterator[AttckChunk]:
    for entry in sorted(os.listdir(src_dir)):
        tactic_path = os.path.join(src_dir, entry)
        if not os.path.isdir(tactic_path):
            continue

        ta_name = entry.split("-", 1)[1] if "-" in entry else entry
        readme = os.path.join(tactic_path, "README.md")

        if os.path.exists(readme):
            text = Path(readme).read_text(encoding="utf-8")
            ta_id = (TA_RE.search(text) or ["TA0000"])[0]
            yield AttckChunk(text, "tactic", ta_id, ta_name)

        for fname in sorted(os.listdir(tactic_path)):
            fpath = os.path.join(tactic_path, fname)
            if os.path.isfile(fpath) and fname.endswith(".md") and fname != "README.md":
                text = Path(fpath).read_text(encoding="utf-8")
                t_id = fname.split("-")[0]
                yield AttckChunk(text, "technique", ta_id, ta_name, t_id)
            elif os.path.isdir(fpath):
                for sub in sorted(os.listdir(fpath)):
                    sp = os.path.join(fpath, sub)
                    if sub.endswith(".md"):
                        text = Path(sp).read_text(encoding="utf-8")
                        sub_id = sub.split("-")[0]
                        yield AttckChunk(text, "sub_technique", ta_id, ta_name, fname, sub_id)


# ---------------------------------------------------------------------------
# Index Builder
# ---------------------------------------------------------------------------

CREATE_SQL = """CREATE TABLE IF NOT EXISTS attck_chunks (
    chunk_text TEXT NOT NULL, metadata TEXT NOT NULL DEFAULT '{}', embedding BLOB
);"""

INSERT_SQL = "INSERT INTO attck_chunks (chunk_text, metadata, embedding) VALUES (?, ?, ?)"

FTS5_SQL = """
CREATE VIRTUAL TABLE IF NOT EXISTS attck_chunks_fts USING fts5(
    chunk_text, ta_id UNINDEXED, t_id UNINDEXED,
    sub_id UNINDEXED, level UNINDEXED,
    content='attck_chunks', content_rowid='rowid'
);"""

FTS5_POPULATE = """INSERT OR IGNORE INTO attck_chunks_fts(rowid, chunk_text, ta_id, t_id, sub_id, level)
SELECT rowid, chunk_text, json_extract(metadata, '$.ta_id'), json_extract(metadata, '$.t_id'),
       json_extract(metadata, '$.sub_id'), json_extract(metadata, '$.level') FROM attck_chunks;"""


def build_index(src_dir: str, db_path: str, model_name: str = "BAAI/bge-small-zh-v1.5"):
    from sentence_transformers import SentenceTransformer
    import sqlite_vec, numpy as np

    chunks = list(parse_mdbook(src_dir))
    logger.info("解析到 %d 个知识块", len(chunks))

    conn = sqlite3.connect(db_path)
    conn.execute(CREATE_SQL)
    conn.commit()

    model = SentenceTransformer(model_name)
    conn.enable_load_extension(True)
    sqlite_vec.load(conn)

    batch_size = 32
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i + batch_size]
        texts = [c.text for c in batch]

        # 处理过长的文本（截断到模型最大 token 数）
        truncated = [t[:8192] if len(t) > 8192 else t for t in texts]
        embeddings = model.encode(truncated, show_progress_bar=False)

        rows = [(c.text, json.dumps(c.meta, ensure_ascii=False),
                 sqlite_vec.serialize_float32(embeddings[j]))
                for j, c in enumerate(batch)]
        conn.executemany(INSERT_SQL, rows)
        conn.commit()

    conn.executescript(FTS5_SQL)
    conn.executescript(FTS5_POPULATE)
    conn.commit()

    count = conn.execute("SELECT COUNT(*) FROM attck_chunks").fetchone()[0]
    conn.close()
    logger.info("索引构建完成: %s (%d 条)", db_path, count)


# ---------------------------------------------------------------------------
# FTS5 Query Builder — safe for CJK + TID queries
# ---------------------------------------------------------------------------

def _sanitize_fts5_query(query: str) -> str:
    """构建安全的 FTS5 查询 — 仅提取字母数字序列。

    FTS5 的 unicode61 tokenizer 对 CJK 单字 MATCH 不生效，
    故只提取 TID（T1059）、TA ID（TA0043）和英文单词用于全文检索。
    中文语义检索完全依赖向量路。

    同时移除 FTS5 特殊字符（. :）避免语法错误。
    """
    cleaned = query.replace('.', ' ').replace(':', ' ')
    tokens = re.findall(r'[A-Za-z0-9]+', cleaned)
    return ' '.join(tokens)


def direct_tid_lookup(conn: sqlite3.Connection, target_tid: str) -> list:
    """精确 TID 元数据召回 — 绕过语义搜索，直接按 metadata 字段匹配。

    用于 depth=1 的精确查询，保证 T1059.009 等子技术始终能被召回。
    """
    results = []
    try:
        cur = conn.execute("""
            SELECT rowid, chunk_text, metadata
            FROM attck_chunks
            WHERE json_extract(metadata, '$.t_id') = ?
               OR json_extract(metadata, '$.sub_id') = ?
               OR json_extract(metadata, '$.ta_id') = ?
            LIMIT 10
        """, (target_tid, target_tid, target_tid))
        for row in cur:
            meta = json.loads(row[2])
            results.append({
                "rowid": row[0], "text": row[1],
                "meta": meta, "rank": -1, "source": "direct_tid"
            })
    except Exception as e:
        logger.warning("Direct TID lookup failed: %s", e)
    return results


# ---------------------------------------------------------------------------
# Query Classification
# ---------------------------------------------------------------------------

EXACT_RE = re.compile(r'(T\d{4}(?:\.\d{3})?|TA\d{4})', re.IGNORECASE)
FACTUAL_KW = ["是什么", "定义", "含义", "编号", "包括哪些", "有哪些", "属于", "用途", "目的", "作用"]

def classify(query: str):
    if EXACT_RE.search(query):
        return "exact", 1
    for kw in FACTUAL_KW:
        if kw in query:
            return "factual", 2
    return "analysis", 3


def extract_target_tid(query: str) -> str | None:
    """从查询中提取目标 TID（用于 EXACT 精确过滤）"""
    m = EXACT_RE.search(query)
    return m.group(0).upper() if m else None


# ---------------------------------------------------------------------------
# Disclosure Filter
# ---------------------------------------------------------------------------

def disclosure_filter(chunks: list, depth: int, query: str = "") -> list:
    if depth >= 3:
        return chunks
    if depth == 1:
        target = extract_target_tid(query) if query else None
        if target:
            # EXACT: 只保留与目标 TID 精确匹配的块
            return [c for c in chunks
                    if c["meta"].get("t_id", "").upper() == target
                    or c["meta"].get("sub_id", "").upper() == target
                    or c["meta"].get("ta_id", "").upper() == target]
        # 无 TID 可匹配时，保留 technique 及以上层级
        return [c for c in chunks if c["meta"].get("level") in {"tactic", "technique"}]
    allowed = {2: {"tactic", "technique"}}
    return [c for c in chunks if c.get("meta", {}).get("level") in allowed.get(depth, set())]


# ---------------------------------------------------------------------------
# Quality Report
# ---------------------------------------------------------------------------

def quality_report(results: list, query_type: str) -> dict:
    """生成检索质量报告，供 Agent 交叉验证回答中的 TID 引用"""
    tids = set()
    ta_ids = set()
    levels = set()
    for r in results:
        meta = r.get("meta", {})
        if meta.get("t_id"):
            tids.add(meta["t_id"])
        if meta.get("sub_id"):
            tids.add(meta["sub_id"])
        if meta.get("ta_id"):
            ta_ids.add(meta["ta_id"])
        if meta.get("level"):
            levels.add(meta["level"])
    return {
        "ground_truth_tids": sorted(tids),
        "ground_truth_tactics": sorted(ta_ids),
        "chunk_count": len(results),
        "levels": sorted(levels),
        "query_type": query_type,
        "verification_note": "Agent 需确保回答中引用的 TID 均在此 ground_truth 列表中；不在列表中的 TID 可能为幻觉。",
    }


# ---------------------------------------------------------------------------
# Hybrid Search
# ---------------------------------------------------------------------------

RRF_K = 60

# 模型缓存 — 避免每次调用 hybrid_search 都重新加载
_MODEL_CACHE = None

def _get_model():
    global _MODEL_CACHE
    if _MODEL_CACHE is None:
        from sentence_transformers import SentenceTransformer
        _MODEL_CACHE = SentenceTransformer("BAAI/bge-small-zh-v1.5")
    return _MODEL_CACHE


def hybrid_search(conn: sqlite3.Connection, query: str, top_k: int, depth: int) -> list:
    # 输入验证 — 拒绝空/纯空格/单字符/孤立 T/TA 前缀
    if not query or not query.strip() or len(query.strip()) < 2 or query.strip().upper() in {"T", "TA"}:
        return []

    import sqlite_vec, numpy as np

    model = _get_model()
    query_emb = model.encode(query).tolist()

    # 向量检索
    vec_results = []
    try:
        cur = conn.execute(
            "SELECT rowid, chunk_text, metadata, vec_distance_L2(embedding, ?) AS d "
            "FROM attck_chunks ORDER BY d LIMIT ?",
            (json.dumps(query_emb), top_k * 2))
        for i, row in enumerate(cur):
            vec_results.append({"rowid": row[0], "text": row[1],
                                "meta": json.loads(row[2]), "rank": i, "source": "vec"})
    except Exception as e:
        logger.warning("向量检索失败: %s", e)

    # FTS5 检索（使用 sanitized query，避免 . 等特殊字符崩溃）
    fts_results = []
    try:
        fts_q = _sanitize_fts5_query(query)
        if fts_q.strip():
            cur = conn.execute(
                "SELECT a.rowid, a.chunk_text, a.metadata, rank "
                "FROM attck_chunks_fts f JOIN attck_chunks a ON f.rowid = a.rowid "
                "WHERE attck_chunks_fts MATCH ? ORDER BY rank LIMIT ?",
                (fts_q, top_k * 2))
            for i, row in enumerate(cur):
                fts_results.append({"rowid": row[0], "text": row[1],
                                    "meta": json.loads(row[2]), "rank": i, "source": "fts"})
    except Exception as e:
        logger.warning("FTS5 检索失败: %s", e)

    # 精确 TID 召回（depth=1 时保证子技术等精确匹配）
    tid_results = []
    if depth == 1:
        target = extract_target_tid(query)
        if target:
            tid_results = direct_tid_lookup(conn, target)
            logger.debug("Direct TID lookup for %s: %d results", target, len(tid_results))

    # RRF 融合 + 去重
    scores, docs = {}, {}
    for r in vec_results + fts_results + tid_results:
        rid = r["rowid"]
        # direct_tid results get rank=-1, which scores highest
        rank = r.get("rank", 0)
        scores[rid] = scores.get(rid, 0) + 1.0 / (RRF_K + rank + 1)
        if rid not in docs:
            docs[rid] = r

    merged = [docs[rid] for rid, _ in sorted(scores.items(), key=lambda x: -x[1])]
    merged = disclosure_filter(merged, depth, query)
    return merged[:top_k]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="ATT&CK RAG — 索引构建与检索")
    ap.add_argument("--build", action="store_true", help="构建索引")
    ap.add_argument("--src", help="attck-knowledge/src 目录路径")
    ap.add_argument("--db", default=DEFAULT_DB, help=f"数据库路径 (默认: {DEFAULT_DB})")
    ap.add_argument("--query", help="查询问题")
    ap.add_argument("--top-k", type=int, default=5, help="返回结果数 (默认: 5)")
    ap.add_argument("--json", action="store_true", help="JSON 格式输出")
    args = ap.parse_args()

    if args.build:
        if not args.src:
            ap.error("--build 需要 --src 参数")
        build_index(args.src, args.db)
        return

    if args.query:
        if not os.path.exists(args.db):
            logger.error("索引不存在: %s。请先运行 --build", args.db)
            return

        # 输入验证 — 拒绝空/纯空格/过短查询
        q_stripped = args.query.strip()
        if not q_stripped or len(q_stripped) < 2 or q_stripped.upper() in {"T", "TA"}:
            empty_report = {
                "query": args.query, "query_type": "invalid",
                "depth": 0, "results": [],
                "quality": {
                    "ground_truth_tids": [], "ground_truth_tactics": [],
                    "chunk_count": 0, "levels": [],
                    "query_type": "invalid",
                    "verification_note": "输入无效：查询为空、纯空格或过短。"
                }
            }
            if args.json:
                print(json.dumps(empty_report, ensure_ascii=False, indent=2))
            else:
                print("输入无效：查询为空、纯空格或过短。")
            return

        conn = sqlite3.connect(args.db)
        conn.enable_load_extension(True)
        try:
            import sqlite_vec
            sqlite_vec.load(conn)
        except Exception:
            pass

        # 确保 FTS5
        try:
            conn.executescript(FTS5_SQL)
            conn.executescript(FTS5_POPULATE)
            conn.commit()
        except Exception as e:
            logger.debug("FTS5 初始化: %s", e)

        qtype, depth = classify(args.query)
        results = hybrid_search(conn, args.query, args.top_k, depth)
        conn.close()

        if args.json:
            report = quality_report(results, qtype)
            print(json.dumps({
                "query": args.query,
                "query_type": qtype,
                "depth": depth,
                "results": [{
                    "level": r["meta"].get("level"),
                    "ta_id": r["meta"].get("ta_id"),
                    "t_id": r["meta"].get("t_id"),
                    "text": r["text"],
                } for r in results],
                "quality": report,
            }, ensure_ascii=False, indent=2))
        else:
            print(f"查询类型: {qtype}  |  披露深度: {depth}  |  结果数: {len(results)}")
            print("=" * 60)
            for i, r in enumerate(results, 1):
                meta = r["meta"]
                tid = meta.get("t_id") or meta.get("sub_id") or meta.get("ta_id", "?")
                level = meta.get("level", "?")
                preview = r["text"][:200].replace("\n", " ")
                print(f"\n[{i}] [{level}] {tid}")
                print(f"    {preview}...")
        return

    ap.print_help()


if __name__ == "__main__":
    main()
