---
name: attck-rag
description: 在需要对 MITRE ATT&CK 知识库进行本地 RAG 查询时使用——触发词包括 TID（如 T1059/T1566）、TTP 编号、战术英文名（Reconnaissance/Execution）、中文战术名（侦察/执行）、技术描述（如 DLL 侧加载、Scripting）、攻击链分析。覆盖精确 TID 查询、事实性问答、跨技术分析推理三类场景。不适用于非 ATT&CK 领域的通用问答。English triggers: ATT&CK query, TTP lookup, technique search, kill chain analysis, mitigations, detections.
---

# ATT&CK RAG — 本地知识库查询

基于 [attck-knowledge](https://github.com/tonydeng/attck-knowledge)（MITRE ATT&CK 中文知识库）的 RAG 流水线，让 Agent 能用本地 sqlite-vec 向量库精确回答 ATT&CK 相关问题。

## 核心流程

```
用户提问（含 TID/战术/技术描述）
  ↓
① 查询分类（RuleQueryClassifier）
   ├─ EXACT    — TID 精确匹配     → 仅目标文档
   ├─ FACTUAL  — 事实关键词       → 战术+技术
   └─ ANALYSIS — 推理/分析（默认） → 全量检索
   │
   └─ 🔴 CHECKPOINT: 分类结果正确？
       ├─ 是 → 按 query_type 限定检索范围
       └─ 否（如 TID 漏匹配）→ 强制走 ANALYSIS 兜底
  ↓
② 混合检索（Hybrid Search）
   ├─ 向量路：sentence-transformers + sqlite-vec (L2 距离)
   └─ 全文路：SQLite FTS5（字符级分词）
       ↓ RRF（Reciprocal Rank Fusion）融合
   │
   └─ 🔴 CHECKPOINT: 检索返回结果数 > 0？
       ├─ 是 → 进入渐进披露
       └─ 否 → 放宽检索（扩 Top-K / 降相似度阈值 / 纯 FTS5 重试）
  ↓
③ 渐进披露（Progressive Disclosure）
   └─ 按 depth 过滤层级：level_1/level_2/level_3
   │
   └─ 🔴 CHECKPOINT: 过滤后仍有结果？
       ├─ 是 → 组装 prompt 模板
       └─ 否 → 降级到全库 Top-3 并追加"检索结果有限，以下为近似内容"
  ↓
④ Agent 回答生成
   └─ 将检索结果 + query_type 模板注入当前上下文
       Agent 使用自身模型能力生成回答
  ↓
⑤ 质量度量（Quality Metrics）
   └─ TID 引用列表、命中率、幻觉检测
```

## Agent 操作步骤

收到 ATT&CK 相关提问后，按以下步骤执行：

```
Step 1: 判断是否为 ATT&CK 类问题
  ├─ 含 TID/战术名/技术描述 → 继续
  └─ 不是 ATT&CK 问题 → 跳过本 skill，用自身能力回答

Step 2: 运行检索命令（得先确认数据库存在）
  ├─ 检查 attck_vec.db 是否存在（默认在当前 SKILL 目录下）
  ├─ 不存在 → 先运行 --build（指向 attck-knowledge 的 src/）
  └─ 存在 → python scripts/rag.py --query "<用户问题>" --json
      ⚠️ 工作目录: 必须在 SKILL 目录下执行（即 SKILL.md 所在目录）

Step 3: 解析 JSON 输出
  └─ query_type: "exact" | "factual" | "analysis"
  └─ depth: 1 | 2 | 3
  └─ results[]: 每个条目的 text 字段为知识原文
  └─ 引用字段: ta_id (战术编号), t_id (技术编号), level (层级)

Step 4: 将结果注入上下文，生成回答
  ├─ exact → 直接给出 TID 定义 + 战术归属，引用 t_id/ta_id
  ├─ factual → 逐条列举各技术及用途，每项引用 t_id
  └─ analysis → 对比分析，跨 t_id 引用，尽量给出检测建议

Step 5: 在回答末尾标注来源
  └─ "来源: attck-knowledge v2025.x"

Step 6: 修改后回归验证（仅修改了索引或查询逻辑后执行）
  ├─ 运行 python scripts/run_tests.py
  ├─ 确认全部 100 条测试 PASS（0 FAIL, 0 CRASH）
  ├─ 如有失败 → 根据 test-report.md 定位根因并修复
  └─ 全部通过 → 可提交变更
```

> **🔴 CHECKPOINT**: 如果 `rag.py` 报错（如路径错误、依赖缺失），请查阅下方「常见错误」表定位修复。修复后重试步骤 2。

## 使用方式

### 1. 构建索引

```bash
# 克隆 ATT&CK 中文知识库
git clone https://github.com/tonydeng/attck-knowledge <path>

# 使用本 skill 脚本构建索引
python scripts/rag.py --build --src <attck-knowledge/src>
```

### 2. 查询

```bash
# 在 SKILL 目录下运行（必须确保工作目录正确）
python scripts/rag.py --query "T1059 是什么"

# JSON 格式输出（供 Agent 程序化解析注入上下文）
python scripts/rag.py --query "T1059 是什么" --json
```

### 3. Agent 回答生成规则

Agent 使用 `--json` 模式获取结构化检索结果，**按以下规则转化为自然语言回答**：

```
1. 运行: python scripts/rag.py --query "<用户问题>" --json
2. 解析 JSON 输出:
   - results[].text     → 知识库原文（注入上下文作为参考）
   - results[].ta_id    → 战术编号（引用来源）
   - results[].t_id     → 技术编号
   - query_type         → 用于选择回答风格（exact简短/factual列举/analysis对比）
3. 将 text 内容注入当前对话上下文
4. 根据 query_type 选择回答风格:
   - exact:   直接给出 TID 定义 + 战术归属（引用 t_id/ta_id）
   - factual: 逐条列举各技术及其用途（引用每个 t_id）
   - analysis: 对比分析 + 检测建议（跨 t_id 引用）
5. 在回答中标注知识库来源（attck-knowledge）
```

### 4. 回归测试验证

修改索引构建、查询逻辑或配置参数后，运行回归测试确认无回归：

```bash
# 运行全部 100 条测试用例
python scripts/run_tests.py

# 预期输出：All 100 tests: 100 PASS, 0 FAIL, 0 CRASH
# 失败时查看 test-report.md 定位根因
```

测试用例按类型覆盖：

| 类型 | 数量 | 覆盖范围 |
|------|:----:|---------|
| EXACT | 30 | TID/TA 精确匹配、含子编号、同 TID 多结果 |
| FACTUAL | 25 | 战术技术列举、是什么/有哪些/包括哪些 |
| ANALYSIS | 20 | 跨技术对比、检测建议、攻击链分析 |
| BOUNDARY | 25 | 空输入/乱码/不存在 TID/SQL 注入/超长输入等 |

> **原则**：先测试后修改（确保基线通过），修改后再次测试（确认无回归）。

### 5. 查询输出示例（JSON）

实际 `rag.py --json` 输出格式如下（Agent 应据此解析）：

```json
{
  "query": "T1059 是什么",
  "query_type": "exact",
  "depth": 1,
  "results": [
    {
      "level": "technique",
      "ta_id": "TA0002",
      "t_id": "T1059",
      "text": "...（知识块原文，由 Agent 注入上下文后生成回答）"
    }
  ],
  "quality": {
    "ground_truth_tids": ["T1059"],
    "ground_truth_tactics": ["TA0002"],
    "chunk_count": 1,
    "levels": ["technique"],
    "query_type": "exact",
    "verification_note": "Agent 需确保回答中引用的 TID 均在此 ground_truth 列表中；不在列表中的 TID 可能为幻觉。"
  }
}
```

> **注意**: `query_type` 小写（`exact`/`factual`/`analysis`），`depth` 为整数（1/2/3）。Agent 判断时应做大小写归一化。**不要将原始 JSON 直接输出给用户**，应解析后生成自然语言回答。`quality` 字段提供地面真值 TID 列表，Agent 可在回答后交叉验证引用完整性。

## 步进规格（INPUT → PROCESS → OUTPUT）

| 步骤 | 输入 | 处理 | 输出 |
|------|------|------|------|
| ① 查询分类 | 用户原始提问文本 | `RuleQueryClassifier.classify()`: TID 正则匹配 / 事实关键词匹配 / 默认 ANALYSIS | `query_type` ∈ {EXACT, FACTUAL, ANALYSIS} + `depth` ∈ {level_1, level_2, level_3} |
| ② 混合检索 | `query_type` + 用户提问 | `HybridSearch.search()`: 向量路 (Top-10, L2 距离) + 全文路 (FTS5, Top-10) → RRF 融合 (k=60) | `ranked_chunks`（最多 10 条，含 score 降序） |
| ③ 渐进披露 | `ranked_chunks` + `depth` | `ProgressiveDisclosure.filter()`: 按 level 过滤；若过滤后 < 3 条则降级到上层 level | `filtered_chunks`（≤ 10 条） |
| ④ Agent 回答 | `filtered_chunks` + `query_type` | 组装 prompt 模板 → 注入上下文 → Agent 用自身 LLM 能力生成回答 | 格式化自然语言回答（含 TID 引用） |
| ⑤ 质量度量 | Agent 回答 + `filtered_chunks` | 统计引用 TID 列表 + 计算命中率 + 交叉验证幻觉 | `quality_report`：TID 命中率 / 引用完整度 / 幻觉告警列表 |

## 参数配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--src` | 必需 | attck-knowledge 仓库的 `src/` 目录路径（`--build` 时需要） |
| `--db` | `attck_vec.db`（SKILL 目录下） | sqlite-vec 数据库路径（默认相对 SKILL 目录） |
| `--query` | — | 用户提问原文 |
| `--top-k` | 5 | 各检索路的 Top-K 候选数（如检索结果不够，手动增大） |
| `--json` | 否（纯文本输出） | 若指定，输出 JSON 格式（供 Agent 程序化消费） |
| `--build` | — | 构建索引（首次使用前必须运行，后续用于 `--rebuild`） |

> **实现说明**: embedding 模型硬编码为 `BAAI/bge-small-zh-v1.5`（~25M 参数，768 维，适合 CPU 推理）；RRF 常数为 60。如需修改，需直接编辑 `scripts/rag.py` 第 92、170 行。

## 查询分类规则

| 类型（API 输出) | 触发条件 | 例 |
|-----------------|---------|-----|
| `exact` (depth=1) | 正则匹配 `T\d{4}(\.\d{3})?` 或 `TA\d{4}` | "T1059 是什么" |
| `factual` (depth=2) | 含"是什么/定义/包括哪些/有哪些" | "侦察阶段有哪些技术" |
| `analysis` (depth=3) | 以上都不匹配（默认） | "DLL 侧加载怎么检测" |

