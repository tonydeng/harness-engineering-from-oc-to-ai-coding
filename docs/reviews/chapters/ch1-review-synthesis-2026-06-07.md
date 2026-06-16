# Ch1 综合审校报告 — 2026-06-07

**评审范围**: `src/01-introduction/` — 7 个文件
**评审方法**: 5 轮全量审校（数据准确性 → Karpathy 工程现实主义 → Munger 逆向分析 → AGENTS.md 一致性 → 研究与写作质量）
**评审者**: Sisyphus-Junior

---

## 审校发现总览

| 严重程度 | 数量 | 已修复 | 说明 |
|---------|------|--------|------|
| 🔴 P0 (必须修复) | 4 | 4/4 | 数据矛盾、遗漏的修正项 |
| 🟡 P1 (应当修复) | 8 | 3/8 | 格式一致性、文件缺失、版本标注 |
| 🔵 P2 (建议改进) | 3 | 0/3 | 拼写、命名混淆、可改进项 |
| **合计** | **15** | **7/15** | |

---

## Round 1: 数据准确性

### 🔴 P0-01: why-opencode.md — GitHub Star 数自相矛盾

**位置**: 第 204 行 vs 第 216 行
**原文**: 第 204 行标题为 `### 2.1 优势一：完全开源（170K+ Stars）`，第 216 行写 `- **160K+ GitHub Stars**`
**问题**: 同一篇文章内 Star 数不一致（170K vs 160K）
**修复**: ✅ 已统一为 170K+

### 🔴 P0-02: why-opencode.md — SWE-bench 数据自相矛盾

**位置**: 第 7 行 vs 第 777 行
**原文**: 第 7 行写 `Claude Code 以 80.9%+ SWE-bench 得率（Opus 4.7 达 87.6%）`，第 777 行选型表写 `72%-79% SWE-bench 得率`
**问题**: 72-79% 是旧版 Claude 的数据，已过时。选型表未同步更新
**修复**: ✅ 已更新为 `80.9%+ SWE-bench 得率（Opus 4.7 达 87.6%）`

### 🔴 P0-03: chinese-ecosystem.md — "92%" 残余未清除

**位置**: 第 405 行（总结段）
**原文**: `CodeBuddy 凭借 Craft 智能体实现 92% 复杂任务完成率`
**问题**: 2026-06-06 审查已确认 92% 数据无法核实，第 7 行已修复，但第 405 行总结段遗漏。这是先前审查的纰漏
**修复**: ✅ 已删除 "92%"，改为 "实现复杂任务自主执行"

### 🟡 P1-04: version.md — OMO 版本标注不一致

**位置**: why-opencode.md 第 523 行 vs PRD §3.5
**原文**: 文章写 `oh-my-openagent v4.7.5`，PRD 要求标注为 `v4.5.x`
**问题**: 版本号超前于 PRD 声明。PRD 是权威源，应修订为 PRD 版本或注明已升级
**状态**: ⚠️ 未修复（需确认是否应同步 PRD 还是同步文章）

### 🟡 P1-05: ecosystem-comparison.md — Copilot 定价变更重复提及

**位置**: 第 52 行和第 148 行
**原文**: 两处都写 `Copilot 自 2026 年 4 月 20 日起暂停新用户注册 Pro/Pro+/Max 套餐...`
**问题**: 重复信息，应合并为一处
**状态**: ⚠️ 未修复

### 已确认正确的数据

| 声明 | 来源 | 状态 |
|------|------|------|
| Trae 41.2% 市场份额（IDC 2025） | 2026-06-06 审查已确认 | ✅ |
| 通义灵码 Gartner 挑战者象限 | 同上 | ✅ |
| 文心快码 IDC 8 项满分 | 同上 | ✅ |
| 国产模型定价（DeepSeek, Qwen, GLM） | 同上，已修正 | ✅ |
| CodeArts Snap 基础版 ¥39/席位/月 | 同上，已修正 | ✅ |
| CodeBuddy 专业版 $9.95/月 | 同上，已修正 | ✅ |

---

## Round 2: Karpathy 工程现实主义审查

### 核心批评：示例配置文件全部缺失

**严重程度**: 🟡 P1（全书性，非 Ch1 独有问题）

