# Pi **Agent（智能体）** 扩展体系详解

Pi 的核心设计哲学是"极简核心 + 强力扩展"。它主动不做许多功能（**MCP（模型上下文协议）**、子智能体、Plan 模式等），而是提供 4 层扩展机制，让用户按需构建工作流。

## 扩展体系总览

| 层级 | 能力 | 格式 | 加载位置 | 适用场景 |
|------|------|------|---------|---------|
| **Extensions** | 自定义工具、命令、事件处理、UI 组件 | TypeScript | `~/.pi/agent/extensions/` / `.pi/extensions/` | 深度定制，需要编程能力的扩展 |
| **Skills** | 按需系统指令注入 | SKILL.md（YAML frontmatter + 指令） | `~/.pi/agent/skills/` / `.pi/skills/` | 添加领域知识、角色设定、规则集 |
| **Prompt Templates** | 可复用提示词模板 | Markdown（YAML frontmatter + 模板） | `~/.pi/agent/prompts/` / `.pi/prompts/` | 常用指令模版 |
| **Themes** | UI 主题定制 | JSON | `~/.pi/agent/themes/` / settings.json | 配色和外观定制 |

此外还有 **Pi Packages** 作为打包分发机制，可将上述四种扩展打包为一个 npm 可分发的单元。

---

## Extensions（TypeScript 插件系统）

Extensions 是 Pi 最强大的扩展层，允许通过 TypeScript 编写自定义工具、命令、事件处理器、覆盖层和 UI 组件。

### 架构模型

Extensions 在 Pi 的 Agent 运行时中注册钩子，可以：

- **注册自定义工具**：新增 LLM 可调用的工具函数
- **注册自定义命令**：新增 Slash 命令（`/mycommand`）
- **替换内置工具**：例如 Gondolin extension 将 `read`/`write`/`edit`/`bash` 路由到微 VM 中执行
- **监听事件**：Agent 生命周期的各类事件（上下文准备、工具调用前/后 等）
- **添加 UI 组件**：自定义 Widget、状态行、覆盖层（Overlay）
- **替换编辑器**：自定义 TUI 编辑器组件

### 编写 Extension

Extensions 是标准的 TypeScript 文件，放置在 `~/.pi/agent/extensions/` 或 `.pi/extensions/` 目录：

```typescript:src/appendix-d/pi/customization.md
// ~/.pi/agent/extensions/my-extension.ts
import type { ExtensionAPI } from "@earendil-works/pi-agent-core";

export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "my_tool",
    description: "我的自定义工具",
    parameters: { /* TypeBox schema */ },
    execute: async (args) => {
      return "工具执行结果";
    },
  });

  pi.registerCommand({
    name: "mycommand",
    description: "我的自定义命令",
    execute: async (args) => {
      return "命令执行结果";
    },
  });
}
```

### 内置 Extension 示例

Pi 自带 3 个示例 Extension：

| Extension | 功能 |
|-----------|------|
| `prompt-url-widget.ts` | 编辑器中的 `@url` 自动补全，解析 URL 内容后提交给 LLM |
| `redraws.ts` | TUI 屏幕重绘事件处理 |
| `tps.ts` | 在状态行显示 Token Per Second 实时速率 |

