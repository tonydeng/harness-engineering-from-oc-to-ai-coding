# 读者导航 — 本书适合你吗？

> **适合读者**: AI初学者, 效率追求者, 技术负责人

> 本书不是"从零学编程"教程，而是帮你从"跟 AI 聊天写代码"到"用工程体系做开发"的实践指南。花 30 秒判断这本书是否适合你。

---

## 角色自测区

### 自我诊断问卷

回答以下 5 个问题，快速定位你的角色类型：

| 序号 | 问题 | Yes → 跳转 | No → 继续 |
|---|------|-----------|----------|
| **Q1** | 你是否刚接触 AI 编程工具（如 Copilot、Cursor、Claude Code）？ | → **入门开发者** | → Q2 |
| **Q2** | 你是否已有 AI 编程工具使用经验，想系统提升效率？ | → **效率开发者** 或 **智能体开发工程师** | → Q3 |
| **Q3** | 你是否负责团队技术决策或工具选型？ | → **技术负责人** 或 **工程经理** | → Q4 |
| **Q4** | 你是否需要开发自定义 Skill 或集成外部工具？ | → **Skill 作者** 或 **后端开发者** | → Q5 |
| **Q5** | 你是否关注安全合规、威胁建模或渗透测试？ | → **安全工程师** 或 **红队成员** | → **其他角色** |

```mermaid
flowchart TB
    START((开始诊断)) --> Q1{Q1: 刚接触<br/>AI 编程?}
    Q1 -->|Yes| 入门[入门<br/>入门开发者]
    Q1 -->|No| Q2{Q2: 已有经验<br/>想提升效率?}

    Q2 -->|想系统提升效率?| 效率[效率<br/>效率开发者]
    Q2 -->|想深入理解<br/>AI 配置和行为?| 智能体工程师Node[智能体工程师<br/>智能体开发工程师]
    Q2 -->|No| Q3{Q3: 负责团队<br/>技术决策?}

    Q3 -->|Yes| Q3a{管理职责?}
    Q3a -->|偏管理| 工程经理[工程经理]
    Q3a -->|偏技术| 技术负责人[技术负责人]
    Q3 -->|No| Q4{Q4: 需要开发<br/>自定义 Skill?}

    Q4 -->|Yes| Q4a{开发类型?}
    Q4a -->|Skill 开发| Skill作者[Skill 作者]
    Q4a -->|后端/MCP| 后端[后端<br/>后端开发者]
    Q4a -->|前端场景| 前端[前端<br/>前端开发者]
    Q4 -->|No| Q5{Q5: 关注安全<br/>合规?}

    Q5 -->|Yes| Q5a{安全视角?}
    Q5a -->|防御/合规| 安全工程师[安全工程师]
    Q5a -->|攻击/测试| 红队[红队<br/>红队成员]
    Q5 -->|No| 其他角色[其他角色<br/>需求分析师/架构师/UX/QA]

    classDef start fill:#4A90D9,stroke:#2E5A8C,color:#fff
    classDef core fill:#50C878,stroke:#2E8B57,color:#fff
    classDef ext fill:#FF9F43,stroke:#D35400,color:#fff
    classDef other fill:#A66CFF,stroke:#7D3C98,color:#fff

    class START start
    class 入门,效率,智能体工程师Node,技术负责人,Skill作者,工程经理 core
    class 后端,前端,安全工程师,红队 ext
    class 其他角色 other
```

### 14 种读者角色速查

