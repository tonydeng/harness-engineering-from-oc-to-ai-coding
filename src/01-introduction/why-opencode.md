# 为什么选择 OpenCode

> 在 AI 编程工具百花齐放的今天，为什么 OpenCode 是承载 Harness Engineering 理念的最佳平台？——从四个核心优势和双层架构说起。

## 文章概述

当前的 AI 编程工具市场呈现"战国时代"格局：Cursor 以其编辑器内嵌体验赢得前端开发者青睐，Claude Code 以强大的终端 Agent 能力占据极客市场，GitHub Copilot 凭借生态渗透稳坐装机量第一。在这片红海中，OpenCode 凭借其独特的设计哲学杀出重围——它不仅是一个工具，更是一个"AI 编程操作系统"。

OpenCode 的四个核心优势使其成为 Harness Engineering 的理想载体：**完全开源**（167K+ GitHub Stars，社区驱动）、**Provider 自由**（支持 75+ LLM 提供商，不锁定任何一家）、**Agent 架构**（Build/Plan 分工 + @general/@explore 等内置 Agent + 自定义 Agent）、**扩展生态**（Plugin 20+ Hook 点 + MCP 协议 + Skills Marketplace）。这些特性不是偶然堆叠，而是围绕"工程化"这一核心目标设计的有机整体。

本文还将介绍 **oh-my-openagent（OMO）** 双层架构——原生的 OpenCode 提供基础 Agent 能力，OMO 在其上叠加编排层（11+ 专业 Agent、类别路由、Team Mode、Ultrawork、Hyperplan）。最后，我们会诚实讨论 OpenCode 的局限性，帮助读者做出理性的选型决策。

## 内容要点

1. **AI 编程工具全景对比** — 从开源性、Provider 自由度、Agent 类型、Plugin/扩展能力、学习曲线、隐私保护、定价模式等维度，对比 OpenCode、Cursor、Claude Code、Copilot、Continue、Tabby 六款主流工具。对比矩阵表一目了然地展示各工具的能力边界。

2. **OpenCode 的四个核心优势** — （1）完全开源：代码可审计、可定制、可自行贡献，企业级部署无后顾之忧；（2）Provider 自由：不绑定任何模型，可在 75+ Provider 间自由切换甚至混合使用，彻底消除供应商锁定风险；（3）Agent 架构：内置 Build/Plan/Explore 等多角色 Agent 体系，支持自定义 Agent，天然适配复杂任务分解；（4）扩展生态：Plugin 的 20+ Hook 点覆盖工具链全生命周期，MCP 协议连接外部服务，Skills Marketplace 共享可复用能力。

3. **Agent vs Copilot 的本质差异** — Copilot 是"补全器"：基于光标位置给出代码建议，被动响应。Agent 是"执行器"：理解任务意图后自主执行多步操作，主动完成。这是工具哲学的根本分野。

4. **OMO 双层架构** — 原生 OpenCode 能力边界（6 个核心 Agent + Skills + 基本 Workflow）vs OMO 扩展能力（11+ 专业 Agent、类别路由、Team Mode、Ultrawork、Hyperplan、53+ Hook 点）。决策树帮助判断：什么场景用原生就够了，什么场景需要 OMO。

5. **OpenCode 的局限性（诚实告知）** — （1）终端界面体验不如 Cursor 的编辑器内嵌流畅；（2）六个核心概念（Agent/Skill/Workflow 等）带来一定学习曲线；（3）远程/云端模式仍在完善中。这些局限在某些场景下可能是关键决策因素。

## 关联章节

- → [Ch3 环境搭建](../03-setup/README.md)（安装和配置的详细实操）
- → [Ch5 Skill 开发](../05-skills/README.md)（深入 Skill 系统的设计与实现）
- ← 承接 [什么是 Harness Engineer](what-is-harness-engineer.md)（理解概念后，自然延伸至工具选择）
