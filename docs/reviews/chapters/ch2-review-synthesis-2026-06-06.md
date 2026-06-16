# Ch2 核心概念 — 5 轮质量 Review 综合报告

> **日期**：2026-06-06
> **审查范围**：`src/02-core-concepts/` 下 6 篇文章
> **审查方法**：5 轮独立审查 + 交叉验证
> **参考基线**：`docs/planning/specs/ch02-core-concepts.md`、`docs/reference/` 4 篇参考文档、`AGENTS.md` 品牌规范

---

## 一、审查总览

| 轮次 | 视角 | 发现问题数 | 严重/中等/轻微 |
|------|------|-----------|---------------|
| R1 | 数据准确性 | 14 | 5/6/3 |
| R2 | Karpathy 视角（技术可靠性） | 7 | 2/3/2 |
| R3 | Munger 视角（概念混淆/学习障碍） | 8 | 3/3/2 |
| R4 | 内容一致性（Mermaid/交叉引用） | 12 | 0/5/7 |
| R5 | 内容研究写作（对比开源/官网） | 6 | 2/2/2 |
| **合计** | | **47** | **12/19/16** |

**总体评价**：Ch2 六篇文章的概念框架完整，OS 类比和 Mermaid 图表质量较高。主要问题集中在三方面：(1) OMO 扩展与 OpenCode 原生功能的标注不一致；(2) 部分技术细节自相矛盾；(3) validation-harness.md 内容显著不足。

---

## 二、R1 — 数据准确性审查

### 严重问题（5）

| # | 文件 | 行号 | 问题 | 修复方案 |
|---|------|------|------|---------|
| R1-01 | agent-orchestration.md | 12 | "3 个后台系统进程（compaction/title/**summary**）"——wiki 和源码中均无 "summary" hidden agent 记录 | 删除 "summary"，改为 "2 个后台系统进程（compaction/title）" |
| R1-02 | agent-orchestration.md | 212 | @general 描述为"处理**不需要文件编辑**的通用任务"，但同文 trust boundary 表（L362）和 L206 均标注 @general **可编辑文件** | 修改为"处理通用任务（可编辑文件）" |
| R1-03 | agent-orchestration.md | 573 | "OMO 提供了多个专业 Agent（核心 5 个）"——wiki 实际记录 **11 个** Agent（含 Metis/Momus/Librarian/Explore/Multimodal Looker/Sisyphus-Junior） | 更新为 11 个，补充缺失 Agent 说明 |
| R1-04 | constraints-system.md | 714 | STRIDE 威胁表格式损坏——表头和前两行（Spoofing/Tampering）缺失，只剩后 4 行 | 补全完整 STRIDE 表 |
| R1-05 | validation-harness.md | 全文 | 仅 363 行，远低于 spec 的 200 行有效内容要求（扣除 frontmatter 和空行后不足）；缺少 YOLO 分类器完整说明、质量门禁分级、威胁建模 | 大幅扩展内容 |

### 中等问题（6）

| # | 文件 | 问题 | 修复方案 |
|---|------|------|---------|
| R1-06 | agent-orchestration.md L622-687 | 类别路由系统未标注为 **OMO 扩展**（非 OpenCode 原生），与 spec 要求冲突 | 添加 OMO 扩展标注 |
| R1-07 | skills-system.md L336-362 | "六路搜索路径"中包含 `.claude/skills/` 和 `.agents/skills/` 路径，这些是 **OMO 兼容层扩展**，非 OpenCode 原生 | 标注 OMO 扩展路径 |
| R1-08 | workflow-patterns.md L48 | "5 个核心内置命令"不完整——实际有 10+ 内置命令（/new, /sessions, /compact, /export, /connect, /models, /themes, /editor, /details, /thinking） | 扩展内置命令列表 |
| R1-09 | context-engineering-core.md | 多处配置引用 "OpenCode >= v1.16.x, OMO >= v4.7.x"，与 PRD 基线（v1.15.x / v4.5.x）不一致 | 统一版本号或标注为"规划中" |
| R1-10 | context-engineering-core.md | `tokenBudget.overrunHandling.modelDowngrade` 等配置字段无法验证为真实 OpenCode 配置 | 标注为 OMO 扩展或架构建议 |
| R1-11 | validation-harness.md | 缺少 YOLO 分类器详细说明（spec 明确要求），仅简略提及 "YOLO mode 是布尔开关" | 补充 YOLO 分类机制说明 |

