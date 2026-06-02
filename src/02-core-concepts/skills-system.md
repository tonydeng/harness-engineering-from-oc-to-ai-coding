# Skill 系统

> 理解 Skill 的结构规范、发现路径与加载机制——从定义领域知识包到实现精确权限控制。

> **前置条件**
> - 已完成 [Agent 编排](agent-orchestration.md)，理解 Agent 的加载和执行机制
> - 已安装 OpenCode CLI 并完成基础配置
> - 已了解 YAML frontmatter 和 Markdown 格式

## 文章概述

Skill 是 OpenCode 中封装领域知识的核心载体，它让 Agent 不必每次从零学习，而是像加载驱动程序一样按需获取专业技能。本章节详细讲解 SKILL.md 的完整格式规范，包括 frontmatter 元数据字段（name、description、allowed-tools、target_agent）、正文结构（工作流 + 指令 + 输出规范）以及捆绑资源目录（scripts/、templates/、reference/）。读者将理解 Skill 与普通 Prompt 的核心差异——权限控制、工具绑定和元数据索引——这是 Skill 能够工程化复用的根基。

Skill 的发现路径（项目级→用户级→内置）和加载机制是整个 Skill 系统的工作流核心。我们深入分析语义匹配的设计权衡——降低认知负荷的同时可能带来不精确触发——以及渐进式披露策略如何实现按需加载。在 OMO 扩展部分，我们介绍 Skills Marketplace（社区共享与版本管理）、Scoped Skills（target_agent 限定可见性）和 Skill Overrides 机制。学完本节，读者应能独立创建 Skill 文件，并为团队搭建可共享的 Skill 体系。

### 最小示例

用一个最简单的 SKILL.md 来理解 Skill：

```yaml
---
name: "hello-world"
description: "向世界打招呼的简单 Skill"
allowed-tools:
  - Read
---
```

这就是一个 Skill 的最小单元：`name` 是唯一标识，`description` 用于语义匹配，`allowed-tools` 定义权限边界。Agent 读到这份文件就知道："遇到打招呼的任务时，我可以加载这个 Skill 来处理。"

## Skill 的本质

### 定义：结构化指令包

Skill 是 OpenCode 生态中将**领域知识封装为可复用指令**的核心载体。如果说 Agent 是执行者，Skill 就是方法论——它告诉 Agent "遇到这类问题时应该怎么思考、按什么步骤做"。

一个 Skill 的本质包含三个维度：

| 维度 | 说明 | 类比 |
|------|------|------|
| **知识** | 特定领域的最佳实践、方法论、决策树 | 教科书 |
| **权限** | 完成任务所需的工具访问范围 | 门禁卡 |
| **约束** | 输出格式、质量标准、边界条件 | 检查清单 |

Skill 与普通 Prompt 的核心差异在于**工程化能力**：

```mermaid
graph LR
    subgraph Prompt[普通 Prompt]
        P1[自然语言指令]
        P2[无元数据]
        P3[无权限控制]
    end
    
    subgraph Skill[Skill 结构化指令包]
        S1[frontmatter 元数据]
        S2[正文指令]
        S3[allowed-tools 权限]
        S4[捆绑资源]
    end
    
    Prompt -->|"工程化升级"| Skill
    
    style Prompt fill:#f5f5f5,stroke:#999
    style Skill fill:#50C878,stroke:#333,color:#fff
```

### 操作系统类比：Skill = 驱动程序

理解 Skill 最直观的方式是将其类比为操作系统的**驱动程序**：

| 操作系统概念 | OpenCode 对应 | 说明 |
|--------------|---------------|------|
| 内核 | Agent 运行时 | 提供基础执行能力 |
| 驱动程序 | Skill | 让内核"懂得"如何操作特定设备/领域 |
| 设备 | 领域任务 | 前端开发、安全审计、数据库设计等 |
| 设备驱动接口 | Skill 接口规范 | SKILL.md 格式标准 |

没有驱动程序，操作系统无法识别和使用硬件设备。同样，没有 Skill，Agent 只能执行通用任务，无法深入特定领域。加载一个 Skill，就像安装了一个驱动程序——Agent 瞬间获得了该领域的"专业知识"。

### 组件化视角：前端架构师的类比

对于前端开发者，可以用**组件化思维**来理解 Skill 系统：

