# 2026-06-02: Sprint 01: 项目初始化

> [TAG: agile-coach]

## 基本信息

| 项目 | 内容 |
|------|------|
| Session ID | ses_181a75affffegM4I5ifv1BISY6 |
| Sprint 周期 | 2026-05-31 ~ 2026-06-02 |
| 风险等级 | 中 |
| 必需工作流 | agile-coach 头脑风暴 → 计划 → 实施 → 验证 |
| 主模型 | deepseek-v4-flash-free |
| 协调人 | Sisyphus |
| 项目 | Harness Engineering — From OpenCode to AI Coding |

---

## 1. 用户需求（输入）

### 1.1 原始需求

创建名为 "harness-engineering-from-oc-to-ai-coding" 的项目，用于编写基于 OpenCode 进行 AI 编程的 Harness Engineer 最佳实践。

**关键要求**：
1. 初始化 git 配置（GitHub）
2. 使用 docsify 做书籍渲染
3. 规划目录结构（含书籍编写目录 + 计划 + 需求目录）
4. 基于 opencode + oh-my-openagent 的最佳实践配置

### 1.2 需求确认过程

用户通过 3 轮对话澄清了关键设计决策：

| 轮次 | 确认事项 | 决策结果 |
|------|---------|---------|
| 1 | docsify 内容存放位置 | 放入 `src/` 目录，非根目录或 `book/` |
| 2 | git init 后是否提交 | 手动提交，不自动创建初始 commit |
| 3 | index.html 位置 | 放入 `src/` 目录 |
| 4 | 计划和需求目录 | 统一放入 `docs/` 目录 |
| 5 | GitHub Pages 部署方式 | GitHub Actions 部署，非 Pages 设置 |

---

## 2. 团队架构与角色分配

依据 agile-coach 团队的软件研发团队配置，本次 Sprint 启用的角色：

| 角色 | 职责 | 参与阶段 |
|------|------|---------|
| **Sisyphus（主协调器）** | 全局规划、任务分解、质量控制 | 全部 |
| **需求分析师** | 需求调研、用户故事编写 | 头脑风暴 |
| **架构顾问** | 技术选型评估（docsify / opencode / OMO） | 头脑风暴、计划 |
| **测试工程师** | 验证 docsify 本地预览 | 验证 |

未启用角色及其原因：后端/前端/UI 架构师——本项目为书籍写作，非软件项目，无需开发型角色。

---

## 3. 工作流阶段记录

### 3.1 头脑风暴阶段（Plan Mode）

**输入**: 用户原始需求 + AGENTS.md 规范要求
**输出**: 项目目录结构方案 + 技术选型清单

#### 调用的调查工具

| 工具 | 目标 | 关键发现 |
|------|------|---------|
| `read` (workspace) | 检查工作区状态 | 空目录，从零开始 |
| `bash` (git/node/docsify) | 确认工具版本 | git 2.54.0, node 26, npm 11.12, docsify 4.4.4 |
| `bash` (opencode config) | 查看 OMO 配置 | 用户已有 75+ skill，opencode.json 使用 deeprouter provider |
| `websearch` | 调研 oh-my-openagent 项目结构 | 确认配置路径：项目级 `.opencode/oh-my-openagent.jsonc` |
| `webfetch` | 调研 docsify 结构 | 确认 docsify 为纯客户端、无需构建 |

#### 关键决策记录（ADR）

| 编号 | 决策 | 方案 | 备选 |
|------|------|------|------|
| ADR-001 | 书籍内容目录用 `src/` | 分离项目说明与书籍正文 | 根目录、`book/` |
| ADR-002 | docsify index.html 放 `src/` 内 | 单源目录，GitHub Actions 直接发布 `src/` | 根目录、`docs/` |
| ADR-003 | 计划和需求放入 `docs/` | 统一的项目管理文档目录 | 分散的 `plans/` + `requirements/` 根目录 |
| ADR-004 | opencode 配置用 JSONC | 支持注释，方便文档说明 | JSON（无注释） |
| ADR-005 | 部署用 GitHub Actions | 自动化，无需手动配置 Pages 设置 | Pages 设置选 `/src` |

### 3.2 计划阶段（Plan Mode）

**输入**: 头脑风暴产出的目录结构方案
**输出**: 完整的任务分解清单

#### 任务分解

```
P0 — 创建目录结构
P0 — 创建 git 相关文件 (.gitignore, .nojekyll)
P0 — 创建 docsify 入口和书籍框架 (src/)
P0 — 创建 opencode + oh-my-openagent 配置
P0 — 创建编写计划和需求文档 (docs/)
P1 — 创建辅助文件和示例目录
P0 — git init
```