### 轻微问题（3）

| # | 文件 | 问题 |
|---|------|------|
| R1-12 | agent-orchestration.md | 类别路由配置示例中的模型名（claude-opus-4）与 wiki 中的模型名（Claude Opus 4.7）不一致 |
| R1-13 | skills-system.md | Skills Marketplace 的"社区替代方案"描述模糊，读者可能误以为是官方功能 |
| R1-14 | workflow-patterns.md | Profile 系统的 `$extends` 继承机制虽已标注 OMO，但配置 JSON 示例是虚构结构 |

---

## 三、R2 — Karpathy 视角审查（技术可靠性）

### 核心判断框架

以 Karpathy 的"构建即理解"和"锯齿状智能"原则审视：

| # | 文件 | 问题 | 严重度 |
|---|------|------|--------|
| R2-01 | workflow-patterns.md | Profile 配置 JSON（L239-339）字段结构（`"profile"`, `"agent": {"default_mode"}`, `"behavior"`）**无法验证为真实 OpenCode 配置**。读者照抄会失败。这违反了"构建即理解"原则——给出的示例必须可运行。 | 严重 |
| R2-02 | context-engineering-core.md | `compaction.rules`、`caching.crossSession`、`tokenBudget.allocation` 等配置字段看起来像是真实的 opencode.json 配置，但实际可能是 OMO 扩展或虚构的。**未标注来源**。 | 严重 |
| R2-03 | agent-orchestration.md | "实践洞察：锯齿状智能与验证心态"段落质量极高，准确传达了 AI 能力不均匀的核心洞察。 | ✅ 优秀 |
| R2-04 | skills-system.md | "描述匹配"的设计权衡分析（优势 vs 挑战）体现了工程现实主义。 | ✅ 优秀 |
| R2-05 | context-engineering-core.md | "缓存优先，压缩兜底"的策略排序是正确的工程直觉，但缺少实际验证数据。 | 中等 |
| R2-06 | constraints-system.md | "反面案例"部分（L833-1018）的教学价值极高，两个事故案例的时间线、根因分析、修复方案都很扎实。 | ✅ 优秀 |
| R2-07 | validation-harness.md | 文章对"YOLO"的解释过于简略，没有给出具体的工程实践指导。"构建即理解"要求读者能通过文章构建出可用的验证系统，但目前做不到。 | 中等 |

### Karpathy 总结

> Ch2 文章的概念框架和 OS 类比做得好，但**配置示例的可验证性是最大隐患**。读者拿到一本书，第一件事就是复制配置跑一下——如果跑不通，信任就崩了。建议：所有配置示例标注"已在 OpenCode vX.X 验证"或"OMO 扩展配置，需安装 oh-my-openagent"。

---

## 四、R3 — Munger 视角审查（概念混淆/学习障碍）

### 概念混淆风险矩阵

| # | 混淆点 | 涉及文件 | 严重度 | 说明 |
|---|--------|---------|--------|------|
| R3-01 | @general 权限自相矛盾 | agent-orchestration.md | 严重 | "不需要文件编辑" vs "可编辑文件"——读者会彻底困惑 |
| R3-02 | OMO 扩展 vs 原生功能 边界模糊 | 全章 6 篇 | 严重 | 类别路由、Profile 系统、六路搜索路径等未统一标注 OMO 来源，读者无法区分"OpenCode 能做什么"和"OMO 额外提供的" |
| R3-03 | "YOLO" 术语混乱 | validation-harness.md | 严重 | Spec 称"YOLO 分类器"，文章称"YOLO mode 是布尔开关"，实际上 OpenCode 的 YOLO 是自动批准所有操作的模式，而非风险分类。Spec 描述的三级分类是架构建议，不是 YOLO 本身。 |
| R3-04 | 权限键名不一致 | skills-system.md + constraints-system.md | 中等 | skills-system 用 `permission.skill`，constraints-system 用 `permission.read/edit/bash`——键名体系不统一 |
| R3-05 | "三种权限动作" vs "三级策略" | constraints-system.md | 中等 | 同一概念用了两个不同名称（"三种权限动作"和"三级策略"），增加认知负荷 |
| R3-06 | Hidden Agent 数量 | agent-orchestration.md | 中等 | 文中说 3 个但只描述了 2 个（compaction 和 title），"summary" 不存在 |
| R3-07 | Skill 搜索路径 6 路 vs 3 级 | skills-system.md | 轻微 | 标题写"六路搜索路径"但 spec 和概述都说"三级"——六路是三级在三个兼容生态中的展开 |
| R3-08 | 上下文工程三层模型命名 | context-engineering-core.md | 轻微 | "压缩/缓存/预算"——spec 用"压缩、缓存、预算"，文章一致，✅ |

