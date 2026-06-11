# OpenCode 配置审查 — Munger 思维模型视角

**审查日期**: 2026-06-06
**审查者**: Charlie Munger（思维操作系统）
**审查文件**: `src/03-setup/opencode-config.md`

---

## 开场

我很少读技术文档。但既然让我看，我就用我惯用的方法：**不找它做对了什么，找它自相矛盾的地方**。一份跟自己打架的文档比一份错误的文档更危险——前者让读者不知道该信什么。

这篇文章的问题是：它有时在说真话，有时在编造方便自己的故事。两个声音交替出现，读者读到最后已经分不清哪个是哪个。

---

## 问题 1：Compaction 配置——同一篇文章里出了两个版本

### 事实

**版本 A**（第 397-407 行，Compaction 配置段）：

```json
{
  "compaction": {
    "auto": true,
    "prune": true,
    "tail_turns": 2,
    "preserve_recent_tokens": 4096,
    "reserved": 1024
  }
}
```

字段：`auto`、`prune`、`tail_turns`、`preserve_recent_tokens`、`reserved`

**版本 B**（第 1077-1085 行，成本管控·策略四）：

```json
{
  "compaction": {
    "enabled": true,
    "threshold": 0.8,
    "strategy": "summarize"
  }
}
```

字段：`enabled`、`threshold`、`strategy`

### 分析

两个配置段之间零个字段名重合。`auto` vs `enabled`，`prune` vs —（不存在），`tail_turns` vs —，`threshold` 和 `strategy` 在第一版里根本不存在。

这篇文章相当于说：「你的车有四个轮子：前左、前右、后左、后右。」然后在第 15 页又说：「换胎时拧这些螺丝：主驾驶门把手、副驾驶杯架、后备箱锁扣。」

哪个版本是对的？不知道。但读者如果照着版本 B 配，他的 compaction 配置会静默失效——配置加载器不认识 `enabled`、`threshold`、`strategy` 这三个键，直接忽略。

### 为什么会出现这个矛盾？

我猜作者的激励结构：成本管控章节想要展示「压缩配配置帮省钱」的画面。但真实的 compaction 配置（版本 A）的参数名不够直观（`auto`、`prune`、`tail_turns`），作者觉得「读者看不懂」，于是为了好理解而重命名了字段。

**好心办了坏事。** 你为了让读者理解而编造了一组不存在的配置键。读者理解了概念，但配置跑不起来。这不是教学，是误导。

---

## 问题 2：`categories` 这个顶层键从何而来？

### 事实

第 92-109 行的「核心配置段概览」列出了文章声称的完整顶层键：

`$schema`, `model`, `small_model`, `default_agent`, `provider`, `agent`, `command`, `mcp`, `permission`, `server`, `formatter`, `lsp`, `compaction`, `autoupdate`, `snapshot`

——共计 **14 个**（加 `$schema` 是 15 个）。

第 1006-1071 行的成本管控章节（策略一、二、三）突然引入了一个全新的顶层键：

```json
{
  "categories": {
    "quick": { "model": "fast-model", ... },
    "ultrabrain": { "fallbackChain": [...] }
  }
}
```

这个 `categories` 键**不在**第 92-109 行的概览中。概览里没有它，前文没有任何地方提到过配置中有一个 `categories` 段落。

### 分析

文章前面的类别路由系统（第 609-774 行）讲的是一套基于**任务级别** `category` 字段的机制——你在任务请求中指定 `"category": "ultrabrain"`，系统用配置的 `model`/`small_model` 自行处理。这和使用 `categories` 顶层块来配置完全是两码事。

成本管控章节引入的 `categories` 配置块看起来像是另一个系统的配置方式（或许来自 oh-my-openagent 或某个扩展），但文章从未说明这一点。它被当作 OpenCode 原生配置的一部分呈现，而文章自身的概览已经证明了它不是。

**文章的前半段说地图上有 15 个城市，后半段却在地图画了一个从来没标记过的第 16 个城市。** 读者要么以为前半段漏了，要么以为后半段是编的。

---

## 问题 3：`fallbackChain`——两个降级机制互不承认

### 事实

**机制 A**（第 761-774 行，降级链机制段）：

```
1. 类别使用 model 配置的模型，应用对应 variant
2. 主模型不可用 → 尝试 small_model
3. 仍不可用 → 尝试其他已配置 Provider 中的等效模型
4. 全部失败 → 报错
```

这是一个**内置的、按层级降级**的机制。它依赖 `model` 和 `small_model` 两个全局字符串配置，不需要用户定义列表。

**机制 B**（第 1057-1071 行，成本管控·策略三）：

