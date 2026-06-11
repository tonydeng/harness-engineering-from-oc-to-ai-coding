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

`src/SUMMARY.md` 是 mdBook 的导航命脉。新增/重命名/删除文件后不更新它 → 页面直接 404。无自动检测。

**CI 已有链接检查**（`.github/workflows/deploy-mdbook.yml` 中的 `Check internal links` 步骤），但只检查 SUMMARY.md 内的目标是否存在，不检查正文内链。

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

语言和路径之间用冒号，路径从项目根相对。Mermaid 块**不需要** path 注解。示例：

````
```json:examples/opencode-configs/basic.json
```
````

全书已全部合规（474 块已标注）。新增代码块时保持此格式。

### 4. 品牌名

全书统一 **OpenCode**（大写 C，没有空格）。
其他品牌速查：**oh-my-openagent**（全小写，连字符），**MCP**（大写），**mdBook**（小写 m，大写 B）。

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
- 用"你能对应上自己的使用场景吗"检验每段话是否够具体

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
theme/             ← 自定义 CSS/JS（含 Vega 图表库、Mermaid、lightbox）
docs/              ← 写作计划、PRD、评审报告、工作日志、PR 记录、Wiki
  job-logs/        ← Sprint 工作日志（9 份）
  reviews/         ← 多视角审阅报告（90+ 份）
  requirements/    ← PRD + user-stories + specs
  plans/           ← 全书大纲 + 分阶段计划
  prs/             ← PR 变更记录
  wiki/            ← 参考记录
