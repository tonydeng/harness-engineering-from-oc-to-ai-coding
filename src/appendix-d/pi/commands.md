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

在 Agent 工作时可以排队提交消息：

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
| `/reload` | 重新加载快捷键、扩展、Skills、Prompts 和 Context Files |
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
