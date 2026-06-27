# Pi Agent 概述与核心概念

## 什么是 Pi？

Pi 是一个**极简终端编码智能体工具**，由 Mario Zechner 创建，现由 Earendil Inc. 维护。它不追求"开箱即用的一切功能"，而是提供一个约 1K token 的极简系统提示核心，通过 4 层扩展体系让用户按需塑造工具行为。

> **设计哲学**：适应你的工作流，而不是让你适应工具。不需要 fork 和修改 Pi 的内部代码——通过扩展来定制一切。

### 核心数据

| 指标 | 数值 |
|------|------|
| GitHub Stars | 65K+ |
| 周 npm 下载量 | 210 万 |
| 许可证 | MIT |
| 语言 | TypeScript |
| 最新包名 | `@earendil-works/pi-coding-agent` |
| 作者 | Mario Zechner（badlogicgames） |

### 一句话定位

Pi 是"可编程的编码智能体"——它不给用户强加工作流，而是提供一套极简基座和强大的扩展 API，让用户构建自己的工作流。

---

## 与 Harness Engineering 四层进化的映射

Pi 的架构设计与 Harness Engineering 的 L1-L4 进化路径高度吻合：

| Harness Engineering 层级 | Pi 的对应能力 |
|-------------------------|--------------|
| **L1 提示词工程** | AGENTS.md / SYSTEM.md / APPEND_SYSTEM.md 多层提示词定制 |
| **L2 上下文工程** | 自动/手动压缩、Session Tree 分支管理、Context Files 多级加载 |
| **L3 驾驭工程** | Extension API（自定义工具/命令/事件处理）、Project Trust 系统 |
| **L4 循环工程** | SDK 嵌入、RPC 模式、Pi Packages 自动化扩展部署 |

→ 四层进化理论详见 [Harness Engineering 理论框架](../../01-introduction/harness-engineering-theory.md)

---

## 核心架构全景

Pi 由 4 个 npm 包组成，形成分层架构：

```
┌─────────────────────────────────────┐
│   pi-coding-agent（CLI 与交互界面）  │
│  交互模式 / Print模式 / RPC / SDK   │
├─────────────────────────────────────┤
│   pi-agent-core（Agent 运行时）      │
│  工具调用 / 状态管理 / 事件流 / 压缩  │
├─────────────────────────────────────┤
│   pi-ai（统一多 Provider LLM API）   │
│  20+ Provider / Token追踪 / 跨Provider切换│
├─────────────────────────────────────┤
│   pi-tui（终端 UI 组件库）           │
│  差分渲染 / 自定义编辑器 / Widget    │
└─────────────────────────────────────┘
```

### 核心包说明

#### @earendil-works/pi-ai

统一多 Provider LLM 接口层，支持 OpenAI、Anthropic、Google、DeepSeek、Mistral、Groq、GitHub Copilot 等 **20+ 内置 Provider**。核心能力：

- 统一的流式 API，TypeBox schema 实现类型安全的工具定义
- 自动认证解析（API Key / OAuth）
- Token 与成本追踪
- 跨 Provider 切换：同一 Session 可中途切换模型
- 支持工具调用（Function Calling）的模型自动筛选
- 摇树优化支持：可按需注册单个 Provider，减小打包体积

#### @earendil-works/pi-agent-core

Agent 运行时层，管理完整的 LLM 交互循环：

- **Agent** 类：核心 LLM 交互，支持 `transformContext`（上下文预处理）、`beforeToolCall`/`afterToolCall` 钩子
- **AgentState**：状态管理，包括系统提示、模型配置、消息历史、工具列表
- **Steering Mode**：`one-at-a-time`（默认，逐条交付）或 `all`（批量交付）两种消息交付策略
- **Follow-up Mode**：同上，控制后续消息交付
- **Tool Execution**：`parallel`（默认）或 `sequential` 两种工具执行模式
- **Thinking Budgets**：支持 `minimal`/`low`/`medium`/`high` 四档推理预算
- **事件流**：底层 `agentLoop()`/`agentLoopContinue()` 提供可观测的低级事件流

#### @earendil-works/pi-coding-agent

用户直接面对的上层 CLI 包，整合了所有下层能力并提供了：

- 4 种运行模式（见下文）
- 编辑器特性（@文件引用、!bash 执行、多行输入、图片粘贴）
- Session 管理（JSONL 存储、Tree 分支、Fork/Clone）
- 扩展加载器（Extensions / Skills / Prompt Templates / Themes）
- Project Trust 安全机制
- 自动/手动上下文压缩

#### @earendil-works/pi-tui

终端 UI 组件库，提供差分渲染（differential rendering）能力，支持：

- 自定义编辑器替换
- Widget 添加（状态行、页眉、页脚）
- 覆盖层（Overlay）
- 主题系统


### 包依赖关系

```
pi-tui ──→ pi-coding-agent ──→ pi-agent-core ──→ pi-ai
                                       ↑
                                  harness/
```

