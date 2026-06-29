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
    A["🎯 Analyze<br/>运行 HEDQ 评分"] --> B["🔍 Diagnose<br/>解读报告定位根因"]
    B --> C["🛠 Fix<br/>按优先级修复"]
    C --> D["✅ Verify<br/>重新评分验证"]
    D --> A
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

---

## 第一步：Analyze（评分）

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

读取 HEDQ 报告后，确定当前最低分维度，按以下逻辑定位根因：

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

### 自检：诊断完整性确认

在进入 Fix 前进行元认知自检，避免以下常见诊断失误：
- **确认根因而非症状**：是否找到了最低分的具体检测项而非猜测？应 grep 验证后再下结论
- **确认修复可行性**：该维度的低分是否可通过单向修复提升？若为内容深度问题（D3/D5），1 轮内提升幅度有限
- **确认范围边界**：修复范围是否局限在问题维度内？检查是否计划修改了无关文件
- **存在 P0 违规时**：是否已优先修复 P0 而非优化低分维度？

---

### 🔴 CHECKPOINT

在进入 Fix 前确认：
- 已定位最低维度的根因（若定位不到 → 使用 grep 手动扫描）
- 选定的修复维度是当前最低分
- 用户确认修复方案后执行

---

## 第三步：Fix（修复）

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

### 常见修复手法

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
```

---

### 🔴 CHECKPOINT

在从 Fix 进入 Verify 前确认：
- 所有修改已做原子性提交：每轮 fix 后 `git add + git commit`，不得跳过
- 修复范围不超过所选维度：若修改了其他维度内容，先回退再进入 Verify
- 修复手法符合规范：代码块 path 格式、内部链接格式、品牌名大小写全部按 AGENTS.md 规范
- 已完成元认知自检：当前修改有明确可验证的提升预期

---

## 第四步：Verify（验证）

每次修复后必须重新运行 HEDQ 确认分数提升：

```bash
python ./scripts/qa/run-hedq.py --json --no-save
```

验证通过条件：
- 无 P0 违规
- 修复维度分数明显提升
- 未引入新的 D1/D4/D7 违规

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
