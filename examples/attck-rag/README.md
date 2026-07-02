# ATT&CK RAG — 本地 RAG 知识库示例

基于 [attck-knowledge](https://github.com/tonydeng/attck-knowledge)（MITRE ATT&CK 中文知识库）的本地 RAG 问答系统完整示例，演示书籍第 7 章案例中讨论的完整技术方案。

提供 **Python**（可直接运行）和 **Java/Spring AI**（Scorpius DDD 风格，需 PostgreSQL）两种实现。

## 文档结构

```
examples/attck-rag/
├── README.md                              # 本文件 — 使用说明
├── AGENTS.md                              # AI 智能体操作指南（Agent 在此目录下工作时的行为约束）
├── config/                                # 配置与参考文件
│   ├── requirements.txt                   # Python 依赖清单
│   ├── schema.sql                         # pgvector 数据库表结构（参考）
│   ├── mdbook-parser.json                 # 元数据字段设计（参考）
│   └── progressive-disclosure.json         # 渐进披露配置（参考）
├── python/                                # Python 实现（可直接运行，依赖见 requirements.txt）
│   ├── __init__.py
│   ├── README.md                          # Python 实现使用说明
│   ├── config.py                          # 配置模块（环境变量驱动）
│   ├── index_builder.py                   # 构建索引：解析 mdBook → embedding → SQLite
│   ├── query.py                           # 交互式查询：混合检索 → 模型降级 → 质量度量
│   ├── setup.py                           # 一键设置（跨平台，自动安装依赖 + 拉模型 + 建索引）
│   ├── install_env.py                     # 完整环境安装（跨平台）
│   └── download_models.py                 # 下载本地 Embedding 模型（HF Hub → models/）
├── java/                                  # Spring AI 实现（Scorpius DDD 风格，需 PostgreSQL）
│   ├── README.md                          # Java 实现使用说明
│   ├── install_env.py                     # 环境准备脚本（JDK/Maven/DB/Ollama 自动检测）
│   ├── setup.py                           # 一键启动脚本（编译+启动 + 可选仅建库）
│   ├── pom.xml                            # Maven 构建（Spring Boot 3.5.15 + Spring AI 1.1.8）
│   └── src/main/
        ├── java/com/scorpius/knowledge/attck/
        │   ├── AttckKnowledgeApplication.java          # Spring Boot 启动类
        │   ├── api/rest/
        │   │   ├── QueryController.java                # REST 接口 /api/v1/attck/query
        │   │   └── ApiResponse.java                    # 统一响应包装
        │   ├── application/
        │   │   ├── dto/
        │   │   │   ├── QueryRequest.java               # 查询请求 DTO
        │   │   │   └── QueryResponse.java              # 查询响应 DTO（含 SourceItem）
        │   │   └── service/
        │   │       ├── AttckQueryAppService.java       # 应用服务：分类 → 检索 → 生成
        │   │       └── AttckRagProperties.java         # @ConfigurationProperties 配置绑定
        │   ├── domain/
        │   │   ├── model/
        │   │   │   ├── AttckChunk.java                 # 知识块领域模型
        │   │   │   └── QueryType.java                  # 查询类型枚举（EXACT/FACTUAL/ANALYSIS）
        │   │   ├── repository/
        │   │   │   └── AttckChunkRepository.java       # 仓储接口（全文检索契约）
        │   │   └── service/
        │   │       ├── QueryClassifierService.java     # 查询分类领域服务接口
        │   │       └── HybridRetrieverService.java     # 混合检索领域服务接口
        │   └── infrastructure/
        │       ├── persistence/
        │       │   └── JdbcAttckChunkRepository.java   # JDBC 实现：pgvector FTS5 全文检索
        │       └── retrieval/
        │           ├── VectorRetrievalService.java     # 混合检索：向量 + 全文 + RRF + 渐进披露
        │           └── RuleQueryClassifier.java        # 规则分类器（TID 匹配 / 关键词判断）
        └── resources/
            └── application.yml            # Spring Boot 配置（PostgreSQL + Ollama）
```

## 前置条件

| 组件 | Python 版 | Java 版 |
|------|-----------|---------|
| Python 3.10+ | 必需 | — |
| JDK 17+ | — | 必需 |
| Maven 3.9+ | — | 必需 |
| PostgreSQL 16+ with pgvector | — | 必需（`schema.sql` 建表） |
| Ollama | 必需 | 必需 |
| attck-knowledge | `git clone https://github.com/tonydeng/attck-knowledge` | 同上 |
| 16 GB RAM | 推荐 | 推荐 |

## 快速开始

### Python 版（一键运行）

```bash
cd examples/attck-rag
python python/setup.py --src /path/to/attck-knowledge/src
```

脚本自动完成：检查运行环境 → 安装 pip 依赖 → 拉取 Ollama 模型 → 构建 SQLite 向量库 → 进入交互查询。

### Java 版（Spring Boot + PostgreSQL，需先初始化数据库）

```bash
# 1. 建库 + 建表
createdb attck_rag
psql -d attck_rag -f config/schema.sql

# 2. 导入数据至 PostgreSQL（Python 版 SQLite 数据迁移脚本待实现，
#    可参照 schema.sql 表结构自行编写 ETL 脚本）

# 3. 修改 application.yml 中的数据库连接 + 数据源路径

# 4. 编译并启动
cd java
mvn spring-boot:run

# 5. 调用 REST API
curl -X POST http://localhost:8000/api/v1/attck/query \
  -H "Content-Type: application/json" \
  -d '{"question":"T1059 是什么","topK":5}'
```

## 核心设计

该示例演示了书籍第 7 章案例中讨论的 5 个核心组件：

### 1. mdBook 层级解析
`index_builder.py` 按 mdBook 的目录结构解析 ATT&CK 知识库，保留 TA→T→sub 的三级层次，注入结构化元数据。Java 版通过 `AttckChunk` 领域模型承载相同元数据。

### 2. 混合检索（Hybrid Search）
双路召回（向量语义相似度 + PostgreSQL FTS5 全文检索）→ **RRF（Reciprocal Rank Fusion）** 算法融合两路得分。

- Python 版：`query.py` 使用 sentence-transformers + sqlite-vec + FTS5
- Java 版：`VectorRetrievalService` 使用 Spring AI VectorStore + JdbcTemplate

### 3. 模型降级链（Model Cascade）
查询按类型路由到不同大小的模型：

| 查询类型 | 触发条件 | 模型（默认） | 披露深度 |
|----------|---------|-------------|---------|
| EXACT | TID 精确匹配（如 `T1059`） | qwen2.5:latest | level 1 — 目标文档 |
| FACTUAL | 事实性关键词（如"是什么"） | qwen2.5:latest | level 2 — 战术+技术 |
| ANALYSIS | 推理/分析（默认） | qwen2.5:latest | level 3 — 全量 |

> 模型路由通过环境变量 `LLM_EXACT`、`LLM_FACTUAL`、`LLM_ANALYSIS` 可单独配置，支持按查询类型使用不同模型。

Java 版通过 `RuleQueryClassifier` 实现分类规则，`QueryType` 枚举携带披露深度和默认模型配置。

### 4. 渐进披露（Progressive Disclosure）
按查询类型控制上下文的披露深度：
- `EXACT`（depth=1）：只返回 tactic 层级文档
- `FACTUAL`（depth=2）：返回 tactic + technique
- `ANALYSIS`（depth=3）：全量 Top-5 + 战术聚合

### 5. 质量度量（Quality Metrics）
Python `query.py` 每次查询后自动报告：TID 引用列表、命中率、幻觉检测。Java 版 `QueryResponse.SourceItem` 结构携带每个来源项的得分和层级信息。

## Java 架构说明（Scorpius DDD）

Java 实现遵循 **Scorpius DDD** 四层架构：

| 层 | 包路径 | 职责 |
|----|--------|------|
| **api/rest** | `com.scorpius.knowledge.attck.api.rest` | REST 控制器 + 统一 ApiResponse |
| **application** | `com.scorpius.knowledge.attck.application` | DTO + 应用服务编排（AttckQueryAppService） |
| **domain** | `com.scorpius.knowledge.attck.domain` | 纯业务模型（AttckChunk, QueryType）+ 接口契约 |
| **infrastructure** | `com.scorpius.knowledge.attck.infrastructure` | JDBC 持久化 + Spring AI 集成实现 |

### 技术栈

| 组件 | 版本 | 说明 |
|------|------|------|
| Spring Boot | 3.5.15 | 基础框架 |
| Spring AI | 1.1.8 | OpenAI-compatible client → Ollama |
| pgvector | 0.7.x | 向量存储 + IVFFlat 索引 |
| PostgreSQL | 16+ | 关系数据库 + FTS5 全文检索 |

### Spring AI 1.1.x API 注意事项

- 依赖 artifact 已重命名：`spring-ai-starter-model-ollama` 而非 `spring-ai-ollama-spring-boot-starter`
- `SearchRequest` 使用 builder 模式：`SearchRequest.builder().query(...).topK(...).build()`
- `Document.getContent()` 已变更为 `Document.getText()`
- Spring AI 1.1.8 已发布到 Maven Central，无需配置 milestone 仓库

## 配置

### Python 版

通过环境变量或编辑 `python/config.py`：

```
ATTCK_SRC   — attck-knowledge 源码路径
DB_PATH     — 向量库路径（默认 attck_vec.db）
OLLAMA_HOST — Ollama 地址（默认 http://localhost:11434）
```

### Java 版

编辑 `java/src/main/resources/application.yml`：

```yaml
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/attck_rag
    username: postgres
    password: postgres
  ai:
    openai:
      base-url: http://localhost:11434/v1       # Ollama 端点
      api-key: ollama                            # Ollama API key 占位
      chat:
        options:
          model: qwen2.5:7b-instruct-q4_K_M
          temperature: 0.1
      embedding:
        options:
          model: nomic-embed-text                # Ollama 支持的 embed 模型
  vectorstore:
    pgvector:
      index-type: IVFFlat
      distance-type: COSINE_DISTANCE
      dimensions: 768
attck:
  rag:
    models:
      exact: qwen2.5:3b-instruct-q4_K_M
      factual: qwen2.5:3b-instruct-q4_K_M
      analysis: qwen2.5:7b-instruct-q4_K_M
    retrieval:
      top-k: 5
      similarity-threshold: 0.3
      rrf-constant: 60
      over-retrieve-factor: 2
    source-path: /path/to/attck-knowledge/src
```

## 故障排除

| 问题 | 原因 | 解决 |
|------|------|------|
| `sqlite-vec 扩展未加载`（Python） | 未安装 sqlite-vec | `pip install -r config/requirements.txt`，或忽略（仅降级为全文检索） |
| `Ollama 调用失败` | Ollama 未运行 | 启动 Ollama 服务：`ollama serve` |
| `索引文件不存在` | 未建索引 | 先运行 `python/index_builder.py --src <path>` |
| `模型未找到` | 未拉取模型 | `ollama pull qwen2.5:latest` |
| `org.postgresql 连接失败`（Java） | PostgreSQL 未运行或配置错误 | 检查 `application.yml` 数据库连接 |
| `Could not find artifact ...:1.1.8`（Java） | Maven Central 尚未同步 | 确认 `pom.xml` 使用正确的 starter artifact 名 |
| 编译报错 `getContent()` / `SearchRequest.query()` | Spring AI 版本不匹配 | 参考"Spring AI 1.1.x API 注意事项"更新代码 |
