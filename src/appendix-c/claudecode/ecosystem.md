# Claude Code 生态参考

本章节围绕 **Harness Engineering（驾驭工程）** 和 **Loop Engineering（循环工程）** 两大主线，将 Claude Code 生态资源按工程价值分类组织，帮助你在实际工作中找到最相关的配置参考和开源工具。

## 驾驭工程生态（Harness Engineering）

聚焦 CLAUDE.md 配置规范、权限管控和扩展体系——让 Claude Code **Agent（智能体）** 在可控范围内可靠执行。

### 配置规范生态

CLAUDE.md 是 Claude Code 生态中的核心约束系统，支持多层级文件覆盖（按优先级从低到高）：

| 层级 | 路径 | 作用域 | 说明 |
|------|------|--------|------|
| 用户全局 | `~/.claude/CLAUDE.md` | 所有项目 | 个人偏好 |
| 企业策略 | `/Library/Application Support/ClaudeCode/CLAUDE.md` | 组织全员 | IT/DevOps 管理 |
| 项目根目录 | `./CLAUDE.md` | 当前仓库 | 团队共享规则（提交到 git） |
| 项目本地 | `./CLAUDE.local.md` | 当前仓库 | 个人覆盖（加入 .gitignore） |
| 子目录 | `./<subdir>/CLAUDE.md` | 特定子树 | 按需加载 |
| 规则目录 | `.claude/rules/*.md` | 项目 | 模块化规则文件 |

**写作原则（应当包含 ✅）：**
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
- 常识性实践（如"写干净代码"）

**关键实践：**

| # | 实践 | 说明 |
|---|------|------|
| 1 | **保持简洁** | 控制在 200 行以内；更长的文件会降低遵循率 |
| 2 | **具体优于笼统** | "使用 2 空格缩进，无分号，单引号" > "正确格式化代码" |
| 3 | **定期审查** | 像代码一样审查 CLAUDE.md：出错时检查，定期修剪 |
| 4 | **用强调提高遵循** | "IMPORTANT" 或 "YOU MUST" 提升特定规则的遵循率 |
| 5 | **提交到 git** | 团队共享规则应该版本控制 |
| 6 | **用 .claude/rules/ 拆分** | 按主题拆分：testing.md、api-design.md |
| 7 | **AGENTS.md 兼容** | 多工具用户：`ln -s AGENTS.md CLAUDE.md` |

**社区模板参考（按工程复杂度排序）：**

| 模板 | 行数 | 哲学 | 适用场景 | 在 Harness Engineering 中的角色 |
|------|------|------|----------|-----------------------------|
| CLAUDE-template-1 | ~101 | 紧凑自包含 + 记忆韧性 | 快速开始，小项目 | 基础约束 |
| CLAUDE-template-2 | ~153 | 记忆库标题 + 双重记忆 | 已有记忆库的用户 | 上下文工程 |
| CLAUDE-template-3 | ~105 | 渐进式披露原生 | 团队，最大上下文效率 | 驾驭工程配置 |

### 扩展体系层次

Claude Code 的扩展体系包含六个层次（按复杂度递增），从 L3 驾驭工程到 L4 循环工程逐层递进：

1. **CLAUDE.md** — 项目记忆与规则（约束系统基础）
2. **Skills** — 可复用指令集（质量门禁）
3. **MCP 服务器** — 外部工具连接（集成扩展）
4. **Subagents** — 隔离上下文的子任务代理（编排工程）
5. **Hooks** — 生命周期事件确定性执行（循环触发）
6. **Plugins** — 打包分发以上所有组件（循环封装）

### 生态规模

| 指标 | 数据 |
|-----|------|
| GitHub Stars | 131K+ |
| 发布版本 | 136+ |
| 当前版本 | v2.1.193（2026-06-26） |
| 插件生态 | 官方市场 101+ 插件，社区 9,000+ 插件 |
| Skills 生态 | 20,300+ 技能，覆盖 25+ 类别 |
| **MCP（模型上下文协议）** 服务器 | 9,900+ 服务器连接各类外部工具 |
| GitHub 提交占比 | 2026 Q1 峰值 326K 次/天，占公开提交 10%+ |

### 成本管控

| 方案 | 价格 | 适用场景 |
|------|------|----------|
| Claude Pro | $20/月 | 日常开发 |
| Claude Max 5x | $100/月 | 更高用量限额 |
| Claude Max 20x | $200/月 | 大量使用场景 |
| API 按量付费 | 按 token | 适合脚本/CI 场景 |

---

## 循环工程生态（Loop Engineering）

