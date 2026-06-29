# Harness Engineering — From OpenCode to AI Coding

从"跟 AI 聊天写代码"到"用工程体系做开发"的最佳实践指南。

## 这是什么？

本项目是一本**开源书籍**，也是一份**工程实践指南**，旨在系统化地讲解如何通过 [OpenCode](https://opencode.ai) 及其生态（oh-my-openagent / MCP / Skills）构建高效的 AI 编程工作流。

## 书籍大纲

书籍内容在 [`src/`](./src/) 目录下：

| 章节 | 正文数 | 内容 |
|------|--------|------|
| [读者导航](src/00-guide/) | 3 | 14 种读者角色自测、阅读路径矩阵、5 分钟快速体验 |
| [简介](src/01-introduction/) | 7 | Harness Engineering 定义、AI 编程生态对比、失败案例分析 |
| [核心概念](src/02-core-concepts/) | 6 | Agent/Skill/Workflow 抽象、约束与验证护栏、上下文工程 |
| [环境搭建](src/03-setup/) | 5 | 安装配置、国产模型集成、多环境部署 |
| [工作流实战](src/04-workflows/) | 6 | Ultrawork 循环、多 Agent 协作、派生工作流模式 |
| [Skill 开发](src/05-skills/) | 5 | 创建 Skill、MCP 桥接、插件模式、Skill 市场 |
| [高级话题](src/06-advanced/) | 15 | MCP 服务器、上下文压缩、安全模型、可观测性、沙箱 |
| [案例研究](src/07-case-studies/) | 8 | 微服务、遗留系统、安全审计、全流程自动化实战 |
| [附录A 术语&参考](src/appendix-a/) | 2 | 术语解释、参考文献与延伸阅读 |
| [附录B OpenCode 能力](src/appendix-b/) | 7 | 内置命令、Agent 架构、SDK、插件生态 |
| [附录C Claude Code](src/appendix-c/) | 8 | Claude Code 能力、命令、扩展、SDK |
| [附录D Pi Agent](src/appendix-d/) | 7 | Pi Agent 概念、CLI、SDK、定制化 |

全书共 **80 篇正文**，覆盖 12 个章节/附录。

## 快速开始

```bash
# 本地预览书籍
mdbook serve
```

## 目录说明

```
src/               - 书籍正文（mdBook 源目录）
docs/              - 编写计划(planning/ 含 requirements/ plans/ sprints/ specs/)、评审(reviews/ 含 articles/ chapters/ deep-research/ overall/ archive/)、参考(reference/)、日志(logs/)
assets/            - 图片等静态资源
examples/          - 配套配置和代码示例
.opencode/         - oh-my-openagent 项目配置
