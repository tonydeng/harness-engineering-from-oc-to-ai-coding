# MiMo Code 架构深度解析

> **适合读者**: Agent工程师(AE), 架构师(SYSA)

本章深入分析 MiMo Code 的架构设计，重点解读其主循环状态机、检查点写入器、四层记忆系统和动态工作流执行引擎。这些设计共同解决了长任务自动化中的核心挑战：**可靠性**和**状态连续性**。

## 架构全景

MiMo Code 的架构围绕三个核心问题设计：

1. **如何减少每一步的决策错误？** → 计算层（Max Mode、Goal）
2. **如何让逻辑会话无限延伸？** → 记忆层（检查点、四层记忆、重建）
3. **如何从过去的工作中积累？** → 进化层（Dream、Distill）

```
┌─────────────────────────────────────────────────────────────┐
│                      主循环状态机                            │
├─────────────────────────────────────────────────────────────┤
│  用户输入 → 模型推理 → 工具调用 → 结果反馈 → 循环            │
│      ↑                                       │              │
│      │         ┌─────────────────────────────┘              │
│      │         ↓                                            │
│      │   检查点触发？                                        │
│      │         │                                            │
│      │    是 ──┴── 否                                       │
│      │    │       │                                         │
│      │    ↓       │                                         │
│      │  写入器子智能体                                       │
│      │    │       │                                         │
│      │    ↓       │                                         │
│      │  更新检查点文件                                       │
│      │    │       │                                         │
│      │    └───────┘                                         │
│      │         │                                            │
│      │         ↓                                            │
│      │   上下文接近限制？                                     │
│      │         │                                            │
│      │    是 ──┴── 否                                       │
│      │    │       │                                         │
│      │    ↓       │                                         │
│      │  执行重建                                             │
│      │    │       │                                         │
│      │    ↓       │                                         │
│      │  注入持久化文件                                        │
│      │    │       │                                         │
│      │    └───────┘                                         │
│      │         │                                            │
│      └─────────┘                                            │
└─────────────────────────────────────────────────────────────┘
```

## 主循环状态机

MiMo Code 的主循环是一个确定性的状态机，管理智能体与运行时的交互。核心状态包括：

| 状态 | 说明 | 转换条件 |
|------|------|---------|
| **IDLE** | 等待用户输入 | 用户发送消息 |
| **THINKING** | 模型正在推理 | 推理完成 |
| **TOOL_CALLING** | 执行工具调用 | 工具返回结果 |
| **CHECKPOINTING** | 写入器正在保存状态 | 写入完成 |
| **REBUILDING** | 重建上下文窗口 | 重建完成 |
| **COMPLETED** | 任务完成 | 新任务开始 |

关键设计决策：

1. **非阻塞检查点**：写入器在后台运行，不阻塞主智能体
2. **增量更新**：每次检查点是前一次的增量，非一次性摘要
3. **预算控制**：注入内容严格控制在 65K tokens 以内

## 检查点写入器

检查点写入器是 MiMo Code 的核心创新之一。它解决了长任务中的关键问题：**如何在不干扰主智能体的情况下保存状态**。

### 设计原则

1. **独立性**：写入器不共享主智能体的注意力或 token 预算
2. **单写入者**：每个结构化文件只允许一个写入者，防止并发冲突
3. **固定结构**：检查点文件有 11 个固定字段，确保一致性

### 检查点文件结构

```markdown
# 会话检查点

## 1. 当前意图
用户想要完成什么？当前的目标是什么？

## 2. 下一步操作
接下来应该做什么？具体的行动计划。

## 3. 工作约束
有哪些限制条件？技术约束、业务规则等。

## 4. 任务树
任务的层次结构（T1, T1.1, T1.2...）

## 5. 当前工作
正在处理的具体内容。

## 6. 涉及文件
已经读取或修改的文件列表。

## 7. 跨任务发现
在当前任务中发现的、可能影响其他任务的信息。

## 8. 错误和修复
遇到的错误以及如何修复的。

## 9. 运行时状态
环境变量、配置、版本等运行时信息。

## 10. 设计决策
做出的关键设计选择及其理由。

## 11. 杂项笔记
其他需要记住的内容。
```

