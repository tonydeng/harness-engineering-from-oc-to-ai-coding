# 数据研究报告：src/03-setup/opencode-config.md 事实核查

> 研究日期：2026-06-06
> 数据来源：OpenCode 官方文档 (opencode.ai)、GitHub 源码 (anomalyco/opencode, sst/opencode)、开源书籍 (opencodebook.xyz, opencode.runman.ai/zh)、oh-my-openagent 项目源码
> 研究方法：网络搜索 + 官方文档抓取 + 源码阅读（config.ts, provider.ts, compaction.ts）

---

## 验证项总览

| 编号 | 待验证项 | 结论 | 严重程度 |
|------|---------|------|---------|
| a | `$schema` URL | ✅ 已验证 | — |
| b | 默认端口 4096 | ✅ 已验证 | — |
| c | Config key 名称 (agent/command/mcp) | ✅ 已验证 | — |
| d | Permission tool 列表 | ⚠️ 部分已废弃 | 低 |
| e | 8 个内置类别 + 变体名 | ⚠️ 属于 oh-my-openagent | 中 |
| f | Config 合并行为 | ✅ 已验证 | — |
| g | Compaction config keys | ❌ 主段正确，成本段错误 | 高 |
| h | disabled_providers / enabled_providers | ✅ 已验证 | — |
| i | fallbackChain 是否真实 | ⚠️ 属于 oh-my-openagent | 中 |
| j | categories 是否为顶级 key | ⚠️ 属于 oh-my-openagent | 中 |
| k | enterpriseUrl | ✅ 已验证 | — |
| l | setCacheKey | ✅ 已验证 | — |

---

## (a) $schema URL

**文章中使用的值**：`https://opencode.ai/config.json`

**实际值**：`https://opencode.ai/config.json`

**结论**：✅ **已确认，值正确**

**证据**：
- OpenCode 官方文档配置页中所有示例均使用 `"$schema": "https://opencode.ai/config.json"`（来源：https://opencode.ai/docs/config/）
- GitHub 源码中 remote config 加载也使用了此 URL：
  ```typescript
  if (!remoteConfig.$schema) remoteConfig.$schema = "https://opencode.ai/config.json"
  ```
  （来源：https://github.com/sst/opencode/blob/4086a9ae/packages/opencode/src/config/config.ts）

**注意**：根据 GitHub Issue #2151 (anomalyco/opencode)，此 URL 曾间歇性返回 404（JSON Schema 未托管），但这是托管问题，URL 本身是官方定义的。

---

## (b) 默认端口 4096

**文章中使用的值**：`"port": 4096`，标注"默认 4096"

**实际值**：4096

**结论**：✅ **已确认，值正确**

**证据**：
- OpenCode 官方 Server 文档：
  ```
  | `--port` | Port to listen on | `4096` |
  ```
  （来源：https://opencode.ai/docs/server/）
- 多个 GitHub Issue 将 4096 称为"default port"（来源：https://github.com/anomalyco/opencode/issues/10357）

---

## (c) Config key 名称：agent / command / mcp

**文章中使用的 key**：
- `"agent": {}`（第 99 行）— 单数
- `"command": {}`（第 100 行）— 单数
- `"mcp": {}`（第 101 行）— 单数

**实际值**：

| 文章 key | 源码中的 key | 是否匹配 |
|----------|-------------|---------|
| `agent` | `agent: z.object({...})` | ✅ 匹配 |
| `command` | `command: z.record(z.string(), ConfigCommand.Info)` | ✅ 匹配 |
| `mcp` | `mcp: z.record(z.string(), ...)` | ✅ 匹配 |

**结论**：✅ **已确认，三个 key 名称均正确**

**证据**：
- GitHub 源码 `packages/opencode/src/config/config.ts`：
  - `agent: z.object({ ... }).catchall(ConfigAgent.Info).optional()`（来源：https://github.com/anomalyco/opencode/blob/9afbdc10/packages/opencode/src/config/config.ts）
  - `command: z.record(z.string(), ConfigCommand.Info).optional()`
  - `mcp: z.record(z.string(), ...).optional()`
- 官方文档同样使用单数形式（来源：https://opencode.ai/docs/config/）

**注意**：子目录名称使用复数（`agents/`, `commands/`），但配置文件中的顶级 key 使用单数。

---

## (d) Permission tool 列表

