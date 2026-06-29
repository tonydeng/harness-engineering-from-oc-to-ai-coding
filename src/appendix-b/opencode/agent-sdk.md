# OpenCode SDK：编程式 **Agent（智能体）** 开发

> 通过 `@opencode-ai/sdk` 用代码控制 OpenCode Server，实现 CI/CD 集成、自定义工作流和远程 Agent 调度。

OpenCode SDK 提供了一套类型安全的 JavaScript/TypeScript 客户端，通过 REST API 与运行中的 OpenCode Server 通信。和 [oh-my-openagent **Agent（智能体）** 设计与开发指南](./agent-architecture.md) 中介绍的配置式自定义 Agent（Category/`task()`）不同，SDK 面向的是**将 OpenCode 嵌入到你的应用或流水线中**的场景。

---

## SDK vs 配置式 Agent

在决定使用 SDK 之前，先理解它与配置式自定义 Agent 的适用边界：

| 维度 | 配置式 Agent（`agent-architecture.md`） | SDK 编程式 | 取舍分析 |
|------|---------------------------------------|-----------|---------|
| **本质** | 在 OMO 框架内定义 Agent 行为（Category + **Skill（技能）**） | 通过 REST API 远程控制 OpenCode Server | 配置式 Agent 天然获得 OMO 的 **Plugin（插件）** Hook、Skill 系统等生态支持；SDK 是 HTTP 客户端，无法利用框架内部机制。如果你的业务逻辑大部分在 OpenCode 内部完成，配置式更省心；如果 OpenCode 只是你系统中的一个组件，SDK 更灵活 |
| **调用方式** | `task()` 函数，由 OMO 调度 | `client.session.prompt()` HTTP API 调用 | `task()` 是同步调用，由 OMO 调度器管理优先级和并发；`session.prompt()` 是 HTTP 请求，你需要自己管理超时、重试和并发控制。SDK 方式更灵活但责任也更大 |
| **执行环境** | OpenCode TUI 会话内 | 任意 Node.js/浏览器/CI 环境 | 配置式 Agent 绑定在 TUI 会话生命周期内，无法脱离终端运行；SDK 可以在任何有 HTTP 网络的环境中运行，包括 CI/CD Runner、Serverless Function 甚至是浏览器端。这是选择 SDK 的最强理由 |
| **Agent 定义** | `oh-my-openagent.jsonc` 中的 Category 配置 | 无法定义新 Agent；使用现有 Agent /@ 提到子 Agent | 配置式可以在 JSON 中声明完整的 Agent 行为（system prompt、温度、工具权限等）；SDK 只能使用已经存在的 Agent，Agent 的定义仍需在配置层完成。如果你的 Agent 需要精细的权限控制和工具白名单，配置式更合适 |
| **适用场景** | 交互式开发、TUI 工作流 | CI/CD 流水线、Web 应用、自定义工具链 | 交互式开发中配置式更方便，`task()` 调用无缝集成工作流；SDK 的场景是"把 OpenCode 当服务调用"，适合完全自动化的任务。需要人工介入和实时调整的场景选配置式，完全自动化选 SDK |
| **状态管理** | 会话持久化在 TUI 中 | 每次 `prompt()` 是独立请求，可绑定 Session | 配置式 Agent 的上下文由 OMO 自动维护，多轮调用上下文自动延续；SDK 每次调用上下文通过在同一个 Session 中累积来保持。这意味着你需要自己设计上下文的生命周期和 compaction 策略 |
| **内置能力** | 完整 OMO Hook 链、Skill 系统、Team Mode | REST API 暴露的能力子集 | 配置式拥有完整的工具链、Hook 链、Skill 系统等所有内置能力；SDK 通过 REST API 暴露了核心功能的子集——文件操作、搜索、会话管理等都可用，但 Plugin 系统、TUI 交互、某些高级 Agent 功能不可用 |

**一句话选型**：你在 TUI 里工作 → 配置式 Agent；你要把 OpenCode 能力嵌入自己的应用 → SDK。

---

## 安装与初始化

```bash
npm install @opencode-ai/sdk
```

### 创建 Server + Client（一体式启动）

```typescript:src/appendix-b/opencode/agent-sdk.md
import { createOpencode } from '@opencode-ai/sdk'

const { client, server } = await createOpencode({
  hostname: '127.0.0.1',
  port: 4096,
  config: {
    model: 'anthropic/claude-sonnet-4-6',
  },
})

// 检查连接
const health = await client.global.health()
console.log(`Server version: ${health.data.version}`)
```

> 💡 **设计决策**：这里显式指定 `hostname: '127.0.0.1'` 而非 `'0.0.0.0'`，是为了确保 Server 只监听本地回环地址，避免暴露到局域网或被外部扫描到。如果你需要从其他机器访问（例如 Docker 容器中），才改成 `0.0.0.0`。

`createOpencode()` 会自动启动一个 OpenCode Server 实例（相当于 `opencode serve`），连接成功后返回 `client` 供后续操作。用完记得 `server.close()`。

> 💡 **设计决策**：`createOpencode()` 一体化方案适合测试和开发环境。生产环境中推荐 Server 独立部署，应用侧只使用 `createOpencodeClient()` 连接。这样可以做到 Server 复用、热更新不断连。

