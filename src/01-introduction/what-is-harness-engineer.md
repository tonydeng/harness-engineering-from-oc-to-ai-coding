# 什么是 Harness Engineer

> 从"用 AI 写代码的人"到"驾驭 AI Agent 完成工程交付的人"——定义 AI 编程第三时代的核心角色。

## 文章概述

AI 编程工具在短短五年内经历了三次浪潮：从 2021 年的代码补全（GitHub Copilot），到 2024 年的对话编程（Cursor、Claude Code），再到 2026 年的工程流水线（OpenCode）。每一次浪潮都重新定义了开发者与 AI 的关系。**Harness Engineer（驾驭工程师）** 就是第三时代的核心角色——不是简单地用 AI 写代码，而是设计和管理 AI 工程流水线的人。

为什么"对话"不够？单纯依赖聊天式交互带来了四个根本性问题：Token 成本失控（长对话上下文膨胀）、跨 Session 上下文丢失（失忆问题）、生成结果质量不可控（缺乏审查机制）、以及优质工作流无法复用（重复劳动）。这些问题决定了"对话编程"只能是过渡形态，而非终局。

本文将从 AI 编程的演进脉络出发，定义 Harness Engineer 的概念与核心能力，并阐述 Harness Engineering 的三大核心原则——**可复现（Reproducible）**、**可审计（Auditable）**、**可改进（Improveable）**。这三大原则贯穿全书，是衡量一切 AI 工程实践的标准。

## 内容要点

1. **AI 编程的三次浪潮** — 1.0 代码补全（Copilot 2021，被动响应）、2.0 对话编程（Cursor/Claude Code 2024，单 Agent 聊天交互）、3.0 工程流水线（OpenCode 2026，多 Agent 编排与工具链集成）。通过时间线图和三阶段对比表清晰展示每次浪潮的核心特征与能力边界。

2. **"对话"的四个瓶颈** — Token 成本失控（长对话上下文越用越贵）、失忆问题（跨 Session 无法继承上下文）、质量不可控（缺乏 Code Review 机制）、重复劳动（工作流无法沉淀复用）。这些瓶颈是推动范式转变的根本驱动力。

3. **Harness Engineer 的核心定义** — Harness Engineer 不等于"会用 AI 写代码的工程师"。Mitchell Hashimoto 的原始定义强调"驾驭"而非"辅助"；Harrison Chase 的公式 `Agent = Model + Harness` 点明了 Agent 与工程化框架的不可分割性。本文提炼 Harness Engineer 的五大核心能力框架：需求澄清、工作流设计、Agent 编排、质量审查、知识沉淀。

4. **Harness Engineer vs Prompt Engineer** — 两者关注点截然不同：Prompt Engineer 关注"怎么写好的提示词"，Harness Engineer 关注"怎么设计好的工程流水线"。前者是战术层面的技巧，后者是战略层面的能力。

5. **三大核心原则** — 可复现（Reproducible）：同样的输入输出同样质量的输出，消除随机性和幻觉带来的不确定性。可审计（Auditable）：每一步操作有记录、可回放、可审查，确保安全可控。可改进（Improveable）：从每次运行中学习，持续优化流水线，形成正向循环。

## 关联章节

- → [Ch2 核心概念](../02-core-concepts/README.md)（为理解 Agent、Skill、Workflow 等概念奠定基础）
- → [Ch4 工作流实战](../04-workflows/README.md)（工程流水线的具体实现与最佳实践）
- ← 承接 [第 0 章 读者导航](../00-guide/README.md)（建立对全书结构的基本认知后，从这里正式开始）