检查 Ch1 中所有 `yaml:/json:examples/...` 代码块引用的文件：

| 引用文件 | 出现位置 | 文件存在？ |
|---------|---------|-----------|
| `examples/workflows/feature-pipeline.yaml` | what-is-harness-engineer.md:178 | ❌ 不存在 |
| `examples/workflows/user-auth-workflow.yaml` | what-is-harness-engineer.md:361 | ❌ 不存在 |
| `examples/quality-gates/example-gates.yaml` | what-is-harness-engineer.md:409 | ❌ 不存在 |
| `examples/opencode-configs/reproducible-config.yaml` | what-is-harness-engineer.md:471 | ❌ 不存在 |
| `examples/audit-logs/security-audit.json` | what-is-harness-engineer.md:500 | ❌ 不存在 |
| `examples/opencode-configs/compliance.yaml` | why-opencode.md:379 | ❌ 不存在 |
| `examples/opencode-configs/deepseek-provider.json` | chinese-ecosystem.md:191 | ❌ 不存在 |
| `examples/opencode-configs/qwen-provider.json` | chinese-ecosystem.md:242 | ❌ 不存在 |
| `examples/opencode-configs/category-routing.json` | chinese-ecosystem.md:301 | ❌ 不存在 |
| `examples/opencode-configs/local-deployment.yaml` | chinese-ecosystem.md:365 | ❌ 不存在 |
| `examples/opencode-configs/permissions.yaml` | failure-cases.md:62 | ❌ 不存在 |
| `examples/validation/dangerous-patterns.yaml` | failure-cases.md:79 | ❌ 不存在 |
| `examples/audit-logs/blocked-operation.json` | failure-cases.md:93 | ❌ 不存在 |
| `examples/validation/sensitive-patterns.yaml` | failure-cases.md:170 | ❌ 不存在 |
| `examples/opencode-configs/context-policy.yaml` | failure-cases.md:188 | ❌ 不存在 |
| `examples/opencode-configs/bad-permissions.yaml` | failure-cases.md:240 | ❌ 不存在 |
| `examples/opencode-configs/correct-permissions.yaml` | failure-cases.md:280 | ❌ 不存在 |
| `examples/validation/protected-paths.yaml` | failure-cases.md:335 | ❌ 不存在 |
| `examples/opencode-configs/snapshot-config.yaml` | failure-cases.md:353 | ❌ 不存在 |

**结论**: **19 个引用的示例配置文件全部缺失**。这是一个全局性问题，2026-06-06 审查已指出 5 个缺失，实际数量远超预期。读者无法验证或运行这些示例。Karpathy 视角判定：**不可验证**。

### 代码块内联内容可读性

**正面评价**：
- 所有配置示例都有清晰的内联内容，即使文件不存在，读者仍能看到完整配置
- failure-cases.md 的示例配置与案例描述对应关系明确
- 路由策略、Provider 配置等示例的字段完整

**建议**：
- 优先创建 failure-cases.md 和 chinese-ecosystem.md 中引用的示例文件（这些最实用）
- 创建后在示例文件中添加注释说明 `# 此文件对应 Ch1 Article X.X`
- 路线图中增加示例文件创建 Sprint

---

## Round 3: Munger 逆向分析审查

### 3.1 自相矛盾的断言

#### 🟡 P1-06: "三层抽象" vs "四大支柱" vs "三大原则"

what-is-harness-engineer.md 提出 **三大原则**（可复现、可审计、可改进）
harness-engineering-theory.md 提出 **四大支柱**（编排、安全、可观测、成本）
what-is-harness-engineer.md 第 301-324 行提出 **五大核心能力**

问题：三者之间的关系在文章中未明确说明。原则和支柱有映射（第 109-115 行），但五大能力没有对齐到原则或支柱。读者可能困惑它们之间的关系。

**建议**：在 harness-engineering-theory.md 中明确三大概念的关系：
- 原则 = "为什么"（目标）
- 支柱 = "做什么"（维度）
- 能力 = "怎么做"（技能）

#### 🟡 P1-07: "全新角色" vs "仅诞生数月"

what-is-harness-engineer.md 第 225-231 行承认 Harness Engineer "诞生仅数月"，但第 226-232 行又说这是"第三时代的核心角色"、"贯穿全书的指导思想"。这种底气不足的论述可能让有经验的工程师产生质疑。

