package com.scorpius.knowledge.attck.application.service;

import com.scorpius.knowledge.attck.application.dto.QueryRequest;
import com.scorpius.knowledge.attck.application.dto.QueryResponse;
import com.scorpius.knowledge.attck.application.dto.QueryResponse.SourceItem;
import com.scorpius.knowledge.attck.domain.model.AttckChunk;
import com.scorpius.knowledge.attck.domain.model.QueryType;
import com.scorpius.knowledge.attck.domain.service.HybridRetrieverService;
import com.scorpius.knowledge.attck.domain.service.QueryClassifierService;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.prompt.PromptTemplate;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * ATT&CK 查询应用服务 — 协调分类 → 检索 → 生成 全链路
 * <p>
 * Scorpius 模式: 应用层协调多个领域服务完成一个用例，
 * 不含业务逻辑（业务逻辑在 domain service 中）。
 */
@Service
public class AttckQueryAppService {

    private static final Logger log = LoggerFactory.getLogger(AttckQueryAppService.class);

    private final QueryClassifierService classifier;
    private final HybridRetrieverService retriever;
    private final ChatClient chatClient;
    private final AttckRagProperties properties;

    public AttckQueryAppService(QueryClassifierService classifier,
                                HybridRetrieverService retriever,
                                ChatClient.Builder chatClientBuilder,
                                AttckRagProperties properties) {
        this.classifier = classifier;
        this.retriever = retriever;
        this.chatClient = chatClientBuilder.build();
        this.properties = properties;
    }

    /**
     * 执行 ATT&CK 知识库查询
     * <p>
     * 1. 查询分类 → 2. 混合检索 + 渐进披露 → 3. LLM 生成回答
     */
    public QueryResponse query(QueryRequest request) {
        String question = request.getQuestion();

        // ---- Step 1: 查询分类 ----
        QueryType queryType = classifier.classify(question);
        log.info("Query classified as: {} (depth={})", queryType, queryType.getDisclosureDepth());

        // ---- Step 2: 混合检索 ----
        List<AttckChunk> results = retriever.retrieve(question, queryType, request.getTopK());

        // ---- Step 3: LLM 生成 ----
        String answer = generateAnswer(question, results, queryType);

        // ---- Step 4: 构建响应 ----
        List<SourceItem> sources = results.stream()
                .map(c -> new SourceItem(c.getId(), c.getLevel(), c.getTaId(),
                        c.getTId(), c.getScore()))
                .collect(Collectors.toList());

        return new QueryResponse(
                question,
                queryType.name().toLowerCase(),
                queryType.getDisclosureDepth(),
                answer,
                sources
        );
    }

    /** 调用 LLM 生成自然语言回答 */
    private String generateAnswer(String question, List<AttckChunk> chunks, QueryType queryType) {
        String context = chunks.stream()
                .map(c -> String.format("[%s] TA:%s T:%s %s",
                        c.getLevel(), c.getTaId(), c.getTId(),
                        c.getText().length() > 500
                                ? c.getText().substring(0, 500)
                                : c.getText()))
                .collect(Collectors.joining("\n\n---\n\n"));

        PromptTemplate template = new PromptTemplate("""
                请根据以下 ATT&CK 知识库内容回答问题。
                {context}

                问题: {question}
                """);

        return chatClient.prompt(template.create(Map.of("context", context, "question", question)))
                .call()
                .content();
    }
}