### 仅创建 Client（连接已有 Server）

如果你的 OpenCode Server 已经在运行（手动启动或由其他进程管理），使用 `createOpencodeClient()`：

```typescript:src/appendix-b/opencode/agent-sdk.md
import { createOpencodeClient } from '@opencode-ai/sdk'

const client = createOpencodeClient({
  baseUrl: 'http://localhost:4096',
})

const sessions = await client.session.list()
console.log(`Active sessions: ${sessions.data.length}`)
```

> 💡 **设计决策**：`createOpencodeClient()` 的 `baseUrl` 默认为 `http://localhost:4096`。如果你在 CI 环境中运行，Server 可能在临时端口上启动，需要从环境变量读取端口号再传入。另外，`createOpencodeClient` 默认不抛出 HTTP 错误（`throwOnError: false`），生产环境建议设为 `true` 以便及时发现连接问题。

### 从 E2B Sandbox 连接

OpenCode SDK 也支持在 E2B Sandbox 中运行，实现完全隔离的执行环境：

```typescript:src/appendix-b/opencode/agent-sdk.md
import { Sandbox } from 'e2b'
import { createOpencodeClient } from '@opencode-ai/sdk'

const sandbox = await Sandbox.create('opencode', {
  envs: { ANTHROPIC_API_KEY: process.env.ANTHROPIC_API_KEY },
  timeoutMs: 10 * 60 * 1000,
})

// 启动 OpenCode Server
sandbox.commands.run('opencode serve --hostname 0.0.0.0 --port 4096', { background: true })

// 等待 Server 就绪
const host = sandbox.getHost(4096)
while (true) {
  try { await fetch(`https://${host}/global/health`); break }
  catch { await new Promise(r => setTimeout(r, 500)) }
}

const client = createOpencodeClient({ baseUrl: `https://${host}` })
```

> 💡 **设计决策**：这里的轮询等待（retry loop）是必须的——Sandbox 环境启动 Server 是异步的，不等待就发起请求会得到连接拒绝。500ms 间隔是经验值：太快会增加无谓的请求数，太慢会拖长冷启动时间。生产环境中可替换为 `AbortSignal` 控制的超时轮询（见"运行时防护"一节）。

---

## API 总览

SDK 的能力按命名空间组织，以下是核心方法速查：

### 会话管理（`client.session.*`）

| 方法 | 描述 | 返回 |
|------|------|------|
| `session.list()` | 列出所有会话 | `Session[]` |
| `session.get({ path })` | 获取单个会话详情 | `Session` |
| `session.create({ body })` | 创建新会话 | `Session` |
| `session.update({ path, body })` | 更新会话属性（标题等） | `Session` |
| `session.delete({ path })` | 删除会话 | `boolean` |
| `session.abort({ path })` | 中止运行中的会话 | `boolean` |
| `session.prompt({ path, body })` | 发送提示词（核心方法） | `AssistantMessage`（默认）或 `UserMessage`（`noReply: true`）|
| `session.command({ path, body })` | 发送命令给会话 | `{ info, parts }` |
| `session.shell({ path, body })` | 在会话中执行 Shell 命令 | `AssistantMessage` |
| `session.messages({ path })` | 列出会话中的消息列表 | `{ info, parts }[]` |
| `session.message({ path })` | 获取单条消息详情 | `{ info, parts }` |
| `session.summarize({ path, body })` | 手动触发会话摘要/压缩 | `boolean` |
| `session.revert({ path, body })` | 回退到指定消息 | `Session` |
| `session.unrevert({ path })` | 恢复被回退的消息 | `Session` |
| `session.share({ path })` | 分享会话 | `Session` |
| `session.unshare({ path })` | 取消分享 | `Session` |

### 文件与搜索（`client.find.*` / `client.file.*`）

| 方法 | 描述 |
|------|------|
| `find.text({ query })` | 正则搜索文件内容 |
| `find.files({ query })` | 按模式查找文件路径 |
| `find.symbols({ query })` | 搜索代码符号 |
| `file.read({ query })` | 读取文件内容 |
| `file.list({ query? })` | 列出项目跟踪文件 |
| `file.status({ query? })` | 查看文件的状态变更 |

### 配置与应用（`client.config.*` / `client.app.*`）

| 方法 | 描述 |
|------|------|
| `config.get()` | 获取当前配置 |
| `config.providers()` | 列出配置的 Provider 和默认模型 |
| `app.agents()` | 列出所有可用 Agent |
| `app.log()` | 写入日志 |

### 其他命名空间

| 命名空间 | 描述 | 典型用途 |
|---------|------|---------|
| `client.global.*` | Server 状态检查 | `global.health()` 连接健康检查 |
| `client.project.*` | 项目信息 | `project.current()` 获取当前项目路径 |
| `client.path.*` | 路径查询 | `path.get()` 获取 Server 当前工作目录 |
| `client.auth.*` | Provider 认证 | `auth.set()` 动态设置 API Key |
| `client.event.*` | 实时事件流 | `event.subscribe()` 监听 Server 事件 |
| `client.tui.*` | TUI 控制 | `tui.showToast()`、`tui.appendPrompt()` |

### 结构化输出

SDK 的 `session.prompt()` 支持 `format` 参数，让 AI 返回 JSON 格式的结构化数据，而非自然语言：

```typescript:src/appendix-b/opencode/agent-sdk.md
const result = await client.session.prompt({
  path: { id: sessionId },
  body: {
    parts: [{ type: 'text', text: '分析这个目录下的 TypeScript 文件数量' }],
    format: {
      type: 'json_schema',
      schema: {
        type: 'object',
        properties: {
          totalFiles: { type: 'number' },
          directories: { type: 'array', items: { type: 'string' } },
        },
      },
    },
  },
})
```

> 💡 **设计决策**：结构化输出使用 `format` 参数而非 `outputFormat`（旧版 SDK 曾用名）。模型会通过 `StructuredOutput` 工具返回经过 Schema 校验的 JSON，避免了解析自然语言的脆弱性。对复杂 Schema 可设置 `retryCount`（默认 2 次），让模型在输出不符合 Schema 时自动重试。

这对于将 SDK 嵌入自动化流水线非常关键——不再需要解析自然语言输出。

---

## 上下文管理

> 上下文（**Context（上下文）**）是 SDK 编程中最容易被忽视的陷阱——Session 累积的消息越多，Token 消耗越大，响应越慢，最终超出模型上下文窗口。

### 自动压缩（Auto-Compaction）

OpenCode Server 内置了自动上下文压缩机制：

- **触发阈值**：当 Session 的 `PromptTokens + CompletionTokens` 达到模型上下文窗口的 **95%** 时，Server 自动触发压缩
- **压缩过程**：使用专用 Agent（`AgentSummarizer`）对先前的对话生成摘要摘要消息，替代原始的多轮对话。原始消息被归档，新消息在摘要后续接
- **标记**：压缩后 Session 的 `SummaryMessageID` 字段指向摘要消息；`PromptTokens` 和 `CompletionTokens` 计数器重置

```typescript:src/appendix-b/opencode/agent-sdk.md
// 查看 Session 的 Token 消耗状态
const { data: session } = await client.session.get({
  path: { id: sessionId },
})