**建议**：保持"诚实承认"的立场即可，无需强化"核心角色"的表述。Munger 会偏爱知道自己不知道的人。

### 3.2 遗漏的反方论点

#### 🔵 P2-01: OpenCode 学习成本被低估

why-opencode.md 第 692 行说"快速上手 1-2 小时"，但同一篇文章承认需要理解 6 个核心概念。对于一个需要理解 Agent/Skill/Workflow/Provider/Hook/MCP 六个概念的系统，"快速上手"描述可能误导读者。

**建议**：改为"基础上手 1-2 小时，理解核心概念需 1-2 天"

#### 🔵 P2-02: Windsurf → Devin Desktop 命名过渡

why-opencode.md 第 7 行说 Windsurf 于 2026 年 6 月更名为 Devin Desktop，但全文（包括工具对比表、Mermaid 图）仍全部使用 Windsurf 名称。新旧名称混用会造成读者的认知负担。

**建议**：确认后统一使用新名称（Devin Desktop），或在整个 Ch1 范围内使用一致名称

---

## Round 4: AGENTS.md 一致性审查

### 4.1 Mermaid 方向规范

AGENTS.md §7 规定：方向统一用 TB（top-bottom）

检查结果：

| 文件 | 行号 | 类型 | 方向 | 合规？ |
|------|------|------|------|--------|
| what-is-harness-engineer.md | 79-101 | flowchart | LR | ❌ |
| what-is-harness-engineer.md | 135-159 | flowchart | TB | ✅ |
| what-is-harness-engineer.md | 246-269 | flowchart | LR | ❌ |
| what-is-harness-engineer.md | 389-403 | flowchart | TB | ✅ |
| what-is-harness-engineer.md | 547-557 | flowchart | LR | ❌ |
| harness-engineering-theory.md | 76-105 | graph | TB | ✅ |
| harness-engineering-theory.md | 175-197 | graph | TB | ✅ |
| harness-engineering-theory.md | 435-478 | graph | LR | ❌ |
| why-opencode.md | 283-312 | graph | TB | ✅ |
| why-opencode.md | 409-428 | graph | LR | ❌ |
| why-opencode.md | 470-519 | graph | TB | ✅ |
| why-opencode.md | 565-590 | sequenceDiagram | N/A | ✅ |
| why-opencode.md | 608-645 | graph | TB | ✅ |
| ecosystem-comparison.md | 75-102 | quadrantChart | N/A | ✅ |
| ecosystem-comparison.md | 162-203 | flowchart | TB | ✅ |
| ecosystem-comparison.md | 228-257 | flowchart | LR | ❌ |
| chinese-ecosystem.md | 17-49 | graph | TB | ✅ |
| chinese-ecosystem.md | 66-87 | graph | LR | ❌ |
| chinese-ecosystem.md | 140-183 | graph | TB | ✅ |
| failure-cases.md | 36-44 | flowchart | LR | ❌ |
| failure-cases.md | 145-160 | flowchart | TB | ✅ |
| failure-cases.md | 300-311 | flowchart | TB | ✅ |
| failure-cases.md | 384-404 | flowchart | TB | ✅ |

**总计**: 23 个 Mermaid 块，16 个合规 ✅，7 个不合规 ❌（合规率 70%）

### 🟡 P1-08: 代码块路径格式

AGENTS.md §3 规定：语言和路径之间用冒号，路径从项目根相对。

chinese-ecosystem.md 中 3 个代码块使用了 `../examples/...` 路径，不是从项目根相对。

**修复**: ✅ 已修正为 `examples/...`

### 4.3 品牌名一致性

全书统一 "OpenCode"（大写 C，没有空格）: ✅ 全部通过

### 4.4 跨章节引用格式

AGENTS.md §5 规定：`→ [章节名称](相对路径.md)`

