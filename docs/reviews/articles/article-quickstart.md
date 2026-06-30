# 综合评审：article-quickstart

**审查日期**: 2026-06-06  
**目标文件**: `src/03-setup/quickstart.md`  
**评审视角**: Karpathy（工程现实主义/事实核查）、Munger（认知偏误/逆向思维）、TechLead（技术事实逐行核验）

---

## 评审概述

对 `src/03-setup/quickstart.md`（24 节，~685 行）从三个互补视角进行了综合评审。Karpathy 发现 7 个事实性问题（2 CRITICAL、2 MAJOR、3 MINOR），Munger 识别出 8 个认知偏误类别，TechLead 完成了 16/17 个主要声明的行级验证。关键事实错误已修复，但 Munger 视角揭示的结构性偏误（激励偏差、隐藏成本）需要更深入的修改。

---

## 各视角发现汇总

### Karpathy 视角（工程现实主义 — 事实核查）

发现 **7 个事实性问题**：

#### CRITICAL（严重 — 会直接导致用户操作失败）

| # | 问题 | 行号 | 说明 | 状态 |
|---|------|------|------|------|
| C1 | Docker 安装方式存在证据冲突 | 154 | `docker manifest inspect` 返回 `no such manifest`，但数据研究确认镜像存在于代理站点 | ⚠️ 存疑待确认 |
| C2 | Copilot 模型名称与官方推荐列表有差异 | 356-361 | 文档写 `gpt-5.3-codex` 等，官方推荐为 GPT 5.2、Claude Opus 4.5 等 | ⚠️ 存疑待确认 |

#### MAJOR（主要 — 会产生错误行为/误导）

| # | 问题 | 行号 | 说明 | 状态 |
|---|------|------|------|------|
| M1 | 安全配置路径错误：`.opencode/config.json` → `opencode.json` | 555-557 | `.opencode/` 用于 agents/skills 子目录 | ✅ 已修复 |
| M2 | Homebrew tap 需预处理 | 72 | `brew install anomalyco/tap/opencode` 默认会失败 | ✅ 已修复 |

#### MINOR（次要 — 不准确但影响有限）

| # | 问题 | 行号 | 状态 |
|---|------|------|------|
| m1 | 版本号 v1.15.x 过时（当前 1.16.2） | 171 | ✅ 已修复 |
| m2 | 模型 ID 格式可优化，官方 ID 含日期戳 | 297-298 | ⏳ 后续优化 |
| m3 | Copilot AI Credits 定价可补充细节 | 311 | ⏳ 后续补充 |

### Munger 视角（认知偏误分析 — 逆向思维）

识别 **8 个认知偏误类别**：

| # | 偏误类别 | 严重度 | 涉及行号 | 说明 |
|---|---------|--------|---------|------|
| 1 | **激励偏差（Incentive Bias）** | 🔴 高 | 28, 193-233, 373-377 | OpenCode Zen 作为"新手推荐"但未披露利益冲突（OpenCode 自营商业服务） |
| 2 | **隐藏成本（Hidden Costs）** | 🔴 高 | 206, 313, 对比表 | OpenCode Zen 需填账单信息但不提价格；无 TCO 对比 |
| 3 | **遗漏最坏情况（Omitted Worst Case）** | 🟡 中 | 80, 444, 553 | `curl \| bash` 无安全警告；"Always"权限选项无危险说明 |
| 4 | **确认偏误（Confirmation Bias）** | 🟡 中 | 229-233, 667-674 | 只呈现使用好处，未讨论局限性和适用边界 |
| 5 | **虚假确定性（False Certainty）** | 🟡 中 | 3, 7, 397-398 | 20-30 分钟排除了首次注册/安装 Node.js/排查时间 |
| 6 | **隐含假设（Unstated Assumptions）** | 🟡 中 | 15-30, 80 | 假设读者已有 Node.js 18+、现代终端、GitHub 账户等 |
| 7 | **叙事谬误（Narrative Fallacy）** | 🟢 低 | 398, 677 | AGENTS.md"出生证明"隐喻暗示永久权威性 |
| 8 | **锚定效应（Anchoring）** | 🟢 低 | 193-194, 373-377 | OpenCode Zen 排"方式一"且标"推荐新手"，锚定读者选择 |

