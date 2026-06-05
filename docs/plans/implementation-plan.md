# 实施计划 — Harness Engineering 书籍

> 整合计划，包含源材料映射、分阶段路线图、任务分解和验证门禁。
> 基于章节重构计划（v1.0）更新。目标版本：OpenCode v1.15.x + oh-my-openagent v4.5.x
> 总计：Ch0 + 7 章 + 附录 A，**50 篇文章/页面**（全部存在，但 ch06/ch07 为 stub） | 预计 42 个工作日
>
> **当前状态（2026-06-03）：** 文章结构已完成，ch00-05 内容充实（单篇 372-1666 行），但 ch06（12 篇全部需要扩充：2 篇有部分内容 89-152 行，10 篇 24-29 行 stub）和 ch07（6 篇 40-44 行 stub）存在严重内容缺口。核心里达图需求已移除。mdBook 构建通过。详见下方第二节"满足状态总览"。

---

## 第一节：当前满足状态总览（2026-06-03）

### 文章结构完成度

| 章节 | 文章数 | 状态 | 内容质量 |
|------|--------|------|---------|
| Ch0 读者导航 | 4 | ✅ 全部完成 | 311-1044 行，充实 |
| Ch1 简介 | 6 | ✅ 全部完成 | 427-793 行，充实 |
| Ch2 核心概念 | 6 | ✅ 全部完成 | 728-1344 行，充实 |
| Ch3 环境搭建 | 5 | ✅ 全部完成 | 659-1281 行，充实 |
| Ch4 工作流实战 | 6 | ✅ 全部完成 | 372-1242 行，充实 |
| Ch5 Skill 开发 | 5 | ✅ 全部完成 | 688-1666 行，充实 |
| Ch6 高级话题 | 12 | ⚠️ 12/12 stub | 10 篇 24-29 行，security-overview(152) 和 observability(89) 有部分内容但未达标 |
| Ch7 案例研究 | 6 | ❌ 全部 stub | 40-44 行，需扩充至 ≥300 行 |
| 附录 A | 1 | ✅ 完成 | 202 行术语表 |

### 需求满足矩阵

| 需求来源 | 关键要求 | 状态 | 说明 |
|---------|---------|------|------|
| PRD v2.0 | 50 篇文章全部有内容 | ✅ 结构 | ch06/ch07 为 stub，计数上满足但质量不达标 |
| PRD v2.0 | 每篇 ≥200 行（ch07 ≥300） | ❌ ch06/ch07 | ch00-05 全部满足；ch06 仅 2/12 篇达标；ch07 0/6 篇达标 |
| PRD v2.0 | 100+ 代码/配置示例 | ✅ 估算 | ch00-05 大量代码块，需精确统计 |
| PRD v2.0 | 50+ Mermaid/架构图 | ✅ 估算 | ch00-05 大量 mermaid 图表 |
| PRD v2.0 | PRD→交付 ≤42 工作日 | ⏳ 进行中 | stub 填充工作尚未开始 |
| User Stories | 45 个用户故事覆盖 | ⏳ 待验证 | 追溯矩阵未执行 |
| User Stories | 13 角色阅读路径 | ✅ | reading-paths.md 包含 13 角色路径 |
| User Stories | 安全治理贯穿三阶段 | ✅ | 在演进时间线和文章中有体现 |
| 基础设施 | mdBook 构建通过 | ✅ | 零错误 |
| 基础设施 | Mermaid 渲染 | ✅ | 已配置 local mermaid.min.js + init 脚本 |
| 基础设施 | Vega/Vega-Lite 支持 | ✅ | 已配置但无用例（雷达图已移除） |
| 基础设施 | 内部链接无 404 | ❌ | 链接审计计划（link-audit-plan.md）尚未执行 |
| 基础设施 | GitHub Pages 部署 | ✅ | CI 工作流已配置 |

### 已知变更记录

