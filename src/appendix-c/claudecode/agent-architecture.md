# Claude Code **Agent（智能体）** 设计与开发指南

> 从"配一个自定义命令"到"设计一套多 Agent 体系"——读完本文，你应该能独立设计、实现并迭代 Cluade Code 中的自定义 Agent 和 Subagent。

Claude Code 的 Agent 体系虽然没有 oh-my-openagent 那样的三层编排架构，但它的 **Subagent** 系统加上 **Hooks**、**MCP** 和 **Plugins**，同样能实现灵活的多 Agent 协作。本文面向**需要设计 Agent 的开发者**——不只告诉你有什么配置项，还给出一套从入门到生产的完整方法。

---

## 快速上手：创建你的第一个自定义 Agent

在 Claude Code 中创建一个自定义 Agent 只需要两步：

### 第 1 步：创建 Subagent 文件

在项目 `.claude/agents/` 目录下创建一个 Markdown 文件：

```markdown:.claude/agents/my-helper.md
---
name: my-helper
description: 我的通用助手，处理常规开发任务
model: sonnet
effort: medium
maxTurns: 30
tools: Read Write Edit Bash Grep Glob
---

# System Prompt

你是一个通用的开发助手。请遵循以下原则：

1. 先理解问题再动手，必要时列出方案让用户选择
2. 修改前先读取相关文件，理解上下文
3. 所有输出用中文
```

### 第 2 步：在会话中调用

```
/fork my-helper "重构这个模块的 API 接口"
```

Claude Code 会创建一个后台子 Agent 独立执行，完成后将摘要返回主会话。

> `/fork` 命令（v2.1.161+ 引入）生成一个隔离的子 Agent 会话，继承当前会话的上下文，在后台独立运行。简单来说——你把一件事交给一个 Agent，它干完回来告诉你结果，你继续做自己的事。

---

## 快速动手：给你的 Subagent 配个 **Skill（技能）**

Agent + Skill 的组合是 Claude Code 最实用的模式。Skill 就是 `SKILL.md` 文件——一个包含完整指令集的文档。把 Skill 挂在 Agent 上，Agent 就获得了该领域的专业知识。

```markdown:.claude/agents/react-expert.md
---
name: react-expert
description: React/Next.js 前端专家，专注于组件设计和性能优化
model: sonnet
skills:
  - react-performance
  - testing
tools: Read Write Edit Glob Bash
maxTurns: 25
color: blue
---

# System Prompt

你是 React 前端专家。
```

对应的 Skill 文件可以是：

```markdown:.claude/skills/react-performance.md
---
name: react-performance
description: React 性能优化最佳实践
---

当你分析 React 组件性能时，遵循以下步骤：

1. **识别问题**：检查不必要的重渲染、大组件拆分、状态提升层次
2. **分析工具**：用 React DevTools Profiler 或浏览器 Performance 面板定位瓶颈
3. **优化手段**（按优先级）：
   - `React.memo` 包裹纯展示组件
   - `useMemo` / `useCallback` 缓存计算和回调
   - 状态下推，减少 Context 提供者范围
4. **验证**：优化前后对比渲染次数
```

然后用户在会话中执行：

```
/fork react-expert "检查 pages/dashboard 下的组件性能问题"
```

Subagent 会加载 `react-performance` Skill 的完整指令，以此为指导分析代码。

---

## 架构概览——Claude Code 的 Agent 体系

Claude Code 没有设计一个全局编排层（没有 Sisyphus 这样的主 Agent），它的 Agent 体系建立在四个核心概念上：

| 概念 | 本质 | 用途 |
|------|------|------|
| **内置 Agent 模式** | 角色切换 | Plan Mode（只读分析）、Code Mode（读写执行）|
| **Subagent** | 独立子任务执行器 | 在隔离上下文中执行委派任务 |
| **Background Agent** | 后台运行的全功能会话 | 长时间任务不阻塞主会话 |
| **自定义 Agent 配置** | 预定义角色模板 | 通过 `/agents` 在运行中切换 Agent 行为 |

