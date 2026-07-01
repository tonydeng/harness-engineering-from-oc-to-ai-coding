package com.scorpius.knowledge.attck.domain.repository;

import com.scorpius.knowledge.attck.domain.model.AttckChunk;

import java.util.List;

/**
 * ATT&CK 知识块仓储接口 — 领域层
 * <p>
 * 定义数据访问契约，实现在 infrastructure 层。
 * 方法命名遵循 Scorpius DDD 规范: findBy{Field} / save / deleteBy{Field}
 */
public interface AttckChunkRepository {

    /**
     * 全文检索 (pgvector FTS5 tsvector)
     *
     * @param query 搜索关键词
     * @param limit 最大返回数
     * @return 按 ts_rank 降序排列的匹配块
     */
    List<AttckChunk> fullTextSearch(String query, int limit);
}
