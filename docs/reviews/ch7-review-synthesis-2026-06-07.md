# Ch7 案例研究 — 5 轮质量审查报告

**审查日期**: 2026-06-07
**审查范围**: src/07-case-studies/ (7 个文件)
**审查方法**: 5 轮（数据准确性 → Karpathy 可运行性 → Munger 误导性 → AGENTS.md 合规 → 官方文档交叉引用）

---

## 摘要

| 严重程度 | 数量 | 说明 |
|---------|:----:|------|
| P0 (必须修复) | 3 | 违反 AGENTS.md 规范、版本号错误、技能来源误标 |
| P1 (建议修复) | 5 | OMO 扩展未标注、非标准安全评分、不可证实声明、配置格式疑问 |
| P2 (可改进) | 4 | Mermaid 颜色语义偏离、缺乏可核实来源的统计声明、OMO 归属遗漏 |

---

## 分轮详细发现

### 第 1 轮：数据准确性

#### real-world-01.md（案例一：从零搭建微服务）

| # | 行号 | 严重程度 | 问题 | 建议修复 |
|---|------|---------|------|---------|
| 1.1 | 236, 241 | **P0** | `"source": "built-in"` 对 `backend-architect` 和 `qa-engineer` 不准确。这两个技能不是 OpenCode 内置技能，而是来自用户配置/AgentKit。只有 `customize-opencode`、`playwright`、`review-work` 等极少数是内置的。 | 改为 `"source": "marketplace"` 或移除该字段 |
| 1.2 | 259 | P1 | `"@opencode/mcp-postgres"` 包名无法确认真实存在。OpenCode 生态中 MCP 服务器的 npm 包命名规则不确定。 | 验证实际包名。如不存在，改为通用描述或标注 "示例包名" |
| 1.3 | 199-204 | P2 | ADR-001 日期 2025-06-04，但案例叙事中使用 2024 年数据（其它文件有 RED-2024 编号）。整书时间线不一致。 | 统一为 2025 或 2026 时间线（全书主线为 OpenCode v1.15.x 即 2026） |
| 1.4 | 204 | P2 | "Prisma 的类型安全可减少 30-40% 的运行时错误"——未提供可核实来源。 | 添加引用或降低精确度（改为"显著减少"） |

#### real-world-02.md（案例二：遗留系统现代化）

| # | 行号 | 严重程度 | 问题 | 建议修复 |
|---|------|---------|------|---------|
| 1.5 | 9, 23, 73, 76, 539, 698 | **P1** | `/init-deep`、`@explore`、`@audit`、`@explore --tech-debt` 是 oh-my-openagent (OMO) 扩展命令，不是原生 OpenCode CLI。书中未标注 OMO 扩展。 | 在首次出现处标注"（OMO 扩展）"或添加脚注 |
| 1.6 | 159, 177, 194, 212, 229, 247 | **P1** | `pro-capability-model`、`balanced-model` 是 OMO 的抽象模型类型，不是真实模型名（如 gpt-4o）。未标注 OMO 扩展。 | 标注"（OMO 抽象模型类型）"或改为真实模型名 |
| 1.7 | 150-263 | P1 | `security-research` 团队配置结构（role、permissions 中的 edit/bash/team_send_message）可能不是 OpenCode `teams` 配置的标准格式。这可能是 OMO 团队模式的自定义格式。 | 标注为"OMO Team Mode 配置格式"或参照 OpenCode 标准团队配置重写 |

#### case-security-audit.md（案例：安全审计流水线）

| # | 行号 | 严重程度 | 问题 | 建议修复 |
|---|------|---------|------|---------|
| 1.8 | 6 | **P1** | 提到"OpenCode 的 `security-research` 团队"，但 `security-research` 实际上是 OMO 提供的团队模式技能，不是 OpenCode 原生团队。 | 改为"oh-my-openagent (OMO) 的 `security-research` 团队" |
| 1.9 | 169 | P2 | 报告编号 `RED-2024-03-21-001` 使用 2024 年，与整书主线（2026，OpenCode v1.15.x）不一致。 | 统一为 2025 或 2026 |
| 1.10 | 611-635 | P2 | GitHub Actions 配置中 `${{ env.TARGET_URL }}` 使用了 `env` context，但未在 workflow 中定义该环境变量。 | 添加 `env.TARGET_URL` 定义或标注为占位符 |

