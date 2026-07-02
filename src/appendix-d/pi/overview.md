# Pi **Agent（智能体）** 概述与核心概念

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

## 与 **Harness Engineering（驾驭工程）** 四层进化的映射

Pi 的架构设计与 Harness Engineering 的 L1-L4 进化路径高度吻合：

| Harness Engineering 层级 | Pi 的对应能力 |
|-------------------------|--------------|
| **L1 提示词工程** | AGENTS.md / SYSTEM.md / APPEND_SYSTEM.md 多层提示词定制 |
| **L2 上下文工程** | 自动/手动压缩、Session Tree 分支管理、**Context（上下文）** Files 多级加载 |
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
- 扩展加载器（Extensions / Skills / **Prompt（提示词）** Templates / Themes）
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
| **Skill（技能）** 加载 | 遍历目录解析 SKILL.md，支持忽略文件和诊断 |
| Prompt Template 管理 | 加载命名模板供 `/name` 快捷调用 |
| 上下文压缩 | Token 预算计算、Cut Point 搜索、LLM 摘要生成 |
| Session 管理 | JSONL 存储、分支导航、Fork/Clone |
| Agent 生命周期 | Agent 创建 → 配置 → 运行 → 重置 |

### 消息类型增强模式

Pi 使用 TypeScript **模块增强（module augmentation）** 扩展消息类型：

```typescript:src/appendix-d/pi/overview.md
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

```typescript:src/appendix-d/pi/overview.md
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
| **MCP（模型上下文协议）** 支持 | 不内置 MCP | 通过 Extension 添加，或直接用 CLI 工具 + Skills |
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

→ [Pi **Agent（智能体）** 扩展体系详解](./customization.md) 涵盖四层扩展体系
→ [Pi **Agent（智能体）** 生态参考](./ecosystem.md) 涵盖 Provider 和集成方式

## 与 OpenCode / Claude Code 的定位差异

| 维度 | Pi Agent | OpenCode | Claude Code |
|------|----------|----------|-------------|
| 设计哲学 | 极简核心 + 扩展驱动 | 功能全面 + **Plugin（插件）** 体系 | Claude 深度集成 |
| 默认工具 | 4 个（read/write/edit/bash） | 丰富工具链（LSP/AST/CodeGraph） | 基础工具（文件/命令/搜索） |
| 扩展机制 | Extensions/Skills/Packages | Plugin/Skill/MCP/Agent | CLAUDE.md + 自定义命令 |
| 模型支持 | 20+ Provider | 75+ Provider | 仅 Claude |
| 内置功能 | 极简（需扩展补充） | 丰富（Plan/Ultrawork 等） | 适中 |
| 定制深度 | 极高（TypeScript Extension API） | 高（Plugin Hook 系统） | 中（指令配置） |
| 适用场景 | DIY 开发者、嵌入场景 | 多模型团队、复杂工作流 | Claude 生态系统用户 |

> 详细对比见 [AI 编程工具生态对比](../../01-introduction/ecosystem-comparison.md)

---

## 读者视角

### 适用读者角色
- 入门开发者 — 适合 Pi 的极简核心，让新手无需面对复杂配置即可上手
- 智能体开发工程师 — Pi 的 Extension API 为深度定制提供 TypeScript 支持
- 效率开发者 — 4 工具 + 20+ Provider 组合，满足快速迭代需求
- 技术负责人 — 容器化方案（Gondolin/Docker/OpenShell）满足企业安全要求
- Skill 作者 — Skills 系统遵循标准化，易于创建和分享
- 系统架构师 — 明确的安全边界和信任机制，便于架构评估
- 安全工程师 — 安全模型透明，易于威胁建模和合规评估

