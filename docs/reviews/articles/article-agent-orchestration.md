# 综合评审：agent-orchestration.md

> **目标文件**: `src/02-core-concepts/agent-orchestration.md`
> **评审日期**: 2026-06-06

---

## 评审概述

本文从三个独立视角对 `agent-orchestration.md` 进行了交叉评审：

| 视角 | 评审人 | 核心关注 |
|------|--------|---------|
| **Karpathy（工程现实主义）** | Andrej Karpathy 视角 | 技术准确性、事实错误核实、版本与配置正确性 |
| **Munger（逆向思维 + 激励分析）** | Charlie Munger 视角 | 分类谬误、认知偏误叠加、能力圈审计、概念框架验证 |
| **TechLead（生产环境验证）** | 技术负责人视角 | 生产就绪度、配置正确性、架构完整性、修复优先级 |

**总体结论**: 文章的概念框架（Agent = Model + Tools + Skills + Memory、OMO 核心 Agent、Plan/Build 模式区分）被各视角一致认可为准确。但存在 **3 个关键事实错误**，会导致读者在实际使用时立即出错。

---

## 各视角发现汇总

### Karpathy 视角：技术准确性审查

**核心发现**: 文章包含 **3 个严重事实错误** 和 **5 个中等问题**。

**✅ 验证准确的内容**:
- OpenCode 3 层架构（CLI → Agent → Tool → Provider → Extension）
- Plan/Build 模式区分
- OMO 核心 Agent（Sisyphus、Prometheus、Atlas、Hephaestus、Oracle）
- Category 路由系统
- Ultrawork 和 Prometheus 模式
- Agent = Model + Tools + Skills + Memory 公式
- Hidden Agents（compaction、title、summary）存在性
- @general、@explore、@scout 的 Subagent 调用语法

**❌ 严重错误（必须修复）**:

| # | 问题 | 影响 |
|---|------|------|
| 1 | **Plan 模式权限**: 声称"默认拒绝所有文件编辑和命令执行"（`deny`），实际为 `ask` 模式（需用户确认） | 安全文档错误，用户预期自动拒绝却收到确认提示 |
| 2 | **Subagent 写权限**: 声称"Subagent 默认不能编辑文件"，实际 @general 具有完整工具访问权限（含文件写入） | 权限模型根本性错误，可能造成安全隐患 |
| 3 | **配置文件路径**: `opencode.yml` 应为 `opencode.json`；`.opencode/config.jsonc` 应为 `.opencode/oh-my-openagent.jsonc` | 用户按文档操作会立即遇到配置错误 |

**🟡 中等问题**:

| # | 问题 | 修正建议 |
|---|------|---------|
| 4 | 版本号不一致：Line 568 使用 v1.16.x，Line 674 使用 v1.15.x | 统一为 v1.16.x |
| 5 | Agent 数量误分类："7 种 Agent 类型"应为 2 种类型、8 个实例 | 修正分类描述 |
| 6 | "马书"章节引用错误：声称第 4 章，实际 Agent Loop 在第 3 章 | 改为第 3 章 |
| 7 | Compaction 阈值（80%/40%）无官方依据 | 改为定性描述"接近上限" |

**🟢 低优先级**:
- @scout Agent 仅出现在本文，未在官方文档中出现，需验证
- Trust Boundary 图应将 @general 标记为可写

---

### Munger 视角：逆向思维 + 激励分析

**核心判断**: 文章**概念框架可靠但事实细节不可靠**。

**逆向思维检验（5 个关键问题）**:

| # | 逆向问题 | 文章声称 | 实际状态 | Munger 评价 |
|---|---------|---------|---------|------------|
| 1 | 如果 OpenCode 没有 7 种 Agent？ | "7 种 Agent 类型" | 2 种类型、8 个实例 | **分类谬误**——混淆类型和实例层次 |
| 2 | 如果 Plan 不是"拒绝所有"？ | "默认拒绝所有" | 实际为 `ask` 模式 | **安全工程的简化**——真正的安全需要验证 |
| 3 | 如果 Subagent 不全是只读？ | "Subagent 默认不能编辑文件" | @general 可写 | **事实错误**，不是分类问题 |
| 4 | 如果 `opencode.yml` 不存在？ | 引用 `opencode.yml` | 实际为 `opencode.json` | **虚构的架构**——不在能力圈内 |
| 5 | 如果马书第 4 章是错的？ | "马书第 4 章" | 实际为第 3 章 | **粗心的引用**——暗示整体引用质量存疑 |

