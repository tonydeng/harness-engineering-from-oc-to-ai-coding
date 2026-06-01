# 什么是 Harness Engineer

> 从"用 AI 写代码的人"到"驾驭 AI Agent 完成工程交付的人"——定义 AI 编程第三时代的核心角色。

## 文章概述

AI 编程工具在短短五年内经历了三次浪潮：从 2021 年的代码补全（GitHub Copilot），到 2024 年的对话编程（Cursor、Claude Code），再到 2026 年的工程流水线（OpenCode）。每一次浪潮都重新定义了开发者与 AI 的关系。**Harness Engineer（驾驭工程师）** 就是第三时代的核心角色——不是简单地用 AI 写代码，而是设计和管理 AI 工程流水线的人。

为什么"对话"不够？单纯依赖聊天式交互带来了四个根本性问题：Token 成本失控（长对话上下文膨胀）、跨 Session 上下文丢失（失忆问题）、生成结果质量不可控（缺乏审查机制）、以及优质工作流无法复用（重复劳动）。更危险的是，当 Agent 获得执行终端命令的权限后，一次误操作可能导致数据泄露、系统崩溃甚至安全入侵——这是"安全失控"痛点，也是推动工程化范式转变的关键驱动力。

本文将从 AI 编程的演进脉络出发，定义 Harness Engineer 的概念与核心能力，并阐述 Harness Engineering 的三大核心原则——**可复现（Reproducible）**、**可审计（Auditable）**、**可改进（Improveable）**。这三大原则贯穿全书，是衡量一切 AI 工程实践的标准。

## AI 编程的三次浪潮

### 阶段 1：提示词工程（Prompt Engineering，2021-2023）

**定义**：通过精心设计的输入指令，最大限度地激发模型的正确能力。

2021 年 6 月，GitHub 与 OpenAI 联合发布 GitHub Copilot，标志着 AI 编程正式进入主流视野。这一阶段的核心特征是**被动响应**：AI 根据光标位置和上下文，预测并补全下一行代码。

```javascript:examples/snippets/copilot-example.js
// 开发者输入函数签名
function calculateTotal(items) {
    // Copilot 自动补全函数体
    return items.reduce((sum, item) => sum + item.price * item.quantity, 0);
}
```

**核心能力**：
- 零样本/少样本提示（Zero-shot/Few-shot Prompting）
- 思维链
- 角色扮演（Role-playing）
- 提示链（Prompt Chaining）

**代表工具**：GitHub Copilot, Tabnine, CodeWhisperer

**用户角色**：操作员—— 需要逐行审查生成代码

**安全关注点**：Prompt Injection 防护

**局限**：
- 单次交互优化，缺乏持久状态
- 上下文窗口受限（4K-8K tokens）
- 无法处理跨文件依赖

### 阶段 2：上下文工程（Context Engineering，2023-2025）

**定义**：设计和构建 AI 系统的信息架构，决定哪些信息进入上下文窗口以及如何组织。

2024 年，Cursor 和 Claude Code 的出现改变了游戏规则。开发者不再只是"接受或拒绝补全"，而是可以通过自然语言与 AI 进行多轮对话，让 AI 理解需求、解释代码、甚至重构整个模块。

这一阶段的核心特征是**单 Agent 聊天交互**：AI 变成了"对话伙伴"，可以回答问题、生成代码、解释原理。但本质上，它仍然是一个"超级聊天机器人"——每次对话都是独立的，缺乏持久记忆和工程化能力。

```markdown
> 用户：帮我重构这个函数，让它更易测试
> 
> Claude：我来分析一下这个函数的问题...
> [生成重构建议]
> 
> 用户：好的，帮我应用这些修改
> 
> Claude：[执行修改]
```

**核心能力**：
- 检索增强生成（RAG）
- 长上下文管理（100K-1M tokens）
- 多文件编辑
- 项目级理解

**代表工具**：Cursor, Sourcegraph Cody, Codeium

**用户角色**：协作者—— 描述需求，审查结果

**安全关注点**：敏感数据过滤、访问控制

**突破**：
- 从"单次交互"到"持久会话"
- 从"文件级"到"项目级"理解
- 从"被动补全"到"主动编辑"

**局限**：
- 仍需人工干预调试
- 缺乏独立执行环境
- 工作流无法固化复用

### 阶段 3：驾驭工程（Harness Engineering，2025-2026 探索期）

