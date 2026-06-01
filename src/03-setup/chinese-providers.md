# 国产模型供应商配置

> DeepSeek、Qwen、Kimi 等国产大模型的 API 接入方法，以及 Provider 切换策略。

## 文章概述

OpenCode 的设计哲学之一是 Provider 无关性——你不被任何模型供应商锁定。对于国内开发者来说，这意味着可以直接接入国产大模型，享受更低的 API 成本（通常为 GPT-4 的 1/10 到 1/20）和更稳定的网络连接。但国产模型的 API 格式、参数含义、Token 计算方式和内容安全策略各有不同，需要针对性配置。

这篇文章覆盖 DeepSeek、阿里 Qwen、月之暗面 Kimi 三个主流国产 Provider 的完整配置流程，包括 Base URL、API Key、模型名称等关键字段。还会讨论国产模型的典型参数调优建议、Token 计算差异、速率限制和内容安全过滤的影响，以及如何在 OpenCode 的类别路由中实现国产模型与国际模型的混合路由策略。

## 内容要点

1. **国产 AI 模型概览** — DeepSeek（性价比之王）、Kimi（长上下文优势）、Qwen（生态完整），以及其他国产 Provider 的定位对比。
2. **配置方法** — 三个 Provider 的 Base URL + API Key 配置方式，含完整 opencode.json 配置片段和支持的模型名称列表。
3. **典型参数调优** — 温度（temperature）、top_p、max_tokens 的推荐值，不同任务类型的最佳参数组合。
4. **注意事项与常见问题** — Token 计算差异（国产模型 vs 国际模型）、内容安全过滤对输出的影响、API 可用性和速率限制、网络代理设置。

## 关联章节

- ← [快速上手](quickstart.md) — Provider 配置基础
- → [性能调优与成本管理](../06-advanced/performance-tuning.md) — 国产模型在模型降级链中的应用
- ← [国产 AI 编程生态适配](../01-introduction/chinese-ecosystem.md) — 生态现状与配置前提
