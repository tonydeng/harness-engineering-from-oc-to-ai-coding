# ATT&CK RAG Skill — OpenCode Agent Skill

本目录是 `examples/attck-rag/skills/attck-rag/`，为 AI 智能体（OpenCode / Claude Code 等）提供的本地 ATT&CK 知识库 RAG Skill。

## 目录结构

```
skills/attck-rag/
├── SKILL.md              ← Skill 定义（Agent 加载后获知完整操作流程）
├── README.md             ← 本文件 — Skill 使用说明
├── attck_vec.db          ← sqlite-vec 向量数据库（索引构建后生成）
├── scripts/
│   ├── rag.py            ← 索引构建 + 混合检索 + 质量报告（CLI / JSON）
│   └── run_tests.py      ← 批量测试运行器（100 条 test-prompts）
├── references/
│   ├── mdbook-parser.json           ← 元数据字段设计参考
│   └── progressive-disclosure.json  ← 渐进披露策略参考
└── test-prompts.json     ← 100 个测试 prompt（30 EXACT + 25 FACTUAL + 20 ANALYSIS + 25 BOUNDARY）
```

## 使用方式

### 构建索引（首次使用前必须运行）

```bash
python scripts/rag.py --build --src /path/to/attck-knowledge/src
```

### 查询

```bash
python scripts/rag.py --query "T1059 是什么"
python scripts/rag.py --query "T1059 是什么" --json   # Agent 调用推荐
```

### 运行测试

```bash
python scripts/run_tests.py
```

输出 100 条测试的 PASS/FAIL 报告，包含每种查询类型的评估指标。

## 测试系统

`run_tests.py` 是批量测试运行器，读取 `test-prompts.json`，对每条用例执行完整检索管线并输出 PASS/FAIL 报告。

### 测试类型

| 类型 | 数量 | 评估标准 |
|------|:----:|----------|
| EXACT | 30 | 精确命中目标 TID/TAID，chunk_count > 0 |
| FACTUAL | 25 | 返回有意义的结果（chunk_count > 0） |
| ANALYSIS | 20 | 至少返回 2 个块才有分析价值 |
| BOUNDARY | 25 | 按场景分别验证（空输入/格式异常/不存在TID/大小写/特殊字符等） |

### 边界测试覆盖

| 场景 | 示例 | 预期 |
|------|------|------|
| 空输入 | `""` | chunk_count = 0 |
| 纯空格 | `"   "` | chunk_count = 0 |
| 单字符 T | `"T"` | chunk_count = 0 |
| 不存在 TID | `T9999` | chunk_count = 0 |
| 小写 TID | `t1059` | 大小写归一化，正常返回 |
| 尾部句号 | `T1059.` | 自动截断，正常返回 |
| 双点 | `T1059..001` | 格式修正，正常返回 |
| 前导点 | `.T1059` | 截断前导点，正常返回 |
| 连字符 | `T-1059` | 格式修正，正常返回 |
| 特殊字符 | `<script>alert('xss')</script>` | 安全过滤，不崩溃 |
| 多 TID | `T1059 T1078 T1003 T1190` | 至少解析部分 TID |
| SQL 注入 | `'; DROP TABLE ...` | 安全过滤，不崩溃 |
| 无关内容 | `今天天气怎么样` | 返回提示而非硬关联 |

## ATT&CK RAG Skill 优化评分

对 `SKILL.md` 的 9 维度质量评估（满分 45），涵盖结构、清晰度、完整性、可操作性、一致性、简洁性、错误处理、适应性和测试覆盖率。

### 基线评估（Phase 1）

| 维度 | 得分 | 说明 |
|------|:----:|------|
| D1 结构 (Structure) | 5/5 | 文档结构完整，步骤清晰 |
| D2 清晰度 (Clarity) | 5/5 | 语言简洁，无歧义 |
| D3 完整性 (Completeness) | 5/5 | 覆盖构建、查询、测试全流程 |
| D4 可操作性 (Actionability) | 5/5 | 每个步骤可立即执行 |
| D5 一致性 (Consistency) | 5/5 | 术语、格式、风格统一 |
| D6 简洁性 (Conciseness) | 5/5 | 无冗余信息 |
| D7 错误处理 (Error Handling) | 5/5 | 异常表、CHECKPOINT 机制完备 |
| D8 适应性 (Adaptability) | 5/5 | 支持多种查询类型和输出格式 |
| D9 测试覆盖率 (Test Coverage) | 3/5 | 未引用测试用例文件和运行器 |
| **总分** | **43/45** | 基线评分 |

### 优化提升（Phase 2）

| 改进项 | 说明 |
|--------|------|
| 添加参考文件引用 | 在"参考文件"表中添加 `test-prompts.json` 和 `scripts/run_tests.py` |
| Agent 工作流第 6 步 | 增加回归测试步骤：运行→确认全部 100 条 PASS→修复→通过 |
| 新增"回归测试验证"小节 | 包含测试类型覆盖表（EXACT/FACTUAL/ANALYSIS/BOUNDARY）和验证原则 |

### 优化后评分（Phase 2 Re-eval）

| 维度 | 得分 | 变化 |
|------|:----:|:----:|
| D9 测试覆盖率 | 5/5 | +2 |
| **总分** | **45/45** | +2 |

### 盲审评估（Phase 3 — 3 独立评审）

| 评审方 | 评分 | 说明 |
|--------|:----:|------|
| Judge A | 44/45 | 优秀，建议在示例中补充 `--json` 的典型使用方式 |
| Judge B | 44/45 | 结构清晰，建议进一步细化"非 ATT&CK 问题"的判断标准 |
| Judge C | 45/45 | 无需改进 |
| **平均** | **44.3/45 (98.5%)** | 综合评分 |

## 修复记录

### 2026-07 — 子技术 TID 匹配 + 输入验证 + 评测优化

**问题**：3 个 test-prompts FAIL（原 10 条测试）

- **Test 4 (T1059.009)**：FTS5 遇到 `.` 崩溃，向量检索未召回子技术块
- **Test 2 (侦察阶段) & Test 9 (凭据转储)**：`disclosure_filter` 中 `level` 字段路径错误（`c.get("level")` 应为 `c.get("meta", {}).get("level")`），depth=2 过滤掉所有结果

**修复**：

1. `direct_tid_lookup()` — SQL 元数据精确匹配，绕过 FTS5/向量直接按 `t_id` / `sub_id` / `ta_id` 召回
2. `_sanitize_fts5_query()` — 移除 `.` `:` 防止 FTS5 语法崩溃
3. 修复 `disclosure_filter` — `c.get("meta", {}).get("level")` 而非 `c.get("level")`
4. 模型缓存 — 避免每次 `hybrid_search` 重新加载 embedding 模型

### 2026-07 — 扩展到 100 条测试 + 边界测试修复

**问题**：12 个 BOUNDARY FAIL（首次运行 100 条测试时）

- 空/纯空格/单字符 T 未做输入验证
- 格式异常 TID（`T1059.`、`T1059..001`、`.T1059`、`T-1059`）被 evaluate 分支提前截胡
- 小写 `t1059` 和多 TID 查询被 fake_tids 检查错误拦截

**修复**：

1. `hybrid_search()` 前端添加输入验证层 — 空/纯空格/单字符/单 TA 直接返回空结果
2. `evaluate_boundary()` 重排检查顺序 — 按特异性从高到低：空→小写→格式异常→多TID→不存在TID→其他
3. `quality_report()` 完善 sub_id 收集
4. `run_tests.py` 使用 `test[type]` 而非 classifier 推断的类型进行评估
