package com.scorpius.knowledge.attck.api.rest;

import com.scorpius.knowledge.attck.application.dto.QueryRequest;
import com.scorpius.knowledge.attck.application.dto.QueryResponse;
import com.scorpius.knowledge.attck.application.service.AttckQueryAppService;

import jakarta.validation.Valid;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.web.bind.annotation.*;

/**
 * ATT&CK 知识库查询接口 — Scorpius REST 风格
 * <p>
 * 遵循 Scorpius API 规范:
 * - 路径前缀 /api/v1/
 * - 统一 ApiResponse 包装
 * - POST 体查询
 */
@RestController
@RequestMapping("/api/v1/attck")
public class QueryController {

    private static final Logger log = LoggerFactory.getLogger(QueryController.class);

    private final AttckQueryAppService appService;

    public QueryController(AttckQueryAppService appService) {
        this.appService = appService;
    }

    /**
     * 执行 ATT&CK RAG 查询
     * <p>
     * 请求体: {"question": "T1059 是什么", "topK": 5}
     */
    @PostMapping("/query")
    public ApiResponse<QueryResponse> query(@Valid @RequestBody QueryRequest request) {
        log.info("Query request: question='{}', topK={}", request.getQuestion(), request.getTopK());
        QueryResponse response = appService.query(request);
        return ApiResponse.ok(response);
    }

    /** 健康检查 */
    @GetMapping("/health")
    public ApiResponse<String> health() {
        return ApiResponse.ok("ok");
    }
}
