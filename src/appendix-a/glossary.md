# 术语表

本术语表收录全书使用的专业术语，按拼音字母排序，方便读者快速查阅。每个术语包含三部分信息：英文原名、中文翻译、一句话定义。遇到不熟悉的概念时，可以在这里快速查找对应的解释和首次出现的章节。

> **⏱ 时间有限？先读这些：** **Agent（智能体）** → AGENTS.md → Build Agent → Command → Feature Flag → **Skill（技能）** → Ultrawork → **Workflow（工作流）**

## A

### Agent(智能体)

**定义**:具有自主决策能力的 AI 执行实体,能够调用工具、访问资源、执行任务。一个 Agent 包含四个核心要素:Model(模型)+ Tools(工具)+ Skills(技能)+ Memory(记忆)。

> **人话**: 能自己干活的小助手

**首次出现**:[什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md)

### AGENTS.md

**定义**:OpenCode 的项目指令文件,用于定义项目的架构规范、技术栈、约束条件。它是实现架构护栏的核心载体,让 Agent "认识"项目。

> **人话**: 告诉 Agent 项目怎么做的说明书

**首次出现**:[工作流模式](../02-core-concepts/workflow-patterns.md)

### Architecture Guardrails(架构护栏)

**定义**:约束 Agent 架构决策的规则体系,不关心"代码写得对不对",而是关心"架构方向对不对"。通过 AGENTS.md 实现。

> **人话**: 管架构方向不管代码细节的规则

**首次出现**:[约束系统解析](../02-core-concepts/constraints-system.md)

## B

### Build Agent(构建代理)

**定义**:OpenCode 的默认执行模式,读写执行全能型 Agent,拥有完整的工具访问权限,适用于功能实现、代码重构、Bug 修复等场景。

> **人话**: 权限最大的全能型 Agent，适合写代码干活

**首次出现**:[Agent 编排](../02-core-concepts/agent-orchestration.md)

## C

### Command(命令)

**定义**:OpenCode 中最直观的工作流入口,将复杂的操作序列封装为简单的 `/command` 形式,让用户无需记忆繁琐步骤即可触发预设行为。

> **人话**: 把复杂操作变成一句话

**首次出现**:[工作流模式](../02-core-concepts/workflow-patterns.md)

### Compaction(上下文压缩)

**定义**:当上下文接近窗口上限时自动触发的压缩机制,通过后台 Agent 分析当前上下文,生成摘要并选择性保留关键信息。

> **人话**: 记不住时就总结一下

**首次出现**:[上下文工程核心](../02-core-concepts/context-engineering-core.md)

### **Context Engineering（上下文工程）**(上下文工程)

**定义**:管理 AI Agent 有限 Token 空间的方法论,包含三个核心维度:压缩(缩减信息量)、缓存(重用已有信息)、预算(分配有限空间)。

> **人话**: 管好 AI 的有限记忆空间

**首次出现**:[上下文工程核心](../02-core-concepts/context-engineering-core.md)

### Category Routing(分类路由)

**定义**:根据任务类型(代码生成、调试、重构等)自动选择最合适的模型和配置,实现任务级别的智能调度。

> **人话**: 根据任务类型自动选模型的调度器

**首次出现**:[自定义 Agent 与 **Plugin（插件）**](../06-advanced/custom-agents.md)

## F

### Feature Flag(功能开关)

**定义**:一种渐进式交付机制,新功能以 Flag 形式隐藏在代码中,按需开启或关闭,而不是等到全部开发完成才一次发布。

> **人话**: 不用改代码就能开关功能的开关

**首次出现**:[Feature Flags 路线图](../06-advanced/feature-flags.md)

### 反馈循环（Feedback Loop）

**定义**:Agent 行为质量控制的闭环验证机制。每次 Agent 执行后，通过独立的验证步骤检查输出质量，将验证结果反馈回系统，驱动下一次执行的改进。反馈循环是 L3 驾驭工程到 L4 循环工程的关键桥梁。

> **人话**: 做完一步就检查一步，把检查结果用来改进下一步

**首次出现**:[性能调优](../06-advanced/context/performance-tuning.md)

