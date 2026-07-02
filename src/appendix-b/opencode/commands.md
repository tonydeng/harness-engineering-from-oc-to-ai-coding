# OpenCode 内置命令参考

> OpenCode 内置命令的完整参考手册，按功能分类，方便快速查阅。所有命令在对话输入框中以 `/` 开头输入即可触发。

OpenCode 提供了两大类命令：**核心内置命令**（Core Commands）由 OpenCode 本体提供，覆盖项目初始化、会话管理、模型配置等基础操作；**OMO 扩展命令**（oh-my-openagent Extended Commands）由 oh-my-openagent 插件提供，增加了自动化循环、智能重构、代码质量治理等高级能力。此外，OpenCode 支持通过 Markdown 文件或 JSON 配置创建自定义命令（Custom Commands）。

→ [工作流模式](../../02-core-concepts/workflow-patterns.md) 详细讲解 Command 系统的设计原理。
→ [oh-my-openagent 集成](../../03-setup/oh-my-openagent-setup.md) 介绍 OMO 的安装与配置。

---

## Core Commands（核心命令）

### 项目初始化

| 命令 | 别名 | 功能 | 典型场景 |
|------|------|------|----------|
| `/init` | — | 扫描项目结构，生成 AGENTS.md 项目知识库 | 新项目首次打开 |
| `/help` | — | 显示可用命令和快捷键列表 | 不确定命令时查看帮助 |

**`/init`** 是 OpenCode 工程化的起点。执行后，它会扫描项目目录结构、识别技术栈、生成包含项目概述的 AGENTS.md 文件，让 **Agent（智能体）** "认识"你的项目。

→ [AGENTS.md 约定系统](../../06-advanced/agents-dot-md.md) 讲解生成的文件结构和如何手动扩展。

### 会话管理

| 命令 | 别名 | 功能 | 典型场景 |
|------|------|------|----------|
| `/new` | `/clear` | 新建空白会话，清除当前上下文 | 开始新任务，或上下文混乱时重置 |
| `/sessions` | `/resume`、`/continue` | 列出历史会话，选择恢复 | 中断工作后继续，或切换任务 |
| `/compact` | `/summarize` | 压缩当前上下文，保留关键信息 | 上下文接近窗口上限时 |
| `/export` | — | 将当前会话导出为 Markdown 文件 | 保存调试记录或分享排查过程 |
| `/share` | — | 导出会话链接，方便他人查看 | 协作排查 Bug 或代码审查 |
| `/undo` | — | 撤销上一步操作（文件修改、命令执行） | 回滚错误的文件修改 |
| `/redo` | — | 重做被撤销的操作 | 恢复误撤销的修改 |

**上下文压缩**（Compaction）是长会话的必备技能。当对话轮次增多、上下文接近 Token 窗口上限时，`/compact` 会触发后台 Agent 分析当前对话，生成摘要并保留关键信息，释放 Token 空间。

→ [上下文压缩与Token 预算](../../06-advanced/context-compression.md) 深入讲解压缩机制和触发策略。
→ [上下文压缩与Token 预算](../../06-advanced/context-compression.md) 讲解如何合理分配有限的 Token 空间。

### 模型与配置

| 命令 | 功能 | 典型场景 |
|------|------|----------|
| `/models` | 列出可用模型，切换当前模型 | 需要更强推理能力时切换到旗舰模型 |
| `/connect` | 添加新的 LLM Provider | 接入新的模型供应商（如国产模型） |
| `/themes` | 切换界面主题 | 个性化界面风格 |
| `/editor` | 打开编辑器，编辑当前对话内容 | 精确修改长 **Prompt（提示词）** |
| `/details` | 显示最近一次工具调用的详细信息 | 排查工具执行结果 |
| `/thinking` | 切换推理过程的显示状态 | 查看 Agent 的思考链路 |
| `/exit` | 退出 OpenCode | 结束工作 |

→ [国产模型供应商配置](../../03-setup/chinese-providers.md) 介绍如何通过 `/connect` 接入国内模型。
→ [OpenCode 配置深度解析](../../03-setup/opencode-config.md) 讲解所有配置项的含义。

---

## oh-my-openagent Extended Commands（OMO 扩展命令）

