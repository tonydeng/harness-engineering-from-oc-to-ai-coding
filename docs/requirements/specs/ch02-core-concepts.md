# Ch2: 核心概念

## 概述

本章是全书的知识基础，系统讲解OpenCode的6大核心概念：Agent（执行主体）、Skill（专业技能包）、Command（快捷指令）、Plugin（扩展能力）、Team（多Agent协作）、MCP（外部协议）。每个概念从"是什么→怎么用→最佳实践"三层递进，配合操作系统类比帮助读者建立直觉。本章也是后续所有章节的概念基础。

**章节核心主题**：理解6大核心概念的各自定位和协作关系，这是Harness Engineering的"积木箱"。

> **章节规模**：6 篇文章（3 现有 + 3 新增），2 篇修改

## 文章

### Article 2.1: Agent 系统
- **阅读时间**：20 min
- **学习目标**：
  - 理解OpenCode内置Agent类型：Build/Plan/General/Explore/Scout
  - 理解Primary Agent vs Subagent vs Hidden Agent的分层设计
  - 掌握Plan/Build双模式切换的实际用法
  - 了解OMO扩展的11+专业Agent体系
- **前置知识**：Ch1（了解Harness Engineering框架）
- **源材料映射**：OpenCode实战 01（核心概念速通-Agent部分）+ OpenCode实战 02（OMO Agent扩展）

#### 大纲
1. Agent的基本认知
   - 定义：Agent是AI任务的执行主体——"容器"（承载模型+工具+技能+记忆）
   - 操作系统类比：Agent = 进程
2. OpenCode内置Agent类型详解
   - Primary Agent：Build（读写执行）、Plan（只读分析）
   - Subagent：@general（通用任务）、@explore（代码探索）
   - Hidden Agent：compaction（上下文压缩）、title（会话命名）
3. Plan模式：Harness Engineering的安全机制
   - 什么是Plan模式（默认拒绝所有文件编辑和命令执行）
   - Plan模式的4个典型使用场景
   - Plan→Build两阶段工作流的工程价值
4. @ 子Agent调用
   - 语法：`@agent_name 任务描述`
   - 实战示例：`@explore 查找项目中所有API路由定义`
   - 子Agent的权限隔离
5. OMO Agent体系扩展
   - Sisyphus（总指挥官）、Prometheus（战略规划）、Atlas（任务指挥）
   - Hephaestus（深度工作）、Oracle（架构顾问）
   - 类别路由系统：按任务类型自动分派到最优Agent
6. Agent选择决策树

#### 核心概念
- **Plan模式是设计哲学**：OpenCode的Plan模式不仅是一个功能，更体现了"先思考后执行"的工程原则。这与Harness Engineering的"可审计"原则直接呼应。
- **Primary vs Subagent的权限差异**：Subagent默认不能编辑文件，这是安全设计——让"思考者"无法碰代码。
- **类别路由的设计意图**：按任务复杂度自动选用不同模型，本质是成本管控 + 质量平衡。

#### 代码/配置示例
- Plan模式拒绝示例（edit/bash被拒的输出）
- @general 和 @explore 调用示例
- OMO类别路由配置示例

#### Mermaid 图表
- OpenCode官方意图推理流程图（Agentic Loop）
- Agent选择决策树
- 类别路由映射图

#### 关联章节
- → Article 2.3（Agent + Command + Profile联动）
- ← Article 1.1（承接"为什么需要Harness Engineering"）
- → Ch4（Agent编排是工作流的核心）

### 团队角色评审补充
- **架构顾问需求**：Article 2.1 开头增加OpenCode整体分层架构图（CLI层→Agent层→Tool层→Provider层→扩展层）；补充Agent信任边界图（Primary与Subagent之间的数据隔离模型）。
- **安全架构师需求**：Article 2.1 补充Plan模式作为安全前置审查机制的说明；Article 2.2 allowed-tools的安全含义——"权限边界就是攻击面"。
- **前端架构师需求**：Article 2.2 增加"组件↔Skill"系统类比（Props=frontmatter, Composition=编排, 单一职责相互印证）。
- **后端架构师需求**：Article 2.3 AGENTS.md模板增加后端专用部分（API路径约定、请求/响应格式、分页规范、错误码约定）。
- **渗透测试员需求**：Article 2.1 补充Prompt注入风险说明——Agent如何被注入恶意指令导致横向移动。

---

