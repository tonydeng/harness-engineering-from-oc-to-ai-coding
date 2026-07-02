# Pi SDK：编程式 **Agent（智能体）** 开发

> 通过 `@earendil-works/pi-coding-agent` 将 Pi 的 Agent 引擎直接嵌入你的 Node.js 应用——无需子进程、无需 REST API，在同进程中调用 Agent 的全部能力。

Pi SDK 和其他工具 SDK 的核心差异在于**架构模式**：OpenCode SDK 通过 REST API 控制远程 Server（进程间通信），Claude Agent SDK 通过 spawn 子进程（进程间通信），而 Pi SDK 是**同进程 TypeScript 库嵌入**——`createAgentSession()` 在当前进程中直接创建 Agent 运行时。

---

## SDK 架构模式对比

Pi SDK 的核心差异在于**同进程嵌入**——`createAgentSession()` 在当前进程中直接创建 Agent 运行时，无需子进程或 REST 调用。完整对比见 → [与 OpenCode SDK / Claude Agent SDK 的差异详解](#与-opencode-sdk--claude-agent-sdk-的差异详解)。

---

## 安装与快速入门

### 安装

```bash:README.md
npm install @earendil-works/pi-coding-agent
```

> **包结构说明**：Pi 有两个 npm 包——`@earendil-works/pi-agent-core`（核心运行时，提供 Agent 类和扩展系统）和 `@earendil-works/pi-coding-agent`（CLI + SDK，依赖 `pi-agent-core`）。`createAgentSession()` 等 SDK API 由 `pi-coding-agent` 导出，开发者只需安装这一个包。参考源码：[pi-agent-core README](https://github.com/earendil-works/pi/blob/v0.79.8/packages/agent/README.md)、[pi-coding-agent SDK 文档](https://github.com/earendil-works/pi/blob/v0.79.0/packages/coding-agent/docs/sdk.md)。

### 最小示例

```typescript:src/appendix-d/pi/agent-sdk.md
import {
  AuthStorage,
  createAgentSession,
  ModelRegistry,
  SessionManager,
} from "@earendil-works/pi-coding-agent";

async function main() {
  const authStorage = AuthStorage.create();
  const modelRegistry = ModelRegistry.create(authStorage);

  const { session } = await createAgentSession({
    sessionManager: SessionManager.inMemory(),
    authStorage,
    modelRegistry,
  });

  const result = await session.prompt("列出当前目录的文件");
  console.log(result.content);

  await session.close();
}

main().catch(console.error);
```

与 SDK 参考（`sdk.md`）中的示例代码一致，这是嵌入 Pi Agent 的标准入口模式。

### 流式响应

```typescript:src/appendix-d/pi/agent-sdk.md
const { session } = await createAgentSession({ /* ... */ });

// 监听事件流
session.on("message", (msg) => {
  if (msg.role === "assistant") {
    process.stdout.write(msg.content);
  }
});

const result = await session.prompt("生成一篇关于 TypeScript 的文章");
```

---

## 核心 API 进阶

### `createAgentSession()` 完整配置

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `sessionManager` | `SessionManager` | 必需 | `inMemory()` 或 `fileSystem(cwd)` |
| `authStorage` | `AuthStorage` | 必需 | API Key 和凭证管理 |
| `modelRegistry` | `ModelRegistry` | 必需 | Provider 和模型注册 |
| `model` | `string` | （自动选择） | 指定初始模型 ID |
| `systemPrompt` | `string` | — | 初始系统提示词 |
| `resourceLoader` | `DefaultResourceLoader` | 默认 | 自定义 Extension/Skill 发现 |
| `maxTurns` | `number` | 无限制（生产建议 25-50） | 最大对话轮次 |

> ⚠️ **成本控制**：Pi SDK 默认不限制 `maxTurns`，生产环境建议设置 25-50 的上限。无限轮次可能导致 LLM API 费用失控。结合 [Token 预算控制](#3-token-预算控制) 和 [超时控制](#超时控制) 形成三层防护。

### `AuthStorage` — 认证管理

```typescript:src/appendix-d/pi/agent-sdk.md
const auth = AuthStorage.create();

// 设置 API Key
auth.set("anthropic", process.env.ANTHROPIC_API_KEY);
auth.set("openai", process.env.OPENAI_API_KEY);

// 支持加密持久化（可选）
const auth = AuthStorage.create({ encryptKeys: true });
```

### `ModelRegistry` — 模型管理

```typescript:src/appendix-d/pi/agent-sdk.md
const registry = ModelRegistry.create(auth);

// 注册 Provider
registry.addProvider("anthropic", {
  baseUrl: "https://api.anthropic.com",
  models: ["claude-sonnet-4-6", "claude-opus-4-7"],
});

// 查询可用的工具调用模型
const toolModels = registry.getModelsSupportingToolCalls();

// 查询所有模型
const allModels = registry.getAllModels();
```

### `SessionManager` — 会话持久化

```typescript:src/appendix-d/pi/agent-sdk.md
// 内存模式——进程结束后丢失，适合短任务
const memManager = SessionManager.inMemory();

// 文件系统模式——持久化到磁盘，支持 Session Tree
const fsManager = SessionManager.fileSystem(process.cwd());

// 自定义实现——可接入数据库
class DbSessionManager implements SessionManager {
  async createSession(title?: string): Promise<string> { /* ... */ }
  async loadSession(id: string): Promise<SessionState> { /* ... */ }
  async saveSession(state: SessionState): Promise<void> { /* ... */ }
  // ...
}
```

---

## 事件系统详解

Pi SDK 提供 25+ 生命周期事件（源码：[extensions/index.ts](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/src/core/extensions/index.ts)），覆盖 Agent 运行全流程，按类别分组：

| 类别 | 事件 | 触发时机 | 用途 |
|------|------|---------|------|
| **Session** | `session_start` | Session 启动 | 初始化资源 |
| | `session_shutdown` | Session 关闭 | 清理资源 |
| | `session_compact` | 上下文压缩时 | 监控压缩策略效果 |
| | `session_before_compact` | 压缩执行前 | 自定义压缩逻辑 |
| | `session_before_fork` | Fork Session 前 | Frok 前钩子 |
| | `session_before_switch` | 切换 Session 前 | 切换前保存状态 |
| | `session_before_tree` | 查看 Session Tree 前 | 自定义树展示 |
| **Agent** | `agent_start` | Agent 循环开始 | 注入系统提示、初始化 |
| | `agent_end` | Agent 循环结束 | 资源清理、结果汇总 |
| **Turn** | `turn_start` | 每轮 LLM 交互开始 | 性能监控、计时 |
| | `turn_end` | 每轮 LLM 交互结束 | 统计 Token 消耗、成本核算 |
| **Message** | `message_start` | 消息开始生成 | 流式 UI 开始 |
| | `message_update` | 消息增量更新 | 流式 UI 增量渲染 |
| | `message_end` | 消息生成完成 | 流式 UI 结束 |
| **Tool** | `tool_call` | LLM 请求工具调用前 | 审计、拦截、修改参数 |
| | `tool_result` | 工具返回结果后 | 审计、修改结果 |
| | `tool_execution_start` | 工具开始执行 | 计时、监控 |
| | `tool_execution_update` | 工具执行中（流式） | 实时进度展示 |
| | `tool_execution_end` | 工具执行结束 | 记录执行耗时 |
| **Provider** | `before_provider_request` | 请求 Provider 前 | 请求日志、修改请求 |
| | `after_provider_response` | Provider 响应后 | 响应日志、缓存 |
| **其他** | `resources_discover` | 发现资源时 | 资源加载监控 |
| | `input` | 用户输入 | 输入审计 |
| | `model_select` | 模型选择时 | 模型路由审计 |
| | `user_bash` | 用户执行 bash | Bash 交互审计 |
| | `project_trust` | 项目信任检查 | 安全检查日志 |

```typescript:src/appendix-d/pi/agent-sdk.md
interface MessageEvent {
  role: "user" | "assistant" | "system";
  content: string;
}

interface ToolCallEvent {
  toolName: string;
  args: Record<string, unknown>;
}

interface TurnEndEvent {
  tokensUsed?: number;
  totalCost?: number;
}

const { session } = await createAgentSession({ /* ... */ });

// 实时流式输出
session.on("message", (msg: MessageEvent) => {
  if (msg.role === "assistant") process.stdout.write(msg.content);
});

// 工具调用监控
session.on("tool_call", (event: ToolCallEvent) => {
  console.log(`[Tool] ${event.toolName}`, event.args);
});

// Token 消耗追踪
let totalTokens = 0;
session.on("turn_end", (event: TurnEndEvent) => {
  totalTokens += event.tokensUsed || 0;
  console.log(`本轮消耗: ${event.tokensUsed}, 累计: ${totalTokens}`);
});

// 异常处理
session.on("error", (err: Error) => {
  console.error("Agent 异常:", err.message);
  // 在这里实现清理或重试逻辑
});
```

---

## 运行时防护

### 轮次限制（maxTurns）

```typescript:src/appendix-d/pi/agent-sdk.md
const { session } = await createAgentSession({
  sessionManager: SessionManager.inMemory(),
  authStorage: AuthStorage.create(),
  modelRegistry: ModelRegistry.create(AuthStorage.create()),
  maxTurns: 30, // 最多 30 轮交互
});

// maxTurns 耗尽后 prompt() 返回当前累积结果而非失败
const result = await session.prompt("分析这个大型代码库...");
if (result.truncated) {
  console.warn(`达到最大轮次限制，结果可能不完整`);
}
```

### 超时控制

```typescript:src/appendix-d/pi/agent-sdk.md
// 通过 AbortController 实现超时
async function promptWithTimeout(
  session: { prompt: (msg: string, opts?: { signal?: AbortSignal }) => Promise<{ content: string }> },
  prompt: string,
  timeoutMs = 120_000
) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);

  try {
    return await session.prompt(prompt, { signal: controller.signal });
  } catch (err: unknown) {
    if (err instanceof DOMException && err.name === "AbortError") {
      throw new Error(`Prompt 超时 (${timeoutMs}ms)`);
    }
    throw err;
  } finally {
    clearTimeout(timeout);
  }
}
```

### 成本追踪

```typescript:src/appendix-d/pi/agent-sdk.md
session.on("turn_end", (event) => {
  // 每轮结束后检查累计成本
  const cost = event.totalCost || 0;
  if (cost > 0.50) {
    console.warn(`成本警告: 当前累计 $${cost.toFixed(4)}`);
    // 可在此决定是否中断
  }
});
```

### 可观测性与审计日志

Pi SDK 通过 `sessionManager` 和事件系统提供可观测性基础。建议生产环境集成结构化日志：

```typescript:src/appendix-d/pi/agent-sdk.md
interface AgentSession {
  prompt: (msg: string) => Promise<{ content: string; truncated?: boolean }>;
  close: () => Promise<void>;
  on: (event: string, handler: (...args: unknown[]) => void) => void;
}

// 基于事件的审计日志
function enableAuditLogging(session: AgentSession) {
  // 记录所有工具调用
  session.on("tool_call", (event) => {
    console.log(JSON.stringify({
      timestamp: new Date().toISOString(),
      type: "tool_call",
      tool: (event as ToolCallEvent).toolName,
      args: (event as ToolCallEvent).args,
    }));
  });

  // 记录每次 Provider 请求
  session.on("before_provider_request", (event) => {
    console.log(JSON.stringify({
      timestamp: new Date().toISOString(),
      type: "provider_request",
      // event 包含模型、Token 预估等信息
    }));
  });

  // 记录错误
  session.on("error", (err: Error) => {
    console.error(JSON.stringify({
      timestamp: new Date().toISOString(),
      type: "error",
      message: err.message,
      stack: err.stack,
    }));
  });
}
```

**OpenTelemetry 集成推荐**：将 `session.on()` 事件桥接到 OpenTelemetry Span 和 Metric，实现链路追踪和 Token 消耗的集中监控。Pi 的事件模型天然适配 OpenTelemetry 的 Span 生命周期（turn_start → turn_end 作为 Span 边界）。

---

## 错误处理与重试

Pi SDK 是**同进程嵌入**，错误模式不同于 OpenCode SDK（网络错误）和 Claude Agent SDK（子进程崩溃）。主要错误类型：

| 错误类型 | 产生原因 | 处理策略 |
|---------|---------|---------|
| **API 错误** | Provider API 不可用、认证失败 | 切换 Provider 或重试 |
| **模型错误** | 模型不支持工具调用、上下文超限 | 降级到其他模型 |
| **工具错误** | Extension 内未捕获异常 | 工具内 try-catch |
| **超时错误** | 模型响应过慢 | 增加超时或切换更快模型 |
| **OOM 错误** | 上下文过大 | 降低上下文或拆分任务 |

```typescript:src/appendix-d/pi/agent-sdk.md
interface PromptResult {
  content: string;
  truncated?: boolean;
}

async function robustPrompt(
  session: { prompt: (msg: string) => Promise<PromptResult> },
  prompt: string,
  maxRetries = 2
): Promise<PromptResult> {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await session.prompt(prompt);
    } catch (err: unknown) {
      if (attempt === maxRetries) throw err;

      // 区分可重试和不可重试错误
      // 推荐使用 err.code 或 err.status（Provider 独立），
      // 回退到 err.message 字符串匹配（Provider 相关，更脆弱）
      const errRecord = err as Record<string, unknown>;
      const errMsg = typeof errRecord.message === "string" ? errRecord.message : "";
      const isRetryable =
        errRecord.code === "RATE_LIMIT" ||
        errRecord.status === 429 ||
        errMsg.includes("rate limit") ||
        errMsg.includes("timeout");
      if (isRetryable) {
        const delay = Math.min(1000 * Math.pow(2, attempt), 10_000);
        console.warn(`Attempt ${attempt + 1} failed, retrying in ${delay}ms`);
        await new Promise((r) => setTimeout(r, delay));
      } else {
        // 不可重试错误（如认证失败）直接抛出
        throw err;
      }
    }
  }
}
```

### Extension 内的错误处理

```typescript:src/appendix-d/pi/agent-sdk.md
interface ToolArgs {
  url: string;
  method?: string;
}

interface ToolBlock {
  type: "text";
  text: string;
}

interface ToolResult {
  content: ToolBlock[];
  details: { isError?: boolean };
}

pi.registerTool({
  name: "api_call",
  description: "调用外部 API",
  execute: async (args: ToolArgs): Promise<ToolResult> => {
    try {
      const response = await fetch(args.url);
      if (!response.ok) {
        return { content: [{ type: "text", text: `API 返回错误: ${response.status}` }], details: { isError: true } };
      }
      const data = await response.json();
      return { content: [{ type: "text", text: JSON.stringify(data) }], details: {} };
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : String(err);
      return { content: [{ type: "text", text: `调用失败: ${message}` }], details: { isError: true } };
    }
  },
});
```

工具返回 `details.isError: true` 时，Agent 可以感知错误并尝试其他策略（如换一个 API 端点）。

---

## 并行模式

Pi SDK 同进程嵌入的特性使其并行性能优于 OpenCode SDK（REST 调用延迟）和 Claude Agent SDK（子进程开销）。

### 基础并行：多个 Session

```typescript:src/appendix-d/pi/agent-sdk.md
async function parallelAnalysis(files: string[]) {
  const base = {
    authStorage: AuthStorage.create(),
    modelRegistry: ModelRegistry.create(AuthStorage.create()),
  };

  // 创建多个 Session 并行执行
  const sessions = await Promise.all(
    files.map((file) =>
      createAgentSession({
        ...base,
        sessionManager: SessionManager.inMemory(),
        systemPrompt: `你是代码分析专家。分析 ${file}。`,
      }).then((r) => r.session)
    )
  );

  // 并发发送 prompt
  const results = await Promise.all(
    sessions.map((session) => session.prompt("分析这个文件的安全风险"))
  );

  // 清理所有 Session
  await Promise.all(sessions.map((s) => s.close()));
  return results;
}
```

### 带并发上限

```typescript:src/appendix-d/pi/agent-sdk.md
async function parallelWithLimit<T>(
  items: string[],
  taskFn: (item: string) => Promise<T>,
  limit = 3
): Promise<T[]> {
  const results: T[] = [];
  for (let i = 0; i < items.length; i += limit) {
    const batch = items.slice(i, i + limit);
    const batchResults = await Promise.all(batch.map(taskFn));
    results.push(...batchResults);
  }
  return results;
}

// 使用
const analyses = await parallelWithLimit(
  files,
  (file) => analyzeFile(file),
  3 // 同时最多 3 个分析任务
);
```

---

## RPC 服务器模式

适用于需要从非 Node.js 语言调用 Pi 的场景。SDK 可以用于构建定制的 RPC 服务器。

> **架构说明**：RPC 服务器是应用层的设计模式，并非 Pi SDK 内置功能。Pi 的 SDK 是同进程嵌入，RPC 模式通过 JSONL（JSON Lines）在进程间通信实现跨语言调用。关键在于每个请求应创建独立 Session，避免多客户端状态泄漏。

```typescript:src/appendix-d/pi/agent-sdk.md
import * as readline from "node:readline/promises";
import {
  AuthStorage,
  createAgentSession,
  ModelRegistry,
  SessionManager,
} from "@earendil-works/pi-coding-agent";

// 复用重量级对象（Provider 连接等）
const authStorage = AuthStorage.create();
const modelRegistry = ModelRegistry.create(authStorage);

async function startRpcServer() {
  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
  });

  console.log("RPC Server 就绪，等待 JSONL 输入...");

  for await (const line of rl) {
    try {
      const request = JSON.parse(line);
      if (request.type === "prompt") {
        // ✅ 每个请求创建独立 Session，避免状态泄漏
        const { session } = await createAgentSession({
          sessionManager: SessionManager.inMemory(),
          authStorage,
          modelRegistry,
          maxTurns: 25,
        });
        try {
          const result = await session.prompt(request.prompt);
          console.log(JSON.stringify({ type: "result", content: result.content }));
        } finally {
          await session.close(); // 确保释放资源
        }
      } else if (request.type === "close") {
        break;
      }
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : String(err);
      console.log(JSON.stringify({ type: "error", message }));
    }
  }
}
```

> ⚠️ **注意**：不要将 Session 共享给多个客户端——Agent Session 维护对话历史，共享会导致用户 A 的上下文泄漏到用户 B 的请求中。每条请求创建独立 Session 是最安全的模式。

**客户端示例（Python）**：

```python:src/appendix-d/pi/agent-sdk.md
import subprocess
import json

class PiRpcClient:
    """Pi RPC 客户端，使用 JSONL 协议通信。

    连接生命周期内复用子进程，但每个 prompt() 调用对应 RPC
    服务器端的独立 Agent Session。
    """

    def __init__(self, cmd: list[str]):
        self.proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True,
        )

    def query(self, prompt_text: str) -> dict:
        """发送 prompt，读取完整 JSON 响应。

        使用 json.loads() 逐行解析，每行都是一个完整的 JSON 对象
        （JSONL 协议）。对于含换行符的响应内容，JSON.stringify
        会将其转义为 \\n，确保 JSON 本身保持单行。
        """
        req = json.dumps({"type": "prompt", "prompt": prompt_text})
        self.proc.stdin.write(req + "\n")
        self.proc.stdin.flush()
        line = self.proc.stdout.readline()
        if not line:
            raise ConnectionError("RPC 服务器连接断开")
        return json.loads(line)

    def close(self):
        self.proc.stdin.write(json.dumps({"type": "close"}) + "\n")
        self.proc.stdin.flush()
        self.proc.wait()

# 使用
client = PiRpcClient(["npx", "tsx", "rpc-server.ts"])
result = client.query("列出当前目录的文件")
print(result["content"])
client.close()
```

---

## 容器化部署

### Docker 部署 SDK Agent

```dockerfile:Dockerfile.pi-sdk
FROM node:22-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    git ripgrep ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# 创建非 root 用户
RUN groupadd -r piagent && useradd -r -g piagent -m -d /home/piagent piagent

WORKDIR /app
COPY package.json .
RUN npm install && chown -R piagent:piagent /app
COPY . .

# 切换到非 root 用户
USER piagent

# Healthcheck — 验证进程存活
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD node -e "process.exit(0)" || exit 1

CMD ["node", "my-agent.js"]
```

```yaml:docker-compose.yml
services:
  pi-agent:
    build: .
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./workspace:/app/workspace
    mem_limit: 2g
    cpus: "2.0"
```

### Gondolin 沙箱 + SDK

对于需要隔离内置工具执行的场景，Gondolin Extension 可以和 SDK 组合使用：

```typescript:src/appendix-d/pi/agent-sdk.md
import {
  AuthStorage,
  createAgentSession,
  ModelRegistry,
  SessionManager,
  DefaultResourceLoader,
} from "@earendil-works/pi-coding-agent";

async function createSandboxedSession() {
  // 加载 Gondolin Extension（将内置工具路由到微 VM）
  const resourceLoader = new DefaultResourceLoader({
    extensions: ["~/.pi/agent/extensions/gondolin"],
  });

  const { session } = await createAgentSession({
    sessionManager: SessionManager.inMemory(),
    authStorage: AuthStorage.create(),
    modelRegistry: ModelRegistry.create(AuthStorage.create()),
    resourceLoader,
  });

  return session;
}
```

---

## CI/CD 集成

### GitHub Actions

```yaml:.github/workflows/pi-analysis.yml
name: Pi Code Analysis
on:
  pull_request:
    paths: ["src/**/*.ts"]

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: "22" }
      - run: npm install @earendil-works/pi-coding-agent
      - name: Run code analysis
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: npx tsx analysis-agent.ts
```

### 分析 Agent 脚本

```typescript:analysis-agent.ts
import {
  AuthStorage,
  createAgentSession,
  ModelRegistry,
  SessionManager,
} from "@earendil-works/pi-coding-agent";
import { writeFileSync } from "fs";

async function main() {
  const { session } = await createAgentSession({
    sessionManager: SessionManager.inMemory(),
    authStorage: AuthStorage.create(),
    modelRegistry: ModelRegistry.create(AuthStorage.create()),
    systemPrompt: `你是一个代码审查专家。审查当前 PR 的变更。
使用 git diff 获取变更内容，然后输出结构化审查报告。
输出格式：Markdown 表格 (问题 | 严重级别 | 位置 | 建议)`,
  });

  const result = await session.prompt("审查当前分支的代码变更");
  writeFileSync("analysis-report.md", result.content);
  await session.close();
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
```

---

## 部署模式

### 嵌入式（Embedded）

Pi SDK 作为应用的一个 npm 依赖嵌入，适合：

- **Express/Fastify 应用**：在每个 API 路由中创建 Agent Session 处理请求
- **CLI 工具**：在命令行工具中集成 AI Agent 能力
- **定时任务**：在 cron job 中周期性地执行 Agent 任务

```typescript:src/appendix-d/pi/agent-sdk.md
// Express 集成示例
import express from "express";
import { createAgentSession, AuthStorage, ModelRegistry, SessionManager } from "@earendil-works/pi-coding-agent";

const app = express();
const auth = AuthStorage.create();
const registry = ModelRegistry.create(auth);

app.post("/api/analyze", async (req, res) => {
  const { session } = await createAgentSession({
    sessionManager: SessionManager.inMemory(),
    authStorage: auth,
    modelRegistry: registry,
  });

  try {
    const result = await session.prompt(req.body.prompt);
    res.json({ result: result.content });
  } finally {
    await session.close();
  }
});
```

### Serverless

在 Serverless 环境中（AWS Lambda、Vercel Functions），每次调用创建新的 Session：

```typescript:src/appendix-d/pi/agent-sdk.md
// AWS Lambda Handler
interface LambdaEvent {
  prompt: string;
  sessionId?: string;
}

export async function handler(event: LambdaEvent) {
  const { session } = await createAgentSession({
    sessionManager: SessionManager.inMemory(),
    authStorage: AuthStorage.create(),
    modelRegistry: ModelRegistry.create(AuthStorage.create()),
  });

  try {
    const result = await session.prompt(event.prompt);
    return { statusCode: 200, body: JSON.stringify({ result: result.content }) };
  } finally {
    await session.close();
  }
}
```

**冷启动优化**——`createAgentSession()` 是同进程调用，没有子进程开销，但仍然需要初始化 Provider 连接（~500ms）。以下策略可减少冷启动影响：

```typescript:src/appendix-d/pi/agent-sdk.md
// 1. 全局复用 AuthStorage 和 ModelRegistry（模块级单例）
const sharedAuth = AuthStorage.create({ encryptKeys: true });
const sharedRegistry = ModelRegistry.create(sharedAuth);

// 2. Session 状态持久化（将状态保存到外部存储）
interface SessionPersistence {
  save(sessionId: string, state: SessionState): Promise<void>;
  load(sessionId: string): Promise<SessionState | null>;
}

// 以 Redis 为例
class RedisSessionStore implements SessionPersistence {
  async save(sessionId: string, state: SessionState): Promise<void> {
    await redis.set(`pi:session:${sessionId}`, JSON.stringify(state), {
      EX: 3600, // 1 小时过期
    });
  }

  async load(sessionId: string): Promise<SessionState | null> {
    const data = await redis.get(`pi:session:${sessionId}`);
    return data ? JSON.parse(data) : null;
  }
}

// 3. 热启动处理函数
export async function warmHandler(event: LambdaEvent) {
  const startTime = Date.now();

  // 尝试恢复已有 Session
  let session;
  if (event.sessionId) {
    const state = await sessionStore.load(event.sessionId);
    if (state) {
      // 从持久化状态恢复，避免完整初始化
      const sessionManager = SessionManager.inMemory();
      await sessionManager.importState(state);
      const result = await createAgentSession({
        sessionManager,
        authStorage: sharedAuth,
        modelRegistry: sharedRegistry,
      });
      session = result.session;
      console.log(`Session 恢复耗时: ${Date.now() - startTime}ms`);
    }
  }

  // 没有已有 Session，创建新 Session
  if (!session) {
    const result = await createAgentSession({
      sessionManager: SessionManager.inMemory(),
      authStorage: sharedAuth,
      modelRegistry: sharedRegistry,
      maxTurns: 25,
    });
    session = result.session;
    console.log(`新 Session 创建耗时: ${Date.now() - startTime}ms`);
  }

  try {
    const result = await session.prompt(event.prompt);
    // 持久化当前 Session 状态供下次使用
    if (session.sessionId) {
      await sessionStore.save(session.sessionId, await session.exportState());
    }
    return { statusCode: 200, body: JSON.stringify({ result: result.content }) };
  } finally {
    await session.close();
  }
}
```

> 对于 AWS Lambda，全局变量（`sharedAuth`、`sharedRegistry`）在函数实例存续期间保持热状态，后续调用跳过 Provider 初始化。配合 `sessionStore` 持久化可实现跨实例的 Session 状态共享。

---

## 与 OpenCode SDK / Claude Agent SDK 的差异详解

| 维度 | Pi SDK | OpenCode SDK | Claude Agent SDK |
|------|--------|--------------|------------------|
| **包名** | `@earendil-works/pi-coding-agent` | `@opencode-ai/sdk` | `@anthropic-ai/claude-agent-sdk` |
| **架构** | 同进程 TypeScript 库 | REST API 客户端 | 子进程（spawn CLI） |
| **入口** | `createAgentSession()` | `createOpencodeClient()` + `session.prompt()` | `query()` async 生成器 |
| **启动开销** | 零（已在进程） | 需 Server 运行 | 1-2s 子进程启动 |
| **自定义工具** | `registerTool()` 直接注册 | Plugin 系统 | `tool()` + `createSdkMcpServer()` |
| **事件模型** | `session.on()` 回调 | `event.subscribe()` | async `for await` |
| **并行** | 多 Session 同进程 | 多 Session 同 Server | 多子进程 |
| **跨语言** | RPC 模式（需自建） | REST（任何 HTTP 客户端） | Node.js/Python SDK |
| **Session 管理** | Tree 分支（独有） | 线性 Session | 线性 + sessionId |
| **适合场景** | Node.js 应用嵌入 | 远程调用、CI/CD | 子进程隔离、跨语言 |

---

## 最佳实践

### 1. 复用 AuthStorage 和 ModelRegistry

`AuthStorage` 和 `ModelRegistry` 是重量级对象（涉及 Provider 初始化），应在应用生命周期内复用：

```typescript:src/appendix-d/pi/agent-sdk.md
// ✅ 正确：复用
const auth = AuthStorage.create();
const registry = ModelRegistry.create(auth);

async function createAnalysisSession(systemPrompt: string) {
  const { session } = await createAgentSession({
    sessionManager: SessionManager.inMemory(),
    authStorage: auth,
    modelRegistry: registry,
    systemPrompt,
  });
  return session;
}

// ❌ 错误：每次创建新的
async function badPattern() {
  const { session } = await createAgentSession({
    authStorage: AuthStorage.create(),  // 每次都初始化
    modelRegistry: ModelRegistry.create(AuthStorage.create()),  // 重复创建
  });
}
```

### 2. Session 生命周期管理

```typescript:src/appendix-d/pi/agent-sdk.md
interface AgentSession {
  prompt: (msg: string) => Promise<{ content: string; truncated?: boolean }>;
  close: () => Promise<void>;
  on: (event: string, handler: (...args: unknown[]) => void) => void;
}

// 推荐：使用 try/finally 保证释放
async function withSession<T>(
  factory: (session: AgentSession) => Promise<T>,
  systemPrompt?: string
): Promise<T> {
  const { session } = await createAgentSession({
    sessionManager: SessionManager.inMemory(),
    authStorage: auth,
    modelRegistry: registry,
    systemPrompt,
  });

  try {
    return await factory(session);
  } finally {
    await session.close();
  }
}

// 使用
const result = await withSession(async (session) => {
  return session.prompt("分析代码");
});
```

### 3. Token 预算控制

```typescript:src/appendix-d/pi/agent-sdk.md
// 监控 Token 消耗，超限时切换 Session
let totalTokens = 0;
const TOKEN_LIMIT = 100_000;

session.on("turn_end", (event) => {
  totalTokens += event.tokensUsed || 0;
  if (totalTokens > TOKEN_LIMIT) {
    console.warn("Token 预算耗尽，建议创建新 Session");
  }
});
```

### 4. Extension 与 SDK 的协作

SDK 创建的 Session 同样可以加载 Extension：

```typescript:src/appendix-d/pi/agent-sdk.md
import { DefaultResourceLoader } from "@earendil-works/pi-coding-agent";

const resourceLoader = new DefaultResourceLoader({
  extensions: ["./my-extension.ts"],
  skills: ["./my-skill.md"],
});

const { session } = await createAgentSession({
  sessionManager: SessionManager.inMemory(),
  authStorage: auth,
  modelRegistry: registry,
  resourceLoader,
  systemPrompt: "你是一个安全审查专家。",
});

// Agent 会自动使用 Extension 中注册的工具
const result = await session.prompt("审查当前目录的代码");
```

### 5. 生产部署清单

将 Pi SDK Agent 部署到生产环境前，对照检查：

- [ ] `AuthStorage` 和 `ModelRegistry` 是否复用？（避免每次创建的开销）
- [ ] `maxTurns` 是否设置？（防止无限执行）
- [ ] 工具调用是否包含 try-catch？（防止未捕获异常导致 Session 崩溃）
- [ ] `session.close()` 是否在 finally 中保证执行？（防止资源泄漏）
- [ ] 超时控制是否实现？（`AbortController` 或 Promise.race）
- [ ] 是否有日志记录？（`session.on("tool_call")` 审计日志）
- [ ] 是否在非 Node.js 场景需要 RPC 模式？
- [ ] 环境变量中的 API Key 是否正确配置？
- [ ] Extension 来源是否可信任？

---

## 相关章节

- → [Pi **Agent（智能体）** SDK 与程序化集成](./sdk.md) — SDK 基础参考与 Weather Agent 案例
- → [Pi **Agent（智能体）** 架构设计与开发指南](./agent-architecture.md) — Extension API 和设计模式
- → [Pi **Agent（智能体）** 扩展体系详解](./customization.md) — Extensions 完整开发指南
- → [Pi **Agent（智能体）** 生态参考](./ecosystem.md) — 容器化、Provider 生态
- → [OpenCode SDK：编程式 **Agent（智能体）** 开发](../../appendix-b/opencode/agent-sdk.md) — REST API 方式对比参考
- → [Claude **Agent（智能体）** SDK：编程式 Agent 开发](../../appendix-c/claudecode/agent-sdk.md) — 子进程方式对比参考

---

## 适用场景与限制

### 只支持 Node.js/TypeScript 环境

Pi SDK 是一个 Node.js npm 包，只能在 Node.js 或 TypeScript 环境中使用。如果你的后端服务使用 Python（FastAPI/Django）、Go、Rust 或 Java，无法直接通过 SDK 嵌入 Pi Agent 能力。对于非 Node.js 环境，需要使用 RPC 模式（`pi --mode rpc`）通过 JSONL 协议进行跨语言调用，但这会增加进程间通信的延迟和复杂度。

如果你的团队技术栈以 Node.js 为主，Pi SDK 的同进程嵌入模式提供了最佳的性能和开发体验。如果团队使用多语言栈，建议评估 OpenCode 的 REST API SDK（`@opencode-ai/sdk`），它对任何 HTTP 客户端都可用。

### 并发 prompt 调用受限于单 Session 锁

`session.prompt()` 方法在执行期间会锁定 Session 的状态，包括消息历史、工具注册表和上下文窗口。对同一个 Session 并发发送两个 prompt 会导致第二个调用排队等待或覆盖第一个的上下文。这与 OpenCode SDK 的 REST API 不同，后者可以通过多 Session 并发处理请求。

需要并发处理多个用户请求时，为每个请求创建独立的 Session。可以在请求处理函数中 `createAgentSession()`，处理完毕后 `session.close()`。重量级对象（`AuthStorage`、`ModelRegistry`）复用以减少初始化开销，Session 隔离以避免上下文污染。

### Serverless 冷启动延迟不可避免

Pi SDK 的 `createAgentSession()` 虽然是同进程调用，但仍然需要初始化 `AuthStorage`、`ModelRegistry` 和 Provider 连接池，首次调用约需 500ms。在 AWS Lambda 等 Serverless 环境中，冷启动的总延迟可能达到 1-2 秒，这对于延迟敏感的 API 端点可能不可接受。

利用 Lambda 的热启动特性：在模块级创建 `AuthStorage` 和 `ModelRegistry` 的全局单例，多次调用间复用这些重量级对象。使用 Provisioned Concurrency 预热函数实例以消除冷启动延迟。Session 状态通过 Redis 或 DynamoDB 持久化，热启动时恢复而非重建。

---

## 常见反模式

### 在循环中创建独立的 AuthStorage 和 ModelRegistry

这是 Pi SDK 使用中最常见的性能反模式。许多开发者在处理批量任务时，为每个文件或每次查询都创建全新的 `AuthStorage.create()` 和 `ModelRegistry.create()` 实例。每个实例都需要初始化 Provider 连接池和认证状态，单次初始化耗时约 500ms。处理 100 个文件时，仅初始化开销就浪费 50 秒。

正确的做法是在应用的入口处创建一次 `AuthStorage` 和 `ModelRegistry`，然后在所有 Session 创建中复用这两个实例。只在 Session 级别创建新的 `SessionManager`（因为 Session 状态需要隔离）。这样批量任务的启动开销从 O(n) 降低到 O(1)。

### 忽略 session.close() 导致资源泄漏

`createAgentSession()` 创建的 Session 会占用内存和保持与 Provider 的连接。如果不调用 `session.close()`，Session 对象会在 JavaScript 垃圾回收时被回收，但异步资源（如 HTTP 连接池、事件监听器）可能不会被及时释放。在高并发场景中，累积的未关闭 Session 可能导致文件描述符耗尽或内存溢出。

始终使用 try/finally 模式确保 Session 被关闭。推荐封装一个 `withSession()` 高阶函数，在 finally 中保证清理。对于 Express/Fastify 等 Web 框架，确保在请求处理完毕后关闭 Session，即使处理过程中发生了异常。

### 不设 maxTurns 导致成本失控

Pi SDK 默认不限制 `maxTurns`，这意味着 Agent 可以无限轮次地调用 LLM 和工具。一个模糊的 prompt 可能让 Agent 进入循环推理：反复读取文件、分析、得出不满意的结论、再次读取……每轮消耗数百个 Token，在使用 Opus 模型时可能在一分钟内消耗数十美元。

生产环境必须设置 `maxTurns`。对于简单查询设 10-20，对于代码分析设 30-50，对于复杂的多步骤任务设 50-100。结合 `session.on("turn_end")` 事件监控累计 Token 消耗，设置成本告警阈值。

## 常见失败与陷阱

### RPC 模式下多客户端共享 Session 导致上下文泄漏

在 RPC 服务器实现中，如果多个客户端请求共享同一个 Agent Session，用户 A 的对话历史会泄漏到用户 B 的上下文中。这是因为 Session 维护了完整的对话消息列表，不同用户的 prompt 会被追加到同一个消息历史中。

每个 RPC 请求必须创建独立的 Session。可以在请求处理函数中为每次 `prompt` 调用创建新的 `createAgentSession()`，处理完毕后立即 `session.close()`。重量级对象（`AuthStorage`、`ModelRegistry`）可以复用，但 Session 必须隔离。

### Extension 内的未捕获异常导致 Agent 静默失败

Pi SDK 创建的 Session 中加载的 Extension，如果在工具执行时抛出未捕获的异常，Agent 会收到一个错误结果（`details.isError: true`），但不会中断整个 Session。LLM 可能根据错误结果做出不正确的推理，或者反复重试同一个失败的工具调用。

每个 Extension 的 `execute()` 函数都必须用 try-catch 包裹。返回结果时检查是否需要设置 `details.isError: true`，让 LLM 能感知错误并调整策略。在生产环境中，通过 `session.on("error")` 事件监听器捕获所有未预期的异常。

### Serverless 冷启动时 Session 状态丢失

在 AWS Lambda 等 Serverless 环境中，每次冷启动会重新初始化 Node.js 进程，之前创建的 Session 状态（对话历史、工具注册信息）会丢失。如果用户在上一次调用中建立的上下文没有持久化，新的调用会从空白状态开始，Agent 不记得之前的对话内容。

实现 Session 状态的外部持久化：在每次 `turn_end` 事件后将 Session 状态序列化到 Redis 或 DynamoDB，在下次调用时尝试恢复。Pi SDK 的 `session.exportState()` 和 `sessionManager.importState()` 方法提供了状态序列化能力。同时在全局模块级复用 `AuthStorage` 和 `ModelRegistry`，利用 Lambda 的热启动保持 Provider 连接池。
