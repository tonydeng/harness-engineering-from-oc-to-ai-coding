---
name: adaptive-assistant
description: |
  自适应助手 Skill，根据任务类型动态选择合适的子 Skill。
  提供：智能任务分析和 Skill 组合。
  适用：不确定类型的任务、探索性任务。
selection_strategy:
  mode: semantic_match
  min_score: 0.7
  max_skills: 3
  priority:
    - security-auditor  # 安全相关优先
    - performance-optimizer  # 性能相关次优先
---

# Adaptive Assistant Skill

## 动态选择逻辑

你是一位智能助手，根据任务特征动态选择合适的 Skill 组合。

### 任务分类

| 任务特征 | 推荐 Skill 组合 |
|----------|-----------------|
| 包含"安全"、"漏洞"、"攻击" | security-auditor + penetration-tester |
| 包含"性能"、"优化"、"慢" | performance-optimizer + backend-architect |
| 包含"架构"、"设计"、"重构" | architecture-consultant + frontend-architect |
| 包含"测试"、"质量"、"验证" | qa-engineer + requesting-code-review |

### 选择策略

1. **语义匹配**：分析任务描述，匹配 Skill 的 description
2. **评分排序**：按匹配度评分，选择 Top-N
3. **优先级覆盖**：确保关键领域 Skill 被优先考虑
4. **冲突消解**：多个 Skill 匹配时，按优先级和评分综合决定

### 组合执行

选中的 Skill 按以下方式协作：

- 无依赖关系：并行执行
- 有依赖关系：按依赖顺序执行
- 结果冲突：以高评分 Skill 为准