### 触发时机

检查点在以下位置触发：

| 触发点 | 上下文利用率 | 说明 |
|-------|------------|------|
| **检查点 1** | ~20% | 早期状态捕获，空间充裕 |
| **检查点 2** | ~45% | 中期状态更新，增量修改 |
| **检查点 3** | ~70% | 后期状态保存，准备重建 |
| **重建** | ~90% | 最终状态注入，开始新窗口 |

这种设计避免了"中间丢失"问题：在模型压缩能力最佳时执行最关键的提取。

### 写入器的工作流程

```
触发检查点
    │
    ↓
读取当前对话历史
    │
    ↓
读取上一次检查点（如果有）
    │
    ↓
分析对话，提取关键信息
    │
    ↓
更新 11 个结构化字段
    │
    ↓
写入 checkpoint.md
    │
    ↓
检查是否需要更新 MEMORY.md
    │
    ↓
完成
```

## 四层记忆系统

MiMo Code 的记忆系统是分层的，每层具有不同的生命周期和用途。

### 层次结构

```
┌─────────────────────────────────────────┐
│           全局记忆（用户偏好）            │
├─────────────────────────────────────────┤
│           项目记忆（MEMORY.md）          │
├─────────────────────────────────────────┤
│           会话记忆（checkpoint.md）      │
├─────────────────────────────────────────┤
│           历史（SQLite）                 │
└─────────────────────────────────────────┘
```

### 各层详解

#### 1. 会话记忆（checkpoint.md）

- **生命周期**：仅当前逻辑会话
- **内容**：该会话的完整工作状态
- **更新频率**：每次检查点触发时
- **访问权限**：主智能体只读，写入器读写

#### 2. 项目记忆（MEMORY.md）

- **生命周期**：持久化，跨会话
- **内容**：项目级知识——架构决策、用户规则、反复验证的技术事实
- **更新频率**：当观察在多个会话检查点中稳定时
- **访问权限**：主智能体只读，写入器读写

**MEMORY.md 示例结构**：

```markdown
# 项目记忆

## 架构决策
- 使用微服务架构，服务间通过 gRPC 通信
- 数据库选择 PostgreSQL，缓存使用 Redis

## 用户规则
- 所有 API 必须有单元测试
- 提交消息使用 Conventional Commits 格式

## 技术事实
- 项目使用 TypeScript 5.x，Node.js 20.x
- 构建工具是 Turborepo
```

#### 3. 全局记忆

- **生命周期**：持久化，跨项目
- **内容**：用户级偏好（编码风格、常用工具等）
- **存储位置**：配置文件
- **访问权限**：主智能体只读

#### 4. 历史（SQLite）

- **生命周期**：持久化，完整保留
- **内容**：每个会话的完整追踪——每条消息和工具调用的原始文本
- **访问方式**：通过 `history` 工具按需查询
- **用途**：当结构化记忆中找不到细节时，回溯到原始记录

### 记忆流转机制

```
观察在多个会话中稳定
    │
    ↓
写入器检测到稳定模式
    │
    ↓
从会话记忆提升到项目记忆
    │
    ↓
更新 MEMORY.md
    │
    ↓
清除相关会话记忆条目
```

这种机制确保：
- **项目记忆保持精炼**：只包含经过验证的稳定知识
- **会话记忆保持最新**：只包含当前工作状态
- **历史保持完整**：作为最终的回退来源

## 动态工作流执行引擎

Dynamic Workflow 是 MiMo Code 解决大规模任务编排的核心机制。它将编排逻辑从自然语言转为代码，确保确定性执行。

### 设计动机

传统方法（SKILL.md + 自然语言）的问题：

