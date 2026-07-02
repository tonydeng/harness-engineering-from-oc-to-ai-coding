# CLI 命令与交互模式参考

Pi 支持 4 种运行模式，适应不同的使用场景。本章覆盖交互模式下的编辑器功能、Slash 命令、键盘快捷键，以及运行模式和 CLI 参数参考。

---

## 运行模式

| 模式 | 命令 | 适用场景 |
|------|------|---------|
| **交互模式** | `pi` | 日常编码，终端交互 |
| **Print / JSON 模式** | `pi -p "prompt"` / `pi --mode json` | 单次查询，脚本集成 |
| **RPC 模式** | `pi --mode rpc` | 非 Node.js 进程集成 |
| **SDK 模式** | 程序化调用 | Node.js 应用嵌入 |

### 交互模式

默认模式，启动进入 TUI 界面：

```bash
pi                                    # 当前目录启动
pi -c                                 # 继续最近的 Session
pi -r                                 # 浏览并选择历史 Session
pi --name "my task"                   # 设置 Session 显示名称
pi --session <path|id>                # 指定 Session 文件或 ID
pi --fork <path|id>                   # Fork 一个已有 Session
pi --no-session                       # 临时模式（不保存 Session）
pi --no-context-files                 # 不加载 AGENTS.md 等上下文文件
pi --approve                          # 自动信任项目（覆盖 trust 设置）
```

### Print 模式

非交互式单次执行：

```bash
pi -p "列出当前目录的文件"              # 执行后打印结果并退出
pi -p "解释这个函数" --source file.ts   # 附带源文件
```

### JSON Event Stream 模式

结构化事件输出，适合脚本消费：

```bash
pi --mode json -p "重构这个函数"
```

### RPC 模式

基于 stdin/stdout JSONL 的进程间通信协议，适合非 Node.js 环境集成：

```bash
pi --mode rpc
```

RPC 模式使用严格的 LF 分隔 JSONL 帧（禁止在 JSON 载荷内使用 Unicode 分隔符）。