### 内置 Subagent 类型

| 类型 | 模型 | 工具 | 用途 |
|------|------|------|------|
| **Explore** | Haiku（快速）| Read / Grep / Glob | 代码搜索和分析 |
| **Plan** | 继承主会话 | Read / Grep / Glob | 规划模式调研 |
| **General-purpose** | 继承主会话 | 全部工具 | 复杂多步骤任务 |

### 自定义 Agent 的工作方式

```
主会话（编排器）
  │
  ├── /fork ──► 后台 Subagent（独立上下文窗口）
  │                     │
  │                完成后返回摘要
  │
  ├── /background ──► 转为后台 Agent（全功能）
  │
  └── Task 调用 ──► Subagent A
      Task 调用 ──► Subagent B
```

---

## Agent 设计模式

掌握了"怎么配"之后，下一个问题是"怎么设计"。以下五种模式覆盖了 90% 的 Claude Code Agent 使用场景。

### 1. Simple Agent（单 Agent）

**适用场景**：一个 Agent 完成一件事。这是最常用的模式。

```markdown:.claude/agents/db-reviewer.md
---
name: db-reviewer
description: 数据库 Schema 和查询审查专家
model: sonnet
effort: high
tools: Read Grep Glob
disallowedTools: Write Edit Bash
maxTurns: 15
color: purple
---

# System Prompt

你是一个数据库专家。审查以下方面：

1. Schema 设计是否符合第三范式
2. 索引策略是否合理（关注联合索引顺序）
3. SQL 查询是否存在 N+1 问题
4. 是否有潜在的死锁或锁竞争风险
```

**特点**：单一职责、只读权限、专注一件事。大多数自定义 Subagent 都是这种模式。

### 2. Fork 模式（后台并行）

**适用场景**：多个独立任务可以同时进行。

```
# 用户在主会话中
/fork code-reviewer "审查 src/auth/ 下的变更"
/fork db-reviewer "审查 migrations/ 下的新迁移文件"  
/fork security-scanner "检查依赖是否有已知漏洞"

# 三个 Subagent 各自独立运行，完成后汇总结果
```

Fork 模式的关键优势是**不阻塞主会话**。你可以在等待子 Agent 结果的同时继续在主会话中工作。

### 3. Pipeline（流水线模式）

**适用场景**：A 的输出是 B 的输入。适合分阶段处理。

```
第一阶段：Code Reviewer → 输出问题列表
第二阶段：Fixer → 根据问题列表逐个修复
第三阶段：Tester → 验证修复是否引入新问题
```

Claude Code 不提供内置的 Pipeline 编排器——你需要通过 Hooks 或手动调度来实现：

```markdown:.claude/agents/pipeline-runner.md
---
name: pipeline-runner
description: 多阶段流水线协调者
model: sonnet
maxTurns: 50
tools: Read Write Edit Grep Glob Bash
---

# System Prompt

你是一个流水线协调者。你需要按顺序执行以下阶段：

1. **规划阶段**：分析需求，生成实现计划
2. **实现阶段**：按计划逐步实现
3. **自检阶段**：检查实现是否满足需求
4. **修正阶段**：对发现的问题进行修复

每个阶段完成后，输出阶段小结，再进入下一步。
```

用单个 Agent 做 Chain 模式时，**关键是把步骤写入 prompt 让 Agent 自己编排**。

### 4. Hook 触发的自动化 Agent

**适用场景**：在特定事件（如写入文件、执行命令）后自动触发 Subagent。

```json:.claude/hooks/hooks.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "agent",
            "agent": "code-reviewer",
            "prompt": "审查刚刚修改的文件：{{output}}"
          }
        ]
      }
    ]
  }
}
```

这样每次文件修改后，会自动触发 code-reviewer Subagent 审查变更。审查结果（而非被阻断）会出现在输出中。

