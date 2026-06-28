# Ch6: 高级话题

## 概述

本章覆盖四个子主题：核心扩展、上下文与记忆、安全与沙箱、运维与演进。每个主题都涉及 OpenCode 的底层机制，需要前三章的基础知识。

**章节核心主题**：深入底层机制——扩展、定制和优化 AI 编程工作流。

> **章节规模**：10 篇主文章 + 5 篇子文章（共 15 篇内容文件 + README）。**这是全书篇幅最大（约 10000 行）、内容最深的一章。**

### 实际交付 vs 规划对比

| 变更类型 | 规划项 | 实际交付 | 说明 |
|---------|-------|---------|------|
| **文章数** | 12 篇 | 10 篇主文章 + 5 篇子文章（context/目录下） | 原规划中 Article 6.10/6.11/6.12 编号顺移，新增 context/ 子目录 |
| **文章合并** | Article 6.4（上下文压缩）+ 6.5（Token 预算） | 合并为"上下文压缩与Token 预算"一篇 | Token 预算是压缩的超限处理策略，分开讲反而割裂 |
| **文章新增** | 未规划 | 上下文注入与检索（1006 行） | 选择性上下文注入 + AST 语义分块是 OMO 特有能力，需专文覆盖 |
| **文章新增** | 未规划 | DCP 与高级上下文管理插件（566 行） | DCP/ACM/Context Guard/Context Manager 四款生产级插件需统一介绍 |
| **文章新增** | 未规划 | 上下文质量度量（445 行） | 质量指标和监控命令是上下文优化的闭环 |
| **文章合并** | Article 6.10（CLAUDE.md 系统） | 合并入 AGENTS.md 约定系统（483 行） | CLAUDE.md 和 AGENTS.md 属同一约定系统，合并精简 |
| **文章新增** | 未规划 | 可观测性参考（335 行 → 550+ 行） | 作为 observability.md 的配置命令速查 Companion |
| **内容扩展** | 20 min 阅读 / 200+ 行 | 35 min 阅读 / 800+ 行 | OTel GenAI 语义约定 v1.41 引发的 14 项差距补充：评估第四支柱、MCP 追踪、Agent Span 类型、LLM 专有指标、内容捕获模式、成本估算、采样策略、四类仪表板、遥测管道健康自检、流式指标、日志持久化策略 |
| **子主题重组** | 三个进阶主题（MCP/Agent/性能） | 四个子主题（核心扩展/上下文与记忆/安全与沙箱/运维与演进） | 按工程领域组织更符合读者认知 |
| **阅读时间** | 每篇文章独立标注 | 文章内已添加 "⏱ 时间有限？先读这些" 导读 + 章节总时间（120 分钟） | 更灵活的时间导航 |
| **验证标准** | 需求验证项 | 7 篇已有 + 9 篇待补全 | 逐步对齐中 |

### 创作辅助

本章内容创作和评审中推荐配备以下智能体组合：

| 类型 | 推荐 | 理由 |
|------|------|------|
| **思维框架** | 没有调查没有发言权（研究源代码后再写）、矛盾论（抓关键杠杆点） | 高级话题面向深度用户，内容缺口最大，需要从底层机制出发的权威解释 |
| **人物视角** | Karpathy（底层机制理解）、Musk（成本优化）、Taleb（尾部风险） | 同上 |
| **启用阶段** | 初稿（视角驱动）+ 审校（框架验证） | 初稿时用人物视角打开思路，审校时用思维框架检查逻辑 |



## 文章

### Article 6.1: MCP 服务器
- **阅读时间**：25 min
- **学习目标**：
  - 理解MCP协议的核心概念（工具/资源/提示/传输层）
  - 掌握MCP服务器的配置方法（stdio / streamable-http / websocket）
  - 理解MCP与内置Tool的关系（同一ToolRegistry）
  - 能够独立配置至少一个MCP服务器
  - 了解MCP的安全考虑（环境变量隔离、认证）
- **前置知识**：Ch2（Tool系统理解），Article 3.2（MCP配置在opencode.json中的位置）
- **源材料映射**：OpenCode实战 01（MCP部分）+ OpenCode实战 02（MCP集成架构）

#### 大纲
1. MCP协议概览
   - 什么是MCP（Model Context Protocol）—— AI Agent的"API集成层"
   - Plugin vs MCP：内扩展 vs 外连接
   - MCP能做什么：数据库查询/API调用/文件系统/搜索引擎/AI服务
2. MCP配置详解
   - 传输类型：stdio（本地子进程）、streamable-http（远程服务）、websocket（全双工）
   - 配置格式：opencode.json中的mcpServers段
   - 环境变量管理
3. MCP与ToolRegistry的集成
   - 对LLM而言，内置Tool和MCP Tool无区别
   - MCP Tool的生命周期：注册 → 发现 → 调用 → 结果返回
   - 内置OMO MCP：Exa WebSearch / Context7 / Grep.app
4. 安全考虑
   - MCP服务器的进程隔离
   - 环境变量分离（不共享OpenCode进程环境）
   - OAuth认证配置
5. 实战：配置一个自定义MCP服务器
   - 从创建到验证的完整流程

#### 核心概念
- **MCP == 给Agent添加API能力**：每个MCP服务器相当于一个API网关，让Agent能够与外部系统交互。
- **MCP vs Plugin**：Plugin是能力扩展（添加新工具或Hook事件），MCP是外部集成（连接现有服务）。两者是互补关系。
- **ToolRegistry无差别集成**：LLM调用内置工具和MCP工具完全一样，没有任何代码层面的差异。

#### 代码/配置示例
- 三种传输类型的配置示例
- 数据库MCP配置
- 内置OMO MCP配置
- OAuth认证配置

