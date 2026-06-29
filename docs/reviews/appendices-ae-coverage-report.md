# Review Report: Appendices A/B/C/D — Agent Engineer Role Coverage

**Reviewer**: agent-engineer
**Date**: 2026-06-27
**Scope**: Appendix A (Glossary + References), B (OpenCode), C (Claude Code), D (Pi Agent)
**Criteria**: US-AE-01 (Agent Config), US-AE-02 (Context Engineering), US-AE-03 (Loop Engineering)

---

## Executive Summary

The four appendices collectively provide **strong reference coverage** for an Agent Engineer (AE) across all three tools (OpenCode, Claude Code, Pi Agent). The agent-architecture.md articles in Appendix B and C are the most directly relevant, offering comprehensive configuration guides and design pattern catalogs.

**Key strength**: Cross-tool comparison tables throughout all appendices allow AE to compare agent config approaches side-by-side.

**Key gaps**:
1. **Glossary misses several AE-specific terms** (Loop Engineering, Model Routing, Feedback Loop, Generator-Evaluator, March of Nines)
2. **No appendix explicitly discusses context engineering capabilities** — no dedicated section on context compression strategies, token budget management, or context injection patterns within the appendices (these live in Ch6)
3. **Cross-references to Ch6 context content and Ch4 workflow patterns exist but are minimal for AE-specific needs**
4. **No dedicated "best practices for Agent Engineer" section** in any appendix — the content is API/capability reference, not AE methodology guidance

---

## US-AE-01: Agent Config

**Question**: Do appendices cover AGENTS.md/CLAUDE.md patterns? Agent config best practices? Cross-tool comparison?

### Appendix B (OpenCode) — Rating: ⭐⭐⭐ (3/3)

| Article | Relevance | Key AE content |
|---------|-----------|----------------|
| **agent-architecture.md** | **High** | Full Category system reference, 5 design patterns (Simple/Chain/Router/Parallel/Orchestrator), model routing strategy, error handling patterns, test methodology, complete security-reviewer case study with 3 iterations. Covers AGENTS.md sharing of team configs. Covers `tools.allow`/`tools.deny` permission system. |
| **ecosystem.md** | **Medium** | AGENTS.md recommended structure (from `/init`), community config templates (3 listed), quality gate Skill chains, cost management via Category routing. |
| **plugins.md** | **Medium** | Plugin-based agent customization via `definePlugin`, Hook system for runtime behavior modification, but focused on code-level extension not config patterns. |

**Config approach cross-reference to Appendix C/D**: The ecosystem.md and README both contain comparison tables across OpenCode/Claude Code/Pi Agent config approaches.

### Appendix C (Claude Code) — Rating: ⭐⭐⭐ (3/3)

| Article | Relevance | Key AE content |
|---------|-----------|----------------|
| **agent-architecture.md** | **High** | Custom Subagent config (frontmatter: name, model, tools, skills, isolation, memory, mcpServers, hooks), 5 design patterns (Simple/Fork/Pipeline/Hook/Batch), CLAUDE.md writing guide, minimal permission principle. Complete code-reviewer pipeline case study (V1→V2→V3). |
| **extensions.md** | **High** | 6-layer extension architecture, complete `.claude/` directory structure, 12 Hook event types, 4 Hook execution types (command/prompt/agent/http), full frontmatter field reference for Subagents and Skills. |
| **ecosystem.md** | **Medium** | CLAUDE.md template comparison (3 templates by engineering complexity), 6 key practices for CLAUDE.md writing, community templates. |

### Appendix D (Pi Agent) — Rating: ⭐⭐ (2/3)

| Article | Relevance | Key AE content |
|---------|-----------|----------------|
| **overview.md** | **Medium** | Maps Pi to L1-L4 evolution, Extension API overview, comparison table across tools. |
| **customization.md** | **High** | 4-layer extension system (Extensions/Skills/Prompt Templates/Themes), Extension API hook points (16 lifecycle events), Pi Packages distribution, Context Files (AGENTS.md/SYSTEM.md/APPEND_SYSTEM.md). |
| **ecosystem.md** | **Low** | Provider strategy, security model. Migration guides from Claude Code and OpenCode. |

