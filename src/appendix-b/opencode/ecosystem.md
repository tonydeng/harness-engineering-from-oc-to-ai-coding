# OpenCode 生态参考

本章节收录 OpenCode 的开源生态资源，涵盖社区项目、Skill 推荐、MCP 服务器和最佳实践。

## 开源生态概览

OpenCode 的生态体系由以下几层构成：

| 生态层级 | 说明 | 关键入口 |
|---------|------|---------|
| **官方仓库** | 核心引擎、SDK、桌面应用 | anomalyco/opencode |
| **Plugin 系统** | JS/TS 模块，通过 npm 或本地文件加载 | [Plugin 系统参考](./plugins.md) |
| **Skill 系统** | SKILL.md 格式的可复用指令集 | [Skill 开发](../../05-skills/) |
| **MCP 集成** | Model Context Protocol 外部工具接入 | [MCP 服务器](../../06-advanced/mcp-servers.md) |
| **社区聚合** | awesome-opencode、skills.sh | 见下文详表 |

### 生态规模

| 指标 | 数据 |
|-----|------|
| GitHub Stars | 160K+ |
| 贡献者 | 900+ |
| 月活开发者 | 750 万+ |
| 支持 LLM 供应商 | 75+（通过 Models.dev） |
| awesome-opencode 收录项目 | 90+ |
| skills.sh 累计安装量 | 659K+ |

## 优质开源项目

### 官方仓库

