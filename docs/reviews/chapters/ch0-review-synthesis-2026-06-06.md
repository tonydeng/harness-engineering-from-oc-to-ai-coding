# Ch0 读者导航 — 5 轮质量 Review 综合报告

> **审查日期**：2026-06-06
> **审查范围**：`src/00-guide/` 下 4 篇文章（README.md, reading-paths.md, how-to-read.md, quick-start.md）
> **审查方法**：数据准确性验证 → Karpathy 视角 → Munger 视角 → 内容一致性 → 内容研究写作
> **参考源**：PRD v2.5, user-stories v2.2, ch00-reader-guide spec, wiki 4 篇, GitHub 官方仓库实时验证

---

## 一、数据准确性验证（Review 1）

### 验证方法

直接访问 GitHub 仓库页面和 `mdbook build` 进行实时验证。

### 验证结果

| 项目 | 文章声明 | 实际值 | 判定 |
|------|---------|--------|------|
| OpenCode 版本 | v1.16.x (v1.16.2) | v1.16.2 (Jun 5, 2026) | ✅ 正确 |
| oh-my-openagent 版本 | v4.13.x (v4.13.0) | v4.13.0 (Jun 3, 2026) | ✅ 正确 |
| mdBook 版本 | v0.5.x (v0.5.3) | v0.5.3 (本地安装) | ✅ 正确 |
| OpenCode GitHub URL | `anomalyco/opencode` | `anomalyco/opencode` (171k stars) | ✅ 正确 |
| oh-my-openagent GitHub URL | `code-yeongyu/oh-my-openagent` | `code-yeongyu/oh-my-openagent` (61.2k stars) | ✅ 正确 |
| 写作状态 (README.md L390) | "42 篇已完成，8 篇写作中" | PRD 声明 "50 篇全部完成（100%）" | ❌ 不一致 |
| 写作状态 (reading-paths.md L13) | "42 篇文章完成，8 篇写作中" | 同上 | ❌ 不一致 |
| reading-paths 文章状态标记 | 多处 "⚠️ 写作中" | 全部应为 "✅ 已完成" | ❌ 不一致 |
| Node.js 描述 (quick-start L15) | "OpenCode 运行环境" | OpenCode 是 TypeScript 项目，以独立二进制发布，Node.js 仅 npm 安装方式需要 | ❌ 误导 |
| Node.js 描述 (README.md L327) | "本地预览环境" | mdBook 是 Rust 编写的，不需要 Node.js 做本地预览 | ❌ 误导 |
| 安装方式 (quick-start) | 仅列 npm/curl/scoop/choco | 缺少 `brew install anomalyco/tap/opencode`（官方推荐方式） | ⚠️ 不完整 |
| 时间线 (README.md L337) | "2026-Q4 (12月) : oh-my-openagent 项目创建" | 项目在 2026-06 已有 61.2k stars 和 8228 commits，创建时间远早于 2026-Q4 | ❌ 事实错误 |
| how-to-read.md 配置示例 (L399) | `"model": "claude-3-opus"` | 过时模型名称，当前应为 `claude-opus-4-7` 等 | ⚠️ 过时 |
| `mdbook build` | — | 构建成功，无错误 | ✅ |
| SUMMARY.md 链接 | — | 所有链接目标文件存在 | ✅ |
| PRD 版本号 (v1.15.x/v4.5.x) | — | 实际为 v1.16.x/v4.13.x | ⚠️ PRD 滞后（非 Ch0 问题） |

---

## 二、Karpathy 视角（Review 2）— 技术可靠性与可验证性

### 核心原则："构建即理解"

> "If you can't reproduce it, you don't understand it."

### 发现的问题

#### K1: Node.js 依赖声明不可验证 [MUST-FIX]

**问题**：quick-start.md 将 Node.js 描述为 "OpenCode 运行环境"，但实际上 OpenCode 通过 curl/brew 安装时下载的是预编译的独立二进制文件，不依赖本地 Node.js 运行时。只有 `npm install -g opencode-ai` 这条安装路径需要 Node.js。

**Karpathy 会问**："你说 Node.js 是运行环境，那我 `which node` 找不到 Node.js 的时候，OpenCode 能跑吗？答案是能。这就是命名不等于理解。"

**修复**：将 Node.js 描述改为"npm 安装方式所需"，并标明 curl/brew 安装不需要 Node.js。

#### K2: "提升 2x+ 效率"未提供验证路径 [INFO]

**问题**：reading-paths.md 中"效率开发者"的核心目标是"提升 2x+ 效率"，但没有提供任何度量方法或参考数据。

**Karpathy 会说**："这是一个不可证伪的声明。march of nines —— 你说 2x 就是 2x？拿什么量？"

**建议**：不修改（属于 SHOULD-FIX 范围，需要后续补充数据支撑）。

#### K3: 版本声明可验证性 [PASS]

