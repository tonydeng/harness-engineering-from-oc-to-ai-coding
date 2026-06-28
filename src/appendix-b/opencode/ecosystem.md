# OpenCode 生态参考

本章节围绕 **Harness Engineering（驾驭工程）** 和 **Loop Engineering（循环工程）** 两大主线，将 OpenCode 生态项目按工程价值分类组织，帮助你在实际工作中找到最相关的工具和实践参考。

## 驾驭工程生态（Harness Engineering）

聚焦配置约束、安全管控和质量门禁——让 **Agent（智能体）** 在可控范围内可靠执行。

### 配置规范生态

AGENTS.md 是 OpenCode 生态中的项目级 AI 指令标准，已纳入 Linux Foundation 的 Agentic AI Foundation，GitHub 上有 6 万+ 开源项目采用。

在 OpenCode TUI 中运行 `/init` 即可自动扫描项目结构生成 AGENTS.md。

**推荐结构：**

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

**社区配置模板（可直接用于约束 Agent 行为）：**

| 配置 | 来源 | 说明 |
|-----|------|------|
| opencode-config | gotar | 完整配置：Agent + Command + **Context（上下文）** + **Skill（技能）** |
| opencode | jjmartres | 灵活的配置起点：Agent、Command、Rule、Skill、**MCP（模型上下文协议）** |
| opencode.config | ridakaddir | 日常使用的实战配置 |

**生态规模：**

| 指标 | 数据 |
|-----|------|
| GitHub Stars | ~180K |
| 贡献者 | 900+ |
| 月活开发者 | 800 万+ |
| 支持 LLM 供应商 | 75+（通过 Models.dev） |
| awesome-opencode 收录项目 | 90+ |
| skills.sh 累计安装量 | 659K+ |

### 权限与安全生态

OpenCode 的 **Plugin（插件）** Hook 系统（53+ Hook 点）和安全权限模型为约束 Agent 行为提供了工程化基础：

| 项目 | 说明 |
|------|------|
| **oh-my-openagent** | 全能插件：后台 Agent、LSP/AST/MCP 工具预置，内置权限管理和质量门禁 |
| **container-use**（Dagger） | 安全的 Agent 容器沙箱，隔离执行环境 |
| **ocx** | OpenCode 扩展管理器，支持便携式隔离 Profile，通过 Profile 隔离不同项目的 Agent 行为 |

### 质量门禁与验证生态

以下 Skill 构成了完整的质量门禁链条——覆盖从规划到验证的 Harness Engineering 闭环：

| Skill | 来源 | 安装量 | 在 Harness Engineering 中的角色 |
|-------|------|--------|-----------------------------|
| **writing-plans** | obra/superpowers | 138K | 实现计划编写（可复现性） |
| **executing-plans** | obra/superpowers | 113K | 计划执行与审查（可审计性） |
| **requesting-code-review** | obra/superpowers | 124K | 代码审查请求（可审计性） |
| **verification-before-completion** | obra/superpowers | 104K | 完成前验证（可改进性） |
| **brainstorming** | obra/superpowers | 215K | 头脑风暴与需求探索（需求工程化） |
| **subagent-driven-development** | obra/superpowers | 106K | 子 Agent 驱动开发（编排工程化） |
| **systematic-debugging** | obra/superpowers | 138K | 系统化调试（排错工程化） |
| **test-driven-development** | obra/superpowers | 122K | TDD 工作流（质量工程化） |
| **code-reviewer** | farmage/opencode-skills | — | 代码审查专家，识别 Bug、安全漏洞、代码异味 |
| **grill-me** | mattpocock/skills | 297K | 代码质量审查 |
| **diagnose** | mattpocock/skills | 202K | 问题诊断 |
| **improve-codebase-architecture** | mattpocock/skills | 243K | 代码库架构改进 |

### 成本管控生态

OpenCode 通过 Category 路由系统实现模型降级链，将文档任务用便宜模型处理、复杂编码用高端模型，是 Harness Engineering 成本支柱的核心实践。

| 资源 | 说明 |
|-----|------|
| **Models.dev** | 75+ 模型供应商统一接口，按任务类别自动路由 |
| **Token 预算配置** | Session 级上限 + 工具输出保护窗口（最近 40K Token） |
| **上下文压缩策略** | 自动/手动/微压缩三层，详见 → [上下文压缩](../../06-advanced/context-compression.md) |

---

## 循环工程生态（Loop Engineering）

聚焦 CI/CD 集成、工作流自动化和会话管理——"我不在时工作如何继续"。