## G

### Generator-Evaluator 模式

**定义**:将"生成"与"验证"职责分离给不同 Agent 的架构决策模式。生成 Agent（Generator）负责输出代码或内容，验证 Agent（Evaluator）独立评估输出质量。这是 Agent 工程中最有影响力的架构决策。

> **人话**: 写代码的 Agent 和检查代码的 Agent 分开，避免自己检查自己

**首次出现**:[Ultrawork 模式](../04-workflows/ultrawork-mode.md)

## H

### 后台任务（Background Task）

**定义**:通过 `delegate_task(run_in_background: true)` 启动的异步子 Agent 执行单元，在后台独立运行，不阻塞父 Agent。任务完成后通过系统通知触发结果收集。

> **人话**: 让子 Agent 在后台默默干活，不耽误你继续做其他事情

**相关概念**:
- **后台任务 ID（`bg_xxx`）**:标识一次后台执行，用于收集结果
- **延续会话 ID（`ses_xxx`）**:标识子 Agent 会话，用于继续对话

**首次出现**:[多 Agent 协作](../04-workflows/multi-agent-collab.md#后台任务机制)

### **Harness Engineering（驾驭工程）**

**定义**:设计和管理 AI 工程流水线的方法论,核心是让 AI 的输出可靠、可复现、有价值。三大原则:可复现(Reproducible)、可审计(Auditable)、可改进(Improveable)。

> **人话**: 让 AI 编程可靠可控的方法论

**首次出现**:[什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md)

### Harness Engineer(驾驭工程师)

**定义**:AI 编程第三时代的核心角色,不是简单地"用 AI 写代码",而是设计和管理 AI 工程流水线的人。五大核心能力:需求澄清、工作流设计、Agent 编排、质量审查、知识沉淀。

> **人话**: 不是'用 AI 写代码'的人，是'设计 AI 工作流'的人

**首次出现**:[什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md)

## M

### **MCP（模型上下文协议）** (Model Context Protocol)

**定义**:模型上下文协议,一种标准化的外部工具接入协议,让 Agent 能够访问外部数据源和工具能力。

> **人话**: Agent 连接外部工具的标准化接口

**首次出现**:[Agent 编排](../02-core-concepts/agent-orchestration.md)

### March of Nines / 九个九的征程

**定义**:AI 系统可靠性提升的成本曲线规律——每提升一个"9"的可靠性（从 90% 到 99%、99% 到 99.9%，以此类推），所需投入的成本等于之前所有"9"的总和。这一规律决定了 Agent 自主度的演进是渐进的，也解释了为什么 L4 完全自主在当前仍是长期目标。

> **人话**: 可靠性爬坡越往后越贵——从 99% 到 99.9% 花的钱，和从 0% 到 99% 一样多

**首次出现**:[什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md)

### 模型路由（Model Routing）

**定义**:根据任务类型（代码生成、调试、重构、文件读取等）智能选择最合适的 AI 模型和配置的策略机制。与供应商路由（Provider Routing）在供应商级别容错不同，模型路由在任务级别做最优匹配，是成本管控和效率优化的核心手段。

> **人话**: 根据任务类型自动选最合适的模型，不浪费钱也不委屈任务

**首次出现**:[Agent 编排](../02-core-concepts/agent-orchestration.md)

## O

### opencode.json

**定义**:OpenCode 的配置文件,定义权限策略、工具配置、模型选择、自定义命令等项目级设置。

> **人话**: OpenCode 的总配置文件

**首次出现**:[工作流模式](../02-core-concepts/workflow-patterns.md)

## P

### Permission Model(权限模型)

**定义**:定义 Agent "能做什么"的约束系统基础层,包含六种权限模式(allow/ask/deny/passive/restricted/inherit)和三级策略。

> **人话**: 管 Agent 能不能做的规则

**首次出现**:[约束系统解析](../02-core-concepts/constraints-system.md)

### Plan Agent(规划代理)

**定义**:OpenCode 的只读分析模式,专注于需求分析、架构设计、安全审查等需要思考但不应该改动的场景。遵循"先思考后执行"原则。

> **人话**: 只动脑不动手的 Agent，适合分析和设计

**首次出现**:[Agent 编排](../02-core-concepts/agent-orchestration.md)

### Plugin(插件)

**定义**:OpenCode 中代码层面的扩展点,通过 Hook 系统拦截和修改 Agent 的行为。Plugin 运行在 Agent 进程内,可以添加自定义工具、拦截文件操作、修改 LLM 请求等。核心 API 为 `definePlugin`。

> **人话**: 改 Agent 行为逻辑的代码扩展

**首次出现**:[自定义 Agent 与 Plugin](../06-advanced/custom-agents.md)

### Provider(模型供应商)

**定义**:提供大语言模型推理能力的服务商,如 Anthropic Claude、OpenAI GPT、Google Gemini 等,或本地部署的模型。

> **人话**: 提供 AI 模型的服务商

**首次出现**:[Agent 编排](../02-core-concepts/agent-orchestration.md)

### Provider Routing(供应商路由)

**定义**:当首选模型供应商不可用或响应异常时,自动切换到备用供应商的容错机制。

> **人话**: 模型出错了自动换一个

**首次出现**:[自定义 Agent 与 Plugin](../06-advanced/custom-agents.md)

### **Prompt（提示词）**(提示词)

**定义**:用户输入给 AI 模型的自然语言指令。Prompt Engineer 关注"怎么写好的提示词",是战术层面的技巧。

> **人话**: 你对 AI 说的话

**首次出现**:[什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md)

### Quality Gates(质量门禁)

**定义**:验证护栏的核心机制,按严重程度分为三级:硬性门禁(编译/语法/类型/安全)、质量门禁(覆盖率/规范/复杂度)、量化门禁(性能/安全评分)。

> **人话**: 代码入库前必须过的关卡

**首次出现**:[验证护栏体系](../02-core-concepts/validation-harness.md)

## S

### Skill(技能)

**定义**:OpenCode 中封装领域知识的可复用指令包,包含三个维度:知识(最佳实践)、权限(工具访问范围)、约束(输出规范)。本质是结构化指令包。

> **人话**: 教 Agent 怎么写好代码的说明书

**首次出现**:[Skill 系统](../02-core-concepts/skills-system.md)

### Subagent(子代理)

**定义**:由 Primary Agent 调用的子任务执行单元,通过 `@agent-name` 语法触发,用于执行特定类型的子任务,如代码探索、通用任务等。

> **人话**: 被主 Agent 调用的帮手

**首次出现**:[Agent 编排](../02-core-concepts/agent-orchestration.md)

### Session(会话)

**定义**:一次对话从开始到结束的全过程,包含上下文积累、工具调用和状态变化的完整生命周期。

> **人话**: 一次对话从开始到结束的全过程

**首次出现**:[上下文工程核心](../02-core-concepts/context-engineering-core.md)

### 延续会话 ID（Session Continuation ID）

**定义**:格式为 `ses_xxx...` 的会话标识符,用于在一个子 Agent 的现有对话基础上继续工作。通过 `task(task_id="ses_xxx")` 重用已有上下文,避免重头开始。

> **人话**: 告诉子 Agent"接着上次说的继续"

**首次出现**:[多 Agent 协作](../04-workflows/multi-agent-collab.md#后台任务id体系)

### System Prompt(系统提示词)

**定义**:在对话开始前预设的指令文本,告诉 Agent 它的角色定位、行为规范和工作方式,是 Agent 行为的"底层操作系统"。

> **人话**: 告诉 Agent'你是谁、该怎么做'的那段话

**首次出现**:[自定义 Agent 与 Plugin](../06-advanced/custom-agents.md)

## T

### Token

**定义**:AI 模型处理文本的基本单位,上下文窗口的容量单位。Token 空间有限而信息需求无限,是上下文工程要解决的核心矛盾。

> **人话**: AI 处理信息的字数上限

**首次出现**:[什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md)

### Token Budget(Token 预算)

**定义**:为每个任务分配的 Token 使用上限,防止单个任务无限消耗资源,确保多任务并行时的公平性。

> **人话**: 一次任务最多花多少钱

**首次出现**:[Token 预算策略](../06-advanced/context-compression.md)

### Tool(工具)

**定义**:Agent 可以调用的能力集合,包括文件操作(Read/Write/Edit/Delete)、命令执行(Bash)、网络请求(WebSearch/WebFetch)、代码搜索(Grep/Glob)等。

> **人话**: Agent 能用的工具（读文件、跑命令等）

**首次出现**:[Agent 编排](../02-core-concepts/agent-orchestration.md)

## V

### Validation Harness(验证护栏)

**定义**:确保 AI 生成代码质量的"最后一道防线",管理 Agent 的"准出"。与约束系统(管"准入")形成双翼,验证三原则:自动化、可追溯、可配置。

> **人话**: 改完代码后自动检查，不过就拦

**首次出现**:[验证护栏体系](../02-core-concepts/validation-harness.md)

## W

### Workflow(工作流)

**定义**:将 Agent 与 Skill 组合为可重复执行流程的方法论,是 Harness Engineering 的"生产线"。从 Command 系统到高级编排模式的完整体系。

> **人话**: 把多个步骤串起来的自动化流程

**首次出现**:[工作流模式](../02-core-concepts/workflow-patterns.md)

## X

### 循环工程（**Loop Engineering（循环工程）**）

**定义**:AI 编码智能体的第四层进化阶段（L4），关注自动化循环的设计与管控。核心要素包括：Generator-Evaluator 模式（执行器与验证器分离）、Worktree 隔离（任务并行空间）、看门狗超时（防止无限循环）、Token 预算控制（成本管控）。循环工程是驾驭工程的再上层，解决"我不在时工作如何继续"的问题。

> **人话**: 让 Agent 自己循环干活还能管住它——设置好规则后让它自动跑

**首次出现**:[读者导航 - 智能体开发工程师](../00-guide/reading-paths.md#智能体开发工程师)

## Y

### 风险分类器 (Risk Classifier)

**定义**:验证护栏的智能决策核心,将操作分为高风险(阻止执行)、中风险(确认后执行)、低风险(自动执行)三类,实现智能化的门禁决策。

> **人话**: 自动判断操作风险高低的引擎

**首次出现**:[验证护栏体系](../02-core-concepts/validation-harness.md)

## 约束系统

**定义**:确保 Agent 行为可控的核心机制,由三大支柱构成:权限模型(能不能做)、架构护栏(怎么做)、Lint 规范(做得对)。

> **人话**: 告诉 Agent 什么能干、什么不能干的规则

**首次出现**:[约束系统解析](../02-core-concepts/constraints-system.md)

### 约束 (Constraint)

**定义**:限制 Agent 行为边界的规则,定义哪些操作被允许、哪些被禁止、哪些需要确认,是约束系统的原子单元。

> **人话**: 限制 Agent 行为边界的规则

**首次出现**:[约束系统解析](../02-core-concepts/constraints-system.md)

### 上下文窗口 (Context Window)

**定义**:AI 模型单次对话中能处理的最大 Token 数量,决定了 Agent 一次能"记住"多少信息。

> **人话**: Agent 一次能记住的信息量

**首次出现**:[上下文工程核心](../02-core-concepts/context-engineering-core.md)

### 门禁 (Gate)

**定义**:代码入库前必须通过的质量关卡,只有满足预设条件(编译通过、测试通过、安全检查通过)才能继续。

> **人话**: 代码入库前必须通过的质量关卡

**首次出现**:[验证护栏体系](../02-core-concepts/validation-harness.md)

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
| 反馈循环 | Feedback Loop | [性能调优](../06-advanced/context/performance-tuning.md) |
| Generator-Evaluator 模式 | Generator-Evaluator Pattern | [Ultrawork 模式](../04-workflows/ultrawork-mode.md) |
| Harness Engineering | Harness Engineering | [什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md) |
| 驾驭工程师 | Harness Engineer | [什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md) |
| MCP | Model Context Protocol | [Agent 编排](../02-core-concepts/agent-orchestration.md) |
| March of Nines / 九个九的征程 | March of Nines | [什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md) |
| 模型路由 | Model Routing | [Agent 编排](../02-core-concepts/agent-orchestration.md) |
| opencode.json | opencode.json | [工作流模式](../02-core-concepts/workflow-patterns.md) |
| 权限模型 | Permission Model | [约束系统解析](../02-core-concepts/constraints-system.md) |
| Plan Agent | Plan Agent | [Agent 编排](../02-core-concepts/agent-orchestration.md) |
| Plugin | Plugin | [自定义 Agent 与 Plugin](../06-advanced/custom-agents.md) |
| Provider | Provider | [Agent 编排](../02-core-concepts/agent-orchestration.md) |
| 提示词 | Prompt | [什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md) |
| 质量门禁 | Quality Gates | [验证护栏体系](../02-core-concepts/validation-harness.md) |
| Skill | Skill | [Skill 系统](../02-core-concepts/skills-system.md) |
| Subagent | Subagent | [Agent 编排](../02-core-concepts/agent-orchestration.md) |
| Token | Token | [什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md) |
| 工具 | Tool | [Agent 编排](../02-core-concepts/agent-orchestration.md) |
| 验证护栏 | Validation Harness | [验证护栏体系](../02-core-concepts/validation-harness.md) |
| 工作流 | Workflow | [工作流模式](../02-core-concepts/workflow-patterns.md) |
| 后台任务 | Background Task | [多 Agent 协作](../04-workflows/multi-agent-collab.md#后台任务机制) |
| 后台任务 ID | bg_xxx | [多 Agent 协作](../04-workflows/multi-agent-collab.md#后台任务id体系) |
| 延续会话 ID | ses_xxx | [多 Agent 协作](../04-workflows/multi-agent-collab.md#后台任务id体系) |
| 循环工程 | Loop Engineering | [读者导航 - 智能体开发工程师](../00-guide/reading-paths.md#智能体开发工程师) |
| 风险分类器 (Risk Classifier) | Risk Classifier | [验证护栏体系](../02-core-concepts/validation-harness.md) |
| 约束系统 | Constraints System | [约束系统解析](../02-core-concepts/constraints-system.md) |

---

## AI 编程工具决策对比

管理者在选型 AI 编程工具时，可参考以下对比框架。数据截至 2026 年 6 月，各工具仍在快速迭代。

| 维度 | OpenCode | Claude Code | Cursor | Codex CLI |
|------|----------|-------------|--------|-----------|
| 定位 | 开源 AI 编码平台 | CLI 编码助手 | IDE 集成 | 代码生成 CLI |
| 核心优势 | 灵活配置、多模型支持、插件生态 | 安全沙箱、Anthropic 模型深度集成 | 无缝 IDE 体验、实时补全 | 轻量级、快速启动 |
| 适用团队 | 中大型团队 | 个人 / 小团队 | 前端团队 | 后端团队 |
| 成本模型 | 开源 + 模型费用 | 订阅制（$20/月起） | 订阅制（$20/月起） | API 按量计费 |
| 学习曲线 | 中等（需配置） | 低（开箱即用） | 低（IDE 原生） | 低（CLI 工具） |
| 企业级特性 | 强（权限 / 审计 / 合规） | 中 | 弱 | 弱 |
| 自定义能力 | 高（Agent / Skill / Plugin） | 低 | 中 | 低 |
| 模型选择 | 多模型切换 | 仅 Claude | 多模型 | 仅 OpenAI |

### 选择建议

- **5 人以下团队**：优先考虑 Claude Code 或 Cursor。开箱即用，学习成本低，适合快速验证 AI 编程价值。
- **10-50 人团队**：推荐 OpenCode + 自定义配置。灵活的 Agent 编排和权限管理满足团队协作需求，多模型支持降低单一供应商风险。
- **50 人以上团队**：OpenCode + 企业级部署 + 安全合规配置。权限审计、Agent 行为日志、合规报告是刚需，开源方案也便于内部二次开发。

> **注意**：工具选型应结合团队技术栈、安全要求和预算综合评估，不存在"最优解"。建议从一个试点项目开始，用 2-4 周验证后再做决策。