console.log({
  promptTokens: session.promptTokens,       // 当前累积的输入 Token
  completionTokens: session.completionTokens, // 当前累积的输出 Token
  summaryMessageId: session.summaryMessageID, // 非空表示已压缩
  cost: session.cost,                         // 累计消耗金额（USD）
})
```

### 手动压缩

在 TUI 中可以用 `/compact` 命令手动触发压缩。通过 SDK 可以调用 `session.summarize()`：

```typescript:src/appendix-b/opencode/agent-sdk.md
await client.session.summarize({
  path: { id: sessionId },
  body: { messageID: lastMessageId },
})
```

> 💡 **设计决策**：`session.summarize()` 指定 `messageID` 表示从该消息之前的对话进行压缩，保留后续消息的完整性。如果不指定，Server 会压缩整个会话的历史。建议在长会话中每隔 20-30 轮对话手动触发一次压缩，避免到达自动阈值时的一次性压缩导致上下文剧烈变化。

### Token 预算意识

```typescript:src/appendix-b/opencode/agent-sdk.md
// 在每次 prompt 后检查 Token 消耗
const { data: result } = await client.session.prompt({
  path: { id: session.id },
  body: { parts: [{ type: 'text', text: prompt }] },
})

// 通过 session.get() 获取更新后的 Token 计数
const { data: updated } = await client.session.get({
  path: { id: session.id },
})

// 当超过阈值时主动切换 Session
const TOKEN_WARNING = 50_000 // 经验值：视模型上下文窗口调整
if ((updated.promptTokens + updated.completionTokens) > TOKEN_WARNING) {
  console.warn(`Session ${session.id} 已接近上下文限制，建议创建新会话`)
}
```

### 最佳实践：何时重建 Session

| 条件 | 建议 |
|------|------|
| 单轮 prompt 即可完成的任务 | 每次创建新 Session，用完即删 |
| 多轮对话，< 20 轮 | 复用 Session，依赖自动压缩 |
| 长对话，> 30 轮 | 主动调用 `session.summarize()` 或在逻辑检查点创建新 Session |
| 跨不同任务的调用 | 不同任务用不同 Session，避免上下文串扰 |

**核心原则**：同一个 Session 共享全部上下文。如果你的应用逻辑中，步骤 B 不需要知道步骤 A 的细节（例如两个独立的数据分析任务），就创建两个 Session 并行执行。这比在一个 Session 中串行更高效，且不会互相污染上下文。

---

## 运行时防护

生产环境中使用 SDK 不能只关注功能正确性，还要考虑运行时的安全边界。

### 最大响应 Token 控制

在 `createOpencode()` 的 `config` 中设置模型的 `maxTokens` 限制：

```typescript:src/appendix-b/opencode/agent-sdk.md
const { client } = await createOpencode({
  hostname: '127.0.0.1',
  port: 4096,
  config: {
    model: 'anthropic/claude-sonnet-4-6',
    maxTokens: 4096, // 限制每次响应的最大 Token 数
  },
})
```

> 💡 **设计决策**：设置 `maxTokens` 是一种成本控制手段——模型可能在某些 prompt 下生成超长输出（比如要求"列出所有文件"），没有上限时 Token 消耗会失控。对于简单问答 1024 足够，代码生成建议 4096，复杂分析可以设到 8192。如果你通过 `createOpencodeClient()` 连接已有 Server，需要在 Server 的 `opencode.json` 中配置此项。

### 超时处理（AbortSignal）

`createOpencode()` 支持传入 `AbortSignal` 和超时时间：

```typescript:src/appendix-b/opencode/agent-sdk.md
import { createOpencode } from '@opencode-ai/sdk'

