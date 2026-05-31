# Agent 编排

> 理解 OpenCode 的 Agent 体系——从内置执行单元到 OMO 扩展生态，掌握任务分派与权限隔离的设计哲学。

## 文章概述

Agent 是 OpenCode 生态中一切任务执行的起点。本章节系统梳理 OpenCode 内置的 5 种 Agent 类型（Build/Plan/General/Explore/Scout），讲解 Primary Agent 与 Subagent 的分层设计如何实现权限隔离，以及 Hidden Agent 在后台完成的上下文压缩与会话管理等自动化任务。读者将理解 Plan 模式作为"先思考后执行"工程原则的具体体现，并掌握 @ 子 Agent 调用的语法与权限模型。

在 OMO 扩展部分，我们介绍 Sisyphus、Prometheus、Atlas、Hephaestus、Oracle 等专业 Agent 的职责分工，以及类别路由系统如何按任务复杂度自动分派到最优模型。本节还涵盖 Prompt 注入风险分析与 Agent 选择决策树，帮助读者根据任务特征选择合适的 Agent 组合。学完本节，读者应能独立规划多 Agent 协作方案，并理解分层设计对工程安全的意义。

## 内容要点

1. **Agent 的基本认知** — 定义 Agent 为"容器"（承载模型 + 工具 + Skill + 记忆），用操作系统进程类比建立直觉。
2. **内置 Agent 类型详解** — Build（读写执行）、Plan（只读分析）、General（通用任务）、Explore（代码探索）、Scout（快速扫描），以及 Primary/Subagent/Hidden 三层架构的职责划分。
3. **Plan 模式** — 默认拒绝所有文件编辑和命令执行的安全机制，Plan→Build 两阶段工作流的工程价值，以及 4 个典型使用场景（需求分析/架构评审/安全审查/代码审查）。
4. **@ 子 Agent 调用** — `@agent_name 任务描述` 语法，实战示例，子 Agent 的权限隔离与信任边界。
5. **OMO Agent 体系扩展** — Sisyphus（总指挥官）、Prometheus（战略规划）、Atlas（任务指挥）、Hephaestus（深度工作）、Oracle（架构顾问）等专业 Agent 的职责，以及类别路由系统的工作原理。
6. **Prompt 注入风险** — Agent 如何被注入恶意指令导致横向移动，以及防御策略。
7. **Agent 选择决策树** — 根据任务类型（分析/执行/探索/规划）选择最优 Agent 组合的操作指南。

## 关联章节

- → [工作流模式](workflow-patterns.md)：Agent 是工作流的基本执行单元，工作流编排依赖 Agent 的能力边界
- → [Skill 系统](skills-system.md)：Agent 是 Skill 的宿主，Skill 通过 Agent 加载和执行
- ← [Ch1 简介](../01-introduction/README.md)：承接"为什么需要 Harness Engineering"
- → [Ch4 工作流实战](../04-workflows/README.md)：多 Agent 协作是复杂工作流的构建基础