#### Mermaid 图表
- MCP集成架构图（ToolRegistry → MCP Client → MCP Servers）
- 三种传输方式的对比图

> ⚠️ 写作时需包含威胁建模分析：使用 STRIDE 方法分析 MCP 通信通道（stdio/SSE/WebSocket）的威胁面，重点关注中间人攻击和未授权访问风险。

#### 关联章节
- ← Article 2.1（Agent的工具调用机制）
- ← Article 3.2（MCP配置）
- → Article 6.3（MCP调用的性能考量）

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 覆盖MCP核心概念
- [ ] 包含三种传输类型的配置示例
- [ ] 包含MCP与ToolRegistry集成的说明
- [ ] 包含安全配置说明


**创作辅助**:
- 思维框架：没有调查没有发言权（MCP协议需阅读源码）
- 人物视角：Karpathy（底层机制理解）
- 理由：MCP是高级话题中最核心的内容

---

### Article 6.2: 自定义 Agent 与 Plugin
- **阅读时间**：25 min
- **学习目标**：
  - 理解自定义Agent的完整过程（定义→注册→使用）
  - 掌握Plugin开发基础（Hook点 + 自定义Tool）
  - 理解Plugin的Pipeline执行模式
  - 了解OMO的Hook点体系（53+ Hook点）
- **前置知识**：Article 2.1（Agent系统理解），Article 3.2（配置基础）
- **源材料映射**：OpenCode实战 01（Plugin部分）+ OpenCode实战 02（Plugin系统、OMO Hook点）+ OpenCode实战 04（Plugin做守卫Env Guard完整代码）

#### 大纲
1. 自定义Agent
   - Agent定义方式（agent.json / opencode.json agents段）
   - 指定角色、Skill、工具集、温度、最大轮次
   - 自定义Agent的使用：Tab切换或Command指定
   - OMO自定义Agent配置
2. Plugin开发基础
   - definePlugin API
   - 添加自定义Tool：Tool定义 → 注册 → Agent使用
   - 工具优先级：Plugin Tool > MCP Tool > Built-in Tool
   - 覆盖内置工具（同名覆盖）
3. Plugin Hook点
   - OpenCode内置20+ Hook：session:start/end, tool:before/after, command:before/after, permission:check
   - OMO 53+ Hook点：onWorkflowStart, onAgentSelect, onContextAssemble, onLLMRequest, onQualityGate
   - Pipeline模式：上一个输出 = 下一个输入
4. 完整Plugin示例：Env Guard
   - 功能：防止敏感信息泄露
   - Hook点：preReadFile + preWriteFile
   - 正则检测：AWS Key / Private Key / GitHub Token / OpenAI Key
   - 策略：mask（遮盖）/ reject（拒绝）/ audit（记录）
5. Plugin部署和管理

#### 核心概念
- **Plugin的pipeline设计**：多个Plugin按顺序组成处理链，每个Plugin接收上一个的输出。这种设计让Plugin可组合、可复用。
- **Hook点的时机选择**：before Hook适合拦截/修改/增强，after Hook适合记录/统计/通知。
- **覆盖内置工具的风险**：同名覆盖虽然灵活，但可能导致意外行为。建议只在确有必要时使用。

#### 代码/配置示例
- 自定义Agent定义示例（agent.json）
- OMO自定义Agent配置示例
- Plugin基本定义（添加Tool）
- 完整Env Guard Plugin代码
- Plugin展开和工具优先级配置

#### Mermaid 图表
- Plugin Pipeline执行流程图
- Hook点事件时间线图
- 自定义Agent声明周期图

#### 关联章节
- ← Article 2.1（Agent系统）+ Article 2.2（Plugin概念）
- → Ch7（自定义Agent在案例中的应用）
- ← Ch3（配置中注册Plugin）

#### 验证标准
- [ ] 文章 ≥ 250 行有效内容
- [ ] 包含自定义Agent的完整定义示例
- [ ] 包含Plugin开发的完整流程
- [ ] 包含Env Guard Plugin的完成代码
- [ ] 覆盖至少10个Hook点


**创作辅助**:
- 思维框架：矛盾论（分清副驾驶的两种模式）
- 人物视角：Karpathy（人机协作最佳实践）
- 理由：副驾驶模式是人机协作的重要范式

---

### Article 6.3: 性能调优与成本管理
- **阅读时间**：20 min
- **学习目标**：
  - 理解OpenCode的性能瓶颈识别方法
  - 掌握成本管控策略（模型降级、Token预算）
  - 理解Hashline编辑（零错误编辑）机制
  - 掌握Session管理和上下文优化技巧
- **前置知识**：Article 3.2（配置中的成本管控段）
- **源材料映射**：OpenCode实战 02（成本架构/Token管控/可观测性54+事件）+ OpenCode实战 03（Token效率优化）+ OpenCode实战 04（模型降级链）

#### 大纲
1. 性能瓶颈识别
   - 响应慢 vs Token消耗大 vs 错误率高
   - 54+ Event Hooks的可观测性体系
   - Session日志分析
2. 成本管控策略
   - Token预算与会话级上限
   - 模型降级链（Category-based Auto-downgrade）
   - 上下文压缩（Compaction策略）
   - 工具输出保护窗口（保护最近40K Token）
   - 成本对比数据（各类任务节省比例）
3. Hashline编辑
   - 基于LINE#ID内容哈希的编辑
   - 0%陈旧行错误
   - 配置和使用
4. 上下文优化
   - .opencodeignore排除无关文件
   - 安装本地搜索工具（ripgrep/ast-grep）
   - Context7 MCP自动查询文档
   - Session Compaction策略选择
5. 性能基准和调优案例

