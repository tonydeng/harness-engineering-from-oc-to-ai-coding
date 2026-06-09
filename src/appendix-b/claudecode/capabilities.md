# Claude Code 内置能力

Claude Code 是 Anthropic 官方推出的终端 AI 编程工具，深度集成 Claude 模型，提供简洁的命令行交互体验。本章梳理 Claude Code 的内置能力，作为与 OpenCode 对比的参考。

## 概述

Claude Code 的核心定位：**Claude 模型的终端原生界面**。它专注于与 Claude 模型的深度集成，提供简洁、高效的编码体验。

Claude Code 的核心能力包括：

- **深度 Claude 集成**：直接对接 Claude 模型，支持最新模型切换
- **项目指令系统**：通过 CLAUDE.md 定义项目级行为规范
- **权限控制**：细粒度的工具调用权限管理
- **终端集成**：Vim 模式、终端设置等开发者友好功能
- **成本追踪**：实时查看 Token 使用统计

## 内置命令

Claude Code 的命令以 `/` 开头，在对话中直接输入。

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
| `/vim` | 切换 Vim 编辑模式 |

### 命令使用示例

```
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

Claude Code 支持两种基本模式，通过切换控制 AI 的操作范围。

### Plan Mode（只读分析）

只读模式，AI 只能读取文件和搜索代码，不能修改文件或执行命令。适合在动手之前先做分析和规划。

### Code Mode（默认）

读写模式，AI 可以读取、写入、编辑文件，执行命令。这是默认的工作模式。

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

```
.claude/
  settings.json    # 项目设置
  commands/        # 自定义命令
```

### 权限配置

Claude Code 对工具调用有细粒度的权限控制。每次调用 Bash、Write 等敏感工具时，会提示用户确认。可以通过配置文件预设权限规则，减少重复确认。

权限配置示例：

```json
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
| 扩展机制 | Plugin + Skill + MCP + 自定义 Agent | CLAUDE.md + 自定义命令 |
| 工具链 | 完整（AST-grep、LSP、CodeGraph 等） | 基础（文件、命令、搜索） |
| Hook 系统 | 20+ Hook Points，事件驱动 | 无 |
| 成本控制 | 内置 Token 追踪 | `/cost` 命令查看 |
| 会话管理 | 压缩、导出、分享、撤销 | 压缩、清除 |
| 开源状态 | 开源 | 闭源 |

→ [OpenCode 内置能力](opencode-capabilities.md) 有 OpenCode 各项能力的详细说明。
→ [核心概念](../02-core-concepts/) 章节对两者的设计哲学有更深入的对比。
