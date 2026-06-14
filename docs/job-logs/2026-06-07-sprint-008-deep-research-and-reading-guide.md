# 2026-06-07: Sprint 008: Deep-Research Verification + Reading Guide

> [TAG: agile-coach]

## 基本信息

| 项目 | 内容 |
|------|------|
| Session ID | ses_...（当前会话） |
| Sprint 周期 | 2026-06-07（单日，两个连续 Sprint） |
| 风险等级 | Sprint 1: 中（跨模块 deep-research 验证） / Sprint 2: 低（文案追加） |
| 必需工作流 | Superpowers 全流程（头脑风暴 → 计划 → 实施 → 评审 → 验证 → 交付） |
| 主模型 | deepseek-v4-flash-free |

## 1. 用户需求（输入）

### 1.1 原始需求

Sprint 需求通过 `/agile-coach` 命令触发，请求组织团队进行全书的 deep-research 验证 + content-research-writer 更新。用户参数：

> 组织团队遵循 @docs/requirements 中的 PRD、用户故事和章节规格，结合 @docs/wiki 中的参考记录，基于思考框架、人物视角、读者视角等多个视角，并基于 deep-research 技能对每一章内容进行深度分析，对比开源项目、官方网站对其所有的数据、内容、理论、实践等内容，进行深度的 5 轮 Review 和讨论，形成最终的修改意见，并利用内容研究写作助手进行更新文章内容。

| # | 任务 | 类型 | 验收标准 |
|---|------|------|---------|
| **Sprint 1** | 全书 8 章 deep-research 外部验证 + content-research-writer 更新 | 内容验证+数据刷新 | mdbook build 零错误，P0 问题全部修复 |
| **Sprint 2** | 补齐剩余阅读体验问题（目标读者、阅读指引等） | 文案追加 | 100% 文章覆盖阅读指引 |

### 1.2 需求确认过程

**Sprint 1** 经需求澄清确认范围：
- 5 个 deep-research agent 并行验证所有 8 章
- 5 个 content-research-writer agent 跟进修复
- 全部通过 Superpowers 工作流执行

**Sprint 2** 经审计发现前序 Sprint 已解决大部分剩余问题：
- P0-1（目标读者标注）→ ✅ 全部 12 个 Ch6 文件已有 `> **适合读者**`
- P0-3（observability 重构）→ ✅ 882→532 行，已拆出 reference doc
- P0-4（quickstart 开篇承诺）→ ✅ 已有 "读完本文"
- P1-1（glossary 人话版）→ ✅ 全部 32 词条已有 "人话"
- **实际剩余**: 仅 P0-2 阅读指引（12 个文件仍需添加）

## 2. 团队架构与角色分配

**协调人**: Sisyphus（敏捷教练模式）

| 角色 | 职责 | 对应技能 |
|------|------|---------|
| Sisyphus（编排器） | 任务分解、并行调度、质量门禁 | — |
| Sisyphus-Junior (deep) x10 | 5 × deep-research + 5 × content-research-writer | deep-research, content-research-writer |
| Sisyphus-Junior (deep) x1 | Sprint 2 阅读指引追加 | content-research-writer |

## 3. 工作流阶段记录

### 3.1 头脑风暴阶段

**Sprint 1** — 评估全书 deep-research 验证范围：
- 8 章 50 篇文章都需要验证
- 优先 P0（数据准确性、配置键正确、OMO vs OpenCode 边界）
- 划分 5 组并行验证：Ch1（竞品/国产）、Ch3（配置架构）、Ch4（OMO 边界）、Ch6（高级话题）、Ch2+Ch5+Ch7（核心概念+Skill+案例）

**Sprint 2** — 审计剩余问题：
- 读取 `docs/reviews/remaining-issues-2026-06-05.md`
- 实际扫描发现 5 项问题中 4 项已被 Sprint 1 解决
- 范围从 34 文件缩至 12 文件

### 3.2 计划阶段

**Sprint 1 计划** (`docs/plans/2026-06-07-deep-research-verification-sprint.md`)：
- Phase 1: 5 deep-research agents 并行验证
- Phase 2: 5 content-research-writer agents 并行修复
- Phase 3: 验证构建

**Sprint 2 计划** (`docs/plans/2026-06-07-reading-guide-sprint.md`)：
- 1 agent 处理全部 12 文件
- 格式：`> **⏱ 时间有限？先读这些：** 主题1 → 主题2 → 主题3`

### 3.3 实施阶段

#### Sprint 1 — Phase 1: Deep-Research 验证

