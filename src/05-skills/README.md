# 第5章：Skill 开发 — 封装领域知识，让 Agent 更聪明

> 本章教你如何将领域知识封装为可复用的 Skill，让 AI Agent 在特定场景下表现出专家级别的能力。

## 章节概述

Skill 是 OpenCode 生态中最具扩展性的抽象。第 5 章从 Skill 的基础创建流程开始，讲解如何将项目规范、领域术语、最佳实践打包成一个可加载的 Skill 文件。然后深入 Skill 模板系统，学会使用模板变量、条件渲染和嵌套模板来构建灵活的 Skill 体系。接着总结来自真实项目的最佳实践——如何设计 Skill 边界、如何管理 Skill 版本、如何测试 Skill 质量。最后，我们探讨两个高阶话题：**Skill-MCP 桥接**（让 Skill 调用外部工具的标准化方式）和 **Skill 插件化模式**（将 Skill 组织成可插拔的模块化系统）。

本章包含以下文章（建议按顺序阅读）：

| 文章 | 说明 |
|------|------|
| [创建 Skill](creating-skills.md) | Skill 文件结构、元数据定义、指令编写规范和加载测试 |
| [Skill 模板](skill-templates.md) | 模板语法、变量注入、条件渲染和嵌套模板的最佳实践 |
| [Skill 最佳实践](skill-best-practices.md) | Skill 设计原则、版本管理、测试策略和性能优化经验 |
| [Skill-MCP 桥接](skill-mcp-bridge.md) | 通过 MCP 协议让 Skill 调用外部 API、数据库和工具的标准化方案 |
| [Skill 插件化模式](plugin-patterns.md) | 将 Skill 设计为可插拔插件的架构模式与依赖管理 |

> [上一页：工作流实战](../04-workflows/) | [下一页：高级话题 →](../06-advanced/)
