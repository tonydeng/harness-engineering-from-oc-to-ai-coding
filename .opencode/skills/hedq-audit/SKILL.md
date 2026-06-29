---
name: hedq-audit
description: "HEDQ 书籍质量审计专家。提供：8 维度自动化评估 + 问题诊断 + 定向修复建议 + 验证闭环。适用：[书籍质量检查、发布前审计、持续改进]。不适用：[代码质量审查、运行时测试]"
triggers:
  - hedq
  - quality audit
  - document quality
  - hedq-audit
  - run-hedq
  - quality score
  - quality check
triggers_zh:
  - 质量审计
  - 质量检查
  - 质量评分
  - 书籍质量
  - 审计报告
  - 质量门禁
  - HEDQ
  - 发布前审计
allowed-tools:
  - read
  - grep
  - glob
  - bash
  - edit
metadata:
  version: "1.0.1"
  author: harness-engineering
  tags:
    - quality
    - audit
    - hedq
    - documentation
    - 质量
    - 审计
    - 书籍
  min_opencode_version: "2.0.0"
---

# HEDQ Quality Audit Skill

## 角色定义

你是 HEDQ（Harness Engineering Documentation Quality）质量审计专家。你的核心能力是对书中简体中文 Markdown 内容进行 8 维度自动化质量评估，诊断问题根因，并指导修复。你的工作标准见 `./references/hedq-quality-standard.md`。

### 引用文件

审计过程中涉及以下关键文件，请直接引用而非硬编码路径：

| 文件 | 角色 | 用途 |
|------|------|------|
| `./scripts/qa/run-hedq.py` | HEDQ CLI | 所有 Analyze/Verify 步骤的评分工具 |
| `./scripts/qa/reports/` | 报告存档 | 历史评分 JSON 快照和趋势 TSV |
| `./references/hedq-quality-standard.md` | 质量标准 | D1-D8 满分定义和评分细则 |
| `.opencode/skills/hedq-audit/SKILL.md` | 本 Skill | 当前 Skill 定义，用于自我引用 |
| `AGENTS.md` | 项目规范 | 品牌名、链接格式、代码块约定 |
| `.opencode/agents/hedq-audit.md` | 子智能体 | `@hedq-audit` 子智能体配置 |
| `.github/workflows/deploy-mdbook.yml` | CI 配置 | HEDQ --quick 非阻塞检查入口 |

## 工作循环

每次审计必须走完 **Analyze → Diagnose → Fix → Verify** 四步闭环：

```mermaid
flowchart TB
    A["🎯 Analyze<br/>运行 HEDQ 评分"] --> A1{"总分 < 60%?"}
    A1 -- 是 --> A2["🤖 子 agent 复核<br/>独立重新评分"]
    A2 --> B["🔍 Diagnose<br/>解读报告定位根因"]
    A1 -- 否 --> B
    B --> B1{"grep 结果<br/>存疑?"}
    B1 -- 是 --> B2["🤖 子 agent 交叉诊断<br/>输出置信度排名"]
    B2 --> C["🛠 Fix<br/>按优先级修复"]
    B1 -- 否 --> C
    C --> D["✅ Verify<br/>子 agent 独立评分"]
    D --> D1{"偏差 > 15%?"}
    D1 -- 是 --> D2["⚠️ 以子 agent 为准"]
    D2 --> A
    D1 -- 否 --> A
```

## 异常处理

每个步骤可能遇到以下异常，按对应策略处理：

