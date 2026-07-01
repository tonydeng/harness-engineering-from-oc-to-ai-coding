# ATT&CK RAG — Python 实现

ATT&CK 本地 RAG 的 Python 实现，零外部服务依赖（仅需 Ollama）。

## 文件速览

| 文件 | 角色 | 一句话 |
|------|------|--------|
| `config.py` | 配置 | 环境变量驱动的 `AttckRagConfig` 数据类 |
| `index_builder.py` | 索引构建 | 解析 mdBook → embedding → 写入 SQLite 向量库 |
| `query.py` | 查询 CLI | 混合检索 → 模型降级 → 质量度量 |
| `setup.py` | 一键启动 | 环境检查 → 装依赖 → 拉模型 → 建索引 → 进入查询 |
| `install_env.py` | 完整环境安装 | 装 Docker PostgreSQL + Ollama + Python venv（跨平台） |
| `download_models.py` | 本地模型下载 | 从 Hugging Face Hub 下载 embedding 模型到 `models/` |
| `__init__.py` | 包标记 | 仅一行注释 |

### 依赖

见 `../config/requirements.txt`：

```
sentence-transformers
sqlite-vec
httpx
numpy
```

## 本地 Embedding 模型

`index_builder.py` 和 `query.py` 使用 **sentence-transformers** 加载 `BAAI/bge-small-zh-v1.5` 生成 embedding。默认行为是从 Hugging Face Hub 自动下载并缓存到 `~/.cache/huggingface/hub/`。

### 为什么建议用本地模型

- **完全离线**：首次下载后无需任何网络访问
- **路径可控**：显式存储在项目 `models/` 目录下，不依赖系统缓存
- **环境隔离**：换机器 / 重装系统不需要重新下载
- **内网友好**：只需一次下载，后续可在无外网环境运行

### 使用方式

```bash
# 1. 首次：下载模型到本地
python download_models.py

# 2. 后续：设环境变量后完全离线运行
EMBED_MODEL_PATH=./models/bge-small-zh-v1.5 python query.py "T1059 是什么"
EMBED_MODEL_PATH=./models/bge-small-zh-v1.5 python index_builder.py --src /path/to/src
```

### 工作原理

```text
┌─────────────────────────────────────────────────┐
│ download_models.py（首次，需联网）                 │
│                                                   │
│ SentenceTransformer("BAAI/bge-small-zh-v1.5")     │
│   ↓ model.save()                                  │
│ models/bge-small-zh-v1.5/                         │
│     ├── config.json    ← PyTorch 模型配置          │
│     ├── pytorch_model.bin  ← 权重文件 (~80MB)      │
│     ├── tokenizer.json ← 分词器                    │
│     └── ...                                       │
└─────────────────────────────────────────────────┘
                        │
           ┌────────────┴────────────┐
           ▼                         ▼
   EMBED_MODEL_PATH env var    config.py 默认值
           │                         │
           └────────┬────────────────┘
                    ▼
    SentenceTransformer(local_path)   ← 完全本地加载，不联网
```

### 目录结构

```
python/
├── models/
│   └── bge-small-zh-v1.5/       ← 本地模型文件（.gitignore 建议忽略）
│       ├── config.json
│       ├── pytorch_model.bin
│       └── ...
├── download_models.py           ← 下载脚本
├── query.py                     ← 自动读取 EMBED_MODEL_PATH
└── index_builder.py
```

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `EMBED_MODEL_PATH` | 本地 embedding 模型路径 | `./models/bge-small-zh-v1.5` |

> 不设该变量时，`index_builder.py` 和 `query.py` 回退到 Hugging Face Hub 自动下载（兼容原行为）。

## config.py — 配置模块

通过环境变量覆盖默认值，所有 Python 模块共享同一 `AttckRagConfig` 实例：

```bash
# 常用环境变量
ATTCK_SRC          — attck-knowledge 源码路径
DB_PATH            — SQLite 向量库路径（默认 ../attck_vec.db）
EMBED_MODEL_PATH   — 本地 embedding 模型路径（默认 Hugging Face Hub 自动下载）
OLLAMA_HOST        — Ollama 地址（默认 http://localhost:11434）
LLM_EXACT          — 精确 TID 查询模型（默认 qwen2.5）
LLM_FACTUAL        — 事实查询模型（默认 qwen2.5）
LLM_ANALYSIS       — 分析推理模型（默认 qwen2.5）
LOG_LEVEL          — 日志级别（默认 INFO，查问题时设 DEBUG）
```

## index_builder.py — 索引构建