**优点**：README.md 的版本声明（v1.16.2 / v4.13.0 / v0.5.3）经过实时验证全部正确。这是"构建即理解"的好例子——声明具体版本号，读者可以自行验证。

---

## 三、Munger 视角（Review 3）— 实用故障模式与误导性表述

### 核心原则：逆向思考

> "Invert, always invert. 先想想怎么会失败。"

### 发现的问题

#### M1: quick-start 安全检查位置错误 [MUST-FIX]

**问题**：安全检查（权限控制）在第 238 行，位于"步骤三：启动第一个 Session"（第 122 行）之后。读者可能在读到安全部分之前就已经执行了 AI 生成的代码。

**Munger 会说**："你把安全警告放在人们已经做了危险动作之后，就像在车祸后才告诉人要系安全带。 incentives 完全搞反了。"

**修复**：在"步骤二：初始化项目"之后、"步骤三"之前插入简要安全提示，或至少在步骤三中添加安全提示链接。

#### M2: Provider 配置指引模糊 [SHOULD-FIX]

**问题**：quick-start.md 第 100 行写"编辑 `~/.config/opencode/opencode.json` 添加 API 配置"，但没有给出任何配置示例或说明应该添加什么内容。

**Munger 会说**："你告诉人家去编辑一个配置文件，但不告诉他该写什么。这就像告诉人家'去投资'但不说怎么开户。普通人会在这里放弃。"

**修复**：添加最小可用的 Provider 配置示例。

#### M3: 版本状态不一致损害可信度 [MUST-FIX]

**问题**：README.md 和 reading-paths.md 都说"42 篇已完成，8 篇写作中"，但 PRD 和 src/README.md 都说"50 篇全部完成"。读者在不同页面看到矛盾的数字会失去信任。

**Munger 会说**："如果一本书连自己有多少篇文章写完都搞不清楚，我怎么相信它的技术内容是准确的？这是最基本的一致性。"

#### M4: 时间线包含未来事件 [MUST-FIX]

**问题**：README.md 的 Mermaid 时间线把"2026-Q4 (12月) : oh-my-openagent 项目创建"标为已发生事件，但当前是 2026 年 6 月。

**Munger 会说**："把还没发生的事写成已经发生了，这不叫乐观，这叫不诚实。读者会想：这书里还有什么是编的？"

**修复**：修正时间线，使用实际的项目创建时间（根据 GitHub 历史，oh-my-openagent 在 2025 年就已存在）。

---

## 四、内容一致性（Review 4）— AGENTS.md 规范检查

### 规范符合性

| 规范项 | 状态 | 说明 |
|--------|------|------|
| 品牌名 "OpenCode"（大写 C） | ✅ PASS | 全部一致 |
| 内部链接格式 `[text](file.md)` | ✅ PASS | 同目录链接正确 |
| 跨目录链接 `[text](../target/file.md)` | ✅ PASS | 格式正确 |
| 章节首页链接 `[text](chapter/)` | ✅ PASS | 使用目录形式 |
| Mermaid 颜色规范 | ✅ PASS | 使用 #4A90D9 / #50C878 / #FF9F43 / #A66CFF |
| Mermaid 方向 TB | ✅ PASS | 全部使用 TB 或 LR |
| 英文术语首次标注 | ✅ PASS | 如 "Agent（智能体）" |
| 跨章节引用格式 `→ [章节名称](路径)` | ✅ PASS | reading-paths.md 末尾使用正确 |

### 发现的不一致

#### C1: README.md 章节导航文章计数 [INFO]

README.md 第 393-396 行列出 3 篇子文章（reading-paths, how-to-read, quick-start），这是正确的（README.md 自身是章节首页）。无问题。

#### C2: how-to-read.md 过时配置示例 [SHOULD-FIX]

how-to-read.md 第 399 行使用 `"model": "claude-3-opus"` 作为配置示例，这是过时的模型名称。

#### C3: PRD/AGENTS.md 版本滞后 [INFO，非 Ch0 范围]

PRD §3.5 声明 OpenCode v1.15.x / OMO v4.5.x，AGENTS.md 声明 mdBook v0.4.x，但实际版本为 v1.16.x / v4.13.x / v0.5.x。Ch0 文章的版本号是正确的。

---

## 五、内容研究写作（Review 5）— 与官方源对比

### 安装命令对比（与 OpenCode 官方 README）

| 安装方式 | 官方 README | quick-start.md | 差异 |
|----------|-------------|---------------|------|
| curl 脚本 | `curl -fsSL https://opencode.ai/install \| bash` | ✅ 有 | — |
| npm | `npm i -g opencode-ai@latest` | ✅ 有（缺 `@latest`） | 次要 |
| Homebrew (推荐) | `brew install anomalyco/tap/opencode` | ❌ 缺失 | **应补充** |
| Homebrew (official) | `brew install opencode` | ❌ 缺失 | 可选 |
| Scoop | `scoop install opencode` | ✅ 有 | — |
| Chocolatey | `choco install opencode` | ✅ 有 | — |
| Arch Linux | `sudo pacman -S opencode` | ❌ 缺失 | 可选 |
| mise | `mise use -g opencode` | ❌ 缺失 | 可选 |
| Desktop App | 有 BETA 桌面版 | ❌ 未提及 | 可选 |

