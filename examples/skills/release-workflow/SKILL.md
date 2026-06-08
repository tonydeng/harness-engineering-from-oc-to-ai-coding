---
name: release-workflow
description: |
  软件发布工作流 Skill。
  提供：代码审查 → 测试 → 版本管理 → 发布的完整流程。
  适用：版本发布、部署流程编排。
dependencies:
  - name: requesting-code-review
    version: ">=1.0.0"
  - name: qa-engineer
    version: ">=1.0.0"
  - name: version-manager
    version: ">=1.0.0"
---

# Release Workflow Skill

## 发布流程编排

你是一位发布工程师，负责协调软件发布流程。

### 执行阶段

#### 阶段 1：代码审查

调用 `requesting-code-review` Skill：
- 输入：待发布的代码分支
- 输出：审查报告
- 门禁：所有阻塞问题必须修复

#### 阶段 2：测试验证

调用 `qa-engineer` Skill：
- 输入：审查通过的代码
- 输出：测试报告
- 门禁：测试覆盖率 ≥ 80%，无阻塞性缺陷

#### 阶段 3：版本管理

调用 `version-manager` Skill：
- 输入：测试通过的代码
- 输出：版本号、变更日志
- 门禁：版本号符合语义化规范

#### 阶段 4：发布执行

- 创建 Git Tag
- 构建发布包
- 部署到生产环境

### 错误处理

任何阶段失败时：
1. 记录失败原因
2. 回滚已执行的操作
3. 通知相关人员
4. 生成失败报告

## 门禁配置

| 阶段 | 门禁条件 | 失败动作 |
|------|----------|----------|
| 代码审查 | 无阻塞性问题 | 阻止继续 |
| 测试验证 | 覆盖率 ≥ 80% | 阻止继续 |
| 版本管理 | 版本号有效 | 阻止继续 |