```json
"categories": {
  "visual-engineering": {
    "fallbackChain": [
      { "providers": ["google", "github-copilot"], "model": "best-capability-model", "variant": "high" },
      { "providers": ["zai-coding"], "model": "balanced-model" },
      { "providers": ["anthropic"], "model": "best-capability-model", "variant": "max" }
    ]
  }
}
```

这是一个**用户显式定义的、按顺序尝试**的 provider/model 列表。它和 `model`/`small_model` 没有关系——它自己指定了每个降级步骤的 provider 和 model。

### 分析

这两个机制的关系是什么？

- `fallbackChain` 是**替代**内置降级链吗？如果配置了 `fallbackChain`，系统就不再走 `model` → `small_model` → 其他 Provider 这条路径？
- `fallbackChain` 是**补充**吗？先走 `model`/`small_model`，都不行再走 `fallbackChain`？
- 如果 `fallbackChain` 和全局 `model` 配置不同（比如全局用 Claude，但 `fallbackChain` 第一步就是 DeepSeek），谁优先？

文章一个字没提。成本和我说我这有两种支付方式——现金和信用卡——但不说它们怎么配合使用。读者只能猜测，而猜测导致错误。

### 额外的矛盾

`fallbackChain` 被嵌套在 `categories` 块里。如果 `categories` 块本身不是有效的 OpenCode 配置（见问题 2），那么 `fallbackChain` 也是一个无效配置。两层嵌套的虚构。

---

## 问题 4：类别路由表说 8 个，图里只有 6 个

### 事实

第 624-633 行的「内置类别一览」表格列了 8 个类别：

| visual-engineering | ultrabrain | deep | artistry | quick | **unspecified-low** | **unspecified-high** | writing |

第 637-686 行的 Mermaid 映射图只画了 6 个：

| visual-engineering | ultrabrain | deep | artistry | quick | writing |

`unspecified-low` 和 `unspecified-high` 在图里消失了。

### 分析

这不是「图简化了一下」的问题。这两个是 **unspecified（未指定）** 类别——当任务没有显式指定类别时的兜底分类。它们是整个路由系统的**默认行为**，是系统核心逻辑的一部分。省略它们等于省略了「如果用户不指定类别会发生什么」这个关键信息。

读者看完图后，以为系统只有 6 个类别。他们会在任务中不指定类别，然后困惑结果为什么不对应图中任何一个。

---

## 问题 5：核心配置概览自称「完整」，但少了 10 个键

### 事实

第 92-109 行的「核心配置段概览」展示了 opencode.json 的顶层结构。文章随后单独配置段解释了以下顶层键：

| 键 | 所在章节 | 是否在概览中 |
|---|---|---|
| `skills` | Skills 配置（第 441 行） | ❌ |
| `reference` | Reference 配置（第 462 行） | ❌ |
| `plugin` | Plugin 配置（第 482 行） | ❌ |
| `disabled_providers` | Provider 控制（第 496 行） | ❌ |
| `enabled_providers` | Provider 控制（第 496 行） | ❌ |
| `share` | Share 配置（第 511 行） | ❌ |
| `attachment` | Attachment 配置（第 521 行） | ❌ |
| `enterprise` | Enterprise 配置（第 545 行） | ❌ |
| `tool_output` | Tool Output 配置（第 557 行） | ❌ |
| `experimental` | Experimental 配置（第 575 行） | ❌ |

概览声称展示「完整结构」，但实际上漏掉了文章自行文档的 **42% 的顶层键**（10/24）。

### 分析

这不是「概览简化了」，因为概览已经包含了 15 个键——它显然是打算展示全部。但它展示的 `$schema` 也算一个「键」的话，那 `skills` 为什么不算？它出现在本文第 441 行，比 `$schema` 更值得在概览中出现。

这种遗漏导致：
- **新手读到概览以为就是全部**——然后被后面不断出现的新键搞晕
- **读者尝试从概览理解配置结构**——得到的是不完整的画面
- **维护者要在概览中加新键**——没人记得，因为漏了 10 个还没修

---

## 问题 6：`read` 工具在权限例子中使用了，但行为不明确

### 事实

第 172 行的 Agent 权限示例：

```json
"permission": {
  "edit": "deny",
  "read": "allow",
  "bash": { "git diff*": "allow", ... }
}
```

权限工具列表中 `read` 标注为「✅ glob 匹配」（第 828 行）。

### 分析

「读取文件」的 `read` 权限在细粒度 glob 模式下意味着什么？如果 `read: "allow"` 是对所有文件读，那设置 `read: { "*.env": "deny", "*": "allow" }` 是否可行？

但更核心的问题是：权限系统控制的是 Agent 的**工具调用**。`read` 作为一个 permission 工具名，对应的是 OpenCode 系统中的哪个实际工具？

