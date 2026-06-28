# 产品需求文档 (PRD)

## 1. 项目背景

### 1.1 行业背景

AI 编程工具这些年进化很快。2021 年有 Copilot 帮你补全代码，2024-2025 年 Cursor 和 Claude Code 能跟你对话写代码，到 2026 年 OpenCode 这类 Agent 工具已经能编排复杂的开发任务。但大多数人还是把它们当"聊天工具"在用——问一句答一句，没形成稳定的工作方式。

OpenCode 是 GitHub 上最热门的开源 AI 编程 Agent 项目（167K+ Star），但市面上缺少一本系统化的实践指南告诉你该怎么用好它。大多数用户只用到了它 10% 的能力。

### 1.2 问题定义

- **学习曲线陡峭**：6 个核心概念（Agent/Skill/Command/Plugin/Team/MCP）联动方式复杂，4 个附录覆盖 OpenCode/Claude Code/Pi Agent 完整生态全景
- **信息碎片化**：官方文档涵盖基础功能，但缺乏实战导向的完整教程
- **最佳实践缺失**：社区虽有大量使用技巧，但未经系统整理和验证
- **团队推广困难**：缺乏可复用的工程化方法论和模板

### 1.3 项目定位

本书是一本**开源书籍**，面向想系统化掌握 OpenCode 生态（oh-my-openagent / MCP / Skills）的开发者。核心理念是**从"跟 AI 聊天写代码"到"用工程体系做开发"**。

## 2. 项目目标

### 2.1 核心目标

- **体系化学习**：全书共 Ch0 + 7 章 + 附录 A/B/C/D，60+ 篇文章（实际 88 个 .md 文件），从核心概念到高级话题逐步深入
- **即学即用**：每章都有概念讲解、可直接运行的配置示例，以及来自真实项目的经验总结
- **拿来就能改**：配套的配置模板、Skill 代码、工作流示例都在 `examples/` 目录下，你可以直接复制到自己的项目里用
- **持续更新**：标注了对应的 OpenCode 版本号，重大版本更新后 2 周内刷新对应章节。社区通过 PR 和 Issue 协作维护

### 2.2 量化目标

| 指标 | 目标值 | 衡量方式 |
|------|--------|---------|
| 内容完整度 | 60+ 篇文章全部有完整内容（实际 88 个 .md 文件；附录 B/C/D 部分文章篇幅较短，2-7KB） | 文件数量统计 |
| 代码示例 | 100+ 个可运行的代码/配置示例 | 代码块统计 |
| 图表数量 | 50+ 张 Mermaid/架构图 | 图表数量统计 |
| 内容质量 | 每篇文章 > 200 行有效内容（附录 B/C/D ≥ 200 行基线） | 文件行数统计 |
| 总有效行数 | ≥ 50,000 行（实际 ~88 个 .md 文件，全量 ~51,000+ 行） | 文件行数统计 |
| 版本同步 | 在 OpenCode 重要版本发布后 2 周内更新 | 版本追踪 |
| PRD→交付时间 | 从内容规划到全部完成 ≤ 42 个工作日 | 里程碑追踪 |

## 3. 内容架构

### 3.1 书籍结构

