# 附录 B

本附录收录 OpenCode 和 Claude Code 的内置能力与生态参考。

## 内容导航

- [OpenCode 内置能力](./opencode/capabilities.md) — OpenCode 所有内置命令、Plugin 系统、工具集的完整参考
- [OpenCode 内置命令参考](./opencode/commands.md) — 按功能分类的命令速查手册，含核心命令、OMO 扩展命令和自定义命令模板语法
- [OpenCode Plugin 系统参考](./opencode/plugins.md) — Plugin API、Hook 点、配置管理和安全实践的完整参考
- [OpenCode 生态参考](./opencode/ecosystem.md) — OpenCode 开源社区项目、Skill 推荐、MCP 服务器和最佳实践
- [Claude Code 内置能力](./claudecode/capabilities.md) — Claude Code 内置命令和功能参考
- [Claude Code 命令参考](./claudecode/commands.md) — 按功能分类的详细命令速查手册，含 Slash 命令、CLI 命令和配置参考
- [Claude Code 扩展机制](./claudecode/plugins.md) — 六层扩展体系：CLAUDE.md、Skills、MCP、Subagent、Hook、Plugin
- [Claude Code 生态参考](./claudecode/ecosystem.md) — Claude Code 社区扩展、CLAUDE.md 实践、MCP 服务器生态和集成工作流

## 内容概要

**[opencode/capabilities.md](./opencode/capabilities.md)** 梳理 OpenCode 的完整内置能力，包括命令系统、Plugin 架构、内置工具集（文件操作、搜索、网络、代码分析、任务管理）、Agent 类型（Build、Plan、Explore、Scout）以及四个层面的自定义扩展方式（Skill、Command、Plugin、Agent）。适合快速了解 OpenCode "能做什么"。

**[opencode/commands.md](./opencode/commands.md)** 是 OpenCode 所有内置命令的详细参考手册。核心命令覆盖项目初始化（`/init`）、会话管理（`/compact`、`/undo`）、模型切换（`/models`）等基础操作；OMO 扩展命令提供自动化循环（`/ralph-loop`、`/ulw-loop`）、智能重构（`/refactor`）、对抗性规划（`/hyperplan`）等高级能力；自定义命令部分介绍 Markdown 文件和 JSON 配置两种创建方式，以及 `$ARGUMENTS`、`!shell`、`@file` 三种模板语法。

**[opencode/plugins.md](./opencode/plugins.md)** 是 Plugin 系统的完整参考，涵盖 `definePlugin` API 用法、20+ 个内置 Hook 点（Session、Message、Tool、Command、Permission、File、LLM、Agent、Provider 等级别）、53+ 个 OMO 扩展 Hook 点、opencode.json 配置格式、优先级与执行顺序、安全考量（风险分级、权限提升攻击面、安全 Checklist）以及 Hello World、Env Guard、自定义 Tool、Prompt 注入等快速示例。适合需要深度定制 Agent 行为的 Plugin 开发者。

**[claudecode/capabilities.md](./claudecode/capabilities.md)** 梳理 Claude Code 的内置命令、工具集、Agent 模式（Plan Mode / Code Mode）和 CLAUDE.md 配置方式，并通过对比表格说明 OpenCode 与 Claude Code 在模型支持、扩展机制、工具链、Hook 系统等维度的主要差异。适合想了解 Claude Code 能力或在两者之间做选型对比的读者。

**[claudecode/commands.md](./claudecode/commands.md)** 是 Claude Code 所有命令的详细参考手册。Slash 命令覆盖会话管理、模型控制、代码审查、MCP 扩展等 12 个类别，共 70+ 个命令；CLI 命令涵盖会话启动、后台管理、MCP 管理等 25+ 个 Shell 级别命令；另有 CLI 标志速查和键盘快捷键参考。适合需要在 Claude Code 中快速查找命令用法的用户。

**[claudecode/plugins.md](./claudecode/plugins.md)** 是 Claude Code 六层扩展体系的完整参考。从 CLAUDE.md 项目规则到 Skills 指令集、MCP 服务器、Subagent、Hooks 再到 Plugin 打包分发，逐层深入。每层包含配置格式、存储位置和关键字段说明，末尾有 Claude Code 与 OpenCode 扩展体系的对比表格。适合想深度定制 Claude Code 行为的用户。

**[opencode/ecosystem.md](./opencode/ecosystem.md)** 收录 OpenCode 的开源生态资源，包括社区优质项目（awesome-opencode、oh-my-openagent 等）、推荐 Skill（按开发工作流、代码质量、设计等分类）、常用 MCP 服务器以及社区最佳实践（AGENTS.md 规范、配置模板等）。适合想在 OpenCode 生态中寻找工具和参考的开发者。

**[claudecode/ecosystem.md](./claudecode/ecosystem.md)** 收录 Claude Code 的开源生态参考，包括社区扩展项目、CLAUDE.md 最佳实践（文件层级、写作原则、关键实践）、MCP 服务器生态以及 CI/CD 集成工作流。末尾提供 Claude Code 与 OpenCode 的生态对比表格。适合 Claude Code 用户或正在评估工具的读者。

## 阅读建议

本附录是**工具参考手册**，不需要通读。按你的实际需要查阅对应章节即可。

- **想快速了解 OpenCode 能做什么** → [opencode/capabilities.md](./opencode/capabilities.md)，5 分钟建立全景认知
- **想查找某个命令的用法** → [opencode/commands.md](./opencode/commands.md)，按分类速查，含示例和交叉引用
- **想开发 Plugin 或理解 Hook 机制** → [opencode/plugins.md](./opencode/plugins.md)，从 API 参考到安全实践一应俱全
- **想查找 Claude Code 某个命令的用法** → [claudecode/commands.md](./claudecode/commands.md)，按分类速查，含语法、参数和示例
- **想深度定制 Claude Code 行为** → [claudecode/plugins.md](./claudecode/plugins.md)，六层扩展体系从入门到精通
- **想对比 Claude Code 和 OpenCode** → [claudecode/capabilities.md](./claudecode/capabilities.md)，末尾有对比表格
- **想在 OpenCode 生态中找工具和技能** → [opencode/ecosystem.md](./opencode/ecosystem.md)，推荐社区项目、Skill 和 MCP 服务器
- **想了解 Claude Code 的社区扩展和最佳实践** → [claudecode/ecosystem.md](./claudecode/ecosystem.md)，含 CLAUDE.md 写作指南和集成工作流

## 相关资源

`[examples/](../../examples/)` 目录包含本附录提到的配置和代码示例，包括：

- `opencode-configs/` — OpenCode 配置文件示例（basic.jsonc、plugin-config.json 等）
- `skills/` — Skill 文件示例
- `workflows/` — 工作流配置示例
- `quality-gates/` — 质量门禁配置示例

这些示例可直接复制到你的项目中使用，也可以作为自定义扩展的起点。