> Hook 类型的 `agent` 使用 Subagent（最多 50 轮）执行任务，适合需要代码库状态验证的场景。

### 5. Batch 分解模式

**适用场景**：一个大型变更需要分解为多个独立单元并行处理。

```
/batch

Claude Code 会将你的需求分解为多个独立子任务，每个子任务交给一个 Subagent 并行执行。所有 Subagent 完成后汇总合并。
```

`/batch` 是 Claude Code 对"大规模并行变更"的内置解决方案。它会自动分析变更范围、分解为无冲突的子任务、并行执行并合并结果。

---

## 自定义 Subagent 配置参考

### Frontmatter 完整字段

| 字段 | 必需 | 类型 | 说明 |
|------|------|------|------|
| `name` | ✅ | string | 唯一标识符（小写+连字符）|
| `description` | ✅ | string | Claude 用来判断何时自动委派 |
| `model` | ❌ | enum | `sonnet` / `opus` / `haiku` / `inherit`（默认）|
| `effort` | ❌ | enum | `low` / `medium` / `high` / `max` |
| `maxTurns` | ❌ | number | 最大交互轮次（默认 20）|
| `tools` | ❌ | string[] | 允许的工具白名单 |
| `disallowedTools` | ❌ | string[] | 禁用的工具黑名单 |
| `permissionMode` | ❌ | enum | `default` / `acceptEdits` / `plan` / `auto` |
| `memory` | ❌ | enum | `user` / `project` / `local` 持久记忆 |
| `isolation` | ❌ | string | `worktree` 隔离工作区 |
| `background` | ❌ | boolean | 是否默认后台运行 |
| `skills` | ❌ | string[] | 预加载的 Skill 列表 |
| `mcpServers` | ❌ | string[] | 作用域 **MCP（模型上下文协议）** 服务器 |
| `hooks` | ❌ | object | 作用域生命周期钩子 |
| `color` | ❌ | string | 会话栏颜色标识 |

### 关键字段详解

#### model 选择策略

| 值 | 特点 | 适用场景 |
|----|------|----------|
| `haiku` | 速度最快、成本最低 | 简单任务：文件搜索、代码分析 |
| `sonnet`（默认）| 速度与质量平衡 | 大多数日常任务 |
| `opus` | 推理最强、速度最慢 | 复杂架构分析、安全审查 |
| `inherit` | 继承主会话模型 | 需要与主会话一致的分析深度 |

#### tools 权限设计

```markdown:.claude/agents/readonly-expert.md
---
name: readonly-expert
description: 只读分析专家，不修改任何文件
tools: Read Grep Glob WebFetch
disallowedTools: Write Edit Bash
---
```

权限设计原则：**最小权限**。只给 Agent 完成工作所必需的工具。只读 Agent 永远不应该有 Write/Edit 权限。

#### isolation 工作区隔离

```markdown:.claude/agents/experimental-coder.md
---
name: experimental-coder
description: 实验性代码修改，不污染主工作区
model: sonnet
isolation: worktree
tools: Read Write Edit Bash Grep Glob
---
```

`isolation: worktree` 会在独立的 Git worktree 中执行，修改不会影响主分支。适合风险较高的变更。

---

## 运行 Agent

### 在交互会话中

| 方法 | 命令 | 说明 |
|------|------|------|
| 分叉 Subagent | `/fork <agent-name> <prompt>` | 后台执行，返回摘要 |
| 切换 Agent | `/agents` | 交互式管理界面 |
| 手动转后台 | `/background` | 当前会话转为后台 |
| 批量分解 | `/batch <description>` | 自动分解并行执行 |

### 通过 CLI 启动

```bash
# 指定 Agent 启动
claude --agent react-expert "实现这个组件"

# 直接后台运行
claude --bg "分析测试失败原因并给出修复建议"

# 非交互模式 + 指定 Agent
claude -p "审查 src/auth/" --agent security-reviewer
```