oh-my-openagent（简称 OMO）是 OpenCode 的增强插件，提供了 9 个扩展命令。安装 OMO 后，这些命令自动可用。

→ [oh-my-openagent 集成](../../03-setup/oh-my-openagent-setup.md) 介绍安装方法。

### 自动化循环

| 命令 | 功能 | 适用场景 |
|------|------|----------|
| `/ralph-loop` | 启动自引用开发循环，Agent 自主执行直到完成 | 明确的任务，需要持续执行到完成 |
| `/ulw-loop` | 启动 Ultrawork 模式循环，持续工作直到完成 | 复杂任务，需要多轮迭代 |
| `/cancel-ralph` | 取消当前活跃的 Ralph Loop 或 Ultrawork Loop | 需要中断自动执行时 |

**Ralph Loop** 和 **Ultrawork Loop** 都是持续执行机制，区别在于 Ralph Loop 偏向自引用（Agent 自我评估进度），Ultrawork Loop 偏向任务驱动（按预设计划推进）。

→ [Ultrawork 模式](../../04-workflows/ultrawork-mode.md) 讲解 Ultrawork 的设计哲学和使用策略。
→ [Prometheus 规划模式](../../04-workflows/prometheus-mode.md) 介绍配合 `/start-work` 使用的规划模式。

### 代码质量

| 命令 | 功能 | 适用场景 |
|------|------|----------|
| `/refactor` | 智能重构，结合 LSP、AST 分析和架构评估 | 需要安全地重构代码结构 |
| `/remove-ai-slops` | 移除 AI 生成的代码异味，分类清理 10 类问题 | 代码审查后清理 AI 生成的低质量模式 |

**`/refactor`** 会自动分析代码结构、查找引用关系、评估影响范围，然后执行重构。它集成了 Language Server Protocol（LSP）和 AST（抽象语法树）分析，确保重构不会破坏现有功能。

**`/remove-ai-slops`** 专注于清理 AI 编程工具生成的常见代码异味（Slop），包括：过度注释、不必要的封装、冗余的错误处理、不一致的命名风格等。它先锁定回归测试，再分批清理，最后验证质量门禁。

→ [验证护栏体系](../../02-core-concepts/validation-harness.md) 讲解重构和清理背后的质量保障机制。

### 任务执行

| 命令 | 功能 | 适用场景 |
|------|------|----------|
| `/start-work` | 从 Prometheus 计划开始执行工作 | 已完成规划，准备进入执行阶段 |
| `/hyperplan` | 启动对抗性多 Agent 规划，5 个 Agent 交叉评审 | 重要决策前，需要多视角评估方案 |

**`/start-work`** 配合 [Prometheus 规划模式](../../04-workflows/prometheus-mode.md) 使用。先通过 Prometheus 生成详细的实现计划，再用 `/start-work` 启动执行。

**`/hyperplan`** 是一种对抗性规划机制。5 个不同视角的 Agent 同时评审同一个方案，互相挑刺，最终综合出经过多轮攻防的高质量计划。

→ [多 Agent 协作](../../04-workflows/multi-agent-collab.md) 讲解多 Agent 通信和协调机制。
→ [Agent 派生模式](../../04-workflows/agent-derivation.md) 介绍 Agent 如何根据任务动态生成子 Agent。

### 会话续接

| 命令 | 功能 | 适用场景 |
|------|------|----------|
| `/handoff` | 创建上下文摘要，用于新会话续接 | 会话过长需要重开，但不想丢失进度 |
| `/stop-continuation` | 停止所有续接机制（Ralph Loop、Ultrawork、Todo 续接） | 需要完全停止自动续接行为 |

**`/handoff`** 生成一份结构化的上下文摘要，包含已完成的工作、待处理的任务、关键决策记录等。新会话中导入这份摘要即可无缝续接。

→ [上下文工程核心](../../02-core-concepts/context-engineering-core.md) 讲解上下文管理的设计哲学。

---

### 功能规格工具包（Speckit）

Speckit 系列命令提供从需求澄清到实现验证的全流程规格管理能力，适合需要结构化功能开发的团队：

