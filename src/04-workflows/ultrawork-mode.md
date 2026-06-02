# Ultrawork 模式

> 目标驱动而非指令驱动：让 Agent 自主探索代码库、研究模式、实现功能并验证结果的全自动工作流。

## 文章概述

Ultrawork 模式是 oh-my-openagent 的旗舰工作流。它代表了一种从"精确指令"到"目标驱动"的范式转变：你不需要告诉 Agent 怎么做，只需要告诉它做什么。Agent 会自动探索代码库、研究现有模式、实现功能、通过 LSP 验证结果，然后根据结果决定下一步。

本文从原理出发，深入讲解 Ultrawork 的工作机制和适用场景。你将学习如何启用 Ultrawork 模式（对话输入 `ulw` 或设置为默认模式），以及如何配合 Ralph Loop（`/ulw-loop`）实现自我迭代直到 100% 完成。我们还通过对比表分析 Ultrawork 与传统 Prompt 方式在精准度、探索深度、Token 消耗和人工介入方面的差异，帮助你在合适的场景做出正确选择。

学习本文后，你将理解 Ultrawork 的工程价值：在不确定性和探索成本之间取得平衡。这在上下文复杂的任务、快速原型和大型重构中尤其有价值。

---

## Ultrawork 的工作原理

### 定义："懒得想"模式

Ultrawork 的核心理念可以用一句话概括：**你只说目标，Agent 自己想办法**。这是一种"懒得想"模式——当你不想花时间写详细的需求文档、不想逐步指导 Agent 如何实现时，Ultrawork 让 Agent 自主完成从探索到验证的全过程。

### 闭环工作机制

Ultrawork 的工作流程是一个持续迭代的闭环：

```mermaid
flowchart TB
    subgraph 探索阶段
        A[用户目标] --> B[探索代码库]
        B --> C[识别现有模式]
    end

    subgraph 实现阶段
        C --> D[制定实现方案]
        D --> E[编写代码]
    end

    subgraph 验证阶段
        E --> F[LSP 类型检查]
        F --> G{验证通过?}
        G -->|否| H[分析错误]
        H --> D
        G -->|是| I[运行测试]
    end

    subgraph 决策阶段
        I --> J{测试通过?}
        J -->|否| K[定位失败原因]
        K --> D
        J -->|是| L{完成度评估}
        L -->|未完成| B
        L -->|完成| M[输出结果]
    end

    style A fill:#4A90D9,color:#fff
    style B fill:#50C878,color:#fff
    style C fill:#50C878,color:#fff
    style D fill:#FF9F43,color:#fff
    style E fill:#FF9F43,color:#fff
    style F fill:#A66CFF,color:#fff
    style M fill:#4A90D9,color:#fff
```

**各阶段详解**：

| 阶段 | 核心活动 | 关键能力 |
|------|---------|---------|
| **探索阶段** | 扫描项目结构、阅读相关文件、理解现有架构 | 代码库导航、模式识别 |
| **实现阶段** | 设计方案、编写代码、遵循项目规范 | 代码生成、风格匹配 |
| **验证阶段** | LSP 类型检查、运行测试、静态分析 | 错误诊断、问题定位 |
| **决策阶段** | 评估完成度、决定下一步行动 | 自我评估、路径规划 |

### 与传统 Prompt 的本质区别

传统 Prompt 模式是"指令驱动"：你需要详细说明每一步怎么做。Ultrawork 是"目标驱动"：你只说想要什么结果。

**传统 Prompt 示例**：

```
请帮我实现用户登录功能：
1. 先阅读 src/auth/ 目录下的现有认证代码
2. 参考 AuthService 的实现风格
3. 在 src/auth/LoginService.ts 中创建 LoginService 类
4. 实现 login 方法，使用 bcrypt 验证密码
5. 添加单元测试到 tests/auth/LoginService.test.ts
6. 运行测试确保通过
```

**Ultrawork 示例**：

```
ulw 实现用户登录功能
```

Agent 会自动完成上述所有步骤，无需你逐条指定。

---

## Ultrawork 使用方式

### 方式一：对话中临时激活

在任意对话中输入 `ulw` 或 `ultrawork`，即可将当前会话切换到 Ultrawork 模式：