| 问题 | 说明 | Dynamic Workflow 的解决 |
|------|------|------------------------|
| **上下文压缩吞没步骤** | 压缩时可能丢失关键步骤 | 代码逻辑不受压缩影响 |
| **模型跳过阶段** | 模型可能"认为"某些步骤不重要 | 代码强制执行每个步骤 |
| **分支逻辑依赖判断** | 模型的分支判断可能错误 | 代码的 if/else 是确定性的 |
| **重试逻辑不可靠** | 模型可能忘记重试 | 代码的循环是可靠的 |
| **执行路径不一致** | 同一流程两次运行可能不同 | 代码保证一致性 |

### 核心 API

```javascript:appendix-e/mimocode/agent-core.js
// 调度子智能体
const result = await agent({
  prompt: "实现用户认证模块",
  model: "mimo-v2.5-pro",
  tools: ["read", "write", "edit"]
});

// 并行执行
const results = await parallel([
  agent({ prompt: "实现登录接口" }),
  agent({ prompt: "实现注册接口" }),
  agent({ prompt: "实现密码重置" })
]);

// 顺序执行
await pipeline([
  agent({ prompt: "设计数据库 schema" }),
  agent({ prompt: "实现数据访问层" }),
  agent({ prompt: "实现 API 接口" })
]);

// 调用其他脚本
await workflow("./scripts/test-all.js");
```

### 执行保证

Dynamic Workflow 提供以下保证：

1. **确定性**：相同的输入产生相同的输出
2. **原子性**：每个 agent() 调用要么完全成功，要么完全失败
3. **可恢复性**：每个 agent() 的结果同步写入磁盘，中断后可从日志恢复
4. **隔离性**：每个 agent() 在隔离沙箱中执行，互不干扰

### 与 Anthropic Dynamic Workflow 的兼容性

MiMo Code 的实现兼容 Anthropic Dynamic Workflow 的核心语义，并扩展了以下能力：

| 能力 | 说明 |
|------|------|
| **`workflow()` 原语** | 脚本可以调用其他脚本，实现可复用和组合 |
| **结果持久化** | 每个 `agent()` 调用的结果同步写入磁盘 |
| **沙箱文件操作** | 在沙箱内可以直接读写文件 |

## 记忆层 API 参考

### SessionMemoryStore

```typescript:appendix-e/mimocode/session-store.ts
interface SessionMemoryStore {
  read(sessionId: string, key?: string): Promise<MemoryEntry | Record<string, MemoryEntry> | null>;
  write(sessionId: string, key: string, value: MemoryEntry, options?: WriteOptions): Promise<void>;
  query(sessionId: string, filter: QueryFilter): Promise<MemoryEntry[]>;
  clear(sessionId: string, keyPattern?: string): Promise<v
```

### ProjectMemoryStore

```typescript:appendix-e/mimocode/project-store.ts
interface ProjectMemoryStore {
  read(projectId: string, key?: string): Promise<MemoryEntry | Record<string, MemoryEntry> | null>;
  write(projectId: string, key: string, value: MemoryEntry, options?: WriteOptions): Promise<void>;
  query(projectId: string, filter: QueryFilter): Promise<MemoryEntry[]>;
  search(projectId: string, query: string, options?: SearchOptions): Promise<MemoryEntry[]>;
  compact(projectId: string, options?: CompactOptions): Promise<void>;
}
```

### GlobalMemoryStore

```typescript:appendix-e/mimocode/global-store.ts
interface GlobalMemoryStore {
  read(userId: string, key?: string): Promise<MemoryEntry | Record<string, MemoryEntry> | null>;
  write(userId: string, key: string, value: MemoryEntry, options?: WriteOptions): Promise<void>;
  list(userId: string, options?: ListOptions): Promise<string[]>;
  archive(userId: string, key: string, options?: ArchiveOptions): Promise<void>;
}
```

### HistoryStore

