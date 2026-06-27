# Category 系统

> OpenCode 的任务分类与模型路由机制，实现任务复杂度与模型能力的精准匹配。

---

## 概述

Category（类别）是 OpenCode 的核心路由机制，用于将用户任务自动分类并路由到最适合的 AI 模型。通过 Category 系统，OpenCode 能够：

- **智能匹配**：根据任务复杂度和类型选择最优模型
- **成本优化**：简单任务使用轻量模型，复杂任务使用旗舰模型
- **质量保障**：确保每个任务都有合适的模型能力支撑

---

## 8 个内置 Category

| Category | 默认模型 | 描述 |
|----------|---------|------|
| `visual-engineering` | Gemini 3.1 Pro (high) | 前端、UI/UX、设计、动画 |
| `ultrabrain` | GPT-5.5 (xhigh) | 深度逻辑推理、复杂架构 |
| `deep` | GPT-5.5 (medium) | 自主问题解决、彻底研究 |
| `artistry` | Gemini 3.1 Pro (high) | 创意/非传统方法 |
| `quick` | GPT-5.4-mini | 琐碎任务、单文件修改 |
| `unspecified-low` | Claude Sonnet 4.6 | 一般任务、低复杂度 |
| `unspecified-high` | Claude Opus 4.7 (max) | 一般任务、高复杂度 |
| `writing` | Kimi K2.5 | 文档、技术写作 |

### Category 详细说明

#### visual-engineering

**适用场景**：
- 前端组件开发与样式调整
- UI/UX 设计评审与优化
- 动画效果实现
- 响应式布局调整
- 可视化图表开发

**模型选择理由**：Gemini 3.1 Pro 在视觉理解和多模态任务上表现优异，适合处理涉及设计、布局和视觉效果的工程任务。

#### ultrabrain

**适用场景**：
- 复杂系统架构设计
- 深度逻辑推理与问题分析
- 多系统集成方案设计
- 性能瓶颈诊断与优化
- 安全架构评审

**模型选择理由**：GPT-5.5 (xhigh) 具备最强的推理能力，适合需要深度思考和复杂决策的任务。

#### deep

**适用场景**：
- 自主问题解决与调试
- 代码库深度研究与理解
- 技术方案调研与评估
- 复杂 bug 排查

**模型选择理由**：GPT-5.5 (medium) 在保持较强推理能力的同时，提供更好的响应速度和成本效益。

#### artistry

**适用场景**：
- 创意解决方案探索
- 非常规技术方案设计
- 创新功能原型开发
- 用户体验创新设计

**模型选择理由**：Gemini 3.1 Pro 在创意生成和非传统思维任务上表现出色。

#### quick

**适用场景**：
- 单文件小修改
- 简单代码格式化
- 快速文档更新
- 配置文件调整
- 简单查询回答

**模型选择理由**：GPT-5.4-mini 响应迅速、成本低廉，适合不需要深度推理的简单任务。

#### unspecified-low

**适用场景**：
- 一般编程任务
- 代码审查
- 简单重构
- 常规功能开发

**模型选择理由**：Claude Sonnet 4.6 在通用编程任务上表现均衡，成本适中。

#### unspecified-high

**适用场景**：
- 复杂功能开发
- 多模块协调修改
- 架构调整
- 技术债务处理

**模型选择理由**：Claude Opus 4.7 (max) 具备强大的代码理解和生成能力，适合高复杂度通用任务。

#### writing

**适用场景**：
- 技术文档撰写
- API 文档生成
- README 编写
- 技术博客创作
- 代码注释完善

**模型选择理由**：Kimi K2.5 在中文技术写作上表现优异，特别适合中文文档生成任务。

---

## Category 与模型路由机制

### 路由流程

```
用户输入 → 任务分析 → Category 选择 → 模型路由 → 执行任务
                ↓
           Provider Fallback
                ↓
           备选模型执行
```

### 路由决策因素

1. **任务复杂度**：评估任务需要的推理深度
2. **任务类型**：识别是视觉、逻辑、创意还是写作任务
3. **上下文规模**：考虑需要处理的代码量或文档量
4. **响应速度要求**：是否需要快速响应

### Provider Fallback 机制

当首选模型不可用时，系统自动降级到备选模型：

```
首选模型 → 次选模型 → 兜底模型
```

Fallback 链确保服务可用性，避免因单个 Provider 故障导致任务失败。

---

## 自定义 Category

用户可以根据团队需求定义自定义 Category，实现更精细的模型路由控制。

### 配置示例

```json
{
  "categories": {
    "git": {
      "model": "opencode/gpt-5-nano",
      "description": "所有 git 操作",
      "prompt_append": "专注于原子提交、清晰消息和安全操作。"
    },
    "security": {
      "model": "opencode/claude-opus-4.7",
      "description": "安全审计与漏洞分析",
      "prompt_append": "以安全专家视角审查代码，关注 OWASP Top 10 和常见漏洞模式。"
    },
    "test": {
      "model": "opencode/gpt-5.4-mini",
      "description": "测试用例生成",
      "prompt_append": "生成全面的测试用例，覆盖边界条件和异常场景。"
    }
  }
}
```

### 配置字段说明

| 字段 | 类型 | 必填 | 描述 |
|------|------|------|------|
| `model` | string | 是 | 指定的模型标识符 |
| `description` | string | 是 | Category 用途描述 |
| `prompt_append` | string | 否 | 追加到系统提示的指令 |

### 自定义 Category 最佳实践

1. **单一职责**：每个 Category 聚焦特定任务类型
2. **明确描述**：description 应清晰说明适用场景
3. **精简提示**：prompt_append 保持简洁，避免冗长指令
4. **合理选型**：根据任务特点选择合适的模型

---

## Category 与 Skill 的关系

Category 和 Skill 是互补的概念：

| 维度 | Category | Skill |
|------|----------|-------|
| 作用 | 模型路由 | 能力封装 |
| 配置位置 | opencode.json | SKILL.md |
| 用户感知 | 隐式（自动路由） | 显式（主动调用） |
| 可定制性 | 支持自定义 | 支持自定义 |

### 协作模式

```
Skill 定义能力边界 → Category 选择最优模型 → 执行任务
```

Skill 可以指定推荐的 Category，确保任务使用合适的模型执行。

---

## 常见问题

### Q: Category 是自动选择还是手动指定？

A: 默认情况下，OpenCode 会根据任务特征自动选择 Category。用户也可以在请求中显式指定 Category。

### Q: 如何查看当前使用的 Category？

A: 通过 `--verbose` 模式或查看日志可以观察到 Category 选择过程。

### Q: 自定义 Category 会覆盖内置 Category 吗？

A: 不会。自定义 Category 与内置 Category 并存，通过名称区分。

### Q: Provider Fallback 会跨 Category 吗？

A: 不会。Fallback 仅在同一 Category 内的模型间进行，确保任务类型的一致性。

---

> 最后更新：2026-06-02