```bash
# 简写形式
ulw 为订单模块添加批量导出功能

# 完整形式
ultrawork 重构用户服务，提取公共逻辑
```

**特点**：
- 仅对当前任务生效
- 任务完成后恢复默认模式
- 适合临时性、探索性任务

### 方式二：设置为默认模式

在 `opencode.json` 中配置默认模式，让所有任务都使用 Ultrawork：

```json
{
  "agent": {
    "default_mode": "ultrawork"
  }
}
```

或使用 OMO 扩展配置：

```json
{
  "default_mode": {
    "ultrawork": {
      "enabled": true,
      "ralph_loop": {
        "max_turns": 10,
        "stop_condition": "completion_100"
      }
    }
  }
}
```

**特点**：
- 所有任务默认使用 Ultrawork
- 适合探索性开发、原型项目
- 可通过 `/plan` 命令临时切换到精确模式

### 方式三：配合 Ralph Loop 使用

使用 `/ulw-loop` 命令启动带自我迭代的 Ultrawork：

```bash
# 基础用法
/ulw-loop 实现用户登录功能

# 指定最大迭代次数
/ulw-loop --max-turns 20 重构订单模块

# 自定义停止条件
/ulw-loop --stop-condition="coverage>80" 添加单元测试
```

---

## Ultrawork vs 传统 Prompt 对比

### 四维度对比表

| 维度 | Ultrawork | 传统 Prompt |
|------|-----------|-------------|
| **精准度** | 中等（依赖 Agent 自主判断） | 高（用户精确控制） |
| **探索深度** | 深（自动发现相关上下文） | 浅（受限于用户指定范围） |
| **Token 消耗** | 较高（探索开销） | 可控（按指令执行） |
| **人工介入** | 低（设定目标后放手） | 高（需要逐步指导） |
| **学习曲线** | 低（只需描述目标） | 高（需要了解项目细节） |
| **结果一致性** | 中等（可能有多条路径） | 高（按预设路径执行） |
| **审计友好** | 低（过程不透明） | 高（步骤清晰可追溯） |
| **适用周期** | 探索期、原型期 | 生产期、维护期 |

### 决策指南：何时选择 Ultrawork

**选择 Ultrawork 的场景**：

1. **不熟悉的项目**：Agent 自主探索比你自己研究更高效
2. **快速原型开发**：时间紧迫，不需要完美方案
3. **探索性编程**：不确定最佳实现路径，让 Agent 尝试
4. **大型重构**：涉及多个模块，难以预见所有依赖
5. **文档补全**：让 Agent 自动发现缺失文档的 API

**选择传统 Prompt 的场景**：

1. **关键业务逻辑**：需要精确控制每个细节
2. **安全敏感代码**：不允许自主决策
3. **需要审计轨迹**：每一步都要有记录
4. **团队协作项目**：变更需要可预测
5. **性能关键路径**：实现方式有严格要求

### 混合策略

实际项目中，建议采用混合策略：

```mermaid
graph LR
    A[新任务] --> B{熟悉项目?}
    B -->|否| C[Ultrawork 探索]
    B -->|是| D{任务关键性?}
    C --> E[理解上下文]
    E --> D
    D -->|高| F[传统 Prompt 精确控制]
    D -->|低| G[Ultrawork 快速实现]
    F --> H[完成]
    G --> H

    style C fill:#50C878,color:#fff
    style F fill:#4A90D9,color:#fff
    style G fill:#50C878,color:#fff
```

---

## Ralph Loop 机制

### 什么是 Ralph Loop

Ralph Loop（`/ulw-loop`）是 Ultrawork 的自我迭代机制。与普通 Loop 不同，Ralph Loop 不是预设步骤的重复执行，而是 Agent 根据当前完成情况自主决定下一步行动。

**核心理念**：Agent 会持续工作直到任务 100% 完成，而非单次执行后停止。

### Ralph Loop vs 普通 Loop

| 特性 | Ralph Loop | 普通 Loop |
|------|-----------|----------|
| **决策主体** | Agent 自主决策 | 预设步骤 |
| **停止条件** | 完成度评估 | 固定次数/条件 |
| **路径规划** | 动态调整 | 固定路径 |
| **适应性** | 高（根据反馈调整） | 低（机械重复） |
| **适用场景** | 目标导向任务 | 流程化任务 |

