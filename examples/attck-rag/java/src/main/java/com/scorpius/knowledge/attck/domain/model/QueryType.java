package com.scorpius.knowledge.attck.domain.model;

/**
 * 查询类型枚举 — 决定模型路由 + 渐进披露深度
 * <p>
 * Scorpius 模式：按查询复杂度路由到不同模型/成本管控。
 */
public enum QueryType {

    /** 精确 TID/TA ID 查询 — 走 FTS5 精确匹配，3B 模型即可 */
    EXACT(1, "qwen2.5:3b-instruct-q4_K_M"),

    /** 事实性/定义性查询 — 需聚合多个技术信息，3B 模型即可 */
    FACTUAL(2, "qwen2.5:3b-instruct-q4_K_M"),

    /** 分析/推理类查询 — 需跨战术关联推理，7B 模型 */
    ANALYSIS(3, "qwen2.5:7b-instruct-q4_K_M");

    private final int disclosureDepth;
    private final String defaultModel;

    QueryType(int disclosureDepth, String defaultModel) {
        this.disclosureDepth = disclosureDepth;
        this.defaultModel = defaultModel;
    }

    /** 渐进披露深度: 1=tactic, 2=tactic+technique, 3=all */
    public int getDisclosureDepth() { return disclosureDepth; }

    /** 此查询类型推荐的默认模型 */
    public String getDefaultModel() { return defaultModel; }
}
