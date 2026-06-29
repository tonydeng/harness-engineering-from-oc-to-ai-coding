# Ch5 (Skill 开发) Agent Engineer Role Coverage Review

> **Review Date**: 2026-06-27
> **Scope**: `src/05-skills/` — 5 articles
> **Target**: Agent Engineer (AGENT-ENGINEER) — US-AE-01, US-AE-02, US-AE-03
> **Method**: Per-article scoring (0-3) + gap analysis with file paths

---

## Executive Summary

Ch5 covers the Skill author's perspective comprehensively, but **only partially addresses Agent Engineer concerns**. The chapter excels at Skill creation mechanics (`target_agent`, `allowed-tools`, `category` routing) but has three systematic blind spots:

1. **No explicit connection to AGENTS.md** — Skills and Agent configs are treated as separate worlds
2. **No context engineering lens** — Skills affect context budgets but this is never discussed
3. **Loop engineering is nascent** — Only plugin-patterns.md touches orchestration; no iterative loop patterns

**Overall rating**: 1.3 / 3 across all three stories.

---

## Per-Article Scoring Matrix

| Article | US-AE-01 (Agent config) | US-AE-02 (Context engineering) | US-AE-03 (Loop Engineering) |
|---------|:---:|:---:|:---:|
| 5.1 creating-skills.md | 2/3 | 1/3 | 0/3 |
| 5.2 skill-templates.md | 1/3 | 1/3 | 1/3 |
| 5.3 skill-best-practices.md | 2/3 | 1/3 | 1/3 |
| 5.4 skill-mcp-bridge.md | 1/3 | 1/3 | 0/3 |
| 5.5 plugin-patterns.md | 2/3 | 1/3 | 2/3 |
| **Average** | **1.6/3** | **1.0/3** | **0.8/3** |

---

## US-AE-01: Agent Config — Detailed Gap Analysis

**Coverage score**: 1.6/3

### What Ch5 Does Well

| Article | What exists | Where |
|---------|------------|-------|
| 5.1 | `target_agent` field explanation | `creating-skills.md:109-137` |
| 5.1 | `category` field for classification routing | `creating-skills.md:788-819` |
| 5.1 | Three Skill-Agent association modes (global, category, target_agent) | `creating-skills.md:737-845` |
| 5.3 | Team Mode Skill integration with overrides | `skill-best-practices.md:1087-1259` |
| 5.5 | Skill dependency declaration and interface contracts | `plugin-patterns.md:664-746` |

### Gap Analysis — AGENTS.md Integration Missing

**The fundamental problem**: Ch5 treats Skill-to-Agent association as purely an `opencode.json` / SKILL.md frontmatter configuration mechanism. It never connects this to **AGENTS.md** — the primary artifact the Agent Engineer creates and maintains.

| # | What's missing | Where it should be | Why it matters |
|---|---------------|-------------------|----------------|
| G1 | **Skills should appear in AGENTS.md managed skills list** — AGENTS.md is where an Agent Engineer declares which Skills an Agent should load. Ch5 never explains how to reference Skills from AGENTS.md. | `creating-skills.md` §"Skill 与 Agent 的关联方式" (after line 845) | Agent Engineer needs to know: "If I declare a Skill in AGENTS.md, what's the syntax? What's the loading priority?" |
| G2 | **No AGENTS.md Skill loading syntax** — The article shows `opencode.json` `skills` config but not AGENTS.md `skills` section format. | `creating-skills.md` §"Skill 加载机制" (after line 392) | Reader can configure Skills in JSON but doesn't know how AGENTS.md references them. |
| G3 | **No "AGENTS.md as Skill inventory" guidance** — An Agent Engineer uses AGENTS.md as a team's Skill inventory. Ch5 doesn't explain how to organize, version, or document Skills in AGENTS.md for a team. | `skill-best-practices.md` §"Team Mode 中的 Skill 集成" (after line 1259) | Missing the "configuration management" perspective — how to track Skill versions, document which Skills are active, and manage Skill lifecycle. |
| G4 | **Profile-to-Skill mapping absent** — Skills can vary by environment (dev vs prod) but Ch5 doesn't show how AGENTS.md profiles reference different Skill sets. | `skill-best-practices.md` §"Overrides 的最佳使用场景" (after line 1248) | Overrides are shown as JSON config, not integrated with the Profile concept described in Ch3. |
| G5 | **No Skill version pinning in AGENTS.md** — Agent Engineers need to pin Skill versions for reproducibility. Ch5 mentions SemVer for SKILL.md but not how AGENTS.md references specific versions. | `plugin-patterns.md` §"版本管理" (after line 604) | Missing the "lockfile" pattern — how a team ensures all members use the same Skill versions. |