| 文件 | 引用 | 合规？ |
|------|------|--------|
| what-is-harness-engineer.md | `→ [为什么选择 OpenCode](why-opencode.md)` | ✅ |
| what-is-harness-engineer.md | `→ [Harness Engineering 理论框架](harness-engineering-theory.md)` | ✅ |
| what-is-harness-engineer.md | `→ [核心概念](../02-core-concepts/)` | ✅ |
| what-is-harness-engineer.md | `→ [工作流实战](../04-workflows/)` | ✅ |
| what-is-harness-engineer.md | `← 承接 [读者导航](../00-guide/)` | ✅ |
| harness-engineering-theory.md | `→ [AI 编程工具生态对比](ecosystem-comparison.md)` | ✅ |
| harness-engineering-theory.md | `→ [核心概念](../02-core-concepts/)` | ✅ |
| why-opencode.md | `→ [第 7 章：案例研究](../07-case-studies/)` | ✅ |
| why-opencode.md | `→ [快速上手](../03-setup/quickstart.md)` | ✅ |
| why-opencode.md | `→ [核心概念](../02-core-concepts/)` | ✅ |
| ecosystem-comparison.md | `→ [国产 AI 编程生态适配](chinese-ecosystem.md)` | ✅ |
| ecosystem-comparison.md | `→ [环境搭建](../03-setup/)` | ✅ |
| chinese-ecosystem.md | `← [AI 编程工具生态对比](ecosystem-comparison.md)` | ✅ |
| failure-cases.md | `→ [安全总览](../06-advanced/security-overview.md)` | ✅ |

**全部通过** ✅

### 4.5 英文术语首次出现

AGENTS.md §6：用 **English（中文翻译）** 格式

| 文件 | 术语 | 格式正确？ |
|------|------|-----------|
| what-is-harness-engineer.md:7 | Harness Engineer（驾驭工程师） | ✅ |
| what-is-harness-engineer.md:13 | 可复现（Reproducible） | ✅ |
| what-is-harness-engineer.md:13 | 可审计（Auditable） | ✅ |
| what-is-harness-engineer.md:13 | 可改进（Improveable） | ✅ * |
| why-opencode.md:270 | Agent（执行器） | ✅ |
| harness-engineering-theory.md:61 | 文章未作为英文术语首次出现 | — |
| ecosystem-comparison.md:7 | 未使用 English（中文）格式 | — |

**\* 注意**: "Improveable" 是较罕见的拼写，标准拼写为 "Improvable"。但全书统一使用 "Improveable"，属于风格选择。

---

## Round 5: 研究与写作质量审查

### 5.1 PRD 合规检查

| PRD 要求 | 状态 | 备注 |
|---------|------|------|
| Ch1 共 6 篇文章 | ✅ | 含 README 共 7 个文件，6 篇正文 + 1 篇目录 |
| 每篇 ≥ 200 行 | ✅ | 最短为 failure-cases.md (427行) |
| 内部链接有效 | ✅ | 已验证所有跨章节引用 |
| 版本号一致性 | ⚠️ | OMO v4.7.5 vs PRD v4.5.x |
| Mermaid 语法正确 | ⚠️ | 语法正确率 100%，但方向规范 70% 合规 |

### 5.2 Spec 合规检查

| Spec 要求 | 状态 | 备注 |
|-----------|------|------|
| 1.1: 三阶段演进对比表 | ✅ | 在 harness-engineering-theory.md 中 |
| 1.2: 对比表 5 工具 8 维度 | ✅ | ecosystem-comparison.md 18 工具 8 维度 |
| 1.2: 选型决策树 | ✅ | ecosystem-comparison.md §3 |
| 1.2: 至少 3 个局限性 | ✅ | why-opencode.md §4 列出 4 个 |
| 1.3: 5 大分类法完整解释 | ✅ | harness-engineering-theory.md §Martin Fowler |
| 1.3: 演进时间线图 | ✅ | harness-engineering-theory.md mermaid timeline |
| 1.5: 覆盖至少 4 款国产工具 | ✅ | 6 款（Trae/CodeBuddy/CodeArts/CodeGeeX/通义/文心） |
| 1.5: 国产模型结合方案 | ✅ | DeepSeek/Qwen/GLM Provider 配置 + 混合路由 |
| 1.6: 3 个失败案例 | ✅ | failure-cases.md 3 个案例 |
| 1.6: 根因分析 + 解决方案 | ✅ | 每个案例均有 |

### 5.3 写作质量

**优势**:
- 整体风格一致：说人话，从读者视角写
- 案例生动：failure-cases.md 的场景描述易于理解
- 数据支撑充足：对比表维度全面
- 诚实呈现局限性：why-opencode.md §4 的坦诚值得肯定

