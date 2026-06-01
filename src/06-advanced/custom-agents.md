# 自定义 Agent 与 Plugin

> 从 Agent 定义到 Plugin 扩展，掌握 OpenCode 生态中最灵活的定制能力——让 AI 编程流水线完全为你所用。

## 文章概述

OpenCode 的内置 Agent 已经足够强大，但在真实工程场景中，你几乎总是需要定制。也许是需要一个专门处理安全审计的 Agent（安全工具集 + 严格的权限策略），也许是想在每次文件读写前自动检查敏感信息泄露。这些需求催生了 OpenCode 的两个扩展维度：**自定义 Agent**（配置层面的组合）和 **Plugin**（代码层面的扩展）。

本文先讲解自定义 Agent 的完整流程——从 `agent.json` 或 `opencode.json` 的 `agents` 段定义，到指定角色、Skill、工具集、温度和最大轮次，再到通过 Tab 切换或 Command 指定使用。然后深入 Plugin 开发：`definePlugin` API、添加自定义 Tool（Tool 定义、注册、Agent 使用）、工具优先级（Plugin Tool > MCP Tool > Built-in Tool）、覆盖内置工具。最后以 Env Guard Plugin 作为完整示例，展示 Hook 点如何拦截和保护敏感信息。

## 内容要点

1. **自定义 Agent** — Agent 定义方式（`agent.json` / `opencode.json` `agents` 段），指定角色、Skill、工具集、温度、最大轮次等参数。探讨三种 Agent 派生模式，以及 Effort/Fast Mode/Thinking 等配置选项。自定义 Agent 的使用方式：Tab 切换或 Command 指定。OMO 自定义 Agent 配置示例。

2. **Plugin 开发基础** — `definePlugin` API 的使用，添加自定义 Tool 的三步流程：Tool 定义、注册、Agent 使用。工具优先级机制（Plugin Tool > MCP Tool > Built-in Tool）和同名覆盖内置工具的策略，分析覆盖内置工具的风险与最佳实践。

3. **Plugin Hook 点体系** — OpenCode 内置 20+ Hook 点全景（session:start/end、tool:before/after、command:before/after、permission:check），OMO 扩展的 53+ Hook 点（onWorkflowStart、onAgentSelect、onContextAssemble、onLLMRequest、onQualityGate）。Pipeline 模式的设计哲学——上一个 Hook 的输出是下一个 Hook 的输入。

4. **完整 Plugin 示例：Env Guard** — 实现一个防止敏感信息泄露的安全守卫 Plugin。使用 `preReadFile` + `preWriteFile` Hook 点，通过正则检测 AWS Key、Private Key、GitHub Token、OpenAI Key 等敏感信息。三种处理策略：mask（遮盖）、reject（拒绝）、audit（记录）。

5. **Plugin 部署和管理** — Plugin 的安装、启用/禁用、版本管理和日志调试。

## 关联章节

- ← [Agent 编排](../02-core-concepts/agent-orchestration.md)（Agent 系统基础）
- ← [Skill 系统](../02-core-concepts/skills-system.md)（Plugin 概念初探）
- ← [OpenCode 配置详解](../03-setup/opencode-config.md)（在配置中注册 Plugin）
- → [案例研究](../07-case-studies/)（自定义 Agent 在案例中的应用）
