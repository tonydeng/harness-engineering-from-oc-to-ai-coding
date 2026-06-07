# Ch3 环境搭建 — 5 轮质量 Review 综合报告

**审查日期**: 2026-06-06
**审查范围**: `src/03-setup/` 全部 5 篇文章 + README
**审查方法**: 5 轮独立审查 + 综合修复

---

## 审查轮次概述

| 轮次 | 视角 | 关注点 | 发现问题数 |
|------|------|--------|-----------|
| 1 | 数据准确性 | 安装命令、配置示例、API Key 格式、国产模型定价 | 8 |
| 2 | Karpathy 工程现实主义 | 安装步骤在当前版本的可执行性 | 6 |
| 3 | Munger 逆向思维 | 环境搭建常见坑、自相矛盾的配置 | 5 |
| 4 | 内容一致性 | 链接格式、代码块格式、路径引用 | 4 |
| 5 | 内容研究写作 | 国产模型供应商配置信息时效性 | 7 |

---

## 按文章汇总的发现

### Article 3.1: quickstart.md (686 行)

| # | 问题 | 严重度 | 来源轮次 | 状态 |
|---|------|--------|---------|------|
| Q1 | Docker 安装方式 `ghcr.io/anomalyco/opencode` 存在证据冲突 | 🔴 | R1/R2 | 待验证 |
| Q2 | Copilot 模型名称（`gpt-5.3-codex`、`claude-sonnet-4.6`）与官方推荐列表有差异 | 🟡 | R2 | 已加说明 |
| Q3 | `#provider-配置` 锚点链接在 mdBook 中可能不生效 | 🟡 | R4 | 已修复 |

### Article 3.2: opencode-config.md (1176 行)

| # | 问题 | 严重度 | 来源轮次 | 状态 |
|---|------|--------|---------|------|
| C1 | `categories` 不是 OpenCode 原生配置键（属于 OMO 扩展），文章未清晰标注 | 🔴 | R2/R3 | 已加标注 |
| C2 | Compaction 配置两处自相矛盾（`auto/prune/tail_turns` vs `enabled/threshold/strategy`） | 🔴 | R3 | 需修复 |
| C3 | `compaction.prune` 默认值写错（`true` → 实际 `false`） | 🟡 | R2 | 已修复 |
| C4 | 默认权限模型描述误导：暗示默认 `ask`，实际默认 `allow` | 🔴 | R2/R3 | 已加说明 |
| C5 | 配置优先级图谱缺少 `.opencode` 子目录层 | 🟡 | R2 | 已加说明 |

### Article 3.3: oh-my-openagent-setup.md (726 行)

| # | 问题 | 严重度 | 来源轮次 | 状态 |
|---|------|--------|---------|------|
| O1 | GitHub Stars/Forks 数据已更新到 61K+ / 4.9K+ | 🟡 | R1/R2 | ✅ 已修复 |
| O2 | 版本号信息改为动态链接 | 🟡 | R2 | ✅ 已修复 |
| O3 | `Sisyphus-Junior` 在 Agent 列表中但架构图未包含 | 🟡 | R4 | 已添加 |

### Article 3.4: chinese-providers.md (709 行)

| # | 问题 | 严重度 | 来源轮次 | 状态 |
|---|------|--------|---------|------|
| P1 | 配置文件路径 `.opencode/config.json` 错误（5 处），应为 `opencode.json` | 🔴 | R1/R4 | **本次修复** |
| P2 | `examples/opencode-configs/multi-provider-hybrid.json` 文件不存在 | 🔴 | R4 | **本次修复** |
| P3 | 混合路由示例仍使用 Legacy 模型 ID（`deepseek-chat`、`deepseek-reasoner`），2026-07-24 退役 | 🔴 | R1/R5 | **本次修复** |
| P4 | DeepSeek reasoning_effort 参数值域不准确（`low`/`medium` 映射到 `high`） | 🟡 | R2 | 已修复 |
| P5 | Kimi 国际端点 `api.moonshot.ai/v1` 已补充 | 🟡 | R2 | ✅ 已修复 |

### Article 3.5: multi-env-setup.md (444 行)

| # | 问题 | 严重度 | 来源轮次 | 状态 |
|---|------|--------|---------|------|
| M1 | Agent 配置示例中 model ID `claude-sonnet-4-6`、`claude-opus-4-7` 需验证 | 🟡 | R2 | 保留待验证 |
| M2 | `$extends` Profile 继承系统已在早期修正中移除（改用 Agent 配置方案） | ✅ | R2 | ✅ 已修正 |
| M3 | CI 配置示例已修正（`--permission` → `OPENCODE_PERMISSION`） | ✅ | R2 | ✅ 已修正 |

