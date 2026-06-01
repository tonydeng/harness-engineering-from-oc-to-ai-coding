# 章节重构计划

> **给执行代理：** 本计划定义章节级别的内容增补顺序和范围，非逐文件实现任务。实际写作任务需进一步分解为文章级任务。

**目标：** 基于3个外部资料库（HE实践、《驾驭工程：从 Claude Code 源码到 AI 编码最佳实践》（中文别名：《马书》）、马书读书笔记）和现有13个读者角色45个用户故事的深度分析，重构本书7章的内容结构和覆盖范围。

**架构：** 保留现有的7章框架 + Ch0，每章按"概念讲解 → 实战示例 → 最佳实践"三层结构增补内容。4个P0缺口优先填充，P1缺口按依赖顺序推进。

**核心参考资料：**
- HE实践：`/Users/tonydeng/workspace/gitee/user-requ/AI研究/Harness Engineering实践/`
- 马书读书笔记：`/Users/tonydeng/workspace/gitee/user-requ/AI研究/马书读书笔记/`
- cc-to-ai-book：`/Users/tonydeng/workspace/github/harness-engineering-from-cc-to-ai-coding/`

---

## 内容缺口优先级总览

| 优先级    | 缺口                           | 影响章节    | 外部资料依据                           | 工作量 |
| ------ | ---------------------------- | ------- | -------------------------------- | --- |
| **P0** | Harness Engineering 理论框架完整性  | Ch1     | HE实践 01（584行），《马书》第25-27章          | L   |
| **P0** | 上下文工程 / 记忆系统 / 提示词缓存         | Ch6 新增  | 《马书》第3-4篇（12章 + 长篇），HE实践 02        | XL  |
| **P0** | 安全防御体系（权限/注入防御/沙箱/Hooks）     | Ch6     | 《马书》第5篇（6章），HE实践 02 §2             | L   |
| **P0** | 可观测性与监控（Hook点/Telemetry）     | Ch6     | 《马书》第29章，OMO 54+ 事件体系              | M   |
| **P1** | 工具生态对比表                      | Ch1     | HE实践 04（678行），包含 24+ 工具          | M   |
| **P1** | 国产 AI 工具链配置                  | Ch3     | HE实践 04 §国产工具，Trae/CodeGeeX/通义灵码 | S   |
| **P1** | 角色阅读路径                       | Ch0     | 马书读书笔记有 4 种路径推荐                  | S   |
| **P1** | 案例研究扩展到 4-5 个                | Ch7     | HE实践 02（1137行），《马书》第30章            | L   |
| **P2** | Agent派生 / Teams 多进程协作工作流     | Ch4     | 《马书》第20-20b章                       | M   |
| **P2** | MCP 桥接与插件系统                  | Ch5/Ch6 | 《马书》第22-22b章，HE实践 02               | M   |
| **P2** | Effort/Fast Mode/Thinking 优化 | Ch6     | 《马书》第21章                           | S   |

---

## 章节详细重构方案

### Ch0: 读者导航（增补）

**当前状态：** 1 个 README，内容为空
**目标状态：** 完整的读者决策指南 + 角色阅读路径

**新增文章：**
- `00-guide/reading-paths.md`：按 13 个读者角色的阅读路径推荐（参考马书读书笔记的4路径模式）
- `00-guide/how-to-read.md`：2 种阅读方式（线性通读 / 按角色跳读）

**外部资料引用：**
- 马书读书笔记 README §阅读建议（角色路径模式）
- AGENTS.md §用户故事规范（13 角色定义）

---

### Ch1: 简介（大幅增补）

**当前状态：** 2 篇文章，偏薄
**目标状态：** Harness Engineering 完整理论框架 + 工具生态全景

**新增文章：**
| 文章 | 内容 | 来源 |
|------|------|------|
| `harness-engineering-theory.md` | 定义、5大分类法（Fowler）、演进时间线 2024→2026 | HE实践 01 |
| `ecosystem-comparison.md` | OpenCode vs Cursor vs Claude Code vs Codex vs Cline vs Windsurf 对比 | HE实践 04 |
| `chinese-ecosystem.md` | 国产方案（Trae、CodeGeeX、通义灵码、文心快码）全景 | HE实践 04 §国产 |

**现有文章修改：**
- `what-is-harness-engineer.md`：增补 Mitchell Hashimoto 原始定义 + Harrison Chase "Agent = Model + Harness" 公式
- `why-opencode.md`：增补 OMO v4.5+ 特性（11+ Agent, 53+ Hook点）