**Cross-tool config comparison**: All three appendices have README comparison tables. Appendix B README has a dedicated 11-dimension comparison table. Ecosystem articles in all three appendices have comparison tables.

### Gap: No "Agent Engineer best practices" section

None of the appendices has a dedicated section on **how an AE should apply these config patterns** in practice. The content is purely reference-oriented. For example:
- When to use Category vs Subagent vs Extension (decision tree) is missing — individual articles cover each but no integrated guide
- No guidance on AGENTS.md structure design principles (progressive disclosure, minimal constraint, etc.) — these live in Ch6 `agents-dot-md.md`
- No template library for common AE scenarios (security audit agent, CI gate agent, etc.)

---

## US-AE-02: Context Engineering

**Question**: Do any appendices discuss context-related capabilities? Cross-references to Ch6 context content?

### Overall Rating: ⭐ (1/3) — Weakest coverage across all three stories

| Appendix | Context Engineering Coverage | Ch6 Cross-references |
|----------|------------------------------|---------------------|
| **App B** | `ecosystem.md` mentions context compression strategies (auto/manual/micro) and Token budget config with a cross-reference. `commands.md` covers `/compact` command. | `ecosystem.md` → `06-advanced/context/compression.md` (1 cross-ref). `agent-architecture.md` → `06-advanced/context-compression.md` (indirect). |
| **App C** | `capabilities.md` mentions `/compact` command. No dedicated context engineering section. | None found. |
| **App D** | `overview.md` explicitly maps to L2 context engineering: compaction engine (`summarizeWithBudget()`), session management (`session.ts`), context compression with unique design (compaction summaries as AgentMessage type). `ecosystem.md` covers session branch management. | Referenced → Harness Engineering theory (Ch1), but no direct cross-refs to Ch6 context articles. |

**Key finding**: Context engineering is **addressed in detail in Ch6** (context-compression.md and its 5 sub-articles in `06-advanced/context/`) but **not replicated or summarized** in any appendix. This is acceptable since appendices are reference material — but cross-references are sparse.

**Missing**: None of the appendices has a dedicated "Context Engineering Reference" section that an AE could use as a quick lookup for:
- Token budget calculation formulas
- Context window sizes by model
- Compression trigger strategies
- Context injection patterns (see Ch6: `context-injection-patterns.md`)

### Table: Context-related content in each appendix

| Context Topic | App A (Glossary) | App B (OpenCode) | App C (Claude Code) | App D (Pi Agent) |
|--------------|-----------------|-----------------|-------------------|-----------------|
| Context Engineering (term) | ✅ (in glossary) | ❌ | ❌ | ✅ (in L2 mapping) |
| Compaction/Compression | ✅ (Compaction in glossary) | ✅ (/compact command, compression strategies in ecosystem.md) | ✅ (/compact command) | ✅ (auto+manual compaction) |
| Token Budget | ✅ (Token Budget in glossary) | ✅ (budget config in ecosystem.md) | ✅ (/cost command) | ❌ |
| Context injection patterns | ❌ | ❌ | ❌ | ❌ |
| Context quality metrics | ❌ | ❌ | ❌ | ❌ |
| Cross-refs to Ch6 context | N/A | 1 (ecosystem → compression) | 0 | 0 |

---

## US-AE-03: Loop Engineering

**Question**: Do any appendices discuss loop/session management capabilities? Cross-references to Ch4 workflow patterns?

### Overall Rating: ⭐⭐ (2/3)

