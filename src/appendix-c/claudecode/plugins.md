# Claude Code 扩展机制参考

> Claude Code 没有类似 OpenCode `definePlugin` 的 **Plugin（插件）** API。它的"扩展"概念通过六个层次实现，从声明式配置到可打包分发的完整组件，复杂度逐层递增。

Claude Code 的扩展体系包含六个层次：**CLAUDE.md**（项目规则）→ **Skills**（可复用指令集）→ **MCP 服务器**（外部工具连接）→ **Subagents**（子任务代理）→ **Hooks**（生命周期事件）→ **Plugins**（打包分发）。所有层次均基于配置文件（Markdown / JSON / Shell 脚本），无需编译构建。

→ [Claude Code 内置能力](./capabilities.md) 提供了全貌概览。
→ [Claude Code 命令参考](./commands.md) 列出了所有内置命令和捆绑 **Skill（技能）**。

---

## 扩展体系总览

| 层次 | 本质 | 配置格式 | 执行位置 | 复杂度 |
|------|------|----------|----------|--------|
| CLAUDE.md | 项目规则与记忆 | Markdown | **Agent（智能体）** 上下文 | 低 |
| Skills | 可复用指令集 | SKILL.md + YAML frontmatter | **Prompt（提示词）** 注入 / 子 Agent | 低 |
| **MCP（模型上下文协议）** 服务器 | 外部工具连接 | JSON + 外部进程 | 独立进程 | 中 |
| Subagents | 专用子 Agent | Markdown + YAML frontmatter | 独立上下文窗口 | 中 |
| Hooks | 生命周期事件 | JSON + Shell / LLM / Agent | 事件触发时执行 | 中高 |
| Plugins | 打包分发 | plugin.json 清单 | 整合以上所有组件 | 高 |

> **OpenCode 对比**：OpenCode 的扩展体系是 Plugin（代码级 Hook）→ Skill（指令级）→ MCP（工具级）三层架构，核心扩展点是 TypeScript `definePlugin` API。Claude Code 的扩展全部通过配置文件（JSON / Markdown / Shell 脚本）和外部进程（MCP 服务器）实现，没有 TypeScript 函数回调级别的代码扩展 API（如 OpenCode 的 `definePlugin`）。

---

## CLAUDE.md — 项目规则与记忆

CLAUDE.md 是 Claude Code 最基础也最重要的扩展方式。它包含项目规范、构建命令、编码约定等信息，写入 Agent 的 System Prompt。

### 文件层级

| 优先级 | 位置 | 作用域 | 共享方式 |
|--------|------|--------|----------|
| 1（最高） | 系统目录配置 | 组织全员 | IT 部署（只读）|
| 2 | `~/.claude/CLAUDE.md` | 所有项目 | 个人 |
| 3 | `./CLAUDE.md` 或 `./.claude/CLAUDE.md` | 当前仓库 | 团队（提交到 Git）|
| 4 | `./CLAUDE.local.md` | 当前仓库（个人） | 个人（加入 `.gitignore`）|
| 5 | 父目录向上遍历 | Monorepo 场景 | 自动发现 |
| 6 | 子目录 CLAUDE.md | 特定目录 | 按需加载 |

### 写作原则

**应当包含（✅）：**
- 构建和测试命令（最高 ROI 的配置）
- 与默认不同的代码风格规则
- 项目特定的架构决策
- 环境变量和开发环境要求
- 常见陷阱和非显而易见的行为

**不应包含（❌）：**
- Claude 读代码就能推断的内容
- 标准语言约定（Claude 已经知道）
- 详细的 API 文档（改为链接引用）
- 逐文件的代码库描述

### 关键实践

| 实践 | 说明 |
|------|------|
| **控制在 200 行以内** | 过长文件因 "lost in the middle" 效应导致遵循率下降 |
| **测试/构建命令置顶** | 每次会话都需要，放在文件最前面 |
| **删除 linter 已覆盖的规则** | 重复配置浪费上下文空间 |
| **提交到 Git** | 团队成员获得一致的 Agent 行为 |
| **@import 模块化** | 大项目拆分为多个文件，递归深度最多 5 层 |
| **使用 `.claude/rules/` 拆分** | 按路径条件加载的模块化规则文件 |

