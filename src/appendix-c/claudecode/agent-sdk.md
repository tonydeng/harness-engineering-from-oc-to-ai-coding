# Claude **Agent（智能体）** SDK：编程式 Agent 开发

> 通过 `@anthropic-ai/claude-agent-sdk` 将 Claude Code 的 Agent 引擎嵌入你的应用——用代码驱动工具调用、子 Agent 调度和 **MCP（模型上下文协议）** 集成。

Claude Agent SDK 把 Claude Code 的 Agent 循环（工具执行、上下文管理、自动压缩）作为库暴露出来。和 [Agent 设计指南](./agent-architecture.md) 中介绍的 filesystem Subagent（`.claude/agents/*.md`）不同，SDK 面向的是**在代码中创建和管理 Agent**的场景——CI/CD 流水线、自定义 Web 应用、后台服务。

---

## SDK vs Filesystem 子 Agent

| 维度 | Filesystem Subagent（`agent-architecture.md`） | Agent SDK 编程式 | 取舍分析 |
|------|-----------------------------------------------|-----------------|----------|
| **定义方式** | `.claude/agents/*.md` Markdown 文件，带 YAML frontmatter | `query()` 选项中的 `AgentDefinition` 对象 | Filesystem 适合人类编辑和版本追踪；SDK 适合动态生成和多租户场景 |
| **调用方式** | `/fork <name>`、`/agent <name>`、Agent tool | `agents` 参数传入字典，Agent tool 调用 | CLI 方式天然适合交互式工作流；SDK 方式适合嵌入自动化流程 |
| **Agent 定义来源** | 静态文件系统 | 运行时动态构造（可来自数据库、用户配置） | 静态=可审计、可代码审查；动态=灵活、支持多租户隔离配置 |
| **执行环境** | Claude Code CLI 会话内 | 独立 Node.js/Python 进程 | 进程内=共享上下文零开销；独立进程=隔离性好但增加子进程通信延迟 |
| **自定义工具** | 无原生支持 | `tool()` + `createSdkMcpServer()` 创建自定义工具 | SDK 弥补了 filesystem 的最大能力短板，但自定义工具需要额外编码和维护 |
| **Hook 系统** | filesystem Hook（shell 脚本） | 编程式 Hook 回调（`PreToolUse`、`PostToolUse`） | Shell 脚本简单但表达能力有限；编程式回调可做复杂验证、阻断和状态管理 |
| **适用场景** | 交互式 TUI、团队共享 | 生产自动化、自定义应用、CI/CD | 二者互补非替代：TUI 场景用 filesystem，自动化场景用 SDK |
| **CLAUDE.md 加载** | 自动加载 | 通过 `settingSources` 控制 | SDK 提供精细控制（可选择性加载），但需要显式配置，增加了心智负担 |

**一句话选型**：你在 Claude Code TUI 中工作 → filesystem Subagent；你要构建一个调用 Claude 能力的应用 → Agent SDK。

---

## 安装与快速入门

### 安装

```bash
npm install @anthropic-ai/claude-agent-sdk
```

### 最小示例：Hello World

```typescript:src/appendix-c/claudecode/agent-sdk.md
import { query } from '@anthropic-ai/claude-agent-sdk'

async function main() {
  for await (const message of query({
    prompt: '这个目录下有哪些文件？',
    options: {
      allowedTools: ['Bash', 'Glob'],
      permissionMode: 'bypassPermissions',
    },
  })) {
    if (message.type === 'assistant') {
      for (const block of message.message.content) {
        if ('text' in block) console.log(block.text)
      }
    }
    if (message.type === 'result') {
      console.log('Done:', message.subtype)
    }
  }
}

main()
```

`query()` 返回一个 async 生成器——Claude 思考时产生 `assistant` 消息，调用工具时产生 tool 消息，任务结束时产生 `result` 消息。你只需消费这个流，SDK 处理所有工具执行和上下文管理。

> 💡 **设计决策**：SDK 选择 async 生成器（`async for`）而非 Promise/回调模式，因为 Agent 是**持续产生中间状态的事件流**——每步思考、每次工具调用都需要实时可见。Promise 只适合一次性结果，而生成器天然支持逐步消费。如果应用只关心最终结果，可以在 `for await` 循环外层包一层 Promise。

> 💡 **设计决策**：Hello World 示例使用了 `bypassPermissions` 来保持代码简洁，但这在生产中意味着**无条件自动批准所有操作**。实际使用时，应从 `acceptEdits` 或 `auto` 开始，仅在严格限制的沙箱环境（如 CI 中只给 `Read`、`Glob`、`Grep` 三个工具）才用 `bypassPermissions`。

---

## 核心 API

### `query()` — 主要入口

```typescript:src/appendix-c/claudecode/agent-sdk.md
function query({ prompt, options }: {
  prompt: string | AsyncIterable<SDKUserMessage>
  options?: Options
}): Query
```

| 参数 | 类型 | 说明 |
|------|------|------|
| `prompt` | `string \| AsyncIterable<SDKUserMessage>` | 提示词，或用于流式输入的 async 迭代器 |
| `options.allowedTools` | `string[]` | 允许 Agent 自动使用的工具列表 |
| `options.permissionMode` | `PermissionMode` | 见下文权限模式 |
| `options.model` | `string` | 模型别名：`"sonnet"`、`"opus"`、`"haiku"`、`"inherit"` |
| `options.maxTurns` | `number` | 最大对话轮次（默认无限制） |
| `options.systemPrompt` | `object` | 自定义系统提示词（`preset` + `append` 或完全替换） |
| `options.cwd` | `string` | Agent 工作目录 |
| `options.settingSources` | `string[]` | 是否加载 CLAUDE.md/Skills（`["project"]`、`["user"]`） |
| `options.agents` | `Record<string, AgentDefinition>` | 编程式子 Agent 定义 |
| `options.hooks` | `object` | 工具调用前/后的 Hook 回调 |
| `options.mcpServers` | `Record<string, McpServerConfig>` | MCP 服务器配置 |
| `options.maxBudgetUsd` | `number` | 最大美元预算上限 |
| `options.env` | `Record<string, string>` | 传递给子进程的环境变量 |

### `startup()` — 预初始化（减少延迟）

对于延迟敏感的场景，`startup()` 可以提前启动 Claude Code 子进程：