**定义**：设计、构建和维护编排 AI Agent 的基础设施，使其在生产环境中可靠运行。

2026 年，OpenCode 引领的 Agent 编排范式标志着 AI 编程进入第三时代。核心特征从"对话"升级为**工程流水线**：多个专业 Agent 协同工作，每个 Agent 负责特定任务（规划、执行、审查），通过 Skill 系统封装领域知识，通过 Workflow 编排复杂流程。

```mermaid
timeline
    title AI 编程演进时间线
    section 阶段 1：提示词工程
        2021 : GitHub Copilot 发布<br/>被动补全模式
        2022 : Tabnine / CodeWhisperer<br/>补全竞争格局
        2023 : Copilot X 预览<br/>对话能力萌芽
    section 阶段 2：上下文工程
        2023 : 长上下文窗口突破<br/>100K tokens
        2024 : Cursor / Claude Code<br/>项目级理解
        2024 : RAG 技术普及<br/>代码库检索
        2025 : Agent 自主执行<br/>单 Agent 时代巅峰
    section 阶段 3：驾驭工程（探索期）
        2025 : 多 Agent 编排兴起<br/>OpenCode / Windsurf
        2026 : Skill 系统成熟<br/>知识可沉淀
        2026 : Workflow 工程化<br/>流水线可复现
```

**核心能力**：
- 多 Agent 编排
- 工作流固化与复用
- 质量门禁与审计日志
- 知识沉淀与持续改进

**三大工程化特性**：
1. **可复现性**（Reproducible）：确定性配置、版本锁定、环境隔离
2. **可审计性**（Auditable）：操作日志、决策追溯、变更审计
3. **可改进性**（Improveable）：效果度量、反馈闭环、A/B 测试

**代表工具**：OpenCode + OMO, Claude Code, Windsurf, Cursor Agent Mode

**用户角色**：观察者/审批者—— 设定目标，验收结果

**安全关注点**：安全审计、沙箱隔离、合规检查

**突破**：
- 从"辅助工具"到"自主系统"
- 从"单 Agent"到"多 Agent 协作"
- 从"不可控"到"工程化"

### 三阶段对比表

| 维度 | 阶段 1：提示词工程 | 阶段 2：上下文工程 | 阶段 3：驾驭工程 |
|------|-------------------|-------------------|-----------------|
| **时间范围** | 2021-2023 | 2023-2025 | 2025-2026（探索期） |
| **代表工具** | GitHub Copilot, Tabnine, CodeWhisperer | Cursor, Sourcegraph Cody, Codeium | OpenCode + OMO, Claude Code, Windsurf, Cursor Agent Mode |
| **交互模式** | 被动补全 | 多轮对话 | Agent 编排 |
| **用户角色** | 操作员 | 协作者 | 观察者/审批者 |
| **AI 角色** | 打字加速器 | 对话伙伴 | 工程执行者 |
| **上下文范围** | 当前文件（4K-8K tokens） | 当前会话（100K-1M tokens） | 跨会话持久化 |
| **执行能力** | 无 | 单步操作 | 多步流水线 |
| **知识复用** | 无 | 无法复用 | Skill 系统 |
| **质量保障** | 无 | 生成即信任 | 审查门禁 |
| **安全关注点** | Prompt Injection 防护 | 敏感数据过滤、访问控制 | 安全审计、沙箱隔离、合规检查 |
| **成本可控性** | 按补全计费 | Token 膨胀失控 | 预算策略 |

## 为什么"对话"不够？

对话编程模式在短期内极大提升了开发效率，但随着使用深入，四个根本性瓶颈逐渐暴露。

### 瓶颈一：Token 成本失控

长对话的上下文会持续累积，每次提问都要携带完整历史。一个 30 分钟的对话可能消耗 50K+ Token，而大多数历史内容与当前任务已无关。

```
Session 开始：5K Token（项目上下文）
↓ 第 10 轮对话：25K Token（历史累积）
↓ 第 20 轮对话：60K Token（继续膨胀）
↓ 第 30 轮对话：120K Token（成本失控）
```

更糟糕的是，Token 膨胀不仅增加成本，还会降低模型推理质量——过多无关上下文会稀释有效信息。

### 瓶颈二：失忆问题

每次启动新 Session，之前的对话历史、项目理解、代码决策全部丢失。开发者被迫重复"教 AI 认识项目"的过程。