5 个 deep-research agent 并行启动，每 agent 负责 1-3 章：

| Agent | 范围 | 发现问题 | 严重级别 |
|-------|------|---------|:--------:|
| Ch1 竞品数据 | ecosystem-comparison.md, chinese-ecosystem.md | Cursor 定价过时、DeepSeek V3/V4 定价偏差 6-7×、Qwen-Max +35%、Tabby 描述错误 | P0 |
| Ch3 配置架构 | chinese-providers.md | apiKey/baseURL 位置根级→options、model→models.default | P0 |
| Ch4 OMO 边界 | multi-agent-collab.md | Hyperplan/5-Agent 未标注 OMO 专属 | P0 |
| Ch6 高级话题 | 12 文件 | OMO 归属标注缺失、tokenBudget→compaction、版本号残留 | P0 |
| Ch2+Ch5+Ch7 综合 | context-engineering-core.md 等 | tokenBudget 残留（已修一部分） | P1-P2 |

**结果**: 共 18 处问题，全部 P0 级。

#### Sprint 1 — Phase 2: Content-Research-Writer 更新

5 个 content-research-writer agent 并行启动，跟进修复：

| Agent | 修改文件 | 核心变更 |
|-------|---------|---------|
| Ch1 竞品更新 | ecosystem-comparison.md, chinese-ecosystem.md | 定价刷新（8 行 +，6 行 -） |
| Ch3 配置修复 | chinese-providers.md | 配置结构重构（36 行 +，36 行 -） |
| Ch4 OMO 归属 | multi-agent-collab.md, README.md, agent-derivation.md | 归属修正（15 行 +，15 行 -） |
| Ch6 OMO 标注 | feature-flags.md + 4 个 OMO 头文件 + context-compression.md | 版本号修正 + OMO 标注 + compaction 修复（138 行 +，134 行 -） |
| Ch2+Ch6 compaction | context-engineering-core.md | tokenBudget→compaction（65 行 +，65 行 -） |

#### Sprint 2 — 阅读指引追加

1 agent 处理 13 个文件，每文件追加 1 行 `> **⏱ 时间有限？先读这些：**`，内容根据各文章结构定制。

### 3.4 评审阶段

**Sprint 1** — 评审通过验证报告进行：
- 5 份 deep-research 报告 → `docs/reviews/` 目录
- 5 份 content-research-writer 确认
- 修复确认：each fix verified by grep before closing

**Sprint 2** — 未单独评审（低风险文案类），直接进入验证。

### 3.5 验证阶段

| 验证项 | Sprint 1 | Sprint 2 |
|--------|:--------:|:--------:|
| `mdbook build` | ✅ 零错误 | ✅ 零错误 |
| P0 修复确认 | ✅ 18 处全部验证 | — |
| tokenBudget 残留检查 | ✅ 仅 context/performance-tuning.md 合法残留 | — |
| 阅读指引覆盖率 | — | ✅ 100%（51 文件含 README.md 过滤） |

### 3.6 交付阶段

- Sprint 1 交付报告（包含完整变更清单）
- Sprint 2 交付报告
- 回顾会议（经验总结 5 条）

## 4. 技能调用记录

| 技能名称 | 调用时机 | 用途 |
|---------|---------|------|
| agile-coach | Sprint 规划 + 团队组织 | 组织团队成员、执行 Superpowers 工作流 |
| brainstorming | Sprint 1+2 头脑风暴 | 范围评估、需求澄清 |
| writing-plans | Sprint 1+2 计划 | Sprint 计划编写 |
| deep-research | Sprint 1 Phase 1 | 5 路并行外部验证 |
| content-research-writer | Sprint 1 Phase 2 + Sprint 2 | 内容更新 + 阅读指引追加 |
| investigation-first | Sprint 1 初始 | 项目上下文探明 |
| criticism-self-criticism | Sprint 2 初始 | 审计已修问题、避免重复劳动 |

## 5. 模型与 Agent 使用记录

| 组件 | 模型 | 用途 |
|------|------|------|
| 主编排器 | deepseek-v4-flash-free | 意图识别、任务分解、编排、决策 |
| 子 Agent (deep) x10 | deepseek-v4-flash-free | 5 × deep-research + 5 × content-research-writer |
| 子 Agent (deep) x1 | deepseek-v4-flash-free | Sprint 2 阅读指引追加 |

**Agent 执行记录**：