#### 风险评估

| 风险 | 概率 | 影响 | 应对措施 |
|------|------|------|---------|
| docsify basePath 配置错误 | 中 | 高 | 创建后立刻验证 `curl` 测试 |
| 书籍章节编号不一致 | 低 | 中 | 统一使用 `0N-` 前缀 |
| git 操作失误 | 低 | 低 | 先 init 不提交 |

### 3.3 实施阶段（Build Mode）

**输入**: 任务分解清单
**输出**: 47 个文件/目录 + git 初始化

#### 执行步骤与调用的工具

| 步骤 | 工具 | 操作 |
|------|------|------|
| 创建目录 | `mkdir -p` | 15+ 目录一次性创建 |
| 创建 git 文件 | `write` | `.gitignore`（OS/Node/IDE/Env 规则） |
| GitHub Pages 标记 | `write` | `.nojekyll` 空文件 |
| 项目说明 | `write` | `README.md`（中英文双语、章节大纲、目录说明） |
| docsify 入口 | `write` | `src/index.html`（docsify@4、搜索、emoji、bash/json 高亮） |
| 书籍导航栏 | `write` | `src/_sidebar.md`（7 章 19 篇文章的完整链接） |
| 书籍首页 | `write` | `src/README.md`（封面 + 目标读者 + 使用方式） |
| 7 章 README | `write` × 7 | 每章索引页 |
| 19 篇章节正文 | `write` × 19 | 含 TODO 占位的骨架内容 |
| opencode 配置 | `write` | `opencode.jsonc`（启用 oh-my-openagent 插件） |
| OMO 配置 | `write` | `.opencode/oh-my-openagent.jsonc`（骨架） |
| AGENTS.md | `write` | 给 AI agent 看的项目说明 |
| 编写计划 | `write` × 4 | 全书大纲 + 3 阶段计划 |
| 需求文档 | `write` × 2 | 用户故事 + PRD |
| GitHub Actions | `write` | `.github/workflows/deploy-docsify.yml` |
| 示例配置 | `write` × 2 | 基础 opencode 配置 + Hello World Skill |
| 启动脚本 | `write` | `scripts/serve.sh` |
| git init | `bash` | `git init && git branch -m main` |

#### AGENTS.md 两次迭代

| 版本 | 操作 | 内容 | 说明 |
|------|------|------|------|
| v1 | 创建 | `.opencode/AGENTS.md`（中文） | 初始创建含目录树和规范 |
| v2 | 重写 | 英文、精简 | 去除泛泛描述，仅保留 agent 可能遗漏的关键事实 |
| v3 | 确认 | 无变更 | 文件已是英文，无需修改 |

### 3.4 验证阶段

| 验证项 | 方法 | 结果 |
|--------|------|------|
| docsify 本地预览 | `docsify serve ./src` + `curl localhost:4000` | ✅ 正常返回 HTML |
| 目录结构完整性 | `find . -not -path './.git/*' -type f \| sort` | ✅ 46 个文件全部就位 |
| git 状态 | `git status --short` | ✅ 所有文件处于 untracked 状态 |
| 侧边栏链接可访问 | 手动检查 `_sidebar.md` 路径 | ✅ 所有路径与目录结构匹配 |

---

## 4. 技能调用记录

| 技能 | 调用时机 | 用途 |
|------|---------|------|
| `investigation-first` | 对话开始时 | 建立调查方法论，避免凭直觉做架构决策 |
| `agile-coach` | 最终任务 | 作为敏捷教练组织工作日志 |
| `using-superpowers` | 间接（通过 agile-coach 依赖） | 确认工作流规则 |

---

## 5. 模型与 Agent 使用记录

| Agent/模型 | 阶段 | 用途 |
|-----------|------|------|
| **Sisyphus（主协调器）** | 全部 | 需求确认、架构决策、任务分解、文件创建、验证 |
| **deepseek-v4-flash-free** | 全部 | 底层推理模型 |

**说明**: 本 session 未使用后台 Agent（explore/librarian/oracle），因为项目为从零初始化，所有信息可直接通过工具获取。

---

## 6. 创建的文件清单

### 项目根文件（5 个）

```
.gitignore              # Git 忽略规则
.nojekyll               # GitHub Pages 标记
README.md               # 项目说明
opencode.jsonc          # OpenCode 项目配置
```

### Git 配置（1 个）

```
.git/                   # git init（main 分支）
```

