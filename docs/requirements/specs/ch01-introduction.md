# Ch1: 简介

## 概述

本书第1章为全书定调：先说清楚什么是"Harness Engineer"（驾驭式工程师），再解释为什么AI编程正在从"跟 AI 聊天写代码"转向"用工程体系做开发"，以及OpenCode在这股浪潮里的位置。读完本章你就能快速判断：这本书和OpenCode值不值得你花时间。

**章节核心主题**：从"跟 AI 聊天写代码"到"用工程体系做开发"——讲明白 Harness Engineering 是什么、为什么重要、用什么工具来实现。

> **章节规模**：6 篇文章（3 现有 + 3 新增），2 篇修改

### 创作辅助

本章内容创作和评审中推荐配备以下智能体组合：

| 类型 | 推荐 | 理由 |
|------|------|------|
| **思维框架** | 没有调查没有发言权（比较研究前先调查）、矛盾论（抓核心痛点） | 简介定义全书基调，需要有力的叙事和令人信服的价值主张 |
| **人物视角** | Paul Graham（散文式叙事）、张一鸣（产品思维）、Jobs（现实扭曲力场） | 同上 |
| **启用阶段** | 初稿（视角驱动）+ 审校（框架验证） | 初稿时用人物视角打开思路，审校时用思维框架检查逻辑 |



## 文章

### Article 1.1: 什么是 Harness Engineer
- **阅读时间**：15 min
- **学习目标**：
  - 理解AI编程三阶段演进：提示词工程(2021-2023)→上下文工程(2023-2025)→驾驭工程(2025-2026 探索期)
  - 定义"Harness Engineer"：不是"用AI写代码的人"，而是"驾驭AI Agent完成工程交付的人"
  - 理解Harness Engineer的5个核心能力：需求澄清、工作流设计、Agent编排、质量审查、知识沉淀
- **前置知识**：无（本文章是全书起点）
- **源材料映射**：OpenCode实战 01（概念速通，OS类比部分）+ OpenCode实战 04（Profile切换/AGENTS.md理念）

#### 大纲
1. AI编程的三阶段演进
   - 阶段 1：提示词工程（Prompt Engineering，2021-2023）
     - 核心能力：零样本/少样本提示、思维链（CoT）、角色扮演、提示链
     - 国际代表工具：GitHub Copilot（$2B+ ARR, 2000万用户）, Google Gemini Code Assist, OpenAI Codex（历史意义）
     - 国内代表工具：CodeGeeX（智谱AI，开源可私有化）, 文心快码（百度，IDC 8项满分）, 通义灵码（阿里，Gartner挑战者）
     - 用户角色：操作员（Operator）—— 需要逐行审查生成代码
     - 安全关注点：Prompt Injection 防护
     - 局限：单次交互优化，缺乏持久状态；上下文窗口受限（4K-8K tokens）；无法处理跨文件依赖
   - 阶段 2：上下文工程（Context Engineering，2023-2025）
     - 核心能力：检索增强生成（RAG）、长上下文管理（100K-1M tokens）、多文件编辑、项目级理解
     - 国际代表工具：Cursor（$293亿估值，$2B+ ARR）, Windsurf（Cascade Agent）, Google Project IDX, OpenAI ChatGPT Code Interpreter
     - 国内代表工具：Trae/MarsCode（字节，25%市场份额）, CodeBuddy（腾讯，92%复杂任务完成率）, CodeArts Snap（华为，鸿蒙生态）
     - 用户角色：协作者（Collaborator）—— 描述需求，审查结果
     - 安全关注点：敏感数据过滤、访问控制
     - 突破：从"单次交互"到"持久会话"；从"文件级"到"项目级"理解；从"被动补全"到"主动编辑"
     - 局限：仍需人工干预调试；缺乏独立执行环境；工作流无法固化复用
   - 阶段 3：驾驭工程（Harness Engineering，2025-2026 探索期）
     - 核心能力：多 Agent 编排、工作流固化与复用、质量门禁与审计日志、知识沉淀与持续改进
     - 国际代表工具：Claude Code（Anthropic，72-79% SWE-bench）, OpenCode + OMO, Google Jules（异步自主Agent）, OpenAI Codex CLI, GitHub Copilot Workspace
     - 国内代表工具：Trae SOLO模式（字节）, CodeBuddy Craft智能体（腾讯）
     - 用户角色：观察者/审批者（Observer/Approver）—— 设定目标，验收结果
     - 安全关注点：安全审计、沙箱隔离、合规检查
     - 突破：从"辅助工具"到"自主系统"；从"单 Agent"到"多 Agent 协作"；从"不可控"到"工程化"
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
- **三阶段演进模型**：提示词工程 → 上下文工程 → 驾驭工程，这是全书的理论基石
- **阶段 1（提示词工程）**：通过精心设计的输入指令，最大限度地激发模型的正确能力
- **阶段 2（上下文工程）**：设计和构建 AI 系统的信息架构，决定哪些信息进入上下文窗口以及如何组织
- **阶段 3（驾驭工程）**：设计、构建和维护编排 AI Agent 的基础设施，使其在生产环境中可靠运行
- **Harness Engineer vs Prompt Engineer**：Prompt Engineer关心"怎么写好提示词"；Harness Engineer关心"怎么设计一套可靠的工程体系"
- **3个可**原则：可复现/可审计/可改进——全书所有实践都围绕这三个原则展开
- **安全治理演进**：从 Prompt Injection 防护 → 敏感数据过滤/访问控制 → 安全审计/沙箱隔离/合规检查