```markdown
Session 1（上午）：
> 用户：这个项目使用 React 18 + TypeScript，状态管理用 Zustand...
> AI：明白了，我会记住这些...

Session 2（下午）：
> 用户：帮我添加一个新功能...
> AI：请问这个项目使用什么技术栈？
> 用户：（再次解释 React + TypeScript + Zustand...）
```

这种"金鱼记忆"让 AI 无法积累项目知识，每次都从零开始。

### 瓶颈三：质量不可控

对话模式下，AI 生成的代码"生成即信任"——没有自动审查机制，质量完全依赖开发者的即时判断。当代码量增大、逻辑变复杂时，潜在问题容易被忽略。

```javascript
// AI 生成的代码，看起来正确
async function fetchUserData(userId) {
    const response = await fetch(`/api/users/${userId}`);
    return response.json();
}

// 潜在问题：
// 1. 无错误处理
// 2. 无超时机制
// 3. 无输入验证
// 4. 无类型安全
```

在对话模式下，这些问题需要开发者主动发现并要求修复。而在工程流水线模式下，审查 Agent 会自动检查并生成改进建议。

### 瓶颈四：重复劳动

当你在某个项目中摸索出一套高效的工作流（例如"先分析依赖 → 生成测试 → 实现功能 → 运行验证"），这套流程无法被保存和复用。下一个项目，你又要重新"教"AI 这个流程。

```mermaid
flowchart LR
    subgraph 对话模式
        A1[新项目] --> B1[重新解释需求]
        B1 --> C1[重新设计流程]
        C1 --> D1[重新调试]
    end
    
    subgraph 工程模式
        A2[新项目] --> B2[加载已有 Skill]
        B2 --> C2[执行标准化流程]
        C2 --> D2[自动质量检查]
    end
    
    style A1 fill:#ffcccc
    style B1 fill:#ffcccc
    style C1 fill:#ffcccc
    style D1 fill:#ffcccc
    style A2 fill:#ccffcc
    style B2 fill:#ccffcc
    style C2 fill:#ccffcc
    style D2 fill:#ccffcc
```

### 瓶颈五：安全失控（关键痛点）

当 Agent 获得执行终端命令的权限后，一次误操作可能导致严重后果。这是对话模式最危险的隐患。

**风险场景示例**：

```bash
# 用户意图：删除测试目录
> 用户：删除 test 文件夹

# AI 误判执行
> AI：执行 rm -rf test /
# 注意：多了一个空格，变成删除根目录！

# 或者更隐蔽的风险
> 用户：帮我清理临时文件
> AI：执行 rm -rf /tmp/*
# 可能误删其他程序正在使用的文件
```

**安全失控的具体表现**：

| 风险类型 | 场景描述 | 潜在后果 |
|---------|---------|---------|
| **命令误执行** | AI 理解错误或命令拼接错误 | 数据丢失、系统崩溃 |
| **权限越界** | AI 访问了不该访问的敏感文件 | 数据泄露、合规违规 |
| **代码注入** | AI 生成的代码包含恶意片段 | 安全漏洞、后门植入 |
| **配置篡改** | AI 修改了关键配置文件 | 服务中断、安全策略失效 |
| **凭证泄露** | AI 将密钥写入日志或临时文件 | 凭证暴露、账号被盗 |

在对话模式下，这些风险完全依赖开发者的即时审查——但人总会疲劳、会遗漏。工程流水线模式通过**权限控制**、**审计日志**、**沙箱隔离**等机制，将安全防护系统化。

```mermaid
flowchart TB
    subgraph 对话模式安全
        A1[AI 提议执行命令] --> B1[开发者人工审查]
        B1 -->|通过| C1[执行]
        B1 -->|拒绝| D1[取消]
        C1 --> E1[❌ 无审计日志]
        C1 --> F1[❌ 无回滚机制]
    end
    
    subgraph 工程模式安全
        A2[AI 提议执行命令] --> B2[权限系统检查]
        B2 -->|允许| C2[沙箱执行]
        B2 -->|需确认| D2[开发者确认]
        B2 -->|禁止| E2[自动拒绝]
        C2 --> F2[✅ 审计日志记录]
        C2 --> G2[✅ 可回滚操作]
        D2 --> C2
    end
    
    style E1 fill:#ffcccc
    style F1 fill:#ffcccc
    style F2 fill:#ccffcc
    style G2 fill:#ccffcc
```