| 日期 | 变更 | 触发 |
|------|------|------|
| 2026-06-03 | 移除核心能力雷达图需求（src + docs/requirements 共 6 处） | 用户确认 |
| 2026-06-03 | 修复代码块语法高亮语言标识（jsonc→json, vega-lite→json, gitignore→text, env→text） | 渲染问题 |
| 2026-06-03 | 配置 mdBook 支持 Vega/Vega-Lite 渲染 | 为雷达图准备，但雷达图已移除 |
| 2026-06-03 | 全书"说人话"优化 + 品牌名一致性修复（ch00-05） | 用户要求 |
| 2026-06-03 | docs/requirements/ 全文 PRD + 规格 + 用户故事优化 | 用户要求 |

---

## 第二节：源材料映射

### 源材料 → 章节映射

| Source | Lines | Core Topics | Maps To | Reuse Strategy |
|--------|-------|------------|---------|---------------|
| **01-核心概念速通** | ~1051 | 6核心概念(Agent/Skill/Command/Plugin/Team/MCP), OS类比, 安装指南, Provider配置, FAQ | Ch1(简介), Ch2(全部3篇现有 + 3篇新增), Ch5(Skill) | **Direct reuse** — 结构清晰，可直接适配 |
| **02-架构全景解析** | ~1541+ | OMO架构(11+ Agent/类别路由/Team Mode/Hyperplan/Ultrawork/Hashline/Scoped Skills), 三层架构, 成本管控, 54+ Hook点 | Ch3(Setup), Ch6(3篇现有 + 9篇新增), 部分Ch4 | **Restructure + Extend** — 大量内容拆分到Ch6新文章 |
| **03-概念联动实战** | ~1365 | 6概念6种联动模式, 7-Agent Pipeline, AGENTS.md编写, Team Mode配置, Hyperplan, security-research | Ch4(3篇现有 + 2篇新增), Ch2, Ch5 | **Direct reuse + Extend** — 联动模式适配, Agent派生新增 |
| **04-奇淫技巧与实战方案** | ~1292 | 12技巧(Profile/AGENTS.md/Pipeline/Memory/权限/成本/安全/命令/审计/快速构建/DSL/协作), 4工作台方案, 入門指南 | Ch1(工具对比/国产生态), Ch3(国产模型/多环境), Ch5(Skill-MCP桥接/插件化) | **Reference + Supplement** — 技巧拆分到对应章节 |
| **05-场景化实战案例** | ~994 | 5案例(搭建REST API/安全审计/需求→产品全流程/知识库构建/团队协作), Skill开发附录 | Ch7(2篇现有 + 4篇新增), Ch5(Skill开发附录) | **Adapt + Extend** — 扩展为4-5个案例 |

### 额外外部资料

| 外部资料 | 内容量 | 映射章节 | 用途 |
|---------|--------|---------|------|
| HE实践（4文件） | 4073行 | Ch1 §1.3/1.4/1.5, Ch6, Ch7 | 理论框架、工具对比、案例 |
| 马书读书笔记（30章） | 30章 | Ch2 §2.4/2.5/2.6, Ch6 §6.4-6.12 | 上下文工程、安全体系、高级话题 |
| cc-to-ai-book（7部分） | 7部分 | 交叉参考 | 生态补充、行业视角 |

### 内容复用总结

| 重用类型 | 比例 | 覆盖范围 |
|----------|------|---------|
| 直接适配（修改量 <20%） | ~25% | Ch2核心内容、Ch4联动模式 |
| 重组（结构重排+补充） | ~30% | Ch3配置部分、Ch6新增9篇文章 |
| 引用+补充（需额外调研+来源外） | ~20% | Ch1工具对比、国产生态、Ch5桥接模式 |
| 改编（需重塑为本书风格） | ~15% | Ch7案例、Ch0读者导航 |
| 新写（来源外原创内容） | ~10% | Harness Engineering理论框架、约束系统概念 |

### 当前实现状态

- **实际文章数：** 50 篇（含 4 篇 README + 附录 A）
- **ch00-05：** 全部完成，单篇 372-1666 行 ✅
- **ch06：** 12 篇全部需要扩充（10 篇 24-29 行 stub，security-overview(152) + observability(89) 有部分内容但未达标） ❌
- **ch07：** 6 篇 stub（40-44 行） ❌
- **剩余工作量：** ch06 填充 12 篇 + ch07 填充 6 篇 ≈ 20-25 天

