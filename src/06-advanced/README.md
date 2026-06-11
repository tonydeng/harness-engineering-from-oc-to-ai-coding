# 第6章：高级话题 — 深入 Harness Engineering 的深层能力

> 本章是全书最深的技术章节，涵盖上下文优化、安全加固、可观测性和生态演进等进阶主题，面向追求极致的 Power User。

## 章节概述

第 6 章是全书篇幅最大、内容最深的一章，按四个子主题组织。**核心扩展**篇补齐 MCP 服务器、自定义 Agent 和性能调优等生产级能力。**上下文与记忆**篇深入讨论 Token 经济的优化策略——上下文压缩、Token 预算、提示词缓存和记忆系统设计。**安全与沙箱**篇构筑 AI 编程的安全防线：安全总览、沙箱隔离、Hook 钩子系统和 AGENTS.md 约定系统。**运维与演进**篇探讨可观测性（日志/追踪/度量）和 Feature Flags 路线图，帮助你构建可持续演进的生产环境。

本章包含以下文章（可按兴趣跳转阅读）：

### 核心扩展 (Core Extensions)
| 文章 | 说明 |
|------|------|
| [MCP 服务器](mcp-servers.md) | 模型上下文协议的完整实现：服务器开发、工具注册和安全控制 |
| [自定义 Agent](custom-agents.md) | 基于 OpenCode Agent SDK 开发自定义 Agent 的路由、记忆和工具链 |
| [性能调优](performance-tuning.md) | Token 消耗分析、并发策略、缓存优化和延迟瓶颈排查 |

### 上下文与记忆 (Context & Memory)
| 文章 | 说明 |
|------|------|
| [上下文压缩技术](context-compression.md) | 上下文窗口的压缩算法、摘要策略和信息优先级排序 |
| [Token 预算策略](token-budget.md) | 任务级 Token 分配、超限处理和经济性分析 |
| [提示词缓存机制](prompt-caching.md) | 系统提示词和应用提示词的分层缓存设计与失效策略 |
| [记忆系统设计](memory-system.md) | 短期/长期记忆的分层架构、持久化方案和检索增强 |

### 安全与沙箱 (Security & Sandbox)
| 文章 | 说明 |
|------|------|
| [安全总览](security-overview.md) | AI 编程安全威胁模型：提示注入、权限滥用、数据泄露防护 |
| [沙箱与 Hook 系统](sandbox-hooks.md) | Agent 执行沙箱的隔离机制、Hook 事件系统和策略引擎 |
| [AGENTS.md 约定系统](agents-dot-md.md) | 项目级约定文件的定义、继承和自动化更新机制 |

### 运维与演进 (Operations & Evolution)
| 文章 | 说明 |
|------|------|
| [可观测性](observability.md) | Agent 行为的日志、追踪和指标体系设计 |
| [Feature Flags 路线图](feature-flags.md) | OpenCode 路线图中的 Feature Flags、A/B 测试和多版本策略 |

> [上一页：Skill 开发](../05-skills/) | [下一页：案例研究 →](../07-case-studies/)