pi-agent-core 的 `harness/` 目录是全书主题的直接代码映射：Skills 加载、上下文压缩、Session 管理、Prompt 模板注入——所有 Harness Engineering 概念在此集中实现。

---

## 架构设计模式

### Agent Loop 模式

Agent 运行时采用"状态容器 + 事件流"的分离设计：

```
Agent 类（可变状态容器）
  ├── AgentState：系统提示、模型配置、消息历史、工具列表
  ├── transformContext() — 上下文预处理钩子
  ├── beforeToolCall() / afterToolCall() — 工具调用钩子
  └── 被 agentLoop() 消费 → 产出 AsyncGenerator<AgentEvent>

agentLoop() → AgentEvent 流
  ├── TextDelta     — 流式文本片段
  ├── ToolCall      — LLM 请求的工具调用
  ├── ToolResult    — 工具执行结果
  ├── Thinking      — 推理过程
  ├── Error         — 异常
  └── Done          — 完成信号
```

所有 4 种运行模式（交互 / Print / JSON / RPC）共享同一个 `agentLoop()` 事件流，差异仅在于事件的消费方式。添加新模式只需要实现一个新的事件消费者。

### Harness 模式

`packages/agent/src/harness/agent-harness.ts`（36KB）是整合所有上层能力的编排器：

| 组件 | 职责 |
|------|------|
| System Prompt 构造 | 从 Skills + Prompt Templates + Context Files 动态拼接 |
| Skill 加载 | 遍历目录解析 SKILL.md，支持忽略文件和诊断 |
| Prompt Template 管理 | 加载命名模板供 `/name` 快捷调用 |
| 上下文压缩 | Token 预算计算、Cut Point 搜索、LLM 摘要生成 |
| Session 管理 | JSONL 存储、分支导航、Fork/Clone |
| Agent 生命周期 | Agent 创建 → 配置 → 运行 → 重置 |

### 消息类型增强模式

Pi 使用 TypeScript **模块增强（module augmentation）** 扩展消息类型：

```typescript
// types.ts — 定义可扩展接口
interface CustomAgentMessages {}

// messages.ts — 通过模块增强注册新类型
declare module "../types.ts" {
  interface CustomAgentMessages {
    bashExecution: BashExecutionMessage;
    custom: CustomMessage;
    branchSummary: BranchSummaryMessage;
    compactionSummary: CompactionSummaryMessage;
  }
}
```

这使得新消息类型可以跨文件注册，无需修改核心类型定义。压缩摘要和分支摘要都是通过此机制注册的特殊消息类型，在 `convertToLlm()` 中被渲染为 LLM 可读的 `<summary>` XML 块。

---

## Harness Engineering 深度映射

Pi 的架构与 Harness Engineering 四层进化路径的对应不止于表面能力，而是深入到代码结构：

### L1 → Harness 中的 `prompt-templates.ts` + `system-prompt.ts`

- `system-prompt.ts` 的 `formatSkillsForSystemPrompt()` 将 Skill 封装为 XML `<skill>` 块
- `prompt-templates.ts` 的 `loadPromptTemplates()` 读取 YAML frontmatter 命名模板
- Context Files 加载（AGENTS.md / SYSTEM.md / APPEND_SYSTEM.md）支持全局 + 项目二级覆盖

### L2 → Harness 中的 `compaction/compaction.ts` + `session.ts` + `messages.ts`

- `summarizeWithBudget()`：计算上下文 Token → 搜索 Cut Point → LLM 摘要 → 注入为 `compactionSummary`
- `session.ts`：JSONL 序列化/反序列化、Git 分支创建、Session Tree 导航
- `convertToLlm()`：将 `branchSummary` / `compactionSummary` 等自定义消息渲染为 LLM 可理解的格式

Pi 的上下文工程有个独特设计：**压缩摘要和分支摘要都被建模为 AgentMessage 类型**，在消息历史中与其他消息地位相同，不丢失上下文连续性。

### L3 → Harness 中的 Extension API + Project Trust

- Extension API 通过 `export default function(pi: ExtensionAPI)` 注册工具/命令/事件处理器
- 钩子点：`onStartup`、`onShutdown`、`onContextReady`、`beforeToolCall`、`afterToolCall`
- Gondolin extension 演示了替换内置工具的能力——将 `read`/`write`/`edit`/`bash` 路由到微 VM
- Project Trust 系统（`/trust`）控制 per-project 信任决策

Pi 不提供 OpenCode 式的质量门禁（quality gates），而是让用户通过 Extension 自行构建。这符合极简哲学。

### L4 → SDK + RPC + 容器化

Pi **主动不做**内置自动化循环（如 OpenCode 的 ralph-loop），而是提供：
- SDK 嵌入：在外部 Node.js 应用中实现自定义循环
- RPC 模式：跨语言进程间通信
- 容器化：Gondolin / Docker / OpenShell 三种隔离方案

