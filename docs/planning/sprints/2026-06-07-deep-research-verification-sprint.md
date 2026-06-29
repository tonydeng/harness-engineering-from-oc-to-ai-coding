# Deep-Research 外部验证 Sprint ✅ 已完成

> **给代理工作者：** 使用 subagent-driven-development 模式执行此计划。
> **完成日期**：2026-06-07

**目标：** 对所有 8 章 50 篇文章进行 deep-research 外部验证 — 交叉比对 OpenCode GitHub、官方文档、竞品官网，验证所有版本号、配置键、定价和功能声明的准确性。

**架构：** 按章节并行 deep-research → 汇总修改意见 → 应用 P0 修复

**技术栈：** deep-research, librarian (Context7), websearch, content-research-writer

---

## Task 1: Ch1 竞品数据外部验证

**文件：** `src/01-introduction/` (7 个文件)
**重点：** ecosystem-comparison.md, why-opencode.md, chinese-ecosystem.md

- [ ] **1.1** deep-research: 验证所有竞品定价/功能/声明（GitHub Copilot, Cursor, Claude Code, Windsurf 等 vs 2026年6月实际数据）
- [ ] **1.2** librarian: 查 OpenCode GitHub Star 数、SWE-bench 排名等核心数据
- [ ] **1.3** 应用 P0 修复（数据更新、过时声明替换）
- [ ] **1.4** 保存验证报告

## Task 2: Ch3 配置/版本号外部验证

**文件：** `src/03-setup/` (6 个文件)
**重点：** opencode-config.md, chinese-providers.md, multi-env-setup.md

- [ ] **2.1** librarian: 查 OpenCode GitHub opencode.json schema, provider 配置
- [ ] **2.2** deep-research: 验证所有配置项名称、版本号、Provider API Key 名称
- [ ] **2.3** 应用 P0 修复（错误配置键、过时版本号）
- [ ] **2.4** 保存验证报告

## Task 3: Ch6 高级话题外部验证

**文件：** `src/06-advanced/` (14 个文件)
**重点：** mcp-servers.md, security-overview.md, feature-flags.md, memory-system.md

- [ ] **3.1** librarian: 查 OpenCode MCP 配置 schema、安全文档、feature flags 列表
- [ ] **3.2** deep-research: 验证所有功能配置键、安全声明、性能数据
- [ ] **3.3** 应用 P0 修复
- [ ] **3.4** 保存验证报告

## Task 4: Ch4 工作流 + OMO 边界验证

**文件：** `src/04-workflows/` (7 个文件)
**重点：** ultrawork-mode.md, prometheus-mode.md, multi-agent-collab.md

- [ ] **4.1** deep-research: 验证 OMO vs OpenCode 原生功能边界
- [ ] **4.2** librarian: 查 OpenCode 官方工作流文档
- [ ] **4.3** 应用 P0 修复（OMO 标注、虚构建配置移除）
- [ ] **4.4** 保存验证报告

## Task 5: Ch2 + Ch5 + Ch7 综合验证

**文件：** `src/02-core-concepts/` (7) + `src/05-skills/` (6) + `src/07-case-studies/` (7)
**重点：** 外部引用存在性、Skill 配置验证、案例声明核实

- [ ] **5.1** deep-research: 验证 Ch2 中 马书 引用准确性
- [ ] **5.2** librarian: 验证 Ch5 Skill 配置与 OpenCode 实际 Schema
- [ ] **5.3** deep-research: 验证 Ch7 案例中技术声明的真实性
- [ ] **5.4** 应用 P0 修复
- [ ] **5.5** 保存验证报告

## Task 6: Ch0 导航验证

**文件：** `src/00-guide/` (4 个文件)

- [ ] **6.1** 验证所有内部链接和阅读路径引用
- [ ] **6.2** 应用 P0 修复

## Task 7: 全局验证

- [ ] **7.1** 汇总所有验证报告，形成全书修改意见
- [ ] **7.2** Run `mdbook build`
- [ ] **7.3** 交付最终报告