### Ralph Loop 决策流程

```mermaid
flowchart TB
    A[启动 /ulw-loop] --> B[执行当前任务]
    B --> C[评估完成度]
    C --> D{完成度 >= 100%?}
    D -->|是| E[输出最终结果]
    D -->|否| F{达到最大迭代?}
    F -->|是| G[汇报当前进度<br/>等待用户决策]
    F -->|否| H[分析剩余工作]
    H --> I[规划下一步行动]
    I --> B

    G --> J{用户选择}
    J -->|继续| I
    J -->|调整目标| K[更新任务目标]
    K --> B
    J -->|终止| L[输出当前结果]

    style A fill:#4A90D9,color:#fff
    style E fill:#50C878,color:#fff
    style G fill:#FF9F43,color:#fff
    style L fill:#A66CFF,color:#fff
```

### 控制参数

| 参数 | 说明 | 默认值 | 示例 |
|------|------|--------|------|
| `max_turns` | 最大迭代次数 | 10 | `--max-turns 20` |
| `stop_condition` | 停止条件 | `completion_100` | `--stop-condition="tests_pass"` |
| `progress_report` | 进度汇报频率 | 每次迭代 | `--progress-report=verbose` |
| `timeout` | 单次迭代超时 | 300s | `--timeout 600` |

**停止条件类型**：

| 条件类型 | 说明 | 示例 |
|---------|------|------|
| `completion_100` | 完成度达到 100% | 默认条件 |
| `tests_pass` | 所有测试通过 | 适合测试驱动开发 |
| `coverage>N` | 测试覆盖率超过 N% | `coverage>80` |
| `lint_clean` | 无 Lint 错误 | 适合代码清理任务 |
| `custom:expr` | 自定义表达式 | `custom:"errors.length==0"` |

### 完整配置示例

```json
{
  "default_mode": {
    "ultrawork": {
      "enabled": true,
      "ralph_loop": {
        "max_turns": 15,
        "stop_condition": "completion_100",
        "progress_report": "verbose",
        "timeout": 300,
        "on_max_turns": "report"
      },
      "exploration": {
        "max_files": 50,
        "priority_patterns": ["*.ts", "*.js", "src/**"],
        "ignore_patterns": ["node_modules", "dist", "*.test.ts"]
      },
      "verification": {
        "lsp_enabled": true,
        "test_command": "npm test",
        "lint_command": "npm run lint"
      }
    }
  }
}
```

**配置说明**：

| 配置项 | 说明 |
|-------|------|
| `max_turns` | 最大迭代次数，防止无限循环 |
| `stop_condition` | 任务完成的判断标准 |
| `on_max_turns` | 达到最大迭代时的行为：`report`（汇报进度）或 `continue`（继续执行） |
| `exploration.max_files` | 探索阶段最多读取的文件数 |
| `exploration.priority_patterns` | 优先探索的文件模式 |
| `verification.lsp_enabled` | 是否启用 LSP 类型检查 |

---

## 实战案例：使用 Ultrawork 为开源项目添加功能

### 场景描述

假设你刚接手一个不熟悉的开源项目，需要为其添加"用户头像上传"功能。项目使用 React + Node.js + PostgreSQL 技术栈，但你不确定：

- 现有的文件上传机制是什么
- 用户模型如何定义
- API 路由如何组织
- 数据库迁移如何处理

### 使用 Ultrawork 完成

**步骤 1：启动 Ultrawork**

```bash
ulw 为用户添加头像上传功能，支持 JPG/PNG 格式，最大 2MB
```

**步骤 2：观察 Agent 的探索过程**

Agent 会自动执行以下操作：

```
[探索阶段]
→ 扫描项目结构，识别技术栈
→ 查找现有文件上传相关代码
→ 阅读用户模型定义
→ 分析 API 路由组织方式
→ 检查数据库迁移文件

[发现]
→ 项目已有 multer 中间件处理文件上传
→ 用户模型在 src/models/User.ts
→ API 路由在 src/routes/api/ 目录
→ 数据库迁移使用 Knex.js

[实现阶段]
→ 创建 src/routes/api/avatar.ts 路由
→ 扩展 User 模型添加 avatar_url 字段
→ 创建数据库迁移文件
→ 添加文件大小和格式验证
→ 编写单元测试

[验证阶段]
→ 运行 TypeScript 编译检查
→ 执行单元测试
→ 检查代码风格

[完成度评估]
→ 功能实现：100%
→ 测试覆盖：85%
→ 文档更新：待完成

[继续迭代]
→ 添加 API 文档
→ 更新 README
```

