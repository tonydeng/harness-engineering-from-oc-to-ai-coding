# OpenCode 内置能力

OpenCode 是一个终端原生的 AI 编程助手，支持多种 LLM Provider，内置丰富的命令、工具和扩展机制。本章完整梳理 OpenCode 的核心能力，供日常使用和自定义扩展时速查。

## 概述

OpenCode 的核心设计哲学：**让 AI 在你的终端里干活，而不是替你干活**。它不是一个黑盒 IDE 插件，而是一个透明的协作环境。你能看到 AI 的每一步操作，随时介入，随时纠正。

OpenCode 的核心能力包括：

- **多模型支持**：通过 Provider 系统接入 Claude、GPT、Gemini、本地模型等任意 LLM
- **内置工具链**：文件读写、命令执行、代码搜索、网络请求、AST 分析、LSP 集成，开箱即用
- **Plugin 系统**：20+ Hook Points，支持在工具调用前后注入自定义逻辑
- **Agent 架构**：Build、Plan、Explore 等多种 Agent 类型，各有分工
- **Skill 系统**：可安装、可分享的专家级指令集，扩展 AI 的领域知识
- **会话管理**：压缩、导出、分享、撤销，完整的会话生命周期

## 内置命令

OpenCode 的命令以 `/` 开头，在输入框中直接输入即可执行。

### 核心命令

| 命令 | 别名 | 功能 |
|------|------|------|
| `/init` | | 生成 AGENTS.md 项目知识库 |
| `/help` | | 显示帮助信息 |
| `/new` | `/clear` | 新建会话，清空当前上下文 |
| `/sessions` | `/resume`, `/continue` | 列出历史会话，切换或恢复 |
| `/compact` | `/summarize` | 压缩上下文，减少 Token 消耗 |
| `/export` | | 导出当前会话为 Markdown 文件 |
| `/share` | | 生成会话分享链接 |
| `/undo` | | 撤销上一步 AI 操作 |
| `/redo` | | 重做被撤销的操作 |
| `/models` | | 列出可用模型，切换当前模型 |
| `/connect` | | 添加新的 LLM Provider |
| `/themes` | | 切换界面主题 |
| `/editor` | | 打开系统默认编辑器 |
| `/details` | | 显示最近一次工具调用的详细信息 |
| `/thinking` | | 切换推理过程（Thinking）的显示 |
| `/exit` | | 退出 OpenCode |

### OMO 扩展命令

这些命令来自 oh-my-openagent 增强层，在标准 OpenCode 基础上提供更高级的工作流控制。

| 命令 | 功能 |
|------|------|
| `/ralph-loop` | 启动自引用开发循环，持续执行直到完成 |
| `/ulw-loop` | 启动 Ultrawork 模式循环 |
| `/cancel-ralph` | 取消当前活跃的 Loop |
| `/refactor` | 智能重构：LSP 分析 + AST-grep 替换 + 架构检查 |
| `/remove-ai-slops` | 移除 AI 生成的代码异味（10 类 slop 清洗） |
| `/start-work` | 从 Prometheus 计划开始执行实现任务 |
| `/hyperplan` | 对抗性多 Agent 规划：5 个 Agent 互相批评，Lead 综合 |
| `/handoff` | 创建详细的上下文摘要，便于在新会话中继续工作 |
| `/stop-continuation` | 停止所有续接机制（ralph loop、todo continuation、boulder） |

### 命令使用示例

 

```bash:terminal
/init                          # 首次进入项目时运行，生成 AGENTS.md
/compact                       # 上下文过长时压缩
/undo                          # AI 改错了文件，立刻撤销
/models                        # 从 Claude 切换到 GPT
/refactor                      # 选中一段代码，智能重构
```

## Plugin 系统

Plugin 是 OpenCode 的核心扩展机制。它不是简单的脚本注入，而是一套完整的事件驱动框架，能在工具调用的生命周期中插入自定义逻辑。

### 什么是 Plugin

Plugin 是一个声明式的配置文件（通常是 JSON 或 YAML），定义了一组 Hook Point 和对应的处理器。当 OpenCode 执行工具调用时，会按顺序触发相应的 Hook，Plugin 在这些 Hook 中注入自己的行为。

### Plugin vs Skill vs MCP

这三个概念容易混淆，核心区别在于**作用时机**和**作用范围**：

| 维度 | Plugin | Skill | MCP |
|------|--------|-------|-----|
| 作用时机 | 工具调用前后（事件驱动） | 对话开始时（指令注入） | 工具调用时（外部服务） |
| 作用范围 | 全局，影响所有工具调用 | 单次对话，影响 AI 行为 | 单个工具，提供新能力 |
| 配置位置 | `.opencode/plugins/` | `.opencode/skills/` | `opencode.json` 的 mcp 字段 |
| 典型用途 | 自动化检查、权限控制、审计 | 专家级工作流、领域知识 | 数据库查询、API 调用 |

### Hook Points

OpenCode 提供 20+ 个 Hook Points，覆盖工具调用的完整生命周期：

**工具调用前（Pre-Hook）**

- `pre-tool-call` — 工具调用前触发，可修改参数或阻止调用
- `pre-file-write` — 文件写入前触发，可做格式化、lint 检查
- `pre-bash-exec` — 命令执行前触发，可做安全检查、参数注入

**工具调用后（Post-Hook）**

