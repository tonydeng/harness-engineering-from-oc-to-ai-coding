# Claude Code 生态参考

本章节收录 Claude Code 的开源生态资源，涵盖社区项目、CLAUDE.md 最佳实践、MCP 服务器生态和集成工作流。

## 生态概览

Claude Code 是 Anthropic 于 2025 年 2 月发布的终端 AI 编程助手，截至 2026 年 6 月已发展为庞大的开发者生态：

| 指标 | 数据 |
|-----|------|
| GitHub Stars | 131K+ |
| 发布版本 | 136+ |
| 当前版本 | v2.1.170（2026-06-09） |
| 插件生态 | 官方市场 101+ 插件，社区 9,000+ 插件 |
| Skills 生态 | 20,300+ 技能，覆盖 25+ 类别 |
| MCP 服务器 | 9,900+ 服务器连接各类外部工具 |
| GitHub 提交占比 | 2026 Q1 峰值 326K 次/天，占公开提交 10%+ |

### 扩展体系层次

Claude Code 的扩展体系包含六个层次（按复杂度递增）：

1. **CLAUDE.md** — 项目记忆与规则
2. **Skills** — 可复用指令集（Markdown 文件）
3. **MCP 服务器** — 外部工具连接协议
4. **Subagents** — 隔离上下文的子任务代理
5. **Hooks** — 生命周期事件确定性执行
6. **Plugins** — 打包分发以上所有组件

### 定价与订阅

| 方案 | 价格 | 特点 |
|------|------|------|
| Claude Pro | $20/月 | 基础 Claude Code 访问 |
| Claude Max 5x | $100/月 | 更高用量限额 |
| Claude Max 20x | $200/月 | 大量使用场景 |
| API 按量付费 | 按 token | 适合脚本/CI 场景 |

## 开源扩展与工具

### 官方仓库

| 项目 | 描述 | GitHub |
|-----|------|--------|
| **claude-code** | 核心 CLI 工具 | anthropics/claude-code（131K+ Stars）|
| **claude-plugins-official** | 官方插件市场（101+ 插件） | anthropics/claude-plugins-official |
| **claude-plugins-community** | 社区插件市场 | anthropics/claude-plugins-community |
| **claude-code-action** | GitHub Actions 集成 | anthropics/claude-code-action |
| **skills** | 官方 Skills 仓库 | anthropics/skills（111K+ Stars）|
| **claude-agent-sdk-demos** | Agent SDK 演示 | anthropics/claude-agent-sdk-demos |

### 社区生态项目（1,000+ Stars）

| 项目 | Stars | 描述 |
|------|-------|------|
| **awesome-claude-code**（hesreallyhim） | 45.7K | 最大的 Claude Code 资源精选列表 |
| **awesome-claude-skills**（ComposioHQ） | 53.4K | Claude Skills 精选 + 500+ 外部应用集成 |
| **awesome-claude-plugins**（ComposioHQ） | 1.6K+ | 生产就绪的插件精选 |
| **awesome-claude-code**（subinium） | 15K+ | 1,000+ Stars 项目的精选列表 |
| **everything-claude-code**（affaan-m） | 141.9K+ | 全面的 Claude Code 配置集合 |
| **SuperClaude_Framework**（SuperClaude-Org） | — | 30 个斜杠命令 + 16 个代理 + 7 种行为模式 |
| **claude-code-system-prompts**（piebald-ai） | 8.6K | Claude Code 系统提示词分析 |

### Skills 生态

| 项目 | Stars | 描述 |
|------|-------|------|
| **antigravity-awesome-skills**（sickn33） | 32.5K | 1,400+ 可安装技能 |
| **awesome-agent-skills**（VoltAgent） | 15.4K | 1,000+ 跨代理兼容技能 |
| **awesome-claude-skills**（travisvn） | 11.1K | 渐进式架构说明 |
| **awesome-claude-code-subagents**（VoltAgent） | 17.1K | 126+ 专业子代理 |
| **claude-skills**（Jeffallan） | — | 66 个全栈开发技能 |
| **claude-skills**（alirezarezvani） | — | 169 个生产就绪技能 |

### 工具与框架

