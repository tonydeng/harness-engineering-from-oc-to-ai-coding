# 实施计划 — Harness Engineering 书籍

> 整合计划，包含源材料映射、分阶段路线图、任务分解和验证门禁。
> 基于章节重构计划（v1.0）更新。目标版本：OpenCode v1.15.x + oh-my-openagent v4.5.x
> 总计：Ch0 + 7 章，46 篇文章/页面（19 现有 + 27 新增） | 预计 42 个工作日

---

## 第一节：源材料映射

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
| 直接适配（修改量 <20%） | ~25% | Ch2核心内容、Ch4联动模式、现有19篇文章 |
| 重组（结构重排+补充） | ~30% | Ch3配置部分、Ch6新增9篇文章 |
| 引用+补充（需额外调研+来源外） | ~20% | Ch1工具对比、国产生态、Ch5桥接模式 |
| 改编（需重塑为本书风格） | ~15% | Ch7新案例4篇、Ch0读者导航 |
| 新写（来源外原创内容） | ~10% | Harness Engineering理论框架、约束系统概念 |

---

## 第二节：分阶段执行路线图

### Phase 1: P0 基础（并行 — 约 20 天）

**核心目标**：填补 P0 内容缺口，夯实全书理论基础。

| 阶段 | 任务 | 交付物 | 工作量 |
|------|------|--------|--------|
| **1A: Ch6 上下文工程/记忆/缓存** | 上下文压缩、Token预算、提示词缓存、记忆系统 | Ch6 Art.6.4-6.7（4篇P0文章） | 10 天 |
| **1B: Ch6 安全体系** | 安全总览、沙箱与Hook、CLAUDE.md系统 | Ch6 Art.6.8-6.10（3篇P0文章） | 7 天 |
| **1C: Ch1 理论框架** | Harness Engineering理论框架 + 现有文章修改 | Ch1 Art.1.3, Art.1.1修改, Art.1.2修改 | 5 天 |

**并行策略**：1A 先行启动（最大工作量），1B 依赖 Ch2 约束系统概念但可并行启动，1C 独立启动。

**门禁**：所有 P0 文章完成初稿 ≥ 200 行

### Phase 2: 横向增补（串行 — 约 12 天）

**核心目标**：为 Phase 1 提供前置概念，增补读者导航。

| 顺序 | 任务 | 交付物 | 工作量 |
|------|------|--------|--------|
| D1-D5 | Ch2 新核心概念 + 现有文章改写 | Art.2.4/2.5/2.6（3篇新）+ Art.2.1/2.3修改 | 5 天 |
| D6-D8 | Ch0 读者导航 + 现有文章修改（Ch3/Ch4） | reading-paths, how-to-read, Ch3 Art.3.2/3.3修改, Ch4 Art.4.1/4.2修改 | 3 天 |
| D9-D12 | Ch6 可观测性 + Feature Flags | Art.6.11/6.12（2篇）+ 其他文章润色 | 4 天 |

**依赖**：Phase 1 完成后启动

**门禁**：全部文章完成初稿，交叉引用正确

### Phase 3: 生态与案例（并行+串行 — 约 10 天）

**核心目标**：工具对比、国产生态、新增案例。

| 并行组 | 任务 | 交付物 | 工作量 |
|--------|------|--------|--------|
| **组A: 市场定位** | 工具生态对比、国产AI生态、国产模型配置、多环境部署 | Ch1 Art.1.4/1.5, Ch3 Art.3.4/3.5 | 4 天 |
| **组B: 模块增强** | Agent派生、Teams协作、Skill-MCP桥接、Skill插件化 | Ch4 Art.4.4/4.5, Ch5 Art.5.4/5.5 | 4 天 |
| **组C: 案例扩展** | 安全审计流水线、全流程自动化、混合架构、Skill市场 | Ch7 Art.7.3/7.4/7.5/7.6 + Art.7.1/7.2修改 | 6 天 |