```mermaid
graph TB
    subgraph React[React 组件模型]
        RP[Props] --> |"输入配置"| RC[Component]
        RS[State] --> |"内部状态"| RC
        RC --> |"渲染输出"| RD[DOM]
    end
    
    subgraph Skill[Skill 模型]
        SF[frontmatter] --> |"元数据配置"| SK[Skill Body]
        SA[allowed-tools] --> |"权限边界"| SK
        SK --> |"指令输出"| SAO[Agent 行为]
    end
    
    React --> |"概念映射"| Skill
    
    style React fill:#4A90D9,stroke:#333,color:#fff
    style Skill fill:#50C878,stroke:#333,color:#fff
```

**Props = frontmatter**

就像组件通过 Props 接收外部配置，Skill 通过 frontmatter 定义元数据：

| React Props | Skill frontmatter | 作用 |
|-------------|-------------------|------|
| `name` | `name: "skill-name"` | 组件/Skill 的唯一标识 |
| `propTypes` | `description` + `metadata` | 类型声明与文档 |
| `defaultProps` | 默认值机制 | OMO Overrides 覆盖 |

**Composition = 编排**

多个组件组合成页面，多个 Skill 组合成 Workflow：

```mermaid
graph LR
    subgraph Page[页面 = 组件组合]
        C1[Header]
        C2[Content]
        C3[Footer]
    end
    
    subgraph Workflow[工作流 = Skill 组合]
        S1[需求分析 Skill]
        S2[代码生成 Skill]
        S3[测试验证 Skill]
    end
    
    C1 --> C2 --> C3
    S1 --> S2 --> S3
    
    style Page fill:#4A90D9,stroke:#333,color:#fff
    style Workflow fill:#50C878,stroke:#333,color:#fff
```

**单一职责原则**

优秀的组件只做一件事，优秀的 Skill 也只解决一个领域问题：

| 反模式 | 正确做法 |
|--------|----------|
| 一个 Skill 处理"前端开发+后端开发+测试" | 拆分为 `frontend-dev`、`backend-dev`、`test-engineer` |
| 一个组件包含"用户登录+商品列表+购物车" | 拆分为 `Login`、`ProductList`、`Cart` |

**生命周期对比**

| React 生命周期 | Skill 生命周期 | 触发时机 |
|----------------|----------------|----------|
| `constructor` | 元数据解析 | Skill 被发现时 |
| `render` | 指令执行 | Agent 调用 Skill 时 |
| `componentDidMount` | 资源加载 | 首次使用捆绑资源时 |
| `componentWillUnmount` | 清理 | 会话结束 |

## SKILL.md 完整格式

### frontmatter 字段详解

SKILL.md 以 YAML frontmatter 开头，定义 Skill 的元数据。以下是完整的字段规范：

```yaml
---
# 必填字段
name: "skill-name"              # Skill 的唯一标识符
description: "简短描述，用于语义匹配"  # 触发匹配的关键描述

# 权限控制
allowed-tools:                  # 允许访问的工具列表
  - Read
  - Write
  - Bash

# 可见性控制
target_agent: "build"           # 限定特定 Agent 可见（可选）

# 元数据扩展
license: "MIT"                  # 许可证（发布到 Marketplace 时重要）
metadata:
  version: "1.0.0"
  author: "your-name"
  tags:
    - frontend
    - react
  min_opencode_version: "2.0.0"
---
```

**必填字段**

| 字段 | 类型 | 说明 | 示例 |
|------|------|------|------|
| `name` | string | Skill 的唯一标识符，用于日志和调试 | `frontend-architect` |
| `description` | string | 简短描述，用于语义匹配触发 | `"React/Vue 组件架构设计专家"` |

**权限控制字段**

| 字段 | 类型 | 说明 | 安全含义 |
|------|------|------|----------|
| `allowed-tools` | string[] | 允许该 Skill 调用的工具列表 | **权限边界即攻击面**，见后文详解 |

**可见性控制字段**

| 字段 | 类型 | 说明 | 使用场景 |
|------|------|------|----------|
| `target_agent` | string | 限定只有特定 Agent 可以加载此 Skill | 专业 Skill 限定给专业 Agent |

**元数据扩展字段**

