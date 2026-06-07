# Karpathy-Style Critical Review: Chapter 3 README

**Review Date**: 2026-06-06  
**Target**: `src/03-setup/README.md`  
**Reviewer**: Karpathy Engineering Perspective (engineering pragmatism)

---

## Executive Summary

The Chapter 3 README is **70% accurate** with **3 critical factual errors** that mislead readers on:

1. **Time commitment** (10 min claimed vs 20–30 min actual)
2. **GLM provider coverage** (claimed, not delivered)
3. **Workflow binding capability** (claimed, not implemented)

These are not typos—they are **misleading promises** that will frustrate readers.

---

## Findings

### 🔴 Finding 1: Time Estimate Discrepancy

**README Claim (Line 13):**
```
10 分钟内完成 OpenCode 安装和第一个 AI 编程任务
```

**Article Actual (quickstart.md Lines 3, 7):**
```
预计 20-30 分钟完成 OpenCode 安装和第一个 AI 编程任务
快速上手的定位是让读者在约 20 分钟内完成...
```

**Engineering Reality:**
- README: 10 minutes
- Article: 20–30 minutes
- **Gap: 2–3×** (the article undercuts its own README claim)

**Correction:**
```diff
- 10 分钟内完成 OpenCode 安装和第一个 AI 编程任务
+ 20–30 分钟内完成 OpenCode 安装和第一个 AI 编程任务
```

---

### 🔴 Finding 2: GLM Provider Not Covered

**README Claim (Line 16):**
```
国内大模型 API 接入（DeepSeek/Qwen/GLM 等）与网络代理设置
```

**Article Reality (chinese-providers.md):**
- DeepSeek section: ✅ Line 119
- Kimi section: ✅ Line 194
- Qwen section: ✅ Line 273
- **GLM/Zhipi section: ❌ 0 mentions**

GLM only appears in `oh-my-openagent-setup.md` (Line 173, 232) as passing references—not as a configuration guide.

**Correction:**
```diff
- 国内大模型 API 接入（DeepSeek/Qwen/GLM 等）
+ 国内大模型 API 接入（DeepSeek/Qwen/Kimi 等）
```

---

### 🔴 Finding 3: "Workflow Binding" is Overstated

**README Claim (Line 14):**
```
opencode.json 的完整参考：Agent 定义、Skill 注册、Workflow 绑定
```

**Article Reality (opencode-config.md):**
- Agent 定义: ✅ Lines 161–217
- Skill 注册: ✅ Lines 439–461
- **Workflow 绑定: ❌ No dedicated chapter or configuration field**

The article mentions "类别路由 (Category Routing)" as "工作流引擎的调度核心" (Line 613), but **category routing is not workflow binding**. It's about model selection, not defining Workflow objects.

**Correction:**
```diff
- opencode.json 的完整参考：Agent 定义、Skill 注册、Workflow 绑定
+ opencode.json 的完整参考：Agent 定义、Skill 注册、类别路由
```

---

## Confirmed Accurate Elements

| Claim | Verdict | Evidence |
|-------|---------|----------|
| "5 articles" | ✅ Accurate | 5 .md files + 1 README.md |
| All linked files exist | ✅ Confirmed | quickstart.md, opencode-config.md, oh-my-openagent-setup.md, chinese-providers.md, multi-env-setup.md |
| Cross-references (`../02-core-concepts/`, `../04-workflows/`) | ✅ Correct | Directory-style format per mdBook rules |
| Chapter structure (Ch2→Ch3→Ch4) | ✅ Validated | Bidirectional links exist |
| OMO 11-Agent system description | ✅ Accurate | Line 7 of oh-my-openagent-setup.md |
| GitHub stars claim (61K+) | ✅ Verified | 61,159 stars / 4,949 forks (as of 2026-06-05) |

---

## Secondary Issues (Chapter-Level, Not README)

⚠️ **Note**: These are in the *articles themselves*, not the README. They affect reader outcomes:

1. **`multi-env-setup.md` uses wrong env var syntax**
   - Claims: `${ENV_VAR}` (Line 114)
   - Reality: `{env:VAR_NAME}` (all other files use this)
   - **Impact**: Copy-paste configs will break

2. **`multi-env-setup.md` uses invalid `logging` field**
   - Uses: `"logging": { "level": "...", "file": "..." }`
   - Reality: OpenCode uses `logLevel: "string"` (Line 433 of opencode-config.md)

3. **`multi-provider-hybrid.json` referenced but doesn't exist**
   - chinese-providers.md Line 361: `json:examples/opencode-configs/multi-provider-hybrid.json`
   - File does not exist in examples directory

---

## Recommended Fixes (Order of Priority)

### Immediate (README corrections)

1. **Line 13**: Change "10 分钟内" → "20–30 分钟内"
2. **Line 16**: Change "DeepSeek/Qwen/GLM" → "DeepSeek/Qwen/Kimi"
3. **Line 14**: Change "Workflow 绑定" → "类别路由"

### Important (Article corrections)

4. **`multi-env-setup.md`**: Replace all `${ENV_VAR}` with `{env:ENV_VAR}` (10 occurrences)
5. **`multi-env-setup.md`**: Replace `logging` object with `logLevel` string
6. **Create missing file** `examples/opencode-configs/multi-provider-hybrid.json` OR remove code block annotation

---

## Bottom Line

The Chapter 3 README is **structurally sound** but contains **3 misleading claims** that will cause reader frustration. These are easy to fix—just change 3 words in the README table.

**Engineering principle**: Be conservative in your claims. The 20–30 minute timeline in the article is honest. The 10-minute claim in the README is optimistic marketing that backfires.

---

## Files Audited

- `/src/03-setup/README.md` (19 lines)
- `/src/03-setup/quickstart.md` (684 lines)
- `/src/03-setup/opencode-config.md` (1283 lines)
- `/src/03-setup/oh-my-openagent-setup.md` (725 lines)
- `/src/03-setup/chinese-providers.md` (661 lines)
- `/src/03-setup/multi-env-setup.md` (432 lines)
- `/src/SUMMARY.md` (chapter navigation)
- `/src/02-core-concepts/README.md` (previous chapter link)
- `/src/04-workflows/README.md` (next chapter link)