> **注意**: API 输出使用小写类型名 + 整数深度。SKILL 内部概念使用大写 + `level_N` 以保持可读性，Agent 在解析响应时需要做归一化。

## 快速参考

### 何时使用本 Skill

| 场景 | 查询类型 | 预期行为 |
|------|---------|---------|
| 用户问"T1059 是什么" | EXACT | 返回精确 TID 文档，depth=1 |
| 用户问"XX战术有哪些技术" | FACTUAL | 返回该战术下的技术列表，depth=2 |
| 用户问"XXX 和 YYY 有什么区别" | ANALYSIS | 全库检索对比，depth=3 |
| 用户问"DLL 侧加载怎么检测" | ANALYSIS | 全库检索 + 检测建议聚合 |

### 何时不使用本 Skill

| 场景 | 替代方式 |
|------|---------|
| 非 ATT&CK 领域的通用问答 | 直接由 Agent 自身能力回答 |
| 需要最新 ATT&CK 版本（知识库未包含） | 先运行 `--rebuild` 更新索引 |
| 询问同义词但不含 TID 或战术名 | 先转为精确 TID 再查 |

## 渐进披露深度

| 层级（API) | 范围 | Top-K | 对应查询类型 |
|-----------|------|-------|-------------|
| `1` / `level_1` | 仅目标文档（仅返回与 TID 精确匹配的块） | 1-3 条 | exact |
| `2` / `level_2` | 同一战术下的战术概览 + 技术列表（过滤掉 sub_technique） | 5-10 条 | factual |
| `3` / `level_3` | 全库 Top-K + 跨战术聚合（不过滤任何层级） | 10-20 条 | analysis |