聚焦 Subagents 编排、CI/CD 自动化和跨 Session 持久化——"我不在时工作如何继续"。

### CI/CD 集成

**GitHub Actions 集成：**

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
| `prompt` | 给 Claude 的指令（纯文本或 skill 名称） |
| `claude_args` | 传递给 Claude Code 的 CLI 参数 |
| `trigger_phrase` | 自定义触发词（默认 `@claude`） |

**编程式使用（Agent SDK）：**

```typescript:src/appendix-c/claudecode/ecosystem.md
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

### 典型自动化工作流

```bash:terminal
# 代码审查（自动化审查循环）
claude -p "审查最近的变更，检查安全漏洞和代码质量问题"

# 自动化测试与修复（修复循环）
claude -p "运行测试套件，分析失败测试，修复它们" \
  --allowedTools "Bash,Edit,Read" \
  --permission-mode dontAsk

# 多代理协作（子 Agent 编排）
claude --agent "backend-architect" "设计微服务架构"

# 文档生成（批处理循环）
claude -p "为这个项目生成全面的 API 文档和 README"
```

### 子 Agent 与工作流工具

| 项目 | 说明 | 在 Loop Engineering 中的角色 |
|------|------|---------------------------|
| **SuperClaude_Framework**（SuperClaude-Org） | 30 个斜杠命令 + 16 个代理 + 7 种行为模式 | 预置编排模板 |
| **crystal** | 并行 worktree 会话管理，支持并发分支开发 | 工作树隔离 |
| **claudekit** | 自动保存检查点 + 20+ 专业子代理 | 检查点 + 子代理编排 |
| **claude-code-tools** | 会话连续性工具 + 跨代理交接 | 跨会话持久化 |
| **claude-toolbox** | 开发环境启动模板 | 环境标准化 |

### 跨工具 MCP 封装器

| 项目 | 描述 | 在循环工程中的价值 |
|------|------|-----------------|
| **cc-mcp**（csbrandt） | 封装 Claude Code CLI 为 MCP 服务器，支持 OpenCode | 跨工具编排 |
| **claude-code-mcp**（steipete） | 一次性 MCP 模式的 Claude Code | 轻量嵌入调用 |
| **ai-cli-mcp**（mkXultra） | 支持 Claude、Codex、Gemini、Forge、OpenCode 的统一 MCP | 多工具统一接口 |

---

## 扩展集成生态

### MCP 服务器生态

**安装方式：**

```bash:terminal
# 远程 HTTP 服务器
claude mcp add --transport http notion https://mcp.notion.com/mcp

# 本地 stdio 服务器
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub --dsn "postgresql://..."

