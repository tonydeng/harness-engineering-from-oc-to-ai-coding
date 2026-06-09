# OpenCode 内置命令参考

> OpenCode 内置命令的完整参考手册，按功能分类，方便快速查阅。所有命令在对话输入框中以 `/` 开头输入即可触发。

OpenCode 提供了两大类命令：**核心内置命令**（Core Commands）由 OpenCode 本体提供，覆盖项目初始化、会话管理、模型配置等基础操作；**OMO 扩展命令**（oh-my-openagent Extended Commands）由 oh-my-openagent 插件提供，增加了自动化循环、智能重构、代码质量治理等高级能力。此外，OpenCode 支持通过 Markdown 文件或 JSON 配置创建自定义命令（Custom Commands）。

→ [工作流模式](../02-core-concepts/workflow-patterns.md) 详细讲解 Command 系统的设计原理。
→ [oh-my-openagent 集成](../03-setup/oh-my-openagent-setup.md) 介绍 OMO 的安装与配置。

---

## Core Commands（核心命令）

### 项目初始化

| 命令 | 别名 | 功能 | 典型场景 |
|------|------|------|----------|
| `/init` | — | 扫描项目结构，生成 AGENTS.md 项目知识库 | 新项目首次打开 |
| `/help` | — | 显示可用命令和快捷键列表 | 不确定命令时查看帮助 |

**`/init`** 是 OpenCode 工程化的起点。执行后，它会扫描项目目录结构、识别技术栈、生成包含项目概述的 AGENTS.md 文件，让 Agent "认识"你的项目。

→ [AGENTS.md 约定系统](../06-advanced/agents-dot-md.md) 讲解生成的文件结构和如何手动扩展。

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

→ [上下文压缩技术](../06-advanced/context-compression.md) 深入讲解压缩机制和触发策略。
→ [Token 预算策略](../06-advanced/token-budget.md) 讲解如何合理分配有限的 Token 空间。

### 模型与配置

| 命令 | 功能 | 典型场景 |
|------|------|----------|
| `/models` | 列出可用模型，切换当前模型 | 需要更强推理能力时切换到旗舰模型 |
| `/connect` | 添加新的 LLM Provider | 接入新的模型供应商（如国产模型） |
| `/themes` | 切换界面主题 | 个性化界面风格 |
| `/editor` | 打开编辑器，编辑当前对话内容 | 精确修改长 Prompt |
| `/details` | 显示最近一次工具调用的详细信息 | 排查工具执行结果 |
| `/thinking` | 切换推理过程的显示状态 | 查看 Agent 的思考链路 |
| `/exit` | 退出 OpenCode | 结束工作 |

→ [国产模型供应商配置](../03-setup/chinese-providers.md) 介绍如何通过 `/connect` 接入国内模型。
→ [OpenCode 配置详解](../03-setup/opencode-config.md) 讲解所有配置项的含义。

---

## oh-my-openagent Extended Commands（OMO 扩展命令）

oh-my-openagent（简称 OMO）是 OpenCode 的增强插件，提供了 9 个扩展命令。安装 OMO 后，这些命令自动可用。

→ [oh-my-openagent 集成](../03-setup/oh-my-openagent-setup.md) 介绍安装方法。

### 自动化循环

| 命令 | 功能 | 适用场景 |
|------|------|----------|
| `/ralph-loop` | 启动自引用开发循环，Agent 自主执行直到完成 | 明确的任务，需要持续执行到完成 |
| `/ulw-loop` | 启动 Ultrawork 模式循环，持续工作直到完成 | 复杂任务，需要多轮迭代 |
| `/cancel-ralph` | 取消当前活跃的 Ralph Loop 或 Ultrawork Loop | 需要中断自动执行时 |

**Ralph Loop** 和 **Ultrawork Loop** 都是持续执行机制，区别在于 Ralph Loop 偏向自引用（Agent 自我评估进度），Ultrawork Loop 偏向任务驱动（按预设计划推进）。

→ [Ultrawork 模式](../04-workflows/ultrawork-mode.md) 讲解 Ultrawork 的设计哲学和使用策略。
→ [Prometheus 规划模式](../04-workflows/prometheus-mode.md) 介绍配合 `/start-work` 使用的规划模式。

### 代码质量

| 命令 | 功能 | 适用场景 |
|------|------|----------|
| `/refactor` | 智能重构，结合 LSP、AST 分析和架构评估 | 需要安全地重构代码结构 |
| `/remove-ai-slops` | 移除 AI 生成的代码异味，分类清理 10 类问题 | 代码审查后清理 AI 生成的低质量模式 |

**`/refactor`** 会自动分析代码结构、查找引用关系、评估影响范围，然后执行重构。它集成了 Language Server Protocol（LSP）和 AST（抽象语法树）分析，确保重构不会破坏现有功能。

**`/remove-ai-slops`** 专注于清理 AI 编程工具生成的常见代码异味（Slop），包括：过度注释、不必要的封装、冗余的错误处理、不一致的命名风格等。它先锁定回归测试，再分批清理，最后验证质量门禁。

→ [验证护栏体系](../02-core-concepts/validation-harness.md) 讲解重构和清理背后的质量保障机制。

### 任务执行

| 命令 | 功能 | 适用场景 |
|------|------|----------|
| `/start-work` | 从 Prometheus 计划开始执行工作 | 已完成规划，准备进入执行阶段 |
| `/hyperplan` | 启动对抗性多 Agent 规划，5 个 Agent 交叉评审 | 重要决策前，需要多视角评估方案 |

**`/start-work`** 配合 [Prometheus 规划模式](../04-workflows/prometheus-mode.md) 使用。先通过 Prometheus 生成详细的实现计划，再用 `/start-work` 启动执行。

**`/hyperplan`** 是一种对抗性规划机制。5 个不同视角的 Agent 同时评审同一个方案，互相挑刺，最终综合出经过多轮攻防的高质量计划。

→ [多 Agent 协作](../04-workflows/multi-agent-collab.md) 讲解多 Agent 通信和协调机制。
→ [Agent 派生模式](../04-workflows/agent-derivation.md) 介绍 Agent 如何根据任务动态生成子 Agent。

### 会话续接

| 命令 | 功能 | 适用场景 |
|------|------|----------|
| `/handoff` | 创建上下文摘要，用于新会话续接 | 会话过长需要重开，但不想丢失进度 |
| `/stop-continuation` | 停止所有续接机制（Ralph Loop、Ultrawork、Todo 续接） | 需要完全停止自动续接行为 |

**`/handoff`** 生成一份结构化的上下文摘要，包含已完成的工作、待处理的任务、关键决策记录等。新会话中导入这份摘要即可无缝续接。

→ [上下文工程核心](../02-core-concepts/context-engineering-core.md) 讲解上下文管理的设计哲学。

---

## Custom Commands（自定义命令）

OpenCode 支持用户创建自己的命令。两种方式各有优势，Markdown 文件方式更适合团队协作，JSON 配置方式更适合精细控制。

→ [工作流模式 · Command 系统](../02-core-concepts/workflow-patterns.md) 讲解完整的 Command 设计原理。

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