### 典型使用场景
- 嵌入式 AI 工具开发，提供极简的编程智能体核心
- 构建定制化代码编辑器，替换内置工具实现特定工作流
- 构建多模型切换工作流，动态调整模型以适应不同任务
- 构建安全沙箱环境，隔离生产环境中的 AI 工具执行
- 构建 Skill 市场，分享和复用社区编写的领域知识
- 构建安全审计流水线，评估 AI 工具的攻击面
- 构建模型路由系统，实现不同复杂度任务的模型自动选择

### 使用示例
```bash
# 安装 Pi Agent
npm install -g @earendil-works/pi-coding-agent

# 启动交互模式
pi

# 创建一个简单的 Pi Extension
pi -e ./my-extension.ts

# 加载自定义 Skill
/skill:weather-assistant

# 使用 Prompt Template
/cl

# 切换主题
/settings { "theme": "dark" }
```

### 工程化示例

**配置顺序检查表：**

1. **安装 Pi Core**
   ```bash
   npm install -g @earendil-works/pi-coding-agent
   ```

2. **创建 Extension 目录**
   ```bash
   mkdir -p ~/.pi/agent/extensions/my-extension
   cd ~/.pi/agent/extensions/my-extension
   ```

3. **编写 Extension**
   ```typescript:src/appendix-d/pi/overview.md
   // my-extension/index.ts
   import type { ExtensionAPI } from "@earendil-works/pi-agent-core";
   
   export default function (pi: ExtensionAPI) {
     pi.registerTool({
       name: "my_tool",
       description: "我的自定义工具",
       parameters: { type: "object", properties: {} },
       execute: async () => "工具执行结果"
     });
   }
   ```

4. **启动 Pi**
   ```bash
   pi -e ~/.pi/agent/extensions/my-extension
   ```

### 与前/后文章的衔接
- ← [Pi Agent 概述与核心概念](overview.md) — 提供 Pi 的设计哲学和核心架构
- → [CLI 命令与交互模式参考](./commands.md) — 学习 Pi 的运行模式和编辑器功能

---

## 常见反模式

### 期望 Pi 开箱即用提供完整功能

许多从 Claude Code 或 OpenCode 转来的用户，第一次使用 Pi 时会发现它缺少很多"理应有"的功能：没有 Plan 模式、没有内置 MCP 支持、没有子智能体编排、没有权限弹窗。他们花了大量时间尝试通过配置来补齐这些功能，结果发现 Pi 的设计哲学就是"不内置这些"。

Pi 的正确使用方式是接受它的极简基座，把精力放在核心工作流上。如果某个功能对你至关重要（比如 MCP），通过 Extension 添加。如果某个功能你很少用（比如子智能体），用 tmux 手动启动多个 Pi 实例替代。Pi 的价值不在于功能全面，而在于每个功能都可以按你的需求深度定制。

### 把 AGENTS.md 写成 API 文档

Pi 的 AGENTS.md 支持全局和项目两级配置，许多开发者把它当作 API 参考文档使用，把所有相关库的接口说明都复制进去。但 AGENTS.md 的内容会注入到每次 LLM 请求的系统提示中，过长的 AGENTS.md 会消耗上下文窗口，降低 Agent 对核心规则的遵循率。

AGENTS.md 应该只包含 Agent 无法从代码推断的信息：构建命令、团队特有的约定、常见陷阱和环境怪异之处。API 文档改为在代码注释或外部文档中维护，AGENTS.md 中用一行链接引用即可。

### 忽略不同运行模式下 Extension 行为的差异

为交互模式开发的 Extension 在 Print 模式、JSON 模式和 RPC 模式下可能表现不同。例如，一个使用 `ctx.ui` 更新状态行的 Extension 在非交互模式下会报错，因为没有 TUI 渲染器。开发者在交互模式下测试通过后，直接在 CI 脚本中使用，结果 Extension 崩溃导致任务失败。

Extension 开发时应该考虑所有运行模式。使用 `ctx.hasUI` 检查是否有 TUI 环境，非交互模式下降级为日志输出。在 CI/CD 中测试 Extension 时，使用 `pi -p "..."` 而非 `pi` 来验证兼容性。

