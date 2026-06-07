# Technical Lead Review: agent-orchestration.md

> **Reviewer**: Technical Lead (生产环境验证)
> **Article**: `src/02-core-concepts/agent-orchestration.md`
> **Date**: 2026-06-06

---

## Executive Summary

This review focuses on **production-readiness** of the technical claims. The article provides a solid conceptual framework for OpenCode agent orchestration, but contains **3 critical technical errors** that would cause immediate issues for readers attempting to apply this knowledge in production.

---

## Verified Against Sources

| Source | URL |
|--------|-----|
| Official OpenCode Docs | https://opencode.ai/docs/agents |
| OpenCode GitHub | https://github.com/anomalyco/opencode |
| OMO GitHub | https://github.com/code-yeongyu/oh-my-openagent |
| "马书" GitHub | https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding |

---

## Critical Technical Issues (Must Fix Before Publication)

### 1. Plan Mode Permission Model - **❌ PRODUCTION-BREAKING**

**Line 183**: "Plan Agent（规划模式）——**只读分析型 Agent，默认拒绝所有文件编辑和命令执行**"

**Actual Behavior** (from official docs):
```json
{
  "edit": "ask",  // Prompts user for confirmation, does NOT deny outright
  "bash": "ask"
}
```

**Problem**: The article claims Plan mode "rejects all" (拒绝所有). This is **factually wrong**. Plan mode uses `ask` mode - it prompts users for confirmation, but does NOT automatically reject.

**Production Impact**:
- Users following this article expecting automatic rejection will be confused when they get confirmation prompts
- Security documentation claiming "automatic denial" is misleading
- Could lead to users bypassing safety mechanisms expecting them to be "always on"

**Required Fix**:
```markdown
"Plan Agent（规划模式）——只读分析型 Agent，文件编辑和命令执行默认需要用户确认（ask 模式）"
```

### 2. @general Subagent Write Permissions - **❌ PRODUCTION-BREAKING**

**Line 206**: "Subagent 默认不能编辑文件"

**Official OpenCode Documentation**:
> "**@general**: A general-purpose agent... **Has full tool access (except todo), so it can make file changes when needed.**"

**Problem**: The article claims ALL subagents are read-only. This is **fundamentally wrong**.

- ✅ @explore: read-only
- ✅ @scout: read-only  
- ❌ @general: **full tool access including file writes**

**Production Impact**:
- Users relying on @general as "read-only" could inadvertently make unwanted file changes
- Security model documentation is factually incorrect
- Trust boundary diagrams are misleading

**Required Fix** (lines 206-210):
```markdown
Subagent 默认不能编辑文件，**但 @general 例外**——它可以执行文件编辑和命令执行（除非显式限制）。@explore 和 @scout 才是真正的只读 Agent。
```

**Related Files to Fix**:
- Line 336-341: Trust boundary diagram shows all subagents as read-only - **update to show @general can write**
- Line 511-515: Permission isolation diagram - **update for @general**
- Line 525: "让'思考者'无法碰代码" - **misleading, @general IS an executor**

### 3. Config File Paths - **❌ PRODUCTION-BREAKING**

**Line 566**: `opencode.yml`  
**Line 672**: `.opencode/config.jsonc`

**Actual Files**:
- OpenCode main config: `opencode.json` (JSON ONLY, no YAML support)
- OMO config: `.opencode/oh-my-openagent.jsonc`

**Problem**: Users following this article will:
1. Create `opencode.yml` which **does not exist** in OpenCode
2. Try to use `.opencode/config.jsonc` which is **not the OMO config path**

**Production Impact**:
- Immediate configuration errors for users
- Wasted time debugging non-existent files
- Lost trust in the documentation

**Required Fix**:
- Line 566: Change `opencode.yml` to `opencode.json`
- Line 672: Change `.opencode/config.jsonc` to `.opencode/oh-my-openagent.jsonc`

---

## High Priority Issues (Should Fix)

### 4. Version Number Inconsistency

**Line 568**: `Requires OpenCode >= v1.16.x, OMO >= v4.7.x`  
**Line 674**: `Requires OpenCode >= v1.15.x, OMO >= v4.5.x`

**Current Versions** (from src/00-guide/README.md):
- OpenCode: v1.16.2
- oh-my-openagent: v4.7.5

**Problem**: Line 674 uses outdated version numbers. This creates confusion about which versions are required.

**Fix**: Unify all version references to `OpenCode >= v1.16.x, OMO >= v4.7.x`

### 5. Agent Count Classification

**Line 12**: "OpenCode 内置 7 种 Agent 类型"

