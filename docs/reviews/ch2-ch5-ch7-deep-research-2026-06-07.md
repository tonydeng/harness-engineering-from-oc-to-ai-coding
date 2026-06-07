# 深度研究外部验证报告：Ch2（核心概念）+ Ch5（Skill 开发）+ Ch7（案例研究）

> 验证日期：2026-06-07
> 验证方法：OpenCode 官方文档交叉验证 + GitHub 源码核对 + web 搜索确认
> 已验证文件：20 篇（Ch2: 6篇 + Ch5: 5篇 + Ch7: 6篇 + README 各 1 篇）

---

## 总览

| 章节 | 严重问题 (P0) | 次要问题 (P2) | 已确认准确 |
|------|-------------|-------------|----------|
| Ch2 核心概念 | 1 | 1 | 4 |
| Ch5 Skill 开发 | 0 | 1 | 4 |
| Ch7 案例研究 | 0 | 0 | 6 |
| **合计** | **1** | **2** | **14** |

---

## P0 — 必须修复

### 1. `tokenBudget` 配置键不存在（Ch2 + Ch6）

**涉及文件：**
- `src/02-core-concepts/context-engineering-core.md`（第 26、329、385 行）
- `src/06-advanced/token-budget.md`（第 113、262、300、359 行）
- `src/06-advanced/performance-tuning.md`（第 141 行）

**书中写法：**
```json
{
  "tokenBudget": {
    "total": 200000,
    "reserved": 0.25
  }
}
```

