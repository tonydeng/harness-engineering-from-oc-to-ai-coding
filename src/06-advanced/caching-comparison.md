# 缓存机制深度对比：OpenCode vs Claude Code vs Pi Agent

> Prompt Caching 已从可选优化变为必须工程化的核心能力。三大 AI 编码工具在缓存与上下文压缩上形成了三种截然不同的工程范式——理解它们的差异，直接影响长会话的 Token 成本和响应质量。
> **适合读者**: 架构师 · 效率开发者 · 工程经理

## 文章概述

在 AI 编码工作流中，大部分 Token 被花在了重复内容上。每次 Agent 请求都携带系统指令、项目上下文、工具定义和对话历史前缀——这些内容在同一会话甚至跨项目中几乎不变。缓存和上下文压缩（Compaction）就是为了解决这个问题而设计的，但两者的工作方式和使用成本截然不同。

本文从"缓存 ≠ 压缩"这个核心洞察出发，分别分析三大工具的缓存和压缩实现——OpenCode 的三级缓存架构、Claude Code 的 5 级渐进压缩 Pipeline、Pi Agent 的极简可扩展 Compaction。然后提供每个工具中**如何激活缓存**的配置指南，以及围绕缓存能力的**最佳开源项目和插件**。最后，通过成本对比和趋势分析，帮助读者在不同场景下做出合理选择。

> **⏱ 时间有限？先读这些：** 缓存 vs 压缩 → 各工具开启方式对比表 → 选型矩阵

## 缓存 ≠ 压缩：理解两套机制

这是理解整篇文章的第一原则。缓存和压缩做的是两件不同的事：

| 维度 | 缓存（Prompt Caching） | 压缩（Compaction） |
|------|----------------------|-------------------|
| **本质** | 消除重复传输 | 精简必要内容 |
| **副作用** | **零副作用**——缓存命中和未命中的输出一致 | **有损**——压缩后的信息是摘要，不是原始内容 |
| **成本影响** | 命中时读价格 0.1x（Anthropic 90% 折扣） | 每次压缩消耗一次 LLM 调用 |
| **对质量的影响** | 不影响输出质量 | 摘要可能丢失细节 |
| **适用场景** | 重复的系统指令、工具定义、固定前缀 | 对话历史太长、工具输出过多 |
| **失败模式** | Cache Miss——退化为正常请求价格 | 压缩过度——Agent 丢失关键上下文 |

**核心关系**：压缩是缓存前缀的天敌。压缩会修改消息结构，导致 cache key 变化，使之前缓存的全部失效（Cache Miss）。Cache-Aligned Compaction 的设计目标就是"如何压缩但不破坏缓存"——这个话题在后面各工具中会多次出现。

---

## OpenCode：三级缓存 + 阶梯式治理

### 缓存架构

OpenCode 拥有三大工具中最完整的多级缓存体系。缓存直接在 `opencode.json` 中配置：

```json
{
  "cache": {
    "session": {
      "enabled": true,
      "maxSize": 100000,
      "maxAge": "session"
    },
    "project": {
      "enabled": true,
      "maxSize": 500000,
      "maxAge": "24h",
      "patterns": ["**/*.md", "**/AGENTS.md", "**/package.json"]
    },
    "global": {
      "enabled": true,
      "maxSize": 2000000,
      "maxAge": "7d",
      "patterns": ["~/.opencode/global/**"]
    }
  }
}
```

| 层级 | 范围 | 命中率 | 生命周期 | 管理方式 |
|------|------|--------|---------|---------|
| **L1 Session** | 单次对话内 | ~95% | 会话全程 | 自动 |
| **L2 项目** | 同一项目跨 Session | ~80% | 24h（可配） | 自动 |
| **L3 全局** | 跨项目全局共享 | ~60% | 7d（可配） | 手动标记 |

**缓存断点（Breakpoints）**：用户通过注释语法手动标记可复用上下文片段：

```text:terminal
#cache-breakpoint: project-rules
AGENTS.md 中定义的所有约束规则
#cache-breakpoint: end
```