### Article 2.2: Skill 系统
- **阅读时间**：20 min
- **学习目标**：
  - 理解SKILL.md的完整格式规范（frontmatter + 正文）
  - 理解Skill的发现路径（项目→用户→内置）
  - 理解Skill的加载机制（description语义匹配，按需加载）
  - 掌握Skill的权限控制（allow/ask/deny三级）
  - 了解OMO扩展：Skills Marketplace、Scoped Skills、Overrides
- **前置知识**：Article 2.1（理解Agent是Skill的宿主）
- **源材料映射**：OpenCode实战 01（Skill部分，OS类比+格式+发现路径+加载机制）+ OpenCode实战 04（Skill做DSL）+ OpenCode实战 02（OMO Skills Marketplace）

#### 大纲
1. Skill的本质
   - 定义：结构化指令包（结构化Prompt + 工具绑定 + 权限控制）
   - 操作系统类比：Skill = 驱动程序
   - Skill vs 普通Prompt的核心差异：权限控制、工具绑定、元数据索引
2. SKILL.md完整格式
   - frontmatter字段详解：name, description, license, metadata, allowed-tools, target_agent
   - 正文结构：工作流 + 指令 + 输出规范
   - 捆绑资源：scripts/ + templates/
3. Skill的发现与加载
   - 搜索路径：项目级 → 用户级 → 内置
   - 加载机制：只读description → 匹配后加载正文 → 需要时读捆绑资源（渐进式披露）
   - 语义匹配示例
4. 权限控制
   - 三级策略：allow（自动）/ ask（询问）/ deny（禁止）
   - 在opencode.json中配置Skill权限
   - allowed-tools 字段控制工具访问
5. OMO扩展
   - Skills Marketplace：社区共享、版本管理、一键安装
   - Scoped Skills（v4.3+）：target_agent限定Agent可见性
   - Skill Overrides：在OMO配置中覆盖SKILL.md字段
6. Skill使用最佳实践

#### 核心概念
- **描述匹配的设计权衡**：语义匹配降低了用户认知负荷（不需要记名字），但可能导致不精确触发。解决方法是编写精准的描述。
- **Scoped Skills的意义**：对Skill开发者而言是权限隔离，对Agent编排而言是专业化分工的基础。
- **Skill vs Plugin**：Skill是"教Agent怎么做"（指令层），Plugin是"改Agent能做什么"（能力层）。

#### 代码/配置示例
- 完整SKILL.md示例（frontmatter + 正文）
- 三级权限配置示例
- OMO Skills Marketplace发现和安装流程

#### Mermaid 图表
- Skill加载流程图（用户输入 → 描述匹配 → 权限检查 → 加载正文）
- Skill搜索路径流程图

#### 关联章节
- ← Article 2.1（Skill是Agent加载的）
- → Article 5.2（Skill模板的实操）
- → Article 4.3（Skill在Team模式中的作用域）

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 完整解释SKILL.md的所有关键字段
- [ ] 包含匹配机制的图文说明
- [ ] 包含权限控制示例

---

### Article 2.3: 工作流模式
- **阅读时间**：20 min
- **学习目标**：
  - 理解Command系统的设计：内置命令 + 自定义命令 + 模板语法
  - 掌握Profile切换管理不同工作状态
  - 理解AGENTS.md在工程化中的核心地位
  - 了解OMO引入的高级工作流模式：Ultrawork vs Prometheus
- **前置知识**：Article 2.1（Agent基础）+ Article 2.2（Skill概念）
- **源材料映射**：OpenCode实战 01（Command部分）+ OpenCode实战 04（Profile切换、AGENTS.md、团队共享命令）+ OpenCode实战 02（OMO Ultrawork/Prometheus）

#### 大纲
1. Command系统
   - 内置命令一览（/init, /connect, /undo, /diff, /share, /plan, /models, /help）
   - 自定义命令的两种方式（Markdown文件推荐 vs opencode.json配置）
   - 模板语法：$ARGUMENTS, !shell输出, @file引用
   - 高级特性：指定Agent、指定模型、子命令
   - 团队共享命令库
2. Profile切换
   - 痛点：写代码、Code Review、Debug需要不同的行为偏好
   - 三套Profile示例（dev/review/debug）
   - Profile继承机制（$extends）
   - 命令行选择Profile
3. AGENTS.md：项目知识库
   - /init生成AGENTS.md的机制
   - AGENTS.md的金字塔结构：项目概述 → 技术栈 → 目录 → 命令 → 规范 → 约束
   - 提交AGENTS.md到Git：持久化项目知识
   - AGENTS.md作为团队开发规范载体（Workflow as Code）
