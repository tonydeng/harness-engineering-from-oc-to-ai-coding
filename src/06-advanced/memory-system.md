# 记忆系统设计

> 缓存让 **Agent（智能体）** 记住"系统知道的"，记忆让 Agent 记住"自己经历过的"。OpenCode 原生不包含语义记忆系统，但插件生态提供了多种选择。**本文从概念原理到实战选型，完整覆盖记忆系统的设计与落地——包括 5 款记忆插件的深度对比、决策树、推荐配置和 MCP 记忆服务器方案。**
> **适合读者**: 架构师 · 技术负责人 · 高级用户 · 效率开发者

## 文章概述

缓存是被动的——它存储的是系统预设的内容（系统指令、工具定义、项目知识）。记忆是主动的——它记录的是 Agent 在执行任务过程中的上下文、决策和发现。这是两者的本质区别。记忆系统解决的问题是：当 Agent 从一个 Session 进入下一个 Session 时，如何不忘记之前做过什么、发现过什么、决定了什么。

本文首先澄清"记忆 vs 缓存"的概念差异。然后介绍 OpenCode 记忆插件生态——5 款真实可用的插件，涵盖本地优先、云同步、Claude Code 兼容、蒸馏架构和认知心理学路线。接着分析 Auto-Dream 机制——记忆插件如何自动生成摘要、评估重要度、淘汰低价值记忆。然后介绍 Compaction 与记忆的配合。在安全考虑之后，提供完整的实战选型指南：五款插件速览、全维度对比表、Mermaid 决策树、首选推荐配置、**MCP（模型上下文协议）** 记忆服务器选型和常见误区。读完本文，你将能够根据自身需求选择合适的记忆插件，并配置 Agent 的跨 Session 上下文保持。

> **⏱ 时间有限？先读这些：** 记忆与缓存的区别 → 插件选型 → Auto-Dream 机制 → 实战选型指南（决策树 + 推荐配置）

## 内容要点

1. **记忆 vs 缓存** — 记忆是主动的（Agent"记得"什么），缓存是被动的（系统"存了"什么）。记忆系统解决的核心问题：跨 Session 上下文保持。记忆的三个层次：短期记忆（当前 Session）、中期记忆（相关 Session）、长期记忆（项目级知识）。

2. **插件选型** — 5 款真实插件的设计理念和配置方法：`opencode-mem`（最成熟的 OpenCode 原生插件，SQLite+向量索引，Web UI）、`opencode-supermemory`（云同步记忆，Supermemory API 后端）、`opencode-claude-memory`（移植 Claude Code 的 Memdir 模块，共享记忆目录）、`@loreai/opencode`（蒸馏式三层记忆架构，模拟人类遗忘）、`true-mem`（认知心理学路线，艾宾浩斯遗忘曲线，STM/LTM 双存储）。

3. **Auto-Dream 机制** — 自动生成记忆摘要的工作原理（Session 结束时自动总结），记忆重要度评分（基于任务类型、决策影响、用户反馈），记忆自动淘汰策略及跨 Session 融合。

4. **Compaction 与记忆的配合** — Compaction 在保留重要决策和上下文时如何参考记忆系统的优先级排序，记忆作为 Compaction 的输入来源。

5. **安全考虑** — 敏感信息保护、多项目隔离、记忆导出与备份。

6. **实战选型指南** — 五款插件速览、全维度对比表、Mermaid 决策树、首选推荐配置（本地优先 + 云同步）、MCP 记忆服务器选型（@modelcontextprotocol/server-memory、Kronvex、Memstate）、常见误区。

## 关联章节

- ← [提示词缓存机制](context/prompt-caching.md)（缓存是记忆的基础设施）
- ← [上下文工程核心](../02-core-concepts/context-engineering-core.md)（上下文工程基础）
- → [可观测性](observability.md)（可观测性监控记忆效果）

> **设计说明**：OpenCode 原生不包含语义记忆系统——它的上下文加载机制是文档驱动的（通过 `AGENTS.md`/`CLAUDE.md` 读取项目指令，而非持久化记忆数据库）。本文介绍的插件通过 OpenCode 的 **Plugin（插件）** API 实现记忆能力。其中 Memdir 架构最初来自 Claude Code（《驾驭工程：从 Claude Code 源码到 AI 编码最佳实践》第 24 章），`opencode-claude-memory` 插件将这一架构移植到了 OpenCode 生态。

## 记忆 vs 缓存

### 本质差异

缓存是被动的——"系统帮你存了什么"；记忆是主动的——"Agent 自己记住了什么"。

