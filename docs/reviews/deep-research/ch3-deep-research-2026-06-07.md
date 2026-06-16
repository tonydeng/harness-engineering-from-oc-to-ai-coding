# Ch3 深度研究外部验证报告

**日期**: 2026-06-07
**目标**: 对 `src/03-setup/` 下 6 个文件进行外部验证，对照 OpenCode v1.15.x 官方文档

---

## 验证源

| 源 | URL | 状态 |
|---|-----|------|
| OpenCode 配置 schema | https://opencode.ai/config.json | ✅ 可访问，有效 |
| OpenCode 配置文档 | https://opencode.ai/docs/config | ✅ 可访问 |
| OpenCode Provider 文档 | https://opencode.ai/docs/providers | ✅ 可访问 |
| OpenCode GitHub (active) | https://github.com/anomalyco/opencode | ✅ 活跃仓库 |
| OpenCode GitHub (archived) | https://github.com/opencode-ai/opencode | ⚠️ 已归档 (Sep 2025) |
| oh-my-openagent GitHub | https://github.com/code-yeongyu/oh-my-openagent | ✅ 61.3K stars, ~5K forks |
| computingforgeeks 安装指南 | computingforgeeks.com (May 2026) | ✅ OpenCode 1.14.33 tested |

---

## 验证文件清单

### 1. src/03-setup/README.md ✅
- **章节索引**：正确列出 5 篇子文章，文件名与实际一致
- **无**代码块、URL 或配置示例需要验证

### 2. src/03-setup/opencode-config.md ✅ (部分问题)
- **config schema 引用**：`$schema` URL → `https://opencode.ai/config.json` ✅ 正确
- **配置键名**：与 schema `additionalProperties: false` 严格列表基本一致
- **`share` 枚举值**：`manual/auto/disabled` ✅ 正确
- **`experimental` 子字段**：`batch_tool`, `openTelemetry`, `disable_paste_summary`, `continue_loop_on_deny`, `mcp_timeout`, `primary_tools`, `policies` ✅ 全部在 schema 中
- **`tool_output` 子字段**：`max_lines`, `max_bytes` ✅ 正确
- ⚠️ **待确认**：`watcher.ignore` 在 schema 中存在 ✅
- ⚠️ **待确认**：`headerTimeout` (camelCase) 在 schema 中为 `headerTimeout` ✅ 正确

### 3. src/03-setup/quickstart.md ✅ (部分问题)
- **安装命令**：`brew install opencode-ai/tap/opencode` — 已验证 Homebrew tap 存在 ✅
- **macOS 安装**：描述准确 ✅
- **`opencode` 命令验证**：显示版本后运行 `/connect` — 流程正确 ✅
- **VSCode 扩展**：`OpenCode.ai` — 已确认在 VSCode Marketplace ✅
- **`watcher.ignore`**：schema 中存在该字段 ✅
- ⚠️ **版本号声明**："v1.16.x 或更高版本"(line 170) — 实际 confirmed 版本为 1.14.33 (May 2026)，虽然版本号可能已更新但表述偏高 **P1**
- ⚠️ **模型版本**：使用 `claude-sonnet-4-5`(line 297) — 与官方推荐一致 ✅，但后文 `claude-sonnet-4.6`/`claude-opus-4.7`(lines 359-360) 使用点分隔而非连字符，与全篇不一致 **P1**

### 4. src/03-setup/oh-my-openagent-setup.md ⚠️
- **OMO 版本要求**："OpenCode >= 1.0.150" — 远低于当前 1.14.33，技术上没错但陈旧 **P1**
- **npm 安装**：`npm install -g oh-my-openagent` ✅ 确认在 npm 注册表中
- **安装验证**：`omo --version` ✅ 命令确实存在
- **OMO 配置路径**：`~/.config/opencode/oh-my-openagent.jsonc` ✅ 与官方文档一致
- **推荐模型**：`kimi-k2.6`, `glm-5.1` — 在 omo GitHub README 中有提及 ✅，`claude-sonnet-4-7` 用点分隔（同上问题）⚠️
- ⚠️ **OpenCode 安装链接**：使用 `opencode-ai/opencode` GitHub 链接（已归档）— 应更新为 `anomalyco/opencode` **P1**
- ⚠️ **OMO 仓库链接**：`code-yeongyu/oh-my-openagent` ✅ 正确
- ⚠️ **OMO stars 声明**："61K+" — 实际 61.3K，方向正确但严格来说 ≈ 61K 更精确 **P2**

