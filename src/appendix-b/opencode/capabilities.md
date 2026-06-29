# OpenCode 内置能力

OpenCode 是一个终端原生的 AI 编程助手，支持多种 LLM Provider，内置丰富的命令、工具和扩展机制。本章是 OpenCode 能力的**全景索引**——每项能力的详细参考在对应子章节。

## 设计哲学

OpenCode 的核心设计理念：**让 AI 在你的终端里干活，而不是替你干活**。它不是一个黑盒 IDE 插件，而是一个透明的协作环境。你能看到 AI 的每一步操作，随时介入，随时纠正。

<!-- mdBook TOC 会自动生成目录，此处不需要手动列出子章节 -->

## 命令系统

OpenCode 的命令以 `/` 开头，在输入框中直接输入即可执行。命令分为三类：

- **核心内置命令**：由 OpenCode 本体提供，覆盖项目初始化（`/init`）、会话管理（`/compact`、`/undo`）、模型切换（`/models`）、Provider 管理（`/connect`）等基础操作。
- **OMO 扩展命令**：由 oh-my-openagent 插件提供，包括自动化循环（`/ralph-loop`、`/ulw-loop`）、智能重构（`/refactor`）、对抗性规划（`/hyperplan`）等高级能力。
- **自定义命令**：通过 Markdown 文件或 JSON 配置创建，支持 `$ARGUMENTS`、`!shell`、`@file` 三种模板语法。

→ 完整命令列表、参数说明和示例见 [OpenCode 内置命令参考](./commands.md)。
→ 完整工具列表和用法见 [OpenCode 内置命令参考](./commands.md)。
→ OMO 完整 Agent 架构（含 11 个 Agent 详解、Category 系统、配置管道）见 [oh-my-openagent **Agent（智能体）** 设计与开发指南](./agent-architecture.md)。
→ Agent 设计哲学和基础类型体系见 [Agent 编排](../../02-core-concepts/agent-orchestration.md)。

## 工具集

OpenCode 内置了一套完整的工具集，涵盖文件操作（Read / Write / Edit / Glob）、命令执行（Bash）、搜索（Grep / AST-grep）、网络（WebSearch / WebFetch / GitHub Search）、代码分析（LSP）、任务管理（Task / Todo），以及 `apply_patch`、`skill`、`agent` 等辅助工具。