#### 代码/配置示例
- 无（本章以概念阐述为主）

#### Mermaid 图表
- AI编程三阶段演进时间线图（2021-2026，标注探索期）
- 三阶段对比矩阵图（时间范围、核心能力、代表工具、用户角色、安全关注点）

#### 关联章节
- → Ch2 Core Concepts（为六概念奠定理解基础）
- → Ch4 Workflows（工作流的实际应用）

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 包含三阶段演进对比表（时间范围、核心能力、代表工具、用户角色、安全关注点）
- [ ] 每个阶段有明确的时间节点
- [ ] 每个阶段有代表性的工具示例
- [ ] 每个阶段有核心特征描述
- [ ] 阶段 3 明确标注为"探索期"
- [ ] 安全治理维度贯穿三个阶段


**创作辅助**:
- 思维框架：矛盾论（抓核心痛点）
- 人物视角：张一鸣（产品思维）
- 理由：定义全书价值主张，需要说服力

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


**创作辅助**:
- 思维框架：没有调查没有发言权（对比前充分调研）
- 人物视角：Musk（第一性原理）
- 理由：工具对比需要客观深入

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
    - 从"驾驭 AI 写代码"到"设计 AI 工程体系"
    - Harness 的 4 个核心支柱：编排、安全、可观测、成本
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


**创作辅助**:
- 思维框架：实践论（理论框架经实际案例验证）
- 人物视角：Karpathy（工程现实主义）
- 理由：理论框架是全书方法论基础

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
   - OpenCode / Cursor / Claude Code / Windsurf / Cline / Continue
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

#### 工具生态对比

**来源**：awesome-opencode 项目

**AI 编程三阶段演进代表工具**：

| 阶段 | 时间范围 | 国际代表工具 | 国内代表工具 |
|------|---------|-------------|-------------|
| **阶段 1：提示词工程** | 2021-2023 | GitHub Copilot ($2B+ ARR), Google Gemini Code Assist, OpenAI Codex | CodeGeeX (智谱AI, 开源可私有化), 文心快码 (百度, IDC 8项满分), 通义灵码 (阿里, Gartner挑战者) |
| **阶段 2：上下文工程** | 2023-2025 | Cursor ($293亿估值), Windsurf (Cascade Agent), Google Project IDX, ChatGPT Code Interpreter | Trae/MarsCode (字节, 25%市场份额), CodeBuddy (腾讯, 92%复杂任务完成率), CodeArts Snap (华为, 鸿蒙生态) |
| **阶段 3：驾驭工程** | 2025-2026 探索期 | Claude Code (72-79% SWE-bench), OpenCode + OMO, Google Jules, OpenAI Codex CLI, GitHub Copilot Workspace | Trae SOLO模式 (字节), CodeBuddy Craft智能体 (腾讯) |

**6 大 AI 编码工具对比**：

| 工具 | 核心优势 | 适用场景 | 国产替代 |
|------|---------|---------|---------|
| **OpenCode** | 开源、可扩展、多模型支持 | 个人开发者、团队协作 | 原生支持国产模型 |
| **Cursor** | IDE 集成、代码补全 | 快速编码 | 通义灵码、CodeGeeX |
| **Windsurf** | AI 原生 IDE | 全栈开发 | - |
| **Cline** | VSCode 插件 | VSCode 用户 | - |
| **Aider** | 命令行工具 | 终端用户 | - |
| **Trae** | 字节跳动出品 | 国内用户 | 原生 |

**选型决策树**：
1. 需要开源？→ OpenCode / Aider
2. 需要 IDE 集成？→ Cursor / Windsurf / Cline
3. 需要国产模型？→ OpenCode / 通义灵码 / CodeGeeX
4. 需要多 Agent？→ OpenCode + OMO

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 对比表覆盖至少 6 款工具的 8 个维度
- [ ] 包含场景化选型决策树


**创作辅助**:
- 思维框架：统筹兼顾（多维度对比平衡）
- 人物视角：Karpathy（工程严谨性）
- 理由：工具生态对比需要结构化评估

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

#### 国产 AI 生态

**来源**：awesome-opencode 项目

**国产模型 Provider**：