4. OMO高级工作流模式
   - Ultrawork模式（"懒得想"模式）：自动探索→研究→实现→验证循环
   - Prometheus模式（"精准执行"模式）：访谈式规划→生成计划→/start-work执行
   - 决策树：什么时候用什么模式
5. Ralph Loop（/ulw-loop）：自我迭代直到完成

#### 核心概念
- **Command的工程价值**：将重复操作封装为/command，本质是"将个人经验固化为团队共有资产"——Harness Engineering的核心实践之一。
- **AGENTS.md是团队契约**：不是可选的辅助文件，而是团队开发规范的代码化形式。
- **Ultrawork vs Prometheus**：前者是"Agent自主探索"，后者是"人工引导的精准执行"——两种模式对应不同场景。

#### 代码/配置示例
- 自定义命令Markdown文件示例
- JSON格式命令配置示例
- 三套Profile配置示例
- AGENTS.md模板示例
- Ultrawork/Prometheus配置示例

#### Mermaid 图表
- AGENTS.md金字塔结构图
- Ultrawork vs Prometheus决策树
- Profile切换的时间线示意图

#### 关联章节
- ← Article 2.1（Command调用Agent）
- ← Article 2.2（Command可指定Skill）
- → Ch4（工作流模式在Ch4中深入展开）
- → Ch5（自定义命令需要维护，与Skill同理）

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 覆盖所有内置命令
- [ ] 提供至少2种自定义命令方式示例
- [ ] 包含AGENTS.md完整模板
- [ ] 包含Ultrawork vs Prometheus的决策树

---

## 章节重构增补

### 修改标注（基于章节重构计划）

**Article 2.1（Agent 编排）**：
- 增加马书 Agent Loop 状态机视角的对比
- 补充 OpenCode Agentic Loop 与马书框架的异同分析

**Article 2.3（工作流模式）**：
- 增加马书 6 种工作流模式引用
- 补充马书工作流与 OpenCode 工作流的映射关系

---

### Article 2.4: 上下文工程核心
- **阅读时间**：20 min
- **学习目标**：
  - 理解上下文工程作为核心概念的定义和边界
  - 掌握上下文压缩、缓存、Token 预算的基本原理
  - 理解上下文工程与 Agent 性能的直接关系
- **前置知识**：Ch1（Harness Engineering 理论框架）
- **源材料映射**：马书第3-4篇，HE实践 03 §实践一

#### 大纲
1. 上下文工程的定义
   - 为什么需要上下文工程——Token 空间有限，信息无限
   - 上下文工程的 3 个维度：压缩、缓存、预算
2. 上下文压缩原理
   - 自动压缩机制（Compaction）
   - 微压缩策略（选择性保留）
   - 压缩后恢复和保真度
3. 上下文缓存策略
   - Session 级缓存 vs 跨 Session 缓存
   - 缓存命中率和 Token 节省
4. Token 预算管理
   - 预算是如何分配的（系统/用户/工具输出）
   - 预算超限的处理机制
5. 上下文工程在 Harness Engineering 中的位置
   - 与约束系统、验证护栏的关系

#### 核心概念
- **上下文是 AI Agent 的"工作记忆"**：就像人的工作记忆有限，Agent 的上下文窗口也有限。上下文工程就是管理这个有限空间的方法论。
- **三层上下文管理**：压缩（缩减信息量）→ 缓存（重用已有信息） → 预算（分配有限空间）

#### 代码/配置示例
- Compaction 配置示例
- 上下文预算分配配置

#### Mermaid 图表
- 上下文工程三层模型图
- 压缩/缓存/预算的决策流程图

#### 关联章节
- → Article 2.5（约束系统是上下文工程的安全补充）
- → Article 2.6（验证护栏与上下文的交互）
- → Ch6（上下文工程的深入实现）

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 包含上下文工程的三层模型完整解释
- [ ] 包含至少 2 个配置示例

---

### Article 2.5: 约束系统
- **阅读时间**：15 min
- **学习目标**：
  - 理解约束系统的构成要素
  - 掌握权限模型、架构护栏、lint 规则这三大支柱
  - 理解约束系统在工程化中的作用
- **前置知识**：Article 2.4（上下文工程）
- **源材料映射**：马书第5篇（权限），HE实践 03 §实践二

#### 大纲
1. 约束系统总览
   - Agent 需要"牢笼"——没有约束就没有可控性
   - 三大支柱：权限 → 架构 → 编码规范
2. 权限模型
   - 6 种权限模式概览
   - allow/deny/ask 三级策略
   - 工具级与文件级的权限控制