| 角色 | 简称 | 典型特征 | 核心目标 | 推荐优先级 |
|------|------|----------|----------|------------|
| **入门开发者** | 入门 | 刚接触 AI 编程，基本编程能力 OK | 快速上手 OpenCode | ★★★★★ |
| **智能体开发工程师** | 智能体工程师 | 已有 AI 工具使用经验，需要设计、调试、进化 AI 编码智能体 | 掌握 Agent 配置、**Context Engineering（上下文工程）**、循环工程 | ★★★★★ |
| **效率开发者** | 效率 | 已用 AI 工具，想升级到 Agent 编排 | 提升 2x+ 效率 | ★★★★★ |
| **技术负责人** | 技术负责人 | 团队技术决策者，关注标准化 | 建立团队级体系 | ★★★★★ |
| **Skill 作者** | **Skill（技能）** 作者 | 有 AI 使用经验，想扩展能力 | 开发高质量 Skill | ★★★★★ |
| **工程经理** | 工程经理 | 评估团队工具选型 | 判断投资回报率 | ★★★★☆ |
| **需求分析师** | 需求分析师 | 需求分析、产品规划经验 | 验证需求覆盖完整性 | ★★★☆☆ |
| **系统架构师** | 架构师 | 5 年以上架构经验 | 评估技术可行性 | ★★★★☆ |
| **后端开发者** | 后端 | 熟悉 REST/微服务/数据库 | **MCP（模型上下文协议）** 服务端集成 | ★★★★☆ |
| **前端开发者** | 前端 | 熟悉 React/Vue/Angular | 前端工作流应用 | ★★★☆☆ |
| **文档 UX 专家** | UX | 信息架构/开发者文档经验 | 文档体验优化 | ★★☆☆☆ |
| **技术审校** | QA | 测试或技术写作背景 | 建立质量门禁 | ★★★☆☆ |
| **安全工程师** | 安全工程师 | 安全工程/合规/威胁建模 | 建立安全基线 | ★★★★☆ |
| **红队成员** | 红队 | 渗透测试/安全研究 | 评估攻击面 | ★★★★☆ |

### 跨角色比对表：技术深度 vs 管理职责

```mermaid
quadrantChart
    title 读者角色分布：技术深度 vs 管理职责
    x-axis "管理职责低" --> "管理职责高"
    y-axis "技术深度低" --> "技术深度高"
    quadrant-1 "技术管理者"
    quadrant-2 "深度技术专家"
    quadrant-3 "入门学习者"
    quadrant-4 "业务决策者"
    "入门": [0.15, 0.20]
    "智能体工程师": [0.28, 0.82]
    "效率": [0.25, 0.75]
    "技术负责人": [0.75, 0.85]
    "Skill作者": [0.18, 0.90]
    "工程经理": [0.85, 0.35]
    "需求分析师": [0.60, 0.30]
    "架构师": [0.45, 0.95]
    "后端": [0.20, 0.85]
    "前端": [0.20, 0.70]
    "UX": [0.30, 0.40]
    "QA": [0.35, 0.55]
    "安全工程师": [0.30, 0.90]
    "红队": [0.20, 0.95]
```

| 维度 | 核心角色 (6) | 扩展角色 (8) |
|------|-------------|-------------|
| **技术深度高** | 智能体工程师, Skill 作者, 效率, 技术负责人 | 架构师, 红队, 安全工程师, 后端 |
| **技术深度中** | 入门 | 前端, QA |
| **技术深度低** | 工程经理 | 需求分析师, UX |
| **管理职责高** | 技术负责人, 工程经理 | 需求分析师 |
| **管理职责中** | 效率 | 架构师, QA |
| **管理职责低** | 入门, 智能体工程师, Skill 作者 | 后端, 前端, UX, 安全工程师, 红队 |

---

## 优先级矩阵：8 章 × 14 角色

### 矩阵说明

| 优先级 | 标记 | 定义 | 阅读建议 |
|--------|------|------|----------|
| **P0** | ● | 必备章节 | 必须精读，是理解后续内容的基础 |
| **P1** | ◐ | 重要章节 | 推荐阅读，能显著提升实践效果 |
| **P2** | ○ | 可选章节 | 按需阅读，锦上添花 |
| **Skip** | - | 跳过 | 初期可跳过，后续按需回溯 |

### 完整矩阵