| Appendix | Loop Engineering Coverage | Ch4 Cross-references |
|----------|--------------------------|---------------------|
| **App B** | `agent-architecture.md` covers multi-agent coordination (concurrency limits, resource contention, deadlock prevention, progress monitoring), Team Mode, `runWithConcurrencyLimit()`, `safeCollect()` patterns. `ecosystem.md` has "Loop Engineering Ecology" section covering CI/CD, session compaction, worktree isolation. | `agent-architecture.md` → `04-workflows/multi-agent-collab.md` ✅, `04-workflows/teams-collaboration.md` ✅ |
| **App C** | `ecosystem.md` has "Loop Engineering Ecology" section covering CI/CD, GitHub Actions, SDK usage, Subagent/workflow tools (SuperClaude_Framework, crystal, claudekit), cross-tool MCP wrappers. `agent-architecture.md` covers Fork/Batch patterns. | `agent-architecture.md` → `04-workflows/custom-workflows.md` ✅, `04-workflows/agent-derivation.md` ✅ |
| **App D** | `ecosystem.md` has "Loop Engineering Ecology" section covering SDK/RPC integration (4 modes: SDK/RPC/Print/JSON), Session Tree (Fork/Clone/Tree/Export/Import/Share), context compression (auto/manual/branch summary). `sdk.md` covers programmatic integration with full API reference. | Referenced → Ch1 Harness Engineering theory, no direct Ch4 cross-refs found. |

**Key strength**: All three ecosystem articles now have explicit "Loop Engineering Ecology" sections, reflecting the book's L1-L4 framework.

**Missing**:
- No appendix provides a **loop/session lifecycle reference** that an AE could use as a design pattern catalog for automation loops
- **Generator-Evaluator pattern** (the most impactful loop engineering pattern per AE SKILL) is not covered anywhere in the appendices
- **Stop conditions** (success/timeout/budget/manual) for loops are mentioned in `agent-architecture.md` (App B) implicitly but not formalized as a reference table

---

## Detailed Appendix-by-Appendix Analysis

### Appendix A (Glossary + References)

**Glossary — AE-relevant terms present** (17 of ~32 entries):
- Agent, AGENTS.md, Architecture Guardrails, Build Agent, Context Engineering, Harness Engineering, Harness Engineer, MCP, opencode.json, Permission Model, Plan Agent, Plugin, Provider, Provider Routing, Skill, Subagent, System Prompt, Token, Token Budget, Tool, Validation Harness, Workflow, Constraints System, Quality Gates, Risk Classifier, Background Task, Session Continuation ID

**Glossary — AE-relevant terms MISSING** (8 gaps):

| Missing Term | Why needed for AE | Suggested entry |
|-------------|-------------------|----------------|
| **Loop Engineering / 循环工程** | Core concept in AE SKILL (L4). The third pillar after prompt/context/harness. | "设计和管理AI Agent自主循环的方法论，关注'我不在时工作如何继续'。核心要素：触发条件、停止条件、预算管控、看门狗机制。" |
| **Model Routing / 模型路由** | Critical AE decision: which model for which task. "Category Routing" exists but "Model Routing" is the broader concept. | "根据任务复杂度、延迟要求和成本预算，自动选择最合适的AI模型的路由策略，是驾驭工程的核心实践。" |
| **Feedback Loop / 反馈循环** | Core AE mechanism: validate output, feed back errors, retry. | "Agent输出→验证→反馈→修正的闭环机制，是实现Agent可靠性的核心设计模式。" |
| **Generator-Evaluator Pattern** | AE SKILL calls it "the most impactful architecture decision" | "一种智能体设计模式，将生成器（执行任务的Agent）与评估器（验证输出的Agent）分离，避免自我验证的盲区。" |
| **March of Nines / Nine的征程** | Reliability cost principle: each 9 costs as much as all previous combined | "AI Agent可靠性的成本规律：从90%到99%到99.9%，每个9的提升成本等于之前所有9的总和。" |
| **Category Routing / 分类路由** | Exists as sub-entry under "Category Routing" but as separate term | Already covered ✅ |
| **Skill Agent (Skill Worker)** | How Skills execute — relevant to agent orchestration | Indirectly covered via Skill definition |
| **Worktree Isolation / 工作树隔离** | AE best practice for parallel agent execution, used in all three tools | "在独立的Git工作树中执行Agent任务，防止多个Agent同时修改同一文件导致冲突的隔离机制。" |

**References — AE-relevant gaps**:
- No references to Agent Engineering methodology sources (march of nines, Generator-Evaluator pattern papers)
- No references to AI coding tool benchmarks relevant to AE decision-making (Terminal-Bench, SWE-bench agent-specific evaluations)
- Missing: `code-yeongyu/oh-my-openagent` docs, `earendil-works/pi` docs, etc. (but these are tool docs, not methodology)