| 字段 | 类型 | 说明 |
|------|------|------|
| `license` | string | 许可证类型，发布到 Marketplace 时必需 |
| `metadata.version` | string | Skill 版本号，遵循语义化版本 |
| `metadata.author` | string | 作者信息 |
| `metadata.tags` | string[] | 标签，用于分类和搜索 |
| `metadata.min_opencode_version` | string | 最低 OpenCode 版本要求 |

### 正文结构

frontmatter 之后是 Skill 的正文，通常包含以下结构：

```markdown
---
name: "frontend-architect"
description: "前端架构设计专家，精通 React/Vue 组件设计"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
---

# 前端架构师 Skill

## 角色定义

你是一位资深前端架构师，专注于...

## 工作流程

1. **需求分析阶段**
   - 分析组件职责边界
   - 识别状态管理需求
   
2. **架构设计阶段**
   - 设计组件层次结构
   - 规划数据流向

## 输出规范

所有输出必须包含：
- 组件结构图（Mermaid 格式）
- 接口定义（TypeScript）
- 实现建议

## 约束条件

- 遵循单一职责原则
- 优先使用函数式组件
- ...
```

**正文结构最佳实践**

| 部分 | 内容 | 篇幅建议 |
|------|------|----------|
| 角色定义 | 明确 Skill 扮演的角色和职责 | 2-3 段 |
| 工作流程 | 分步骤描述执行逻辑 | 核心部分，占 40-50% |
| 输出规范 | 定义输出的格式和质量标准 | 1-2 段 + 示例 |
| 约束条件 | 明确边界条件和禁止事项 | 列表形式 |

### 捆绑资源目录

Skill 可以捆绑额外的资源文件，放在与 SKILL.md 同级的目录中：

```
my-skill/
├── SKILL.md              # Skill 定义文件
├── scripts/              # 可执行脚本
│   ├── setup.sh
│   └── validate.py
├── templates/            # 代码模板
│   ├── component.tsx.tmpl
│   └── test.spec.ts.tmpl
└── reference/            # 参考文档
    ├── best-practices.md
    └── examples.md
```

**资源目录用途**

| 目录 | 用途 | 典型内容 |
|------|------|----------|
| `scripts/` | 自动化脚本 | 初始化脚本、验证脚本、部署脚本 |
| `templates/` | 代码模板 | 组件模板、配置模板、测试模板 |
| `reference/` | 参考文档 | 最佳实践、设计模式、示例代码 |

## Skill 的发现与加载

### 三级搜索路径

OpenCode 按照以下优先级搜索 Skill：

```mermaid
graph TB
    subgraph Search[Skill 搜索路径]
        direction TB
        P1[项目级 .opencode/skills/] --> |"未找到"| P2[用户级 ~/.opencode/skills/]
        P2 --> |"未找到"| P3[内置 Skills]
        P3 --> |"未找到"| P4[Skills Marketplace]
    end
    
    P1 --> |"优先级最高"| R1[项目特定 Skill]
    P2 --> |"用户共享"| R2[个人 Skill 库]
    P3 --> |"开箱即用"| R3[官方 Skill]
    P4 --> |"社区贡献"| R4[第三方 Skill]
    
    style P1 fill:#50C878,stroke:#333,color:#fff
    style P2 fill:#4A90D9,stroke:#333,color:#fff
    style P3 fill:#FF9F43,stroke:#333,color:#fff
    style P4 fill:#A66CFF,stroke:#333,color:#fff
```

**项目级 Skills（`.opencode/skills/`）**

- 位置：项目根目录下的 `.opencode/skills/` 目录
- 优先级：最高
- 用途：项目特定的 Skill，如项目代码规范、特定业务逻辑
- 版本控制：建议纳入 Git 管理

**用户级 Skills（`~/.opencode/skills/`）**

- 位置：用户主目录下的 `.opencode/skills/` 目录
- 优先级：次高
- 用途：个人积累的 Skill，跨项目共享
- 版本控制：可选，适合个人知识沉淀

**内置 Skills**

- 位置：OpenCode 安装目录
- 优先级：最低
- 用途：官方提供的通用 Skill
- 更新：随 OpenCode 版本更新

### 渐进式披露机制

Skill 的加载采用**渐进式披露**策略，按需加载不同层级的内容：