```
Ch0: 读者导航（读者决策页 + 阅读路径 + 快速体验）
  ├── README （角色自诊 → 推荐路线 → 预期收获 → 跳过指南）
  ├── reading-paths（14 角色阅读路径推荐 + 全局依赖图）
  ├── how-to-read（2 种阅读方式：线性通读 / 按角色跳读）
  └── quick-start（5 分钟快速体验：安装 → 配置 → 第一个操作）

第1章: 简介 (6 篇文章)
  ├── 什么是 Harness Engineer（增补 Mitchell Hashimoto 原始定义 + Harrison Chase 公式）
  ├── 为什么选择 OpenCode（增补 OMO v4.5+ 特性）
  ├── harness-engineering-theory（理论框架、5大分类法、演进时间线 2024→2026）
  ├── ecosystem-comparison（OpenCode vs Cursor vs Claude Code vs Codex vs Cline vs Windsurf）
  ├── chinese-ecosystem（国产方案全景：Trae、CodeGeeX、通义灵码、文心快码）
  └── failure-cases（AI 编程失败案例：约束系统缺失、上下文注入攻击、权限配置错误）

第2章: 核心概念 (6 篇文章)
  ├── Agent 编排（增补《马书》第4章 Agent Loop 状态机视角）
  ├── Skill 系统
  ├── 工作流模式（增补《马书》第6章 6 种工作流模式引用）
  ├── context-engineering-core（上下文工程：压缩、缓存、Token预算）
  ├── constraints-system（约束系统：权限模型、架构护栏、lint规则）
  └── validation-harness（验证护栏：质量门禁、YOLO分类、自动验证）

第3章: 环境搭建 (5 篇文章)
  ├── 快速上手
  ├── OpenCode 配置详解（增补 Category 路由 + OMO v4.5+ 新配置项）
  ├── oh-my-openagent 集成（增补 OMO 11+ Agent 注册表引用）
  ├── chinese-providers（国产模型配置：DeepSeek/Kimi/Qwen）
  └── multi-env-setup（多环境配置：本地dev/CI/生产、Profile切换）

第4章: 工作流实战 (6 篇文章)
  ├── Ultrawork 模式（增补 Ralph Loop /ulw-loop 机制详解）
  ├── Prometheus 规划模式（访谈式需求收集 + Atlas 执行指挥官）
  ├── 多 Agent 协作（增补 Hyperplan 5批评者规划 + security-research模式）
  ├── 自定义工作流
  ├── agent-derivation（Agent 派生模式：子Agent、委派、协调者）
  └── teams-collaboration（多进程协作：Teams 架构、消息传递、进程内集群）

第5章: Skill 开发 (5 篇文章)
  ├── 创建 Skill
  ├── Skill 模板（含安全审计模板、UI审查模板）
  ├── 最佳实践
  ├── skill-mcp-bridge（Skill 作为 MCP 桥接层）
  └── plugin-patterns（Skill 插件化：独立 → 市场 → 组合）

第6章: 高级话题 (12 篇文章)
  ├── MCP 服务器（扩展：stdio/SSE/WebSocket、ToolRegistry、沙箱）
  ├── 自定义 Agent（增补三种Agent派生模式 + Effort/Fast Mode/Thinking）
  ├── 性能调优（增补模型降级链、成本优化、Token预算策略）
  ├── context-compression（自动压缩 + 微压缩 + 压缩后恢复）[P0]
  ├── token-budget（Token预算策略、估算规则、预算分配）[P0]
  ├── prompt-caching（三级缓存架构、缓存断点、7+优化模式）[P0]
  ├── memory-system（跨会话记忆：Memdir架构、Auto-Dream、Compaction）[P0]
  ├── security-overview（安全总览：6权限模式、YOLO分类器、注入防御）[P0]
  ├── sandbox-hooks（沙箱系统 + 53+ Hook点）[P0]
  ├── agents-dot-md（AGENTS.md 项目指令系统 + CLAUDE.md 兼容）[P0]
  ├── observability（可观测性：logEvent、5层遥测架构）[P0]
  └── feature-flags（89个 Feature Flag 路线图）[P2]

第7章: 案例研究 (6 篇文章)
  ├── 案例一：从零搭建微服务（增补 Martin Fowler Harness Template 对照）
  ├── 案例二：遗留系统现代化（增补灰度策略 + 增量演进）
  ├── case-security-audit（安全审计流水线：红队+蓝队全流程）[P1]
  ├── case-full-pipeline（需求→PR 全流程自动化）[P1]
  ├── case-multi-model（国产模型+OpenCode 混合架构）[P1]
   └── case-skills-marketplace（团队级 Skill 市场建设）[P2]

附录A: 术语表与参考资料 (2 篇文章)
   ├── glossary（术语表）
   └── references（参考资料）

附录B: OpenCode 内置能力与生态 (7 篇文章)
   ├── capabilities（OpenCode 内置能力清单）
   ├── commands（内置命令参考）
   ├── plugins（Plugin 系统）
   ├── agent-architecture（Agent 架构）
   ├── sdk（SDK 参考）
   ├── agent-sdk（Agent SDK 编程）
   └── ecosystem（生态参考）

附录C: Claude Code 内置能力与生态 (8 篇文章)
   ├── capabilities（Claude Code 内置能力清单）
   ├── commands（命令参考）
   ├── plugins（扩展机制）
   ├── sdk（SDK 参考）
   ├── agent-sdk（Agent SDK 编程）
   ├── agent-architecture（Agent 设计指南）
   └── ecosystem（生态参考）

附录D: Pi Agent (5 篇文章)
   ├── overview（Pi Agent 概述与核心概念）
   ├── commands（CLI 命令与交互模式参考）
   ├── customization（扩展体系详解）
   ├── sdk（SDK 参考）
   └── ecosystem（生态与集成场景）
```

### 3.2 内容来源映射

> **源材料说明**：《驾驭工程：从 Claude Code 源码到 AI 编码最佳实践》（中文别名：《马书》）是一本 Engineering（驾驭工程）的中文技术书。它以 Claude Code `v2.1.88` 的公开发布包与 source map 还原结果为分析材料，从真实工程实现中提炼 AI 编码 Agent 的架构模式、上下文策略、权限体系和生产实践。在线阅读：https://zhanghandong.github.io/harness-engineering-from-cc-to-ai-coding/

| 书本章节 | 来源 | 来源描述 | 内容比例 |
|---------|------|---------|---------|
| Ch1 简介 | OpenCode实战 01 + 04 | 核心概念速通 + 工作台方案 | 部分引用 |
| Ch2 核心概念 | OpenCode实战 01 | 核心概念速通（1051行） | 主要来源 |
| Ch3 环境搭建 | OpenCode实战 02 | 架构全景解析（1541+行） | 主要来源 |
| Ch4 工作流 | OpenCode实战 03 | 概念联动实战（1365行） | 主要来源 |
| Ch5 Skill 开发 | OpenCode实战 04 | 奇淫技巧（1292行） | 主要来源 |
| Ch6 高级话题 | OpenCode实战 02 + 互联网搜索 | 架构 + MCP 协议资料 | 混合来源 |
| Ch7 案例研究 | OpenCode实战 05 | 场景化案例（994行） | 主要来源 |
| 附录A 术语表 | 全书汇总 | 全书术语统一整理 | 衍生来源 |
| 附录B OpenCode 能力 | OpenCode 官方文档 + 源码 | OpenCode 内置能力、命令、Plugin、SDK | 衍生来源 |
| 附录C Claude Code 能力 | Claude Code 官方文档 + 源码 | Claude Code 内置能力、命令、扩展、SDK | 衍生来源 |
| 附录D Pi Agent | Pi Agent 官方文档 + 源码 | Pi Agent 概述、命令、扩展、SDK | 衍生来源 |

