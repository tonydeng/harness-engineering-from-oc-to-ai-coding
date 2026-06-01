# 术语表

本术语表收录全书核心术语,按拼音字母排序,方便读者快速查阅。

## A

### Agent(智能体)

**定义**:具有自主决策能力的 AI 执行实体,能够调用工具、访问资源、执行任务。一个 Agent 包含四个核心要素:Model(模型)+ Tools(工具)+ Skills(技能)+ Memory(记忆)。

**首次出现**:[什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md)

### AGENTS.md

**定义**:OpenCode 的项目指令文件,用于定义项目的架构规范、技术栈、约束条件。它是实现架构护栏的核心载体,让 Agent "认识"项目。

**首次出现**:[工作流模式](../02-core-concepts/workflow-patterns.md)

### Architecture Guardrails(架构护栏)

**定义**:约束 Agent 架构决策的规则体系,不关心"代码写得对不对",而是关心"架构方向对不对"。通过 AGENTS.md 实现。

**首次出现**:[约束系统解析](../02-core-concepts/constraints-system.md)

## B

### Build Agent(构建代理)

**定义**:OpenCode 的默认执行模式,读写执行全能型 Agent,拥有完整的工具访问权限,适用于功能实现、代码重构、Bug 修复等场景。

**首次出现**:[Agent 编排](../02-core-concepts/agent-orchestration.md)

## C

### Command(命令)

**定义**:OpenCode 中最直观的工作流入口,将复杂的操作序列封装为简单的 `/command` 形式,让用户无需记忆繁琐步骤即可触发预设行为。

**首次出现**:[工作流模式](../02-core-concepts/workflow-patterns.md)

### Compaction(上下文压缩)

**定义**:当上下文接近窗口上限时自动触发的压缩机制,通过后台 Agent 分析当前上下文,生成摘要并选择性保留关键信息。

**首次出现**:[上下文工程核心](../02-core-concepts/context-engineering-core.md)

### Context Engineering(上下文工程)

**定义**:管理 AI Agent 有限 Token 空间的方法论,包含三个核心维度:压缩(缩减信息量)、缓存(重用已有信息)、预算(分配有限空间)。

**首次出现**:[上下文工程核心](../02-core-concepts/context-engineering-core.md)

## H

### Harness Engineering

**定义**:设计和管理 AI 工程流水线的方法论,核心是让 AI 的输出可靠、可复现、有价值。三大原则:可复现(Reproducible)、可审计(Auditable)、可改进(Improveable)。

**首次出现**:[什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md)

### Harness Engineer(驾驭工程师)

**定义**:AI 编程第三时代的核心角色,不是简单地"用 AI 写代码",而是设计和管理 AI 工程流水线的人。五大核心能力:需求澄清、工作流设计、Agent 编排、质量审查、知识沉淀。

**首次出现**:[什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md)

## M

### MCP (Model Context Protocol)

**定义**:模型上下文协议,一种标准化的外部工具接入协议,让 Agent 能够访问外部数据源和工具能力。

**首次出现**:[Agent 编排](../02-core-concepts/agent-orchestration.md)

## O

### opencode.json

**定义**:OpenCode 的配置文件,定义权限策略、工具配置、模型选择、自定义命令等项目级设置。

**首次出现**:[工作流模式](../02-core-concepts/workflow-patterns.md)

## P

### Permission Model(权限模型)

**定义**:定义 Agent "能做什么"的约束系统基础层,包含六种权限模式(allow/ask/deny/passive/restricted/inherit)和三级策略。

**首次出现**:[约束系统解析](../02-core-concepts/constraints-system.md)

### Plan Agent(规划代理)

**定义**:OpenCode 的只读分析模式,专注于需求分析、架构设计、安全审查等需要思考但不应该改动的场景。遵循"先思考后执行"原则。

**首次出现**:[Agent 编排](../02-core-concepts/agent-orchestration.md)

### Provider(模型供应商)

**定义**:提供大语言模型推理能力的服务商,如 Anthropic Claude、OpenAI GPT、Google Gemini 等,或本地部署的模型。

**首次出现**:[Agent 编排](../02-core-concepts/agent-orchestration.md)

### Prompt(提示词)

**定义**:用户输入给 AI 模型的自然语言指令。Prompt Engineer 关注"怎么写好的提示词",是战术层面的技巧。

**首次出现**:[什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md)

### Quality Gates(质量门禁)

**定义**:验证护栏的核心机制,按严重程度分为三级:硬性门禁(编译/语法/类型/安全)、质量门禁(覆盖率/规范/复杂度)、量化门禁(性能/安全评分)。

**首次出现**:[验证护栏体系](../02-core-concepts/validation-harness.md)