**文章中列出的工具（第 826-844 行）**：
`read`, `edit`, `glob`, `grep`, `list`, `bash`, `task`, `external_directory`, `lsp`, `skill`, `todowrite`, `question`, `webfetch`, `websearch`, `doom_loop`

**实际工具列表**（来源：https://opencode.ai/docs/agents/）：

| 工具 | 文章中是否存在 | 官方是否认可 |
|------|--------------|------------|
| `read` | ✅ | ✅ |
| `edit` | ✅ | ✅（覆盖 write, patch, multiedit） |
| `glob` | ✅ | ✅ |
| `grep` | ✅ | ✅ |
| `list` | ✅ | ✅ |
| `bash` | ✅ | ✅ |
| `task` | ✅ | ✅ |
| `external_directory` | ✅ | ✅ |
| `lsp` | ✅ | ✅ |
| `skill` | ✅ | ✅ |
| `todowrite` | ✅ | ✅（官方文档还有 `todoread`） |
| `question` | ✅ | ✅ |
| `webfetch` | ✅ | ✅ |
| `websearch` | ✅ | ✅ |
| `doom_loop` | ✅ | ✅ |
| `codesearch` | ❌ 缺失 | ✅ 官方认可 |
| `todoread` | ❌ 缺失 | ✅ 官方认可 |

**结论**：⚠️ **基本完整，但有遗漏**

- 所有列出的 15 个工具都是真实的 ✅
- 官方文档中还有 `codesearch` 和 `todoread` 两个工具未被列出
- 官方文档将 `edit` 定义为覆盖 `write`, `patch`, `multiedit` 三个工具，文章未提及此细节
- 文章第 828 行为 `edit` 标注 "✅ glob 匹配" — 确认正确
- 文章第 842 行 `doom_loop` 标注 "简单动作" — 确认正确（它是触发式检测，非 glob 可配）
- 文章第 835 行 `external_directory` 标注 "✅ glob 匹配" — 确认正确

---

## (e) 8 个内置类别 + 变体名

**文章中使用的值**（第 622-633 行表格 + 第 657-663 行）：

| 类别 | 文章中的变体 |
|------|------------|
| visual-engineering | high |
| ultrabrain | xhigh |
| deep | medium |
| artistry | high |
| quick | —（无） |
| unspecified-low | —（无） |
| unspecified-high | max |
| writing | —（无） |

**结论**：⚠️ **类别系统本身属于 oh-my-openagent 项目，非 OpenCode 核心功能**

**详细分析**：

1. **OpenCode 核心（anomalyco/opencode）** 不包含 `categories` 顶级 key，也没有内置类别路由系统。其 config schema 中没有 `categories` 或 `fallbackChain` 定义。

2. **oh-my-openagent（code-yeongyu/oh-my-openagent）** 实现了完整的类别路由系统，源码见 `src/shared/model-requirements.ts` 中的 `CATEGORY_MODEL_REQUIREMENTS`，其中确实定义了 8 个类别。

3. **变体名确认**：oh-my-openagent 源码中使用的变体名：
   - `visual-engineering` → `variant: "high"` ✅
   - `ultrabrain` → `variant: "xhigh"` ✅
   - `deep` → `variant: "medium"` ✅
   - `artistry` → `variant: "high"` ✅
   - `quick` → 无 variant ✅
   - `unspecified-low` → 无 variant ✅
   - `unspecified-high` → `variant: "max"` ✅
   - `writing` → 无 variant ✅

   来源：https://github.com/code-yeongyu/oh-my-openagent/blob/dev/src/shared/model-requirements.ts

4. **建议**：文章应在类别路由章节明确标注这些功能属于 **oh-my-openagent** 而非 OpenCode 原生功能，或将其从该文章移至 `oh-my-openagent-setup.md`。

---

## (f) Config 合并行为

**文章中使用的表述**（第 57 行）："配置文件是合并（merge）而非替换。后加载的配置仅覆盖冲突的键，非冲突配置会保留。"

**结论**：✅ **描述准确**

**证据**：
- 源码使用 `mergeDeep()` 和 `mergeConfigConcatArrays()` 函数进行合并（来源：https://github.com/sst/opencode/blob/4086a9ae/packages/opencode/src/config/config.ts）
- 官方文档描述与文章一致（来源：https://opencode.ai/docs/config/）
- 大多数 key（如 `model`）后加载覆盖先加载，数组字段（如 `instructions`）做拼接 + 去重

---

## (g) Compaction config keys