| 名称 | 说明 |
|------|------|
| **claudekit** | 自动保存检查点 + 20+ 专业子代理 |
| **claude-code-tools** | 会话连续性工具 + 跨代理交接 |
| **claude-toolbox** | 开发环境启动模板 |
| **crystal** | 并行 worktree 会话管理 |
| **container-use**（Dagger） | 安全的代理容器沙箱 |

## CLAUDE.md 最佳实践

### 文件层级结构

| 层级 | 路径 | 作用域 | 说明 |
|------|------|--------|------|
| 用户全局 | `~/.claude/CLAUDE.md` | 所有项目 | 个人偏好 |
| 企业策略 | `/Library/Application Support/ClaudeCode/CLAUDE.md` | 组织全员 | IT/DevOps 管理 |
| 项目根目录 | `./CLAUDE.md` | 当前仓库 | 团队共享规则（提交到 git） |
| 项目本地 | `./CLAUDE.local.md` | 当前仓库 | 个人覆盖（加入 .gitignore）|
| 子目录 | `./<subdir>/CLAUDE.md` | 特定子树 | 按需加载 |
| 规则目录 | `.claude/rules/*.md` | 项目 | 模块化规则文件 |

### 写作原则

**应当包含（✅）：**
- Claude 无法从代码推断的构建命令
- 与默认不同的代码风格规则
- 测试说明和首选测试运行器
- 仓库礼仪（分支命名、PR 约定）
- 项目特定的架构决策
- 开发环境怪异之处（必需的环境变量）
- 常见陷阱或非显而易见的行为

**不应包含（❌）：**
- Claude 读代码就能推断的内容
- 标准语言约定（Claude 已经知道）
- 详细的 API 文档（改为链接引用）
- 频繁变更的信息
- 逐文件的代码库描述
- 显而易见的实践（如"写干净代码"）

### 关键实践

| # | 实践 | 说明 |
|---|------|------|
| 1 | **保持简洁** | 控制在 200 行以内；更长的文件会降低遵循率 |
| 2 | **具体优于笼统** | "使用 2 空格缩进，无分号，单引号" > "正确格式化代码" |
| 3 | **定期审查** | 像代码一样审查 CLAUDE.md：出错时检查，定期修剪 |
| 4 | **用强调提高遵循** | "IMPORTANT" 或 "YOU MUST" 提升特定规则的遵循率 |
| 5 | **提交到 git** | 团队共享规则应该版本控制 |
| 6 | **用 .claude/rules/ 拆分** | 按主题拆分：testing.md、api-design.md |
| 7 | **AGENTS.md 兼容** | 多工具用户：`ln -s AGENTS.md CLAUDE.md` |

### 社区模板参考

| 模板 | 行数 | 哲学 | 适用场景 |
|------|------|------|----------|
| CLAUDE-template-1 | ~101 | 紧凑自包含 + 记忆韧性 | 快速开始，小项目 |
| CLAUDE-template-2 | ~153 | 记忆库标题 + 双重记忆 | 已有记忆库的用户 |
| CLAUDE-template-3 | ~105 | 渐进式披露原生 | 团队，最大上下文效率 |

## MCP 服务器生态

### 安装方式

```bash:terminal
# 远程 HTTP 服务器
claude mcp add --transport http notion https://mcp.notion.com/mcp

# 本地 stdio 服务器
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub --dsn "postgresql://..."

# 从 Claude Desktop 导入
claude mcp add-from-claude-desktop
```

### 作用域管理

| 作用域 | 存储位置 | 团队共享 | 说明 |
|--------|----------|----------|------|
| Local（默认）| `~/.claude.json` | 否 | 当前项目，个人 |
| Project | `.mcp.json` | 是 | 版本控制共享 |
| User | `~/.claude.json` | 否 | 所有项目 |

### 常用 MCP 服务器

**开发工具类：**

| 服务器 | 用途 |
|--------|------|
| github/github-mcp-server | GitHub 仓库、Issue、PR、Actions |
| @playwright/mcp | 浏览器自动化测试 |
| @upstash/context7-mcp | LLM 文档上下文 |
| @bytebase/dbhub | PostgreSQL/MySQL 数据库查询 |
| @modelcontextprotocol/server-memory | 记忆持久化 |
| @modelcontextprotocol/server-filesystem | 文件系统访问 |