const controller = new AbortController()

// 30 秒超时自动中止
const timeout = setTimeout(() => controller.abort(), 30_000)

try {
  const { client } = await createOpencode({
    hostname: '127.0.0.1',
    port: 4096,
    signal: controller.signal,  // 支持取消 Server 启动
    timeout: 5000,              // Server 启动超时（毫秒）
    config: { model: 'anthropic/claude-sonnet-4-6' },
  })

  // 发送 prompt 时也可能长时间无响应
  const result = await client.session.prompt({
    path: { id: sessionId },
    body: { parts: [{ type: 'text', text: '分析这个大型代码库...' }] },
  })
} catch (err) {
  if (controller.signal.aborted) {
    console.error('请求超时，已自动取消')
  } else {
    console.error('其他错误:', err)
  }
} finally {
  clearTimeout(timeout)
}
```

对于长时间运行的分析任务，可以在客户端设置一个 HTTP 级别的超时。`createOpencodeClient()` 的选项中没有直接超时参数，但可以传入自定义 `fetch` 实现：

```typescript:src/appendix-b/opencode/agent-sdk.md
const client = createOpencodeClient({
  baseUrl: 'http://localhost:4096',
  throwOnError: true,
  fetch: (url, init) => {
    // 为每个请求添加 60 秒超时
    const controller = new AbortController()
    const timeout = setTimeout(() => controller.abort(), 60_000)
    return fetch(url, { ...init, signal: controller.signal })
      .finally(() => clearTimeout(timeout))
  },
})
```

### 会话中止

当某个 prompt 不需要继续执行时（例如用户取消了操作），可以主动中止：

```typescript:src/appendix-b/opencode/agent-sdk.md
// 在另一个控制路径中
await client.session.abort({ path: { id: sessionId } })
```

`session.abort()` 会立即中断当前正在执行中的 prompt，释放 Server 资源。

### Fire-and-Forget 模式

当只需要向 Session 注入上下文而不期望 AI 回复时（比如提前告知 Agent 某些项目规则），使用 `noReply: true`：

```typescript:src/appendix-b/opencode/agent-sdk.md
// 注入系统上下文，不消耗响应 Token
await client.session.prompt({
  path: { id: session.id },
  body: {
    noReply: true,
    parts: [{ type: 'text', text: '注意：该项目遵循严格的 TypeScript 类型规范，所有函数必须显式标注返回值类型。' }],
  },
})

// 后续 prompt 会自动包含上述上下文
const { data: result } = await client.session.prompt({
  path: { id: session.id },
  body: {
    parts: [{ type: 'text', text: '审查以下代码...' }],
  },
})
```

> 💡 **设计决策**：`noReply: true` 的典型用途包括：提前注入项目规范、设置角色背景、多阶段进度推进（第一阶段查文件→第二阶段分析→第三阶段生成报告），每阶段之间用 `noReply` 传中间结果而不触发模型回复。这比把所有内容塞到一个 prompt 中更可控，也更省钱。

### 成本监控

Session 对象包含 `cost` 字段，可以在每次 prompt 后检查消耗：

```typescript:src/appendix-b/opencode/agent-sdk.md
async function promptWithBudget(
  client: any,
  sessionId: string,
  prompt: string,
  budget: number, // 本次调用的预算上限（USD）
) {
  const { data: before } = await client.session.get({ path: { id: sessionId } })

  const result = await client.session.prompt({
    path: { id: sessionId },
    body: { parts: [{ type: 'text', text: prompt }] },
  })

  const { data: after } = await client.session.get({ path: { id: sessionId } })
  const cost = (after.cost || 0) - (before.cost || 0)

  if (cost > budget) {
    console.warn(`Token 消耗 $${cost.toFixed(4)} 超过预算 $${budget}`)
  }

  return result
}
```

---

## 安全注意事项

将 SDK 集成到生产环境时，以下安全要点需要特别注意：

### API Key 管理

**永远不要**在代码中硬编码 API Key。OpenCode Server 启动时通过环境变量或 `opencode.json` 配置 Provider 认证信息，SDK Client 通过 REST API 通信时无需传递 API Key：

```bash
# 正确：通过环境变量注入
ANTHROPIC_API_KEY="sk-ant-..." opencode serve --port 4096