### 管理后台任务

```bash
# 查看所有后台 Agent
claude agents

# 连接到后台会话
claude attach <id>

# 停止后台会话
claude stop <id>

# 查看后台会话日志
claude logs <id>
```

---

## Agent 设计工具箱——Subagent 之外的能力

除了 Subagent，Claude Code 还有几个与 Agent 密切相关的能力，组合使用效果更佳。

### Background Agent

`/background` 将当前会话转为后台运行。与 `/fork` 的区别：

| 方式 | 场景 | 特点 |
|------|------|------|
| `/fork` | 派生子任务 | 继承上下文，完成后返回摘要 |
| `/background` | 当前会话转为后台 | 独立运行，不阻塞终端 |
| `--bg` | 新启动后台会话 | 从 CLI 直接启动 |

### /batch——并行任务分解

`/batch` 是 Claude Code 对大范围变更的"分解-并行-合并"方案。适用场景：

- 同时重构多个独立模块
- 为多个功能编写测试
- 批量更新代码风格

Claude Code 自动分析变更范围，拆分为无冲突的子任务，分配给多个 Subagent 并行执行。

### Task 工具

在 Claude Code 的 Hooks 和 Plugins 中可以通过 Task 工具调用 Subagent：

```typescript:src/appendix-c/claudecode/agent-architecture.md
// Pseudocode——Hook 中的 Subagent 调用
{
  "type": "agent",
  "agent": "security-reviewer",
  "prompt": "审查最近修改的敏感文件"
}
```

Task 工具是 Claude Code 中 Agent 间通信的基础——主 Agent 通过它委派工作给子 Agent，子 Agent 完成后返回结构化摘要。

---

## 案例：构建一个代码审查流水线

我们从头构建一个可投入生产的代码审查 Subagent，并在迭代中完善它。

### V1：基础版本

```markdown:.claude/agents/code-reviewer.md
---
name: code-reviewer
description: 代码审查专家，检查实现变更的质量
model: sonnet
effort: high
tools: Read Grep Glob Bash
disallowedTools: Write Edit
maxTurns: 20
color: yellow
---

# System Prompt

你是严格的代码审查者。审查以下维度：

## 检查清单

1. **逻辑正确性**：条件判断是否完整？边界情况是否处理？
2. **安全风险**：是否存在注入、越权、敏感信息泄露？
3. **性能隐患**：是否存在不必要的循环、内存泄漏？
4. **代码质量**：命名是否清晰？函数是否过长？错误处理是否得当？

## 输出格式

对每个问题输出：
- `[CRITICAL]` — 必须修复的问题
- `[WARNING]` — 建议修复的问题
- `[INFO]` — 观察和建议
```

使用方式：

```
/fork code-reviewer "审查最近的 Git 变更"
```

### V2：增加格式化和上下文

```markdown:.claude/agents/code-reviewer.md
---
name: code-reviewer
description: 代码审查专家，检查实现变更的质量
model: sonnet
effort: high
tools: Read Grep Glob Bash
disallowedTools: Write Edit
maxTurns: 20
memory: project
color: yellow
---

# System Prompt

你是严格的代码审查者。审查以下维度：
...
```

`memory: project` 让 Subagent 可以访问项目的持久记忆——包括历史审查记录和项目约定。

### V3：接入 Hook 实现自动审查

将 Subagent 与 Hook 绑定，每次代码变更后自动触发审查：

```json:.claude/hooks/hooks.json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "agent",
            "agent": "code-reviewer",
            "prompt": "审查刚刚修改的文件，重点关注安全和正确性问题"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo \"$CLAUDE_TOOL_INPUT\" | grep -qE 'rm -rf /|DROP DATABASE' && exit 2 || exit 0"
          }
        ]
      }
    ]
  }
}
```

这个配置实现了：
- 写/改文件后 → 自动触发 code-reviewer 审查
- 执行危险命令前 → 自动拦截

