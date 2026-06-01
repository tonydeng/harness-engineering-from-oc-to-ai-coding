# Ch1: 简介

## 概述

本书第1章为全书定调：定义"Harness Engineer"（驾驭式工程师）这一概念，阐述为什么AI编程正在经历从"聊天对话"到"工程流水线"的范式转变，以及OpenCode在这场转变中的独特定位。本章帮助读者快速判断：这本书/OpenCode是否值得投入时间。

**章节核心主题**：从"对话式AI编程"到"工程化AI流水线"——Harness Engineering的定义、价值与工具选择。

> **章节规模**：5 篇文章（2 现有 + 3 新增），2 篇修改

## 文章

### Article 1.1: 什么是 Harness Engineer
- **阅读时间**：15 min
- **学习目标**：
  - 理解AI编程三个阶段的演进：代码补全(2021)→对话编程(2024)→工程流水线(2026)
  - 定义"Harness Engineer"：不是"用AI写代码的人"，而是"驾驭AI Agent完成工程交付的人"
  - 理解Harness Engineer的5个核心能力：需求澄清、工作流设计、Agent编排、质量审查、知识沉淀
- **前置知识**：无（本文章是全书起点）
- **源材料映射**：OpenCode实战 01（概念速通，OS类比部分）+ OpenCode实战 04（Profile切换/AGENTS.md理念）

#### 大纲
1. AI编程的"三次浪潮"
   - 1.0 代码补全（GitHub Copilot 2021）—— 补全粒度，被动响应
   - 2.0 对话编程（Cursor/Claude Code 2024-2025）—— 聊天交互，单Agent
   - 3.0 工程流水线（OpenCode 2026）—— Agent编排，多工具链，工程化
2. 为什么"对话"不够？
   - Token成本失控：长对话上下文膨胀
   - "失忆"问题：跨Session上下文丢失
   - 质量不可控：生成即信任，缺乏Review机制
   - 重复劳动：好的工作流无法复用
3. Harness Engineer定义
   - H ≠ "会用AI写代码的工程师"
   - H = "能设计AI工作流、编排多Agent、建立质量门禁、沉淀知识体系"的工程师
   - 5大核心能力框架
4. Harness Engineering的3个核心原则
   - 可复现（Reproducible）：同样的输入得到同样质量的输出
   - 可审计（Auditable）：每一步有记录、可回放、可审查
   - 可改进（Improveable）：从每次运行中学习，持续优化

#### 核心概念
- **三个阶段模型**：这是全书的理论基石，用三维对比表+时间线图清晰展示
- **Harness Engineer vs Prompt Engineer**：Prompt Engineer关注"怎么写好的提示词"；Harness Engineer关注"怎么设计好的工程流水线"
- **3个可**原则：可复现/可审计/可改进——全书所有实践都围绕这三个原则展开

#### 代码/配置示例
- 无（本章以概念阐述为主）

#### Mermaid 图表
- AI编程三阶段演进时间线图
- Harness Engineer能力雷达图（5维度）

#### 关联章节
- → Ch2 Core Concepts（为六概念奠定理解基础）
- → Ch4 Workflows（工程流水线的具体实现）

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 包含三个阶段的对比表
- [ ] 包含Harness Engineer能力雷达图

---

### Article 1.2: 为什么选择 OpenCode
- **阅读时间**：15 min
- **学习目标**：
  - 理解OpenCode vs Cursor vs Claude Code vs Copilot的核心差异
  - 理解OpenCode的4个核心优势：开源、Provider自由、Agent编排、Plugin/MCP生态
  - 能够根据团队/个人场景判断OpenCode是否是最佳选择
  - 了解OpenCode + oh-my-openagent的双层架构价值
- **前置知识**：Article 1.1
- **源材料映射**：OpenCode实战 01（核心概念速通的附录和FAQ）+ OpenCode实战 02（三层架构解析）+ OpenCode实战 04（Profile切换、自定义命令）

#### 大纲
1. AI编程工具全景对比
   - 对比维度：开源性、Provider自由度、Agent类型、Plugin/扩展、学习曲线、隐私、价格
   - OpenCode vs Cursor vs Claude Code vs Copilot vs Continue vs Tabby
   - 对比矩阵表
