package com.scorpius.knowledge.attck.domain.service;

import com.scorpius.knowledge.attck.domain.model.AttckChunk;
import com.scorpius.knowledge.attck.domain.model.QueryType;

import java.util.List;

/**
 * 混合检索领域服务 — 领域层接口
 * <p>
 * 双路召回（向量 + 全文）→ RRF 融合 → Progressive Disclosure 过滤。
 * 实现在 infrastructure 层，领域层只定义契约。
 */
public interface HybridRetrieverService {

    /**
     * 执行混合检索
     *
     * @param query    用户原始查询
     * @param queryType 查询类型（决定披露深度）
     * @param topK     最终返回 TOP K
     * @return RRF 融合并经过披露过滤后的结果
     */
    List<AttckChunk> retrieve(String query, QueryType queryType, int topK);
}