#### 核心概念
- **成本优化的三层模型**：模型选择（Type-level） → Token预算（Session-level） → 上下文压缩（Message-level）。
- **Category-based Auto-downgrade的设计意图**：不是降级"所有"简单任务，而是根据任务类型智能选择模型。文档任务用便宜模型，复杂编码用高端模型。
- **可观测性是调优的前提**：不知道Agent在做什么、花了多少Token、为什么慢，就无法调优。Event Hooks提供了完整的可观测性。

#### 代码/配置示例
- Token预算配置
- 模型降级链配置
- 成本对比数据表
- Hashline配置示例
- .opencodeignore示例

#### Mermaid 图表
- 成本管控策略三层模型图
- Compaction触发流程图
- 性能调优决策树

#### 关联章节
- ← Article 3.2（成本管控是配置的一部分）
- ← Ch4（工作流效率与Token消耗的平衡）
- → Ch7（大型案例中的成本考量）


**创作辅助**:
- 思维框架：统筹兼顾（性能与成本的权衡）
- 人物视角：Musk（成本效率分析）
- 理由：性能调优直接影响用户体验和成本

### 团队角色评审补充
- **安全架构师需求（P0）**：Article 6.1 MCP安全节扩展为完整安全子节——OAuth认证流程、JWT令牌管理、MCP进程隔离技术细节、MCP供应链风险评估指南；Article 6.2 Env Guard增加自定义敏感信息检测规则和策略配置；Plugin Hook点威胁分析——哪些Hook点风险最高。
- **后端架构师需求（P0）**：Article 6.1 增加MCP服务端实现视角——"如何将你的后端服务变成MCP Server"（Node.js/Python服务端SDK、Tool/Resource/Prompt实现模式）；补充"将Express/Fastify服务转为MCP Server"的完整示例。
- **架构顾问需求**：Article 6.1 补充MCP威胁建模——每种传输类型的攻击面分析（stdio本地提权、streamable-http MITM、websocket会话劫持）；Article 6.2 Plugin提权分析——Hook点的权限放大风险。
- **渗透测试员需求**：Article 6.1 补充MCP的Prompt注入和供应链安全；Article 6.2 Agent生成代码的安全审查流程和常见AI生成漏洞模式。
- **测试工程师需求**：Ch6 所有文章的配置示例需要标注最低版本要求。

---

## 章节重构增补

> **源材料说明**：《驾驭工程：从 Claude Code 源码到 AI 编码最佳实践》（中文别名：《马书》）是一本 Engineering（驾驭工程）的中文技术书。它以 Claude Code `v2.1.88` 的公开发布包与 source map 还原结果为分析材料，从真实工程实现中提炼 AI 编码 Agent 的架构模式、上下文策略、权限体系和生产实践。在线阅读：https://zhanghandong.github.io/harness-engineering-from-cc-to-ai-coding/

### 修改标注（基于章节重构计划）

**Article 6.1（MCP 服务器）**：
- 扩展 MCP 协议深度（stdio/SSE/WebSocket）
- 补充 ToolRegistry 统一架构说明
- 新增 MCP 服务器沙箱安全配置

**Article 6.2（自定义 Agent）**：
- 增加《马书》第20章三种 Agent 派生模式引用
- 增加 Effort/Fast Mode/Thinking 配置详解
- 补充 Agent 派生模式在 OMO 中的实现

**Article 6.3（性能调优）**：
- 增加模型降级链的完整配置
- 增加成本优化的策略对比
- 补充 Token 预算策略的深入分析

---

### Article 6.4: 上下文压缩（P0）
- **阅读时间**：20 min
- **学习目标**：
  - 理解自动上下文压缩（Compaction）的原理
  - 掌握微压缩策略的配置方法
  - 理解压缩后恢复的机制和保真度
- **前置知识**：Ch2 Art.2.4（上下文工程核心概念）
- **源材料映射**：《马书》第9-11章

#### 大纲
1. 为什么需要上下文压缩
   - Token 窗口是 Agent 的"工作记忆"
   - 长 Session 中的上下文膨胀问题
2. Compaction 工作原理
   - 自动摘要机制
   - 优先级保留策略
   - 压缩比和保真度权衡
3. 微压缩策略
   - 选择性保留（代码 vs 对话 vs 工具输出）
   - 工具输出保护窗口（最近 40K Token）
   - 自定义压缩规则
4. 压缩后恢复机制
   - 从压缩状态恢复到完整工作状态
   - 恢复的触发条件
   - 恢复失败的处理
5. 实测效果
   - 压缩比数据
   - Token 节省统计
   - 准确率影响评估

#### 核心概念
- **压缩是"有损"还是"无损"**：上下文压缩是有损的，但好的策略让损失降到最低。关键在于知道什么可以丢，什么必须保留。
- **压缩不是一次性的**：上下文在 Session 中会被多次压缩，每次压缩都会损失信息。设计目标是在"可接受的信息损失"内最大化 Token 节省。

#### 代码/配置示例
- Compaction 配置参数
- 工具输出保护窗口配置
- 自定义压缩规则

#### Mermaid 图表
- Compaction 触发流程图
- 压缩/恢复的全生命周期图
- 压缩比 vs 保真度关系曲线

#### 关联章节
- ← Ch2 Art.2.4（上下文工程基础）
- → Article 6.5（Token 预算与压缩的配合）
- → Article 6.11（可观测性监控压缩效果）

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 包含 Compaction 原理说明
- [ ] 包含压缩配置示例
- [ ] 包含至少 1 组压缩前后 Token 量对比数据
- [ ] 包含压缩后恢复机制的完整流程说明


**创作辅助**:
- 思维框架：实践论（自定义Agent需端到端实现）
- 人物视角：Karpathy（构建即理解）
- 理由：自定义Agent开发是深度定制场景

#### 上下文压缩机制

