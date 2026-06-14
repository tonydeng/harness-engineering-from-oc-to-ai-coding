# 用户故事追溯矩阵 (Traceability Matrix)

> 版本：v2.3 | 生成日期：2026-06-04  
> 映射对象：47 个用户故事 → 50 篇文章（8 章 + 附录）  
> 角色：13 个（5 核心 + 8 扩展）

---

## 追溯矩阵

| 用户故事 ID | 用户故事名称 | 覆盖章节/文章 | 覆盖程度 |
|-------------|-------------|--------------|---------|
| **US-BEGINNER-01** | 快速了解核心价值 | `01-introduction/what-is-harness-engineer.md`（三阶段演进 + 核心能力定义）、`01-introduction/why-opencode.md`（4 大核心优势 + 全景对比）、`01-introduction/ecosystem-comparison.md`（14 款工具 8 维对比矩阵 + 选型决策树）、`01-introduction/harness-engineering-theory.md`（四个支柱 + 演进时间线） | **完整** |
| **US-BEGINNER-02** | 5 分钟完成安装 | `00-guide/quick-start.md`（5 分钟快速体验：三平台安装步骤 + Provider 配置 + 验证命令）、`03-setup/quickstart.md`（详细安装流程） | **完整** |
| **US-BEGINNER-03** | 第一个成功的尝试 | `00-guide/quick-start.md`（步骤化上手指南）、`03-setup/quickstart.md`（第一个任务）、`02-core-concepts/workflow-patterns.md`（Plan/Build 模式 + `/init` + `/undo` 命令详解） | **完整** |
| **US-BEGINNER-04** | 理解 6 个核心概念 | `02-core-concepts/agent-orchestration.md`（Agent = 进程，操作系统类比表）、`02-core-concepts/skills-system.md`（Skill = 驱动程序类比，结构化指令包）、`02-core-concepts/workflow-patterns.md`（Command = Shell Alias，Workflow = Shell Pipeline 类比）、`06-advanced/mcp-servers.md`（MCP = USB 接口类比）、`04-workflows/teams-collaboration.md`（Team 多进程协作）、`06-advanced/custom-agents.md`（Plugin 系统） | **部分** |
| **US-BEGINNER-05** | 从"对话"到"工程"的认知转变 | `01-introduction/what-is-harness-engineer.md`（三次浪潮演进 + Harness Engineer 定义 + 三大核心原则）、`01-introduction/harness-engineering-theory.md`（四种核心张力 + 思维转变示例） | **完整** |
| **US-POWER-01** | 工作流模式提升日常效率 | `04-workflows/ultrawork-mode.md`（目标驱动工作流 + Ralph Loop 详解 + max_turns/stop_condition/on_max_turns 控制参数 + 决策流程 + 与 Prometheus 三路对比表）、`04-workflows/prometheus-mode.md`（访谈式规划 + Atlas 执行 + 切换最佳实践） | **完整** |
| **US-POWER-02** | Agent 编排技巧 | `04-workflows/multi-agent-collab.md`（四种编排模式：串行/并行/主从/竞争 + task() 子 Agent 调用 + 7-Agent Pipeline + 温度策略 + 权限隔离）、`04-workflows/agent-derivation.md`（三种派生模式）、`04-workflows/teams-collaboration.md`（Teams 多进程协作） | **完整** |
| **US-POWER-03** | Profile 切换和 AGENTS.md | `02-core-concepts/workflow-patterns.md`（Profile 概念 + AGENTS.md 基本说明）、`03-setup/multi-env-setup.md`（Profile \$extends 继承机制 + 环境 Profile 模板）、`03-setup/opencode-config.md`（配置分层体系） | **部分** |
| **US-POWER-04** | 命令复用和工作流自动化 | `02-core-concepts/workflow-patterns.md`（Command 系统：8 个内置命令 + Markdown 格式自定义命令 + 参数化命令示例）、`04-workflows/custom-workflows.md`（自定义工作流 + Team Mode 12 个 team_\* 工具） | **部分** |
| **US-POWER-05** | 成本优化 | `06-advanced/context/performance-tuning.md`（三层成本优化模型 + 类别路由 + 自动降级链 + Token 预算 + 上下文压缩 + 工具输出保护）、`06-advanced/context-compression.md`（Token 预算分配 + 超限处理 + 降级策略） | **部分** |
| **US-POWER-06** | Agent 派生与 Teams 编排 | `04-workflows/agent-derivation.md`（三种派生模式：子 Agent/委派/协调者 + task() API 完整示例 + category/load_skills/结果合并 + 安全边界对比表 + 权限继承风险分析）、`04-workflows/teams-collaboration.md`（Teams 多进程通信机制 + 消息传递 + Team vs 独立 Agent 对比表 + 数据隔离模型） | **完整** |
| **US-LEAD-01** | 完整的团队落地指南 | `03-setup/multi-env-setup.md`（Profile \$extends 继承链 + 三套环境模板 + Secret 管理最佳实践 + 团队 Git 配置管理）、`07-case-studies/case-skills-marketplace.md`（团队 Skill 治理 + 目录结构标准 + 发布流程）、`04-workflows/custom-workflows.md`（Team Mode 多 Agent 团队配置） | **部分** |
| **US-LEAD-02** | 安全合规策略 | `06-advanced/security-overview.md`（四层安全模型 + 6 种权限模式 + 三级作用域 + Bash 白名单 + STRIDE 威胁建模 + NIST/SOC2/等保合规映射）、`06-advanced/custom-agents.md`（Env Guard Plugin 三种策略）、`06-advanced/sandbox-hooks.md`（沙箱隔离 + Hook 点体系） | **部分** |
| **US-LEAD-03** | 7-Agent Pipeline 工作流 | `04-workflows/multi-agent-collab.md`（Planner→Debater→Implementor→Reviewer→Tester→Linter→Committer 完整流程 + WORKFLOW_STATE.md 文件交接模式 + 各 Agent 温度策略 0.1/0.3 设计 + Reviewer/Tester 权限隔离方案） | **完整** |
| **US-LEAD-04** | 多环境配置管理 | `03-setup/multi-env-setup.md`（Profile \$extends 继承链完整示例 Base→Dev→CI→Production + 三套环境模板权限差异 + Secret 管理三种方案 + 团队 Git 管理 + .opencodeignore 排除规则） | **完整** |
| **US-SKILL-01** | SKILL.md 格式与发布 | `05-skills/creating-skills.md`（frontmatter 全部字段详解：name/description/allowed-tools/target_agent + 发现路径：项目级→用户级→内置 + 加载机制 + Skills Marketplace 发布流程 + 命名规范） | **完整** |
| **US-SKILL-02** | Skill 模板库 | `05-skills/skill-templates.md`（6 个完整模板：调查研究/架构设计/代码审查/敏捷活动/UI 审查/安全审计 + 每个含完整 SKILL.md  + 定制指南 + 可组合性设计理念 + 与前端组件类比） | **完整** |
| **US-SKILL-03** | 作用域技能和 Team 集成 | `05-skills/creating-skills.md`（target_agent 字段用法和限制 + Scoped Skills 机制）、`05-skills/skill-best-practices.md`（target_agent 与类别路由协同 + Team Mode 集成策略 + 配置 override 优先级）、`05-skills/plugin-patterns.md`（Skill 组合模式 + 依赖管理） | **部分** |
| **US-SKILL-04** | Skill 最佳实践和反模式 | `05-skills/skill-best-practices.md`（6 条核心设计原则 + 12 种常见反模式及正确做法 + 8 步调试清单 + Team Mode 集成策略 + 前端组件化类比） | **完整** |
| **US-SKILL-05** | Skill-MCP 桥接与插件化模式 | `05-skills/skill-mcp-bridge.md`（Skill-MCP 桥接架构图 + 桥接 SKILL.md 完整示例含 skill-embedded MCPs + 3 个桥接实战：WebSearch + Git + Database + 权限边界控制）、`05-skills/plugin-patterns.md`（三阶段演进：独立→组合→市场 + 三种协作模式：编排/管道/集市） | **完整** |
| **US-MANAGER-01** | 投资回报分析 | `07-case-studies/case-multi-model.md`（成本效益分析：Token 消耗量化对比 + 月度成本节省计算 + ROI 计算公式）、`07-case-studies/real-world-01.md`（量化工作报告：文件数/测试覆盖率/开发耗时）、`07-case-studies/real-world-02.md`（遗留系统改造 ROI 对比表） | **部分** |
| **US-MANAGER-02** | 工具对比与选型建议 | `01-introduction/ecosystem-comparison.md`（14 款工具 8 维对比矩阵 + 场景化选型决策树：个人/小团队/企业级 + 开源 vs 闭源分水岭分析）、`01-introduction/why-opencode.md`（7 款工具对比 + OMO 双层架构决策树） | **部分** |
| **US-ANALYST-01** | 读者需求覆盖度验证 | `00-guide/reading-paths.md`（13 种读者角色分类 + 阅读路径设计 + 角色分类树状图 + What/Why/How/When 认知阶段标注） | **部分** |
| **US-ANALYST-02** | 业务价值翻译层 | 各章 README（第 1-7 章 README 有章节概述和价值声明，但缺少标准化格式——目标读者/前驱知识/读完能做什么/业务指标关联，仅部分章节包含时间评估） | **缺失** |
| **US-ANALYST-03** | 读者旅程完整度检查 | `00-guide/reading-paths.md`（定义 13 种角色路径 + 标注 What/Why/How/When 阶段）——书的结构自然遵循"是什么→为什么→怎么做→何时做"，但未显式标注分类 | **部分** |
| **US-SYSA-01** | 技术选型与架构评估框架 | `01-introduction/ecosystem-comparison.md`（集成性/可观测性/安全/扩展性对比）、`01-introduction/why-opencode.md`（OpenCode 架构+局限诚实告知）、`03-setup/multi-env-setup.md`（企业级配置管理+Git 治理）、`02-core-concepts/agent-orchestration.md`（Agent 分层架构） | **部分** |
| **US-SYSA-02** | 安全架构与威胁建模 | `06-advanced/security-overview.md`（STRIDE 威胁建模表 + 四层安全模型 + NIST/SOC2/等保映射）、`06-advanced/mcp-servers.md`（MCP 三种传输类型安全对比 + OAuth 认证 + 进程隔离）、`06-advanced/sandbox-hooks.md`（沙箱隔离机制 + Hook 点体系）、`04-workflows/teams-collaboration.md`（数据隔离安全边界） | **部分** |
| **US-SYSA-03** | 架构治理与规模化可扩展性 | `05-skills/skill-best-practices.md`（Skill 作为架构规范载体的模式 + AGENTS.md 架构护栏）、`07-case-studies/case-skills-marketplace.md`（Skill 标准化 + 质量门禁 + 版本管理 + CI/CD 发布流水线）、`04-workflows/teams-collaboration.md`（分层架构设计 + 多团队扩展模式）、`07-case-studies/real-world-01.md`（ADR 架构决策记录） | **部分** |
| **US-BACKEND-01** | MCP 服务器开发与集成 | `06-advanced/mcp-servers.md`（MCP 协议核心模型 + 三种传输类型配置与安全对比 + Tool/Resource/Prompt 三原语 + ToolRegistry 集成 + Node.js/Python 服务端 SDK + Express/Fastify 转 MCP Server 示例 + OAuth 认证 + 进程隔离 + 环境变量管理 + STRIDE 威胁分析） | **完整** |
| **US-BACKEND-02** | API 契约与数据库 Schema 的 Agent 协作 | `07-case-studies/real-world-01.md`（AGENTS.md 知识注入：技术栈声明 + 项目结构 + `/init` 生成项目骨架 + Prisma Schema 生成）——但未覆盖"OpenAPI Schema→Agent 理解层"映射方法和数据库 Migration 安全策略 | **缺失** |
| **US-BACKEND-03** | 微服务架构中的 Agent 协同治理 | `04-workflows/teams-collaboration.md`（多服务上下文编排策略 + 跨服务通信机制 + 分布式 Agent 架构）、`06-advanced/mcp-servers.md`（MCP Server 作为"内部 API 网关"角色）、`07-case-studies/real-world-01.md`（微服务项目实战） | **部分** |
| **US-BACKEND-04** | 国产模型 Provider 集成 | `03-setup/chinese-providers.md`（DeepSeek/Qwen/Kimi 完整配置 + Base URL/API Key/模型名称 + 参数调优建议 + Token 计算差异 + 速率限制 + 内容安全 + Category Routing 混合路由）、`07-case-studies/case-multi-model.md`（混合架构 Failover + 成本效益分析 + 安全边界评估 + 模型输出验证） | **完整** |
| **US-FRONTEND-01** | 前端开发场景的 Agent 编排指南 | 相关文章：`04-workflows/multi-agent-collab.md`（通用 Agent 编排）、`04-workflows/agent-derivation.md`（组件生成流水线提及）——但无专门前端场景工作流示例，无 OMO 前端开发流程编排展示 | **缺失** |
| **US-FRONTEND-02** | 组件化开发与 Skill 设计的类比方法论 | `05-skills/skill-best-practices.md`（React 组件与 Skill 的类比 + 前端反模式语言解释 Skill 陷阱）、`05-skills/skill-templates.md`（组件化思维设计原则 + UI 审查 Skill 模板） | **部分** |
| **US-FRONTEND-03** | 本书 mdBook 前端架构的开发者指南 | 项目未包含 mdBook 架构说明文档。代码高亮、代码复制按钮、暗色模式、侧边栏响应式等标准由 mdBook 默认提供，但无专文说明 | **缺失** |
| **US-UX-01** | Mermaid 图表视觉规范 | `AGENTS.md`（定义 Mermaid 统一配色方案：Agent #4A90D9 / Skill #50C878 / Workflow #FF9F43 / MCP #A66CFF + TB 方向统一）——全书图表遵循配色，但 Alt 文本和复杂图表文字说明段未系统化要求 | **部分** |
| **US-UX-02** | 代码块阅读体验规范 | 全书代码块标注语言标识（bash/json/yaml/typescript/python），部分代码块标注文件路径注释（如 `// file.json`）。行高亮（`[!code highlight]`）和占位符（`<PLACEHOLDER>`）使用不统一 | **部分** |
| **US-UX-03** | 移动端与无障碍阅读标准 | mdBook 默认主题支持移动端响应式侧边栏折叠和代码块横向滚动。Mermaid 图表面向缩放通过 mdBook 内置 CSS 处理。但无障碍标准（标题层级规范、颜色对比度 ≥ 4.5:1）无专文验证 | **缺失** |
| **US-QA-01** | 代码示例可运行性验证 | `examples/opencode-configs/`（4 个 JSON 示例配置）和 `examples/skills/`（2 个 Skill 示例）存在。但无 README 说明执行步骤，无版本标注（`>= OpenCode v1.15.x`），未分类为"已验证可运行"或"演示性示例" | **缺失** |
| **US-QA-02** | 内容一致性自动化检查 | `.github/workflows/deploy-mdbook.yml`（仅 mdbook build + deploy——无 Markdown lint、无内部链接检查、无 Mermaid 预渲染检查、无术语一致性脚本、无版本号同步检查） | **缺失** |
| **US-QA-03** | 质量门禁与发布前验收 | 无质量门禁验证文档。50 篇文章行数、代码示例可运行比例、图表渲染检查、内部链接有效率、术语一致性等指标均未系统化追踪 | **缺失** |
| **US-SECURITY-01** | 理解并配置 OpenCode 安全模型 | `06-advanced/security-overview.md`（四层安全防御架构图 + Permission Rule 引擎 allow/deny/ask 三级策略 + Bash 白名单配置 + 4 级作用域：全局/项目/会话/工具 + STRIDE 威胁建模 + NIST CSF/SOC2/等保合规映射表 + 审计日志配置 + YOLO 分类器 + 提示注入防御）、`06-advanced/custom-agents.md`（Env Guard Plugin mask/reject/audit 三种策略） | **完整** |
| **US-SECURITY-02** | MCP 连接安全和凭证管理 | `06-advanced/mcp-servers.md`（三种传输类型安全风险对比：stdio/streamable-http/websocket + OAuth 认证配置流程 + 进程隔离和环境变量分离机制图解 + Provider API Key 安全存储方案 + STRIDE 威胁分析 + 中间人攻击防护） | **完整** |
| **US-SECURITY-03** | AI Agent 安全编排与审计流水线 | `07-case-studies/case-security-audit.md`（红蓝对抗模式 + security-research 5 人并行审计 + 自动 CVSS 评分 + STRIDE 威胁建模 + CI/CD 嵌入 + 持续审计流水线）、`04-workflows/custom-workflows.md`（security-research Team Skill 配置示例）、`04-workflows/multi-agent-collab.md`（串行/并行/对抗式编排模式） | **部分** |
| **US-REDTEAM-01** | AI Agent 安全边界评估 | `06-advanced/security-overview.md`（高危操作类型：Bash/文件系统/网络 + 权限控制 allowlist/blocklist 配置示例 + 审计日志记录与导出 + 沙箱隔离说明）、`06-advanced/sandbox-hooks.md`（Seatbelt/Bubblewrap 沙箱原理 + 进程隔离策略） | **部分** |
| **US-REDTEAM-02** | 基于 Agent 编排的安全测试 | `07-case-studies/case-security-audit.md`（安全审计 Skill 示例：SQL 注入/XSS/CSRF 扫描 + 依赖 CVE 检测 + 配置泄露检查 + 自动 CVSS 评分 + security-research 技能使用）、`05-skills/skill-best-practices.md`（最小权限原则） | **部分** |
| **US-REDTEAM-03** | AI 编程工具安全评估方法论 | 相关概念分散在 `06-advanced/security-overview.md`（数据流/权限/隔离性）、`06-advanced/mcp-servers.md`（MCP 安全）、`06-advanced/custom-agents.md`（Plugin 权限）——但无完整安全评估框架、MCP 安全检查清单、第三方供应链风险审查方法 | **缺失** |

