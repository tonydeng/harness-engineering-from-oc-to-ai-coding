# 源材料交叉引用

> OpenCode实战 源材料与 Harness Engineering 书籍之间的双向追溯矩阵。
> 维护者：当源章节更新或书籍内容变更时，请更新本文档。

---

## 第一节：源材料清单

| # | 源文件 | 行数 | 核心主题 | 关键章节 | 质量 | 新鲜度 |
|---|-------------|-------|-----------|-------------|---------|-----------|
| 01 | `01-核心概念速通.md` | ~1051 | 6核心概念(Agent/Skill/Command/Plugin/Team/MCP)的OS类比讲解 + 安装与配置指南 | §Agent(执行主体), §Skill(专业技能包), §Command(快捷指令), §Plugin(扩展能力), §Team(多Agent协作), §MCP(外部协议), §概念关系图, §附录A-E | ✅ 生产就绪 | 2026-05 |
| 02 | `02-架构全景解析.md` | ~1541+ | OpenCode三层架构 + OMO多智能体扩展 + 部署架构 + 数据架构 | §产品架构(TUI/Desktop/ACP), §技术架构(三层), §部署架构(本地/远程/Web), §OMO架构扩展(11+ Agent/类别路由/Ultrawork/Team Mode/版本演进), §非功能架构(安全/成本/可观测性) | ✅ 生产就绪 | 2026-05 |
| 03 | `03-概念联动实战.md` | ~1365 | 6概念6种联动模式 + 7-Agent Pipeline + AGENTS.md + 团队工作流 | §1-6(6种联动模式: C+A/S+A/P+T/T+S/C+A+S), §6(全链路图), §7(常见问题), §9(7-Agent Pipeline/安全权限/AGENTS.md/Token优化/反模式) | ✅ 生产就绪 | 2026-05 |
| 04 | `04-奇淫技巧与实战方案.md` | ~1292 | 12个高级技巧 + 4个行业工作台方案 + 入門指南 | §技巧1-12(Profile/AGENTS.md/Pipeline/Memory/权限/成本/安全/命令/审计/快速构建/DSL/协作), §方案1-4(PM/架构师/DevOps/安全工作台), §附录(安装/入門/速查/学习路线) | ⚠️ 部分内容待验证 | 2026-05 |
| 05 | `05-场景化实战案例.md` | ~994 | 5个端到端案例 + Skill开发附录 | §案例1(REST API从零搭建), §案例2(安全审计遗留项目), §案例3(需求→产品全流程), §案例4(AI知识库构建), §案例5(团队协作), §附录(SKILL开发与Team Mode集成指南), §总结(十大铁律/反模式/效果指标) | ⚠️ 部分内容待验证 | 2026-05 |

---

## 第二节：源材料 → 书籍映射

### 01-核心概念速通 → 书籍
| 源材料章节 | 书籍位置 | 改编说明 |
|----------------|---------------|----------------|
| OS类比表（Agent=进程, Skill=驱动, etc.） | Ch1 Art.1.1 | 直接使用 — 完美类比，用于 Harness Engineering 引言 |
| Agent：执行主体 | Ch2 Art.2.1 | 直接使用 — 增加 OMO 11+ Agent 扩展内容 |
| Skill：专业技能包 | Ch2 Art.2.2 | 直接使用 — 增加 Scoped Skills 和 Marketplace 内容 |
| Command：快捷指令 | Ch2 Art.2.3 | 直接使用 — 与源材料 04 Profile 切换整合 |
| Plugin：扩展能力 | Ch2 Art.2.2 | 仅引用 — 详细 Plugin 内容在第6章 |
| Team：多Agent协作 | Ch2 Art.2.1 | 仅引用 — 详细 Team Mode 内容在第4章 |
| MCP：概念+配置 | Ch6 Art.6.1 | 基础 — 用源材料 02 MCP 集成扩展 |
| 概念关系图 | Ch2 Art.2.2 | 直接使用 — 关键图表 |
| 安装指南 | Ch3 Art.3.1 | 直接使用 — 为 v1.15.x 更新 Provider 名称 |
| Provider配置 | Ch3 Art.3.1 | 直接使用 — 添加 Zen 流程 |
| 上下文工程基础概念 | Ch2 Art.2.4 | 基础引用 — 引出上下文工程作为核心概念 |
| 约束系统基础概念 | Ch2 Art.2.5 | 基础引用 — 引出权限模型概念 |
| 验证护栏基础概念 | Ch2 Art.2.6 | 基础引用 — 引出质量门禁概念 |

