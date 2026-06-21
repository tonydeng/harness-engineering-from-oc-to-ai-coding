# OpenCode 内置能力

OpenCode 是一个终端原生的 AI 编程助手，支持多种 LLM Provider，内置丰富的命令、工具和扩展机制。本章是 OpenCode 能力的**全景索引**——每项能力的详细参考在对应子章节。

## 设计哲学

OpenCode 的核心设计理念：**让 AI 在你的终端里干活，而不是替你干活**。它不是一个黑盒 IDE 插件，而是一个透明的协作环境。你能看到 AI 的每一步操作，随时介入，随时纠正。

<!-- mdBook TOC 会自动生成目录，此处不需要手动列出子章节 -->

## 命令系统

OpenCode 的命令以 `/` 开头，在输入框中直接输入即可执行。命令分为三类：

- **核心内置命令**：由 OpenCode 本体提供，覆盖项目初始化（`/init`）、会话管理（`/compact`、`/undo`）、模型切换（`/models`）、Provider 管理（`/connect`）等基础操作。
- **OMO 扩展命令**：由 oh-my-openagent 插件提供，包括自动化循环（`/ralph-loop`、`/ulw-loop`）、智能重构（`/refactor`）、对抗性规划（`/hyperplan`）等高级能力。
- **自定义命令**：通过 Markdown 文件或 JSON 配置创建，支持 `$ARGUMENTS`、`!shell`、`@file` 三种模板语法。

→ 完整命令列表、参数说明和示例见 [OpenCode 内置命令参考](./commands.md)。

## 工具集

OpenCode 内置了一套完整的工具集，涵盖文件操作（Read / Write / Edit / Glob）、命令执行（Bash）、搜索（Grep / AST-grep）、网络（WebSearch / WebFetch / GitHub Search）、代码分析（LSP）、任务管理（Task / Todo），以及 `apply_patch`、`skill`、`agent` 等辅助工具。

→ 完整工具列表和用法见 [OpenCode 内置命令参考](./commands.md)。
→ 官方文档参见 [opencode.ai/docs/tools](https://opencode.ai/docs/tools/)。

## Agent 架构

OpenCode 采用多 Agent 架构：**Build**（默认主 Agent，完整权限）、**Plan**（只读主 Agent）、**General**（通用子 Agent）、**Explore**（只读探索子 Agent）、**Scout**（Web 检索子 Agent），以及若干系统级 Hidden Agent（Compaction / Title / Summary）。

→ OMO 完整 Agent 架构（含 11 个 Agent 详解、Category 系统、配置管道）见 [OpenCode Agent 架构参考](./agent-architecture.md)。
→ Agent 设计哲学和基础类型体系见 [Agent 编排](../../02-core-concepts/agent-orchestration.md)。

## Plugin 系统

Plugin 是 OpenCode 的核心扩展机制。通过 JavaScript/TypeScript 模块定义 Hook 处理函数，在工具调用生命周期中注入自定义逻辑。OpenCode 原生支持约 20 个 Hook 点（命令执行、文件写入、会话管理等），OMO 扩展后增至 50+。

Plugin 通过 `opencode.json` 的 `plugins` 字段或文件系统加载，支持本地文件和 npm 包两种方式。

→ Plugin API、Hook 点列表、安全实践详见 [OpenCode Plugin 系统参考](./plugins.md)。

## SDK 编程接口

OpenCode 提供 `@opencode-ai/sdk` 包，通过 REST API 以编程方式控制 OpenCode Server。适用于 CI/CD 集成、Web 应用嵌入和自定义工作流自动化。

→ SDK 安装、API 参考和完整示例见 [OpenCode SDK 编程参考](./agent-sdk.md)。

## Skill 系统

Skill 是轻量级的扩展方式——一个 `SKILL.md` 文件，定义 AI 的行为指令和工作流。可放置于 `.opencode/skills/`（全局或项目级），支持通过 `npx skills` CLI 安装社区 Skill。

→ Skill 开发指南见 [Skill 开发](../../05-skills/)。

## MCP 集成

MCP（Model Context Protocol）是连接外部世界的标准化协议。通过 MCP，Agent 可以查询数据库、调用 API、搜索网络，支持 stdio / streamable-http / websocket 三种传输方式。

→ MCP 配置和实践指南见 [MCP 服务器](../../06-advanced/mcp-servers.md)。

## 配置体系

OpenCode 的配置以 `opencode.json` 为核心，支持全局（`~/.config/opencode/`）、项目（`./`）、环境（`opencode.{env}.json`）三层继承，定义 Provider、权限、MCP 服务器等全局设置。

→ 配置详解见 [配置详解](../../03-setup/opencode-config.md)。

## 社区生态

社区驱动的开源生态，涵盖 Skills、配置模板、MCP 服务器等资源。社区 Skill 可通过 `skills-download` 命令安装，`examples/` 目录包含 74+ 个示例文件。

→ 社区资源列表见 [生态参考](./ecosystem.md)。

## 版本参考

本书基于 OpenCode v1.17.x 和 oh-my-openagent v4.7.x 编写。