**Lollapalooza 效应检测**:

| 偏误 | 表现 |
|------|------|
| 分类谬误 | "7 种 Agent 类型"混合不同类型层次 |
| 过度承诺 | "拒绝所有"暗示绝对安全 |
| 确认偏误 | @scout 仅在本文件出现，未跨源验证 |
| 近期偏误 | v1.15.x vs v1.16.x 版本混用 |
| 被剥夺超级反应 | "必须掌握"制造紧迫感 |

**能力圈审计结果**:

| 做得好 | 做得不好 |
|--------|---------|
| Agent = Model + Tools + Skills + Memory 公式 ✅ | "7 种"分类谬误 ❌ |
| Plan/Build 模式区分 ✅ | Plan mode `ask` vs `deny` ❌ |
| OMO 5 核心 Agent ✅ | @general 写权限 ❌ |
| Ultrawork/Prometheus 模式 ✅ | `opencode.yml` 不存在 ❌ |

**一句评价**: "The article is conceptually sound but factually unreliable. Like many AI-era technical documents, it captures the right concepts but gets the wrong details."

---

### TechLead 视角：生产环境验证

**核心判断**: **❌ 未达到生产就绪状态**，存在 3 个生产阻断级错误。

**生产就绪检查清单**:

| 类别 | 状态 | 备注 |
|------|------|------|
| **Agent 类型** | ⚠️ 需修复 | "7 种"→"8 个实例，2 种类型" |
| **权限模型** | ❌ 错误 | Plan=`ask` 非 `deny`，@general 可写 |
| **配置文件** | ❌ 错误 | `opencode.yml` 和 `.opencode/config.jsonc` 不存在 |
| **版本号** | ⚠️ 不一致 | v1.15.x → v1.16.x |
| **OMO Agent** | ✅ 已验证 | Sisyphus/Prometheus/Atlas/Hephaestus/Oracle |
| **Agent Loop** | ✅ 已验证 | "马书"存在，第 3 章 |
| **安全模型** | ⚠️ 误导 | "拒绝所有"→"ask 模式" |
| **Hidden Agents** | ✅ 已验证 | compaction/title/summary 存在 |

**生产阻断级问题详情**:

1. **Plan 模式权限**（Line 183）: `deny` → `ask`，用户预期自动拒绝却收到确认提示
2. **@general 写权限**（Line 206）: 声称只读，实际 @general 具有完整工具访问权限
3. **配置文件路径**（Lines 566, 672）: `opencode.yml` 和 `.opencode/config.jsonc` 均不存在

**推荐修复顺序**:
1. 修复生产阻断级问题（Plan 模式、@general 权限、配置路径）
2. 修复版本号不一致（v1.15.x → v1.16.x）
3. 修复次级问题（Agent 数量、compaction 阈值、@scout 有效性）
4. 更新相关文件（`why-opencode.md`）
5. 运行 `mdbook build` 验证

---

## 问题与建议

### 问题优先级矩阵