### 02-架构全景解析 → 书籍
| 源材料章节 | 书籍位置 | 改编说明 |
|----------------|---------------|----------------|
| 产品架构（TUI/Desktop/ACP） | Ch2 Art.2.3 | 仅引用 — 为 Command/Agent 讨论提供背景 |
| 技术架构三层详解 | Ch3 Art.3.2 | 改编 — 聚焦 opencode.json 结构，非 Rust 内部实现 |
| 配置路径汇总 | Ch3 Art.3.2 | 直接使用 — 关键参考表 |
| OMO Agent体系 | Ch3 Art.3.3 | 改编 — 聚焦 Sisyphus/Atlas/Hephaestus，非全部 13 个 |
| OMO类别路由 | Ch3 Art.3.3 | 直接使用 — 完整章节 |
| OMO Ultrawork Mode | Ch4 Art.4.1 | 直接使用 — 完整章节 |
| OMO Team Mode | Ch4 Art.4.3 | 直接使用 — 增加 12 个 team_* 工具 |
| OMO Hyperplan | Ch4 Art.4.3 | 直接使用 — 增加 team 配置 |
| OMO Scoped Skills | Ch5 Art.5.1 | 直接使用 — target_agent 字段 |
| OMO Hashline | Ch6 Art.6.3 | 直接使用 — 0% 陈旧行编辑 |
| OMO Hook点53+ | Ch6 Art.6.2 | 仅引用 — 列出关键 Hook |
| 成本架构 | Ch6 Art.6.3 | 直接使用 — Token 预算 + 模型降级 |
| 安全架构4层 | Ch3 Art.3.2 | 改编 — 聚焦面向用户的配置，非内部架构 |
| 可观测性54+事件 | Ch6 Art.6.3 | 仅引用 — 列出有用的监控事件 |
| MCP集成 | Ch6 Art.6.1 | 直接使用 — MCP 客户端架构 |
| 版本演进 | Ch3 Art.3.3 | 直接使用 — v4.0→v4.5 |
| 上下文压缩原理 | Ch6 Art.6.4 | 改编 — 从架构视角解释压缩机制 |
| Token 预算机制 | Ch6 Art.6.5 | 直接使用 — 预算分配策略 |
| 提示词缓存架构 | Ch6 Art.6.6 | 改编 — 聚焦三级缓存 |
| 记忆系统架构 | Ch6 Art.6.7 | 直接使用 — Memdir 架构 |
| 安全架构与权限模型 | Ch6 Art.6.8 | 直接使用 — 扩展马书6模式视角 |
| 沙箱与Hook点 | Ch6 Art.6.9 | 直接使用 — 53+ Hook分类 |
| 可观测性54+事件 | Ch6 Art.6.11 | 直接使用 — 5层遥测架构 |
| Feature Flags 路线图 | Ch6 Art.6.12 | 直接使用 — 89 Flag分类 |
| 全流程自动化 | Ch7 Art.7.4 | 改编 — HE实践Codex案例适配 |
| 安全审计流水线 | Ch7 Art.7.3 | 改编 — HE实践Cline案例适配 |

