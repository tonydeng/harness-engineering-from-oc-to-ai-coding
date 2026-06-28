# 质量门禁与发布前验收流程

> **User Story**: US-QA-03 | **优先级**: P1
> **用途**: 定义全书发布前的质量验证流程，确保每次发布都经过系统化检查
> **参考**: `docs/reviews/overall/overall-evaluation-2026-06-11.md` 综合评估报告

---

## 一、流程概览

每次发布（含 v1.0、v1.1 等版本迭代）前，必须依次通过以下 5 道门禁。**任何一道门禁出现 ❌ 阻塞项，不得发布。**

```
Gate 1: 自动化构建 ──→ Gate 2: 链接完整性 ──→ Gate 3: 内容质量
                                                  │
                                     Gate 4: 品牌与格式 ──→ Gate 5: 人工审阅 ──→ 签核发布
```

**门禁分级**:

| 级别 | 含义 | 未通过时 |
|------|------|---------|
| ✅ PASS | 检查通过 | 继续下一道门禁 |
| ⚠️ WARN | 非阻塞警告 | 记录到已知限制，可带条件发布 |
| ❌ BLOCK | 阻塞发布 | 必须修复后重新验证 |

---

## 二、Gate 1: 自动化构建检查

**目的**: 确保 mdBook 能正确构建，无渲染错误。

| # | 检查项 | 命令 | 阈值 | 级别 |
|---|--------|------|------|:----:|
| 1.1 | mdBook 构建零错误 | `mdbook build` | 0 个 error | ❌ |
| 1.2 | 无弃用警告 | 构建输出 grep `WARNING` | 0 个 WARNING | ⚠️ |
| 1.3 | Mermaid 渲染正常 | 打开 `_book/` 中含 Mermaid 的页面 | 无空白/报错 | ❌ |
| 1.4 | book.toml 配置完整 | 人工确认 Mermaid/搜索/自定义样式 | 全部就绪 | ⚠️ |

**执行方式**: 在本地运行 `mdbook build`，或触发 CI 构建（`.github/workflows/deploy-mdbook.yml`）。

**CI 集成说明**: 当前 CI 工作流在构建前会检查 SUMMARY.md 链接（步骤 `Check internal links`），构建后部署到 GitHub Pages。CI 使用 `mdbook-version: 'latest'`，建议发布前锁定版本避免意外行为。

---

## 三、Gate 2: 链接完整性

**目的**: 确保全书无断链，读者不会遇到 404 页面。

| # | 检查项 | 命令 | 阈值 | 级别 |
|---|--------|------|------|:----:|
| 2.1 | SUMMARY.md 所有链接有效 | `awk -F '[()]' '/\.md\)/ {print $2}' src/SUMMARY.md \| while read f; do [ -f "src/$f" ] \|\| echo "BROKEN: $f"; done` | 0 个断链 | ❌ |
| 2.2 | 正文内部 .md 链接无断链 | `find src -name '*.md' -exec grep -n '\](' {} + \| grep '\.md)'` 逐条验证 | 0 个断链 | ❌ |
| 2.3 | 跨章节引用 `→ [标题](路径)` 有效 | 按 2.2 同等方式检查 | 0 个断链 | ❌ |
| 2.4 | 链接文字与目标 H1 标题一致 | 人工抽查或脚本对比 | 100% 一致 | ⚠️ |

**常见坑点**:

- 跨目录链接必须用 `../target/file.md`，不能用 `target/file.md`
- `README.md` 在 mdBook 中渲染为 `index.html`，链接用目录形式而非 `README.md`
- 附录子目录文件（如 `appendix-b/opencode/`）的 `../` 需要向上两级

**执行方式**: 先运行自动化脚本扫描，再人工验证脚本无法覆盖的跨章节引用。

---

## 四、Gate 3: 内容质量

**目的**: 确保每篇文章达到最低内容标准，无占位/空白内容。

| # | 检查项 | 命令 | 阈值 | 级别 |
|---|--------|------|------|:----:|
| 3.1 | 主文章行数 ≥ 200 行 | `wc -l src/chapters/*.md` | 主体章节 ≥ 200 | ⚠️ |
| 3.2 | 案例研究行数 ≥ 300 行 | `wc -l src/07-case-studies/*.md` | ≥ 300 | ⚠️ |
| 3.3 | 无占位/stub 文件 | grep `TODO\|PLACEHOLDER\|占位` | 0 个匹配 | ❌ |
| 3.4 | 全书文章总数达标 | `find src -name '*.md' ! -name 'SUMMARY.md' \| wc -l` | ≥ 目标数量 | ⚠️ |
| 3.5 | 代码示例可运行性 | 抽查关键代码块 | 核心示例无语法错误 | ⚠️ |
| 3.6 | 术语表完整 | `wc -l src/appendix-a/glossary.md` | ≥ 200 行 | ⚠️ |

