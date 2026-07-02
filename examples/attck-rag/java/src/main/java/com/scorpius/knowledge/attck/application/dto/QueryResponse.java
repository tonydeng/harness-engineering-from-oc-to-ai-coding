package com.scorpius.knowledge.attck.application.dto;

import java.util.List;
import java.util.Map;

/**
 * 查询响应 DTO — 包含答案、检索来源、查询分类信息
 */
public class QueryResponse {

    private final String question;
    private final String queryType;
    private final int disclosureDepth;
    private final String answer;
    private final List<SourceItem> sources;

    public QueryResponse(String question, String queryType, int disclosureDepth,
                         String answer, List<SourceItem> sources) {
        this.question = question;
        this.queryType = queryType;
        this.disclosureDepth = disclosureDepth;
        this.answer = answer;
        this.sources = sources;
    }

    public String getQuestion() { return question; }
    public String getQueryType() { return queryType; }
    public int getDisclosureDepth() { return disclosureDepth; }
    public String getAnswer() { return answer; }
    public List<SourceItem> getSources() { return sources; }

    /** 来源项 */
    public static class SourceItem {
        private final String id;
        private final String level;
        private final String taId;
        private final String tId;
        private final String score;

        public SourceItem(String id, String level, String taId, String tId, Double score) {
            this.id = id;
            this.level = level;
            this.taId = taId;
            this.tId = tId;
            this.score = score != null ? String.format("%.3f", score) : null;
        }

        public String getId() { return id; }
        public String getLevel() { return level; }
        public String getTaId() { return taId; }
        public String getTId() { return tId; }
        public String getScore() { return score; }
    }
}
