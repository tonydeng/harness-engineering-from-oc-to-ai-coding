# Pi Agent 扩展体系详解

Pi 的核心设计哲学是"极简核心 + 强力扩展"。它主动不做许多功能（MCP、子智能体、Plan 模式等），而是提供 4 层扩展机制，让用户按需构建工作流。

## 扩展体系总览

| 层级 | 能力 | 格式 | 加载位置 | 适用场景 |
|------|------|------|---------|---------|
| **Extensions** | 自定义工具、命令、事件处理、UI 组件 | TypeScript | `~/.pi/agent/extensions/` / `.pi/extensions/` | 深度定制，需要编程能力的扩展 |
| **Skills** | 按需系统指令注入 | SKILL.md（YAML frontmatter + 指令） | `~/.pi/agent/skills/` / `.pi/skills/` | 添加领域知识、角色设定、规则集 |
| **Prompt Templates** | 可复用提示词模板 | Markdown（YAML frontmatter + 模板） | `~/.pi/agent/prompts/` / `.pi/prompts/` | 常用指令模版 |
| **Themes** | UI 主题定制 | JSON | `~/.pi/agent/themes/` / settings.json | 配色和外观定制 |

此外还有 **Pi Packages** 作为打包分发机制，可将上述四种扩展打包为一个 npm 可分发的单元。

---

## Extensions（TypeScript 插件系统）

Extensions 是 Pi 最强大的扩展层，允许通过 TypeScript 编写自定义工具、命令、事件处理器、覆盖层和 UI 组件。

### 架构模型

Extensions 在 Pi 的 Agent 运行时中注册钩子，可以：

- **注册自定义工具**：新增 LLM 可调用的工具函数
- **注册自定义命令**：新增 Slash 命令（`/mycommand`）
- **替换内置工具**：例如 Gondolin extension 将 `read`/`write`/`edit`/`bash` 路由到微 VM 中执行
- **监听事件**：Agent 生命周期的各类事件（上下文准备、工具调用前/后 等）
- **添加 UI 组件**：自定义 Widget、状态行、覆盖层（Overlay）
- **替换编辑器**：自定义 TUI 编辑器组件

### 编写 Extension

Extensions 是标准的 TypeScript 文件，放置在 `~/.pi/agent/extensions/` 或 `.pi/extensions/` 目录：

```typescript
// ~/.pi/agent/extensions/my-extension.ts
import type { ExtensionAPI } from "@earendil-works/pi-agent-core";

export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "my_tool",
    description: "我的自定义工具",
    parameters: { /* TypeBox schema */ },
    execute: async (args) => {
      return "工具执行结果";
    },
  });

  pi.registerCommand({
    name: "mycommand",
    description: "我的自定义命令",
    execute: async (args) => {
      return "命令执行结果";
    },
  });
}
```

### 内置 Extension 示例

Pi 自带 3 个示例 Extension：

| Extension | 功能 |
|-----------|------|
| `prompt-url-widget.ts` | 编辑器中的 `@url` 自动补全，解析 URL 内容后提交给 LLM |
| `redraws.ts` | TUI 屏幕重绘事件处理 |
| `tps.ts` | 在状态行显示 Token Per Second 实时速率 |