**依赖**：Phase 2 完成后启动（组C概念依赖较多）

**门禁**：全部 46 篇文章完成，通过 L1 质量门禁

---

## 第三节：任务分解

### Phase 1 任务（P0 基础）

| ID | 任务 | 文件 | 工作量 | 依赖 | 验证标准 |
|----|------|------|--------|------|---------|
| R-1A-1 | 编写 Ch6 Art.6.4: 上下文压缩 | `src/06-advanced/context-compression.md` | XL | Ch2 Art.2.4概念 | ≥200行，含压缩机制 |
| R-1A-2 | 编写 Ch6 Art.6.5: Token预算策略 | `src/06-advanced/token-budget.md` | M | R-1A-1 | ≥200行，含预算分配 |
| R-1A-3 | 编写 Ch6 Art.6.6: 提示词缓存 | `src/06-advanced/prompt-caching.md` | XL | R-1A-1 | ≥250行，三级缓存 |
| R-1A-4 | 编写 Ch6 Art.6.7: 记忆系统 | `src/06-advanced/memory-system.md` | L | R-1A-1 | ≥200行，Memdir架构 |
| R-1B-1 | 编写 Ch6 Art.6.8: 安全总览 | `src/06-advanced/security-overview.md` | XL | Ch2 Art.2.5 | ≥250行，6权限模式 |
| R-1B-2 | 编写 Ch6 Art.6.9: 沙箱与Hook | `src/06-advanced/sandbox-hooks.md` | XL | R-1B-1 | ≥250行，53+ Hook |
| R-1B-3 | 编写 Ch6 Art.6.10: CLAUDE.md | `src/06-advanced/claude-dot-md.md` | M | R-1B-1 | ≥200行，@include系统 |
| R-1C-1 | 编写 Ch1 Art.1.3: Harness Engineering理论 | `src/01-introduction/harness-engineering-theory.md` | L | 无 | ≥200行，5大分类法 |
| R-1C-2 | 修改 Ch1 Art.1.1: 增补Hashimoto定义+Chase公式 | `src/01-introduction/what-is-harness-engineer.md` | S | 无 | 增补完整 |
| R-1C-3 | 修改 Ch1 Art.1.2: 增补OMO v4.5+特性 | `src/01-introduction/why-opencode.md` | S | 无 | 增补完整 |

### Phase 2 任务（横向增补）

| ID | 任务 | 文件 | 工作量 | 依赖 | 验证标准 |
|----|------|------|--------|------|---------|
| R-2-1 | 编写 Ch2 Art.2.4: 上下文工程核心 | `src/02-core-concepts/context-engineering-core.md` | M | Phase 1C | ≥200行 |
| R-2-2 | 编写 Ch2 Art.2.5: 约束系统 | `src/02-core-concepts/constraints-system.md` | M | R-2-1 | ≥200行 |
| R-2-3 | 编写 Ch2 Art.2.6: 验证护栏 | `src/02-core-concepts/validation-harness.md` | M | R-2-2 | ≥200行 |
| R-2-4 | 修改 Ch2 Art.2.1: 增补《马书》Agent Loop | `src/02-core-concepts/agent-orchestration.md` | S | R-2-1 | 增补完整 |
| R-2-5 | 修改 Ch2 Art.2.3: 增补6种工作流模式 | `src/02-core-concepts/workflow-patterns.md` | S | R-2-1 | 增补完整 |
| R-2-6 | 编写 Ch0 reading-paths.md | `src/00-guide/reading-paths.md` | M | 无 | ≥80行，13角色路径 |
| R-2-7 | 编写 Ch0 how-to-read.md | `src/00-guide/how-to-read.md` | S | R-2-6 | ≥50行 |
| R-2-8 | 修改 Ch3 Art.3.2: Category路由+新配置 | `src/03-setup/opencode-config.md` | M | R-2-1 | 增补完整 |
| R-2-9 | 修改 Ch3 Art.3.3: 11+ Agent注册表 | `src/03-setup/oh-my-openagent-setup.md` | M | 无 | 增补完整 |
| R-2-10 | 修改 Ch4 Art.4.1: Ralph Loop详解 | `src/04-workflows/ultrawork-mode.md` | S | 无 | 增补完整 |
| R-2-11 | 修改 Ch4 Art.4.2: Hyperplan+security-research | `src/04-workflows/multi-agent-collab.md` | M | 无 | 增补完整 |
| R-2-12 | 编写 Ch6 Art.6.11: 可观测性 | `src/06-advanced/observability.md` | L | R-1B-2 | ≥200行，5层遥测 |
| R-2-13 | 编写 Ch6 Art.6.12: Feature Flags | `src/06-advanced/feature-flags.md` | S | 无 | ≥200行 |