2. OpenCode的4个核心优势
   - 完全开源（167K+ Stars，社区驱动）
   - 任意LLM提供商（75+ Provider，不锁定）
   - Agent架构（Build/Plan + @general/@explore + 自定义Agent）
   - 扩展生态（Plugin 20+ Hook点 + MCP协议 + Skills Marketplace）
3. oh-my-openagent：什么时候需要它
   - 原生OpenCode vs OMO：能力边界对比表
   - OMO增加的能力：11+专业Agent、类别路由、Team Mode、Ultrawork、Hyperplan
   - 决策树：什么时候用原生、什么时候加OMO
4. OpenCode的局限性（诚实告知）
   - 终端界面 vs 编辑器内嵌（Cursor体验优势）
   - 学习曲线（6个概念需要理解）
   - 远程模式仍在完善（vs Cursor的云端体验）
5. 选型决策框架

#### 核心概念
- **Provider自由度**：OpenCode不绑定任何LLM提供商，75+ Provider自由切换，甚至可混合使用。这是与Cursor（只支持自有模型+OpenAI）的核心差异。
- **Agent vs Copilot**：Copilot是"补全器"——基于光标位置给出建议；Agent是"执行器"——理解任务后自主执行多步操作。
- **双层架构**：OpenCode提供基础Agent能力，OMO在其上叠加编排层。两者是扩展关系而非替代。

#### 代码/配置示例
- 安装命令示例（4种方式）
- Provider配置示例（3种方式）
- `opencode --help` 输出片段

#### Mermaid 图表
- 工具对比矩阵（表格即可，不一定要Mermaid）
- 选型决策树

#### 关联章节
- → Ch3 Setup（安装和配置的实操）
- ↑ 承接Article 1.1（"为什么选择OpenCode"是"What is Harness Engineering"的自然延伸）

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 对比表覆盖至少5个工具的8个维度
- [ ] 包含选型决策树
- [ ] 诚实列出至少3个OpenCode的局限性

### 团队角色评审补充
- **架构顾问需求**：Article 1.2 工具对比表增加架构维度（集成性/可观测性/安全架构/扩展性），增加"OpenCode的企业架构定位"小节。
- **安全架构师需求**：Article 1.1 增加"安全失控"痛点——Agent接管终端后的误操作风险；将"可审计"原则与安全审计日志关联。
- **需求分析师需求**：Ch1 开头增加价值声明块（目标读者/前驱知识/学习收获/预计投入时间）。
- **UI设计师需求**：Ch1 两篇Mermaid图需使用统一配色方案，每张图有Alt文本描述。

---

## 章节重构增补

### 修改标注（基于章节重构计划）

#### 需要修改的现有文章

**Article 1.1（什么是 Harness Engineer）**：
- 增补 Mitchell Hashimoto 原始定义
- 增补 Harrison Chase "Agent = Model + Harness" 公式

**Article 1.2（为什么选择 OpenCode）**：
- 增补 OMO v4.5+ 特性（11+ Agent, 53+ Hook点）

---

### Article 1.3: Harness Engineering 理论框架
- **阅读时间**：20 min
- **学习目标**：
  - 理解 Harness Engineering 的完整理论定义
  - 掌握 Martin Fowler 5 大分类法
  - 理解 AI 编程工具从 2024 到 2026 的演进时间线
- **前置知识**：Article 1.1（Harness Engineer 基础概念）
- **源材料映射**：HE实践 01

#### 大纲
1. Harness Engineering 定义深化
   - 从"驾驭 AI 写代码"到"设计 AI 工程流水线"
   - Hatness 的 4 个核心支柱：编排、安全、可观测、成本
2. Martin Fowler 5 大分类法
   - 每个分类的定义和典型工具
   - 分类法的工程实践意义
3. 演进时间线 2024→2026
   - 2024: Copilot Chat + Cursor 对话编程时代
   - 2025: Claude Code + Agent 自主执行
   - 2026: OpenCode + OMO Agent 编排体系
4. Harness Engineering 在企业级落地中的价值
5. 本书的理论框架在全书中的位置

#### 核心概念
- **5 大分类法**：将 AI 编程工具分为 5 个类别，建立统一的讨论框架
- **演进时间线**：帮助读者理解"为什么是现在"需要 Harness Engineering