## 参考文件

- `references/mdbook-parser.json` — 元数据字段设计（level / ta_id / t_id / sub_id）
- `references/progressive-disclosure.json` — 渐进披露策略与 prompt 模板
- `test-prompts.json` — 100 条标准化测试用例（覆盖 EXACT/FACTUAL/ANALYSIS/BOUNDARY 四类）
- `scripts/run_tests.py` — 批量测试运行器（输出 PASS/FAIL 报告，含 JSON 统计摘要）

## 反例黑名单

| 不要这样做 | 原因 | 正确做法 |
|-----------|------|---------|
| 直接问 LLM "T1059 是什么" 而不运行检索 | LLM 可能幻觉生成不存在的技术描述 | 先运行 `--query "T1059"` 获取知识库精确内容 |
| 用 `--json` 输出直接喂给用户 | JSON 原始数据结构不友好 | 让 Agent 用自然语言组织回答，`--json` 仅用于程序化调用 |
| 修改 `mdbook-parser.json` 中的字段名 | 与索引构建脚本的元数据映射不同步 | 改 schema 必须同步更新 `rag.py` 中的 SQL 建表语句 |
| 在索引构建后移动 attck-knowledge 目录 | 数据库中的 `source` 路径失效 | 重建索引或使用符号链接 |
| 用模糊描述代替精确 TID 提问 | Agent 需要猜测目标，增加错误概率 | 优先使用 `T\d{4}` 格式查询 |

## 常见错误

| 触发条件 | 一线修复 | 仍失败兜底 |
|---------|---------|-----------|
| `sqlite-vec 扩展未加载` | `pip install sqlite-vec` | 检查 Python 版本是否 ≥3.10；降级至 sqlite-vec 0.9.x |
| `attck_vec.db 不存在` | 先运行 `--build` | 确认 `--src` 指向含有 `SUMMARY.md` 的目录；尝试 `--rebuild` 强制重建 |
| `sentence-transformers 未安装` | `pip install sentence-transformers` | 使用 `pip install sentence-transformers==2.2.2` 指定版本 |
| 检索结果为空 | 换同义词重试，或检查 FTS5 索引状态 | `--rebuild` 重建索引；确认索引脚本中 parse_mdbook() 成功解析了文档 |
| `--src` 路径指向仓库根而非 `src/` 子目录 | 确认 `--src` 指向 attck-knowledge 的 `src/` 目录 | 将 `--src` 参数改为 `<repo>/attck`（attck-knowledge 的实际 markdown 路径） |
| Embedding 模型下载超时 | 设置 `HF_ENDPOINT=https://hf-mirror.com` 镜像 | 手动下载模型文件到 `~/.cache/huggingface/hub/` |
