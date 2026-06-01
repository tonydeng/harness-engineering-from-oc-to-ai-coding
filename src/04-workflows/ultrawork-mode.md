# Ultrawork 模式

> 目标驱动而非指令驱动：让 Agent 自主探索代码库、研究模式、实现功能并验证结果的全自动工作流。

## 文章概述

Ultrawork 模式是 oh-my-openagent 的旗舰工作流。它代表了一种从"精确指令"到"目标驱动"的范式转变：你不需要告诉 Agent 怎么做，只需要告诉它做什么。Agent 会自动探索代码库、研究现有模式、实现功能、通过 LSP 验证结果，然后根据结果决定下一步。

本文从原理出发，深入讲解 Ultrawork 的工作机制和适用场景。你将学习如何启用 Ultrawork 模式（对话输入 `ulw` 或设置为默认模式），以及如何配合 Ralph Loop（`/ulw-loop`）实现自我迭代直到 100% 完成。我们还通过对比表分析 Ultrawork 与传统 Prompt 方式在精准度、探索深度、Token 消耗和人工介入方面的差异，帮助你在合适的场景做出正确选择。

学习本文后，你将理解 Ultrawork 的工程价值：在不确定性和探索成本之间取得平衡。这在上下文复杂的任务、快速原型和大型重构中尤其有价值。

## 内容要点

1. **Ultrawork 的工作原理** — Agent 自主探索代码库、研究现有模式、实现功能、LSP 验证、重复的闭环机制；适用场景（上下文复杂任务、快速原型）和配置方式（`default_mode.ultrawork` + `ralph_loop`）。
2. **Ultrawork 的使用方式** — 对话中输入 `ulw` 或 `ultrawork` 激活；设置为默认模式以持续启用；配合 `/ulw-loop` 命令实现自动化迭代。
3. **Ultrawork vs 传统 Prompt** — 对比表分析精准度、探索深度、Token 消耗和人工介入四个维度的差异；给出何时 Ultrawork 优于手动 Prompt、何时需要精确控制的决策指南。
4. **Ralph Loop 机制** — `/ulw-loop` 的自引用循环原理：Agent 根据当前完成情况自主决定下一步行动，而非预设步骤的重复执行；Loop 控制参数（`max_turns`, `stop_condition`）；实用场景如单元测试覆盖率提升和持续重构。
5. **实战案例** — 使用 Ultrawork 为开源项目添加功能的全流程演示，从目标设定到最终验证的端到端示例。

## 关联章节

- ← [工作流模式](../02-core-concepts/workflow-patterns.md) — Command 触发 Ultrawork
- ← [oh-my-openagent 集成](../03-setup/oh-my-openagent-setup.md) — OMO 配置是 Ultrawork 的基础
- → [多 Agent 协作](multi-agent-collab.md) — Ultrawork 与多 Agent 协作的关系
