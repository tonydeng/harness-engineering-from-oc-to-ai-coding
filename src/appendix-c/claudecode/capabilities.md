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

| 命令 | 功能 |
|------|------|
| `/init` | 初始化项目，生成 CLAUDE.md 文件 |
| `/clear` | 清除当前对话上下文 |
| `/compact` | 压缩上下文，减少 Token 消耗 |
| `/cost` | 显示当前会话的 Token 使用统计 |
| `/doctor` | 诊断环境问题，检查配置完整性 |
| `/help` | 显示帮助信息 |
| `/login` | 登录 Anthropic 账户 |
| `/logout` | 登出当前账户 |
| `/memory` | 编辑 CLAUDE.md 记忆文件 |
| `/model` | 切换当前使用的模型 |
| `/permissions` | 查看和管理工具调用权限 |
| `/review` | 对代码变更进行审查 |
| `/status` | 显示当前状态信息 |
| `/terminal-setup` | 设置终端集成（Shell 集成、快捷键等） |


→ 完整命令列表和详细用法见 [commands.md](./commands.md)。

### 命令使用示例

 

```bash:terminal
/init                          # 首次进入项目时初始化
/compact                       # 上下文过长时压缩
/cost                          # 查看消耗了多少 Token
/doctor                        # 遇到问题时诊断环境
/model claude-sonnet-4-20250514   # 切换到 Sonnet 模型
```

## 工具集

Claude Code 内置的工具集相对精简，聚焦于核心编码场景。

### 文件操作

| 工具 | 功能 | 说明 |
|------|------|------|
| Read | 读取文件内容 | 支持文本和 PDF |
| Write | 写入文件 | 覆盖写入 |
| Edit | 精确文本替换 | 基于 oldString/newString 匹配 |

### 命令执行

| 工具 | 功能 | 说明 |
|------|------|------|
| Bash | 执行 shell 命令 | 支持超时设置 |

### 搜索

| 工具 | 功能 | 说明 |
|------|------|------|
| Grep | 正则内容搜索 | 按正则表达式搜索文件内容 |
| Glob | 文件模式匹配 | 按 glob 模式搜索文件名 |

### 网络

| 工具 | 功能 | 说明 |
|------|------|------|
| WebFetch | URL 抓取 | 获取网页内容 |

## Agent 模式

Claude Code 支持 6 种权限模式，通过切换控制 AI 的操作范围。

### 6 种权限模式

| 模式 | 说明 |
|------|------|
| **default** | 每次执行敏感操作前询问用户确认 |
| **acceptEdits** | 自动接受文件编辑（Write/Edit），执行命令时询问 |
| **plan** | 只读分析，不能修改文件或执行命令。适合动手前先规划 |
| **auto** | 自动批准所有操作，无交互确认 |
| **dontAsk** | 不主动询问，静默拒绝权限外的操作 |
| **bypassPermissions** | 绕过所有权限检查，完全信任 Agent |

通过 `--permission-mode` 标志或 `/permissions` 命令切换。

## 自定义配置

Claude Code 的自定义主要通过文件配置实现。

### CLAUDE.md 项目指令

CLAUDE.md 是 Claude Code 的项目级指令文件，放在项目根目录。它告诉 Claude 在这个项目中应该怎么工作，类似 OpenCode 的 AGENTS.md。

CLAUDE.md 通常包含：

- 项目简介和技术栈说明
- 代码风格和命名规范
- 测试和构建命令
- 常用路径和模块说明
- 不能做的事（约束条件）

Claude Code 支持多级 CLAUDE.md：

- `~/.claude/CLAUDE.md` — 全局配置，所有项目生效
- `项目根目录/CLAUDE.md` — 项目级配置
- `子目录/CLAUDE.md` — 目录级配置，进入该目录时加载

### .claude/ 目录结构

Claude Code 使用 `.claude/` 目录管理项目配置：

```text:terminal
.claude/
  settings.json    # 项目设置
  commands/        # 自定义命令
```

### 权限配置

Claude Code 对工具调用有细粒度的权限控制。每次调用 Bash、Write 等敏感工具时，会提示用户确认。可以通过配置文件预设权限规则，减少重复确认。

权限配置示例：

```json:examples/claudecode/permissions.json
{
  "permissions": {
    "allow": [
      "Bash(npm test)",
      "Bash(npm run build)",
      "Write(src/**)"
    ],
    "deny": [
      "Bash(rm -rf *)",
      "Write(.env*)"
    ]
  }
}
```

## 与 OpenCode 的主要差异

了解两者的能力差异，有助于选择合适的工具。

