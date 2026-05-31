# Skill-MCP 桥接

> 打通 Skill 的方法论与 MCP 的工具能力，让 Agent 既知道"怎么做"也有"用什么做"。

## 文章概述

Skill 擅长流程和方法论，MCP 擅长外部工具集成和数据访问。但实际开发中，一个完整的自动化任务往往同时需要两者——Skill 定义思考步骤，MCP 提供执行手段。Skill-MCP 桥接模式正是为了解决这个分工问题而设计的。

本文讲解 Skill 如何在内部工作流中调用 MCP 工具，以及如何将 MCP Server 注册为 Skill 的外部依赖。通过调查研究+WebSearch、代码审查+Git、数据查询+Database 等实战示例，展示桥接模式在不同场景下的具体配置。理解这个模式，相当于为 Skill 装上了"机械臂"——不再局限于 Agent 内置能力，可以触达任何外部系统。

## 内容要点

1. **桥接为什么必要** — Skill 擅长定义方法论和流程但缺少外部执行能力，MCP 擅长集成外部工具但不关心业务逻辑，桥接模式让两者各司其职、协同工作。
2. **桥接模式的设计方案** — Skill 内部引用 MCP Tool 的工作流写法，MCP Server 作为 Skill "外部能力层"的注册方式，以及权限边界和工具隔离的设计考量。
3. **桥接实战示例** — 调查研究 Skill + WebSearch MCP、代码审查 Skill + Git MCP、数据查询 Skill + Database MCP 的完整配置和运行流程。
4. **Skill-embedded MCPs 配置** — 在 Skill 的 SKILL.md 中直接嵌入 MCP 工具声明，让 Skill 自带外部依赖，实现"即插即用"的体验。
5. **最佳实践与反模式** — 桥接场景下的常见陷阱：Skill 过度依赖 MCP 可用性、MCP 凭证硬编码、缺乏降级策略等。

## 关联章节

- ← [§2.2 Skill 系统](../02-core-concepts/skills-system.md)（Skill 的基础概念）
- ← [§6.1 MCP 服务器](../06-advanced/mcp-servers.md)（MCP 配置和协议基础）
- → [§5.5 插件化模式](plugin-patterns.md)（桥接是插件化的前置技术）