```typescript:src/appendix-c/claudecode/agent-sdk.md
import { startup } from '@anthropic-ai/claude-agent-sdk'

// 在应用启动时预初始化
const warm = await startup({ options: { maxTurns: 3 } })

// 后续使用时立即响应
for await (const message of warm.query('这个目录有什么文件？')) {
  // 这里不会因为子进程启动而延迟
}
```

> 💡 **设计决策**：`startup()` 本质是用**内存换延迟**——预热保持一个空闲子进程常驻。对于高吞吐服务，这省去了每次 `query()` 的 spawn + handshake 开销（1-2 秒）。但注意：预热时指定的 `options` 也会占用上下文资源（如 `settingSources` 加载的 CLAUDE.md），如果预热配置和后续 query 配置不一致，`startup()` 的优势会被抵消。

### Query 对象方法

`query()` 返回的 `Query` 对象提供运行时控制：

| 方法 | 说明 |
|------|------|
| `interrupt()` | 中断当前执行 |
| `setPermissionMode(mode)` | 动态修改权限模式 |
| `setModel(model?)` | 切换模型 |
| `setMaxThinkingTokens(n)` | 设置推理 Token 上限 |
| `supportedCommands()` | 获取支持的 Slash 命令列表 |
| `supportedModels()` | 获取可用模型列表 |
| `mcpServerStatus()` | 查看 MCP 服务器状态 |
| `close()` | 关闭会话释放资源 |

---

## 上下文管理

Agent SDK 的上下文管理是保障长任务可靠性的核心机制。理解它的工作原理，能帮助你避免"Agent 做了一半忘记上下文"的生产事故。

### 自动压缩（Compaction）

Claude 的上下文窗口有限（通常 200K tokens）。当对话接近窗口上限时，SDK **自动对较早的对话历史进行摘要压缩**，保留最近的交互和关键决策，释放空间给后续操作。

```typescript:src/appendix-c/claudecode/agent-sdk.md
// 监听 compact_boundary 消息，了解压缩发生时机
for await (const message of query({
  prompt: '执行一个需要很多步骤的数据分析任务...',
  options: { maxTurns: 100 },
})) {
  // TypeScript 中 compaction 事件是 SDKCompactBoundaryMessage 类型
  if (message.type === 'system' && message.subtype === 'compact_boundary') {
    console.log(`[上下文压缩] 触发: ${message.trigger}`)
    console.log(`  压缩前 tokens: ${message.compact_metadata.pre_tokens}`)
    // trigger 取值：'auto'（自动）或 'manual'（手动 /compact）
  }
}
```

**压缩的工作方式**：

1. SDK 在每次模型请求后监控 token 用量
2. 当上下文接近限制（默认约 100K tokens 触发阈值），自动注入摘要指令
3. 模型对较早的对话轮次生成结构化摘要
4. 清空被压缩的对话历史，仅保留摘要继续执行
5. 如果有 `PreCompact` Hook，会在压缩前触发

**💡 设计决策**：压缩用摘要替代原始对话，意味着早期 prompt 中的**具体指令可能丢失**。持久性规则（如编码规范、架构约定）应放在 CLAUDE.md 中，因为 CLAUDE.md 在每个请求中都会重新注入，不会因为压缩而丢失。

### 控制 context 加载：`settingSources`

默认情况下，`query()` 加载和 Claude Code CLI 相同的 filesystem 设置——用户级、项目级、本地级的 CLAUDE.md、Skills、Agents 和 Commands。通过 `settingSources` 可以精细控制：

```typescript:src/appendix-c/claudecode/agent-sdk.md
// 场景 A：完全自主控制——不加载任何 filesystem 设置
for await (const message of query({
  prompt: '分析这段代码',
  options: {
    settingSources: [], // 空数组 = 只加载程序化配置
    allowedTools: ['Read', 'Glob', 'Grep'],
    // CLAUDE.md、Skills 等均不加载
  },
}))


// 场景 B：仅加载项目级 CLAUDE.md，跳过用户级配置
for await (const message of query({
  prompt: '修复项目中的 bug',
  options: {
    settingSources: ['project'], // 只加载项目目录下的配置
    allowedTools: ['Read', 'Edit', 'Glob', 'Grep', 'Bash'],
  },
}))

// 场景 C：加载全部（默认行为，显式写出更清晰）
for await (const message of query({
  prompt: '审查代码',
  options: {
    settingSources: ['user', 'project', 'local'],
  },
}))
```

**各 source 加载的内容**：

| Source | 加载内容 | 典型用途 |
|--------|---------|----------|
| `"user"` | `~/.claude/CLAUDE.md`、用户级 Skills、用户级 Commands | 个人偏好、全局快捷键 |
| `"project"` | `./CLAUDE.md` 或 `./.claude/CLAUDE.md`、项目级 Skills | 编码规范、架构决策记录 |
| `"local"` | `.claude/settings.local.json`、本地 Hook | 环境特定配置，不提交 Git |

> 💡 **设计决策**：什么情况下该限制 `settingSources`？
> - **CI/CD 环境**：用 `settingSources: []` 确保构建环境干净，不受开发者个人配置影响
> - **多租户服务**：每个租户的 CLAUDE.md 路径不同，应通过 `cwd` 隔离而非依赖默认加载
> - **性能敏感场景**：大量 Skills 定义会增加系统提示词大小，影响首 token 延迟
>
> 注意：少数配置**不受** `settingSources` 控制——Managed Policy（管理端强制策略）和 `~/.claude.json` 全局配置始终加载。

### 手工压缩

除了自动压缩，还可以通过发送 `/compact` 命令手动触发：

```typescript:src/appendix-c/claudecode/agent-sdk.md
for await (const message of query({
  prompt: '/compact', // 手工触发上下文压缩
  options: { maxTurns: 1 },
})) {
  if (message.type === 'system' && message.subtype === 'compact_boundary') {
    console.log('手工压缩完成')
  }
}
```

### PreCompact Hook

在压缩发生前执行自定义逻辑——例如存档完整对话记录：

```typescript:src/appendix-c/claudecode/agent-sdk.md
for await (const message of query({
  prompt: '长时间运行的任务...',
  options: {
    maxTurns: 200,
    hooks: {
      PreCompact: [{
        matcher: '*',
        hooks: [
          async (input) => {
            // 在压缩前将完整对话写入日志
            await archiveConversation(input.sessionId)
            return { continue: true }
          },
        ],
      }],
    },
  },
}))
```