→ SDK 和 RPC 的详细用法见 [生态与集成场景](./ecosystem.md#程序化集成)

---

## 编辑器特性

Pi 的交互模式编辑器提供丰富的输入能力：

### 基本编辑

| 操作 | 快捷键 |
|------|--------|
| 提交消息 | Enter |
| 多行输入 | Shift+Enter（Windows Terminal 为 Ctrl+Enter） |
| 清空编辑器 | Ctrl+C |
| 退出 Pi | Ctrl+C 两次 |
| 取消/中止 | Escape |
| 打开 Session Tree | Escape 两次 |

### 文件与路径

| 操作 | 说明 |
|------|------|
| `@` | 模糊搜索项目文件并引用 |
| Tab | 补全路径 |
| 图片粘贴 | Ctrl+V 粘贴图片（Windows 为 Alt+V），或拖入终端 |

### Bash 集成

| 操作 | 说明 |
|------|------|
| `!command` | 执行 Bash 命令，输出发送给 LLM |
| `!!command` | 执行 Bash 命令，输出不发送给 LLM |

### 消息队列

在 **Agent（智能体）** 工作时可以排队提交消息：

| 操作 | 说明 |
|------|------|
| Enter | 排队 **Steering** 消息：当前工具调用执行完后交付 |
| Alt+Enter | 排队 **Follow-up** 消息：Agent 全部工作完成后交付 |
| Escape | 中止当前处理，恢复队列中的消息到编辑器 |
| Alt+Up | 将队列中的消息取回编辑器 |

消息交付策略可通过 `/settings` 配置：
- `steeringMode`：`"one-at-a-time"`（默认，逐条等待响应）或 `"all"`（批量交付）
- `followUpMode`：同上

---

## Slash 命令

Pi 的 Slash 命令以 `/` 开头，在编辑器中输入即可触发。

### 会话管理

| 命令 | 功能 |
|------|------|
| `/new` | 新建会话 |
| `/resume` | 从历史会话中选择恢复 |
| `/session` | 显示当前会话信息（文件路径、ID、消息数、Token 用量、成本） |
| `/name <name>` | 设置当前会话显示名称 |
| `/fork` | 从当前分支的用户消息创建新 Session 文件 |
| `/clone` | 复制当前活动分支为新 Session |
| `/tree` | 在 Session Tree 中导航，可从任意历史点继续 |
| `/compact [prompt]` | 手动触发上下文压缩，可选自定义指令 |
| `/export [file]` | 导出会话为 HTML 或 JSONL 文件 |
| `/import <file>` | 导入并恢复 JSONL Session 文件 |
| `/share` | 以私有 GitHub Gist 上传并生成分享链接 |

### 认证与模型

| 命令 | 功能 |
|------|------|
| `/login` | OAuth 登录（订阅类 Provider） |
| `/logout` | 登出 |
| `/model` | 切换当前使用的模型 |
| `/scoped-models` | 启用/禁用模型以用于 Ctrl+P 循环切换 |

### 设置与信息

| 命令 | 功能 |
|------|------|
| `/settings` | 修改 Thinking Level、主题、消息交付、传输协议等 |
| `/trust` | 保存项目信任决策（重启后生效） |
| `/reload` | 重新加载快捷键、扩展、Skills、Prompts 和 **Context（上下文）** Files |
| `/hotkeys` | 显示所有键盘快捷键 |
| `/changelog` | 显示版本历史 |
| `/quit` | 退出 Pi |

### 复制与分享

| 命令 | 功能 |
|------|------|
| `/copy` | 复制最后一条助手消息到剪贴板 |

### 扩展命令

通过 [Extensions](../pi/customization.md#extensions) 可以注册自定义命令。安装了 Skills 后可通过 `/skill:name` 调用。

---

## 键盘快捷键

### 常用快捷键

| 快捷键 | 操作 |
|--------|------|
| Ctrl+C | 清空编辑器 |
| Ctrl+C 两次 | 退出 Pi |
| Escape | 取消/中止当前操作 |
| Escape 两次 | 打开 Session Tree 导航 |
| Ctrl+L | 打开模型选择器 |
| Ctrl+P | 循环切换到下一个已启用的模型 |
| Shift+Ctrl+P | 循环切换到上一个已启用的模型 |
| Shift+Tab | 切换 Thinking Level |
| Ctrl+O | 展开/折叠工具输出 |
| Ctrl+T | 展开/折叠推理过程（Thinking blocks） |

### 完整列表

在交互模式中输入 `/hotkeys` 可查看全部快捷键。自定义快捷键通过 `~/.pi/agent/keybindings.json` 配置。

---

## 配置层级

Pi 的配置分全局和项目两层：

| 位置 | 作用域 | 内容 |
|------|--------|------|
| `~/.pi/agent/settings.json` | 全局（所有项目） | 默认配置 |
| `.pi/settings.json` | 项目级 | 覆盖全局配置 |
| `~/.pi/agent/keybindings.json` | 全局快捷键 | 自定义键位映射 |

### 常用配置项

通过 `/settings` 在交互模式中修改，或直接编辑 JSON 文件：

- **thinkingLevel**：推理程度（off / minimal / low / medium / high / xhigh）
- **theme**：主题（dark / light / 自定义）
- **steeringMode**：Steering 消息交付策略
- **followUpMode**：Follow-up 消息交付策略
- **transport**：Provider 传输协议偏好（sse / websocket / auto）
- **defaultProjectTrust**：项目信任默认行为（ask / always / never）
- **enableInstallTelemetry**：安装/更新匿名遥测

→ 更详细的配置说明见 [生态与集成场景](./ecosystem.md#安全与沙箱)
→ 完整命令列表参见 Pi 官方文档：[pi.dev/docs/latest](https://pi.dev/docs/latest)

---

## 读者视角

### 适用读者角色
- 入门开发者 — Pi 的 4 种运行模式降低了使用门槛，适合快速上手
- 智能体开发工程师 — Extension API 为深度定制提供 TypeScript 支持
- 效率开发者 — 丰富的 Slash 命令和编辑器特性提升工作效率
- 技术负责人 — 容器化方案（Gondolin/Docker/OpenShell）满足企业安全要求
- **Skill（技能）** 作者 — Skills 系统遵循标准化，易于创建和分享
- 系统架构师 — 明确的安全边界和信任机制，便于架构评估
- 安全工程师 — 安全模型透明，易于威胁建模和合规评估

### 典型使用场景
- 日常编码中使用 Pi 的交互模式，提高代码编辑效率
- 通过 Print 模式实现单次查询，集成到 CI/CD 管道
- 使用 JSON Event Stream 模式实现自动化测试和监控
- 通过 RPC 模式实现跨语言集成，构建多语言开发工具
- 使用 Session Tree 分支管理，实现并行探索和实验
- 通过 Gondolin 容器化方案实现安全隔离，满足企业需求
- 使用 Extension API 构建自定义工具，满足特定领域需求

### 使用示例
```bash
# 启动交互模式
pi

# 执行单次查询
pi -p "列出当前目录的文件"

# 使用 JSON Event Stream 模式
pi --mode json -p "重构这个函数"

# 使用 RPC 模式
pi --mode rpc

# 创建新会话
/new

# 恢复历史会话
/resume

# 使用 Slash 命令
/settings
/trust
/tree
/compact
```

### 工程化示例

**配置顺序检查表：**

1. **安装 Pi Core**
   ```bash
   npm install -g @earendil-works/pi-coding-agent
   ```

2. **创建项目目录**
   ```bash
   mkdir -p my-project
   cd my-project
   ```

3. **启动 Pi 并配置**
   ```bash
   pi --name "my task"
   ```

4. **使用 Slash 命令**
   ```bash
   /settings { "theme": "dark" }
   /trust
   ```

5. **执行任务**
   ```bash
   /new
   # 输入提示词
   ```

### 与前/后文章的衔接
- ← [Pi Agent 概述与核心概念](./overview.md) — 提供 Pi 的设计哲学和核心架构
- → [扩展体系详解](./customization.md) — 学习 Pi 的四层扩展体系

---

## 常见反模式

### 在 CI/CD 中使用交互模式而非 Print 模式

有些开发者在自动化管道中使用 `pi`（交互模式）而非 `pi -p "query"`（Print 模式）。交互模式启动 TUI 界面，在没有终端的 CI 环境中会导致渲染错误或进程挂起。更严重的是，交互模式会等待用户输入，这在无人值守的 CI 流水线中意味着永远无法完成。

CI/CD 场景必须使用 Print 模式（`pi -p "query"`）或 JSON 模式（`pi --mode json -p "query"`）。Print 模式执行完毕后自动退出，JSON 模式提供结构化输出便于脚本解析。对于需要复杂工作流的场景，使用 SDK 模式在 Node.js 脚本中直接嵌入 Pi Agent。

### 过度使用 /compact 而不管理上下文窗口

`/compact` 命令手动触发上下文压缩，但它会丢失较早对话的细节。许多用户在每次感到对话变慢时就执行 `/compact`，结果导致之前讨论的设计决策、代码约定和技术选择被摘要简化，Agent 在后续操作中偏离了原始方向。

上下文管理应该是主动的而非被动的。在开始新任务前用 `/new` 创建新会话，而不是在一个超长会话中反复压缩。如果必须使用长会话，将关键约束写入 AGENTS.md（不受压缩影响），并在 `/compact` 时附带自定义指令保留重要信息。

### 在非交互模式下使用需要 UI 的 Slash 命令

Pi 的部分 Slash 命令（如 `/settings`、`/tree`、`/hotkeys`）依赖 TUI 渲染器来显示交互式界面。在 Print 模式或 RPC 模式下执行这些命令会失败或产生无意义的输出。例如 `pi -p "/settings"` 不会打开设置界面，而是把 `/settings` 当作普通 prompt 发送给 LLM。

使用命令前确认当前的运行模式。Print 模式下需要修改配置，直接编辑 `~/.pi/agent/settings.json` 文件而非通过 Slash 命令。RPC 模式下通过 JSONL 协议的 `get_state` 请求获取状态信息。

## 适用场景与限制

### RPC 模式的 JSONL 协议只支持同步请求-响应

Pi 的 RPC 模式通过 stdin/stdout 的 JSONL 帧通信，每个请求对应一个响应。这种同步模式意味着在等待 Agent 响应期间，客户端无法发送其他请求或接收中间状态更新。对于需要并发处理多个请求或实时流式输出的场景，RPC 模式的限制比较明显。

如果需要并发处理，可以在 RPC 服务器端为每个请求创建独立 Session 并行处理。如果需要流式输出，考虑使用 JSON Event Stream 模式（`pi --mode json`），它支持逐行输出事件流，延迟比 RPC 模式的完整响应更低。

### 消息队列的交付策略可能不符合预期

Pi 的编辑器支持 Steering（Enter）和 Follow-up（Alt+Enter）两种消息交付策略。Steering 消息在当前工具调用完成后交付，Follow-up 消息在 Agent 全部工作完成后交付。但如果你不清楚两者的区别，可能在错误的时机发送消息——例如在 Agent 执行 Bash 命令时用 Enter 发送了 Steering 消息，期望它等 Agent 完成全部工作，实际上消息会在当前命令完成后立即被消费。

理解两种交付策略的行为差异，并在 `/settings` 中根据工作流习惯配置默认策略。对于需要严格顺序执行的场景，使用 `one-at-a-time` 模式（默认）；对于可以并行处理的场景，使用 `all` 模式批量交付。

### JSON 模式的事件类型有限

`pi --mode json` 输出的事件类型包括 `assistant`、`tool_call`、`error`、`done` 等基础类型，但不包含完整的 25+ 生命周期事件（如 `turn_start`、`tool_execution_start` 等）。如果你的监控系统需要更细粒度的可观测性（比如追踪每个工具的执行耗时），JSON 模式提供的信息不够充分。

对于需要完整事件流的场景，使用 SDK 模式（`session.on()` 监听所有事件），或者使用 RPC 模式配合自定义的事件收集 Extension。JSON 模式适合轻量级的脚本集成，不适合深度的运行时监控。

## 常见失败与陷阱

### /fork 创建的 Session 分支在进程退出后可能丢失

`/fork` 从当前对话创建新的 Session 文件，但这个操作依赖本地文件系统。如果你在 fork 后立即退出 Pi（`/quit`），且 Pi 在退出时的清理逻辑尚未完成 Session 文件的写入，新创建的分支可能不完整。

使用 `/fork` 后等待几秒钟确认 Session 文件已写入，或者在退出前用 `/export` 手动导出当前 Session。对于需要可靠保存的对话，定期用 `/export` 备份到指定路径，而非仅依赖 Pi 的自动保存机制。

### /trust 的信任决策在非交互模式下不生效

Pi 的 Project Trust 机制在交互模式下会弹出确认对话框，但在 Print 模式或 RPC 模式下没有交互能力。如果 `defaultProjectTrust` 设置为 `"ask"`（默认值），非交互模式下项目级 Extension 和 Skills 不会被加载，Agent 可能缺少必要的工具。

在非交互模式使用前，先在交互模式中用 `/trust` 信任项目，或者通过 `--approve` 标志一次性覆盖信任设置。在 CI/CD 环境中，显式设置 `defaultProjectTrust: "always"` 或使用 `-a` 标志确保项目资源被加载。

### Esc 两次打开 Session Tree 的时机容易误触

在交互模式中，按一次 Esc 取消当前操作，按两次 Esc 打开 Session Tree 导航。但用户在快速按 Esc 试图取消工具执行时，可能因为按了两次而意外打开 Session Tree，打断了工作流。特别是在 Agent 正在执行长时间任务时，误触 Session Tree 会暂停当前操作。

了解 Esc 的单击和双击行为差异。如果只是想取消当前操作，按一次 Esc 然后等待。如果想彻底停止 Agent，使用 Ctrl+C。自定义快捷键（编辑 `~/.pi/agent/keybindings.json`）可以将 Session Tree 绑定到其他不常用的按键组合。