**行数检查参考阈值**（来自 v1.0 评估数据）:

| 章节 | 最低行数 | 说明 |
|------|:--------:|------|
| Ch0-Ch6 | 200 | 主体内容章节 |
| Ch7 案例研究 | 300 | 案例需深度 |
| 附录 | 161（最低） | 附录可较短，但建议 ≥ 200 |

---

## 五、Gate 4: 品牌与格式规范

**目的**: 确保全书品牌名、代码块格式、术语格式、图表配色一致。

| # | 检查项 | 命令 | 阈值 | 级别 |
|---|--------|------|------|:----:|
| 4.1 | "OpenCode" 拼写一致 | `grep -rn 'Opencode\|opencode[^.]' src/ --include='*.md'` | 0 处错误 | ❌ |
| 4.2 | "oh-my-openagent" 格式 | `grep -rn 'OH-MY-OPENAGENT\|Oh-My-Openagent' src/ --include='*.md'` | 0 处错误 | ❌ |
| 4.3 | "MCP" 大写 | `grep -rni 'mcp' src/ --include='*.md' \| grep -v 'MCP'` | 0 处错误 | ⚠️ |
| 4.4 | "mdBook" 大写 B | `grep -rn 'mdbook\|Mdbook' src/ --include='*.md'` | 0 处错误 | ⚠️ |
| 4.5 | 代码块 `language:path` 格式 | `awk '/^```[a-z]/ && !/mermaid/ && !/:/ {count++} END {print count}' src/**/*.md` | 0 个缺失 | ⚠️ |
| 4.6 | 跨章节引用格式 | `grep -rn '→ \[' src/ --include='*.md'` 检查格式 | 100% 统一 | ⚠️ |
| 4.7 | 英文术语首次出现格式 | `grep -rn '\*\*[A-Z][a-z].*（' src/ --include='*.md'` | 符合规范 | ⚠️ |
| 4.8 | Mermaid 配色规范 | 人工抽查图表 | Agent #4A90D9, Skill #50C878, Workflow #FF9F43, MCP #A66CFF | ⚠️ |

**品牌名速查**:

| 品牌 | 正确写法 | 常见错误 |
|------|---------|---------|
| OpenCode | OpenCode（大写 C，无空格） | Opencode, Open Code, opencode |
| oh-my-openagent | oh-my-openagent（全小写） | Oh-My-Openagent, OH-MY-OPENAGENT |
| MCP | MCP（全大写） | Mcp, mcp |
| mdBook | mdBook（小写 m，大写 B） | Markdownbook, mdbook |

---

## 六、Gate 5: 人工审阅

**目的**: 通过人工视角验证内容质量，覆盖自动化无法检测的问题。

| # | 检查项 | 负责人 | 检查方式 | 级别 |
|---|--------|--------|---------|:----:|
| 5.1 | 内容准确性 | 技术负责人 | 抽查关键技术描述 | ⚠️ |
| 5.2 | 读者视角 | 内容负责人 | 选 2-3 个角色路径通读 | ⚠️ |
| 5.3 | 示例可复现性 | QA 工程师 | 按文中步骤实际执行 | ⚠️ |
| 5.4 | Mermaid 图可读性 | 内容负责人 | 人工查看渲染效果 | ⚠️ |
| 5.5 | 阅读指引有效 | 内容负责人 | 验证 14 角色路径可达 | ⚠️ |
| 5.6 | 追溯矩阵验证 | 需求分析师 | 对照用户故事确认覆盖 | ⚠️ |

**读者角色路径**（必须覆盖）:

完整角色列表见 `src/00-guide/reading-paths.md`，包含 14 种读者角色。每次发布至少验证 3 条代表性路径。

---

## 七、执行流程

### 7.1 发布前检查顺序

