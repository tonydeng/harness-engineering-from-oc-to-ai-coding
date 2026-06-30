# 性能调优与成本管理

> **OMO 扩展说明**：本文中的 `tokenBudget`、`compaction`、`hashline` 配置字段、54+ Event Hooks 体系及类别自动降级 (Category-based Auto-downgrade) 模型配置是 **oh-my-openagent (OMO)** 对 OpenCode 的扩展增强。原生 OpenCode 不含这些字段。`.opencodeignore` 排除策略、`ripgrep` 本地搜索、Context7 **MCP（模型上下文协议）** 优化及 Session 日志分析命令是通用实践，可独立于 OMO 使用。OpenCode 版本 v1.17.x，OMO 版本 v4.13.x。
>
> 响应慢？Token 消耗大？错误率高？从性能瓶颈识别到成本管控策略，系统性优化 AI 编程工作流。
> **适合读者**: 效率开发者 · 工程经理

> **前置条件**
> - 已完成 [可观测性](../observability.md)
> - 已完成 [上下文压缩与Token 预算](../context-compression.md)
> - 已完成 [上下文压缩与Token 预算](../context-compression.md)

## 文章概述

本文从性能瓶颈识别入手，介绍 54+ Event Hooks 可观测性体系如何定位三类性能问题。然后深入成本管控策略：Token 预算、模型降级链、上下文压缩和工具输出保护窗口。接着讲解 Hashline 编辑机制，最后讨论上下文优化技巧。目标是让读者形成"测量-分析-优化-再测量"的持续调优闭环。读完本文，你将能够识别 AI 编程工作流中的性能瓶颈，制定成本管控策略并建立持续调优机制。

> **⏱ 时间有限？先读这些：** 瓶颈识别 → 成本管控 → Hashline 机制 → 上下文优化

## 一、性能瓶颈识别

### 1.1 三类性能问题

| 问题类型 | 症状 | 典型根因 | 排查入口 |
|---------|------|---------|---------|
| 响应慢 | 单轮对话超 30 秒 | 上下文过大、模型过重、工具阻塞 | Session 耗时追踪 |
| Token 消耗大 | 月账单暴涨 | 模型选型过重、无效工具调用 | Token 用量审计 |
| 错误率高 | 频繁报错重试 | 工具调用失败、上下文丢失 | 错误事件日志 |

**响应慢**：200K 上下文窗口的请求，模型自注意力计算 O(n²)。窗口从 50K 膨胀到 200K，推理耗时增约 16 倍（引用自 GPT-4 技术报告）。

**Token 消耗大**：**Agent（智能体）** 可能在不知情下调用大量工具——一次 `glob` 返回 500 个文件、一次 `grep` 结果 50K Token。每个工具调用都产生输入输出 Token。

**错误率高**：错误率与成本正反馈循环——错误越多，重试越多，Token 消耗越大。错误率从 5% 降到 1%，成本可降 15-20%（实测）。

### 1.2 54+ Event Hooks 定位瓶颈

每个 Hook 点在 Agent 执行路径上埋点，生成结构化事件：

```text:terminal
Agent 启动 → Session 开始 → 工具调用 → 模型请求 → 响应生成
   ↓           ↓              ↓            ↓            ↓
 onStart    onSession     onToolCall   onModelReq  onResponse
```

通过事件分析回答三个问题：
1. **哪个步骤最慢** — `onModelReq` 通常占 60-80%，若 `onToolCall` 占比异常，说明工具链有问题
2. **哪个步骤最贵** — `read_file` 通常是输入 Token 的"隐形杀手"
3. **哪个步骤易失败** — 某些工具（如 `delete_file`）在高权限模式下失败率更高

### 1.3 Session 日志分析

```bash:terminal
# 导出最近 Session 的耗时 Top 5 事件
opencode logs --session latest --sort duration --top 5
# 按 Token 消耗排序
opencode logs --session latest --sort tokens --top 5
# 过滤错误事件
opencode logs --session latest --level error
```

## 二、成本管控策略

### 2.1 三层优化模型

下图展示了成本管控的三层优化模型，从 Prompt 优化到缓存策略再到模型选择。

