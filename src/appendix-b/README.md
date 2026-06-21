# 附录 B

本附录收录 OpenCode 和 Claude Code 的内置能力与生态参考。

## 内容导航

- [OpenCode 内置能力](./opencode/capabilities.md) — OpenCode 所有内置命令、Plugin 系统、工具集的完整参考
- [OpenCode 内置命令参考](./opencode/commands.md) — 按功能分类的命令速查手册，含核心命令、OMO 扩展命令和自定义命令模板语法
- [OpenCode Plugin 系统参考](./opencode/plugins.md) — Plugin API、Hook 点、配置管理和安全实践的完整参考
- [OpenCode Agent 架构参考](./opencode/agent-architecture.md) — OMO 三层 Agent 架构、11 个内置 Agent 详解、Category 系统和配置体系
- [OpenCode SDK 编程参考](./opencode/agent-sdk.md) — 通过 `@opencode-ai/sdk` 以 REST API 编程方式驱动 OpenCode Server，含完整数据分析 Agent 实现
- [OpenCode 生态参考](./opencode/ecosystem.md) — OpenCode 开源社区项目、Skill 推荐、MCP 服务器和最佳实践
- [Claude Code 内置能力](./claudecode/capabilities.md) — Claude Code 内置命令和功能参考
- [Claude Code 命令参考](./claudecode/commands.md) — 按功能分类的详细命令速查手册，含 Slash 命令、CLI 命令和配置参考
- [Claude Code 扩展机制](./claudecode/extensions.md) — 六层扩展体系：CLAUDE.md、Skills、MCP、Subagent、Hook、Plugin
- [Claude Code Agent 设计指南](./claudecode/agent-architecture.md) — 自定义 Agent 和 Subagent 的从入门到生产的完整教程
- [Claude Code Agent SDK 编程参考](./claudecode/agent-sdk.md) — 通过 `@anthropic-ai/claude-agent-sdk` 编程式驱动 Agent，含完整数据分析 Agent 实现
- [Claude Code 生态参考](./claudecode/ecosystem.md) — Claude Code 社区扩展、CLAUDE.md 实践、MCP 服务器生态和集成工作流

---

## OpenCode vs Claude Code 全景对比

在深入阅读各章节之前，下表从 11 个关键维度对比 OpenCode 和 Claude Code，帮助你在第一时间建立核心差异认知。

| 维度 | OpenCode | Claude Code |
|------|----------|-------------|
| **模型支持** | 20+ 种（Claude、GPT、Gemini、本地模型等 75+ LLM 供应商） | 6 种（仅 Claude 系列模型） |
| **开源性** | Apache 2.0 开源 | Proprietary 闭源 |
| **GitHub Stars** | 176K ⭐ | 133K ⭐ |
| **扩展机制** | Plugin + Skill + MCP + 自定义 Agent | 6 层体系：CLAUDE.md + Skills + MCP + Subagent + Hook + Plugin |
| **Hook 系统** | 20+ 进程内 Hook 点（OMO 扩展后 53+） | 14+ 外部 Shell 事件 |
| **SDK 能力** | REST API（`@opencode-ai/sdk`） | 子进程控制（`@anthropic-ai/claude-agent-sdk`） |
| **命令体系** | 30+ 内置命令 + 9 个 OMO 扩展命令 | 70+ Slash 命令 + 25+ CLI 命令 |
| **自定义 Agent** | OMO Category 系统 + Task API | Markdown Subagent + SDK Programmatic |
| **Agent 架构理念** | 大模型驱动编排，8 个内置 Category | 精简设计，5 种设计模式 |
| **适用场景** | 多模型混合、复杂编排、团队标准化 | Claude 深度集成、快速上手、轻量需求 |
| **适合人群** | 需要灵活扩展的工程团队 | 个人开发者、Claude 忠实用户 |

