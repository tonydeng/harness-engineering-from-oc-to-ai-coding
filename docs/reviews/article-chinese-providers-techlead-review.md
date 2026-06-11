# TechLead Configuration Review: Chinese Providers Article

**Review Date:** 2026-06-06  
**Source:** `src/03-setup/chinese-providers.md`  
**Reviewer:** TechLead Engineering Perspective Agent

---

## Executive Summary

The JSON configuration blocks in this article contain **critical structural errors** that would cause production failures. The document uses an incorrect configuration schema that violates the official OpenCode configuration structure.

---

## 🔴 CRITICAL ISSUES (Production-Blocking)

### Issue 1: `apiKey` and `baseURL` at Wrong Nesting Level

**Location:** Lines 158-159, 228-229, 307-308, 375-376, 384-385

**Document's Structure (WRONG):**
```json
"deepseek": {
  "baseURL": "https://api.deepseek.com",
  "apiKey": "{env:DEEPSEEK_API_KEY}"
}
```

**Required Structure (from official OpenCode schema):**
```json
"deepseek": {
  "options": {
    "baseURL": "https://api.deepseek.com",
    "apiKey": "{env:DEEPSEEK_API_KEY}"
  }
}
```

**Evidence:** OpenCode TypeScript source (`config/provider.ts`) defines:
```typescript
export const Info = Schema.Struct({
  options: Schema.optional(
    Schema.StructWithRest(Schema.Struct({
      apiKey: Schema.optional(Schema.String),
      baseURL: Schema.optional(Schema.String),
      ...
    }), [Schema.Record(Schema.String, Schema.Any)])
  ),
  models: Schema.optional(Schema.Record(Schema.String, Model)),
  ...
})
```

**Impact:** OpenCode will silently ignore top-level `apiKey` and `baseURL`. Provider will fail at runtime.

---

### Issue 2: Model Fields Use Wrong Structure

**Location:** Lines 163-171, 231-257, 310-341

**Document's Structure (WRONG):**
```json
"deepseek-chat": {
  "name": "DeepSeek Chat",
  "context": 128000,
  "maxOutput": 8000
}
```

**Required Structure:**
```json
"deepseek-chat": {
  "name": "DeepSeek Chat",
  "limit": {
    "context": 128000,
    "output": 8000
  }
}
```

**Evidence:** OpenCode Model schema uses `limit.context` and `limit.output`.

**Impact:** OpenCode won't recognize model limits. They default to 0, causing silent context overflow.

---

### Issue 3: Missing `npm` Field for Qwen (Custom Provider)

**Location:** Lines 304-341

Qwen (via Alibaba DashScope) is **not** a built-in OpenCode provider. It requires:
```json
"qwen": {
  "npm": "@ai-sdk/openai-compatible",
  "name": "Qwen",
  "options": {
    "baseURL": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "apiKey": "{env:DASHSCOPE_API_KEY}"
  },
  "models": { ... }
}
```

**Note:** DeepSeek and Moonshot/Kimi ARE built-in providers, so they don't need `npm`.

**Impact:** Without `npm`, OpenCode doesn't know which AI SDK adapter to use for Qwen.

---

### Issue 4: `/connect` TUI Flow for Kimi/Moonshot is Wrong

**Location:** Line 211

**Document says:** "选择 **Custom Provider**"

**Reality:** **Moonshot AI IS a built-in OpenCode provider** — searchable directly via `/connect`.

The correct instruction should be: "搜索 **Moonshot AI**", not "选择 Custom Provider".

---

### Issue 5: `fallback` Field is Not Valid OpenCode Config Key

**Location:** Line 407

```json
"models": {
  "default": "deepseek/deepseek-chat",
  "fallback": "balanced-model"  // ❌ INVALID
}
```

The `fallback` key at `models` level is **not documented**. OpenCode uses:
- `fallbackChain` within category configs
- `runtime_fallback` in oh-my-openagent's config

**Impact:** Config is silently ignored. No fallback behavior occurs.

---

### Issue 6: Multi-Provider Hybrid Uses Invalid Model Names

**Location:** Lines 368-370

```json
"anthropic": {
  "models": {
    "balanced-model": {},      // ❌ Not a real model ID
    "best-capability-model": {} // ❌ Not a real model ID
  }
}
```

`"balanced-model"` and `"best-capability-model"` are **abstraction-layer names** from oh-my-openagent, not actual Anthropic model IDs.

**Impact:** Category routing will fail because no actual provider matches these fake model names.

---

### Issue 7: `proxy` Field is Not Supported in Provider Config

