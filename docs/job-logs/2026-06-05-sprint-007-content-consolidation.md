# 2026-06-05: Sprint 007: Content Consolidation

> [TAG: agile-coach]

## 基本信息

| 项目 | 内容 |
|------|------|
| Session ID | ses_... |
| Sprint 周期 | 2026-06-03 ~ 2026-06-05 |
| 风险等级 | 低 |
| 必需工作流 | agile-coach 回顾工作流 |
| 主模型 | deepseek-v4-flash-free |

## 1. 用户需求（输入）

### 1.1 原始需求
**主线任务**: 三个递进目标——从文章重写，到项目级规范升级，再到文档体系对齐。

| # | 任务 | 类型 | 验收标准 |
|---|------|------|---------|
| T1 | 记忆系统 + AGENTS.md 文章重写 | 内容深度升级 | 501 行 + 481 行，真实插件生态与 AGENTS.md 主体 |
| T2 | 项目 README + AGENTS.md 读者视角优化 | 项目级规范 | 说人话、从读者视角写、高信号指令 |
| T3 | PRD/用户故事/Specs 文档体系对齐 | 需求层统一 | 单一权威源、13 角色全覆盖 |

### 1.2 需求确认过程
触发原因：用户指出封面 tagline "将 AI 编程从'聊天对话'升级为'工程流水线'"不易理解。

**诊断**：
- "聊天对话" → 用户想"我用的是 Cursor/Claude Code，不是聊天框"
- "工程流水线" → 工厂意象，难以映射到 Agent 编排

## 2. 团队架构与角色分配

**协调人**: Sisyphus（敏捷教练模式）

团队成员通过背景任务执行具体工作：
- librarian 类型 Agent 负责调研任务
- unspecified-high 类型 Agent 负责内容重写和改写

## 3. 工作流阶段记录

### 3.1 头脑风暴阶段
在记忆系统和指令机制的调研阶段进行头脑风暴：
- 记忆系统调研：探索 OpenCode 原生记忆能力和真实插件生态
- 指令机制调研：分析 AGENTS.md 加载顺序和源代码实现

### 3.2 计划阶段
Sprint 规划阶段制定三个递进目标：
- T1: 记忆系统 + AGENTS.md 文章重写
- T2: 项目 README + AGENTS.md 读者视角优化  
- T3: PRD/用户故事/Specs 文档体系对齐

### 3.3 实施阶段
详细执行过程包括：

#### T1：高级话题文章重写
**记忆系统重写**：
```
Source: Claude Code 的 Memdir 架构（《马书》第24章）
→ 调研发现 OpenCode 原生无此机制
→ 转向真实插件生态调研
→ 四款插件对比选型
→ 文章重构为"插件选型 → Auto-Dream → Compaction协同 → 安全考虑"框架
→ 结果: 501 行，包含可运行的配置示例和决策树
```

**AGENTS.md 重写（含重命名）**：
```diff
- src/06-advanced/claude-dot-md.md (CLAUDE.md 为主体, 已删除)
+ src/06-advanced/agents-dot-md.md (AGENTS.md 为主体, 481行)
```

#### T2：项目级规范升级
**README.md 读者视角优化**：
```diff
- 将 AI 编程从"聊天对话"升级为"工程流水线"
+ 从"跟 AI 聊天写代码"到"用工程体系做开发"
```
同步更新了 `src/README.md`、`src/01-introduction/README.md`、项目根 `README.md` 三处。

**AGENTS.md 重建**：
- 旧版问题：章节结构表数据错误、CI 输出目录写错、包含通用知识、缺少读者视角写作原则
- 新版亮点："一句话说清" → "最容易翻车的地方" → 8 条高频事故、校验命令 → Mermaid 颜色规范 → 品牌名 → 写作原则

| 维度 | 旧版 | 新版 |
|------|------|------|
| 行数 | 155 行 | 118 行 |
| 章节数据 | **错误** | 基于文件大小的实际状态 |
| CI 目录 | `./book` ❌ | `_book` ✅ |
| 写作原则 | 无 | **第 8 条**：说人话、从读者视角写 |

#### T3：文档体系对齐
**统一映射权威源**：
- PRD §5.4 确认为 13 角色 → 智能体编排映射的单一权威源
- user-stories 映射表简化为速查简表，引用 PRD §5.4

**缺口的检查结果**：
- 7/7 内容章节 spec 全部包含"团队角色评审补充" → ✅ 已覆盖
- ch00-reader-guide.md 为读者导航，不需要团队角色评审 → ✅ 合理

### 3.4 验证阶段
- ✅ `mdbook build` 零错误
- ✅ 旧文件 `claude-dot-md.md` 已删除（全局搜索零残留）
- ✅ 链接引用全部更新（SUMMARY.md + 6 处跨文件引用）

## 4. 技能调用记录

| 技能名称 | 调用时机 | 用途 |
|---------|---------|------|
| agile-coach | Sprint 规划 + 团队组织 | 组织团队成员、生成工作日志 |
| 思维框架 | 内容审校 | 矛盾论/实践论 检查内容逻辑 |
| 人物视角 | 内容创作 | Musk/Karpathy/Feynman 提供差异化视角 |

## 5. 模型与 Agent 使用记录

| 组件 | 模型 | 用途 |
|------|------|------|
| 主编排器 | deepseek-v4-flash-free | 意图识别、任务分解、编排、决策 |
| 子 Agent | 各类型 | 调研 + 内容生成 + 文章改写 |

