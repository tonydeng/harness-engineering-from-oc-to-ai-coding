"""
attck-knowledge mdBook Parser & Vector Indexer — 零 llama-index 版

移除所有 llama-index 依赖，直接用 sentence-transformers 做 embedding，
用 sqlite-vec Python 包做向量存储。

使用方式:
    python index_builder.py --src <attck-knowledge/src> --db <output.db>

依赖:
    pip install sentence-transformers sqlite-vec
"""

import os, re, json, logging, argparse, sqlite3
from typing import Iterator
from dataclasses import dataclass, field, asdict

logging.basicConfig(
    level=getattr(logging, os.getenv("LOG_LEVEL", "INFO").upper()),
    format="%(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class AttckChunk:
    """一个 ATT&CK 知识块，包含文本和结构化元数据"""
    text: str
    meta: dict = field(default_factory=lambda: {
        "level": None,          # tactic | technique | sub_technique
        "ta_id": None,
        "ta_name": None,
        "t_id": None,
        "t_name": None,
        "sub_id": None,
        "difficulty": None,
        "section": None,
    })


# ---------------------------------------------------------------------------
# Parser — mdBook 导航目录结构感知（与原版一致）
# ---------------------------------------------------------------------------

TA_ID_PATTERN = re.compile(r'(TA\d{4})')
T_ID_PATTERN  = re.compile(r'(T\d{4}(?:\.\d{3})?)')

def extract_ta_id(text: str) -> str:
    """从正文中提取第一个 TAxxxx 编号"""
    m = TA_ID_PATTERN.search(text)
    return m.group(1) if m else "TA0000"

def extract_t_id(text: str) -> str:
    """从正文中提取第一个 Txxxx 编号"""
    m = T_ID_PATTERN.search(text)
    return m.group(1) if m else "T0000"


def parse_mdbook(src_dir: str) -> Iterator[AttckChunk]:
    """
    按 mdBook 标准目录结构遍历：
      src/{NN}-{TacticName}/
          README.md                    ← 战术概览
          T{NNNN}-{TechniqueName}.md   ← 技术文档
          T{NNNN}/                     ← 子技术目录
              T{NNNN}.{NNN}-{Sub}.md   ← 子技术文档
    """
    if not os.path.isdir(src_dir):
        raise FileNotFoundError(f"Source directory not found: {src_dir}")

    for entry in sorted(os.listdir(src_dir)):
        tactic_path = os.path.join(src_dir, entry)
        if not os.path.isdir(tactic_path):
            continue

        # 提取战术名称： "00-reconnaissance" → "Reconnaissance"
        ta_name = entry.split("-", 1)[1] if "-" in entry else entry
        tactic_readme = os.path.join(tactic_path, "README.md")

        if os.path.exists(tactic_readme):
            text = _read_file(tactic_readme)
            ta_id = extract_ta_id(text)
            yield AttckChunk(
                text=text,
                meta={"level": "tactic", "ta_id": ta_id, "ta_name": ta_name},
            )
        else:
            ta_id = "TA0000"

        # 扫描技术和子技术
        for fname in sorted(os.listdir(tactic_path)):
            fpath = os.path.join(tactic_path, fname)

            if os.path.isfile(fpath) and fname.endswith(".md") and fname != "README.md":
                text = _read_file(fpath)
                t_id = fname.split("-")[0]  # "T1059-command.md" → "T1059"
                yield AttckChunk(
                    text=text,
                    meta={"level": "technique", "ta_id": ta_id, "t_id": t_id},
                )

            elif os.path.isdir(fpath):
                # 子技术目录
                for sub_fname in sorted(os.listdir(fpath)):
                    sub_fpath = os.path.join(fpath, sub_fname)
                    if sub_fname.endswith(".md"):
                        text = _read_file(sub_fpath)
                        sub_id = sub_fname.split("-")[0]  # "T1059.001-sub.md" → "T1059.001"
                        yield AttckChunk(
                            text=text,
                            meta={
                                "level": "sub_technique",
                                "ta_id": ta_id,
                                "t_id": fname,  # 父目录名即技术ID
                                "sub_id": sub_id,
                            },
                        )


def _read_file(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# ---------------------------------------------------------------------------
# Index Builder — sentence-transformers + sqlite-vec
# ---------------------------------------------------------------------------

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS attck_chunks (
    chunk_text TEXT NOT NULL,
    metadata   TEXT NOT NULL DEFAULT '{}',
    embedding  BLOB
);
"""

INSERT_CHUNK_SQL = """
INSERT INTO attck_chunks (chunk_text, metadata, embedding)
VALUES (?, ?, ?)
"""


def build_index(src_dir: str, db_path: str, model_name: str = "BAAI/bge-small-zh-v1.5"):
    """
    全流程：解析 → 向量化 → 存储到 sqlite-vec 数据库

    Args:
        src_dir: attck-knowledge 仓库的 src/ 目录
        db_path: 输出 SQLite 数据库路径
        model_name: sentence-transformers 模型名
    """
    # 1. 解析 mdBook 目录
    chunks = list(parse_mdbook(src_dir))
    logger.info(f"Parsed %d chunks from %s", len(chunks), src_dir)

    # 2. 初始化 SQLite 数据库
    conn = sqlite3.connect(db_path)
    conn.execute(CREATE_TABLE_SQL)
    conn.commit()

    # 3. 加载 sentence-transformers 模型
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(model_name)
    logger.info("Embedding model loaded: %s", model_name)

    # 4. 加载 sqlite-vec 扩展
    conn.enable_load_extension(True)
    import sqlite_vec
    sqlite_vec.load(conn)
    logger.debug("sqlite-vec 扩展已加载")

    # 5. 分批 embedding 并写入
    batch_size = 32
    total = len(chunks)

    for i in range(0, total, batch_size):
        batch = chunks[i:i + batch_size]
        texts = [c.text for c in batch]

        # 批量编码（自动 GPU 加速如果可用）
        embeddings = model.encode(texts, show_progress_bar=False)

        # 序列化为 BLOB 并批量插入
        rows = []
        for j, chunk in enumerate(batch):
            blob = sqlite_vec.serialize_float32(embeddings[j])
            rows.append((
                chunk.text,
                json.dumps(chunk.meta, ensure_ascii=False),
                blob,
            ))

        conn.executemany(INSERT_CHUNK_SQL, rows)
        conn.commit()

        inserted = min(i + batch_size, total)
        logger.info("  Inserted %d/%d chunks", inserted, total)

    # 6. 验证
    count = conn.execute("SELECT COUNT(*) FROM attck_chunks").fetchone()[0]
    conn.close()
    logger.info("Index built successfully: %s (%d chunks)", db_path, count)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Build ATT&CK knowledge index")
    ap.add_argument("--src", required=True, help="attck-knowledge/src/ directory")
    ap.add_argument("--db", default="attck_vec.db", help="Output SQLite path (default: attck_vec.db)")
    args = ap.parse_args()

    try:
        build_index(args.src, args.db)
    except ImportError as e:
        logger.warning("Missing dependency (%s); falling back to JSON export", e)
        chunks = list(parse_mdbook(args.src))
        json_path = args.db.replace(".db", ".json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump([asdict(c) for c in chunks], f, ensure_ascii=False, indent=2)
        logger.info("Chunks saved to %s (%d chunks)", json_path, len(chunks))


if __name__ == "__main__":
    main()