### 03-概念联动实战 → 书籍
| 源材料章节 | 书籍位置 | 改编说明 |
|----------------|---------------|----------------|
| Command + Agent联动 | Ch4 Art.4.3 | 改编 — 与 Workflow 设计整合 |
| Skill + Agent (Scoped) | Ch2 Art.2.2 | 直接使用 — 增加 target_agent 细节 |
| Plugin + Tool | Ch6 Art.6.2 | 改编 — 用源材料 04 Env Guard 扩展 |
| Team + Skill | Ch4 Art.4.3 | 直接使用 — Hyperplan + security-research |
| Config + Agent + Skill | Ch3 Art.3.2 | 直接使用 — 完整注释的 opencode.json |
| 全链路流程图 | Ch7 Art.7.1 | 直接使用 — 案例研究的关键图表 |
| 7-Agent Pipeline | Ch4 Art.4.2 | 直接使用 — 完整章节 |
| 安全权限配置 | Ch3 Art.3.2 | 直接使用 — 风险等级表 |
| AGENTS.md金字塔结构 | Ch2 Art.2.3 | 直接使用 — 模板 |
| Token效率优化 | Ch6 Art.6.3 | 直接使用 — .opencodeignore, ripgrep, Context7 |
| 反模式清单 | Ch5 Art.5.3 | 直接使用 — 用源材料 04 反模式扩展 |
| 团队命令库 | Ch2 Art.2.3 | 直接使用 — 目录结构 |
| Agent 派生概念 | Ch4 Art.4.4 | 改编 — 三种派生模式详解 |
| Teams 多进程协作 | Ch4 Art.4.5 | 改编 — 进程内集群与独立Agent |

### 04-奇淫技巧与实战方案 → 书籍
| 源材料章节 | 书籍位置 | 改编说明 |
|----------------|---------------|----------------|
| Profile切换 | Ch2 Art.2.3 | 改编 — 聚焦 dev/review/debug 三个 Profile |
| AGENTS.md规范 | Ch2 Art.2.3 | 直接使用 — 增加分层注入策略 |
| Pipeline as Team | Ch4 Art.4.2 | 仅引用 — 与 7-Agent Pipeline 对比 |
| Compaction + Mem0 MCP | Ch6 Art.6.3 | 仅引用 — 跨会话记忆策略 |
| Bash白名单 | Ch3 Art.3.2 | 仅引用 — 高级权限模式 |
| 模型降级链 | Ch6 Art.6.3 | 直接使用 — 完整成本优化章节 |
| Env Guard Plugin | Ch6 Art.6.2 | **直接使用 — 完整代码** |
| Command Families | Ch2 Art.2.3 | 仅引用 — 高级命令模式 |
| 一键安全审计 | Ch7 Art.7.2 | 直接使用 — 集成到遗留系统案例 |
| 从零快速构建 | Ch7 Art.7.1 | 直接使用 — 集成到微服务案例 |
| Skill做DSL | Ch5 Art.5.3 | 直接使用 — 最佳实践 |
| 共享Session | 仅引用 | 省略 — 过于小众，不适合单篇文章 |
| PM工作台方案 | 仅引用 | 省略 — 让读者从模板推导 |
| 架构师/DevOps/安全工作台 | 仅引用 | 省略 — 让读者从模板推导 |
| 国产模型配置 | Ch3 Art.3.4 | 直接使用 — DeepSeek/Kimi/Qwen配置 |
| 多环境配置（Profile） | Ch3 Art.3.5 | 直接使用 — 本地dev/CI/生产三环境 |
| 工具生态对比 | Ch1 Art.1.4 | 引用+网络调研 — 6工具全景对比 |
| Harness Engineering理论 | Ch1 Art.1.3 | 引用 — 5大分类法+时间线 |
| 国产AI生态 | Ch1 Art.1.5 | 直接使用 — 国产方案全景 |
| Skill-MCP桥接 | Ch5 Art.5.4 | 改编 — Skill作为MCP桥接层 |
| Skill插件化模式 | Ch5 Art.5.5 | 改编 — 独立→市场→组合 |

### 05-场景化实战案例 → 书籍
| 源材料章节 | 书籍位置 | 改编说明 |
|----------------|---------------|----------------|
| 案例1: REST API从零搭建 | Ch7 Art.7.1 | **大幅改编** — 扩展展示所有 6 个概念协作 |
| 案例2: 安全审计遗留项目 | Ch7 Art.7.2 | **大幅改编** — 增加时间线、渐进式策略 |
| 案例3: 需求→产品全流程 | Ch7 Art.7.2 (ref) | 仅引用 — 改编多角色流程中的部分内容 |
| 案例4: AI知识库构建 | 仅引用 | 省略 — 非书籍核心叙事 |
| 案例5: 团队协作远程 | 仅引用 | 省略 — 过于具体 |
| SKILL开发附录 | Ch5 Art.5.1-5.3 | 直接使用 — 完整格式文档 |
| 十大铁律 | Ch7 Conclusion | 改编 — 集成到案例研究结论 |
| 常见反模式 | Ch5 Art.5.3 | 直接使用 |
| 效果指标表 | Ch7 Conclusion | 直接使用 |
| 安全审计案例（Cline） | Ch7 Art.7.3 | **大幅改编** — 红蓝队全流程自动化 |
| 全流程案例（Codex） | Ch7 Art.7.4 | **大幅改编** — 需求→PR全流程 |
| 国产模型混合架构 | Ch7 Art.7.5 | **大幅改编** — DeepSeek+GPT混合 |
| 团队Skill市场建设 | Ch7 Art.7.6 | **大幅改编** — 内部Skill生态 |