| 维度 | OpenCode | Claude Code |
|------|----------|-------------|
| 模型支持 | 多模型（Claude、GPT、Gemini、本地模型） | 仅 Claude 模型 |
| 扩展机制 | Plugin + Skill + MCP + 自定义 Agent | CLAUDE.md + Skills + MCP + Subagents + Hooks + Plugins 六层 |
| 工具链 | 完整（AST-grep、LSP、CodeGraph 等） | 基础（文件、命令、搜索） |
| Hook 系统 | 20+ Hook Points，事件驱动 | 无 |
| 成本控制 | 内置 Token 追踪 | `/cost` 命令查看 |
| 会话管理 | 压缩、导出、分享、撤销 | 压缩、清除 |
| 开源状态 | 开源 | 闭源 |

## 扩展机制

Claude Code 的扩展方式相对收敛，主要依赖配置文件和外部协议。

### CLAUDE.md 自定义指令

CLAUDE.md 是最核心的扩展手段。通过编写结构化的指令，你可以改变 Claude 在项目中的行为，无需编写任何代码。多级 CLAUDE.md 支持全局、项目、目录三个层次的配置叠加。

### 自定义命令

在 `.claude/commands/` 目录下放置 Markdown 文件，每个文件自动注册为一个 `/` 命令。文件名即命令名，文件内容作为发送给 Claude 的 Prompt。这相当于一种轻量级的 Skill 机制，适合封装重复性的项目操作。

```text:terminal
.claude/commands/
  review.md       # → /review 命令
  fix-lint.md     # → /fix-lint 命令
  deploy.md       # → /deploy 命令
```

### MCP Server 连接

Claude Code 支持连接外部 MCP Server，通过 `.claude/settings.json` 配置。MCP 为 Claude Code 提供了接入外部工具和数据源的能力，比如数据库查询、API 调用、文件系统操作等。

### 扩展方式对比

| 扩展方式 | 实现形式 | 灵活度 | 适用场景 |
|----------|----------|--------|----------|
| CLAUDE.md 指令 | Markdown 文本 | 低 | 行为规范、编码约束 |
| Skills | SKILL.md + YAML frontmatter | 低 | 可复用指令集 |
| MCP Server | 外部进程 JSON-RPC | 高 | 外部工具、数据源接入 |
| Subagents | Markdown + YAML frontmatter | 中 | 隔离上下文的子任务代理 |
| Hooks | JSON + Shell / LLM / Agent | 中高 | 生命周期事件自动化 |
| Plugins | plugin.json 清单打包 | 高 | 分发以上所有组件 |

与 OpenCode 的扩展体系相比，Claude Code 没有 Plugin 层（无法在 Agent 进程内注入运行时逻辑），也没有 Skill 市场（无法从社区安装可复用的指令包）。扩展能力集中在"指令配置 + 外部协议"两个维度。

→ 扩展体系详解见 [plugins.md](./plugins.md)，涵盖 CLAUDE.md、Skills、MCP、Subagent、Hook、Plugin 六层架构。
→ [Plugin 系统](../opencode/plugins.md) 详细介绍了 OpenCode 的 Plugin/Skill/MCP 三层扩展架构。

## 生态与社区

### Anthropic 生态

Claude Code 的生态紧密围绕 Anthropic 的产品体系：

- **Anthropic Console**：统一管理 API Key、用量监控、账单
- **Claude 模型家族**：Sonnet（性价比）、Opus（最强能力）、Haiku（最快速度）
- **Model Context Protocol**：Anthropic 主导的开放协议，用于标准化 AI 工具与外部系统的连接

MCP 是 Claude Code 生态中最有价值的部分。通过 MCP，Claude Code 可以连接数据库、版本控制、CI/CD 流水线、项目管理工具等。Anthropic 维护了一份 MCP Server 参考实现列表，社区也贡献了大量 Server 实现。

### 社区资源

Anthropic 官方提供了完整的 Claude Code 使用指南。GitHub 上有多个展示 CLAUDE.md 最佳实践的参考项目，开发者也在论坛和社交媒体上分享配置方案和使用技巧。

### 生态对比

| 生态维度 | Claude Code | OpenCode |
|----------|-------------|----------|
| 模型生态 | 仅 Claude 模型族 | Claude/GPT/Gemini/本地模型等 10+ Provider |
| 工具扩展 | MCP Server（JSON-RPC） | MCP + Plugin + Skill + 自定义 Tool |
| 社区资产 | CLAUDE.md 模板、MCP Server 实现 | Skill 市场、Plugin 仓库、oh-my-openagent 社区 |
| 协议标准 | MCP（Anthropic 主导） | MCP（完全兼容） + 原生 Plugin API |
| 扩展粒度 | 指令级 + 外部工具级 | 代码级（Hook）+ 指令级 + 工具级 |

Claude Code 的生态优势在于 Anthropic 的品牌背书和 MCP 协议的标准化推广。OpenCode 的生态优势在于多模型支持和更丰富的扩展层次（Plugin 可以拦截任意 Agent 行为）。

→ [MCP 服务器](../06-advanced/mcp-servers.md) 详细讲解了 MCP 协议在 OpenCode 中的配置和实践。

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
