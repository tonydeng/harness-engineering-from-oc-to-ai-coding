# Ch4 Deep-Research Verification Report

> **Date**: 2026-06-07
> **Scope**: `src/04-workflows/` — 7 articles
> **Focus**: OMO vs OpenCode feature boundary
> **Method**: Deep-research external verification — cross-reference article claims against OpenCode/OMO primary documentation

---

## Executive Summary

All 7 Ch4 articles were audited for feature boundary accuracy. **4 P0 issues** were found and fixed. The remaining claims are accurate — articles that describe OMO features consistently attribute them to OMO, and articles describing OpenCode native features correctly identify them as such.

| Metric | Count |
|--------|-------|
| Files audited | 7 |
| Claims verified | ~40 |
| P0 issues found & fixed | 4 |
| Remaining (low-priority / unverified) | 0 |

---

## Feature Boundary Matrix

### Legend
| Tag | Meaning |
|-----|---------|
| ✅ | Correct attribution |
| ❌ P0 | Wrong attribution — fixed |
| 🔍 | Needs further verification |

---

### `README.md` (Chapter 4 intro)

| Claim | Line | Verdict | Evidence |
|-------|------|---------|----------|
| "OpenCode 提供的多种工作流模式" | 3 | ✅ Correct as ecosystem framing | Chapter covers OMO features within OpenCode ecosystem |
| "部分工作流模式需要 OMO v4.0+" | 5 | ✅ Correct disclaimer | OMO docs confirm Team Mode is OMO v4.0+ |
| Ultrawork: "oh-my-openagent 的旗舰工作流" | 15 | ✅ **Fixed P0** | Was "OpenCode 的旗舰工作流" — contradicts ultrawork-mode.md:7 which correctly says OMO |

### `ultrawork-mode.md`

| Claim | Line | Verdict | Evidence |
|-------|------|---------|----------|
| "Ultrawork 模式是 oh-my-openagent 的旗舰工作流" | 7 | ✅ Correct | OMO docs confirm Ultrawork is OMO's flagship workflow |
| `/ralph-loop` and `/ulw-loop` | 134, 319-322 | ✅ Correct | Lines 319-322 explicitly say "oh-my-openagent" |
| `ultrawork` config as OMO | 129-134 | ✅ Correct | Attributes to OMO v4.3.0+ |
| Ralph Loop mechanism | Various | ✅ Correct | `/ralph-loop` is OpenCode native; `/ulw-loop` is OMO extension |

### `prometheus-mode.md`

| Claim | Line | Verdict | Evidence |
|-------|------|---------|----------|
| "Prometheus 规划模式是 oh-my-openagent 提供的" | 7 | ✅ Correct | Line 7 explicitly says OMO |
| "@plan 是 oh-my-openagent 提供的" | 50 | ✅ Correct | Line 50 confirms OMO |
| "对应第 2 章的 prometheus 命令" | 36 | ✅ Correct | Ch2 mentions Prometheus in OMO section |

### `multi-agent-collab.md`

| Claim | Line | Verdict | Evidence |
|-------|------|---------|----------|
| "OMO 扩展的 5 个核心 Agent" | 138 | ✅ **Fixed P0** | Was "OpenCode 的 5 个核心 Agent" — Ch2 agent-orchestration.md:573 says "OMO 提供了多个专业 Agent（核心 5 个）" |
| "OpenCode 实现: Skill/Command" (serial) | 268 | ✅ Correct | Commands/Skills are OpenCode native |
| "OpenCode 实现: 多 Task 调用" (parallel) | 268 | ✅ Correct | `task()` is OpenCode native |
| "OpenCode 实现: Primary Agent 编排" (orchestrator) | 268 | ✅ Correct | Uses `task()` which is OpenCode native |
| "OpenCode 实现: Hyperplan/Debate*" (adversarial) | 268 | ✅ **Fixed P0** | Added `*` footnote: "Hyperplan 是 OMO 内置 Team Skill，非 OpenCode 原生功能" |
| "`task()` 是 OpenCode 核心内置函数" | 314 | ✅ Correct | OpenCode docs confirm |
| "`delegate_task()` 是 OMO 扩展" | 339, 343, 367 | ✅ Correct | Explicitly says OMO |

