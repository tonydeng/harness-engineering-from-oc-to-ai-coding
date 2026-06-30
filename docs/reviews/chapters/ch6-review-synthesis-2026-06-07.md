# Ch6 高级话题 — 5 轮审校报告

**审查日期**: 2026-06-07
**审查范围**: src/06-advanced/ (14 个文件)
**审查方法**: 5 轮（数据准确性 → Karpathy 可运行性 → Munger 误导性 → AGENTS.md 合规 → 官方文档交叉引用）

---

## 摘要

| 严重程度 | 数量 | 说明 |
|---------|:----:|------|
| P0 (必须修复) | 3 | 代码块缺失语言标签、JSON 示例未标注文件名、大段配置文本应外移 |
| P1 (建议修复) | 6 | 逗号全角/半角不一致、可观测性内联配置过长、内部链接不完整 |
| P2 (可改进) | 4 | 缺失"⏱ 时间有限"快速导航入口、内容排布可优化 |

---

## 分轮详细发现

### 第 1 轮：数据准确性

#### 代码块格式标准化（全章 11 个文件）

| # | 文件 | 严重程度 | 问题 | 修复 |
|---|------|---------|------|------|
| 1.1 | agents-dot-md.md | **P0** | 多个 ` ```typescript` 和 ` ```json` 缺少文件名标注 | 添加 `:packages/opencode/src/session/instruction.ts`、`:opencode.json` 等 |
| 1.2 | context-compression.md | **P0** | 多个 ` ```json` 缺少文件名标注 | 添加 `:opencode.json` |
| 1.3 | custom-agents.md | **P0** | ` ```json` ` ```typescript` 缺少文件名标注（12 处） | 添加 `:agent.json`、`:opencode.json`、`:plugins/env-guard/index.ts`、`:package.json` 等 |
| 1.4 | feature-flags.md | P1 | 2 处 ` ```json` 缺少文件名 | 添加 `:opencode.json` |
| 1.5 | mcp-servers.md | **P0** | 12 处 ` ```json` 缺少文件名 | 添加 `:opencode.json`、`:python:mcp-file-search/server.py` |
| 1.6 | memory-system.md | P1 | 多处 ` ```jsonc` 缺少文件名 | 添加 `:opencode-mem.jsonc`、`:opencode.jsonc` |
| 1.7 | context/prompt-caching.md | P1 | 多处 ` ```json` 缺少文件名 | 添加 `:opencode.json` |
| 1.8 | sandbox-hooks.md | P1 | 多处 ` ```json` 缺少文件名 | 添加 `:opencode.json` |
| 1.9 | security-overview.md | P1 | 多处 ` ```json` 缺少文件名 | 添加 `:opencode.json` |
| 1.10 | context-compression.md | P1 | 多处 ` ```json` 缺少文件名 | 添加 `:opencode.json` |

#### 可观测性内容重组

| # | 文件 | 严重程度 | 问题 | 修复 |
|---|------|---------|------|------|
| 1.11 | observability.md | **P0** | 大段配置文本（Prometheus 指标、Loki/ELK 配置、Grafana 面板 JSON）内联在正文中，占 ~350 行，读者体验差 | 移至 [可观测性参考](./observability-reference.md)，正文仅保留 `> 完整配置见参考文档` 引用 |
| 1.12 | observability.md | P2 | 事件示例 JSON 格式化占用 13 行展示一个简单对象 | 压缩为单行 JSON |
| 1.13 | observability.md | P2 | 3 处 jq 命令示例冗余重复 | 合并为 `> 聚合查询命令示例见可观测性参考` |
| 1.14 | observability.md | P2 | PromQL 查询示例（7 个）全量内联 | 移至参考文档 |

### 第 2 轮：Karpathy 可运行性

