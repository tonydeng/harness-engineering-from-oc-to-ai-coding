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

## 工作日志经验总结

以下经验来自 `docs/job-logs/` 中记录的 6 轮 Sprint 实践，每一条都经过真实项目的检验与修正。

### 编排原则

| # | 原则 | 来源 Sprint | 一句话说清 |
|---|------|-----------|-----------|
| 1 | **审计先行** | 005 | 动手修改前先做完整审计，确认哪些已经修过，避免重复劳动 |
| 2 | **调研先于改写** | 007 | 技术文章改写必须先验证当前版本的真实性（重写记忆系统前调研发现 OpenCode 原生无 Memdir） |
| 3 | **并行度优先** | 005, 006 | 无依赖的任务一次部署并行执行，6 个 agent 墙钟时间仅 2 分钟 |
| 4 | **原子化 agent** | 005, exec | 1 agent = 1 file / 1 perspective，prompt 打包完整上下文 |
| 5 | **需求澄清 > 直接开干** | 006 | 用户说"记录 session" → 追问细化后才能产出符合预期的结构化日志 |
| 6 | **单一权威源** | 007 | PRD 和 user-stories 的映射表只维护一份，另一份引用而非复制 |

### Prompt 工程

| # | 实践 | 来源 Sprint | 说明 |
|---|------|-----------|------|
| 1 | **5 段式 prompt 结构** | 005, exec | TASK + EXPECTED OUTCOME + TONE REQUIREMENTS + MUST DO + MUST NOT DO |
| 2 | **读者视角锚定** | 005, 007 | 每段话自问"不给这个信息 agent 会犯错吗"，TONE REQUIREMENTS 要求以读者真实困惑开头 |
| 3 | **视角差异化指令** | exec | Musk/Jobs/Munger/Karpathy 各自风格在输出中可区分，靠 TONE REQUIREMENTS 实现 |
| 4 | **MUST NOT DO 防呆** | exec | 明确禁止删除现有内容、重构、超长度，避免 agent 越界行为 |

### 技术踩坑

| # | 坑 | 来源 Sprint | 修复方案 |
|---|-----|-----------|---------|
| 1 | **Mermaid 跨子图边渲染** | 006 | 子图外部的边连接子图内部节点时，节点ID需加引号避免歧义 |
| 2 | **CI/CD checkout 默认分支** | 006 | 默认分支 main → 实际 master，需显式指定 `ref: main` |
| 3 | **mdBook 版本锁定** | 006 | 不指定 latest 而是锁定 `v0.4.40`，避免 CI 意外行为 |
| 4 | **session_info 调用失败** | 005, exec | 获取会话元数据时必须使用真实 session_id，占位符会导致调用失败 |
| 5 | **多 agent 同文件冲突** | exec | 多个 agent 修改同一文件的相邻区域存在冲突风险，需检测或串行化 |

### 文档规范

| # | 规范 | 来源 Sprint | 说明 |
|---|------|-----------|------|
| 1 | **内容变更 → spec 同步** | 006 | 修改正文后必须即时同步 docs/ 中的规格文档，否则需求文档滞后 |
| 2 | **AGENTS.md 信号密度** | 007 | 每行自问：不给这个信息 agent 会犯错吗？通用知识（安装命令）全部移除 |
| 3 | **统一工作日志格式** | 全部 | 所有 sprint 日志采用本节开头定义的统一模板（基本信息 → 需求 → 团队 → 工作流 → 技能 → 模型 → 变更 → 经验） |
| 4 | **链接修复模式** | 006 | 全局 50+ 链接一次性修复，模式统一：同目录 `[text](file.md)`，跨目录 `[text](../target/file.md)` |

### 后续待办

- [ ] **P2 代码块格式统一**（Sprint 005 遗留）
- [ ] **pre-commit hook 自动检查链接**（Sprint 006 建议）
- [ ] **CI/CD 自动触发测试**（Sprint 006 未完全解决）
- [ ] **session 日志模板标准化**（Sprint 006 建议）

## 写完后的验证

```bash
# 检查所有内部 .md 链接
find src -name '*.md' -exec grep -n '\](' {} + | grep '\.md)'

# 验证 SUMMARY.md 所有链接目标存在
awk -F '[()]' '/\.md\)/ {print $2}' src/SUMMARY.md | while read f; do [ -f "src/$f" ] || echo "BROKEN: src/$f"; done

# 本地构建，确认无警告
mdbook build
```