| 项目 | 描述 | 地址 |
|-----|------|------|
| **opencode** | 核心引擎（TUI + Server + Agent 系统） | [github.com/anomalyco/opencode](https://github.com/anomalyco/opencode) |
| **opencode-sdk-js** | JavaScript/TypeScript SDK | [github.com/anomalyco/opencode-sdk-js](https://github.com/anomalyco/opencode-sdk-js) |
| **opencode-sdk-go** | Go SDK | [github.com/anomalyco/opencode-sdk-go](https://github.com/anomalyco/opencode-sdk-go) |

### 社区推荐项目

| 项目 | ⭐ | 描述 | 类别 |
|-----|-----|------|------|
| **oh-my-openagent** | 高 | 全能插件：后台 Agent、LSP/AST/MCP 工具预置 | Plugin |
| **awesome-opencode** | 7.8K | 生态聚合清单 | 资源 |
| **opencode-manager** | — | OpenCode 会话管理器，支持多实例 | 工具 |
| **OpenCode-Everything-You-Need-to-Know** | 270 | 全面教程：安装到自定义 Agent、Skill、Plugin、MCP | 教程 |
| **opencode-docs** | — | 社区维护的完整文档（v1.2.27，31 个文档） | 文档 |
| **opencode-browser** | 54 | Browser MCP 插件，支持浏览器自动化 | Plugin |
| **opencode.nvim** | — | Neovim 集成 | 集成 |
| **portal** | — | 移动端 Web UI，支持 Tailscale/VPN 远程访问 | 工具 |
| **OpenChamber** | — | Web/Desktop App + VS Code Extension | 客户端 |
| **OpenCode-Obsidian** | — | Obsidian 插件，在 Obsidian 内嵌入 OpenCode | 集成 |
| **ocx** | — | OpenCode 扩展管理器，支持便携式隔离 Profile | 工具 |
| **CodeNomad** | — | Desktop/Web/Mobile/Remote 全平台客户端 | 客户端 |

## 社区 Skill 推荐

### Skill 安装方式

```bash:terminal
# 通过 skills CLI（推荐）
npx skills add <owner/repo>@<skill-name>

# 通过 BuySkills CLI
npx buyskills install <skill-name>

# 手动放置
cp -r skill-folder/ ~/.config/opencode/skills/
```

Skill 文件可放置于以下位置：

| 位置 | 路径 | 作用域 |
|-----|------|-------|
| 项目级 | `.opencode/skills/<name>/SKILL.md` | 仅当前项目 |
| 全局级 | `~/.config/opencode/skills/<name>/SKILL.md` | 所有项目 |
| Claude 兼容 | `.claude/skills/<name>/SKILL.md` | 项目级 |

### 开发工作流类

| Skill | 来源 | 安装量 | 说明 |
|-------|------|--------|------|
| **find-skills** | vercel-labs/skills | 2.0M | Skill 发现与安装 |
| **vercel-react-best-practices** | vercel-labs/agent-skills | 467K | React/Next.js 最佳实践 |
| **web-design-guidelines** | vercel-labs/agent-skills | 382K | Web 设计规范 |
| **systematic-debugging** | obra/superpowers | 138K | 系统化调试 |
| **test-driven-development** | obra/superpowers | 122K | TDD 工作流 |
| **writing-plans** | obra/superpowers | 138K | 实现计划编写 |
| **executing-plans** | obra/superpowers | 113K | 计划执行与审查 |
| **requesting-code-review** | obra/superpowers | 124K | 代码审查请求 |
| **verification-before-completion** | obra/superpowers | 104K | 完成前验证 |
| **brainstorming** | obra/superpowers | 215K | 头脑风暴与需求探索 |
| **subagent-driven-development** | obra/superpowers | 106K | 子 Agent 驱动开发 |

### 代码质量类

| Skill | 来源 | 说明 |
|-------|------|------|
| **code-reviewer** | farmage/opencode-skills | 代码审查专家，识别 Bug、安全漏洞、代码异味 |
| **grill-me** | mattpocock/skills | 代码质量审查（297K 安装） |
| **diagnose** | mattpocock/skills | 问题诊断（202K 安装） |
| **improve-codebase-architecture** | mattpocock/skills | 代码库架构改进（243K 安装） |

### AI/ML 与设计类

| Skill | 来源 | 说明 |
|-------|------|------|
| **frontend-design** | anthropics/skills | 前端设计（529K 安装） |
| **skill-creator** | anthropics/skills | Skill 创建工具（264K 安装） |
| **shadcn** | shadcn/ui | shadcn/ui 组件库最佳实践（185K 安装） |
| **patent-writer** | wpf19911118/opencode-skills | AI 驱动的学术论文专利撰写 |

## 常用 MCP 服务器

OpenCode 在 `opencode.json` 中配置 MCP 服务器，支持本地（stdio）和远程（HTTP/WebSocket）两种模式：

```jsonc:terminal
{
  "mcpServers": {
    "my-local-server": {
      "command": "npx",
      "args": ["-y", "my-mcp-command"]
    },
    "my-remote-server": {
      "url": "https://example.com/mcp"
    }
  }
}
```

> MCP 服务器会增加上下文占用。建议按需启用，避免超出上下文限制。

### 官方参考实现

| 服务器 | 安装命令 | 用途 |
|-------|---------|------|
| **server-git** | `npx @modelcontextprotocol/server-git` | Git 操作 |
| **server-github** | `npx @modelcontextprotocol/server-github` | GitHub API |
| **server-filesystem** | `npx @modelcontextprotocol/server-filesystem` | 文件系统读写 |
| **server-sequential-thinking** | `npx @modelcontextprotocol/server-sequential-thinking` | 强制分步推理 |
| **server-postgres** | `npx @modelcontextprotocol/server-postgres` | PostgreSQL 查询 |
| **server-sqlite** | `npx @modelcontextprotocol/server-sqlite` | SQLite 数据库 |
| **server-puppeteer** | `npx @modelcontextprotocol/server-puppeteer` | 浏览器自动化 |
| **server-brave-search** | `npx @modelcontextprotocol/server-brave-search` | 搜索引擎 |
| **server-fetch** | `npx @modelcontextprotocol/server-fetch` | HTTP 请求 |

### 社区推荐

| 服务器 | 说明 |
|-------|------|
| **Context7**（@upstash/context7-mcp） | 拉取最新库文档，防止 API 过时幻觉（37K+ 下载） |
| **GitMCP** | 零配置文档访问：将 GitHub URL 中的 `github.com` 替换为 `gitmcp.io` |
| **Browser MCP**（browsermcp.io） | 浏览器自动化 |
| **opencode-mcp**（nosolosoft/opencode-mcp） | 通过 MCP 协议执行 OpenCode 命令、管理会话 |

### MCP 最佳实践

1. **按需启用**：仅启用当前工作流需要的 MCP 服务器
2. **上下文预算**：监控 token 使用，GitHub MCP 容易超出上下文限制
3. **环境变量安全**：使用 `${ENV_VAR}` 从 shell 环境读取密钥，不硬编码
4. **远程服务器**：组织可通过 `.well-known/opencode` 端点提供默认 MCP 服务器
5. **最小权限**：仅启用必要的 MCP 服务器，减少攻击面

## 最佳实践参考

### AGENTS.md 项目规范

AGENTS.md 是 OpenCode 生态中的项目级 AI 指令标准，已纳入 Linux Foundation 的 Agentic AI Foundation，GitHub 上有 6 万+ 开源项目采用。

推荐结构：

```markdown:AGENTS.md
# 项目名称

## 构建与测试
- 安装依赖：`pnpm install`
- 启动开发：`pnpm dev`
- 运行测试：`pnpm test`

## 代码规范
- TypeScript 严格模式
- 单引号，无分号

## 项目结构
- `packages/` — 工作区包
- `infra/` — 基础设施定义
```

在 OpenCode TUI 中运行 `/init` 即可自动扫描项目结构生成 AGENTS.md。

### 社区配置模板

| 配置 | 来源 | 说明 |
|-----|------|------|
| opencode-config | gotar | 完整配置：Agent + Command + Context + Skill |
| opencode | jjmartres | 灵活的配置起点：Agent、Command、Rule、Skill、MCP |
| opencode.config | ridakaddir | 日常使用的实战配置 |

### 推荐学习资源

| 资源 | 地址 | 说明 |
|-----|------|------|
| 官方文档 | [opencode.ai/docs](https://opencode.ai/docs/) | 权威参考 |
| awesome-opencode | [github.com/awesome-opencode/awesome-opencode](https://github.com/awesome-opencode/awesome-opencode) | 生态聚合清单（7.8K Star） |
| opencode.cafe | [opencode.cafe](https://opencode.cafe) | 社区扩展市场 |
| skills.sh | [skills.sh](https://skills.sh) | 开放 Agent Skills 生态（659K+ 安装） |
| BuySkills | [buyskills.ai](https://buyskills.ai/) | 跨 Agent Skill 市场 |

## 相关章节

- → [OpenCode 内置能力](./capabilities.md) — 命令、工具、自定义扩展的完整参考
- → [Plugin 系统参考](./plugins.md) — Plugin API、Hook 点、安全实践
- → [MCP 服务器](../../06-advanced/mcp-servers.md) — MCP 协议在 OpenCode 中的配置和实践
- → [Skill 开发](../../05-skills/) — 创建和发布自定义 Skill

> 数据来源：官方文档、awesome-opencode 注册表、skills.sh 排行榜、BuySkills 市场。数据截止 2026 年 6 月。
