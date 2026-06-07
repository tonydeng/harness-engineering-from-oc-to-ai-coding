# Karpathy 视角审查：opencode-config.md

> 以工程现实主义的眼光逐条核对事实。不说好话，只找问题。

**审查日期**: 2026-06-06
**审查文件**: `src/03-setup/opencode-config.md`
**方法**: 逐段对照 `opencode.ai/config.json` schema + 官方文档 config/agents/permissions/mcp 页面 + DeepWiki 实现参考

---

## 🔴 确认的事实错误

### 1. 权限工具表包含不存在的 key：`repo_clone`、`repo_overview`

**位置**: 第 836-839 行

**文章声称**: 权限系统支持 `repo_clone` 和 `repo_overview` 两个工具，且支持 glob 匹配。

**事实**: 官方 schema 的 `PermissionConfig` 定义中，完整列表是：`read`、`edit`、`glob`、`grep`、`list`、`bash`、`task`、`external_directory`、`todowrite`、`question`、`webfetch`、`websearch`、`lsp`、`doom_loop`、`skill`。

**没有** `repo_clone`。**没有** `repo_overview`。

这意味着用户配置了这两个 key 会被静默忽略，且可能以为某个操作被限制了而实际上没有。imo，权限系统的文档不能有虚构 key——这是最危险的文档错误类型。

---

### 2. 项目配置文件路径错误

**位置**: 第 36-37 行（流程图）、第 1126-1127 行（团队配置示例）

**文章声称**: 项目级配置文件路径是 `./.opencode/config.json`。

**事实**: 官方文档明确说项目配置文件就是项目根目录下的 `opencode.json`：
> "Add `opencode.json` in your project root."

`.opencode/` 目录是**子目录结构**，存放 agents/、commands/、plugins/ 等。它本身不是一个配置文件路径。这个项目自己就是证据——根目录是 `opencode.json`，不是 `.opencode/config.json`。

---

### 3. 默认权限模型描述有根本性偏差

**位置**: 第 887-904 行

**文章声称**:
```
OpenCode 默认保护以下敏感路径：
{
  "permission": {
    "edit": {
      "*": "ask",
      ".env": "deny",
      ...
    }
  }
}
```

隐含的意思是：OpenCode 默认是「大部分操作需要批准 + 敏感路径禁止编辑」。

**事实**: 官方文档明确说：
> "By default, opencode **allows all operations** without requiring explicit approval."

默认是 `"allow"` 几乎所有操作。唯一的例外是 `.env` 文件在 `read` 权限下被 deny（注意是 read 不是 edit）。文章展示的 `"*": "ask"` 是一个显式收紧配置，不是默认值。

imo，这是整篇文章最误导人的地方——把安全建议伪装成了默认行为。

---

### 4. `compaction.prune` 默认值写反

**位置**: 第 412 行

**文章声称**: `prune` 默认值为 `true`。

**事实**: Schema 定义：
> "Enable pruning of old tool outputs (default: false)"

实际默认是 `false`。文章写反了。

---

### 5. 成本管控章节的 `categories` 配置不存在于 OpenCode Schema

**位置**: 第 1008、1031、1061 行

**文章声称**: 在 `opencode.json` 顶层使用 `"categories"` key，配置 `model`、`fallbackChain` 等字段。

```json
{
  "categories": {
    "quick": { "model": "fast-model" },
    "ultrabrain": { "fallbackChain": [...] }
  }
}
```

**事实**: 官方 schema 的顶层 Config 对象中**没有** `categories` 这个 key。完整的顶层 key 列表是：`$schema`、`shell`、`logLevel`、`server`、`command`、`skills`、`reference`、`watcher`、`snapshot`、`plugin`、`share`、`autoupdate`、`disabled_providers`、`enabled_providers`、`model`、`small_model`、`default_agent`、`username`、`agent`、`provider`、`mcp`、`formatter`、`lsp`、`instructions`、`permission`、`tools`、`attachment`、`enterprise`、`tool_output`、`compaction`、`experimental`。

没有 `categories`。没有 `fallbackChain`。这可能是 oh-my-openagent 的扩展配置——文章没有说明，且使用了错误的 schema URL。

---

### 6. 成本管控章节的 compaction 配置使用了完全不同的字段名

**位置**: 第 1077-1091 行

**文章声称**:
```json
{
  "compaction": {
    "enabled": true,
    "threshold": 0.8,
    "strategy": "summarize"
  }
}
```

**事实**: 官方 `compaction` 的字段是：`auto`、`prune`、`tail_turns`、`preserve_recent_tokens`、`reserved`。文章列的三个字段（enabled、threshold、strategy）全部不存在。

更尴尬的是——文章之前在第 397-415 行已经**正确描述了一遍 compaction 的实际 schema**。然后在成本管控章节又用了三个不存在的字段。自相矛盾。

---

### 7. MCP filesystem 命令示例不对