### CI/CD 集成

OpenCode 可通过 SDK 或 CLI 模式嵌入 CI/CD 流水线：

```bash:terminal
# CLI 模式执行单次操作，适合 CI/CD 脚本
npx opencode -m "review the latest PR changes for security issues"

# 指定权限模式，避免交互等待
npx opencode -m "run tests and fix failures" --permission-mode acceptEdits
```

### 工作流自动化工具

| 项目 | 说明 |
|------|------|
| **opencode-manager** | 会话管理器，支持多实例并行运行 |
| **ocx** | 扩展管理器，支持便携式隔离 Profile，可在不同项目中复用 Agent 配置 |
| **opencode-browser** | Browser MCP 插件，支持浏览器自动化，适合 E2E 循环 |

### 会话与持久化

| 资源 | 说明 |
|-----|------|
| **Session Compaction** | 超长 Session 自动压缩摘要，释放上下文空间 |
| **.opencodeignore** | 排除无关文件，减少上下文负担 |
| **opencode-mcp**（nosolosoft） | 通过 MCP 协议执行 OpenCode 命令、管理会话 |

---

## 扩展集成生态

### MCP 服务器

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

**官方参考实现：**

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

**社区推荐：**

| 服务器 | 说明 |
|-------|------|
| **Context7**（@upstash/context7-mcp） | 拉取最新库文档，防止 API 过时幻觉（37K+ 下载） |
| **GitMCP** | 零配置文档访问：将 GitHub URL 中的 `github.com` 替换为 `gitmcp.io` |
| **Browser MCP**（browsermcp.io） | 浏览器自动化 |
| **opencode-mcp**（nosolosoft/opencode-mcp） | 通过 MCP 协议执行 OpenCode 命令、管理会话 |

**MCP 最佳实践：**
1. **按需启用**：仅启用当前工作流需要的 MCP 服务器
2. **上下文预算**：监控 token 使用，GitHub MCP 容易超出上下文限制
3. **环境变量安全**：使用 `${ENV_VAR}` 从 shell 环境读取密钥，不硬编码
4. **远程服务器**：组织可通过 `.well-known/opencode` 端点提供默认 MCP 服务器
5. **最小权限**：仅启用必要的 MCP 服务器，减少攻击面

### Plugin 生态

OpenCode 的 Plugin 系统允许通过 JavaScript/TypeScript 模块扩展 Agent 能力：

| 项目 | 说明 |
|------|------|
| **oh-my-openagent** | 全能插件：后台 Agent、LSP/AST/MCP 工具预置 |
| **opencode-browser** | Browser MCP 插件 |
| **opencode-mcp** | OpenCode 命令 MCP 封装 |
| **opencode.nvim** | Neovim 编辑器集成 |

Plugin 架构详见 → [Plugin 系统参考](./plugins.md)

### SDK 生态

| SDK | 包名 | 用途 |
|-----|------|------|
| JavaScript/TypeScript | `@opencode-sdk-js` | Node.js 应用中嵌入 Agent 能力 |
| Go | `opencode-sdk-go` | Go 服务集成 |
| Plugin Hook API | 内置 | 通过 definePlugin 扩展引擎能力 |

### Skill 安装方式

Skill 可通过 CLI 安装或手动放置到 `.opencode/skills/`（项目级）或 `~/.config/opencode/skills/`（全局级）。

```bash:terminal
npx skills add <owner/repo>@<skill-name>          # 通过 skills CLI（推荐）
npx buyskills install <skill-name>                 # 通过 BuySkills CLI
```

→ Skill 安装和路径说明详见 [Skill 开发](../../05-skills/)。

---

## 社区精选项目

### 官方仓库