### Phase 3 任务（生态与案例）

| ID | 任务 | 文件 | 工作量 | 依赖 | 验证标准 |
|----|------|------|--------|------|---------|
| R-3-1 | 编写 Ch1 Art.1.4: 工具生态对比 | `src/01-introduction/ecosystem-comparison.md` | L | Phase 2 | ≥200行，6工具对比 |
| R-3-2 | 编写 Ch1 Art.1.5: 国产AI生态 | `src/01-introduction/chinese-ecosystem.md` | M | R-3-1 | ≥200行 |
| R-3-3 | 编写 Ch3 Art.3.4: 国产模型配置 | `src/03-setup/chinese-providers.md` | M | Phase 2 | ≥200行 |
| R-3-4 | 编写 Ch3 Art.3.5: 多环境部署 | `src/03-setup/multi-env-setup.md` | M | Phase 2 | ≥200行 |
| R-3-5 | 编写 Ch4 Art.4.4: Agent派生模式 | `src/04-workflows/agent-derivation.md` | L | Phase 2 | ≥200行 |
| R-3-6 | 编写 Ch4 Art.4.5: Teams多进程协作 | `src/04-workflows/teams-collaboration.md` | L | R-3-5 | ≥200行 |
| R-3-7 | 编写 Ch5 Art.5.4: Skill-MCP桥接 | `src/05-skills/skill-mcp-bridge.md` | M | Phase 2 | ≥200行 |
| R-3-8 | 编写 Ch5 Art.5.5: 插件化模式 | `src/05-skills/plugin-patterns.md` | M | R-3-7 | ≥200行 |
| R-3-9 | 编写 Ch7 Art.7.3: 安全审计流水线 | `src/07-case-studies/case-security-audit.md` | XL | Phase 2 | ≥300行 |
| R-3-10 | 编写 Ch7 Art.7.4: 全流程自动化 | `src/07-case-studies/case-full-pipeline.md` | XL | Phase 2 | ≥300行 |
| R-3-11 | 编写 Ch7 Art.7.5: 国产模型混合架构 | `src/07-case-studies/case-multi-model.md` | L | R-3-2, R-3-3 | ≥300行 |
| R-3-12 | 编写 Ch7 Art.7.6: 团队Skill市场 | `src/07-case-studies/case-skills-marketplace.md` | L | R-3-8 | ≥300行 |
| R-3-13 | 修改 Ch7 Art.7.1: 增补Fowler对照 | `src/07-case-studies/real-world-01.md` | M | Phase 2 | 增补完整 |
| R-3-14 | 修改 Ch7 Art.7.2: 增补灰度策略 | `src/07-case-studies/real-world-02.md` | M | Phase 2 | 增补完整 |
| R-3-15 | 更新侧边栏 + AGENTS.md + README | 项目根目录 + `src/` | S | 所有文章完成 | 所有链接有效 |
| R-3-16 | 交叉引用验证 + 术语一致性 | 全部 `src/` 文件 | M | R-3-15 | 无404链接 |