```mermaid
flowchart TB
    subgraph T["Type-level（任务类型层）"]
        A1[任务分类] --> A2[模型自动降级]
        A2 --> A3["文档 → Flash"]
        A2 --> A4["审查 → Sonnet"]
        A2 --> A5["重构 → Opus"]
    end
    subgraph S["Session-level（会话层）"]
        B1[Token 预算] --> B2[总量上限]
        B1 --> B3[预留比例 20-30%]
    end
    subgraph M["Message-level（消息层）"]
        C1[Compaction] --> C2[触发阈值 80%]
        C1 --> C3[保护窗口 40K]
    end
    T --> S --> M
    style A1 fill:#4A90D9,color:#fff
    style B1 fill:#50C878,color:#fff
    style C1 fill:#FF9F43,color:#fff
```

**Type-level（任务类型层）** — 节约贡献 50-70%：按任务类型选模型，单价差可达 100 倍（Flash $0.15 vs Opus $5/$25/M Token）。Opus 4.8 fast 模式约 2 倍标准价格，但速度快 2.5 倍。

**Session-level（会话层）** — 节约贡献 15-25%：每个会话设定预算上限，超限触发三级降级。

**Message-level（消息层）** — 节约贡献 10-20%：Compaction 保护最近 40K Token 工具输出。

### 2.2 类别自动降级 (Category-based Auto-downgrade)

核心思路：不是所有任务都需要最强模型。

```json:opencode.json
{
  "model": {
    "defaultModel": "claude-sonnet-4",
    "downgradeChain": [
      {
        "category": ["documentation", "readme"],
        "model": "gemini-2.0-flash",
        "provider": "google",
        "maxTokens": 32000,
        "reason": "文档不需要深度推理"
      },
      {
        "category": ["refactor", "bugfix"],
        "model": "claude-sonnet-4",
        "provider": "anthropic",
        "maxTokens": 64000,
        "reason": "中等复杂度，性价比最优"
      },
      {
        "category": ["architecture", "core_design"],
        "model": "claude-opus-4",
        "provider": "anthropic",
        "maxTokens": 128000,
        "reason": "核心架构需要最强推理"
      }
    ],
    "fallback": { "model": "claude-sonnet-4", "provider": "anthropic" }
  }
}
```

**实测成本对比**（30 天用量统计，引用自内部案例）：

| 任务类型 | 模型 | 月成本（有降级链） | 全部用 Opus |
|---------|------|------------------|------------|
| 文档编写 | Flash | $30 | $3,000 |
| 代码审查 | Sonnet | $900 | $4,500 |
| 架构设计 | Opus | $450 | $450 |
| 简单编辑 | Sonnet | $1,500 | $7,500 |
| **合计** | — | **$2,880** | **$15,450** |

降级链节省 81% 成本。文档类任务从 Opus 降到 Flash，成本降 100 倍，用户几乎无感知。

### 2.3 Token 预算与 Compaction 触发

```json:opencode.json
{
  "tokenBudget": {
    "total": 200000,
    "reserved": 0.25,
    "maxInputTokens": 160000,
    "perSession": { "maxTokens": 100000, "maxRounds": 50 }
  },
  "compaction": {
    "strategy": "adaptive",
    "threshold": 0.80,
    "protectWindow": 40000
  }
}
```

当 Token 利用率超 70% 时，Compaction 分级触发：

```mermaid
flowchart TB
    S[每轮对话结束] --> C{Token 利用率}
    C --> |"< 70%"| N[正常运行]
    C --> |"70-85%"| L[轻量压缩<br>摘要对话历史]
    C --> |"85-95%"| M[中度压缩<br>合并工具输出]
    C --> |"> 95%"| H[深度压缩+模型降级]
    L --> V{验证}
    V --> |通过| OK[继续]
    V --> |失败| M
    M --> H
    H --> F[截断至 80%]
    style C fill:#4A90D9,color:#fff
    style L fill:#50C878,color:#fff
    style M fill:#FF9F43,color:#fff
    style H fill:#E74C3C,color:#fff
```

## 三、Hashline 编辑

### 3.1 问题背景

传统"搜索-替换"编辑模式有三个问题：
1. **陈旧行错误**：文件被读取后发生变化，旧的搜索文本匹配不到
2. **模糊匹配**：Agent 记不住精确缩进，替换失败
3. **冲突风险**：多 Agent 编辑时相互覆盖

