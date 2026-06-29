# Harness Engineering — AGENTS.md

## 一句话说清

**这是本开源书籍，不是软件项目。** 所有内容都是简体中文 Markdown，用 mdBook 渲染成静态网站。不要跑 npm test、npm run build 这些东西。

## 唯一命令

```bash
mdbook serve    # 本地预览（默认 http://localhost:3000）
mdbook build    # 构建到 _book/（被 .gitignore 忽略，不提交）
```

另外在 `scripts/serve.sh` 中有一个便捷封装脚本。

## 最容易翻车的地方

### 1. 增删文章必须同步 SUMMARY.md

`src/SUMMARY.md` 是 mdBook 的导航命脉。新增/重命名/删除文件后不更新它 → 页面直接 404。

**CI 已有链接检查**（`.github/workflows/deploy-mdbook.yml`），但只检查 SUMMARY.md 内的目标是否存在，不检查正文内链。

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

语言和路径之间用冒号，路径从项目根相对。Mermaid 块**不需要** path 注解。全书已全部合规。

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

方向统一用 TB（top-bottom）。跨子图的边连接子图内部节点时，节点 ID 需加引号避免歧义。

### 8. 写作原则：说人话，从读者视角写

- 避免抽象隐喻（如"工程流水线"这种需要二次理解的表达）
- 优先用开发者熟悉的日常语言
- 每段话回答一个问题：读者读完能做什么/知道什么？
- 13 种读者角色见 `src/00-guide/reading-paths.md`，写作时对号入座

## 项目结构速览

```
src/               ← 正文（10 个章节，约 53 篇文章）
  SUMMARY.md       ← 导航配置文件（改它之前想清楚）
  README.md        ← 书籍首页
  00-guide/        ← 读者导航
  01-introduction/ ← 简介（6 篇）
  02-core-concepts/← 核心概念（6 篇）
  03-setup/        ← 环境搭建（5 篇）
  04-workflows/    ← 工作流实战（6 篇）
  05-skills/       ← Skill 开发（5 篇）
  06-advanced/     ← 高级话题（12 篇）
  07-case-studies/ ← 案例研究（6 篇）
  appendix-a/      ← 术语 & 参考
  appendix-b/      ← OpenCode & Claude Code 内置能力
book.toml          ← mdBook 配置（主题、搜索、Mermaid、Vega）
theme/             ← 自定义 CSS/JS（Vega、Mermaid、lightbox、pagetoc）
docs/              ← 规划(planning/ 含 requirements/ plans/ sprints/ specs/)、评审(reviews/ 含 articles/ chapters/ deep-research/ overall/ archive/)、参考(reference/)、执行日志(logs/)
examples/          ← 示例配置（opencode-configs/ + skills/）
assets/            ← 图片等静态资源
```

## CI

`.github/workflows/deploy-mdbook.yml`：push 到 `main`（以及 `d/**`、`docs/**` 分支）时自动构建并部署到 GitHub Pages。CI 使用 `mdbook-version: 'latest'`（非锁定版本号）。

部署到 `gh-pages` 环境，构建输出 `_book/`。

## Pre-commit hook

`.githooks/pre-commit` — 提交前自动检查内部 `.md` 链接 + 运行 `mdbook build`。启用方式：

```bash
git config core.hooksPath .githooks
```

## 语言约束

AI 助手的回复**必须使用简体中文**，除非用户明确要求或引用的英文术语需要保留原名。全书为中文书籍，所有交流、分析、建议均以中文输出。

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
```

### HEDQ 质量审计

8 维度内容质量评分（满分 52.5，自动检测口径）。标准详见 [docs/reference/hedq-quality-standard.md](docs/reference/hedq-quality-standard.md)。

```bash
# 快速模式：D1 结构 + D6 文风 + D7 术语（满分 23，约 10 秒）
python scripts/qa/run-hedq.py --quick

# 完整模式：8 个维度全检（满分 52.5，约 30 秒）
python scripts/qa/run-hedq.py