```typescript:appendix-e/mimocode/history-store.ts
interface HistoryStore {
  append(sessionId: string, entry: HistoryEntry): Promise<void>;
  list(sessionId: string, options?: ListOptions): Promise<HistoryEntry[]>;
  get(sessionId: string, entryId: string): Promise<HistoryEntry | null>;
  prune(sessionId: string, before?: Date, keepLatest?: number): Promise<void>;
}
```

## 状态转换条件表

| 当前状态 | 触发条件 | 下一状态 | 说明 |
|----------|-----------|----------|------|
| **IDLE** | 用户发送消息 | **THINKING** | 接收到用户输入，开始推理 |
| **THINKING** | 推理完成 | **TOOL_CALLING** | 模型形成计划，准备执行工具 |
| **TOOL_CALLING** | 工具返回结果 | **THINKING** | 工具执行完成，回到推理状态 |
| **任何状态** | token 阈值达到 20% | **CHECKPOINTING** | 达到第一个检查点，保存状态 |
| **任何状态** | token 阈值达到 45% | **CHECKPOINTING** | 达到第二个检查点，增量保存 |
| **任何状态** | token 阈值达到 70% | **CHECKPOINTING** | 达到第三个检查点，准备重建 |
| **CHECKPOINTING** | 写入完成 | **REBUILDING** | 检查点保存完成，开始重建 |
| **REBUILDING** | 上下文重建完成 | **THINKING** | 重建完成，恢复推理 |
| **任何状态** | 目标达成或收到停止信号 | **COMPLETED** | 任务完成，进入完成状态 |

## 子智能体系统

子智能体系统是 MiMo Code 实现大规模任务编排的核心。它支持并行、顺序和混合执行模式，确保复杂任务的可靠性和可扩展性。

### 生命周期状态机

子智能体拥有完整的状态机管理生命周期：

| 状态 | 说明 | 进入条件 | 退出条件 |
|------|------|----------|----------|
| **PENDING** | 等待调度 | 创建子智能体 | 被调度器分配 |
| **RUNNING** | 正在执行 | 被调度器分配 | 完成或失败 |
| **WAITING_FOR_TOOLS** | 等待工具结果 | 请求工具 | 工具返回结果 |
| **COMPLETED** | 执行成功 | 所有任务完成 | 被清理或归档 |
| **FAILED** | 执行失败 | 遇到错误 | 被重试或取消 |
| **CANCELLED** | 已取消 | 用户或系统请求取消 | 被清理 |

### 子智能体生命周期 API

```typescript:appendix-e/mimocode/subagent-api.ts
// 创建子智能体
function createSubAgent(config: SubAgentConfig): Promise<SubAgent>;

// 列出所有子智能体
function listSubAgents(filter?: SubAgentFilter): Promise<SubAgent[]>;

// 获取子智能体状态
function getSubAgentStatus(agentId: string): Promise<SubAgentStatus>;

// 取消子智能体
function cancelSubAgent(agentId: string, reason?: string): Promise<void>;

// 等待子智能体完成
function waitForSubAgent(agentId: string, timeout?: number): Promise<SubAgentResult>;
```

### 调度策略

子智能体系统支持多种调度策略：

1. **并行调度**：同时执行多个子智能体，提高吞吐量
2. **顺序调度**：按依赖关系依次执行，确保正确性
3. **混合调度**：根据任务复杂度动态选择策略

### 执行保证

- **隔离性**：每个子智能体在独立沙箱中执行
- **可恢复性**：每个子智能体的执行状态持久化
- **超时控制**：每个子智能体都有超时限制
- **错误处理**：子智能体失败时自动重试或回滚

- **生命周期**：持久化，完整保留
- **内容**：每个会话的完整追踪——每条消息和工具调用的原始文本
- **访问方式**：通过 `history` 工具按需查询
- **用途**：当结构化记忆中找不到细节时，回溯到原始记录

### 记忆流转机制

