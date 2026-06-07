# Data Research: OpenCode Permission Schema Verification

> **Research Date**: 2026-06-06
> **Purpose**: Verify OpenCode's actual permission model configuration schema against claims in `src/02-core-concepts/constraints-system.md`
> **Sources**: OpenCode official docs, OpenCode GitHub repo, oh-my-openagent repos, cross-repo validation

---

## 1. OpenCode Permission Model (Actual)

### Source: OpenCode Official Documentation

OpenCode's permission system is defined in the `opencode.json` config under the `"permission"` key (singular, not plural):

```json
{
  "permission": {
    "read": "allow",
    "edit": "ask",
    "bash": {
      "git *": "allow",
      "rm *": "deny"
    }
  }
}
```

**Key facts**:
- Root key is `"permission"` (singular), NOT `"permissions"` (plural as used in article)
- Permission values are only: `"allow"` | `"ask"` | `"deny"` — only 3 actions exist
- `"passive"`, `"restricted"`, `"inherit"` — **DO NOT EXIST** as permission modes
- No sub-key `"tools"`, `"paths"`, or `"commands"` — these are FICTIONAL
- Permission keys use capability names, not tool names:
  - `"read"` — not `"read_file"`
  - `"edit"` — not `"write_file"` 
  - `"bash"` — not `"execute_command"`
  - No `"delete_file"`, `"network_request"`, `"search_code"` keys exist

### Complete List of Actual OpenCode Permission Keys

| Key | Description | Article Claim | Actual |
|-----|------------|--------------|--------|
| `read` | Read files/directories | `read_file` | ✅ |
| `edit` | Edit/create files | `write_file` | ✅ differs |
| `list` | List directory contents | Not mentioned | ✅ exists |
| `glob` | File glob patterns | Not mentioned | ✅ exists |
| `grep` | Content search | Not mentioned | ✅ exists |
| `codesearch` | Code search | `search_code` | ✅ different name |
| `lsp` | LSP queries | Not mentioned | ✅ exists |
| `bash` | Shell commands | `execute_command` | ✅ different name |
| `task` | Task management | Not mentioned | ✅ exists |
| `todo` / `todowrite` | Todo management | Not mentioned | ✅ exists |
| `skill` | Skill loading | Not mentioned | ✅ exists |
| `webfetch` | Web fetching | `network_request` | ✅ different name |
| `websearch` | Web search | Not mentioned | ✅ exists |
| `question` | User questions | Not mentioned | ✅ exists |
| `external_directory` | External paths | Not mentioned | ✅ exists |
| `doom_loop` | Loop detection | Not mentioned | ✅ exists |

### Agent Mode Values

Source: OpenCode agent config docs
- `agent.mode` values: `"primary"` | `"subagent"` | `"all"`
- `"mode": "passive"` — **DOES NOT EXIST**
- `"allowedOperations"` / `"deniedOperations"` — **DO NOT EXIST**

---

## 2. Fictional Config Keys in the Article

The article uses these config keys that **DO NOT EXIST** in actual OpenCode:

| Config Key | Location in Article | Status |
|-----------|-------------------|--------|
| `"permissions"` (plural) | Lines 63, 255, 299, 771, 795, 841, 873, 968, 1054 | ❌ Should be `"permission"` |
| `"tools"` | Lines 64, 259, 774, 799, 844, 873 | ❌ Doesn't exist |
| `"paths"` | Lines 266, 773, 782, 855, 881, 980 | ❌ Doesn't exist |
| `"commands"` | Lines 272, 798, 858, 886, 975 | ❌ Doesn't exist |
| `"pathPermissions"` | Line 301 | ❌ Doesn't exist |
| `"defaultAction"` | Line 798 | ❌ Doesn't exist |
| `"allowedTools"` | Line 800 | ❌ Doesn't exist |
| `"deniedTools"` | Line 806 | ❌ Doesn't exist |
| `"environment"` | Lines 843, 872 | ❌ Doesn't exist |
| `"audit"` | Lines 891-895 | ❌ Doesn't exist |
| `"preview"` | Lines 991-995 | ❌ Doesn't exist |
| `"outputFilter"` | Lines 1066-1080 | ❌ Doesn't exist |
| `"warnings"` | Lines 1077-1079 | ❌ Doesn't exist |
| `"database"` | Lines 982-990 | ❌ Doesn't exist |
| `"agent.mode": "passive"` | Line 365 | ❌ Doesn't exist |

