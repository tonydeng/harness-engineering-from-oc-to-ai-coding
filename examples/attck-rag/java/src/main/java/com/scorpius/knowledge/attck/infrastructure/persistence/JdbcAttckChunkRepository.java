package com.scorpius.knowledge.attck.infrastructure.persistence;

import com.scorpius.knowledge.attck.domain.model.AttckChunk;
import com.scorpius.knowledge.attck.domain.repository.AttckChunkRepository;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.jdbc.core.JdbcTemplate;
import org.springframework.jdbc.core.RowMapper;
import org.springframework.stereotype.Repository;

import java.sql.ResultSet;
import java.sql.SQLException;
import java.util.List;
import java.util.Map;

/**
 * ATT&CK 知识块仓储实现 — JDBC 直接查询 pgvector FTS5
 * <p>
 * Scorpius 模式: RepositoryImpl 实现 domain 层的 Repository 接口，
 * 数据访问细节封装在 infrastructure 层。
 */
@Repository
public class JdbcAttckChunkRepository implements AttckChunkRepository {

    private static final String FTS_SQL = """
        SELECT id, chunk_text, metadata::text,
               ts_rank(to_tsvector('simple', chunk_text),
                       plainto_tsquery('simple', ?)) AS score
        FROM attck_chunks
        WHERE to_tsvector('simple', chunk_text) @@ plainto_tsquery('simple', ?)
        ORDER BY score DESC
        LIMIT ?
        """;

    private final JdbcTemplate jdbcTemplate;
    private final ObjectMapper objectMapper;

    public JdbcAttckChunkRepository(JdbcTemplate jdbcTemplate, ObjectMapper objectMapper) {
        this.jdbcTemplate = jdbcTemplate;
        this.objectMapper = objectMapper;
    }

    @Override
    public List<AttckChunk> fullTextSearch(String query, int limit) {
        return jdbcTemplate.query(FTS_SQL, rowMapper(), query, query, limit);
    }

    private RowMapper<AttckChunk> rowMapper() {
        return (rs, rowNum) -> {
            String id = rs.getString("id");
            String text = rs.getString("chunk_text");
            Map<String, Object> metadata = parseMetadata(rs.getString("metadata"));
            double score = rs.getDouble("score");
            return new AttckChunk(id, text, metadata, score);
        };
    }

    @SuppressWarnings("unchecked")
    private Map<String, Object> parseMetadata(String json) {
        try {
            return objectMapper.readValue(json, Map.class);
        } catch (Exception e) {
            return Map.of();
        }
    }
}
