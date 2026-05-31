# 性能调优与成本管理

> 响应慢？Token 消耗大？错误率高？从性能瓶颈识别到成本管控策略，系统性优化你的 AI 编程流水线。

## 文章概述

当 AI 编程流水线从个人工具升级为团队基础设施时，性能和成本就成了绕不开的话题。你可能遇到过这些问题：为什么同一个任务有时候 10 秒完成、有时候要 2 分钟？Token 消耗为什么忽高忽低？模型调用费用能不能降下来？答案隐藏在 Agent 执行的每一个环节里。

本文从性能瓶颈识别入手，介绍 OpenCode 基于 54+ Event Hooks 的可观测性体系。然后深入成本管控的核心策略：Token 预算、模型降级链（Category-based Auto-downgrade）、上下文压缩（Compaction）和工具输出保护窗口。接着讲解 Hashline 编辑机制——基于 LINE#ID 内容哈希实现的零陈旧行错误编辑。最后讨论上下文优化技巧，包括 `.opencodeignore` 排除策略、本地搜索工具安装和 Session Compaction 策略选择。目标是让读者形成"测量-分析-优化-再测量"的持续调优闭环。

## 内容要点

1. **性能瓶颈识别** — 区分三类性能问题：响应慢 vs Token 消耗大 vs 错误率高。介绍 54+ Event Hooks 构建的可观测性体系如何帮助定位瓶颈，Session 日志分析方法。

2. **成本管控策略** — 成本优化的三层模型：模型选择（Type-level）、Token 预算（Session-level）、上下文压缩（Message-level）。详细讲解 Token 预算与会话级上限、Category-based Auto-downgrade 的设计意图（按任务类型智能选择模型——文档任务用便宜模型、复杂编码用高端模型）、Compaction 策略、工具输出保护窗口（保护最近 40K Token），以及各类任务的成本对比数据。

3. **Hashline 编辑** — 基于 LINE#ID 内容哈希的编辑机制，实现 0% 陈旧行错误的精确编辑。配置方法和使用场景。

4. **上下文优化** — `.opencodeignore` 排除无关文件、安装本地搜索工具（ripgrep/ast-grep）、Context7 MCP 自动查询文档、Session Compaction 策略选择。

5. **性能基准和调优案例** — 通过真实数据对比展示调优前后的性能差异。

## 关联章节

- ← [§3.2 OpenCode 配置详解](../03-setup/opencode-config.md)（成本管控是配置的一部分）
- ← [§4.1 Ultrawork 模式](../04-workflows/ultrawork-mode.md)（工作流效率与 Token 消耗的平衡）
- → [§7 案例研究](../07-case-studies/README.md)（大型案例中的成本考量）