### TechLead 视角（技术事实行级核验）

16/17 个主要声明验证结果：

| 行号 | 声明 | 结论 |
|------|------|------|
| L17 | Node.js >= 18 | ✅ 已验证 |
| L28 | 注册 URL `https://opencode.ai/auth` | ✅ 已验证 |
| L29 | Anthropic API Key 前缀 `sk-ant-api03-` | ✅ 已验证 |
| L29 | OpenAI API Key 前缀 `sk-proj-` | ✅ 已验证 |
| L44, L86, L118, L148 | npm 包名 `opencode-ai` | ✅ 已验证 |
| L72 | Homebrew 命令 | ✅ 已修正 → `brew install opencode` |
| L89 | npm 镜像 `registry.npmmirror.com` | ✅ 已验证 |
| L105 | `choco install opencode` | ✅ 已验证 |
| L124, L160 | `mise use -g opencode` | ✅ 已验证 |
| L142 | `paru -S opencode-bin` | ✅ 已验证 |
| L154 | Docker 镜像 | ⚠️ 证据冲突 |
| L171 | 版本号 | ✅ 已修正 → v1.16.x |
| L190 | "75+ 种 LLM Provider" | ✅ 已验证 |
| L206 | Zen 认证 URL | ✅ 已验证 |
| L311 | Copilot 定价 | ✅ 基础价格正确（遗漏 Pro+ 和 Free） |
| L358-361 | Copilot 模型名 | ✅ 数据研究确认存在 |

---

## 问题与建议

### 已修复项

| # | 问题 | 来源视角 | 状态 |
|---|------|---------|------|
| 1 | Homebrew tap 需预处理 → `brew install opencode` | Karpathy, TechLead | ✅ 已修复 |
| 2 | Scoop 命令不一致 | TechLead | ✅ 已修复 |
| 3 | 版本号 v1.15.x → v1.16.x | Karpathy, TechLead | ✅ 已修复 |
| 4 | 路径 `.opencode/config.json` 错误 | Karpathy, TechLead | ✅ 已修复 |

### 待处理项

| # | 问题 | 来源视角 | 建议 | 优先级 |
|---|------|---------|------|--------|
| 5 | Docker 镜像存在证据冲突 | Karpathy, TechLead | 实际 `docker pull` 验证后决定保留/移除 | 🟡 中 |
| 6 | Copilot 模型名与推荐列表差异 | Karpathy | 添加说明以 `/models` 输出为准 | 🟡 中 |
| 7 | 激励偏差：推荐 OpenCode Zen 未披露利益冲突 | Munger | 添加利益冲突声明；增加成本透明性 | 🔴 高 |
| 8 | 隐藏成本：无 TCO 对比，OpenCode Zen 价格不可见 | Munger | 在对比表增加价格列 | 🔴 高 |
| 9 | `curl \| bash` 安全反模式无警告 | Munger | 添加安全警告和验证步骤 | 🟡 中 |
| 10 | Anthropic OAuth 禁令需官方链接 | TechLead | 添加官方文档引用 | 🟡 中 |
| 11 | 遗漏 Copilot Pro+ 和 Free | TechLead | 补充不同套餐说明 | 🟢 低 |
| 12 | AI Credits 描述细节优化 | TechLead | 补充消耗速率说明 | 🟢 低 |

---

## 综合评分

| 评估维度 | Karpathy | Munger | TechLead | 综合 |
|---------|----------|--------|----------|------|
| 事实准确性 | 修复后 90% | — | 16/17 说明通过 | **~90%** |
| 认知偏误风险 | — | 🔴 3 高风险项 | — | **需修复** |
| 技术声明完整性 | 修复后良好 | — | 已修正 4 项 | **良好** |
| 读者利益保护 | — | 🟡 中风险 | — | **需改进** |

**总体判断**: 技术事实在 Karpathy 和 TechLead 视角下已基本修正，但 Munger 视角揭示了更深层的问题——文章中 OpenCode Zen 推荐存在激励偏差和隐藏成本，`curl | bash` 缺少安全警告。这些结构性偏误需要作者层面做出修改决策。

---

*评审文件来源: article-quickstart-karpathy-review.md, article-quickstart-munger-review.md, article-quickstart-techlead-review.md*


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