| 章节 | 入门 | 智能体工程师 | 效率 | 技术负责人 | Skill 作者 | 工程经理 | 需求分析师 | 架构师 | 后端 | 前端 | UX | QA | 安全工程师 | 红队 |
|------|:----:|:----------:|:----:|:----------:|:----------:|:--------:|:----------:|:------:|:----:|:----:|:--:|:--:|:----------:|:----:|
| **读者导航** | ○ | ● | ○ | ● | ○ | ○ | ● | ○ | ○ | ○ | ● | ● | ○ | ○ |
| **简介** | ● | ● | ◐ | ● | ◐ | ● | ● | ● | ◐ | ◐ | ◐ | ● | ◐ | ◐ |
| **核心概念** | ● | ● | ● | ● | ● | ◐ | ◐ | ● | ◐ | ◐ | ◐ | ● | ◐ | ◐ |
| **环境搭建** | ● | ● | ● | ● | ● | - | - | ◐ | ● | ◐ | - | ● | ● | ◐ |
| **工作流实战** | ● | ● | ● | ● | ◐ | - | - | ● | ● | ● | - | ● | ● | ● |
| **Skill 开发** | ◐ | ● | ◐ | ◐ | ● | - | - | ◐ | ◐ | ● | - | ● | ◐ | ◐ |
| **高级话题** | ○ | ● | ● | ● | ● | ◐ | - | ● | ● | ○ | - | ● | ● | ● |
| **案例研究** | ◐ | ◐ | ● | ● | ● | ● | ● | ● | ● | ◐ | ◐ | ● | ● | ● |

### 优先级热力图

```mermaid
graph TB
    subgraph Ch0["读者导航"]
        C0_1["读者导航<br/>入门/智能体工程师/技术负责人/需求分析师/UX/QA: P0"]
    end

    subgraph Ch1["简介"]
        C1_1["核心简介<br/>入门/智能体工程师/技术负责人/工程经理/需求分析师/架构师: P0"]
        C1_2["生态对比<br/>技术负责人/工程经理/智能体工程师/架构师: P0<br/>其他: P1"]
    end

    subgraph Ch2["核心概念"]
        C2_1["核心三要素<br/>入门/效率/智能体工程师/技术负责人/Skill 作者: P0"]
        C2_2["进阶概念<br/>效率/智能体工程师/Skill 作者/架构师/安全工程师: P0"]
    end

    subgraph Ch3["环境搭建"]
        C3_1["快速上手<br/>入门/效率/智能体工程师/技术负责人/Skill 作者/后端/安全工程师: P0"]
        C3_2["高级配置<br/>智能体工程师: P0<br/>效率/Skill 作者/架构师/后端: P1"]
    end

    subgraph Ch4["工作流实战"]
        C4_1["核心工作流<br/>入门/效率/智能体工程师/技术负责人/架构师/后端/前端: P0"]
        C4_2["高级协作<br/>效率/智能体工程师/技术负责人/架构师/后端/安全工程师/红队: P1"]
    end

    subgraph Ch5["Skill 开发"]
        C5_1["Skill 核心<br/>智能体工程师/Skill 作者/前端: P0<br/>其他: P1"]
        C5_2["高级集成<br/>智能体工程师/Skill 作者/后端/架构师: P1"]
    end

    subgraph Ch6["高级话题"]
        C6_1["MCP 服务器<br/>智能体工程师/Skill 作者/后端/架构师/安全工程师/红队: P0"]
        C6_2["性能调优<br/>效率/智能体工程师/工程经理: P0"]
        C6_3["安全章节<br/>智能体工程师/技术负责人/架构师/安全工程师/红队: P0"]
    end

    subgraph Ch7["案例研究"]
        C7_1["核心案例<br/>效率/技术负责人/工程经理/后端: P0<br/>智能体工程师: P1"]
        C7_2["安全审计<br/>架构师/安全工程师/红队: P0"]
        C7_3["Skill 市场<br/>技术负责人/Skill 作者: P0"]
    end

    C0_1 --> C1_1
    C1_1 --> C2_1
    C2_1 --> C3_1
    C3_1 --> C4_1
    C4_1 --> C5_1
    C5_1 --> C6_1
    C6_1 --> C7_1

    classDef p0 fill:#4A90D9,stroke:#2E5A8C,color:#fff
    classDef p1 fill:#50C878,stroke:#2E8B57,color:#fff
    classDef p2 fill:#FF9F43,stroke:#D35400,color:#fff

    class C0_1,C1_1,C2_1,C3_1,C4_1,C5_1,C6_1,C6_2,C6_3,C7_1,C7_2,C7_3 p0
    class C1_2,C2_2,C3_2,C4_2,C5_2 p1
```