> **对比 OpenCode**：OpenCode 使用 AGENTS.md，单文件 + 项目级，不支持多级继承和子目录自动发现。

---

## Skills — 可复用指令集

Skills 是 Claude Code 中封装可复用 AI 行为的单位。一个 Skill 就是一个包含 SKILL.md 的目录，支持 YAML frontmatter 声明触发条件、工具权限和执行模式。

### 核心格式

```yaml:.claude/skills/my-skill/SKILL.md
---
name: my-skill
description: 这个 Skill 做什么以及何时使用
allowed-tools: Read Grep Bash
disallowed-tools: Write Edit
context: fork
agent: Explore
---

# 指令内容

这里是 Skill 的核心指令...
```

### 三级加载设计

| 层级 | 内容 | 何时加载 |
|------|------|----------|
| 1. YAML frontmatter | 触发条件、元信息、工具权限 | 始终加载 |
| 2. SKILL.md body | 完整指令 | Claude 决定需要时加载 |
| 3. 引用的辅助文件 | reference.md、scripts/ | Agent 需要时才读取 |

### Frontmatter 关键字段

| 字段 | 必需 | 说明 |
|------|------|------|
| `name` | ✅ | 显示名称，不决定命令名（目录名决定）|
| `description` | ✅ | 描述，Claude 用来判断何时自动激活 |
| `allowed-tools` | ❌ | Skill 激活时自动授权的工具白名单 |
| `disallowed-tools` | ❌ | Skill 激活时禁用的工具黑名单 |
| `context: fork` | ❌ | 在隔离的子 Agent 中运行 |
| `user-invocable` | ❌ | `false` 时仅 Claude 可调用 |
| `disable-model-invocation` | ❌ | `true` 时仅用户可调用 |
| `agent` | ❌ | 指定执行的 Agent 类型 |
| `model` | ❌ | 覆盖当前会话模型 |
| `effort` | ❌ | 覆盖努力级别 |
| `paths` | ❌ | glob 模式限定仅在匹配文件时激活 |

### 存储位置

| 位置 | 路径 | 适用范围 |
|------|------|----------|
| 个人 | `~/.claude/skills/<name>/SKILL.md` | 个人所有项目 |
| 项目 | `.claude/skills/<name>/SKILL.md` | 当前项目（提交到 Git）|
| 插件捆绑 | `<plugin>/skills/<name>/SKILL.md` | 插件启用时 |

### 动态上下文注入

```
---
description: 总结未提交的变更
---

## 当前变更
!`git diff HEAD`

## 指令
总结上述变更...
```