---

## 测试与迭代

Agent 开发不是一次性工作——你需要一个反馈循环来持续改进。

### 测试清单

测试你的 Subagent 时，确认以下问题：

| 维度 | 检查项 | 验证方法 |
|------|--------|----------|
| prompt 质量 | 输出的质量是否稳定？ | 用同一个任务跑 3 次，对比差异 |
| 权限配置 | 用到不该用的工具了吗？ | 检查 `.claude/logs/` 工具调用记录 |
| 模型选择 | 模型速度/质量是否满足需求？ | 换不同 model 跑同一任务对比 |
| 边界处理 | 任务超出 maxTurns 会怎样？ | 故意给一个超大任务 |
| 隔离性 | 和其他 Agent 会不会冲突？ | 同时跑多个同类型 Subagent |

### 版本管理

Subagent 是代码，应该版本控制：

```bash
# 推荐目录结构
.claude/
  agents/
    code-reviewer-v1.md
    code-reviewer-v2.md
  skills/
    react-performance.md
```

版本演进记录建议：

```
V1：基础审查功能，输出问题列表
V2：增加 memory:project 记忆历史审查结果
V3：接入 Hook，自动触发后审查
```

### 常见问题排查

| 问题 | 原因 | 解决 |
|------|------|------|
| Subagent 没被调用 | description 不匹配 | 检查 name/description 是否与触发方式一致 |
| 工具调用失败 | 权限不足 | 检查 tools 白名单是否包含所需工具 |
| 结果太长 | maxTurns 过高或被 Agent 遗忘 | 降低 maxTurns 或增加 prompt 中的指令 |
| hook 触发无响应 | Hook Agent 配置错误 | 检查 hooks.json 中 `agent` 字段是否匹配 agents/ 目录的文件名 |

---

## 最佳实践

### 1. 命名清晰、职责单一

每个 Subagent 只做一件事。好的命名标准：看到名字就知道它干什么。

```
✅ security-scanner：安全扫描
✅ db-migration-reviewer：数据库迁移审查
✅ api-doc-generator：API 文档生成

❌ helper：太模糊
❌ super-agent：职责不清晰
```

### 2. **Prompt（提示词）** 要具体、可操作

不写笼统的指令，写 Agent 能逐条执行的具体规则。

```
❌ "审查代码质量"
✅ "检查：是否存在 SQL 注入风险？错误处理是否覆盖了网络超时？日志是否包含敏感信息？"
```

### 3. 最小权限原则

只给 Agent 完成工作所必需的工具。审查类 Agent 不要给 Write/Edit/Bash 权限，以防意外修改。

### 4. 用 Skill 做知识库，用 Agent 做执行器

| 角色 | 内容 | 示例 |
|------|------|------|
| **Skill** | 领域知识、规则、清单 | `react-performance.md`（性能优化清单）|
| **Agent** | 执行逻辑、工具权限、模型配置 | `react-expert.md`（加载 skill + 具体任务）|

Skill 是可复用的知识包，Agent 是执行者。一个 Skill 可以被多个 Agent 共享。

### 5. 把常用命令存为 Subagent

不要每次都手写长 prompt。常见的任务——代码审查、安全扫描、数据库迁移检查——都应该做成 Subagent 文件，一个 `/fork` 搞定。

### 6. 生产级 Agent 的配置要完整

```markdown:.claude/agents/production-ready.md
---
name: production-ready
description: 生产级 Agent 配置模板
model: sonnet
effort: high
maxTurns: 30
tools: Read Write Edit Bash Grep Glob
disallowedTools: rm rf
permissionMode: acceptEdits
memory: project
isolation: worktree
skills:
  - team-conventions
  - security-checklist
mcpServers:
  - sentry
color: green
---

# System Prompt
...
```

### 7. 做好隔离

变更类任务（重构、迁移）一定要用 `isolation: worktree`。只读任务（审查、分析）不需要隔离。