### 3.3 核心概念覆盖

本书必须覆盖以下 OpenCode 6 大核心概念及其联动模式，并通过 4 个附录系统化覆盖 OpenCode/Claude Code/Pi Agent 的完整生态能力：

| 概念 | 需要覆盖的内容 | 涉及章节 |
|------|--------------|---------|
| Agent | Build/Plan/General/Explore/Scout 类型、Primary/Subagent 区别、自定义 Agent | Ch2, Ch3, Ch6 |
| Skill | SKILL.md 格式、加载机制、作用域技能、Skills Marketplace | Ch2, Ch5 |
| Command | 内置命令、自定义命令、模板语法、团队共享命令库 | Ch2, Ch4 |
| Plugin | 事件 Hook、自定义工具、覆盖内置行为 | Ch6 |
| Team | 多 Agent 编排、Team Mode（v4.0+）、Hyperplan | Ch4, Ch6 |
| MCP | 协议概念、本地/远程配置、OAuth 认证、工具集成 | Ch6 |

此外，附录 B/C/D 分别覆盖：

| 附录 | 覆盖内容 |
|------|---------|
| 附录B OpenCode 内置能力 | OpenCode 内置能力参考、命令大全、Plugin 系统、Agent 架构、SDK 编程指南、生态集成参考（7 篇文章） |
| 附录C Claude Code 内置能力 | Claude Code 内置能力参考、命令大全、扩展机制、Agent 架构设计、SDK 编程指南、生态集成参考（8 篇文章） |
| 附录D Pi Agent | Pi Agent 概述与核心概念、CLI 命令参考、扩展体系、SDK 编程、生态与集成场景（5 篇文章） |

### 3.4 必须包含的 OMO 特性

| OMO 特性 | 版本要求 | 覆盖章节 |
|----------|---------|---------|
| 类别路由系统 | v4.0+ | Ch2, Ch3 |
| Ultrawork 模式 | v4.0+ | Ch4 |
| Prometheus 规划模式 | v4.0+ | Ch4 |
| Team Mode (12 个 team_* 工具) | v4.0+ | Ch4, Ch6 |
| Hyperplan 技能 | v4.0+ | Ch4, Ch5 |
| Security-research 技能 | v4.4+ | Ch5, Ch7 |
| 作用域技能 (Scoped Skills) | v4.3+ | Ch5 |
| Hashline 编辑 | v4.2+ | Ch6 |
| Ralph Loop (ulw-loop) | v4.0+ | Ch4 |
| 54+ Hook 点 | v4.0+ | Ch6 |
| Skill-embedded MCPs | v4.0+ | Ch5, Ch6 |

### 3.5 版本要求

- OpenCode: v1.16.x（基于 2026-06 最新稳定版）
- oh-my-openagent: v4.13.x（基于 2026-06 最新版本）
- 书中标注版本号，以便读者识别过时内容
- 重大版本更新后 2 周内更新对应章节

## 4. 技术规格

### 4.1 平台要求

- **渲染引擎**：mdBook v0.4.x
- **部署平台**：GitHub Pages
- **源码格式**：Markdown + Mermaid 图表
- **本地预览**：`mdbook serve`
- **响应式设计**：支持桌面端和移动端阅读

#### 4.1.1 前端技术栈

| 组件 | 选型 | 说明 |
|------|------|------|
| 渲染引擎 | mdBook v0.4.x | Rust 编写的静态站点生成器 |
| 代码高亮 | mdBook 内置 | 基于 syntect，支持 200+ 语言 |
| 图表引擎 | mdbook-mermaid | Mermaid 预处理器 |
| 搜索 | mdBook 内置 | 全文搜索 |
| 页面导航 | mdBook 内置 | 上一章/下一章导航 |
| 主题 | mdBook 内置 | rust/ayu/coal/navy |
| 编辑链接 | mdBook 内置 | "在 GitHub 上编辑此页" |

#### 4.1.2 移动端体验要求

- 移动端 375px-414px 宽度无内容溢出
- 代码块在移动端可横向滚动
- Mermaid 图表在移动端自动缩放至屏幕宽度
- 侧边栏在移动端可正常折叠/展开
- 字体大小在移动端不低于 16px

#### 4.1.3 无障碍要求

- 页面标题层级规范：h1 → h2 → h3（不跳级）
- 所有 Mermaid 图表和图片需有 Alt 文本
- 字体颜色与背景对比度 ≥ 4.5:1
- 支持键盘导航（Tab 切换）

#### 4.1.4 性能要求

- 页面加载时间 ≤ 2s（GitHub Pages CDN）
- Mermaid 图表渲染后需人工检查布局和中文文本

### 4.2 内容格式规范

- 使用 YAML frontmatter 管理文档元数据（标题/作者/版本/阅读时间）
- 每章开头包含**价值声明块**：目标读者 / 前驱知识 / 学习收获 / 预计投入时间
- 代码块规范：
  - 标注语言标识（bash/json/yaml/typescript/python）
  - 首行为文件路径注释（如 `# opencode.json`）
  - 关键行使用行高亮（`// [!code highlight]`）
  - 占位符用 `<PLACEHOLDER>` 标注