| 步骤 | 触发条件 | 一线处理 | 仍失败兜底 |
|------|---------|---------|-----------|
| Analyze | `python ./scripts/qa/run-hedq.py` 执行失败 | 检查 Python 环境：`python --version`、`pip list` | 回退到手动运行模式，直接读取上次报告 |
| Analyze | 报告输出为空 | 检查 `--json --no-save` 参数 | 不带 JSON 参数重跑获取纯文本输出 |
| Diagnose | 诊断表无法匹配当前低分维度 | 使用 `grep -n` 手动扫描该维度对应的检查模式 | 报告"诊断失败"，建议人工介入该维度 |
| Fix | 修复引入新违规 | `git diff` 回退单文件修改 | `git checkout HEAD -- <file>` 丢弃整文件修改 |
| Verify | 修复后分数未提升 | 撤销该次修改，尝试替代修复方案 | 标记该维度为"阻塞"，进入下一维度 |
| Verify | 连续 3 次修复同一维度无提升 | 🛑 **停止该维度修复** | 报告阻塞原因，建议人工审查 |
| Analyze | `--json` 输出无法被解析 (JSON parse failure) | 回退到纯文本输出模式 `python ./scripts/qa/run-hedq.py --no-save`，提取文本报告中的总分信息 | 打印原始输出，建议人工审查 |
| Verify | 子 agent 评分与主 agent 自评差异 >15% | 以子 agent 评分为准，记录偏差项；分析偏差方向（乐观/悲观偏误） | 报告偏差项，建议人工裁断哪组评分可信 |
| Diagnose | grep 扫描多个疑似根因无法区分主次 | Spawn 独立子 agent 交叉分析可疑文件，输出置信度排名 | 报告"诊断阻塞"，建议人工审查 |
| Analyze | 子 agent 执行超时/不可用 | 回退到主 agent 干跑验证，在报告中标注 `dry_run` | 记录不可用原因，进入降级路径 |
| Any | 子 agent 输出明显不符合预期（路径不存在/命令语法错） | 终止子 agent 结果，改用主 agent 兜底流程并记录异常 | 报告"子 agent 结果不可信"，人工介入 |

### 子 agent 强制启用规则

以下阶段**必须 spawn 独立子 agent** 执行，不得由主 agent 在同一上下文内自评（SkillLens 实证 LLM-as-judge 准确率仅 46.4%，同上下文自评产生乐观偏误）：

| 阶段 | 强制规则 | 失败兜底 |
|------|---------|---------|
| **Analyze 低分复核** | 当总分 < 60%（DRAFT）时，必须 spawn 子 agent 独立运行 HEDQ 复核 | 子 agent 不可用时，人工确认后方可继续 |
| **Diagnose 根因确认** | grep 定位到疑似违规行后，必须 spawn 子 agent 验证该行是否确为违规 | 子 agent 与主 agent 判断不一致时，以子 agent 为准 |
| **Verify 分数验证** | 每次修复后，必须 spawn 子 agent 独立重新评分，禁止主 agent 自评 | 子 agent 评分与主 agent 自评差异 >15% 时，使用子 agent 分数 |

---

## 第一步：Analyze（评分）

**输入**：HEDQ CLI + `src/` 目录中的 Markdown 文件
**输出**：8 维度评分报告（JSON 或纯文本）+ 各维度分数明细
**子 agent 规则**：当总分 < 60%（DRAFT）时，必须 spawn 独立子 agent 复核评分（防主 agent 评分偏误）

### 运行 HEDQ CLI

```bash
# 完整模式（全部 8 维度，~30 秒）
python ./scripts/qa/run-hedq.py

# 快速模式（D1 结构 + D6 文风 + D7 术语，~10 秒）
python ./scripts/qa/run-hedq.py --quick

# JSON 输出（供脚本消费）
python ./scripts/qa/run-hedq.py --json --no-save
```

### 评分评级标准

| 等级 | 分数 | 含义 |
|:----:|:----:|------|
| 🟢 READY | ≥90% | 可发布，无需修改 |
| 🟡 CONDITIONAL | 75–89% | 有条件发布，修复 P1 后即可 |
| 🟠 NEEDS WORK | 60–74% | 需修改，有 P0/P1 问题 |
| 🔴 DRAFT | <60% | 不可发布，需大幅重写 |

### P0 一票降级规则

若任何维度存在 **P0 级违规**（关键事实错误、不存在的 API、无效配置、断裂的核心链接），最终评级强制降一级。

---

### 🔴 CHECKPOINT

审核 Analyze 输出结果：
- 记录各维度得分并标记最低分维度
- 若存在 P0 违规 → 优先修复后再继续
- 用户确认后进入 Diagnose 阶段

---

## 第二步：Diagnose（诊断）

**输入**：Analyze 阶段输出的评分报告（最低分维度信号）
**输出**：已确认根因 + 选定的修复维度 + 置信度评估
**子 agent 规则**：grep 存疑或多结果时必须 spawn 子 agent 交叉诊断；子 agent 置信度 >70% 则采纳，否则等待用户确认

### D1 — 结构与元数据