断点生命周期：**创建 → 引用 → 更新 → 失效**。具体参见 → [提示词缓存机制](context/prompt-caching.md)。

### Compaction 机制

OpenCode 采用两层压缩：

- **工具输出修剪（Prune）**：给旧消息打时间戳使其"不可见"（非物理删除，仍存数据库）。阈值：总工具输出 > 40K token。
- **LLM 摘要压缩**：隐藏的专用 Compaction Agent 生成 5 段式摘要，压缩后自动重放最后用户消息——用户完全无感知。

溢出保护通过 `compaction.reserved` 控制预留缓冲区。具体触发阈值、微压缩策略和保真度实测数据，参见 → [上下文压缩与Token 预算](context-compression.md)。

### 如何激活缓存

| 机制 | 激活方式 | 备注 |
|------|---------|------|
| 三级缓存 | `opencode.json` 配置 `cache` 块 | L2/L3 需主动配置，L1 默认开启 |
| Compaction | `compaction.auto: true`（默认开启） | 可配置 `reserved` 缓冲区大小 |
| **Prefix Preservation** | 环境变量 `OPENCODE_EXPERIMENTAL_COMPACTION_PRESERVE_PREFIX=true` | 实验性，复用 Agent 前缀缓存，实测 99% cache hit |
| **Cache-Aligned Compaction** | 环境变量 `OPENCODE_EXPERIMENTAL_CACHE_ALIGNED=true` | 实验性，节省 ~90% Compaction 成本 |
| 自定义 Compaction Prompt | 环境变量 `OPENCODE_EXPERIMENTAL_COMPACTION_PROMPT` | 自定义摘要格式指令 |
| **Double-Buffer** | `compaction.checkpointThreshold` 和 `compaction.swapThreshold` | ~50% 时后台 Checkpoint，~75% 时 Swap |
| 缓存断点 | Markdown 中 `#cache-breakpoint` 注释 | 手动标记可复用片段 |

### 相关开源项目与插件

| 项目/插件 | 说明 | 链接 |
|----------|------|------|
| **DCP 插件** | 内置插件，AI 驱动的深度上下文剪枝，与 Compaction 互补 | OpenCode 内置 |
| **opencode-contrib** | 社区贡献的配置模板和缓存策略示例 | GitHub: anomalyco/opencode-contrib |
| **TokenPilot**（学术） | Cache-Efficient Context Management for LLM Agents，arXiv 2606.17016 | arXiv, 2026-06 |
| **opencode-cache-monitor** | 社区脚本，监控缓存命中率和 Token 消耗趋势 | GitHub 社区 |

---

## Claude Code：5 级渐进压缩 + Prompt Caching 原生集成

### 缓存架构

Claude Code 的缓存哲学是"最便宜的先做，最贵的最后做"。与 OpenCode 不同，**它没有独立的多级缓存架构**——缓存完全依赖 Anthropic API 的 Prompt Caching，并在 Compaction 策略中深度集成 cache-aware 设计。

#### Anthropic Prompt Caching 机制

| 参数 | 值 |
|------|-----|
| 缓存读价格 | **0.1x** 基础输入价（90% 折扣） |
| 缓存写价格（5min TTL） | **1.25x** 基础输入价 |
| 缓存写价格（1h TTL） | **2x** 基础输入价 |
| 缓存最小大小 | 1,024 tokens（Sonnet/Haiku），2,048 tokens（Opus） |
| 缓存 TTL | 5 分钟（每次命中刷新），可扩展至 1h |
| 最大缓存断点数 | 4 个/请求 |

Claude Code 通过 `SYSTEM_PROMPT_DYNAMIC_BOUNDARY` 将一个 `__boundary__` 哨兵字符串插入系统提示，将指令分为：

- **静态半**（哨兵前）：核心指令、工具描述、安全规则 → `scope: 'global'` 全局缓存
- **动态半**（哨兵后）：MCP 指令、输出偏好、语言设置 → 不全局缓存