- 架构图优先使用 Mermaid 语法，使用统一配色方案
- 中英文术语对照表附在附录，首次出现时标注英文
- 跨章节引用格式统一：`参见第 X 章「章节标题」`

### 4.3 配套资源

- `examples/` 目录：可运行的 OpenCode 配置示例
- `.opencode/skills/` 目录：示例 Skill 代码
- `.github/workflows/`：CI/CD 部署流水线
- `assets/`：图片和静态资源

## 5. 读者画像

### 5.1 核心读者角色

| 角色 | 标识 | 背景 | 目标 | 推荐阅读路径 | 预计占比 |
|------|------|------|------|------------|---------|
| 入门开发者 | BEGINNER | 刚接触 AI 编程，基本编程能力 OK | 快速上手 OpenCode，在日常开发中用起来 | Ch0 → Ch1 → Ch2 → Ch3 | 25% |
| 效率开发者 | POWER | 已用 AI 工具（Copilot/Cursor），想升级 | 掌握 Agent 编排，提升 2x+ 效率 | Ch0 → Ch2 → Ch4 → Ch6 | 20% |
| 技术负责人 | LEAD | 团队技术决策者，关注标准化 | 建立团队级的 AI 编程工程体系 | Ch0 → Ch1 → Ch2 → Ch4 → Ch7 | 15% |
| Skill 作者 | SKILL | 有 AI 使用经验，想扩展能力 | 掌握 Skill 开发方法，产出高质量 Skill | Ch0 → Ch5 → Ch6 | 5% |
| 工程经理 | MANAGER | 评估团队工具选型 | 判断 OpenCode 的投资回报率 | Ch0 → Ch1 → Ch7 | 5% |
| 智能体开发工程师 | AGENT-ENG | 已有 AI 编程工具使用经验，需要设计、调试、进化 AI 编码智能体 | 掌握 Agent 配置、上下文工程与循环工程 | Ch0 → Ch2 → Ch3 → Ch4 → Ch6 | 10% |

### 5.2 扩展读者角色（团队角色Review补充）

| 角色 | 标识 | 背景 | 目标 | 推荐阅读路径（★标注新增文章） | 预计占比 |
|------|------|------|------|----------------------------|---------|
| **需求分析师/产品经理** | ANALYST | 需求分析、产品规划经验 | 验证需求覆盖完整性、评估内容价值主张 | Ch0 → Ch1(★理论框架/★工具对比) → Ch7(★全流程自动化) → Ch4(★Teams协作) | 5% |
| **系统架构师/技术顾问** | SYSA | 5年以上架构经验，负责技术决策 | 评估OpenCode的技术可行性、架构集成与安全合规 | Ch1(★工具对比/★理论框架) → Ch6(★安全总览/★可观测性/★CLAUDE.md) → Ch2(★约束系统/★验证护栏) → Ch4(★Agent派生/★Teams协作) → Ch5(★Skill-MCP桥接) → Ch7(★混合架构) | 10% |
| **后端开发者/API工程师** | BACKEND | 熟悉REST/GraphQL/微服务/数据库 | 将AI Agent嵌入后端开发工作流、MCP服务端集成 | Ch2(★上下文工程/★约束系统) → Ch3(★多环境部署) → Ch6(★沙箱Hook/★Token预算/★可观测性) → Ch4(★Agent派生) → Ch5(★Skill-MCP桥接) → Ch7(★全流程自动化) | 15% |
| **前端开发者/UI工程师** | FRONTEND | 熟悉React/Vue/Angular、组件化开发 | 将Agent编排应用到前端场景、类比理解Skill系统 | Ch2(★上下文工程/★验证护栏) → Ch5(★Skill插件化/★MCP桥接) → Ch4(★Agent派生/★Teams协作) → Ch6(★可观测性) | 10% |
| **安全工程师/安全架构师** | SECURITY | 安全工程/合规/威胁建模 | 建立OpenCode安全基线、评估企业级合规 | Ch2(★约束系统/★验证护栏) → Ch3(★多环境部署/国产模型安全) → Ch6(★安全总览/★沙箱Hook/★CLAUDE.md) → Ch4(★Agent派生安全) → Ch7(★安全审计) | 10% |
| **安全研究人员/红队成员** | REDTEAM | 渗透测试/安全研究 | 评估AI Agent攻击面、利用Agent自动化安全测试 | Ch2(★上下文工程安全/★约束系统绕过) → Ch6(★安全总览/★沙箱Hook) → Ch5(★Skill插件化安全) → Ch7(★安全审计/★Skill市场) | 10% |
| **文档UX专家** | UX | 信息架构/开发者文档经验 | 确保文档可读性、Mermaid规范、移动端/无障碍体验 | 全书按需审校（特别注意★工具对比雷达图/★监控仪表板/★架构总览图的可视化质量） | N/A(顾问) |
| **技术审校/QA编辑** | QA | 测试或技术写作背景 | 建立质量门禁、验证代码示例可运行性、术语一致性 | 全量审校（特别关注篇幅较短文章的验证标准完备性） | N/A(内部) |

### 5.3 反读者画像（本书不适用于）

- 纯管理层希望完全跳过技术细节的读者 → 推荐阅读公众号摘要
- 仅对产品本身而非方法论感兴趣的读者 → 推荐官方文档
- 已深度掌握 Agent 编排 + Skill 开发的资深用户 → 可能没有太多新内容


### 5.4 读者角色 → 智能体编排映射