---

## 第三节：书籍 → 源材料反向映射

| 书籍章节 | 主要源材料 | 次要源材料 | 需要网络调研？ |
|-------------|---------------|-----------------|--------------------------|
| Ch0: 读者决策指南 | — | PRD §5.2 (读者画像), 团队评审画像 | 否 — 源自 PRD |
| Ch1 Art.1.1: 什么是 Harness Engineer | 01 (OS类比, 引言) | 04 (Profile/AGENTS.md理念) | 否 |
| Ch1 Art.1.2: 为什么选择 OpenCode | 01 (FAQ, 附录) | 02 (架构对比) | 是 — 当前市场对比 |
| Ch1 Art.1.3: Harness Engineering理论 | HE实践 01 | — | 否 |
| Ch1 Art.1.4: 工具生态对比 | HE实践 04 | — | 是 — 6工具最新对比 |
| Ch1 Art.1.5: 国产AI生态 | HE实践 04 §国产 | — | 是 — 国产工具最新动态 |
| Ch2 Art.2.1: Agent 系统 | 01 (Agent 章节) | 02 (OMO Agent体系) | 否 |
| Ch2 Art.2.2: Skill 系统 | 01 (Skill 章节) | 03 (Scoped Skills) | 否 |
| Ch2 Art.2.3: Workflow 模式 | 01 (Command 章节) | 03 (AGENTS.md) + 04 (Profile) | 否 |
| Ch2 Art.2.4: 上下文工程核心 | 马书第3-4篇 | HE实践 03 §实践一 | 否 |
| Ch2 Art.2.5: 约束系统 | 马书第5篇 | HE实践 03 §实践二 | 否 |
| Ch2 Art.2.6: 验证护栏 | 马书第17章 | HE实践 03 §实践三 | 否 |
| Ch3 Art.3.1: 快速开始 | 01 (附录 A/B) | 04 (附录安装指南) | 是 — 最新安装命令 |
| Ch3 Art.3.2: 配置深入 | 03 (Config 章节) | 02 (配置路径/安全架构/成本) | 否 |
| Ch3 Art.3.3: OMO 集成 | 02 (OMO 整章) | — | 是 — 最新 OMO v4.5 特性 |
| Ch3 Art.3.4: 国产模型配置 | HE实践 04 | HE实践 README §国产环境 | 是 — 国产模型API更新 |
| Ch3 Art.3.5: 多环境部署 | 04 §Profile | — | 否 |
| Ch4 Art.4.1: Ultrawork 模式 | 02 (Ultrawork) | 03 (对比表) | 否 |
| Ch4 Art.4.2: 多 Agent | 03 (7-Agent Pipeline) | 04 (Pipeline as Team) | 否 |
| Ch4 Art.4.3: 自定义工作流 | 02 (Team Mode) | 03 (Hyperplan/security-research) | 否 |
| Ch4 Art.4.4: Agent派生模式 | 马书第20章 | — | 否 |
| Ch4 Art.4.5: Teams多进程协作 | 马书第20b章 | — | 否 |
| Ch5 Art.5.1: 创建 Skill | 01 (SKILL.md 格式) | 05 (Skill 开发附录) | 否 |
| Ch5 Art.5.2: Skill 模板 | 01 (agile-coach 示例) | 04 (DSL, 工作台模式) | 否 |
| Ch5 Art.5.3: 最佳实践 | 03 (反模式) | 04 (技巧) + 05 (调试清单) | 否 |
| Ch5 Art.5.4: Skill-MCP桥接 | 马书第22章 | HE实践 02 | 否 |
| Ch5 Art.5.5: Skill插件化模式 | 马书第22b章 | — | 否 |
| Ch6 Art.6.1: MCP 服务器 | 01 (MCP 章节) | 02 (MCP 集成架构) | 是 — 最新 MCP 协议规范 |
| Ch6 Art.6.2: 自定义 Agent 和 Plugin | 01 (Plugin 章节) | 04 (Env Guard 完整代码) + 02 (OMO Hook点) | 否 |
| Ch6 Art.6.3: 性能调优 | 02 (成本架构) | 03 (Token优化) + 04 (模型降级链) | 否 |
| Ch6 Art.6.4: 上下文压缩 | 马书第9-11章 | — | 否 |
| Ch6 Art.6.5: Token预算策略 | 马书第12章 | — | 否 |
| Ch6 Art.6.6: 提示词缓存 | 马书第13-15章 | — | 否 |
| Ch6 Art.6.7: 记忆系统 | 马书第24章 | — | 否 |
| Ch6 Art.6.8: 安全总览 | 马书第16-17b章 | — | 否 |
| Ch6 Art.6.9: 沙箱与Hook系统 | 马书第18-18b章 | OMO Hook | 否 |
| Ch6 Art.6.10: CLAUDE.md系统 | 马书第19章 | — | 否 |
| Ch6 Art.6.11: 可观测性 | 马书第29章 | OMO 54+事件 | 否 |
| Ch6 Art.6.12: Feature Flags | 马书第23章 | — | 否 |
| Ch7 Art.7.1: 微服务案例 | 05 (案例1) | 03 (全链路图) | 否 |
| Ch7 Art.7.2: 遗留系统案例 | 05 (案例2, 案例3) | 03 (7-Agent Pipeline) | 否 |
| Ch7 Art.7.3: 安全审计流水线 | HE实践 02 (Cline案例) | 马书第30章 | 否 |
| Ch7 Art.7.4: 全流程自动化 | HE实践 02 (Codex案例) | — | 否 |
| Ch7 Art.7.5: 国产模型混合架构 | HE实践 04 §国产 | — | 是 — 国产模型最新动态 |
| Ch7 Art.7.6: 团队Skill市场 | 马书第22-22b章 | HE实践 03 | 否 |