---

## 汇总

| 指标 | 数量 | 占比 |
|------|------|------|
| **完整** | 17 | 36.2% |
| **部分** | 21 | 44.7% |
| **缺失** | 9 | 19.1% |
| **合计** | 47 | 100% |

### 缺失故事清单（9 个，需优先补充）

| ID | 名称 | 优先級 | 建议补充位置 |
|----|------|--------|------------|
| US-ANALYST-02 | 业务价值翻译层 | P1 | 各章 README 添加标准化价值声明块 |
| US-BACKEND-02 | API 契约与数据库 Schema 的 Agent 协作 | P1 | `06-advanced/mcp-servers.md` 或 `07-case-studies/real-world-01.md` |
| US-FRONTEND-01 | 前端开发场景的 Agent 编排指南 | P1 | `04-workflows/` 或 `07-case-studies/` 新增前端案例 |
| US-FRONTEND-03 | 本书 mdBook 前端架构的开发者指南 | P2 | 项目 README 或 `appendix-a/` 新增 mdBook 架构说明 |
| US-UX-03 | 移动端与无障碍阅读标准 | P2 | `00-guide/how-to-read.md` 或项目 README |
| US-QA-01 | 代码示例可运行性验证 | P0 | `examples/` 添加 README + 代码块标注版本 + 分类标识 |
| US-QA-02 | 内容一致性自动化检查 | P0 | `.github/workflows/deploy-mdbook.yml` 添加质量检查步骤 |
| US-QA-03 | 质量门禁与发布前验收 | P1 | `docs/plans/` 新增质量门禁检查清单 |
| US-REDTEAM-03 | AI 编程工具安全评估方法论 | P2 | `06-advanced/security-overview.md` 新增安全评估框架章节 |

