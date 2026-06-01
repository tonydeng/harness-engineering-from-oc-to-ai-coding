# 自定义工作流

> 使用 Team Mode 和 12 个 team\_\* 工具构建自定义多 Agent 工作流，以及 Hyperplan 对抗式规划模式的设计哲学。

## 文章概述

当内置工作流不能满足你的需求时，oh-my-openagent 的 Team Mode（v4.0+）提供了完整的自定义能力。你可以创建自己的多 Agent 团队，定义它们的角色、通信方式和任务分配策略。本文是 Team Mode 的完整指南。

我们从 Team Mode 的架构概览开始，介绍可用的 Agent 类型（sisyphus / atlas / sisyphus-junior / hephaestus）和启用配置。然后逐一讲解 12 个 `team_*` 工具——从团队创建、成员管理到任务调度和通信的全套 API。接着深入两个内置 Team Skills：Hyperplan（5 个"敌对"评审者交叉批评的对抗式规划）和 security-research（5 人安全团队并行审计），理解它们的设计哲学。最后，你将学会设计自定义工作流的四个步骤（拆解→映射→配置→验证），并看到常见工作流模板和完整的实战示例。

## 内容要点

1. **Team Mode 概览** — OMO 核心创新：多 Agent 并行系统的架构设计；启用配置（`team_mode.enabled`）；可用 Agent 类型及其分工（sisyphus / atlas / sisyphus-junior / hephaestus）。
2. **12 个 team_\* 工具** — 团队管理（`team_create`, `team_delete`）；成员管理（`team_add_member`, `team_remove_member`, `team_list_members`）；通信（`team_send_message`）；任务管理（`team_task_create`, `team_task_list`, `team_task_update`, `team_task_get`）；状态查询（`team_status`, `team_list`）。
3. **内置 Team Skills** — Hyperplan：5 个"敌对"评审者交叉批评机制，目的是在写一行代码之前发现所有假设的错误；security-research：5 人安全团队（3 漏洞猎手 + 2 PoC 工程师）并行审计的设计原理。
4. **设计自定义工作流** — 工作流设计的四个步骤：拆解任务 → 映射到 Agent 角色 → 配置工作流定义 → 验证和调试；常见工作流模板（PR Review Pipeline / Security Audit / Documentation Generation）；错误处理和重试策略。
5. **实战示例** — 从需求到工作流设计的完整案例；并行与串行的选择策略（并行适合探索性任务，串行适合生产性任务，混合模式效果最佳）。
6. **Team Mode 的限制和注意事项** — 不允许嵌套团队；成员无 `delegate-task` 权限——这些设计约束都是为了防止失控。

## 关联章节

- ← [多 Agent 协作](multi-agent-collab.md) — Pipeline 是基础，Team 是升级
- ← [工作流模式](../02-core-concepts/workflow-patterns.md) — Command 触发 Team 工作流
- → [案例研究](../07-case-studies/) — Team Mode 在案例中的应用
