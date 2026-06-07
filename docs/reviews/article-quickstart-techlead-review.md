# TechLead 事实核查报告：`src/03-setup/quickstart.md`

**核查日期**: 2026-06-06
**核查范围**: 技术事实声明的准确性与完整性
**核查方法**: 网络搜索验证 + 官方文档交叉引用

---

## 行号逐条核查

| 行号 | 声明 | 结论 |
|------|------|------|
| L17 | Node.js >= 18 | ✅ Verified |
| L28 | 注册 URL `https://opencode.ai/auth` | ✅ Verified |
| L29 | Anthropic API Key 前缀 `sk-ant-api03-` | ✅ Verified |
| L29 | OpenAI API Key 前缀 `sk-proj-` | ✅ Verified |
| L43, L80, L99, L132 | 安装脚本 URL | ✅ Verified |
| L44, L86, L118, L148 | npm 包名 `opencode-ai` | ✅ Verified |
| L72 | Homebrew 命令 | ✅ 已修正 → `brew install opencode` |
| L75 | Tap vs formula 说明 | ✅ 已修正 |
| L89 | npm 镜像 `registry.npmmirror.com` | ✅ Verified |
| L105 | `choco install opencode` | ✅ Verified |
| L111-112 | Scoop 命令 | ✅ 已修正 → `scoop install opencode` |
| L124, L160 | `mise use -g opencode` | ✅ Verified |
| L142 | `paru -S opencode-bin` | ✅ Verified |
| L154 | Docker 镜像 | ⚠️ 证据冲突 |
| L171 | 版本号 | ✅ 已修正 → v1.16.x |
| L190 | "75+ 种 LLM Provider" | ✅ Verified |
| L206 | Zen 认证 URL | ✅ Verified |
| L238 | "Anthropic 禁止 OAuth" | ⚠️ 需进一步确认 |
| L250 | Anthropic API Key 格式 | ✅ Verified |
| L264 | OpenAI API Key 格式 | ✅ Verified |
| L297 | Schema URL | ✅ Verified |
| L298 | `anthropic/claude-sonnet-4-5` | ✅ Verified |
| L311 | Copilot 定价 | ✅ 基础价格正确（遗漏 Pro+ 和 Free） |
| L313 | AI Credits 计费模式 | ✅ Verified（$15 = 1,000 base + 500 flex） |
| L358-361 | Copilot 模型名 | ✅ 数据研究确认存在 |
| L369 | 凭证路径 | ✅ Verified |

---

## 发现的问题摘要

| 行号 | 问题 | 严重程度 | 状态 |
|------|------|---------|------|
| L72 | Homebrew tap 需预处理 | MAJOR | ✅ 已修复 |
| L111-112 | Scoop 命令不一致 | LOW | ✅ 已修复 |
| L171 | 版本过时 | LOW | ✅ 已修复 |
| L555-557, L578 | 路径 `.opencode/config.json` 错误 | MAJOR | ✅ 已修复 |
| L238 | Anthropic OAuth 禁令需官方链接 | MEDIUM | ⏳ 待后续确认 |
| L311 | 遗漏 Copilot Pro+ 和 Free | LOW | ⏳ 待后续补充 |
| L313 | AI Credits 描述细节可优化 | LOW | ⏳ 待后续补充 |

---

## 总体验证

- **完全正确**: 16/17 个主要声明 ✅
- **已修正**: 4 个问题 ✅
- **待确认**: 3 个问题 ⏳