---

### Appendix B (OpenCode) — Detailed Gap Analysis

| Article | Lines | US-AE-01 | US-AE-02 | US-AE-03 | Key Gaps |
|---------|-------|----------|----------|----------|----------|
| capabilities.md | 256 | ⭐ | ⭐ | ⭐ | Purely index, no depth |
| commands.md | 414 | ⭐ | ⭐⭐ | ⭐⭐ | Session management commands covered (compact/new/undo) but no loop engineering patterns |
| plugins.md | 1139 | ⭐⭐ | ⭐ | ⭐⭐ | Deep Plugin API ref, Hook system for loop interception. No context engineering hooks. |
| agent-architecture.md | 1049 | ⭐⭐⭐ | ⭐ | ⭐⭐ | **Most relevant for AE**. Missing: explicit Generator-Evaluator pattern, stop condition reference table. |
| sdk.md | ~180 | ⭐ | ⭐ | ⭐⭐ | SDK for CI/CD automation. No context engineering. |
| agent-sdk.md | 1062 | ⭐⭐ | ⭐ | ⭐⭐ | Detailed SDK ref, programmatic Agent control. Missing: context engineering patterns for Session management via SDK. |
| ecosystem.md | 376 | ⭐⭐ | ⭐⭐ | ⭐⭐ | Harness Engineering + Loop Engineering sections. Cross-refs to Ch6 context exist. Missing: direct cross-refs to Ch4 workflow patterns. |

**Summary for App B**: Strongest AE content in `agent-architecture.md` (US-AE-01). Weakest in context engineering (US-AE-02). Loop engineering covered in `ecosystem.md` and `agent-architecture.md` multi-agent coordination section.

---

### Appendix C (Claude Code) — Detailed Gap Analysis

| Article | Lines | US-AE-01 | US-AE-02 | US-AE-03 | Key Gaps |
|---------|-------|----------|----------|----------|----------|
| capabilities.md | 359 | ⭐ | ⭐ | ⭐ | Overview only, covers 6 permission modes (useful for AE) |
| commands.md | ~200 | ⭐ | ⭐ | ⭐⭐ | Covers fork/background/batch commands for loop engineering |
| extensions.md | 704 | ⭐⭐⭐ | ⭐ | ⭐⭐ | **Most relevant for US-AE-01**. Complete 6-layer extension ref. Missing: context engineering. |
| sdk.md | ~150 | ⭐ | ⭐ | ⭐⭐ | Claude Code SDK via `@anthropic-ai/claude-code` |
| agent-sdk.md | ~200 | ⭐ | ⭐ | ⭐⭐ | Agent SDK via `@anthropic-ai/claude-agent-sdk` |
| agent-architecture.md | 743 | ⭐⭐⭐ | ⭐ | ⭐⭐ | 5 design patterns, Subagent config ref. Missing: Generator-Evaluator pattern. |
| ecosystem.md | 409 | ⭐⭐ | ⭐ | ⭐⭐ | Harness + Loop Engineering sections, CLAUDE.md templates. Missing: Ch4 cross-refs. |

**Summary for App C**: Parallel to App B in structure and quality. Agent config coverage is excellent (US-AE-01). Context engineering is absent (no dedicated sections, only `/compact` mention). Loop engineering covered in ecosystem + agent-architecture.

---

### Appendix D (Pi Agent) — Detailed Gap Analysis

| Article | Lines | US-AE-01 | US-AE-02 | US-AE-03 | Key Gaps |
|---------|-------|----------|----------|----------|----------|
| overview.md | 388 | ⭐⭐ | ⭐⭐ | ⭐⭐ | Maps to L1-L4. Context engineering explicitly discussed (compaction, session mgmt). Missing: config pattern decision tree. |
| commands.md | ~150 | ⭐ | ⭐ | ⭐ | Command reference only. |
| customization.md | 658 | ⭐⭐ | ⭐ | ⭐⭐ | 4-layer extension system. 16 lifecycle events. Extension API ref. Missing: context engineering hooks. |
| sdk.md | ~250 | ⭐ | ⭐ | ⭐⭐ | 3 integration modes (Agent Session API, Runtime API, RPC). |
| ecosystem.md | 399 | ⭐ | ⭐⭐ | ⭐⭐⭐ | **Strongest Loop Engineering coverage** of all appendices. SDK/RPC/Print/JSON modes, Session Tree (Fork/Clone/Tree), 3 containerization options. Provider strategy (20+ providers) for model routing. |