| 命令 | 功能 | 适用场景 |
|------|------|----------|
| `/speckit.constitution` | 创建/更新项目章程 | 新项目启动时定义编码原则和团队规范 |
| `/speckit.clarify` | 识别规格中的模糊点并提问 | 需求不明确时自动追问澄清 |
| `/speckit.specify` | 从自然语言生成功能规格 | 将需求描述转化为结构化的规格文档 |
| `/speckit.plan` | 根据规格生成实现计划 | 将规格分解为有依赖关系的实现步骤 |
| `/speckit.tasks` | 生成可执行任务列表 | 从设计产物生成细粒度的开发任务 |
| `/speckit.taskstoissues` | 将任务转为 GitHub Issues | 将任务列表自动创建为 GitHub issues |
| `/speckit.implement` | 按任务列表依次执行实现 | 自动化执行 tasks.md 中的所有任务 |
| `/speckit.converge` | 检查代码与规格的差距 | 验证已实现的功能是否符合原定规格 |
| `/speckit.analyze` | 跨产物一致性分析 | 检查 spec/plan/tasks 之间的内容一致性 |
| `/speckit.checklist` | 根据需求生成检查清单 | 将验收标准转化为可勾选的检查项 |
| `/speckit.agent-context.update` | 刷新 Agent 上下文中的 Speckit 部分 | 在多会话工作中保持规格信息同步 |

**工作流示例**：一个完整的功能开发流通常按以下顺序使用 Speckit 命令：

```text:terminal
/speckit.clarify         → 澄清模糊需求
/speckit.specify         → 生成功能规格
/speckit.plan            → 制定实现计划
/speckit.tasks           → 分解为执行任务
/speckit.implement       → 自动化执行实现
/speckit.converge        → 验证实现完整性
```

### 持久记忆系统（Supermemory）

Supermemory 系列命令提供跨会话的持久记忆管理能力，适用于需要长期积累项目知识的场景：

| 命令 | 功能 | 适用场景 |
|------|------|----------|
| `/supermemory-init` | 用代码库知识初始化记忆 | 首次使用时构建项目知识索引 |
| `/supermemory-login` | 通过浏览器登录 Supermemory | 首次使用或凭证过期时需要认证 |
| `/supermemory-logout` | 退出登录并清除凭证 | 在共享设备上使用后退出 |
| `/supermemory-status` | 查看连接状态 | 确认记忆系统是否正常运行 |

→ [记忆系统设计](../../06-advanced/memory-system.md) 讲解 Supermemory 的架构和使用策略。

---

## Custom Commands（自定义命令）

OpenCode 支持用户创建自己的命令。两种方式各有优势，Markdown 文件方式更适合团队协作，JSON 配置方式更适合精细控制。

→ [工作流模式 · Command 系统](../../02-core-concepts/workflow-patterns.md) 讲解完整的 Command 设计原理。

### 创建方式

#### 方式一：Markdown 文件（推荐）

在 `.opencode/commands/` 目录下创建 Markdown 文件，文件名即为命令名：

```text:terminal
.opencode/
└── commands/
    ├── review-pr.md      → /review-pr
    ├── search.md         → /search
    └── review/
        ├── security.md   → /review:security
        └── performance.md → /review:performance
```

将 `.opencode/commands/` 目录提交到 Git，团队成员克隆仓库后即可使用所有自定义命令。

**优势**：版本控制友好，团队共享方便，Markdown 格式可读性强。

#### 方式二：opencode.json 配置

在 `opencode.json` 的 `command` 字段中定义：

```json:examples/opencode-configs/basic.jsonc
{
  "command": {
    "test-coverage": {
      "template": "运行测试并生成覆盖率报告，标记覆盖率低于 80% 的文件",
      "description": "测试覆盖率检查",
      "agent": "build",
      "model": "anthropic/claude-sonnet-4-20250514"
    }
  }
}
```

**优势**：可以指定 Agent 类型和模型，适合需要精确控制执行环境的命令。

### 模板语法

自定义命令支持三种模板语法（Template Syntax），实现动态内容注入：

| 语法 | 功能 | 示例 |
|------|------|------|
| `$ARGUMENTS` | 命令参数替换，调用时传入的内容会替换占位符 | `/search $ARGUMENTS` |
| `!shell` | Shell 命令输出，执行时动态获取结果 | `!git branch --show-current` |
| `@file` | 文件内容引用，将指定文件完整注入 Prompt | `@docs/api-spec.md` |