## Harness Engineer 定义

### 从 Prompt Engineer 到 Harness Engineer

在定义 Harness Engineer 之前，需要先厘清它与 Prompt Engineer 的区别。

**Prompt Engineer** 关注的是"怎么写好的提示词"——这是战术层面的技巧。例如：

```markdown
# Prompt Engineer 的典型工作
优化提示词：
"你是一个专业的 React 开发者，请帮我实现一个带有分页功能的数据表格组件，
要求：1) 使用 TypeScript 2) 支持排序 3) 支持自定义列渲染..."
```

**Harness Engineer** 关注的是"怎么设计好的工程流水线"——这是战略层面的能力。例如：

```yaml
# Harness Engineer 的典型工作
workflow:
  name: feature-implementation-pipeline
  steps:
    - agent: plan
      skill: requirements-analysis
      output: design-doc
    - agent: build
      skill: tdd-implementation
      input: design-doc
      gates:
        - type: test-coverage
          threshold: 80%
        - type: lint-check
    - agent: review
      skill: code-review
      input: build-output
```

两者的核心差异：

| 维度 | Prompt Engineer | Harness Engineer |
|------|----------------|------------------|
| **关注点** | 单次交互质量 | 流水线整体效能 |
| **时间尺度** | 即时响应 | 长期可维护 |
| **复用性** | 提示词难以复用 | Workflow 可模板化 |
| **质量保障** | 依赖人工判断 | 自动化门禁 |
| **能力沉淀** | 个人经验 | 组织知识库 |

### Mitchell Hashimoto 的原始定义

**Mitchell Hashimoto**（HashiCorp 创始人）在 2024 年首次提出 Harness Engineer 概念：

> "The future of programming is not about writing code, but about **harnessing** AI systems to write code. A Harness Engineer doesn't just prompt an AI—they design the systems, constraints, and workflows that make AI output reliable, reproducible, and valuable."
> 
> "编程的未来不是写代码，而是**驾驭** AI 系统来写代码。Harness Engineer 不仅仅是给 AI 发指令——他们设计系统、约束和工作流，使 AI 的输出可靠、可复现、有价值。"

这个定义的关键词是 **Harness（驾驭）**，而非 **Use（使用）** 或 **Prompt（提示）**。"驾驭"意味着：

1. **主动设计**：不是被动接受 AI 输出，而是主动设计 AI 的行为边界
2. **系统思维**：不是单点优化，而是端到端的系统设计
3. **可控性**：AI 的每一步操作都在预期范围内，可预测、可干预

### Harrison Chase 的 Agent 公式

**Harrison Chase**（LangChain 创始人）进一步将 Harness 的概念形式化，提出了著名的 Agent 公式：

$$\text{Agent} = \text{Model} + \text{Harness}$$

这个公式揭示了一个深刻洞见：**Agent 不等于 Model**。

- **Model（模型）**：大语言模型本身，如 GPT-4、Claude、Gemini。它提供推理能力，但本身不具备执行能力。
- **Harness（驾驭框架）**：围绕模型的工程化框架，包括工具调用、权限控制、上下文管理、错误处理、审计日志等。

```mermaid
flowchart LR
    subgraph Model
        M1[推理能力]
        M2[知识储备]
        M3[语言理解]
    end
    
    subgraph Harness
        H1[工具调用]
        H2[权限控制]
        H3[上下文管理]
        H4[错误处理]
        H5[审计日志]
    end
    
    Model --> Agent
    Harness --> Agent
    
    Agent[Agent<br/>完整执行单元]
    
    style Model fill:#4A90D9,color:#fff
    style Harness fill:#50C878,color:#fff
    style Agent fill:#FF9F43,color:#fff
```

**为什么这个公式重要？**

它解释了为什么"同样的模型"在不同工具上表现迥异：

| 工具 | Model | Harness | Agent 能力 |
|------|-------|---------|-----------|
| ChatGPT | GPT-4 | 基础对话 | 只能聊天 |
| GitHub Copilot | GPT-4 | 编辑器集成 | 代码补全 |
| Cursor | Claude/GPT-4 | IDE + 对话 | 对话编程 |
| OpenCode | 多模型可选 | Agent 编排 + Skill + Workflow | 工程流水线 |

