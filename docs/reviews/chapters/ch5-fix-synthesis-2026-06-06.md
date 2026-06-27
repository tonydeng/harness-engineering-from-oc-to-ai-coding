# Ch5 修复总结报告

**日期**: 2026-06-06
**范围**: `src/05-skills/` 全部 5 篇文章
**Agent 任务**: 5 个并行修复 agent（bg_138bff71, bg_969a37b2, bg_2e6dd345, bg_494b8154, bg_539fc11b）
**总变更**: 182 行新增，150 行删除

---

## 修复概览

| 文件 | 变更量 | 主要修复内容 |
|------|--------|-------------|
| `creating-skills.md` | 149 行 | 核心文章，大规模修复 |
| `skill-templates.md` | 92 行 | 模板文章，结构优化 |
| `skill-mcp-bridge.md` | 34 行 | 桥接文章，较小修复 |
| `skill-best-practices.md` | 31 行 | 最佳实践，较小修复 |
| `plugin-patterns.md` | 26 行 | 插件化模式，较小修复 |

---

## 系统性修复（跨所有文件）

### 1. 工具命名规范化

全章统一将 `allowed-tools` 中的大写工具名改为小写，以匹配全书约定：

| 旧（大写） | 新（小写） | 出现次数 |
|-----------|-----------|---------|
| `Read` | `read` | 20 |
| `Grep` | `grep` | 16 |
| `Glob` | `glob` | 11 |
| `Write` | `edit` | 5 |
| `RunCommand` | `bash` | 4 |
| `WebSearch` | `websearch` | 3 |
| `WebFetch` | `webfetch` | 3 |

### 2. OMO 扩展字段 ⚠️ 声明追加

- `creating-skills.md`: 为 `allowed-tools` 增加了 OMO 扩展说明
- `plugin-patterns.md`: 为 `dependencies`/`pipeline` 增加了 OMO 扩展说明
- 语义匹配功能标注为第三方插件，非 OpenCode 核心

### 3. 代码块格式修正

- ```` ```yaml ```` → ```` ```markdown:examples/skills/*.md ````（含路径）
- ```` ```json ```` → ```` ```json:opencode.json ````

### 4. Skill 搜索路径扩展

`creating-skills.md`: 从 3 级搜索路径（项目 / 用户 / 内置）扩展为 6 路路径（.opencode / .claude / .agents 各分项目级和用户级），增加跨平台兼容说明。

### 5. 语义匹配技术细节

替换了空的阈值设计表，改为真实的技术说明（HuggingFace `all-MiniLM-L6-v2` 嵌入模型、余弦相似度、阈值 0.35、Top-K 5、缓存路径）。

---

## 余项（本次未涉及）

- `creating-skills.md` 中的 Skills Marketplace 发布命令仍然是前瞻性说明（已有 ⚠️ 声明）
- 其他章节的跨章节引用未纳入本批次修复
