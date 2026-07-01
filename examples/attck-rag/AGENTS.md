# ATT&CK RAG — 智能体工作指南

## 一句话说清

**这是本书第 7 章案例研究的配套示例项目，不是书籍正文。** 目录包含 Python 和 Java 两套 RAG 实现，服务于 `examples/attck-rag/` 路径引用。不要修改 `src/` 下的书籍正文。

## 目录结构

```
examples/attck-rag/
├── README.md                  ← 使用说明（启动前先看它）
├── AGENTS.md                  ← 本文件 — AI 智能体操作约束
├── config/                    ← 只读配置参考，勿修改
│   ├── requirements.txt       ← Python 依赖
│   ├── schema.sql             ← pgvector 建表 SQL
│   ├── mdbook-parser.json     ← 元数据字段设计参考
│   └── progressive-disclosure.json  ← 渐进披露策略配置
├── python/                    ← Python 实现（可直接运行）
│   ├── README.md              ← Python 使用说明
│   ├── config.py              ← Python 配置
│   ├── index_builder.py       ← 索引构建
│   ├── query.py               ← 交互式查询
│   ├── setup.py               ← 一键安装脚本
│   ├── install_env.py         ← 环境安装助手
│   └── download_models.py     ← 本地 Embedding 模型下载
├── java/                      ← Spring AI 实现（需 PostgreSQL）
│   ├── README.md              ← Java 使用说明
│   ├── install_env.py         ← 环境准备脚本
│   ├── setup.py               ← 一键启动脚本
│   ├── pom.xml                ← Maven 构建
    └── src/main/
        ├── java/com/scorpius/knowledge/attck/
        │   ├── AttckKnowledgeApplication.java
        │   ├── api/rest/
        │   │   ├── QueryController.java
        │   │   └── ApiResponse.java
        │   ├── application/
        │   │   ├── dto/
        │   │   │   ├── QueryRequest.java
        │   │   │   └── QueryResponse.java
        │   │   └── service/
        │   │       ├── AttckQueryAppService.java
        │   │       └── AttckRagProperties.java
        │   ├── domain/
        │   │   ├── model/
        │   │   │   ├── AttckChunk.java
        │   │   │   └── QueryType.java
        │   │   ├── repository/
        │   │   │   └── AttckChunkRepository.java
        │   │   └── service/
        │   │       ├── QueryClassifierService.java
        │   │       └── HybridRetrieverService.java
        │   └── infrastructure/
        │       ├── persistence/
        │       │   └── JdbcAttckChunkRepository.java
        │       └── retrieval/
        │           ├── VectorRetrievalService.java
        │           └── RuleQueryClassifier.java
        └── resources/
            └── application.yml
```

## 运行命令

```bash
# Python 版（一键启动）
cd examples/attck-rag
python python/setup.py --src /path/to/attck-knowledge/src

# Java 版（需先建 PostgreSQL 数据库）
cd examples/attck-rag/java
mvn compile           # 仅编译验证
mvn spring-boot:run   # 编译 + 启动（需数据库 + Ollama）
```

## 代码规范

### Scorpius DDD 四层架构（Java）

| 层 | 包 | 规则 |
|----|-----|------|
| **api/rest** | `api.rest` | 只放 @RestController 和 ApiResponse；不写业务逻辑 |
| **application** | `application` | DTO（不可包含领域模型）+ AppService（编排用例，不含业务规则） |
| **domain** | `domain` | 纯 POJO + 接口 + 枚举；零框架注解（除 @Override），零基础设施依赖 |
| **infrastructure** | `infrastructure` | 实现 domain 接口；可以依赖 Spring AI / JDBC / 框架注解 |
| **启动类** | 根包 `attck` | @SpringBootApplication 置于所有子包之上 |

### 依赖注入

- 构造器注入（推荐）或 `@Autowired` 字段注入
- 禁止 `@Value` 注解；全部通过 `@ConfigurationProperties` 绑定
- 禁止 `@PostConstruct` 初始化；使用 `ApplicationRunner` 或 `InitializingBean`

### API 规范

- 路径前缀：`/api/v1/`
- 响应统一包装：`ApiResponse<T>`（scuccess / message / data / errorCode / timestamp）
- POST 请求体使用 `@Valid` 校验，DTO 字段使用 `jakarta.validation` 注解

## 最容易翻车的地方

### 1. Spring AI 1.1.8 与旧版 API 不兼容

| 旧 API（0.x/1.0 M 版） | 新 API（1.1.8+） |
|------------------------|------------------|
| `spring-ai-ollama-spring-boot-starter` | `spring-ai-starter-model-ollama` |
| `spring-ai-pgvector-store-spring-boot-starter` | `spring-ai-starter-vector-store-pgvector` |
| `SearchRequest.query(String)` | `SearchRequest.builder().query(String).build()` |
| `Document.getContent()` | `Document.getText()` |
| `spring-ai-openai-spring-boot-starter` | `spring-ai-starter-model-openai` |

### 2. Maven 仓库

Spring AI 1.1.8 已发布到 **Maven Central**，不需要配置 `https://repo.spring.io/milestone` 仓库。pom.xml 只配置 central 即可。

### 3. PostgreSQL

- 需要 PostgreSQL 16+ 并启用 pgvector 扩展
- 建表 SQL 在 `config/schema.sql`（`CREATE EXTENSION vector` + 建表 + IVFFlat 索引 + GIN 全文索引）
- 启动前必须手动 `createdb attck_rag` 并执行 schema.sql

### 4. Python 索引构建

Python `index_builder.py` 目前仅支持 SQLite 输出。Java 版需要独立的数据加载机制——`index_builder.py` 中的 `parse_mdbook()` 解析器逻辑可与 Java 共享，但写入目标不同。修改了解析逻辑后需要同步更新 Java 的 `JdbcAttckChunkRepository`。

### 5. 配置文件映射

`application.yml` 中 `attck.rag.*` 绑定到 `AttckRagProperties`，路径前缀 `attck` 前不要加 `spring`。Ollama 配置走 `spring.ai.openai.*`（OpenAI-compatible client 协议），不通过 `spring.ai.ollama.*`。

## 验证清单

修改代码后必须验证：

```bash
# 1. Java 编译
cd examples/attck-rag/java
mvn compile -q       # 无 Error 即通过

# 2. 链接检查（修改了 README 或引用）
cd /path/to/repo/root
find src -name '*.md' -exec grep -n '\](' {} + | grep '\.md)'

# 3. Python 语法（修改了 Python 代码）
python -m py_compile examples/attck-rag/python/index_builder.py
python -m py_compile examples/attck-rag/python/query.py
```

## 修改原则

- **README.md**：同步更新 Java 目录结构、构建命令和依赖版本
- **AGENTS.md**：同步更新目录树、API 变更和约束条件
- **Java 代码**：遵循 Scorpius DDD 四层架构，新增类必须归属于正确层
- **Python 代码**：依赖全部声明在 `requirements.txt` 中，不引入隐式依赖
- **config/**：配置参考文件与 Java/Python 代码中的默认值一致；改了代码就改 config