> 各维度的详细展开见对应章节。快速选型建议 → 参考下方的 [选型决策](#选型决策) 阅读路径。

---

## 内容概要

**[OpenCode 内置能力](./opencode/capabilities.md)** 梳理 OpenCode 的完整内置能力，包括命令系统、Plugin 架构、内置工具集、Agent 类型、SDK 编程接口以及四个层面的自定义扩展方式。适合快速了解 OpenCode "能做什么"。

**[OpenCode 内置命令参考](./opencode/commands.md)** 是 OpenCode 所有内置命令的详细参考手册。核心命令覆盖项目初始化（`/init`）、会话管理（`/compact`、`/undo`）、模型切换（`/models`）等基础操作；OMO 扩展命令提供自动化循环（`/ralph-loop`、`/ulw-loop`）、智能重构（`/refactor`）、对抗性规划（`/hyperplan`）等高级能力；自定义命令部分介绍 Markdown 文件和 JSON 配置两种创建方式，以及 `$ARGUMENTS`、`!shell`、`@file` 三种模板语法。

**[OpenCode Plugin 系统参考](./opencode/plugins.md)** 是 Plugin 系统的完整参考，涵盖 `definePlugin` API 用法、20+ 个内置 Hook 点（Session、Message、Tool、Command、Permission、File、LLM、Agent、Provider 等级别）、53+ 个 OMO 扩展 Hook 点、opencode.json 配置格式、优先级与执行顺序、安全考量（风险分级、权限提升攻击面、安全 Checklist）以及 Hello World、Env Guard、自定义 Tool、Prompt 注入等快速示例。适合需要深度定制 Agent 行为的 Plugin 开发者。

**[OpenCode Agent 架构参考](./opencode/agent-architecture.md)** 是 oh-my-openagent（OMO）的 Agent 架构完整技术参考。涵盖三层架构（规划层/执行层/工兵层）、11 个内置 Agent 的模型与职责、Category 系统的 8 个内置类别与自定义配置、5 层 Hook 体系、3 层 MCP 系统、工具权限矩阵、6 阶段配置管道、后台 Agent 调度和 Team Mode。适合想深入理解 OMO Agent 编排机制或在项目中复制这套架构的读者。

**[Claude Code 内置能力](./claudecode/capabilities.md)** 梳理 Claude Code 的内置命令、工具集、Agent 模式（Plan Mode / Code Mode）和 CLAUDE.md 配置方式，并通过对比表格说明 OpenCode 与 Claude Code 在模型支持、扩展机制、工具链、Hook 系统等维度的主要差异。适合想了解 Claude Code 能力或在两者之间做选型对比的读者。

**[Claude Code 命令参考](./claudecode/commands.md)** 是 Claude Code 所有命令的详细参考手册。Slash 命令覆盖会话管理、模型控制、代码审查、MCP 扩展等 12 个类别，共 70+ 个命令；CLI 命令涵盖会话启动、后台管理、MCP 管理等 25+ 个 Shell 级别命令；另有 CLI 标志速查和键盘快捷键参考。适合需要在 Claude Code 中快速查找命令用法的用户。

**[Claude Code 扩展机制](./claudecode/extensions.md)** 是 Claude Code 六层扩展体系的完整参考。从 CLAUDE.md 项目规则到 Skills 指令集、MCP 服务器、Subagent、Hooks 再到 Plugin 打包分发，逐层深入。每层包含配置格式、存储位置和关键字段说明，末尾有 Claude Code 与 OpenCode 扩展体系的对比表格。适合想深度定制 Claude Code 行为的用户。

**[Claude Code Agent 设计指南](./claudecode/agent-architecture.md)** 是 Claude Code 自定义 Agent 的从入门到生产完整教程。涵盖快速上手（创建第一个 Subagent）、Agent 设计模式（Simple/Fork/Pipeline/Hook/Batch 五种模式）、Subagent 配置参考、工具权限设计、技能组合、背景与并行模式、代码审查流水线案例，以及测试迭代方法和最佳实践。适合需要在 Claude Code 中构建自定义 Agent 工作流的开发者。

**[OpenCode SDK 编程参考](./opencode/agent-sdk.md)** 是 OpenCode 官方 SDK（`@opencode-ai/sdk`）的编程指南。涵盖 SDK 与配置式 Agent 的对比、安装与初始化、核心 API 总览（会话管理、文件搜索、配置管理、结构化输出），以及与 OMO Category 系统的对比详解。包含一个完整的数据分析 Agent——用 SDK 连接 OpenCode Server，自动扫描 CSV 文件并生成结构化分析报告。适合需要将 OpenCode 能力嵌入 CI/CD 流水线或自定义应用的开发者。

**[Claude Code Agent SDK 编程参考](./claudecode/agent-sdk.md)** 是 Claude Agent SDK（`@anthropic-ai/claude-agent-sdk`）的编程指南。涵盖 SDK 与 filesystem Subagent 的对比、query() 和 startup() 核心 API、权限模式、编程式 Subagent 定义、自定义工具（tool() + createSdkMcpServer()）、Hook 系统，以及完整的 CI/CD 集成示例。包含一个完整的数据分析 Agent——用 SDK 读取 CSV 文件、执行统计分析、生成报告并提交 PR 评论。适合需要将 Claude Code Agent 嵌入生产应用的开发者。

**[OpenCode 生态参考](./opencode/ecosystem.md)** 收录 OpenCode 的开源生态资源，包括社区优质项目（awesome-opencode、oh-my-openagent 等）、推荐 Skill（按开发工作流、代码质量、设计等分类）、常用 MCP 服务器以及社区最佳实践（AGENTS.md 规范、配置模板等）。适合想在 OpenCode 生态中寻找工具和参考的开发者。

**[Claude Code 生态参考](./claudecode/ecosystem.md)** 收录 Claude Code 的开源生态参考，包括社区扩展项目、CLAUDE.md 最佳实践（文件层级、写作原则、关键实践）、MCP 服务器生态以及 CI/CD 集成工作流。末尾提供 Claude Code 与 OpenCode 的生态对比表格。适合 Claude Code 用户或正在评估工具的读者。

---

## 术语速查

以下是本附录中频繁出现的核心术语，建议在阅读正文前快速过一遍。

| 术语 | 中文定义 |
|------|----------|
| **MCP** (Model Context Protocol) | 模型上下文协议，一种标准化协议，让 AI Agent 通过 JSON-RPC 连接外部工具、数据库和 API。 |
| **Hook** | 钩子函数，在 Agent 执行生命周期中特定事件（如文件写入、命令执行）发生时触发的回调机制。 |
| **Plugin** | 插件，通过 JavaScript/TypeScript 模块定义的扩展单元，可以注册 Hook 处理函数来定制 Agent 行为。 |
| **Skill** | 技能，一个 `SKILL.md` 文件，定义 AI 在特定任务中的行为指令、工作流和约束规则。 |
| **Subagent** | 子代理，在主 Agent 之外独立运行的轻量级 Agent 实例，用于并行执行子任务。 |
| **Agent** | 智能体，一个自主执行任务的 AI 实例，拥有独立的模型配置、工具权限和行为指令。 |
| **OMO** (oh-my-openagent) | 基于 OpenCode Plugin 系统的增强集成方案，提供三层 Agent 架构、Category 系统、53+ Hook 等扩展能力。 |
| **SDK** | 软件开发工具包（Software Development Kit），通过编程接口（REST API / 子进程）驱动 Agent 的官方库。 |
| **Category** | 类别，OMO 中的自定义 Agent 类型定义，通过 `oh-my-openagent.jsonc` 配置模型、工具权限和系统提示词。 |
| **Frontmatter** | 前置元数据，Markdown 文件开头的 YAML/JSON 格式元数据块，用于定义命令或文档的属性（如 `agent`、`model`）。 |

---

## 阅读建议

本附录是**工具参考手册**，不需要通读。按你的实际需要查阅对应章节即可。

### 新手入门

快速了解每个工具的核心能力，建立全局认知。

- **想快速了解 OpenCode 能做什么** → [OpenCode 内置能力](./opencode/capabilities.md)，5 分钟建立全景认知
- **想查找某个命令的用法** → [OpenCode 内置命令参考](./opencode/commands.md)，按分类速查，含示例和交叉引用
- **想查找 Claude Code 某个命令的用法** → [Claude Code 命令参考](./claudecode/commands.md)，按分类速查，含语法、参数和示例
- **想快速了解 Claude Code 能做什么** → [Claude Code 内置能力](./claudecode/capabilities.md)，同步了解它在命令、工具集、Agent 模式方面的基础能力

### 开发与定制

深入掌握每个工具的扩展机制，构建自定义工作流。

- **想开发 Plugin 或理解 Hook 机制** → [OpenCode Plugin 系统参考](./opencode/plugins.md)，从 API 参考到安全实践一应俱全
- **想深入理解 OMO Agent 编排机制** → [OpenCode Agent 架构参考](./opencode/agent-architecture.md)，三层架构和 11 个 Agent 详解
- **想把 OpenCode 嵌入 CI/CD 或 Web 应用** → [OpenCode SDK 编程参考](./opencode/agent-sdk.md)，REST API 编程方式
- **想深度定制 Claude Code 行为** → [Claude Code 扩展机制](./claudecode/extensions.md)，六层扩展体系从入门到精通
- **想设计 Claude Code 自定义 Agent** → [Claude Code Agent 设计指南](./claudecode/agent-architecture.md)，五种设计模式和完整案例
- **想把 Claude Code 嵌入生产应用** → [Claude Code Agent SDK 编程参考](./claudecode/agent-sdk.md)，编程式接口和自定义工具
- **想在 OpenCode 生态中找工具和技能** → [OpenCode 生态参考](./opencode/ecosystem.md)，推荐社区项目、Skill 和 MCP 服务器
- **想了解 Claude Code 的社区扩展和最佳实践** → [Claude Code 生态参考](./claudecode/ecosystem.md)，含 CLAUDE.md 写作指南和集成工作流

### 选型决策

在多工具之间做技术选型或能力评估。

- **想对比 Claude Code 和 OpenCode** → 先阅读上方的 [全景对比表格](#opencode-vs-claude-code-全景对比)，再深入 [Claude Code 内置能力](./claudecode/capabilities.md) 查看详细对比表格
- **想从生态体量评估两个工具** → [OpenCode 生态参考](./opencode/ecosystem.md) 和 [Claude Code 生态参考](./claudecode/ecosystem.md) 各有生态规模数据

---

> **📌 OMO 扩展标注说明**
>
> 本附录中，凡由 **oh-my-openagent（OMO）** 扩展提供的能力均使用以下标注方式标识：
>
> - **命令列表** — `需要 OMO` 列标记为"是"的行（参见 [OMO 扩展命令速查](./opencode/commands.md#omo-扩展命令速查)）
> - **章节标题** — 明确标注为"OMO 扩展命令"或"OMO 扩展 XXX"的专有章节
> - **Hook 点统计** — 数量表述中区分"20+ 内置 Hook 点"和"53+ OMO 扩展 Hook 点"
>
> 未标注 OMO 的能力均为 OpenCode 原生支持。安装 OMO 后，所有标注为 OMO 扩展的能力自动可用。

## 相关资源

[示例配置](../../examples/) 目录包含本附录提到的配置和代码示例，包括：

- `opencode-configs/` — OpenCode 配置文件示例（basic.jsonc、plugin-config.json 等）
- `skills/` — Skill 文件示例
- `workflows/` — 工作流配置示例
- `quality-gates/` — 质量门禁配置示例

这些示例可直接复制到你的项目中使用，也可以作为自定义扩展的起点。