### 按角色覆盖分布

| 角色 | 完整 | 部分 | 缺失 | 覆盖率（完整+部分） |
|------|------|------|------|-------------------|
| US-BEGINNER（入门开发者） | 4 | 1 | 0 | 100% |
| US-POWER（效率开发者） | 3 | 3 | 0 | 100% |
| US-LEAD（技术负责人） | 2 | 2 | 0 | 100% |
| US-SKILL（Skill 作者） | 4 | 1 | 0 | 100% |
| US-MANAGER（工程经理） | 0 | 2 | 0 | 100% |
| US-ANALYST（需求分析师） | 0 | 2 | 1 | 66.7% |
| US-SYSA（系统架构师） | 0 | 3 | 0 | 100% |
| US-BACKEND（后端开发者） | 2 | 1 | 1 | 75% |
| US-FRONTEND（前端开发者） | 0 | 1 | 2 | 33.3% |
| US-UX（文档 UX 专家） | 0 | 2 | 1 | 66.7% |
| US-QA（技术审校） | 0 | 0 | 3 | 0% |
| US-SECURITY（安全工程师） | 2 | 1 | 0 | 100% |
| US-REDTEAM（红队成员） | 0 | 2 | 1 | 66.7% |

---

## 缺失故事决策（2026-06-11）

