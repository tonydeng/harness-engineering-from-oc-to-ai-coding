# Harness Engineering — From OpenCode to AI Coding

将 AI 编程从"聊天对话"升级为"工程流水线"的最佳实践指南。

## 这是什么？

本项目是一本**开源书籍**，也是一份**工程实践指南**，旨在系统化地讲解如何通过 [Opencode](https://opencode.ai) 及其生态（oh-my-openagent / MCP / Skills）构建高效的 AI 编程工作流。

## 书籍大纲

书籍内容在 [`src/`](./src/) 目录下：

| 章节 | 内容 |
|------|------|
| 01-introduction | Harness Engineer 的定义、为什么需要工程化 |
| 02-core-concepts | Agent、Skill、Workflow 核心概念 |
| 03-setup | 环境搭建、配置详解 |
| 04-workflows | 典型工作流与实战模式 |
| 05-skills | Skill 开发与最佳实践 |
| 06-advanced | MCP、副驾驶、性能调优 |
| 07-case-studies | 真实案例复盘 |

## 快速开始

```bash
# 本地预览书籍
npx docsify serve ./src
```

## 目录说明

```
src/               - 书籍正文（docsify 源目录）
docs/              - 编写计划与需求文档
assets/            - 图片等静态资源
examples/          - 配套配置和代码示例
.opencode/         - oh-my-openagent 项目配置
