# Karpathy 工程现实主义审查：`src/03-setup/quickstart.md`

**审查日期**: 2026-06-06
**目标文件**: `src/03-setup/quickstart.md`
**审查方法**: 事实核查 + 技术验证 + 交叉引用官方 OpenCode 文档
**验证工具**: 本地 OpenCode v1.16.2 二进制文件、官方 opencode.ai/docs/、opencode.ai/config.json schema、opencode.ai/docs/permissions/、opencode.ai/docs/models/

## 审查原则

> "只有你**验证过确实存在**的东西才写进文档。如果文档说 `/init` 命令存在，先去运行它，确认它确实存在。不要凭空假设。"
>
> — Karpathy 式工程思维

本次审查发现 **7 个事实性问题**：**2 个 CRITICAL**（用户将无法继续）、**2 个 MAJOR**（产生错误行为/误导）、**3 个 MINOR**（不准确但影响有限）。

---

## Critical（严重——会直接导致用户操作失败）

### C1. Docker 安装方式存在证据冲突（第 154 行）

| 字段 | 值 |
|------|------|
| **行号** | 154 |
| **文档中写明** | `docker run -it --rm ghcr.io/anomalyco/opencode` |
| **实际情况** | 存在证据冲突：本地 `docker manifest inspect` 返回 `no such manifest`，但数据研究发现多个 Docker 代理站点确认该镜像存在。需进一步验证。 |
| **严重程度** | **CRITICAL（存疑，保留待后续确认）** |
| **建议修正** | 使用 `docker pull ghcr.io/anomalyco/opencode:latest` 实际验证后再决定是否保留。 |

### C2. Copilot 模型名称与官方推荐列表有差异（第 356–361 行）

| 字段 | 值 |
|------|------|
| **行号** | 356–361 |
| **文档中写明** | `gpt-5.3-codex`、`gpt-5.1`、`claude-sonnet-4.6`、`claude-opus-4.7` |
| **官方推荐模型**（opencode.ai/docs/models/） | GPT 5.2、GPT 5.1 Codex、Claude Opus 4.5、Claude Sonnet 4.5 |
| **严重程度** | **CRITICAL（存疑，数据研究确认这些模型名存在于 Copilot 生态中）** |
| **建议修正** | 添加说明实际可用模型以 `/models` 命令输出为准。考虑同步官方推荐模型名称。 |

---

## Major（主要——会产生误导或引发问题行为）

### M1. 安全配置路径错误：`.opencode/config.json` → `opencode.json` — ✅ 已修复

| 字段 | 值 |
|------|------|
| **行号** | 555–557 |
| **问题** | 文档使用 `.opencode/config.json`，但官方 OpenCode 的项目级配置文件是项目根目录下的 `opencode.json`。`.opencode/` 目录用于 agents/、skills/ 等子目录。 |
| **严重程度** | **MAJOR** |
| **修正** | 改为 `opencode.json`，并更新两个代码块标签。 |

### M2. Homebrew tap 需预处理 — ✅ 已修复

| 字段 | 值 |
|------|------|
| **行号** | 72 |
| **问题** | `brew install anomalyco/tap/opencode` 默认会失败，因为 tap 未安装。 |
| **严重程度** | **MAJOR** |
| **修正** | 改为 `brew install opencode`（homebrew-core formula，无需 tapping）。 |

---

## Minor（次要）

### m1. 版本号更新 — ✅ 已修复

| 行号 | 问题 | 修正 |
|------|------|------|
| 171 | `v1.15.x` → 当前版本 1.16.2 | 改为 `v1.16.x` |

### m2. 模型 ID 格式（第 297–298 行）

`anthropic/claude-sonnet-4-5` 是常见缩写，官方模型 ID 含日期戳如 `claude-sonnet-4-5-20250929`。可作为后续优化项。

### m3. Copilot AI Credits 定价（第 311 行）

$15 = 1,000 base + 500 flex credits，此信息基本正确但可补充细节。

---

## 已验证正确的项目

| 项目 | 行号 | 状态 |
|------|------|------|
| Anthropic API Key 前缀 `sk-ant-api03-` | 29, 250, 284 | ✅ |
| OpenAI API Key 前缀 `sk-proj-` | 29, 264, 287 | ✅ |
| `"permission"`（单数） | 557, 581 | ✅ |
| `$schema` URL | 297, 559, 580 | ✅ |
| 凭证路径 `~/.local/share/opencode/auth.json` | 369 | ✅ |
| TUI 命令 `/connect`, `/init`, `/models` 等 | 518–526 | ✅ |
| Tab 键切换 Plan/Build 模式 | 453, 477 | ✅ |
| `.ignore` 文件格式 | 607 | ✅ |
| npm 包名 `opencode-ai` | 86, 118, 148 | ✅ |
| 官方安装脚本 | 80, 132 | ✅ |