---

## 第三节B：多角色评审覆盖（团队角色Review补充）

| 读者角色 | 重点章节 | 评审关注点 | 映射到内容缺口 |
|-------------|-------------------|--------------------------|-----------------------|
| **需求分析师** | Ch1, Ch2 | 读者画像完整性，内容可追溯性 | Ch0 读者指南，PRD §5 扩展 |
| **架构顾问** | Ch3, Ch7 | 架构决策日志，部署拓扑 | PRD §附录A 中的 ADR 模板 |
| **后端架构师** | Ch4, Ch6 | Pipeline 错误处理，API 版本策略 | Ch4 规格§补充，Ch6 规格§补充 |
| **前端架构师** | Ch2, Ch3 | 侧边栏 UX，Docsify 插件配置，移动端导航 | src/index.html 修复，侧边栏更新 |
| **UI设计师** | Ch0, Ch1 | 视觉层级，Ch0→Ch1 读者流程 | Ch0 页面创建，侧边栏顺序 |
| **测试工程师** | 全部 | 质量门禁验证，示例测试策略 | PRD §7.1.1-7.1.3 质量门禁 |
| **安全架构师** | Ch3, Ch6 | 权限模型 §3.2 完整性，STRIDE 映射 | Ch3 规格§补充（增强安全模型） |
| **渗透测试员** | Ch6 | MCP 服务器沙箱，输入验证，威胁模型 | Ch6 规格§补充（MCP 安全章节） |

---

## 第四节：概念追溯矩阵