#### case-full-pipeline.md（案例：全流程自动化）

| # | 行号 | 严重程度 | 问题 | 建议修复 |
|---|------|---------|------|---------|
| 1.11 | 11 | **P0** | 使用 "→ Article 7.5" 引用格式。违反 AGENTS.md §5：全书不用 `§X.Y` 编号，直接用章节名称。链接文字必须和目标文件的 H1 标题一致。 | 改为 `→ [案例：国产模型混合架构](case-multi-model.md)` |
| 1.12 | 557 | P2 | "Claude 3 Opus" 和 "Claude 3 Haiku" —— Claude 3 Opus 于 2024 年发布，到 2026 年可能已被更新型号（如 Claude 4）取代。 | 使用当前版本号或泛化描述 |

#### case-multi-model.md（案例：国产模型混合架构）

| # | 行号 | 严重程度 | 问题 | 建议修复 |
|---|------|---------|------|---------|
| 1.13 | 124-194 | **P1** | Category 路由配置中的 `priority`、`weight`、`routing` 段（`strategy`/`default_model`/`fallback_enabled`）和 `testing` 分类的 `weight` 字段——这些是 OpenCode 实际配置格式吗？标准配置格式中 categories 不支持这些字段。 | 确认实际配置格式；如非标准则标注"概念设计" |
| 1.14 | 216-250 | P1 | `failover` 配置中的 `circuit_breaker`（`failure_threshold`/`reset_timeout_ms`）可能不是 OpenCode 原生支持。 | 确认实际配置支持情况 |
| 1.15 | 39 | P2 | "张一鸣视角的判断"——虽然是视角模拟，但未标注非真实引用。可能被读者误认为是张一鸣的原话。 | 添加"（视角模拟）"标注 |

#### case-skills-marketplace.md（案例：团队级 Skill 市场）

| # | 行号 | 严重程度 | 问题 | 建议修复 |
|---|------|---------|------|---------|
| 1.16 | 115 | **P0** | `compatibility: ">= 3.0.0"` 标注为 OpenCode 版本兼容性。OpenCode 当前版本为 v1.15.x，`>= 3.0.0` 错误。 | 改为 `>= 1.0.0` 或 `>= 1.15.0` |

---

### 第 2 轮：Karpathy 视角（代码/配置可运行性）

| # | 文件 | 行号 | 严重程度 | 问题 | 建议 |
|---|------|------|---------|------|------|
| 2.1 | real-world-01.md | 251 | P1 | `"aggregator": "oracle"` 在 teams 配置中——OpenCode 的 team 配置是否支持 `aggregator` 字段？这可能不是可运行配置。 | 确认实际配置结构 |
| 2.2 | real-world-01.md | 259 | P1 | `"command": "npx", "args": ["@opencode/mcp-postgres", ...]` ——`@opencode/mcp-postgres` 包未在 npm 确认存在。 | 验证替换为真实包名 |
| 2.3 | real-world-02.md | 150-263 | P1 | security-research 团队配置中 `"permissions": { "edit": "deny", "bash": "allow", "team_send_message": "allow" }` 不是标准 OpenCode 权限格式。标准格式是 `permissions: [{ "path": "...", "allow": [...] }]`。 | 改用 OpenCode 标准权限格式或标注 OMO 专有 |
| 2.4 | real-world-02.md | 556-570 | P1 | 7-Agent Pipeline 配置中 `"parallel": 3` 在 steps 里——OpenCode workflow 配置不支持这种结构。不符合可运行标准。 | 标注"概念设计——非实际配置格式" |
| 2.5 | case-full-pipeline.md | 68-101 | P2 | JSON 格式的用户故事——示例数据有效，但缺少 JSON Schema 校验的实际配置示例。 | 可补充 JSON Schema 示例 |
| 2.6 | case-multi-model.md | 124-194 | P1 | `"provider"` 和 `"categories"` 顶层配置混合——OpenCode 的标准配置中 provider 和 categories 在不同的配置段。`categories` 的 `priority`/`weight` 字段不可运行。 | 按标准配置格式修改或标注"扩展设计" |
| 2.7 | case-skills-marketplace.md | 180-187 | P2 | `opencode skill validate` 和 `opencode skill publish` 已正确标注为"前瞻性设计"。 | 保持当前标注 ✅ |

