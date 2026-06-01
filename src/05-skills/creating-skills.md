# 创建 Skill

> 掌握 SKILL.md 格式规范、目录结构、加载机制和发布流程，从零开始创建你的第一个 Skill。

## 文章概述

Skill 是 OpenCode 生态中将领域知识封装为可复用指令的核心载体。如果说 Agent 是执行者，Skill 就是方法论——它告诉 Agent "遇到这类问题时应该怎么思考、按什么步骤做"。本文从最基础的 SKILL.md 格式出发，系统讲解一个 Skill 从创建到上线的完整生命周期。

读完本文后，读者应该能够独立编写一个结构完整的 SKILL.md 文件，理解其加载机制和发现路径，并掌握将其发布到 Skills Marketplace 的方法。本文也是后续三篇文章（模板、最佳实践、桥接、插件化）的基础。

## 内容要点

1. **SKILL.md 格式深入** — 详解 frontmatter 的必填与可选字段（name、description、allowed-tools、target_agent、metadata 等），以及正文结构的组织方式：工作流定义 + 指令编写 + 输出规范，同时介绍 scripts/ 和 templates/ 等捆绑资源的使用方法。
2. **目录结构和命名规范** — Skill 的标准目录树布局、文件命名规则（小写连字符、1-64 字符）、以及不同 Skill 类型的目录组织差异。
3. **Skill 加载机制** — 从元数据加载到按需激活的渐进式披露流程，分析描述匹配触发逻辑，并提供调试 Skill 不加载的排查技巧。
4. **Skills Marketplace 发布** — 从本地 Skill 到公开市场的发布流程、版本管理和更新通知机制，让 Skill 可以被团队或社区发现和使用。
5. **第一个 Skill 的完整创建过程** — 手把手演示从编写 SKILL.md 到加载测试的完整闭环，包含多种用途的 Skill 示例。

## 关联章节

- ← [Skill 系统](../02-core-concepts/skills-system.md)（Skill 的理论基础和设计理念）
- → [Skill 模板](skill-templates.md)（基于基础格式的模板复用）
- → [Skill 最佳实践](skill-best-practices.md)（从实践经验中提炼的设计原则）