```mermaid
sequenceDiagram
    participant User as 用户
    participant Agent as Agent
    participant FS as 文件系统
    
    User->>Agent: 提交任务描述
    Agent->>FS: 扫描所有 Skill 的 description
    Note over Agent,FS: 第一阶段：元数据匹配<br/>只读取 frontmatter
    
    alt 匹配成功
        Agent->>FS: 加载匹配 Skill 的完整内容
        Note over Agent,FS: 第二阶段：正文加载<br/>读取 SKILL.md 全文
        
        alt 需要捆绑资源
            Agent->>FS: 加载 scripts/templates/reference
            Note over Agent,FS: 第三阶段：资源加载<br/>按需读取捆绑文件
        end
        
        Agent->>User: 执行 Skill 指令
    else 无匹配
        Agent->>User: 使用默认行为
    end
```

**三阶段加载详解**

| 阶段 | 加载内容 | 触发条件 | 性能影响 |
|------|----------|----------|----------|
| 元数据匹配 | 只读取 frontmatter | 每次任务开始时 | 极低，只解析 YAML |
| 正文加载 | 读取完整 SKILL.md | description 匹配成功 | 中等，解析 Markdown |
| 资源加载 | 读取捆绑目录 | Skill 执行需要时 | 按需，可能较高 |

### 语义匹配的设计权衡

Skill 的发现依赖**语义匹配**——Agent 根据用户任务描述和 Skill 的 description 进行匹配。这种设计有利有弊：

**优势**

- **降低认知负荷**：用户无需记忆 Skill 名称，自然语言描述即可触发
- **灵活扩展**：新增 Skill 无需修改配置，自动参与匹配
- **跨语言支持**：多语言 description 可支持不同语言用户

**挑战**

- **匹配不精确**：相似描述可能导致错误触发
- **调试困难**：难以预测哪个 Skill 会被激活
- **版本冲突**：多个 Skill 匹配时的优先级问题

**最佳实践：编写精准的 description**

```yaml
# 反例：描述过于宽泛
description: "帮助开发"

# 正例：描述具体且包含关键词
description: "React 组件架构设计专家，精通状态管理、性能优化、TypeScript 类型设计"
```

## 权限控制

### 三级策略：allow/ask/deny

OpenCode 的权限系统采用三级策略模型：

| 策略 | 行为 | 适用场景 |
|------|------|----------|
| `allow` | 自动执行，无需确认 | 安全操作，如读取文件 |
| `ask` | 每次执行前询问用户 | 敏感操作，如写入文件、执行命令 |
| `deny` | 禁止执行，直接拒绝 | 危险操作，如删除文件、访问敏感路径 |

权限可以在不同层级配置：

```jsonc
// opencode.json
{
  "permissions": {
    // 全局默认策略
    "default": "ask",
    
    // 工具级策略
    "tools": {
      "Read": "allow",
      "Write": "ask",
      "Bash": "ask",
      "Delete": "deny"
    },
    
    // Skill 级策略
    "skills": {
      "frontend-architect": {
        "tools": ["Read", "Write", "Glob", "Grep"]
      }
    }
  }
}
```

### allowed-tools 安全含义

**权限边界即攻击面**——这是安全架构师视角下 Skill 权限设计的核心原则。

```mermaid
graph TB
    subgraph Attack[攻击面分析]
        S[Skill] --> |"allowed-tools"| T1[Read]
        S --> T2[Write]
        S --> T3[Bash]
        S --> T4[WebFetch]
    end
    
    T1 --> |"信息泄露风险"| R1[读取敏感文件<br/>.env, credentials]
    T2 --> |"篡改风险"| R2[修改关键配置<br/>注入恶意代码]
    T3 --> |"命令执行风险"| R3[执行任意命令<br/>横向移动]
    T4 --> |"数据外泄风险"| R4[向外部发送数据<br/>SSRF 攻击]
    
    style S fill:#50C878,stroke:#333,color:#fff
    style R1 fill:#E74C3C,stroke:#333,color:#fff
    style R2 fill:#E74C3C,stroke:#333,color:#fff
    style R3 fill:#E74C3C,stroke:#333,color:#fff
    style R4 fill:#E74C3C,stroke:#333,color:#fff
```

**最小权限原则**

每个 Skill 的 `allowed-tools` 应遵循最小权限原则——只授予完成任务所需的最小权限集：