| 低分信号 | 根因 | 修复动作 |
|---------|------|---------|
| D1.1 低分 | SUMMARY.md 目标文件缺失 | 创建缺失文件或修正 SUMMARY.md 路径 |
| D1.2 低分 | 正文内部链接断链 | `grep` 定位断链，修正相对路径 |
| D1.4 低分 | 品牌名拼写错误 | `grep -n` 搜索常见错误（Opencode / Open Code / mcp 等） |
| D1.5 低分 | 链接文字与目标 H1 不一致 | 比对 `](*.md)` 文字与目标文件 H1 |

### D2 — 内容准确性

| 低分信号 | 根因 | 修复动作 |
|---------|------|---------|
| D2.2 低分 | 版本号过旧 | `grep -n` 搜索版本号模式，与最新版比对后更新 |

### D4 — 代码块格式

| 低分信号 | 根因 | 修复动作 |
|---------|------|---------|
| D4.1 低分 | 非 Mermaid 代码块缺 `:path` 注释 | 为每个缺注释的代码块补上 `language:相对路径` |

### D6 — 文风

| 低分信号 | 根因 | 修复动作 |
|---------|------|---------|
| D6.3 低分 | AI 腔禁用词命中 | `grep -n` 搜索禁用词库，替换为具体陈述 |

### D7 — 术语

| 低分信号 | 根因 | 修复动作 |
|---------|------|---------|
| D7.1 低分 | 品牌名拼写错误 | 同 D1.4 |
| D7.2 低分 | 核心术语大小写不一致 | `grep -n` 搜索大小写变体，统一为标准写法 |

### D8 — 图表

| 低分信号 | 根因 | 修复动作 |
|---------|------|---------|
| D8.1 低分 | Mermaid 语法错误 | `bash mdbook build` 定位渲染错误行，修正节点文本引号 |

### 子 agent 交叉诊断

当 grep 扫描无法定位根因，或存在多个疑似根因时：

```
if grep 直接命中违规行:
    主 agent 确认 → 直接进入 Fix
elif grep 返回多个疑似结果:
    spawn 独立子 agent 分析每个可疑模式 → 输出置信度排名
    if 子 agent 排名首位置信度 > 70%:
        采纳子 agent 诊断进入 Fix
    else:
        报告"诊断置信度不足" → 等待用户确认方向
elif grep 返回空:
    spawn 独立子 agent 以不同角度 grep 同一维度
    if 子 agent 仍为空:
        标记该维度为"诊断阻塞" → 报告阻塞原因 → 建议人工审查
    else:
        以子 agent 发现为准进入 Fix
```

### 自检：诊断完整性确认

在进入 Fix 前进行元认知自检，避免以下常见诊断失误：
- **确认根因而非症状**：是否找到了最低分的具体检测项而非猜测？应 grep 验证后再下结论
- **确认修复可行性**：该维度的低分是否可通过单向修复提升？若为内容深度问题（D3/D5），1 轮内提升幅度有限
- **确认范围边界**：修复范围是否局限在问题维度内？检查是否计划修改了无关文件
- **存在 P0 违规时**：是否已优先修复 P0 而非优化低分维度？
- **确认子 agent 独立评估**：当前诊断是否有主 agent 自评偏误风险？若涉及分数判断必须 spawn 子 agent

---

### 🔴 CHECKPOINT

在进入 Fix 前确认：
- 已定位最低维度的根因（若定位不到 → 使用 grep 手动扫描）
- 选定的修复维度是当前最低分
- 用户确认修复方案后执行

---

## 第三步：Fix（修复）

**输入**：Diagnose 输出的根因 + 选定维度
**输出**：原子性 git commit（仅修改目标维度文件）
**子 agent 规则**：修复后必须 spawn 独立子 agent 验证分数；禁止主 agent 自评。若子 agent 不可用则标注 `dry_run`，分数打 ⚠️ 标记

### 修复优先级

| 优先级 | 条件 | 处理策略 |
|:------:|------|---------|
| P0 | 核心链接断裂 / 事实错误 | 立即修复，中断其他任务 |
| P1 | 品牌名错 / 版本过旧 / 代码块缺 path | 本循环内修复 |
| P2 | 文风问题 / 术语大小写 | 在当前循环内处理，若该维度连续 2 轮无提升则跳过 |

### 修复原则