# JSON 输出（供 CI/脚本消费）
python scripts/qa/run-hedq.py --json --no-save
```

评级标准：≥90% READY · 75-89% CONDITIONAL · 60-74% NEEDS WORK · <60% DRAFT。报告自动保存到 `scripts/qa/reports/`（含 JSON 快照 + results.tsv 趋势记录）。

### HEDQ Skill 工作流（Agent 使用）

当 AI 智能体需要对书籍进行质量审计和修复时，加载 `hedq-audit` Skill 并遵循 Analyze → Diagnose → Fix → Verify 四步闭环：

```
1. Analyze  — 运行 python scripts/qa/run-hedq.py 获取 8 维评分报告
2. Diagnose — 解读报告，定位最低分维度的根因（断链/品牌名/代码块path等）
3. Fix      — 按 P0 > P1 > P2 优先级定向修复，每次只修一个维度
4. Verify   — 重新运行 HEDQ，确认分数提升且未引入新问题
```

**适用场景**：
- 发布前全面质量审计 → 完整模式 `run-hedq.py`
- 日常 PR 质量门禁 → 快速模式 `run-hedq.py --quick`
- 新章节编写中的持续改进 → 单维度定向检查

**自动触发条件**：当 Agent 检测到以下信号时，应自动加载 `hedq-audit` Skill：
- 用户说"检查质量"、"跑一下 HEDQ"、"审计"、"质量评分"
- CI 中 HEDQ 任务失败
- 发布 / 提 PR 前的自检环节
- 新文章或章节完成后需要质量验证

Skill 定义文件位于 `.opencode/skills/hedq-audit/SKILL.md`。

## 经验总结（来自 9 轮 Sprint 实践）

### 编排原则

| # | 原则 | 一句话说清 |
|---|------|-----------|
| 1 | **审计先行** | 动手修改前先做完整审计，确认哪些已经修过 |
| 2 | **调研先于改写** | 技术文章改写必须先 deep-research 验证当前版本真实性 |
| 3 | **并行度优先** | 无依赖的任务一次部署并行执行 |
| 4 | **原子化 agent** | 1 agent = 1 file / 1 perspective，避免 scope creep |
| 5 | **需求澄清 > 直接开干** | 抽象需求追问细化后才能产出预期输出 |
| 6 | **单一权威源** | 映射表只维护一份，另一份引用而非复制 |
| 7 | **模块化审阅团队** | 多独立视角 → 综合共识 → 定向修复，避免单一盲区 |
| 8 | **验证闭环** | 每阶段末尾执行 `mdbook build`，确保零错误递进 |

### Prompt 工程

| # | 实践 | 说明 |
|---|------|------|
| 1 | **5 段式 prompt 结构** | TASK + EXPECTED OUTCOME + TONE REQUIREMENTS + MUST DO + MUST NOT DO |
| 2 | **读者视角锚定** | 自问"不给这个信息 agent 会犯错吗"，prompt 以读者真实困惑开头 |
| 3 | **视角差异化指令** | 人物视角靠 TONE REQUIREMENTS 区分，Mermaid 颜色规范也靠它 |
| 4 | **MUST NOT DO 防呆** | 明确禁止删除现有内容、重构、超长度、修改 Mermaid 块 |
| 5 | **子 agent 环境 skill fallback** | 部分 skill 在子 agent 上下文中不存在，需提前准备替代视角 |

### 技术踩坑

| # | 坑 | 修复方案 |
|---|-----|---------|
| 1 | **Mermaid 跨子图边渲染** | 子图外部边连接子图内部节点时，节点 ID 加引号 |
| 2 | **CI/CD checkout 默认分支** | 显式指定 `ref: main` |
| 3 | **多 agent 同文件冲突** | 串行化同文件操作或检测冲突 |
| 4 | **代码块替换过广** | 模式匹配用行尾锚定 `$` 避免误替换 |
| 5 | **虚构模型名称发现晚** | 审阅检查清单早期就应纳入模型名核验 |
| 6 | **Mermaid 波浪号 `~` 解析错误** | Mermaid v9 词法解析器不识别 `~`，节点文本 `Node[~path]` 需改为 `Node["~path"]` |

### 文档规范

| # | 规范 | 说明 |
|---|------|------|
| 1 | **内容变更 → spec 同步** | 修改正文后必须即时同步 docs/ 中的规格文档 |
| 2 | **链接修复模式** | 全局链接一次性修复，同目录 `[text](file.md)`，跨目录 `[text](../target/file.md)` |
| 3 | **低风险任务轻量计划** | 文案追加类不需要完整 plan，确认范围 → 直接执行 → 验证 |
| 4 | **审阅粒度区分** | 规范级发现与内容级发现分开跟踪，避免混在一起降低审计效率 |