### 持久规则的最佳位置

| 规则类型 | 放置位置 | 理由 |
|---------|---------|------|
| 编码规范、架构约定 | CLAUDE.md（通过 `settingSources` 加载） | 每轮请求重新注入，不因压缩丢失 |
| 一次性任务指令 | 放在 `prompt` 中 | 压缩可能丢失，但任务往往单次有效 |
| 需要跨 session 保留的状态 | 外部数据库，通过 Hook 或 Custom Tool 注入 | 压缩和 session 边界都会导致上下文丢失 |

---

## 运行时防护

生产环境中的 Agent 需要**成本、时间和安全**三个维度的防护。SDK 提供了多层防护机制。

### maxTurns 决策指南

`maxTurns` 限制工具调用的轮次（API 往返次数）。不设置则无上限——可能导致无限循环和意外费用。

```typescript:src/appendix-c/claudecode/agent-sdk.md
// 简单任务：10-20 轮足够
for await (const message of query({
  prompt: '格式化 src/ 下所有 TypeScript 文件',
  options: { allowedTools: ['Read', 'Edit', 'Glob'], maxTurns: 15 },
}))

// 复杂编码任务：50-100 轮
for await (const message of query({
  prompt: '实现用户认证模块：登录、注册、JWT 刷新',
  options: { allowedTools: ['Read', 'Edit', 'Write', 'Bash', 'Glob'], maxTurns: 80 },
}))

// 探索性任务：200-250 轮
for await (const message of query({
  prompt: '分析这个大型代码库的架构，生成文档',
  options: { allowedTools: ['Read', 'Glob', 'Grep', 'Bash'], maxTurns: 250 },
}))
```

**maxTurns 选择速查表**：

| 任务类型 | 推荐范围 | 典型消耗 | 风险 |
|---------|---------|---------|------|
| 纯问答 | 1-5 | 1-2 轮 | 无 |
| 简单文件操作 | 5-20 | 3-10 轮 | 低 |
| 单功能实现 | 20-50 | 10-30 轮 | 中 |
| 多步骤代码审查 | 50-80 | 20-50 轮 | 中 |
| 全模块开发 | 80-150 | 40-100 轮 | 高 |
| 探索性分析 | 150-250 | 50-200 轮 | 高 |

> 💡 **设计决策**：maxTurns 是**安全网不是精确预算**。它防止 Agent 失控，而非精确限制工作量。如果你的 Agent 频繁达到上限，应增大限制或拆分任务——这不是"超过预算"，而是"预算估算偏低"。另外注意：maxTurns 只计算**工具调用轮次**，纯思考不占用名额。

### 成本估算模型

不同模型在不同任务上的 token 消耗差异显著：

| 模型 | 平均 tokens/轮（简单操作） | 平均 tokens/轮（代码生成） | 估算成本/轮（以 Sonnet 为基准） |
|------|--------------------------|--------------------------|-------------------------------|
| Sonnet | 2K-4K | 5K-10K | 1×（基准） |
| Opus | 3K-6K | 8K-15K | 3-5× Sonnet |
| Haiku | 1K-2K | 2K-4K | 0.25× Sonnet |

**实用估算公式**：`总成本 ≈ maxTurns × 平均 tokens/轮 × token 单价`

例如：Sonnet + 50 轮代码生成 → 50 × 7.5K × 单价。

### 预算控制策略

```typescript:src/appendix-c/claudecode/agent-sdk.md
// 硬预算上限——超过即终止
for await (const message of query({
  prompt: '批量重构服务层代码',
  options: {
    allowedTools: ['Read', 'Edit', 'Glob', 'Grep', 'Bash'],
    maxTurns: 100,
    maxBudgetUsd: 2.00, // 美元上限
  },
}))
```

使用 `result` 消息的 `subtype` 信息监控成本：

```typescript:src/appendix-c/claudecode/agent-sdk.md
for await (const message of query({
  prompt: '分析并优化性能瓶颈',
  options: { maxTurns: 50 },
})) {
  if (message.type === 'result') {
    // result 消息的 subtype 指示终止原因
    switch (message.subtype) {
      case 'success':
        console.log('任务正常完成')
        break
      case 'max_turns_reached':
        console.log('达到最大轮次限制')
        break
      case 'error':
        console.log('任务出错')
        break
    }
  }
}
```

### 超时控制

SDK 支持多层超时，通过环境变量传递：

```typescript:src/appendix-c/claudecode/agent-sdk.md
for await (const message of query({
  prompt: '分析大型代码库结构',
  options: {
    allowedTools: ['Read', 'Glob', 'Grep'],
    maxTurns: 200,
    env: {
      // 每轮 API 请求超时（默认 600000ms = 10 分钟）
      API_TIMEOUT_MS: '300000',
      // 最大 API 重试次数（默认 10）
      CLAUDE_CODE_MAX_RETRIES: '3',
      // 后台子 Agent 无活动超时
      CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS: '120000',
      // 启用流式响应看门狗
      CLAUDE_ENABLE_STREAM_WATCHDOG: '1',
      // 流式响应空闲超时（默认 300000ms）
      CLAUDE_STREAM_IDLE_TIMEOUT_MS: '120000',
    },
  },
}))
```

**超时参数说明**：

| 环境变量 | 默认值 | 作用 | 建议调整场景 |
|---------|--------|------|------------|
| `API_TIMEOUT_MS` | 600000 | 单次 API 请求超时 | 模型响应慢（加大）或快速失败场景（减小） |
| `CLAUDE_CODE_MAX_RETRIES` | 10 | API 请求最大重试次数 | 网络不稳定场景（加大）或成本敏感场景（减小） |
| `CLAUDE_ASYNC_AGENT_STALL_TIMEOUT_MS` | 600000 | 后台子 Agent stall 检测 | 子 Agent 长时间无响应时自动终止 |
| `CLAUDE_STREAM_IDLE_TIMEOUT_MS` | 300000 | 流式响应 body 空闲超时 | 需配合 `CLAUDE_ENABLE_STREAM_WATCHDOG=1` 使用 |

### 权限模式安全