| 概念 | 主要源材料位置 | 书籍章节 | 需包含的要点 |
|---------|------------------------|-----------------|----------------------|
| Reader Persona | PRD §5.2, team role review | Ch0 | 6 种读者画像，阅读路径推荐 |
| Architecture Decision | PRD §附录A | Ch7 | 用于案例可追溯性的 ADR 模板 |
| Agent (Build/Plan) | 01 §Agent + 02 §AgentRegistry | Ch2 Art.2.1, Ch6 Art.6.2 | OS类比, Primary/Subagent/Hidden, Plan安全网 |
| Agent (OMO 11+) | 02 §OMO Agent体系 | Ch3 Art.3.3 | Sisyphus/Prometheus/Atlas/Hephaestus/Oracle |
| Skill (SKILL.md) | 01 §Skill格式 + 05 §A SKILL开发 | Ch2 Art.2.2, Ch5 Art.5.1-5.3 | frontmatter, allowed-tools, 渐进式披露 |
| Scoped Skills | 02 §作用域技能(v4.3) | Ch5 Art.5.1 | target_agent, 可见性控制 |
| Command | 01 §Command + 03 §1 C+A | Ch2 Art.2.3, Ch4 Art.4.3 | 内置/自定义, 模板语法, 团队命令库 |
| Plugin | 01 §Plugin + 06 §Env Guard | Ch6 Art.6.2 | Hook点, Pipeline模式, 工具优先级 |
| 上下文工程 (Context Engineering) | 马书第3-4篇 | Ch2 Art.2.4 | 压缩, 缓存, Token预算, 三层模型 |
| 约束系统 (Constraints System) | 马书第5篇 | Ch2 Art.2.5 | 权限模型, 架构护栏, Lint规则 |
| 验证护栏 (Validation Harness) | 马书第17章 | Ch2 Art.2.6 | 质量门禁, YOLO分类, 自动验证 |
| 工具生态对比 (Ecosystem) | HE实践 04 | Ch1 Art.1.4 | 6工具对比, 选型决策树 |
| 国产AI生态 (Chinese Ecosystem) | HE实践 04 §国产 | Ch1 Art.1.5, Ch3 Art.3.4 | Trae/CodeGeeX/通义灵码/文心快码 |
| Harness Engineering理论框架 | HE实践 01 | Ch1 Art.1.3 | 5大分类法, 演进时间线 |
| Agent派生 (Agent Derivation) | 马书第20章 | Ch4 Art.4.4 | 子Agent, 委派, 协调者 |
| Teams多进程协作 (Teams) | 马书第20b章 | Ch4 Art.4.5 | 消息传递, 进程内集群 |
| MCP桥接 (Skill-MCP Bridge) | 马书第22章 | Ch5 Art.5.4 | Skill作为桥接层, 外部工具包装 |
| Skill插件化 (Plugin Patterns) | 马书第22b章 | Ch5 Art.5.5 | 组合Skill, Skills Marketplace |
| 上下文压缩 (Compaction) | 马书第9-11章 | Ch6 Art.6.4 | 自动压缩, 微压缩, 压缩后恢复 |
| Token预算 (Token Budget) | 马书第12章 | Ch6 Art.6.5 | 预算分配, 估算规则, 超限处理 |
| 提示词缓存 (Prompt Caching) | 马书第13-15章 | Ch6 Art.6.6 | 三级缓存, 缓存断点, 7+优化模式 |
| 记忆系统 (Memory System) | 马书第24章 | Ch6 Art.6.7 | Memdir架构, Auto-Dream, Compaction |
| 安全模型 (Security Model) | 马书第16-17b章 | Ch6 Art.6.8 | 6权限模式, YOLO分类器, 注入防御 |
| 沙箱隔离 (Sandbox) | 马书第18-18b章 | Ch6 Art.6.9 | Seatbelt/Bubblewrap, 53+Hook |
| CLAUDE.md指令层 | 马书第19章 | Ch6 Art.6.10 | 用户指令覆盖, @include系统 |
| 可观测性 (Observability) | 马书第29章 | Ch6 Art.6.11 | logEvent, 5层遥测, 生产监控 |
| Feature Flags路线图 | 马书第23章 | Ch6 Art.6.12 | 89 Flags, 产品演进 |
| Team Mode | 02 §Team Mode + 03 §4 T+S | Ch4 Art.4.3 | 12 tools, 成员类型, 内置Skills |
| MCP | 01 §MCP + 02 §MCP集成 | Ch6 Art.6.1 | stdio/SSE/WebSocket, ToolRegistry统一 |
| Category Routing | 02 §类别路由 | Ch3 Art.3.3 | 工作流路由 + 模型路由 |
| Ultrawork | 02 §Ultrawork + 03 §9.6 | Ch4 Art.4.1 | 自动探索循环, Ralph Loop |
| Prometheus Mode | 02 §Prometheus | Ch3 Art.3.3 | 访谈式规划, /start-work |
| 7-Agent Pipeline | 03 §9.4 | Ch4 Art.4.2 | Planner→Debater→...→Commit |
| Hashline Editing | 02 §Hashline | Ch6 Art.6.3 | LINE#ID, 0%陈旧行 |
| AGENTS.md | 03 §9.7 + 04 §技巧二 | Ch2 Art.2.3 | 金字塔结构, 分层注入 |
| Profile | 04 §技巧一 | Ch2 Art.2.3 | dev/review/debug, $extends继承 |
| Permission Model | 02 §权限数据模型 + 03 §9.3 | Ch3 Art.3.2 | 4层安全架构, allow/deny/ask |
| Cost Management | 02 §成本架构 + 04 §技巧六 | Ch6 Art.6.3 | Token预算, 模型降级, Compaction |
| Hyperplan | 02 §hyperplan + 03 §4.4 | Ch4 Art.4.3 | 5批评者, 对抗式规划 |
| security-research | 02 §security-research + 03 §4.4 | Ch4 Art.4.3 | 5人安全团队, CVSS评分 |
| Hook点(53+) | 02 §OMO Hook点 | Ch6 Art.6.2 | onWorkflowStart → onWorkflowEnd |
| Env Guard Plugin | 04 §技巧七 | Ch6 Art.6.2 | 正则检测, mask/reject/audit |
| Skills Marketplace | 01 §Skills Marketplace(OMO) | Ch2 Art.2.2 | 社区共享, 版本管理, 一键安装 |
| Ralph Loop | 02 §Ralph Loop | Ch4 Art.4.1 | /ulw-loop, 自引用循环 |