**Official OpenCode** (https://opencode.ai/docs/agents):
- **2 types**: primary agents, subagents
- **5 user-facing**: Build, Plan, General, Explore, Scout
- **3 hidden**: compaction, title, summary
- **Total named instances**: 8 (not 7)

**Problem**: The article conflates "types" with "instances" and says "7 types" when:
- Official count is **8 instances** (missing "summary")
- Agent **types** are only **2** (primary/subagent), not 7

**Fix**: "OpenCode 内置 2 种 Agent 类型（Primary Agent 和 Subagent），5 个用户调用 Agent（Build/Plan/General/Explore/Scout），plus 3 个后台系统进程（compaction/title/summary）"

### 6. "马书" Chapter Reference

**Line 776**: "马书第 4 章"

**Actual "马书" structure** (https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding):
- **Chapter 3**: Agent Loop (第 3 章)
- **Chapter 4**: Tool Orchestration (第 4 章)

**Problem**: Agent Loop is in **Chapter 3**, not Chapter 4.

**Fix**: Change "马书第 4 章" to "马书第 3 章"

### 7. compaction Thresholds

**Line 288**: "80% 占用" → "40% 占用"

**Problem**: These specific percentages (80%, 40%) are not documented in official OpenCode. Compaction behavior is heuristics-based and varies by context.

**Fix**: "接近上下文窗口上限时自动触发" and "释放 Token 空间" without specific numbers.

---

## Medium Priority Issues (Consider Fixing)

### 8. @scout Agent Validity

**Lines 248-270**: Introduces @scout as OpenCode native Subagent.

**Problem**: @scout **only appears in this article**. It's not mentioned elsewhere in OpenCode docs. Could be:
- Recent addition not yet documented elsewhere
- OMO-specific agent misclassified as native
- Fabrication

**Fix**: Add cross-reference or note "社区扩展" if uncertain.

### 9. Trust Boundary Diagram

**Lines 310-355**: Shows all Subagents as read-only.

**Fix**: Update to show @general with write access.

---

## Production Readiness Checklist

| Category | Status | Notes |
|----------|--------|-------|
| **Agent Types** | ⚠️ Needs Fix | "7 种" → "8 个实例，2 种类型" |
| **Permission Model** | ❌ **Wrong** | Plan=`ask` not `deny`, @general CAN write |
| **Config Files** | ❌ **Wrong** | `opencode.yml` and `.opencode/config.jsonc` don't exist |
| **Version Numbers** | ⚠️ Inconsistent | v1.15.x → v1.16.x |
| **OMO Agents** | ✅ Verified | Sisyphus/Prometheus/Atlas/Hephaestus/Oracle |
| **Agent Loop** | ✅ Verified | "马书" exists, Ch.3 not Ch.4 |
| **Security Model** | ⚠️ Misleading | "拒绝所有" → "ask 模式" |
| **Hidden Agents** | ✅ Verified | compaction/title/summary exist |

---

## Files Requiring Updates

### Primary: `src/02-core-concepts/agent-orchestration.md`
- Line 12: Agent count correction
- Line 183: Plan mode permissions
- Line 206-210: @general write access
- Lines 288-293: compaction thresholds
- Line 336-341: Trust boundary diagram
- Line 511-515: Permission isolation diagram
- Line 566: `opencode.yml` → `opencode.json`
- Line 568: Keep v1.16.x/v4.7.x
- Line 672: `.opencode/oh-my-openagent.jsonc`
- Line 674: v1.15.x → v1.16.x
- Line 776: "马书第 4 章" → "马书第 3 章"

### Secondary: `src/01-introduction/why-opencode.md`
- Line 238: Same `opencode.yml` → `opencode.json` issue

---

## Recommended Revision Order

1. **Fix critical production-breaking issues first** (Plan mode, @general permissions, config paths)
2. **Then fix version number inconsistency** (v1.15.x → v1.16.x)
3. **Then fix secondary issues** (Agent count, compaction thresholds, @scout validity)
4. **Finally update related files** (why-opencode.md)
5. **Run mdbook build** to verify no breakage
6. **Update docs/reviews/** directory with review files

---

## Conclusion

The article provides a solid conceptual framework for OpenCode agent orchestration. However, **3 critical technical errors** would immediately break production usage:

1. **Plan mode is `ask` not `deny`** - users expecting automatic denial will get confirmation prompts
2. **@general CAN write files** - not read-only as claimed
3. **Wrong config file paths** - `opencode.yml` and `.opencode/config.jsonc` don't exist

These must be fixed before publication. The remaining issues are clarifications and should be addressed as time permits.

**Production Verdict**: **❌ NOT PRODUCTION-READY** until critical fixes are applied.

---

<Review generated by Technical Lead review process.
Focus: Production-readiness, technical accuracy, configuration correctness.
</Review>