---

### Ch2: 核心概念（中等增补）

**当前状态：** 3 篇文章（Agent/Skill/Workflow），基本结构合理
**目标状态：** 补充 3 个新核心概念 + 《马书》体系交叉引用

**新增文章：**
| 文章 | 内容 | 来源 |
|------|------|------|
| `context-engineering-core.md` | 上下文工程作为核心概念：压缩、缓存、Token预算 | 《马书》第3-4篇，HE实践 03 §实践一 |
| `constraints-system.md` | 约束系统：权限模型、架构护栏、lint规则 | 《马书》第5篇（权限），HE实践 03 §实践二 |
| `validation-harness.md` | 验证护栏：质量门禁、YOLO分类、自动验证 | 《马书》第17章，HE实践 03 §实践三 |

**改写文章：**
- `agent-orchestration.md`：增加《马书》Agent Loop 状态机视角的对比
- `workflow-patterns.md`：增加《马书》6 种工作流模式引用

---

### Ch3: 环境搭建（中等增补）

**当前状态：** 3 篇文章，基本完整
**目标状态：** 国产 AI 模型配置支持 + 多环境部署方案

**新增文章：**
| 文章 | 内容 | 来源 |
|------|------|------|
| `chinese-providers.md` | 国产模型配置（DeepSeek/Kimi/Qwen）：API配置、典型参数、注意事项 | HE实践 04，HE实践 README §国产环境 |
| `multi-env-setup.md` | 多环境配置：本地dev / CI / 生产，Profile切换最佳实践 | 现有技巧来自 04 §Profile |

**修改文章：**
- `opencode-config.md`：增加 Category 路由配置详解 + OMO v4.5+ 新配置项
- `oh-my-openagent-setup.md`：增加 OMO 11+ Agent 注册表引用

---

### Ch4: 工作流实战（微调增补）

**当前状态：** 3 篇文章，本模块较成熟
**目标状态：** 补充 Agent 高级协作模式

**新增文章：**
| 文章 | 内容 | 来源 |
|------|------|------|
| `agent-derivation.md` | Agent 派生模式：子Agent、委派、协调者模式 | 《马书》第20章 |
| `teams-collaboration.md` | 多进程协作：Teams 架构、消息传递、进程内集群 | 《马书》第20b章 |

**修改文章：**
- `ultrawork-mode.md`：增补 Ralph Loop / /ulw-loop 机制详解
- `multi-agent-collab.md`：增补 Hyperplan 5批评者对抗式规划 + security-research模式

---

### Ch5: Skill 开发（微调增补）

**当前状态：** 3 篇文章，结构合理
**目标状态：** 补充 MCP 桥接和插件化模式

**新增文章：**
| 文章 | 内容 | 来源 |
|------|------|------|
| `skill-mcp-bridge.md` | Skill 作为 MCP 桥接层：如何包装外部工具为可复用 Skill | 《马书》第22章，HE实践 02 |
| `plugin-patterns.md` | Skill 插件化：从独立 Skill → Skill 市场 → 组合 Skill | 《马书》第22b章 |

---

### Ch6: 高级话题（大幅扩展）

**当前状态：** 3 篇文章，篇幅不足。**这是内容缺口最大的章节**
**目标状态：** 覆盖完整的高级技术栈

**新增文章：**
| 文章 | 内容 | 来源 | 优先级 |
|------|------|------|--------|
| `context-compression.md` | 自动压缩原理 + 微压缩 + 压缩后恢复 | 《马书》第9-11章 | **P0** |
| `token-budget.md` | Token预算策略、估算规则、预算分配 | 《马书》第12章 | **P0** |
| `prompt-caching.md` | 三级缓存架构、缓存断点、中断检测、7+优化模式 | 《马书》第13-15章 | **P0** |
| `memory-system.md` | 跨会话记忆：Memdir架构、Auto-Dream、Compaction | 《马书》第24章 | **P0** |
| `security-overview.md` | 安全总览：权限模型(6模式)、YOLO分类器、提示注入防御 | 《马书》第16-17b章 | **P0** |
| `sandbox-hooks.md` | 沙箱系统(Seatbelt/Bubblewrap) + Hook点(53+事件) | 《马书》第18-18b章，OMO Hook | **P0** |
| `claude-dot-md.md` | CLAUDE.md 用户指令覆盖层 + @include 指令系统 | 《马书》第19章 | **P0** |
| `observability.md` | 可观测性：logEvent、5层遥测架构、生产级监控 | 《马书》第29章，OMO 54+事件 | **P0** |
| `feature-flags.md` | OMO 89个Feature Flag 路线图、产品演进方向 | 《马书》第23章 | P2 |

