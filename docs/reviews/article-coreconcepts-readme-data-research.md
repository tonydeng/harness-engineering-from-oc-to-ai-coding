# OpenCode 平台术语事实核查报告

**审查文件**: `src/02-core-concepts/README.md`
**审查方法**: 基于官方文档的术语验证
**审查日期**: 2026-06-06
**数据来源**: https://open-code.ai 官方文档

---

## 逐条核查

### 1. "Agent（智能体）" — ⚠️ 部分正确

| 项目 | 结果 |
|------|------|
| **官方中文译名** | 官方中文文档的章节标题直接用 **"Agents"**（英文），正文中通篇保留 **"agent"**（英文小写），未翻译成"智能体" |
| **社区使用"智能体"** | 中文社区（CSDN、SegmentFault）广泛使用"智能体"一词。第三方中文文档站 `opencode.doczh.com` 将其译为"智能体" |
| **结论** | 官方文档从未将 `Agent` 翻译为"智能体"，而是保持英文原名。该书使用"智能体"是**社区约定译法，非官方标准** |

> 来源：https://open-code.ai/zh/docs/agents

### 2. "Skill（技能）" — ✅ 确认正确

| 项目 | 结果 |
|------|------|
| **官方中文译名** | 官方中文文档章节标题 **"Agent 技能"**，正文使用 **"Skills"** 或 **"skills"** |
| **结论** | "技能"作为 Skill 的中文翻译在官方文档中确认使用。✅ |

> 来源：https://open-code.ai/zh/docs/skills

### 3. "Workflow（工作流）" — ⚠️ 有误

| 项目 | 结果 |
|------|------|
| **官方文档状态** | OpenCode 官方文档**没有任何名为 "Workflow" 的一级或二级章节**。Workflow 一词仅出现在 Agents 页面的描述性语句中 |
| **与 Agent/Skill 的关系** | 官方文档中 Workflow **不是独立子系统**。Agent 编排和工作流模式是通过 Agent 配置 + Task tool + 子会话实现的 |
| **结论** | ⚠️ **非官方一等抽象**。OpenCode 官方没有 "Workflow" 作为一等核心抽象 |

> 来源：https://open-code.ai/en/docs — 完整导航目录，无 "Workflow"

### 4. "上下文工程"（Context Engineering）— ❌ 非官方子系统名称

| 项目 | 结果 |
|------|------|
| **官方文档状态** | OpenCode 官方文档**没有任何名为 "Context Engineering" 或 "上下文工程" 的章节** |
| **实际相关功能** | OpenCode 有内置的**上下文管理**功能：自动压缩、溢出检测、token 跟踪 |
| **行业背景** | "Context Engineering" 是一个独立的行业通用术语，由 Andrej Karpathy 在 2025 年提出 |
| **结论** | ❌ **非 OpenCode 官方子系统名称**。官方称为 "Context Management" |

> 来源：https://open-code.ai/en/docs — 导航无 "Context Engineering"

### 5. "约束系统"（Constraints System）— ❌ 非官方子系统名称

| 项目 | 结果 |
|------|------|
| **官方文档状态** | OpenCode 官方文档**没有任何名为 "Constraints System" 或 "约束系统" 的章节** |
| **最近似的官方子系统** | 有两个相关但独立的官方章节：**Rules（规则）**— AGENTS.md；**Permissions（权限）**— allow/deny/ask |
| **结论** | ❌ **非官方子系统名称**。真正的官方子系统是 **Rules** 和 **Permissions** |

> 来源：https://open-code.ai/en/docs/rules；https://open-code.ai/en/docs/permissions

### 6. "验证护栏体系"（Validation Harness）— ❌ 非官方子系统名称

| 项目 | 结果 |
|------|------|
| **官方文档状态** | OpenCode 官方文档**没有任何名为 "Validation Harness" 或 "验证护栏" 的章节** |
| **背景说明** | "Harness Engineering" 是 OpenAI 在 2026 年 2 月发表的一篇博客文章标题 |
| **结论** | ❌ **非官方子系统名称**。是全书的主题框架概念，非 OpenCode 平台特性 |

> 来源：https://openai.com/index/harness-engineering/

### 7. "3 级约束层级：全局/会话/任务级" — ❌ 不匹配

| 项目 | 结果 |
|------|------|
| **官方层级** | 远程（Remote）→ 全局（Global）→ 项目（Project） |
| **书中所称层级** | "全局/会话/任务级"（global/session/task-level） |
| **结论** | ❌ **术语不匹配**。官方层级为：远程级 → 全局级 → 项目级 |

> 来源：https://open-code.ai/en/docs/config

---

## 整体评估

| 维度 | 准确率 |
|------|--------|
| **完全准确** | ~20%（Skill 系统 ✅） |
| **部分有偏差** | ~20%（Agent 译名、Workflow 地位） |
| **不准确/无法确认** | ~60%（子系统命名、约束层级） |

**最严重的问题**：将行业通用概念和作者构建的分类框架包装成 OpenCode 的平台特性。读者会误以为 OpenCode 文档中有这些章节。

**注意**：上述问题涉及全书的概念框架定位，不属于本次 README 修正范围（`MUST NOT DO: Restructure the article or change the writing tone. Only fix factual errors.`）但建议在后续迭代中考量。