| Provider | 模型 | 特点 | OpenCode 配置 |
|---------|------|------|--------------|
| **DeepSeek** | deepseek-chat | 性价比之王 | `deepseek` |
| **Kimi** | moonshot-v1 | 长上下文 | `moonshot` |
| **Qwen** | qwen-turbo | 生态完整 | `qwen` |
| **智谱 AI** | glm-4 | 国产大模型 | `zhipu` |
| **百度文心** | ernie-4 | 企业级 | `ernie` |

**国产工具生态**：

| 工具 | 功能 | 仓库 |
|------|------|------|
| **Qwen Code OAI Proxy** | 通义千问 OpenAI 兼容代理 | `aptdnfapt/qwen-code-oai-proxy` |
| **Gemini CLI to API** | Gemini CLI 转 OpenAI 端点 | `gzzhongqi/geminicli2api` |
| **GolemBot** | 统一 AI 助手框架（支持飞书） | - |
| **opencode-mystatus** | 配额检查（支持智谱 AI） | - |

**国产模型混合架构**：
- DeepSeek（低成本）+ GPT-4（高质量）混合使用
- 国产模型处理常规任务，国际模型处理复杂任务
- 成本优化可达 50%-80%

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 覆盖至少 4 款国产工具
- [ ] 包含国产模型与 OpenCode 结合方案


**创作辅助**:
- 思维框架：星星之火（国产生态刚起步，找最小可用路径）
- 人物视角：张一鸣（本土化策略）
- 理由：国产模型生态需务实视角

---

### Article 1.6: AI 编程失败案例
- **阅读时间**：15 min
- **学习目标**：
  - 理解缺少约束系统、上下文注入攻击、权限配置错误等常见陷阱
  - 从真实失败案例中汲取经验，避免在自身项目中重蹈覆辙
  - 理解 Harness Engineering 核心支柱（约束系统、审计、验证护栏）如何防范这些风险
- **前置知识**：Article 1.1（Harness Engineer 基础概念）
- **源材料映射**：全书实践经验总结

#### 大纲
1. 案例一：没有约束系统会发生什么
   - 场景：AI Agent 失控修改了生产数据库
   - 根因分析：缺少 Bash 白名单、缺少文件路径约束
   - Harness Engineering 的解决方案：约束系统、权限分层
2. 案例二：上下文注入攻击实例
   - 场景：恶意代码通过 README 注入 Agent 上下文
   - 根因分析：缺少注入防护、过分信任外部输入
   - Harness Engineering 的解决方案：CLAUDE.md 用户指令覆盖层、沙箱隔离
3. 案例三：权限配置错误案例
   - 场景：Skill 权限过大导致敏感信息泄露
   - 根因分析：最小权限原则未被遵守、缺乏审计
   - Harness Engineering 的解决方案：权限模型、审计日志
4. 经验总结
   - 从失败到工程化的逆向思考
   - 预防性设计 vs 事后补救

#### 核心概念
- **预防性设计**：在问题发生之前通过工程化手段预防，而非在问题发生后补救
- **逆向思考**：从"什么情况下会失败"反向推导应该做什么
- **约束即自由**：合理的约束能防止灾难性错误，让 Agent 在安全范围内发挥最大效能

#### 代码/配置示例
- Bash 白名单配置示例
- CLAUDE.md 用户指令覆盖层示例
- Skill 最小权限配置示例

#### 关联章节
- ← Article 1.1（Harness Engineer 的核心能力）
- → Ch2（约束系统、验证护栏的概念基础）
- → Ch6（安全总览、沙箱 Hook 系统）

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容（当前 427 行 ✅）
- [ ] 包含至少 3 个真实场景改编的失败案例
- [ ] 每个案例包含根因分析和 Harness Engineering 解决方案
- [ ] 包含经验总结章节


**创作辅助**:
- 思维框架：批评与自我批评（从失败中学习）
- 人物视角：Feynman（反自欺）
- 理由：失败案例需要深度反思

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
| **头脑风暴** | 收集 Ch1 六篇文章的读者需求、确定价值主张、识别安全/架构视角缺口 | 需求清单、视角缺口报告 | 需求分析师 |
| **计划** | 将用户故事拆分为技术写作任务、分配团队角色、确定写作顺序 | 写作任务分配表、Sprint 计划 | 敏捷教练 |
| **实施** | 按 Article 1.1 → 1.2 → 1.3 → 1.4 → 1.5 → 1.6 顺序写作，每篇文章包含概念+示例+Mermaid | 6 篇文章初稿 | 各角色按分工执行 |
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
| 工具对比矩阵图 | `infographic` / `chart-visualization` | Article 1.4 | 高维数据可视化 |
| 选型决策树 | `mindmap` / `uml` | Article 1.4 | Mermaid decision tree |
| 5 大分类法树形图 | `mindmap` | Article 1.3 | 层级分类树 |
| 混合架构示意图 | `architecture` | Article 1.5 | 分层架构图 |
| 国产工具对比矩阵 | `infographic` | Article 1.5 | 多维度对比表图表化 |