### 3.2 原理

Hashline 的核心：**按内容哈希定位，不是按行号定位**。

每行代码 = 行号 + SHA256 内容哈希。Agent 编辑时引用哈希而不是行号——验证当前行哈希匹配才执行修改，不匹配直接报错。实现 0% 陈旧行错误。

### 3.3 配置

```json:opencode.json
{
  "experimental": {
    "hashline": {
      "enabled": true,
      "algorithm": "sha256",
      "hashPrefixLength": 12,
      "verifyOnWrite": true,
      "conflictResolution": "reject"
    }
  }
}
```

| 场景 | 推荐 | 原因 |
|------|------|------|
| 单人开发 | 可关闭 | 无冲突风险 |
| 多人协作 | 强烈推荐 | 防止覆盖同事修改 |
| CI/CD 流水线 | 建议开启 | 确定性要求高 |
| 大型重构 | 开启 | 多文件编辑，旧状态风险高 |

**性能影响**：1000 行文件哈希计算约 1.2ms，对比 Agent 推理耗时（2-15 秒）占比 < 0.1%。

## 四、上下文优化

### 4.1 `.opencodeignore` 排除策略

```markdown:terminal
# 构建产物
dist/ build/ .next/ target/
# 依赖目录
node_modules/ vendor/ .venv/
# 日志和临时文件
*.log *.tmp .DS_Store
# 二进制文件
*.bin *.dll *.so *.pkl
```

**实测效果**（Spring Boot 40K 行代码）：

| 配置 | 文件数 | Token/搜索 | 耗时 |
|------|-------|-----------|------|
| 无 ignore | 8,420 | 38,000 | 4.2s |
| 有 ignore | 420 | 1,800 | 0.3s |

Token 降 95%，搜索快 14 倍。

### 4.2 本地搜索工具

| 工具 | 作用 | 提速 |
|------|------|------|
| ripgrep | 内容搜索替代 grep | 10-50x |
| ast-grep | AST 级结构搜索 | 5-10x |

安装后 Agent 自动调用 `rg` 替代 `grep`，大项目从 5-15 秒降到 1 秒内。

### 4.3 Context7 MCP

按需查询依赖文档，减少"试错"性工具调用 30-50%（引用自 Context7 官方文档）。Agent 检测到库 → 调 Context7 查文档 → 注入摘要。

### 4.4 Session Compaction 策略

| 策略 | 适用场景 | 压缩比 |
|------|---------|-------|
| `aggressive` | 长会话、预算紧张 | 50-70% |
| `adaptive`（默认） | 大多数场景 | 30-50% |
| `conservative` | 深度架构讨论 | 10-20% |

## 五、性能决策树

下图展示了性能优化方案的决策树，帮助根据场景选择合适的上下文配置策略。

```mermaid
flowchart TB
    S[发现性能问题] --> D{问题类型}
    D --> |响应慢| Slow[检查 Session 日志]
    D --> |Token 高| Cost[检查 Token 用量]
    D --> |错误多| Error[检查错误事件]

    Slow --> M{模型过重}
    M --> |是| DG[配置降级链]
    M --> |否| CX{上下文过大}
    CX --> |是| CP[调整压缩策略]
    CX --> |否| TL{工具阻塞}
    TL --> |是| OT[优化工具链]

    Cost --> IG{配了 ignore}
    IG --> |否| AI[配置 .opencodeignore]
    IG --> |是| LS{本地搜索}
    LS --> |否| IS[安装 ripgrep]
    LS --> |是| BG{预算合理}
    BG --> |否| AB[调整 Token 预算]

    Error --> PM{权限不足}
    PM --> |是| FP[调整权限]
    PM --> |否| TE{工具失败}
    TE --> |是| FT[检查工具参数]
    TE --> |否| CM{上下文缺失}
    CM --> |是| OC[增大保护窗口]

    style S fill:#4A90D9,color:#fff
    style D fill:#50C878,color:#fff
```

## 六、调优案例

以下数据来自真实项目（40K 行 Java，团队 5 人）：