将 [attck-knowledge](https://github.com/tonydeng/attck-knowledge) mdBook 源码解析为结构化知识块，用 sentence-transformers 生成 embedding 后存入 sqlite-vec。

```bash
python index_builder.py --src /path/to/attck-knowledge/src                        # 默认输出 attck_vec.db
python index_builder.py --src /path/to/attck-knowledge/src --db /tmp/my_index.db  # 指定输出路径
```

**工作流**：

1. 按 mdBook 目录结构逐层扫描（TA → T → sub_technique），提取战术/技术 ID 作为元数据
2. 加载 `BAAI/bge-small-zh-v1.5` embedding 模型
3. 分批编码（batch_size=32），通过 sqlite-vec `serialize_float32` 写入 BLOB
4. 若缺少 sentence-transformers 依赖，自动降级为 JSON 导出

## query.py — 交互式查询 CLI

核心查询引擎，演示完整 RAG 流水线。

```bash
# 交互模式
python query.py

# 单次查询
python query.py "T1059 是什么"
python query.py "TA0001 包含哪些技术"
python query.py "什么是命令注入"
```

**流水线**：

```text
用户输入
  ↓
① 查询分类（RuleQueryClassifier）
   ├─ EXACT    — TID 精确匹配     → depth=1（仅目标文档）
   ├─ FACTUAL  — 事实关键词       → depth=2（战术+技术）
   └─ ANALYSIS — 推理/分析（默认） → depth=3（全量）
  ↓
② 混合检索（Hybrid Search）
   ├─ 向量路：sentence-transformers + sqlite-vec (L2 距离)
   └─ 全文路：SQLite FTS5（字符级分词）
       ↓ RRF 融合
③ 渐进披露（Progressive Disclosure）
   └─ 按 depth 过滤层级
  ↓
④ 模型降级链（Model Cascade）
   └─ query_type → LLM 选择（默认全用 qwen2.5）
  ↓
⑤ 质量度量（Quality Metrics）
   └─ TID 命中率、幻觉检测
```

**日志级别**：默认 INFO 只输出关键流程信息。设 `LOG_LEVEL=DEBUG` 可见模型路由、查询分类等内部细节：

```bash
LOG_LEVEL=DEBUG python query.py "T1059"
```

## setup.py — 一键启动脚本

面向终端用户的最简入口，自动完成全部启动步骤：

```bash
python setup.py --src /path/to/attck-knowledge/src

# 跳过查询模式（仅建索引）
python setup.py --src /path/to/attck-knowledge/src --no-query

# 指定数据库路径
python setup.py --src /path/to/attck-knowledge/src --db /tmp/my_index.db
```

**执行步骤**：
1. 检查 Python 版本（需 3.10+）
2. `pip install -r config/requirements.txt`
3. 检测 Ollama 服务是否运行
4. 拉取 `qwen2.5:latest`（如本地不存在）
5. 确定 ATT&CK 知识库源码路径（支持 `ATTCK_SRC` 环境变量 / `--src` 参数 / 交互输入）
6. 如索引未构建则调用 `index_builder.py` 创建
7. 进入交互查询模式（调用 `query.py`）

## install_env.py — 完整环境安装

面向从零开始的环境搭建，覆盖 Docker PostgreSQL + Ollama + Python venv 全链路：

```bash
# 全量安装
python install_env.py

# 仅安装 Ollama + 拉模型
python install_env.py --ollama-only

# 仅安装 PostgreSQL + pgvector
python install_env.py --db-only

# 指定 PostgreSQL 端口和密码
python install_env.py --pg-port 15432 --pg-pass mysecret
```

**安装内容**：
- Docker PostgreSQL 16 + pgvector 扩展
- Ollama 服务 + qwen2.5 模型
- `.venv` 虚拟环境 + pip 依赖
- 最终输出环境健康检查报告

## 架构概要

```text
┌────────────────────────────────────────────────────┐
│                    setup.py                         │
│  ① 环境检查 → ② 装依赖 → ③ 拉模型 → ④ 建索引 → ⑤ 查询 │
└──────────────────────┬─────────────────────────────┘
                       │
            ┌──────────┴──────────┐
            ▼                     ▼
   ┌────────────────┐   ┌──────────────────┐
   │ index_builder   │   │    query.py       │
   │                 │   │                   │
   │ mdBook 解析     │   │ 混合检索          │
   │ embedding 编码  │   │ 模型降级          │
   │ sqlite-vec 存储 │   │ 渐进披露          │
   │                 │   │ 质量度量          │
   └────────┬───────┘   └────────┬─────────┘
            │                    │
            ▼                    ▼
   ┌──────────────────────────────────────────────┐
   │          SQLite (sqlite-vec + FTS5)           │
   │          attck_vec.db                         │
   └──────────────────────────────────────────────┘
```

## 快速上手

```bash
# 1. 安装依赖
pip install -r ../config/requirements.txt

# 2. （可选）下载 embedding 模型到本地，后续可离线运行
python download_models.py

# 3. 克隆知识库
git clone https://github.com/tonydeng/attck-knowledge /path/to/attck-knowledge

# 4. 构建索引（如已下载本地模型）
EMBED_MODEL_PATH=./models/bge-small-zh-v1.5 python index_builder.py --src /path/to/attck-knowledge/src

# 5. 开始查询
EMBED_MODEL_PATH=./models/bge-small-zh-v1.5 python query.py
```

或者直接用 `setup.py` 一键完成 2-5 步（本地模型需先运行 `python download_models.py`）：

```bash
python setup.py --src /path/to/attck-knowledge/src
```