**位置**: 第 255 行

**文章声称**:
```json
"command": ["node", "mcp-filesystem", "--root", "/workspace"]
```

**事实**: `mcp-filesystem` 不是 npm 上的包名。正确的包是 `@modelcontextprotocol/server-filesystem`，通过 npx 运行：
```json
"command": ["npx", "-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
```

---

## 🟡 很可能是事实错误（缺乏官方文档直接证据）

### 8. 类别路由系统（8 个内置类别）未在官方文档中出现

**位置**: 第 609-774 行

**文章声称**: OpenCode 内置 8 个类别（visual-engineering、ultrabrain、deep、artistry、quick、unspecified-low、unspecified-high、writing），每个有预设变体（variant）和降级链。

**疑点**: 官方 config schema 和文档都没有 `category` 或 `categories` 这两个 key。官方文档没有「类别路由系统」这个概念。这很可能又是 oh-my-openagent 的功能。

imo，文章花了很大篇幅（165 行）描述一个可能不存在于 OpenCode 原生的系统。如果它是 oh-my-openagent 的功能，应该明确标出来。

---

### 9. 内置 agent 列表与官方文档不一致

**位置**: 第 624-633 行的类别表格

**文章声称的类别变体**:
- ultrabrain: xhigh
- deep: medium
- artistry: high
- unspecified-high: max

**疑点**: 官方 schema 中 `AgentConfig.variant` 的类型是 `string`，没有定义可选值范围。schema 中没有 `xhigh`、`max` 这些变体名。官方文档也没有 category-related variants 的定义。

这可能存在，但我找不到证据。

---

### 10. 配置优先级图谱缺少 `.opencode` 目录层

**位置**: 第 21-55 行

**文章声称的 6 层优先级**: 远程 → 全局 → OPENCODE_CONFIG → .opencode/config.json → OPENCODE_CONFIG_CONTENT → 托管配置

**实际优先级（来自官方文档）**:
1. 远程配置（.well-known/opencode）
2. 全局配置（~/.config/opencode/opencode.json）
3. 自定义路径（OPENCODE_CONFIG 环境变量）
4. 项目配置（项目根目录 opencode.json）
5. **`.opencode` 子目录**（agents/、commands/、plugins/ 等）
6. 内联配置（OPENCODE_CONFIG_CONTENT）
7. 托管配置文件
8. macOS 托管偏好（.mobileconfig）

文章完全漏掉了第 5 层（`.opencode` 子目录），且错误地把 `.opencode/config.json` 当作项目配置文件。

---

## ⚪ 遗漏和次要问题

### 11. 完全没有提及 `tui.json`

官方文档明确将 TUI 设置（theme、keybinds、scroll_speed 等）分离到 `tui.json`，且 `opencode.json` 中的这些 key 已被标记为 deprecated 并自动迁移。文章完全没有提及这个分离架构。

### 12. 缺失顶层 `tools` 配置

官方 schema 顶层有 `tools`（类型 `Record<string, boolean>`），用于全局控制工具开/关。文章没有提及。

### 13. 缺失 `{file:path}` 变量语法

文章只介绍了 `{env:VAR_NAME}` 变量引用，但官方文档还支持 `{file:path/to/file}` 语法（从文件中读取 API Key 等内容）。

### 14. `disabled_providers` 与 `enabled_providers` 优先级关系未说明

官方文档明确说 `disabled_providers` 优先级高于 `enabled_providers`。文章只分别列出了两个 key，没说明冲突时的行为。

### 15. 模型 ID 格式

文章使用 `anthropic/claude-sonnet-4-5`。官方文档当前示例使用 `anthropic/claude-sonnet-4-20250514`（带日期后缀）。不确定 `4-5` 是否仍是有效 ID，但值得确认。

---

## 总结

| 类别 | 数量 | 核心问题 |
|------|------|---------|
| 🔴 确认的事实错误 | 7 | 权限表虚构 key、项目配置路径、默认权限描述、prune 默认值、categories 不存在、cost 章节的 compaction 字段、MCP 命令示例 |
| 🟡 很可能错误 | 3 | 类别路由系统归属、variant 值域、配置优先级漏层 |
| ⚪ 遗漏/次要 | 5 | tui.json 分离、顶层 tools 配置、{file:} 语法、provider 优先级、模型 ID 格式 |

**IMO**：这篇文章最严重的问题不是单个错误，而是一个系统性偏差——把 oh-my-openagent 的扩展配置混入 OpenCode 原生配置描述（类别路由、categories、fallbackChain），同时用一个宽松的 schema URL 作为引用。读者复制成本管控章节的配置会完全静默失效。最危险的文档永远是那种看起来正确、实际上被忽略的。

另一个系统性风险在「默认权限」的描述——把安全最佳实践包装成「默认行为」，给读者的心理模型是 OpenCode 默认是安全的，这跟事实相反。