### 5 级渐进式压缩 Pipeline

| 层级 | 触发条件 | 操作 | Cache 影响 |
|------|---------|------|-----------|
| **T1 Microcompact** | 每 API 调用前 | 保留最近 5 个工具结果，替换其余为标记清理 | **Cache 友好**：排队 `cache_edits`，服务端精确删除 |
| **T2 API-Native** | 服务端自动 | 移除旧 thinking/tool_use/tool_result 块 | 零客户端开销 |
| **T3 Full Compaction** | ~83.5%（167K/200K） | **9 段式结构化摘要** + cache-safe forking | 复用父会话 cache key |
| **T4 Context Collapse** | ~90% 利用率 | 摘要存 collapse store，可逆 | 保留原始消息 |
| **T5 Sub-agent** | 极少见 | 重型探索路由到子 Agent | 主会话稳定 |

**cache-safe forking**（T3 的关键创新）：不修改父会话消息，而是 fork 出一个新分支复用自己的系统提示、工具定义和消息前缀——服务端看到相同的 cache key → hits。

### 如何激活缓存

| 机制 | 激活方式 | 备注 |
|------|---------|------|
| 自动 Compaction | **默认开启**，无需配置 | 接近 200K 窗口上限自动触发 |
| Manual Compaction | `/compact` 命令 | 可附带自定义压缩指令 |
| Compaction 阈值 | `compact_20260112` API beta：最小 50K，默认 150K | 通过 API 配置 |
| 自定义摘要指令 | `/compact` 后加自然语言描述 | 例如 `/compact 重点保留架构决策和 API 设计` |
| 推理 Token 预算 | `--effort` 参数：low/medium/high/xhigh/max/ultracode | `claude --effort high` |
| 会话安全网 | `maxTurns`（最大交互轮次）| 通过 claude.json 配置 |
| 美元上限 | `maxBudgetUsd` | 通过 claude.json 配置 |
| 超时控制 | `API_TIMEOUT_MS` 等环境变量 | 自定义 API 超时 |
| **CLAUDE.md** 持久规则 | 项目根目录创建 CLAUDE.md | 每轮请求重新注入，不因压缩丢失 |
| 会话持久化 | `sessionId` 参数 | 跨多次 `query()` 保留上下文 |
| **Agent checkpointing**（Beta） | Claude Code v2.1.128+ | 2026 年 6 月功能 |

### 相关开源项目与插件

| 项目/插件 | 说明 | 链接 |
|----------|------|------|
| **claude-code** | 官方 CLI（闭源），缓存机制通过 Anthropic API 原生实现 | GitHub: anthropics/claude-code |
| **anthropic-caching-examples** | Anthropic 官方的 Prompt Caching 示例代码 | GitHub: anthropics/anthropic-cookbook |
| **TokenPilot** | 缓存优先的 Agent 上下文管理器（学术研究） | arXiv 2606.17016 |
| **Don't Break the Cache**（论文） | 长周期 Agent 任务中 Prompt Caching 的实证评估 | arXiv 2601.06007 |
| **@anthropic-ai/sdk** | Anthropic SDK，`cache_control` 参数支持自定义缓存断点 | npm |
| **claude-code-extensions** | 社区扩展集合，包括 PreCompact Hook 示例 | GitHub 社区 |

---

## Pi Agent：极简 Compaction + Extension 自定义

### 缓存架构

Pi Agent 的设计哲学是"极简核心，强力扩展"——**它没有内置的多级缓存**，也不依赖 Provider 级 Prompt Caching。缓存管理完全通过 Compaction 实现，而 Compaction 行为可通过 Extension API 完全自定义。

#### Compaction 核心流程

```
Find Cut Point → Extract Messages → Generate Summary → Append Entry → Reload
```

整个过程由 `pi-agent-core/harness/compaction/compaction.ts` 中的 `summarizeWithBudget()` 驱动：

