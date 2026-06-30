# Ch4 Full-Book Quality Sprint — 综合审校报告

> **日期**: 2026-06-06
> **范围**: 第4章（工作流实战）全部6篇文章
> **方法**: 每篇5轮审校（数据准确性 → Karpathy工程视角 → Munger逆向验证 → TechLead内容质量 → 整合）
> **前置状态**: Ch0-Ch3 已完成（21篇），Ch4 6篇 all full content

---

## 总体统计

| 文章 | 行数 | 发现总数 | 严重 | 高 | 中 | 低/信息 |
|------|:----:|:--------:|:----:|:-:|:-:|:-------:|
| ultrawork-mode.md | 633 | 18 | 4 | 6 | 6 | 2 |
| prometheus-mode.md | 374 | 14 | 3 | 4 | 4 | 3 |
| multi-agent-collab.md | 1,240 | 13 | 6 | 2 | 3 | 2 |
| custom-workflows.md | 1,246 | 20 | 4 | 5 | 4 | 7 |
| agent-derivation.md | 797 | 15 | 4 | 5 | 0 | 6 |
| teams-collaboration.md | 1,220 | 15 | 4 | 5 | 6 | 0 |
| **合计** | **5,510** | **95** | **25** | **27** | **23** | **20** |

---

## 跨篇章共性发现

### C1 — `task()` API 参数被系统性误述
- **影响**: ultrawork-mode (P1), multi-agent-collab (F1-F4, F8), agent-derivation (C1-C2, C4)
- **问题**: 全书多处将 `task()` API 参数描述为 `category`（取值`subagent/delegate/orchestrator`）、`context.inherit/isolate`、`onFailure`、`timeout`。实际 OpenCode `task()` 的参数只有 `description`、`prompt`、`subagent_type`、`session_id`、`command`。而 `category`/`load_skills` 是 oh-my-opencode `delegate_task` 的概念。
- **修复方向**: 区分 OpenCode core `task()` 和 oh-my-opencode `delegate_task()`，统一参数描述

### C2 — OMO vs OpenCode 边界模糊
- **影响**: 所有6篇文章
- **问题**: 多处将 oh-my-opencode 的配置和行为当作 OpenCode 原生功能描述（如 `default_mode`、`Team Mode`、`load_skills`）。未标注版本号和所属项目。
- **修复方向**: 增加 "OMO vX.Y+" 标注，明确区分 OpenCode core 与 oh-my-opencode 插件

### C3 — 配置项虚构
- **影响**: ultrawork-mode (F1, F5-F8), prometheus-mode (R1-M3), custom-workflows (F3, F8), agent-derivation (C1, M3, M5)
- **问题**: 存在大量不存在的配置键（`stop_condition`, `exploration.max_files`, `verification.lsp_enabled`, `progress_report`, `on_max_turns`, `consensus_threshold`, `veto_power`, `maxDepth`, `context.inherit` 等）
- **修复方向**: 删除所有不存在的配置项，替换为真实 OMO schema

### C4 — 遗漏关键架构组件
- **影响**: prometheus-mode (R1-C2, R1-C3), custom-workflows (F1-F4), agent-derivation (C1-C4)
- **问题**: Prometheus 文章完全遗漏 Metis（强制级）和 Momus（高精度审查循环）。Hyperplan 完全虚构角色名和流程。Agent Derivation 遗漏 `task_budget`/`level_limit` 等真实机制。
- **修复方向**: 补充 Metis/Momus 步骤，重写 Hyperplan 为实际实现

### C5 — 参考来源不可验证
- **影响**: agent-derivation (C3), teams-collaboration (C3)
- **问题**: 《马书》第20章/第20b章引用无法验证，或不存在
- **修复方向**: 删除或替换为可验证引用

---

## 各文章主要问题