#### 5.4.1 映射总表

| 读者角色 | OMO 团队成员 | 思维框架智能体 | 人物视角智能体 | 编排理由 |
|---------|------------|--------------|--------------|---------|
| BEGINNER 入门开发者 | 需求分析师、前端架构师 | 实践论、星星之火 | Paul Graham、Naval | 入门者需要最简路径和直观示例 |
| POWER 效率开发者 | 后端架构师、前端架构师 | 集中兵力、统筹兼顾 | Karpathy、Musk | 效率开发者追求可复用的高阶模式 |
| LEAD 技术负责人 | 架构顾问、安全架构师 | 矛盾论、论持久战、统筹兼顾 | Musk、Jobs、张一鸣 | 技术负责人需要战略视角 |
| SKILL Skill作者 | 后端架构师、QA | 实践论、批评与自我批评 | Karpathy、Feynman | Skill开发需要系统性和可验证性 |
| MANAGER 工程经理 | 需求分析师、架构顾问 | 统筹兼顾、矛盾论 | Munger、Naval、Musk | 经理关心投入产出比 |
| ANALYST 需求分析师 | 需求分析师、架构顾问 | 群众路线、没有调查没有发言权 | Paul Graham、张一鸣 | 分析师需要敏锐的读者需求感知 |
| SYSA 系统架构师 | 架构顾问、安全架构师 | 矛盾论、统筹兼顾 | Karpathy、Musk、张一鸣 | 系统架构师处理复杂权衡 |
| BACKEND 后端开发者 | 后端架构师、QA | 实践论、批评与自我批评 | Karpathy、Feynman | 后端开发者需要可执行的实现指南 |
| FRONTEND 前端开发者 | 前端架构师、UI设计师 | 实践论、星星之火 | Jobs、MrBeast | 前端开发者关注体验和可视化 |
| UX 文档UX专家 | UI设计师、需求分析师 | 群众路线、没有调查没有发言权 | Paul Graham、Jobs | UX专家为全书质量兜底 |
| QA 技术审校 | QA、渗透测试员 | 批评与自我批评、没有调查没有发言权 | Feynman、Taleb | QA需要"挑错"意识 |
| SECURITY 安全工程师 | 安全架构师、蓝队、漏洞管理员 | 矛盾论、没有调查没有发言权 | Karpathy、Taleb、Ilya | 安全需要攻击面意识 |
| REDTEAM 安全研究人员 | 红队指挥、资深红队黑客、渗透测试员、网情分析员 | 矛盾论、批评与自我批评 | Karpathy、Taleb、Ilya | 红队需要进攻性思维 |
| AGENT-ENG 智能体开发工程师 | 架构顾问、后端架构师 | 实践论、批评与自我批评 | Karpathy、Feynman | Agent 工程师需要可调试的工程实践和系统性验证 |

#### 5.4.2 智能体编排模式

根据内容创作阶段，推荐以下编排策略：

| 阶段 | 主导智能体组合 | 任务 |
|------|-------------|------|
| **内容规划** | 矛盾论 + 没有调查没有发言权 | 识别读者痛点和知识缺口，确定文章定位 |
| **初稿创作** | 对应章节的 OMO 团队成员 + 人物视角智能体 | 从特定视角出发撰写内容，确保深度和独特性 |
| **审校优化** | 批评与自我批评 + Feynman/Taleb | 检查逻辑漏洞，核实示例可运行性，验证断言 |
| **质量门禁** | 统筹兼顾 + 群众路线 | 平衡各方质量指标，收集多角色反馈，确认通过 |

#### 5.4.3 视角智能体启用指南

启用人物视角智能体时，创作团队应遵循以下原则：

1. **为什么选这个视角？** 它带来了什么单一视角无法覆盖的洞察？（避免为用而用）
2. **启用后谁控盘？** 人物视角是"顾问"而非"作者"——主笔仍然是 OMO 团队成员
3. **何时关闭？** 视角智能体在事实陈述、代码示例、步骤说明中应关闭，仅在分析、观点、策略部分启用
4. **多视角冲突？** 当两个视角给出矛盾建议时，回归实事求是原则——以读者真实需求为裁决标准

---

> **编排版本**: v1.0 | 创建日期：2026-06-04 | 基础数据：OMO 团队 14 角色 + 毛泽东思想方法论 10 框架 + 15 人物视角智能体## 6. 编排与内容策略

### 6.1 内容开发优先级

| 优先级 | 章节 | 理由 |
|--------|------|------|
| P0 | Ch2 核心概念, Ch3 环境搭建 | 基础知识，读者必须先读 |
| P0 | Ch7 案例研究 | 最大吸引力和实用性 |
| P1 | Ch4 工作流实战, Ch5 Skill 开发 | 进阶内容，高价值 |
| P2 | Ch1 简介 | 框架性内容，篇幅较小 |
| P2 | Ch6 高级话题 | 专项深入，受众较窄 |

### 6.2 内容重用策略

- OpenCode实战 01（核心概念速通）：直接作为 Ch2 内容基础，补充 OMO 部分
- OpenCode实战 02（架构全景解析）：拆分到 Ch3（环境搭建）和 Ch6（高级话题）
- OpenCode实战 03（概念联动实战）：直接作为 Ch4 内容基础
- OpenCode实战 04（奇淫技巧）：提取适用于 Ch1（Profile 切换/AGENTS.md）和 Ch5（Skill 开发）
- OpenCode实战 05（场景化案例）：适配为 Ch7 的两个案例