**来源**：《马书》第9章

**核心架构**：

| 压缩类型 | 触发条件 | 压缩策略 | 恢复能力 |
|---------|---------|---------|---------|
| **自动压缩** | 上下文超过阈值 | 智能摘要 | 可恢复 |
| **微压缩** | 单轮对话过长 | 关键信息提取 | 部分恢复 |
| **手动压缩** | 用户触发 | 完整摘要 | 完全可恢复 |

**配置示例**：
```json
{
  "context": {
    "compaction": {
      "enabled": true,
      "threshold": 0.8,
      "strategy": "auto"
    }
  }
}
```

---

### Article 6.5: Token 预算策略（P0）
- **阅读时间**：15 min
- **学习目标**：
  - 掌握 Token 预算的估算方法
  - 理解预算分配策略
  - 能够配置合理的 Token 上限
- **前置知识**：Article 6.4（上下文压缩）
- **源材料映射**：《马书》第12章

#### 大纲
1. Token 预算的概念
   - 什么是 Token 预算（类似于"内存配额"）
   - 为什么需要预算——防止无限消耗
2. 预算分配策略
   - 系统消息占用
   - 用户输入占用
   - 工具输出占用
   - 预留空间
3. 估算方法
   - 按任务类型估算
   - 按代码行数估算
   - 经验公式和工具
4. 预算超限处理
   - 压缩触发
   - 降级（使用更便宜的模型）
   - 强制截断
5. 最佳实践

#### Mermaid 图表
- Token 预算分配饼图
- 预算超限处理决策树

#### 关联章节
- ← Article 6.4（压缩在预算超限时触发）
- → Article 6.3（配置中的预算参数）
- → Article 6.6（缓存可以节省预算）

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 包含预算分配策略
- [ ] 包含按任务类型的估算方法
- [ ] 包含配置示例
- [ ] 包含预算超限的降级策略（压缩/降模型/截断）
- [ ] 包含至少 1 个预算分配的完整实例（含估算→分配→调整过程）


**创作辅助**:
- 思维框架：集中兵力（聚焦Token消耗最大的场景）
- 人物视角：Musk（成本敏感度）
- 理由：Token预算管理直接影响API成本

#### Token 预算策略

**来源**：《马书》第12章

**预算分配模型**：

| 预算类型 | 分配比例 | 用途 | 超限处理 |
|---------|---------|------|---------|
| **系统提示词** | 20% | Agent 系统指令 | 不可压缩 |
| **上下文** | 50% | 项目文件、对话历史 | 触发压缩 |
| **输出** | 30% | Agent 响应 | 截断或续写 |

**配置示例**：
```json
{
  "budget": {
    "total": 200000,
    "system": 0.2,
    "context": 0.5,
    "output": 0.3
  }
}
```

---

### Article 6.6: 提示词缓存（P0）
- **阅读时间**：25 min
- **学习目标**：
  - 理解三级缓存架构
  - 掌握缓存断点和中断检测
  - 了解 7+ 种缓存优化模式
- **前置知识**：Article 6.5（Token 预算）
- **源材料映射**：《马书》第13-15章

#### 大纲
1. 缓存的价值
   - 重复内容的 Token 浪费
   - 缓存 vs 压缩：互补策略
2. 三级缓存架构
   - 第一级：Session 内缓存
   - 第二级：跨 Session 缓存
   - 第三级：持久化缓存
3. 缓存断点
   - 什么是断点（用户定义的可复用上下文片段）
   - 断点设置策略
   - 断点的生命周期
4. 中断检测
   - 会话中断的自动检测
   - 断点续传机制
   - 中断后的恢复策略
5. 7+ 缓存优化模式
   - 系统指令固化
   - 项目知识缓存
   - 工具输出缓存
   - 往返模式缓存
6. 缓存命中率优化

#### Mermaid 图表
- 三级缓存架构图
- 缓存命中流程时序图
- 7 种缓存优化模式对比图

#### 关联章节
- ← Article 6.5（缓存是预算策略的一部分）
- → Article 6.7（记忆系统与缓存的关系）
- ← Ch2 Art.2.4（上下文工程基础）

#### 验证标准
- [ ] 文章 ≥ 250 行有效内容
- [ ] 包含三级缓存架构说明
- [ ] 包含缓存断点配置
- [ ] 覆盖至少 5 种优化模式


**创作辅助**:
- 思维框架：星星之火（可观测性从最小指标开始）
- 人物视角：Feynman（测量才能理解）
- 理由：可观测性帮助用户理解Agent行为

#### 提示词缓存架构

**来源**：《马书》第13章

**三级缓存架构**：

| 缓存级别 | 缓存内容 | 命中率 | 刷新策略 |
|---------|---------|--------|---------|
| **L1：系统级** | 系统提示词 | 95%+ | 版本更新 |
| **L2：项目级** | AGENTS.md、项目配置 | 80%+ | 文件修改 |
| **L3：会话级** | 对话历史 | 60%+ | 会话结束 |

**缓存断点设计**：
```markdown
<!-- cache-breakpoint -->
```

**7+ 优化模式**：
1. 静态内容前置
2. 动态内容后置
3. 缓存断点标记
4. 分段缓存
5. 缓存预热
6. 缓存失效检测
7. 缓存命中率监控

---

### Article 6.7: 记忆系统（P0）
- **阅读时间**：20 min
- **学习目标**：
  - 理解 Memdir 架构的设计原理
  - 掌握 Auto-Dream 跨会话记忆机制
  - 理解 Compaction 在记忆系统中的作用
- **前置知识**：Article 6.6（缓存系统）
- **源材料映射**：《马书》第24章

