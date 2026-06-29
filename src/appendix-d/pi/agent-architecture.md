# Pi **Agent（智能体）** 架构设计与开发指南

> 从"用 Pi 写代码"到"用 Pi 构建自己的 Agent"——读完本文，你应该能利用 Pi 的 Extension API、事件系统和运行模式，设计并实现自定义的 Agent 工作流。

Pi 不提供 OpenCode 式的 Category 编排层，也没有 Claude Code 的 Subagent 文件系统。它的 Agent 架构建立在 **Extension API + 事件流 + 运行模式（Mode）** 三支柱上——核心极简，所有扩展通过 TypeScript Extension 按需注入。

Pi 的 Agent 相关功能分布在四个 npm 包中，层级关系如下：

| 包名 | 版本 | 职责 | 大小 |
|------|------|------|------|
| `@earendil-works/pi-ai` | v0.80.2 | 统一 LLM Provider 接口（20+ Provider） | — |
| `@earendil-works/pi-agent-core` | v0.80.2 | Agent 运行时核心：Agent 类、Extension API、事件系统、Mode 调度（102 文件，MIT） | 核心 |
| `@earendil-works/pi-coding-agent` | v0.80.2 | CLI + SDK：完整的编码 Agent 体验，65K+ Stars | 应用层 |
| `@earendil-works/pi-tui` | v0.80.2 | TUI 渲染组件（交互模式的终端 UI） | 渲染层 |

依赖链：`pi-agent-core ← pi-coding-agent ← pi-tui`，`pi-ai` 作为独立的 Provider 抽象层被 `pi-agent-core` 和 `pi-coding-agent` 共同引用。