### 各角色推荐阅读路径

| 角色 | P0 章节 | P1 章节 | 预计用时 |
|------|---------|---------|----------|
| **入门** | [读者导航](./), [简介](../01-introduction/), [核心概念](../02-core-concepts/), [环境搭建](../03-setup/), [工作流实战](../04-workflows/) | [Skill 开发](../05-skills/), [案例研究](../07-case-studies/) | 4-5 小时 |
| **智能体工程师** | [核心概念](../02-core-concepts/), [环境搭建](../03-setup/), [工作流实战](../04-workflows/), [高级话题](../06-advanced/), [案例研究](../07-case-studies/) | [读者导航](./), [简介](../01-introduction/), [Skill 开发](../05-skills/) | 5-6 小时 |
| **效率** | [核心概念](../02-core-concepts/), [环境搭建](../03-setup/), [工作流实战](../04-workflows/), [高级话题](../06-advanced/), [案例研究](../07-case-studies/) | [简介](../01-introduction/), [Skill 开发](../05-skills/) | 5-6 小时 |
| **技术负责人** | [读者导航](./), [简介](../01-introduction/), [核心概念](../02-core-concepts/), [环境搭建](../03-setup/), [工作流实战](../04-workflows/), [高级话题](../06-advanced/), [案例研究](../07-case-studies/) | [Skill 开发](../05-skills/) | 6-7 小时 |
| **Skill 作者** | [核心概念](../02-core-concepts/), [环境搭建](../03-setup/), [Skill 开发](../05-skills/), [高级话题](../06-advanced/), [案例研究](../07-case-studies/) | [简介](../01-introduction/), [工作流实战](../04-workflows/) | 5-6 小时 |
| **工程经理** | [简介](../01-introduction/), [案例研究](../07-case-studies/) | [核心概念](../02-core-concepts/), [高级话题](../06-advanced/) | 3-4 小时 |
| **需求分析师** | [读者导航](./), [简介](../01-introduction/), [案例研究](../07-case-studies/) | [核心概念](../02-core-concepts/) | 4-5 小时 |
| **架构师** | [简介](../01-introduction/), [核心概念](../02-core-concepts/), [工作流实战](../04-workflows/), [高级话题](../06-advanced/), [案例研究](../07-case-studies/) | [环境搭建](../03-setup/), [Skill 开发](../05-skills/) | 7-8 小时 |
| **后端** | [环境搭建](../03-setup/), [工作流实战](../04-workflows/), [Skill 开发](../05-skills/), [高级话题](../06-advanced/), [案例研究](../07-case-studies/) | [简介](../01-introduction/), [核心概念](../02-core-concepts/) | 5-6 小时 |
| **前端** | [工作流实战](../04-workflows/), [Skill 开发](../05-skills/) | [简介](../01-introduction/), [核心概念](../02-core-concepts/), [环境搭建](../03-setup/), [案例研究](../07-case-studies/) | 4-5 小时 |
| **UX** | [读者导航](./), [案例研究](../07-case-studies/) | [简介](../01-introduction/), [核心概念](../02-core-concepts/) | 3-4 小时 |
| **QA** | [读者导航](./), [简介](../01-introduction/), [核心概念](../02-core-concepts/), [环境搭建](../03-setup/), [工作流实战](../04-workflows/), [Skill 开发](../05-skills/), [高级话题](../06-advanced/), [案例研究](../07-case-studies/) | - | 6-7 小时 |
| **安全工程师** | [环境搭建](../03-setup/), [工作流实战](../04-workflows/), [Skill 开发](../05-skills/), [高级话题](../06-advanced/), [案例研究](../07-case-studies/) | [简介](../01-introduction/), [核心概念](../02-core-concepts/) | 5-6 小时 |
| **红队** | [工作流实战](../04-workflows/), [Skill 开发](../05-skills/), [高级话题](../06-advanced/), [案例研究](../07-case-studies/) | [简介](../01-introduction/), [核心概念](../02-core-concepts/) | 5-6 小时 |

