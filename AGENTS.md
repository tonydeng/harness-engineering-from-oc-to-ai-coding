# Harness Engineering — AGENTS.md（项目规范）

## 项目性质

**此仓库是开源书籍，不是软件项目。** 所有内容为简体中文 Markdown，由 Docsify v4 渲染，JS 运行时全部从 CDN 加载。

- **无构建/测试/类型检查**。不要运行 `npm test`、`npm run build` 等。
- `.nojekyll` 文件存在于根目录（GH Pages 部署 `_sidebar.md` 的必要条件）。

## 唯一命令

```bash
npx docsify serve ./src    # 本地预览，端口 3000
```

## CI/CD

`.github/workflows/deploy-docsify.yml`：push 到 main 时直接将 `src/` 目录上传到 GitHub Pages。无构建步骤。

## 目录结构（关键路径）

| 路径 | 用途 |
|------|------|
| `src/` | 书籍正文，8 章 46 篇文章（19 篇完成 + 27 篇 stub） |
| `src/_sidebar.md` | **手动导航** — 增删/重命名页面时必须同步更新，否则页面不可达 |
| `docs/` | 项目管理：写作计划、PRD、评审报告、wiki |
| `examples/` | 示例配置（`opencode-configs/` + `skills/`） |
| `.opencode/AGENTS.md` | OpenCode 会话的指令文件（与本书内容无关） |

## 写作规范（违反会导致导航或渲染问题）

- **章节目录**：零填充编号 `01-introduction/`、`02-core-concepts/`
- **文件命名**：小写 kebab-case（如 `my-skill.md`）
- **代码块**：````language:relative/path {行号}````（语言冒号后紧跟相对路径）
- **内部链接（Docsify 规则）**：链路基于当前页 URL 路径解析（默认 `relativePath: false`）：
  - **同目录**：`[text](file.md)` ✓ — 从 `/#/chapter/` 解析为 `/#/chapter/file`
  - **跨目录**：`[text](../target-chapter/file.md)` ✓ — 必须带 `../`，否则解析为 `/#/source-chapter/target-chapter/file`（404）
  - **根 README**：从子目录回首页用 `[text](../README.md)` ✓
  - **根级文件**（`src/README.md`、`src/_sidebar.md`）：`[text](chapter/file.md)` ✓ — 它们在 `src/` 根
  - ❌ **严禁**：从子目录写 `](chapter/file.md)` 或 `](子目录/target.md)`（不带 `../` 或「同目录加前缀」均会 404）
- **跨章节引用**：`→ [§X.Y 标题](相对路径.md)` — 链接文字必须与目标文件的 H1 一致
- **英文术语**：首次出现用 **英文（中文翻译）** 格式
- **Mermaid 颜色**：Agent=#4A90D9, Skill=#50C878, Workflow=#FF9F43, MCP/外部=#A66CFF，方向统一 TB

## 品牌名（常见陷阱）

全书统一 **`OpenCode`**（大写 C）。`src/README.md` 中出现的 `Opencode`（小写 c）是遗留问题。

## 章节编号（基于 `_sidebar.md` 条目顺序）

| 章 | 文章数 | §X.Y 最大范围 |
|----|--------|--------------|
| Ch0 | 2 | §0.2 |
| Ch1 | 5 | §1.5 |
| Ch2 | 6 | §2.6 |
| Ch3 | 5 | §3.5 |
| Ch4 | 5 | §4.5 |
| Ch5 | 5 | §5.5 |
| Ch6 | 12 | §6.12 |
| Ch7 | 6 | §7.6 |

全书规划 **46 篇文章**。§X.Y 中的 Y 不能超出上表范围。

## 内部链接验证

每次新增/修改文件后，执行：

```bash
# 检查所有内部 .md 链接是否有效（macOS/Linux 通用）
find src -name '*.md' -exec grep -n '\](' {} + | grep '\.md)'
# 验证侧边栏所有链接目标文件都存在
awk -F '[()]' '/\.md\)/ {print $2}' src/_sidebar.md | while read f; do [ -f "src/$f" ] || echo "BROKEN: src/$f"; done
```

全书当前约 269 条内部链接，无断链残留。

## 用户故事模板（仅 `docs/requirements/` 内使用）

```
作为 <角色>
我想要 <功能>
以便 <价值>
验收标准：[可验证清单]
优先级：P0/P1/P2 | 工作量：S/M/L/XL
```

13 个读者角色：BEGINNER, POWER, LEAD, SKILL, MANAGER, ANALYST, SYSA, BACKEND, FRONTEND, UX, QA, SECURITY, REDTEAM。