1. **Find Cut Point**：从最新消息向前遍历，累积 token 估算直到 `keepRecentTokens`（默认 20K）
2. **Extract Messages**：收集上一次保留边界到切点之间的消息
3. **Generate Summary**：调用 LLM 生成结构化摘要，传递上一次摘要作为迭代上下文
4. **Append Entry**：保存 `CompactionEntry`（含摘要和 `firstKeptEntryId`）
5. **Reload**：Session 重载，使用摘要 + `firstKeptEntryId` 之后的消息

#### Provider 模型缓存成本定义

Pi Agent 的 Provider 模型定义中可指定缓存成本字段：

```typescript
// Provider 定义中的缓存字段
{
  "model": "claude-sonnet-4",
  "pricing": {
    "input": 3.0,
    "output": 15.0,
    "cacheRead": 0.3,   // 缓存读价格（0.1x）
    "cacheWrite": 3.75  // 缓存写价格（1.25x）
  }
}
```

这样即使 Pi Agent 不管理缓存，也能在 Token 成本统计中准确反映实际花费。

### 如何激活缓存

| 机制 | 激活方式 | 备注 |
|------|---------|------|
| 自动 Compaction | `settings.json` 中 `enabled: true` | 默认开启 |
| 手动 Compaction | `/compact [prompt]` | 可附带自定义压缩指令 |
| 预留 Token | `reserveTokens: 16384` | 为 LLM 响应预留 |
| 保留最近上下文 | `keepRecentTokens: 20000` | 不被摘要的最近 token 数 |
| Extension 自定义压缩 | 监听 `session_before_compact` 事件 | 可替换默认压缩行为 |
| 切换摘要模型 | Extension 中设置压缩专用模型 | 例如用 Gemini Flash 做摘要 |
| **Context Files** | AGENTS.md / SYSTEM.md / APPEND_SYSTEM.md | 多级加载，不因压缩丢失 |
| **Session Tree** | Fork / Clone / Tree 导航 | 分支上下文隔离 |

**完整配置示例**（`~/.pi/agent/settings.json`）：

```json
{
  "compaction": {
    "enabled": true,
    "reserveTokens": 16384,
    "keepRecentTokens": 20000
  },
  "provider": {
    "primary": { "model": "claude-sonnet-4" },
    "compaction": { "model": "gemini-2.0-flash" }
  }
}
```

> 上述配置中的 `compaction.model` 并非 Pi Agent 内置选项，但可通过 **Extension 自定义压缩** 实现——见下方示例。

### 自定义压缩 Extension 示例

```typescript
// custom-compaction.ts — 替换默认压缩，使用更便宜的模型
import { Extension, AgentSession } from '@earendil-works/pi-coding-agent'

export default {
  name: 'custom-compaction',
  onSessionBeforeCompact: async ({ reason, session }) => {
    // reason: "manual" | "threshold" | "overflow"
    console.log(`Compaction triggered: ${reason}`)
    
    // 替换压缩器为 Gemini Flash，降低摘要成本
    session.compressor = new CustomCompressor({
      model: 'gemini-2.0-flash',
      temperature: 0.3,
      maxTokens: 2048
    })
  }
}
```

### 相关开源项目与插件

| 项目/插件 | 说明 | 链接 |
|----------|------|------|
| **pi** | Pi Agent 本体（MIT 开源），核心在 `packages/coding-agent/harness/compaction/` | GitHub: earendil-works/pi |
| **pi-extension-examples** | 官方 Extension 示例，含自定义 Compaction 实现 | pi Agent 仓库 `examples/extensions/` |
| **custom-provider-template** | 自定义 Provider 模板，包含 cacheRead/cacheWrite 成本字段 | pi Agent 仓库 |
| **gondolin** | Pi 的沙箱隔离方案（可选），不影响缓存但保护上下文 | GitHub: earendil-works/gondolin |

---

## 成本对比与选型建议

### 典型场景 Token 成本对比