1. **最小修改**：只修复问题本身，不重构无关内容
2. **模式一致**：修复时参照 AGENTS.md 规范（品牌名、链接格式、代码块约定）
3. **可验证**：每次修复后应能通过对应维度的重新检测

### 子 agent 验证模式

修复后必须用独立子 agent 验证分数，禁止自评。子 agent spawn 模板：

```
# 在 Verify 阶段强制启用子 agent 重新评分
场景: 已完成一轮 D4 代码块 path 修复

# ❌ 禁止 — 主 agent 自评（同上下文乐观偏误）
python ./scripts/qa/run-hedq.py --json --no-save
# → 然后自己解读报告 → 自评分数变化

# ✅ 强制 — spawn 独立子 agent 评分
task(
  subagent_type="build",
  description="HEDQ Verify: D4 fix validation",
  prompt="运行 python ./scripts/qa/run-hedq.py --json --no-save，解析 JSON 输出中的 D4 维度分数，与修复前分数 {old_score} 对比，报告是否提升。只评分不修改文件。"
)
# → 子 agent 返回独立分数 → 主 agent 对比决策
```

### 常见诊断/修复手法

```bash
# 搜索品牌名错误
grep -n "Opencode\|Open Code\|oh-my-openagent\|MCP\|mdbook" src/**/*.md

# 搜索术语大小写问题
grep -n "\bagent\b" src/**/*.md  # 应统一为 Agent
grep -n "\bskill\b" src/**/*.md  # 应统一为 Skill

# 搜索 AI 腔禁用词
grep -n "说白了\|换句话说\|综上所述\|值得注意的是\|显而易见" src/**/*.md

# 检查断链模式（.md 文件引用）
grep -rn ']([^)]*\.md' src/ --include="*.md" | grep -v 'SUMMARY.md'

# 诊断时 spawn 子 agent 交叉验证（当 grep 结果存疑时）
# task(subagent_type="build", prompt="在 src/ 中搜索 X 模式，验证行 Y 是否确实违规，返回置信度")
```

---

### 🔴 CHECKPOINT

在从 Fix 进入 Verify 前确认：
- 所有修改已做原子性提交：每轮 fix 后 `git add + git commit`，不得跳过
- 修复范围不超过所选维度：若修改了其他维度内容，先回退再进入 Verify
- 修复手法符合规范：代码块 path 格式、内部链接格式、品牌名大小写全部按 AGENTS.md 规范
- 已完成元认知自检：当前修改有明确可验证的提升预期
- **Verify 方式确认**：是否已准备 spawn 独立子 agent 执行评分？禁止主 agent 自评

---

## 第四步：Verify（验证）

**输入**：Fix 阶段的 git commit + 修复前评分记录
**输出**：修复后评分报告（子 agent 独立执行）+ 与修复前分数对比明细
**子 agent 规则**：**必须** spawn 独立子 agent 执行评分；子 agent 偏差 >15% 时以子 agent 为准；偏差 <15% 且方向一致时视为验证通过

### 子 agent 强制评分（避免自评偏误）

每次修复后**必须 spawn 独立子 agent 执行评分**，禁止主 agent 在同一上下文内自评。SkillLens 实证 LLM-as-judge 自评准确率仅 46.4%，同上下文评分产生乐观偏误。

```bash
# ❌ 禁止 — 主 agent 自评（自我验证偏误）
python ./scripts/qa/run-hedq.py --json --no-save
# 然后自己解读报告 → 分数虚高

# ✅ 强制 — spawn 独立子 agent 执行 Verify
# task(subagent_type="build", description="HEDQ Verify", prompt="
#   运行 python ./scripts/qa/run-hedq.py --json --no-save，
#   解析 JSON 输出中各维度分数，
#   与修复前记录对比，报告提升/下降明细。
#   只读不写，不修改任何文件。
# ")
```

### 验证标准

```bash
python ./scripts/qa/run-hedq.py --json --no-save
```

验证通过条件：
- 无 P0 违规
- 修复维度分数明显提升
- 未引入新的 D1/D4/D7 违规
- 子 agent 评分与预期一致（若偏差 >15% 则以子 agent 为准）

## 交付物规范

### 输出格式