| Skill 类型 | 推荐 allowed-tools | 安全考量 |
|------------|-------------------|----------|
| 代码审查 | `Read`, `Glob`, `Grep` | 只读，无修改风险 |
| 代码生成 | `Read`, `Write`, `Glob` | 需要写入，但禁止命令执行 |
| 部署脚本 | `Read`, `Write`, `Bash` | 高风险，需严格审计 |
| 安全审计 | `Read`, `Grep`, `Bash` | 需要执行扫描工具，但禁止写入 |

**allowed-tools 配置示例**

```yaml
---
name: "code-reviewer"
description: "代码审查专家，识别代码异味和安全漏洞"
allowed-tools:
  - Read      # 读取代码文件
  - Glob      # 搜索文件
  - Grep      # 搜索内容
  # 注意：没有 Write，禁止修改代码
  # 注意：没有 Bash，禁止执行命令
---
```

**权限提升攻击防护**

恶意 Skill 可能尝试通过以下方式提升权限：

| 攻击方式 | 防护措施 |
|----------|----------|
| 诱导用户执行命令 | `Bash` 工具默认 `ask` 策略 |
| 修改配置文件获取权限 | 敏感路径 `deny` 策略 |
| 链式调用其他 Skill | `target_agent` 限制可见性 |
| 通过 WebFetch 外泄数据 | 网络请求审计日志 |

### Skill 权限审计

所有 Skill 的工具调用都会被记录到审计日志：

```
[2025-06-01 10:23:45] [Skill: frontend-architect] Called Read on src/App.tsx
[2025-06-01 10:23:46] [Skill: frontend-architect] Called Write on src/components/Header.tsx
[2025-06-01 10:23:47] [Skill: frontend-architect] DENIED: Bash not in allowed-tools
```

审计日志可用于：
- 安全事件调查
- 合规审计
- Skill 行为分析
- 权限配置优化

## OMO 扩展

### Skills Marketplace

Skills Marketplace 是 OMO 生态的 Skill 共享平台：

```mermaid
graph LR
    subgraph Local[本地 Skill]
        L1[项目级]
        L2[用户级]
    end
    
    subgraph Marketplace[Skills Marketplace]
        M1[官方 Skill]
        M2[社区 Skill]
        M3[企业私有 Skill]
    end
    
    L1 --> |"发布"| Marketplace
    L2 --> |"发布"| Marketplace
    Marketplace --> |"安装"| L1
    Marketplace --> |"安装"| L2
    
    style Local fill:#4A90D9,stroke:#333,color:#fff
    style Marketplace fill:#50C878,stroke:#333,color:#fff
```

**Marketplace 功能**

| 功能 | 说明 |
|------|------|
| 版本管理 | 每个 Skill 有独立的版本号和更新历史 |
| 依赖声明 | Skill 可以声明对其他 Skill 的依赖 |
| 评分系统 | 用户可以对 Skill 进行评分和评论 |
| 安全扫描 | 上传的 Skill 经过安全检查 |

### Scoped Skills

`target_agent` 字段可以实现 Skill 的可见性控制：

```yaml
---
name: "security-scanner"
description: "安全漏洞扫描专家"
target_agent: "security-audit"  # 只有 security-audit Agent 可见
allowed-tools:
  - Read
  - Grep
  - Bash
---
```

**使用场景**

| 场景 | target_agent 设置 |
|------|-------------------|
| 通用 Skill | 不设置，所有 Agent 可见 |
| 专业 Skill | 设置为专业 Agent，如 `build`、`plan` |
| 安全敏感 Skill | 设置为专用安全 Agent，限制传播 |

### Skill Overrides

OMO 配置可以覆盖 SKILL.md 中的默认值：

```jsonc:opencode.json
{
  "skills": {
    "frontend-architect": {
      // 覆盖 allowed-tools
      "allowed-tools": ["Read", "Glob", "Grep"],
      // 覆盖 target_agent
      "target_agent": "build",
      // 禁用特定 Skill
      "disabled": false
    }
  }
}
```

**覆盖优先级**

```
OMO 配置 > 项目级 SKILL.md > 用户级 SKILL.md > 内置 SKILL.md
```

## Skill vs Plugin

Skill 和 Plugin 是 OpenCode 生态中两个互补的概念：