| 场景 | OpenCode | Claude Code | Pi Agent |
|------|----------|-------------|----------|
| **短 Session（5 轮）** | 三级缓存节省 60-70% 重复内容 | 0.1x 缓存读 + Microcompact | 上下文小，基本无需 Compaction |
| **长 Session（50 轮）** | Compaction + Cache-Aligned（实验性）节省 ~90% | 5 级渐进 + 缓存读 0.1x，综合最优 | 依赖 Extension 自定义压缩 |
| **跨项目共享** | L3 全局缓存（7d TTL） | 无跨项目缓存 | 无跨项目缓存 |
| **本地模型** | 不依赖 Provider 缓存，Compaction 成本仅 LLM 摘要 | 仅支持 Anthropic | 不依赖 Provider 缓存 |

### 选型决策矩阵

| 场景 | 推荐工具 | 理由 |
|------|---------|------|
| **长 Session 成本敏感** | Claude Code | Prompt Caching 原生，5 级渐进保证缓存命中率，性价比最优 |
| **多模型灵活切换** | OpenCode | 75+ Provider，Cache-Aligned Compaction 跨模型工作 |
| **嵌入式 / 极致定制** | Pi Agent | Extension 完全自定义压缩行为 |
| **本地模型 / 预算有限** | OpenCode 或 Pi | 不依赖 Provider 级缓存 |
| **开源 / 研究需求** | Pi Agent 或 OpenCode | 均 Apache 2.0/MIT 开源，源码可读 |

### 跨工具通用最佳实践

1. **先命缓存，再压缩**——缓存消除重复传输（零副作用），压缩精简必要内容（有损）。优化顺序：先确保缓存命中率达标（>80%），再考虑压缩策略。

2. **在自然断点手动 `/compact`**——比自动压缩更可控。任务完成一个阶段后手动压缩，避免 Agent 在任务中间被截断。

3. **监控缓存命中率**——低于 60% 说明配置有问题。对于 Anthropic 用户，检查是否有太多动态内容破坏缓存前缀。

4. **保持配置文件简洁**——CLAUDE.md 或 AGENTS.md 越稳定，缓存命中率越高。频繁变动的配置文件是缓存的最大杀手。

5. **理解 TTL 的成本含义**——Anthropic 5min TTL 意味着**连续工作比间歇工作更便宜**。长时间中断后第一次请求缓存未命中需交全价。

---

## 趋势：Cache-Aligned Compaction 成为共识

2026 年的重要趋势是，三大工具在缓存意识上趋于一致：

- **OpenCode**（2026-04）实验性推出 Cache-Aligned Compaction（PR #25100），通过保持消息序列化与普通请求一致、仅在末尾追加摘要指令来复用缓存前缀
- **Claude Code** 从设计之初就采用 cache-safe forking，Full Compaction 时复用父会话缓存 key
- **Pi Agent** 的 Extension 架构允许社区自行实现 cache-aware 压缩策略

**底层原因**：随着 Anthropic/OpenAI/Google 等 Provider 的 Prompt Caching 定价逐步标准化（读 0.1x vs 写 1.25x），缓存命中率直接决定了 AI 编码工具的实际运营成本。不 cache-aware 的 Compaction 会破坏缓存前缀，导致每次压缩后都需重新缓存——成本从 0.1x 涨回 1x，差距可达 10 倍。

可以预见，**Cache-Aligned 设计将在 2026 年底前从"实验性特性"升级为所有 AI 编码工具的标准特性**。未来读者在评估编码工具时，缓存命中率和 Cache-Aligned 设计将与模型能力、工具生态并列为核心决策维度。

## 关联章节

- → [提示词缓存机制](context/prompt-caching.md)（OpenCode 三级缓存架构详解）
- → [上下文压缩与Token 预算](context-compression.md)（OpenCode Compaction 完整技术栈与实测数据）
- ← [上下文工程核心](../../02-core-concepts/context-engineering-core.md)（上下文工程在 L2 中的定位）
- → [记忆系统设计](memory-system.md)（记忆系统与缓存的协同工作）
- → [性能调优与成本管理](context/performance-tuning.md)（各 Provider 的 Token 定价策略）