**Summary for App D**: Most balanced across all three criteria. Strongest in Loop Engineering (US-AE-03) due to SDK/RPC modes and session branch management. Context engineering (US-AE-02) is discussed but not as a dedicated reference. Agent config (US-AE-01) is covered through extension system but lacks the structured config patterns of App B/C.

---

## Cross-Tool Comparison Tables

### US-AE-01: Agent Config Comparison

| Config Aspect | OpenCode (App B) | Claude Code (App C) | Pi Agent (App D) |
|---------------|------------------|---------------------|------------------|
| Primary config file | AGENTS.md + `oh-my-openagent.jsonc` (categories) | CLAUDE.md + `.claude/agents/*.md` | AGENTS.md + `system-prompt.ts` |
| Agent definition | Category system (`model`, `temperature`, `prompt_append`, `tools.allow/deny`, `fallback_models`) | Subagent frontmatter (`model`, `effort`, `tools`, `disallowedTools`, `memory`, `isolation`) | Extension API (TypeScript), Skills (Markdown) |
| Design patterns | 5 (Simple/Chain/Router/Parallel/Orchestrator) | 5 (Simple/Fork/Pipeline/Hook/Batch) | Not formalized |
| Permission model | 6 modes (allow/ask/deny/passive/restricted/inherit) | 6 modes (default/acceptEdits/plan/auto/dontAsk/bypass) | Project Trust + containerization |
| Tool isolation | `tools.allow`/`tools.deny` | `tools`/`disallowedTools` | No built-in (via Gondolin) |
| Model routing | Category routing + `fallback_models` | `model` field per Subagent | `/model` command, Ctrl+P switching |

### US-AE-03: Loop Engineering Comparison

| Loop Aspect | OpenCode | Claude Code | Pi Agent |
|-------------|----------|-------------|----------|
| Background tasks | `task(run_in_background=true)` + `background_output()` | `/fork`, `/background`, `--bg` | SDK/RPC modes |
| Session management | `/new`, `/compact`, `/export`, `/sessions` | `/compact`, `/clear` | Session Tree (Fork/Clone/Tree), JSONL storage |
| CI/CD integration | SDK (`@opencode-ai/sdk`), CLI (`-p` flag) | CLI (`-p`), GitHub Action, Python/TS SDK | CLI (`-p`), RPC (JSONL), SDK (`@pi-agent-core`) |
| Worktree isolation | Recommended in agent-architecture.md | `isolation: worktree` field | Git worktree (manual) |
| Stop conditions | Implicit in agent-architecture.md (retry patterns) | `maxTurns` field | `maxTurns` (via extension) |
| Automation loops | `/ralph-loop`, `/ulw-loop` (OMO commands) | Semi-automatic (via Hooks + MCP) | **Actively doesn't build-in** — SDK/RPC for custom loops |

---

## Cross-Reference Audit

### Cross-references to Ch6 (Context Engineering)

| Source Appendix | Target | Count | Quality |
|----------------|--------|-------|---------|
| App B `ecosystem.md` | `06-advanced/context/compression.md` | 1 | Single line, could be more descriptive |
| App B `agent-architecture.md` | `06-advanced/custom-agents.md` | 1 | ✅ Good ref for Plugin development |
| App B `commands.md` | `06-advanced/context-compression.md` | 2 | ✅ Good, links to compression + token budget |
| App C | Ch6 context articles | **0** | ❌ Missing entirely |
| App D `overview.md` | Ch1 `harness-engineering-theory.md` | 1 | Maps L1-L4 but to Ch1, not Ch6 |

### Cross-references to Ch4 (Workflow Patterns)