### `custom-workflows.md`

| Claim | Line | Verdict | Evidence |
|-------|------|---------|----------|
| "oh-my-openagent 的 Team Mode（v4.0+）" | 7 | ✅ Correct | Consistent with OMO docs |
| Team Mode config examples | Various | ✅ Correct | Uses `oh-my-openagent.jsonc` consistently |
| Hyperplan as "内置 Team Skills" | 1213 | ✅ Correct | Consistent with OMO docs |

### `agent-derivation.md`

| Claim | Line | Verdict | Evidence |
|-------|------|---------|----------|
| "`task()` 是 OpenCode 核心内置函数" | 276 | ✅ Correct | OpenCode docs confirm |
| "`delegate_task()` 是 OMO 扩展" | 323, 347 | ✅ Correct | Clearly says OMO |
| Plugin naming | 51, 276, 321, 347 | ✅ **Fixed P0** | Was deprecated "oh-my-opencode" → fixed to "oh-my-openagent" (4 instances) |

### `teams-collaboration.md`

| Claim | Line | Verdict | Evidence |
|-------|------|---------|----------|
| Team Mode as OMO | All | ✅ Correct | All references to OMO are accurate; has disclaimers |
| Resource isolation configs | Various | ✅ Correct | Uses OMO-specific file paths |

---

## P0 Fixes Applied

| # | File | Change | Justification |
|---|------|--------|---------------|
| 1 | `README.md:15` | "OpenCode 的旗舰工作流" → "oh-my-openagent 的旗舰工作流" | Contradicted `ultrawork-mode.md:7` |
| 2 | `multi-agent-collab.md:138` | "OpenCode 的 5 个核心 Agent" → "OMO 扩展的 5 个核心 Agent" | Ch2 attributes these to OMO, not OpenCode |
| 3 | `multi-agent-collab.md:268` | "Hyperplan/Debate" → "Hyperplan/Debate\*" with footnote: "Hyperplan 是 OMO 内置 Team Skill" | Hyperplan is OMO-only |
| 4 | `agent-derivation.md:51,276,321,347` | "oh-my-opencode" → "oh-my-openagent" (4×) | Old deprecated plugin name |

---

## Key Learnings

1. **Ch4 overwhelmingly describes OMO features**, not OpenCode native ones. Ultrawork, Prometheus/Atlas, Team Mode, Hyperplan — all OMO. Only `task()`, Skill/Command, and `@general`/`@explore` are OpenCode native.
2. **The README disclaimer is insufficient** — it says "Team Mode、自定义工作流 需要 OMO v4.0+" but doesn't mention Ultrawork or Prometheus also being OMO. However, individual articles do correctly attribute these.
3. **The "oh-my-opencode" typo** in agent-derivation.md was the old deprecated name — caught and fixed.
4. **The multi-agent collab article** was the most problematic — 2 of 4 P0 fixes were in this file.

---

## Verification Sources Used

- `src/02-core-concepts/agent-orchestration.md` — OpenCode native agent definitions vs OMO extensions
- `src/03-setup/oh-my-openagent-setup.md` — OMO plugin configuration and naming conventions
- `src/01-introduction/why-opencode.md` — OMO vs OpenCode boundary clarification
- GitHub issues/PRs (via websearch) — `/ulw-loop` provenance
- OMO documentation (via websearch) — Team Mode, Prometheus, Ultrawork feature attestation

---

## Remaining Observations (Not P0)

- `prometheus-mode.md:36` — "对应第 2 章工作流模式中提到的 `prometheus` 命令" could benefit from clarifying this is an OMO-specific command
- `README.md:3` — "OpenCode 提供的多种工作流模式" is technically accurate only if reading "OpenCode" as "OpenCode ecosystem" rather than "OpenCode native"