### Munger 总结

> 最大的认知陷阱是**OMO 扩展冒充原生功能**。一个刚接触 OpenCode 的读者读完 Ch2 后，会以为类别路由、Profile 切换、六路搜索路径都是 OpenCode 自带的——然后安装 OpenCode 发现这些都不存在。这是"知识负债"的典型案例。建议：每篇涉及 OMO 功能的段落开头加 `> ⚠️ OMO 扩展：以下功能需要安装 oh-my-openagent` 的统一格式。

---

## 五、R4 — 内容一致性审查

### Mermaid 图表审查

#### 颜色规范合规性（标准：Agent=#4A90D9, Skill=#50C878, Workflow=#FF9F43, MCP=#A66CFF）

| 文件 | 图表数 | 合规 | 不合规 | 问题 |
|------|--------|------|--------|------|
| agent-orchestration.md | 9 | 8 | 1 | MCP 节点用 `#E8F4FD` 背景色而非 `#A66CFF`（L126 MCP 扩展层 subgraph） |
| skills-system.md | 5 | 4 | 1 | 攻击面图中 `#E74C3C` 用于风险节点——非品牌色但语义合理（红色=危险），保留 |
| workflow-patterns.md | 3 | 3 | 0 | ✅ 全部合规 |
| context-engineering-core.md | 7 | 6 | 1 | Token 预算图中 R(预留) 用 `#A66CFF`——非 MCP 概念但颜色复用，可接受 |
| constraints-system.md | 12 | 9 | 3 | 多处使用 `#ff6b6b` 而非标准红色——应统一为 `#E74C3C` |
| validation-harness.md | 2 | 2 | 0 | ✅ 合规 |

#### 方向规范合规性（标准要求 TB = top-bottom）

| 文件 | 不合规图表 | 当前方向 | 建议 |
|------|-----------|---------|------|
| skills-system.md L73 | Skill vs Prompt 对比图 | LR | 保留 LR（对比图适合横向） |
| skills-system.md L145 | 组件组合对比图 | LR | 保留 LR（对比图适合横向） |
| skills-system.md L393 | 渐进式披露时序图 | sequenceDiagram | 时序图无方向要求 |
| constraints-system.md L189 | 权限动作谱系 | LR | 保留 LR（线性谱系适合横向） |

**结论**：LR 方向均用于合理的对比/谱系场景，不强制改为 TB。

### 交叉引用审查

| 文件 | 引用 | 状态 |
|------|------|------|
| agent-orchestration.md → skills-system.md | ✅ 有效 |
| agent-orchestration.md → workflow-patterns.md | ✅ 有效 |
| agent-orchestration.md → ../01-introduction/ | ✅ 有效 |
| agent-orchestration.md → ../04-workflows/ | ✅ 有效 |
| skills-system.md → ../05-skills/ | ✅ 有效 |
| skills-system.md → ../06-advanced/security-overview.md | ✅ 有效 |
| workflow-patterns.md → ../03-setup/ | ✅ 有效 |
| context-engineering-core.md → ../06-advanced/context-compression.md | ✅ 有效 |
| constraints-system.md → ../06-advanced/sandbox-hooks.md | ✅ 有效 |
| validation-harness.md → ../03-setup/ | ✅ 有效 |
| validation-harness.md → ../05-skills/ | ✅ 有效 |
| validation-harness.md → ../07-case-studies/ | ✅ 有效 |

**所有交叉引用有效**，无 404 风险。

---

## 六、R5 — 内容研究写作审查

### 与开源生态对比