**`$ARGUMENTS` 示例**：

```markdown:.opencode/commands/search.md
# search

在代码库中搜索 $ARGUMENTS，返回匹配的文件和行号。
使用 ripgrep 进行高效搜索，忽略 node_modules 和 .git 目录。
```

调用方式：`/search API_KEY`，Agent 会将 `$ARGUMENTS` 替换为 `API_KEY`。

**`!shell` 示例**：

```markdown:.opencode/commands/branch-status.md
# branch-status

当前分支：!git branch --show-current
最近提交：!git log -1 --oneline
未提交变更：!git status --short
```

每次执行 `/branch-status` 时，Shell 命令会被动态执行，返回当前 Git 状态。

**`@file` 示例**：

```markdown:.opencode/commands/implement-api.md
# implement-api

根据以下 API 规范实现接口：

@docs/api-spec.md

请遵循项目的编码规范，并添加单元测试。
```

`@file` 语法会将指定文件的完整内容注入到 Prompt 中，适合引用规范文档、API 定义等。

### 高级特性

#### 指定 Agent

通过 YAML frontmatter（前置元数据）指定执行命令的 Agent 类型：

```markdown:.opencode/commands/analyze-architecture.md
---
agent: plan
---

# analyze-architecture

分析当前项目的架构设计，输出架构图和改进建议。
```

设置 `agent: plan` 后，该命令会在只读的 Plan Agent 中执行，不会修改文件。

#### 指定模型

为特定命令指定使用的模型：

```markdown:.opencode/commands/complex-refactor.md
---
model: claude-opus-4
---

# complex-refactor

执行复杂的重构任务，需要深度推理能力。
```

适合需要旗舰模型深度推理的复杂任务，日常命令可以省略此配置。

#### 子命令

支持 `command:subcommand` 形式的命令层级结构：

```bash:terminal
/review:security     # 安全审查
/review:performance  # 性能审查
/review:style        # 代码风格审查
```

在 `.opencode/commands/review/` 目录下创建子目录，目录名作为父命令，文件名作为子命令。

#### 团队共享命令库

建议的目录结构：

```text:terminal
.opencode/
├── commands/
│   ├── review/
│   │   ├── security.md
│   │   ├── performance.md
│   │   └── style.md
│   ├── deploy/
│   │   ├── staging.md
│   │   └── production.md
│   └── utils/
│       ├── branch-status.md
│       └── search.md
└── AGENTS.md
```

将 `.opencode/commands/` 目录提交到 Git，团队成员克隆仓库后即可使用所有自定义命令。无需额外安装或配置。

---

## 命令配置参考

以下汇总所有内置命令的配置速查表，方便快速查找。

### 核心命令速查

| 命令 | 别名 | 功能 | 需要 OMO |
|------|------|------|----------|
| `/init` | — | 生成 AGENTS.md 项目知识库 | 否 |
| `/help` | — | 显示帮助 | 否 |
| `/new` | `/clear` | 新建会话 | 否 |
| `/sessions` | `/resume`、`/continue` | 会话管理 | 否 |
| `/compact` | `/summarize` | 上下文压缩 | 否 |
| `/export` | — | 导出会话为 Markdown | 否 |
| `/share` | — | 导出会话链接 | 否 |
| `/undo` | — | 撤销上一步操作 | 否 |
| `/redo` | — | 重做撤销的操作 | 否 |
| `/models` | — | 模型列表与切换 | 否 |
| `/connect` | — | 添加 LLM Provider | 否 |
| `/themes` | — | 主题切换 | 否 |
| `/editor` | — | 编辑器 | 否 |
| `/details` | — | 工具调用详情 | 否 |
| `/thinking` | — | 推理过程显示 | 否 |
| `/exit` | — | 退出 OpenCode | 否 |

### OMO 扩展命令速查