## S

### Skill(技能)

**定义**:OpenCode 中封装领域知识的可复用指令包,包含三个维度:知识(最佳实践)、权限(工具访问范围)、约束(输出规范)。本质是结构化指令包。

**首次出现**:[Skill 系统](../02-core-concepts/skills-system.md)

### Subagent(子代理)

**定义**:由 Primary Agent 调用的子任务执行单元,通过 `@agent-name` 语法触发,用于执行特定类型的子任务,如代码探索、通用任务等。

**首次出现**:[Agent 编排](../02-core-concepts/agent-orchestration.md)

## T

### Token

**定义**:AI 模型处理文本的基本单位,上下文窗口的容量单位。Token 空间有限而信息需求无限,是上下文工程要解决的核心矛盾。

**首次出现**:[什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md)

### Tool(工具)

**定义**:Agent 可以调用的能力集合,包括文件操作(Read/Write/Edit/Delete)、命令执行(Bash)、网络请求(WebSearch/WebFetch)、代码搜索(Grep/Glob)等。

**首次出现**:[Agent 编排](../02-core-concepts/agent-orchestration.md)

## V

### Validation Harness(验证护栏)

**定义**:确保 AI 生成代码质量的"最后一道防线",管理 Agent 的"准出"。与约束系统(管"准入")形成双翼,验证三原则:自动化、可追溯、可配置。

**首次出现**:[验证护栏体系](../02-core-concepts/validation-harness.md)

## W

### Workflow(工作流)

**定义**:将 Agent 与 Skill 组合为可重复执行流程的方法论,是 Harness Engineering 的"生产线"。从 Command 系统到高级编排模式的完整体系。

**首次出现**:[工作流模式](../02-core-concepts/workflow-patterns.md)

## Y

### YOLO 分类器

**定义**:验证护栏的智能决策核心,将操作分为高风险(阻止执行)、中风险(确认后执行)、低风险(自动执行)三类,实现智能化的门禁决策。

**首次出现**:[验证护栏体系](../02-core-concepts/validation-harness.md)

## 约束系统

**定义**:确保 Agent 行为可控的核心机制,由三大支柱构成:权限模型(能不能做)、架构护栏(怎么做)、Lint 规范(做得对)。

**首次出现**:[约束系统解析](../02-core-concepts/constraints-system.md)

---

## 术语索引

| 术语 | 英文 | 首次出现章节 |
|------|------|-------------|
| Agent | Agent | [什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md) |
| AGENTS.md | AGENTS.md | [工作流模式](../02-core-concepts/workflow-patterns.md) |
| 架构护栏 | Architecture Guardrails | [约束系统解析](../02-core-concepts/constraints-system.md) |
| Build Agent | Build Agent | [Agent 编排](../02-core-concepts/agent-orchestration.md) |
| 命令 | Command | [工作流模式](../02-core-concepts/workflow-patterns.md) |
| 上下文压缩 | Compaction | [上下文工程核心](../02-core-concepts/context-engineering-core.md) |
| 上下文工程 | Context Engineering | [上下文工程核心](../02-core-concepts/context-engineering-core.md) |
| Harness Engineering | Harness Engineering | [什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md) |
| 驾驭工程师 | Harness Engineer | [什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md) |
| MCP | Model Context Protocol | [Agent 编排](../02-core-concepts/agent-orchestration.md) |
| opencode.json | opencode.json | [工作流模式](../02-core-concepts/workflow-patterns.md) |
| 权限模型 | Permission Model | [约束系统解析](../02-core-concepts/constraints-system.md) |
| Plan Agent | Plan Agent | [Agent 编排](../02-core-concepts/agent-orchestration.md) |
| Provider | Provider | [Agent 编排](../02-core-concepts/agent-orchestration.md) |
| 提示词 | Prompt | [什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md) |
| 质量门禁 | Quality Gates | [验证护栏体系](../02-core-concepts/validation-harness.md) |
| Skill | Skill | [Skill 系统](../02-core-concepts/skills-system.md) |
| Subagent | Subagent | [Agent 编排](../02-core-concepts/agent-orchestration.md) |
| Token | Token | [什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md) |
| 工具 | Tool | [Agent 编排](../02-core-concepts/agent-orchestration.md) |
| 验证护栏 | Validation Harness | [验证护栏体系](../02-core-concepts/validation-harness.md) |
| 工作流 | Workflow | [工作流模式](../02-core-concepts/workflow-patterns.md) |
| YOLO 分类器 | YOLO Classifier | [验证护栏体系](../02-core-concepts/validation-harness.md) |
| 约束系统 | Constraints System | [约束系统解析](../02-core-concepts/constraints-system.md) |
