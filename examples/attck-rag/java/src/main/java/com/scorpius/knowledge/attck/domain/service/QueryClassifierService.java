package com.scorpius.knowledge.attck.domain.service;

import com.scorpius.knowledge.attck.domain.model.QueryType;

/**
 * 查询分类领域服务 — 领域层接口
 * <p>
 * 按查询内容自动分类为 EXACT / FACTUAL / ANALYSIS，
 * 决定使用哪个模型和多少上下文深度。
 */
public interface QueryClassifierService {

    /**
     * 对用户查询进行分类
     *
     * @param query 用户原始查询
     * @return 分类结果
     */
    QueryType classify(String query);
}