| 项目 | 描述 | 地址 |
|-----|------|------|
| **opencode** | 核心引擎（TUI + Server + Agent 系统） | [github.com/anomalyco/opencode](https://github.com/anomalyco/opencode) |
| **@opencode-sdk-js** | JavaScript/TypeScript SDK | [github.com/anomalyco/opencode-sdk-js](https://github.com/anomalyco/opencode-sdk-js) |
| **opencode-sdk-go** | Go SDK | [github.com/anomalyco/opencode-sdk-go](https://github.com/anomalyco/opencode-sdk-go) |

### 社区高星项目

按与 Harness Engineering 的相关性分类：

| 项目 | ⭐ | 工程化分类 | 说明 |
|-----|-----|-----------|------|
| **awesome-opencode** | 7.8K | 生态聚合 | 90+ 收录项目 |
| **oh-my-openagent** | 高 | 编排 + 安全 | Plugin 扩展 + LSP/AST 工具预置 |
| **ocx** | — | 配置隔离 | Profile 管理，支持环境隔离 |
| **opencode-manager** | — | 会话管理 | 多实例并行运行 |
| **OpenCode-Everything-You-Need-to-Know** | 270 | 教程 | 安装到自定义 Agent、Skill、Plugin、MCP |
| **opencode-docs** | — | 文档 | 社区维护的完整文档（v1.2.27，31 个文档）|
| **opencode.nvim** | — | 编辑器集成 | Neovim 插件 |
| **portal** | — | 远程访问 | 移动端 Web UI，支持 Tailscale/VPN |
| **OpenChamber** | — | 客户端 | Web/Desktop App + VS Code Extension |
| **OpenCode-Obsidian** | — | 编辑器集成 | Obsidian 插件 |
| **CodeNomad** | — | 客户端 | Desktop/Web/Mobile/Remote 全平台 |

### Skill 生态（按工程阶段分类）

**Harness Engineering 核心技能（配置→执行→验证）：**

| Skill | 来源 | 安装量 | 工程阶段 |
|-------|------|--------|----------|
| **find-skills** | vercel-labs/skills | 2.0M | 配置发现 |
| **vercel-react-best-practices** | vercel-labs/agent-skills | 467K | 执行规范 |
| **web-design-guidelines** | vercel-labs/agent-skills | 382K | 执行规范 |
| **skill-creator** | anthropics/skills | 264K | 配置扩展 |
| **frontend-design** | anthropics/skills | 529K | 执行指导 |
| **shadcn** | shadcn/ui | 185K | 组件库最佳实践 |
| **patent-writer** | wpf19911118/opencode-skills | — | 特定领域写作 |

### 推荐学习资源

| 资源 | 地址 | 说明 |
|-----|------|------|
| 官方文档 | [opencode.ai/docs](https://opencode.ai/docs/) | 权威参考 |
| awesome-opencode | [github.com/awesome-opencode/awesome-opencode](https://github.com/awesome-opencode/awesome-opencode) | 生态聚合清单（7.8K Star） |
| opencode.cafe | [opencode.cafe](https://opencode.cafe) | 社区扩展市场 |
| skills.sh | [skills.sh](https://skills.sh) | 开放 Agent Skills 生态（659K+ 安装） |
| BuySkills | [buyskills.ai](https://buyskills.ai/) | 跨 Agent Skill 市场 |

## 迁移指南

从其他 AI 编程工具迁移到 OpenCode 时，需要关注以下关键差异：

### 从 Claude Code 迁移

- **模型灵活性**：Claude Code 仅支持 Claude 系列模型，OpenCode 支持 75+ LLM 供应商/20+ 模型。迁移后可在 `opencode.json` 的 Provider 配置中添加多模型，按任务需求切换
- **CLAUDE.md → AGENTS.md**：Claude Code 的 `CLAUDE.md` 项目指令在 OpenCode 中对应 `AGENTS.md`，格式兼容但语法扩展更多（AGENTS.md 支持 Mermaid 图表、Role 定义、条件指令）。在项目根运行 `/init` 自动生成 AGENTS.md
- **Subagent → Category 系统**：Claude Code 的 Markdown Subagent 在 OpenCode 中对应 OMO Category 系统。`CLAUDE.md` 中 `@agent` 块需重写为 OMO 的 `category` 配置或 `agent.json` 文件
- **Plugin → Skill + Plugin**：Claude Code 的 Plugin（JavaScript 文件）在 OpenCode 中对应 Skill（Markdown 指令文件）和 Plugin（TypeScript API）两层。简单行为用 Skill，深度定制用 Plugin
- **命令习惯**：Claude Code 的 `/init`、`/add` 等命令在 OpenCode 中存在对应版本，但参数和快捷键不同。参见 [OpenCode 命令参考](./commands.md) 对照

### 从 Pi Agent 迁移

- **Extension → Plugin/Skill**：Pi Agent 的 Extension（TypeScript 函数）在 OpenCode 中可拆为 Skill（声明式行为）和 Plugin（程序化 Hook）两层。纯数据处理用 Skill，需要监听 Agent 生命周期用 Plugin
- **Provider 配置**：Pi Agent 通过 `~/.pi/config.yaml` 配置 Provider；OpenCode 通过 `opencode.json` 管理。迁移时需将 Provider 定义从 YAML 转为 JSON 格式
- **命令体系**：Pi Agent 的 `/model`、`/system` 等命令在 OpenCode 中有对应实现（`/models`、`/prompt`），路径不同但功能类似

## 相关章节

- → [OpenCode 内置能力](./capabilities.md) — 命令、工具、自定义扩展的完整参考
- → [Plugin 系统参考](./plugins.md) — Plugin API、Hook 点、安全实践
- → [MCP 服务器](../../06-advanced/mcp-servers.md) — MCP 协议在 OpenCode 中的配置和实践
- → [Skill 开发](../../05-skills/) — 创建和发布自定义 Skill
- → [Pi Agent 迁移指南](../../appendix-d/pi/ecosystem.md#迁移指南) — 从 OpenCode/Claude Code 迁移到 Pi Agent

---

## 读者视角

### 适用读者角色
- 入门开发者 — 适合快速上手 OpenCode 的基础能力，了解核心概念和常用命令
- 智能体开发工程师 — 需要设计、调试、进化 AI 编码智能体，建立系统化的 Agent 工程体系
- 效率开发者 — 已用 AI 工具，想掌握 Agent 编排和工作流模式，提升日常开发效率 2x+
- 技术负责人 — 团队技术决策者，关注标准化，建立团队级 Harness Engineering 体系
- Skill 作者 — 有 AI 使用经验，想开发高质量、可复用的 Skill
- 工程经理 — 评估团队工具选型，判断 OpenCode 的投资回报率
- 需求分析师/产品经理 — 验证需求覆盖完整性，评估内容价值主张
- 系统架构师/技术顾问 — 评估 OpenCode 的技术可行性、架构集成与安全合规
- 后端开发者/API 工程师 — 将 AI Agent 嵌入后端开发工作流，掌握 MCP 服务端集成
- 前端开发者/UI 工程师 — 将 Agent 编排应用到前端场景，类比理解 Skill 系统
- 文档 UX 专家 — 确保文档可读性、Mermaid 规范、移动端/无障碍体验
- 技术审校/QA 编辑 — 建立质量门禁，验证代码示例可运行性、术语一致性
- 安全工程师/架构师 — 建立 OpenCode 安全基线，评估企业级合规
- 安全研究人员/红队成员 — 评估 AI Agent 攻击面，利用 Agent 自动化安全测试

### 典型使用场景
- 快速上手 OpenCode，完成第一个成功的尝试
- 设计和调试 AI 智能体，建立系统化的 Agent 工程体系
- 掌握 Agent 编排和工作流模式，提升日常开发效率
- 建立团队级 Harness Engineering 体系，进行技术决策
- 开发高质量、可复用的 Skill，封装领域知识
- 评估 OpenCode 的投资回报率，进行工具选型决策
- 验证需求覆盖完整性，评估内容价值主张
- 评估 OpenCode 的技术可行性，进行架构集成与安全合规
- 将 AI Agent 嵌入后端开发工作流，实现 MCP 服务端集成
- 将 Agent 编排应用到前端场景，类比理解 Skill 系统
- 确保文档可读性、Mermaid 规范、移动端/无障碍体验
- 建立质量门禁，验证代码示例可运行性、术语一致性
- 建立 OpenCode 安全基线，评估企业级合规
- 评估 AI Agent 攻击面，利用 Agent 自动化安全测试

### 使用示例
```bash
# 快速上手 OpenCode
opencode serve

# 创建项目知识库
opencode /init

# 使用自定义 Skill
opencode "分析代码质量"

# 执行自动化安全审计
opencode /ralph-loop

# 并行执行多个任务
opencode /hyperplan
```

### 工程化示例

**配置顺序检查表：**

1. **第1步：初始化项目**
   ```bash
   opencode /init
   ```

2. **第2步：配置 Provider**
   ```json
   {
     "providers": {
       "anthropic": {
         "apiKey": "sk-ant-...",
         "defaultModel": "claude-3-5-sonnet-20241022"
       }
     }
   }
   ```

3. **第3步：加载 Skill**
   ```bash
   opencode skills add myorg/my-skill
   ```

### 与前/后文章的衔接
- ← [OpenCode 内置能力](./capabilities.md) — 了解 OpenCode 的核心功能和能力
- → [OpenCode 内置命令参考](./commands.md) — 详细了解每个命令的用法和参数

> 数据来源：官方文档、awesome-opencode 注册表、skills.sh 排行榜、BuySkills 市场。数据截止 2026 年 6 月。