### g1. 主章节（第 397-406 行）

**文章中使用的 key**：`auto`, `prune`, `tail_turns`, `preserve_recent_tokens`, `reserved`

**实际 key**（来源：https://opencode.ai/docs/config/#compaction + 源码）：

官方文档列出：`auto`, `prune`, `reserved`

源码（最新版）中增加：`tail_turns`, `preserve_recent_tokens`

| Key | 文章中是否使用 | 官方文档 | 源码中是否存在 |
|-----|--------------|---------|--------------|
| `auto` | ✅ | ✅ | ✅ |
| `prune` | ✅ | ✅ | ✅ |
| `tail_turns` | ✅ | ❌ | ✅（2026 年 4-5 月新增） |
| `preserve_recent_tokens` | ✅ | ❌ | ✅（2026 年 4-5 月新增） |
| `reserved` | ✅ | ✅ | ✅ |

**结论**：⚠️ **基本正确，但 `tail_turns` 和 `preserve_recent_tokens` 是较新特性**

- 这些 key 在 2026 年 4-5 月的 PR #21822 中才加入（来源：https://github.com/anomalyco/opencode/pull/21822）
- 官方文档尚未更新以包含它们
- 文章对 `tail_turns` 的描述（"保留最近 N 轮用户对话"）与源码注释匹配 ✅
- 文章对 `reserved` 的描述（"预留 Token 缓冲区"）与官方文档一致 ✅

### g2. 成本管控章节（第 1075-1089 行）— ❌ 错误

**文章中使用的 key**：
```json
{
  "compaction": {
    "enabled": true,     // ❌ 不存在
    "threshold": 0.8,    // ❌ 不存在
    "strategy": "summarize"  // ❌ 不存在
  }
}
```

**实际 key**：`auto`, `prune`, `reserved`, `tail_turns`, `preserve_recent_tokens`

**结论**：❌ **成本管控章节中的 compaction 配置 key 全部错误**

- `enabled` → 正确 key 是 `auto`
- `threshold` → 不存在此 key（有未合并的 PR #10123 提议 `token_threshold` 和 `context_threshold`，但尚未被合并到主线）
- `strategy` → 不存在此 key（官方文档没有策略字段）

**严重程度**：高 — 读者如果直接使用此配置，OpenCode 会忽略这些无效 key 而不报错，导致配置不生效。

---

## (h) disabled_providers / enabled_providers

**文章中使用的 key**（第 499-509 行）：`disabled_providers`, `enabled_providers`

**结论**：✅ **已验证，key 正确**

**证据**：
- 源码 `config.ts`：
  ```typescript
  disabled_providers: z.array(z.string()).optional().describe("Disable providers that are loaded automatically"),
  enabled_providers: z.array(z.string()).optional().describe("When set, ONLY these providers will be enabled. All other providers will be ignored"),
  ```
  （来源：https://github.com/anomalyco/opencode/blob/9afbdc10/packages/opencode/src/config/config.ts）

---

## (i) fallbackChain

**文章中使用的值**（第 1031-1068 行）：`"fallbackChain": [{ "providers": [...], "model": "...", "variant": "..." }]`

**结论**：⚠️ **该 key 属于 oh-my-openagent，不属于 OpenCode 核心 config**

**详细分析**：
- OpenCode 核心（anomalyco/opencode）的 `config.ts` 中没有 `fallbackChain` 字段
- oh-my-openagent 的 `model-requirements.ts` 中定义了 `FallbackEntry` 类型和 `CATEGORY_MODEL_REQUIREMENTS`，其中使用了 `fallbackChain`
- 官方 OpenCode 文档中没有 `fallbackChain` 配置项

**建议**：文章的成本管控章节（策略二和策略三）使用了 `categories` + `fallbackChain`，应注明这属于 oh-my-openagent 的功能。

---

## (j) categories 是否为顶级 config key

**文章中使用的值**（第 1006-1044 行）：将 `"categories"` 作为顶级 key 使用

**结论**：⚠️ **属于 oh-my-openagent 的配置 key，不是 OpenCode 核心的配置 key**

**证据**：
- OpenCode 核心源码 `config.ts` 的 `Info` schema 中没有 `categories` 字段
- oh-my-openagent 的配置 schema 支持 `categories` 作为顶级 key
- 官方 OpenCode 文档中从未出现过 `categories` 配置项

**建议**：文章应将此内容移至 `oh-my-openagent-setup.md` 或明确标注为 oh-my-openagent 功能。

