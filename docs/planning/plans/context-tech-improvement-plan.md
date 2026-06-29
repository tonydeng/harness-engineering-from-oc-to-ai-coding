# 上下文技术章节改善计划

**创建日期**: 2026-06-14
**来源**: 3 路深度研究（DCP/插件生态、高级工程技术、全工具生态）
**目标**: 在现有 4 篇文章基础上补充可落地的上下文利用率提升技术

---

## 一、核心发现

### 发现 1：现有内容有三大维度空白

| 维度 | 现有覆盖 | 缺口 |
|------|----------|------|
| **管理 Token 空间** | ✅ 压缩/缓存/预算 | — |
| **管理代码结构** | ❌ | 语义分块、代码库上下文检索 |
| **管理 Agent 行为** | ❌ | 上下文注入模式、长程连贯性、质量度量 |
| **管理跨工具生态** | ❌ | 跨模型适配、多工具共享上下文 |

### 发现 2：行业共识已转向

> "当前瓶颈不是模型能力，而是上下文检索质量。" — The AI Runtime, 2026

意味着投资上下文工程的投资回报率 > 投资下一个模型升级。

### 发现 3：OpenCode 生态已有成熟工具

DCP（3,300⭐）、Supermemory（1,322⭐）、context-mode（17,000⭐）、OMO（54+ hooks）等工具已量产可用。

---

## 二、建议新增文章（5 篇 + 2 篇更新）

### 🔴 P0（高优先级 — 核心缺口）

#### 新增 1：上下文质量度量与可观测性

**为什么需要**：现有内容只教"怎么做"（配置压缩/缓存/预算），没有教"怎么知道做得好不好"。

**核心内容**：
1. 四大质量框架：HumanLayer（正确性>完整性>大小>方向）、Wire（5维度）、Scorable（检索质量×窗口组合×利用率）、IBM
2. 五个黄金指标：Context Utilization Rate, Information Density, Compression Ratio, Cache Hit Rate, Task Completion Rate
3. CLI 监控：`/dcp context`（DCP 插件）查看 token 分布，`/context`（context-mode）实时预览
4. 健康范围速查：利用率 60-80%、缓存命中 > 80%、压缩比 3:1–5:1
5. 从指标到行动：什么指标触发什么调整

**参考文献**：HumanLayer Blog, Scorable Framework, Wire Five Dimensions

**估算篇幅**: ~350 行

---

#### 新增 2：选择性上下文注入模式

**为什么需要**："不让 Agent 一次看完所有东西"是提升上下文利用率最直接的手段。

**核心内容**：
1. **延迟加载**（Lazy Loading）：Skill 描述层（~50 tokens）vs 完整内容（500-3000 tokens），Opencode 原生支持，CLAUDE.md 分层设计
2. **预取**（Pre-fetching）：Session 启动时预加载高频内容，workflow-aware 预取
3. **分层上下文**（Tier 1-2-3）：
   - Tier 1（热）：最近 15-25 轮对话，原文保留
   - Tier 2（温）：当前 Session 滚动摘要，600-1200 tokens
   - Tier 3（冷）：项目级归档知识
4. **缓存感知组装**：两区架构（stable prefix + dynamic chunks），避免破坏 Provider 前缀缓存
5. **OpenCode 实现**：Plugin Hook（session.created）加载 Tier 3，Skill 描述层实现 Lazy Loading

**参考文献**：Vercel Skills 实测（~97.5% 节省）、Context Assembly Layer（CAL）论文、SurePrompts Attention Pattern 分析

**估算篇幅**: ~400 行

---

### 🟡 P1（中优先级 — 生态补齐）

#### 新增 3：代码语义分块与智能检索

**为什么需要**：代码是树结构，文本分割把函数切半、API 签名和实现分离，导致 Agent 理解错误。

**核心内容**：
1. 为什么文本分割对代码无效：Agent 引用未定义变量、错误方法签名
2. AST 分块流程：parse → extract entities → build scope tree → greedy window → contextualizedText
3. 工具选型：`supermemoryai/code-chunk`（最成熟）、`Nugine/astchunk`（Rust，cAST 论文）、`oguzhankir/omnichunk`（15+ 语言）
4. 量化效果：AST 分块 Recall@5 = 70.1% vs 朴素文本 49%（+43%）
5. Context-RAG 四层频谱：snippet-aware → file-aware → repo-aware → org-aware
6. 检索工具选型：Sourcegraph MCP（SCIP 符号索引）、vexp MCP（依赖图遍历，减少 65-70% token）、opencode-context-manager（静态分析，97-99% 增量节省）

**估算篇幅**: ~450 行

---

#### 新增 4：DCP 与高级上下文管理插件实战

**为什么需要**：OpenCode 原生 Compaction 只是基础，社区已出现更强大的方案。

**核心内容**：
1. **DCP（@tarquinen/opencode-dcp）——3,300⭐**：AI-driven 替代 Compaction，模型驱动压缩 vs 系统自动压缩
   - 三大自动策略：去重、SupersedeWrites（写后跟读 → 保留读）、PurgeErrors（连续失败 → 移除输入）
   - 命令集：`/dcp context`、`/dcp stats`、`/dcp compress`、`/dcp sweep`
   - 配置：`~/.config/opencode/dcp.jsonc`，支持 per-model overrides