# Client 端只需连接 Server，不涉及 API Key
npx tsx my-agent.ts
```

### 最小权限原则

`createOpencode()` 或 `createOpencodeClient()` 的配置应遵循最小权限原则：

- 只暴露需要的端口（`127.0.0.1` 而非 `0.0.0.0`），避免 Server 暴露到局域网
- 通过 Server 端的工具配置限制 Agent 的能力范围，只分配必要的工具权限
- 在多租户场景中为每个租户创建独立的 Server 实例，避免租户间越权

### Session 隔离

不同任务使用独立 Session，避免上下文串扰导致信息泄露。敏感任务完成后及时调用 `session.delete()` 清理 Session 数据。

### 输入验证

通过 SDK 发送的 prompt 本质上是用户输入。如果 SDK 暴露给终端用户（如 Web 应用中的 AI 助手），需要在应用层对输入进行长度限制、注入检测和内容过滤，防止 **Prompt（提示词）** 注入攻击。

### 审计日志

通过 `client.event.subscribe()` 监听 Server 事件流，记录所有会话操作。生产环境建议将审计日志输出到独立存储（如 ELK、Splunk），保留至少 90 天以便安全追溯。

---

## 错误处理与重试

SDK 编程中最常见的一类 Bug 就是**没有妥善处理网络错误和部分失败**。以下是生产级错误处理模式。

### 基础重试：指数退避

Server 连接失败、网络抖动、临时过载时，重试是最直接的策略：

```typescript:src/appendix-b/opencode/agent-sdk.md
async function promptWithRetry(
  client: any,
  sessionId: string,
  prompt: string,
  maxRetries = 3,
) {
  for (let i = 0; i < maxRetries; i++) {
    try {
      return await client.session.prompt({
        path: { id: sessionId },
        body: { parts: [{ type: 'text', text: prompt }] },
      })
    } catch (err: any) {
      if (i === maxRetries - 1) throw err

      // 只对可重试错误进行重试
      if (!isRetryableError(err)) throw err

      const delay = Math.min(1000 * Math.pow(2, i), 10_000) // 指数退避 + 上限
      console.warn(
        `Attempt ${i + 1} failed: ${err.message}. Retrying in ${delay}ms...`,
      )
      await new Promise(r => setTimeout(r, delay))
    }
  }
}

function isRetryableError(err: any): boolean {
  const msg = err.message || ''
  // 网络错误、503、429 可重试；4xx 客户端错误不可重试
  return (
    msg.includes('fetch failed') ||
    msg.includes('ECONNREFUSED') ||
    msg.includes('ECONNRESET') ||
    msg.includes('503') ||
    msg.includes('429') ||
    msg.includes('timeout')
  )
}
```

> 💡 **设计决策**：为什么用指数退避而不是固定间隔？Server 过载时，大量客户端同时重试会加剧负载（惊群效应）。指数退避 + 随机抖动（jitter）能让重试请求自然分散。上限 10 秒确保用户体验不会因无限制等待而恶化。

### 会话超时与中止

长时间运行的 prompt 可能因为各种原因卡住（模型推理慢、工具调用循环、输出量超大）：

```typescript:src/appendix-b/opencode/agent-sdk.md
async function promptWithTimeout(
  client: any,
  sessionId: string,
  prompt: string,
  timeoutMs = 120_000,
): Promise<any> {
  const result = await Promise.race([
    client.session.prompt({
      path: { id: sessionId },
      body: { parts: [{ type: 'text', text: prompt }] },
    }),
    new Promise((_, reject) =>
      setTimeout(() => reject(new Error('Prompt timeout')), timeoutMs),
    ),
  ])

  return result
}
```

如果检测到超时，建议同时中止 Server 端的执行，避免资源浪费：

```typescript:src/appendix-b/opencode/agent-sdk.md
async function promptWithAbortOnTimeout(
  client: any,
  sessionId: string,
  prompt: string,
  timeoutMs = 120_000,
): Promise<any> {
  const timeout = setTimeout(async () => {
    await client.session.abort({ path: { id: sessionId } }).catch(() => {})
  }, timeoutMs)

  try {
    return await client.session.prompt({
      path: { id: sessionId },
      body: { parts: [{ type: 'text', text: prompt }] },
    })
  } finally {
    clearTimeout(timeout)
  }
}
```

### 结构化错误处理模式

在 SDK 应用中，推荐统一的错误处理结构：

```typescript:src/appendix-b/opencode/agent-sdk.md
interface PromptResult {
  success: boolean
  data?: any
  error?: {
    type: 'timeout' | 'network' | 'validation' | 'server' | 'unknown'
    message: string
    retryable: boolean
  }
}

async function safePrompt(
  client: any,
  sessionId: string,
  prompt: string,
): Promise<PromptResult> {
  try {
    const { data } = await client.session.prompt({
      path: { id: sessionId },
      body: { parts: [{ type: 'text', text: prompt }] },
    })
    return { success: true, data }
  } catch (err: any) {
    const msg = err.message || String(err)

    if (msg.includes('timeout')) {
      return { success: false, error: { type: 'timeout', message: msg, retryable: true } }
    }
    if (msg.includes('fetch') || msg.includes('ECONN')) {
      return { success: false, error: { type: 'network', message: msg, retryable: true } }
    }
    if (msg.includes('400') || msg.includes('422')) {
      return { success: false, error: { type: 'validation', message: msg, retryable: false } }
    }
    if (msg.includes('500') || msg.includes('503')) {
      return { success: false, error: { type: 'server', message: msg, retryable: true } }
    }

    return { success: false, error: { type: 'unknown', message: msg, retryable: false } }
  }
}
```

### 部分失败处理

长 prompt 的中间部分可能失败（例如模型在分析 100 个文件时，中途工具调用出错）。此时不会抛出异常，而是消息中可能包含 `structuredOutput` 的错误信息：

```typescript:src/appendix-b/opencode/agent-sdk.md
const { data: result } = await client.session.prompt({
  path: { id: sessionId },
  body: {
    parts: [{ type: 'text', text: '分析这个仓库的所有模块...' }],
    format: {
      type: 'json_schema',
      schema: {
        type: 'object',
        properties: {
          modules: { type: 'array', items: { type: 'object' } },
          failedAnalyses: { type: 'array', items: { type: 'string' } },
          partial: { type: 'boolean' },
        },
      },
    },
  },
})