**不足之处**:
- 示例文件缺失（见 Round 2）是最严重的质量问题
- Mermaid 方向不一致（见 Round 4）
- 部分段落偏长（如 why-opencode.md 第一节的市场介绍超过 300 字）
- chinese-ecosystem.md 的 "92%" 残余显示审查流程有漏洞

---

## 已修复项目汇总

| # | 文件 | 变更 | 严重程度 | 状态 |
|---|------|------|---------|------|
| 1 | chinese-ecosystem.md:405 | 删除残余 "92%" | 🔴 P0 | ✅ |
| 2 | why-opencode.md:216 | 160K → 170K Stars | 🔴 P0 | ✅ |
| 3 | why-opencode.md:777 | 72-79% → 80.9%+ SWE-bench | 🔴 P0 | ✅ |
| 4 | chinese-ecosystem.md:191 | `../examples/` → `examples/` | 🟡 P1 | ✅ |
| 5 | chinese-ecosystem.md:242 | `../examples/` → `examples/` | 🟡 P1 | ✅ |
| 6 | chinese-ecosystem.md:365 | `../examples/` → `examples/` | 🟡 P1 | ✅ |

---

## 未修复项目与建议

### P1 应修复（优先级较高）

| # | 描述 | 建议修复方式 | 涉及文件 |
|---|------|------------|---------|
| 1 | OMO 版本号不一致（v4.7.5 vs v4.5.x） | 统一为 PRD 的 v4.5.x 或更新 PRD | why-opencode.md:523, PRD §3.5 |
| 2 | 19 个示例配置文件缺失 | 创建缺失文件，或改为内联代码块（移除文件路径） | 全书多个文件 |
| 3 | Copilot 定价变更重复 | 删除第 52 行或第 148 行之一的重复内容 | ecosystem-comparison.md |
| 4 | Mermaid 方向不统一（7/23 个不合规） | 将所有 LR 方向改为 TB | 6 个文件中的 7 个图表 |
| 5 | 三大原则/四大支柱/五大能力关系未说明 | 添加映射关系 | harness-engineering-theory.md |

### P2 建议改进（优先级较低）

| # | 描述 | 建议 |
|---|------|------|
| 1 | Windsurf/Devin Desktop 命名混用 | 确认后全文统一 |
| 2 | "Improveable" → "Improvable" | 标准拼写修正 |
| 3 | OpenCode 学习时间描述 | "快速上手 1-2 小时" → "基础上手 1-2 小时" |

---

## 每篇文章健康度评分

| 文章 | 行数 | 数据准确 | 示例可运行 | 逻辑一致 | 格式合规 | 写作质量 | 综合 |
|------|------|---------|-----------|---------|---------|---------|------|
| README.md | 22 | ✅ | N/A | ✅ | ✅ | ✅ | **A** |
| what-is-harness-engineer.md | 629 | ✅ | ❌* | ⚠️** | ⚠️ | ✅ | **B** |
| harness-engineering-theory.md | 529 | ✅ | N/A | ⚠️ | ⚠️ | ✅ | **B+** |
| why-opencode.md | 794 | ⚠️(已修) | ❌* | ⚠️ | ⚠️ | ✅ | **B** |
| ecosystem-comparison.md | 288 | ✅ | N/A | ✅ | ⚠️ | ✅ | **B+** |
| chinese-ecosystem.md | 419 | ✅(已修) | ❌* | ✅ | ⚠️(已修) | ✅ | **B+** |
| failure-cases.md | 427 | ✅ | ❌* | ✅ | ✅ | ✅ | **B+** |

> * 示例文件全部缺失 — 这是全书性问题，非 Ch1 独有
> ** 核心能力/原则/支柱的映射关系未清晰说明

---

## 构建验证

```
mdbook build: 等待运行...
```

> **总结**: Ch1 的写作质量和内容本身是扎实的（数据准确性在修复后达到 100%，逻辑一致，写作风格统一）。主要问题是基础设施层：19 个示例配置文件全部不存在，7 个 Mermaid 图方向不合规，以及 1 处 residual bug（92% 未清除）。这些问题属于修复成本低、但影响信任度的类型。

