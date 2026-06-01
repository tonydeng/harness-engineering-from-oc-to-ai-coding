# 多 Agent 协作

> 串行、并行、主从、竞争——四种协作模式的设计原理、配置方法和工程实践，以及完整的 7-Agent Pipeline 实现。

## 文章概述

单个 Agent 的能力再强，也有边界。多 Agent 协作的核心思想是"角色分离"：每个 Agent 只做一件事——Planner 规划不写代码，Implementor 实现不审查，Reviewer 审查不改代码。这降低了单个 Agent 的复杂度，显著提高了输出质量。

本文系统讲解四种 Agent 协作模式：串行模式（A → B → C 顺序执行）、并行模式（A 同时触发多个子 Agent 并汇总结果）、主从模式（Master 分配任务给 Slave 独立执行）和竞争模式（多个 Agent 从不同角度分析并达成共识）。然后深入 7-Agent Pipeline 的设计和实现——这是当前最成熟的多 Agent 协作方案，包含 Planner、Debater、Implementor、Reviewer、Tester、Linter 和 Commit-message 七个角色。

你还会学到 `task()` 的子 Agent 调用方法、WORKFLOW_STATE.md 的文件交接模式（比对话历史交接更可审计、可恢复）、各 Agent 的温度策略设计（Planner 0.1、Implementor 0.1、Debater 0.3 等），以及权限隔离方案（Reviewer 和 Tester 字面无法修改代码）。

## 内容要点

1. **Agent 协作的四种模式** — 串行模式（Pipeline：A → B → C 顺序执行）、并行模式（Fan-out：A 同时触发 B1/B2/B3 并汇总）、主从模式（Master 分配任务给 Slave）、竞争模式（Adversarial：多角度分析取共识）；各模式的架构特征对比（延迟 vs 吞吐 vs 一致性 vs 容错性）。
2. **使用 task() 调用子 Agent** — `task()` 的参数体系（`category`, `load_skills`, `prompt`, `description`）；子 Agent 的权限隔离设计；任务的返回值和结果合并策略。
3. **7-Agent Pipeline** — 七个角色的职责定义和协作流程；WORKFLOW_STATE.md 的文件交接模式（状态持久化、可审计、可恢复）；权限隔离设计（Reviewer/Tester 无法改代码）；温度策略（Planner 0.1、Debater 0.3、Implementor 0.1、Reviewer 0.1、Tester 0.1、Linter 0.0、Commit-message 0.3）；各 Agent 的权限矩阵和隔离策略表。
4. **质量门禁集成** — 在 Pipeline 中嵌入 Quality Gate 验证节点；工作流安全门禁模式；门禁失败时的回滚和重试策略。
5. **实战启动 Pipeline** — 完整启动命令；观察每个阶段的输出；调试和重试策略；前端场景的工作流示例（组件生成→UI 审查→响应式调整→视觉回归测试）。

## 关联章节

- ← [Ultrawork 模式](ultrawork-mode.md) — 单 Agent → 多 Agent
- → [自定义工作流](custom-workflows.md) — Team Mode 是更高级的协作形式
- ← [工作流模式](../02-core-concepts/workflow-patterns.md) — Command 触发 Pipeline
