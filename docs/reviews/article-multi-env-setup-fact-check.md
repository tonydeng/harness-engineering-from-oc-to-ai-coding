# Article Fact-Check Report: multi-env-setup.md

**Review Date:** 2026-06-06  
**Article:** `src/03-setup/multi-env-setup.md`  
**Review Method:** Direct API research + official documentation cross-reference  
**Status:** ❌ **MUST BE CORRECTED** - Multiple critical factual errors found

---

## Executive Summary

The article contains **fundamental factual errors** about OpenCode's configuration system. The `$extends` profile inheritance mechanism described in the article **does not exist** in the official OpenCode implementation. The actual configuration uses an `agent`-centric model, not a profile-inheritance model.

---

## Critical Factual Errors (MUST FIX)

### 1. `$extends` Profile Inheritance Mechanism

**❌ FALSE CLAIM (Lines 50-90, 93-116, etc.)**
> "OpenCode 的 Profile 系统支持通过 `$extends` 字段实现配置继承"

**Fact:** OpenCode **does not support** `$extends` syntax or a "Profile" inheritance system.

**Evidence from Official Docs:**
- URL: https://opencode.ai/docs/config/
- URL: https://opencode.ai/docs/agents/
- URL: https://opencode.ai/docs/cli/

Actual OpenCode configuration uses:
```json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "build": {
      "mode": "primary",
      "model": "anthropic/claude-sonnet-4-20250514",
      "permission": {
        "edit": "allow",
        "bash": "allow"
      }
    }
  }
}
```

**Corrected Description:**
OpenCode configuration uses **Agent-specific configuration** within the `agent` field, not profile inheritance. Each agent can have its own configuration with permissions and model settings.

---

### 2. CLI Flags

**❌ FALSE CLAIM (Lines 294-319)**
> CLI flags: `--profile`, `--model`, `--max-tokens`, `--non-interactive`

**Fact Check:**

| CLI Flag | Status | Evidence |
|----------|--------|----------|
| `--model` / `-m` | ✅ **TRUE** | OpenCode CLI supports `--model` flag |
| `--profile` | ❌ **FALSE** | No such flag exists in official CLI |
| `--max-tokens` | ❌ **FALSE** | Not a standard CLI flag |
| `--non-interactive` | ❌ **FALSE** | Not documented in official CLI |

**Evidence:** https://opencode.ai/docs/cli/

**Corrected Implementation:**
```bash
# Actual OpenCode CLI usage
opencode --model anthropic/claude-opus-4-7
opencode  # Uses default model from config
```

---

### 3. Environment Variables

**❌ FALSE CLAIM (Lines 270-293)**
> "OPENCODE_ENV", "OPENCODE_PROFILE" environment variables

**Fact Check:**

| Environment Variable | Status | Evidence |
|---------------------|--------|----------|
| `OPENCODE_CONFIG` | ✅ TRUE | Config file path override |
| `OPENCODE_CONFIG_CONTENT` | ✅ TRUE | Inline config JSON |
| `OPENCODE_DISABLE_AUTOCOMPACT` | ✅ TRUE | Disable auto compaction |
| `OPENCODE_ENV` | ❌ FALSE | Not documented |
| `OPENCODE_PROFILE` | ❌ FALSE | Not documented |

**Evidence:** https://opencode.ai/docs/cli/#environment-variables

---

### 4. Hook System

**❌ FALSE CLAIM (Lines 145-147, 397-406)**
> Built-in `hooks` configuration with `onSessionStart`, `onSessionEnd`, `onError`

**Fact:** OpenCode **does not** have built-in hook configuration in `opencode.json`.

