# 附录 C

本附录收录 Claude Code 的内置能力与生态参考。

## 内容导航

- [Claude Code 内置能力](./claudecode/capabilities.md) — Claude Code 内置命令和功能参考
- [Claude Code 命令参考](./claudecode/commands.md) — 按功能分类的详细命令速查手册，含 Slash 命令、CLI 命令和配置参考
- [Claude Code 扩展机制](./claudecode/plugins.md) — 六层扩展体系：CLAUDE.md、Skills、**MCP（模型上下文协议）**、Subagent、Hook、**Plugin（插件）**
- [Claude Code SDK 参考](./claudecode/sdk.md) — MCP 服务器、Hooks 与 CLI 程序化集成，含天气预报智能体案例
- [Claude Code 生态参考](./claudecode/ecosystem.md) — Claude Code 社区扩展、CLAUDE.md 实践、MCP 服务器生态和集成工作流

## 内容概要


**[claudecode/capabilities.md](./claudecode/capabilities.md)** 梳理 Claude Code 的内置命令、工具集、**Agent（智能体）** 模式（Plan Mode / Code Mode）和 CLAUDE.md 配置方式，并通过对比表格说明 OpenCode 与 Claude Code 在模型支持、扩展机制、工具链、Hook 系统等维度的主要差异。适合想了解 Claude Code 能力或在两者之间做选型对比的读者。

**[claudecode/commands.md](./claudecode/commands.md)** 是 Claude Code 所有命令的详细参考手册。Slash 命令覆盖会话管理、模型控制、代码审查、MCP 扩展等 12 个类别，共 70+ 个命令；CLI 命令涵盖会话启动、后台管理、MCP 管理等 25+ 个 Shell 级别命令；另有 CLI 标志速查和键盘快捷键参考。适合需要在 Claude Code 中快速查找命令用法的用户。

**[claudecode/plugins.md](./claudecode/plugins.md)** 是 Claude Code 六层扩展体系的完整参考。从 CLAUDE.md 项目规则到 Skills 指令集、MCP 服务器、Subagent、Hooks 再到 Plugin 打包分发，逐层深入。每层包含配置格式、存储位置和关键字段说明，末尾有 Claude Code 与 OpenCode 扩展体系的对比表格。适合想深度定制 Claude Code 行为的用户。

**[claudecode/ecosystem.md](./claudecode/ecosystem.md)** 收录 Claude Code 的开源生态参考，包括社区扩展项目、CLAUDE.md 最佳实践（文件层级、写作原则、关键实践）、MCP 服务器生态以及 CI/CD 集成工作流。末尾提供 Claude Code 与 OpenCode 的生态对比表格。适合 Claude Code 用户或正在评估工具的读者。

**[claudecode/sdk.md](./claudecode/sdk.md)** 提供 Claude Code 的程序化集成参考，涵盖三种集成层次（MCP 服务器、Hooks、CLI 程序化控制）和核心 API 速查表。通过全球天气预报智能体案例，演示外部 API 调用 → 数据规范化 → 结果验证的完整实现模式。适合需要为 Claude Code 开发自定义扩展或将其嵌入 CI/CD 流程的开发者。

## 阅读建议

本附录是**工具参考手册**，不需要通读。按你的实际需要查阅对应章节即可。

- **想查找 Claude Code 某个命令的用法** → [claudecode/commands.md](./claudecode/commands.md)，按分类速查，含语法、参数和示例
- **想深度定制 Claude Code 行为** → [claudecode/plugins.md](./claudecode/plugins.md)，六层扩展体系从入门到精通
- **想对比 Claude Code 和 OpenCode** → [claudecode/capabilities.md](./claudecode/capabilities.md)，末尾有对比表格
- **想了解 Claude Code 的社区扩展和最佳实践** → [claudecode/ecosystem.md](./claudecode/ecosystem.md)，含 CLAUDE.md 写作指南和集成工作流
- **想为 Claude Code 开发自定义扩展或嵌入 CI/CD** → [claudecode/sdk.md](./claudecode/sdk.md)，程序化集成参考，含可运行案例
