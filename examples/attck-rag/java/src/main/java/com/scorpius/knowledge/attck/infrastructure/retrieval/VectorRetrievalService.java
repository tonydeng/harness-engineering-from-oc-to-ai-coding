package com.scorpius.knowledge.attck.infrastructure.retrieval;

import com.scorpius.knowledge.attck.domain.model.AttckChunk;
import com.scorpius.knowledge.attck.domain.model.QueryType;
import com.scorpius.knowledge.attck.domain.repository.AttckChunkRepository;
import com.scorpius.knowledge.attck.domain.service.HybridRetrieverService;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.ai.embedding.EmbeddingModel;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.stereotype.Service;

import java.util.*;
import java.util.stream.Collectors;

/**
 * 混合检索实现 — 向量 + 全文双路召回 + RRF 融合 + 渐进披露过滤
 * <p>
 * Scorpius 模式: 基础设施层实现领域服务接口，
 * 组合 VectorStore（Spring AI）+ AttckChunkRepository（JDBC）。
 */
@Service
public class VectorRetrievalService implements HybridRetrieverService {

    private static final Logger log = LoggerFactory.getLogger(VectorRetrievalService.class);

    private static final int DEFAULT_RRF_CONSTANT = 60;
    private static final int DEFAULT_OVER_RETRIEVE = 2;

    private final VectorStore vectorStore;
    private final EmbeddingModel embeddingModel;
    private final AttckChunkRepository chunkRepository;

    public VectorRetrievalService(VectorStore vectorStore,
                                  EmbeddingModel embeddingModel,
                                  AttckChunkRepository chunkRepository) {
        this.vectorStore = vectorStore;
        this.embeddingModel = embeddingModel;
        this.chunkRepository = chunkRepository;
    }

    @Override
    public List<AttckChunk> retrieve(String query, QueryType queryType, int topK) {
        int overRetrieve = topK * DEFAULT_OVER_RETRIEVE;

        // ---- 双路召回 ----
        List<AttckChunk> vecResults = vectorSearch(query, overRetrieve);
        List<AttckChunk> ftsResults = chunkRepository.fullTextSearch(query, overRetrieve);

        log.debug("Vector results: {}, FTS results: {}", vecResults.size(), ftsResults.size());

        // ---- RRF 融合 + 渐进披露过滤 ----
        return fuse(vecResults, ftsResults, topK, queryType.getDisclosureDepth());
    }

    /** 向量检索 — Spring AI VectorStore API */
    private List<AttckChunk> vectorSearch(String query, int k) {
        float[] embedding = embeddingModel.embed(query);

        SearchRequest request = SearchRequest.builder()
                .query(query)
                .topK(k)
                .similarityThreshold(0.3)
                .build();

        return vectorStore.similaritySearch(request).stream()
                .map(doc -> new AttckChunk(
                        doc.getId(), doc.getText(), doc.getMetadata(), 0.0))
                .collect(Collectors.toList());
    }

    /** RRF 融合算法 */
    private List<AttckChunk> fuse(List<AttckChunk> vecResults,
                                  List<AttckChunk> ftsResults,
                                  int topK, int depth) {
        Map<String, Double> rrfScores = new HashMap<>();
        Map<String, AttckChunk> docMap = new HashMap<>();

        // 向量路: rank = index + 1
        for (int i = 0; i < vecResults.size(); i++) {
            AttckChunk doc = vecResults.get(i);
            rrfScores.merge(doc.getId(), 1.0 / (DEFAULT_RRF_CONSTANT + i + 1), Double::sum);
            docMap.putIfAbsent(doc.getId(), doc);
        }

        // 全文路: rank = index + 1
        for (int i = 0; i < ftsResults.size(); i++) {
            AttckChunk doc = ftsResults.get(i);
            rrfScores.merge(doc.getId(), 1.0 / (DEFAULT_RRF_CONSTANT + i + 1), Double::sum);
            docMap.putIfAbsent(doc.getId(), doc);
        }

        // 按得分排序 + 渐进披露过滤
        return rrfScores.entrySet().stream()
                .sorted(Map.Entry.<String, Double>comparingByValue().reversed())
                .map(Map.Entry::getKey)
                .map(docMap::get)
                .filter(doc -> passesDisclosureGate(doc, depth))
                .limit(topK)
                .collect(Collectors.toList());
    }

    /** Progressive Disclosure 门禁: depth=1 tactic / depth=2 tactic+technique / depth=3 all */
    private boolean passesDisclosureGate(AttckChunk doc, int depth) {
        if (depth >= 3) return true;
        String level = doc.getLevel();
        if (level == null) return true;
        return switch (depth) {
            case 1 -> "tactic".equals(level);
            case 2 -> "tactic".equals(level) || "technique".equals(level);
            default -> true;
        };
    }
}