| 命令 | 功能 | 所属类别 |
|------|------|----------|
| `/ralph-loop` | 自引用开发循环 | 自动化循环 |
| `/ulw-loop` | Ultrawork 模式循环 | 自动化循环 |
| `/cancel-ralph` | 取消活跃的循环 | 自动化循环 |
| `/refactor` | 智能重构（LSP + AST） | 代码质量 |
| `/remove-ai-slops` | 移除 AI 代码异味 | 代码质量 |
| `/start-work` | 从 Prometheus 计划开始执行 | 任务执行 |
| `/hyperplan` | 对抗性多 Agent 规划 | 任务执行 |
| `/handoff` | 创建上下文摘要用于续接 | 会话续接 |
| `/stop-continuation` | 停止所有续接机制 | 会话续接 |
| `/speckit.*` | Speckit 功能规格工具包（11 个命令） | 功能规格 |
| `/supermemory-*` | Supermemory 持久记忆系统（4 个命令） | 记忆管理 |

### 自定义命令配置速查

| 配置项 | 位置 | 说明 |
|--------|------|------|
| Markdown 文件 | `.opencode/commands/*.md` | 文件名即命令名 |
| JSON 配置 | `opencode.json` → `command` 字段 | 支持 template、description、agent、model |
| `$ARGUMENTS` | 模板内容中 | 调用时的参数替换 |
| `!shell` | 模板内容中 | 动态执行 Shell 命令 |
| `@file` | 模板内容中 | 引用外部文件内容 |
| `agent` | frontmatter | 指定执行 Agent 类型 |
| `model` | frontmatter | 指定使用的模型 |
| 子命令 | 目录层级 | `command:subcommand` 形式 |

---

## 读者视角

### 适用读者角色
- 入门开发者 — 适合快速上手 OpenCode 的基础能力，了解核心概念和常用命令
- 智能体开发工程师 — 需要设计、调试、进化 AI 编码智能体，建立系统化的 Agent 工程体系
- 效率开发者 — 已用 AI 工具，想掌握 Agent 编排和工作流模式，提升日常开发效率 2x+
- 技术负责人 — 团队技术决策者，关注标准化，建立团队级 **Harness Engineering（驾驭工程）** 体系
- **Skill（技能）** 作者 — 有 AI 使用经验，想开发高质量、可复用的 Skill
- 工程经理 — 评估团队工具选型，判断 OpenCode 的投资回报率
- 需求分析师/产品经理 — 验证需求覆盖完整性，评估内容价值主张
- 系统架构师/技术顾问 — 评估 OpenCode 的技术可行性、架构集成与安全合规
- 后端开发者/API 工程师 — 将 AI Agent 嵌入后端开发工作流，掌握 **MCP（模型上下文协议）** 服务端集成
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
- → [OpenCode **Plugin（插件）** 系统参考](./plugins.md) — 了解 Plugin 系统的完整参考

---

## 常见反模式

### 滥用 `/ralph-loop` 和 `/ulw-loop` 自动化循环

自动化循环命令（`/ralph-loop`、`/ulw-loop`）是 OpenCode 最强大的能力之一，但也最容易被滥用。一些开发者在任务描述模糊、范围不明确的情况下直接启动循环，导致 Agent 陷入无限迭代或产出大量无用代码。正确做法是：先用 `/hyperplan` 或 Prometheus 模式生成明确的实现计划，确认计划中的每个步骤都有清晰的输入和预期输出后，再用 `/start-work` 启动执行。循环机制适合"知道要做什么，只是需要持续执行"的场景，不适合"边做边想"的探索式开发。

### 在生产环境频繁使用 `/undo` 和 `/redo`

`/undo` 和 `/redo` 撤销的是文件修改和命令执行，但不会回滚数据库变更、环境变量修改或外部服务调用。在生产环境中频繁使用这两个命令，可能导致部分操作被撤销而另一部分未被撤销，产生不一致的中间状态。更安全的做法是通过 Git 分支隔离生产环境变更，用 `git stash` 或 `git checkout` 回滚，而不是依赖 OpenCode 的会话级撤销。

### 把所有任务塞进同一个会话

有些开发者习惯在一个长会话中完成所有工作，从代码编写到测试到部署都在同一个 Session 中进行。这导致上下文膨胀、Token 消耗失控，而且不同任务的上下文会互相污染（例如调试 Bug 的上下文影响了后续的代码审查）。正确做法是按任务类型使用独立会话：代码编写、代码审查、Bug 调试、部署操作分别使用不同的 Session，通过 `/sessions` 在会话间切换。

### 自定义命令不使用 `$ARGUMENTS` 参数化