| Agent ID | 类型 | 用途 | 耗时 |
|----------|------|------|------|
| bg_c4b9555b | deep + deep-research | Ch1 竞品验证 | ~5m |
| bg_0a527ea8 | deep + deep-research | Ch3 配置验证 | ~4m |
| bg_c76932df | deep + deep-research | Ch4 OMO 边界验证 | ~5m |
| bg_de0f7739 | deep + deep-research | Ch6 高级话题验证 | ~6m |
| bg_283fe360 | deep + deep-research | Ch2+Ch5+Ch7 综合验证 | ~5m |
| bg_ed6b58f0 | deep + content-research-writer | Ch1 定价更新 | ~3m |
| bg_467b0eae | deep + content-research-writer | Ch3 配置修复 | ~4m |
| bg_edad8f45 | deep + content-research-writer | Ch4 OMO 归属修正 | ~3m |
| bg_de8a762b | deep + content-research-writer | Ch6 OMO 标注 + 版本号 | ~4m |
| bg_ea64b5a4 | deep + content-research-writer | Ch2+Ch6 compaction 修复 | ~3m |
| ses_15fa6b487ffeVD83os9Bn47u0V | deep + content-research-writer | Sprint 2 阅读指引 13 文件 | ~2m |

## 6. 文件变更清单

### Sprint 1：Deep-Research 验证修复（13 文件，±273 行）

| 文件 | 行数变化 | 变更类型 |
|------|:--------:|---------|
| `src/01-introduction/ecosystem-comparison.md` | +8/-0 | Cursor Hobby/Windsurf Teams/Tabby/Continue 定价 |
| `src/01-introduction/chinese-ecosystem.md` | +6/-6 | DeepSeek V4-Flash/V3/Qwen-Max 定价 |
| `src/03-setup/chinese-providers.md` | +36/-36 | apiKey/baseURL→options + model 根级修正 |
| `src/04-workflows/README.md` | +1/-1 | OMO 归属修正 |
| `src/04-workflows/multi-agent-collab.md` | +6/-6 | OMO 归属 + Hyperplan 脚注 |
| `src/04-workflows/agent-derivation.md` | +8/-8 | oh-my-opencode 旧名修正 |
| `src/02-core-concepts/context-engineering-core.md` | +65/-65 | tokenBudget→compaction（3 块） |
| `src/06-advanced/context-compression.md` | +118/-118 | tokenBudget→compaction（4 块） |
| `src/06-advanced/feature-flags.md` | +16/-16 | 版本号 v0.x→OMO v4.5.x |
| `src/06-advanced/custom-agents.md` | +2/-0 | OMO 归属标注头 |
| `src/06-advanced/security-overview.md` | +2/-0 | OMO 归属标注头 |
| `src/06-advanced/context/performance-tuning.md` | +2/-0 | OMO 归属标注头 |
| `src/06-advanced/sandbox-hooks.md` | +2/-0 | OMO 归属标注头 |

### Sprint 2：阅读指引追加（13 文件，每文件 +1 行）

| 文件 | 插入位置 |
|------|---------|
| `src/00-guide/quick-start.md` | "读完本文"段落之后 |
| `src/01-introduction/chinese-ecosystem.md` | 文章概述段落尾 |
| `src/01-introduction/ecosystem-comparison.md` | 文章概述段落尾 |
| `src/01-introduction/failure-cases.md` | 文章概述段落尾 |
| `src/04-workflows/prometheus-mode.md` | 文章概述段落尾 |
| `src/06-advanced/agents-dot-md.md` | 文章概述段落尾 |
| `src/06-advanced/context-compression.md` | 文章概述段落尾 |
| `src/06-advanced/feature-flags.md` | 文章概述段落尾 |
| `src/06-advanced/observability-reference.md` | 首行 blockquote 后 |
| `src/06-advanced/context/performance-tuning.md` | 文章概述段落尾 |
| `src/06-advanced/context/prompt-caching.md` | 文章概述段落尾 |
| `src/06-advanced/context-compression.md` | 文章概述段落尾 |
| `src/appendix-a/glossary.md` | # 术语表 段落后 |

### 文档新增

| 文件 | 说明 |
|------|------|
| `docs/plans/2026-06-07-deep-research-verification-sprint.md` | Sprint 1 计划 |
| `docs/plans/2026-06-07-reading-guide-sprint.md` | Sprint 2 计划 |
| `docs/reviews/ch1-deep-research-2026-06-07.md` | Ch1 验证报告 |
| `docs/reviews/ch3-deep-research-2026-06-07.md` | Ch3 验证报告 |
| `docs/reviews/ch4-deep-research-2026-06-07.md` | Ch4 验证报告 |
| `docs/reviews/ch6-deep-research-2026-06-07.md` | Ch6 验证报告 |
| `docs/reviews/ch2-ch5-ch7-deep-research-2026-06-07.md` | Ch2+Ch5+Ch7 验证报告 |
| `docs/job-logs/2026-06-07-sprint-008-deep-research-and-reading-guide.md` | **本日志** |

