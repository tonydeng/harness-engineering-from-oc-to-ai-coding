# OpenCode 配置详解

> opencode.json 的完整参考：从 Agent 定义到安全模型，理解配置即代码的设计哲学。

## 文章概述

快速上手之后，你的 OpenCode 已经能跑了。但"能跑"和"好用"之间隔着一个配置文件的深度理解。opencode.json 不仅是参数列表，更是一个声明式的工程流水线定义文件。它的分层设计（全局→项目→环境变量→CLI flag）允许团队将配置纳入版本控制，实现配置可审计、可复现。

这篇文章逐一拆解配置文件的每个关键段：agents 定义、skills 注册、mcpServers 集成、权限规则引擎、成本管控策略，以及最重要的类别路由系统。类别路由（Category Routing）决定了 Agent 如何根据任务类型自动分派到合适的模型，是整个工作流引擎的调度核心。读完本文，你将能够手写或评审一份工程级的 opencode.json 配置。

## 内容要点

1. **配置范围与合并逻辑** — 全局 ~/.config/opencode/config.json、项目 .opencode/config.json、环境变量、CLI flag 的四层覆盖机制和 mergeDeep 规则。
2. **关键配置段详解** — agents（自定义 Agent）、commands（命令注册）、skills（Skill 来源与权限）、plugins（插件）、mcpServers（外部 MCP 服务）、permissions（权限规则）、profiles（工作状态切换）、defaults（运行时默认值）。
3. **类别路由系统** — 按任务复杂度/领域自动分派，路由类别（quick / plan / research / review / deploy / document / security）与模型路由（visual-engineering / ultrabrain / artistry / deep / quick / writing）的双层映射。
4. **四层安全架构** — 权限分层、Skill 隔离、沙箱隔离、注入防御；Permission Rule 引擎的 allow/deny/ask + glob 匹配 + 优先级；敏感文件默认保护（.env、node_modules）；Bash 白名单配置。
5. **成本管控** — Token 预算与会话级上限、模型降级链（Category-based Auto-downgrade）、上下文压缩（Compaction）策略。

## 关联章节

- ← [§3.1 快速上手](quickstart.md) — 基础配置的深化
- → [§4 工作流实战](../04-workflows/README.md) — 工作流模式依赖正确的类别路由配置
- → [§6.3 性能调优与成本管理](../06-advanced/performance-tuning.md) — 成本管控配置的进阶应用
