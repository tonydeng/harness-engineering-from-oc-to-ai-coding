# 附录 B

本附录收录 OpenCode 的内置能力与生态参考。

## 内容导航

- [OpenCode 内置能力](./opencode/capabilities.md) — OpenCode 所有内置命令、**Plugin（插件）** 系统、工具集的完整参考
- [OpenCode 内置命令参考](./opencode/commands.md) — 按功能分类的命令速查手册，含核心命令、OMO 扩展命令和自定义命令模板语法
- [OpenCode Plugin 系统参考](./opencode/plugins.md) — Plugin API、Hook 点、配置管理和安全实践的完整参考
- [OpenCode SDK 与程序化集成](./opencode/sdk.md) — Plugin SDK、npm SDK 与 CLI 程序化集成，含天气预报智能体案例
- [OpenCode 生态参考](./opencode/ecosystem.md) — OpenCode 开源社区项目、**Skill（技能）** 推荐、**MCP（模型上下文协议）** 服务器和最佳实践

---

## OpenCode vs Claude Code 全景对比

在深入阅读各章节之前，下表从 11 个关键维度对比 OpenCode 和 Claude Code，帮助你在第一时间建立核心差异认知。

| 维度 | OpenCode | Claude Code |
|------|----------|-------------|
| **模型支持** | 20+ 种（Claude、GPT、Gemini、本地模型等 75+ LLM 供应商） | 6 种（仅 Claude 系列模型） |
| **开源性** | Apache 2.0 开源 | Proprietary 闭源 |
| **GitHub Stars** | ~180K ⭐ | ~135K ⭐ |
| **扩展机制** | Plugin + Skill + MCP + 自定义 **Agent（智能体）** | 6 层体系：CLAUDE.md + Skills + MCP + Subagent + Hook + Plugin |
| **Hook 系统** | 20+ 进程内 Hook 点（OMO 扩展后 53+） | 14+ 外部 Shell 事件 |
| **SDK 能力** | REST API（`@opencode-ai/sdk`） | 子进程控制（`@anthropic-ai/claude-agent-sdk`） |
| **命令体系** | 30+ 内置命令 + 9 个 OMO 扩展命令 | 70+ Slash 命令 + 25+ CLI 命令 |
| **自定义 Agent** | OMO Category 系统 + Task API | Markdown Subagent + SDK Programmatic |
| **Agent 架构理念** | 大模型驱动编排，8 个内置 Category | 精简设计，5 种设计模式 |
| **适用场景** | 多模型混合、复杂编排、团队标准化 | Claude 深度集成、快速上手、轻量需求 |
| **适合人群** | 需要灵活扩展的工程团队 | 个人开发者、Claude 忠实用户 |