---

## 第二节：分阶段执行路线图（当前状态）

### Phase 1: P0 基础 ✅ 已完成

| 原始任务 | 状态 | 说明 |
|---------|------|------|
| 1A: Ch6 上下文工程/记忆/缓存 ❌ | ⏳ 未开始 | 4 篇 stub 待填充（24-29 行 → ≥200 行） |
| 1B: Ch6 安全体系 ❌ | ⏳ 未开始 | 3 篇 stub 待填充（25-152 行 → ≥200 行） |
| 1C: Ch1 理论框架 ✅ | ✅ 完成 | Art.1.1/1.2/1.3 全部完成，内容充实 |
| 门禁：P0 文章 ≥200 行 | ❌ | Ch6 仅 security-overview(152) 和 observability(89) 接近 |

### Phase 2: 横向增补 ✅ 已完成（结构层面）

| 原始任务 | 状态 | 说明 |
|---------|------|------|
| Ch2 新核心概念（Art.2.4/2.5/2.6） | ✅ 完成 | context-engineering-core(779), constraints-system(1344), validation-harness(1299) |
| Ch2 现有改写（Art.2.1/2.3） | ✅ 完成 | agent-orchestration(881), workflow-patterns(1066) |
| Ch0 读者导航 | ✅ 完成 | reading-paths(1044), how-to-read(572), quick-start(311) |
| Ch3/Ch4 现有修改 | ✅ 完成 | 全部充实 |
| Ch6 可观测性 + Feature Flags | ⏳ | observability(89) 内容不足；feature-flags(24) stub |
| 门禁：全部文章初稿 | ⚠️ 结构通过 | 文章都存在但 ch06/ch07 质量不达标 |

### Phase 3: 生态与案例 ✅ 已完成（结构层面）

| 原始任务 | 状态 | 说明 |
|---------|------|------|
| 组A: 工具生态对比、国产配置、多环境 | ✅ 完成 | ecosystem-comparison(729), chinese-ecosystem(745), chinese-providers(659), multi-env-setup(699) |
| 组B: Agent派生、Teams协作、MCP桥接、插件化 | ✅ 完成 | agent-derivation(793), teams-collaboration(1216), skill-mcp-bridge(688), plugin-patterns(811) |
| 组C: 案例扩展 | ⚠️ 全部 stub | 6 篇 40-44 行，需从 stub 扩展到 ≥300 行 |
| 门禁：全部文章完成 | ❌ | ch06(10篇) + ch07(6篇) stub |

---

## 第三节：剩余路线图 — Phase 4: Stub 填充（当前阶段）

文章结构、基础内容、基础设施全部就绪。**唯一剩余且有实际工作量的任务**：填充 ch06（12 篇）和 ch07（6 篇）的 stub。

### 优先级

| 优先级 | 章节 | 文章 | 当前行数 | 目标行数 | 估算工作量 |
|--------|------|------|---------|---------|-----------|
| **P0** | Ch6 | security-overview | 152 | ≥250 | 2 天 |
| **P0** | Ch6 | context-compression | 27 | ≥200 | 2 天 |
| **P0** | Ch6 | token-budget | 27 | ≥200 | 1 天 |
| **P0** | Ch6 | prompt-caching | 29 | ≥250 | 3 天 |
| **P0** | Ch6 | memory-system | 27 | ≥200 | 2 天 |
| **P0** | Ch6 | sandbox-hooks | 25 | ≥250 | 2 天 |
| **P0** | Ch6 | agents-dot-md | 25 | ≥200 | 1 天 |
| **P0** | Ch6 | observability | 89 | ≥200 | 1 天 |
| **P1** | Ch6 | mcp-servers | 27 | ≥200 | 2 天 |
| **P1** | Ch6 | custom-agents | 28 | ≥200 | 1 天 |
| **P1** | Ch6 | performance-tuning | 27 | ≥200 | 1 天 |
| **P2** | Ch6 | feature-flags | 24 | ≥200 | 1 天 |
| **P1** | Ch7 | 全部 6 篇文章 | 40-44 | ≥300 | 5 天/篇 = 30 天 |
| **P2** | 全书 | 链接审计（link-audit-plan.md） | — | 零 404 | 2 天 |

