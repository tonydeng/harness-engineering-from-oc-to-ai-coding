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

---

## 修复计划与检查清单

> **执行状态**: 全部 P0(7项) 修复已完成 ✅ (2026-06-30)

### 优先级矩阵

| 优先级 | 项数 | 来源 |
|--------|------|------|
| **P0 🔴** | 7 | 导航重塑(对比矩阵+README) + 3 SDK 补丁 + 2 事实错误（已全部完成 ✅） |
| **P1 🟡** | 12 | 优化项（ecosystem.md、语言一致性、版本对齐） |
| **P2 🟢** | 8 | 企业级覆盖、分发机制、跨工具对比 |

### P0 修复项

| # | 问题 | 目标文件 | 操作 | 验证 |
|---|------|---------|------|------|
| B-P0-1 | **缺对比矩阵** | `src/appendix-b/ecosystem.md` | 添加 OpenCode vs Claude Code vs Pi Agent 功能对比表 ✅ 已完成 | 对比表存在 |
| B-P0-2 | **README 导航断链** | `src/README.md` | 修复指向附录B的内链路径 ✅ 已完成 | 点击跳转正常 |
| B-P0-3 | **版本号不一致（v1.16x vs v1.17x）** | `src/appendix-b/*.md` | 统一为最新版本号 ✅ 已完成 | 全书版本号一致 |
| B-P0-4 | **SDK 缺上下文管理** | `src/appendix-b/sdk-reference.md` | 补充上下文管理 API 说明 ✅ 已完成 | SDK 节完整 |
| B-P0-5 | **缺 maxTurns 参数** | `src/appendix-b/agent-config.md` | 补充 maxTurns 配置项说明 ✅ 已完成 | 参数完整 |
| B-P0-6 | **缺错误重试机制** | `src/appendix-b/sdk-reference.md` | 补充错误处理与重试策略 ✅ 已完成 | 机制说明完整 |
| B-P0-7 | **Hook 返回值不一致** | `src/appendix-b/hooks-system.md` | 统一 Hook 返回值格式文档 ✅ 已完成 | 文档一致 |

### 检查清单

- [x] B-P0-1: 对比矩阵已添加
- [x] B-P0-2: README 导航断链已修复
- [x] B-P0-3: 版本号已统一
- [x] B-P0-4: SDK 上下文管理已补充
- [x] B-P0-5: maxTurns 参数已补充
- [x] B-P0-6: 错误重试已补充
- [x] B-P0-7: Hook 返回值已统一
- [x] ✅ 最终验证：`mdbook build` 0 错误