**步骤 3：验收结果**

Agent 会输出完整的变更摘要：

```
任务完成！已实现用户头像上传功能：

新增文件：
- src/routes/api/avatar.ts（头像上传路由）
- src/middleware/avatarValidator.ts（文件验证中间件）
- migrations/20260602_add_avatar_url.ts（数据库迁移）
- tests/api/avatar.test.ts（单元测试）

修改文件：
- src/models/User.ts（添加 avatar_url 字段）
- src/routes/index.ts（注册新路由）

测试结果：12/12 通过
代码风格检查：通过
```

### 使用 Ralph Loop 确保完整交付

如果需要确保测试覆盖率达到目标：

```bash
/ulw-loop --stop-condition="coverage>80" --max-turns 15 为用户添加头像上传功能
```

Agent 会持续迭代直到测试覆盖率达标：

```
[迭代 1] 实现基础功能，覆盖率 45%
[迭代 2] 添加边界条件测试，覆盖率 62%
[迭代 3] 添加错误处理测试，覆盖率 78%
[迭代 4] 添加文件验证测试，覆盖率 85%
[完成] 覆盖率达标，任务完成
```

---

## Ultrawork 的最佳实践

### 1. 提供清晰的目标描述

虽然 Ultrawork 是"目标驱动"，但目标本身的清晰度直接影响结果质量。

**好的目标描述**：

```
ulw 实现用户头像上传功能，支持 JPG/PNG，最大 2MB，存储到 S3
```

**不好的目标描述**：

```
ulw 加个头像功能
```

### 2. 利用 AGENTS.md 提供上下文

在项目的 AGENTS.md 中记录关键信息，帮助 Ultrawork 更好地理解项目：

```markdown
## 技术栈

- 前端：React 18 + TypeScript
- 后端：Node.js + Express
- 数据库：PostgreSQL + Knex.js
- 文件存储：AWS S3

## 编码规范

- 所有 API 路由放在 src/routes/api/ 目录
- 使用 Zod 进行请求验证
- 测试文件与源文件同名加 .test.ts 后缀
```

### 3. 合理设置迭代参数

根据任务复杂度调整 `max_turns`：

| 任务复杂度 | 建议 max_turns | 说明 |
|-----------|---------------|------|
| 简单（单文件修改） | 3-5 | 快速完成 |
| 中等（多文件变更） | 10-15 | 默认值 |
| 复杂（跨模块重构） | 20-30 | 允许更多探索 |
| 探索性（不确定范围） | 30+ | 充分探索 |

### 4. 监控 Token 消耗

Ultrawork 的探索过程会消耗较多 Token。建议：

- 设置 `exploration.max_files` 限制探索范围
- 使用 `priority_patterns` 优先探索关键文件
- 定期检查 Token 使用情况

### 5. 与版本控制配合

Ultrawork 完成后，建议：

1. 使用 `git diff` 审查所有变更
2. 运行完整测试套件
3. 检查是否有意外的文件修改
4. 确认变更符合预期后再提交

---

## 常见问题

### Q: Ultrawork 会修改我不想修改的文件吗？

A: Ultrawork 遵循 AGENTS.md 中的约束规则。你可以在 AGENTS.md 中明确禁止修改某些文件：

```markdown
## 约束规则

- 禁止修改 config/ 目录下的配置文件
- 禁止修改 migrations/ 目录下已执行的迁移文件
- 禁止直接修改数据库 schema
```

### Q: Ultrawork 的探索过程会泄露敏感信息吗？

A: Ultrawork 只读取本地文件，不会将代码发送到外部服务器（除了发送给 LLM API）。建议：

- 不要在代码中存储敏感信息
- 使用环境变量管理密钥
- 将敏感文件添加到 `.gitignore`

### Q: 如何中断 Ultrawork 的执行？