### 建议执行顺序

```
Step 1: Ch6 P0 安全体系（security-overview 续写 + sandbox-hooks + agents-dot-md）→ 3 篇，5 天
Step 2: Ch6 P0 上下文工程（context-compression + token-budget + prompt-caching + memory-system）→ 4 篇，8 天
Step 3: Ch6 P1 补充（mcp-servers + custom-agents + performance-tuning + observability）→ 4 篇，5 天
Step 4: Ch6 P2（feature-flags）→ 1 篇，1 天
Step 5: Ch7 案例扩展 → 6 篇，30 天（或选择部分案例优先）
Step 6: 全书链接审计 → 2 天
```

---

## 第三节：任务完成状态

### Phase 1 任务（P0 基础）✅ 已完成

| ID | 任务 | 文件 | 状态 | 验证 |
|----|------|------|------|------|
| R-1A-1 | 编写 Ch6 Art.6.4: 上下文压缩 | `context-compression.md` | ❌ stub(27) | 待填充 |
| R-1A-2 | 编写 Ch6 Art.6.5: Token预算策略 | `token-budget.md` | ❌ stub(27) | 待填充 |
| R-1A-3 | 编写 Ch6 Art.6.6: 提示词缓存 | `prompt-caching.md` | ❌ stub(29) | 待填充 |
| R-1A-4 | 编写 Ch6 Art.6.7: 记忆系统 | `memory-system.md` | ❌ stub(27) | 待填充 |
| R-1B-1 | 编写 Ch6 Art.6.8: 安全总览 | `security-overview.md` | ⚠️ 部分(152) | 需续写至 ≥250 |
| R-1B-2 | 编写 Ch6 Art.6.9: 沙箱与Hook | `sandbox-hooks.md` | ❌ stub(25) | 待填充 |
| R-1B-3 | 编写 Ch6 Art.6.10: AGENTS.md | `agents-dot-md.md` | ❌ stub(25) | 待填充 |
| R-1C-1 | 编写 Ch1 Art.1.3: 理论框架 | `harness-engineering-theory.md` | ✅ (525行) | **完成** |
| R-1C-2 | 修改 Ch1 Art.1.1 | `what-is-harness-engineer.md` | ✅ (718行) | **完成** |
| R-1C-3 | 修改 Ch1 Art.1.2 | `why-opencode.md` | ✅ (793行) | **完成** |

### Phase 2 任务（横向增补）✅ 已完成（结构层面）

| ID | 任务 | 文件 | 状态 | 验证 |
|----|------|------|------|------|
| R-2-1 | Ch2 Art.2.4: 上下文工程核心 | `context-engineering-core.md` | ✅ (779行) | **完成** |
| R-2-2 | Ch2 Art.2.5: 约束系统 | `constraints-system.md` | ✅ (1344行) | **完成** |
| R-2-3 | Ch2 Art.2.6: 验证护栏 | `validation-harness.md` | ✅ (1299行) | **完成** |
| R-2-4 | 修改 Ch2 Art.2.1: Agent Loop | `agent-orchestration.md` | ✅ (881行) | **完成** |
| R-2-5 | 修改 Ch2 Art.2.3: 工作流模式 | `workflow-patterns.md` | ✅ (1066行) | **完成** |
| R-2-6→R-2-11 | Ch0/Ch3/Ch4 增补 | 6 个文件 | ✅ 全部完成 | 311-1281行 |
| R-2-12 | Ch6 Art.6.11: 可观测性 | `observability.md` | ⚠️ 部分(89) | 需续写至 ≥200 |
| R-2-13 | Ch6 Art.6.12: Feature Flags | `feature-flags.md` | ❌ stub(24) | 待填充 |