| 维度       | 缓存                             | 记忆                             |
| ---------- | -------------------------------- | -------------------------------- |
| 存储什么   | 系统预设（指令、工具、项目知识） | Agent 经历（决策、发现、上下文） |
| 谁管理     | 系统自动管理                     | Agent 自主管理                   |
| 写入时机   | 首次访问时被动写入               | 任务关键节点主动记录             |
| 读取方式   | key-value 精确匹配               | 语义检索 + 相关性排序            |
| 生命周期   | 固定 TTL                         | 动态——由重要度评分决定           |
| 跨 Session | 可配置                           | 核心能力                         |

**一句话直觉**：缓存就像 IDE 的自动补全缓存——你打开文件时它自动加载了最近的内容；记忆就像你的笔记本——你在解决 bug 时主动记下了"上一步试过什么方案，为什么不行"。

### 记忆的三个层次

| 层次     | 范围         | 存储方式            | 典型容量 | 失效机制     |
| -------- | ------------ | ------------------- | -------- | ------------ |
| 短期记忆 | 当前 Session | 上下文窗口          | ~100 条  | Session 结束 |
| 中期记忆 | 相关 Session | 插件长期存储        | ~1000 条 | 重要度淘汰   |
| 长期记忆 | 跨项目       | 插件长期存储 + 归档 | ~5000 条 | 手动归档     |

## OpenCode 记忆插件选型

> OpenCode 原生没有内置语义记忆——它的插件系统开放了 `session.created`、`session.idle`、`session.deleted` 等生命周期钩子和 `experimental.session.compacting` 接口，第三方插件通过这些入口实现持久化记忆。目前社区有以下 4 款主流方案：

### 插件生态概览

```mermaid
graph TB
    subgraph User["你的选择取决于"]
        A1[需要 Claude Code 兼容?] -->|是| B1[opencode-claude-memory]
        A1 -->|否| A2[需要最高召回率?]
        A2 -->|是| B2[agentmemory]
        A2 -->|否| A3[需要认知心理学管理?]
        A3 -->|是| B3[true-mem]
        A3 -->|否| B4[opencode-mem ★ 首选]
    end

    subgraph Features["功能矩阵"]
        C1[向量检索]
        C2[Web UI]
        C3[自动捕获]
        C4[跨 Session]
        C5[多项目隔离]
    end

    B4 --- C1
    B4 --- C2
    B4 --- C3
    B4 --- C4
    B4 --- C5

    style User fill:#4A90D9,color:#fff
    style Features fill:#50C878,color:#fff
    style B4 fill:#FF9F43,color:#fff
```

### ① opencode-mem（首选推荐）