---

## 前置知识确认

### 必须具备

| 前置知识 | 要求程度 | 验证方式 |
|----------|----------|----------|
| **编程语言** | 至少熟悉一种（TypeScript/Python/Go/Java/Rust 等） | 能独立完成一个完整的小项目 |
| **命令行** | 基本使用经验 | 熟悉 cd、ls、grep、管道等基本操作 |
| **Git** | 基本使用经验 | 能完成 clone、commit、push、pull 等操作 |

### 建议具备

| 前置知识 | 要求程度 | 说明 |
|----------|----------|------|
| **AI 编程助手** | 使用过至少一种 | Copilot / Claude Code / Cursor / Codeium 等 |
| **Agent/LLM 概念** | 了解基本概念 | 知道什么是 LLM、**Prompt（提示词）**、Context 即可 |
| **MCP 协议** | 听说过即可 | Model Context Protocol，后续章节会详细讲解 |

### 前置知识自检清单

```markdown:terminal
- [ ] 我能用一种编程语言完成一个完整的小项目
- [ ] 我能在命令行中导航目录、执行命令
- [ ] 我能用 Git 完成基本的版本控制操作
- [ ] 我使用过至少一种 AI 编程助手（可选但建议）
- [ ] 我了解 LLM/Prompt 的基本概念（可选但建议）
```

> 如果你勾选了前三项，你就具备了阅读本书的基础。后两项是加分项，会在书中相关章节补充讲解。

---

## 本书不涵盖的内容

### 明确边界