| 优先级 | 问题 | 涉及视角 | 影响范围 |
|--------|------|---------|---------|
| **🔴 P0** | Plan 模式权限：`deny` → `ask` | Karpathy、Munger、TechLead | 安全文档错误，用户预期偏差 |
| **🔴 P0** | @general Subagent 写权限错误 | Karpathy、Munger、TechLead | 权限模型根本性错误 |
| **🔴 P0** | 配置文件路径错误（`opencode.yml`/`config.jsonc`） | Karpathy、Munger、TechLead | 用户操作立即出错 |
| **🟡 P1** | Agent 数量误分类（"7 种"→"2 种类型，8 个实例"） | Karpathy、Munger、TechLead | 基础概念错误 |
| **🟡 P1** | 版本号不一致（v1.15.x vs v1.16.x） | Karpathy、TechLead | 造成版本困惑 |
| **🟡 P1** | "马书"章节引用错误（第 4 章→第 3 章） | Karpathy、Munger | 引用准确性 |
| **🟡 P1** | Compaction 阈值无官方依据 | Karpathy、Munger | 数据准确性 |
| **🟢 P2** | @scout Agent 需验证 | Karpathy、Munger、TechLead | 内容完整性 |
| **🟢 P2** | Trust Boundary 图需更新 @general 权限 | Karpathy、TechLead | 图表准确性 |
| **🟢 P2** | Shell 类比确定性幻觉（Munger 发现） | Munger | 教学类比局限 |
| **🟢 P2** | Lollapalooza 偏误叠加需警惕 | Munger | 读者认知防护 |

### 各视角独特建议

**Karpathy 视角特有建议**:
- 提供逐行修复方案（Lines 12, 183, 206, 288, 566, 672, 674, 776）
- compaction 行为应改为定性描述而非具体百分比

**Munger 视角特有建议**:
- 读者应警惕"必须掌握"等制造紧迫感的表述
- 文章最好用作"概念框架目录"而非"技术事实来源"

**TechLead 视角特有建议**:
- 需同时修复 `why-opencode.md` Line 238 的相同配置路径错误
- STRIDE 严重性修正建议

### 需修改的文件清单

**主要文件**: `src/02-core-concepts/agent-orchestration.md`
- Line 12: Agent 数量修正
- Line 183: Plan 模式权限修正
- Lines 206-210: @general 写权限修正
- Lines 288-293: compaction 阈值修正
- Lines 336-341: Trust Boundary 图更新
- Lines 511-515: 权限隔离图更新
- Line 566: `opencode.yml` → `opencode.json`
- Line 568: 保留 v1.16.x/v4.13.x
- Line 672: `.opencode/oh-my-openagent.jsonc`
- Line 674: v1.15.x → v1.16.x
- Line 776: "马书第 4 章" → "马书第 3 章"

**关联文件**: `src/01-introduction/why-opencode.md` Line 238

---

## 综合评分

| 维度 | 评分 | 说明 |
|------|------|------|
| **概念框架** | ★★★★☆ | Agent 编排的核心概念准确，OMO 体系描述正确 |
| **技术准确性** | ★★☆☆☆ | 3 个关键事实错误，多个中等问题 |
| **生产就绪度** | ★★☆☆☆ | 3 个生产阻断级问题，❌ 未就绪 |
| **安全性描述** | ★★☆☆☆ | 权限模型根本性错误，安全承诺与实际不符 |
| **可操作性** | ★★★☆☆ | 配置示例具体但指向不存在的文件 |
| **偏误控制** | ★★★☆☆ | 存在分类谬误和过度承诺倾向 |

**综合评定**: 文章的概念设计层面评价较高，但技术事实准确性评价极低。三个视角一致认为：**必须修复 3 个 P0 级事实错误后才能达到发布标准**。

---

*合并自：Karpathy 技术审查、Munger 思维审计、TechLead 生产验证（2026-06-06）*


---

## 修复计划与检查清单

| 优先级 | 说明 |
|--------|------|
| P0 | 附录B断链/US-QA-02 CI/品牌名/代码块path — 详见 reader-needs-deep-analysis §8.2 |
| P1 | D3角色声明/AE/SYSA/FRONTEND/UX — 详见 reader-needs-deep-analysis §8.3 |
| P2 | MOD-009暂缓/角色专属内容v1.1 |

**检查清单**：
- [ ] P0: 见顶层修复计划 reader-needs-deep-analysis §8.2
- [ ] P1: 见顶层修复计划 reader-needs-deep-analysis §8.3
- [ ] ✅ 最终验证: `mdbook build` 0 错误