---

### 第 3 轮：Munger 视角（误导性声明/矛盾/不切实际建议）

| # | 文件 | 行号 | 严重程度 | 问题 | 建议 |
|---|------|------|---------|------|------|
| 3.1 | real-world-01.md | 691 | **P1** | "交付后 Bug 数 0 个"——零 bug 交付是一个极强声明，在现实项目中几乎不可能。案例虽是虚构，但"实测"表述（"实测：运行 2 周"）会让读者认为是真实数据。 | 改为"交付后两周内零线上 Bug 上报"或直接说明为虚构案例数据 |
| 3.2 | real-world-01.md | 204 | P2 | "Prisma 的类型安全可减少 30-40% 的运行时错误"——精确的百分比数字暗示有严谨测量，但无来源。 | 加引用或改为范围更大的表述 |
| 3.3 | real-world-01.md | 314 | P2 | "低 temperature 在代码生成场景中可减少 50%+ 的无意义变量名变化"——精确百分比但无来源。 | 加引用或弱化表述 |
| 3.4 | real-world-02.md | 19 | P2 | "丢失了原系统 80% 的经验积累"——引用自《Working Effectively with Legacy Code》，但该数字可能是估算而非书中的确切数据。 | 核实引用，或改为"大部分经验积累" |
| 3.5 | real-world-02.md | 754 | **P1** | "安全评分从 'D' 级别提升到 'A' 级别"——安全评分没有标准化的 A-F 字母等级体系（CVSS 使用数字评分，OWASP 使用不同评级）。这种表述可能让专业读者困惑。 | 改为"Critical/High 漏洞清除"等可衡量表述 |
| 3.6 | case-multi-model.md | 80 | P2 | "DeepSeek 在安全审计任务上的漏报率高出约 22%（基于内部 50 次对比测试）"——未提供测试方法、样本和数据。 | 补充方法论说明或降低精确度 |
| 3.7 | case-multi-model.md | 85 | P2 | "对 100 条中文技术文案的润色任务，DeepSeek 的接受率 91%，GPT-4o 接受率 82%"——精确对比数据但无来源。 | 补充测试说明或改为定性描述 |
| 3.8 | case-skills-marketplace.md | 468 | P2 | 效果指标数据（6 个月数据，精确百分比）来自"某团队"——虚构案例但表述为真实数据。 | 明确标注为"基于虚构案例的示意数据" |

---

### 第 4 轮：AGENTS.md 合规性

| # | 文件 | 行号 | 严重程度 | 违反规则 | 建议 |
|---|------|------|---------|---------|------|
| 4.1 | case-full-pipeline.md | 11 | **P0** | §5 跨章节引用：使用 "→ Article 7.5" 而非 `→ [章节名称](相对路径.md)`。AGENTS.md 明确要求"全书不用 `§X.Y` 编号，直接用章节名称"。 | 改为 `→ [案例：国产模型混合架构](case-multi-model.md)` |
| 4.2 | case-multi-model.md | 362-395 | **P2** | §7 Mermaid 颜色规范：信任边界图中 DeepSeek/Qwen 使用 #FF9F43（橙色/Workflow 色），GPT-4o/Claude 使用 #4A90D9（蓝色/Agent 色），日志审计使用 #50C878（绿色/Skill 色）。这些是信任层级颜色而非按照 AGENTS.md 语义。 | 如果要遵循规范，按语义重新配色；或说明该图使用信任层语义而非组件语义配色 |
| 4.3 | 多处 | — | P2 | §6 英文术语首次出现格式：部分英文术语（如 "Feature Flag"、"PR"、"ADR"）未在首次出现时标注中文翻译。AGENTS.md 要求用 **English（中文翻译）** 格式。 | 在首次出现的关键术语处添加中文翻译 |

