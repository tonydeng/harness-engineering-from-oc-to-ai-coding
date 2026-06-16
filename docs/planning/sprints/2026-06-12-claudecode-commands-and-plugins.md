# Claude Code commands.md + plugins.md 创建计划

> **背景：** 附录 B 中 OpenCode 目录有 4 个文档（capabilities.md, commands.md, plugins.md, ecosystem.md），而 Claude Code 目录只有 2 个（capabilities.md, ecosystem.md）。为对齐结构，需补充 commands.md 和 plugins.md。

**目标：**
1. 创建 `src/appendix-b/claudecode/commands.md` — 详细命令速查手册
2. 创建 `src/appendix-b/claudecode/plugins.md` — 扩展机制参考
3. 调整 `src/appendix-b/claudecode/capabilities.md` — 精简并引用新文档
4. 更新 `src/SUMMARY.md` — 添加索引
5. `mdbook build` — 验证

**并行策略：** Phase 1（deep-research）需要串行获取数据，Phase 2-3 可并行创建文档。

---

### 任务 1：Deep-research Claude Code 命令和能力

**文件：** 无（信息收集）

- [ ] **步骤 1：搜索 Claude Code 最新命令列表和 CLI 参数**

运行 2 个平行搜索：
- `npx @upstash/context7-mcp` 或 websearch 搜索 "Claude Code CLI commands reference 2026"
- websearch 搜索 "Claude Code plugins extension mechanisms architecture 2026"

- [ ] **步骤 2：整理研究成果为结构化数据**

输出格式：
- 命令清单（按分类，含语法、参数、示例）
- 扩展机制清单（CLAUDE.md、Skills、MCP、Subagents、Hooks、Plugins）
- 对比 opencode/commands.md 和 opencode/plugins.md 的结构参考

---

### 任务 2：创建 src/appendix-b/claudecode/commands.md

**文件：** 创建 `src/appendix-b/claudecode/commands.md`

**参考：** `src/appendix-b/opencode/commands.md`（结构风格对齐）

**参考：** `src/appendix-b/claudecode/capabilities.md`（已有命令表，需要更详细）

- [ ] **步骤 1：按功能分类编写命令参考**

分类建议：
1. 核心命令（会话控制、项目管理）
2. Agent 模式命令（/plan、/code、/goal）
3. 工具命令（Bash、Edit、Read、Search）
4. 配置命令（CLAUDE.md、MCP）
5. Agent SDK 命令（非交互模式）
6. 自定义命令（.claude/commands/）

每个命令包含：语法、参数说明、示例

- [ ] **步骤 2：添加使用场景和最佳实践**

---

### 任务 3：创建 src/appendix-b/claudecode/plugins.md

**文件：** 创建 `src/appendix-b/claudecode/plugins.md`

**参考：** `src/appendix-b/opencode/plugins.md`（结构风格对齐）

**注意：** Claude Code 没有类似 OpenCode 的 `definePlugin` API。其"插件"概念是六层扩展架构。

- [ ] **步骤 1：描述六层扩展架构**

1. CLAUDE.md — 项目记忆与规则
2. Skills — 可复用指令集
3. MCP 服务器 — 外部工具连接
4. Subagents — 子任务代理
5. Hooks — 生命周期事件
6. Plugins — 打包分发组件

- [ ] **步骤 2：详细介绍每层扩展的配置方式、适用场景和局限**

- [ ] **步骤 3：创建对比表格（vs OpenCode 插件系统）**

---

### 任务 4：调整 src/appendix-b/claudecode/capabilities.md

**文件：** 修改 `src/appendix-b/claudecode/capabilities.md`

- [ ] **步骤 1：在命令表和扩展机制部分添加交叉引用**

在命令表后添加：`→ 详细命令参考见 [commands.md](./commands.md)`
在扩展机制部分添加：`→ 扩展体系详解见 [plugins.md](./plugins.md)`

- [ ] **步骤 2：简化命令表为概览（去掉过于详细的参数说明）**

---

### 任务 5：更新 SUMMARY.md 和 README.md

**文件：** 修改 `src/SUMMARY.md` 和 `src/appendix-b/README.md`

- [ ] **步骤 1：在 SUMMARY.md 中添加新文件索引**

```
  - [Claude Code 内置能力](appendix-b/claudecode/capabilities.md)
    - [Claude Code 命令参考](appendix-b/claudecode/commands.md)
    - [Claude Code 扩展机制](appendix-b/claudecode/plugins.md)
    - [Claude Code 生态参考](appendix-b/claudecode/ecosystem.md)
```

- [ ] **步骤 2：在 README.md 中添加新文件的导航和概要**

---

### 任务 6：mdbook build 验证

**文件：** 无

- [ ] **步骤 1：运行 `mdbook build` 检查错误和警告**

- [ ] **步骤 2：修复任何链接断裂或格式问题**
