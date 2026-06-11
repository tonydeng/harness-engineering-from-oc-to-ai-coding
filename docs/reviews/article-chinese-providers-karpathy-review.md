# DeepSeek/V3.2 - Andrej Karpathy Perspective Review

**Review Date:** 2026-06-06  
**Source:** `src/03-setup/chinese-providers.md`  
**Reviewer:** Karpathy AI Perspective Agent (deepseek-v4-flash)

---

## Executive Summary

This article contains **3 critical errors** that would cause production failures, **4 outdated claims** due to rapid 2026 model releases (DeepSeek V4 and Kimi K2.6), and **3 missing context items** that need clarification.

---

## 🔴 CRITICAL ERRORS (Must Fix)

### 1. DeepSeek V3.2 Doesn't Exist (Lines 19, 77, 123-170)

**Claim:** "DeepSeek-V3.2 采用 MoE 架构，671B 总参数，激活 37B"

**Reality:** 
- **DeepSeek V4 was released April 24, 2026** — 6 weeks before the stated "2026 年 6 月" snapshot
- Current models: `deepseek-v4-flash` (284B total / 13B active) and `deepseek-v4-pro` (1.6T / 49B)
- Legacy IDs `deepseek-chat` and `deepseek-reasoner` **will retire on 2026-07-24**
- V4 models have **1M context window**, not 128K

**Impact:** Article presents superseded technology as current. The legacy model IDs in all config examples will stop working July 24, 2026.

**Fix:** Add V4 as the current generation with pricing $0.14/$0.28 per million tokens (V4-Flash), note V3.2 as historical reference.

---

### 2. DeepSeek Pricing Wrong (Lines 79-80, 123-170)

**Claim:** "DeepSeek-V3.2: $0.28/百万 input, $0.42/百万 output"

**Reality:**
- V4-Flash: **$0.14/M input** (cache miss), **$0.28/M output**
- V4-Pro: $0.435/M input, $0.87/M output
- Legacy deepseek-chat: $0.27/M cache-miss input, $1.10/M output
- No official SKU matches $0.28/$0.42

**Impact:** Cost calculations (lines 547-557) are based on wrong pricing. The "1/30 of GPT-4o" claim at line 23 doesn't match the article's own data.

**Fix:** Update to V4-Flash pricing ($0.14/$0.28) and clarify that legacy pricing differs.

---

### 3. Qwen3-Max USD Pricing Wrong (Lines 79, 525-541)

**Claim:** "Qwen3-Max: $0.35/百万 input, $1.40/百万 output"

**Reality:**
- **International (Singapore) pricing:** $1.20/M input, $6.00/M output (tiered)
- China mainland tier-1 (0-32K): ¥2.5 input, ¥10 output ≈ $0.35/$1.40 at ~7.2 CNY/USD
- The $0.35 figure is a rough CNY→USD conversion of tier-1 China pricing, **not the official international pricing**

**Impact:** The comparison table at lines 525-541 understates Qwen pricing by **~3.4x** for international users.

**Fix:** Either use correct international USD pricing ($1.20/$6.00) or clearly state that ¥2.5/¥10 is China mainland tier-1 pricing with tiered structure.

---

### 4. DeepSeek Reasoner MaxOutput Wrong (Line 171)

**Claim:** `maxOutput: 64000` for `deepseek-reasoner`

**Reality:**
- V3.2 API: max output **8K tokens** (with 32K CoT tokens)
- V4-Flash (which `deepseek-reasoner` now routes to): up to **384K** max output

**Impact:** The config example at lines 153-178 shows incorrect model limits.

**Fix:** Set to 8192 for V3.2 accuracy, or update to reflect V4's 384K max output.

---

### 5. Reasoning Effort Values Wrong (Lines 498-502)

**Claim:** Values `low`, `medium`, `high` are three distinct levels

**Reality:** 
- Official DeepSeek V4 API docs state: `low` and `medium` are **mapped to `high`**
- `xhigh` is mapped to `max`
- Only `high` and `max` produce distinct behavior

**Impact:** The article misleads readers about available parameter values.

**Fix:** Update to valid values: `"high"` (default) and `"max"` (maximum reasoning effort).

---

## ⚠️ OUTDATED CLAIMS

### 6. Kimi K2.6 Missing (Lines 36-51, 77, 198)

**Claim:** Kimi K2.5 ($0.60/$3.00 per million) is the flagship