### GitHub Actions（1 个）

```
.github/workflows/deploy-docsify.yml  # 自动部署到 GitHub Pages
```

### OpenCode 配置（2 个）

```
.opencode/AGENTS.md                # 给 AI agent 看的项目说明（英文）
.opencode/oh-my-openagent.jsonc    # oh-my-openagent 插件配置骨架
```

### 书籍内容（27 个）

```
src/index.html                      # docsify 入口
src/README.md                       # 书籍首页
src/_sidebar.md                     # 章节导航
src/01-introduction/README.md        # 第1章索引
src/01-introduction/what-is-harness-engineer.md
src/01-introduction/why-opencode.md
src/02-core-concepts/README.md       # 第2章索引
src/02-core-concepts/agent-orchestration.md
src/02-core-concepts/skills-system.md
src/02-core-concepts/workflow-patterns.md
src/03-setup/README.md               # 第3章索引
src/03-setup/quickstart.md
src/03-setup/opencode-config.md
src/03-setup/oh-my-openagent-setup.md
src/04-workflows/README.md           # 第4章索引
src/04-workflows/ultrawork-mode.md
src/04-workflows/multi-agent-collab.md
src/04-workflows/custom-workflows.md
src/05-skills/README.md              # 第5章索引
src/05-skills/creating-skills.md
src/05-skills/skill-templates.md
src/05-skills/skill-best-practices.md
src/06-advanced/README.md            # 第6章索引
src/06-advanced/mcp-servers.md
src/06-advanced/custom-agents.md
src/06-advanced/context/performance-tuning.md
src/07-case-studies/README.md        # 第7章索引
src/07-case-studies/real-world-01.md
src/07-case-studies/real-world-02.md
```

### 项目管理文档（7 个）

```
docs/planning/requirements/book-outline.md          # 全书大纲
docs/planning/plans/phase-1-scaffold.md      # 第1阶段：搭建框架
docs/planning/plans/phase-2-content.md       # 第2阶段：内容编写
docs/planning/plans/phase-3-polish.md        # 第3阶段：打磨发布
docs/planning/requirements/user-stories.md   # 用户故事
docs/planning/requirements/prd.md            # 产品需求文档
docs/planning/specs/            # 详细规格目录（空）
```

### 辅助资源（5 个）

```
assets/images/.gitkeep              # 图片占位
examples/opencode-configs/basic.jsonc   # 示例配置
examples/skills/hello-world/SKILL.md    # Hello World Skill
scripts/serve.sh                    # 本地启动脚本
```

---

## 7. 经验教训与改进建议

### 做得好的

- **分层工作流**：先 Plan 再 Build，Plan 阶段充分调查和澄清需求，减少了 Build 阶段的返工
- **及时验证**：目录创建完毕后即时用 `curl` 测试 docsify 服务，确认配置正确
- **统一的目录命名**：章节采用 `0N-english-name`，排序友好且含义清晰
- **JSONC 格式**：选 JSONC 而非 JSON，支持注释方便后续维护

### 可改进的

- **工具调用频率**：大量独立的 `write` 调用可以通过 `task` 并行委托给子 agent 加速
- **AGENTS.md 未在 opencode.jsonc 中引用**：可以在 `opencode.jsonc` 中添加 `"instructions": ".opencode/AGENTS.md"`，让 opencode 自动加载
- **缺失 favicon**: `src/index.html` 引用了 `opencode.ai/favicon.ico`，可替换为项目自定义图标

### 后续 Sprint 建议

1. 将 `opencode.jsonc` 补全 provider 和 model 配置（当前仅为骨架）
2. 将 `.opencode/oh-my-openagent.jsonc` 补全 agent 和 categories 配置
3. 开始填充第 01~03 章的正文内容（P0 优先级）

---

## 附录

### A. 搜索的关键词与链接

- oh-my-openagent configuration → 确认 `.opencode/oh-my-openagent.jsonc` 路径
- docsify quickstart → 确认 docsify 结构与 basePath 配置
- GitHub Pages docsify → 确认 Actions 部署方案

### B. 引用的用户技能库

当前用户共有 75+ 技能，本次 Sprint 直接依赖 3 个：
- `investigation-first`
- `agile-coach`
- `using-superpowers`（间接）

### C. 配置文件 schema 引用

- opencode schema: `https://opencode.ai/config.json`
- oh-my-openagent schema: `https://raw.githubusercontent.com/code-yeongyu/oh-my-openagent/refs/heads/master/assets/oh-my-openagent.schema.json`