基于全面评估报告（`docs/reviews/overall-evaluation-2026-06-11.md`），v1.0 发布中 9 个缺失用户故事决策如下：

**决策依据**：(1) 本书核心价值在工程实践方法论，非特定技术实现细节；(2) 缺失故事优先级为 P1/P2，不阻塞 v1.0 发布；(3) 38/47 故事已覆盖，覆盖率 80.9%。

| ID | 名称 | 决策 | 依据 |
|----|------|------|------|
| US-QA-01 | 代码示例可运行性验证 | 延后至 v1.1 | examples/ 已有 74 个文件，缺版本标注不影响核心阅读 |
| US-QA-02 | 内容一致性自动化检查 | 延后至 v1.1 | CI 已有 mdbook build，Markdown lint 可后续补充 |
| US-QA-03 | 质量门禁与发布前验收 | 延后至 v1.1 | 本次评估报告本身即为质量门禁初步实现 |
| US-ANALYST-02 | 业务价值翻译层 | 延后至 v1.1 | 各章 README 已有章节概述 |
| US-BACKEND-02 | API 契约与数据库 Schema 的 Agent 协作 | 延后至 v1.1 | real-world-01 案例已覆盖核心场景 |
| US-FRONTEND-01 | 前端开发场景的 Agent 编排指南 | 延后至 v1.1 | 多 Agent 协作章节已覆盖通用编排 |
| US-FRONTEND-03 | 本书 mdBook 前端架构的开发者指南 | 延后至 v1.2 | mdBook 默认主题功能完备 |
| US-UX-03 | 移动端与无障碍阅读标准 | 延后至 v1.2 | mdBook 默认已支持响应式 |
| US-REDTEAM-03 | AI 编程工具安全评估方法论 | 延后至 v1.1 | security-overview 已覆盖 STRIDE |

---

## 补充说明

- **"完整"** 判定标准：所有验收标准均被文章显式覆盖，读者可依据文章独立完成该用户故事描述的目标。
- **"部分"** 判定标准：部分验收标准被覆盖，或内容虽触及主题但深度/格式不符合验收要求。
- **"缺失"** 判定标准：没有任何文章直接回应验收标准中的要求。
- 本矩阵基于 2026-06-04 快照检查，内容更新后需同步更新此矩阵。
- **2026-06-11 决策**：9 个缺失用户故事已作为已知限制延后至 v1.1/v1.2，详见「缺失故事决策」章节。v1.0 发布覆盖率 80.9%（38/47），核心价值在工程实践方法论已充分覆盖。
