# 第3章：环境搭建 — 从零构建你的 AI 编程工作台

> 本章是实践起点，手把手带你完成 OpenCode 开发环境的安装、配置和集成。

## 章节概述

第 3 章解决"怎么装、怎么配、怎么用"的问题。我们从零开始：安装 OpenCode 和 oh-my-openagent、配置基础参数、连接模型供应商。然后深入 OpenCode 的配置体系，讲解主配置文件的每个关键字段。接着完成 oh-my-openagent 的集成，解锁多 Agent 编排能力。针对国内开发者，我们单独讨论国产模型供应商的配置方案。最后，给出在多环境（本地开发、CI/CD、远程服务器）下的部署最佳实践。

本章包含以下文章（建议按顺序阅读）：

| 文章 | 说明 |
|------|------|
| [快速上手](quickstart.md) | 5 分钟内完成 OpenCode 安装和第一个 AI 编程任务 |
| [OpenCode 配置详解](opencode-config.md) | opencode.json 的完整参考：Agent 定义、Skill 注册、Workflow 绑定 |
| [oh-my-openagent 集成](oh-my-openagent-setup.md) | oh-my-openagent 的安装配置与 OpenCode 的协同工作模式 |
| [国产模型供应商配置](chinese-providers.md) | 国内大模型 API 接入（DeepSeek/Qwen/GLM 等）与网络代理设置 |
| [多环境部署方案](multi-env-setup.md) | 开发/测试/生产环境的配置分离与 CI/CD 集成要点 |

> [上一页：核心概念](../02-core-concepts/) | [下一页：工作流实战 →](../04-workflows/)
