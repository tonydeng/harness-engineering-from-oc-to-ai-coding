# oh-my-openagent 概览

## 项目定位

**oh-my-openagent** 是 OpenCode 的多模型 Agent 编排系统，将单个 AI Agent 转换为协调的开发团队。它打破了单一模型的限制，让不同专长的 Agent 协同工作，实现更高效、更专业的 AI 辅助开发体验。

## 核心理念

### 模型无关设计

oh-my-openagent 不绑定任何模型提供商，支持：

- **Anthropic Claude** (Opus, Sonnet, Haiku)
- **OpenAI** (GPT 系列)
- **Google** (Gemini 系列)
- **国内模型** (Kimi、DeepSeek 等)
- **75+ Provider** 通过 OpenCode 集成

### 智能任务路由

通过 **Category 系统** 自动将任务路由到最合适的模型：

- 复杂推理任务 → 高能力模型 (Claude Opus, GPT-5)
- 快速响应任务 → 轻量模型 (GPT-5.4-mini-fast)
- 视觉分析任务 → 多模态模型

### 专业化分工协作

每个 Agent 专注于特定领域，形成类似人类团队的协作模式：

- 规划者负责战略
- 执行者负责实施
- 审查者负责质量把控

## 三层架构

```mermaid
flowchart TB
    subgraph Planning["规划层 Planning Layer"]
        User[用户请求]
        Prometheus[Prometheus<br/>战略规划师]
        Metis[Metis<br/>缺口分析]
        Momus[Momus<br/>严格审查]
    end

    subgraph Execution["执行层 Execution Layer"]
        Atlas[Atlas<br/>执行指挥]
    end

    subgraph Worker["工作层 Worker Layer"]
        SJ[Sisyphus-Junior<br/>任务执行]
        Oracle[Oracle<br/>架构顾问]
        Explore[Explore<br/>代码搜索]
        Librarian[Librarian<br/>文档搜索]
        VE[visual-engineering<br/>视觉工程]
    end

    User --> Prometheus
    Prometheus --> Metis
    Metis --> Momus
    Momus --> Atlas
    Atlas --> SJ
    Atlas --> Oracle
    Atlas --> Explore
    Atlas --> Librarian
    Atlas --> VE

    style Prometheus fill:#4A90D9
    style Metis fill:#4A90D9
    style Momus fill:#4A90D9
    style Atlas fill:#50C878
    style SJ fill:#FF9F43
    style Oracle fill:#FF9F43
    style Explore fill:#FF9F43
    style Librarian fill:#FF9F43
    style VE fill:#FF9F43
```

### 架构说明

| 层级 | 职责 | Agent |
|------|------|-------|
| **规划层** | 理解需求、制定计划、审查方案 | Prometheus, Metis, Momus |
| **执行层** | 协调任务、分配工作 | Atlas |
| **工作层** | 执行具体任务、提供专业能力 | Sisyphus-Junior, Oracle, Explore, Librarian, visual-engineering |

## 11 个内置 Agent

```mermaid
flowchart LR
    subgraph Coordinators["编排器"]
        Sisyphus[Sisyphus<br/>主编排器]
        Hephaestus[Hephaestus<br/>GPT 原生自主 Agent]
    end

    subgraph Planners["规划者"]
        Prometheus[Prometheus<br/>战略规划师]
        Metis[Metis<br/>缺口分析]
        Momus[Momus<br/>严格审查]
    end

    subgraph Executors["执行者"]
        Atlas[Atlas<br/>执行指挥]
        SJ[Sisyphus-Junior<br/>任务执行]
    end

    subgraph Specialists["专家"]
        Oracle[Oracle<br/>架构顾问]
        Librarian[Librarian<br/>文档搜索]
        Explore[Explore<br/>代码搜索]
        ML[Multimodal Looker<br/>视觉分析]
    end

    style Sisyphus fill:#4A90D9
    style Hephaestus fill:#4A90D9
    style Prometheus fill:#50C878
    style Metis fill:#50C878
    style Momus fill:#50C878
    style Atlas fill:#FF9F43
    style SJ fill:#FF9F43
    style Oracle fill:#A66CFF
    style Librarian fill:#A66CFF
    style Explore fill:#A66CFF
    style ML fill:#A66CFF
```

### Agent 详细说明

| Agent | 职责 | 推荐模型 | 说明 |
|-------|------|---------|------|
| **Sisyphus** | 主编排器 | Claude Opus 4.7 / Kimi K2.6 | 系统核心，协调所有 Agent 的工作流程 |
| **Hephaestus** | GPT 原生自主 Agent | GPT-5.5 | 专为 OpenAI 模型优化的自主执行 Agent |
| **Prometheus** | 战略规划师 | Claude Opus 4.7 / GPT-5.5 | 分析需求，制定高层策略和实施路线图 |
| **Atlas** | 执行指挥 | Claude Sonnet 4.6 / Kimi K2.6 | 将计划分解为具体任务，协调执行 |
| **Oracle** | 架构顾问 | GPT-5.5 / Claude Opus 4.7 | 提供架构建议，评估技术方案 |
| **Librarian** | 文档搜索 | GPT-5.4-mini-fast | 快速检索项目文档和知识库 |
| **Explore** | 代码搜索 | GPT-5.4-mini-fast | 在代码库中定位相关代码片段 |
| **Metis** | 缺口分析 | Claude Sonnet 4.6 | 识别方案中的遗漏和不足 |
| **Momus** | 严格审查 | GPT-5.5 | 批判性审查，确保方案质量 |
| **Multimodal Looker** | 视觉分析 | GPT-5.5 | 分析图像、图表等视觉内容 |
| **Sisyphus-Junior** | 任务执行 | Claude Sonnet 4.6 | 执行具体开发任务 |