# 从 Claude Desktop 导入
claude mcp add-from-claude-desktop
```

**作用域管理：**

| 作用域 | 存储位置 | 团队共享 | 说明 |
|--------|----------|----------|------|
| Local（默认） | `~/.claude.json` | 否 | 当前项目，个人 |
| Project | `.mcp.json` | 是 | 版本控制共享 |
| User | `~/.claude.json` | 否 | 所有项目 |

**常用 MCP 服务器：**

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

### Skills 生态

Skills 作为可复用指令集，在 Harness Engineering 中扮演"质量门禁"角色，在 Loop Engineering 中扮演"可复用执行模板"角色：

| 项目 | Stars | 规模 | 工程化优势 |
|------|-------|------|-----------|
| **antigravity-awesome-skills**（sickn33） | 32.5K | 1,400+ 可安装技能 | 覆盖面最广 |
| **awesome-agent-skills**（VoltAgent） | 15.4K | 1,000+ 跨代理兼容技能 | 跨工具复用 |
| **awesome-claude-skills**（travisvn） | 11.1K | 渐进式架构说明 | 学习路径清晰 |
| **awesome-claude-code-subagents**（VoltAgent） | 17.1K | 126+ 专业子代理 | 编排模板就绪 |
| **claude-skills**（Jeffallan） | — | 66 个全栈开发技能 | 全栈覆盖 |
| **claude-skills**（alirezarezvani） | — | 169 个生产就绪技能 | 生产就绪 |

### 定价与订阅

| 方案 | 价格 | 特点 |
|------|------|------|
| Claude Pro | $20/月 | 基础 Claude Code 访问 |
| Claude Max 5x | $100/月 | 更高用量限额 |
| Claude Max 20x | $200/月 | 大量使用场景 |
| API 按量付费 | 按 token | 适合脚本/CI 场景 |

---

## 社区精选项目

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

按工程化价值分类：

| 项目 | Stars | 工程化分类 | 描述 |
|------|-------|-----------|------|
| **everything-claude-code**（affaan-m） | 141.9K+ | 配置聚合 | 全面的 Claude Code 配置集合 |
| **awesome-claude-skills**（ComposioHQ） | 53.4K | 技能聚合 | Claude Skills 精选 + 500+ 外部应用集成 |
| **awesome-claude-code**（hesreallyhim） | 45.7K | 资源精选 | 最大的 Claude Code 资源精选列表 |
| **antigravity-awesome-skills**（sickn33） | 32.5K | 技能聚合 | 1,400+ 可安装技能 |
| **awesome-claude-code-subagents**（VoltAgent） | 17.1K | 编排模板 | 126+ 专业子代理 |
| **awesome-claude-code**（subinium） | 15K+ | 资源精选 | 1,000+ Stars 项目的精选列表 |
| **awesome-agent-skills**（VoltAgent） | 15.4K | 技能聚合 | 1,000+ 跨代理兼容技能 |
| **awesome-claude-skills**（travisvn） | 11.1K | 技能聚合 | 渐进式架构说明 |
| **claude-code-system-prompts**（piebald-ai） | 8.6K | 逆向分析 | Claude Code 系统提示词分析 |
| **awesome-claude-plugins**（ComposioHQ） | 1.6K+ | 插件聚合 | 生产就绪的插件精选 |

### 工具与框架

| 名称 | 说明 |
|------|------|
| **claudekit** | 自动保存检查点 + 20+ 专业子代理 |
| **claude-code-tools** | 会话连续性工具 + 跨代理交接 |
| **claude-toolbox** | 开发环境启动模板 |
| **crystal** | 并行 worktree 会话管理 |
| **container-use**（Dagger） | 安全的代理容器沙箱 |

### 推荐学习资源

| 资源 | 说明 |
|------|------|
| Claude Code 官方文档 | [docs.anthropic.com](https://docs.anthropic.com) |
| awesome-claude-code | 最大的 Claude Code 资源精选（45.7K Star） |
| claude-code-system-prompts | 系统提示词逆向分析（8.6K Star） |

## 迁移指南

从其他 AI 编程工具迁移到 Claude Code 时，需要关注以下关键差异：

### 从 OpenCode 迁移

- **AGENTS.md → CLAUDE.md**：OpenCode 的 `AGENTS.md` 项目指令在 Claude Code 中对应 `CLAUDE.md`，格式大部分兼容。需注意 Claude Code 不支持 Mermaid 图表和 OMO 扩展语法，需移除或替换为纯文本描述
- **Plugin → Skills + Hooks**：OpenCode 的 **Plugin（插件）**（TypeScript API）在 Claude Code 中没有直接对应——Claude Code 的扩展体系使用 JSON 和 Shell 脚本。Plugin 中的 Hook 逻辑需重构为 Claude Code 的外部 Shell Hook 或 MCP 工具
- **Category → Subagent**：OMO Category 系统定义的 Agent 行为需重写为 Claude Code 的 `AGENTS.md` 中 `@agents` 块或独立的 `.mdc` 文件。Category 的模型/工具组合需手动分配到对应 Subagent
- **命令习惯**：OpenCode 的 `/compact`、`/undo` 等命令在 Claude Code 中存在对应版本（`/compact`、`/undo`），但功能范围和参数不同

### 从 Pi Agent 迁移

- **Extension → Hooks + MCP**：Pi Agent 的 Extension（TypeScript 函数）在 Claude Code 中可拆为外部 Hook（Shell 脚本）和 MCP 工具两部分。需要监听生命周期用 Hook，提供外部能力用 MCP
- **Provider 配置**：Pi Agent 支持 20+ Provider；Claude Code 仅支持 Anthropic 提供的 Claude 系列模型。迁移后模型选择范围大幅缩小
- **命令体系**：Pi Agent 的 `/model`、`/system` 等命令在 Claude Code 中没有直接对应，需通过 `CLAUDE.md` 配置预设系统提示词来替代
- **迁移前提**：如果项目需要多模型支持或复杂 Plugin 生态，建议先评估 OpenCode 或保留 Pi Agent

## 相关章节

- → [Claude Code 内置能力](./capabilities.md) — 命令、工具、配置方式的完整参考
- → [OpenCode 生态参考](../../appendix-b/opencode/ecosystem.md) — OpenCode 开源生态对比
- → [MCP 服务器](../../06-advanced/mcp-servers.md) — MCP 协议在 OpenCode 中的配置和实践
- → [生态对比](../../01-introduction/ecosystem-comparison.md) — AI 编程工具生态全景

---

## 读者视角

### 适用读者角色
- 入门开发者 — 需要快速上手 Claude Code 的 Agent 体系
- 智能体开发工程师 — 需要设计、调试、进化 Claude Code 中的自定义 Agent 和 Subagent
- 效率开发者 — 已有 AI 工具经验，想通过 Claude Code 提升 2x+ 效率
- 技术负责人 — 需要评估 Claude Code 的技术可行性和团队级 Harness Engineering 体系
- **Skill（技能）**作者 — 需要开发自定义 Skill 和 MCP 桥接，实现团队最佳实践复用

### 典型使用场景
- 需要查找 Claude Code 社区扩展和最佳实践
- 需要了解 MCP 服务器生态和集成工作流
- 需要评估 Claude Code 与 OpenCode 的生态对比
- 需要查找官方和社区资源
- 需要进行工具迁移和对比

### 使用示例
```bash
# 查找 MCP 服务器
claude mcp list

