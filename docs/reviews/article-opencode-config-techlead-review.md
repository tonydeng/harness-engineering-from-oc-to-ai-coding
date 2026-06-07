# OpenCode 配置审查 - TechLead 工程视角

**审查日期**: 2026-06-06  
**审查者**: TechLead Engineering Agent  
**审查文件**: `src/03-setup/opencode-config.md`

---

## 执行摘要

**总体评分**: 75/100

**状态**: ❌ **必须修正** - 发现 5 个关键事实错误（会导致配置静默失效），3 个中等问题

**验证方法**: 与官方 OpenCode JSON Schema (`https://opencode.ai/config.json`)、官方文档 (`opencode.ai/docs/config`) 和实际示例配置进行交叉验证

---

## 🔴 关键错误（会导致配置静默失效）

### 错误 C1: 项目配置文件路径错误

**行号**: 36-37（Mermaid 图表第 4 层），1126-1127（团队模板），1142（文件路径标签）

**文章声称**:
> `./.opencode/config.json` 是项目级配置路径

**事实**: 
- 官方 OpenCode 文档明确指出：**项目配置是 `opencode.json` 在项目根目录**
- `.opencode/` 目录用于子目录（`agents/`, `commands/`, `plugins/`），**不是**主配置文件

**官方文档引用**:
> "Add `opencode.json` in your project root"（来源：`open-code.ai/en/docs/config`）

**实际验证**: 
- 项目根目录有 `opencode.json`
- `.opencode/` 目录包含 `package.json`（npm 插件），**没有** `config.json`

**影响**:
- 用户在 `./.opencode/config.json` 创建配置
- OpenCode **不会读取**该文件
- 配置被静默忽略

**建议修复**:
- 所有位置将 `.opencode/config.json` 改为 `opencode.json`
- Mermaid 图表第 4 层标签更新
- 代码块标签更新

---

### 错误 C2: 不存在的权限工具 `repo_clone` 和 `repo_overview`

**行号**: 836-837（权限工具表）

**文章声称**:
> `repo_clone` 和 `repo_overview` 是具有 glob 匹配支持的有效权限工具

**事实**: 
- **这两个工具在 OpenCode 权限 schema 中完全不存在**

**官方 Schema 支持的权限工具**:
```
read, edit, glob, grep, list, bash, task,
external_directory, todowrite, question,
webfetch, websearch, lsp, doom_loop, skill
```

**没有**: `repo_clone` 或 `repo_overview`

**影响**:
- 用户配置这些权限会静默被忽略
- 可能导致意外的权限范围

**建议修复**:
- 从权限工具表中删除这两行

---

### 错误 C3: 成本管控使用不存在的 `categories` 和 `fallbackChain`

**行号**: 1005-1047（策略一、策略二）

**文章声称**:
```json
{
  "categories": {
    "quick": { "model": "fast-model" }
  },
  "fallbackChain": [...]
}
```

**事实**: 
- **`categories` 不是基础 OpenCode 配置字段**
- **`fallbackChain` 不存在于基础 OpenCode Schema**
- 这些是 **oh-my-openagent** 的扩展功能

**证据**:
- 官方 OpenCode Schema (`https://opencode.ai/config.json`) **没有** `categories` 字段
- oh-my-openagent 使用不同的 Schema URL：`https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/dev/assets/oh-my-opencode.schema.json`

**文章混淆**:
- 第 609-774 行描述的是内置类别路由系统（使用 `model` 和 `small_model`）
- 第 1005-1047 行展示虚构的 `categories` 配置
- 将 oh-my-openagent 特性当作基础 OpenCode 功能呈现

**影响**:
- 用户复制配置会完全静默失效
- 没有任何错误提示
- 成本管控策略不生效

**建议修复**:
- 移除策略一、二的配置示例
- 或明确标记为 oh-my-openagent 功能
- 改用基础 OpenCode 的降级链（`model` → `small_model`）

---

### 错误 C4: 成本管控中 Compaction 字段名完全错误

**行号**: 1077-1091（策略四）

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

**事实**: 
- **这三个字段在 OpenCode Schema 中完全不存在**

**官方 Compaction Schema**:
```json
{
  "auto": true,
  "prune": false,
  "tail_turns": 2,
  "preserve_recent_tokens": 4096,
  "reserved": 1024
}
```

**冲突**:
- 第 397-415 行正确描述了 compaction 字段（`auto`, `prune`, `tail_turns` 等）
- 第 1077-1091 行使用完全虚构的字段名

**影响**:
- 配置完全静默失效
- 读者配置的 compaction 不生效

**建议修复**:
- 替换为正确的字段名：`auto`, `prune`, `tail_turns` 等
- 与第 397-415 行保持一致

---

### 错误 C5: `compaction.prune` 默认值错误

**行号**: 412（compaction 字段表）

**文章声称**:
> `prune` 默认值是 `true`

**Schema 实际说明**:
> "Enable pruning of old tool outputs (**default: false**)"

**事实**: 默认值是 `false`

**影响**:
- 读者期望启用的修剪功能实际是关闭的
- 可能导致 Token 消耗超出预期

**建议修复**:
- 将表格中的默认值从 `true` 改为 `false`