## 适用场景与限制

### 极简核心意味着开箱能力有限

Pi 的 4 个内置工具（read/write/edit/bash）和 ~1K token 系统提示是刻意设计的极简基座。对于不需要扩展的场景（简单代码编辑、快速问答），Pi 的开箱体验足够好。但对于需要 LSP 代码智能、AST 级别重构、跨文件引用分析的场景，纯靠 LLM 的推理能力加上基础工具可能不够精确。

如果你的工作流高度依赖代码智能工具（如 TypeScript 项目的精确重构），OpenCode 的开箱体验可能更适合。Pi 的优势在于你可以通过 Extension 逐步构建所需的能力，但初始阶段需要更多配置工作。

### Session Tree 分支管理的学习曲线

Pi 独有的 Session Tree 分支功能（`/fork`、`/tree`）非常强大，但它的行为模式与 Git 分支有微妙差异。Session 分支不是 Git 分支的简单复制——每个分支有独立的完整对话历史，分支间的上下文不共享。不理解这一点的用户可能在分支间切换时丢失上下文。

使用 Session Tree 前，先理解它的存储模型：每个分支是独立的 JSONL 文件，从分叉点开始记录新的消息。分支间的共享仅限于分叉点之前的历史。适合"探索多方案然后选择"的工作流，不适合"并行处理不同子任务"的场景。

### 4 种运行模式增加了心智负担

Pi 提供交互、Print、JSON、RPC 四种运行模式，加上 SDK 嵌入实际上是五种。每种模式的事件消费方式、工具可用性和 UI 交互都不同。开发者需要理解每种模式的限制才能正确使用，这增加了入门的学习成本。

对于大多数场景，只需要掌握两种模式：交互模式（日常开发）和 Print 模式（脚本集成）。RPC 和 SDK 模式是高级功能，只在有明确需求时才学习。JSON 模式适合需要结构化输出的脚本，但如果只是简单的文本输出，Print 模式更简单。

## 常见失败与陷阱

### Extension 加载失败后静默降级

Pi 的 Extension 加载器捕获所有异常以保证 Agent 能正常启动。这意味着如果你的 Extension 有语法错误、依赖缺失或类型不匹配，Pi 不会报错退出，而是跳过该 Extension 继续运行。你可能以为 Extension 已经加载成功，实际上所有工具和事件处理器都没有注册。

每次添加或修改 Extension 后，用 `pi.getAllTools()` 或 `/reload` 验证工具是否注册成功。在开发阶段使用 `pi --log-level debug` 查看详细的加载日志。定期运行 `pi -e ./my-extension.ts` 单独测试 Extension 的加载。

### 上下文压缩摘要丢失关键信息

Pi 的自动压缩在上下文接近窗口上限时触发，将较早的对话历史压缩为摘要。但摘要的质量取决于 LLM 的理解能力，可能遗漏具体的技术细节（如特定的函数名、变量名、配置值）。如果你在对话早期讨论了一个关键的架构决策，压缩后 Agent 可能不记得这个决策。

关键规则和架构决策应该放在 AGENTS.md 中而非对话 prompt 中。AGENTS.md 在每次请求时重新注入，不受压缩影响。使用 `/compact` 时附带自定义指令，明确告诉 LLM 需要在摘要中保留哪些关键信息。

### 跨 Provider 切换时工具兼容性问题

Pi 支持在会话中通过 `/model` 命令实时切换 Provider，但不同 Provider 对工具调用（Function Calling）的支持程度不同。切换到一个不支持工具调用的 Provider 后，之前注册的自定义工具将无法被调用，Agent 可能尝试用自然语言描述工具调用而非实际执行。

切换 Provider 前确认目标 Provider 支持工具调用。使用 `registry.getModelsSupportingToolCalls()` 查询支持工具调用的模型列表。对于需要可靠工具调用的场景，固定使用 Anthropic 或 OpenAI 的模型，避免切换到工具支持不完善的 Provider。