### Recommended Fixes for US-AE-01

| # | Fix | Target article | Suggested location | Complexity |
|---|-----|---------------|-------------------|------------|
| F1 | Add section "在 AGENTS.md 中声明 Skill" showing AGENTS.md syntax for Skill loading | `creating-skills.md` | After existing §"三种关联方式" comparison table (line 845) | Low — 1 paragraph + 1 code block |
| F2 | Add subsection "AGENTS.md 作为 Skill 清单" explaining how to organize Skills in AGENTS.md | `skill-best-practices.md` | After §"Team Mode 中的 Skill 集成" (line 1259) | Low — 2-3 paragraphs |
| F3 | Add note connecting `target_agent` and `category` to AGENTS.md agent definitions | `creating-skills.md` | In §"Skill 与 Agent 的关联方式" intro (line 735) | Minimal — 1 sentence per association mode |

---

## US-AE-02: Context Engineering — Detailed Gap Analysis

**Coverage score**: 1.0/3

### What Ch5 Does Well

| Article | What exists | Where |
|---------|------------|-------|
| 5.1 | Progressive disclosure loading (metadata → content → resources) | `creating-skills.md:328-361` |
| 5.1 | Description-based semantic matching (minimal context load) | `creating-skills.md:394-410` |
| 5.3 | Anti-pattern: bundling large files | `skill-best-practices.md:699-726` |

### Gap Analysis — Skill-Level Context Engineering Absent

**The fundamental problem**: Ch5 describes how Skills are loaded but never addresses the **context cost** of Skills — how much context a Skill consumes, how to optimize it, or how multiple loaded Skills share a limited context window.

| # | What's missing | Where it should be | Why it matters |
|---|---------------|-------------------|----------------|
| G6 | **Token/budget awareness for Skills** — No discussion of how many tokens a Skill's content consumes, how to estimate context cost, or how to keep Skills lean for context efficiency. | `creating-skills.md` §"正文结构设计" (after line 221) | Agent Engineer must budget context. A 500-line Skill = thousands of tokens. |
| G7 | **Multi-Skill context budgeting** — When 3+ Skills are loaded simultaneously, how do they share context? No guidance on total Skill context budget. | `skill-best-practices.md` §"Skill 设计 6 条核心原则" (after line 40) or `plugin-patterns.md` §"组合 Skill 的三种协作模式" (after line 208) | Complex tasks load multiple Skills — context pressure increases non-linearly. |
| G8 | **Skill output as context input** — Skills produce outputs that become context for downstream steps. No guidance on how to structure Skill outputs for optimal context reuse. | `plugin-patterns.md` §"接口契约标准化" (before line 716) | Pipeline/Skill-chain patterns pass outputs as inputs — output format directly affects context quality. |
| G9 | **Context compression for Skill-embedded MCP** — MCP tools called from Skills produce large outputs. No discussion of output truncation, filtering, or compression. | `skill-mcp-bridge.md` §"最佳实践与反模式" (after line 623) | MCP results (e.g., web search, database query) can fill context window rapidly. |
| G10 | **Context refreshes between Skill invocations** — Long-running Skills accumulate context. No discussion of when to reset/refresh context between Skill stages. | `plugin-patterns.md` §"编排模式" (after line 308) | Pipeline patterns risk context degradation after 3+ stages. |

### Recommended Fixes for US-AE-02

| # | Fix | Target article | Suggested location | Complexity |
|---|-----|---------------|-------------------|------------|
| F4 | Add "Skill 的上下文成本" subsection noting token consumption patterns | `creating-skills.md` | In §"正文结构设计" after the best practices table (line 221) | Low — 1 paragraph |
| F5 | Add "多 Skill 上下文预算" guidance to the composability section | `skill-best-practices.md` | In §"原则 2：可组合" (after line 113) | Low — 1-2 paragraphs |
| F6 | Add context management note to the pipeline sections | `plugin-patterns.md` | In both §"编排模式" and §"管道模式" | Minimal — one sentence per pattern |

---

## US-AE-03: Loop Engineering — Detailed Gap Analysis

**Coverage score**: 0.8/3

### What Ch5 Does Well