`` `!`command` `` 语法在 Claude 看到内容前执行 Shell 命令，输出替换占位符。适合注入实时数据。

### 与 OpenCode 对比

| 维度 | Claude Code Skills | OpenCode Skills |
|------|-------------------|-----------------|
| 格式 | SKILL.md + YAML frontmatter | SKILL.md（类似）|
| 自动发现 | ✅ 按 description 自动激活 | ✅ 按触发词匹配 |
| 隔离执行 | `context: fork` | Skill Agent |
| 动态注入 | `!`command`` 语法 | Shell 集成 |

> → 自定义命令（`.claude/commands/*.md`）与 Skills 已统一。两者都会创建 `/command-name`，同名时 Skills 优先。

---

## MCP 服务器 — 外部工具连接

MCP（Model **Context（上下文）** Protocol）是 Claude Code 连接外部世界的标准化协议。通过 MCP，Agent 可以查询数据库、调用 API、搜索网络，而不需要把能力硬编码到工具链里。

### 配置位置

| 位置 | 文件 | 作用域 |
|------|------|--------|
| 项目级 | `.mcp.json` | 当前项目（提交到 Git）|
| 用户级 | `~/.claude.json` | 所有项目 |
| 插件内 | `<plugin>/.mcp.json` | 插件作用域 |

### 传输类型

| 类型 | 说明 | 适用场景 |
|------|------|----------|
| `stdio` | 本地子进程，标准输入输出 | 本地工具，低延迟高安全 |
| `http` | HTTP 请求 | 远程服务，灵活部署 |
| `sse` | Server-Sent Events | 流式传输 |

### 配置格式

```json:.mcp.json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_..."
      }
    },
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://..."]
    }
  }
}
```

### CLI 管理

```bash:terminal
# 添加 MCP 服务器
claude mcp add --transport http notion https://mcp.notion.com/mcp

# 设置环境变量
claude mcp set-env github-mcp GITHUB_TOKEN=ghp_...

# 列出已配置服务器
claude mcp list

# 启动自身作为 MCP 服务器
claude mcp serve
```

### 常用 MCP 服务器

| 服务器 | 功能 | 来源 |
|--------|------|------|
| **github-mcp** | PR、Issue、代码搜索 | Anthropic 官方 |
| **filesystem** | 沙箱化文件读写 | Anthropic 官方 |
| **postgres / sqlite** | 数据库查询 | Anthropic 官方 |
| **brave-search** | Web 搜索 | Anthropic 官方 |
| **playwright** | 浏览器自动化 | 社区 |
| **context7** | 实时文档查询 | 社区 |
| **slack** | 消息发送/搜索 | 社区 |
| **sentry** | 错误监控 | 社区 |
| **notion** | 文档与项目管理 | 社区 |

> → [MCP 服务器](../../06-advanced/mcp-servers.md) 章节有 OpenCode 中 MCP 的完整配置指南。
> → [Claude Code 生态参考](./ecosystem.md) 有更多 MCP 服务器推荐。

---

## Subagents — 专用子 Agent

Subagents（子代理）是拥有独立上下文窗口、自定义 System Prompt 和受限工具访问的 Agent。主 Agent 通过 Task 工具委派任务给子 Agent，子 Agent 完成并以摘要形式返回结果。

### 工作原理

```
主会话（编排器）
  │
  ├── Task 调用 ──► Subagent A（独立上下文窗口）
  ├── Task 调用 ──► Subagent B（独立上下文窗口）
  └── Task 调用 ──► Subagent C（独立上下文窗口）
                           │
                      ▼ 摘要（~200 tokens）返回主会话
```

### 内置 Subagent 类型

| 类型 | 模型 | 工具 | 用途 |
|------|------|------|------|
| **Explore** | Haiku（快速）| 只读 | 代码搜索、分析 |
| **Plan** | 继承主会话 | 只读 | 规划模式研究 |
| **General-purpose** | 继承主会话 | 全部 | 复杂多步骤任务 |

### 自定义 Subagent 格式

```markdown:.claude/agents/security-reviewer.md
---
name: security-reviewer
description: 安全分析专家，专注于认证和授权代码
model: sonnet
effort: medium
maxTurns: 20
tools: Read Grep Glob Bash
disallowedTools: Write Edit
memory: project
isolation: worktree
color: red
---

# System Prompt

你是一名安全专家，专注于认证漏洞...

## 审查清单
1. SQL 注入风险
2. XSS 漏洞
3. Session 管理缺陷
```

### Frontmatter 关键字段

| 字段 | 必需 | 说明 |
|------|------|------|
| `name` | ✅ | 唯一标识符（小写+连字符）|
| `description` | ✅ | Claude 用来判断何时自动委派 |
| `model` | ❌ | sonnet / opus / haiku / inherit |
| `tools` | ❌ | 允许的工具白名单 |
| `disallowedTools` | ❌ | 禁用的工具黑名单 |
| `maxTurns` | ❌ | 最大交互轮次 |
| `permissionMode` | ❌ | 权限模式覆盖 |
| `memory` | ❌ | user / project / local 持久记忆 |
| `isolation` | ❌ | `worktree` 隔离工作区 |
| `background` | ❌ | 是否后台运行 |
| `skills` | ❌ | 预加载的 Skill 列表 |
| `mcpServers` | ❌ | 作用域 MCP 服务器 |
| `hooks` | ❌ | 作用域生命周期钩子 |

### 存储位置优先级

| 优先级 | 位置 | 作用域 |
|--------|------|--------|
| 1（最高）| 托管设置 | 组织级 |
| 2 | `--agents` CLI 标志 | 当前会话 |
| 3 | `.claude/agents/` | 当前项目（提交到 Git）|
| 4 | `~/.claude/agents/` | 个人所有项目 |

---

## Hooks — 生命周期事件

Hooks 是 Claude Code 中的事件驱动自动化机制。在 Agent 生命周期的关键节点插入自定义逻辑，支持 Shell 脚本、LLM 评估、子 Agent 和 HTTP 请求四种执行类型。

### 完整事件列表

| 事件 | 触发时机 | 可阻断 | 最佳用途 |
|------|----------|--------|----------|
| `SessionStart` | 会话开始/恢复/压缩后 | 否 | 加载上下文、设置环境变量 |
| `UserPromptSubmit` | 用户提交 Prompt | 是 | 上下文注入、内容验证 |
| `PreToolUse` | 工具执行前 | 是 | 安全拦截、自动审批 |
| `PermissionRequest` | 权限对话框出现 | 是 | 自动审批/拒绝 |
| `PostToolUse` | 工具执行成功后 | 否 | 自动格式化、审计日志 |
| `PostToolUseFailure` | 工具执行失败后 | 否 | 错误处理和恢复 |
| `SubagentStart` | Subagent 生成 | 否 | 子 Agent 初始化 |
| `SubagentStop` | Subagent 完成 | 是 | 验证子 Agent 结果 |
| `Stop` | Claude 完成响应 | 是 | 任务强制执行 |
| `PreCompact` | 上下文压缩前 | 否 | 转录备份 |
| `SessionEnd` | 会话终止 | 否 | 清理、日志 |
| `Notification` | Claude 发送通知 | 否 | 桌面提醒 |

### Hook 类型

| 类型 | 说明 | 适用场景（90% 场景）|
|------|------|------------------|
| `command` | 执行 Shell 脚本，退出码 0=成功、2=阻断 | 格式化、拦截、日志 |
| `prompt` | LLM 单轮评估 | 需要判断但无需文件访问 |
| `agent` | 多轮 Subagent（最多 50 轮）| 需要代码库状态验证 |
| `http` | POST 请求到 URL | 外部系统集成 |
| `mcp_tool` | 调用 MCP 服务器工具 | MCP 集成 |

### 配置格式

```json:.claude/hooks/hooks.json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$CLAUDE_TOOL_INPUT\" | grep -qE 'rm -rf|DROP TABLE' && exit 2 || exit 0"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write \"$CLAUDE_TOOL_INPUT_FILE_PATH\""
          }
        ]
      }
    ]
  }
}
```

### 实用 Hook 示例

**拦截危险命令：**

```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "Bash",
      "hooks": [{"type": "command", "command": "echo \"$CLAUDE_TOOL_INPUT\" | grep -qE 'rm -rf|DROP TABLE' && exit 2 || exit 0"}]
    }]
  }
}
```

**自动格式化文件：**

```json
{
  "hooks": {
    "PostToolUse": [{
      "matcher": "Write|Edit",
      "hooks": [{"type": "command", "command": "npx prettier --write \"$CLAUDE_TOOL_INPUT_FILE_PATH\""}]
    }]
  }
}
```

**注入 Git 上下文：**

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{"type": "command", "command": "echo '{\"additionalContext\": \"Branch: '$(git branch --show-current)'\"}'"}]
    }]
  }
}
```

### 退出码语义

| 退出码 | 行为 |
|--------|------|
| 0 | 成功，继续正常执行 |
| 2 | 阻断操作（仅 PreToolUse 等支持阻断的事件）|
| 其他 | 记录警告但不阻断 |

> **对比 OpenCode**：Claude Code Hooks 通过外部 Shell 进程执行，配置方式为 JSON 声明式；OpenCode Hooks 通过 `definePlugin` TypeScript API，在 Agent 进程内部以函数回调执行。Claude Code 的优势是无需编译，劣势是无法执行复杂运行时逻辑。

---

## Plugins — 打包与分发

Plugin 是 Claude Code 扩展体系的最顶层，将 Skills、Subagents、Hooks、MCP 服务器等组件打包为可分发的单元。

### Plugin 组件

| 组件 | 目录/文件 | 说明 |
|------|-----------|------|
| Skills | `skills/` | 自定义斜杠命令和自动触发指令 |
| Agents | `agents/` | 专用 Subagent |
| Hooks | `hooks/hooks.json` | 事件处理器 |
| MCP Servers | `.mcp.json` | 外部工具连接 |
| LSP Servers | `.lsp.json` | 代码智能 |
| Monitors | `monitors/monitors.json` | 后台监控 |
| Themes | `themes/` | 颜色主题 |

### Plugin 清单格式

```json:.claude-plugin/plugin.json
{
  "name": "my-plugin",
  "displayName": "我的插件",
  "version": "1.0.0",
  "description": "插件描述",
  "author": { "name": "作者" },
  "skills": "./skills/",
  "agents": "./agents/",
  "hooks": "./hooks.json",
  "mcpServers": "./.mcp.json"
}
```

### 插件安装

```bash:terminal
# 从市场安装
claude plugin install code-review@anthropic-agent-skills

# 本地路径安装
claude plugin install ./my-plugin

# 验证插件
claude plugin validate ./my-plugin --strict

# 重新加载
/reload-plugins
```

### Skills-Directory 插件（零安装）

任何包含 `.claude-plugin/plugin.json` 的 Skills 目录子文件夹会自动加载为插件：

```
~/.claude/skills/
└── my-tool/
    ├── .claude-plugin/
    │   └── plugin.json    ← 自动识别为插件
    ├── skills/
    │   └── code-review/
    │       └── SKILL.md
    ├── agents/
    │   └── reviewer.md
    └── hooks/
        └── hooks.json
```

### 安装作用域

| 作用域 | 配置文件 | 用途 |
|--------|----------|------|
| `user` | `~/.claude/settings.json` | 个人插件（默认）|
| `project` | `.claude/settings.json` | 团队插件（Git 共享）|
| `managed` | 托管设置 | 组织级（只读）|

### 生态规模

| 指标 | 数据 |
|------|------|
| 活跃插件 | 9,000+ |
| 官方市场 | `/plugin` Discover 标签页 |
| 第三方市场 | ClaudePluginHub.com、claude-plugins.dev |
| 安装复杂度 | 0 构建（纯 Markdown + JSON）|

---

## 完整 .claude/ 目录结构

```
your-project/
├── CLAUDE.md                       # 团队指令（提交到 Git）
├── CLAUDE.local.md                 # 个人覆盖（Gitignore）
└── .claude/
    ├── settings.json               # 权限 + 配置（提交到 Git）
    ├── settings.local.json         # 个人权限覆盖（Gitignore）
    ├── .mcp.json                   # MCP 服务器配置
    ├── rules/                      # 模块化规则文件
    │   ├── code-style.md
    │   └── testing.md
    ├── commands/                   # 自定义命令（已废弃，用 skills 替代）
    ├── skills/                     # 自动触发的工作流
    │   └── deploy/
    │       ├── SKILL.md
    │       └── deploy-config.md
    ├── agents/                     # 专用子 Agent
    │   ├── code-reviewer.md
    │   └── security-auditor.md
    └── hooks/                      # 事件驱动自动化
        └── validate-bash.sh

~/.claude/
├── CLAUDE.md                       # 全局指令（所有项目）
├── settings.json                   # 全局设置
├── skills/                         # 个人 Skill
├── agents/                         # 个人子 Agent
└── projects/                       # 项目记忆
```

---

## 扩展体系对比：Claude Code vs OpenCode

| 维度 | Claude Code | OpenCode |
|------|-------------|----------|
| **扩展入口** | 6 层：CLAUDE.md → Skills → MCP → Subagents → Hooks → Plugins | 4 层：Skill → Command → Plugin → Agent |
| **代码级扩展** | 无（纯配置文件）| `definePlugin` TypeScript API |
| **Hook 数量** | 14+ 外部 Shell 事件 | 20+ 进程内函数回调（OMO 53+）|
| **Subagent** | 自动委派 + 持久记忆 + worktree 隔离 | Agent 类型配置 |
| **权限模型** | 6 种模式 + allow/deny/ask 规则 | 插件沙箱 |
| **插件分发** | 纯文件目录 + JSON 清单（零构建）| npm 包 + TypeScript 编译 |
| **生态规模** | 9,000+ 插件 | 较小 |
| **学习曲线** | 配置驱动，声明式 | 代码驱动，编程式 |

## 读者视角

### 使用示例

场景：通过 MCP 服务器将外部数据库集成到 Claude Code 工作流。

1. 在 `~/.claude/servers.json` 中注册 Postgres MCP 服务器
2. 重启 Claude Code，自动发现并使用 `query_database` 工具
3. 在对话中直接说"查询最近 10 条用户记录"

```json
{
  "mcpServers": {
    "postgres": {
      "command": "node",
      "args": ["/path/to/mcp-postgres-server/index.js"],
      "env": {
        "PGHOST": "localhost",
        "PGDATABASE": "myapp"
      }
    }
  }
}
```

### 工程化示例

场景：CI 中自动监督 MCP 工具调用权限。

```yaml
# .github/workflows/audit-mcp.yml
name: MCP 权限审计
on:
  push:
    paths:
      - '.claude/servers.json'
jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: 检查高风险 MCP 工具
        run: |
          HAS_SHELL=$(jq '.mcpServers | to_entries[] | select(.value.command == "bash" or .value.command == "sh")' .claude/servers.json)
          if [ -n "$HAS_SHELL" ]; then
            echo "❌ 高风险: MCP 暴露 Shell 执行能力"
            exit 1
          fi
          echo "✅ MCP 权限审计通过"
```

## 相关章节

- → [Claude Code 内置能力](./capabilities.md) — 命令、工具集、配置方式的完整参考
- → [Claude Code 命令参考](./commands.md) — 内置命令和捆绑 Skill 的详细用法
- → [Claude Code 生态参考](./ecosystem.md) — 社区项目、最佳实践和集成工作流
- → [OpenCode Plugin 系统参考](../../appendix-b/opencode/plugins.md) — OpenCode 插件系统对比参考
- → [MCP 服务器](../../06-advanced/mcp-servers.md) — MCP 协议在 OpenCode 中的配置和实践

> 数据来源：Anthropic 官方文档 code.claude.com/docs，社区项目 awesome-claude-code。基于 Claude Code v2.1.x（2026 年 6 月）。Claude Code 生态发展迅速，建议参考官方文档获取最新信息。

---

## 常见反模式

### 在 CLAUDE.md 中实现应由 Hook 处理的逻辑

许多开发者把所有定制逻辑都塞进 CLAUDE.md，包括本应由 Hook 实现的自动化操作。例如，在 CLAUDE.md 中写"每次修改文件后运行 Prettier 格式化"，期望 Claude 记住并执行。但 LLM 的遵循率不是 100%，特别是在长会话中，这类指令容易被遗忘或忽略。

自动化操作（格式化、lint 修复、审计日志）应该用 Hook 实现，因为 Hook 是确定性执行的——Shell 脚本返回退出码 0 或 2，行为完全可预测。CLAUDE.md 适合放行为规范和约束规则，Hook 适合放必须执行的操作。两者结合才能构建可靠的扩展体系。

### Subagent 定义过于复杂导致委派失败

当 Subagent 的 System Prompt 过长或工具列表过多时，LLM 在判断"是否应该委派给这个 Subagent"时可能产生混淆。一个包含 10 个工具和 500 行指令的 Subagent 定义，其描述信息可能让主 Agent 无法准确理解它的适用场景，导致该委派时不委派，不该委派时误委派。

Subagent 的定义应该遵循"单一职责"原则：每个 Subagent 只做一件事，描述控制在 2-3 句话内，工具列表只包含该任务必需的工具。如果一个 Subagent 需要覆盖多个场景，拆分为多个更小的 Subagent。

### MCP 服务器配置未纳入版本控制

`.mcp.json` 文件包含团队共享的 MCP 服务器配置（如 GitHub Token、数据库连接串），许多团队选择将其加入 `.gitignore`。这导致新加入团队的成员需要手动配置每个 MCP 服务器，容易遗漏或配置错误。更严重的是，不同成员可能安装了不同版本的 MCP 服务器，导致行为不一致。

将 `.mcp.json` 提交到 Git（脱敏后），确保团队成员获得一致的 MCP 配置。对于包含敏感信息的环境变量（如 API Key），使用 `${ENV_VAR}` 占位符，让每个成员在本地环境变量中设置实际值。这样既保证了配置一致性，又避免了凭据泄露。

## 适用场景与限制

### 六层扩展体系的学习成本较高

Claude Code 的六层扩展体系（CLAUDE.md → Skills → MCP → Subagents → Hooks → Plugins）提供了丰富的定制能力，但也意味着新人需要理解六个层次的配置格式、存储位置和交互关系。一个完整的 Claude Code 项目可能同时包含 CLAUDE.md 规则、多个 Skills 定义、MCP 服务器配置、自定义 Subagent、Shell Hook 脚本和 Plugin 打包清单。

对于简单项目，只使用 CLAUDE.md 和 1-2 个 MCP 服务器就足够了。随着项目复杂度增长，逐步引入 Skills（封装重复操作）和 Hooks（自动化格式化）。Subagents 和 Plugins 是高级功能，只在团队有多人协作需求时才考虑。

### Hooks 只能通过外部 Shell 进程执行

Claude Code 的 Hook 系统通过 JSON 配置声明，实际执行由外部 Shell 脚本完成。这意味着 Hook 无法访问 Claude Code 的内部状态（如完整的消息历史、Agent 的推理过程），只能通过环境变量获取有限的上下文信息（`$TOOL_NAME`、`$TOOL_INPUT`、`$TOOL_OUTPUT`）。

如果你需要在 Hook 中访问 Agent 的完整上下文（例如分析整个对话历史来决定是否放行），Claude Code 的 Hook 系统做不到。此时需要使用 Agent SDK 的编程式 Hook（`PreToolUse`/`PostToolUse` 回调），它在进程内部执行，可以访问完整的运行时状态。

### Plugin 无法在 Agent 进程内注入运行时逻辑

Claude Code 的 Plugin 本质上是打包分发单元（Skills + Hooks + MCP 服务器的组合），不提供类似 OpenCode `definePlugin` 的代码级扩展 API。你不能通过 Plugin 在 Agent 的推理循环中插入自定义逻辑——Plugin 只能组合已有的扩展机制。

对于需要深度定制 Agent 行为的场景（如自定义推理策略、动态工具注册），Claude Code 的 Plugin 机制不够灵活。需要通过 Agent SDK 进行编程式集成，或者评估是否应该迁移到扩展体系更丰富的工具。

## 常见失败与陷阱

### Hook 脚本的退出码语义不一致

Claude Code Hook 的退出码语义是：0 = 成功继续，2 = 阻断操作，其他 = 记录警告但不阻断。许多开发者习惯性地在 Shell 脚本中使用 `exit 1` 表示失败，这在 Hook 系统中不会阻断操作，只是记录一条警告。如果你的安全检查脚本在检测到违规时 `exit 1`，Agent 会继续执行被标记为危险的操作。

安全相关的 Hook 必须使用 `exit 2` 来阻断操作。在编写 Hook 脚本后，用一个已知违规的输入测试，确认操作确实被阻断而非仅记录警告。建议在团队的 Hook 开发规范中明确"安全检查必须使用 exit 2"的约定。

### Skills 的三级加载导致指令执行不确定

Skills 的内容分三级加载：YAML frontmatter 始终加载，SKILL.md 正文在 Claude 判断需要时加载，辅助文件在 Agent 需要时才读取。这种设计节省了上下文空间，但也意味着 Skill 中的关键指令不一定在每次会话中都生效。

如果你的 Skill 包含必须始终执行的规则（如安全检查清单），确保它放在 SKILL.md 的 body 部分且 description 足够明确，让 Claude 判断"始终需要这个 Skill"。或者更稳妥的做法是将核心规则放在 CLAUDE.md 中，Skill 只封装可选的增强行为。

### MCP 服务器的传输类型选择错误

MCP 支持 stdio、http 和 sse 三种传输类型。stdio 适合本地工具（最低延迟、最高安全性），http 适合远程服务。许多开发者习惯性地使用 http 传输连接本地 MCP 服务器，这增加了不必要的网络开销和安全暴露面。

本地 MCP 服务器应该使用 stdio 传输，远程服务才使用 http。stdio 通信通过标准输入输出进行，不监听任何端口，不受网络攻击影响。如果你的 MCP 服务器只在本地运行，使用 http 传输不仅浪费资源，还可能在本地暴露一个 HTTP 端口。