### oh-my-openagent 安装方式对比

| 安装方式 | 官方 README | 文章内容 | 差异 |
|----------|-------------|---------|------|
| `bunx oh-my-openagent install` | ✅ 推荐 | 未在任何 Ch0 文章中提及 | 应补充 |
| 手动配置 | ✅ | 未提及 | 可选 |

### OpenCode 核心特性对比

官方 README 提到的内置 Agent：
- `build`（默认，完全访问）— quick-start.md 中提到的 "Build 模式"
- `plan`（只读，分析和代码探索）— quick-start.md 中提到的 "Plan 模式"
- `@general`（复杂搜索和多步骤任务）— **文章中未提及**

---

## 六、修复清单汇总

### MUST-FIX（必须修复，影响准确性或可信度）

| ID | 文件 | 问题 | 修复方案 |
|----|------|------|---------|
| MF-1 | README.md L390 | 写作状态 "42 篇已完成" 与 PRD "50 篇全部完成" 不一致 | 改为 "50 篇文章全部完成" |
| MF-2 | reading-paths.md L13 | 同上 | 改为 "50 篇文章全部完成" |
| MF-3 | reading-paths.md 多处 | 文章状态标记 "⚠️ 写作中" 应全部为 "✅ 已完成" | 批量替换 |
| MF-4 | README.md L337 | 时间线 "2026-Q4 oh-my-openagent 项目创建" 是未来日期 | 修正为实际创建时间 |
| MF-5 | README.md L327 | Node.js 描述为 "本地预览环境" 不准确 | 改为 "npm 安装方式所需运行时" |
| MF-6 | quick-start.md L15 | Node.js 描述为 "OpenCode 运行环境" 不准确 | 改为 "npm 安装方式所需（curl/brew 安装不需要）" |
| MF-7 | quick-start.md | 缺少 brew 安装方式（官方推荐） | 补充 `brew install anomalyco/tap/opencode` |
| MF-8 | quick-start.md | 安全检查在首次执行之后才出现 | 在步骤三之前添加简要安全提示 |

### SHOULD-FIX（建议修复，提升质量）

| ID | 文件 | 问题 | 修复方案 |
|----|------|------|---------|
| SF-1 | quick-start.md L100 | Provider 配置无示例 | 添加最小可用配置示例 |
| SF-2 | how-to-read.md L399 | 配置示例用 `claude-3-opus` 过时 | 改为 `claude-opus-4-7` |
| SF-3 | quick-start.md L70 | `opencode --version` 预期输出 v1.16.0 | 改为 v1.16.x 或 v1.16.2 |
| SF-4 | quick-start.md | 未提及 `@general` 子 Agent | 在常用操作表中补充 |
| SF-5 | quick-start.md | npm 安装命令缺少 `@latest` | 改为 `npm install -g opencode-ai@latest` |

### INFO（记录但不修改）

| ID | 说明 |
|----|------|
| I-1 | PRD §3.5 版本号滞后（v1.15.x/v4.5.x vs 实际 v1.16.x/v4.13.x），非 Ch0 范围 |
| I-2 | AGENTS.md 声明 mdBook v0.4.x，实际为 v0.5.3 |
| I-3 | wiki/oh-my-openagent-overview.md 中 GitHub URL 用了 `anomalyco/oh-my-openagent`（应为 `code-yeongyu/oh-my-openagent`） |
| I-4 | PRD 声明 OpenCode 167K+ stars，实际为 171k |
| I-5 | "提升 2x+ 效率" 声明缺少数据支撑，需后续补充 |

---

## 七、各轮 Review 总结

| 轮次 | 视角 | 核心发现 | MUST-FIX 数 | SHOULD-FIX 数 |
|------|------|---------|-------------|--------------|
| R1 | 数据准确性 | 版本号正确，写作状态不一致，时间线含未来日期 | 4 | 1 |
| R2 | Karpathy | Node.js 依赖声明不可验证 | 2 | 0 |
| R3 | Munger | 安全检查位置错误，配置指引模糊 | 2 | 1 |
| R4 | 内容一致性 | 品牌名/链接/颜色全部合规 | 0 | 1 |
| R5 | 内容研究 | 缺少 brew 安装（官方推荐），Provider 配置无示例 | 1 | 2 |
| **合计** | — | — | **8** | **5** |

---

> **审查者**：Sisyphus-Junior（5 轮独立审查）
> **审查日期**：2026-06-06
> **下次审查建议**：PRD 版本号同步更新 + Ch6/Ch7 文章状态确认