| Article | What exists | Where |
|---------|------------|-------|
| 5.5 | Orchestration pattern (main Skill schedules sub-Skills) | `plugin-patterns.md:210-308` |
| 5.5 | Pipeline pattern (Skills chained with input/output passing) | `plugin-patterns.md:312-426` |
| 5.5 | Quality gate configurations (stop conditions between stages) | `plugin-patterns.md:272-309` |
| 5.5 | Error handling and rollback for multi-step workflows | `plugin-patterns.md:293-299` |
| 5.2 | Template combination patterns (pipeline mode, parallel mode) | `skill-templates.md:1600-1631` |
| 5.3 | Composability principle (Skills chainable into workflows) | `skill-best-practices.md:87-113` |

### Gap Analysis — Loop Engineering Patterns Missing

**The fundamental problem**: Ch5 patterns are linear (chain/pipeline/orchestration) but don't cover **iterative loops** — Skills designed to repeat, refine, or iterate until a condition is met. The Agent Engineer's L4 (Loop Engineering) concerns are not addressed.

| # | What's missing | Where it should be | Why it matters |
|---|---------------|-------------------|----------------|
| G11 | **Generator-Evaluator pattern for Skills** — No Skill pattern where one Skill generates output and another evaluates/validates it in a loop. | `skill-templates.md` §"模板设计理念" (after line 78) or `plugin-patterns.md` §"编排模式" (after line 308) | The most powerful loop engineering pattern is completely absent. |
| G12 | **Iterative refinement loops** — No Skill pattern for "do → review → improve → re-review" cycles. A core loop engineering need. | `skill-templates.md` as a new template variant, or `plugin-patterns.md` §"组合 Skill 的模式" section | Real-world AI coding requires refinement loops (code → review → fix → re-review). |
| G13 | **Stop conditions for Skill loops** — No discussion of max iterations, quality thresholds, timeout, or token budget limits for looping Skills. | `plugin-patterns.md` §"编排模式" error handling section (after line 299) | Without stop conditions, loops become infinite token drains. |
| G14 | **Loop monitoring/debugging** — No guidance on how to detect when a Skill enters an infinite loop, excessive iterations, or quality degradation over repeated passes. | `skill-best-practices.md` §"8 步调试清单" (after line 978) | Agent Engineers need diagnostics for runaway loops. |
| G15 | **Skills designed with explicit phase transitions** — Loop engineering requires "phases" (scout → act → verify) but Ch5 Skills are flat workflows without phase-aware design. | `creating-skills.md` §"正文结构设计" (after line 221) | Skills need to be designed with awareness of where they fit in a loop, not just as one-shot instructions. |

### Recommended Fixes for US-AE-03

| # | Fix | Target article | Suggested location | Complexity |
|---|-----|---------------|-------------------|------------|
| F7 | Add "Generator-Evaluator 模式" as a new composition pattern alongside the existing three | `plugin-patterns.md` | After §"三种协作模式对比" table (line 526) | Medium — new subsection with diagram + example |
| F8 | Add iteration/refinement as a new use case for template combination | `skill-templates.md` | After §"组合模式" (line 1631) | Low — 1 paragraph + 1 diagram |
| F9 | Add "停止条件设计" guidance for Skills used in loops | `skill-best-practices.md` | In §"原则 2：可组合" or new §"原则 7" | Low — 2-3 paragraphs |
| F10 | Extend 8-step debug checklist with loop-specific troubleshooting items | `skill-best-practices.md` | In §"调试清单汇总" (after line 978) | Low — 2-3 new checklist items |

---

## Summary of All Gaps

| Gap ID | Story | Severity | File | What's Missing |
|--------|-------|----------|------|----------------|
| G1 | US-AE-01 | High | `creating-skills.md` | AGENTS.md Skill loading syntax |
| G2 | US-AE-01 | High | `creating-skills.md` | AGENTS.md `skills` section format |
| G3 | US-AE-01 | Medium | `skill-best-practices.md` | AGENTS.md as Skill inventory guidance |
| G4 | US-AE-01 | Medium | `skill-best-practices.md` | Profile-to-Skill mapping across environments |
| G5 | US-AE-01 | Low | `plugin-patterns.md` | Skill version pinning in AGENTS.md |
| G6 | US-AE-02 | High | `creating-skills.md` | Token budget awareness for Skill content |
| G7 | US-AE-02 | High | `skill-best-practices.md` / `plugin-patterns.md` | Multi-Skill context budgeting |
| G8 | US-AE-02 | Medium | `plugin-patterns.md` | Skill output as context input optimization |
| G9 | US-AE-02 | Medium | `skill-mcp-bridge.md` | Context compression for MCP outputs |
| G10 | US-AE-02 | Low | `plugin-patterns.md` | Context refreshes between Skill stages |
| G11 | US-AE-03 | High | `plugin-patterns.md` | Generator-Evaluator pattern for Skills |
| G12 | US-AE-03 | High | `skill-templates.md` / `plugin-patterns.md` | Iterative refinement loops |
| G13 | US-AE-03 | High | `plugin-patterns.md` | Stop conditions for Skill loops |
| G14 | US-AE-03 | Medium | `skill-best-practices.md` | Loop monitoring/debugging |
| G15 | US-AE-03 | Medium | `creating-skills.md` | Phase-aware Skill design for loop integration |