同样的底层模型，不同的 Harness，产生截然不同的 Agent 能力。Harness Engineer 的核心工作，就是设计和管理这个 Harness 层。

### Harness Engineer 的五大核心能力

基于以上定义，我们可以提炼出 Harness Engineer 的五大核心能力框架：

| 能力维度 | 能力要求 | 入门水平 | 差距 |
|---------|---------|---------|-----|
| 需求澄清 | 85 | 35 | +50 |
| 工作流设计 | 90 | 30 | +60 |
| Agent 编排 | 88 | 25 | +63 |
| 质量审查 | 82 | 40 | +42 |
| 知识沉淀 | 78 | 20 | +58 |

#### 1. 需求澄清能力

将模糊的业务需求转化为 AI 可执行的任务规格。

```markdown
# 模糊需求
"帮我做一个用户登录功能"

# 澄清后的任务规格
任务：实现用户登录功能
技术栈：React + Node.js + JWT
验收标准：
  - 支持邮箱/手机号登录
  - 密码错误 5 次锁定账户
  - 登录状态 7 天有效
  - 单元测试覆盖率 ≥ 80%
约束条件：
  - 不存储明文密码
  - 使用 HTTPS 传输
```

#### 2. 工作流设计能力

将复杂任务分解为可编排的步骤序列。

```yaml
workflow:
  name: user-auth-implementation
  steps:
    - step: design
      agent: plan
      skill: architecture-design
      output: architecture.md
    
    - step: implement
      agent: build
      skill: tdd-development
      input: architecture.md
      gates:
        - test-coverage >= 80%
        - no-security-warnings
    
    - step: review
      agent: review
      skill: security-review
      input: implementation
      output: review-report
```

#### 3. Agent 编排能力

理解不同 Agent 的能力边界，合理分配任务。

```mermaid
flowchart TB
    Task[复杂任务] --> Plan[Plan Agent<br/>需求分析+架构设计]
    Plan --> Build[Build Agent<br/>代码实现]
    Plan --> Explore[Explore Agent<br/>代码探索]
    Explore --> Build
    Build --> Review[Review Agent<br/>质量审查]
    Review --> |通过| Done[交付]
    Review --> |问题| Build
    
    style Plan fill:#4A90D9,color:#fff
    style Build fill:#50C878,color:#fff
    style Explore fill:#A66CFF,color:#fff
    style Review fill:#FF9F43,color:#fff
```

#### 4. 质量审查能力

建立自动化质量门禁，而非依赖人工检查。

```yaml:examples/quality-gates/example-gates.yaml
quality_gates:
  - name: test-coverage
    condition: coverage >= 80%
    action: block_if_failed
  
  - name: lint-check
    condition: no-errors
    action: warn_if_failed
  
  - name: security-scan
    condition: no-critical-vulnerabilities
    action: block_if_failed
  
  - name: code-review
    condition: approved-by-review-agent
    action: block_if_failed
```

#### 5. 知识沉淀能力

将项目经验转化为可复用的 Skill 和 Workflow。

```markdown
# Skill: react-component-tdd

## 描述
使用测试驱动开发模式实现 React 组件

## 工作流
1. 分析组件需求，编写测试用例
2. 实现最小代码通过测试
3. 重构优化代码
4. 运行完整测试套件

## 输出规范
- 组件源码：src/components/{ComponentName}.tsx
- 测试文件：src/components/{ComponentName}.test.tsx
- 文档：src/components/{ComponentName}.md
```

## Harness Engineering 的三大核心原则

Harness Engineering 的所有实践都围绕三个核心原则展开：**可复现**、**可审计**、**可改进**。这三个原则是衡量一切 AI 工程实践的标准。

### 原则一：可复现（Reproducible）

**定义**：同样的输入，经过同样的流水线，得到同样质量的输出。

**为什么重要**：AI 模型的输出具有随机性（Temperature 参数、采样策略）。如果没有工程化约束，同样的需求可能得到截然不同的结果。可复现性消除了这种不确定性。

**实现机制**：

| 机制 | 说明 |
|------|------|
| **确定性配置** | 固定 Temperature、Seed 等参数 |
| **版本锁定** | Skill、Workflow、Model 版本明确记录 |
| **环境隔离** | 项目级配置，避免全局污染 |
| **输入标准化** | 任务规格模板化，减少歧义 |

**示例**：