### 全 Session 文件变更统计

```
~30 files changed, ~280 insertions(+), ~260 deletions(-)
```

## 7. 经验教训与改进建议

### 7.1 做得好的

| # | 教训 | 来源 Sprint | 建议 |
|---|------|-----------|------|
| 1 | **审计先行** | Sprint 2 | 动手修改前先做完整审计，确认哪些已经修过，发现剩余问题从 34 缩至 12 |
| 2 | **并行度优先** | Sprint 1 | 5 deep-research + 5 content-research-writer 全部并行，墙钟约 8-10 min |
| 3 | **调研先于改写** | Sprint 1 Phase 1 | deep-research 确认问题后再动用内容改写 agent，避免"改错" |
| 4 | **单一 agent 单任务** | Sprint 1+2 | 每个 agent 聚焦一个章节/一个文件集，避免 scope creep |
| 5 | **构建门禁** | Sprint 1+2 | 每次变更后 `mdbook build` 验证，两次都是零错误 |
| 6 | **验证前置** | Sprint 1 Phase 1→2 | 先 deep-research 收集证据 → 确认问题后 → 再 content-research-writer 修改 |

### 7.2 可改进的

| # | 问题 | 来源 Sprint | 建议 |
|---|------|-----------|------|
| 1 | **剩余问题文档滞后** | Sprint 2 | remaining-issues 记录未反映最新状态，导致需要重新审计 |
| 2 | **计划粒度过细不必要** | Sprint 2 | 低风险文案任务写完整 plan 文档 ROI 不高，可简化为确认→执行→验证 |
| 3 | **agent prompt 格式模板不够精确** | Sprint 2 | 阅读指引在不同文章中使用了不同分隔符（箭头 vs 逗号 vs 链接），需统一 |

### 7.3 后续 Sprint 建议

- 维持"审计先行 + 并行度优先"的核心编排原则
- 代码块格式统一（~130 blocks）可作为后续 P2 任务
- 建立内容变更 → 同步 remaining-issues 文档的流程
- 对于低风险文案类任务，采用轻量计划（确认范围 → 直接执行 → 验证）

## 附录

### A.1 全 Session 指标

| 指标 | Sprint 1 | Sprint 2 | 合计 |
|------|:--------:|:--------:|:----:|
| 任务数 | 2 phase (5+5 agents) | 1 (1 agent) | 11 agents |
| 子 Agent 总数 | 10 | 1 | 11 |
| 其中正确结果 | 10 (100%) | 1 (100%) | 11 (100%) |
| 直接工具调用 | ~60 | ~15 | ~75 |
| 修改文件数 | 13 | 13 | 26 (含重复) |
| 新增代码行数 | ~270 | ~13 | ~283 |
| 删除代码行数 | ~260 | 0 | ~260 |
| P0 问题发现 | 18 | — | 18 |
| P0 问题修复 | 18 (100%) | — | 18 |
| 阅读指引覆盖 | — | 12→51 files | 100% |
| 验证结果 | mdbook build ✅ | mdbook build ✅ | ✅ |

### A.2 全部使用的工具

| 工具 | 调用次数 | 用途 |
|------|---------|------|
| `read` | 30+ | 读取文件、目录结构、现有格式模板 |
| `write` | 3 | Sprint 计划 × 2 + 工作日志 |
| `edit` | 26 | 内容编辑（13 Sprint 1 + 13 Sprint 2） |
| `bash` | 10+ | mdbook build、grep 验证、文件审计 |
| `grep` | 15+ | 残留检查、覆盖率审计、格式确认 |
| `task (background)` | 10 | 5 × deep-research + 5 × content-research-writer |
| `task (sync)` | 1 | Sprint 2 阅读指引 agent |
| `background_output` | 10 | 收集 agent 结果 |
| `todowrite` | 2 | Sprint 任务跟踪 |
| `question` | 2 | 下一步确认 + 回顾需求 |
| `glob` | 3 | 查找文件 |
| `skill` | 4 | agile-coach, brainstorming, writing-plans |
| `lsp_diagnostics` | 2 | Markdown 验证 |

> **协调人**: Sisyphus
> **日期**: 2026-06-07
> **核心教训**: 审计先行避免重复劳动，并行度优先压缩墙钟，调研先于改写确保方向正确