---

## 3. Version Numbers Verified

**Article claim** (lines 256, 772):
```
// Requires OpenCode >= v1.16.x, OMO >= v4.7.x
```

**Verification**:
- OpenCode v1.16.x: ✅ CONFIRMED (current v1.16.2)
- oh-my-openagent v4.7.x: ✅ CONFIRMED (current v4.7.5)
- Source: `src/00-guide/README.md` lines 322-323

**Conclusion**: Version numbers are correct.

---

## 4. Example Files Verification

**Article claims** 10 example files exist on these paths:

| Path | Exists? |
|------|---------|
| `examples/opencode-configs/basic.jsonc` | ✅ Yes (16 lines, no permissions) |
| `examples/opencode-configs/permissions.jsonc` | ❌ NOT FOUND |
| `examples/opencode-configs/path-permissions.jsonc` | ❌ NOT FOUND |
| `examples/opencode-configs/passive-mode.jsonc` | ❌ NOT FOUND |
| `examples/opencode-configs/least-privilege.jsonc` | ❌ NOT FOUND |
| `examples/opencode-configs/default-deny.jsonc` | ❌ NOT FOUND |
| `examples/opencode-configs/dev-permissions.jsonc` | ❌ NOT FOUND |
| `examples/opencode-configs/prod-permissions.jsonc` | ❌ NOT FOUND |
| `examples/opencode-configs/database-safety.jsonc` | ❌ NOT FOUND |
| `examples/opencode-configs/secrets-protection.jsonc` | ❌ NOT FOUND |
| `examples/ast-grep-rules/no-direct-sql.yaml` | ❌ NOT FOUND (directory doesn't exist) |

**Actual directory contents**:
```
examples/opencode-configs/
├── basic.jsonc              (16 lines)
├── oh-my-openagent-advanced.json  (117 lines)
└── oh-my-openagent-basic.json     (21 lines)
```

---

## 5. AST-grep Integration

**Article claim** (lines 44, 150, 594-637): AST-grep is part of OpenCode's constraint system.

**Verification**: 
- AST-grep is an **external tool** (npm package `@ast-grep/cli`)
- OpenCode does NOT natively integrate AST-grep
- The directory `examples/ast-grep-rules/` does not exist in this project
- AST-grep is referenced elsewhere in the project as a "recommended local tool" (in `src/06-advanced/performance-tuning.md`)

**Conclusion**: Article misrepresents AST-grep as an integrated feature.

---

## 6. LSP Integration

**Article claim** (lines 149-150, 557-592): LSP diagnostics are a built-in constraint mechanism in OpenCode.

**Verification**:
- OpenCode does support LSP diagnostics via the `lsp_diagnostics` tool/API
- OpenCode can detect LSP errors in generated code and trigger auto-fix loops
- The LSP integration claim is **PARTIALLY CORRECT** — OpenCode does have LSP support, but it's not as formalized as the article describes

**Conclusion**: Partially correct — LSP diagnostics exist in OpenCode but the article over-formalizes the mechanism.

---

## 7. Factual Discrepancies Summary

| Severity | Count | Example |
|----------|-------|---------|
| 🔴 HIGH (misleads readers) | 15+ | Fictional 6 modes, wrong config keys, non-existent files |
| 🟡 MEDIUM (imprecision) | 5+ | AST-grep external, LSP details, case studies unverifiable |
| 🟢 LOW (trivial) | 3+ | STRIDE table format, minor wording |

---

*Research compiled on 2026-06-06*
*Sources: OpenCode official docs, GitHub repos, file system verification*
