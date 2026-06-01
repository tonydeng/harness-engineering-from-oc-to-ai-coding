# 快速上手

> 5 分钟内完成 OpenCode 安装和第一个 AI 编程任务，感受工程化 AI 编程的基础操作。

## 文章概述

本章是全书动手的起点。之前两章讨论了"为什么要工程化"和"核心概念是什么"，现在到了"怎么做到"的时候。快速上手的定位是让读者在 5 分钟内完成 OpenCode 的安装、Provider 配置、项目初始化和第一个有意义的任务。

读完这篇文章后，你不会成为配置专家，但会理解 OpenCode 的基本操作循环：配置 Provider、启动 Session、执行任务、查看结果。更重要的是，你会理解 /init 命令为什么是项目的"出生证明"，以及安全权限控制为什么是 Harness Engineering 的第一道防线。

## 内容要点

1. **三平台安装** — macOS（Homebrew）/ Windows / Linux（npm 和官方脚本），含安装验证和常见排障。
2. **Provider 配置** — 三种接入方式：OpenCode Zen（最省心）、自有 API Key（Anthropic / OpenAI / Gemini）、GitHub Copilot 登录，按场景选择。
3. **第一个 Session** — 启动 OpenCode，/init 初始化项目生成 AGENTS.md，Plan 模式提问，Build 模式执行第一个小改动，/undo 回滚操作。
4. **常用命令速查** — /help、/connect、/init、/undo、/redo、/diff、/share、/models、/plan 的核心用法。
5. **安全检查** — edit/bash 权限控制（建议新用户先设为 ask），.opencodeignore 排除敏感目录，理解 OpenCode 的安全模型基础。

## 关联章节

- → [OpenCode 配置详解](opencode-config.md) — 基本安装后的深入配置
- ← [简介](../01-introduction/) — 前置概念理解
- ← [核心概念](../02-core-concepts/) — Agent、Skill、Workflow 基础
