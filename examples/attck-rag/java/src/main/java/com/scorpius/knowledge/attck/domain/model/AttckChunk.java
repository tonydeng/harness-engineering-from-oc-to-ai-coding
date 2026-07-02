package com.scorpius.knowledge.attck.domain.model;

import java.util.Collections;
import java.util.Map;

/**
 * ATT&CK 知识块 — 领域模型
 * <p>
 * 对应 attck-knowledge 中的一篇 Markdown 文档，
 * 按 mdBook 目录层级（战术/技术/子技术）解析并注入结构化元数据。
 */
public class AttckChunk {

    private final String id;
    private final String text;
    private final Map<String, Object> metadata;
    private final Double score;

    public AttckChunk(String id, String text, Map<String, Object> metadata, Double score) {
        this.id = id;
        this.text = text;
        this.metadata = metadata != null
                ? Collections.unmodifiableMap(metadata)
                : Collections.emptyMap();
        this.score = score;
    }

    public AttckChunk(String id, String text, Map<String, Object> metadata) {
        this(id, text, metadata, null);
    }

    /** chunk ID（pgvector 主键 UUID） */
    public String getId() { return id; }

    /** Markdown 原文 */
    public String getText() { return text; }

    /** 结构化元数据: {level, ta_id, ta_name, t_id, t_name, sub_id, difficulty} */
    public Map<String, Object> getMetadata() { return metadata; }

    /** RRF 融合后的得分（仅检索结果包含） */
    public Double getScore() { return score; }

    /** 获取元数据字段辅助方法 */
    public String getLevel() { return (String) metadata.get("level"); }
    public String getTaId() { return (String) metadata.get("ta_id"); }
    public String getTId() { return (String) metadata.get("t_id"); }
    public String getSubId() { return (String) metadata.get("sub_id"); }
}