| # | 发现 | 涉及文件 | 严重度 | 说明 |
|---|------|---------|--------|------|
| R5-01 | OpenCode 官方已更新到 v1.15.x，但文章中部分配置示例的字段名（如 `tokenBudget`、`compaction.rules`）无法在官方文档中找到 | context-engineering-core.md | 严重 | 需标注为 OMO 扩展或验证后修正 |
| R5-02 | OpenCode 的 `permission` 配置键名实际使用 `edit`/`bash`/`webfetch` 等工具名，而非 `read`/`write`/`execute` | constraints-system.md, skills-system.md | 中等 | 文章已正确使用 `read`/`edit`/`bash`，但 `read` 是否实际存在需确认 |
| R5-03 | Claude Code 的 `CLAUDE.md` 在书中多次提及作为兼容目标，但 Ch2 未说明 AGENTS.md 与 CLAUDE.md 的关系 | workflow-patterns.md | 中等 | 建议补充简要说明 |
| R5-04 | MCP 协议在 2026 年已有 WebSocket 传输支持，但 context-engineering-core.md 仅提及 stdio | context-engineering-core.md | 轻微 | 可在 MCP 工具输出段落补充 |
| R5-05 | Skills Marketplace 的实际状态：目前通过 npm 包和 Git 仓库分发，无官方统一注册表 | skills-system.md | 严重 | 文章已部分说明，但需更明确标注"非官方" |
| R5-06 | 类别路由的 8 个 category（visual-engineering, ultrabrain, deep, artistry, quick, unspecified-low, unspecified-high, writing）是 OMO 特有，非 OpenCode 原生 | agent-orchestration.md | 严重 | 需明确标注 |

### 内容更新建议

1. **agent-orchestration.md**: 补充 OMO 11 Agent 的完整列表（含 Metis/Momus/Librarian/Explore/Multimodal Looker/Sisyphus-Junior）
2. **workflow-patterns.md**: 添加 Ralph Loop (/ulw-loop) 说明段落（spec 明确要求）
3. **validation-harness.md**: 添加质量门禁分级体系、YOLO 分类机制（与 spec 对齐）、STRIDE 威胁建模

---

## 七、修复优先级排序

### P0 — 必须立即修复（数据准确性/自相矛盾）

1. **R1-01**: agent-orchestration.md — 删除 "summary" hidden agent
2. **R1-02**: agent-orchestration.md — 修复 @general 权限矛盾
3. **R1-04**: constraints-system.md — 修复 STRIDE 表格式
4. **R1-05**: validation-harness.md — 大幅扩展内容
5. **R3-01**: 同 R1-02
6. **R3-02**: 全章 OMO 标注统一化

### P1 — 重要修复（概念清晰度）

7. **R1-03**: agent-orchestration.md — 补充 OMO 完整 Agent 列表
8. **R1-06**: agent-orchestration.md — 类别路由 OMO 标注
9. **R1-07**: skills-system.md — 搜索路径 OMO 标注
10. **R1-08**: workflow-patterns.md — 扩展内置命令列表
11. **R1-09/R1-10**: context-engineering-core.md — 版本号和配置标注
12. **R3-03**: validation-harness.md — YOLO 术语澄清

### P2 — 改进项（一致性/质量）

13. **R4**: constraints-system.md — `#ff6b6b` 统一为 `#E74C3C`
14. **R5-03**: workflow-patterns.md — 补充 AGENTS.md 与 CLAUDE.md 关系
15. **R5-06**: agent-orchestration.md — 类别路由 OMO 标注

---

## 八、执行记录

### 已完成的修复

| # | 文件 | 修复内容 |
|---|------|---------|
| 1 | agent-orchestration.md | 修复 @general 描述矛盾、删除 summary hidden agent、添加 OMO 标注、补充完整 Agent 列表 |
| 2 | skills-system.md | 标注搜索路径 OMO 扩展、强化 Marketplace 非官方标注 |
| 3 | workflow-patterns.md | 扩展内置命令列表、标注 Ultrawork/Prometheus 为 OMO、添加 Ralph Loop 段落、补充 AGENTS.md 与 CLAUDE.md 关系 |
| 4 | context-engineering-core.md | 统一版本号、标注配置字段来源 |
| 5 | constraints-system.md | 修复 STRIDE 表、统一颜色代码 |
| 6 | validation-harness.md | 扩展 YOLO 分类器、质量门禁、威胁建模内容 |

---

> **审查者**：5 轮综合审查（数据准确性 + Karpathy + Munger + 一致性 + 内容研究）
> **版本**：v1.0 | 2026-06-06
