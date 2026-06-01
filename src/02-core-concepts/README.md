# 第2章：核心概念 — Agent、Skill、Workflow 的抽象世界

> 本章是全书的理论基石，深入理解 OpenCode 生态的三个核心抽象——Agent、Skill 和 Workflow，以及支撑它们高效运转的上下文工程、约束系统和验证护栏。

## 章节概述

第 2 章为你构建使用 OpenCode 必备的概念地图。我们从三个核心抽象开始：**Agent（代理）** 是执行单元，**Skill（技能）** 是领域知识包，**Workflow（工作流）** 是编排模式。在此基础上，进一步探讨上下文工程的核心技术（如何让 Agent 理解项目全貌）、约束系统的工作原理（如何精确控制 Agent 行为），以及验证护栏体系（如何确保输出质量）。掌握这些概念之后，后续章节的实战内容将事半功倍。

本章包含以下文章：

| 文章 | 说明 |
|------|------|
| [Agent 编排](agent-orchestration.md) | Agent 的生命周期、任务分配策略、多 Agent 通信机制 |
| [Skill 系统](skills-system.md) | Skill 的定义、加载机制、版本管理和权限模型 |
| [工作流模式](workflow-patterns.md) | 常见工作流模式：顺序执行、并行分派、审核循环、迭代优化 |
| [上下文工程核心](context-engineering-core.md) | 如何构建和管理 Agent 的上下文窗口，确保信息不丢失、不冗余 |
| [约束系统解析](constraints-system.md) | 约束的层级结构（全局/会话/任务级）、冲突检测与优先级规则 |
| [验证护栏体系](validation-harness.md) | 输出验证机制、自动修复循环、质量门禁的工程实现 |

> [上一页：简介](../01-introduction/) | [下一页：环境搭建 →](../03-setup/)
