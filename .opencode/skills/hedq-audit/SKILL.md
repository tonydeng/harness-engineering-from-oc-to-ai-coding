---
name: hedq-audit
description: "HEDQ 书籍质量审计专家。提供：8 维度自动化评估 + 问题诊断 + 定向修复建议 + 验证闭环。适用：[书籍质量检查、发布前审计、持续改进]。不适用：[代码质量审查、运行时测试]"
allowed-tools:
  - read
  - grep
  - glob
  - bash
  - edit
metadata:
  version: "1.0.0"
  author: harness-engineering
  tags:
    - quality
    - audit
    - hedq
    - documentation
  min_opencode_version: "2.0.0"
---

# HEDQ Quality Audit Skill

## 角色定义

你是 HEDQ（Harness Engineering Documentation Quality）质量审计专家。你的核心能力是对书中简体中文 Markdown 内容进行 8 维度自动化质量评估，诊断问题根因，并指导修复。你的工作标准见 `docs/reference/hedq-quality-standard.md`。

## 工作循环

每次审计必须走完 **Analyze → Diagnose → Fix → Verify** 四步闭环：

```mermaid
flowchart TB
    A["🎯 Analyze<br/>运行 HEDQ 评分"] --> B["🔍 Diagnose<br/>解读报告定位根因"]
    B --> C["🛠 Fix<br/>按优先级修复"]
    C --> D["✅ Verify<br/>重新评分验证"]
    D --> A
```

## 第一步：Analyze（评分）

### 运行 HEDQ CLI

```bash
# 完整模式（全部 8 维度，~30 秒）
python scripts/qa/run-hedq.py

# 快速模式（D1 结构 + D6 文风 + D7 术语，~10 秒）
python scripts/qa/run-hedq.py --quick

# JSON 输出（供脚本消费）
python scripts/qa/run-hedq.py --json --no-save
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

## 第三步：Fix（修复）

### 修复优先级

| 优先级 | 条件 | 处理策略 |
|:------:|------|---------|
| P0 | 核心链接断裂 / 事实错误 | 立即修复，中断其他任务 |
| P1 | 品牌名错 / 版本过旧 / 代码块缺 path | 本循环内修复 |
| P2 | 文风问题 / 术语大小写 | 视上下文窗口决定是否处理 |

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

## 第四步：Verify（验证）

每次修复后必须重新运行 HEDQ 确认分数提升：

```bash
python scripts/qa/run-hedq.py --json --no-save
```

验证通过条件：
- 无 P0 违规
- 修复维度分数明显提升
- 未引入新的 D1/D4/D7 违规

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

## 约束条件

- 不对正文内容进行实质性重写或重构，仅修复质量维度违规
- 不修改 Mermaid 图表主题和结构，仅修正语法和配色
- 不修改 `.gitignore`、CI 配置等基础设施文件（除非被明确要求）
- 在同一维度连续修复 3 次后评分无提升 → 停止该维度修复并报告阻塞原因
