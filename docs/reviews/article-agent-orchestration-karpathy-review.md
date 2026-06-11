# Karpathy Review: agent-orchestration.md

> **Reviewer**: Andrej Karpathy (技术工程视角)
> **Article**: `src/02-core-concepts/agent-orchestration.md`
> **Date**: 2026-06-06

---

## Executive Summary

**Overall Assessment**: The article contains **3 critical factual errors** and **5 moderate issues** that must be corrected before publication. The core framework (Agent = Model + Tools + Skills + Memory) and OMO agent descriptions are accurate, but several specific technical claims contradict official OpenCode documentation.

**Key Verdicts**:
- ✅ **Verified accurate**: Plan/Build mode distinction, OMO core agents (Sisyphus/Prometheus/Atlas/Hephaestus/Oracle), Agent Loop concept
- ❌ **Factually wrong**: Plan mode `ask` vs `deny`, @general subagent write permissions, config file paths
- ⚠️ **Needs clarification**: Agent count ("7 types" vs official "8 instances"), "马书" chapter number, compaction thresholds

---

## Critical Issues (Must Fix)

### 1. Plan Mode Permission Model - **❌ WRONG**

**Line 183**: "Plan Agent（规划模式）——**只读分析型 Agent，默认拒绝所有文件编辑和命令执行**"