**Location:** Lines 628-632

```json
"deepseek": {
  "proxy": "http://127.0.0.1:7890"  // ❌ Not supported
}
```

The OpenCode provider schema does **not** support a `proxy` field. Proxy must be set via environment variables.

---

## 🟡 MODERATE ISSUES

### Issue 8: Missing `env` Field for Startup Validation

**Location:** All provider config blocks

The official OpenCode pattern includes:
```json
"deepseek": {
  "env": ["DEEPSEEK_API_KEY"],
  "options": {
    "apiKey": "{env:DEEPSEEK_API_KEY}"
  }
}
```

Without it, OpenCode won't verify required environment variables at startup.

---

### Issue 9: `deepseek-reasoner` MaxOutput Value Questionable

**Location:** Line 170

Document says `maxOutput: 64000`. Official DeepSeek V3.2 API shows max output **8K tokens**.

This needs verification against official specs.

---

### Issue 10: Pricing Table Has Mixed Currencies

**Location:** Lines 78-80

Qwen prices in CNY (¥) vs. DeepSeek/Kimi in USD ($). This is confusing without clear explanation.

---

## ✅ WHAT IS CORRECT

| Item | Status |
|------|--------|
| `{env:VAR}` syntax | ✅ Correct |
| `/connect` TUI command | ✅ Correct |
| `/models` verification command | ✅ Correct |
| Base URLs (DeepSeek, Kimi, Qwen) | ✅ Correct |
| Cost calculations (lines 549-555) | ✅ Correct |
| Mermaid flow diagram | ✅ Correct |
| Environment variable export | ✅ Correct |

---

## 🔧 CORRECTED CONFIGURATION TEMPLATE

### DeepSeek (Built-in Provider)

```json:.opencode/config.json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "deepseek": {
      "env": ["DEEPSEEK_API_KEY"],
      "models": {
        "deepseek-v4-flash": {
          "name": "DeepSeek V4 Flash",
          "limit": {
            "context": 1000000,
            "output": 384000
          }
        },
        "deepseek-chat": {
          "name": "DeepSeek Chat (Legacy)",
          "limit": {
            "context": 64000,
            "output": 8000
          }
        }
      }
    }
  }
}
```

### Moonshot/Kimi (Built-in Provider)

```json:.opencode/config.json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "moonshot": {
      "env": ["MOONSHOT_API_KEY"],
      "models": {
        "kimi-k2.6": {
          "name": "Kimi K2.6",
          "limit": {
            "context": 262144,
            "output": 8192
          }
        },
        "kimi-k2.5": {
          "name": "Kimi K2.5",
          "limit": {
            "context": 262144,
            "output": 8192
          }
        }
      }
    }
  }
}
```

### Qwen (Custom Provider)

```json:.opencode/config.json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "qwen": {
      "npm": "@ai-sdk/openai-compatible",
      "env": ["DASHSCOPE_API_KEY"],
      "name": "Qwen",
      "options": {
        "baseURL": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "apiKey": "{env:DASHSCOPE_API_KEY}"
      },
      "models": {
        "qwen3-max": {
          "name": "Qwen3 Max",
          "limit": {
            "context": 262144,
            "output": 8192
          }
        }
      }
    }
  }
}
```

---

## Summary of Required Changes

| Priority | Fix | Location |
|----------|-----|----------|
| 🔴 P0 | Move `apiKey`, `baseURL` inside `options` | Lines 158-159, 228-229, 307-308 |
| 🔴 P0 | Change model `context`/`maxOutput` to `limit.context`/`limit.output` | Lines 163-171, 231-257, 310-341 |
| 🔴 P0 | Add `"npm": "@ai-sdk/openai-compatible"` to Qwen provider | Line 305 |
| 🔴 P0 | Fix Kimi TUI flow: "搜索 Moonshot AI" not "Custom Provider" | Line 211 |
| 🔴 P0 | Remove unsupported `"fallback"` key | Line 407 |
| 🔴 P0 | Fix Anthropic model names in multi-provider example | Lines 368-370 |
| 🔴 P0 | Remove unsupported `"proxy"` from provider config | Lines 628-632 |
| 🟡 P1 | Add `"env"` array to all provider configs | Lines 157, 227, 306 |
| 🟡 P1 | Verify `deepseek-reasoner` maxOutput | Line 170 |

---

## References

1. OpenCode Configuration Schema: `opencode.ai/config.json`
2. OpenCode TypeScript Source: `packages/opencode/src/config/provider.ts`
3. Official Provider Documentation: `opencode.ai/docs/providers/`
