"""
ATT&CK RAG — 配置
=================

使用方式:
    # 1) 编辑下面的路径指向你的 attck-knowledge 仓库
    # 2) python index_builder.py --src <你的路径>
    # 3) python query.py "T1059 是什么"

环境变量覆盖:
    ATTCK_SRC   — attck-knowledge 的 src/ 目录
    OLLAMA_HOST — Ollama 服务地址 (默认 http://localhost:11434)
    DB_PATH     — SQLite 向量库路径
"""

import os
from dataclasses import dataclass


@dataclass
class AttckRagConfig:
    # ---- 数据源 ----
    # attck-knowledge 仓库的 src/ 目录
    src_dir: str = os.getenv(
        "ATTCK_SRC",
        os.path.join(os.path.dirname(__file__), "..", "..", "attck-knowledge", "src"),
    )

    # ---- 向量库 ----
    db_path: str = os.getenv("DB_PATH", os.path.join(os.path.dirname(__file__), "..", "attck_vec.db"))
    table_name: str = "attck_chunks"

    # ---- Embedding ----
    embed_model: str = "BAAI/bge-small-zh-v1.5"

    # ---- Ollama ----
    ollama_host: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")

    # ---- 模型降级链 ----
    # 精确 TID 查询 → 轻量模型
    llm_exact: str = os.getenv("LLM_EXACT", "qwen2.5")
    # 事实查询 → 轻量模型
    llm_factual: str = os.getenv("LLM_FACTUAL", "qwen2.5")
    # 分析推理 → 大模型
    llm_analysis: str = os.getenv("LLM_ANALYSIS", "qwen2.5")

    # ---- 检索参数 ----
    top_k: int = 5
    similarity_threshold: float = 0.3

    # ---- RRF 融合 ----
    rrf_constant: int = 60
    over_retrieve_factor: int = 2
