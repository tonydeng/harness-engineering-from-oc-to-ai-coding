# Harness Engineering 理论框架

> 从"驾驭 AI 写代码"到"设计 AI 工程流水线"——建立 Harness Engineering 的系统理论模型，为全书实践提供统一的思维框架。

## 文章概述

如果说"What is Harness Engineer"回答的是"谁"的问题，那么本文回答的是"什么"和"为什么"——Harness Engineering 的系统理论框架是什么，它是如何被提出和定义的，以及为什么在今天这个时间节点变得至关重要。本文提供了全书所有实践章节的理论基础。

Harness Engineering 的理论核心包含四个支柱：**编排（Orchestration）**——多 Agent 如何分工协作、**安全（Security）**——Agent 权限控制与审计、**可观测（Observability）**——运行过程可追踪可理解、**成本（Cost）**——Token 和 API 调用的精细化管理。这四个支柱共同构成了 Harness Engineering 的完整理论边界。

本文将介绍 Martin Fowler 的 **5 大分类法**，将 AI 编程工具分为五个类别，帮助读者建立统一的讨论坐标系。同时通过 2024 到 2026 的演进时间线，解释"为什么是现在"需要 Harness Engineering——从对话编程到 Agent 自主执行，再到 Agent 编排体系，每一次跃迁都对工程化提出了更高要求。

## 内容要点

1. **Harness Engineering 定义深化** — 从 Article 1.1 的初步概念出发，系统定义 Harness Engineering 的完整内涵：它不仅是一套工具使用方法，更是一种工程方法论。四个核心支柱（编排、安全、可观测、成本）构成理论模型的经纬度。

2. **Martin Fowler 5 大分类法** — 将 AI 编程工具分为五个类别：（1）代码补全器（Copilot、TabNine）；（2）对话式助手（Cursor Chat、Copilot Chat）；（3）终端 Agent（Claude Code、OpenCode CLI）；（4）Agent 编排平台（OpenCode + OMO）；（5）专用工具链（Codex、Cline）。每个分类的定义、典型工具和工程实践意义。

3. **演进时间线 2024→2026** — 2024：Copilot Chat + Cursor 代表对话编程时代，以交互式对话为核心交互模式。2025：Claude Code 引领 Agent 自主执行时代，AI 开始独立完成任务。2026：OpenCode + OMO 构建 Agent 编排体系，多个 Agent 协同完成复杂工程交付。每个阶段的代表工具、能力特征和工程化成熟度。

4. **三层抽象模型的雏形** — Agent（执行单元）、Skill（能力模块）、Workflow（协作流程）三层抽象是 Harness Engineering 的核心架构模式。本文建立理论基础，为 Ch2 的详细展开做铺垫。

5. **企业级落地价值** — Harness Engineering 在企业场景中的价值：可重复的交付质量（从个人经验到组织能力）、可追溯的安全合规（每一步都有审计日志）、可度量的效率改进（从"感觉快了"到数据驱动）。本节为 Ch7 案例研究埋下伏笔。

## 关联章节

- ← 承接 [什么是 Harness Engineer](what-is-harness-engineer.md)（从概念到理论的深化）
- → [AI 编程工具生态对比](ecosystem-comparison.md)（5 大分类法为工具对比提供理论框架）
- → [Ch2 核心概念](../02-core-concepts/README.md)（三层抽象模型的详细展开）