#### 大纲
1. 记忆 vs 缓存
   - 记忆是主动的（Agent 记得什么），缓存是被动的（系统存了什么）
   - 记忆系统解决的问题：跨 Session 上下文保持
2. Memdir 架构
   - 目录结构设计
   - 记忆文件的格式和索引
   - 记忆的读写策略
3. Auto-Dream 机制
   - 自动生成记忆摘要
   - 记忆的重要度评分
   - 记忆的自动淘汰
4. Compaction 与记忆的配合
   - Compaction 保留重要决策和上下文
   - 记忆作为 Compaction 的输入
5. 记忆系统的安全考虑
   - 敏感信息保护
   - 多项目隔离

#### Mermaid 图表
- Memdir 架构图
- Auto-Dream 工作流程图
- 记忆生命周期图

#### 关联章节
- ← Article 6.6（缓存是记忆的基础设施）
- → Article 6.11（可观测性监控记忆效果）
- ← Ch2 Art.2.4（上下文工程）

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 包含 Memdir 架构说明
- [ ] 包含 Auto-Dream 机制
- [ ] 包含安全配置


**创作辅助**:
- 思维框架：没有调查没有发言权（Hook机制需实验验证）
- 人物视角：Karpathy（事件驱动架构）
- 理由：沙箱Hook是安全机制的关键组件

#### 记忆系统架构

**来源**：《马书》第24章

**Memdir 架构**：

```
.memdir/
├── conversations/     # 对话记忆
├── decisions/         # 决策记录
├── learnings/         # 学习积累
└── auto-dream/        # 自动整理
```

**核心功能**：
- **Auto-Dream**：自动整理和压缩记忆
- **Compaction**：跨会话记忆压缩
- **检索增强**：基于向量相似度的记忆检索

**配置示例**：
```json
{
  "memory": {
    "enabled": true,
    "path": "./.memdir",
    "autoDream": true,
    "retention": "30d"
  }
}
```

---

### Article 6.8: 安全总览（P0）
- **阅读时间**：25 min
- **学习目标**：
  - 掌握 OpenCode 的 6 种权限模型
  - 理解 YOLO 分类器的决策机制
  - 掌握提示注入防御的基本策略
- **前置知识**：Ch2 Art.2.5（约束系统）
- **源材料映射**：《马书》第16-17b章

#### 大纲
1. 安全的整体架构
   - 权限 → 分类 → 隔离 → 防御的四层模型
   - 攻击面分析
2. 6 种权限模式
   - 全局模式 / 项目模式 / 会话模式 / 工具模式
   - 允许/询问/禁止三级策略
   - 自定义规则的优先级
3. YOLO 分类器
   - 高/中/低风险的分类依据
   - YOLO 分类的训练方法
   - 自定义分类规则
4. 提示注入防御
   - 注入攻击的类型
   - 防御策略
   - 注入检测和记录
5. 权限审计
   - 审计日志
   - 合规映射（NIST/SOC2/等保）
   - 定期审查策略

#### Mermaid 图表
- 四层安全架构图
- YOLO 分类决策流程图
- 提示注入攻击树图

> ⚠️ 写作时需包含威胁建模分析：使用 STRIDE 方法在 Agent 编排全过程中系统性地分析威胁面，特别是权限提升和权限滥用场景。

#### 关联章节
- ← Ch2 Art.2.5（约束系统基础）
- → Article 6.9（沙箱是安全隔离的执行层）
- ← Ch3 §3.2（配置中的安全配置）

#### 验证标准
- [ ] 文章 ≥ 250 行有效内容
- [ ] 覆盖 6 种权限模式
- [ ] 包含 YOLO 分类器配置
- [ ] 包含提示注入防御示例


**创作辅助**:
- 思维框架：批评与自我批评（安全总览需严格审查）
- 人物视角：Taleb（尾部风险）
- 理由：安全总览是全书安全主题的纲领性文章

#### 安全模型详解

**来源**：《马书》第16章

**6 种权限模式**：

| 模式 | 描述 | 适用场景 |
|------|------|---------|
| **allow** | 完全允许 | 受信任的操作 |
| **deny** | 完全拒绝 | 危险操作 |
| **ask** | 每次确认 | 敏感操作 |
| **auto** | 智能决策 | 常规操作 |
| **session** | 会话级缓存 | 批量操作 |
| **bypass** | 绕过检查 | 系统操作 |

**YOLO 分类器**：
- 自动评估操作风险等级
- 高风险操作自动降级为 ask
- 低风险操作自动升级为 allow

**注入防御**：
- 提示词注入检测
- 命令注入过滤
- 路径遍历防护

---

### Article 6.9: 沙箱与 Hook 系统（P0）
- **阅读时间**：25 min
- **学习目标**：
  - 理解沙箱系统（Seatbelt/Bubblewrap）的工作原理
  - 掌握 53+ Hook 点的分类和使用
  - 能够配置自定义 Hook 事件
- **前置知识**：Article 6.8（安全总览）
- **源材料映射**：《马书》第18-18b章，OMO Hook

#### 大纲
1. 沙箱系统
   - Seatbelt（macOS）和 Bubblewrap（Linux）的隔离原理
   - 沙箱的配置策略
   - 沙箱的性能影响
2. Hook 点体系
   - 事件的完整生命周期
   - 53+ Hook 点分类：Session / Tool / Command / Permission / Workflow
   - 关键 Hook 点详解
3. 自定义 Hook
   - Hook 注册和优先级
   - Pipeline 模式：多个 Hook 顺序执行
   - 异步 Hook vs 同步 Hook
4. 沙箱与 Hook 的协作
   - Hook 作为沙箱的"守卫"
   - 事件驱动的安全策略

#### Mermaid 图表
- 沙箱架构隔离图
- Hook 点事件时间线图
- Hook Pipeline 执行流程图

