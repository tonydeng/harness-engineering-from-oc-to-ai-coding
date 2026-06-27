# 附录 B

本附录收录 OpenCode 的内置能力与生态参考。

## 内容导航

- [OpenCode 内置能力](./opencode/capabilities.md) — OpenCode 所有内置命令、Plugin 系统、工具集的完整参考
- [OpenCode 内置命令参考](./opencode/commands.md) — 按功能分类的命令速查手册，含核心命令、OMO 扩展命令和自定义命令模板语法
- [OpenCode Plugin 系统参考](./opencode/plugins.md) — Plugin API、Hook 点、配置管理和安全实践的完整参考
- [OpenCode SDK 参考](./opencode/sdk.md) — Plugin SDK、npm SDK 与 CLI 程序化集成，含天气预报智能体案例
- [OpenCode 生态参考](./opencode/ecosystem.md) — OpenCode 开源社区项目、Skill 推荐、MCP 服务器和最佳实践

## 内容概要

**[opencode/capabilities.md](./opencode/capabilities.md)** 梳理 OpenCode 的完整内置能力，包括命令系统、Plugin 架构、内置工具集（文件操作、搜索、网络、代码分析、任务管理）、Agent 类型（Build、Plan、Explore、Scout）以及四个层面的自定义扩展方式（Skill、Command、Plugin、Agent）。适合快速了解 OpenCode "能做什么"。

**[opencode/commands.md](./opencode/commands.md)** 是 OpenCode 所有内置命令的详细参考手册。核心命令覆盖项目初始化（`/init`）、会话管理（`/compact`、`/undo`）、模型切换（`/models`）等基础操作；OMO 扩展命令提供自动化循环（`/ralph-loop`、`/ulw-loop`）、智能重构（`/refactor`）、对抗性规划（`/hyperplan`）等高级能力；自定义命令部分介绍 Markdown 文件和 JSON 配置两种创建方式，以及 `$ARGUMENTS`、`!shell`、`@file` 三种模板语法。

**[opencode/plugins.md](./opencode/plugins.md)** 是 Plugin 系统的完整参考，涵盖 `definePlugin` API 用法、20+ 个内置 Hook 点（Session、Message、Tool、Command、Permission、File、LLM、Agent、Provider 等级别）、53+ 个 OMO 扩展 Hook 点、opencode.json 配置格式、优先级与执行顺序、安全考量（风险分级、权限提升攻击面、安全 Checklist）以及 Hello World、Env Guard、自定义 Tool、Prompt 注入等快速示例。适合需要深度定制 Agent 行为的 Plugin 开发者。

**[opencode/ecosystem.md](./opencode/ecosystem.md)** 收录 OpenCode 的开源生态资源，包括社区优质项目（awesome-opencode、oh-my-openagent 等）、推荐 Skill（按开发工作流、代码质量、设计等分类）、常用 MCP 服务器以及社区最佳实践（AGENTS.md 规范、配置模板等）。适合想在 OpenCode 生态中寻找工具和参考的开发者。

**[opencode/sdk.md](./opencode/sdk.md)** 提供 OpenCode 的程序化集成参考，涵盖三种集成层次（Plugin SDK、npm SDK、CLI 程序化控制）和核心 API 速查表。通过全球天气预报智能体案例，演示外部 API 调用 → 数据规范化 → 结果验证的完整实现模式。适合需要将 OpenCode 嵌入自定义工具链或自动化流程的开发者。

## 阅读建议

本附录是**工具参考手册**，不需要通读。按你的实际需要查阅对应章节即可。

- **想快速了解 OpenCode 能做什么** → [opencode/capabilities.md](./opencode/capabilities.md)，5 分钟建立全景认知
- **想查找某个命令的用法** → [opencode/commands.md](./opencode/commands.md)，按分类速查，含示例和交叉引用
- **想开发 Plugin 或理解 Hook 机制** → [opencode/plugins.md](./opencode/plugins.md)，从 API 参考到安全实践一应俱全
- **想在 OpenCode 生态中找工具和技能** → [opencode/ecosystem.md](./opencode/ecosystem.md)，推荐社区项目、Skill 和 MCP 服务器
- **想将 OpenCode 嵌入自动化流程或自定义工具** → [opencode/sdk.md](./opencode/sdk.md)，程序化集成参考，含可运行案例

## 相关资源

`[examples/](../../examples/)` 目录包含本附录提到的配置和代码示例，包括：

- `opencode-configs/` — OpenCode 配置文件示例（basic.jsonc、plugin-config.json 等）
- `skills/` — Skill 文件示例
- `workflows/` — 工作流配置示例
- `quality-gates/` — 质量门禁配置示例

这些示例可直接复制到你的项目中使用，也可以作为自定义扩展的起点。