```mermaid
graph TB
    subgraph SkillLayer[Skill 层：指令层]
        S1[Skill: 教 Agent 怎么做]
        S2[定义工作流程]
        S3[提供决策逻辑]
    end
    
    subgraph PluginLayer[Plugin 层：能力层]
        P1[Plugin: 改 Agent 能做什么]
        P2[扩展工具集]
        P3[连接外部服务]
    end
    
    SkillLayer --> |"调用"| PluginLayer
    
    style SkillLayer fill:#50C878,stroke:#333,color:#fff
    style PluginLayer fill:#A66CFF,stroke:#333,color:#fff
```

| 维度 | Skill | Plugin |
|------|-------|--------|
| 本质 | 指令包 | 能力扩展 |
| 作用 | 教 Agent "怎么做" | 改 Agent "能做什么" |
| 示例 | 代码审查流程、架构设计方法论 | MCP 服务器、自定义工具 |
| 配置 | SKILL.md | opencode.json plugins 字段 |
| 权限 | allowed-tools | 工具注册 |

**组合使用示例**

一个完整的"数据库迁移"任务可能需要：

1. **Plugin**：提供数据库连接工具（能力层）
2. **Skill**：定义迁移流程和最佳实践（指令层）

## Skill 使用最佳实践

### 编写精准的 description

```yaml
# 反例：过于宽泛
description: "帮助写代码"

# 正例：具体且包含关键词
description: "React Hooks 最佳实践专家，精通 useEffect/useMemo/useCallback 优化策略，专注性能调优和内存泄漏排查"
```

**description 编写技巧**

- 包含领域关键词（React、安全、测试）
- 说明核心能力（精通、专注、擅长）
- 区分相似 Skill 的差异

### 版本迭代维护

```yaml
---
name: "frontend-architect"
description: "前端架构设计专家"
metadata:
  version: "2.1.0"  # 语义化版本
  changelog:
    - "2.1.0: 新增 Server Components 支持"
    - "2.0.0: 重构为 React 18 兼容"
    - "1.0.0: 初始版本"
---
```

### 团队共享规范

| 规范项 | 建议 |
|--------|------|
| 命名规范 | 小写连字符，如 `frontend-architect` |
| 目录结构 | 每个 Skill 独立目录，包含 SKILL.md 和资源 |
| 版本控制 | 项目级 Skill 纳入 Git，用户级可选 |
| 审查流程 | 敏感 Skill（含 Bash 权限）需安全审查 |

## 小结

Skill 是 OpenCode 生态中将领域知识工程化的核心载体。通过 frontmatter 元数据、正文指令、权限控制的组合，Skill 实现了从"提示词"到"可复用能力模块"的跨越。

理解 Skill 的关键要点：

1. **本质**：结构化指令包 = 知识 + 权限 + 约束
2. **类比**：Skill = 驱动程序，让 Agent 获得领域专业能力
3. **格式**：frontmatter（元数据）+ 正文（指令）+ 资源（捆绑文件）
4. **发现**：项目级→用户级→内置的三级搜索路径
5. **加载**：渐进式披露，按需加载元数据→正文→资源
6. **权限**：allowed-tools 定义权限边界，权限边界即攻击面

在下一章 [工作流模式](workflow-patterns.md) 中，我们将看到多个 Skill 如何被编排成完整的工作流，实现复杂任务的自动化。

---

## 学习检查清单

完成本章学习后，请确认你能够：

- [ ] 解释 Skill 与普通 Prompt 的核心差异（权限控制、工具绑定、元数据索引）
- [ ] 编写符合规范的 SKILL.md 文件，包含 frontmatter 和正文结构
- [ ] 描述 Skill 的三级搜索路径（项目级→用户级→内置）及其优先级
- [ ] 配置 allowed-tools 字段并理解最小权限原则
- [ ] 说明渐进式披露机制的三阶段加载过程

---

## 关联章节

- ← [Agent 编排](agent-orchestration.md)：Skill 由 Agent 加载和执行，理解 Agent 是理解 Skill 的前提
- → [工作流模式](workflow-patterns.md)：Command 可指定 Skill，工作流编排中 Skill 是能力单元
- → [Skill 开发](../05-skills/)：Skill 模板和开发实操，最佳实践的深度展开
- → [安全总览](../06-advanced/security-overview.md)：权限控制的深度分析和安全审计