详见下文的 [权限模式](#权限模式) 章节。这里聚焦 `bypassPermissions` 的安全风险：

> 💡 **安全提醒**：`bypassPermissions` 在以下场景中**有明确的风险**：
> - **CI 环境**：如果 CI Runner 有 sudo 权限，`--dangerously-skip-permissions` 会被 Claude Code 拒绝并报错退出。此时应改用 `acceptEdits` + 限制 `allowedTools` 的组合
> - **多租户服务**：一个 Agent 如果有了 `bypassPermissions`，恶意 prompt 可能导致越权操作。建议用 `default` + `canUseTool` 回调实现细粒度审批
> - **生产数据访问**：永远不要给能接触生产数据的 Agent `bypassPermissions`，使用 Hook 做写入审计

---

## 安全注意事项

将 Claude Agent SDK 集成到生产环境时，以下安全要点需要特别注意：

### API Key 管理

API Key 通过环境变量 `ANTHROPIC_API_KEY` 传递给子进程，**绝不要**在代码或配置文件中硬编码。生产环境中应使用密钥管理服务（如 AWS Secrets Manager、HashiCorp Vault）或 CI/CD 的 Secrets 功能注入：

```yaml
# GitHub Actions 示例
env:
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

### 最小权限原则

通过 `allowedTools` 限制 Agent 的能力范围。只读任务只给 `Read`/`Glob`/`Grep` 三个工具；即使使用 `bypassPermissions`，也务必配合严格的 `allowedTools`：

```typescript:src/appendix-c/claudecode/agent-sdk.md
// 只读 Agent——bypassPermissions 在严格工具限制下安全使用
options: { allowedTools: ['Read', 'Glob', 'Grep'], permissionMode: 'bypassPermissions' }
```

### Session 隔离

每个 `query()` 调用默认创建独立子进程，天然具备进程级隔离。多租户场景中，通过不同 `cwd` 和 `settingSources` 确保租户间上下文不交叉污染。

### 输入验证

如果 prompt 来源包含用户输入（如 Web 表单、API 参数），需要在传入 `query()` 前验证和消毒。恶意构造的 prompt 可能导致 Agent 执行意外操作（**Prompt（提示词）** 注入攻击）。

### 审计日志

通过 `PostToolUse` Hook 记录所有工具调用，建立完整的操作审计链。生产环境建议将审计日志写入独立存储（如 ELK、Splunk），保留至少 90 天便于安全事件追溯。

---

## 权限模式

| 模式 | 行为 | 适用场景 |
|------|------|----------|
| `acceptEdits` | 自动批准文件修改，其他操作询问 | 受信的开发工作流 |
| `dontAsk` | 拒绝 `allowedTools` 外的所有操作 | 锁定的无头 Agent |
| `auto` | 模型分类器自动判据 | 带安全护栏的自主 Agent |
| `bypassPermissions` | 全部自动批准（除非有 `ask` 规则） | 沙箱 CI、全信任环境 |
| `default` | 需要 `canUseTool` 回调处理 | 自定义审批流 |

---

## 编程式 Subagent（vs filesystem Subagent）

### Filesystem 方式（来自 `agent-architecture.md`）

```markdown:.claude/agents/code-reviewer.md
---
name: code-reviewer
description: 代码审查专家
model: sonnet
tools: Read Grep Glob
---
```

### SDK 等效实现

```typescript:src/appendix-c/claudecode/agent-sdk.md
import { query } from '@anthropic-ai/claude-agent-sdk'

for await (const message of query({
  prompt: '审查最近的代码变更',
  options: {
    allowedTools: ['Read', 'Glob', 'Grep', 'Agent'],
    agents: {
      'code-reviewer': {
        description: '代码审查专家，关注安全和质量',
        prompt: '你是一个经验丰富的代码审查专家。检查安全漏洞、性能问题和代码异味。',
        tools: ['Read', 'Glob', 'Grep'],
        model: 'sonnet',
      },
    },
  },
}))
if (message.type === 'result') console.log(message.result)
}
```

### SDK 的优势：动态构造 Agent 定义

Filesystem Agent 在编译期就固定了——SDK 的 Agent 定义可以运行时构造：

```typescript:src/appendix-c/claudecode/agent-sdk.md
// 从数据库加载客户配置
function buildReviewAgent(customerConfig: CustomerConfig): AgentDefinition {
  return {
    description: `${customerConfig.name} 的代码审查代理`,
    prompt: `按照以下风格指南审查代码：${customerConfig.styleGuide}`,
    tools: customerConfig.allowedTools,
    model: customerConfig.tier === 'premium' ? 'opus' : 'sonnet',
  }
}
```

> 💡 **设计决策**：为什么 SDK Subagent 不需要 `maxTurns` 参数（在 `AgentDefinition` 中确实可选）？因为 Subagent 的生命周期由主 Agent 管理——主 Agent 的 `maxTurns` 是总预算，Subagent 的轮次消耗计入主 Agent。如果需要限制 Subagent 自己的消耗，可以在 `AgentDefinition` 中显式设置 `maxTurns`，但要注意这可能导致 Subagent 提前终止而无法完成任务。

### 关键约束

1. **在 `allowedTools` 中包含 `Agent`** 才能让主 Agent 调用 Subagent
2. **Subagent 不能嵌套**——Subagent 内部不能有 Agent tool
3. 编程式定义**优先级高于**同名 filesystem Agent

---

## 自定义工具

SDK 允许用 `tool()` 创建自定义工具，结合 `createSdkMcpServer()` 注册到 Agent。

```typescript:src/appendix-c/claudecode/agent-sdk.md
import { tool, createSdkMcpServer } from '@anthropic-ai/claude-agent-sdk'
import { z } from 'zod'

const weatherTool = tool({
  name: 'get_weather',
  description: '获取指定城市的当前天气',
  parameters: z.object({
    city: z.string().describe('城市名称'),
  }),
  execute: async ({ city }) => {
    const res = await fetch(`https://api.weather.com/current/${city}`)
    const data = await res.json()
    return `当前 ${city} 天气：${data.temp}°C，${data.condition}`
  },
})

// 将自定义工具注入 MCP
const mcpServer = createSdkMcpServer({
  tools: [weatherTool],
})