## 7. 成功标准

### 7.1 三级质量门禁体系

#### 7.1.1 🔴 硬性门禁（必须 100% 通过方可发布）

> 每项都有自动化或手动验证脚本，任何一项未达标则阻断发布。

- [ ] 所有 60+ 篇文章完成编写（全部有内容，第 6、7 章及附录 B/C/D 部分文章篇幅较短）
- [ ] 每篇文章有效正文 ≥ 200 行（第7章文章 ≥ 300 行；排除 frontmatter 和纯空行；代码块计入正文行数）
- [ ] 内部链接有效率达 100%（CI 中 `markdown-link-check` 验证）
- [ ] 本地预览 `mdbook serve` 无报错日志
- [ ] OpenCode/OMO 版本号在全书中保持一致（与第 3.5 节声明一致）

#### 7.1.2 🟡 质量门禁（通过率 ≥ 80% 方可发布）

- [ ] 代码示例已验证可运行比例 ≥ 80%（`examples/` 目录下有配套执行脚本）
- [ ] Mermaid 图表语法正确率 100%（CI 中 `mmdc` 渲染检查）+ 视觉抽检 ≥ 1 轮
- [ ] 术语表中 100% 术语在正文中出现（或标注为附录术语）
- [ ] 所有"第 X 章"交叉引用指向真实章节标题
- [ ] 英文术语大小写一致（如 OpenCode 非 Open code / opencode）

#### 7.1.3 📊 量化统计（发布时记录，持续优化目标）

- [ ] 代码示例总数：≥ 100 个
- [ ] Mermaid/架构图总数：≥ 50 张
- [ ] 全书写稿总有效行数：≥ 50,000 行（实际 ~88 个 .md 文件，全量 ~51,000+ 行）
- [ ] ADR 示例：≥ 3 个
- [ ] 威胁分析表：≥ 2 个（STRIDE 或 PASTA）
- [ ] 架构图：≥ 5 张（分层架构图 + 信任边界图 + 威胁模型图）

### 7.2 技术验收

- [ ] `mdbook serve` 本地预览无错误
- [ ] GitHub Pages 部署成功
- [ ] 移动端阅读排版正常（375px/414px 视口测试通过）
- [ ] 所有内部链接有效（无 404，CI 检查）
- [ ] 示例配置和代码可以实际使用
- [ ] Mermaid 图表在 Docsify 中渲染正确（含暗色模式）
- [ ] 代码高亮支持 6+ 编程语言

### 7.3 社区反馈

- [ ] GitHub Issues 开放收集反馈
- [ ] 每季度更新版本同步
- [ ] 接受社区 PR 贡献
- [ ] QA 自查清单纳入 PR 模板（贡献者需填写代码可运行性、Mermaid 渲染、术语一致性）

## 8. 维护计划

### 8.1 版本同步

| OpenCode 版本变更 | 响应动作 | 时限 |
|------------------|---------|------|
|  Minor 更新 (v1.16.x → v1.17.x) | 检查兼容性，更新版本号 | 1 周 |
|  Major 更新 (v1.x → v2.x) | 全面审查，更新受影响章节 | 2 周 |
| OMO 版本更新 | 更新对应章节内容 | 1 周 |
| Claude Code / Pi Agent 版本更新 | 更新附录 C/D 对应章节内容 | 2 周 |

> **附录 C/D 维护说明**：附录 C（Claude Code 内置能力）和附录 D（Pi Agent）的内容基于对应产品的官方文档和 SDK 版本。厂商发布重大版本更新（如 Claude Code v3.x、Pi Agent 新版本）后，需在 2 周内审查并更新受影响章节。

### 8.2 社区贡献指南

- 使用标准 GitHub Flow（Fork → Branch → PR → Review → Merge）
- PR 需包含：变更摘要、受影响章节、验证步骤
- 至少 1 位维护者 Review 后合并
- 重大的内容变更需在 Issue 中先讨论

---

## 附录 A: ADR 模板（架构决策记录）

在 Ch7 案例研究和架构审视中使用，记录关键架构决策及其上下文。

```markdown
# ADR-NNN: [决策标题，如"选择 OMO Team Mode 作为多 Agent 协作方案"]

## 状态
[提议 / 接受 / 已实施 / 已废弃 / 已替代]

## 上下文
- 要解决什么问题？
- 有哪些约束条件？（版本、团队规模、时间窗口、安全要求）
- 相关的需求和用户故事（链接 PRD 章节）

## 决策
我们选择 **[方案 X]**，因为：
1. [理由 1：如"天然支持自定义Agent注入"]
2. [理由 2：如"与现有 opencode.json 权限模型一致"]
3. [理由 3：如"社区成熟度较高，文档完善"]

## 备选方案
| 方案 | 优势 | 劣势 |
|------|------|------|
| 方案 A（选定） | ... | ... |
| 方案 B | ... | ... |
| 方案 C | ... | ... |

## 后果
- **正面的**：[如"减少跨 Agent 通信的样板代码"]
- **负面的**：[如"增加对 OMO 版本的耦合，需跟踪版本更新"]
- **风险**：[如"v4.5.1 可能调整 API" → 缓解：编写集成测试]

## 合规映射
| 要求 | 满足方式 |
|------|----------|
| PRD §5 安全性 | [如何满足] |
| PRD §7 三级门禁 | [在哪个阶段验证] |

## 相关 ADR
- ADR-001: [关联记录]
- ADR-003: [替代记录]

---

> 决策者：[角色名] | 日期：YYYY-MM-DD | 版本：v1
```

