# oh-my-openagent 集成

> OMO 是叠加在 OpenCode 之上的社区编排框架，将单 Agent 能力扩展为多 Agent 协作系统。

## 文章概述

opencode.json 配好了，OpenCode 已经能完成单 Agent 任务。但 Harness Engineering 的核心是编排，而编排需要多个专业化 Agent 协同工作。oh-my-openagent（OMO）正是为此而生。它不是一个独立工具，而是一个以 Plugin 形式运行在 OpenCode 上的编排框架，类似于"操作系统内核"之上的"Shell 增强工具"。

这篇文章覆盖 OMO 的安装、架构理解和基本配置。你会了解 OMO 的 13+ 个核心 Agent（Sisyphus / Prometheus / Atlas / Hephaestus / Oracle 等）各自负责什么工作模式，类别路由如何在 OpenCode 原生路由之上叠加工作流路由和模型路由，以及 Ultrawork 和 Prometheus 模式的配置方法。读完本文，你的 OpenCode 将从"一个人的工具"升级为"一个 Agent 团队的引擎"。

## 内容要点

1. **OMO 概览** — oh-my-openagent 是什么（社区编排框架，GitHub 60K+ Stars），OMO vs 原生 OpenCode 的能力对比表，何时需要 OMO（决策树）。
2. **安装与验证** — bunx oh-my-opencode install 命令，安装向导的问答流程，bunx oh-my-opencode doctor 验证安装。
3. **OMO 架构** — 核心 Agent 体系（Sisyphus/Prometheus/Atlas/Hephaestus/Oracle），Plugin 系统如何挂载到 OpenCode，类别路由的双层设计（工作流路由 + 模型路由）。
4. **基本配置** — oh-my-openagent.jsonc 位置（全局 vs 项目），agents 配置（每个 Agent 的模型和参数），categories 配置（类别路由的模型映射），skills 配置（来源/禁用/覆盖），Ultrawork/Prometheus 模式配置。
5. **版本演进与兼容性** — v4.0 到 v4.5 核心变化速览，常见陷阱和排查方法。

## 关联章节

- ← [OpenCode 配置详解](opencode-config.md) — 需要在 opencode.json 中配置 OMO 插件
- → [工作流实战](../04-workflows/) — OMO 的工作流模式在 Ch4 深入展开
- → [MCP 服务器](../06-advanced/mcp-servers.md) — OMO 与 MCP 的协同
- → [自定义 Agent 与 Plugin](../06-advanced/custom-agents.md) — 自定义 Agent 依赖 OMO 的扩展能力
