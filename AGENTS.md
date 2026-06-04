# Harness Engineering — AGENTS.md

## 一句话说清

**这是本开源书籍，不是软件项目。** 所有内容都是简体中文 Markdown，用 mdBook v0.4.x 渲染成静态网站。不要跑 npm test、npm run build 这些东西。

## 唯一命令

```bash
mdbook serve    # 本地预览（默认 http://localhost:3000）
mdbook build    # 构建到 _book/（被 .gitignore 忽略，不提交）
```

## 最容易翻车的地方

### 1. 增删文章必须同步 SUMMARY.md

`src/SUMMARY.md` 是 mdBook 的导航命脉。新增/重命名/删除文件后不更新它 → 页面直接 404。没有任何自动检测。

### 2. 内部链接格式（mdBook 规则，错了就 404）

| 场景 | 正确写法 | 错误写法 |
|------|----------|----------|
| 同目录 | `[text](file.md)` | `[text](./file.md)` 也行但多余 |
| 跨目录 | `[text](../target/file.md)` | `[text](target/file.md)` ❌ |
| 指向章节首页 | `[读者导航](00-guide/)` | `[读者导航](00-guide/README.md)` ❌ |
| 从 `src/README.md` 出发 | `[text](chapter/file.md)` | 它在 src/ 根，不需要 `../` |

**原因**：mdBook 把 `README.md` 渲染成 `index.html`，所以链接要写成目录形式。`SUMMARY.md` 例外，它按自身规则写。

### 3. 代码块格式

````
```language:相对路径 {行号}
```
````

语言和路径之间用冒号，路径从项目根相对。示例：
````
```json:examples/opencode-configs/basic.json
```
````

### 4. 品牌名

全书统一 **OpenCode**（大写 C，没有空格）。

### 5. 跨章节引用格式

```
→ [章节名称](相对路径.md)
```

链接文字必须和目标文件的 H1 标题一致。全书不用 `§X.Y` 编号，直接用章节名称。

### 6. 英文术语首次出现

用 **English（中文翻译）** 格式，例如 **Agent（智能体）**。

### 7. Mermaid 图表颜色规范

| 元素 | 色值 |
|------|------|
| Agent | #4A90D9 |
| Skill | #50C878 |
| Workflow | #FF9F43 |
| MCP/外部 | #A66CFF |

方向统一用 TB（top-bottom）。

### 8. 写作原则：说人话，从读者视角写

- 避免抽象隐喻（如"工程流水线"这种需要二次理解的表达）
- 优先用开发者熟悉的日常语言（如"跟 AI 聊天写代码"）
- 每段话回答一个问题：读者读完能做什么/知道什么？
- 13 种读者角色见 `src/00-guide/reading-paths.md`，写作时对号入座

## 项目结构速览

```
src/               ← 正文（8 章 + 附录 A，50 篇文章）
  SUMMARY.md       ← 导航配置文件（改它之前想清楚）
  README.md        ← 书籍首页
  00-guide/        ← 读者导航（阅读路径、角色诊断）
  01-introduction/ ← 简介
  02-core-concepts/← 核心概念
  03-setup/        ← 环境搭建
  04-workflows/    ← 工作流实战
  05-skills/       ← Skill 开发
  06-advanced/     ← 高级话题
  07-case-studies/ ← 案例研究
  appendix-a/      ← 附录
book.toml          ← mdBook 配置（主题、搜索、Mermaid）
theme/             ← 自定义 CSS/JS
docs/              ← 写作计划、PRD、评审报告
examples/          ← 示例配置（opencode-configs/ + skills/）
```

## 写作状态

50 篇文章全部有内容，其中高级话题（06-advanced）和案例研究（07-case-studies）的文章篇幅相对较短（2-7KB），属于初稿阶段，可以迭代扩充。其余章节文章在 15-46KB 之间，相对完整。

## CI

`.github/workflows/deploy-mdbook.yml`：push 到 main 时自动构建并部署到 GitHub Pages。构建输出目录 `_book`（与 `book.toml` 的 `build-dir` 一致）。

## 写完后的验证

```bash
# 检查所有内部 .md 链接
find src -name '*.md' -exec grep -n '\](' {} + | grep '\.md)'

# 验证 SUMMARY.md 所有链接目标存在
awk -F '[()]' '/\.md\)/ {print $2}' src/SUMMARY.md | while read f; do [ -f "src/$f" ] || echo "BROKEN: src/$f"; done

# 本地构建，确认无警告
mdbook build
```