---

## 附录 B: 需求追溯矩阵

将 51 个用户故事（14 角色）映射到 60+ 篇文章（含附录 A/B/C/D），确保全量覆盖。★标记新增文章。

> **注意**：`src/01-introduction/failure-cases.md`（427 行，已完成）原为游离页面，已于 2026-06-03 正式注册为 Ch1 第 6 篇文章（Article 1.6），现计入 60+ 篇文章统计。

### B1 核心读者（6 角色，25 故事）

| 角色 | 故事ID | 覆盖文章（主 + 次） | 状态 |
|------|--------|-------------------|------|
| BEGINNER | US-B-01 核心价值 | Ch1.1 什么是HE, Ch0 README | ✅ 覆盖 |
| BEGINNER | US-B-02 安装 | Ch3.1 快速上手 | ✅ 覆盖 |
| BEGINNER | US-B-03 第一个尝试 | Ch3.1 快速上手 | ✅ 覆盖 |
| BEGINNER | US-B-04 6核心概念 | Ch2.1 Agent编排, Ch2.2 Skill, Ch2.3 工作流 | ✅ 覆盖 |
| BEGINNER | US-B-05 对话→工程 | Ch1.1, Ch1.3 ★理论框架 | ✅ 覆盖 |
| POWER | US-P-01 工作流效率 | Ch4.1 ★Ultrawork, Ch4.3 自定义工作流 | ✅ 覆盖 |
| POWER | US-P-02 Agent编排 | Ch4.2 多Agent协作, Ch4.4 ★Agent派生 | ✅ 覆盖 |
| POWER | US-P-03 Profile切换 | Ch1.2 为什么OpenCode, Ch3.5 ★多环境 | ✅ 覆盖 |
| POWER | US-P-04 命令复用 | Ch4.3 自定义工作流, AGENTS.md | ✅ 覆盖 |
| POWER | US-P-05 成本优化 | Ch6.3 性能调优, Ch6.5 ★Token预算 | ✅ 覆盖 |
| LEAD | US-L-01 团队落地 | Ch7.4 ★全流程自动化, AGENTS.md | ✅ 覆盖 |
| LEAD | US-L-02 安全合规 | Ch6.8 ★安全总览, Ch7.3 ★安全审计 | ✅ 覆盖 |
| LEAD | US-L-03 7-Agent Pipeline | Ch4.2 多Agent协作, ★Teams协作 | ✅ 覆盖 |
| SKILL | US-S-01 SKILL.md格式 | Ch5.1 创建Skill | ✅ 覆盖 |
| SKILL | US-S-02 模板库 | Ch5.2 Skill模板 | ✅ 覆盖 |
| SKILL | US-S-03 作用域/Team | Ch5.3 最佳实践 | ✅ 覆盖 |
| SKILL | US-S-04 最佳实践/反模式 | Ch5.3, Ch5.5 ★插件化 | ✅ 覆盖 |
| MANAGER | US-M-01 ROI分析 | Ch1.1 什么是HE, Ch0 how-to-read | ✅ 覆盖 |
| MANAGER | US-M-02 工具对比 | Ch1.4 ★工具生态对比, Ch1.5 ★国产生态 | ✅ 覆盖 |
| AGENT-ENG | US-AE-01 AGENTS.md 配置 | Ch6.10 ★AGENTS.md, Ch2.5 约束系统 | ✅ 覆盖 |
| AGENT-ENG | US-AE-02 上下文工程 | Ch2.4 ★上下文工程, Ch6.4 ★上下文压缩 | ✅ 覆盖 |
| AGENT-ENG | US-AE-03 循环调试 | Ch4.1 ★Ultrawork, Ch6.3 性能调优 | ✅ 覆盖 |
| AGENT-ENG | US-AE-04 Agent 派生 | Ch4.4 ★Agent派生, Ch5.1 创建Skill | ✅ 覆盖 |
| AGENT-ENG | US-AE-05 团队协作 | Ch4.5 ★Teams协作, Ch6.10 ★AGENTS.md | ✅ 覆盖 |
| AGENT-ENG | US-AE-06 工作流设计 | Ch4.2 ★Prometheus规划, Ch4.3 自定义工作流 | ✅ 覆盖 |

### B2 扩展角色（8 角色，26 故事）