> ⚠️ 写作时需包含威胁建模分析：分析沙箱逃逸威胁场景，包括通过恶意 Hook 点绕过沙箱隔离、权限提升和资源耗尽攻击。

#### 关联章节
- ← Article 6.8（安全的执行层）
- → Article 6.2（Plugin 开发中的 Hook 使用）
- → Ch7（案例中的安全配置）

#### 验证标准
- [ ] 文章 ≥ 250 行有效内容
- [ ] 包含沙箱配置示例
- [ ] 覆盖至少 20 个 Hook 点
- [ ] 包含自定义 Hook 示例


**创作辅助**:
- 思维框架：矛盾论（抓安全与非功能质量的关系）
- 人物视角：Karpathy（AI安全工程）
- 理由：安全与非功能质量紧密相关

#### 沙箱与 Hook 系统

**来源**：《马书》第18章

**沙箱隔离技术**：

| 平台 | 沙箱技术 | 安全级别 |
|------|---------|---------|
| macOS | Seatbelt | 高 |
| Linux | Bubblewrap | 高 |
| Windows | Windows Sandbox | 中 |

**26 种 Hook 事件**：

| Hook 类型 | 触发时机 | 用途 |
|---------|---------|---------|
| `onWorkflowStart` | 工作流开始 | 初始化、日志 |
| `onFileEdit` | 文件编辑 | 审计、备份 |
| `onBashExecute` | Bash 执行 | 安全检查 |
| `onAgentSpawn` | Agent 创建 | 权限验证 |
| `onWorkflowEnd` | 工作流结束 | 清理、报告 |

**四种 Hook 类型**：
1. **Shell 命令**：执行外部脚本
2. **Agent 验证器**：自定义验证逻辑
3. **MCP 调用**：调用外部服务
4. **内置函数**：快速响应

---

### Article 6.10: CLAUDE.md 系统（P0）
- **阅读时间**：15 min
- **学习目标**：
  - 理解 CLAUDE.md 用户指令覆盖层
  - 掌握 @include 指令系统的使用
  - 理解 CLAUDE.md 与 AGENTS.md 的关系
- **前置知识**：Ch2 Art.2.3（AGENTS.md）
- **源材料映射**：《马书》第19章

#### 大纲
1. CLAUDE.md 的作用
   - 用户指令覆盖层的概念
   - 与 AGENTS.md 的职责划分
2. 指令覆盖策略
   - 全局指令（CLAUDE.md）
   - 项目指令（CLAUDE.md 在项目根目录）
   - 子目录指令（@include）
3. @include 指令系统
   - 包含外部文件
   - 指令嵌套
   - 指令的优先级和合并规则
4. 最佳实践
   - 什么放在 AGENTS.md vs CLAUDE.md
   - 团队级指令管理

#### Mermaid 图表
- CLAUDE.md 覆盖层架构图
- @include 指令的加载流程图

#### 关联章节
- ← Ch2 Art.2.3（AGENTS.md）
- → Article 6.8（安全指令覆盖）
- → Ch4（指令对不同工作流的影响）

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 包含 CLAUDE.md 完整说明
- [ ] 包含 @include 使用示例


**创作辅助**:
- 思维框架：实践论（CLAUDE.md需实际项目验证）
- 人物视角：Paul Graham（好的文档就是好的代码）
- 理由：CLAUDE.md是OpenCode的AGENTS.md

---

### Article 6.11: 可观测性（P0）
- **阅读时间**：35 min（含参考文件总计 50 min）
- **学习目标**：
  - 理解 logEvent 系统和 5 层遥测架构
  - 掌握评估（Evaluation）作为 AI 可观测性第四支柱的概念
  - 熟悉 MCP 链路追踪标准和 OTel GenAI 语义约定
  - 掌握生产级监控的配置方法
  - 能够基于可观测性数据做性能优化和成本估算
- **前置知识**：Article 6.9（Hook 点概念）
- **源材料映射**：《马书》第29章，OMO 54+事件，OTel GenAI Semantic Conventions v1.41

#### 大纲
1. 可观测性的 3 + 1 个支柱
   - 日志（Logging）：事件记录
   - 指标（Metrics）：量化统计
   - 追踪（Tracing）：请求链路
   - **评估（Evaluation）**：AI 可观测性的第四支柱（LLM-as-judge、离线评估、黄金信号）
2. 5 层遥测架构
   - Agent 层 / Session 层 / 工具层 / 网络层 / 系统层
   - 每层的可观测性关注点
   - Agent Span 类型与 OTel 对齐（gen_ai.invoke_agent / execute_tool / retrieve_context）
3. MCP 链路追踪
   - MCP span 属性（mcp.request.method / response.status / server.address）
   - W3C Trace Context 传播
4. logEvent 系统
   - 事件的格式和结构
   - 事件的过滤和聚合
   - 事件输出（控制台/文件/外部系统）
   - 内容捕获模式（no-capture / span / external）
   - 日志持久化策略（保留周期、轮转、成本控制）
5. LLM 专有指标与 OTel 对齐
   - gen_ai.usage.prompt_tokens / completion_tokens
   - 流式指标（time_to_first_token、time_between_tokens）
   - Head-based 采样策略
6. 生产级监控
   - 关键指标面板
   - 告警规则（Token 消耗异常 / 错误率上升 / 响应时间超标）
   - 四类仪表板分层（实时诊断 / 容量规划 / 成本分析 / SLA 合规）
   - 性能基准和趋势分析
7. 基于可观测性的优化
   - 从日志发现性能瓶颈
   - 从指标优化成本（含实时成本估算模型）
   - 从追踪定位错误
   - 遥测管道健康自检（背压、丢事件、队列饱和度）