关于 §4 品牌名检查（全书统一 **OpenCode** 大写 C）：
- 所有 7 个文件中 "OpenCode" 大小写使用正确 ✅
- CLI 命令调用 `opencode` 小写是正确用法（作为命令名）✅

关于 §2 内部链接检查：
- 所有跨目录链接使用 `../` 前缀 ✅
- 所有章节首页链接使用目录形式（`../04-workflows/` 而非 `../04-workflows/README.md`）✅
- 所有链接文字与目标 H1 一致（已验证 `real-world-01/02` 间交叉链接、`case-*.md` 间链接、指向其他章节的链接）✅

关于 §3 代码块格式：
- 绝大多数代码块使用 `language:相对路径` 格式 ✅
- 部分内联 JSON 示例（非文件）使用 `json` 无路径，可以接受 ✅
- 代码块格式一致性良好 ✅

---

### 第 5 轮：官方文档交叉引用

| # | 文件 | 行号 | 严重程度 | 问题 | 建议 |
|---|------|------|---------|------|------|
| 5.1 | real-world-01.md | 236, 241 | **P0** | `backend-architect` 和 `qa-engineer` 标记为 `"source": "built-in"`。对照 OpenCode 官方文档，这些技能不在内置技能列表中。 | 改为 `"source": "marketplace"` 或移除 |
| 5.2 | real-world-02.md | 9, 23, 73 | P1 | `/init-deep` 不是原生 OpenCode 命令。OpenCode 原生只有 `/init`。`/init-deep` 是 OMO 扩展。 | 标注"（oh-my-openagent v4.5+ 扩展）" |
| 5.3 | real-world-02.md | 76 | P1 | `@explore` 不是原生 OpenCode CLI 命令格式。OpenCode 使用 `/` 前缀命令（如 `/init`），`@` 前缀是 OMO 的模式。 | 标注"（OMO 扩展）" |
| 5.4 | case-security-audit.md | 6, 483-517 | P1 | `security-research` 团队配置和 workflow 描述——security-research 是 OMO 技能，不是原生 OpenCode 团队。 | 在首次出现时标注"OMO 技能" |
| 5.5 | case-full-pipeline.md | 557 | P2 | "Claude 3 Opus" 和 "Claude 3 Haiku" 模型名——到 2026 年，Anthropic 已发布 Claude 4 系列，使用旧型号名可能让读者怀疑时效性。 | 更新为当前型号或泛化 |
| 5.6 | case-multi-model.md | 124 | P1 | Category 路由的 `categories` 配置中 `priority` / `weight` 字段不在标准 OpenCode v1.15.x 配置规范中。 | 移除非标准字段或添加扩展标注 |
| 5.7 | case-skills-marketplace.md | 115 | **P0** | `compatibility: ">= 3.0.0"` ——OpenCode 版本号错误，当前为 v1.15.x。 | 改为 `>= 1.0.0` |

---

## P0 修复清单（立即执行）

| # | 文件 | 行号 | 修复内容 |
|---|------|------|---------|
| F1 | case-full-pipeline.md | 11 | 将 "→ Article 7.5" 改为 `→ [案例：国产模型混合架构](case-multi-model.md)` |
| F2 | case-skills-marketplace.md | 115 | 将 `compatibility: ">= 3.0.0"` 改为 `>= 1.0.0` |
| F3 | real-world-01.md | 236, 241 | 将 `"source": "built-in"` 改为 `"source": "marketplace"` |

---

## P0 修复结果

全部 3 项 P0 修复已直接应用到源文件（见下方变更记录）。

---

## 构建验证

`mdbook build` 执行结果：待运行。

---

## 附录：变更记录

| 日期 | 操作 | 文件 |
|------|------|------|
| 2026-06-07 | P0 修复 F1 — 修正跨章节引用格式 | case-full-pipeline.md |
| 2026-06-07 | P0 修复 F2 — 修正 OpenCode 版本兼容性 | case-skills-marketplace.md |
| 2026-06-07 | P0 修复 F3 — 修正技能来源标注 | real-world-01.md |

---

*审查人：Sisyphus-Junior | 审查工具：5 轮方法论（数据准确性 + Karpathy + Munger + AGENTS.md 合规 + 研究验证）*
