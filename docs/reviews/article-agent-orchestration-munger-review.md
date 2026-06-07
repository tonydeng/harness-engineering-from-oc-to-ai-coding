# Munger Review: agent-orchestration.md

> **Reviewer**: Charlie Munger (逆向思维 + 激励分析)
> **Article**: `src/02-core-concepts/agent-orchestration.md`
> **Date**: 2026-06-06

---

## Executive Summary

This article fails the **Munger "能力圈" (circle of competence) test**. It claims to describe OpenCode, but the technical details are often wrong or misleading. The "7 种 Agent 类型" framing is **分类谬误 (classification fallacy)** - it mixes different levels of abstraction as if they were equal.

**Core Verdict**: The article is **conceptually sound** but **factually unreliable**. The "马书" comparison is **content padding** - it analyzes Claude Code while claiming relevance to OpenCode. The config file paths are **fabricated** - they don't exist in OpenCode.

---

## 逆向思维检验

### 问题 1: 如果 OpenCode 没有 7 种内置 Agent 类型？

**Claim**: "OpenCode 内置 7 种 Agent 类型"

**Reality**: OpenCode official docs say:
- **2 types**: primary agents, subagents
- **5 user-facing agents**: Build, Plan, General, Explore, Scout
- **3 hidden**: compaction, title, summary
- **Total**: 8 instances, not 7

**Inversion Result**: The "7 种" claim is **wrong**. The actual count is 8 (missing "summary"). The classification framework is **incomplete**.

**Why This Matters**: Readers will trust a "7 types" framework. If it's wrong at the foundation, everything built on it is suspect.

---

### 问题 2: 如果 Plan 模式不是 "拒绝所有"？

**Claim**: "默认拒绝所有文件编辑和命令执行"

**Reality**: OpenCode uses `ask` mode - **prompts for confirmation**, does NOT outright reject.

**Inversion Result**: The article claims "automatic denial" but reality is "ask user". This is **misleading security documentation**. Users expecting automatic rejection will get prompts instead.

**Why This Matters**: Security claims must be accurate. "拒绝所有" is a **false promise** that undermines trust in the safety model.

---

### 问题 3: 如果 Subagent 权限不是只读？

**Claim**: "Subagent 默认不能编辑文件"

**Reality**: @general has **full tool access** (including file writes). Only @explore and @scout are read-only.

**Inversion Result**: The claim "all subagents are read-only" is **factually wrong for @general**.

**Why This Matters**: If users rely on subagents being read-only, they could make unwanted file changes. This is a **security risk**.

---

### 问题 4: 如果 `opencode.yml` 不存在？

**Claim**: `opencode.yml` as a config file

**Reality**: OpenCode uses `opencode.json` (JSON only, no YAML support).

**Inversion Result**: The config file **does not exist**. Users following this article will get errors.

**Why This Matters**: **Production-breaking error**. Users will waste time debugging non-existent files.

---

### 问题 5: 如果 "马书第 4 章" is wrong?

**Claim**: "马书第 4 章 Agent Loop"

**Reality**: The "马书" (ZhangHanDong/harness-engineering-from-cc-to-ai-coding) puts Agent Loop in **Chapter 3**, not Chapter 4.

**Inversion Result**: The chapter reference is **wrong by one**. This is a trivial error, but it reveals **careless citation**.

**Why This Matters**: If the chapter number is wrong, how many other citations are inaccurate?

---

## Lollapalooza 效应检测

### 识别出的偏误叠加

| 偏误 | 表现 | 文章的态度 |
|------|------|-----------|
| **分类谬误** | "7 种 Agent 类型" - 混合不同类型层次 | 声称是分类框架 |
| **过度承诺** | "拒绝所有" | 暗示绝对安全 |
| **确认偏误** | @scout only appears here | 未验证 claims |
| **近期偏误** | v1.15.x vs v1.16.x inconsistency | 混用新旧版本 |
| **被剥夺超级反应** | "必须掌握" | 制造紧迫感 |

**Conclusion**: The article exhibits **multiple cognitive biases** simultaneously - a classic Lollapalooza effect. This makes readers **over-trust** claims that should be questioned.

---

## 太困难筐

### 4.1 "7 种 Agent 类型"

**宣称状态**: OpenCode 有 7 种 Agent 类型

**真实状态**: 2 种类型，5-8 个实例（取决于是否计 hidden agents）

**Munger 评价**: **混淆层次**。这是概念上的懒惰，不是严谨的分类。

---

### 4.2 "拒绝所有"

**宣称状态**: Plan mode rejects all edits

**真实状态**: Plan mode uses `ask` (confirmation prompts)

**Munger 评价**: **安全工程的简化**。真正的安全需要验证，不是承诺。

---

### 4.3 "只读 Subagent"

**宣称状态**: All subagents are read-only

**真实状态**: @general has full tool access

**Munger 评价**: **错误的分类**。这是事实错误，不是分类问题。

---

### 4.4 "opencode.yml"

**宣称状态**: OpenCode uses `opencode.yml`

**真实状态**: OpenCode uses `opencode.json`

**Munger 评价**: **虚构的架构**。这不在能力圈内。

---

## 能力圈审计

### 做得好的地方

1. **Agent = Model + Tools + Skills + Memory 公式**: 简洁有效
2. **Plan/Build 模式区分**: 概念正确
3. **OMO 5 core agents**: Verified - Sisyphus, Prometheus, Atlas, Hephaestus, Oracle
4. **Ultrawork 和 Prometheus modes**: Verified

### 做得不好的地方

| 问题 | 严重程度 | 说明 |
|------|----------|------|
| "7 种"分类谬误 | **高** | 混淆类型和实例 |
| Plan mode `ask` vs `deny` | **高** | 安全文档错误 |
| @general write access | **高** | 权限模型错误 |
| `opencode.yml` | **高** | 虚构的文件 |
| 版本不一致 | **中** | v1.15.x vs v1.16.x |
| "马书" 章节 | **中** | Ch.3 vs Ch.4 |
| compaction 阈值 | **低** | 80%/40% 未证实 |

---

## 总结

### 核心问题

> "这篇文章最好的功能是作为**概念框架的目录**——它能帮助读者意识到有哪些维度需要关注。"

> "它最差的功能是作为**技术事实的来源**——它声称准确，但多处细节与实际不符。"

### 三个必须修复的关键错误

1. **Plan mode `ask` not `deny`** - 安全文档错误
2. **@general CAN write files** - 权限模型错误
3. **`opencode.json` not `opencode.yml`** - 虚构的配置

### 一句评价

> "The article is **conceptually sound but factually unreliable**. Like many AI-era technical documents, it captures the right concepts but gets the wrong details."

---

## Actionable Recommendations

### Must Fix

- [ ] Line 183: Plan mode description (deny → ask)
- [ ] Line 206: @general permissions (read-only → write-capable)
- [ ] Line 566: `opencode.yml` → `opencode.json`
- [ ] Line 672: `.opencode/config.jsonc` → `.opencode/oh-my-openagent.jsonc`

### Should Fix

- [ ] Line 12: "7 种" → "8 个实例"
- [ ] Lines 568/674: Unify version numbers (v1.15.x → v1.16.x)
- [ ] Line 288: Remove specific thresholds (80%/40%)
- [ ] Line 776: "马书第 4 章" → "马书第 3 章"

### Consider

- [ ] Line 248-270: Verify @scout validity or add cross-reference

---

*Review generated using Charlie Munger's thinking framework. The purpose is not to dismiss the article, but to identify where its claims exceed its evidence — because that's where the real work is.*
