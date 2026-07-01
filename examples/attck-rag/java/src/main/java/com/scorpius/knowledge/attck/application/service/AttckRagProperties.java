package com.scorpius.knowledge.attck.application.service;

import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.stereotype.Component;

import java.util.Map;

/**
 * ATT&CK RAG 配置 — 绑定 attck.rag.*
 * <p>
 * Scorpius 模式: @ConfigurationProperties 独立组件管理自有配置。
 */
@Component
@ConfigurationProperties(prefix = "attck.rag")
public class AttckRagProperties {

    private Map<String, String> models;
    private Retrieval retrieval = new Retrieval();
    private String sourcePath;

    /** 按查询类型获取对应模型名 */
    public String getModelForQueryType(String queryType) {
        if (models == null) return "qwen2.5:7b-instruct-q4_K_M";
        return models.getOrDefault(queryType, models.get("analysis"));
    }

    // ---- Getters / Setters ----

    public Map<String, String> getModels() { return models; }
    public void setModels(Map<String, String> models) { this.models = models; }

    public Retrieval getRetrieval() { return retrieval; }
    public void setRetrieval(Retrieval retrieval) { this.retrieval = retrieval; }

    public String getSourcePath() { return sourcePath; }
    public void setSourcePath(String sourcePath) { this.sourcePath = sourcePath; }

    /** 检索参数子配置 */
    public static class Retrieval {
        private int topK = 5;
        private double similarityThreshold = 0.3;
        private int rrfConstant = 60;
        private int overRetrieveFactor = 2;

        public int getTopK() { return topK; }
        public void setTopK(int topK) { this.topK = topK; }
        public double getSimilarityThreshold() { return similarityThreshold; }
        public void setSimilarityThreshold(double similarityThreshold) { this.similarityThreshold = similarityThreshold; }
        public int getRrfConstant() { return rrfConstant; }
        public void setRrfConstant(int rrfConstant) { this.rrfConstant = rrfConstant; }
        public int getOverRetrieveFactor() { return overRetrieveFactor; }
        public void setOverRetrieveFactor(int overRetrieveFactor) { this.overRetrieveFactor = overRetrieveFactor; }
    }
}