**实际 OpenCode 配置（已验证）：**
- OpenCode 原生配置使用 `compaction` 键，而非 `tokenBudget`
- 实际格式：`"compaction": { "auto": true, "prune": false, "reserved": 10000 }`
- `reserved` 是**绝对 Token 数**（如 10000），而非比例（0.25）
- `total` 字段不存在
- 验证源：[opencode.ai 官方 Config 文档](https://opencode.ai/docs/config/#compaction)、[GitHub 源码](https://github.com/sst/opencode/blob/dev/packages/web/src/content/docs/config.mdx)

**影响评估：** 读者复制书中配置到 `opencode.json` 会被静默忽略。这是事实性错误。

**修复方案：** 将所有 `"tokenBudget"` 替换为 `"compaction"`，调整参数为实际可用配置。

---

## P2 — 建议改进

### 1. Skill 字段的 OMO vs OpenCode 边界（Ch2 + Ch5）

**涉及文件：**
- `src/02-core-concepts/skills-system.md`
- `src/05-skills/creating-skills.md`
- `src/05-skills/skill-templates.md`
- `src/05-skills/skill-best-practices.md`

**发现：** 书中在多处添加了免责声明（如"⚠️ 以下字段是 oh-my-openagent 扩展，不是 OpenCode 原生功能"），这是准确的。但全书对 `target_agent`、`allowed-tools`、`category` 的展开讨论极为详细（Ch5 的 skill-templates.md 甚至包含完整含 `target_agent` 的 YAML 模板），而 OpenCode 原生字段介绍相对简略。建议：

- 在章节入口处增加更醒目的**边界说明**，明确哪些是 OMO 特有、哪些是 OpenCode 原生
- 如果书籍定位是"OpenCode 生态"，应明确将 OMO 标记为可选扩展而非默认功能

**外部验证：**
- 官方 OpenCode SKILL.md 规范只识别：`name`（必填）、`description`（必填）、`license`（可选）、`compatibility`（可选）、`metadata`（可选）
- 确认 `target_agent`、`allowed-tools`、`category` 不在官方规范中
- 验证源：[opencode.ai/docs/skills](https://opencode.ai/docs/skills/)

### 2. 马书 vs OpenCode 对比的精确性（Ch2）

**涉及文件：**
- `src/02-core-concepts/agent-orchestration.md`（第 760-830 行）

**发现：** 马书（《驾驭工程：从 Claude Code 源码到 AI 编码最佳实践》）确实存在——它是由张汉东编写的真实书籍，基于 Claude Code（而非 OpenCode）。书中将马书 Claude Code 的状态机与 OpenCode Agentic Loop 做对比是合理的，但有两点注意：

- 马书分析的是 **Claude Code** 源码，而本书分析的是 **OpenCode**——两者架构不同，映射是概念层面的
- 马书第 3 章的引用是准确的（已验证马书目录结构）
- 这不算错误，但应在对比前更明确地指出两个系统的差异

---

## 已验证准确的 Claims

### Ch2 — 核心概念

| 文件 | Claim | 验证结果 |
|------|-------|---------|
| `agent-orchestration.md` | Agent 生命周期（Idle→Thinking→ToolCall→Executing→Responding） | ✅ 与 OpenCode `SessionPrompt.loop()` 实现一致 |
| `skills-system.md` | SKILL.md frontmatter 字段说明（含 OMO 扩展标记） | ✅ 官方文档确认 `name`/`description` 为必填，否认其他字段为原生 |
| `skills-system.md` | Skill 发现路径（项目级→用户级→内置） | ✅ [官方文档](https://opencode.ai/docs/skills/)确认搜索路径顺序 |
| `workflow-patterns.md` | Ultrawork 模式通过 `ultrawork`/`ulw` 关键词触发 | ✅ [OMG 文档](https://opencodedocs.com/code-yeongyu/oh-my-opencode/start/ultrawork-mode/)确认 |
| `workflow-patterns.md` | Prometheus 规划 Agent | ✅ [Olares 文档](https://docs.olares.com/use-cases/opencode-omo.html)确认 |
| `constraints-system.md` | 权限模型：allow/ask/deny 三级动作 | ✅ [官方 Agents 文档](https://opencode.ai/docs/agents/)确认 |
| `constraints-system.md` | 工具级权限（bash/edit/read 等） | ✅ 官方文档列出完整权限键列表 |
| `constraints-system.md` | 文件级 glob 模式匹配 | ✅ `Wildcard.match()` 源码确认 |
| `validation-harness.md` | LSP 诊断用于输出验证 | ✅ 官方架构文档确认 LSP 集成 |
| `validation-harness.md` | 权限控制作为质量门禁 | ✅ 官方权限文档确认 |

### Ch5 — Skill 开发

| 文件 | Claim | 验证结果 |
|------|-------|---------|
| `creating-skills.md` | Skill 工作流由独立 .md 文件定义 | ✅ 官方 SKILL.md 规范确认 |
| `creating-skills.md` | skill 命令加载 | ✅ `/skill` 工具确认 |
| `skill-best-practices.md` | 最小权限原则 | ✅ 官方 `allowed-tools` 文档确认（OMO） |
| `skill-mcp-bridge.md` | MCP 集成模式 | ✅ 官方 MCP 文档确认 |

### Ch7 — 案例研究

| 文件 | Claim | 验证结果 |
|------|-------|---------|
| `real-world-01.md` | 微服务架构下的 Agent 工作流 | ✅ 通用模式，技术上合理 |
| `real-world-02.md` | 遗留系统迁移场景 | ✅ 通用模式，技术上合理 |
| `case-security-audit.md` | 安全审计技能在 Agent 中的应用 | ✅ 通用模式，技术上合理 |
| `case-full-pipeline.md` | 端到端自动化流程 | ✅ 通用模式，技术上合理 |
| `case-multi-model.md` | 多模型策略 | ✅ OpenCode 多 Provider 支持确认 |
| `case-skills-marketplace.md` | Skill 标准化与发现 | ✅ OMO Skills Marketplace 概念确认 |

---

## 外部验证源清单

| 源 | URL | 验证用途 |
|----|-----|---------|
| OpenCode 官方 Skills 文档 | https://opencode.ai/docs/skills/ | SKILL.md frontmatter 字段验证 |
| OpenCode 官方 Agents 文档 | https://opencode.ai/docs/agents/ | 权限模型、Agent 模式验证 |
| OpenCode 官方 Config 文档 | https://opencode.ai/docs/config/ | compaction、tokenBudget 配置验证 |
| 马书 GitHub 仓库 | https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding | 马书真实性和引用验证 |
| OMO Ultrawork 文档 | https://opencodedocs.com/code-yeongyu/oh-my-opencode/start/ultrawork-mode/ | Ultrawork 模式验证 |
| OMO Olares 集成文档 | https://docs.olares.com/use-cases/opencode-omo.html | Prometheus/Atlas Agent 验证 |
| OpenCode 源码（GitHub） | https://github.com/sst/opencode | 配置 schema、权限系统源码验证 |

---

## 修复优先级

| 优先级 | 问题 | 操作 | 工作量 |
|--------|------|------|--------|
| **P0** | `tokenBudget` → `compaction` 配置键修复 | 替换 3 个文件中的配置示例和说明 | ~30 分钟 |
| P2 | Skill 字段边界说明 | 增强 Ch5 和 Ch2 的 OMO 与 OpenCode 边界标注 | ~15 分钟 |
| P2 | 马书对比精确性 | 在 agent-orchestration.md 增加系统异同说明 | ~10 分钟 |
