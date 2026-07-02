# 附录 D

> **适合读者**: 效率追求者, Agent工程师(AE), 架构师(SYSA)

本附录收录 Pi **Agent（智能体）** 的核心能力、架构设计与生态参考。

Pi 是由 Mario Zechner（badlogicgames）创建、Earendil Inc. 维护的开源终端编码智能体工具。它强调"极简核心 + 强力扩展"的设计哲学，提供 4 个核心工具、4 种运行模式和 4 层扩展体系。截至 2026 年中，Pi 拥有 **65K+ GitHub Stars** 和 **210 万周 npm 下载量**。

## 内容导航

- [Pi Agent 概述与核心概念](./pi/overview.md) — Pi 的设计哲学、四层进化能力映射、核心架构全景
- [Pi **Agent（智能体）** 架构设计与开发指南](./pi/agent-architecture.md) — Agent Loop 模式、Extension 设计模式、Provider 路由策略、安全模型
- [CLI 命令与交互模式参考](./pi/commands.md) — 交互模式编辑器、Slash 命令、键盘快捷键、4 种运行模式
- [扩展体系详解](./pi/customization.md) — 四层扩展：Extensions、Skills、**Prompt（提示词）** Templates、Themes，以及 Pi Packages 打包分发机制
- [Pi **Agent（智能体）** SDK 与程序化集成](./pi/sdk.md) — Agent Session API、Runtime API 与 RPC 模式，含天气预报智能体案例
- [Pi SDK：编程式 **Agent（智能体）** 开发](./pi/agent-sdk.md) — SDK 嵌入模式、RPC Server 构建、多实例编排、容器化部署
- [Pi **Agent（智能体）** 生态参考](./pi/ecosystem.md) — 20+ Provider、SDK/RPC 嵌入、Containerization、社区与 Pi Packages 市场

---

## Pi vs OpenCode vs Claude Code：快速选型

在深入各章节之前，下表从 8 个关键维度对比三种工具，帮助你快速定位 Pi 的独特定位：

| 维度 | Pi Agent | OpenCode | Claude Code |
|------|----------|----------|-------------|
| **设计哲学** | 极简核心+扩展驱动 | 功能全面+Plugin 体系 | Claude 深度集成 |
| **模型支持** | 20+ Provider，324 模型 | 75+ LLM 供应商 | 仅 Claude 系列 |
| **默认工具数** | 4 个（read/write/edit/bash） | 15+（含 LSP/AST/CodeGraph） | 基础工具集 |
| **扩展机制** | Extensions/Skills/Packages | Plugin/Skill/MCP/Agent | CLAUDE.md/Skills/MCP/Subagent/Hook/Plugin |
| **SDK 模式** | 原生 TypeScript 库嵌入 | REST API（`@opencode-ai/sdk`） | 子进程控制（`@anthropic-ai/claude-agent-sdk`） |
| **独有能力** | Session Tree 分支、消息双通道、RPC 进程间通信 | OMO Category 编排、Ultrawork 循环 | Plan/Code 双模式、Claude 深度融合 |
| **定制深度** | 极高（TypeScript Extension API 可替换内置工具） | 高（Plugin Hook 系统，53+ Hook 点） | 中（指令配置 + Shell Hook） |
| **适用人群** | DIY 开发者、嵌入场景、需要极简基座的团队 | 多模型团队、复杂编排、团队标准化 | Claude 生态用户、快速上手 |

> 详细对比见 [overview.md 定位差异](./pi/overview.md#与-opencode--claude-code-的定位差异)。附录 B/C 分别提供 OpenCode 和 Claude Code 的完整参考。

## 内容概要

**[Pi **Agent（智能体）** 概述与核心概念](./pi/overview.md)** — 从 **Harness Engineering（驾驭工程）** 视角审视 Pi 的核心设计：它的极简哲学（4 工具、~1K token 系统提示）、包结构（pi-ai / pi-agent-core / pi-coding-agent / pi-tui）、与 L1-L4 四层进化能力的映射关系、以及它在 AI 编码工具生态中的独特定位。

**[CLI 命令与交互模式参考](./pi/commands.md)** — Pi 交互模式的完整参考，涵盖编辑器特性（@引用文件、!bash 执行、消息队列）、所有 Slash 命令速查表、键盘快捷键、以及 4 种运行模式（交互 / Print & JSON / RPC / SDK）。

**[Pi **Agent（智能体）** 扩展体系详解](./pi/customization.md)** — Pi 区别于其他工具的核心竞争力：TypeScript Extensions 可编写自定义工具、命令、事件处理器和 UI 组件；Skills 遵循 Agent Skills 标准提供按需能力；Prompt Templates 实现可复用提示词；Themes 支持热重载主题；Pi Packages 将全部四种扩展打包为 npm/git 可分发单元。

**[Pi **Agent（智能体）** 生态参考](./pi/ecosystem.md)** — Pi 的 Provider 生态（20+ 内置 Provider）、程序化集成方式（SDK 与 RPC 模式）、容器化沙箱方案（Gondolin / Docker / OpenShell）、以及 OSS Session 共享社区。涵盖其与 OpenCode、Claude Code 的生态对比。

**[Pi **Agent（智能体）** SDK 与程序化集成](./pi/sdk.md)** — 提供 Pi Agent 的程序化集成参考，涵盖三种集成层次（Agent Session API、Runtime API、RPC 模式）和核心 API 速查表。通过全球天气预报智能体案例，演示外部 API 调用 → 数据规范化 → 结果验证的完整实现模式。适合需要将 Pi 嵌入自定义应用或构建自动化工作流的开发者。

## 阅读建议

本附录是**独立工具参考**，适合以下读者：

- **想了解 Pi Agent 是什么** → 从 [Pi **Agent（智能体）** 概述与核心概念](./pi/overview.md) 开始，5 分钟建立全景认知
- **正在使用或准备使用 Pi** → [CLI 命令与交互模式参考](./pi/commands.md) 提供完整的操作参考
- **想扩展 Pi 的能力** → [Pi **Agent（智能体）** 扩展体系详解](./pi/customization.md) 详述四层定制机制
- **评估 Pi 是否适合你的项目** → [Pi **Agent（智能体）** 生态参考](./pi/ecosystem.md) 涵盖生态和集成场景
- **对比多种 AI 编码工具** → 结合[附录 B OpenCode](../appendix-b/) 和[附录 C Claude Code](../appendix-c/) 一起阅读
- **想将 Pi 嵌入自定义应用或构建自动化工作流** → [Pi **Agent（智能体）** SDK 与程序化集成](./pi/sdk.md)，程序化集成参考，含可运行案例

## 相关资源

- Pi 官方文档与社区：[pi.dev](https://pi.dev)
- GitHub 仓库：[earendil-works/pi](https://github.com/earendil-works/pi)
- npm 包：[`@earendil-works/pi-coding-agent`](https://www.npmjs.com/package/@earendil-works/pi-coding-agent)