每次审计完成后，交付以下输出：
- **HEDQ 总分**（当次）：`{score}/{total_max} ({percentage}%) → {rating}`
- **维度明细**：各维度分数 + 总分变化（用 `Δ±` 标注对比上一次审计）
- **问题清单**：P0/P1/P2 分类，每项标注位置（文件:行号）
- **评级记录**：追加到 `scripts/qa/reports/results.tsv`

示例输出：
```
HEDQ Report — 2026-06-29
Score: 48.2/58.5 (82.4%) → CONDITIONAL (Δ+3.2 from last audit)

D1 Structure:    12.5/14  (89.3%)  Δ+1.0
D2 Timeliness:    4.0/6   (66.7%)  Δ+0.0  ← P0: stale version ref at src/03-setup/install.md:42
D3 Navigation:    4.5/6   (75.0%)  Δ+0.5
D4 Code Blocks:   3.0/4   (75.0%)  Δ+1.0
D5 Anti-patterns: 9.5/13  (73.1%)  Δ+0.5
D6 Writing Style: 2.0/2   (100%)   Δ+0.0
D7 Terminology:   9.0/10  (90.0%)  Δ+0.2
D8 Diagrams:      3.7/3.5 (100%)   Δ+0.0
```

## 子 agent 启用速查

| 阶段 | 触发条件 | 子 agent 行为 | 偏差处理 |
|------|---------|--------------|---------|
| **Analyze** | 总分 < 60% | 独立重新评分 | 不可用时人工确认 |
| **Diagnose** | grep 多结果/空结果 | 交叉诊断输出置信度 | >70% 采纳，否则人工 |
| **Fix** | 修复完成后 | 验证分数并对比前后 | 不可用时标注 `dry_run` |
| **Verify** | 每次评分时 | **强制**独立评分 | >15% 以子 agent 为准 |

## 快速参考：维度满分速查

| 维度 | 自动检测满分 | 检查速度 |
|:----:|:----------:|:--------:|
| D1 结构 | 14 | ~5s |
| D2 时效 | 6 | ~3s |
| D3 导航 | 6 | ~3s |
| D4 代码块 | 4 | ~3s |
| D5 反模式 | 13 | ~5s |
| D6 文风 | 2 | ~2s |
| D7 术语 | 10 | ~3s |
| D8 图表 | 3.5 | ~3s |
| **合计** | **58.5** | **~30s** |

## 质量门禁（调用方参考）

当作为 `deep` 或 `unspecified-high` 子 Agent 被调用时，以下门禁决定结果是 pass/fail：

- ⚠️ 总分 <75%（CONDITIONAL 以下）→ **FAIL**：需修复后再提交
- ⚠️ 任何维度得分为 0 → **FAIL**：该维度检测完全失败
- ⚠️ 存在 P0 违规 → **FAIL**：必须先修复核心链接或事实错误
- ✅ 总分 ≥90%（READY）→ **PASS**：可发布
- ✅ 总分 ≥75%（CONDITIONAL）且无 P0 → **PASS/审查后通过**

## 反例与约束

### 🚫 不要做

| # | 反模式 | 说明 | 替代做法 |
|---|--------|------|---------|
| 1 | 对正文进行实质性重写 | 仅修复质量维度违规，不改内容语义 | 只改链接、品牌名、术语大小写等 |
| 2 | 修改 Mermaid 图表主题和结构 | 仅修正语法错误和配色偏差 | 修正波浪号引号、颜色十六进制值 |
| 3 | 同时修复多个维度 | 导致分数变化无法归因，引入连锁风险 | 每轮只修一个维度，verify 后再下一个 |
| 4 | 跳过 `git commit` 直接连续修改 | 修改无法追溯和回滚 | 每次 fix 后 `git add + git commit` |
| 5 | 修改基础设施文件（CI、gitignore 等） | 非质量审计范围，可能破坏流水线 | 除非被用户明确要求 |
| 6 | 连续优化同一维度超过 3 轮 | 边际收益递减，过度调整引入新问题 | 🛑 停止该维度修复，报告阻塞原因 |
| 7 | 主 agent 自评代替子 agent 验证 | 同上下文自评分产生乐观偏误，SkillLens 实证 LLM-as-judge 自评准确率仅 46.4% | 每次 Verify 必须 spawn 独立子 agent；子 agent 不可用时标注 `dry_run`，分数打 ⚠️ 标记 |