if (result.data.info.structured_output?.partial) {
  console.warn('分析部分失败：', result.data.info.structured_output.failedAnalyses)
  // 可以针对失败项进行重试
}
```

---

## 与配置式 Agent 的对比详解

### 配置式 Agent 的工作方式（来自 `agent-architecture.md`）

```jsonc:src/appendix-b/opencode/agent-sdk.md
// oh-my-openagent.jsonc
{
  "categories": {
    "code-reviewer": {
      "model": "anthropic/claude-sonnet-4-6",
      "temperature": 0.2,
      "prompt_append": "你是一个代码审查专家..."
    }
  }
}
```

使用时在 TUI 中通过 `task()` 调用：

```typescript:src/appendix-b/opencode/agent-sdk.md
// 在 OMO 工作流内
task(category="code-reviewer", prompt="审查最新的 git diff")
```

### SDK 等效实现

```typescript:src/appendix-b/opencode/agent-sdk.md
import { createOpencodeClient } from '@opencode-ai/sdk'

const client = createOpencodeClient({ baseUrl: 'http://localhost:4096' })

// 创建临时会话
const { data: session } = await client.session.create({
  body: { title: 'Code Review Session' },
})

// 发送审查请求
const { data: review } = await client.session.prompt({
  path: { id: session.id },
  body: {
    parts: [{ type: 'text', text: '审查最近的 git diff。关注安全漏洞和性能问题。' }],
  },
})

console.log(review.message.content)
```

### 差异总结

1. **配置位置**：配置式在 JSON 中声明，SDK 在代码中实时构造
2. **Agent 路由**：配置式通过 `task(category=...)` 指定，SDK 通过在 prompt 中 @提及指定
3. **生命周期**：配置式由 OMO 管理 Agent 进程，SDK 需要自行创建/管理 Session
4. **输出处理**：配置式直接输出到 TUI，SDK 需要用代码处理返回消息
5. **上下文**：配置式共享 OMO 会话上下文，SDK 每个 Session 独立

---

## 完整实战：数据分析 Agent

以下是用 SDK 构建的一个数据分析 Agent——它连接到 OpenCode Server，对项目中的 CSV 数据文件进行分析，输出结构化的统计报告。

### 架构设计

```
你的应用 (Node.js)
  │
  ├─ createOpencodeClient()
  │     │
  │     ▼  HTTP REST (port 4096)
  │  OpenCode Server
  │     │
  │     ▼  (AI Agent 工作)
  │  1. Glob 查找 .csv 文件
  │  2. Read 读取文件内容
  │  3. Bash 运行统计命令 (wc, awk)
  │  4. 生成结构化分析报告
  │
  └─ 返回结果到你的应用
```

### 完整代码

```typescript:data-analysis-agent.ts
import { createOpencodeClient } from '@opencode-ai/sdk'

interface AnalysisReport {
  files: Array<{
    name: string
    rows: number
    columns: number
    columnNames: string[]
    missingValues: number
    numericColumns: string[]
  }>
  summary: {
    totalFiles: number
    totalRows: number
    averageColumns: number
    dataQuality: string
  }
}

async function analyzeData(
  projectDir: string,
  serverUrl = 'http://localhost:4096',
): Promise<AnalysisReport> {
  // 1. 连接 Server
  const client = createOpencodeClient({ baseUrl: serverUrl })

  // 2. 创建分析会话
  const { data: session } = await client.session.create({
    body: { title: 'Data Analysis Session' },
  })

  // 3. 发送分析提示词，要求结构化输出
  const { data: result } = await client.session.prompt({
    path: { id: session.id },
    body: {
      parts: [{
        type: 'text',
        text: `
          分析项目目录 "${projectDir}" 中的所有 CSV 数据文件。

          执行步骤：
          1. 使用 Glob 查找所有 *.csv 文件
          2. 对每个 CSV 文件，用 Bash 运行 wc -l 统计行数
          3. 用 head -1 获取列名，awk -F',' '{print NF}' 统计列数
          4. 检查缺失值数量
          5. 判断哪些列是数值型

          输出格式严格按以下 JSON Schema，不要包含任何额外文字：
        `,
      }],
      format: {
        type: 'json_schema',
        schema: {
          type: 'object',
          properties: {
            files: {
              type: 'array',
              items: {
                type: 'object',
                properties: {
                  name: { type: 'string' },
                  rows: { type: 'number' },
                  columns: { type: 'number' },
                  columnNames: { type: 'array', items: { type: 'string' } },
                  missingValues: { type: 'number' },
                  numericColumns: { type: 'array', items: { type: 'string' } },
                },
                required: ['name', 'rows', 'columns', 'columnNames'],
              },
            },
            summary: {
              type: 'object',
              properties: {
                totalFiles: { type: 'number' },
                totalRows: { type: 'number' },
                averageColumns: { type: 'number' },
                dataQuality: { type: 'string' },
              },
              required: ['totalFiles', 'totalRows', 'averageColumns'],
            },
          },
          required: ['files', 'summary'],
        },
      },
    },
  })

  // 4. 清理会话
  await client.session.delete({ path: { id: session.id } })

  // 5. 解析结构化输出
  const content = result.message.content
  const textBlock = content.find((c: any) => c.type === 'text')
  if (!textBlock) throw new Error('No text output')

  // structuredOutput 字段（如果 format 生效）
  if ((result as any).structuredOutput) {
    return (result as any).structuredOutput as AnalysisReport
  }

  // 回退：JSON 解析
  return JSON.parse(textBlock.text) as AnalysisReport
}

