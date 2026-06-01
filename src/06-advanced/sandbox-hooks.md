# 沙箱与 Hook 系统

> 沙箱是 Agent 执行的"隔离区"，Hook 系统是安全策略的"传感器"。两者协同工作，构建 Agent 行为的可观测、可控制、可拦截能力。

## 文章概述

当 Agent 在开发环境中执行命令、读写文件、操作网络时，这些行为不能脱离管控。沙箱系统提供了执行层面的隔离——基于 Seatbelt（macOS）和 Bubblewrap（Linux）的进程级沙箱，限制 Agent 能接触到什么资源。Hook 系统提供了事件层面的拦截——50+ 个 Hook 点覆盖 Agent 执行的完整生命周期，让你在关键节点插入自定义逻辑。

本文先介绍沙箱系统的工作原理和配置策略，分析沙箱对性能的影响。然后深入 Hook 点体系，包括 53+ 个 Hook 点的分类（Session/Tool/Command/Permission/Workflow）、关键 Hook 点的使用场景和 Pipeline 执行模式（多个 Hook 按顺序组成处理链）。接着讲解自定义 Hook 开发——Hook 的注册、优先级设置、同步 vs 异步模式。最后讨论沙箱与 Hook 的协作模式：Hook 作为沙箱的"守卫"，事件驱动的安全策略如何实现。本文还将分析沙箱逃逸威胁场景，包括通过恶意 Hook 点绕过沙箱隔离、权限提升和资源耗尽攻击。

## 内容要点

1. **沙箱系统** — Seatbelt（macOS）和 Bubblewrap（Linux）的隔离原理（文件系统只读、网络限制、进程权限降级），沙箱的配置策略（允许/禁止的路径和命令清单），沙箱的性能影响评估（开启沙箱后的延迟增加和资源开销）。

2. **Hook 点体系** — 事件生命周期的完整时序。53+ Hook 点的五大分类：Session 级（session:start/end）、Tool 级（tool:before/after）、Command 级（command:before/after）、Permission 级（permission:check）、Workflow 级（onWorkflowStart/End）。每个分类的关键 Hook 点详解。Hook Pipeline 的执行顺序和优先级规则。

3. **自定义 Hook** — Hook 注册的 API 和配置，Pipeline 模式：多个 Hook 顺序执行，前一个输出作为后一个输入。异步 Hook vs 同步 Hook 的差异和选择依据。

4. **沙箱与 Hook 的协作** — Hook 作为沙箱的"守卫"：在执行敏感操作前通过 Hook 检查权限和安全策略。事件驱动的安全策略实现：根据 Hook 上报的事件动态调整沙箱规则。Hook 点威胁分析——哪些 Hook 点风险最高（权限提升风险分析）。

## 关联章节

- ← [安全总览](security-overview.md)（安全的执行层）
- → [自定义 Agent 与 Plugin](custom-agents.md)（Plugin 开发中的 Hook 使用）
- → [案例研究](../07-case-studies/)（案例中的安全配置）
