# 综合评审：opencode-config.md

> 评审日期：2026-06-06
> 评审文件：`src/03-setup/opencode-config.md`
> 来源文件：data-research.md, karpathy-review.md, munger-review.md, techlead-review.md

---

## 评审概述

本文对 `src/03-setup/opencode-config.md` 进行了跨视角综合评审，涵盖数据研究（事实核查）、Karpathy 工程现实主义审查、Munger 逆向思维审查和 TechLead 工程视角审查。主要发现：文章存在多个严重事实错误，其中成本管控章节的 compaction 配置字段完全虚构，`categories`/`fallbackChain` 属于 oh-my-openagent 扩展功能但被表述为 OpenCode 原生特性，且项目配置文件路径、权限工具列表、默认权限描述均有错误。

**总体评分：3/10（技术准确性），建议实质性修订后重新评审。**

---

## 各视角发现汇总

### 数据研究报告发现

基于 OpenCode 官方文档、GitHub 源码和 oh-my-openagent 源码的 12 项事实核查：

| 编号 | 验证项 | 结论 | 严重程度 |
|------|--------|------|---------|
| a | `$schema` URL | ✅ 已验证 | — |
| b | 默认端口 4096 | ✅ 已验证 | — |
| c | Config key 名称 (agent/command/mcp) | ✅ 已验证 | — |
| d | Permission tool 列表 | ⚠️ 遗漏 `codesearch`、`todoread` | 低 |
| e | 8 个内置类别 + 变体名 | ⚠️ 属于 oh-my-openagent | 中 |
| f | Config 合并行为 | ✅ 已验证 | — |
| g1 | Compaction config keys 主段 | ✅ 基本正确 | — |
| g2 | Compaction config keys 成本段 | ❌ 全部错误（enabled/threshold/strategy） | **高** |
| h | disabled_providers/enabled_providers | ✅ 已验证 | — |
| i | fallbackChain | ⚠️ 属于 oh-my-openagent | 中 |
| j | categories 是否为顶级 key | ⚠️ 属于 oh-my-openagent | 中 |
| k | enterpriseUrl | ✅ 已验证 | — |
| l | setCacheKey | ✅ 已验证 | — |

**额外发现**：
- `headerTimeout` 是有效的 provider option ✅
- compaction `prune` 默认值文章写 `true`，官方为 `false` ⚠️
- `tail_turns` 和 `preserve_recent_tokens` 是 2026 年 4-5 月新增特性

### Karpathy 工程现实主义审查发现

15 项问题，分三类：

**🔴 确认的事实错误（7 个）**：
1. 权限工具表包含不存在的 key：`repo_clone`、`repo_overview`
2. 项目配置文件路径错误（`.opencode/config.json` → 应为 `opencode.json`）
3. 默认权限模型描述有根本性偏差（把收紧配置伪造成默认行为）
4. `compaction.prune` 默认值写反（`true` → 实际 `false`）
5. 成本管控章节的 `categories` 配置不存在于 OpenCode Schema
6. 成本管控章节的 compaction 配置使用了完全不同的字段名（`enabled`/`threshold`/`strategy` → 实际 `auto`/`prune`/`reserved`）
7. MCP filesystem 命令示例不对（`mcp-filesystem` → `@modelcontextprotocol/server-filesystem`）

**🟡 很可能错误（3 个）**：
8. 类别路由系统（8 个内置类别）归属未标明为 oh-my-openagent
9. 内置 agent 类别变体值（`xhigh`、`max` 等）在官方文档无定义
10. 配置优先级图谱缺少 `.opencode` 目录层

**⚪ 遗漏/次要（5 个）**：
11. 未提及 `tui.json` 分离架构
12. 缺失顶层 `tools` 配置
13. 缺失 `{file:path}` 变量语法
14. `disabled_providers` 与 `enabled_providers` 优先级关系未说明
15. 模型 ID 格式需确认

### Munger 逆向思维审查发现

重点：**文档内部一致性问题**，识别出 3 个严重自相矛盾和 1 个系统性遗漏：

1. **Compaction 配置有两个互斥版本**：版本 A（第 397-407 行）使用 `auto`/`prune`/`tail_turns`，版本 B（第 1077-1085 行）使用 `enabled`/`threshold`/`strategy`，零个字段名重合。

2. **`categories` 配置块凭空出现**：文章自己的核心配置概览（第 92-109 行）列举了 15 个顶层键，不包括 `categories`，但成本管控章节（第 1006-1071 行）突然将其作为有效配置呈现。

3. **`fallbackChain` 与内置降级链的关系未定义**：内置降级链（`model` → `small_model` → 其他 Provider）与 `fallbackChain`（用户定义的有序列表）如何配合使用，文章未做任何说明。

4. **核心配置概览遗漏 42% 的顶层键**：自称展示"完整结构"（第 92-109 行），但遗漏了 `skills`、`reference`、`plugin`、`disabled_providers`、`enabled_providers`、`share`、`attachment`、`enterprise`、`tool_output`、`experimental` 共 10 个键。

**额外问题**：
- 类别路由表（8 类）与 Mermaid 图（6 类）数量不一致，遗漏 `unspecified-low` 和 `unspecified-high`
- `read` 工具在权限示例中使用但行为不明确

