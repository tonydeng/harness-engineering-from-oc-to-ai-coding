# Harness Engineering — AGENTS.md（项目规范）

## 项目性质

**此仓库是开源书籍，不是软件项目。** 所有内容为简体中文 Markdown，由 mdBook v0.4.x 构建为静态站点。

- **唯一命令**：`mdbook serve`（本地预览，默认端口 3000）。`mdbook build`（构建到 `_book/` 目录）。
- **无构建/测试/类型检查**。不要运行 `npm test`、`npm run build` 等。
- **Chromium 限制**：`_book/` 目录被 `.gitignore` 忽略，不会提交到仓库。

## CI/CD

`.github/workflows/deploy-mdbook.yml`：push 到 main 时构建 mdBook 并部署到 GitHub Pages。使用 `peaceiris/actions-mdbook@v2` action，构建输出目录 `./book`。

## 目录结构（关键路径）

| 路径 | 用途 |
|------|------|
| `src/` | 书籍正文，8 章 46 篇文章（33 篇完成 + 13 篇 stub） |
| `src/SUMMARY.md` | **目录导航** — 增删/重命名页面时必须同步更新，否则页面不可达 |
| `book.toml` | mdBook 配置文件（主题、搜索、Mermaid 预处理器） |
| `theme/` | 自定义 CSS/JS（mermaid 渲染、分页导航、图片灯箱） |
| `docs/` | 项目管理：写作计划、PRD、评审报告、wiki |
| `examples/` | 示例配置（`opencode-configs/` + `skills/`） |
| `.trae/specs/` | 本地写作规格和验收清单 |
| `.opencode/AGENTS.md` | OpenCode 会话的指令文件（与本书内容无关） |

## 写作规范（违反会导致导航或渲染问题）

### 文件结构
- **章节目录**：零填充编号 `01-introduction/`、`02-core-concepts/`
- **文件命名**：小写 kebab-case（如 `my-skill.md`）
- **代码块**：````language:relative/path {行号}````（语言冒号后紧跟相对路径）

### 内部链接（mdBook 规则）
- **同目录**：`[text](file.md)` ✓
- **跨目录**：`[text](../target-chapter/file.md)` ✓ — 必须带 `../`
- **根 README**（`src/README.md`）：`[text](chapter/file.md)` ✓ — 它在 `src/` 根
- ❌ **严禁**：从子目录写 `](chapter/file.md)` 或 `](子目录/target.md)`（不带 `../` 会导致 404）

### 章节首页链接规范
- **目录形式**：指向章节首页 `README.md` 的链接必须使用目录形式
- **示例**：`[读者导航](00-guide/)` 而非 `[读者导航](00-guide/README.md)`
- **原因**：mdBook 将 `README.md` 渲染为 `index.html`，使用目录形式确保链接正确解析
- **适用范围**：所有内部链接，包括 `src/README.md`、各章节文档
- **排除范围**：`SUMMARY.md`

### 跨章节引用
使用 `→ [章节名称](相对路径.md)` — 链接文字必须与目标文件的 H1 一致。

**注意**：全书不使用 `§X.Y` 格式的章节编号，统一使用章节名称进行引用。

### 英文术语
首次出现用 **英文（中文翻译）** 格式。

### Mermaid 图表
- 颜色：Agent=#4A90D9, Skill=#50C878, Workflow=#FF9F43, MCP/外部=#A66CFF，方向统一 TB
- mdBook 通过 `mdbook-mermaid` 预处理器渲染 Mermaid（`book.toml` 中配置，可选依赖）
- 渲染失败时不阻断构建，但应确保所有图表语法正确
- VEGA 图表使用 `vega` 和 `vega-lite` 语法，由 Mermaid 渲染

## 品牌名（常见陷阱）

全书统一 **`OpenCode`**（大写 C）。

## 关键链接

### OpenCode 官方资源

| 资源 | 链接 |
|------|------|
| **官方网站** | https://opencode.ai/ |
| **官方文档** | https://opencode.ai/docs |
| **GitHub 仓库** | https://github.com/anomalyco/opencode |
| **安装脚本** | https://opencode.ai/install |
| **认证页面** | https://opencode.ai/auth |
| **Zen 服务** | https://opencode.ai/zen |
| **GitHub Releases** | https://github.com/anomalyco/opencode/releases |

### 安装命令

```bash
# macOS/Linux 官方脚本
curl -fsSL https://opencode.ai/install | bash

# Homebrew (macOS/Linux)
brew install anomalyco/tap/opencode

# npm (跨平台)
npm install -g opencode-ai

# Arch Linux
sudo pacman -S opencode

# Windows (Scoop)
scoop install opencode

# Windows (Chocolatey)
choco install opencode

# Docker
docker run -it --rm ghcr.io/anomalyco/opencode
```

## 章节结构（基于 `SUMMARY.md` 条目顺序）

| 章 | 文章数 | 完成状态 |
|----|--------|---------|
| 读者导航 | 4 | ✅ 4 篇全部完成 |
| 简介 | 5 | ✅ 5 篇全部完成 |
| 核心概念 | 6 | ✅ 6 篇全部完成 |
| 环境搭建 | 5 | ❌ 5 篇 stub |
| 工作流实战 | 5 | ❌ 5 篇 stub |
| Skill 开发 | 5 | ❌ 5 篇 stub |
| 高级话题 | 12 | ❌ 12 篇 stub |
| 案例研究 | 6 | ❌ 6 篇 stub（有部分内容） |

全书规划 **46 篇文章**，当前 **33 篇完成**、**13 篇 stub**。

## 内部链接验证

每次新增/修改文件后，执行：

```bash
# 检查所有内部 .md 链接是否有效（macOS/Linux 通用）
find src -name '*.md' -exec grep -n '\](' {} + | grep '\.md)'
# 验证 SUMMARY.md 所有链接目标文件都存在
awk -F '[()]' '/\.md\)/ {print $2}' src/SUMMARY.md | while read f; do [ -f "src/$f" ] || echo "BROKEN: src/$f"; done
```

## mdBook 构建检查

```bash
mdbook build   # 应无错误/警告输出
mdbook serve   # 本地预览，确认所有页面可达
```

## 角色标识规范

全书中 13 种读者角色统一使用中文名称（Ch0 已全部中文化）：
- 5 核心：入门开发者、效率开发者、技术负责人、Skill 作者、工程经理
- 8 扩展：需求分析师、架构师、后端、前端、UX、QA、安全工程师、红队
- 首字母英文缩写（BEGINNER/POWER 等）仅用于规格文档和代码示例，不出现在正文表格中

## 用户故事模板（仅 `docs/requirements/` 内使用）

```
作为 <角色>
我想要 <功能>
以便 <价值>
验收标准：[可验证清单]
优先级：P0/P1/P2 | 工作量：S/M/L/XL
```

13 个读者角色：BEGINNER, POWER, LEAD, SKILL, MANAGER, ANALYST, SYSA, BACKEND, FRONTEND, UX, QA, SECURITY, REDTEAM。