3. 架构护栏
   - 什么是架构护栏（约束 Agent 的架构决策）
   - AGENTS.md 作为架构护栏的实现
   - 实战：规范 Service/Repository 层生成规则
4. Lint 规则约束
   - 利用 LSP 和 AST-grep 约束 Agent 输出
   - Code Review 作为人工约束
5. 约束系统的权衡——太松 vs 太紧

#### 核心概念
- **Agent 的"牢笼"设计哲学**：约束不是限制，而是让 Agent 在安全范围内自由发挥。好的约束系统让 Agent 更高效，而不是更慢。
- **三层约束的职责分离**：权限（能不能做）→ 架构（怎么做）→ 规范（做得对）

#### 代码/配置示例
- 权限规则配置示例（allow/deny/ask + glob 匹配）
- AGENTS.md 架构护栏示例
- Lint 规则配置示例

#### Mermaid 图表
- 约束系统三大支柱架构图
- 权限 → 架构 → 规范的金字塔图

> ⚠️ 写作时需包含威胁建模分析：分析攻击者试图绕过约束的典型场景（如越权访问、配置篡改、权限升级），说明约束系统如何防御这些攻击。

#### 关联章节
- ← Article 2.4（上下文工程是约束的前提）
- → Article 2.6（验证护栏是约束的补充）
- → Ch3 §3.2（配置中的权限模型实现）

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 覆盖三大支柱的完整解释
- [ ] 包含权限规则配置示例

---

### Article 2.6: 验证护栏
- **阅读时间**：15 min
- **学习目标**：
  - 理解验证护栏在 AI 编程流水线中的角色
  - 掌握质量门禁的设计模式
  - 理解 YOLO 分类和自动验证机制
- **前置知识**：Article 2.5（约束系统）
- **源材料映射**：马书第17章，HE实践 03 §实践三

#### 大纲
1. 验证护栏的定义
   - 与约束系统的区别：约束管"准入"，验证管"准出"
   - 验证在 Harness Engineering 中的 3 个原则
2. 质量门禁体系
   - 门禁分级：硬性/质量/量化
   - 门禁的阻断和告警模式
   - 门禁的 CI/CD 集成
3. YOLO 分类器
   - 高风险（阻止执行）/ 中风险（确认后执行）/ 低风险（自动执行）
   - 分类依据和训练
   - 自定义分类规则
4. 自动验证机制
   - LSP 验证链
   - 测试自动执行
   - 架构符合性检查

#### 核心概念
- **验证护栏是"最后一道防线"**：约束系统确保 Agent 不做不该做的事，验证护栏确保 Agent 做的事情是正确的。
- **YOLO 分类是工程化的核心实践**：将风险量化并自动化处理，是"可审计"原则的具体实现。

#### 代码/配置示例
- 质量门禁配置示例
- YOLO 分类规则定义
- 自动验证流水线配置

#### Mermaid 图表
- 验证护栏 vs 约束系统的对比图
- YOLO 分类决策流程图
- 质量门禁流水线图

> ⚠️ 写作时需包含威胁建模分析：分析验证护栏的绕过威胁，包括攻击者如何利用 YOLO 分类器误判绕过门禁，以及门禁报文的伪造风险。

#### 关联章节
- ← Article 2.5（约束系统前置）
- → Ch5（Skill 验证的最佳实践）
- → Ch7（案例中的质量门禁应用）

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 包含 YOLO 分类器的完整解释
- [ ] 包含质量门禁配置示例

---

## 团队协作工作流

### 团队分工

| 角色 | 职责 | 负责文章 |
|------|------|---------|
| **架构顾问**（SYSA） | OpenCode 分层架构图、Agent 信任边界图、约束系统三大支柱、马书 Agent Loop 对比 | Article 2.1, Article 2.5, Article 2.1(修改) |
| **后端架构师**（BACKEND） | 上下文工程核心概念、AGENTS.md 后端专用模板、Token 预算机制 | Article 2.4, Article 2.3 |
| **前端架构师**（FRONTEND） | 组件↔Skill 系统类比、Skill 搜索路径可视化、验证护栏前端场景 | Article 2.2, Article 2.6 |
| **安全架构师**（SECURITY） | Plan 模式安全审查机制、allowed-tools 安全含义、约束系统威胁建模 | Article 2.1(补充), Article 2.5(威胁建模) |
| **渗透测试员**（REDTEAM） | Prompt 注入风险说明（Article 2.1）、约束绕过场景（Article 2.5）、验证护栏绕过分析（Article 2.6） | Article 2.1, Article 2.5, Article 2.6 |
| **UI设计师**（UX） | 六篇 Mermaid 图统一配色、Alt 文本规范 | 全文图表 |