---

## 第四节：验证门禁

### 门禁 0：基础设施就绪（写作开始前）
- [ ] `src/index.html` 加载所有插件（mermaid、pagination、copy-code、prism多语言支持）
- [ ] Ch0 读者决策页位于 `src/00-guide/README.md`
- [ ] 计划文档已同步（`docs/` 包含重构计划、规格、交叉引用）
- [ ] `mdbook serve` 启动无错误
- [ ] 所有侧边栏链接可访问（导航无404）

### 门禁 1：结构完整（Phase 1 结束）
- [ ] Ch0 + 7 章，所有 P0 文章已存在（无 TODO 占位符）
- [ ] 每篇文章 ≥ 200 行有效内容
- [ ] Ch6 至少 7 篇 P0 文章完成初稿
- [ ] `mdbook serve` 启动无错误

### 门禁 2：内容完整（Phase 2 结束）
- [ ] 全部 46 篇文章/页面已存在
- [ ] 每篇文章 ≥ 200 行（Ch7 文章 ≥ 300 行）
- [ ] 总计 50+ 个代码/配置示例
- [ ] 总计 30+ 张 Mermaid 图表
- [ ] 所有 Harness Engineering 核心主题出现在各章节概览中
- [ ] 内部链接有效率达 100%

### 门禁 3：本地预览（Phase 3 结束）
- [ ] `mdbook serve` — 无渲染错误
- [ ] 所有 Mermaid 图表正确渲染
- [ ] 所有内部链接可访问（无404）
- [ ] 代码块包含语言标注
- [ ] 中英文术语表完整
- [ ] 移动端视口响应式（无水平滚动）

### 门禁 4：部署上线（最终）
- [ ] GitHub Pages 构建成功
- [ ] 45 个用户故事全部覆盖（追溯矩阵验证）
- [ ] 13 个读者角色均有对应的阅读路径
- [ ] 所有跨章节引用格式正确

---

## 第五节：关键路径与风险评估

### 关键路径
```
Ch1理论框架 → Ch2新核心概念 → Ch6上下文工程 → Ch6安全体系 → Ch7案例扩展
```

Ch6 上下文工程（4 篇 P0 文章）是最长的关键路径，建议优先启动。Ch7 案例扩展（4 篇长文 Ch7 + 2 篇修改）依赖所有前置概念，最晚启动。

### 风险评估

| 风险 | 可能性 | 影响 | 缓解措施 |
|------|--------|------|---------|
| **Phase 1 Ch6 工作量过大**（4+3篇共7篇P0，含多篇XL） | 高 | 高 | 将Ch6拆分为1A/1B并行子阶段；优先保证P0前4篇质量 |
| **3个外部资料库版本偏差**（HE实践/《马书》/cc-to-ai） | 中 | 高 | 标注版本依赖的关键段落；预留验证时间 |
| **42天工期超期风险** | 中 | 中 | Phase间各预留2天缓冲；压缩Phase 3非核心任务 |
| **新增文章与现有19篇文章风格不一致** | 中 | 中 | 每个Phase结束进行风格一致性审查 |
| **新核心概念（Ch2 §2.4-2.6）与现有概念重叠** | 低 | 中 | Ch2新概念设计为"现有概念的深化和系统化"，非替代 |
| **13个角色45个故事覆盖不全** | 中 | 高 | Phase 3结束后用追溯矩阵逐一验证 |

### 缓冲策略
- **Phase 1 → 2**：预留 2 天缓冲（知识消化期）
- **Phase 2 → 3**：预留 2 天缓冲（内容审查期）
- **Phase 3 后**：预留 5 天用于终审、部署、社区反馈

---

> **版本**：v2.0 | **最后更新**：2026-05-31 | **基于**：章节重构计划 v1.0
> **总文章数**：46（19 现有 + 27 新增）| **总任务数**：39 | **预计**：42 个工作日
