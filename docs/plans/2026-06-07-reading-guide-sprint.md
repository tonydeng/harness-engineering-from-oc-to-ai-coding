# Sprint 2: 阅读指引补齐 ✅ 已完成

> **目标**：为全书 12 篇缺少 `> **⏱ 时间有限？先读这些：**` 的文章添加阅读指引
> **完成日期**：2026-06-07

## 范围

| # | 文件 | 当前行数 | 前置内容 |
|---|------|:--------:|---------|
| 1 | `src/00-guide/quick-start.md` | 301 | "读完本文，你将在..." → 无文章概述区块 |
| 2 | `src/01-introduction/chinese-ecosystem.md` | — | 有文章概述 |
| 3 | `src/01-introduction/ecosystem-comparison.md` | — | 有文章概述 |
| 4 | `src/01-introduction/failure-cases.md` | — | 有文章概述 |
| 5 | `src/04-workflows/prometheus-mode.md` | — | 有文章概述 |
| 6 | `src/06-advanced/agents-dot-md.md` | 481 | 有文章概述 |
| 7 | `src/06-advanced/context-compression.md` | — | 有文章概述 |
| 8 | `src/06-advanced/feature-flags.md` | 308 | 有文章概述 |
| 9 | `src/06-advanced/observability-reference.md` | 333 | 参考文档，无文章概述 |
| 10 | `src/06-advanced/performance-tuning.md` | — | 有文章概述 |
| 11 | `src/06-advanced/prompt-caching.md` | — | 有文章概述 |
| 12 | `src/06-advanced/token-budget.md` | — | 有文章概述 |
| 13 | `src/appendix-a/glossary.md` | 324 | 术语表，无文章概述 |

## 格式

### 有 `## 文章概述` 的文件

在文章概述段落后插入（作为区块引用新行）：

```
> **⏱ 时间有限？先读这些：** 主题1 → 主题2 → 主题3 → 主题4
```

### 无 `## 文章概述` 的文件

- `glossary.md`: 在 `# 术语表` 后、`## A` 前插入：
  ```
  > **⏱ 时间有限？先读这些：** 按字母索引 → 前 5 个核心术语
  ```

- `quick-start.md`: 在 `读完本文，你将在...` 段落之后、`## 前置条件` 前插入。
- `observability-reference.md`: 在文件开头附近插入。

## 执行策略

1 agent 处理全部 12 个文件（任务最小，无需拆分）。
每个文件只需读取开头确认结构，追加 1 行。

## 验证

- `mdbook build` 零错误
- 12 个文件全部确认添加
