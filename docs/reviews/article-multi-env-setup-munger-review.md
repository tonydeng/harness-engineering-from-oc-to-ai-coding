# Munger Review Report — multi-env-setup.md

**Review Date:** 2026-06-06  
**Article:** `src/03-setup/multi-env-setup.md`  
**Review Lens:** Decision Quality, Incentive Alignment, Second-Order Effects  

---

## Executive Summary

The article creates **good incentives** for engineering teams. It correctly prioritizes security (no hardcoded keys, env var injection, `.gitignore` enforcement) and provides a clear progression from simple to enterprise-grade solutions. The multi-environment strategy (dev / CI / production) with different permission profiles aligns incentives correctly: developers get flexibility, CI gets determinism, production gets security.

---

## Incentive Alignment Analysis

| Article Advice | Incentive Created | Assessment |
|---------------|-------------------|------------|
| "Don't commit `.env` to Git" | ✅ Prevents credential leaks | Correctly emphasized |
| "Use different API keys per environment" | ✅ Limits blast radius | Good practice |
| "Production: deny edits and bash" | ✅ Prevents accidental changes | Sound zero-trust approach |
| "Start with env vars, graduate to Secret Store" | ✅ Low barrier to entry, clear upgrade path | Pragmatic |
| "API key rotation every 90 days" | ✅ Regular security hygiene | Reasonable cadence |
| "Config-as-code in Git" | ✅ Auditability and reproducibility | Teams should do this |

**No incentive misalignment detected** — the article consistently pushes readers toward secure, maintainable practices.

---

## Decision Quality Assessment

### Good decisions in the article:
1. **Environment separation via config files** — Simple, predictable, no hidden inheritance chains
2. **`OPENCODE_CONFIG` for path switching** — Explicit, debuggable, CI-friendly
3. **Permission layering** — Global defaults + per-agent overrides reduces repetition
4. **Progressive security** — env vars → `.env` → Secret Store, matching team maturity

### Potential decision traps (all mitigated):
1. **"CI needs `--permission` flag"** — The flag doesn't exist; corrected to `OPENCODE_PERMISSION` env var
2. **"Use `logging` config"** — Not in official schema; corrected with CLI `--log-level` note
3. **"Use `${VAR}` syntax"** — Wrong interpolation syntax; corrected to `{env:VAR}`

---

## Second-Order Effects

### Positive second-order effects:
1. Teams that follow this guide will naturally adopt **config-as-code** practices
2. The security checklist creates useful **friction** before deployment
3. Different environment templates **teach** the permission model progressively
4. Secret Store integration advice **future-proofs** the setup

### Negative effects to watch for (none critical):
1. Model IDs may go **stale** — article should note "run `opencode models` to verify current IDs"
2. The CI example uses `opencode` without `run` subcommand — may behave differently across versions
3. No mention of **rate limiting** or **token budget** across environments (covered in another article)

---

## Missing Warnings or Caveats

**Minor gaps (not blockers):**
- No explicit mention that OpenCode auto-loads `.env` — only implied
- No warning about `.env` file permissions (should be `600`)
- No mention of OpenCode's `--dangerously-skip-permissions` flag and its risks
- No discussion of CI/CD token expiration management

---

## Conclusion

The article creates **strong positive incentives** for teams adopting multi-environment OpenCode setups. Decision quality is high after corrections. No structural changes needed. The security-first progression (env vars → `.env` → Vault/AWS) is exactly the right ladder for teams of varying maturity.

---

**Review Completed:** 2026-06-06  
**Reviewer:** Munger Lens (Decision Quality)  
**Build Verification:** ✅ mdbook build passes (0 errors)