### Agent 分类

```mermaid
mindmap
  root((oh-my-openagent))
    编排器
      Sisyphus
        主编排器
        系统入口
      Hephaestus
        GPT 原生
        自主执行
    规划者
      Prometheus
        战略规划
        路线图
      Metis
        缺口分析
        完整性检查
      Momus
        严格审查
        质量把控
    执行者
      Atlas
        任务分解
        执行协调
      Sisyphus-Junior
        具体实现
        代码编写
    专家
      Oracle
        架构建议
        技术评估
      Librarian
        文档检索
        知识管理
      Explore
        代码搜索
        上下文定位
      Multimodal Looker
        视觉分析
        图像理解
```

## 与 OpenCode 集成

### 配置文件

oh-my-openagent 通过 `.opencode/oh-my-openagent.json` 配置：

```json
{
  "agents": {
    "sisyphus": {
      "model": "claude-opus-4-7",
      "category": "reasoning"
    },
    "atlas": {
      "model": "claude-sonnet-4-6",
      "category": "execution"
    },
    "librarian": {
      "model": "gpt-5-4-mini-fast",
      "category": "search"
    }
  },
  "workflows": {
    "planning": ["prometheus", "metis", "momus"],
    "execution": ["atlas", "sisyphus-junior"],
    "consultation": ["oracle"]
  }
}
```

### 安装方式

```bash
# 通过 bunx 安装
bunx oh-my-opencode install

# 或手动配置
mkdir -p .opencode
cp oh-my-openagent.json .opencode/
```

### Provider 支持

通过 OpenCode 的统一接口，oh-my-openagent 支持 **75+ Provider**：

| 类型 | Provider 示例 |
|------|--------------|
| 国际云服务 | OpenAI, Anthropic, Google AI, AWS Bedrock, Azure OpenAI |
| 国内云服务 | 阿里云百炼, 百度千帆, 腾讯混元, 智谱 AI |
| 开源模型托管 | Together AI, Fireworks, Replicate, Hugging Face |
| 本地部署 | Ollama, vLLM, LocalAI |

## 工作流示例

### 代码审查工作流

```mermaid
sequenceDiagram
    participant User as 用户
    participant Sisyphus as Sisyphus<br/>编排器
    participant Prometheus as Prometheus<br/>规划师
    participant Explore as Explore<br/>代码搜索
    participant Momus as Momus<br/>审查员

    User->>Sisyphus: 请求代码审查
    Sisyphus->>Prometheus: 分析审查范围
    Prometheus->>Explore: 定位相关代码
    Explore-->>Prometheus: 返回代码片段
    Prometheus->>Momus: 提交审查请求
    Momus-->>Sisyphus: 返回审查报告
    Sisyphus-->>User: 输出结果
```

### 架构设计工作流

```mermaid
sequenceDiagram
    participant User as 用户
    participant Sisyphus as Sisyphus<br/>编排器
    participant Prometheus as Prometheus<br/>规划师
    participant Oracle as Oracle<br/>架构师
    participant Metis as Metis<br/>分析员
    participant Momus as Momus<br/>审查员

    User->>Sisyphus: 提交架构需求
    Sisyphus->>Prometheus: 制定设计方案
    Prometheus->>Oracle: 请求架构建议
    Oracle-->>Prometheus: 提供架构方案
    Prometheus->>Metis: 缺口分析
    Metis-->>Prometheus: 补充建议
    Prometheus->>Momus: 方案审查
    Momus-->>Sisyphus: 最终方案
    Sisyphus-->>User: 输出架构设计
```

## 最佳实践

### 模型选择策略

| 任务类型 | 推荐配置 | 原因 |
|---------|---------|------|
| 复杂架构设计 | Prometheus + Oracle (Opus/GPT-5) | 需要深度推理能力 |
| 快速代码搜索 | Explore + Librarian (mini-fast) | 响应速度快，成本低 |
| 严格质量审查 | Momus (GPT-5.5) | 批判性思维强 |
| 日常开发任务 | Atlas + Sisyphus-Junior (Sonnet/Kimi) | 性价比高 |

### 成本优化

1. **分层使用模型**：规划用强模型，执行用中等模型，搜索用轻量模型
2. **缓存结果**：Librarian 和 Explore 的搜索结果可复用
3. **并行执行**：多个独立任务可由 Atlas 并行分配

### 调试技巧

```bash
# 查看当前 Agent 配置
opencode agents list

# 查看特定 Agent 状态
opencode agents show sisyphus

# 测试 Agent 响应
opencode agents test prometheus "设计一个用户认证系统"
```

## 相关资源

- **OpenCode 官方文档**: https://opencode.ai/docs
- **oh-my-openagent 仓库**: https://github.com/anomalyco/oh-my-openagent
- **OpenCode GitHub**: https://github.com/anomalyco/opencode

---

> 本文档是 OpenCode 生态系统的一部分，更多内容请参考本书其他章节。