→ 完整工具列表和用法见 [OpenCode 内置命令参考](./commands.md)。
→ 官方文档参见 [opencode.ai/docs/tools](https://opencode.ai/docs/tools/)。

## **Agent（智能体）** 架构

OpenCode 采用多 Agent 架构：**Build**（默认主 Agent，完整权限）、**Plan**（只读主 Agent）、**General**（通用子 Agent）、**Explore**（只读探索子 Agent）、**Scout**（Web 检索子 Agent），以及若干系统级 Hidden Agent（Compaction / Title / Summary）。

→ OMO 完整 Agent 架构（含 11 个 Agent 详解、Category 系统、配置管道）见 [oh-my-openagent **Agent（智能体）** 设计与开发指南](./agent-architecture.md)。
→ Agent 设计哲学和基础类型体系见 [Agent 编排](../../02-core-concepts/agent-orchestration.md)。

## **Plugin（插件）** 系统

| 工具 | 功能 | 说明 |
|------|------|------|
| Grep | 正则内容搜索 | 按正则表达式搜索文件内容，支持结果模式切换 |
| AST-grep ¹ | 代码结构搜索 | 25 种语言支持，基于 AST 模式匹配（非正则） |

Plugin 通过 `opencode.json` 的 `plugins` 字段或文件系统加载，支持本地文件和 npm 包两种方式。

| 工具 | 功能 | 说明 |
|------|------|------|
| WebSearch | 网络搜索 | 通过 Exa 搜索引擎获取清洁内容 |
| WebFetch | URL 抓取 | 获取网页内容，支持 Markdown/Text/HTML 格式 |
| GitHub Search ¹ | GitHub 代码搜索 | 从百万开源仓库中搜索真实代码示例 |

## SDK 编程接口

| 工具 | 功能 | 说明 |
|------|------|------|
| LSP Diagnostics | 获取诊断信息 | 错误、警告、提示 |
| LSP Goto Definition | 跳转到定义 | 符号定义位置 |
| LSP Find References | 查找引用 | 符号的所有引用位置 |
| LSP Rename | 重命名符号 | 跨工作区重命名 |
| LSP Symbols | 文档/工作区符号 | 大纲视图和全局搜索 |
| CodeGraph ¹ | 代码图谱 | 调用链分析、影响范围、上下文构建 |

→ SDK 安装、API 参考和完整示例见 [OpenCode SDK：编程式 **Agent（智能体）** 开发](./agent-sdk.md)。

## **Skill（技能）** 系统

### OMO 扩展工具 ¹

由 oh-my-openagent 增强层提供，在标准 OpenCode 之上扩展更多内置工具：

| 工具 | 功能 | 说明 |
|------|------|------|
| apply_patch | 差异补丁应用 | 基于 diff 格式的精确补丁 |
| todoread | 待办读取 | 读取结构化待办事项 |
| question | 用户提问 | 向用户发起交互式提问 |
| batch | 批量执行 | 批量执行多个工具调用 |
| multiedit | 批量编辑 | 对多个文件进行批量编辑 |
| list | 文件列表 | 列出目录内容和文件结构 |
| codesearch | 代码搜索 | 基于语义的代码搜索 |

> ¹ AST-grep、CodeGraph、GitHub Search 和上表所列工具均由 oh-my-openagent 增强层提供，非 OpenCode 内置工具。

## Agent 类型

→ Skill 开发指南见 [Skill 开发](../../05-skills/)。

## **MCP（模型上下文协议）** 集成

MCP（Model **Context（上下文）** Protocol）是连接外部世界的标准化协议。通过 MCP，Agent 可以查询数据库、调用 API、搜索网络，支持 stdio / streamable-http / websocket 三种传输方式。

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

## MCP 生态

MCP（Model Context Protocol）是 OpenCode 连接外部世界的标准化协议。通过 MCP，Agent 可以查询数据库、调用 API、搜索网络、操作文件系统，而不需要把这些能力硬编码到工具链里。

MCP 定义了三种交互原语（Tool / Resource / **Prompt（提示词）**），支持两种传输方式：

| 传输类型 | 适用场景 | 特点 |
|----------|----------|------|
| stdio | 本地子进程 | 低延迟、高安全 |
| streamable-http | 远程服务 | 灵活部署，跨网络调用 |

MCP 服务器可以配置 OAuth 认证，保护远程服务的访问权限。OpenCode 在 `opencode.json` 的 `mcpServers` 字段中管理所有 MCP 连接，包括认证信息。

→ [MCP 服务器](../../06-advanced/mcp-servers.md) 章节有完整的 MCP 开发和配置指南。

## 社区生态

OpenCode 的生态由社区驱动，涵盖 Skills、配置模板、插件和示例文件。社区贡献的 Skills 可以通过 `skills-download` 命令安装，也可以直接从 GitHub 仓库克隆。Skills 按领域分类，覆盖开发框架、安全测试、思维模型、工作流等场景。

### 示例文件

`examples/` 目录包含 74 个示例文件，按功能类别组织：

| 目录 | 内容 |
|------|------|
| opencode-configs/ | 权限、Provider、路由、合规配置 |
| skills/ | SKILL.md 结构和最佳实践 |
| workflows/ | 多步骤任务编排 |
| quality-gates/ | 自动化检查规则 |
| ast-grep-rules/ | 代码结构匹配模式 |

### 版本参考

本书基于 OpenCode v1.17.x 和 oh-my-openagent v4.13.x 编写。

## 配置体系

OpenCode 的配置以 `opencode.json` 为核心，支持全局（`~/.config/opencode/`）、项目（`./`）、环境（`opencode.{env}.json`）三层继承，定义 Provider、权限、MCP 服务器等全局设置。

→ 配置详解见 [OpenCode 配置深度解析](../../03-setup/opencode-config.md)。

## 社区生态

社区驱动的开源生态，涵盖 Skills、配置模板、MCP 服务器等资源。社区 Skill 可通过 `skills-download` 命令安装，`examples/` 目录包含 74+ 个示例文件。

→ 社区资源列表见 [生态参考](./ecosystem.md)。

---

## 读者视角

### 适用读者角色
- 入门开发者 — 适合快速上手 OpenCode 的基础能力，了解核心概念和常用命令
- 智能体开发工程师 — 需要设计、调试、进化 AI 编码智能体，建立系统化的 Agent 工程体系
- 效率开发者 — 已用 AI 工具，想掌握 Agent 编排和工作流模式，提升日常开发效率 2x+
- 技术负责人 — 团队技术决策者，关注标准化，建立团队级 **Harness Engineering（驾驭工程）** 体系
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

## 常见反模式

使用 OpenCode 内置能力时，以下反模式会导致效率不升反降：

**万能 Agent 幻觉**：认为一个 Agent 可以同时处理编程、写作、数据分析、设计等所有任务。OpenCode 的 Category 系统和子 Agent 机制正是为专业化分工设计的。正确的做法是定义多个专用 Agent（代码审查 Agent、架构设计 Agent、测试 Agent 等），每个只专注一个领域，通过编排实现复杂流程。

**配置过载**：在 `opencode.json` 中堆砌所有可用配置项，包括从不需要的功能。例如同时配置 5 个 MCP 服务器、加载 10 个 Skill、定义 15 个 Hook。这不仅降低启动速度，还增加 Agent 决策噪音。应以最小必要原则配置：只加载当前项目真正需要的扩展。

**Hook 链过深**：在一个事件上注册多个 Hook，且 Hook 之间互相触发形成依赖链。例如 `PostToolUse` Hook 触发检查、检查触发日志、日志触发告警，中间任何一个环节失败都可能导致整条链断裂。Hook 应设计为独立、幂等的处理单元，避免级联依赖。

## 常见错误与陷阱

**Skill 与 Plugin 混淆**：不清楚 Skill 是声明式指令（Markdown 写"做什么"），而 Plugin 是编程式扩展（TypeScript 写"怎么做"）。错误地将需要编程逻辑的扩展写成 Skill（结果无法满足），或者将纯配置指令写成 Plugin（过度工程）。选型原则：能靠规则说清楚的用 Skill，需要代码逻辑的用 Plugin。

**MCP 服务器配置不当**：为每一项数据需求都单独配置一个 MCP 服务器，忽略 OpenCode 内置的文件读取（Read/Glob/Grep）工具。内置工具已经提供高效的本地文件访问，只有需要外部 API 或数据库访问时才需要 MCP。

**tignore 滥用**：在 `opencode.json` 的 `ignore` 列表中排除过多目录，导致 Agent 无法看到项目全貌。常见错误是排除 `node_modules` 以外的所有生成目录，结果 Agent 无法读取 `dist/` 下的构建产物或 `coverage/` 下的测试报告。应只排除确实不需要 Agent 接触的目录（如敏感配置、凭据文件）。

## 适用场景与限制

**适用场景**：OpenCode 最适合需要高度定制化 AI 编码体验的工程团队。多模型支持让团队可以根据任务选择最合适的 LLM（大模型做架构、小模型做格式化）；Plugin + Skill + MCP 三层扩展体系覆盖从配置规则到全功能扩展的所有需求；Category 子 Agent 系统适合需要专业化分工的复杂项目。

**不适用场景**：如果团队只需要一个开箱即用的 AI 编码助手、不需要定制扩展，OpenCode 的灵活性和复杂度反而成为负担。此时 Claude Code 的简洁设计可能更合适。同理，如果项目只有单一模型需求、不需要多模型混排，OMO 的 Category 编排优势不能充分发挥。

**限制说明**：OpenCode 的终端原生 UI 对偏好图形化 IDE 的开发者有学习曲线。Plugin 开发需要 TypeScript 能力，Skill 编写需要了解 Markdown 模板和指令语法。多模型切换虽然灵活，但不同模型的行为差异可能导致结果不一致，需要额外的 prompt 适配工作。

### 与前/后文章的衔接
- ← [OpenCode 内置能力](./capabilities.md) — 了解 OpenCode 的核心功能和能力
- → [OpenCode 内置命令参考](./commands.md) — 详细了解每个命令的用法和参数