| 指标 | 调优前 | 调优后 | 改善 |
|------|--------|--------|------|
| 响应时间 | 45s | 12s | 73% |
| 输入 Token/会话 | 180K | 65K | 64% |
| 错误率 | 12% | 3% | 75% |
| 月成本 | ~$2,100 | ~$385 | 82% |

**各措施贡献**：

| 措施 | 节省占比 | 说明 |
|------|---------|------|
| 降级链 | 55% | 文档/简单任务分配到 Flash |
| .opencodeignore | 18% | 排除无关文件 |
| Compaction | 12% | 减少输入 Token |
| Token 预算 | 10% | 防止 Session 超限 |
| Hashline | 3% | 减少冲突重试 |
| 本地搜索 | 2% | 搜索效率提升 |

**推荐优化路径**：
1. 配置 `.opencodeignore`（10 分钟，见效最快）
2. 安装 ripgrep（5 分钟，搜索快 10 倍）
3. 配置 Token 预算 + Compaction（15 分钟）
4. 配置降级链（20 分钟，大幅降本）
5. 开启 Hashline（5 分钟，多人协作必做）

## 七、性能基准

以下基准数据帮助你在调优前设定合理预期，对比不同技术路线的收益。

### 7.1 任务类型成本基准

| 任务类型 | 模型 | 平均输入 Token | 平均输出 Token | 单次成本 | 延迟 |
|---------|------|---------------|---------------|---------|------|
| 代码审查 | Claude Sonnet | 45K | 2.5K | ~$0.04 | 18s |
| 代码审查 | GPT-5.4-nano | 45K | 2.5K | ~$0.01 | 8s |
| 代码生成 | Claude Sonnet | 28K | 8K | ~$0.05 | 25s |
| 代码生成 | DeepSeek V4-Flash | 28K | 8K | ~$0.002 | 12s |
| 文档编写 | Claude Haiku | 12K | 3K | ~$0.003 | 5s |
| 文档编写 | GPT-5.4-mini | 12K | 3K | ~$0.001 | 3s |
| 文件编辑 | Claude Sonnet | 35K | 1.5K | ~$0.03 | 15s |
| SQL 查询 | GPT-5.4-nano | 10K | 1K | ~$0.002 | 4s |

> 以上数据基于 2026 Q1 定价，以 100 次调用为样本取中位数。实际成本因模型定价波动和 Token 压缩率而异。

### 7.2 优化技术收益对比

| 优化技术 | 实施成本 | Token 节省 | 延迟改善 | 复用性 |
|---------|---------|-----------|---------|--------|
| `.opencodeignore` 排除 | 5 分钟 | 15-30% | 10-20% | 项目级，一次配置 |
| ripgrep 本地搜索 | 3 分钟 | 0% | 40-60%（搜索） | 全局一次安装 |
| Compaction 自动压缩 | 10 分钟 | 20-40% | 15-30% | 配置即生效 |
| 模型降级链 | 20 分钟 | 40-60% | 30-50% | 需持续调整 |
| Hashline 编辑 | 5 分钟 | 2-5% | 5-10%（重试） | 一次启用 |
| 提示词缓存 | 15 分钟 | 15-25% | 20-35% | 缓存逐出需关注 |
| Token 预算上限 | 5 分钟 | 10-20% | 防止极端值 | 全局配置 |

### 7.3 大型项目参考基准

| 项目规模 | 代码行数 | 典型上下文窗口 | 单 Session Token | 推荐模型 |
|---------|---------|--------------|----------------|---------|
| 小型 | < 10K | 50-80K | 30-60K | GPT-5.4-nano / Haiku |
| 中型 | 10-100K | 80-150K | 60-200K | Claude Sonnet |
| 大型 | 100-500K | 150-200K | 100-500K | Claude Sonnet + Flash 降级 |
| 巨型 | > 500K | 200K（需压缩） | 300K-1M+ | Sonnet + Flash 降级 + Aggressive 压缩 |

**关键洞察**：对于 40K 行以上的项目，仅靠模型选择不足以控制成本——必须启用 Compaction 和降级链组合。单 Session Token 超过 200K 时，Compaction 的收益曲线陡峭上升。

## 常见反模式

### 只加模型不调配置

**现象**：发现 Token 成本太高后，直接切换到更便宜的模型（从 Sonnet 换到 Haiku），但 .opencodeignore、Compaction 策略等配置维持不变。