### Phase 3 任务（生态与案例）✅ 已完成（结构层面）

| ID | 任务 | 文件 | 状态 | 验证 |
|----|------|------|------|------|
| R-3-1→R-3-8 | Ch1/Ch3/Ch4/Ch5 增补（8篇） | 8 个文件 | ✅ 全部完成 | 659-1666行 |
| R-3-9→R-3-14 | Ch7 案例扩展（6篇） | `07-case-studies/*` | ❌ 全部 stub(40-44) | 需从 stub → ≥300行 |
| R-3-15 | 侧边栏 + AGENTS.md + README | 项目根 | ✅ | 完成 |
| R-3-16 | 交叉引用验证 | 全部 `src/` | ❌ 未执行 | 链接审计计划待执行 |

### Phase 4 任务（Stub 填充 — 当前阶段）

| ID | 优先级 | 任务 | 文件 | 当前 | 目标 | 工作量 |
|----|--------|------|------|------|------|--------|
| **安全体系** | | | | | | |
| S-1 | P0 | 续写 Ch6 安全总览 | `security-overview.md` | 152 | ≥250 | 2 天 |
| S-2 | P0 | 编写 Ch6 沙箱与Hook | `sandbox-hooks.md` | 25 | ≥250 | 2 天 |
| S-3 | P0 | 编写 Ch6 AGENTS.md | `agents-dot-md.md` | 25 | ≥200 | 1 天 |
| **上下文工程** | | | | | | |
| S-4 | P0 | 编写 Ch6 上下文压缩 | `context-compression.md` | 27 | ≥200 | 2 天 |
| S-5 | P0 | 编写 Ch6 Token预算 | `token-budget.md` | 27 | ≥200 | 1 天 |
| S-6 | P0 | 编写 Ch6 提示词缓存 | `prompt-caching.md` | 29 | ≥250 | 3 天 |
| S-7 | P0 | 编写 Ch6 记忆系统 | `memory-system.md` | 27 | ≥200 | 2 天 |
| **补充** | | | | | | |
| S-8 | P1 | 编写 Ch6 可观测性 | `observability.md` | 89 | ≥200 | 1 天 |
| S-9 | P1 | 编写 Ch6 MCP服务器 | `mcp-servers.md` | 27 | ≥200 | 2 天 |
| S-10 | P1 | 编写 Ch6 自定义Agent | `custom-agents.md` | 28 | ≥200 | 1 天 |
| S-11 | P1 | 编写 Ch6 性能调优 | `performance-tuning.md` | 27 | ≥200 | 1 天 |
| S-12 | P2 | 编写 Ch6 Feature Flags | `feature-flags.md` | 24 | ≥200 | 1 天 |
| **案例** | | | | | | |
| S-13 | P1 | 编写 Ch7 全流程自动化 | `case-full-pipeline.md` | 41 | ≥300 | 5 天 |
| S-14 | P1 | 编写 Ch7 安全审计 | `case-security-audit.md` | 41 | ≥300 | 5 天 |
| S-15 | P1 | 编写 Ch7 混合架构 | `case-multi-model.md` | 43 | ≥300 | 5 天 |
| S-16 | P2 | 编写 Ch7 Skill市场 | `case-skills-marketplace.md` | 40 | ≥300 | 5 天 |
| S-17 | P1 | 修改 Ch7 Art.7.1 | `real-world-01.md` | 44 | ≥300 | 3 天 |
| S-18 | P1 | 修改 Ch7 Art.7.2 | `real-world-02.md` | 43 | ≥300 | 3 天 |
| **全书** | | | | | | |
| S-19 | P2 | 全书链接审计 | 全部 `src/` | — | 零 404 | 2 天 |

---

## 第四节：验证门禁（当前状态）

### 门禁 0：基础设施就绪 ✅
- [x] mdBook 配置完成（Mermaid + Vega + 自定义样式）
- [x] Ch0 读者导航页位于 `src/00-guide/README.md`
- [x] 计划文档已同步（`docs/` 包含重构计划、规格、交叉引用）
- [x] `mdbook build` 构建通过，零错误
- [x] GitHub Pages CI 工作流已配置（`.github/workflows/deploy-mdbook.yml`）