#### Mermaid 图表
- 5 层遥测架构图
- 可观测性数据流图
- 监控面板布局图

#### 关联章节
- ← Article 6.9（Hook 点是可观测性的基础）
- ← Article 6.3（基于可观测性做性能调优）
- → Ch7（案例中的监控配置）

#### 验证标准
- [ ] 文章 ≥ 400 行有效内容
- [ ] 包含 5 层遥测架构说明
- [ ] 包含 logEvent 配置示例
- [ ] 包含监控告警规则示例
- [ ] 包含至少 1 个监控仪表板的布局或关键指标说明
- [ ] 包含评估（Evaluation）作为第四支柱的说明
- [ ] 包含 MCP 链路追踪标准内容
- [ ] 包含 OTel GenAI 语义约定相关内容
- [ ] 包含内容捕获模式说明（no-capture / span / external）
- [ ] 包含成本估算模型说明
- [ ] 包含采样策略讨论
- [ ] 包含遥测管道健康自检


**创作辅助**:
- 思维框架：集中兵力（聚焦最有价值的国产模型）
- 人物视角：张一鸣（本土化策略）
- 理由：国产模型集成面向中国开发者

#### 可观测性架构

**来源**：《马书》第29章

**5 层遥测架构**：

| 层级 | 数据类型 | 用途 |
|------|---------|------|
| **L1：日志** | 操作日志 | 调试、审计 |
| **L2：指标** | 性能指标 | 监控、告警 |
| **L3：追踪** | 调用链 | 性能分析 |
| **L4：事件** | 业务事件 | 业务监控 |
| **L5：告警** | 异常告警 | 故障响应 |

**类型系统级 PII 保护**：
- 敏感字段自动脱敏
- 日志输出前类型检查
- 遥测事件安全设计

**磁盘持久化重试**：
- 网络故障自动重试
- 本地缓存队列
- 断点续传机制

---

### Article 6.12: Feature Flags 路线图（P2）
- **阅读时间**：15 min
- **学习目标**：
  - 了解 OMO 89 个 Feature Flag 的路线图
  - 理解产品演进方向
  - 能够跟踪和配置 Feature Flags
- **前置知识**：无（独立的路线图文章）
- **源材料映射**：《马书》第23章

#### 大纲
1. Feature Flag 机制
   - 什么是 Feature Flag（功能开关）
   - 为什么 OMO 需要 89 个 Flag
2. 路线图概览
   - 当前已实现的 Flags
   - 开发中的 Flags
   - 计划中的 Flags
3. 按领域分类
   - Agent 类 / 安全类 / 性能类 / 集成类 / 体验类
4. 如何跟进
   - 查看当前 Flags
   - 配置 Flags
   - 参与决策

#### Mermaid 图表
- Feature Flag 分类雷达图
- Flags 的版本分布图

#### 关联章节
- → 全书（影响所有章节的功能演进）
- ← Article 6.3（性能优化相关的 Flags）

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 覆盖 89 个 Flag 的主要分类
- [ ] 包含 Flag 配置方法
- [ ] 包含至少 1 个 Flag 的完整启用流程
- [ ] 说明 Flag 的版本演进和废弃机制


**创作辅助**:
- 思维框架：统筹兼顾（多维度性能指标的综合权衡）
- 人物视角：Musk（极致优化思维）
- 理由：性能基准提供量化决策依据

#### Feature Flags 路线图

**来源**：《马书》第23章

**89 个 Feature Flags 分类**：

| 分类 | 数量 | 示例 |
|------|------|------|
| **核心功能** | 20 | `enable_agent`, `enable_skill` |
| **安全特性** | 15 | `enable_sandbox`, `enable_audit` |
| **性能优化** | 18 | `enable_cache`, `enable_compaction` |
| **实验特性** | 25 | `enable_beta_feature` |
| **调试工具** | 11 | `enable_debug_mode` |

**使用场景**：
- 灰度发布
- A/B 测试
- 功能开关
- 紧急回滚

---

## 团队协作工作流

### 团队分工

| 角色 | 职责 | 负责文章 |
|------|------|---------|
| **安全架构师**（SECURITY） | 安全总览（6 权限模型+YOLO+注入防御）、沙箱与 Hook 系统、MCP 威胁分析、安全基线定义 | Article 6.8, Article 6.9, Article 6.1(安全节) |
| **后端架构师**（BACKEND） | MCP 服务端开发视角（Node.js/Python SDK）、ToolRegistry 统一架构、性能调优与成本管控、CI/CD 配置 | Article 6.1, Article 6.3, Article 6.5 |
| **架构顾问**（SYSA） | 上下文工程体系设计、Token 预算分配策略、三级缓存架构、CLAUDE.md 覆盖层架构 | Article 6.4, Article 6.5, Article 6.6, Article 6.10 |
| **渗透测试员**（REDTEAM） | MCP 注入攻击面分析、沙箱逃逸场景、Plugin Hook 点威胁分析、Prompt 注入防御测试 | Article 6.1(攻击面), Article 6.9(逃逸), Article 6.2(威胁) |
| **前端架构师**（FRONTEND） | Feature Flags 路线图可视化、可观测性监控面板布局、记忆系统 UI 设计 | Article 6.12, Article 6.11 |
| **测试工程师**（QA） | 所有配置示例最低版本标注、验证标准细化、可观测性监控规则验证 | 全文(版本标注), Article 6.11 |
| **UI设计师**（UX） | 监控仪表板布局图、Feature Flag 分类雷达图、15 篇文章图表一致性 | Article 6.11, Article 6.12, 全文图表 |

### 流程规范（Superpowers 工作流映射）