### 流程规范（Superpowers 工作流映射）

| 阶段 | 本阶段活动 | 交付物 | 负责人 |
|------|-----------|--------|--------|
| **头脑风暴** | 确定 6 个核心概念的读者理解难点、收集马书引用材料、识别安全/架构增强点 | 概念难点清单、增强需求 | 架构顾问 |
| **计划** | 排序写作依赖（2.1→2.2→2.3→2.4→2.5→2.6）、分配角色、确定马书引用范围 | 写作计划、引用清单 | 敏捷教练 |
| **实施** | 3 篇现有文章修改 + 3 篇新增文章写作，每篇包含 OS 类比+概念+示例+图表 | 6 篇文章初稿 | 各角色按分工 |
| **评审** | 概念一致性审查（跨 6 篇文章的术语统一）、安全审查（Article 2.5/2.6 威胁建模）、架构审查（Article 2.1 分层图） | 评审报告 | 架构顾问 + 安全架构师 |
| **验证** | Mermaid 复杂度验证（Article 2.1 决策树/路由图）、概念依赖链验证、所有配置示例可运行 | 验证报告 | 测试工程师 |
| **交付** | 合并、更新侧边栏（确认 2.4-2.6 新增路径正确）、同步版本号 | 合入确认 | 敏捷教练 |

### 评审要求

**检查点 1：概念依赖链一致性**
- Article 2.1（Agent）→ Article 2.2（Skill 加载于 Agent）→ Article 2.3（Command/Profile 与 Agent 联动）
- Article 2.4（上下文工程）→ Article 2.5（约束系统）→ Article 2.6（验证护栏）
- 跨篇术语统一（如 Agent Loop 在 2.1 和 2.3 中定义一致）

**检查点 2：安全视角完整性**
- Article 2.1 包含 Prompt 注入风险说明
- Article 2.5 包含约束绕过场景和防御建议（渗透测试员视角）
- Article 2.6 包含 YOLO 分类器绕过分析
- 威胁建模分析使用 STRIDE 方法

**检查点 3：架构图准确性**
- OpenCode 分层架构图（CLI→Agent→Tool→Provider→扩展层）必须准确反映 v1.15.x 架构
- Agent 信任边界图标注 Primary vs Subagent 数据隔离

### 质量验收要求

| 门禁类型 | 验收项 | 通过标准 |
|---------|--------|---------|
| 🔴 硬性 | 每篇文章有效行数 | ≥ 200 行 |
| 🔴 硬性 | Mermaid 渲染正确率 | 100%（6+ 张图表） |
| 🔴 硬性 | OS 类比覆盖度 | ≥ 5/6 篇文章包含 OS 类比 |
| 🟡 质量 | 配置示例可运行性 | 所有示例标注最低版本 |
| 🟡 质量 | 威胁建模覆盖 | Article 2.5 + 2.6 各至少 1 个 STRIDE 表 |
| 🟡 质量 | 跨章节引用 | 所有 → 引用指向真实标题 |
| 📊 量化 | 概念关系图 | ≥ 1 张概念联动图 |
| 📊 量化 | 代码/配置示例 | ≥ 8 个 |

### 特殊内容技能映射

| 特殊内容 | 所需技能 | 适用文章 | 说明 |
|---------|---------|---------|------|
| OpenCode 分层架构图 | `architecture` | Article 2.1 | 5 层架构（CLI→Agent→Tool→Provider→扩展） |
| Agent 选择决策树 | `mindmap` / `uml` | Article 2.1 | 决策流程图 |
| 类别路由映射图 | `architecture` / `graphviz` | Article 2.1 | 任务→类别的路由映射 |
| Skill 加载流程图 | `bpmn` / `uml` | Article 2.2 | 渐进式披露流程 |
| AGENTS.md 金字塔结构图 | `architecture` | Article 2.3 | 层级结构 |
| Ultrawork vs Prometheus 决策树 | `mindmap` | Article 2.3 | 对比决策树 |
| 上下文工程三层模型图 | `architecture` | Article 2.4 | 压缩→缓存→预算三层 |
| 约束系统三大支柱架构图 | `architecture` | Article 2.5 | 权限→架构→规范 |
| 验证护栏 vs 约束系统对比图 | `infographic` | Article 2.6 | 对比图 |
| YOLO 分类决策流程图 | `bpmn` | Article 2.6 | 风险分类流程 |