| 不涵盖的内容 | 为什么跳过 | 替代资源 |
|-------------|-----------|---------|
| **编程基础语法** | 假设读者已有开发经验 | 各语言官方教程、《代码大全》 |
| **OpenCode Node.js/TypeScript 实现** | 聚焦用户层面配置和实践 | [OpenCode 源码](https://github.com/anomalyco/opencode) |
| **具体云平台完整教程** | 聚焦 AI 编程工作流本身 | AWS/Azure/GCP/阿里云官方文档 |
| **大模型训练或微调** | 本书是工程实践，不是 **ML（机器学习）**教程 | Hugging Face 课程、各模型官方文档 |
| **特定框架深度教程** | 示例涉及但不深入讲解 | React/Vue/Spring 等框架官方文档 |
| **企业级 DevOps 完整方案** | 聚焦 AI 编程环节 | 《持续交付》《DevOps 手册》 |

### 内容边界示意图

```mermaid
graph TB
    subgraph 本书范围
        A1[Agent 编排设计]
        A2[Skill 开发实践]
        A3[工作流模式]
        A4[上下文工程]
        A5[安全与合规]
        A6[案例研究]
    end
    
    subgraph 相关但不在范围
        B1[编程语言基础]
        B2[OpenCode 源码实现]
        B3[云平台运维]
        B4[大模型训练微调]
        B5[特定框架深度]
        B6[企业 DevOps]
    end
    
    subgraph 前置知识
        C1[基本编程能力]
        C2[命令行操作]
        C3[Git 使用]
    end
    
    C1 --> A1
    C2 --> A1
    C3 --> A1
    
    A1 --> A2
    A2 --> A3
    A3 --> A4
    A4 --> A5
    A5 --> A6
    
    B1 -.->|需要前置| C1
    B2 -.->|相关但不深入| A2
    B3 -.->|相关但不深入| A5
    B4 -.->|完全不在范围| A4
    
    classDef inScope fill:#50C878,stroke:#2E8B57,color:#fff
    classDef outScope fill:#E8E8E8,stroke:#BDBDBD,color:#666
    classDef prereq fill:#4A90D9,stroke:#2E5A8C,color:#fff
    
    class A1,A2,A3,A4,A5,A6 inScope
    class B1,B2,B3,B4,B5,B6 outScope
    class C1,C2,C3 prereq
```

---

## 版本声明

### 技术栈版本

| 组件 | 版本 | 说明 |
|------|------|------|
| **[OpenCode](https://github.com/anomalyco/opencode)** | v1.17.x | 核心 AI 编程引擎（当前为 v1.17.11） |
| **[oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)** | v4.12.x | Agent 编排套件（当前为 v4.12.0） |
| **[mdBook](https://github.com/rust-lang/mdBook)** | v0.5.x | 书籍渲染引擎（当前为 v0.5.3） |
| **[Mermaid](https://github.com/mermaid-js/mermaid)** | v10+ | 图表和架构图 |
| **[Node.js](https://nodejs.org/)** | >=18 | npm 安装方式所需运行时（curl/brew 安装不需要） |

### OpenCode核心生态演进

```mermaid
timeline
    title OpenCode 核心生态演进时间线
    2025-Q2 (4 月) : OpenCode 项目创建
    2025-Q2 (6 月) : OpenCode v0.1.x 早期版本
    2025-Q4 (10 月) : OpenCode v1.0 TUI Rewrite 完整重写
    2026-Q1 (1 月) : OpenCode MCP 支持集成
    2025-Q3 (8 月) : oh-my-openagent 项目创建
```

---

## 快速开始指南

### 30 秒决策流程

```mermaid
flowchart LR
    A[打开本书] --> B{有编程基础?}
    B -->|No| C[先学习编程基础]
    B -->|Yes| D{用过 AI 编程工具?}
    D -->|No| E[入门路径]
    D -->|Yes| F{想提升效率?}
    F -->|Yes| G[效率路径]
    F -->|No| H{负责团队决策?}
    H -->|Yes| I[技术负责人/工程经理路径]
    H -->|No| J{开发 Skill?}
    J -->|Yes| K[Skill 作者路径]
    J -->|No| L{关注安全?}
    L -->|Yes| M[安全工程师/红队路径]
    L -->|No| N[其他角色路径]

    classDef decision fill:#FF9F43,stroke:#D35400,color:#fff
    classDef action fill:#50C878,stroke:#2E8B57,color:#fff
    classDef exit fill:#E8E8E8,stroke:#BDBDBD,color:#666

    class B,D,F,H,J,L decision
    class E,G,I,K,M,N action
    class C exit
```

### 下一步行动

| 你的角色 | 立即行动 |
|----------|----------|
| **入门** | 跳转到 [什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md) |
| **效率** | 跳转到 [Agent 编排](../02-core-concepts/agent-orchestration.md) |
| **技术负责人** | 跳转到 [**Harness Engineering（驾驭工程）** 理论框架](../01-introduction/harness-engineering-theory.md) |
| **Skill 作者** | 跳转到 [Skill 系统](../02-core-concepts/skills-system.md) |
| **工程经理** | 跳转到 [AI 编程工具生态对比](../01-introduction/ecosystem-comparison.md) |
| **后端** | 跳转到 [MCP 服务器](../06-advanced/mcp-servers.md) |
| **前端** | 跳转到 [工作流模式](../02-core-concepts/workflow-patterns.md) |
| **安全工程师** | 跳转到 [安全总览](../06-advanced/security-overview.md) |
| **红队** | 跳转到 [安全审计流水线](../07-case-studies/case-security-audit.md) |
| **其他角色** | 查看完整 [多角色阅读路径](reading-paths.md) |

---

## 章节导航

> ✅ **写作状态提示**：本书 **90 篇全部完成**（100%）。阅读路径和各章节链接均已标注完整规划。

本章包含以下内容：

- **[多角色阅读路径](reading-paths.md)** — 针对 14 种读者角色提供定制化的章节跳转建议，以及对应的阅读时间估算
- **[如何使用本书](how-to-read.md)** — 两种阅读模式（逐章精读 vs 按需跳跃）的对比说明，以及最大化学习收益的实操建议
- **[5 分钟快速体验](quick-start.md)** — 从安装到第一次 AI 编程任务，一站式快速上手

---

## 给出反馈

发现错误？有改进建议？欢迎通过 [GitHub Issues](https://github.com/tonydeng/harness-engineering-from-oc-to-ai-coding/issues) 提交反馈。

---

> [下一页：多角色阅读路径 →](reading-paths.md)