```yaml
# 可复现的配置
workflow:
  name: feature-implementation
  version: 1.2.0
  model: claude-3-opus
  model_config:
    temperature: 0.1
    seed: 42
  skill: tdd-development@2.1.0
```

### 原则二：可审计（Auditable）

**定义**：每一步操作有记录、可回放、可审查。

**为什么重要**：当 AI 获得执行权限后，必须知道它"做了什么"、"为什么做"、"结果如何"。可审计性是安全合规的基础，也是问题排查的关键。

**实现机制**：

| 机制 | 说明 |
|------|------|
| **操作日志** | 记录每次工具调用、文件修改、命令执行 |
| **决策追溯** | 记录 AI 的推理过程和决策依据 |
| **变更审计** | 记录谁在何时修改了什么配置 |
| **合规映射** | 日志格式符合 NIST/SOC2/等保要求 |

**安全审计日志示例**：

```json:examples/audit-logs/security-audit.json
{
  "timestamp": "2026-06-01T14:32:15Z",
  "session_id": "sess-abc123",
  "agent": "build",
  "action": "file_write",
  "target": "src/auth/login.ts",
  "reason": "实现登录功能",
  "changes": {
    "lines_added": 45,
    "lines_removed": 3
  },
  "approval": {
    "required": true,
    "granted_by": "developer@example.com",
    "granted_at": "2026-06-01T14:32:10Z"
  }
}
```

**与安全审计的关联**：

可审计原则直接支撑安全合规：

- **事后追责**：发生安全事件时，可追溯操作链
- **合规证明**：审计日志是 SOC2/等保的必要证据
- **异常检测**：通过日志分析发现异常行为模式
- **权限审查**：定期审查权限使用情况，优化策略

### 原则三：可改进（Improveable）

**定义**：从每次运行中学习，持续优化流水线。

**为什么重要**：AI 编程是新兴领域，最佳实践仍在快速演进。如果流水线是"黑盒"，就无法从经验中学习。可改进性确保持续优化。

**实现机制**：

| 机制 | 说明 |
|------|------|
| **效果度量** | 记录每次运行的耗时、Token 消耗、质量指标 |
| **反馈闭环** | 开发者评价、问题记录、改进建议 |
| **A/B 测试** | 对比不同配置的效果差异 |
| **版本演进** | Skill/Workflow 的版本管理和变更日志 |

**改进循环**：

```mermaid
flowchart LR
    A[执行流水线] --> B[记录效果数据]
    B --> C[分析改进点]
    C --> D[更新 Skill/Workflow]
    D --> A
    
    style A fill:#4A90D9,color:#fff
    style B fill:#50C878,color:#fff
    style C fill:#FF9F43,color:#fff
    style D fill:#A66CFF,color:#fff
```

**度量指标示例**：

```yaml
metrics:
  efficiency:
    - avg_task_duration: 15min
    - avg_token_consumption: 12K
    - first_pass_success_rate: 78%
  
  quality:
    - test_coverage: 85%
    - lint_error_rate: 2%
    - security_issue_rate: 0%
  
  improvement:
    - last_month_success_rate: 72%
    - this_month_success_rate: 78%
    - improvement: +6%
```

## 小结

Harness Engineer 是 AI 编程第三时代的核心角色。他们不是简单地"用 AI 写代码"，而是：

1. **设计** AI 工程流水线（Workflow）
2. **编排** 多个专业 Agent（Agent Orchestration）
3. **建立** 质量门禁和审查机制（Quality Gates）
4. **沉淀** 可复用的领域知识（Skill System）
5. **保障** 安全可控的执行环境（Security Harness）

Harness Engineering 的三大原则——可复现、可审计、可改进——是贯穿全书的指导思想。下一篇文章将探讨"为什么选择 OpenCode"，看看 OpenCode 如何成为承载 Harness Engineering 理念的最佳平台。

## 关联章节

- → [为什么选择 OpenCode](why-opencode.md)（理解概念后，自然延伸至工具选择）
- → [Harness Engineering 理论框架](harness-engineering-theory.md)（从概念到理论的深化）
- → [核心概念](../02-core-concepts/)（为理解 Agent、Skill、Workflow 等概念奠定基础）
- → [工作流实战](../04-workflows/)（工程流水线的具体实现与最佳实践）
- ← 承接 [读者导航](../00-guide/)（建立对全书结构的基本认知后，从这里正式开始）