// 在 query 中使用
for await (const message of query({
  prompt: '北京和上海今天哪个更冷？',
  options: {
    allowedTools: ['Read', 'Bash'],
    mcpServers: {
      'weather-server': mcpServer,
    },
  },
})) {
  // Claude 会调用 get_weather 工具
}
```

> 💡 **设计决策**：SDK 用 `createSdkMcpServer()` 而非直接传 `tool()` 的原因是**工具发现机制不同**——MCP 协议定义了标准的工具元数据交换格式（名称、描述、参数 schema），让 Claude 能动态理解工具的能力。直接传函数的话，SDK 需要额外的桥接逻辑将其转译为 MCP 兼容格式。这种设计取舍的结果是：一个 `tool()` 定义可以在多个 MCP server 之间复用，也支持未来替换为真正的远程 MCP server。

---

## Hook 系统

Hook 让你在工具调用前后注入确定性逻辑（验证、审计、阻断），和 filesystem Hook 不同，SDK Hook 是编程式回调：

```typescript:src/appendix-c/claudecode/agent-sdk.md
for await (const message of query({
  prompt: '审查代码并修改发现的 bug',
  options: {
    allowedTools: ['Read', 'Edit', 'Glob', 'Grep', 'Bash'],
    permissionMode: 'acceptEdits',
    hooks: {
      PreToolUse: [
        {
          matcher: 'Edit|Write|MultiEdit',
          hooks: [
            async (input): Promise<HookJSONOutput> => {
              // 只允许修改 src/ 目录下的文件
              if (input.filepath && !input.filepath.startsWith('src/')) {
                return {
                  decision: 'block',
                  stopReason: '不允许修改 src/ 以外的文件',
                  continue: false,
                }
              }
              return { continue: true }
            },
          ],
        },
      ],
    },
  },
})) {
  // ...
}
```

> 💡 **设计决策**：Hook 的 `matcher` 使用正则表达式字符串而非回调函数，原因是**声明式匹配比命令式检查更可组合**——多个 Hook 可以注册到同一个 matcher 上，SDK 内部可以优化匹配性能。如果改为函数回调，每个工具调用前都需要遍历所有 callback 执行匹配逻辑，不具备短路优化的空间。

---

## 错误处理与重试

SDK 的底层是 Claude Code CLI 子进程（通过 `spawn` 启动），子进程的运行模式决定了可能失败的场景。

<!-- 注意：以下错误类型来自 @anthropic-ai/claude-agent-sdk v0.3.x 的实际行为，错误类名因版本可能有差异，请以官方文档为准 -->

### 子进程崩溃

SDK 每次调用 `query()` 都会 spawn 一个 Claude Code 子进程。如果子进程异常退出（如 OOM kill、段错误、Node.js runtime 崩溃），会产生 `ProcessError`：

```typescript:src/appendix-c/claudecode/agent-sdk.md
import { query } from '@anthropic-ai/claude-agent-sdk'

// 子进程崩溃时，for await 循环会抛出异常
try {
  for await (const message of query({
    prompt: '执行复杂分析...',
    options: { maxTurns: 50 },
  })) {
    // 正常消费消息
  }
} catch (err) {
  if (err.message?.includes('exit code')) {
    console.error('子进程异常退出:', err.message)
    // 可以重试整个 query()
  }
}
```

**常见崩溃原因**：

| 症状 | 典型原因 | 处理方式 |
|------|---------|---------|
| 退出码 137 | 被 OOM killer 杀死（内存不足） | 增加系统内存或减小上下文 |
| 退出码 1 + "stderr" 内容 | Claude Code 内部解析器崩溃 | 重试或升级 SDK 版本 |
| EPIPE（写管道断裂） | 子进程在写入时死亡 | 捕获 EPIPE，重试 query |
| 进程挂起 + 初始化超时 | 子进程初始化卡死 | `startup()` 的 `initializeTimeoutMs` 参数控制超时时间 |

### 请求超时

长时间运行的 Agent 可能因为 API 响应慢或模型推理卡住导致超时。SDK 支持通过 `AbortSignal` 从外部取消，同时也可以通过环境变量控制内部超时：

```typescript:src/appendix-c/claudecode/agent-sdk.md
// 使用 AbortSignal 控制超时
const controller = new AbortController()
setTimeout(() => controller.abort(), 120_000) // 120 秒总超时

try {
  for await (const message of query({
    prompt: '分析大型日志文件',
    options: {
      allowedTools: ['Read', 'Bash', 'Glob', 'Grep'],
      maxTurns: 100,
      signal: controller.signal, // 传递 AbortSignal
      env: {
        API_TIMEOUT_MS: '120000',      // 每轮 2 分钟超时
        CLAUDE_CODE_MAX_RETRIES: '3',   // 最多重试 3 次
      },
    },
  })) {
    if (message.type === 'assistant') {
      process.stdout.write(message.message.content[0]?.text ?? '')
    }
  }
} catch (err) {
  if (err.name === 'AbortError') {
    console.log('操作被用户取消')
  } else {
    console.error('操作失败:', err.message)
  }
}
```

### 流中断

`query()` 返回 async 生成器。如果生成器在中间被 break 或子进程意外终止，SDK 会触发资源清理：

```typescript:src/appendix-c/claudecode/agent-sdk.md
let turnCount = 0

for await (const message of query({
  prompt: '遍历并分析项目所有源码文件',
  options: { maxTurns: 500 },
})) {
  if (message.type === 'result') {
    turnCount = message.num_turns ?? turnCount
    console.log('已完成', turnCount, '轮')
  }

  // 如果已经拿到足够信息，提前中断
  if (turnCount > 50 && hasEnoughData()) {
    break // break 会触发 SDK 的 close() 清理
  }
}
// break 后 SDK 自动清理子进程资源
```

### 重试模式

对于 transient 故障（网络抖动、临时超时、进程初始化失败），推荐使用带指数退避的重试包装器：

```typescript:src/appendix-c/claudecode/agent-sdk.md
import { query } from '@anthropic-ai/claude-agent-sdk'

async function* queryWithRetry(
  prompt: string,
  options: object,
  maxRetries = 3
): AsyncGenerator {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      for await (const message of query({ prompt, options })) {
        yield message // 透传所有消息
      }
      return // 成功完成，不继续重试
    } catch (err) {
      const isRetryable = isRetryableError(err)

      if (!isRetryable || attempt === maxRetries) {
        throw err // 不可重试或已达最大次数
      }

      const waitMs = Math.min(1000 * Math.pow(2, attempt - 1), 30_000)
      console.warn(
        `查询失败（第 ${attempt} 次），${waitMs}ms 后重试:`,
        err.message
      )
      await new Promise(resolve => setTimeout(resolve, waitMs))
    }
  }
}