// 使用示例
async function main() {
  // 确保 OpenCode Server 已启动
  try {
    const report = await analyzeData('/path/to/data')
    console.log('=== 数据分析报告 ===')
    console.log(`总文件数: ${report.summary.totalFiles}`)
    console.log(`总行数: ${report.summary.totalRows}`)
    console.log('---')
    for (const file of report.files) {
      console.log(`${file.name}: ${file.rows} 行 x ${file.columns} 列`)
    }
  } catch (err) {
    console.error('分析失败:', err)
  }
}

main()
```

### 运行方式

```bash
# 先启动 OpenCode Server
opencode serve --port 4096 &

# 然后运行 Agent
npx tsx data-analysis-agent.ts
```

### 扩展方向

以上基础模式可以扩展为：

1. **批量 CI 报告**：在 CI 构建完成后自动分析质量数据，输出 Markdown 报告到 PR 评论
2. **定时巡检**：用 cron 调度 SDK 脚本，定期运行代码健康检查
3. **Web 应用集成**：在 Next.js API Route 中调用 SDK，提供 AI 驱动的数据分析接口
4. **多会话并行**：并行创建多个 Session，独立分析不同数据集

```typescript:src/appendix-b/opencode/agent-sdk.md
// 并行分析多个项目
const projects = ['/data/project-a', '/data/project-b', '/data/project-c']
const results = await Promise.all(
  projects.map(dir => analyzeData(dir))
)
```

---

## 部署模式

### CI/CD 集成（GitHub Actions）

将 SDK Agent 嵌入 CI 流水线时，Server 需要在 CI Runner 中启动：

```yaml
# .github/workflows/code-analysis.yml
name: Code Analysis
on:
  pull_request:
    paths: ['src/**/*.ts']
jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20' }
      - run: npm install @opencode-ai/sdk
      # 启动 OpenCode Server（后台运行）
      - run: opencode serve --port 4096 &
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
      - run: npx tsx analysis-agent.ts
```

### Docker 容器化部署

OpenCode Server + SDK Agent 可容器化部署，适合微服务和后台任务场景：

```dockerfile
FROM node:20-slim
RUN npm install -g @opencode-ai/cli @opencode-ai/sdk
WORKDIR /app
COPY . .
EXPOSE 4096
# 启动 Server 后执行 Agent 脚本
CMD opencode serve --port 4096 & npx tsx agent.ts
```

环境配置通过 Docker Compose 管理：

```yaml
services:
  opencode-agent:
    build: .
    ports: ["4096:4096"]
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENCODE_HOST=0.0.0.0
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:4096/global/health"]
      interval: 30s
      retries: 3
```

关键部署注意事项：
- **健康检查**：通过 `global.health()` 端点实现容器健康检查，确保 Server 就绪后才接收请求
- **环境配置**：使用环境变量而非配置文件管理 Provider 认证和运行参数
- **资源限制**：在容器编排中设置 CPU/内存上限，避免 Agent 任务消耗过多资源

---

## 最佳实践

### 1. Session 复用

每次创建新 Session 会丢失上下文。如果需要多轮对话，复用同一个 Session：

```typescript:src/appendix-b/opencode/agent-sdk.md
const { data: session } = await client.session.create({ body: { title: 'Long Session' } })

// 第一轮
await client.session.prompt({ path: { id: session.id }, body: { parts: [{ type: 'text', text: '读取数据文件' }] } })

// 第二轮（有前一轮上下文）
await client.session.prompt({ path: { id: session.id }, body: { parts: [{ type: 'text', text: '基于刚才的数据生成图表建议' }] } })
```

> 💡 **设计决策**：复用 Session 时要注意上下文膨胀问题。长对话建议在关键节点（如"已完成模块 A 分析，准备开始模块 B"）之间插入 `session.summarize()`，或在每个逻辑阶段完成后创建新的 Session。详见"上下文管理"一节。

### 2. Token 预算控制

长时间运行的 prompt 可能消耗大量 Token。结合"上下文管理"和"运行时防护"中的策略：

- 给 prompt 加上明确的范围限制（"只分析前 100 行"）
- 配置 `maxTokens` 限制每次响应的长度（见"运行时防护"）
- 用 `format` 约束输出为结构化 JSON，避免 AI 额外发挥
- 定期检查 Session 的 Token 计数（`session.promptTokens`），达到阈值时切换 Session
- 使用 `noReply: true` 注入上下文时不计入输出 Token

### 3. 安全考量

- SDK Client 默认连接 `localhost:4096`——不要暴露到公网
- API Key 在 Server 端管理，Client 端不需要传递
- 在多租户场景中使用 E2B Sandbox 隔离
- 设置 `createOpencodeClient` 的 `throwOnError: true`，避免静默吞掉错误响应

### 4. 类型安全

SDK 的所有 API 都有完整的 TypeScript 类型定义，建议充分利用：

```typescript:src/appendix-b/opencode/agent-sdk.md
import type { Session, Message, Part, Config } from '@opencode-ai/sdk'