```
观察在多个会话中稳定
    │
    ↓
写入器检测到稳定模式
    │
    ↓
从会话记忆提升到项目记忆
    │
    ↓
更新 MEMORY.md
    │
    ↓
清除相关会话记忆条目
```

这种机制确保：
- **项目记忆保持精炼**：只包含经过验证的稳定知识
- **会话记忆保持最新**：只包含当前工作状态
- **历史保持完整**：作为最终的回退来源

## 动态工作流执行引擎

Dynamic Workflow 是 MiMo Code 解决大规模任务编排的核心机制。它将编排逻辑从自然语言转为代码，确保确定性执行。

### 设计动机

传统方法（SKILL.md + 自然语言）的问题：

| 问题 | 说明 | Dynamic Workflow 的解决 |
|------|------|------------------------|
| **上下文压缩吞没步骤** | 压缩时可能丢失关键步骤 | 代码逻辑不受压缩影响 |
| **模型跳过阶段** | 模型可能"认为"某些步骤不重要 | 代码强制执行每个步骤 |
| **分支逻辑依赖判断** | 模型的分支判断可能错误 | 代码的 if/else 是确定性的 |
| **重试逻辑不可靠** | 模型可能忘记重试 | 代码的循环是可靠的 |
| **执行路径不一致** | 同一流程两次运行可能不同 | 代码保证一致性 |

### 核心 API

```javascript:appendix-e/mimocode/dynamic-workflow.js
// 调度子智能体
const result = await agent({
  prompt: "实现用户认证模块",
  model: "mimo-v2.5-pro",
  tools: ["read", "write", "edit"]
});

// 并行执行
const results = await parallel([
  agent({ prompt: "实现登录接口" }),
  agent({ prompt: "实现注册接口" }),
  agent({ prompt: "实现密码重置" })
]);

// 顺序执行
await pipeline([
  agent({ prompt: "设计数据库 schema" }),
  agent({ prompt: "实现数据访问层" }),
  agent({ prompt: "实现 API 接口" })
]);

// 调用其他脚本
await workflow("./scripts/test-all.js");
```

### 执行保证

Dynamic Workflow 提供以下保证：

1. **确定性**：相同的输入产生相同的输出
2. **原子性**：每个 agent() 调用要么完全成功，要么完全失败
3. **可恢复性**：每个 agent() 的结果同步写入磁盘，中断后可从日志恢复
4. **隔离性**：每个 agent() 在隔离沙箱中执行，互不干扰

### 与 Anthropic Dynamic Workflow 的兼容性

MiMo Code 的实现兼容 Anthropic Dynamic Workflow 的核心语义，并扩展了以下能力：

| 能力 | 说明 |
|------|------|
| **`workflow()` 原语** | 脚本可以调用其他脚本，实现可复用和组合 |
| **结果持久化** | 每个 `agent()` 调用的结果同步写入磁盘 |
| **沙箱文件操作** | 在沙箱内可以直接读写文件 |

## 架构优势总结

MiMo Code 的架构设计解决了长任务自动化的三个核心挑战：

| 挑战 | 解决方案 | 效果 |
|------|---------|------|
| **决策错误累积** | Max Mode + Goal | 单步错误率降低 10-20% |
| **上下文耗尽** | 检查点 + 四层记忆 + 重建 | 逻辑会话无限延伸 |
| **经验无法积累** | Dream + Distill | 跨会话持续改进 |

这些设计使得 MiMo Code 在 200+ 步骤的长任务中，相比 Claude Code 有 65%+ 的胜率。

## 常见反模式

**反模式一：让主智能体自己维护记忆。** 很多开发者的第一反应是让主智能体在工作过程中顺手记录笔记，觉得"顺手记一下"效率最高。但在长任务中，要求一个正在调试复杂问题的模型同时维护结构化日志，会导致两项任务都做得更差。模型会把有限的注意力分散到"记录"和"工作"之间，笔记质量低且工作质量也下降。MiMo Code 的设计明确禁止主智能体写入结构化文件（除了 `notes.md` 暂存区），提取完全由独立的写入器子智能体完成。写入器不消耗主智能体的 token 预算，也不参与实际工作，因此不存在注意力竞争。这个"单写入者"原则是防止并发写入导致不一致状态的最简单不变量。