### TechLead 工程视角审查发现

**总体评分：75/100**，但**必须修正**。

**🔴 关键错误（5 个）**：
| 编号 | 错误 | 影响 |
|------|------|------|
| C1 | 项目配置路径 `.opencode/config.json` → 应为 `opencode.json` | 配置静默失效 |
| C2 | 不存在的权限工具 `repo_clone`、`repo_overview` | 权限配置静默忽略 |
| C3 | 成本管控使用不存在的 `categories`、`fallbackChain` | 配置完全静默失效 |
| C4 | 成本管控 compaction 字段名完全错误（`enabled`/`threshold`/`strategy`） | 配置静默失效 |
| C5 | compaction `prune` 默认值 `true` → 实际 `false` | Token 消耗超出预期 |

**🟡 中等问题（3 个）**：
| 编号 | 问题 | 说明 |
|------|------|------|
| M1 | 引言使用 `agents`（复数）和 `mcpServers` | 配置键为单数 |
| M2 | `experimental.policies` 资源格式有 `provider:` 前缀 | 应为纯 provider ID |
| M3 | 配置优先级图表 6 层，官方为 8 层 | 缺失 OPENCODE_CONFIG 和 .opencode 目录层 |

**⚪ 低优先级（2 个）**：
- L1: MCP filesystem 示例格式有误
- L2: 模型版本不一致（`claude-sonnet-4-5` vs `claude-sonnet-4-6`）

---

## 问题与建议

### 合并问题汇总表

| # | 问题 | 涉及视角 | 严重程度 | 建议修复 |
|---|------|---------|---------|---------|
| 1 | 项目配置路径错误（`.opencode/config.json`） | Karpathy, TechLead | **高** | 改为 `opencode.json` |
| 2 | 不存在的权限工具 `repo_clone`/`repo_overview` | Karpathy, TechLead | **高** | 从权限表删除 |
| 3 | cost 章节 compaction 字段完全错误（enabled/threshold/strategy） | 所有 4 个视角 | **高** | 改为 auto/prune/tail_turns/reserved |
| 4 | categories/fallbackChain 作为 OpenCode 原生功能呈现 | 所有 4 个视角 | **高** | 注明为 oh-my-openagent 功能 |
| 5 | 默认权限模型描述有偏差 | Karpathy, Munger(间接) | **高** | 改为"大部分操作默认允许" |
| 6 | compaction prune 默认值写反 | Data, Karpathy, TechLead | **中** | true → false |
| 7 | 核心配置概览遗漏 42% 顶层键 | Munger | **中** | 补充完整的键列表 |
| 8 | Compaction 配置两版本互斥 | Munger | **中** | 统一为正确版本 |
| 9 | 配置优先级图示 6 层 vs 官方 8 层 | Karpathy, TechLead | **中** | 补充缺失层 |
| 10 | 类别路由归属未标明 | 所有 4 个视角 | **中** | 明确标注为 oh-my-openagent |
| 11 | MCP filesystem 命令示例不对 | Karpathy, TechLead | **低** | 修正为正确包名 |
| 12 | 遗漏 tui.json 分离架构 | Karpathy | **低** | 补充说明 |
| 13 | 遗漏 {file:path} 变量语法 | Karpathy | **低** | 补充说明 |
| 14 | 文章引言混用复数 agents/mcpServers | TechLead | **低** | 统一为单数 |

### 系统性风险分析（Munger）

1. **展示实用技巧压倒配置准确性**：成本管控章节为展示立即可用的省钱策略，编造了不存在的配置键。
2. **简化压倒精确**：每次简化（配置参数重命名、类别图省略、概览省略）都是一次有意的失真。
3. **章节独立性压倒全文一致性**：不同章节由不同作者撰写，未做交叉校验。

### 静默失效风险

所有关键错误（C1-C4）的共同特征是：配置被加载器静默忽略，**没有任何错误提示**。读者按文章配置后，系统不报错、不告警、不生效。这比配置报错更危险——用户以为是系统不工作，其实是配置根本没被读取。

---

## 综合评分

| 维度 | 评分 | 说明 |
|------|------|------|
| 技术准确性 | 3/10 | 核心配置结构多处错误，成本管控章节字段完全虚构 |
| 内部一致性 | 2/10 | compaction 配置两版本零字段重合，概览遗漏 42% |
| 完整性 | 5/10 | 覆盖面广但遗漏重要特性（tui.json、tools、{file:}） |
| 可用性 | 4/10 | 复制配置会静默失效，对读者造成实际损害 |
| 架构合理性 | 7/10 | 概念框架合理（配置层级、合并行为等），但实现细节错误 |

**总体评价**：文章在概念层面（配置层级、合并行为、权限机制）的架构描述是合理的，但具体配置示例存在严重事实错误。成本管控章节和权限工具列表需要立即重写。最核心的问题是将 oh-my-openagent 的扩展功能（categories、fallbackChain、类别路由）混入 OpenCode 原生配置描述，且未做任何区分说明——这是系统性的归类错误，不是孤立的笔误。

**建议**：立即修复高优先级错误（#1-#6），再将类别路由和成本管控策略重新定位到 oh-my-openagent 配置文中，或明确标注扩展来源。


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