**Actual Implementation:**
- Hooks are implemented via **plugins** (https://opencode.ai/docs/plugins/)
- Third-party plugin `opencode-claude-hooks` provides similar functionality
- Official hooks available through `Plugin.trigger()`:
  - `session.created`, `session.compacted`, `session.deleted`
  - `tool.execute.before`, `tool.execute.after`
  - `experimental.session.compacting`

**Evidence:**
- https://opencode.ai/docs/plugins/
- https://github.com/code-yeongyu/opencode-claude-hooks

---

### 5. Compaction Configuration

**❌ PARTIALLY FALSE (Lines 360-362)**
> `compaction.auto`, `compaction.prune`, `compaction.tail_turns`

**Fact Check:**

| Compaction Config | Status | Evidence |
|------------------|--------|----------|
| `compaction.auto` | ✅ TRUE | Default: `true` |
| `compaction.prune` | ✅ TRUE | Default: `false` (must be explicitly enabled) |
| `compaction.reserved` | ✅ TRUE | Token buffer (default: min(20000, model output limit)) |
| `compaction.tail_turns` | ❌ FALSE | **Does not exist** |

**Corrected Configuration:**
```json
{
  "compaction": {
    "auto": true,
    "prune": false,
    "reserved": 10000
  }
}
```

**Evidence:** https://opencode.ai/docs/config/#compaction

---

### 6. Audit Configuration

**❌ FALSE CLAIM (Lines 451-458)**
> `audit.enabled`, `audit.log_level`, `audit.retention_days`, `audit.include_prompts/responses`

**Fact:** OpenCode **does not have** built-in audit logging configuration in `opencode.json`.

**Actual Implementation:**
- Logging is handled via `logging` configuration:
  ```json
  {
    "logging": {
      "level": "info",
      "file": "~/.opencode/logs/opencode.log",
      "max_size_mb": 100,
      "backup_count": 5
    }
  }
  ```
- Structured logging via `client.app.log()` in plugins
- No built-in audit trail with retention policies

**Evidence:** https://opencode.ai/docs/config/

---

### 7. Output Format Configuration

**❌ FALSE CLAIM (Lines 403-406)**
> `output.format`, `output.include_metrics`

**Fact:** OpenCode **does not support** this configuration structure.

**Actual Implementation:**
- Output format is determined by the TUI or API client
- Metrics are not configurable via `opencode.json`

---

### 8. Model Names

**❌ MISLEADING (Throughout article)**
> Model names: `fast-model`, `best-capability-model`, `balanced-model`

**Fact:** These are **not** real OpenCode model identifiers.

**Actual Model Format:**
- Models use `provider_id/model_id` format
- Examples: `anthropic/claude-opus-4-7`, `openai/gpt-5.5`, `google/gemini-3.1-pro`
- Variants are defined within providers, not as separate model names

**Evidence:** https://opencode.ai/docs/models/

---

## Partially True Claims (Need Clarification)

### 9. Permission System

**✅ PARTIALLY TRUE (Lines 67-73, 97-115, etc.)**

OpenCode **does** have permission configuration, but the structure is different:

**Actual Structure:**
```json
{
  "agent": {
    "build": {
      "permission": {
        "edit": "allow",
        "bash": "ask",
        "glob": "allow"
      }
    }
  }
}
```

**Key Differences:**
- Permissions are per-agent, not per-profile
- Uses wildcard patterns for tool matching
- No `permission.edit`, `permission.bash` top-level structure

---

### 10. Secret Management

**✅ BASICALLY TRUE (Lines 530-623)**

OpenCode **does** support secret management via:
- Environment variables (`ANTHROPIC_API_KEY`, etc.)
- Config file `provider.apiKey` field
- Custom provider configurations

**Corrected Implementation:**
```json
{
  "provider": {
    "anthropic": {
      "apiKey": "${ANTHROPIC_API_KEY}"
    }
  }
}
```

---

## Missing Features (Not Available in OpenCode)

The following features mentioned in the article **do not exist** in OpenCode:

1. **Profile inheritance system** - Does not exist
2. **CLI `--profile` flag** - Does not exist
3. **Built-in audit logging** - Only via plugins
4. **Built-in hook configuration** - Only via plugins
5. **Output format configuration** - Not supported
6. **Environment-specific profile switching** - Not supported
7. **Session lifecycle hooks** - Only via plugins

---

## Recommended Correction Strategy

### Immediate Actions (CRITICAL)

1. **Remove all `$extends` profile inheritance examples**
   - Replace with actual OpenCode agent configuration
   - Use `agent` field for environment-specific settings

2. **Remove false CLI flags**
   - Remove `--profile`, `--max-tokens`, `--non-interactive`
   - Add accurate CLI usage examples

3. **Remove false environment variable claims**
   - Remove `OPENCODE_ENV`, `OPENCODE_PROFILE`
   - Document actual environment variables

4. **Correct compaction configuration**
   - Remove `tail_turns` parameter
   - Keep only `auto`, `prune`, `reserved`

5. **Remove hook configuration examples**
   - Replace with plugin-based hook implementation
   - Link to `opencode-claude-hooks` or similar

6. **Remove audit configuration**
   - Replace with actual logging configuration
   - Document plugin-based auditing

### Content Replacement Strategy

**Current (False):**
```json
{
  "$extends": "base",
  "permission": {
    "edit": { "*": "ask" }
  }
}
```

**Should Be (Actual OpenCode):**
```json
{
  "agent": {
    "dev": {
      "model": "anthropic/claude-sonnet-4-6",
      "permission": {
        "edit": "ask",
        "bash": "ask"
      }
    }
  }
}
```

---

## References

### Official Documentation

1. **Config Reference:** https://opencode.ai/docs/config/
2. **CLI Reference:** https://opencode.ai/docs/cli/
3. **Agents Reference:** https://opencode.ai/docs/agents/
4. **Plugins Reference:** https://opencode.ai/docs/plugins/
5. **Models Reference:** https://opencode.ai/docs/models/

### Community Resources

1. **opencode-claude-hooks:** https://github.com/code-yeongyu/opencode-claude-hooks
2. **GitHub Repository:** https://github.com/anomalyco/opencode

---

## Quality Assessment

| Category | Score | Notes |
|----------|-------|-------|
| Factual Accuracy | ❌ **0/10** | Multiple critical errors |
| Code Examples | ❌ **0/10** | All examples would not work |
| CLI Commands | ❌ **2/10** | Only `--model` is accurate |
| Configuration Schema | ❌ **3/10** | Partial compaction accuracy |
| Security Claims | ⚠️ **5/10** | Basic principles true, implementation false |

**Overall Verdict:** **MUST BE REWRITTEN** - Cannot be fixed with minor edits. The article's core concept (profile inheritance) is fundamentally incorrect.

---

## Next Steps

1. **Archive or delete** current `multi-env-setup.md`
2. **Create new article** based on actual OpenCode features:
   - Agent configuration
   - Provider configuration
   - Environment variables
   - Plugin-based hooks
   - Compaction configuration
3. **Update cross-references** in other chapters
4. **Update SUMMARY.md** if needed

**Review Completed:** 2026-06-06  
**Review By:** Automated Fact-Check (Web Research)
**Confidence Level:** **HIGH** - Based on official documentation