---

## (k) enterpriseUrl

**文章中使用的值**（第 155 行）：`"options.enterpriseUrl": "GitHub Enterprise URL（用于 copilot 认证）"`

**结论**：✅ **已验证，key 和描述正确**

**证据**：
- 源码 `provider.ts`：
  ```typescript
  enterpriseUrl: Schema.optional(Schema.String).annotate({
    description: "GitHub Enterprise URL for copilot authentication",
  }),
  ```
  （来源：https://github.com/anomalyco/opencode/blob/5c5069b6/packages/opencode/src/config/provider.ts）

- 第三方文档（https://opencode.runman.ai/en/appendix/config-ref.html）也证实此字段的存在和用途。

---

## (l) setCacheKey

**文章中使用的值**（第 127/159 行）：`"options.setCacheKey": true`，描述为"启用 Prompt Cache 密钥（Anthropic 专用，默认 false）"

**结论**：✅ **已验证，key 和描述正确**

**证据**：
- 源码 `provider.ts`：
  ```typescript
  setCacheKey: Schema.optional(Schema.Boolean).annotate({
    description: "Enable promptCacheKey for this provider (default false)",
  }),
  ```
  （来源：同上）
- 官方文档（https://opencode.ai/docs/config/）：
  ```
  `setCacheKey` - Ensure a cache key is always set for designated provider.
  ```
- 注意官方文档的描述比文章更通用（不限 Anthropic），但实际上 Anthropic 和 DeepSeek 是最常用的场景。

---

## 额外发现

### 1. headerTimeout

文章第 126 行使用了 `headerTimeout: 30000`。

根据 OpenCode Changelog（https://opencode.ai/changelog）：
> "Added `headerTimeout` config for provider requests, with a 10s default for default OpenAI setups."

以及 GitHub Issue #26602 和 PR #26599，确认 `headerTimeout` 是真实存在的 provider option。虽然它未显式列在 `provider.ts` 的 `Schema.Struct` 中，但 `StructWithRest` + `[Schema.Record(Schema.String, Schema.Any)]` 接受任意额外 key。

**结论**：✅ **headerTimeout 是有效的配置项**

### 2. 文章中`agent` 在概览段（第 99 行）和实际配置段（第 167 行）key 统一为 `agent`（单数）

**结论**：✅ 正确，与源码一致。

### 3. Compaction 字段默认值

文章第 411 行标注 `auto` 默认值为 `true`，第 412 行标注 `prune` 默认值为 `true`。

实际情况：
- `auto` 默认值 `true` ✅（与官方文档一致）
- `prune` 默认值为 `false`（官方文档 https://opencode.ai/docs/config/ 显示 `"prune": false`，且 Issue #24108 也确认此问题）

**结论**：⚠️ **`prune` 的默认值在官方文档中为 `false`，但文章中写的是 `true`**

### 4. `small_model` 降级链的描述

文章第 757 行描述 quick 降级链为：`small_model` → `model`（回退）。这与官方类别路由系统描述一致。

**注意**：官方 OpenCode 核心并没有"类别路由"概念。这里的描述同样来自 oh-my-openagent 的实现。

---

## 总结与建议

### 严重问题（需优先修复）

1. **成本管控章节的 compaction key 完全错误**（第 1075-1089 行）：`enabled`/`threshold`/`strategy` 全部无效，应改为 `auto`/`prune`/`reserved`。

2. **类别路由系统和成本管控中的 `categories`/`fallbackChain`** 属于 oh-my-openagent，文章未注明来源，可能误导读者以为是 OpenCode 原生功能。

### 中等问题（建议修复）

3. **`prune` 默认值**：文章第 412 行标注 `true`，官方文档为 `false`。

4. **缺失 `codesearch` 和 `todoread` 工具**：permission 工具列表遗漏了这两个官方认可的工具。

### 信息性问题（可考虑改进）

5. `tail_turns` 和 `preserve_recent_tokens` 是较新特性，官方文档尚未覆盖。文章可添加脚注说明这些 key 的适用范围。

6. `edit` 工具覆盖的底层工具（`write`, `patch`, `multiedit`）可补充说明。

### 风险说明

文章中所有配置示例均能通过 OpenCode 的 JSON Schema 验证（无效 key 会被忽略而非报错），因此读者若不仔细验证，可能实际使用了不生效的配置而不自知。建议在适当位置添加验证提示。
