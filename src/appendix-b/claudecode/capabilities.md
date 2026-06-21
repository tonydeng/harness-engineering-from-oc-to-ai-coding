# Claude Code 内置能力

Claude Code 是 Anthropic 官方推出的终端 AI 编程工具，深度集成 Claude 模型。本章作为 Claude Code 的**能力索引**，指向各详细参考文件。

## 能力一览

Claude Code 的核心能力可以按以下维度组织：

| 维度 | 简介 | 详细参考 |
|------|------|----------|
| **内置命令** | `/init`、`/compact`、`/cost`、`/doctor` 等 15+ 个斜杠命令 | [命令参考](./commands.md) |
| **文件工具** | Read（文本+PDF）、Write、Edit（精确替换） | —（见下方工具集） |
| **执行工具** | Bash（命令执行，支持超时） | — |
| **搜索工具** | Grep（正则）、Glob（文件模式） | — |
| **网络工具** | WebFetch（URL 抓取） | — |
| **Agent 模式** | Plan Mode（只读分析）、Code Mode（默认读写） | —（见下方 Agent 模式） |
| **项目指令** | CLAUDE.md 多级配置（全局/项目/目录） | [扩展机制参考](./extensions.md) |
| **自定义命令** | `.claude/commands/*.md` 自动注册为 `/` 命令 | [扩展机制参考](./extensions.md) |
| **MCP Server** | 通过 JSON-RPC 接入外部工具和数据源 | [扩展机制参考](./extensions.md) |
| **权限控制** | 细粒度工具调用权限管理 | [扩展机制参考](./extensions.md) |
| **成本追踪** | `/cost` 查看 Token 使用统计 | [命令参考](./commands.md) |
| **生态与社区** | Anthropic 生态、MCP 协议、社区资源 | [生态参考](./ecosystem.md) |

### 工具集速览

Claude Code 内置工具集聚焦核心编码场景：**Read**（支持 PDF）、**Write**（覆盖写入）、**Edit**（oldString/newString 精确匹配替换）、**Bash**（Shell 执行）、**Grep**（正则搜索）、**Glob**（文件名匹配）、**WebFetch**（URL 抓取）。

### Agent 模式

- **Plan Mode**：只读分析，不能修改文件或执行命令。适合在动手前先做规划。
- **Code Mode（默认）**：读写模式，可以读取、写入、编辑文件，执行命令。

## 与 OpenCode 的能力对比

| 维度 | OpenCode | Claude Code |
|------|----------|-------------|
| 模型支持 | 多模型（Claude、GPT、Gemini、本地模型） | 仅 Claude 模型 |
| 扩展机制 | Plugin + Skill + MCP + 自定义 Agent | CLAUDE.md + 自定义命令 + MCP |
| 工具链 | 完整（AST-grep、LSP、CodeGraph 等） | 基础（文件、命令、搜索） |
| Hook 系统 | 20+ Hook Points，事件驱动 | 无 |
| 成本控制 | 内置 Token 追踪 | `/cost` 命令查看 |
| 会话管理 | 压缩、导出、分享、撤销 | 压缩、清除 |
| 开源状态 | 开源 | 闭源 |

## 使用建议

### 选择 Claude Code 还是 OpenCode

两个工具的适用场景有明显重叠，但也各有侧重。如果你的团队已经全面使用 Claude 模型，且项目不需要复杂的 Agent 编排，Claude Code 的简洁性是一个优势。它上手快、配置少、没有 Plugin/Skill 的认知负担。

如果你需要多模型灵活切换、自定义 Agent 行为、或团队共享工作流，OpenCode 的扩展体系更适合。OpenCode 的 Plugin 和 Skill 系统让你可以把最佳实践编码化，在团队内复制和演进。

### CLAUDE.md 写作建议

写好 CLAUDE.md 的关键：**具体、可执行、有边界**。避免空泛的描述，给出明确的规则。推荐的 CLAUDE.md 结构：

1. **项目简介**：一两句话说清楚这是什么项目
2. **技术栈**：语言、框架、包管理器
3. **代码规范**：命名约定、格式化规则、禁止的写法
4. **常用命令**：构建、测试、lint 的具体命令
5. **约束条件**：不能修改的文件、不能执行的操作

### 权限配置建议

Claude Code 的权限提示虽然安全，但频繁弹出会打断工作流。建议在项目早期就把常用的构建、测试命令加入白名单，把危险操作（如 `rm -rf`）加入黑名单。既保证安全，又减少干扰。

> → [命令参考](./commands.md) — Claude Code 全部命令的详细用法
> → [扩展机制参考](./extensions.md) — 六层扩展体系完整参考（CLAUDE.md、Skills、MCP、Subagent、Hook、Plugin）
> → [生态参考](./ecosystem.md) — 社区生态和最佳实践
> → [Agent 设计指南](./agent-architecture.md) — 自定义 Agent 与 Subagent 的从入门到生产完整教程
> → [Agent SDK 编程参考](./agent-sdk.md) — 通过 `@anthropic-ai/claude-agent-sdk` 编程式驱动 Agent
> → [OpenCode 内置能力](../opencode/capabilities.md) — 对应功能的对比参考
> → [核心概念](../02-core-concepts/) — 设计哲学深入对比