function isRetryableError(err: unknown): boolean {
  const msg = (err as Error)?.message ?? ''
  // 子进程退出（非 OOM）、连接超时、EPIPE 等 transient 错误可重试
  if (msg.includes('exit code') && !msg.includes('137')) return true
  if (msg.includes('timeout') || msg.includes('ETIMEDOUT')) return true
  if (msg.includes('EPIPE')) return true
  if (msg.includes('Connection')) return true
  // OOM（137）不可重试——重试只会再次 OOM
  // 权限相关错误不可重试——需要修改配置
  return false
}

// 使用示例
async function main() {
  for await (const message of queryWithRetry(
    '分析 src/ 的代码结构',
    {
      allowedTools: ['Read', 'Glob', 'Grep'],
      maxTurns: 20,
      env: { API_TIMEOUT_MS: '120000' },
    },
    3
  )) {
    if (message.type === 'assistant') {
      for (const block of message.message.content) {
        if ('text' in block) console.log(block.text)
      }
    }
  }
}
```

> 💡 **设计决策**：为什么错误处理需要异步生成器包装器而非 SDK 内置重试？因为 SDK 的自动重试（通过 `CLAUDE_CODE_MAX_RETRIES`）只在**API 请求层面**重试——它重试的是单个 API 调用。如果子进程整体崩溃，API 重试机制无法恢复。外层重试是整个 `query()` 级别的，它重新 spawn 子进程，适合子进程级故障。

---

## 完整实战：数据分析 Agent

以下是一个完整的 SDK 数据分析 Agent——它会读取项目中的 CSV 数据文件，执行统计分析，并生成结构化报告。

### 架构设计

```
你的应用 (Node.js)
  │
  ├─ query() → 启动 Claude Code 子进程
  │     │
  │     ▼  (Agent 循环)
  │  1. Glob 查找 *.csv
  │  2. Read 读取文件内容
  │  3. Bash: wc -l, head -1, awk 分析
  │  4. 生成分析报告
  │     │
  └─ 消费 async 流 → 输出结果
```

### 完整代码

```typescript:data-analysis-agent.ts
import { query } from '@anthropic-ai/claude-agent-sdk'
import { appendFileSync } from 'fs'

interface AnalysisResult {
  files: Array<{
    name: string
    rows: number
    columns: number
    columnNames: string[]
    nullCount: number
  }>
  summary: {
    totalFiles: number
    totalDataRows: number
    issues: string[]
  }
}

async function analyzeCsvData(projectDir: string): Promise<void> {
  const reportLines: string[] = []
  let finalResult: AnalysisResult | null = null

  for await (const message of query({
    prompt: `
      分析 "${projectDir}" 目录中的所有 CSV 文件。

      执行步骤：
      1. 用 Glob 搜索所有 *.csv 文件
      2. 对每个 CSV 文件，使用 Bash 命令：
         - wc -l 统计总行数
         - head -1 获取列名
         - awk -F',' '{print NF; exit}' 统计列数
         - awk -F',' '{for(i=1;i<=NF;i++) if($i=="") count++} END{print count+0}' 统计空值
      3. 汇总所有文件的分析结果
      4. 输出严格 JSON 格式的分析报告，不要包含任何额外文字
      
      JSON Schema:
      {
        "files": [{ "name": string, "rows": number, "columns": number, "columnNames": string[], "nullCount": number }],
        "summary": { "totalFiles": number, "totalDataRows": number, "issues": string[] }
      }
    `,
    options: {
      cwd: projectDir,
      allowedTools: ['Glob', 'Read', 'Bash', 'Grep'],
      permissionMode: 'bypassPermissions',
      maxTurns: 30,
      model: 'sonnet',
    },
  })) {
    // 实时收集输出
    if (message.type === 'assistant') {
      for (const block of message.message.content) {
        if ('text' in block && block.text) {
          reportLines.push(block.text)
          process.stdout.write(block.text) // 实时显示
        }
      }
    }

    if (message.type === 'result') {
      console.log(`\n--- 分析完成: ${message.subtype} ---`)
      if (message.subtype === 'success') {
        // 从输出中提取 JSON
        const fullText = reportLines.join('')
        const jsonMatch = fullText.match(/\{[\s\S]*\}/)
        if (jsonMatch) {
          try {
            finalResult = JSON.parse(jsonMatch[0]) as AnalysisResult
          } catch {
            console.warn('无法解析 JSON 输出，将使用原始文本')
          }
        }
      }
    }
  }

  // 输出格式化报告
  if (finalResult) {
    console.log('\n=== 数据分析报告 ===')
    console.log(`扫描文件: ${finalResult.summary.totalFiles}`)
    console.log(`数据总行数: ${finalResult.summary.totalDataRows}`)

    for (const file of finalResult.files) {
      console.log(`\n📄 ${file.name}`)
      console.log(`  行数: ${file.rows} | 列数: ${file.columns}`)
      console.log(`  列名: ${file.columnNames.join(', ')}`)
      console.log(`  空值: ${file.nullCount}`)
    }

    if (finalResult.summary.issues.length > 0) {
      console.log('\n⚠️ 数据质量问题:')
      finalResult.summary.issues.forEach(i => console.log(`  - ${i}`))
    }

    // 保存报告到文件
    const report = `# Data Analysis Report
Generated: ${new Date().toISOString()}
Total Files: ${finalResult.summary.totalFiles}
Total Rows: ${finalResult.summary.totalDataRows}

## File Details
${finalResult.files.map(f =>
  `- ${f.name}: ${f.rows} rows, ${f.columns} columns`
).join('\n')}

## Issues
${finalResult.summary.issues.map(i => `- ${i}`).join('\n') || 'None'}
`
    appendFileSync('analysis-report.md', report)
    console.log('\n报告已保存到 analysis-report.md')
  }
}

