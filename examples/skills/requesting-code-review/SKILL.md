---
name: requesting-code-review
description: "在完成任务、实现主要功能或合并之前使用，验证工作是否符合需求"
allowed-tools:
  - read
  - grep
  - glob
metadata:
  version: "1.0.0"
  author: opencode-community
---

# Code Review Skill

## 审查维度

1. **正确性**
   - 逻辑是否正确
   - 边界条件是否处理
   - 错误处理是否完善

2. **可读性**
   - 命名是否清晰
   - 结构是否合理
   - 注释是否充分

3. **安全性**
   - 是否有安全风险
   - 敏感信息是否暴露
   - 权限是否合理

4. **性能**
   - 是否有性能问题
   - 资源是否合理使用
   - 是否有内存泄漏

## 输出规范

审查报告应包含：
- 问题列表（按严重程度排序）
- 改进建议
- 最佳实践参考
