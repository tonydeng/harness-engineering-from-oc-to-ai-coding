# 工作流模式

> 将 Agent 与 Skill 组合为可重复的执行流程——从命令快捷方式到高级编排模式的完整工作流体系。

## 文章概述

工作流是 Harness Engineering 的"生产线"。本章节从 Command 系统入手，讲解内置命令（/init、/plan、/undo、/diff、/share、/connect、/models、/help）与自定义命令的两种定义方式（推荐 Markdown 文件 vs opencode.json 配置），以及模板语法（$ARGUMENTS 参数替换、!shell 动态输出、@file 文件引用）。读者将学习如何将日常操作固化为团队共享的命令库，以及如何通过 Profile 切换适应不同工作状态（开发/审查/调试）。

AGENTS.md 是 OpenCode 工程化的核心契约文件。我们深入分析 /init 的生成机制、AGENTS.md 的金字塔结构（项目概述→技术栈→目录→命令→规范→约束），以及它在团队协作中的"Workflow as Code"角色。在高级工作流部分，我们对比 Ultrawork（自主探索→研究→实现→验证循环）和 Prometheus（访谈式规划→/start-work 精准执行）两种模式，并增加 Ralph Loop 自我迭代机制。本节还映射马书六种工作流模式与 OpenCode 的对应关系，帮助读者在不同场景下做出合理选择。

## 内容要点

1. **Command 系统** — 内置命令一览（/init、/plan、/undo 等 8 个），自定义命令的两种方式（推荐 Markdown 文件 vs opencode.json 配置），模板语法（$ARGUMENTS/!shell/@file），指定 Agent 和模型，团队共享命令库。
2. **Profile 切换** — 写代码/Code Review/Debug 三套典型 Profile 配置，`$extends` 继承机制实现配置复用，命令行选择 Profile。
3. **AGENTS.md：项目知识库** — /init 自动生成机制，"金字塔"结构（概述→技术栈→目录→命令→规范→约束），入 Git 实现项目知识持久化，作为团队开发规范的代码化载体。
4. **顺序执行与并行分派** — 单 Agent 顺序工作流的基础模式，并行分派多个 Agent 处理独立任务的编排方法，无状态并行 vs 有状态并行。
5. **审核循环与迭代优化** — 人工审核介入的工作流模式（Plan→Review→Execute），基于反馈的迭代优化闭环机制。
6. **OMO 高级工作流** — Ultrawork（"懒得想"模式：自动探索→研究→实现→验证），Prometheus（"精准执行"模式：访谈式规划→生成计划→/start-work），Ralph Loop（/ulw-loop 自我迭代直到完成）。
7. **马书工作流映射** — 调查研究模式、矛盾分析模式、集中兵力模式、实践认识模式、持久战模式与 OpenCode 工作流的对应关系，帮助读者将工程方法论落地为可执行的工作流。

## 关联章节

- ← [Agent 编排](agent-orchestration.md)：Command 调用 Agent 执行，Agent 是工作流的基本单元
- ← [Skill 系统](skills-system.md)：Command 可指定 Skill，工作流组合依赖 Skill 的能力
- → [Ch4 工作流实战](../04-workflows/README.md)：工作流模式的深入展开与团队级编排
- → [Ch5 Skill 开发](../05-skills/README.md)：自定义命令的维护与 Skill 同理