// 运行
analyzeCsvData('/path/to/data').catch(console.error)
```

> 💡 **设计决策**：这个示例选择 `maxTurns: 30` 而非更大的值，因为数据分析是**读密集型**任务——读文件（1-2 轮）、统计分析（每文件 2-3 轮）、汇总输出（1 轮）。对于 5 个 CSV 文件，大约需要 15-20 轮。30 轮留有余量但不会让 Agent 无限循环。如果分析发现数据质量问题需要额外修复，可以在成功分支后启动新的 query。

> 💡 **设计决策**：prompt 最后要求"输出严格 JSON 格式...不要包含任何额外文字"——这不是锦上添花，而是**生产必需的约束**。没有这句，Claude 经常在 JSON 前后加解释文字，导致 `JSON.parse` 失败。即便如此，代码中还是有 `jsonMatch` 回退逻辑——双重保险。

### Hook 增强版：审计日志

添加一个 PostToolUse Hook 记录 Agent 的每个操作：

```typescript:src/appendix-c/claudecode/agent-sdk.md
const auditLog: string[] = []

for await (const message of query({
  prompt: '分析 CSV 数据',
  options: {
    allowedTools: ['Glob', 'Read', 'Bash', 'Grep'],
    permissionMode: 'bypassPermissions',
    maxTurns: 30,
    hooks: {
      PostToolUse: [
        {
          matcher: '*', // 匹配所有工具
          hooks: [
            async (input) => {
              auditLog.push(`[${new Date().toISOString()}] ${input.toolName}: ${JSON.stringify(input.input)}`)
              return { continue: true }
            },
          ],
        },
      ],
    },
  },
})) {
  // 消费消息
}
```

> 💡 **设计决策**：使用 `matcher: '*'` 匹配所有工具意味着可以全局审计，但在某些场景中会产生大量日志（例如 Bash 工具的每次输出）。如果需要生产级别的审计，建议在 `PreToolUse` 中记录调用意图，在 `PostToolUse` 中记录执行结果和耗时，形成完整的调用链路。

### 完整 CI 集成示例

```yaml
# .github/workflows/data-analysis.yml
name: Data Analysis
on:
  pull_request:
    paths: ['data/**/*.csv']

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm install @anthropic-ai/claude-agent-sdk
      - name: Run data analysis
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: npx tsx data-analysis-agent.ts
      - name: Comment PR
        uses: actions/github-script@v7
        with:
          script: |
            const fs = require('fs')
            const report = fs.readFileSync('analysis-report.md', 'utf8')
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: report
            })
```

### Docker 部署说明

Claude Agent SDK 的子进程模式在容器化环境中需要额外注意：

- **子进程权限**：`query()` 内部 spawn 的 Claude Code 子进程继承容器用户的权限。建议在 Dockerfile 中使用非 root 用户运行，遵循最小权限原则
- **资源限制**：通过 Docker 的 `--memory` 和 `--cpus` 限制容器资源，避免 OOM kill（子进程退出码 137）导致任务中断
- **环境变量注入**：所有 SDK 配置（API Key、超时参数）通过容器环境变量传入，确保 `ANTHROPIC_API_KEY` 不写入镜像层
- **预热策略**：如果需要在容器内多次调用 `query()`，使用 `startup()` 预热可减少每次调用的子进程启动开销

---

## 对比 Claude Code CLI vs SDK 工作流

| 场景 | CLI 方式 | SDK 方式 |
|------|---------|----------|
| 交互式编码 | `claude` TUI | — |
| 一次审查 | `claude -p "审查这个 PR"` | `query({ prompt: "审查...", options: {...} })` |
| CI/CD 集成 | `claude -p "运行测试并修复"` | 嵌入 CI 脚本，处理返回结果 |
| 自定义审批 | 权限提示 | `canUseTool` 回调或 Hook |
| 会话持久化 | 自动 | `sessionId` 参数手动管理 |
| 多 Subagent 并行 | CLI 后台任务 | 多个 `query()` 并行 |
| 自定义工具 | 不支持 | `tool()` + `createSdkMcpServer()` |
| 预热加速 | 不支持 | `startup()` 预初始化 |
| 错误恢复 | 重开 TUI 会话 | 编程式重试 + 指数退避 |
| 成本控制 | 手动估算 | `maxBudgetUsd` + `env` 超时参数 |
| 上下文管理 | 自动不可控 | `settingSources` + PreCompact Hook + `/compact` |

---

## 最佳实践

### 1. 用 `startup()` 预热

对延迟敏感的服务，在初始化阶段调用 `startup()`，后续 query 可省去 1-2 秒的子进程启动时间。

> 💡 `startup()` 的本质是**连接池模式**——保持一个空闲子进程。如果服务重启频繁（如 serverless 函数），预热收益有限，可直接使用 `query()`。

### 2. 设置合理的 `maxTurns`

```typescript:src/appendix-c/claudecode/agent-sdk.md
// 简单任务——限制轮次，防止 runaway
options: { maxTurns: 10 }

// 复杂任务——允许更多推理步骤
options: { maxTurns: 50 }
```

> 💡 `maxTurns` 不是精确预算而是安全网。如果任务频繁达到上限，应增大限制或拆分任务，而非压缩已设置的值。

### 3. 组合 `permissionMode` 和 `allowedTools`

```typescript:src/appendix-c/claudecode/agent-sdk.md
// 只读分析 Agent
options: {
  allowedTools: ['Read', 'Glob', 'Grep'],
  permissionMode: 'bypassPermissions', // 安全：只有读工具
}

// 全功能 Agent（沙箱环境）
options: {
  allowedTools: ['Read', 'Write', 'Edit', 'Bash', 'Glob', 'Grep', 'Agent'],
  permissionMode: 'bypassPermissions',
}
```

> 💡 `permissionMode: 'bypassPermissions'` + 严格限制的 `allowedTools` 组合是推荐的安全模式。`bypassPermissions` 本身并不可怕，可怕的是给了 Agent 所有工具又用 `bypassPermissions`。

### 4. 在 `systemPrompt` 中使用 preset + append

保留 Claude Code 默认系统提示词的基础能力，再附加你的指令：

```typescript:src/appendix-c/claudecode/agent-sdk.md
options: {
  systemPrompt: {
    type: 'preset',
    preset: 'claude_code',
    append: '所有输出必须使用中文。重点关注性能问题。',
  },
}
```

> 💡 选择 `preset: 'claude_code'` 而非自定义完整 system prompt 的原因是 Claude Code 预设包含了**平台特定的工具描述和安全指令**。完全替换可能导致工具描述不完整或安全护栏缺失。

### 5. Hook 增强与审计

使用 Hook 实现审计日志、安全策略和数据脱敏——这是 SDK 相比于 CLI 的独特优势。

### 6. 会话持久化

需要跨多次 `query()` 保留上下文时，使用 sessionId：

```typescript:src/appendix-c/claudecode/agent-sdk.md
let sessionId: string | undefined