**npm**: `opencode-mem` · **GitHub**: [tickernelz/opencode-mem](https://github.com/tickernelz/opencode-mem) · **★ 900+** · **周下载**: 2,787

当前最成熟的 OpenCode 原生记忆插件，v2.17.1，60+ 版本，30+ 贡献者。

**核心能力**：

- **SQLite + USearch 向量索引**——以 SQLite 为数据源，USearch 做高效向量搜索，失败时自动回退到 ExactScan 精确扫描
- **12+ 本地嵌入模型**——支持 Xenova/nomic-embed-text-v1 等，无需外部 API
- **Web UI**——本地 4747 端口提供可视化记忆管理界面
- **自动捕获**——自动提取关键信息写入记忆，支持 toast 通知
- **用户画像学习**——自动分析用户偏好和编码习惯
- **多作用域**——`project`（项目级）和 `all-projects`（全局）两种搜索范围
- **智能去重**——避免重复存储相似记忆

**安装配置**：

```jsonc:opencode.jsonc
// ~/.config/opencode/opencode.json 或项目 .opencode/opencode.json
{
  "plugin": ["opencode-mem"]
}
```

OpenCode 下次启动时自动从 npm 下载。

**详细配置**（`~/.config/opencode/opencode-mem.jsonc`）：

```jsonc:opencode-mem.jsonc
{
  "storagePath": "~/.opencode-mem/data",
  "embeddingModel": "Xenova/nomic-embed-text-v1",
  "memory": {
    "defaultScope": "project"
  },
  "webServerEnabled": true,
  "webServerPort": 4747,
  "autoCaptureEnabled": true,
  "autoCaptureLanguage": "auto",
  "opencodeProvider": "anthropic",
  "opencodeModel": "claude-haiku-4-5-20251001",
  "compaction": {
    "enabled": true,
    "memoryLimit": 10
  },
  "chatMessage": {
    "enabled": true,
    "maxMemories": 3,
    "excludeCurrentSession": true,
    "injectOn": "first"
  }
}
```

**Agent 可调用的记忆操作**：

```typescript:agent-memory-ops.ts
// 添加记忆
memory({ mode: "add", content: "项目采用微服务架构，服务间通过 gRPC 通信" });
// 搜索记忆
memory({ mode: "search", query: "架构决策" });
// 跨项目搜索
memory({ mode: "search", query: "数据库设计方案", scope: "all-projects" });
// 查看用户画像
memory({ mode: "profile" });
// 列出最近记忆
memory({ mode: "list", limit: 10 });
```

**适用场景**：大部分开发者，需要即装即用的全功能记忆系统，偏好向量检索和可视化管理。

---

### ② opencode-claude-memory（Claude Code 兼容）

**npm**: `opencode-claude-memory` · **GitHub**: [kuitos/opencode-claude-memory](https://github.com/kuitos/opencode-claude-memory) · **★ ~15** · **周下载**: 127

如果你同时在用 Claude Code 和 OpenCode，这个插件让两者共享同一套记忆。

**核心能力**：

- **Claude Code 兼容**——直接读写 Claude Code 的 Markdown 记忆文件路径和格式，零迁移成本
- **Auto-Dream 门控**——自动在后台运行记忆整合，默认 24 小时 + 5 个 Session 触发一次
- **5 个记忆工具**——`memory_save`、`memory_delete`、`memory_list`、`memory_search`、`memory_read`
- **Shell Hook 拦截**——安装后 `opencode` 命令自动经过 `opencode-memory` 包装，执行前后自动捕获记忆

**安装配置**：

```bash:terminal
npm install -g opencode-claude-memory
opencode-memory install   # 一次性安装 shell hook
```

**插件配置**：

```jsonc:opencode.jsonc
// ~/.config/opencode/opencode.json
{
  "plugin": ["opencode-claude-memory"]
}
```

**工作流程**：

```text:terminal
opencode 命令 →
  opencode-memory 拦截 →
  启动 OpenCode →
  Agent 执行期间通过 5 个 memory_* 工具读写记忆 →
  退出时 opencode-memory 检查是否有新记忆文件 →
  满足门控条件（>24h + >=5 session）→ 触发 Auto-Dream 后台合并
```

**适用场景**：Claude Code 和 OpenCode 双修用户，希望两套工具共享同一份项目记忆。

---

### ③ agentmemory（企业级高召回）

**npm**: `@agentmemory/agentmemory` · **GitHub**: [rohitg00/agentmemory](https://github.com/rohitg00/agentmemory) · **★ 16,000+** · **周下载**: 17,700

基于 iii 引擎的企业级记忆系统，定位不仅是 OpenCode 插件，而是跨所有 AI 编码工具的通用记忆层。

**核心能力**：

- **混合检索**——BM25 + 向量 + 知识图谱三重检索，95.2% 召回率（LongMemEval-S 基准）
- **53 个 MCP 工具**——最丰富的工具集合，覆盖记忆 CRUD、查询、分析
- **22 个自动捕获钩子**——覆盖 Session 生命周期、消息、工具调用、错误等全部事件
- **跨 Agent 共享**——所有接入同一 server 的 Agent 共享记忆（Claude Code、Cursor、Gemini CLI 等均可）
- **8 个原生 Skill**——Agent 通过 **Skill（技能）** 学会何时使用记忆工具
- **两个斜杠命令**——`/recall` 搜索记忆，`/remember` 保存洞察

**安装配置**（OpenCode MCP 模式）：

```jsonc:opencode.jsonc
// ~/.config/opencode/opencode.json
{
  "mcp": {
    "agentmemory": {
      "type": "local",
      "command": ["npx", "-y", "@agentmemory/mcp"],
      "enabled": true
    }
  },
  "plugin": ["./plugins/agentmemory-capture.ts"]
}
```

需要先复制插件文件和启动 server：

```bash:terminal
npx @agentmemory/agentmemory          # 启动 server，默认 :3111
mkdir -p ~/.config/opencode/plugins
cp plugin/opencode/agentmemory-capture.ts ~/.config/opencode/plugins/
```

**与 opencode-mem 的关键区别**：agentmemory 需要运行独立的 server 进程，而 opencode-mem 是纯插件内嵌运行。前者更重但记忆可跨工具共享，后者更轻但仅限 OpenCode。

**适用场景**：企业团队，需要最高召回率，使用多种 AI 编码工具且希望共享记忆。

---

### ④ true-mem（认知心理学路线）

**npm**: `true-mem` · **GitHub**: [rizal72/true-mem](https://github.com/rizal72/true-mem) · **★ 171** · **周下载**: 315

不追求最大召回率，而是模仿人脑的记忆管理方式——不是所有信息都值得以同样方式记住。

**核心能力**：

- **艾宾浩斯遗忘曲线**——情景记忆按 7 天半衰期衰减，偏好和决策永久保留
- **7 特征评分模型**——Recency、Frequency、Importance、Utility、Novelty、Confidence、Interference
- **STM/LTM 双存储架构**——高强度记忆自动提升到长时存储，弱记忆在短时存储中衰减
- **7 种记忆分类**——constraint、preference、learning、procedural、decision、semantic、episodic，每种有独立的衰减策略和作用域
- **四层防御系统**——问题检测、负面模式过滤、多关键词句子级评分、置信度阈值，防止误存储
- **双重相似度模式**——Jaccard 默认（快速词匹配）或可选的 ML 嵌入（语义理解）
- **非阻塞架构**——异步提取，不阻塞 UI

**配置**：

```jsonc:opencode.jsonc
// ~/.config/opencode/opencode.jsonc
{
  "plugin": ["true-mem"]
}
```

通过环境变量控制行为：

```bash:terminal
TRUE_MEM_INJECTION_MODE=0     # 0=SESSION_START（默认，最省 Token），1=ALWAYS
TRUE_MEM_SUBAGENT_MODE=1      # 0=禁用，1=启用
TRUE_MEM_MAX_MEMORIES=20      # 每次注入的最大记忆数
TRUE_MEM_EMBEDDINGS=0         # 0=仅 Jaccard，1=混合语义搜索
```

**适用场景**：关注 Token 经济性，希望记忆管理更贴近人类认知规律的进阶用户。

### 快速对比

| 维度              | opencode-mem               | opencode-claude-memory | agentmemory                            | true-mem                  |
| ----------------- | -------------------------- | ---------------------- | -------------------------------------- | ------------------------- |
| **安装复杂度**    | 低（纯插件，一行配置）     | 中（需装 CLI + Hook）  | 高（需运行独立 server）                | 低（纯插件，一行配置）   |
| **存储引擎**      | SQLite + USearch 向量索引  | 文件系统（Markdown）   | 混合（BM25 + 向量 + 知识图谱）         | SQLite + Jaccard/嵌入     |
| **向量检索**      | ✅ 原生支持                | ❌ 文件级搜索          | ✅ 原生支持                            | 可选（实验性）            |
| **Web UI**        | ✅ 4747 端口               | ❌                     | ✅ viewer                              | ❌                        |
| **跨工具共享**    | ❌ 仅 OpenCode             | ✅ 与 Claude Code      | ✅ 所有 MCP 客户端                     | ❌ 仅 OpenCode            |
| **自动捕获**      | ✅                         | ✅（通过 shell hook）  | ✅（22 钩子）                          | ✅（非阻塞异步）          |
| **遗忘机制**      | 基于容量淘汰               | Auto-Dream 门控        | 基于置信度 + 生命周期                  | 艾宾浩斯曲线 + 7 分类    |
| **GitHub Stars**  | 810+                       | ~15                    | 16,000+                                | 171                       |
| **每周下载**      | 2,100                      | 127                    | 17,700                                 | 315                       |

## Auto-Dream 机制

> Auto-Dream 是 Agent 的"睡眠记忆巩固"——每次 Session 结束时自动回顾全天经历，抽取最重要的印象存盘。这是记忆插件的核心能力，不同插件以不同方式实现。

### 为什么需要 Auto-Dream

Session 中的原始记忆太多太杂。如果每次打开新 Session 都把前一天的所有记忆塞进去，上下文瞬间爆炸。Auto-Dream 解决的问题：**让 Agent 自己决定什么值得记住**。

**一句话直觉**：Auto-Dream 就像你每天睡前回想今天发生了什么——你不会记得每顿午饭吃了什么，但你会记住"今天在代码评审时发现了一个关键 bug"。

### 通用 Auto-Dream 流程图

```mermaid
sequenceDiagram
    participant Agent as Agent
    participant Plugin as 记忆插件
    participant Store as 持久化存储
    participant Context as 上下文

    Note over Agent,Context: Session 执行阶段

    Agent->>Plugin: 写入原始记忆（自动捕获或主动调用）
    Plugin->>Store: 持久化存储

    Note over Agent,Context: Session 结束触发 Dream

    Store->>Plugin: 触发 Auto-Dream
    Plugin->>Plugin: 扫描当前 Session 记忆
    Plugin->>Plugin: 计算重要度评分
    Plugin->>Plugin: 生成摘要（3-5 句话）
    Plugin->>Store: 写入摘要 / 更新索引

    Note over Agent,Context: 低价值记忆淘汰

    Store->>Plugin: 标记低价值记忆
    Plugin->>Store: 归档或删除
    Plugin->>Store: 同步索引

    Note over Agent,Context: 新 Session 启动 → 检索

    Agent->>Plugin: 查询高相关度记忆
    Plugin->>Plugin: 向量 / 关键词检索
    Plugin->>Agent: 返回 Top-K 记忆
    Context->>Context: 注入到系统提示
```

### 各插件的实现差异

| 环节            | opencode-mem                     | opencode-claude-memory | agentmemory                    | true-mem                        |
| --------------- | -------------------------------- | ---------------------- | ------------------------------ | ------------------------------- |
| 触发时机        | 自动捕获 + 主动调用              | 退出后 shell hook 检测 | 22 个生命周期钩子自动触发      | 非阻塞异步提取                  |
| 重要度评分      | 基于向量相似度 + 用户反馈        | Claude 原生重要度模型  | 置信度 + 生命周期              | 7 特征评分（R/F/I/U/N/C/If）   |
| 淘汰策略        | 容量上限（maxMemories=10）       | Auto-Dream 门控合并    | 置信度阈值淘汰                 | 艾宾浩斯衰减 + 分类策略        |
| 跨 Session 融合 | 自动画像学习 + 统一时间线        | 跨 Session 洞察合并    | 知识图谱关联                    | STM→LTM 自动提升               |

### 重要度评分模型（通用参考）

记忆插件通常用以下维度计算重要度：

| 维度     | 权重 | 判断依据                              | 例子                                    |
| -------- | ---- | ------------------------------------- | --------------------------------------- |
| 任务类型 | 0.35 | 架构决策 > 调试分析 > 代码生成 > 闲聊 | 数据库设计决策=0.9，格式化代码=0.2      |
| 决策影响 | 0.30 | 修改文件数 / 影响模块范围             | 重构核心模块=0.8，改一个变量名=0.1      |
| 用户反馈 | 0.20 | 用户的显式确认、修改次数              | "就这样"=0.7，"不对重来"=0.1            |
| 新颖性   | 0.15 | 与已有记忆的差异化程度                | 全新方案=0.9，重复讨论=0.3              |

### 跨 Session 记忆融合

多个 Session 反复出现同一主题时，插件可自动生成跨 Session 洞察：

```text:terminal
Session A: "用户表查询性能优化" → 创建复合索引
Session B: "订单查询也需要优化" → 也是复合索引方案
合并: → "项目中复合索引策略适用于所有高频查询场景"
```

## Compaction 与记忆的配合

> Compaction 是"现在就要做"的上下文精简，记忆是"以后可能有用"的长期存盘。

### 两者的分工

| 场景                    | 谁负责     | 做什么                    |
| ----------------------- | ---------- | ------------------------- |
| Session 中上下文太满    | Compaction | 压缩对话历史，保留关键信息 |
| Session 结束需要记东西  | 记忆插件   | 写入持久化存储            |
| 新 Session 需要历史信息 | 记忆插件   | 检索并注入上下文          |
| 加载后上下文又太满      | Compaction | 压缩加载进来的历史摘要    |

**协同流程**：

```text:terminal
Agent 执行 → Token 接近窗口上限
  → Compaction 触发：压缩低优先级对话，保留高优先级决策
  → Session 结束 → 记忆插件生成摘要 → 写入持久化存储
  → 新 Session 启动 → 插件检索并注入记忆到上下文
  → 如果还是多了 → Compaction 再次压缩
```

### Compaction 以记忆为输入

记忆插件为 Compaction 提供优先级参考——插件的重要度评分直接告诉 Compaction"什么信息不能丢"：

```jsonc:opencode-mem.jsonc
// opencode-mem 配置中的 compaction 设置
{
  "compaction": {
    "enabled": true,
    "memoryLimit": 10
  }
}
```

### 实测效果

| 配置            | Session Token 节省         | 关键信息保留率 |
| --------------- | -------------------------- | -------------- |
| Compaction 单独 | 20-30%                     | 85%            |
| 记忆插件单独    | 10-15%（通过减少重复分析） | 90%            |
| 两者配合        | 35-45%                     | 95%            |

两者配合的收益大于单独使用之和——属于"1+1 > 2"的协同效应。

## 安全考虑

### 敏感信息保护

Memory 是 Agent 的"私人笔记"——但不该记的东西不能记：

| 禁止的内容             | 原因       | 怎么处理          |
| ---------------------- | ---------- | ----------------- |
| API Key、密码、Token   | 泄露即灾难 | 自动检测，拦截写入 |
| 用户隐私数据（PII）    | 合规风险   | 自动标记并报警    |
| 商业机密（非项目相关） | 权限越界   | 多项目隔离        |

以 `opencode-mem` 为例，它的数据存储在独立的 `~/.opencode-mem/data` 目录，默认不与其他工具共享。`true-mem` 在此基础上增加了四层防御系统防止误存敏感数据。

### 多项目隔离

每个项目的记忆必须严格隔离——项目 A 的 Agent 不应该知道项目 B 的数据库密码。

隔离机制：

- **物理隔离**：记忆插件的数据库或文件目录在各自项目配置路径下
- **作用域隔离**：`opencode-mem` 通过 `scope: "project"` 限制搜索范围
- **配置隔离**：每个项目可配置独立的记忆参数

```jsonc:opencode-mem.jsonc
// opencode-mem 配置中的作用域控制
{
  "memory": {
    "defaultScope": "project"   // 默认只搜索当前项目
  }
}
```

### 记忆导出与备份

以 `opencode-mem` 为例，记忆数据存储在 `~/.opencode-mem/data/`（SQLite 数据库文件）。建议：

- 将插件数据目录纳入 `.gitignore`
- 定期备份 `~/.opencode-mem/` 目录
- 记忆是"个人笔记"，提交到 Git 里通常是坏主意

## 实战选型指南

> 概念和原理已经讲清楚了。下面直接给出 5 款插件的深度对比和选型决策树——面对真实场景，你的项目到底该选哪个。

### 五款插件速览

以下 5 款插件覆盖了当前 OpenCode 社区的全部主流记忆方案。它们不是非此即彼的关系——你可以根据场景组合使用，但更常见的做法是选一个主力方案用到底。

| 插件 | 一句话定位 | 最佳场景 |
|------|-----------|---------|
| **opencode-mem** | 本地优先的全功能记忆插件，SQLite+向量索引 | 隐私敏感的单人开发者，需要即装即用 |
| **opencode-supermemory** | 云同步记忆，Supermemory API 后端 | 多设备跨项目协作，需要全部记忆互通 |
| **@loreai/opencode** | 蒸馏式三层记忆架构，模拟人类遗忘 | 研究型用户，追求记忆精度而非数量 |
| **opencode-claude-memory** | 与 Claude Code 共享同一份 Markdown 记忆文件 | OpenCode + Claude Code 双修用户 |
| **true-mem** | 认知心理学路线，艾宾浩斯遗忘曲线 | Token 经济敏感用户，希望按规律管理记忆 |

#### ⑤ opencode-supermemory（云同步）

**npm**: `opencode-supermemory` · **GitHub**: [supermemoryai/opencode-supermemory](https://github.com/supermemoryai/opencode-supermemory) · **★ ~950** · **周下载**: —（通过 Bun 安装）

opencode-mem 的灵感来源。如果说 opencode-mem 是本地派代表，opencode-supermemory 就是云派代表。它使用 Supermemory API 作为存储后端，所有记忆在云端持久化，跨机器、跨项目互通。

安装方式不同——不是简单加一行配置，而是通过 `bunx opencode-supermemory@latest install` 执行安装脚本，自动注册插件并创建 `/supermemory-init` 命令。需要 Supermemory API Key（支持自托管或 Pro 套餐）。

**关键能力**：Session 启动时自动注入上下文（用户画像 + 项目知识 + 语义相关记忆），关键词触发自动保存（"记住这个"、"保存一下"），上下文使用率达到 80% 时自动压缩并保存为记忆，支持 `<private>` 标签保护隐私。

**一句话点评**：多设备切换频繁、需要全部记忆随处可查的开发团队的首选。代价是需要网络连接和付费计划。

---

#### ⑥ @loreai/opencode（蒸馏架构）

**npm**: `@loreai/opencode`（别名 `opencode-lore`） · **GitHub**: [BYK/loreai](https://github.com/BYK/loreai) · **★ ~44** · **周下载**: ~1,200 · **v0.26.0**

这是 5 款中设计理念最独特的一个。它不追求"记住更多"，而追求"记住更精"。基于 Sanity 的 Nuum 记忆架构和 Mastra 的 Observational Memory 系统，实现了三层存储架构：

| 层级 | 存储内容 | 特征 |
|------|---------|------|
| L0 | 原始对话+工具调用 | 短期，自动滚动淘汰 |
| L1 | 操作知识（文件路径、错误信息、具体决策） | 蒸馏压缩，保留操作精度 |
| L2 | 长期模式（项目惯例、架构选择、团队偏好） | 跨 Session 自动提炼 |

它叫"蒸馏"不叫"摘要"的原因：摘要会丢失细节（"优化了数据库查询"），蒸馏保留操作精度（"在 `findUsers` 方法中增加了 `LIMIT 100`，避免全表扫描"）。这对 Agent 的连续工作至关重要。

**一句话点评**：如果你重视记忆质量而非数量，愿意为更精准的回忆做少量配置，@loreai/opencode 值得尝试。当前处于快速迭代期（0.x），API 可能变化。

### 全维度对比

| 维度 | opencode-mem | opencode-supermemory | @loreai/opencode | opencode-claude-memory | true-mem |
|------|-------------|---------------------|-----------------|----------------------|---------|
| **安装复杂度** | 低（一行配置，自动下载） | 中（需 Bun 安装脚本 + API Key） | 低（一行配置） | 中（npm install + Shell Hook） | 低（一行配置） |
| **存储引擎** | SQLite + USearch 向量 | Supermemory 云端 API | SQLite + FTS5 + 本地嵌入 | 文件系统（Markdown） | SQLite + Jaccard（可选嵌入） |
| **向量检索** | 原生支持 | 云端语义搜索 | 本地嵌入 / Voyage/OpenAI | 文件级关键词搜索 | 可选（实验性嵌入） |
| **Web UI** | 4747 端口 | 无 | 无 | 无 | 无 |
| **跨工具共享** | 仅 OpenCode | 同账号多设备 | 仅 OpenCode | 与 Claude Code | 仅 OpenCode |
| **自动捕获** | 原生支持 | 关键词 + 压缩触发 | 生命周期钩子 | Shell Hook | 非阻塞异步提取 |
| **遗忘机制** | 容量淘汰 | 压缩覆盖 | 三层蒸馏淘汰 | Auto-Dream 门控 | 艾宾浩斯衰减 + 7 分类 |
| **GitHub Stars** | 900 | ~950 | ~44 | 24 | ~143 |
| **每周下载** | 2,787 | — | ~1,200 | — | 315 |

### 决策树

下面的决策树帮你从场景出发，逐级缩小选择范围：

```mermaid
graph TB
    Start((你的场景是什么？)) --> Q1{需要云同步?}

    Q1 -->|是| Q2{多设备跨项目?}
    Q2 -->|是| R1[opencode-supermemory]
    Q2 -->|否| Q3

    Q1 -->|否，本地优先| Q3{使用多种 AI 编码工具?}

    Q3 -->|是| Q4{包括 Claude Code?}
    Q4 -->|是| R2[opencode-claude-memory]
    Q4 -->|否| R3[opencode-mem]

    Q3 -->|否，仅 OpenCode| Q5{记忆管理哲学?}

    Q5 -->|追求记忆质量| R4["@loreai/opencode"]
    Q5 -->|追求 Token 经济性| R5[true-mem]
    Q5 -->|功能均衡| R3

    style Start fill:#4A90D9,color:#fff
    style R1 fill:#A66CFF,color:#fff
    style R2 fill:#A66CFF,color:#fff
    style R3 fill:#FF9F43,color:#fff
    style R4 fill:#A66CFF,color:#fff
    style R5 fill:#A66CFF,color:#fff
```

### 首选推荐配置

#### 本地优先：opencode-mem

这是 80% 用户的最优起点。一行配置启用，Web UI 降低认知门槛，SQLite 本地存储保证隐私。

**基础配置**（`~/.config/opencode/opencode.jsonc`）：

```jsonc:~/.config/opencode/opencode.jsonc
{
  "plugin": ["opencode-mem"]
}
```

**完整配置**（`~/.config/opencode/opencode-mem.jsonc`）：

```jsonc:~/.config/opencode/opencode-mem.jsonc
{
  "storagePath": "~/.opencode-mem/data",
  "embeddingModel": "Xenova/nomic-embed-text-v1",
  "memory": {
    "defaultScope": "project"
  },
  "webServerEnabled": true,
  "webServerPort": 4747,
  "autoCaptureEnabled": true,
  "autoCaptureLanguage": "auto",
  "opencodeProvider": "anthropic",
  "opencodeModel": "claude-haiku-4-5-20251001",
  "compaction": {
    "enabled": true,
    "memoryLimit": 10
  },
  "chatMessage": {
    "enabled": true,
    "maxMemories": 3,
    "excludeCurrentSession": true,
    "injectOn": "first"
  }
}
```

**验证安装**：重启 OpenCode，查看日志中是否有 `opencode-mem` 初始化成功的消息。访问 `http://localhost:4747` 确认 Web UI 正常。

#### 云同步：opencode-supermemory

适合多设备、跨项目、或需要团队共享记忆的场景。

**安装**：

```bash:terminal
bunx opencode-supermemory@latest install
```

**配置 API Key**（`~/.config/opencode/supermemory.jsonc`）：

```jsonc:~/.config/opencode/supermemory.jsonc
{
  "apiKey": "sm_...",
  "maxMemories": 5,
  "compactionThreshold": 0.8,
  "containerTagPrefix": "my-team"
}
```

**验证**：重启 OpenCode，运行 `opencode -c` 确认 `supermemory` 出现在工具列表中。

> **注意**：opencode-supermemory 需要 Supermemory Pro 套餐或自托管后端。自托管方式：运行 `npx supermemory local`，然后设置 `export SUPERMEMORY_API_URL=http://localhost:6767`。

### MCP 记忆服务器选型

除了插件方案，还可以通过 MCP 协议给 OpenCode 添加记忆能力。MCP 方案的好处是记忆服务器独立运行，可以被多个 MCP 客户端共享（Claude Desktop、Cursor、Windsurf 等）。

以下三款 MCP 记忆服务器值得关注：

#### @modelcontextprotocol/server-memory

**npm**: `@modelcontextprotocol/server-memory` · **周下载**: 226K · **官方参考实现**

这是 MCP 官方的记忆服务器参考实现，使用知识图谱（Knowledge Graph）存储实体、关系和观察。数据存储在本机 JSONL 文件中，支持实体创建、关系建立、观察添加和搜索。

**适用场景**：需要标准 MCP 兼容的记忆方案，愿意自定义 prompt 来引导 Agent 如何使用记忆工具。适合对记忆格式有定制需求的团队。

**OpenCode 配置**：

```jsonc:~/.config/opencode/opencode.jsonc
{
  "mcp": {
    "memory": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-memory"],
      "enabled": true
    }
  }
}
```

#### Kronvex

**官网**: [kronvex.io](https://kronvex.io) · **MCP 记忆 API**

Kronvex 提供了一个托管的记忆 API，通过 MCP 协议为 AI Agent 提供持久化记忆。它的核心卖点是零配置——注册账号、获取 API Key、配置 MCP，三步完成。

**适用场景**：不想维护自建基础设施，愿意使用托管服务换取零运维的记忆方案。

**OpenCode 配置**：

```jsonc:~/.config/opencode/opencode.jsonc
{
  "mcp": {
    "kronvex": {
      "type": "local",
      "command": ["npx", "-y", "@kronvex/mcp"],
      "enabled": true,
      "environment": {
        "KRONVEX_API_KEY": "kv_..."
      }
    }
  }
}
```

#### Memstate

**官网**: [memstate.ai](https://memstate.ai) · **结构化树状记忆**

Memstate 的特色是结构化记忆——不是简单的键值对或知识图谱，而是树状层次结构的记忆树。每条记忆可以挂载到项目、子项目、具体模块的层级下，检索时按子树精度返回。

**适用场景**：项目结构复杂，需要按模块粒度管理记忆的团队。树状结构更贴近实际工程组织方式。

**OpenCode 配置**：

```jsonc:~/.config/opencode/opencode.jsonc
{
  "mcp": {
    "memstate": {
      "type": "local",
      "command": ["npx", "-y", "@memstate/mcp"],
      "enabled": true,
      "environment": {
        "MEMSTATE_API_KEY": "ms_..."
      }
    }
  }
}
```

#### 插件 vs MCP 服务器：如何选

| 维度 | 插件方案 | MCP 服务器方案 |
|------|---------|--------------|
| 安装复杂度 | 低（一行配置或 Bun 安装） | 中（需配置 MCP 端点） |
| 独立运行 | 嵌入在 OpenCode 进程中 | 独立进程，可被多客户端共享 |
| 跨工具共享 | 仅 OpenCode 生态内 | 所有 MCP 客户端 |
| 运维负担 | 零运维 | 需要管理进程生命周期 |
| 性能 | 无进程间通信开销 | 有 stdio/HTTP 通信开销 |

**建议**：单人单工具场景选插件方案，多工具多用户场景选 MCP 服务器方案。

### 常见误区

**"插件装得越多记忆越好"** —— 多个记忆插件同时运行会导致重复存储和上下文膨胀。选一个主力插件，禁用其他。

**"MCP 服务器比插件更强大"** —— 不一定。插件方案的集成深度（Hook 点、生命周期绑定、自动捕获）通常优于 MCP 方案。MCP 的优势在跨工具共享，不在单工具能力。

**"记忆插件的 Web UI 是锦上添花"** —— 对新手来说，可视化浏览记忆是理解"Agent 记住了什么"的最快方式。opencode-mem 的 Web UI 是它的核心竞争力之一。

**"向量检索一定比关键词搜索好"** —— 对于代码上下文（变量名、函数名、路径），关键词搜索的精度往往高于向量检索。这是 opencode-claude-memory 用 Markdown 文件级搜索依然可用的原因。

## 验证标准

完成本章学习后，请确认你能够：

- [ ] 区分记忆系统与缓存系统的本质差异
- [ ] 列出 5 款 OpenCode 记忆插件及其核心定位
- [ ] 配置 opencode-mem 插件并描述其核心能力
- [ ] 说明 opencode-claude-memory 与 Claude Code 的兼容方式
- [ ] 说明 opencode-supermemory 的云同步能力和安装方式
- [ ] 解释 @loreai/opencode 的蒸馏架构（L0/L1/L2 三层存储）
- [ ] 解释 true-mem 的 7 种记忆分类和衰减策略
- [ ] 说明 Compaction 如何与记忆系统协同工作
- [ ] 使用决策树根据自身场景做出合理的记忆插件选型
- [ ] 对比插件方案和 MCP 服务器方案的适用场景
- [ ] 识别记忆插件选型的常见误区