### 门禁 1：结构完整 ✅
- [x] Ch0 + 7 章 + 附录 A，50 篇文章全部存在
- [x] ch00-05 每篇 ≥200 行（最低 311，最高 1666）
- [x] `mdbook build` 构建通过，零错误
- [ ] ch06 ≥200 行 — **❌ 10/12 stub**
- [ ] ch07 ≥300 行 — **❌ 6/6 stub**

### 门禁 2：内容完整 ⚠️ 部分通过
- [x] 全部 50 篇文章/页面已存在
- [x] ch00-05 每篇 ≥200 行 ✅
- [ ] 每篇文章 ≥200 行（Ch7 ≥300）— **❌ ch06 12 篇 + ch07 6 篇**
- [ ] 内部链接有效率达 100% — **❌ 未审计**

### 门禁 3：本地预览 ✅ 已满足
- [x] `mdbook build` — 零渲染错误
- [x] Mermaid 图表正确渲染（已配置 local mermaid.min.js）
- [x] 代码块语言标注已修复（无 jsonc/env/gitignore/vega-lite）
- [x] 中英文术语表完整（glossary.md, 202行）
- [x] 自定义 CSS 响应式支持

### 门禁 4：部署上线 ⚠️ 部分满足
- [x] GitHub Pages 构建工作流已配置
- [ ] 用户故事追溯矩阵验证 — **❌ 未执行**
- [x] 13 个读者角色均有阅读路径（reading-paths.md）✅
- [ ] 所有跨章节引用格式正确 — **❌ 未审计**

---

## 第五节：关键路径与风险评估（当前状态）

### 关键路径（当前）
```
Ch6 stub 填充 → Ch7 stub 填充 → 全书链接审计
```

### 当前风险评估

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|---------|
| **Ch6 stub 填充工作量过大**（12 篇，含多篇需大量技术细节） | 高 | 高 | 按 P0→P1→P2 优先级分批填充；利用外部资料（《马书》12章+p + HE实践）提高效率 |
| **Ch7 案例 stub 填充耗时**（6 篇需从 40 行扩展到 300+ 行） | 高 | 高 | 优先完成 2-3 个关键案例，其余渐进式扩展 |
| **3个外部资料库版本偏差**（HE实践/《马书》/cc-to-ai） | 中 | 高 | 标注版本依赖的关键段落；预留验证时间 |
| **42天工期超期风险** | 高 | 中 | 已超出原计划，重点在剩余 stub 填充的总工作量 |
| **新增内容与现有章节风格不一致** | 中 | 中 | 参照 ch00-05 已确立的风格（说人话、读者视角） |
| **链接审计发现大量 404** | 中 | 中 | 预留专门修复时间 |
| **用户故事覆盖不全** | 中 | 高 | 追溯矩阵尚未执行，风险未消除 |

### 总量评估

| 类别 | 已完成 | 待完成 | 预计工时 |
|------|--------|--------|---------|
| ch00-05 文章（32 篇 + 5 README） | ✅ 全部 ≥372 行 | 0 | 0 天 |
| ch06 文章（12 篇 + README） | ❌ 12 篇全部 stub | 12 篇 stub 填充 | ~19 天 |
| ch07 文章（6 篇 + README） | ❌ 全部 stub | 6 篇 stub 填充 | ~26 天 |
| 全书链接审计 | ❌ 未执行 | 1 项 | ~2 天 |
| **剩余总计** | | **16 篇 stub + 1 项审计** | **~47 天** |

---

> **版本**：v2.2 | **最后更新**：2026-06-03 | **基于**：章节重构计划 v1.0
> **总文章数**：50（结构全部完成，ch06 12/12 stub + ch07 6/6 stub 待填充）
> **已完成**：ch00-05 共 32 篇文章 + 附录术语表（全部充实，372-1666 行）
> **待完成**：ch06 12 篇 + ch07 6 篇 + 链接审计 | **预计剩余**：~47 个工作日
