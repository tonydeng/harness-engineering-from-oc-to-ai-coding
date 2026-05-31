# Skill 系统

> 理解 Skill 的结构规范、发现路径与加载机制——从定义领域知识包到实现精确权限控制。

## 文章概述

Skill 是 OpenCode 中封装领域知识的核心载体，它让 Agent 不必每次从零学习，而是像加载驱动程序一样按需获取专业技能。本章节详细讲解 SKILL.md 的完整格式规范，包括 frontmatter 元数据字段（name、description、allowed-tools、target_agent）、正文结构（工作流 + 指令 + 输出规范）以及捆绑资源目录（scripts/、templates/、reference/）。读者将理解 Skill 与普通 Prompt 的核心差异——权限控制、工具绑定和元数据索引——这是 Skill 能够工程化复用的根基。

Skill 的发现路径（项目级→用户级→内置）和加载机制是整个 Skill 系统的工作流核心。我们深入分析语义匹配的设计权衡——降低认知负荷的同时可能带来不精确触发——以及渐进式披露策略如何实现按需加载。在 OMO 扩展部分，我们介绍 Skills Marketplace（社区共享与版本管理）、Scoped Skills（target_agent 限定可见性）和 Skill Overrides 机制。学完本节，读者应能独立创建 Skill 文件，并为团队搭建可共享的 Skill 体系。

## 内容要点

1. **Skill 的本质** — 定义结构化指令包，与操作系统"驱动程序"的类比，Skill vs 普通 Prompt 的核心差异（权限控制、工具绑定、元数据索引）。
2. **SKILL.md 完整格式** — frontmatter 字段详解（name、description、license、metadata、allowed-tools、target_agent），正文结构（工作流 + 指令 + 输出规范），捆绑资源目录（scripts/、templates/、reference/）。
3. **发现路径与加载机制** — 项目级→用户级→内置三级搜索路径，渐进式披露策略（只读 description 语义匹配→匹配后加载正文→需要时读取捆绑资源），语义匹配示例与设计权衡。
4. **三级权限控制** — allow（自动）/ask（询问）/deny（禁止），在 opencode.json 中配置 Skill 权限，allowed-tools 字段控制工具访问范围，权限边界即攻击面的安全含义。
5. **组件↔Skill 类比** — Props = frontmatter，Composition = 编排，单一职责原则，帮助前端开发者快速理解 Skill 设计。
6. **OMO 扩展** — Skills Marketplace（社区共享与版本管理），Scoped Skills（target_agent 限定 Agent 可见性），Skill Overrides（在 OMO 配置中覆盖 SKILL.md 字段）。
7. **Skill vs Plugin** — Skill 是"教 Agent 怎么做"（指令层），Plugin 是"改 Agent 能做什么"（能力层）。
8. **Skill 使用最佳实践** — 精准编写 description 以提升匹配准确度，版本迭代维护策略，团队共享规范。

## 关联章节

- ← [Agent 编排](agent-orchestration.md)：Skill 由 Agent 加载和执行，理解 Agent 是理解 Skill 的前提
- → [工作流模式](workflow-patterns.md)：Command 可指定 Skill，工作流编排中 Skill 是能力单元
- → [Ch5 Skill 开发](../05-skills/README.md)：Skill 模板和开发实操，最佳实践的深度展开