---

## 关联章节

- ← [Claude Code 扩展机制](./extensions.md) — Subagent、Hooks、Plugins 完整参考
- ← [Claude Code 命令参考](./commands.md) — `/fork`、`/background`、`/agents` 命令详解
- ← [Claude Code 生态参考](./ecosystem.md) — 社区 Subagent、Skills 推荐
- → [oh-my-openagent Agent 设计指南](../../appendix-b/opencode/agent-architecture.md) — OMO 三层编排体系对比参考
- → [自定义工作流](../../04-workflows/custom-workflows.md) — Team Mode 多 Agent 协作
- → [Agent 派生模式](../../04-workflows/agent-derivation.md) — Agent 动态生成模式

---

## 读者视角

### 适用读者角色
- 入门开发者 — 需要快速上手 Claude Code 的 Agent 体系
- 智能体开发工程师 — 需要设计、调试、进化 Claude Code 中的自定义 Agent 和 Subagent
- 效率开发者 — 已有 AI 工具经验，想通过 Claude Code 提升 2x+ 效率
- 技术负责人 — 需要评估 Claude Code 的技术可行性和团队级 **Harness Engineering（驾驭工程）** 体系
- Skill作者 — 需要开发自定义 Skill 和 MCP 桥接，实现团队最佳实践复用

### 典型使用场景
- 需要创建自定义 Subagent 处理特定任务
- 需要设计 Agent + Skill 组合实现专业知识
- 需要实现多 Agent 协作工作流
- 需要设置 Hook 自动触发 Subagent
- 需要实现批量任务分解和并行处理

### 使用示例
```bash
# 创建自定义 Subagent
/clone my-helper "重构这个模块的 API 接口"

# 切换到特定 Agent
/agents

# 手动转后台
/background

# 批量分解任务
/batch "重构整个服务层"

# 设置 Hook 自动审查
/hooks
```

### 工程化示例

**配置顺序检查表：**

1. **第1步：创建 Subagent 文件**
   ```markdown
   # .claude/agents/my-helper.md
   ---
   name: my-helper
   description: 我的通用助手，处理常规开发任务
   model: sonnet
   effort: medium
   maxTurns: 30
   tools: Read Write Edit Bash Grep Glob
   ---
   
   # System Prompt
   
   你是一个通用的开发助手。请遵循以下原则：
   
   1. 先理解问题再动手，必要时列出方案让用户选择
   2. 修改前先读取相关文件，理解上下文
   3. 所有输出用中文
   ```

2. **第2步：创建 Skill**
   ```markdown
   # .claude/skills/react-performance.md
   ---
   name: react-performance
   description: React 性能优化最佳实践
   ---
   
   当你分析 React 组件性能时，遵循以下步骤：
   
   1. **识别问题**：检查不必要的重渲染、大组件拆分、状态提升层次
   2. **分析工具**：用 React DevTools Profiler 或浏览器 Performance 面板定位瓶颈
   3. **优化手段**（按优先级）：
      - `React.memo` 包裹纯展示组件
      - `useMemo` / `useCallback` 缓存计算和回调
      - 状态下推，减少 Context 提供者范围
   4. **验证**：优化前后对比渲染次数
   ```

3. **第3步：配置 Hook**
   ```json
   # .claude/hooks/hooks.json
   {
     "hooks": {
       "PostToolUse": [
         {
           "matcher": "Write|Edit",
           "hooks": [
             {
               "type": "agent",
               "agent": "code-reviewer",
               "prompt": "审查刚刚修改的文件：{{output}}"
             }
           ]
         }
       ]
     }
   }
   ```

### 与前/后文章的衔接
- ← [Claude Code 扩展机制](./extensions.md) — Subagent、Hooks、Plugins 完整参考
- → [Claude Code 命令参考](./commands.md) — `/fork`、`/background`、`/agents` 命令详解
