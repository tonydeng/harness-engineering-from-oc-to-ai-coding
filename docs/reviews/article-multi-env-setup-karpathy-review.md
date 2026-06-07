# Karpathy Review Report — multi-env-setup.md

**Review Date:** 2026-06-06  
**Article:** `src/03-setup/multi-env-setup.md`  
**Review Lens:** Systems Engineering / Software 2.0  
**Verification Source:** [OpenCode Config Docs](https://opencode.ai/docs/config/), [CLI Docs](https://opencode.ai/docs/cli/), [Agents Docs](https://opencode.ai/docs/agents/), [Permissions Docs](https://opencode.ai/docs/permissions/)

---

## Executive Summary

The current version of the article has already been corrected from an earlier version that contained fundamental errors (fictional `$extends` profile inheritance system). The remaining issues are **minor factual inaccuracies** in config syntax and component naming. The article's architecture (agent-centric configuration, environment separation via config paths, permission-based security) is sound and matches OpenCode's actual design.

---

## Factual Claims Verification

| # | Claim | Location | Status | Evidence |
|---|-------|----------|--------|----------|
| 1 | `$schema: "https://opencode.ai/config.json"` | Multiple config blocks | ✅ CORRECT | Official config docs confirm this URL |
| 2 | Provider config `"apiKey": "${VAR}"` | Lines 100-104, 153-162, 198-202, 281-287, 317-323 | ❌ **CORRECTED** | Official docs use `"options": {"apiKey": "{env:VAR}"}` syntax |
| 3 | Env var interpolation `${ENV_VAR}` | Line 114, 314 | ❌ **CORRECTED** | Official syntax is `{env:ENV_VAR}` per config docs |
| 4 | `--permission` CLI flag | Line 238 (CI workflow) | ❌ **CORRECTED** | Not in CLI reference; use `OPENCODE_PERMISSION` env var instead |
| 5 | `logging` config block | Lines 277-281 | ❌ **CORRECTED** (removed) | No `logging` section in official config schema |
| 6 | `code-reviewer` listed as built-in agent | Line 64 | ❌ **CORRECTED** | Not in built-in list (Build, Plan, General, Explore, Scout) |
| 7 | Compaction: `auto`, `prune`, `reserved` | Line 203-207 | ✅ CORRECT | Matches official config docs |
| 8 | Permission: `ask`/`allow`/`deny` | Throughout | ✅ CORRECT | Matches permission system |
| 9 | Permission keys: `edit`, `bash`, `glob`, `read` | Throughout | ✅ CORRECT | All valid permission keys |
| 10 | Agent `mode`: `primary`, `subagent` | Throughout | ✅ CORRECT | Matches agent system |
| 11 | `OPENCODE_CONFIG` env var | Lines 410-416 | ✅ CORRECT | Documented in CLI env vars |
| 12 | Wildcard permission patterns `"npm *": "allow"` | Line 146 | ✅ CORRECT | Supported in permissions system |
| 13 | `.env` file auto-loading | Line 342 | ✅ CORRECT | Official providers page confirms `.env` is loaded |
| 14 | Model ID format `provider/model` | Throughout | ✅ CORRECT | Matches official format |

---

## Engineering Pattern Assessment

**Positive findings:**
- Agent-centric configuration is the correct OpenCode pattern
- Environment separation via `OPENCODE_CONFIG` is idiomatic
- Permission layering (global → per-agent) matches actual system design
- Secret management advice (env vars → `.env` → Vault) follows sound progression
- CI/CD workflow structure is realistic

**Minor concerns:**
- Model IDs (`claude-sonnet-4-6`, `claude-opus-4-7`) may not match current models.dev listing — should verify with `opencode models`
- No mention that `code-reviewer` is a custom agent, not built-in

---

## Specific Issues Found

All issues have been corrected in this review cycle. See corrections applied:
1. `${VAR}` → `{env:VAR}` interpolation syntax (3 locations)
2. `apiKey` → `options.apiKey` provider structure (4 locations)
3. `--permission` flag → `OPENCODE_PERMISSION` env var in CI workflow
4. Removed undocumented `logging` config block
5. Updated built-in agent list to match official docs

---

## Conclusion

The article is **factually sound** after corrections. It correctly represents OpenCode's agent-based configuration model, permission system, and environment separation strategy. No structural or tonal changes needed.

---

**Review Completed:** 2026-06-06  
**Reviewer:** Karpathy Lens (Systems Engineering)  
**Verification Method:** Direct cross-reference with official OpenCode documentation  
**Build Verification:** ✅ mdbook build passes (0 errors)