**外部服务集成类：**

| 服务器 | 用途 |
|--------|------|
| Sentry（mcp.sentry.dev/mcp） | 错误监控 |
| Notion（mcp.notion.com/mcp） | 文档与项目管理 |
| Stripe（mcp.stripe.com） | 支付集成 |
| Linear（mcp.linear.app） | 问题追踪 |
| Slack（mcp.slack.com/mcp） | 团队通信 |
| Figma | 设计稿集成 |
| Supabase | 后端即服务 |

**开发框架 MCP：**

| 服务器 | 用途 |
|--------|------|
| Nuxt（nuxt.com/mcp） | Nuxt.js 元框架 |
| go-zero（mcp-zero） | Go 微服务框架 |

### 跨工具 MCP 封装器

| 项目 | 描述 |
|------|------|
| **cc-mcp**（csbrandt） | 封装 Claude Code CLI 为 MCP 服务器，支持 OpenCode |
| **claude-code-mcp**（steipete） | 一次性 MCP 模式的 Claude Code |
| **ai-cli-mcp**（mkXultra） | 支持 Claude、Codex、Gemini、Forge、OpenCode 的统一 MCP |

## 集成与工作流

### GitHub Actions 集成

```yaml:.github/workflows/claude-code.yml
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: "Review this PR for security issues"
    trigger_phrase: "@claude"
```

**关键参数：**

| 参数 | 说明 |
|------|------|
| `prompt` | 给 Claude 的指令（纯文本或 skill 名称）|
| `claude_args` | 传递给 Claude Code 的 CLI 参数 |
| `trigger_phrase` | 自定义触发词（默认 `@claude`）|

### 编程式使用（Agent SDK）

```typescript
import { claude } from '@anthropic-ai/claude-code';

const result = await claude({
  prompt: "重构这个模块",
  allowedTools: ["Read", "Edit", "Bash"],
  permissionMode: "acceptEdits",
  maxBudgetUsd: 1.0,
});
```

**支持的接口：**

- **CLI**：`claude -p "prompt"` — 适合脚本和 CI/CD
- **Python SDK**：`pip install anthropic-ai-sdk`
- **TypeScript SDK**：`npm install @anthropic-ai/sdk`

### 典型工作流

```bash:terminal
# 代码审查
claude -p "审查最近的变更，检查安全漏洞和代码质量问题"

# 自动化测试与修复
claude -p "运行测试套件，分析失败测试，修复它们" \
  --allowedTools "Bash,Edit,Read" \
  --permission-mode dontAsk

# 多代理协作
claude --agent "backend-architect" "设计微服务架构"

# 文档生成
claude -p "为这个项目生成全面的 API 文档和 README"
```

### Claude Code vs OpenCode 生态对比

| 维度 | Claude Code | OpenCode |
|------|-------------|----------|
| 许可证 | 闭源（Anthropic）| MIT 开源 |
| 模型生态 | 仅 Claude 模型族 | 75+ 提供商 |
| GitHub Stars | 131K（2026-06） | 161K（2026-06）|
| 插件/扩展 | 官方 101+ 插件 | Plugin + Skill + MCP 三层 |
| Skills 生态 | 20,300+ 技能 | skills.sh 平台（659K+ 安装）|
| MCP 服务器 | 9,900+ | 完全兼容 MCP 协议 |
| 价格 | $20-200/月 | 免费工具 + 按提供商付费 |
| 优势 | 速度、打磨、模型质量 | 灵活性、成本、隐私 |

## 相关章节

- → [Claude Code 内置能力](./capabilities.md) — 命令、工具、配置方式的完整参考
- → [OpenCode 生态参考](../opencode/ecosystem.md) — OpenCode 开源生态对比
- → [MCP 服务器](../../06-advanced/mcp-servers.md) — MCP 协议在 OpenCode 中的配置和实践
- → [生态对比](../../01-introduction/ecosystem-comparison.md) — AI 编程工具生态全景

> 数据来源：Anthropic 官方文档、awesome-claude-code 注册表、ComposioHQ 精选列表。数据截止 2026 年 6 月。Claude Code 生态发展迅速，建议参考官方文档获取最新信息。