---

## 本次修复的具体变更

### 变更 1: chinese-providers.md — 修复配置文件路径（P1）

**问题**: 5 处使用 `.opencode/config.json` 作为配置文件路径和代码块标签。
**修复**: 
- 第 101 行 Mermaid 图: `.opencode/config.json` → `opencode.json`
- 第 159 行文本: `.opencode/config.json` → `opencode.json`
- 第 161、243、344 行代码块标签: `.opencode/config.json` → `opencode.json`

### 变更 2: chinese-providers.md — 修复混合路由示例（P2/P3）

**问题**: 
1. 引用的 `examples/opencode-configs/multi-provider-hybrid.json` 文件不存在
2. 示例中使用 Legacy 模型 ID

**修复**: 
- 移除外部文件引用，改为内联配置示例
- 将 `deepseek-chat`/`deepseek-reasoner` 替换为 `deepseek-v4-flash`/`deepseek-v4-pro`
- 更新 `kimi-k2.5` → `kimi-k2.6`

### 变更 3: quickstart.md — 修复锚点链接（Q3）

**问题**: `opencode-config.md#provider-配置` 的中文锚点在 mdBook 中可能不正确渲染。
**修复**: 移除锚点，改为直接链接到文件。

### 变更 4: opencode-config.md — 修复 Compaction 自相矛盾（C2）

**问题**: 成本管控章节使用了不存在的 `enabled`/`threshold`/`strategy` 字段。
**修复**: 移除虚构的 compaction 配置示例，改为引用文章前部的正确配置段。

### 变更 5: opencode-config.md — 澄清默认权限行为（C4）

**问题**: 暗示 OpenCode 默认 `ask` 权限，实际默认是 `allow`。
**修复**: 添加明确说明 OpenCode 默认允许所有操作，`ask` 是推荐的安全配置。

---

## 跨文章的系统性问题

### 1. OMO 扩展配置 vs OpenCode 原生配置的边界

**问题**: `opencode-config.md` 的类别路由章节和成本管控章节将 OMO 扩展配置（`categories`、`fallbackChain`）混入 OpenCode 原生配置描述中，未明确标注来源。

**当前状态**: 类别路由章节开头已加说明（第 611 行），但成本管控示例中仍有残留。

**建议**: 在成本管控章节的示例中明确标注"此配置需要 oh-my-openagent"。

### 2. 模型 ID 时效性

**问题**: 所有文章中使用的模型 ID（如 `claude-sonnet-4-5`、`claude-opus-4-7`、`gpt-5.3-codex`）可能随模型更新而变化。

**建议**: 在关键配置示例旁添加注释"具体模型 ID 请以 `/models` 命令输出为准"。

### 3. 国产模型退役时间窗口

**问题**: DeepSeek Legacy 模型（`deepseek-chat`、`deepseek-reasoner`）将于 2026-07-24 退役，距离本书发布时间仅约 7 周。

**建议**: 在所有使用 Legacy ID 的示例中添加退役警告，并优先展示 V4 模型配置。

---

## 验证清单

| 检查项 | 状态 |
|--------|------|
| 所有内部 .md 链接格式正确 | ✅ |
| 代码块标签路径与实际文件一致 | ✅（本次修复 P1/P2） |
| SUMMARY.md 中 Ch3 所有文件存在 | ✅ |
| Mermaid 图表配色符合规范 | ✅ |
| 品牌名 OpenCode（大写 C）统一 | ✅ |
| 英文术语首次出现格式 | ✅ |
| mdbook build 通过 | 待验证 |

---

## 附录：已修复的历史问题

以下问题在之前的单篇审查中已被发现并修复：

1. ✅ quickstart.md: 安全配置路径 `.opencode/config.json` → `opencode.json`
2. ✅ quickstart.md: Homebrew tap 预处理简化
3. ✅ quickstart.md: 版本号 `v1.15.x` → `v1.16.x`
4. ✅ opencode-config.md: MCP filesystem 命令修正
5. ✅ oh-my-openagent-setup.md: Stars/Forks 数据更新
6. ✅ multi-env-setup.md: `$extends` Profile 系统移除
7. ✅ multi-env-setup.md: `${VAR}` → `{env:VAR}` 语法修正
8. ✅ chinese-providers.md: DeepSeek V4 模型信息更新
9. ✅ chinese-providers.md: Kimi K2.6 旗舰模型添加
10. ✅ chinese-providers.md: Qwen 国际定价修正

---

**审查人**: Sisyphus-Junior（综合 5 轮审查结果）
**审查日期**: 2026-06-06
**适用版本**: OpenCode v1.16.x + oh-my-openagent v4.5.x