examples/          ← 示例配置（opencode-configs/ + skills/）
```

## 50 篇文章全部有内容

全书已没有占位文件。ch06-advanced 和 ch07-case-studies 的文章相对较短（2-7KB），其余章节文章在 15-46KB 之间。所有代码块格式已统一为 `language:path` 格式（474 块）。

## CI

`.github/workflows/deploy-mdbook.yml`：push 到 main（以及 `d/**`、`docs/**` 分支）时自动构建并部署到 GitHub Pages。构建前会检查 SUMMARY.md 中所有链接目标是否存在。

部署到 `gh-pages` 环境，构建输出 `_book/`。mdBook 版本锁定 `v0.4.40`（不要用 latest）。

## Pre-commit hook

`.githooks/pre-commit` — 提交前自动检查内部 `.md` 链接 + 运行 `mdbook build`。启用方式：

```bash
git config core.hooksPath .githooks
```

## 工作日志经验总结

以下经验来自 `docs/job-logs/` 中记录的 9 轮 Sprint 实践。

### 编排原则

| # | 原则 | 来源 Sprint | 一句话说清 |
|---|------|-----------|-----------|
| 1 | **审计先行** | 005, 008 | 动手修改前先做完整审计，确认哪些已经修过，避免重复劳动 |
| 2 | **调研先于改写** | 007, 008 | 技术文章改写必须先 deep-research 验证当前版本真实性，确认问题后再动用内容改写 agent |
| 3 | **并行度优先** | 005, 006, 008 | 无依赖的任务一次部署并行执行，6 agent 墙钟仅 2 分钟，11 agent 墙钟仅 8-10 分钟 |
| 4 | **原子化 agent** | 005, 008, exec | 1 agent = 1 file / 1 perspective，prompt 打包完整上下文，避免 scope creep |
| 5 | **需求澄清 > 直接开干** | 006 | 抽象需求（"记录 session"）→ 追问细化后才能产出符合预期的结构化输出 |
| 6 | **单一权威源** | 007 | PRD 和 user-stories 的映射表只维护一份，另一份引用而非复制 |
| 7 | **模块化审阅团队** | 008 | 7 个独立视角（读者/思维框架/人物/技术/安全）→ 综合共识 → 定向修复的流水线，避免单一审阅者盲区 |
| 8 | **验证闭环** | 008 | 每子阶段末尾执行 `mdbook build`，确保零错误递进，避免最后一刻大规模回滚 |

### Prompt 工程

| # | 实践 | 来源 Sprint | 说明 |
|---|------|-----------|------|
| 1 | **5 段式 prompt 结构** | 005, exec | TASK + EXPECTED OUTCOME + TONE REQUIREMENTS + MUST DO + MUST NOT DO |
| 2 | **读者视角锚定** | 005, 007, 008 | 每段话自问"不给这个信息 agent 会犯错吗"，prompt 以读者真实困惑开头 |
| 3 | **视角差异化指令** | exec, 008 | Musk/Jobs/Munger/Karpathy 各自风格靠 TONE REQUIREMENTS 区分，Mermaid 颜色规范也靠它 |
| 4 | **MUST NOT DO 防呆** | exec, 008 | 明确禁止删除现有内容、重构、超长度、修改 Mermaid 块，避免 agent 越界 |
| 5 | **子 agent 环境 skill 不可用 fallback** | 008 | 部分人物视角 skill（zhang-yiming-perspective）在子 agent 上下文中不存在，需提前准备等效替代视角 |

### 技术踩坑

| # | 坑 | 来源 Sprint | 修复方案 |
|---|-----|-----------|---------|
| 1 | **Mermaid 跨子图边渲染** | 006 | 子图外部的边连接子图内部节点时，节点ID需加引号避免歧义 |
| 2 | **CI/CD checkout 默认分支** | 006 | 默认分支 main → 显式指定 `ref: main`（不要假设） |
| 3 | **mdBook 版本锁定** | 006 | 不指定 latest 而是锁定 `v0.4.40`，避免 CI 意外行为 |
| 4 | **session_info 调用失败** | 005, exec | 获取会话元数据时必须使用真实 session_id，占位符会导致调用失败 |
| 5 | **多 agent 同文件冲突** | exec, 008 | 多个 agent 修改同一文件的相邻区域存在冲突风险；串行化同文件操作或检测冲突 |
| 6 | **代码块 agent 单文件替换过广** | 008 | sed 模式匹配不够精确导致误替换合规行；用更窄的模式（行尾锚定 `$`）避免全局匹配 |
| 7 | **虚构模型名称发现晚** | 008 | 早期就应该纳入审阅检查清单（如 claude-opus-4-7、gpt-5.3-codex），而非等全书审阅才发现 |

### 文档规范

| # | 规范 | 来源 Sprint | 说明 |
|---|------|-----------|------|
| 1 | **内容变更 → spec 同步** | 006, 008 | 修改正文后必须即时同步 docs/ 中的规格文档，否则需求文档滞后 |
| 2 | **AGENTS.md 信号密度** | 007 | 每行自问：不给这个信息 agent 会犯错吗？通用知识全移除 |
| 3 | **统一工作日志格式** | 全部 | 所有 sprint 日志采用统一模板（基本信息 → 需求 → 团队 → 工作流 → 技能 → 模型 → 变更 → 经验） |
| 4 | **链接修复模式** | 006 | 全局链接一次性修复，模式统一：同目录 `[text](file.md)`，跨目录 `[text](../target/file.md)` |
| 5 | **低风险任务轻量计划** | 008 | 文案追加类低风险任务不需要写完整 plan，确认范围 → 直接执行 → 验证即可 |
| 6 | **审阅粒度区分 spec vs content** | 005, 008 | 多轮审阅中，规范级发现（ADR、合规映射）与内容级发现混在一起会降低审计效率，需分类跟踪 |

### 后续待办

- [ ] **P2**: 将部分 `:terminal` 代码块路径替换为更具体的真实路径（非虚构示例文件）
- [ ] **P2**: `examples/` 目录添加真实示例文件，对应当前代码块引用
- [ ] **P2**: 跨 session 审计信息持久化 — 修复状态不靠会话压缩摘要，应写入持久文件以便后续 session 直接读取

## 写完后的验证

```bash
# 检查所有内部 .md 链接
find src -name '*.md' -exec grep -n '\](' {} + | grep '\.md)'

# 验证 SUMMARY.md 所有链接目标存在
awk -F '[()]' '/\.md\)/ {print $2}' src/SUMMARY.md | while read f; do [ -f "src/$f" ] || echo "BROKEN: src/$f"; done

# 本地构建，确认无警告
mdbook build

# 检查非 Mermaid 代码块是否遗漏 path 注解
awk '/^```[a-z]/ && !/mermaid/ && !/:/ {count++} END {print count+0 " blocks without path"}' src/**/*.md