---

## 🟡 中等问题

### 错误 M1: 章节 11 使用错误的配置键名

**行号**: 11（引言文本）

**问题**:
> "...agents 定义... mcpServers 集成..."

**实际**:
- 配置键是 `"agent"`（单数），不是 `agents`
- 配置键是 `"mcp"`，不是 `mcpServers`

**影响**: 
- 与代码块中的实际键不一致
- 可能造成混淆

**建议修复**:
- 改为 "Agent 定义" 和 "MCP 服务器集成"

---

### 错误 M2: 成本管控中的 `experimental.policies` 资源格式

**行号**: 第 592 行

**文章声称**:
```json
"resource": "provider:some-expensive-model"
```

**官方文档**:
> `"resource": "openai"` (纯 provider ID)

**事实**: 
- 资源字段应该是纯 provider ID（如 `"openai"`、`"anthropic"`）
- 不需要 `"provider:"` 前缀

**建议修复**:
- 将资源改为纯 provider ID 字符串

---

### 错误 M3: 配置优先级图表不完整

**行号**: 第 21-55 行

**问题**:
- 图表显示 **6 层** 优先级
- 官方文档有 **8 层** 优先级

**官方 8 层优先级**（来源：`opencode.ai/docs/config#precedence-order`）:
1. Remote 配置 (`.well-known/opencode`)
2. 全局配置 (`~/.config/opencode/opencode.json`)
3. 自定义配置 (`OPENCODE_CONFIG` 环境变量)
4. **项目配置 (`opencode.json`)**
5. `.opencode` 目录
6. 内联配置 (`OPENCODE_CONFIG_CONTENT`)
7. 托管配置文件
8. macOS 托管偏好（最高优先级）

**文章缺失**:
- 第 3 层：`OPENCODE_CONFIG` 环境变量（自定义路径）
- 第 5 层：`.opencode` 目录
- macOS 托管作为独立层

**建议修复**:
- 更新图表反映 8 层优先级
- 更正项目配置为 `opencode.json`

---

## 🟡 低优先级问题

### 错误 L1: MCP filesystem 示例格式

**行号**: 第 255 行

**文章代码**:
```
["node", "mcp-filesystem", "--root", "/workspace"]
```

**正确**:
```
["npx", "-y", "@modelcontextprotocol/server-filesystem", "/workspace"]
```

**问题**: 
- 包名为 `@modelcontextprotocol/server-filesystem`
- 需要通过 `npx -y` 运行

**影响**: 
- 该示例不会实际运行
- 但文章后面的完整示例（第 1226 行）使用正确格式

**建议修复**:
- 与第 1226 行保持一致

---

### 错误 L2: 模型版本不一致

**问题**:
- 文章使用 `claude-sonnet-4-5` 和 `claude-haiku-4-5`
- 项目示例文件使用 `claude-sonnet-4-6`、`claude-opus-4-7`
- 第 3 章其他文章使用 `claude-sonnet-4-6`

**说明**: 
- `claude-sonnet-4-5` 是 OpenCode 文档中的示例
- 但 Anthropic 当前模型是 `claude-sonnet-4-6`

**建议**: 
- 考虑更新为 `claude-sonnet-4-6`
- 或明确说明这些是 OpenCode 内部模型 ID

---

## 验证清单

| 项目 | 状态 |
|------|------|
| Schema URL (`https://opencode.ai/config.json`) | ✅ 正确 |
| Provider 端点 (Anthropic, OpenAI, Bedrock) | ✅ 正确 |
| `mcp` 键（不是 `mcpServers`） | ✅ 正确 |
| `permission` 键（不是 `permissions`） | ✅ 正确 |
| `agent` 键（不是 `agents`） | ✅ 正确 |
| `plugin` 数组格式 | ✅ 正确 |
| `compaction` 基础描述（第 397-415 行） | ✅ 正确 |
| Server 配置 | ✅ 正确 |
| Formatter/LSP 配置 | ✅ 正确 |
| 环境变量注入 (`{env:VAR}`) | ✅ 正确 |

---

## 总结

**必须修正的 5 个关键错误**:
1. 项目配置路径（`opencode.json` vs `.opencode/config.json`）
2. 不存在的权限工具 (`repo_clone`, `repo_overview`)
3. 虚构的成本管控配置 (`categories`, `fallbackChain`)
4. 虚构的 compaction 字段 (`enabled`, `threshold`, `strategy`)
5. `prune` 默认值（`false` vs `true`）

**建议修复优先级**:
1. 🔴 高 - 修复成本管控章节（策略一、二、四）
2. 🔴 高 - 从权限表移除不存在的工具
3. 🔴 高 - 更新配置优先级图表
4. 🟡 中 - 修正 MCP 示例格式
5. 🟡 中 - 修正 `experimental.policies` 资源格式
6. 🟡 中 - 更新章节 11 的引言文本
7. ⚪ 低 - 考虑更新模型版本

---

## 审查文件

- `docs/reviews/article-opencode-config-karpathy-review.md`
- `docs/reviews/article-opencode-config-techlead-review.md` (本文件)
- `docs/reviews/article-opencode-config-munger-review.md` (待创建)