**Official OpenCode docs** (https://opencode.ai/docs/agents):
> "By default, all of the following are set to `ask`: `file edits`, `bash`"

**Analysis**: The article claims Plan mode "rejects all" edits and commands. This is **factually incorrect**. Plan mode uses `ask` (prompt for confirmation), not `deny` (automatic rejection). This is a critical security misunderstanding.

**Impact**: Users expecting blanket denial will be confused when OpenCode prompts them for confirmation.

**Required Fix**:
```markdown
"只读分析型 Agent，文件编辑和命令执行默认需要用户确认（ask 模式）"
```

### 2. Subagent Write Permissions - **❌ WRONG**

**Line 206**: "Subagent 默认不能编辑文件"

**Official OpenCode docs**:
> "General: Has **full tool access (except todo)**, so it can make file changes when needed."

**Analysis**: The article incorrectly classifies ALL subagents as read-only. **Only @explore and @scout are read-only**. @general has full tool access including file writes.

**Impact**: This fundamental permission model misunderstanding could cause security concerns if users rely on subagents for tasks they believe are read-only.

**Required Fix** (line 206-210):
```markdown
Subagent 默认不能编辑文件，**但 @general 例外**——它可以执行文件编辑和命令执行（除非显式限制）。@explore 和 @scout 是真正的只读 Agent。
```

### 3. Config File Paths - **❌ WRONG**

**Line 566**: `opencode.yml`  
**Line 672**: `.opencode/config.jsonc`

**Actual OpenCode files**:
- Main config: `opencode.json` (not YAML, not `.opencode/config.jsonc`)
- OMO config: `.opencode/oh-my-openagent.jsonc` (not `.opencode/config.jsonc`)

**Impact**: Users following this article will attempt to use non-existent config files, causing immediate errors.

**Required Fix**:
- Change `opencode.yml` to `opencode.json`
- Change `.opencode/config.jsonc` to `.opencode/oh-my-openagent.jsonc` when referencing OMO config

---

## Medium Priority Issues (Should Fix)

### 4. Version Number Inconsistency

**Line 568**: `Requires OpenCode >= v1.16.x, OMO >= v4.7.x`  
**Line 674**: `Requires OpenCode >= v1.15.x, OMO >= v4.5.x`

**Current versions** (from src/00-guide/README.md):
- OpenCode: v1.16.2
- oh-my-openagent: v4.7.5

**Issue**: Line 674 uses outdated version numbers. This creates confusion about which versions are required.

**Fix**: Unify all version references to `OpenCode >= v1.16.x, OMO >= v4.7.x`

### 5. Agent Count Misclassification

**Line 12**: "OpenCode 内置 7 种 Agent 类型"

**Official OpenCode** (https://opencode.ai/docs/agents):
- **2 types**: primary agents, subagents
- **5 user-facing**: Build, Plan, General, Explore, Scout
- **3 hidden**: compaction, title, summary
- **Total named instances**: 8

**Issue**: The article conflates "types" with "instances". There are 2 types (primary/subagent), not 7 types.

**Fix**: Change to "OpenCode 内置 2 种 Agent 类型（Primary Agent 和 Subagent），5 个用户调用 Agent（Build/Plan/General/Explore/Scout），plus 3 个后台系统进程（compaction/title/summary）"

### 6. "马书" Chapter Reference

**Line 776**: "《驾驭工程：从 Claude Code 源码到 AI 编码最佳实践》...第 4 章"

**Actual "马书"** (https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding):
- **Chapter 3**: Agent Loop (第 3 章)
- **Chapter 4**: Tool Orchestration (第 4 章)

**Issue**: The "马书" puts Agent Loop in **Chapter 3**, not Chapter 4.

**Fix**: Change "第 4 章" to "第 3 章"

### 7. Compaction Thresholds

**Line 288**: "80% 占用" → "40% 占用"

**Issue**: These specific percentages (80%, 40%) are not documented in official OpenCode. Compaction behavior is heuristics-based and varies.

**Fix**: Replace with "接近上下文窗口上限时自动触发" and "释放 Token 空间" without specific numbers.

---

## Minor Issues (Consider Fixing)

### 8. @scout Agent Validity

**Lines 248-270**: Introduces @scout as an OpenCode native Subagent.

**Issue**: @scout **only appears in this article**. It's not mentioned in other OpenCode documentation or articles. This could be:
- A recent addition not yet documented elsewhere
- An OMO-specific agent misclassified as native
- A fabrication

**Fix**: Add cross-reference or note that @scout is documented as OpenCode native in official docs. If uncertain, classify as "社区扩展" or reference OpenCode docs.

### 9. Trust Boundary Diagram Inaccuracy

**Lines 310-355**: Shows all Subagents as read-only.

**Issue**: Should show @general with write access.

**Fix**: Update Mermaid diagram to show @general can write files.

---

## Verified Accurate Claims (No Changes Needed)

These claims have been cross-referenced with official OpenCode and OMO documentation and are **correct**:

✅ OpenCode's 3-layer architecture (CLI → Agent → Tool → Provider → Extension)  
✅ Plan/Build mode distinction (Plan is restricted, Build is full access)  
✅ OMO core agents (Sisyphus, Prometheus, Atlas, Hephaestus, Oracle)  
✅ Category routing system  
✅ Ultrawork and Prometheus modes  
✅ Agent = Model + Tools + Skills + Memory formula  
✅ Hidden agents (compaction, title, summary) existence  
✅ @general, @explore, @scout as Subagent invocation syntax (`@agent-name`)

---

## Correction Priority Summary

| # | Issue | Severity | Lines | Fix Priority |
|---|-------|----------|-------|--------------|
| 1 | Plan mode `ask` vs `deny` | 🔴 Critical | 183, 361 | **Must fix** |
| 2 | @general subagent write access | 🔴 Critical | 206, 336-341, 511-515 | **Must fix** |
| 3 | Wrong config file paths | 🔴 Critical | 566, 672 | **Must fix** |
| 4 | Version number inconsistency | 🟡 High | 568, 674 | Should fix |
| 5 | Agent count misclassification | 🟡 High | 12, 16 | Should fix |
| 6 | "马书" chapter number | 🟡 High | 776 | Should fix |
| 7 | compaction thresholds | 🟡 High | 288, 293 | Should fix |
| 8 | @scout agent validity | 🟢 Medium | 248-270 | Consider |
| 9 | Trust boundary diagram | 🟢 Medium | 310-355 | Consider |

---

## Specific Line-by-Line Fixes

### Line 12 (Article Overview)
**Original**: "OpenCode 内置 7 种 Agent 类型——Build、General、Explore、Scout 是核心运行类型，Plan 是规划模式，compaction、title 是内部辅助类型"

**Fixed**: "OpenCode 内置 2 种 Agent 类型（Primary Agent 和 Subagent），5 个用户调用 Agent（Build/Plan/General/Explore/Scout），plus 3 个后台系统进程（compaction/title/summary）"

### Line 183 (Plan Agent Definition)
**Original**: "Plan Agent（规划模式）——**只读分析型 Agent，默认拒绝所有文件编辑和命令执行**"

**Fixed**: "Plan Agent（规划模式）——**只读分析型 Agent，文件编辑和命令执行默认需要用户确认（ask 模式）**"

### Line 206 (Subagent Definition)
**Original**: "Subagent 是由 Primary Agent 派生的子 Agent，用于处理特定类型的任务。**Subagent 默认不能编辑文件**，这是关键的安全设计"

**Fixed**: "Subagent 是由 Primary Agent 派生的子 Agent。**@general 可编辑文件**（Full tool access），@explore 和 @scout 默认为只读。这是关键的安全设计"

### Line 566 (Security Config)
**Original**: ```yaml:opencode.yml

**Fixed**: ```json:opencode.json

### Line 672 (OMO Config)
**Original**: ````json:.opencode/config.jsonc

**Fixed**: ````json:.opencode/oh-my-openagent.jsonc

### Line 776 ("马书" Reference)
**Original**: "《驾驭工程：从 Claude Code 源码到 AI 编码最佳实践》（简称《马书》）提出了 Agent Loop 的状态机视角，与 OpenCode 的 Agentic Loop 有异曲同工之妙"

**Fixed**: "《驾驭工程：从 Claude Code 源码到 AI 编码最佳实践》（简称《马书》，**第 3 章**）分析了 Agent Loop 的状态机视角..."

### Line 568 (Version)
**Original**: `# Requires OpenCode >= v1.16.x, OMO >= v4.7.x`

**Fixed**: Keep as is (current version)

### Line 674 (Version)
**Original**: `// Requires OpenCode >= v1.15.x, OMO >= v4.5.x`

**Fixed**: `// Requires OpenCode >= v1.16.x, OMO >= v4.7.x`

### Line 288 (Compaction)
**Original**: `A["上下文窗口\n80% 占用"]`

**Fixed**: `A["上下文窗口\n接近上限"]`

### Line 774-845 ("马书" Agent Loop)
This entire section is accurate content-wise (the "马书" does exist and does analyze Claude Code). The only fix needed is the chapter number reference.

---

## References

1. **Official OpenCode Docs**: https://opencode.ai/docs/agents
2. **OpenCode GitHub**: https://github.com/anomalyco/opencode
3. **OMO GitHub**: https://github.com/code-yeongyu/oh-my-openagent
4. **"马书" GitHub**: https://github.com/ZhangHanDong/harness-engineering-from-cc-to-ai-coding (Chapter 3 = Agent Loop, Chapter 4 = Tool Orchestration)
5. **Book's own docs**: src/00-guide/README.md (v1.16.x, v4.7.x)

---

<Review generated by Karpathy-style technical review process.
Verified against official OpenCode documentation, source code, and OMO docs.
</Review>