### 1. ultrawork-mode.md
| ID | 严重度 | 位置 | 问题 | 修复 |
|----|--------|------|------|------|
| F1 | CRITICAL | L127-148, 331-356 | `default_mode` 配置结构完全虚构 | 替换为真实 OMO v4.3.0+ 扁平 boolean schema |
| F2 | CRITICAL | L165, 312, 337, 362, 514-518 | `max_turns` 不存在，实际为 `max_iterations` | 全部替换 |
| F3 | CRITICAL | L312, 516 | 默认值 10 → 实际 100（ultrawork 500） | 更新默认值和复杂度表 |
| F4 | CRITICAL | L168, 312-327 | `stop_condition` 不存在，实际用 completion promise (`DONE` tag) | 删除，替换为准确描述 |
| F5-F8 | HIGH | L343-355, 314, 341, 315 | `exploration`/`verification`/`progress_report`/`on_max_turns`/`timeout` 不存在 | 删除/替换 |
| E3 | HIGH | N/A | 未记录 honor system 漏洞 (issue #1921) | 增加 Known Limitations 章节 |

### 2. prometheus-mode.md
| ID | 严重度 | 位置 | 问题 | 修复 |
|----|--------|------|------|------|
| R1-C1 | CRITICAL | L27-54 | `@general` 被误述为 Prometheus 命令 | 删除 `@general` 引用 |
| R1-C2 | CRITICAL | L151-168 | 完全遗漏 Metis（强制间隙分析） | 工作流中增加 Metis 步骤 |
| R1-C3 | CRITICAL | L151-168 | 完全遗漏 Momus（高精度审查循环） | 增加 Momus 循环 |
| R1-M1 | MAJOR | 全文 | 未提及 `.sisyphus/` 目录 | 增加目录结构章节 |
| R1-M2 | MAJOR | 全文 | 缺少会话连续性 (boulder.json) | 重写 `/start-work` 含 boulder.json 决策树 |
| R1-M3 | MAJOR | L78 | `max_interview_rounds` 不存在 | 替换为许可检查机制（6条件） |
| R4-M2 | MAJOR | L132-137 | `/start-work` 参数不存在 | 替换为实际行为 |

### 3. multi-agent-collab.md
| ID | 严重度 | 位置 | 问题 | 修复 |
|----|--------|------|------|------|
| F-1 | CRITICAL | L318-333 | `category: "subagent"` 无效值 | 使用真实类别名 |
| F-2 | CRITICAL | L318-333 | 缺少 `run_in_background` | 添加参数 |
| F-3 | CRITICAL | L340-341 | `load_skills` 标注为可选，实际必需 | 更新参数表 |
| F-4 | CRITICAL | L324-328, 362-374 | `context.inherit/isolate` 虚假结构 | 删除/替换为真实权限配置 |
| F-5 | CRITICAL | L516-616 | 管道 DSL 不是真实 OpenCode 格式 | 标注为概念示例或替换为真实格式 |
| F-6 | CRITICAL | L485, 496 | Committer `bash: deny` 但需要 bash 提交 | 重命名或更新权限 |

### 4. custom-workflows.md
| ID | 严重度 | 位置 | 问题 | 修复 |
|----|--------|------|------|------|
| F1 | CRITICAL | L574-727 | Hyperplan 5角色名全错 | 全部替换为真实角色 |
| F2 | CRITICAL | L574-727 | Hyperplan 流程严重简化（7阶段→1轮） | 重写为7阶段3轮辩论 |
| F3 | CRITICAL | L574-727 | `consensus_threshold`, `veto_power` 虚构 | 删除 |
| F4 | CRITICAL | L574-727 | Sisyphus-Junior 协调模型不对 | 替换为真实协调模型 |
| F5 | HIGH | L729-898 | security-research 角色名不同 | 更新为真实角色名 |
| F6 | HIGH | L729-898 | 使用 skill-based routing 而非 category-based | 替换 |
| F7 | HIGH | L75-93, 228-242 | 配置文件路径错误 (`opencode.json`) | 改为 `.opencode/oh-my-openagent.jsonc` |

### 5. agent-derivation.md
| ID | 严重度 | 位置 | 问题 | 修复 |
|----|--------|------|------|------|
| C1 | CRITICAL | L272-367 | `task()` API 参数完全虚构 | 重写为真实 API |
| C2 | CRITICAL | L49-268 | `category` 值不存在 | 改为概念框架+真实 API |
| C3 | CRITICAL | L517-553 | 《马书》引用不可验证 | 删除或替换 |
| C4 | CRITICAL | 全文 | OMO `delegate_task` 误作 OpenCode `task()` | 区分两者 |
| M3 | MAJOR | L474-487 | 递归防御配置名错误 | 替换为 `level_limit`/`task_budget` |

### 6. teams-collaboration.md
| ID | 严重度 | 位置 | 问题 | 修复 |
|----|--------|------|------|------|
| C1 | CRITICAL | L3, 7, 31 | 架构描述为多进程，实际为同进程 | 修正为同进程描述 |
| C2 | CRITICAL | L127-167, 203-236 | Message mechanism 完全虚构 | 替换为 inbox JSONL + session injection |
| C3 | CRITICAL | 全文 | 缺失《马书》第20b章比较 | 增加比较章节 |
| C4 | CRITICAL | L431-461 | 资源隔离用 Linux-only cgroups | 标注或提供 macOS 替代 |
| S1-S5 | SIGNIFICANT | 多处 | 缺死锁分析、ack机制不对、物理嵌套图、消息持久化矛盾、缺 API rate limit | 依次修复 |

---

## 修复策略

采用 **并行修复 + 验证** 策略：

1. **6个 fix agent 并行** — 每篇文章一个 agent，携带完整审查报告作为 prompt
2. **约束**: 只修事实性错误（CRITICAL + HIGH），不做风格重构
3. **验证**: 全部修复后运行 `mdbook build` 确认零错误
4. **保存**: 修复后保存审查文件到 docs/reviews/

> **版本**: v1.0 | **审校者**: Sisyphus | **更新**: 2026-06-06


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