| Source Appendix | Target | Count | Quality |
|----------------|--------|-------|---------|
| App B `agent-architecture.md` | `04-workflows/multi-agent-collab.md` | 1 | ✅ |
| App B `agent-architecture.md` | `04-workflows/teams-collaboration.md` | 1 | ✅ |
| App C `agent-architecture.md` | `04-workflows/custom-workflows.md` | 1 | ✅ |
| App C `agent-architecture.md` | `04-workflows/agent-derivation.md` | 1 | ✅ |
| App D | Ch4 workflow articles | **0** | ❌ Missing |

---

## Key Gaps Summary

### Critical Gaps (should fix)

| # | Gap | Location | Impact |
|---|-----|----------|--------|
| 1 | **Missing glossary terms**: Loop Engineering, Model Routing, Feedback Loop, Generator-Evaluator, March of Nines | Appendix A `glossary.md` | AE cannot quickly look up core concepts |
| 2 | **No dedicated context engineering reference** in any appendix | All appendices | AE must cross-reference to Ch6 for common context questions |
| 3 | **No Generator-Evaluator pattern coverage** anywhere | All appendices | AE SKILL's most impactful pattern is absent from reference material |
| 4 | **No stop condition reference table** for loops | All appendices | AE needs clear stop conditions for loop design (success/timeout/budget/manual) |
| 5 | **Ch4 and Ch6 cross-references are sparse** in App C and D | App C/D ecosystem.md | Reader may not discover relevant content |

### Moderate Gaps (nice to fix)

| # | Gap | Location | Impact |
|---|-----|----------|--------|
| 6 | **No AE best practices section** in any appendix | All appendices | Content is reference-oriented, not methodology-oriented |
| 7 | **No formalized design pattern catalog** for Pi Agent | App D | Pi lacks the 5-pattern structure that App B and C provide |
| 8 | **No cross-tool config approach decision tree** | None | AE must manually compare across 3 appendices |
| 9 | **Token budget by model reference** missing | All appendices | AE needs quick lookup for cost planning |
| 10 | **No template library** for common AE scenarios | All appendices | Reusable patterns (security reviewer, CI gate, etc.) not cataloged |

### Appendix A references.md

| # | Gap | Impact |
|---|-----|--------|
| 11 | **No AE methodology references** (march of nines, Generator-Evaluator, loop engineering papers) | AE cannot cite methodology sources |
| 12 | **SWE-bench referenced** but not Terminal-Bench | AE needs both for tool evaluation |
| 13 | **No oh-my-openagent official docs link** listed | Missing OMO documentation ref |

---

## Conclusion

| Criterion | Rating | Summary |
|-----------|--------|---------|
| **US-AE-01 (Agent config)** | ⭐⭐⭐ (3/3) | Strong coverage in App B and C agent-architecture.md. App D adequate via Extension API. Cross-tool comparisons present. **Gap**: no integrated decision tree. |
| **US-AE-02 (Context engineering)** | ⭐ (1/3) | Weakest area. No appendix has dedicated context engineering reference. Coverage limited to `/compact` commands and surface mentions. Ch6 content exists but cross-refs are sparse. |
| **US-AE-03 (Loop engineering)** | ⭐⭐ (2/3) | All three ecosystem articles now have "Loop Engineering Ecology" sections. App D strongest (SDK/RPC + Session Tree). **Gap**: no stop condition reference, no Generator-Evaluator pattern coverage. |

### Recommended Actions (by priority)

1. **P0 — Add missing AE glossary terms** to `appendix-a/glossary.md` (Loop Engineering, Model Routing, Feedback Loop, Generator-Evaluator, March of Nines)
2. **P1 — Add context engineering cross-references** from each appendix's ecosystem.md to Ch6 context articles (context-compression.md, context-injection-patterns.md, performance-tuning.md)
3. **P1 — Add stop condition reference table** to all three ecosystem.md files (under Loop Engineering)
4. **P2 — Add Generator-Evaluator pattern** to App B and C agent-architecture.md design pattern sections
5. **P2 — Add Ch4 workflow cross-references** to App D ecosystem.md
6. **P3 — Create AE cross-tool configuration decision tree** in a single appendix (perhaps App B ecosystem.md)