**反模式二：等到上下文快满了再做检查点。** 直觉上，在窗口快满时一次性压缩似乎最高效——毕竟每次都提取确实"浪费" token。但实际效果恰恰相反。模型在高上下文利用率下的压缩能力严重退化，文献称之为"中间丢失"：输入越长，对中间部分的注意力越差，结构化提取的可靠性显著下降。在 95% 利用率时让模型做最关键的压缩，相当于在最疲劳的时候做最重要的决策。MiMo Code 在 20%、45%、70% 三个阈值触发检查点，每次增量更新，而非等到最后一次性提取。这样每次提取时模型还有充足的"思考空间"，提取质量远高于临满时的一次性压缩。

**反模式三：用自然语言定义复杂工作流。** 把"先做 A，然后做 B，如果发生 C 就做 D"写进 SKILL.md，让模型自己理解并执行——在简单场景下没问题，但在复杂工作流中系统性失败。上下文压缩可能吞没步骤，模型可能"认为"某些步骤不重要就跳过了，分支逻辑和重试逻辑依赖模型的判断而非代码保证，同一流程两次运行可能走不同的路径。Dynamic Workflow 把编排逻辑从提示词转为 JavaScript 代码，`if` 语句不会忘记分支，`for` 循环不会提前退出，barrier 不会遗漏子智能体。模型的判断应该用在"理解和生成代码"上，而不是浪费在"流程控制"上。

## 常见失败与陷阱

**陷阱一：检查点写入器的写入时机与主智能体冲突。** 写入器子智能体在后台运行，不阻塞主智能体，两者互不干扰。但有一个微妙的时序问题：如果主智能体在写入器读取对话历史的瞬间刚好发起了新的工具调用，写入器可能读到不完整的状态。MiMo Code 通过"快照"机制解决这个问题：写入器在触发时立即对当前对话历史做快照，后续新消息不干扰已完成的快照读取。如果你自己实现类似的写入器子智能体，务必确保写入器操作的是对话历史的某个一致时间点的快照，而非实时流。

**陷阱二：重建注入的 token 预算分配不当。** 上下文重建时，系统按优先级注入持久化内容，每个部分有独立的 token 限制，总预算约 65K tokens。但如果你手动调整配置（比如把"最近用户消息"的预算设得太大），可能挤占其他部分的空间，导致项目记忆或任务列表被截断。最常见的情况是把"最近用户消息"的预算留得过多，结果项目记忆只注入了一半，智能体醒来后"记不清"之前的架构决策。默认的预算分配经过大量测试优化，不建议轻易改动。如果确实需要调整，先用 `--dry-run` 模式观察注入各部分的实际 token 分配情况。

**陷阱三：MEMORY.md 膨胀导致信息过载。** 项目记忆文件会随时间增长。如果不维护，过时的条目、重复记录和无效文件引用逐渐积累，信噪比下降。Dream 机制每 7 天自动合并和去重，但如果你在两个 Dream 周期之间手动大量添加记忆条目（比如一次性导入几十条"技术事实"），智能体在重建时需要从膨胀的 MEMORY.md 中提取关键信息，这本身就会消耗大量 token 且降低提取质量。建议定期手动清理明显过时的条目，不要等 Dream 自动处理。特别是那些"验证了但已不再适用"的条目，它们比缺失信息更危险——智能体会信任 MEMORY.md 中的每一条记录。

## 下一步

- 想了解具体的驾驭工程优化？→ [驾驭工程优化设计](./harness-optimizations.md)
- 想了解具体的循环工程优化？→ [循环工程优化设计](./loop-optimizations.md)
- 想对比 OpenCode？→ [MiMo Code vs OpenCode 对比分析](./comparison.md)