创建自定义命令时，有些开发者把所有参数硬编码在 Markdown 文件中，每次修改参数都要编辑文件。这在个人使用时勉强可以，但团队共享时效率低下。应该使用 `$ARGUMENTS` 模板语法让命令参数化，调用时通过 `/command 参数` 传入不同值。这样同一个命令可以适配不同的文件路径、分支名或配置参数，团队成员只需记住命令格式而不需要了解内部实现。

---

## 适用场景与限制

### OMO 扩展命令需要额外安装

核心内置命令（`/init`、`/new`、`/compact` 等）开箱即用，但 OMO 扩展命令（`/ralph-loop`、`/refactor`、`/hyperplan` 等 9 个命令）需要安装 oh-my-openagent 插件后才可用。如果团队中部分成员没有安装 OMO，他们无法使用这些高级命令，可能导致工作流不一致。建议在项目 README 或 AGENTS.md 中明确标注所需的命令和插件依赖。

### `/init` 生成的 AGENTS.md 可能不够精确

`/init` 通过扫描项目结构自动生成 AGENTS.md，但它对项目架构的理解是浅层的——识别技术栈、列出目录结构，但无法理解业务逻辑、领域模型和团队约定。生成的 AGENTS.md 需要人工补充：业务规则、代码审查标准、部署流程、安全约束等只有人才能定义的内容。把 `/init` 的输出当作起点而非终点。

### Speckit 命令链的顺序依赖

Speckit 系列命令（`/speckit.clarify` → `/speckit.specify` → `/speckit.plan` → `/speckit.tasks` → `/speckit.implement`）有严格的顺序依赖。跳过前面的步骤直接执行后面的结果会失败或产出质量低下的结果。例如，没有经过 `/speckit.clarify` 澄清的需求直接 `/speckit.specify`，生成的规格文档会包含大量模糊和矛盾的描述。

### 自定义命令的模板注入安全

`!shell` 语法在每次执行时动态运行 Shell 命令，如果命令中包含用户输入的参数，可能造成命令注入。`@file` 语法会将指定文件的完整内容注入 Prompt，如果文件包含敏感信息（API Key、密码），这些信息会暴露给 LLM。团队共享自定义命令时，应审查模板中的 `!shell` 和 `@file` 用法，避免在命令模板中引入安全风险。

---

## 常见失败与陷阱

### `/compact` 压缩后丢失关键上下文

`/compact` 通过摘要替代原始对话来释放 Token 空间，但摘要过程可能丢失重要的细节信息（如特定的错误日志、代码片段、决策记录）。压缩后如果 Agent 继续基于不完整的上下文工作，可能产出偏差的结果。建议在压缩前手动记录关键决策和待处理事项，压缩后检查 Agent 是否仍能正确理解任务上下文。

### `!shell` 命令执行超时

自定义命令中的 `!shell` 语法在命令执行时动态运行 Shell 命令。如果 Shell 命令耗时过长（如 `git log --all` 在大型仓库中、`find` 在包含大量文件的目录中），会阻塞命令的执行。OpenCode 没有为 `!shell` 提供超时控制，长时间运行的命令可能导致会话卡住。建议 `!shell` 只用于轻量级的快速命令（如 `git branch --show-current`），耗时操作应该用 Agent 的 Bash 工具执行。

### `/handoff` 摘要不完整

`/handoff` 生成的上下文摘要依赖当前会话的历史消息。如果会话历史被压缩过（`/compact`），摘要可能遗漏早期的重要信息。此外，`/handoff` 的摘要格式是固定的，无法自定义包含哪些信息。新会话中导入摘要后，Agent 需要重新建立对项目的理解，这个过程可能需要额外的交互。建议在 `/handoff` 前手动记录关键上下文，摘要生成后检查是否覆盖了所有重要信息。

### Speckit 任务列表与实际代码不匹配

`/speckit.tasks` 从设计产物（spec、plan）生成任务列表，但任务描述可能与实际代码结构不匹配。例如，任务要求"修改 UserService"，但代码中实际的文件名是 `user-service.ts` 或 `UserService.ts`。`/speckit.implement` 执行任务时会逐个匹配文件名，匹配失败会导致任务跳过或错误执行。建议在 `/speckit.tasks` 生成后先人工审核任务列表，确认文件路径和类名与实际代码一致。
