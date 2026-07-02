package com.scorpius.knowledge.attck;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.context.properties.EnableConfigurationProperties;

/**
 * ATT&CK RAG Spring Boot 启动类
 * <p>
 * Scorpius 模式: 顶层启动类不在任何子包中，
 * 确保 @SpringBootApplication 能扫描到所有子包。
 * <p>
 * 前置条件:
 * - PostgreSQL 16+ with pgvector extension
 * - Ollama 服务 (http://localhost:11434)
 * <p>
 * 启动:
 * mvn spring-boot:run
 * <p>
 * 调用:
 * curl -X POST http://localhost:8000/api/v1/attck/query \
 *   -H "Content-Type: application/json" \
 *   -d '{"question":"T1059 是什么","topK":5}'
 */
@SpringBootApplication
public class AttckKnowledgeApplication {

    public static void main(String[] args) {
        SpringApplication.run(AttckKnowledgeApplication.class, args);
    }
}