```
1. 运行 Gate 1（自动化构建）
   └─ 通过 → 继续
   └─ 失败 → 修复构建问题，重新验证

2. 运行 Gate 2（链接完整性）
   └─ 通过 → 继续
   └─ 失败 → 修复断链，回到 Gate 1

3. 运行 Gate 3（内容质量）
   └─ 通过 → 继续
   └─ 失败 → 补充内容，回到 Gate 1

4. 运行 Gate 4（品牌与格式）
   └─ 通过 → 继续
   └─ 失败 → 修复格式，回到 Gate 1

5. 运行 Gate 5（人工审阅）
   └─ 全部通过 → 签核发布
   └─ 有条件通过 → 记录已知限制，签核发布
```

### 7.2 快速检查命令

日常开发中可随时运行的轻量级检查：

```bash
# Gate 1: 构建检查
mdbook build 2>&1 | grep -c "ERROR"

# Gate 2: 链接检查
find src -name '*.md' -exec grep -n '\](' {} + | grep '\.md)'

# Gate 2.1: SUMMARY.md 链接验证
awk -F '[()]' '/\.md\)/ {print $2}' src/SUMMARY.md | while read f; do
  [ -f "src/$f" ] || echo "BROKEN: src/$f"
done

# Gate 3: 行数检查
find src -name '*.md' ! -name 'SUMMARY.md' -exec wc -l {} + | sort -n | head -20

# Gate 4: 品牌名检查
grep -rn 'Opencode' src/ --include='*.md' | grep -v 'OpenCode'

# Gate 4: 代码块格式检查
awk '/^```[a-z]/ && !/mermaid/ && !/:/ {count++} END {print count+0 " blocks without path"}' src/**/*.md
```

### 7.3 带条件发布

当存在 ⚠️ WARN 级问题时，可在签核文档中记录为"已知限制"：

- P2 级问题（如附录篇目行数略低于 200）可标记为 v1.1 迭代
- 缺失的用户故事可标记为已知限制（参见 `docs/planning/plans/quality-gate-checklist.md` 第四节）

---

## 八、签核模板

每次发布前，负责人填写以下签核表：

```markdown
## 发布签核

| 门禁 | 总项 | ✅ PASS | ⚠️ WARN | ❌ BLOCK |
|------|:----:|:-------:|:-------:|:--------:|
| Gate 1: 自动化构建 | 4 | __ | __ | __ |
| Gate 2: 链接完整性 | 4 | __ | __ | __ |
| Gate 3: 内容质量 | 6 | __ | __ | __ |
| Gate 4: 品牌与格式 | 8 | __ | __ | __ |
| Gate 5: 人工审阅 | 6 | __ | __ | __ |
| **合计** | **28** | __ | __ | __ |

**已知限制**:
1. ________________________________
2. ________________________________

**发布决定**: ☐ 批准发布 ☐ 需补充后发布 ☐ 暂缓发布

| 角色 | 签核人 | 日期 |
|------|--------|------|
| 项目负责人 | _________ | ____-__-__ |
| 内容负责人 | _________ | ____-__-__ |
| QA 负责人 | _________ | ____-__-__ |
| 技术负责人 | _________ | ____-__-__ |
```

---

## 九、配置参考

### 阈值配置

可将门禁阈值提取为配置文件（参考 `examples/quality-gates/example-gates.yaml`）：

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `min_lines_main` | 200 | 主文章最低行数 |
| `min_lines_case` | 300 | 案例研究最低行数 |
| `min_total_articles` | 90 | 全书最低文章数 |
| `max_broken_links` | 0 | 允许断链数 |
| `max_brand_errors` | 0 | 允许品牌名错误数 |
| `max_code_blocks_no_path` | 0 | 允许缺 path 的代码块数 |

### 与 CI 集成

当前 CI 流水线（`.github/workflows/deploy-mdbook.yml`）已包含：
- SUMMARY.md 链接检查（步骤 `Check internal links`）
- mdBook 构建（步骤 `Build mdBook`）
- GitHub Pages 部署

建议后续迭代增加：
- 正文内部链接检查脚本
- 品牌名一致性 grep 检查
- 行数阈值检查脚本

---

## 十、相关文档

| 文档 | 说明 |
|------|------|
| `docs/reviews/overall/overall-evaluation-2026-06-11.md` | 综合评估报告（评估模板） |
| `docs/planning/plans/quality-gate-checklist.md` | v1.0 发布签核清单（实例） |
| `examples/quality-gates/example-gates.yaml` | 门禁规则配置示例 |
| `.github/workflows/deploy-mdbook.yml` | CI 构建与部署流水线 |
| `AGENTS.md` | 品牌名、格式、链接等规范汇总 |