| 阶段 | 本阶段活动 | 交付物 | 负责人 |
|------|-----------|--------|--------|
| **头脑风暴** | 收集 15 篇文章的安全/架构/性能需求、确定 P0/P1/P2 分层写作优先级、识别文章间职责边界 | 分层写作计划、边界划分图 | 安全架构师 + 架构顾问 |
| **计划** | 排序写作依赖：6.1/6.2/6.3(现有修改) → 6.4-6.7(上下文体系) → 6.8-6.10(安全体系) → 6.11/6.12(可观测性+路线图) | 写作计划、依赖关系图 | 敏捷教练 |
| **实施** | 15 篇文章分 4 批写作，重点解决内容边界划分（6.1↔6.9 沙箱、6.8↔2.5 安全），每批完成后站会同步 | 15 篇文章初稿 | 各角色按分工 |
| **评审** | 安全体系交叉审查（6.8 与 2.5 不重复）、MCP 技术深度审查、性能数据真实性审查 | 评审报告、边界检查记录 | 安全架构师 + 后端架构师 |
| **验证** | 所有配置示例格式验证、Mermaid 安全图/架构图渲染验证、跨章节引用准确性、200 行门槛 | 验证报告 | 测试工程师 |
| **交付** | 分批合并（P0 优先）、更新 _sidebar.md 确认 12 条路径、同步 PRD 第 3.5 节版本号 | 合入确认、版本同步 | 敏捷教练 |

### 评审要求

**检查点 1：内容边界划分（P0 — 第二轮 Review 阻塞项）**
- Article 6.1（MCP 服务器）与 Article 6.9（沙箱与 Hook）的沙箱内容职责划分清晰：6.1 只写 MCP 进程隔离，6.9 写通用沙箱机制
- Article 6.8（安全总览）与 Article 2.5（约束系统）的职责划分：6.8 写宏观安全视图（6 权限模型+YOLO+注入防御），2.5 写微观权限配置
- Article 6.8 与 Article 6.9 的协作关系：6.8 定义安全策略，6.9 实现执行层

**检查点 2：技术深度一致性**
- MCP 三种传输类型（stdio/SSE/WebSocket）的安全风险对比必须包含 STRIDE 表
- 三级缓存架构（Session内/跨Session/持久化）的实现说明与 OpenCode v1.15.x 实际 API 一致
- 沙箱系统 Seatbelt/Bubblewrap 的配置策略与实际平台能力一致

**检查点 3：跨文章引用一致性**
- 上下文压缩（6.4）→ Token 预算（6.5）→ 提示词缓存（6.6）→ 记忆系统（6.7）的依赖链引用正确
- 安全总览（6.8）→ 沙箱 Hook（6.9）→ CLAUDE.md（6.10）的安全递进关系清晰

### 质量验收要求

| 门禁类型 | 验收项 | 通过标准 |
|---------|--------|---------|
| 🔴 硬性 | 每篇文章有效行数 | ≥ 200 行（Article 6.2/6.6/6.8/6.9 ≥ 250 行） |
| 🔴 硬性 | Mermaid 渲染正确率 | 100%（12+ 张图表，章节规模最大） |
| 🔴 硬性 | 内容边界划分 | 6.1↔6.9、6.8↔2.5 职责划分文档化 |
| 🔴 硬性 | 威胁建模覆盖 | ≥ 4 篇文章包含 STRIDE 表（6.1/6.8/6.9/7.5） |
| 🟡 质量 | 配置示例标注 | 所有示例标注最低 OpenCode/OMO 版本 |
| 🟡 质量 | 安全体系完整性 | 权限/Sandbox/Hook/注入防御 4 层全覆盖 |
| 🟡 质量 | 跨文章引用准确 | 无死链、无循环引用 |
| 📊 量化 | Mermaid 图表 | ≥ 12 张 |
| 📊 量化 | 代码/配置示例 | ≥ 15 个 |
| 📊 量化 | 监控仪表板图 | ≥ 1 张（Article 6.11） |

### 特殊内容技能映射

| 特殊内容 | 所需技能 | 适用文章 | 说明 |
|---------|---------|---------|------|
| MCP 集成架构图 | `architecture` | Article 6.1 | ToolRegistry→MCP Client→MCP Servers |
| 三种传输方式对比图 | `infographic` | Article 6.1 | stdio/SSE/WebSocket 对比 |
| Plugin Pipeline 执行流程图 | `bpmn` | Article 6.2 | Hook 链执行流程 |
| Hook 点事件时间线图 | `uml` (时序图) | Article 6.2 | 事件生命周期 |
| 成本管控三层模型图 | `architecture` | Article 6.3 | 模型选择→Token→压缩 |
| Compaction 触发流程图 | `uml` | Article 6.4 | 压缩决策流程 |
| 三级缓存架构图 | `architecture` | Article 6.6 | 三级缓存层级 |
| Memdir 架构图 | `architecture` | Article 6.7 | 记忆目录结构 |
| 四层安全架构图 | `security` | Article 6.8 | 权限→分类→隔离→防御 |
| YOLO 分类决策流程图 | `bpmn` | Article 6.8 | 高/中/低风险分类 |
| 提示注入攻击树图 | `graphviz` | Article 6.8 | 攻击树分析 |
| 沙箱架构隔离图 | `security` / `architecture` | Article 6.9 | Seatbelt/Bubblewrap 隔离 |
| CLAUDE.md 覆盖层架构图 | `architecture` | Article 6.10 | 指令覆盖层级 |
| @include 指令加载流程图 | `uml` | Article 6.10 | 加载流程 |
| 5 层遥测架构图 | `architecture` | Article 6.11 | Agent→Session→Tool→Network→System |
| 监控面板布局图 | `infographic` | Article 6.11 | Dashboard 布局 |
| Feature Flag 分类雷达图 | `chart-visualization` / `vega` | Article 6.12 | 多维度分类 |