#### 代码/配置示例
- 无（本章以理论框架阐述为主）

#### Mermaid 图表
- Harness Engineering 完整理论框架图
- 5 大分类法的分类树形图
- AI 编程工具演进时间线（Mermaid timeline 图）

#### 关联章节
- ← 承接 Article 1.1（理论的深化）
- → Article 1.4（工具对比的理论框架基础）

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 包含 5 大分类法的完整解释
- [ ] 包含演进时间线图
- [ ] 包含 Harness Engineering 在各分类中的定位说明
- [ ] 包含理论框架到后续章节的显式映射说明

---

### Article 1.4: 工具生态对比
- **阅读时间**：20 min
- **学习目标**：
  - 理解 OpenCode 在 AI 编程工具生态中的定位
  - 掌握 6 款主流工具的优劣势对比
  - 能够根据团队场景做出选型决策
- **前置知识**：Article 1.3（理论框架）
- **源材料映射**：HE实践 04

#### 大纲
1. AI 编程工具全景
   - OpenCode / Cursor / Claude Code / Codex / Cline / Windsurf
   - 各工具的定位和核心差异
2. 多维度对比矩阵
   - 开源性、Provider 自由度、Agent 类型、Plugin/扩展、学习曲线、隐私、价格
3. 场景化选型指南
   - 个人开发者 / 小团队 / 企业级
   - 不同技术栈适配度
4. OpenCode 的优势与局限
5. 工具生态的未来趋势

#### 核心概念
- **开源 vs 闭源的分水岭**：OpenCode 的完全开源 vs Cursor 的闭源模式对团队的影响
- **Provider 自由度的工程意义**：不绑定模型提供商带来的灵活性和风险

#### 代码/配置示例
- 各工具的安装和配置对比示例

#### Mermaid 图表
- 6 款工具对比矩阵图
- 场景化选型决策树

#### 关联章节
- ← Article 1.3（理论框架指导对比维度）
- ↑ 承接 Article 1.2（从 OpenCode 到全景对比）

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 对比表覆盖至少 6 款工具的 8 个维度
- [ ] 包含场景化选型决策树

---

### Article 1.5: 国产 AI 生态
- **阅读时间**：15 min
- **学习目标**：
  - 了解国产 AI 编程工具的发展现状
  - 掌握 Trae、CodeGeeX、通义灵码、文心快码的核心能力
  - 理解国产方案与 OpenCode 的互补关系
- **前置知识**：Article 1.4（工具生态对比）
- **源材料映射**：HE实践 04 §国产工具

#### 大纲
1. 国产 AI 编程工具全景
   - Trae（字节跳动）：IDE 原生体验
   - CodeGeeX（智谱）：VS Code 插件
   - 通义灵码（阿里）：电商场景优化
   - 文心快码（百度）：中文理解优化
2. 国产 vs 国际工具的差异分析
   - 模型能力、中文支持、合规要求
3. OpenCode 与国产模型结合使用
   - 国产 Model Provider 配置
   - DeepSeek + OpenCode 的性价比组合
4. 国产 AI 工具的未来趋势

#### 核心概念
- **国产方案的差异化优势**：中文理解能力、合规部署、成本优势
- **混合架构的可能性**：国产模型做简单任务 + 国外模型做复杂推理

#### 代码/配置示例
- DeepSeek Provider 配置示例
- Qwen Provider 配置示例

#### Mermaid 图表
- 国产 AI 工具对比矩阵
- 混合架构示意图

#### 关联章节
- ← Article 1.4（国产是生态的一部分）
- → Ch3 Article 3.4（国产模型配置的实操）

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 覆盖至少 4 款国产工具
- [ ] 包含国产模型与 OpenCode 结合方案

---

## 团队协作工作流

### 团队分工