**Agent 执行记录**：
| Agent ID | 类型 | 用途 | 耗时 |
|----------|------|------|------|
| — (背景任务) | librarian | OpenCode 记忆系统调研 | ~11m |
| — (背景任务) | librarian | OpenCode 指令加载机制调研 | ~10m |
| — (背景任务) | unspecified-high | memory-system.md 重写 | ~13m |
| — (背景任务) | unspecified-high | agents-dot-md.md 重写+重命名 | ~12m |

## 6. 文件变更清单

### T1：文章重写
| 文件 | 行数 | 变更 |
|------|------|------|
| `src/06-advanced/memory-system.md` | 501 | 完全重写（真实插件生态） |
| `src/06-advanced/agents-dot-md.md` | 481 | **新增**（重命名+重写） |
| `src/06-advanced/claude-dot-md.md` | — | **删除** |
| `src/SUMMARY.md` | — | 链接更新 |
| `src/00-guide/reading-paths.md` | — | 6 处链接更新 |
| `docs/wiki/source-cross-references.md` | — | 引用更新 |
| `docs/plans/implementation-plan.md` | — | 文件名更新 |

### T2：项目规范升级
| 文件 | 变更 |
|------|------|
| `AGENTS.md` | 完全重建（118 行，清除数据错误） |
| `src/README.md` | TAGLINE 优化 |
| `README.md`（项目根） | TAGLINE 同步 |
| `src/01-introduction/README.md` | TAGLINE 同步 |

### T3：文档体系对齐
| 文件 | 变更 |
|------|------|
| `docs/requirements/prd.md` | v2.5 保留为权威源 |
| `docs/requirements/user-stories.md` | 映射表简化为速查引用 |
| `docs/job-logs/2026-06-05-sprint-007-content-consolidation.md` | **新增**（本日志） |

**全 Session 文件变更统计**：
```
  70 files changed, 10568 insertions(+), 2046 deletions(-)
```

| 变更类型 | 文件数 | 主要变更 |
|---------|-------|---------|
| src/ 正文 | 40+ | Ch1-Ch7 全仓内容增强、链接修复、记忆/AGENTS 改写 |
| docs/ 需求 | 10+ | PRD v2.5、user-stories v2.2、8 spec 文件 |
| docs/ 其他 | 5+ | 工作日志、review、cross-references、plans |
| 配置文件 | 2 | AGENTS.md（重建）、opencode.json（新增） |

## 7. 经验教训与改进建议

### 7.1 做得好的
| # | 教训 | 场景 | 建议 |
|---|------|------|------|
| 1 | **调研先行** | 重写记忆系统前做了 2 个调研 Agent → 避免基于错误假设写内容 | 技术文章改写必须先验证当前版本的真实性 |
| 2 | **单一权威源** | PRD 和 user-stories 映射表重复维护 → 必然不同步 | 需求文档采用"权威源 + 引用"模式 |
| 3 | **AGENTS.md 信号密度** | 旧版包含通用知识（opencode 安装命令）→ 浪费上下文 | 每行自问：不给这个信息 agent 会犯错吗？ |
| 4 | **读者视角不是口号** | TAGLINE 修改前后对比说明：说人话需要刻意练习 | 用"你能对应上自己的使用场景吗"检验每段话 |
| 5 | **批量编辑需验证链** | 70 文件编辑后 mdbook build 零错误 → 全文回滚风险降到最低 | 每次内容变更后立即构建验证 |

### 7.2 可改进的
（原文中未明确列出可改进的具体点，但从经验教训中可以推断）
- 需要更系统地收集团队成员反馈
- 可以进一步细化任务分解粒度
- 某些链接更新可能遗漏，需要更全面的验证机制

### 7.3 后续 Sprint 建议
- 继续保持调研先行的原则
- 深化单一权威源的应用范围
- 持续优化 AGENTS.md 的信号密度
- 在读者视角写作上进行更多刻意练习
- 建立更完善的内容变更验证流程

## 附录

### 6.1 全 Sprint 指标
| 指标 | 数值 |
|------|------|
| 任务数 | 3（文章重写 + 规范升级 + 文档对齐） |
| 子 Agent 总数 | 4（全部调研+改写背景任务） |
| 其中正确结果 | 4（100%） |
| 直接工具调用 | ~50+ |
| 修改文件数 | 70 |
| 新增代码行数 | 10,568 |
| 删除代码行数 | 2,046 |
| TAGLINE 更新 | 3 文件（src/README + 项目 README + Ch1 README） |
| AGENTS.md 重建 | 118 行（从 155 行精简，清除数据错误） |
| 构建验证 | mdbook build ✅ 零错误 |

### 6.2 全部使用的工具
| 工具 | 调用次数 | 用途 |
|------|---------|------|
| `read` | 40+ | 读取文件、目录结构 |
| `write` | 3 | 工作日志、AGENTS.md 重建 |
| `edit` | 10+ | 内容编辑、链接修正 |
| `bash` | 15+ | grep 验证、mdbook build、git log |
| `grep` | 20+ | 残留检查、链接验证 |
| `task (background)` | 4 | 调研 + 改写 |
| `background_output` | 4 | 收集 Agent 结果 |
| `todowrite` | 3 | 任务跟踪 |
| `session_read` | 2 | 获取 session 元数据 |
| `session_list` | 1 | 搜索相关 session |
| `question` | 2 | 方案确认（tagline + 作战计划） |
| `glob` | 5+ | 查找文件 |
| `session_info` | 1 | session 详情 |

> **协调人**: Sisyphus
> **日期**: 2026-06-05
> **核心教训**: 调研先于改写、权威源取代副本、读者视角需刻意落地