- `post-tool-call` — 工具调用后触发，可做结果验证
- `post-file-write` — 文件写入后触发，可做自动格式化、git add
- `post-bash-exec` — 命令执行后触发，可做输出解析、告警

**会话级 Hook**

- `session-start` — 会话开始时触发
- `session-end` — 会话结束时触发
- `context-change` — 上下文窗口变化时触发

**Agent 级 Hook**

- `agent-switch` — Agent 切换时触发
- `model-change` — 模型切换时触发

### Plugin 配置

Plugin 配置文件放在 `.opencode/plugins/` 目录下，格式如下：

```json:examples/opencode/plugin-config.json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "hooks": {
    "pre-file-write": {
      "handler": "format-check",
      "options": {
        "formatter": "prettier",
        "extensions": [".ts", ".tsx", ".js"]
      }
    },
    "post-bash-exec": {
      "handler": "alert-on-error",
      "options": {
        "notify": true,
        "log-level": "error"
      }
    }
  }
}
```

### Plugin 管理

OpenCode 提供内置的 Plugin 管理能力：

- 安装：将 Plugin 文件放入 `.opencode/plugins/` 目录
- 禁用：在 Plugin 配置中设置 `"enabled": false`
- 卸载：删除对应的 Plugin 文件

## 工具集

OpenCode 内置了一套完整的工具集，AI Agent 可以直接调用这些工具来完成任务。你不需要手动执行这些操作，但了解它们有助于理解 AI 在做什么。

### 文件操作

| 工具 | 功能 | 说明 |
|------|------|------|
| Read | 读取文件内容 | 支持偏移量和行数限制，大文件分段读取 |
| Write | 写入文件 | 覆盖写入，需要先 Read 过该文件 |
| Edit | 精确文本替换 | 基于 oldString/newString 匹配，支持replaceAll |
| Glob | 文件模式匹配 | 按 glob 模式搜索文件名 |

### 命令执行

| 工具 | 功能 | 说明 |
|------|------|------|
| Bash | 执行 shell 命令 | 持久化 shell 会话，支持超时设置 |

### 搜索

| 工具 | 功能 | 说明 |
|------|------|------|
| Grep | 正则内容搜索 | 按正则表达式搜索文件内容，支持结果模式切换 |
| AST-grep | 代码结构搜索 | 25 种语言支持，基于 AST 模式匹配（非正则） |

### 网络

| 工具 | 功能 | 说明 |
|------|------|------|
| WebSearch | 网络搜索 | 通过 Exa 搜索引擎获取清洁内容 |
| WebFetch | URL 抓取 | 获取网页内容，支持 Markdown/Text/HTML 格式 |
| GitHub Search | GitHub 代码搜索 | 从百万开源仓库中搜索真实代码示例 |

### 代码分析

| 工具 | 功能 | 说明 |
|------|------|------|
| LSP Diagnostics | 获取诊断信息 | 错误、警告、提示 |
| LSP Goto Definition | 跳转到定义 | 符号定义位置 |
| LSP Find References | 查找引用 | 符号的所有引用位置 |
| LSP Rename | 重命名符号 | 跨工作区重命名 |
| LSP Symbols | 文档/工作区符号 | 大纲视图和全局搜索 |
| CodeGraph | 代码图谱 | 调用链分析、影响范围、上下文构建 |

### 任务管理

| 工具 | 功能 | 说明 |
|------|------|------|
| Task | 后台任务调度 | 并行执行子任务，支持后台运行 |
| Todo | 待办事项管理 | 结构化任务追踪，原子化分解 |

## Agent 类型

OpenCode 采用多 Agent 架构，不同 Agent 擅长不同的任务。

### Build Agent（默认）

全能型 Agent，具备完整的工具链权限。文件读写、命令执行、代码搜索、网络请求，全部开放。适合大多数开发任务。

### Plan Agent（只读分析）

只读 Agent，不能修改文件或执行命令。专注于分析代码结构、理解架构、制定计划。适合在动手之前先做调研。

### General Agent

通用 Agent，权限和能力介于 Build 和 Plan 之间。适合不需要完整 Build 权限的场景。

### Explore Agent

探索型 Agent，专门用于代码库探索。擅长搜索、分析、总结，不执行修改操作。适合快速了解陌生代码库。

### Scout Agent

侦察型 Agent，轻量级探索工具。适合快速搜索和信息收集，不涉及深度分析。

## 自定义扩展

OpenCode 的扩展能力覆盖四个层面，从简单到复杂依次是：

### 自定义 Skill

最轻量的扩展方式。一个 SKILL.md 文件就是一个 Skill，定义 AI 的行为指令。适合封装领域知识、工作流规范。

→ [Skill 开发](../05-skills/) 章节有完整的开发指南。

### 自定义 Command

自定义 `/` 命令。在 `.opencode/commands/` 目录下创建 Markdown 文件，文件名即命令名。适合封装常用操作序列。

### 自定义 Plugin

事件驱动的扩展。在 `.opencode/plugins/` 目录下创建配置文件，定义 Hook 和处理器。适合需要在工具调用前后注入逻辑的场景。

### 自定义 Agent

最高级别的扩展。在 `.opencode/agents/` 目录下创建 Agent 配置，定义独立的 Agent 类型。适合需要全新行为模式的场景。

→ [高级配置](../06-advanced/) 章节有更多自定义扩展的实战案例。
