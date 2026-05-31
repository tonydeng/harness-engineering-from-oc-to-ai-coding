# MCP 服务器

> MCP（Model Context Protocol）是 Agent 与外部系统通信的开放协议。理解它的工作原理、传输方式和安全模型，是扩展 AI 编程能力的关键一步。

## 文章概述

MCP 是 OpenCode 生态中让 Agent 突破工具边界的基础设施。如果把 Agent 比作执行者，MCP 就是它的"触手"——让 Agent 能够查询数据库、调用 REST API、搜索网络、操作文件系统。与 Plugin 不同，MCP 走的是"外连接"路线：Agent 通过标准协议与外部服务通信，而不是直接在进程内加载扩展。

本文从 MCP 协议的核心模型出发，讲解三种传输类型（stdio、streamable-http、websocket）的适用场景，分析 MCP 如何与 ToolRegistry 无缝集成（对 LLM 而言，内置工具和 MCP 工具没有任何区别），最后深入安全配置——包括进程隔离、环境变量管理和 OAuth 认证。读完本文，你应该能独立配置并验证至少一个自定义 MCP 服务器。

## 内容要点

1. **MCP 协议概览** — MCP 的核心概念：MCP 是 AI Agent 的"API 集成层"，定义了一套标准的工具/资源/提示接口。对比 Plugin（内扩展）与 MCP（外连接）的架构差异，展示 MCP 能做什么：数据库查询、API 调用、文件系统操作、搜索引擎、AI 服务调用等。

2. **MCP 配置详解** — 三种传输类型的配置方法与选型建议：stdio 适用于本地子进程（低延迟、高安全）、streamable-http 适用于远程服务（灵活部署、跨网络）、websocket 适用于全双工通信（实时推送、长连接）。配置格式围绕 `opencode.json` 中的 `mcpServers` 段展开，包括环境变量管理的最佳实践。

3. **MCP 与 ToolRegistry 集成** — 对 LLM 而言，内置 Tool 和 MCP Tool 完全无差别——它们共享同一套 ToolRegistry。解析 MCP Tool 的完整生命周期：注册、发现、调用、结果返回。介绍内置 OMO MCP 服务器（Exa WebSearch、Context7、Grep.app）作为参考实现。

4. **安全考虑** — MCP 服务器的进程隔离机制、环境变量分离原则（不共享 OpenCode 进程环境）、OAuth 认证配置。使用 STRIDE 方法分析 MCP 通信通道（stdio/SSE/WebSocket）的威胁面，重点关注中间人攻击和未授权访问风险。

5. **实战：配置一个自定义 MCP 服务器** — 从服务器端实现、客户端配置到功能验证的完整流程，涵盖服务端 SDK 的使用方式（Node.js/Python）。

## 关联章节

- ← [§2.1 Agent 编排](../02-core-concepts/agent-orchestration.md)（Agent 的工具调用机制）
- ← [§3.2 OpenCode 配置详解](../03-setup/opencode-config.md)（MCP 在 opencode.json 中的配置位置）
- → [§6.3 性能调优与成本管理](performance-tuning.md)（MCP 调用的性能考量）