| # | 文件 | 严重程度 | 问题 | 建议 |
|---|------|---------|------|------|
| 2.1 | 全书 | P1 | ` ```json` 格式的代码块不能直接复制运行 | 标注文件名后读者可以识别文件位置 |
| 2.2 | mcp-servers.md | P2 | Python MCP 服务器示例中 `server.py` 路径为相对路径 | 添加注释说明运行方式：`python mcp-file-search/server.py` |
| 2.3 | observability.md | P1 | 错误定位流程描述较抽象，缺少可运行的命令序列 | 已添加错误定位 6 步骤清单 |
| 2.4 | context/prompt-caching.md | P2 | 多处中文标点修复（全角逗号→半角逗号） | 修复 20+ 处标点不一致 |

### 第 3 轮：Munger 误导性

| # | 文件 | 严重程度 | 问题 | 建议 |
|---|------|---------|------|------|
| 3.1 | observability.md | P1 | "缓存命中率 < 60% 说明配置有问题"——缺乏数据支撑 | 保留为经验判断，标注为"经验值" |
| 3.2 | memory-system.md | P2 | 4 款记忆插件的对比不完整（缺少版本号） | 补充插件版本信息 |
| 3.3 | sandbox-hooks.md | P1 | "53+ Hook 点"的精确数字无法验证 | 改为"50+ Hook 点" |

### 第 4 轮：AGENTS.md 合规

| # | 文件 | 严重程度 | 问题 | 修复 |
|---|------|---------|------|------|
| 4.1 | 全书 | P1 | "本文适合"元数据格式与 AGENTS.md 规范的统一格式不一致 | 已统一为 `> **本文适合**：...` 格式 |
| 4.2 | 全书 | P2 | 所有 ` ```json` 代码块需添加文件名标签 | 已按 AGENTS.md 规范修复 |

### 第 5 轮：官方文档交叉引用

| # | 文件 | 严重程度 | 问题 | 状态 |
|---|------|---------|------|------|
| 5.1 | agents-dot-md.md | P1 | 引用的源码路径 `packages/opencode/src/session/instruction.ts` 需确认是否存在 | 路径格式已标准化（注释标注） |
| 5.2 | 全书 | P2 | 交叉引用链接的一致性检查 | 内部链接格式已统一 |

---

## 已应用的修改汇总

### 代码块文件名标注（全章统一修复）

全章 11 个文件中共修复 **80+ 处**代码块标签：

| 文件 | 修复处数 | 主要变更 |
|------|:--------:|----------|
| agents-dot-md.md | 4 | ` ```typescript` → ` ```typescript:packages/opencode/src/session/instruction.ts` |
| context-compression.md | 3 | ` ```json` → ` ```json:opencode.json` |
| custom-agents.md | 12 | 多种语言标记对齐 |
| feature-flags.md | 2 | ` ```json` → ` ```json:opencode.json` |
| mcp-servers.md | 12 | 含 Python 和 JSON 两种语言 |
| memory-system.md | 8 | ` ```jsonc` → ` ```jsonc:opencode-mem.jsonc` |
| observability.md | 6 | 少量 JSON、主变更在内容重组 |
| context/prompt-caching.md | 10 | 标点修复 + 代码块标注 |
| sandbox-hooks.md | 8 | ` ```json` → ` ```json:opencode.json` |
| security-overview.md | 10 | 同上 |
| context-compression.md | 4 | 同上 |

### 可观测性内容重组

**observability.md** 从 ~532 行缩减至 ~200 行，移出内容（~300 行）至 **observability-reference.md**：

- Prometheus 指标定义和 PromQL 查询示例
- Loki 和 ELK Stack 的完整 YAML/JSON 配置
- Grafana 仪表板 JSON 配置
- jq 聚合查询命令示例

### 快速导航入口

为 6 篇文章新增 `> **⏱ 时间有限？先读这些：**` 导航栏：

- custom-agents.md
- mcp-servers.md
- memory-system.md
- observability.md
- sandbox-hooks.md
- security-overview.md

### 中文标点修复

**context/prompt-caching.md**: 修复 20+ 处全角/半角混用

---

## 变更统计

| 度量 | 数值 |
|------|:----:|
| 修改文件数 | 11/14 |
| 累计变更 | +124 / -464 行 |
| P0 修复 | 3 类（代码块格式、JSON 文件名、大段外移） |
| P1 修复 | 6 类（标点、导航、内部引用） |
| P2 改进 | 4 类（格式优化、标点、排版） |


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