### Severity Distribution
- **High** (7): G1, G2, G6, G7, G11, G12, G13 — Blocking for Agent Engineer use
- **Medium** (6): G3, G4, G8, G9, G14, G15 — Important but not blocking
- **Low** (2): G5, G10 — Nice-to-have

---

## Cross-Reference: Traceability Matrix Status

The existing traceability matrix (`docs/planning/requirements/traceability-matrix.md`) correctly marks **all three US-AE stories as "部分" (partial)** for Ch5:

| Story | Matrix Status | Our finding | Alignment |
|-------|--------------|-------------|-----------|
| US-AE-01 | 部分 (Ch2/Ch3 coverage noted, not Ch5) | 1.6/3 — misses AGENTS.md linkage | ✅ Aligned |
| US-AE-02 | 部分 (not mapped to Ch5 in matrix) | 1.0/3 — context engineering absent | ✅ Aligned |
| US-AE-03 | 部分 (not mapped to Ch5 in matrix) | 0.8/3 — only plugin-patterns touches it | ✅ Aligned |

**Key observation**: The traceability matrix only maps US-AE-01/02/03 to Ch2, Ch3, Ch4, Ch6 — not to Ch5 at all. Our review confirms that **Ch5 currently contributes very little to Agent Engineer coverage**, which is consistent with the matrix but highlights an opportunity: Ch5 could meaningfully contribute to all three stories with targeted additions.

---

## Appendix: Article-by-Article Score Justification

### 5.1 creating-skills.md
| Story | Score | Rationale |
|-------|:-----:|-----------|
| US-AE-01 | 2/3 | Covers target_agent/category/global association thoroughly, shows opencode.json config for category routing. Misses AGENTS.md connection. |
| US-AE-02 | 1/3 | Progressive disclosure loading is context-relevant. No token budget discussion, no context cost awareness. |
| US-AE-03 | 0/3 | No loop engineering content at all. Skills presented as one-shot instructions. |

### 5.2 skill-templates.md
| Story | Score | Rationale |
|-------|:-----:|-----------|
| US-AE-01 | 1/3 | Templates show allowed-tools and target_agent configs concretely, but no AGENTS.md integration. |
| US-AE-02 | 1/3 | Standardized output formats help context consistency. Selection decision tree reduces unnecessary loading. No explicit context budget. |
| US-AE-03 | 1/3 | Composition patterns (pipeline/parallel) are prerequisites for loop engineering. But no actual loops. |

### 5.3 skill-best-practices.md
| Story | Score | Rationale |
|-------|:-----:|-----------|
| US-AE-01 | 2/3 | Strong Team Mode integration, overrides, scope isolation. Still no AGENTS.md reference. |
| US-AE-02 | 1/3 | Anti-pattern on large resources is context-relevant. Single responsibility helps. No explicit context engineering. |
| US-AE-03 | 1/3 | Composability principle supports loop engineering. 8-step debug could be extended for loops. |

### 5.4 skill-mcp-bridge.md
| Story | Score | Rationale |
|-------|:-----:|-----------|
| US-AE-01 | 1/3 | Covers MCP dependency declaration and permission boundaries. No AGENTS.md integration. |
| US-AE-02 | 1/3 | Graceful degradation strategy touches resource management. No context budget for MCP outputs. |
| US-AE-03 | 0/3 | Bridge is about external tool integration, not loops or iteration patterns. |

### 5.5 plugin-patterns.md
| Story | Score | Rationale |
|-------|:-----:|-----------|
| US-AE-01 | 2/3 | Strong on Skill composition, dependency management, interface contracts. Still no AGENTS.md linkage. |
| US-AE-02 | 1/3 | Pipeline input/output standardization implicitly helps context flow. No explicit context budget. |
| US-AE-03 | 2/3 | Best article for loop engineering — orchestration and pipeline patterns, quality gates, error handling. Missing generator-evaluator, iterative refinement, and explicit stop conditions. |