核心洞察：Pi 认为循环工程高度场景化，提供基础设施（事件流、消息队列、Session 管理）让用户构建适合自己的循环。

---

## 独特创新与设计模式

### 消息队列与双通道交付

编辑器支持两种消息交付策略，互不干扰：

```
Steering 消息（Enter）→ Agent 当前工具调用完成后立即交付
Follow-up 消息（Alt+Enter）→ Agent 全部工作完成后交付
```

消息交付策略可在 `/settings` 中配置为 `one-at-a-time`（逐条）或 `all`（批量）。

### Session Tree 分支管理

Session 支持树状分支结构——`/fork` 从分支点创建新 Session，`/tree` 在分支树中导航。这是其他 AI 编码工具（OpenCode、Claude Code 等）较少提供的功能。

### Differential Rendering TUI

TUI 使用 `diff` 库实现行级别差分渲染——只重绘发生变化的行，而非整个终端输出。这在长输出、滚动场景下显著减少闪烁和性能开销。编辑器基于 textarea 实现，支持多行编辑、图片粘贴、路径 Tab 补全。

### TypeBox Schema 工具定义

使用 `@sinclair/typebox` 而非 JSON Schema 或 Zod 定义工具参数，兼顾静态类型推断、运行时验证和 JSON Schema 生成（给 LLM 用）：

```typescript
import { Type } from "@sinclair/typebox";
const params = Type.Object({
  path: Type.String({ description: "文件路径" }),
});
```

### 最小工具集的开销优势

Pi 默认 4 工具 + ~1K token 系统提示 vs OpenCode 的 15+ 工具 + ~6K token：

| 对比项 | Pi | OpenCode |
|--------|-----|---------|
| 默认工具数 | 4 | 15+ |
| 系统提示 Token | ~1K | ~6K |
| 每次请求固定开销 | 低 | 高 |
| 扩展方式 | Extension 按需添加 | 默认内置 |

Pi 的 `edit` 工具采用差异式编辑（先读后改），区别于 OpenCode 的全量式 `write`（直接覆盖），在大型文件修改场景更节约 LLM Token。

---

## 设计哲学：核心极简，无限扩展

Pi 与其他 AI 编码工具有一个根本性差异：它主动**不做**某些功能，而是提供扩展机制让用户按需构建。

### Pi 主动不做的功能

| 功能 | Pi 的立场 | 替代方案 |
|------|----------|---------|
| MCP 支持 | 不内置 MCP | 通过 Extension 添加，或直接用 CLI 工具 + Skills |
| 子智能体 | 不内置 | 通过 tmux 启动多个 Pi 实例，或用 Extension 构建 |
| 权限弹窗 | 不内置 | 容器化运行，或用 Extension 构建自定义确认流 |
| Plan 模式 | 不内置 | 写 Plan 到文件，或用 Extension 构建 |
| 内置 TODO | 不内置（TODO 混淆模型） | 使用 TODO.md 文件，或用 Extension 构建 |
| 后台 Bash | 不内置 | 使用 tmux（完全可观测、可直接交互） |

### 为什么这样做？

Pi 的核心论点是：**不同的团队、不同的项目、不同的安全需求需要不同的实现方式**。与其内置一个"对所有人都不完美"的实现，不如提供足够强大的扩展 API，让用户定制真正适合自己的方案。

### 核心理念

```
核心（~1K token 系统提示 + 4 工具）→ 够用，但不限制
扩展（Extensions/Skills/Templates/Packages）→ 按需加载，组合出工作流
社区（Pi Packages npm 分发）→ 分享与复用
```

→ [Extensions 详解](./customization.md) 涵盖四层扩展体系
→ [生态与社区参考](./ecosystem.md) 涵盖 Provider 和集成方式

## 与 OpenCode / Claude Code 的定位差异

| 维度 | Pi Agent | OpenCode | Claude Code |
|------|----------|----------|-------------|
| 设计哲学 | 极简核心 + 扩展驱动 | 功能全面 + Plugin 体系 | Claude 深度集成 |
| 默认工具 | 4 个（read/write/edit/bash） | 丰富工具链（LSP/AST/CodeGraph） | 基础工具（文件/命令/搜索） |
| 扩展机制 | Extensions/Skills/Packages | Plugin/Skill/MCP/Agent | CLAUDE.md + 自定义命令 |
| 模型支持 | 20+ Provider | 75+ Provider | 仅 Claude |
| 内置功能 | 极简（需扩展补充） | 丰富（Plan/Ultrawork 等） | 适中 |
| 定制深度 | 极高（TypeScript Extension API） | 高（Plugin Hook 系统） | 中（指令配置） |
| 适用场景 | DIY 开发者、嵌入场景 | 多模型团队、复杂工作流 | Claude 生态系统用户 |

> 详细对比见 [AI 编程工具生态对比](../../01-introduction/ecosystem-comparison.md)