| 角色 | 职责 | 负责文章 |
|------|------|---------|
| **需求分析师**（ANALYST） | 定义读者价值声明块、需求追溯映射、反读者画像 | Article 1.1, Article 1.3 |
| **架构顾问**（SYSA） | Harness Engineering 理论框架深化、工具对比架构维度、企业架构定位 | Article 1.3, Article 1.4 |
| **前端架构师**（FRONTEND） | 工具对比的可视化呈现、雷达图/Mermaid 规范 | Article 1.4, Article 1.5 |
| **安全架构师**（SECURITY） | 补充安全失控痛点说明、"可审计"原则与安全日志关联 | Article 1.1, Article 1.2 |
| **后端架构师**（BACKEND） | 国产 Provider 配置示例验证、混合架构方案审查 | Article 1.5 |
| **UI设计师**（UX） | 两篇 Mermaid 图配色方案统一、Alt 文本规范 | 全文图表 |

### 流程规范（Superpowers 工作流映射）

| 阶段 | 本阶段活动 | 交付物 | 负责人 |
|------|-----------|--------|--------|
| **头脑风暴** | 收集 Ch1 五篇文章的读者需求、确定价值主张、识别安全/架构视角缺口 | 需求清单、视角缺口报告 | 需求分析师 |
| **计划** | 将用户故事拆分为技术写作任务、分配团队角色、确定写作顺序 | 写作任务分配表、Sprint 计划 | 敏捷教练 |
| **实施** | 按 Article 1.1 → 1.2 → 1.3 → 1.4 → 1.5 顺序写作，每篇文章包含概念+示例+Mermaid | 5 篇文章初稿 | 各角色按分工执行 |
| **评审** | 架构评审（Article 1.3/1.4）、安全复审（Article 1.1/1.2）、跨文章一致性检查 | 评审报告、修改清单 | 架构顾问 + 安全架构师 |
| **验证** | 验证标准检查、Mermaid 渲染验证、跨章节引用正确性、200 行门槛 | 验证报告 | 测试工程师 |
| **交付** | 合并到 main、更新 _sidebar.md（如需）、通知团队 | 合入确认、变更日志 | 敏捷教练 |

### 评审要求

**检查点 1：理论框架一致性（Article 1.3 → 全书基础）**
- Harness Engineering 定义与 PRD §1 保持一致
- 5 大分类法的术语与后续章节引用一致
- 演进时间线 2024→2026 的数据来源可追溯

**检查点 2：工具对比完备性（Article 1.4）**
- 至少对比 6 款工具的 8 个维度
- 诚实列出 OpenCode 至少 3 个局限性
- 包含选型决策树

**检查点 3：跨文章交叉引用检查**
- Article 1.3 → 后续章节的显式映射说明
- Article 1.4 ↔ Article 1.2 不重复内容
- Article 1.5 → Ch3 §3.4 的衔接

### 质量验收要求

| 门禁类型 | 验收项 | 通过标准 |
|---------|--------|---------|
| 🔴 硬性 | 每篇文章有效行数 | ≥ 200 行 |
| 🔴 硬性 | Mermaid 图表渲染 | 语法正确率 100% |
| 🔴 硬性 | 内部链接有效性 | 无 404 |
| 🟡 质量 | 价值声明块（Ch1 开头） | 包含目标读者/前驱知识/学习收获/投入时间 |
| 🟡 质量 | 术语一致性 | OpenCode 大写 C、英文术语首次出现标注中文 |
| 🟡 质量 | 团队角色评审要求 | 安全/架构视角缺口已关闭 |
| 📊 量化 | Mermaid 图表总数 | ≥ 5 张（时间线图+雷达图+对比矩阵+决策树+架构图） |

### 特殊内容技能映射

| 特殊内容 | 所需技能 | 适用文章 | 说明 |
|---------|---------|---------|------|
| AI 编程三阶段演进时间线图 | `mindmap` / `infographic` | Article 1.1 | Mermaid timeline 语法 |
| Harness Engineer 能力雷达图 | `vega` / `chart-visualization` | Article 1.1 | 5 维度蛛网图 |
| 工具对比矩阵图 | `infographic` / `chart-visualization` | Article 1.4 | 高维数据可视化 |
| 选型决策树 | `mindmap` / `uml` | Article 1.4 | Mermaid decision tree |
| 5 大分类法树形图 | `mindmap` | Article 1.3 | 层级分类树 |
| 混合架构示意图 | `architecture` | Article 1.5 | 分层架构图 |
| 国产工具对比矩阵 | `infographic` | Article 1.5 | 多维度对比表图表化 |