# 添加 MCP 服务器
claude mcp add --transport http notion https://mcp.notion.com/mcp

# 配置 Hook
claude /hooks

# 打包插件
claude plugin validate ./my-plugin --strict

# 启动 Claude Code
claude
```

### 工程化示例

**配置顺序检查表：**

1. **第1步：MCP 服务器配置**
   ```json
   // .claude/settings.json
   {
     "mcpServers": {
       "github": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-github"],
         "env": {
           "GITHUB_TOKEN": "ghp_..."
         }
       }
     }
   }
   ```

2. **第2步：Hook 配置**
   ```json
   // .claude/settings.json
   {
     "hooks": {
       "PostToolUse": {
         "command": "node",
         "args": [".claude/hooks/validate-output.js"],
         "timeout": 10000
       }
     }
   }
   ```

3. **第3步：插件打包**
   ```bash
   # 验证插件
   claude plugin validate ./my-plugin --strict
   
   # 安装插件
   claude plugin install ./my-plugin
   ```

### 与前/后文章的衔接
- ← [Claude Code 内置能力](./capabilities.md) — 命令、工具、配置方式的完整参考
- → [OpenCode 生态参考](../../appendix-b/opencode/ecosystem.md) — OpenCode 开源生态对比

---

## 常见反模式

### 盲目安装大量 MCP 服务器而不评估性能影响

Claude Code 生态中有 9,000+ MCP 服务器，许多开发者倾向于安装尽可能多的 MCP 服务器来"扩展能力"。但每个 MCP 服务器在启动时都需要建立进程间通信连接，在每次工具发现时都会增加系统提示词的大小。安装 10 个 MCP 服务器后，Claude Code 的启动延迟可能从 2 秒增加到 10 秒以上，且系统提示词膨胀会压缩实际可用的上下文窗口。

应该按实际使用频率评估 MCP 服务器的必要性。把 MCP 服务器分为"每次会话都需要"（如 GitHub）、"偶尔使用"（如 Notion）、"很少使用"（如 Stripe）三类。只加载第一类到项目级配置（`.mcp.json`），第二类和第三类通过 `claude mcp add` 按需手动添加。

### 从社区模板复制 CLAUDE.md 而不理解其原理

社区提供的 CLAUDE-template 和 awesome-claude-code 资源非常有价值，但直接复制粘贴最大的模板而不理解每条规则的作用，会导致 CLAUDE.md 包含与你项目无关的约束。例如，一个 Python 项目可能包含了 TypeScript 的格式化规则，或者一个单体应用包含了微服务架构的约定。

使用社区模板作为起点，但必须逐条审查和裁剪。删除与你项目技术栈不匹配的规则，修改路径引用使其指向你的实际目录结构。最好的 CLAUDE.md 是从零开始编写、只包含你项目独特约束的文件，社区模板的价值在于提供"应该考虑哪些方面"的思路。

### 在 CI/CD 中不使用 --bare 模式

在 CI/CD 流水线中使用 `claude -p "query"` 时，如果不加 `--bare` 标志，Claude Code 会尝试加载所有 hooks、skills、plugins 和 MCP 服务器配置。这在 CI 环境中通常是不必要的——CI 只需要执行特定的自动化任务，不需要团队的个人 Skills 和 Hook 配置。加载这些内容会增加启动延迟，且可能因为 CI 环境缺少依赖而报错。

CI/CD 场景应该使用 `claude --bare -p "query"` 跳过所有扩展加载，只保留核心能力。如果需要特定工具（如 GitHub MCP），单独用 `--allowedTools` 指定即可。

## 适用场景与限制

### Claude Code 生态仅覆盖 Claude 模型生态

Claude Code 的生态紧密围绕 Anthropic 产品体系，MCP 协议虽然是开放标准，但 Claude Code 的核心价值（CLAUDE.md、Skills、Subagents）都深度绑定 Claude 模型。如果你的团队主要使用 GPT-4o、Gemini 或本地模型，Claude Code 生态中的大部分最佳实践和社区资源都不直接适用。

对于多模型团队，建议以 OpenCode 为主力工具，Claude Code 作为特定 Claude 模型场景的补充。OpenCode 完全兼容 MCP 协议，可以复用 Claude Code 社区的 MCP 服务器实现。

### 社区扩展的质量和维护状态参差不齐

awesome-claude-code 等资源列表收录了大量社区项目，但项目的维护状态差异很大。部分项目可能已经停止更新、与最新版 Claude Code 不兼容、或者存在安全漏洞。安装一个长期未维护的 MCP 服务器可能引入已知的安全风险。

安装社区扩展前，检查 GitHub 仓库的最近提交日期、Issue 响应速度和 Star 增长趋势。优先选择 Anthropic 官方维护的 MCP 服务器和近期活跃的社区项目。对于生产环境，建议 fork 社区项目到自己的仓库，确保可以控制更新节奏。

### Skills 生态与 OpenCode Skill 不完全兼容

Claude Code 的 Skills 和 OpenCode 的 Skills 都遵循 SKILL.md + YAML frontmatter 的格式，但两者在 frontmatter 字段、加载机制和执行模式上存在差异。Claude Code 的 Skills 支持 `context: fork` 隔离执行和 `allowed-tools` 工具授权，而 OpenCode 的 Skills 通过触发词匹配和 Category 路由。直接将 OpenCode 的 SKILL.md 复制到 Claude Code 中可能无法正常工作。

跨工具复用 Skills 时，需要检查 frontmatter 字段的兼容性。保留 `name` 和 `description`（两者通用），调整 `allowed-tools` 等工具特定字段。推荐的做法是维护一份核心指令的 Markdown 正文，在两个工具中分别配置各自的 frontmatter。

## 常见失败与陷阱

### 从 OpenCode 迁移时遗漏 Plugin 中的 Hook 逻辑

从 OpenCode 迁移到 Claude Code 时，许多团队只迁移了 AGENTS.md 中的规则，却忽略了 Plugin 中的 Hook 逻辑。OpenCode 的 Plugin 可以在 Agent 进程内部以 TypeScript 函数拦截任意行为（53+ Hook 点），而 Claude Code 的 Hook 只能通过 Shell 脚本在外部执行。Plugin 中的复杂验证逻辑（如跨文件一致性检查、数据库状态验证）无法直接迁移。

迁移前需要审计所有 OpenCode Plugin 的 Hook 实现，按功能分类：简单的文件操作和命令执行可以迁移到 Claude Code 的 Shell Hook；复杂的运行时逻辑需要重构为 MCP 工具或 Agent SDK 的编程式 Hook。建议制作一份 Hook 迁移对照表，逐个验证功能等价性。

### MCP 服务器的 OAuth 配置在团队间不一致

通过 `claude mcp add --transport http` 添加的远程 MCP 服务器可能需要 OAuth 认证。不同团队成员的 OAuth Token 刷新策略可能不同，导致部分成员的 MCP 连接频繁断开。更糟的是，OAuth 凭据可能存储在 `~/.claude.json` 中，不会通过 Git 共享，新加入团队的成员需要手动重新配置。

推荐使用项目级的 `.mcp.json` 文件管理 MCP 服务器配置，将不需要 OAuth 的服务器（如本地 stdio 服务器）纳入版本控制。对于需要认证的远程服务器，在团队文档中明确记录配置步骤，或者使用环境变量注入 Token（如 `${GITHUB_TOKEN}`）。

### Skills 目录结构不规范导致自动发现失败

Claude Code 按特定目录结构自动发现 Skills（`~/.claude/skills/<name>/SKILL.md` 或 `.claude/skills/<name>/SKILL.md`）。如果目录层级不正确（比如把 SKILL.md 直接放在 `.claude/skills/` 而非子目录中），或者文件名不是 `SKILL.md`，自动发现机制会静默跳过，不产生任何错误提示。

创建新 Skill 时，严格遵循目录结构规范。使用 `/skills` 命令验证 Skill 是否被正确识别。如果 Skill 安装后没有出现在列表中，首先检查目录层级和文件名是否正确，然后检查 YAML frontmatter 的 `name` 和 `description` 字段是否完整。