假设 `read` 权限控制的是 Agent 调用 `read` 工具的能力，那这个工具本身是只读的，`deny` 它实际限制了什么？如果限制的是读取敏感文件的能力，那用 glob 限定路径更合理——但 `"read": "deny"` 就没法区分文件类型了。

这个问题不是文章的矛盾，但反映了设计上的模糊：**权限系统的抽象层和实际工具层之间有一个 gap，文章没有解释这是映射关系。**

---

## 激励结构分析：作者为什么会写出这些矛盾？

我不想点名批评谁，但我可以分析一下**什么样的激励会导致这些错误**。

### 错误的激励 1：「展示实用技巧」压倒「配配置准确性」

成本管控章节想要给读者提供**立即可用的省钱策略**。这个目标是好的。但为了展示「你可以配置 fallbackChain 来省钱」，作者需要先让 `categories` 配置块存在——于是它存在了，虽然文章其他地方确认不存在。

**好意图 + 不严谨 = 坏文档。**

### 错误的激励 2：「简化」压倒「精确」

Compaction 配置参数名不直观，所以作者重命名为直观的版本。类别太多，所以图里只画 6 个。概览太长，所以只列一半。

**每一次「简化」都是一次有意的失真。** 单个失真不致命，但累积起来，读者得到的是这篇文章作者脑海中的「简化版 OpenCode」，而不是真实的 OpenCode。

### 错误的激励 3：「章节独立性」压倒「全文一致性」

成本管控章节看起来是被单独撰写的，没有参考前面的 Compaction 配置段和核心配置概览。章节作者复制了一份 compaction 示例，但没有发现它和前文矛盾。

这是典型的**大型文档的分工病**：每个人负责一节，没人读完整本。

---

## 逆向思考：如果我是读者，我会栽在哪儿？

| 我做了什么 | 我以为会怎样 | 实际会怎样 |
|---|---|---|
| 按成本章节配 `categories` | 低成本跑所有任务 | 配置被忽略，成本不变 |
| 按成本章节用 `enabled`/`threshold`/`strategy` | 压缩节省 token | 配置被忽略，上下文可能溢出 |
| 按成本章节用 `fallbackChain` | 模型不可用时优雅降级 | 配置被忽略，没有降级 |
| 看了图以为只有 6 个类别 | 理解了路由系统 | 漏了关键的默认行为 |
| 看了概览以为理解了配置结构 | 对配置形成完整认知 | 漏了 42% 的顶层键 |

这些问题里每一个都会导致**静默失败**。配置被加载器忽略，没有错误提示，没有警告。用户以为是系统不工作，其实是配置根本没被读取。

静默失败是世界上最糟糕的错误，因为它让调试变成了猜谜。

---

## 检查清单

### 内部一致性

| 检查项 | 结果 | 说明 |
|--------|------|------|
| Compaction 字段跨段一致 | ❌ | `auto`/`prune`/`tail_turns` ≠ `enabled`/`threshold`/`strategy` |
| `categories` 在概览中声明 | ❌ | 成本章节引入，但概览未包含 |
| 降级机制单一权威描述 | ❌ | 内置降级链与 `fallbackChain` 共存，关系未定义 |
| 类别数量图文一致 | ❌ | 表 8 个，图 6 个 |
| 概览覆盖所有文档化的键 | ❌ | 漏 10/24 个 |

### 事实核查（基于文档自身证据）

| 检查项 | 结果 | 说明 |
|--------|------|------|
| 权限工具列表与 AGENTS.md 工具集一致 | ⚠️ | `list`、`task`、`external_directory`、`question`、`doom_loop` 在 AGENTS.md 无直接对应工具 |
| 配置层级顺序与实际一致 | ⚠️ | 第 6 层「托管配置」优先级最高但标记了「用户无法覆盖」，与「合并而非替换」原则的边界未明确 |

---

## 总结

一篇文章有三个严重的自相矛盾和一个系统性的遗漏问题：

1. **Compaction 配置有两个互斥的版本。** 读者不知道该信哪个，照着任何一个错的那个配，配置会静默失效。

2. **`categories` 配置块凭空出现。** 文章自己的核心概览不包含它，前文也不曾提及，但它被当作有效配置呈现。

3. **`fallbackChain` 与内置降级链的关系未定义。** 两个机制都在说降级，但没说谁覆盖谁、谁补充谁。

4. **核心概览遗漏了 42% 的顶层键。** 文章自称展示完整结构，实际只展示了不到六成。

这些问题的共同根源：**文章在「准确描述」和「让读者好理解」之间反复摇摆，每次摇摆都在牺牲前者。** 结果是一份读起来流畅、用起来崩溃的文档。

芒格的一句话在这里适用：**"It is better to be approximately right than precisely wrong."** 但这里的错误不是「approximately right」——配置键要么存在要么不存在，不存在就是 wrong，没有近似之说。

**我没什么要补充的了。**