| 角色 | 故事ID | 覆盖文章（主 + 次） | 状态 |
|------|--------|-------------------|------|
| ANALYST | US-A-01 需求覆盖度 | Ch0 ★reading-paths, 全书规格 | ✅ 覆盖 |
| ANALYST | US-A-02 业务价值翻译 | Ch1.3 ★理论框架, Ch1.1 | ✅ 覆盖 |
| ANALYST | US-A-03 读者旅程 | Ch0 (4篇含 quick-start), Ch1 导览 | ✅ 覆盖 |
| SYSA | US-SYSA-01 技术选型 | Ch1.4 ★工具对比, Ch6.3 性能调优 | ✅ 覆盖 |
| SYSA | US-SYSA-02 安全与威胁建模 | Ch6.8 ★安全总览, Ch2.5 ★约束系统 | ⚠️ 规格已覆盖 |
| SYSA | US-SYSA-03 架构治理 | Ch4.5 ★Teams, Ch7.5 ★混合架构, ADR | ✅ 覆盖 |
| BACKEND | US-BE-01 MCP开发 | Ch6.1 MCP服务器, Ch5.4 ★Skill-MCP桥接 | ✅ 覆盖 |
| BACKEND | US-BE-02 API契约/DB | Ch5.4 ★Skill-MCP桥接, Ch7.4 ★全流程 | 🟡 需写作强化 |
| BACKEND | US-BE-03 微服务协同 | Ch7.1 微服务案例, Ch7.5 ★混合架构 | ✅ 覆盖 |
| FRONTEND | US-FE-01 前端Agent编排 | Ch4.4 ★Agent派生, Ch7.2 遗留系统 | ⚠️ 规格已覆盖 |
| FRONTEND | US-FE-02 组件↔Skill类比 | Ch5.5 ★插件化, Ch2.2 Skill系统 | 🟡 需写作强化 |
| FRONTEND | US-FE-03 mdBook架构 | AGENTS.md, Ch3.1 快速上手(mdbook) | ✅ 覆盖 |
| UX | US-UX-01 Mermaid规范 | AGENTS.md §写作规范, 全书图表 | ✅ 覆盖 |
| UX | US-UX-02 代码块规范 | AGENTS.md §写作规范, PRD §4.2 | ✅ 覆盖 |
| UX | US-UX-03 移动端/无障碍 | PRD §4.1.2/4.1.3 | ✅ 覆盖 |
| QA | US-QA-01 代码可运行性 | PRD §7.1.2, examples/目录 | ✅ 覆盖 |
| QA | US-QA-02 自动化检查 | PRD §7.1 CI门禁 | ⚠️ 门禁已定义，需CI落地 |
| QA | US-QA-03 质量门禁验收 | PRD §7 三级门禁体系, AGENTS.md | ✅ 覆盖 |
| SECURITY | US-SEC-01 安全模型 | Ch6.8 ★安全总览, Ch2.5 ★约束系统 | ✅ 覆盖 |
| SECURITY | US-SEC-02 MCP安全 | Ch6.1 MCP服务器(安全), Ch6.9 ★沙箱Hook | ✅ 覆盖 |
| SECURITY | US-SEC-03 安全流水线 | Ch7.3 ★安全审计, Ch6.10 ★CLAUDE.md | ✅ 覆盖 |
| REDTEAM | US-RT-01 安全边界评估 | Ch6.8 ★安全总览, Ch2.5 ★约束系统 | ✅ 覆盖 |
| REDTEAM | US-RT-02 Agent安全测试 | Ch6.9 ★沙箱Hook, Ch7.3 ★安全审计 | ⚠️ 规格已覆盖 |
| REDTEAM | US-RT-03 工具安全评估 | Ch1.4 ★工具对比(安全维度), Ch6.8 | ✅ 覆盖 |

**覆盖统计**：
- ✅ 已覆盖：44/51（86%）
- ⚠️ 规格已定义待写作强化：4/51（8%）
- 🟡 需写作中额外关注：3/51（6%）

---

> **版本**: v3.0 | 最后更新：2026-06-27 | 第七次更新：新增附录 C（Claude Code）和附录 D（Pi Agent），全书结构扩展为 8 章 + 4 附录，~88 个 .md 文件，总计 ~51,000+ 行
> 来源材料：OpenCode v1.16.x + oh-my-openagent v4.13.x | Claude Code SDK / Pi Agent SDK

---

## 附录 C: 变更日志

### v2.4 (2026-06-03)

- **Ch4 结构重构**: Prometheus 规划模式从综述文章提取为独立 Article 4.2，Ch4 文章数 5 → 6
- **Ch1 扩编**: failure-cases.md（427行，原游离页面）正式注册为 Article 1.6，全书 48 → 49 篇
- **完成状态更新**: 完成文章数 30 → 31（新增 failure-cases 计入完成数）
- **量化指标修正**: 总有效行数目标 9,600 → 9,800 行，追溯矩阵 48 → 49 篇
- **spec 更新**: ch04-workflows.md 移除已废弃的 Article 4.6（Agent 编排工作流），新增 Article 4.2 规格和 article 编号顺移
- **spec 更新**: ch01-introduction.md 新增 Article 1.6（AI 编程失败案例）规格定义

### v2.3 (2026-06-02)

- **文章总数修正**: 46 → 48 篇（新增 Ch0 quick-start 和 附录 A glossary）
- **完成状态更新**: Ch0-Ch5 共 30 篇文章已完成，Ch6(12)+Ch7(6) 共 18 篇 stub
- **Ch0 结构修正**: 新增「5 分钟快速体验 (quick-start)」第 4 篇文章
- **章节计数修正**: 第6章已先行更新为12篇，第7章为6篇（与 SUMMARY.md 一致）
- **src/README.md 不同步**: 该书页仍写"19 篇已完成"，已通知更新为 30 篇
- **orphan 文件纳入**: `src/01-introduction/failure-cases.md` (427行) 已注册为 Ch1 Article 1.6，正式计入 49 篇文章统计
- **量化指标更新**: 总有效行数目标 9,200 → 9,800 行，追溯矩阵 46 → 49 篇
- **读者画像增强**: 第5章读者角色与 user-stories.md 中的 14 角色(51 故事)完整对齐
- **内容来源映射更新**: 增加附录 A glossary 的来源说明