完整的 Extension API 参考见 Pi 官方文档：[pi.dev/docs/latest/extensions](https://pi.dev/docs/latest/extensions)

### ExtensionAPI 类型速查表

Extensions 使用 TypeScript 类型系统，以下为核心类型速查：

| 类型 | 用途 | 关键方法/属性 |
|------|------|-------------|
| `ExtensionAPI` | Extension 工厂函数接收的 API 对象 | `registerTool()`, `registerCommand()`, `on()`, `sendMessage()` |
| `ToolDefinition` | 工具定义，描述 LLM 可调用的函数 | `name`, `description`, `parameters`, `execute()` |
| `RegisteredCommand` | Slash 命令定义 | `name`, `description`, `handler()` |
| `ExtensionContext` | 事件处理器和工具执行上下文 | `ctx.ui`, `ctx.cwd`, `ctx.sessionManager`, `ctx.model` |
| `ExtensionCommandContext` | 命令上下文（扩展 ExtensionContext） | `waitForIdle()`, `newSession()`, `fork()`, `reload()` |
| `ToolCallEvent` | 工具调用事件 | `toolName`, `input`, `args` |
| `KeyId` | 键盘快捷键标识 | 如 `"ctrl+x"`, `"ctrl+shift+d"` |

### 生命周期事件详表

Extensions 可监听的**关键事件**，覆盖 Agent 完整生命周期：

| 事件 | 触发时机 | 可阻断/修改 |
|------|---------|-----------|
| `project_trust` | 项目信任决策时 | ✅ 返回 `trusted: "yes"/"no"` |
| `session_start` | Session 启动/重载/切换时 | ❌ 通知型 |
| `session_shutdown` | Session 关闭时 | ❌ 清理资源 |
| `resources_discover` | 资源发现时 | ✅ 贡献额外 skill/prompt/theme 路径 |
| `before_agent_start` | 用户提交 prompt 后、Agent 循环开始前 | ✅ 注入消息/修改 system prompt |
| `agent_start` / `agent_end` | Agent 每次响应开始/结束 | ❌ |
| `turn_start` / `turn_end` | 每一轮 LLM 交互开始/结束 | ❌ |
| `message_end` | 消息完成时 | ✅ 可替换消息内容 |
| `tool_call` | 工具调用前 | ✅ 可阻断或修改参数 |
| `tool_result` | 工具返回结果后 | ✅ 可修改结果 |
| `input` | 用户输入时 | ✅ 可拦截或转换 |
| `session_before_switch` | Session 切换前 | ✅ 可取消 |
| `session_before_compact` | 上下文压缩前 | ✅ 提供自定义摘要 |

### 进阶 Extension 模式

**异步工厂**：当 Extension 需要初始化（如获取远程配置）时返回 Promise：

```typescript:src/appendix-d/pi/customization.md
export default async function (pi: ExtensionAPI) {
  const response = await fetch("http://localhost:1234/v1/models");
  const payload = await response.json();
  pi.registerProvider("local-openai", {
    baseUrl: "http://localhost:1234/v1",
    apiKey: "$LOCAL_OPENAI_API_KEY",
    api: "openai-completions",
    models: payload.data.map((model) => ({
      id: model.id, name: model.name ?? model.id,
      reasoning: false, input: ["text"],
      cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
      contextWindow: model.context_window ?? 128000,
      maxTokens: model.max_tokens ?? 4096,
    })),
  });
}
```

**长时间资源管理**：不要在 factory 中启动后台资源（进程、socket、文件监听）。改为在 `session_start` 中延迟初始化，`session_shutdown` 中清理：

```typescript:src/appendix-d/pi/customization.md
export default function (pi: ExtensionAPI) {
  let watcher: FileWatcher | null = null;

  pi.on("session_start", async (_event, ctx) => {
    watcher = startWatching(ctx.cwd);
  });

  pi.on("session_shutdown", async () => {
    watcher?.close();
    watcher = null;
  });
}
```

### 测试与调试 Extensions

Pi 没有专用的 Extension 测试框架，但有多种成熟的调试方式：

**1. `console.log` + 调试日志**

```bash
pi --log-level debug
```

Extension 中的 `console.log` 输出会显示在调试日志中。

**2. 热重载（`/reload`）**

将 Extension 放在自动发现目录（`~/.pi/agent/extensions/`），修改后用 `/reload` 热重载，无需重启 Pi。注意 `ctx.reload()` 调用后应当立即 `return`，因旧上下文仍在执行。

**3. 用 `-e` 标志快速测试**

```bash
pi -e ./my-extension.ts
```

无需将 Extension 复制到自动发现目录即可验证加载和基本功能。

**4. Extension 样式选择**

| 样式 | 适用场景 |
|------|---------|
| 单文件 `my-ext.ts` | 小型扩展（100 行以内） |
| 目录 + `index.ts` | 多文件组织 |
| Package（含 `package.json`） | 需要 npm 第三方依赖 |

含依赖的 Extension 结构：

```
my-extension/
├── package.json       # 声明 dependencies
├── package-lock.json
├── node_modules/
└── src/
    └── index.ts       # export default function(pi: ExtensionAPI)
```

**5. 错误边界**

Extension 的加载错误**不会**导致 Pi 崩溃——Pi 捕获异常后记录日志并继续运行。但强烈建议在 `execute()` 中自行捕获异常：

```typescript:src/appendix-d/pi/customization.md
execute: async (args) => {
  try {
    return { content: [{ type: "text", text: result }], details: {} };
  } catch (err) {
    return {
      content: [{ type: "text", text: `错误: ${err.message}` }],
      details: { isError: true },
    };
  }
}
```

**6. 常见陷阱**

| 陷阱 | 说明 | 解决方案 |
|------|------|---------|
| 缺少 `typebox` 依赖 | Tool 参数定义需要 TypeBox | `npm install typebox`（注意包名不带 `@sinclair/`） |
| 导入路径错误 | 使用旧包名 `@mariozechner/*` | 改为 `@earendil-works/*` |
| 异步错误未捕获 | Promise reject 不被外部捕获 | 在 `execute()` 内 try/catch |
| 在 factory 中启动后台资源 | session 未启动时资源已创建 | 推迟到 `session_start` 事件中 |
| 忽略 Print/RPC 模式 | 某些 `ctx.ui` 方法在非交互模式不可用 | 先检查 `ctx.hasUI` |
| reload 后继续使用旧状态 | 旧引用已失效 | `await ctx.reload(); return;` |

---

## Skills（Agent Skills 标准）

Skills 遵循 [agentskills.io](https://agentskills.io) 标准，以 SKILL.md 文件提供按需加载的系统指令。

### **Skill（技能）** 文件格式

```markdown
---
name: add-llm-provider
description: 添加自定义 LLM Provider 配置
---

你是一个 LLM Provider 配置专家。你的职责是：

1. 读取当前的 Provider 配置文件
2. 根据用户提供的 API 地址和密钥信息添加新 Provider
3. 验证配置是否正确加载
```

Skills 使用 YAML frontmatter 声明 `name` 和 `description`，正文作为系统指令注入到 Agent 的上下文中。

### 加载位置与优先级

Skills 从多个位置加载：

| 位置 | 作用域 |
|------|--------|
| `~/.pi/agent/skills/` | 全局技能 |
| `.pi/skills/` | 项目级技能 |
| 通过 `pi packages install` 安装 | 包内技能 |

支持 `.gitignore` 风格的忽略文件（`SKILL.md.ignore`）。

### 调用方式

通过 `/skill:name` 在编辑器中调用已识别到的 Skill。Pi 的 harness 层（`formatSkillsForSystemPrompt`）将 Skill 内容格式化为 XML 块注入到系统提示中：

```xml:src/appendix-d/pi/customization.md
<skill name="add-llm-provider">
你是一个 LLM Provider 配置专家。你的职责是：
...
</skill>
```

---

## **Prompt（提示词）** Templates（提示词模板）

Prompt Templates 是命名后可复用的提示词片段。它们与 Skills 的区别在于：

- **Skills** 是**系统性指令**，注入到 Agent 的角色定义中，长期有效
- **Prompt Templates** 是**单次调用模板**，通过 `/name` 快捷注入到当前消息

### 模板文件格式

```markdown
---
name: cl
description: 生成 Conventional Commit 格式的提交信息
---

请为当前变更生成一个 Conventional Commit 格式的提交信息。

格式要求：
<type>(<scope>): <description>

<body>

<footer>

类型包括：feat、fix、docs、style、refactor、test、chore
```

### 内置模板

Pi 自带以下 Prompt Templates：

| 模板 | 文件 | 功能 |
|------|------|------|
| `/cl` | `.pi/prompts/cl.md` | 生成 Conventional Commit 提交信息 |
| `/is` | `.pi/prompts/is.md` | 生成 Issue 模板 |
| `/pr` | `.pi/prompts/pr.md` | 生成 PR 描述模板 |

在编辑器中输入 `/cl` 即可调用模板，模板内容会自动填充到当前消息中，用户可以在此基础上编辑。

### 加载位置

| 位置 | 作用域 |
|------|--------|
| `~/.pi/agent/prompts/` | 全局 |
| `.pi/prompts/` | 项目级 |

---

## Themes（主题系统）

Pi 的 TUI 支持热重载主题配置：

```json
{
  "theme": "dark",
  "colors": { ... }
}
```

通过 `/settings` 在运行中切换主题，无需重启。支持 dark、light 以及完全自定义的主题 JSON。

---

## **Context（上下文）** Files（上下文文件）

Pi 支持多层级上下文文件配置：

| 文件 | 作用 | 优先级 |
|------|------|--------|
| `AGENTS.md` | 项目级指令文件 | 高（项目级最高） |
| `SYSTEM.md` | 添加到系统提示中 | 中 |
| `APPEND_SYSTEM.md` | 追加到系统提示末尾 | 中 |

文件加载位置：

| 位置 | 作用域 | 说明 |
|------|--------|------|
| `~/.pi/agent/AGENTS.md` | 全局 | 所有项目生效 |
| `~/.pi/agent/SYSTEM.md` | 全局 | 所有项目生效 |
| `.pi/AGENTS.md` | 项目级 | 覆盖全局 |
| `.pi/SYSTEM.md` | 项目级 | 覆盖全局 |
| 项目根 `AGENTS.md` | 项目级 | 仅当前项目 |

`--no-context-files` 标志可禁用所有上下文文件加载。

---

## Pi Packages（扩展打包分发）

Pi Packages 是将 Extensions、Skills、Prompt Templates、Themes 打包为可分发 npm 包的机制。

### Package 结构

```
my-pi-package/
├── package.json           # 包含 "pi" 字段声明包类型
├── extensions/
│   └── my-extension.ts
├── skills/
│   └── my-skill.md
├── prompts/
│   └── my-prompt.md
└── themes/
    └── my-theme.json
```

`package.json` 中的 `pi` 字段：

```json
{
  "name": "my-pi-package",
  "version": "1.0.0",
  "pi": {
    "extensions": ["extensions/my-extension.ts"],
    "skills": ["skills/my-skill.md"],
    "prompts": ["prompts/my-prompt.md"],
    "themes": ["themes/my-theme.json"]
  }
}
```

### 安装与分发

```bash
# 从 npm 安装
pi packages install my-pi-package

# 从本地路径安装
pi packages install ./path/to/my-pi-package
```

通过 `pi-build` CLI 工具打包。分发方式包括 npm 仓库、Git 仓库或直接本地路径安装。

---

## 容器化部署

Pi 默认以当前用户权限运行所有工具。在生产环境、多租户或安全敏感场景下，建议将 Pi 放入隔离环境。Pi 提供三种容器化模式：

### Gondolin（微 VM 方案）

Gondolin 是本地 Linux 微 VM，仅隔离内置工具的执行，API Key 等凭据保留在宿主机上：

```bash
cp -R examples/extensions/gondolin ~/.pi/agent/extensions/gondolin
cd ~/.pi/agent/extensions/gondolin && npm install --ignore-scripts
cd /path/to/project && pi -e ~/.pi/agent/extensions/gondolin
```

Extension 将 `read`/`write`/`edit`/`bash`/`grep`/`find`/`ls` 路由到 VM 内执行，宿主机 `cwd` 挂载为 VM 的 `/workspace`。要求 Node.js >= 23.6.0 和 QEMU。

### Docker（全进程隔离）

将整个 Pi 进程运行在 Docker 容器中：

```dockerfile
FROM node:24-bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
  bash ca-certificates git ripgrep && rm -rf /var/lib/apt/lists/*
RUN npm install -g --ignore-scripts @earendil-works/pi-coding-agent
WORKDIR /workspace
ENTRYPOINT ["pi"]
```

```bash
docker build -t pi-sandbox -f Dockerfile.pi .
docker run --rm -it \
  -e ANTHROPIC_API_KEY \
  -v "$PWD:/workspace" \
  -v pi-agent-home:/root/.pi/agent \
  pi-sandbox
```

建议：避免挂载宿主机 `~/.pi/agent`，改用命名卷 `pi-agent-home`，防止 Session 和凭据泄露。

### OpenShell（策略控制沙箱）

适用于需要细粒度安全策略的远程或本地沙箱：

```bash
openshell gateway add <gateway-url> --name my-gateway
openshell gateway select my-gateway
openshell sandbox create --name pi-sandbox --from pi -- pi
```

OpenShell 网关可注入推理凭据，沙箱内代码只需调用 `https://inference.local` 即可使用配置好的 Provider。

### Containerization vs Extension Tool Routing

| 模式 | 隔离粒度 | 凭据安全 | 适用场景 |
|------|---------|---------|---------|
| Gondolin | 仅内置工具 | ✅ 凭据在宿主机 | 本地开发隔离 |
| Docker | 全进程 | ⚠️ 凭据需传入容器 | CI/CD、简单隔离 |
| OpenShell | 全进程 + 策略 | ✅ 网关注入凭据 | 远程/多租户沙箱 |

---

## 安全考量

### 项目信任（Project Trust）

Pi 的信任机制控制**项目级配置和扩展**的自动加载，而非运行时的权限沙箱：

- 当启动目录存在 `.pi/extensions`、`.pi/skills` 等资源时，Pi 询问是否信任该项目
- 信任决定存储在 `~/.pi/agent/trust.json` 中
- 信任前仅加载全局 Extension 和 CLI `-e` Extension
- 可通过 `--approve`/`-a` 或 `--no-approve`/`-na` 覆盖一次运行的决定
- `defaultProjectTrust` 可设为 `"ask"`（默认）、`"always"` 或 `"never"`

信任的作用范围：允许加载项目级 Extension、Skills、配置。`AGENTS.md` 等上下文文件**不**受信任机制限制。

### Extension 权限

Extensions 是 TypeScript 模块，**拥有宿主进程的完整权限**：

- 可以读写任意文件
- 可以执行任意 Shell 命令
- 可以访问所有环境变量

因此，只从信任的来源安装 Extension。通过 `pi packages install` 安装的包在生产模式下使用 `npm install --omit=dev`，确保非开发依赖被正确隔离。

### 安全实践建议

1. **最小权限原则**：Extension 应只请求所需权限。对危险 bash 命令添加确认门禁（参考 `permission-gate.ts` 示例 Extension）
2. **API Key 管理**：使用环境变量而非硬编码。非交互模式（`-p`、`--mode json`、`--mode rpc`）不显示信任提示，确保 CI 中信任策略明确
3. **不受信任的仓库**：在容器中运行 Pi，仅挂载所需工作路径，避免挂载凭据
4. **审计日志**：通过 `session_start`/`session_shutdown` 事件的自定义 Extension 记录操作日志

---

## 扩展体系对比

| 维度 | Pi Agent Extensions | OpenCode **Plugin（插件）** | Claude Code Hooks |
|------|---------------------|-----------------|-------------------|
| 语言 | TypeScript | TypeScript | Node.js / Shell |
| 工具注册 | `pi.registerTool()` | `definePlugin()` | CLAUDE.md 自定义命令 |
| 事件钩子 | 生命周期事件 | 20+ Hook 点 | Hook 系统 |
| UI 定制 | Widget / Overlay / 编辑器替换 | 有限 | 不支持 |
| 打包分发 | Pi Packages (npm) | npm | 无标准机制 |

---

## 测试与调试

### Extension 热重载测试

Pi 支持 `/reload` 命令热重载 Extensions，修改 TypeScript 源码后无需重启 Agent：

```bash
# 编辑 Extension 后，在 Pi 会话中执行
/reload
```

快速测试单个 Extension 用 `-e` 标志：

```bash
pi -e ./my-extension.ts
```

放在 `~/.pi/agent/extensions/` 或 `.pi/extensions/` 目录的 Extension 支持自动发现和热重载；其他路径只能用 `-e` 单次加载，不支持 `/reload`。

### 调试技巧

- **`/debug` 命令**：写入 `~/.pi/agent/pi-debug.log`，包含 TUI 渲染行和最近发送给 LLM 的消息全文
- **console.log**：Extension 中的 `console.log` 输出到 pi 的 stderr，正常启动终端即可看到
- **注册验证**：`pi.registerTool()` 后调用 `pi.getAllTools()` 检查工具是否注册成功
- **零构建**：Pi 使用 `jiti` 即时代译 TypeScript，无需构建步骤，修改保存后 `/reload` 立即生效

### 常见陷阱

| 陷阱 | 现象 | 解决方案 |
|------|------|----------|
| **ExtensionAPI 版本不匹配** | 方法报 `undefined` | 确认 `@earendil-works/pi-agent-core` 版本与安装的 Pi 版本一致 |
| **异步错误被吞** | Extension 加载失败无提示 | 顶层用 try-catch，捕获后 `console.error` 输出错误详情 |
| **工具名冲突** | 注册的工具不生效 | Pi 的策略是"先注册者保留"，用 `pi.getActiveTools()` 检查实际生效的工具列表 |
| **依赖缺失** | Extension 内 import 报错 | 在 Extension 所在目录运行 `npm install`，或创建 `package.json` 声明依赖 |

### CI 集成

Extensions 是标准 TypeScript，可用 `node:test` / Vitest 编写测试：

```bash
npm test
```

Pi 官方推荐在 CI 中跑非 LLM 测试（`./test.sh` 或 `npm test`），验证 Extension 加载、工具注册和事件响应。发布 Pi Package 前用 `npm pack` 验证打包完整性。

---

> → [Pi **Agent（智能体）** 生态参考](./ecosystem.md) 涵盖 Provider 生态、程序化集成方式和容器化方案
> → [Pi **Agent（智能体）** SDK 与程序化集成](./sdk.md) 涵盖程序化集成、Agent Session API 和 RPC 模式

---

## 读者视角

### 适用读者角色
- 入门开发者 — Pi 的四层扩展体系降低了使用门槛，适合快速上手
- 智能体开发工程师 — Extension API 为深度定制提供 TypeScript 支持
- 效率开发者 — 丰富的扩展生态满足快速迭代需求
- 技术负责人 — 容器化方案（Gondolin/Docker/OpenShell）满足企业安全要求
- Skill 作者 — Skills 系统遵循标准化，易于创建和分享
- 系统架构师 — 明确的安全边界和信任机制，便于架构评估
- 安全工程师 — 安全模型透明，易于威胁建模和合规评估

### 典型使用场景
- 通过 Extensions 构建自定义工具，满足特定领域需求
- 通过 Skills 注入领域知识和角色设定，提升 Agent 专业性
- 通过 Prompt Templates 实现常用指令模板，减少重复工作
- 通过 Themes 定制 UI 主题，适应团队偏好
- 通过 Pi Packages 打包扩展，实现团队共享和分发
- 通过 Gondolin 容器化方案实现安全隔离，满足企业需求
- 通过 Pi Packages 安装扩展，实现快速功能扩展

### 使用示例
```bash
# 安装 Pi Core
npm install -g @earendil-works/pi-coding-agent

# 创建 Extension
pi -e ./my-extension.ts

# 加载 Skill
/skill:weather-assistant

# 使用 Prompt Template
/cl

# 切换主题
/settings { "theme": "dark" }

# 安装 Pi Package
pi packages install my-pi-package
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
   ```typescript:src/appendix-d/pi/customization.md
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

5. **创建 Skill**
   ```bash
   # 创建 Skill 文件
   echo "---
name: weather-assistant
description: 天气助手
---

你是一个专业的天气助手。你的职责是：
1. 查询指定城市的天气
2. 格式化输出结果
3. 提供天气建议
" > ~/.pi/agent/skills/weather-assistant.md
   ```

6. **使用 Skill**
   ```bash
   /skill:weather-assistant
   ```

### 与前/后文章的衔接
- ← [Pi Agent 概述与核心概念](./overview.md) — 提供 Pi 的设计哲学和核心架构
- → [Pi **Agent（智能体）** SDK 与程序化集成](./sdk.md) — 学习 Pi 的程序化集成和 SDK 使用

---

## 常见反模式

### 用 Extension 做本应由 Skill 完成的事

Extension 是强大的 TypeScript 编程工具，但许多开发者用它来实现简单的指令集（比如"审查代码时关注安全问题"）。这种场景完全可以用 Skill 实现——一个 SKILL.md 文件就能定义角色和规则，不需要编写任何 TypeScript 代码。用 Extension 做 Skill 的事不仅增加了维护成本，还因为 Extension 的加载和初始化开销拖慢了会话启动速度。

区分标准是：如果你需要的是"系统指令注入"（告诉 Agent 怎么做），用 Skill；如果你需要的是"新能力"（让 Agent 能做之前做不到的事），用 Extension。Skill 是声明式的，Extension 是编程式的。声明式能解决的问题不要升级到编程式。

### Skill 的 description 写得过于笼统

Pi 的 Skill 通过 `description` 字段让 LLM 判断何时激活该 Skill。如果描述写成"一个有用的 Skill"或"处理各种任务"，LLM 几乎会在所有场景下激活它，导致系统提示词膨胀、响应延迟增加，且 Skill 的专业指令被稀释在大量无关上下文中。

每个 Skill 的 description 应该明确描述触发条件。例如"当用户需要审查代码安全性时使用"优于"代码审查 Skill"。好的描述让 LLM 能精确判断何时需要、何时不需要，避免不必要的激活。

### Pi Package 打包时包含不必要的依赖

通过 `pi packages install` 安装的 Extension 使用 `npm install --omit=dev` 安装依赖，确保只包含生产依赖。但许多开发者在打包 Pi Package 时没有清理 `node_modules` 中的开发依赖（TypeScript、测试框架、linter），导致安装包体积膨胀数倍。

使用 `pi-build` CLI 工具打包前，确保 `package.json` 的 `dependencies` 只包含运行时必需的包，`devDependencies` 包含开发工具。打包后用 `npm pack --dry-run` 检查包内容，确认不包含源码测试文件和开发配置。

## 适用场景与限制

### Skills 不支持运行时动态内容注入

Skills 通过 SKILL.md 的 YAML frontmatter 和正文提供静态指令。虽然 Pi 支持 `` !`command` `` 语法在 Skill 加载时执行 Shell 命令并注入输出，但这种注入是一次性的——Skill 加载后内容就固定了，不会随着上下文变化而更新。

如果需要动态内容注入（比如在每次工具调用前注入最新的 Git 状态），应该用 Extension 的事件监听器实现。Extension 可以在 `before_agent_start`、`tool_call` 等事件中动态构造和注入内容，灵活性远高于 Skill。

### Prompt Templates 的命名空间是全局的

Pi 的 Prompt Templates 通过文件名作为命令名（如 `/cl`、`/pr`）。如果两个 Pi Package 定义了同名的 Prompt Template，后加载的会覆盖先加载的，且没有冲突提示。这在安装多个第三方 Package 时可能导致意外行为。

安装新 Package 后，检查它提供的 Prompt Templates 是否与你的自定义模板冲突。对于团队共享的模板，使用明确的命名约定（如项目前缀 `myproject-cl`）避免冲突。Pi 的 Prompt Templates 没有版本控制机制，Package 升级时模板可能被静默替换。

### Theme 系统只支持颜色定制

Pi 的 Theme 系统通过 JSON 配置 TUI 的颜色方案，支持 dark、light 和自定义主题。但它不支持布局定制（如修改面板大小、调整侧边栏位置）或字体配置。对于需要深度 UI 定制的场景，Theme 系统的能力有限。

如果需要修改 TUI 的布局或组件结构，需要通过 Extension 的 UI 定制能力（Widget、Overlay、编辑器替换）实现。Theme 只是 Pi UI 定制的最浅层，更深层次的定制需要编写 TypeScript Extension。

## 常见失败与陷阱

### Extension 热重载后旧状态残留

使用 `/reload` 热重载 Extension 时，Pi 会重新加载所有 Extension 文件。但如果旧 Extension 在模块级维护了状态（全局变量、缓存、连接池），这些状态不会被清理。新 Extension 代码可能意外引用了旧状态，产生"明明改了代码但行为没变"的困惑。

热重载后立即验证 Extension 的行为是否符合预期。在开发阶段，使用 `pi --log-level debug` 查看 Extension 的加载和初始化日志。避免在 Extension 中使用模块级可变状态，改为在事件处理器中使用局部变量或通过 `ctx` 传递状态。

### Skills 的 SKILL.md.ignore 文件不生效

Pi 支持 `.gitignore` 风格的忽略文件（`SKILL.md.ignore`）来排除特定 Skill。但如果忽略文件的路径或格式不正确（比如放在了错误的目录层级，或者使用了不支持的 glob 模式），Skill 不会被排除，仍然会被加载和注入到系统提示中。

创建忽略文件后，用 `/skills` 命令检查 Skill 列表，确认被忽略的 Skill 不在列表中。忽略文件必须放在 Skills 目录的根层级（如 `~/.pi/agent/skills/SKILL.md.ignore`），且每行一个 glob 模式。

### 多个 Extension 注册同名事件处理器的执行顺序不确定

当多个 Extension 监听同一个事件（如 `tool_call`）时，Pi 不保证执行顺序。如果你的两个 Extension 都监听 `tool_call` 事件并返回 `{ block: true }`，哪个先执行取决于 Extension 的加载顺序，而加载顺序可能因文件系统遍历顺序而不同。

不要依赖多个 Extension 对同一事件的处理顺序。每个 Extension 的事件处理器应该独立工作，不假设自己是第一个或最后一个执行的。如果需要有序处理，考虑将多个逻辑合并到一个 Extension 中，用内部的优先级队列控制执行顺序。