**修改文章：**
- `mcp-servers.md`：扩展 MCP 协议深度（stdio/SSE/WebSocket）、ToolRegistry 统一、MCP 服务器沙箱
- `custom-agents.md`：增加《马书》三种Agent派生模式 + Effort/Fast Mode/Thinking 配置
- `performance-tuning.md`：增加模型降级链、成本优化、Token预算策略

---

### Ch7: 案例研究（大幅扩展）

**当前状态：** 2 篇文章（微服务 + 遗留系统）
**目标状态：** 4-5 个案例，覆盖不同维度的 Harness Engineering 实践

**新增案例文章：**
| 案例 | 内容 | 来源 | 优先级 |
|------|------|------|--------|
| `case-security-audit.md` | 安全审计流水线：红队+蓝队全流程，渗透测试自动化 | HE实践 02（Cline案例），《马书》第30章 | P1 |
| `case-full-pipeline.md` | 需求→PR 全流程自动化：需求分析→设计→开发→测试→Review→部署 | HE实践 02（Codex案例） | P1 |
| `case-multi-model.md` | 国产模型+OpenCode 混合架构：DeepSeek经济模型 + GPT 复杂推理的 Harness 设计 | HE实践 04 §国产工具 | P1 |
| `case-skills-marketplace.md` | 团队级 Skill 市场建设：从零构建内部 Skill 生态 | 《马书》第22-22b章，HE实践 03 | P2 |

**修改文章：**
- `real-world-01.md`：增补 Martin Fowler Harness Template 对照分析
- `real-world-02.md`：增补灰度策略 + 增量演进的具体步骤

---

## 执行顺序

```
Phase 1: P0 基础（并行）
├── Ch6 上下文工程/记忆/缓存 ──── 最大工作量，先行启动
├── Ch6 安全体系 ──────────────── 依赖 Ch2 约束系统概念
└── Ch1 理论框架 ──────────────── 全书理论基石

Phase 2: 横向增补
├── Ch2 新核心概念 ────────────── 为 Ch3/Ch4/Ch6 提供前置概念
├── Ch0 读者导航 ──────────────── 依赖读者角色定义
└── Ch6 可观测性 ──────────────── 依赖 Hook 点概念

Phase 3: 生态与案例
├── Ch1 工具对比 + Ch3 国产配置 ─ 市场定位
├── Ch4/Ch5 微调增补 ─────────── 现有模块增强
└── Ch7 新增案例 ──────────────── 依赖所有前置概念
```

---

## 工作量估算

| 章节 | 新增文章 | 修改文章 | 估算工作量 |
|------|---------|---------|-----------|
| Ch0 | 2 | 1 | 3 天 |
| Ch1 | 3 | 2 | 5 天 |
| Ch2 | 3 | 2 | 5 天 |
| Ch3 | 2 | 2 | 3 天 |
| Ch4 | 2 | 2 | 3 天 |
| Ch5 | 2 | 0 | 2 天 |
| Ch6 | 9 | 3 | 15 天（含 P0 核心 7 篇） |
| Ch7 | 4 | 2 | 6 天 |
| **合计** | **27** | **14** | **42 天** |

---

## 验证标准

- [ ] 每篇文章 ≥200 行（L1 质量门禁）
- [ ] 每篇包含可运行的代码/配置示例
- [ ] 所有跨章节引用格式正确（→ [§章节 标题](路径)）
- [ ] 新增术语符合写作规范（首次出现标注中英文）
- [ ] 所有 Mermaid 图表渲染正确
- [ ] 13 个读者角色均有对应的阅读路径
- [ ] 45 个用户故事均被覆盖

---

## 外部资料引用规范

引用外部资料时遵循：
```
来源：HE实践 01 §[章节名]
来源：《马书》[第X章](https://zhanghandong.github.io/harness-engineering-from-cc-to-ai-coding/#/chXX) §[小节名]
来源：cc-to-ai 第X部分 §[内容描述]
```

所有引用在定稿后统一纳入 `docs/wiki/source-cross-references.md`。

---

> **版本**: v1.0 | **创建**: 2026-05-31 | **制作者**: 敏捷教练
> **前置输入**: HE实践（4文件4073行）、《马书》读书笔记（30章）、cc-to-ai book（7部分）
> **基于**: 13读者角色45用户故事 + 8角色团队评审结果