**Reality:**
- **Kimi K2.6** launched ~May 2026 as current flagship
- K2.5 is still available but previous-generation
- K2.6 pricing: **$0.95/M input, $4.00/M output**
- K2 series discontinued May 25, 2026

**Fix:** Add K2.6 as current flagship, keep K2.5 as cost-effective alternative option.

---

### 7. DeepSeek Context Window Wrong (Lines 78, 123-170)

**Claim:** 128K context

**Reality:**
- V3.2 was 128K context
- **V4 models have 1M context window**
- Legacy model IDs (`deepseek-chat`, `deepseek-reasoner`) now route to V4-Flash (1M context)

**Fix:** Update context values and note the V4 upgrade.

---

### 8. Kimi International API Endpoint Missing (Line 216)

**Claim:** Only `https://api.moonshot.cn/v1` is listed

**Reality:**
- `https://api.moonshot.cn/v1` — China region
- `https://api.moonshot.ai/v1` — International users

**Fix:** Document both endpoints for clarity.

---

## ℹ️ MISSING CONTEXT

### 9. Qwen Tiered Pricing Not Explained (Line 79)

**Reality:** Qwen3-Max uses tiered pricing:
- 0–32K tokens: ¥2.5/¥10 (China) / $1.2/$6.0 (International)
- 32K–128K tokens: ¥4/¥16 / $1.6/$6.4
- 128K–256K tokens: ¥7/¥28 / higher rates

**Fix:** Add tiered pricing structure explanation.

---

### 10. Codeforces Claim Needs Qualification (Line 24)

**Claim:** "在 Codeforces 算法竞赛评测中超越所有非 o1 类模型"

**Reality:**
- V3.2 (Thinking): 2386 Codeforces rating
- GPT-5 High: 2537
- Gemini 3.0 Pro: 2708
- **V3.2-Speciale**: 2701 (Grandmaster)

The "非 o1 类" qualifier is misleading since GPT-5 and Gemini 3.0 Pro are also reasoning models.

**Fix:** Be more precise: "标准 API 模型 2386 分；Speciale 变体达到 2701 分（Grandmaster 级别），超越 GPT-5。"

---

## ✅ VERIFIED CORRECT

| Claim | Verdict | Notes |
|-------|---------|-------|
| DeepSeek-V3.2 MoE, 671B total, 37B active | ✅ | Correct for V3.2 (arXiv paper) |
| API endpoint `https://api.deepseek.com` | ✅ | Confirmed |
| API endpoint `https://api.moonshot.cn/v1` | ✅ | Correct for China |
| API endpoint `https://dashscope.aliyuncs.com/compatible-mode/v1` | ✅ | Confirmed |
| Kimi 256K context window | ✅ | 262,144 tokens |
| `enable_thinking` for Qwen | ✅ | Correct parameter |
| Temperature/top_p recommendations | ✅ | Practical, though not official defaults |
| Cache discount percentages | ✅ | Approximately correct |

---

## Summary of Required Changes

| Priority | Fix | Lines |
|----------|-----|-------|
| 🔴 P0 | DeepSeek V3.2 → V4 update | 19, 77, 78, 123-170 |
| 🔴 P0 | Update DeepSeek pricing to V4-Flash ($0.14/$0.28) | 79-80, 525-541 |
| 🔴 P0 | Fix Qwen USD pricing ($1.20/$6.00 international) | 79, 525-541 |
| 🔴 P0 | Fix deepseek-reasoner maxOutput to 8192 or 384000 | 171 |
| 🔴 P0 | Update reasoning_effort to `high`/`max` only | 498-502 |
| 🔴 P0 | Add Kimi K2.6 as flagship | 36-51, 77, 198 |
| 🔴 P0 | Add deprecation warning for legacy model IDs | Throughout |
| 🟡 P1 | Add K2.6 pricing ($0.95/$4.00) | 36-51 |
| 🟡 P1 | Add Qwen tiered pricing explanation | 79, 301-341 |
| 🟡 P1 | Add Kimi international API endpoint | 216 |
| 🟡 P1 | Refine Codeforces claim | 24 |

---

## References

1. DeepSeek V4 Release Notes: April 24, 2026
2. DeepSeek API Documentation: `api-docs.deepseek.com`
3. Kimi Platform: `platform.kimi.ai`, `platform.moonshot.cn`
4. Alibaba Cloud DashScope: `help.aliyun.com`
5. Qwen Pricing: `dashscope.aliyuncs.com`