const session: Session = await client.session.get({
  path: { id: 'session-id' },
})
```

> 💡 **设计决策**：TypeScript 类型定义是从 Server 的 OpenAPI 规范自动生成的（`packages/sdk/js/src/gen/types.gen.ts`）。这意味着 Server 版本更新后，类型定义会自动同步，避免了 SDK 版本与 Server 版本不匹配的问题。建议在 CI 中验证 SDK 版本与 Server 版本的兼容性。

---

## 相关章节

- → [OpenCode SDK 与程序化集成](./sdk.md) — 三层次 SDK 总览（Plugin SDK / CLI 管道 / 天气 Agent 案例）
- → [oh-my-openagent **Agent（智能体）** 设计与开发指南](./agent-architecture.md) — 配置式自定义 Agent（Category + `task()`）
- → [OpenCode Plugin 系统参考](./plugins.md) — Plugin 方式的扩展机制
- → [OpenCode 内置能力](./capabilities.md) — 整体能力索引
- → [OpenCode 生态参考](./ecosystem.md) — 社区生态与 SDK 相关项目
- → [**MCP（模型上下文协议）** 服务器](../../06-advanced/mcp-servers.md) — MCP 协议集成

---

## 读者视角

### 适用读者角色
- 入门开发者 — 适合快速上手 OpenCode 的基础能力，了解核心概念和常用命令
- 智能体开发工程师 — 需要设计、调试、进化 AI 编码智能体，建立系统化的 Agent 工程体系
- 效率开发者 — 已用 AI 工具，想掌握 Agent 编排和工作流模式，提升日常开发效率 2x+
- 技术负责人 — 团队技术决策者，关注标准化，建立团队级 **Harness Engineering（驾驭工程）** 体系
- Skill 作者 — 有 AI 使用经验，想开发高质量、可复用的 Skill
- 工程经理 — 评估团队工具选型，判断 OpenCode 的投资回报率
- 需求分析师/产品经理 — 验证需求覆盖完整性，评估内容价值主张
- 系统架构师/技术顾问 — 评估 OpenCode 的技术可行性、架构集成与安全合规
- 后端开发者/API 工程师 — 将 AI Agent 嵌入后端开发工作流，掌握 MCP 服务端集成
- 前端开发者/UI 工程师 — 将 Agent 编排应用到前端场景，类比理解 Skill 系统
- 文档 UX 专家 — 确保文档可读性、Mermaid 规范、移动端/无障碍体验
- 技术审校/QA 编辑 — 建立质量门禁，验证代码示例可运行性、术语一致性
- 安全工程师/架构师 — 建立 OpenCode 安全基线，评估企业级合规
- 安全研究人员/红队成员 — 评估 AI Agent 攻击面，利用 Agent 自动化安全测试

### 典型使用场景
- 快速上手 OpenCode，完成第一个成功的尝试
- 设计和调试 AI 智能体，建立系统化的 Agent 工程体系
- 掌握 Agent 编排和工作流模式，提升日常开发效率
- 建立团队级 Harness Engineering 体系，进行技术决策
- 开发高质量、可复用的 Skill，封装领域知识
- 评估 OpenCode 的投资回报率，进行工具选型决策
- 验证需求覆盖完整性，评估内容价值主张
- 评估 OpenCode 的技术可行性，进行架构集成与安全合规
- 将 AI Agent 嵌入后端开发工作流，实现 MCP 服务端集成
- 将 Agent 编排应用到前端场景，类比理解 Skill 系统
- 确保文档可读性、Mermaid 规范、移动端/无障碍体验
- 建立质量门禁，验证代码示例可运行性、术语一致性
- 建立 OpenCode 安全基线，评估企业级合规
- 评估 AI Agent 攻击面，利用 Agent 自动化安全测试

### 使用示例
```bash
# 快速上手 OpenCode
opencode serve

# 创建项目知识库
opencode /init

# 使用自定义 Skill
opencode "分析代码质量"

# 执行自动化安全审计
opencode /ralph-loop

# 并行执行多个任务
opencode /hyperplan
```

### 工程化示例

**配置顺序检查表：**

1. **第1步：初始化项目**
   ```bash
   opencode /init
   ```

2. **第2步：配置 Provider**
   ```json
   {
     "providers": {
       "anthropic": {
         "apiKey": "sk-ant-...",
         "defaultModel": "claude-3-5-sonnet-20241022"
       }
     }
   }
   ```

3. **第3步：加载 Skill**
   ```bash
   opencode skills add myorg/my-skill
   ```

### 与前/后文章的衔接
- ← [OpenCode 内置能力](./capabilities.md) — 了解 OpenCode 的核心功能和能力
- → [OpenCode 内置命令参考](./commands.md) — 详细了解每个命令的用法和参数