> 来源：[Pi GitHub 仓库](https://github.com/earendil-works/pi)、[pi-agent-core README](https://github.com/earendil-works/pi/blob/v0.79.8/packages/agent/README.md)、[pi-coding-agent SDK 文档](https://github.com/earendil-works/pi/blob/v0.79.0/packages/coding-agent/docs/sdk.md)

---

## 快速上手：创建一个自定义工具

在 Pi 中"创建 Agent"本质上是编写一个 Extension。以下三步即可完成。

### 第 1 步：创建 Extension 文件

```typescript:~/.pi/agent/extensions/my-helper.ts
import type { ExtensionAPI } from "@earendil-works/pi-agent-core";

export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "list_dir",
    description: "列出指定目录的文件和子目录",
    parameters: {
      type: "object",
      properties: {
        path: { type: "string", description: "目录路径，默认为当前目录" },
      },
    },
    execute: async ({ path = "." }) => {
      const fs = await import("fs/promises");
      const entries = await fs.readdir(path, { withFileTypes: true });
      return entries
        .map((e) => (e.isDirectory() ? `📁 ${e.name}/` : `📄 ${e.name}`))
        .join("\n");
    },
  });
}
```

### 第 2 步：加载 Extension

```bash
pi -e ~/.pi/agent/extensions/my-helper.ts
```

### 第 3 步：使用自定义工具

```text
用户: 列出当前目录的文件
Agent: 调用 list_dir 工具...
📄 README.md
📁 src/
📁 docs/
📄 package.json
```

> 与 OpenCode 的 `task(category="...")` 不同，Pi 不通过 Category 路由任务。工具注册后，Agent 根据 LLM 对工具描述的语义理解自动选择调用。

---

## Pi 的 Agent 设计模式

Pi 的 Extension API 支持 5 种模式，覆盖从简单工具到复杂编排的场景。

### 1. Tool Extension（工具扩展）

**适用场景**：为 Agent 增加一个新能力（查询 API、执行计算、访问数据库）。

```typescript:src/appendix-d/pi/agent-architecture.md
export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "search_docs",
    description: "在项目文档中搜索相关内容",
    parameters: { /* ... */ },
    execute: async ({ query }) => {
      // 调用外部搜索 API 或本地索引
      return searchResults;
    },
  });
}
```

工具注册后，Agent 通过 LLM 的 function calling 自动选择调用。Pi 使用 TypeBox schema 做参数校验，确保 LLM 生成的参数格式正确。

**关键设计决策**：工具名和描述的措辞直接影响 LLM 是否选择调用它。描述应该说明"什么时候用"而非"怎么用"——例如 `"当用户问天气时查询 OpenWeatherMap API"` 优于 `"调用 get_weather 函数"`。

### 2. Replace Built-in Tool（替换内置工具）

**适用场景**：需要改变 Pi 内置的 `read`/`write`/`edit`/`bash` 行为——例如在沙箱中执行。

这是 Pi 区别于其他工具的核心模式。内置工具名是保留的，Extension 注册同名工具会**覆盖**内置行为：

```typescript:src/appendix-d/pi/agent-architecture.md
export default function (pi: ExtensionAPI) {
  // 覆盖内置 bash 工具，在 Docker 容器中执行命令
  pi.registerTool({
    name: "bash",
    description: "在 Docker 容器中执行 Shell 命令",
    parameters: {
      type: "object",
      properties: {
        command: { type: "string", description: "要执行的命令" },
      },
      required: ["command"],
    },
    execute: async ({ command }) => {
      // ⚠️ 以下实现存在命令注入漏洞，详见下方安全说明
      const { execSync } = await import("child_process");
      return execSync(`docker exec my-sandbox sh -c ${JSON.stringify(command)}`, {
        encoding: "utf-8",
      });
    },
  });
}
```

> **安全警告**：上述 `JSON.stringify()` 实现存在**命令注入**漏洞。`JSON.stringify` 不会转义 Shell 元字符（`$`、`` ` ``、`;`、`|`），攻击者可通过 `$(echo pwned)` 或反引号注入任意命令。正确的做法是使用 `child_process.spawn()` 并禁用 Shell（`shell: false`）：
>
> ```typescript:src/appendix-d/pi/agent-architecture.md
> import { spawn } from "child_process";
>
> // 安全版本：spawn 以参数数组传递，无 Shell 注入风险
> const child = spawn("docker", ["exec", "my-sandbox", "sh", "-c", command], {
>   shell: false,
> });
> let output = "";
> for await (const chunk of child.stdout) output += chunk;
> return output;
> ```
>
> 来源：[Pi Extension 安全指南](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/security.md)、[permission-gate.ts 示例](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/permission-gate.ts)

**设计原则**：替换内置工具时，必须保持相同的工具名和参数签名，否则 LLM 可能因参数不匹配而调用失败。

### 3. Event-Driven Extension（事件驱动扩展）

**适用场景**：在 Agent 生命周期事件中注入自定义逻辑——审计日志、权限控制、上下文注入。

```typescript:src/appendix-d/pi/agent-architecture.md
export default function (pi: ExtensionAPI) {
  // 审计所有工具调用
  pi.on("tool_call", async (event) => {
    console.log(`[AUDIT] Tool: ${event.toolName}, Args:`, event.args);
  });

  // 在 Agent 启动前注入上下文
  pi.on("before_agent_start", async (_event, ctx) => {
    const projectRules = await loadProjectRules(ctx.cwd);
    ctx.appendSystemPrompt(projectRules);
  });

  // 阻断危险命令（使用实际 Pi Extension API）
  pi.on("tool_call", async (event) => {
    if (event.toolName === "bash" && event.args.command) {
      // 更精确的检查：比对命令向量而非原始字符串
      const cmd = event.args.command.trim();
      const dangerousPatterns = [/^rm\s+-rf\s+\/$/, /^dd\s+if=/, /^:\(\)\s*\{/];
      if (dangerousPatterns.some((p) => p.test(cmd))) {
        return { block: true, reason: "危险命令已拦截" };
      }
      // 白名单模式：只允许安全的命令前缀
      const allowedPrefixes = ["ls", "cat", "grep", "find", "git", "npm", "node"];
      if (!allowedPrefixes.some((p) => cmd.startsWith(p))) {
        return { block: true, reason: "命令不在白名单中，已拦截" };
      }
    }
  });

  // 或在 Agent 级别使用 beforeToolCall 钩子（更精细的控制）
  // pi.hook("beforeToolCall", async (toolName, args) => {
  //   if (toolName === "bash" && args.command.includes("rm -rf /")) {
  //     return { allow: false, reason: "禁止执行危险命令" };
  //   }
  //   return { allow: true };
  // });
}
```

事件处理器可以有三种返回值：
- **不 return**：放行，继续执行
- **`{ block: true, reason }`**：阻断操作
- **`{ result: modifiedData }`**：修改工具调用参数或结果

> **注意**：事件级别的 `{ block: true }` 模式和 Agent 级别的 `beforeToolCall` 钩子都能实现权限控制。前者适合全局策略（如审计），后者适合针对特定 Agent 的细粒度控制。参考 Pi 官方示例：[permission-gate.ts](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/permission-gate.ts)（命令执行前确认）、[protected-paths.ts](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/protected-paths.ts)（阻止写入敏感路径）。

### 4. Slash Command Extension（命令扩展）

**适用场景**：创建常用工作流的快捷命令。

```typescript:src/appendix-d/pi/agent-architecture.md
export default function (pi: ExtensionAPI) {
  pi.registerCommand({
    name: "review",
    description: "审查当前分支的代码变更",
    execute: async (args, ctx) => {
      const diff = await ctx.exec("git diff main...HEAD");
      // 将审查结果发送到编辑器中
      ctx.sendMessage(`正在审查代码变更...\n\`\`\`\n${diff.slice(0, 2000)}\n\`\`\``);
    },
  });
}
```

### 5. Multi-Session Orchestration（多Session编排）

**适用场景**：多个 Pi 实例并行工作——Pi 不自带 OpenCode 式的后台 Agent，但可以通过 SDK 或 tmux 实现。

```typescript:src/appendix-d/pi/agent-architecture.md
// 使用 Pi SDK 在应用中编排多个 Agent 实例
import { createAgentSession, AuthStorage, ModelRegistry, SessionManager } from "@earendil-works/pi-coding-agent";

async function parallelReview(files: string[]) {
  // 将 AuthStorage 提到循环外部，避免每个 Session 重复创建
  const authStorage = AuthStorage.create();
  const sessions = await Promise.all(
    files.map(async (file) => {
      const { session } = await createAgentSession({
        sessionManager: SessionManager.inMemory(),
        authStorage,                                     // 复用同一实例
        modelRegistry: ModelRegistry.create(authStorage),// 复用同一实例
      });
      return { file, session };
    })
  );

  const results = await Promise.all(
    sessions.map(({ file, session }) =>
      session.prompt(`审查文件 ${file}，关注安全漏洞和性能问题`).then((r) => ({
        file,
        review: r.content,
      }))
    )
  );

  // 清理
  await Promise.all(sessions.map(({ session }) => session.close()));
  return results;
}
```

### 6. MCP Integration（MCP 协议集成）

**适用场景**：通过 MCP 协议连接外部工具服务器（数据库、文件系统、第三方 API）。

Pi **没有内置 MCP 支持**——这是设计选择而非缺失。Pi 的哲学是"一切皆 Extension"：

> "Pi does not include MCP directly — build an extension that adds MCP support." — [pi.dev](https://pi.dev/)

这意味着 MCP 集成也通过 Extension API 实现。一个简单的 MCP 桥接 Extension 原型：

```typescript:src/appendix-d/pi/agent-architecture.md
import type { ExtensionAPI } from "@earendil-works/pi-agent-core";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

export default function (pi: ExtensionAPI) {
  const mcpClient = new Client({ name: "pi-mcp-bridge", version: "1.0.0" });

  // 工具请求时动态连接 MCP 服务器
  pi.on("tool_call", async (event) => {
    if (event.toolName === "mcp_query") {
      const transport = new StdioClientTransport({ command: "node", args: ["./mcp-server.mjs"] });
      await mcpClient.connect(transport);
      const result = await mcpClient.request({ ...event.args });
      return { result: JSON.stringify(result) };
    }
  });
}
```

**三种工具的 MCP 策略对比**：

| 工具 | MCP 集成方式 | 设计理念 |
|------|-------------|---------|
| **Pi** | Extension 桥接 | "一切皆 Extension"——MCP 是 Extension 的一种 |
| **OpenCode** | 原生内置（`mcpServers` 配置） | "开箱即用"——MCP 作为一等公民 |
| **Claude Code** | 子进程 MCP 服务器 | "协议化通信"——MCP 通过子进程管理 |

> 更多关于 MCP 协议的讨论见 → [MCP 协议](../../appendix-b/mcp.md)。Pi 的 Extension 体系参考 → [扩展体系详解](../customization.md)。

---

## 模式选择决策树

```text
你想做什么？
├─ 新增一个能力（查询API/计算/数据库）
│   └─ → Tool Extension
├─ 改变Agent的默认行为（沙箱/安全检查）
│   └─ → Replace Built-in Tool
├─ 在Agent生命周期中注入逻辑（审计/权限）
│   └─ → Event-Driven Extension
├─ 连接 MCP 协议的外部工具服务器
│   └─ → MCP Integration (Extension)
├─ 创建常用工作流的快捷入口
│   └─ → Slash Command Extension
└─ 多个Agent并行协作
    └─ → Multi-Session (SDK)
```

---

## 运行模式架构

Pi 有 4 种运行模式，理解它们的架构差异是设计 Agent 工作流的前提：

| 模式 | 启动方式 | 事件消费者 | 适用场景 |
|------|---------|-----------|---------|
| **交互模式** | `pi` | TUI 渲染器 | 日常交互式开发 |
| **Print 模式** | `pi -p "prompt"` | stdout 文本输出 | 单次查询、脚本集成 |
| **JSON 模式** | `pi --mode json -p "prompt"` | JSON 事件流 stdout | 跨语言管道、程序化消费 |
| **RPC 模式** | `pi --mode rpc` | JSONL stdin/stdout | 进程间双工通信 |
| **SDK 嵌入** | `createAgentSession()` | JavaScript 事件回调 | Node.js 应用嵌入 |

所有模式共享同一个 `agentLoop()` 事件流，差异仅在于事件的消费方式。这意味着：

- 为 TUI 开发的事件处理器（如 UI 组件更新）在 RPC 模式下会被跳过
- JSON 模式按行输出事件（`assistant`、`tool_call`、`error`、`done`），适合按行解析
- SDK 嵌入模式提供最丰富的事件监听能力（`on("message")`、`on("tool_call")`）

**设计含义**：如果你需要让 Extension 在不同模式下工作，检查 `ctx.hasUI` 来决定是否使用 UI 相关 API。

---

## 会话树（Session Tree）模式

Pi 独有的 Session Tree 分支管理功能，允许在对话历史中创建分支、回退和导航：

```bash
# 当前会话树
session_001 (main)
  ├── session_002 (experiment-A)  ← /fork 创建
  └── session_003 (experiment-B)  ← /fork 创建

# 导航到分支
/tree session_002

# 从当前点创建新分支
/fork "重构方案探索"
```

**设计模式**：Session Tree 适用于"探索-比较-选择"的工作流——尝试多个方案，每个方案在独立分支中进行，最后选择最优结果合并到主分支。这在其他 AI 编码工具中较少提供。

---

## 运行模式选择与 Pipelines

### Print 模式（CI/CD 友好）

```bash
# 单次查询，输出纯文本
pi -p "分析 src/ 的代码结构" --model sonnet

# 使用 Extension
pi -e ./audit-extension.ts -p "扫描安全漏洞"
```

### JSON 模式（程序化消费）

```bash
pi --mode json -p "列出文件" | jq 'select(.type == "assistant") | .content'
```

### RPC 模式（双工通信）

RPC 模式通过 JSONL（每行一个 JSON）在 stdin/stdout 上进行双工通信：

```text
→ {"type": "prompt", "prompt": "查询东京天气"}
← {"type": "assistant", "content": "正在查询..."}
← {"type": "tool_call", "tool": "get_weather", "args": {"city": "Tokyo"}}
← {"type": "assistant", "content": "东京当前天气..."}
← {"type": "done", "reason": "success"}
```

---

## 安全架构

Pi 的安全模型分为四个层次：

| 层次 | 机制 | 保护什么 |
|------|------|---------|
| **Project Trust** | 信任对话框 + `trust.json` | 自动加载项目级 Extension 和配置 |
| **工具级权限** | SDK `tools` allowlist + `customTools` | Agent 可调用的内置工具范围 |
| **运行时隔离** | 容器化（Gondolin/Docker/OpenShell） | 内置工具的执行环境（非 Extension 自身） |
| **事件拦截** | `tool_call` 事件阻断 | 自定义安全检查策略 |

### Project Trust 工作流

```text
启动 Pi → 检测到 .pi/extensions/
  ├─ 已信任 → 自动加载
  ├─ 未信任 → 弹出确认对话框（交互模式）
  │            ├─ 信任 → 记录到 trust.json，加载
  │            └─ 不信任 → 跳过项目级资源
  └─ 非交互模式（-p/--mode rpc）
       └─ 默认策略（defaultProjectTrust 配置）
```

### 工具级权限控制（SDK）

Pi 的 SDK（`@earendil-works/pi-coding-agent`）在创建 Session 时提供细粒度的工具权限控制：

```typescript:src/appendix-d/pi/agent-architecture.md
import { createAgentSession } from "@earendil-works/pi-coding-agent";

const { session } = await createAgentSession({
  tools: ["read", "write", "edit"],    // 只允许读取和编辑，不允许 bash
  customTools: ["my_search_tool"],      // 明确允许的自定义工具
  // ... 其他选项
});
```

`tools` 参数接受一个字符串数组，枚举允许使用的内置工具名（`read`、`write`、`edit`、`bash`）。不在列表中的工具将被拒绝。`customTools` 则枚举允许的自定义工具名。

> 这种方式比 Project Trust 更精确——不是"信任整个 Extension"，而是"只允许 Agent 调用特定的工具"。通常应该组合使用：Project Trust 控制 Extension 是否加载，`tools` allowlist 控制 Extension 中哪些工具可以执行。
>
> 参考：[Pi SDK security.md](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/security.md)、[permission-gate.ts](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/permission-gate.ts)

### Extension 的安全风险

Extension 是 TypeScript 模块，拥有**宿主进程的完整权限**。这意味着：

- 可以读写任何文件
- 可以执行任何 Shell 命令
- 可以访问所有环境变量（包括 API Key）

> **关键理解**：Pi **不提供内置沙箱**（来源：[security.md](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/security.md)——"Pi does not include a built-in sandbox"）。上表中的"运行时隔离"层指的是当您通过 Docker/Gondolin/OpenShell 容器化整个 Pi 进程时为内置工具提供的执行环境隔离，而非 Extension 之间的隔离。Extension 之间不存在沙箱隔离——每个 Extension 都共享宿主进程的完整权限。容器化方案（Gondolin 微 VM、Docker、OpenShell 策略沙箱）是推荐的生产级隔离手段。

**安全建议**：
1. 只在信任的来源安装 Extension
2. 利用 SDK 的 `tools` allowlist 限制 Agent 可调用的内置工具范围
3. 对敏感操作（`bash`）添加确认门禁（如 [`permission-gate.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/permission-gate.ts)）
4. 阻止对敏感路径的写入（如 [`protected-paths.ts`](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/examples/extensions/protected-paths.ts)）
5. 在生产环境中使用 Docker 或 Gondolin 容器化
6. `pi packages install` 安装的包使用 `npm install --omit=dev` 确保依赖隔离

---

## API 路由与多 Provider 管理

Pi 的 `pi-ai` 层支持 20+ Provider，但 Agent 的模型路由策略不同于 OpenCode 的 Category 系统：

```typescript:src/appendix-d/pi/agent-architecture.md
// 通过 ModelRegistry 动态管理模型
import { ModelRegistry, AuthStorage } from "@earendil-works/pi-coding-agent";

const auth = AuthStorage.create();
const registry = ModelRegistry.create(auth);

// 注册多个 Provider
registry.addProvider("anthropic", { apiKey: process.env.ANTHROPIC_API_KEY });
registry.addProvider("openai", { apiKey: process.env.OPENAI_API_KEY });

// 获取支持工具调用的模型列表
const toolModels = registry.getModelsSupportingToolCalls();
// → ['anthropic/claude-sonnet-4-6', 'openai/gpt-5.4-mini', ...]
```

在 Pi 的会话中，通过 `/model` 命令动态切换模型，无需重启 Agent：

```bash
/model sonnet     # 切换到 Sonnet
/model opus       # 切换到 Opus
/model gpt-5.4    # 切换到 GPT
```

Pi 的跨 Provider 切换是同 Session 内实时生效的，这是其他工具较少提供的灵活性。

---

## 与 OpenCode / Claude Code 的架构对比

| 维度 | Pi Agent | OpenCode (OMO) | Claude Code |
|------|----------|----------------|-------------|
| **Agent 架构** | 事件流 + Extension 注入 | Category 编排 + Sisyphus 主 Agent | Subagent 文件系统 + `/fork` |
| **自定义方式** | TypeScript Extension | JSON Category + Plugin Hook | Markdown Subagent + Hook |
| **工具注册** | `pi.registerTool()` | `definePlugin()` | 自定义命令 / MCP |
| **事件系统** | Lifecycle Events（15+） | Hook 系统（53+ 点） | Shell Hook（14+） |
| **运行模式** | 4 种（交互/Print/JSON/RPC）+ SDK | TUI + SDK | TUI + SDK |
| **内置 Agent 编排** | ❌ 不内置 | ✅ Category + Task API | ✅ Subagent + `/fork` |
| **模型路由** | 手动 `/model` 切换 | Category 自动路由 | Agent 级别 model 字段 |
| **并行执行** | SDK 多实例 | `run_in_background` | `/fork` 后台 Subagent |
| **Session 管理** | Tree 分支（独有） | 线性 | 线性 |
| **安全沙箱** | Gondolin / Docker / OpenShell | E2B Sandbox | Worktree Isolation |

**核心差异一句话**：Pi 让你**通过 Extension 构建自己的编排**，OpenCode 提供**开箱即用的编排层**，Claude Code 提供**文件系统级子 Agent 定义**。

---

## Extension vs Plugin vs Hook：三种扩展范式对比

| 维度 | Pi Extension | OpenCode Plugin | Claude Code Hook |
|------|-------------|----------------|------------------|
| **本质** | 在 Agent 运行时内部注入能力 | 在 Agent 运行时外部拦截事件 | 在 Agent 生命周期触发 Shell 脚本 |
| **工具注册** | `pi.registerTool()` API | `definePlugin()` Hook | 仅 MCP/自定义命令 |
| **替换内置工具** | ✅ 同名工具名覆盖 | ❌ 不能替换内置工具 | ❌ 不能替换 |
| **UI 定制** | ✅ Widget / Overlay / 编辑器替换 | ❌ | ❌ |
| **权限控制** | 可阻断工具调用 | 可阻断操作 | Shell 脚本返回值控制 |
| **分发机制** | Pi Packages（npm） | npm Plugin | 文件系统 + Git |
| **学习曲线** | 中（需 TypeScript） | 高（需理解 Hook 体系） | 低（Shell 脚本） |

---

## 完整案例：构建一个安全审查 Agent

以下案例演示如何利用 Pi 的多种设计模式组合，构建一个生产可用的安全审查 Agent。

### 需求

> 团队需要一个安全审查工具，在代码合并前自动检查安全漏洞。要求：只读、覆盖 OWASP Top 10、输出结构化报告。

### Extension 实现

```typescript:~/.pi/agent/extensions/security-auditor.ts
import type { ExtensionAPI } from "@earendil-works/pi-agent-core";

export default function (pi: ExtensionAPI) {
  // 工具 1：安全审查
  pi.registerTool({
    name: "security_audit",
    description: "对指定文件或代码片段进行安全审查。检查项：SQL注入、XSS、敏感信息硬编码、路径遍历、不安全的反序列化。",
    parameters: {
      type: "object",
      properties: {
        files: {
          type: "array",
          items: { type: "string" },
          description: "要审查的文件路径列表",
        },
      },
    },
    execute: async ({ files }) => {
      const fs = await import("fs/promises");
      const results: Array<{ file: string; severity: string; issue: string; line: number }> = [];

      for (const file of files) {
        const content = await fs.readFile(file, "utf-8");
        const lines = content.split("\n");

        // 静态模式检查
        lines.forEach((line, i) => {
          if (/SELECT .* FROM .* WHERE/.test(line) && !/preparedStatement|parameterized/i.test(line)) {
            results.push({ file, severity: "HIGH", issue: "可能的 SQL 注入", line: i + 1 });
          }
          if (/api[Kk]ey|secret|password\s*=/.test(line) && !/process\.env|getenv/.test(line)) {
            results.push({ file, severity: "CRITICAL", issue: "硬编码敏感信息", line: i + 1 });
          }
          if (/innerHTML|dangerouslySetInnerHTML/.test(line)) {
            results.push({ file, severity: "MEDIUM", issue: "可能的 XSS 风险", line: i + 1 });
          }
        });
      }

      return JSON.stringify(results, null, 2);
    },
  });

  // 工具 2：依赖安全检查
  pi.registerTool({
    name: "check_dependencies",
    description: "检查项目的依赖是否存在已知漏洞（基于 package.json）",
    parameters: { type: "object", properties: {} },
    execute: async () => {
      const fs = await import("fs/promises");
      const pkg = JSON.parse(await fs.readFile("package.json", "utf-8"));
      const deps = { ...pkg.dependencies, ...pkg.devDependencies };
      // 实际应调用 npm audit 或 Snyk API
      return `检查到 ${Object.keys(deps).length} 个依赖。建议运行 npm audit 获取详细报告。`;
    },
  });

  // 事件：自动审查
  pi.on("before_agent_start", async (_event, ctx) => {
    ctx.appendSystemPrompt(`
你是一个安全审查专家。当你收到代码审查请求时，请：
1. 使用 security_audit 工具检查指定文件
2. 使用 check_dependencies 检查依赖安全
3. 汇总输出结构化报告（Critical/High/Medium/Low）
4. 只读模式，不做任何修改
    `);
  });
}
```

### 使用方式

```bash
# 加载 Extension 启动
pi -e ./security-auditor.ts

# 在会话中
用户: 审查 src/api/ 目录下的所有文件
Agent: 正在审查 src/api/routes/auth.ts...
       [CRITICAL] 硬编码敏感信息 - src/api/routes/auth.ts:42
       [HIGH] 可能的 SQL 注入 - src/api/routes/users.ts:15
```

### 与 OpenCode 版本的区别

| 方面 | Pi 实现 | OpenCode 实现 |
|------|---------|---------------|
| **定义方式** | TypeScript Extension（编程） | Category JSON（声明式） |
| **调用方式** | Agent 通过工具名自动选择 | `task(category="security-reviewer")` |
| **注入指令** | `before_agent_start` 事件 | `prompt_append` 配置 |
| **工具权限** | Extension 内控制 | `tools.deny` 字段 |
| **测试迭代** | 热重载 `/reload` | 修改 JSON 即时生效 |

Pi 的方式更灵活（可以编程控制审查逻辑），但需要 TypeScript 开发经验。OpenCode 的方式声明式更强，适合非编程人员配置。

---

## 测试与迭代

### Extension 测试

Pi 的 Extension 是标准 TypeScript，可以用常规测试框架测试：

```typescript:src/appendix-d/pi/agent-architecture.md
import { test, describe, mock } from "node:test";
import assert from "node:assert";

// 模拟 ExtensionAPI
function createMockAPI() {
  const tools: any[] = [];
  return {
    registerTool: (t: any) => tools.push(t),
    getTools: () => tools,
  };
}

test("security_audit registers tools", () => {
  const api = createMockAPI();
  // 加载 Extension
  const ext = require("./security-auditor.ts").default;
  ext(api);
  assert(api.getTools().length >= 2);
  assert(api.getTools().some((t: any) => t.name === "security_audit"));
});
```

### 调试 Checklist

每次修改 Extension 后：

- [ ] 工具注册是否成功？（`pi.getAllTools()` 检查）
- [ ] 工具名和描述是否准确？（描述影响 LLM 调用决策）
- [ ] 错误处理是否覆盖？（Extension 中未捕获异常会静默失败）
- [ ] 是否在非交互模式测试过？（某些 `ctx.ui` 方法在 Print/RPC 模式不可用）
- [ ] `/reload` 后 Extension 是否正常重载？

---

## 相关章节

- ← [Pi Agent 概述与核心概念](./overview.md) — Pi 的设计哲学和核心架构
- → [Pi **Agent（智能体）** 扩展体系详解](./customization.md) — Extensions、Skills、Templates、Themes 完整参考
- → [Pi **Agent（智能体）** SDK 与程序化集成](./sdk.md) — 程序化集成和 Weather Agent 案例
- → [Pi **Agent（智能体）** 生态参考](./ecosystem.md) — Provider 生态、容器化方案
- → [oh-my-openagent **Agent（智能体）** 设计与开发指南](../../appendix-b/opencode/agent-architecture.md) — OMO Category 编排体系对比参考
- → [Claude Code **Agent（智能体）** 设计与开发指南](../../appendix-c/claudecode/agent-architecture.md) — Claude Code Subagent 体系对比参考