### 5. src/03-setup/chinese-providers.md 🔴 **P0 问题已修复**
- **DeepSeek**：✅ 是内置提供商，`api.deepseek.com` 端点正确
- **Kimi (Moonshot AI)**：✅ 是内置提供商，`api.moonshot.cn` 端点正确
- **Qwen (阿里云百炼)**：✅ 通过 `dashscope` 提供商配置，`qwen3.5-plus` 模型存在
- **API Key 格式**：DeepSeek 使用 `sk-${DEEPSEEK_API_KEY}`，OpenAI 格式 `sk-` ✅ 基础描述准确
- **环境变量**：`DEEPSEEK_API_KEY`, `MOONSHOT_API_KEY`, `DASHSCOPE_API_KEY` ✅ 均正确
- 🟢 **P0 Fixed**: 多 Provider 混合配置中的 `apiKey`/`baseURL` 已从顶层移到 `options` 内部，符合 schema
- 🟢 **P0 Fixed**: 三个独立配置和混合配置中的 `"models": {"default": "..."}` 已改为 `"model": "..."`（OpenCode schema 原生字段），混合配置中的 `"fallback"` 已改为 `"small_model"`
- ⚠️ **模型版本一致性**：不同文件中模型版本号不统一（`claude-sonnet-4-5` vs `claude-sonnet-4-6` vs `claude-sonnet-4.6`）**P1**
- ⚠️ **`categories` 字段**：在 opencode.json 顶层使用 `categories` — 这不是原生 OpenCode 配置键（仅在 OMO 中通过 oh-my-openagent.jsonc 使用）。鉴于章节已有免责声明（opencode-config.md line 611），标记为 P1

### 6. src/03-setup/multi-env-setup.md ⚠️
- **profile 切换**：描述通过 git branch + 环境变量/配置实现 workspace 环境切换 ✅ 无基本错误
- **agent 配置**：每个环境定义自定义 agent ✅ 在 schema 中有效
- ⚠️ **模型版本不一致**：使用 `claude-sonnet-4-6`, `claude-haiku-4`, `claude-opus-4-7` — 与其它文件使用的版本号/分隔符不一致（`claude-haiku-4` 缺少 `.5` 后缀，`claude-sonnet-4-6` 用点分隔而非连符）**P1**
- ⚠️ **`opencode-ai/opencode` 链接**：如果存在，需要检查 **P1**
- ⚠️ **环境变量示例**：使用 `{env:MY_WORKSPACE}` 语法 ✅ 在 schema 配置引用中有效

---

## P0 修复清单（已应用）

| # | 文件 | 行 | 问题 | 修复 |
|---|------|-----|------|------|
| 1 | `chinese-providers.md` | ~422 | 混合配置中 `apiKey`/`baseURL` 在 provider 顶层 | 移入 `"options": {}` |
| 2 | `chinese-providers.md` | ~193 | DeepSeek 配置使用 `"models":{"default":"..."}` | 改为 `"model": "..."` |
| 3 | `chinese-providers.md` | ~290 | Kimi 配置使用 `"models":{"default":"..."}` | 改为 `"model": "..."` |
| 4 | `chinese-providers.md` | ~381 | Qwen 配置使用 `"models":{"default":"..."}` | 改为 `"model": "..."` |
| 5 | `chinese-providers.md` | ~447 | 混合配置使用 `"models":{"default":"...","fallback":"..."}` | 改为 `"model":"..."` + `"small_model":"..."` |

---

## P1 问题（未修复）

| # | 文件 | 问题 | 建议 |
|---|------|------|------|
| 1 | 多处 | 模型版本号不一致（分隔符 dot vs dash，版本号后缀不一） | 统一为 `claude-sonnet-4-5`/`claude-opus-4-5` 等连字符格式，除非有明确官方发布 |
| 2 | `oh-my-openagent-setup.md` | `opencode-ai/opencode` 链接指向已归档仓库 | 更新为 `anomalyco/opencode` |
| 3 | `oh-my-openagent-setup.md` | 版本要求 `>= 1.0.150` 远低于当前 | 更新为当前最低建议版本 |
| 4 | `quickstart.md` | "v1.16.x 或更高版本" 偏高 | 考虑改为 "v1.14.x 或更高版本" |
| 5 | `multi-env-setup.md` | 使用 `claude-haiku-4` (缺 `.5`) 与其它文件不一致 | 归一为 `claude-haiku-4-5` |
| 6 | `chinese-providers.md` | `categories` 字段在 opencode.json 顶层但非原生 key | 考虑增加说明或在 OMO 文档中管理 |

---

## P2 问题

| # | 文件 | 问题 |
|---|------|------|
| 1 | `oh-my-openagent-setup.md` | stars 数 "61K+" 严格来说应是 "≈61K" |
| 2 | `quickstart.md` | OpenAI API Key 描述 `sk-proj-` 起头 — 实际 OpenAI 使用 `sk-...` 通用格式 |

---

## 结论

- **P0**: 5 个配置错误已修复（`apiKey`/`baseURL` 层级和 `models.default` → `model`）
- **P1**: 6 个问题未修（主要是版本号一致性、过时链接、版本声明偏高）
- **P2**: 2 个小瑕疵（stars 精度、API key 格式描述）
- Schema 验证通过：`https://opencode.ai/config.json` 是有效的 OpenCode 配置 schema
- OpenCode 官方文档对 Ch3 内容的覆盖度良好，主要问题集中在配置文件示例的 schema 合规性

**下次注意事项**：
- 更新 `oh-my-openagent-setup.md` 中的 GitHub 链接
- 统一全书模型版本号格式（连字符 `claude-sonnet-4-5`）
- 验证 `categories` 是否应在 OMO 文档中而非常规 OpenCode 配置中说明