**原因**：认为"成本问题的根因是模型太贵"，模型降级是一劳永逸的解决方案。

**对策**：切换模型前，先做配置优化——排除无关文件、启用 Compaction、设置 Token 预算。这些优化通常能节省 30-50% 的 Token，且不牺牲输出质量。模型降级会同时降低输出质量，是最后的手段。

### 基准测试不做全量统计

**现象**：对比优化前后的性能时，只跑了 1-2 次测试就得出结论。

**原因**：想"快速看到效果"，忽略了 LLM 输出的随机性和网络延迟的波动性。

**对策**：性能对比至少跑 10 次取中位数。记录每次的 Token 消耗、延迟和输出质量评分。使用统计方法（t 检验）确认优化效果显著而非随机波动。

### 忽略. opencodeignore 的价值

**现象**：.opencodeignore 文件不存在或只排除了 node_modules，Agent 每次启动仍然扫描大量无关文件。

**原因**：认为"Agent 足够聪明，会自己跳过不相关的内容"。

**对策**：Agent 再聪明也需要先读取文件才能判断是否相关——这个过程已经消耗了 Token。主动排除测试夹具、构建产物、生成的代码、大文件等无关内容，是性价比最高的优化手段。

## 常见错误与陷阱

### 模型降级链配置错误导致任务失败

**场景**：配置了 Sonnet → Haiku → GPT-5.4-nano 的降级链，但第三个模型不支持工具调用，导致依赖工具的任务失败。

**后果**：降级后 Agent 无法完成核心操作，用户以为是 Agent bug，实际上是降级链配置时没有考虑各模型的能力差异。

**预防**：降级链中的每个模型必须验证满足当前任务的核心能力需求（工具调用、长上下文、代码生成质量）。在降级链中跳过能力不匹配的模型。

### Token 预算设得太严导致频繁中断

**场景**：设置了严格的输出 Token 上限（如 500），Agent 生成代码到一半被截断。

**后果**：Agent 需要多次输出来完成同一个任务，反而增加了总 Token 消耗。

**预防**：输出 Token 预算根据任务类型差异化设置。代码生成任务设 2000-4000，简单问答设 500-1000。观察几轮后根据实际输出分布调整。

### 异步并行策略未验证副作用

**场景**：启用并行 Agent 策略后，两个并行 Agent 同时修改同一个文件，导致编辑冲突。

**后果**：一个 Agent 的修改被另一个覆盖，或者文件出现损坏。

**预防**：并行策略只适用于独立任务（不同文件、不同模块）。共享文件的任务应串行执行。在并行策略中配置文件锁或任务隔离规则。

## 适用场景与限制

### 性能优化的最佳场景

- Token 成本已占团队云支出显著比例的生产环境
- 大型项目中 Agent 响应迟缓（> 30 秒）影响开发效率
- 需要量化和展示 AI 编程工具投入产出比的团队

### 性能优化的局限

- **优化的边际收益递减**：完成基础优化（.opencodeignore、Compaction）后，进一步优化的空间越来越小
- **优化与质量的平衡**：过于激进的 Token 节省会损害 Agent 输出质量
- **基准测试本身有成本**：每次性能对比需要多次运行，消耗的 Token 和时间也是成本

### 什么时候不需要优化

个人项目、短会话、或 Token 成本在可接受范围内时，完成基础优化（.opencodeignore + Compaction 默认配置）即可。没必要投入大量时间做精细化调优。

## 关联章节

- ← [可观测性](../observability.md)
- ← [上下文压缩与Token 预算](../context-compression.md)
- ← [上下文压缩与Token 预算](../context-compression.md)
- → [案例研究](../07-case-studies/)

## 验证标准

完成本文学习后，你应该能：

1. 根据 Token 消耗和延迟指标识别性能瓶颈，定位具体的优化方向
2. 配置 Token 预算并启用 Compaction 策略，说明触发条件和压缩效果
3. 设置基于类别（core/security/performance/experimental/debug）的自动模型降级链
4. 解释 Hashline 编辑的零错误机制及其在多人协作中的作用
5. 编写 `.opencodeignore` 文件排除无关文件，验证上下文优化效果
