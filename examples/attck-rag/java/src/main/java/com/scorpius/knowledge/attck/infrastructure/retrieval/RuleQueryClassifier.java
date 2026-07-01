package com.scorpius.knowledge.attck.infrastructure.retrieval;

import com.scorpius.knowledge.attck.domain.model.QueryType;
import com.scorpius.knowledge.attck.domain.service.QueryClassifierService;

import org.springframework.stereotype.Service;

import java.util.Set;
import java.util.regex.Pattern;

/**
 * 查询分类器实现 — 按规则将用户问题分类
 * <p>
 * Scorpius 模式: 简单规则匹配，生产环境可替换为 ML 分类器。
 */
@Service
public class RuleQueryClassifier implements QueryClassifierService {

    private static final Pattern EXACT_PATTERN =
            Pattern.compile("(T\\d{4}(\\.\\d{3})?|TA\\d{4})", Pattern.CASE_INSENSITIVE);

    private static final Set<String> FACTUAL_KEYWORDS = Set.of(
            "是什么", "定义", "含义", "编号", "包括哪些", "有哪些", "属于"
    );

    @Override
    public QueryType classify(String query) {
        if (query == null || query.isBlank()) {
            return QueryType.ANALYSIS;
        }
        if (EXACT_PATTERN.matcher(query).find()) {
            return QueryType.EXACT;
        }
        for (String kw : FACTUAL_KEYWORDS) {
            if (query.contains(kw)) return QueryType.FACTUAL;
        }
        return QueryType.ANALYSIS;
    }
}