---

## 第五节：版本追踪与新鲜度

### 源材料新鲜度

| 源材料 | Gitee 最后更新 | OpenCode 版本 | OMO 版本 | 书籍同步状态 |
|--------|----------------------|------------------|-------------|-----------------|
| 01-core-concepts | 2026-05 | v1.15.x | v4.5.x | ✅ 最新 |
| 02-architecture | 2026-05 | v1.15.x | v4.5.x | ⚠️ 需验证 v4.5.1 具体内容 |
| 03-workflows | 2026-05 | v1.15.x | v4.5.x | ✅ 最新 |
| 04-tricks | 2026-05 (标记 待验证) | v1.12-v1.15 | v1.3-v4.5 | ⚠️ 版本范围较广，需验证 |
| 05-cases | 2026-05 (标记 待验证) | v1.15.x | v4.5.x | ✅ 最新 |

### 需要更新的内容

| 内容 | 触发更新条件 | 优先级 | 更新操作 |
|---------|----------------|----------|---------------|
| Provider 配置、模型名称 | 新模型发布 | 高 | 每月检查新 Provider |
| OMO Team Mode 配置 | OMO 发布 | 高 | 跟踪 OMO 更新日志 |
| MCP 协议细节 | MCP 规范更新 | 中 | 定期检查 MCP RFC |
| 类别路由选项 | OMO 发布 | 中 | 跟踪类别列表 |
| Command 参考 | OpenCode 发布 | 低 | 添加新命令时更新 |
| 文中的版本号 | 任何发布 | 低 | 更新版本标签 |

### 更新流程
1. 当源材料在 Gitee 中更新时 → 检查此矩阵
2. 在"书籍位置"列中标记受影响的书籍章节
3. 更新书籍正文中的版本号
4. 添加变更日志条目

---

> 维护者注：此文档应在以下情况更新：
> - OpenCode 或 OMO 发布新版本
> - 源章节有重大更新
> - 新增或修改书籍文章
> - 团队角色评审产生新的内容缺口或读者画像
>
> 最后更新：2026-05-31 | 团队角色评审（8角色）后更新 — 新增 Ch0、ADR 模板、多角色评审覆盖矩阵和增强的安全模型规格