A: 在任何时候输入 `stop` 或 `cancel` 即可中断当前任务。Agent 会保存当前进度并输出已完成的工作。

### Q: Ultrawork 适合生产环境部署吗？

A: Ultrawork 更适合开发阶段。生产环境的变更建议使用 Prometheus 模式，确保每一步都有审计轨迹。

---

---

## 延伸阅读：Prometheus 规划模式

Ultrawork 的"先做再说"风格在处理探索性任务时非常高效。但对于另一些场景——需要审计轨迹、需求模糊或涉及多方利益时——我们提供了 **Prometheus 规划模式**。

Prometheus 模式（`@plan`）采用访谈式需求收集的工作方式。与 Ultrawork 的"你说目标我干活"不同，Prometheus 会主动向你提问，逐步澄清需求，直到形成一份结构化的执行计划，再由 Atlas 指挥官执行。

> → [Prometheus 规划模式详解](prometheus-mode.md) — 了解访谈式规划、Atlas 执行指挥官和三模式决策框架的完整内容。

以下对比表帮助你在三种模式中快速选择：

| 维度 | 传统 Prompt | Prometheus 模式 | Ultrawork 模式 |
|------|-----------|----------------|---------------|
| **工作方式** | 手动写明所有步骤 | 访谈收集需求 → 结构化计划 → 自动执行 | Agent 自主探索并实现 |
| **需求明确度** | 用户必须完全清楚 | 逐步澄清，从模糊到明确 | 用户只需描述目标 |
| **人工介入** | 高（全程指导） | 中（访谈 + 确认计划） | 低（设定目标后放手） |
| **审计轨迹** | 高（步骤清晰可查） | 高（计划可逐条对照） | 低（过程不透明） |
| **启动速度** | 快（直接写 Prompt） | 中（需完成访谈阶段） | 快（一句话目标） |
| **探索深度** | 浅（受限于指令范围） | 中（按计划执行，边界可控） | 深（Agent 自动发现） |
| **适合场景** | 关键业务、安全敏感 | 需求模糊 + 需要审计 | 快速原型、探索任务 |
| **Token 消耗** | 可控 | 中上（访谈阶段有开销） | 较高（探索阶段开销大） |

**选择指南**：

```
需求明确 + 需要精确控制 → 传统 Prompt
需求模糊 + 需要审计轨迹 → Prometheus 模式
需求模糊 + 追求效率 → Ultrawork 模式
```

---

## 小结

Ultrawork 模式代表了 AI 编程的一次范式转变：从"告诉 Agent 怎么做"到"告诉 Agent 做什么"。这种目标驱动的方式在探索性任务、快速原型和不熟悉的项目中尤其有价值。

Ralph Loop（`/ulw-loop`）进一步增强了 Ultrawork 的能力，让 Agent 能够自我迭代直到任务完全完成。通过合理配置控制参数，你可以在效率和可控性之间找到平衡。

接下来 → [Prometheus 规划模式](prometheus-mode.md) 探讨了"计划优先"的方法论，它补充了 Ultrawork 的"探索优先"哲学。理解何时使用每种模式是 Harness Engineering 的核心能力之一。

---

## 学习检查清单

完成本章学习后，请确认你能够：

- [ ] 解释 Ultrawork 的"目标驱动"理念与传统 Prompt 的区别
- [ ] 使用三种方式启用 Ultrawork：临时激活、默认模式、Ralph Loop
- [ ] 配置 Ultrawork 的控制参数（max_turns、stop_condition 等）
- [ ] 判断何时选择 Ultrawork、何时选择传统 Prompt
- [ ] 使用 `/ulw-loop` 实现自我迭代的任务执行
- [ ] 了解 Prometheus 规划模式与 Ultrawork 的差异和配合方式（→ [Prometheus 规划模式](prometheus-mode.md)）

---

## 关联章节

- ← [工作流模式](../02-core-concepts/workflow-patterns.md) — Command 触发 Ultrawork
- ← [oh-my-openagent 集成](../03-setup/oh-my-openagent-setup.md) — OMO 配置是 Ultrawork 的基础
- → [Prometheus 规划模式](prometheus-mode.md) — 对比探索优先 vs 计划优先
- → [多 Agent 协作](multi-agent-collab.md) — Ultrawork 与多 Agent 协作的关系