// 第一次 query
for await (const msg of query({
  prompt: '读取配置文件',
  options: { allowedTools: ['Read'] },
})) {
  if (msg.type === 'system' && msg.subtype === 'init') {
    sessionId = msg.session_id
  }
}

// 第二次 query（恢复上下文）
for await (const msg of query({
  prompt: '根据刚才的配置，修改数据库连接字符串',
  options: { allowedTools: ['Read', 'Edit'], sessionId },
})) {
  // sessionId 让 Agent 记得上一次的上下文
}
```

> 💡 会话持久化依赖 filesystem 存储（session 文件保存在本地），如果部署在多容器环境中，session 文件不会自动共享。需要自行实现 session-store 持久化（如保存到数据库）或使用外部状态管理。

### 7. 生产部署清单

将 SDK Agent 部署到生产环境前，对照检查：

- [ ] `maxTurns` 已设置（防止无限循环）
- [ ] `maxBudgetUsd` 已设置（防止意外超支）
- [ ] `env` 中配置了合理的 `API_TIMEOUT_MS` 和 `CLAUDE_CODE_MAX_RETRIES`
- [ ] `settingSources` 按需配置（CI 环境应使用 `[]`）
- [ ] 包含错误处理和重试逻辑（`queryWithRetry` 包装器）
- [ ] 敏感环境使用 `acceptEdits` + Hook 而非 `bypassPermissions`
- [ ] 有监控手段捕获 `result` 消息的 `subtype`
- [ ] 子进程崩溃后有清理和恢复机制

---

## 与 OpenCode SDK 的差异

| 维度 | Claude Agent SDK | OpenCode SDK |
|------|-----------------|--------------|
| **包名** | `@anthropic-ai/claude-agent-sdk` | `@opencode-ai/sdk` |
| **架构** | 子进程（spawn Claude Code CLI） | REST API 客户端 |
| **入口** | `query()` async 生成器 | `createOpencodeClient()` + `.session.prompt()` |
| **自定义工具** | `tool()` + `createSdkMcpServer()` | 通过 **Plugin（插件）** 系统 |
| **子 Agent** | `agents` 参数（`AgentDefinition`） | 在 prompt 中 @mention |
| **Hook** | `PreToolUse`/`PostToolUse` 回调 | Plugin Hook 链 |
| **预热** | `startup()` 支持 | 无需预热（已运行 Server） |
| **是否需 CLI** | 自动附带 | 仅需 Server 端 |
| **执行隔离** | `cwd` + `settingSources` | Session 维度隔离 |

---

## 相关章节

- → [Claude Code SDK 参考](./sdk.md) — 三层次 SDK 总览（MCP / Hooks / CLI / 天气 Agent 案例）
- → [Claude Code Agent 设计指南](./agent-architecture.md) — Filesystem Subagent 方式（配置文件比）
- → [Claude Code 扩展机制](./extensions.md) — 六层扩展体系
- → [Claude Code 命令参考](./commands.md) — CLI 命令参考
- → [Claude Code 生态参考](./ecosystem.md) — 社区扩展和最佳实践
- → [OpenCode SDK](../opencode/agent-sdk.md) — 对应功能的对比参考
- → [Agent SDK 官方文档](https://code.claude.com/docs/en/agent-sdk/overview) — Anthropic 官方 SDK 文档

---

## 读者视角

### 适用读者角色
- 入门开发者 — 需要快速上手 Claude Code 的 Agent 体系
- 智能体开发工程师 — 需要设计、调试、进化 Claude Code 中的自定义 Agent 和 Subagent
- 效率开发者 — 已有 AI 工具经验，想通过 Claude Code 提升 2x+ 效率
- 技术负责人 — 需要评估 Claude Code 的技术可行性和团队级 **Harness Engineering（驾驭工程）** 体系
- **Skill（技能）**作者 — 需要开发自定义 Skill 和 MCP 桥接，实现团队最佳实践复用

### 典型使用场景
- 需要编程式驱动 Agent 引擎
- 需要嵌入 Claude Code 到自定义应用中
- 需要实现 CI/CD 流水线集成
- 需要开发自定义工具和 MCP 服务器
- 需要实现生产级 Agent 配置和管理

### 使用示例
```typescript:src/appendix-c/claudecode/agent-sdk.md
import { query } from '@anthropic-ai/claude-agent-sdk'

async function main() {
  for await (const message of query({
    prompt: '这个目录下有哪些文件？',
    options: {
      allowedTools: ['Bash', 'Glob'],
      permissionMode: 'bypassPermissions',
    },
  })) {
    if (message.type === 'assistant') {
      for (const block of message.message.content) {
        if ('text' in block) console.log(block.text)
      }
    }
    if (message.type === 'result') {
      console.log('Done:', message.subtype)
    }
  }
}

main()
```

### 工程化示例

**配置顺序检查表：**

1. **第1步：安装 SDK**
   ```bash
   npm install @anthropic-ai/claude-agent-sdk
   ```

2. **第2步：初始化 Agent**
   ```typescript:src/appendix-c/claudecode/agent-sdk.md
   import { query } from '@anthropic-ai/claude-agent-sdk'
   
   for await (const message of query({
     prompt: '分析这个代码库',
     options: {
       allowedTools: ['Read', 'Glob', 'Grep'],
       permissionMode: 'acceptEdits',
       maxTurns: 50,
     },
   })) {
     // 处理消息
   }
   ```

3. **第3步：配置 MCP 服务器**
   ```typescript:src/appendix-c/claudecode/agent-sdk.md
   import { createSdkMcpServer } from '@anthropic-ai/claude-agent-sdk'
   
   const mcpServer = createSdkMcpServer({
     tools: [weatherTool],
   })
   ```

### 与前/后文章的衔接
- ← [Claude Code Agent 设计指南](./agent-architecture.md) — Subagent 配置方式对比参考
- → [Claude Code SDK 参考](./sdk.md) — 三层次 SDK 总览