> 各维度的详细展开见对应章节。快速选型建议 → 参考下方的 [选型决策](#选型决策) 阅读路径。
>
> Pi Agent 的对比见[附录 D README](../appendix-d/README.md)。

---

## 内容概要

**[OpenCode 内置能力](./opencode/capabilities.md)** 梳理 OpenCode 的完整内置能力，包括命令系统、Plugin 架构、内置工具集、Agent 类型、SDK 编程接口以及四个层面的自定义扩展方式。适合快速了解 OpenCode "能做什么"。

**[OpenCode 内置命令参考](./opencode/commands.md)** 是 OpenCode 所有内置命令的详细参考手册。核心命令覆盖项目初始化（`/init`）、会话管理（`/compact`、`/undo`）、模型切换（`/models`）等基础操作；OMO 扩展命令提供自动化循环（`/ralph-loop`、`/ulw-loop`）、智能重构（`/refactor`）、对抗性规划（`/hyperplan`）等高级能力；自定义命令部分介绍 Markdown 文件和 JSON 配置两种创建方式，以及 `$ARGUMENTS`、`!shell`、`@file` 三种模板语法。

**[OpenCode Plugin 系统参考](./opencode/plugins.md)** 是 Plugin 系统的完整参考，涵盖 `definePlugin` API 用法、20+ 个内置 Hook 点（Session、Message、Tool、Command、Permission、File、LLM、Agent、Provider 等级别）、53+ 个 OMO 扩展 Hook 点、opencode.json 配置格式、优先级与执行顺序、安全考量（风险分级、权限提升攻击面、安全 Checklist）以及 Hello World、Env Guard、自定义 Tool、**Prompt（提示词）** 注入等快速示例。适合需要深度定制 Agent 行为的 Plugin 开发者。

**[OpenCode 生态参考](./opencode/ecosystem.md)** 收录 OpenCode 的开源生态资源，包括社区优质项目（awesome-opencode、oh-my-openagent 等）、推荐 Skill（按开发工作流、代码质量、设计等分类）、常用 MCP 服务器以及社区最佳实践（AGENTS.md 规范、配置模板等）。适合想在 OpenCode 生态中寻找工具和参考的开发者。

**[OpenCode SDK 与程序化集成](./opencode/sdk.md)** 提供 OpenCode 的程序化集成参考，涵盖三种集成层次（Plugin SDK、npm SDK、CLI 程序化控制）和核心 API 速查表。通过全球天气预报智能体案例，演示外部 API 调用 → 数据规范化 → 结果验证的完整实现模式。适合需要将 OpenCode 嵌入自定义工具链或自动化流程的开发者。

## 阅读建议

本附录是**工具参考手册**，不需要通读。按你的实际需要查阅对应章节即可。

- **想快速了解 OpenCode 能做什么** → [OpenCode 内置能力](./opencode/capabilities.md)，5 分钟建立全景认知
- **想查找某个命令的用法** → [OpenCode 内置命令参考](./opencode/commands.md)，按分类速查，含示例和交叉引用
- **想开发 Plugin 或理解 Hook 机制** → [OpenCode **Plugin（插件）** 系统参考](./opencode/plugins.md)，从 API 参考到安全实践一应俱全
- **想在 OpenCode 生态中找工具和技能** → [OpenCode 生态参考](./opencode/ecosystem.md)，推荐社区项目、Skill 和 MCP 服务器
- **想将 OpenCode 嵌入自动化流程或自定义工具** → [OpenCode SDK 与程序化集成](./opencode/sdk.md)，程序化集成参考，含可运行案例

## 术语速查

本附录及全书频繁出现的几个核心术语：

| 术语 | 中文 | 一句话说明 |
|------|------|-----------|
| **Agent** | 智能体 | AI 驱动的编程助手实例，可自主理解上下文、选择工具、执行操作并交付结果 |
| **MCP** | 模型上下文协议 | Model **Context（上下文）** Protocol，Agent 与外部工具/数据源交互的标准协议。Agent 通过 MCP 调用数据库、API、文件系统等 |
| **Hook** | 钩子 | Agent 生命周期的"监听点"，可在特定事件（消息发送前、工具调用后等）触发自定义逻辑。OpenCode 提供进程内 TypeScript Hook；Claude Code 提供外部 Shell Hook |
| **Plugin** | 插件 | OpenCode 的深度扩展方式，通过 TypeScript 编写 Hook 响应函数，可以监听任意 Agent 事件 |
| **Skill** | 技能 | 声明式的能力扩展，通过 Markdown 文件定义 Agent 行为规范和约束。安装即用，无需编程 |
| **Subagent** | 子智能体 | 由主 Agent 创建的子任务执行单元，可指定不同类型（oracle、explore 等）完成专项工作 |
| **Category** | 类别 | OMO 对 Subagent 的分类系统，内置 8 种（visual-engineering、ultrabrain、quick 等），各有专属模型和工具配置 |

## 相关资源

[示例配置](../../examples/) 目录包含本附录提到的配置和代码示例，包括：

- `opencode-configs/` — OpenCode 配置文件示例（basic.jsonc、plugin-config.json 等）
- `skills/` — Skill 文件示例
- `workflows/` — 工作流配置示例
- `quality-gates/` — 质量门禁配置示例

这些示例可直接复制到你的项目中使用，也可以作为自定义扩展的起点。
