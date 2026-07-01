package com.scorpius.knowledge.attck.application.dto;

import jakarta.validation.constraints.NotBlank;

/**
 * 查询请求 DTO
 */
public class QueryRequest {

    @NotBlank(message = "question 不能为空")
    private String question;

    private Integer topK = 5;

    public QueryRequest() {}

    public QueryRequest(String question) {
        this.question = question;
    }

    public String getQuestion() { return question; }
    public void setQuestion(String question) { this.question = question; }

    public int getTopK() { return topK != null ? topK : 5; }
    public void setTopK(int topK) { this.topK = topK; }
}