完整的 Extension API 参考见 Pi 官方文档：[pi.dev/docs/latest/extensions](https://pi.dev/docs/latest/extensions)

---

## Skills（Agent Skills 标准）

Skills 遵循 [agentskills.io](https://agentskills.io) 标准，以 SKILL.md 文件提供按需加载的系统指令。

### Skill 文件格式

```markdown
---
name: add-llm-provider
description: 添加自定义 LLM Provider 配置
---

你是一个 LLM Provider 配置专家。你的职责是：

1. 读取当前的 Provider 配置文件
2. 根据用户提供的 API 地址和密钥信息添加新 Provider
3. 验证配置是否正确加载
```

Skills 使用 YAML frontmatter 声明 `name` 和 `description`，正文作为系统指令注入到 Agent 的上下文中。

### 加载位置与优先级

Skills 从多个位置加载：

| 位置 | 作用域 |
|------|--------|
| `~/.pi/agent/skills/` | 全局技能 |
| `.pi/skills/` | 项目级技能 |
| 通过 `pi packages install` 安装 | 包内技能 |

支持 `.gitignore` 风格的忽略文件（`SKILL.md.ignore`）。

### 调用方式

通过 `/skill:name` 在编辑器中调用已识别到的 Skill。Pi 的 harness 层（`formatSkillsForSystemPrompt`）将 Skill 内容格式化为 XML 块注入到系统提示中：

```xml
<skill name="add-llm-provider">
你是一个 LLM Provider 配置专家。你的职责是：
...
</skill>
```

---

## Prompt Templates（提示词模板）

Prompt Templates 是命名后可复用的提示词片段。它们与 Skills 的区别在于：

- **Skills** 是**系统性指令**，注入到 Agent 的角色定义中，长期有效
- **Prompt Templates** 是**单次调用模板**，通过 `/name` 快捷注入到当前消息

### 模板文件格式

```markdown
---
name: cl
description: 生成 Conventional Commit 格式的提交信息
---

请为当前变更生成一个 Conventional Commit 格式的提交信息。

格式要求：
<type>(<scope>): <description>

<body>

<footer>

类型包括：feat、fix、docs、style、refactor、test、chore
```

### 内置模板

Pi 自带以下 Prompt Templates：

| 模板 | 文件 | 功能 |
|------|------|------|
| `/cl` | `.pi/prompts/cl.md` | 生成 Conventional Commit 提交信息 |
| `/is` | `.pi/prompts/is.md` | 生成 Issue 模板 |
| `/pr` | `.pi/prompts/pr.md` | 生成 PR 描述模板 |

在编辑器中输入 `/cl` 即可调用模板，模板内容会自动填充到当前消息中，用户可以在此基础上编辑。

### 加载位置

| 位置 | 作用域 |
|------|--------|
| `~/.pi/agent/prompts/` | 全局 |
| `.pi/prompts/` | 项目级 |

---

## Themes（主题系统）

Pi 的 TUI 支持热重载主题配置：

```json
{
  "theme": "dark",
  "colors": { ... }
}
```

通过 `/settings` 在运行中切换主题，无需重启。支持 dark、light 以及完全自定义的主题 JSON。

---

## Context Files（上下文文件）

Pi 支持多层级上下文文件配置：

| 文件 | 作用 | 优先级 |
|------|------|--------|
| `AGENTS.md` | 项目级指令文件 | 高（项目级最高） |
| `SYSTEM.md` | 添加到系统提示中 | 中 |
| `APPEND_SYSTEM.md` | 追加到系统提示末尾 | 中 |

文件加载位置：

| 位置 | 作用域 | 说明 |
|------|--------|------|
| `~/.pi/agent/AGENTS.md` | 全局 | 所有项目生效 |
| `~/.pi/agent/SYSTEM.md` | 全局 | 所有项目生效 |
| `.pi/AGENTS.md` | 项目级 | 覆盖全局 |
| `.pi/SYSTEM.md` | 项目级 | 覆盖全局 |
| 项目根 `AGENTS.md` | 项目级 | 仅当前项目 |

`--no-context-files` 标志可禁用所有上下文文件加载。

---

## Pi Packages（扩展打包分发）

Pi Packages 是将 Extensions、Skills、Prompt Templates、Themes 打包为可分发 npm 包的机制。

### Package 结构

```
my-pi-package/
├── package.json           # 包含 "pi" 字段声明包类型
├── extensions/
│   └── my-extension.ts
├── skills/
│   └── my-skill.md
├── prompts/
│   └── my-prompt.md
└── themes/
    └── my-theme.json
```

`package.json` 中的 `pi` 字段：

```json
{
  "name": "my-pi-package",
  "version": "1.0.0",
  "pi": {
    "extensions": ["extensions/my-extension.ts"],
    "skills": ["skills/my-skill.md"],
    "prompts": ["prompts/my-prompt.md"],
    "themes": ["themes/my-theme.json"]
  }
}
```

### 安装与分发

```bash
# 从 npm 安装
pi packages install my-pi-package

# 从本地路径安装
pi packages install ./path/to/my-pi-package
```

通过 `pi-build` CLI 工具打包。分发方式包括 npm 仓库、Git 仓库或直接本地路径安装。

---

## 扩展体系对比

| 维度 | Pi Agent Extensions | OpenCode Plugin | Claude Code Hooks |
|------|---------------------|-----------------|-------------------|
| 语言 | TypeScript | TypeScript | Node.js / Shell |
| 工具注册 | `pi.registerTool()` | `definePlugin()` | CLAUDE.md 自定义命令 |
| 事件钩子 | 生命周期事件 | 20+ Hook 点 | Hook 系统 |
| UI 定制 | Widget / Overlay / 编辑器替换 | 有限 | 不支持 |
| 打包分发 | Pi Packages (npm) | npm | 无标准机制 |

---

> → [生态与社区参考](./ecosystem.md) 涵盖 Provider 生态、程序化集成方式和容器化方案
