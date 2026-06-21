# 附录 B 全体审阅共识报告

**日期**: 2026-06-20
**范围**: 附录 B 全部 12 篇文章 + SUMMARY.md + README.md
**方法**: 5 个读者视角并行审阅 → 共识合成
**状态**: 已存档，待修复

---

## 审阅视角

| 代号 | 视角 | 负责人 |
|------|------|--------|
| R1 | 小白视角（新手入门） | Sisyphus-Junior |
| R2 | 配置用户视角（日常配置/整合） | Sisyphus-Junior |
| R3 | Agent 开发者视角（SDK/Agent 深度开发） | Sisyphus-Junior |
| R4 | 插件 API 开发者视角（Plugin/Skill 扩展） | Sisyphus-Junior |
| R5 | 决策者视角（技术选型/架构决策） | Sisyphus-Junior |

---

## 共识发现汇总

### 🚨 Tier 1 — P0 必须修复（7 项）

| # | 问题 | 提及 | 严重性 | 涉及文件 |
|---|------|------|--------|---------|
| 1 | 缺少 OpenCode vs Claude Code 统一对比/选型决策矩阵 | R1·R2·R3·R5 (4/5) | 极高 | README.md, capabilities.md ×2, ecosystem.md ×2 |
| 2 | README.md 缺少面向不同读者角色的导航引导 | R1·R2·R5 (3/5) | 高 | README.md |
| 3 | 版本号不一致（v1.16.x vs v1.17.x） | R2·R5 | 极高 | plugins.md, capabilities.md |
| 4 | 两篇 SDK 文章均缺少上下文窗口管理策略 | R3 | 高 | agent-sdk.md ×2 |
| 5 | 缺少 maxTurns / 运行时防护机制讨论 | R3 | 高 | agent-sdk.md ×2 |
| 6 | 缺少错误传播和重试策略 | R3·R4 (2/5) | 高 | agent-sdk.md ×2, plugins.md |
| 7 | Hook 返回值不一致 & 存在性矛盾 | R4 | 极高 | plugins.md, extensions.md |

### ⚡ Tier 2 — P1 强烈推荐（12 项）

| # | 问题 | 提及 | 涉及文件 |
|---|------|------|---------|
| 8 | 超长文章缺内部 TOC | R1·R2 | plugins.md, agent-architecture.md |
| 9 | capabilities/ecosystem 边界模糊 | R2·R1·R5 | capabilities.md, ecosystem.md |
| 10 | OMO 扩展 vs 原生边界不清晰 | R1·R2 | README.md |
| 11 | Plugin 缺 WebSocket/SSE 实时通信 | R4 | plugins.md |
| 12 | 代码示例多但设计决策解释少 | R1·R3·R4 | agent-sdk.md ×2 |
| 13 | CLI 命令缺失 | R2 | claudecode/commands.md |
| 14 | 术语首次出现缺乏说明 | R1 | README.md |
| 15 | SDK 示例硬编码 API 密钥 | R2 | agent-sdk.md ×2 |
| 16 | agent-architecture.md "何时使用"不够直接 | R5·R3 | agent-architecture.md |
| 17 | SDK vs 配置对比表缺"Why" | R5·R3 | agent-sdk.md ×2 |
| 18 | 后台任务多 Agent 协调缺管理讨论 | R5 | agent-architecture.md |
| 19 | 缺少 Managed Agents 讨论 | R2 | ecosystem.md 或 SDK 文章 |

### 🧹 Tier 3 — P2 锦上添花（8 项）

| # | 问题 | 提及 |
|---|------|------|
| 20 | Token 成本估算模型缺失 | R3 |
| 21 | OMO subagent vs task API 对比缺失 | R3 |
| 22 | Claude Code → OpenCode 迁移路径缺失 | R5 |
| 23 | 企业级特性覆盖不足 | R5 |
| 24 | SDK 类型定义导出细节缺失 | R4 |
| 25 | 认证/授权模式未说明 | R4 |
| 26 | claudecode/ecosystem.md 语言不一致 | R2 |
| 27 | 176K Stars 缺评价锚点 | R5 |

---

## 修复建议优先级

1. **先修 P0 的 7 项**（导航重塑 + 3 个 SDK 技术补丁 + 2 个事实错误）
2. **再做 P1 的 12 项优化**
3. **P2 的 8 项按资源情况选择处理**
