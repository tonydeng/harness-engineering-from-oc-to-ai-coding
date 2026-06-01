# 多环境部署方案

> 开发、CI/CD、生产环境的配置分离与 Profile 继承机制的最佳实践。

## 文章概述

个人开发者在笔记本上跑 OpenCode 和团队在生产环境中运行 OpenCode 是两回事。不同环境对模型选择、权限级别、Token 预算、安全策略有完全不同的需求。本地开发可能用低成本模型加高权限，CI/CD 需要低权限加快速模型，生产环境则要求严格权限控制和高 Token 预算。

OpenCode 的 Profile 系统通过 $extends 继承机制优雅地解决了这个问题。你可以定义一个 Base Profile 包含公共配置，然后为每个环境创建派生 Profile，只覆盖需要差异化的部分。这篇文章从 Profile 继承的设计模式出发，给出本地开发、CI/CD 流水线、生产环境三套完整模板，并讨论团队级 Git 管理的配置治理、Secret Store 集成和多环境测试策略。

## 内容要点

1. **多环境部署的挑战** — 不同环境需要不同的模型、权限、Token 预算；配置泄漏风险（生产环境的 API Key 保护）。
2. **Profile 切换的高级用法** — $extends 继承机制实现 Base 到 Dev/CI/Production 的层层覆盖；环境变量注入区分环境；CLI flag 临时覆盖。
3. **三套环境模板** — 本地开发（高权限、低成本模型）、CI/CD（低权限、快速模型）、生产环境（严格权限、高 Token 预算）的完整配置示例。
4. **团队级配置管理** — Git 管理的 opencode.json 治理流程、Secret Store 集成（Kubernetes Secret / HashiCorp Vault）、多环境测试策略。

## 关联章节

- ← [OpenCode 配置详解](opencode-config.md) — Profile 配置基础
- → [性能调优与成本管理](../06-advanced/performance-tuning.md) — 环境相关的成本管控配置
- → [工作流实战](../04-workflows/) — 不同环境使用不同的工作流模式
