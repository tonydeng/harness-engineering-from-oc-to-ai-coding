-- ============================================================================
-- ATT&CK RAG — pgvector 数据库表结构
-- 单表存储向量 + 全文索引 + 元数据，无需额外组件
-- ============================================================================

-- 启用 pgvector 扩展
CREATE EXTENSION IF NOT EXISTS vector;

-- --------------------------------------------------------------------------
-- 主表：ATT&CK 知识块
-- --------------------------------------------------------------------------
CREATE TABLE attck_chunks (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chunk_text  TEXT NOT NULL,                              -- 原始文本
    embedding   vector(768),                                -- bge-small-zh-v1.5 768 维
    metadata    JSONB NOT NULL DEFAULT '{}',                 -- {level, ta_id, t_id, sub_id, ...}
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- --------------------------------------------------------------------------
-- 索引
-- --------------------------------------------------------------------------

-- 1. 向量索引 (IVFFlat, 100 lists ≈ 适中的准确率/速度平衡)
CREATE INDEX idx_attck_embedding
    ON attck_chunks
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- 2. 全文检索索引 (GIN + simple 分词器，适合英文 TID + 中文混合)
CREATE INDEX idx_attck_fts
    ON attck_chunks
    USING GIN (to_tsvector('simple', chunk_text));

-- 3. JSONB 元数据索引 (GIN，支持 @>、?、->> 等操作符)
CREATE INDEX idx_attck_metadata
    ON attck_chunks
    USING GIN (metadata);

-- 4. 分层查询索引 (加速 level 过滤)
CREATE INDEX idx_attck_level
    ON attck_chunks ((metadata ->> 'level'));

-- --------------------------------------------------------------------------
-- 更新触发器
-- --------------------------------------------------------------------------
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_attck_chunks_updated_at
    BEFORE UPDATE ON attck_chunks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at();

-- --------------------------------------------------------------------------
-- 查询示例
-- --------------------------------------------------------------------------

-- 纯向量搜索
-- SELECT id, chunk_text, 1 - (embedding <=> '[0.01, 0.02, ...]') AS score
-- FROM attck_chunks
-- ORDER BY embedding <=> '[0.01, 0.02, ...]'
-- LIMIT 5;

-- 全文检索
-- SELECT id, chunk_text, ts_rank(to_tsvector('simple', chunk_text), plainto_tsquery('simple', 'DLL 注入')) AS score
-- FROM attck_chunks
-- WHERE to_tsvector('simple', chunk_text) @@ plainto_tsquery('simple', 'DLL 注入')
-- ORDER BY score DESC
-- LIMIT 5;

-- 元数据过滤 + 全文检索
-- SELECT id, chunk_text
-- FROM attck_chunks
-- WHERE metadata @> '{"ta_id": "TA0001"}'
--   AND to_tsvector('simple', chunk_text) @@ plainto_tsquery('simple', 'T1059')
-- LIMIT 10;

-- RRF 融合 (应用层实现，SQL 层只负责各自检索)
-- Java: HybridRetriever.retrieve(query, topK=5)