2. **ACM（opencode-acm）**：15+ 显式上下文管理工具（pin/scan/prune/compact/snapshot/diagnose）
3. **opencode-context-guard**：运行时强制上下文执行 — 解决 Agent 20 轮后忘记 AGENTS.md 的问题
4. **opencode-context-manager (fractalswift)**：自动扫描仓库生成模块化上下文文件，后续运行 97-99% token 节省
5. **Plugin 兼容性矩阵**：DCP vs Magic Context vs OMO hooks 冲突分析

**估算篇幅**: ~500 行

---

### 🟢 P2（低优先级 — 锦上添花）

#### 新增 5：跨 Session 记忆 —— 从插件选型到实战配置

**为什么需要**：现有 "记忆系统设计" 文章已有概念说明，但缺少**实战选型指南**和**配置对比**。

**核心内容**：
1. 5 款开源 + 2 款云服务的完整矩阵
2. 各插件的实测对比：延迟、token 开销、召回率、存储占用
3. 配置 checklist：什么场景选什么方案
4. 集成案例：一次配置，跨工具共享记忆

**这篇文章可以理解为 "记忆系统设计" 的姊妹篇** — 那篇讲概念，这篇讲选型和配置。

**估算篇幅**: ~350 行

---

### 更新现有文章（2 篇）

#### 更新 1：Token 预算策略 — 补充插件化预算监控

- 增加 `Opencode-Context-Analysis-Plugin`（138⭐），提供 `/context` 实时 token 分解命令
- 增加 DCP 的 `/dcp context` 和 `/dcp stats` 命令用于预算监控
- 增加多模型预算分配策略（Claude 200K vs GPT 128K vs Gemini 1M）

#### 更新 2：上下文压缩技术 — 补充 DCP 对比

- 增加一节 "DCP：AI 驱动的上下文剪枝"，对比原生 Compaction 和 DCP 的差异
- 增加 DCP 的三大自动策略说明
- 增加 Plugin 冲突说明（DCP 不能与 Magic Context 同时启用）

---

## 三、建议新增文章估算量

| 优先级 | 文章 | 估算行数 | 类型 | 对应缺口维度 |
|--------|------|---------|------|-------------|
| 🔴 P0 | 上下文质量度量与可观测性 | ~350 | 新增 | 管理 Agent 行为 |
| 🔴 P0 | 选择性上下文注入模式 | ~400 | 新增 | 管理 Agent 行为 |
| 🟡 P1 | 代码语义分块与智能检索 | ~450 | 新增 | 管理代码结构 |
| 🟡 P1 | DCP 与高级上下文管理插件实战 | ~500 | 新增 | 管理跨工具生态 |
| 🟢 P2 | 跨 Session 记忆实战选型 | ~350 | 新增 | 管理跨工具生态 |
| — | Token 预算策略更新 | — | 更新 | — |
| — | 上下文压缩技术更新 | — | 更新 | — |

**总计新增**: ~2,050 行（5 篇新文章 + 2 篇更新）

---

## 四、建议的写作顺序

```
Phase 1（基础先行）：
  ├── 上下文质量度量与可观测性
  └── Token 预算策略（更新）

Phase 2（模式与机制）：
  ├── 选择性上下文注入模式
  └── 上下文压缩技术（更新）

Phase 3（代码与检索）：
  ├── 代码语义分块与智能检索
  └── DCP 与高级上下文管理插件实战

Phase 4（完整生态）：
  └── 跨 Session 记忆实战选型
```

---

## 五、关键工具/技术速查

| 技术 | 类型 | GitHub⭐ | 安装方式 | 解决的问题 |
|------|------|---------|---------|-----------|
| DCP | Plugin | 3,300 | `opencode plugin @tarquinen/opencode-dcp` | AI 驱动上下文剪枝替代 Compaction |
| Supermemory | Plugin | 1,322 | `bunx opencode-supermemory@latest install` | 云持久化跨 Session 记忆 |
| context-mode | MCP+Plugin | 17,000 | `plugin: ["context-mode"]` + MCP 配置 | 跨平台上下文沙箱缩减 |
| Magic Context | Plugin | 918 | `npx @cortexkit/magic-context@latest setup` | 后台 historian + Dreamer 无限上下文 |
| ACM | Plugin | — | `plugin: ["opencode-acm"]` | 15+ 显式上下文管理工具 |
| code-chunk | Library | — | `npm i supermemoryai/code-chunk` | AST 语义代码分块 |
| vexp | MCP | — | MCP 配置 | 依赖图上下文检索（-65% token） |
| opencode-context-manager | Plugin | — | `npx opencode-context-manager init` | 自动生成模块化上下文文件 |

---

## 六、会重叠/冲突的内容（需注意）

1. **DCP vs Magic Context**：两者不能同时启用。Magic Context 启动时会自动检测 DCP 循环并禁用自身
2. **DCP vs OMO preemptive-compaction hook**：两者竞争同一作用域，需在行文中说明
3. **上下文可观测性 vs 现有可观测性文章**：现有 observability.md 覆盖 Agent 行为的日志/追踪/度量，新文章覆盖**上下文窗口组成的实时可视化**，是不同的维度
4. **语义分块 vs 上下文压缩**：分块处理"代码库的结构化拆解"，压缩处理"会话历史的精简"，互补关系
