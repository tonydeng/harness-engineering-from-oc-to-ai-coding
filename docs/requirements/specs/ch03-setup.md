# Ch3: 环境搭建

## 概述

本章是所有读者必须动手操作的一章。从零开始搭建OpenCode开发环境，覆盖安装、配置、Provider设置、安全初始化全流程。本章还深入解析opencode.json配置文件的完整结构，以及如何集成oh-my-openagent搭建完整的多Agent工作环境。目标是让读者在读完本章后拥有一个可正常工作的OpenCode开发环境。

**章节核心主题**：从"能用"到"好用"——搭建可工程化的AI编程环境。

> **章节规模**：5 篇文章（3 现有 + 2 新增），2 篇修改

## 文章

### Article 3.1: 快速上手
- **阅读时间**：15 min
- **学习目标**：
  - 能够在Mac/Windows/Linux上安装OpenCode
  - 能够配置至少一种Provider（Zen / API Key / GitHub Copilot）
  - 能够完成第一次有意义的操作（项目分析、小改动）
  - 理解/init和AGENTS.md的作用
- **前置知识**：Ch1-Ch2概念理解
- **源材料映射**：OpenCode实战 01（附录A安装指南、附录B Provider配置、快速上手部分）+ OpenCode实战 04（附录快速上手指南）

#### 大纲
1. 安装（3种平台）
   - 官方安装脚本（推荐）、npm全局安装、Homebrew
   - 验证安装：`opencode --version`
   - 常见安装问题排障
2. Provider配置
   - 方式一：OpenCode Zen（最省心，推荐入门用户）
   - 方式二：自有API Key（Anthropic / OpenAI / Google Gemini）
   - 方式三：GitHub Copilot登录
3. 第一个Session
   - 启动OpenCode
   - /init初始化项目（生成AGENTS.md）
   - Plan模式问3个关于项目的问题
   - Build模式做第1个小改动
   - /undo撤销操作
4. 常用命令速查
   - /help, /connect, /init, /undo, /redo, /diff, /share, /models, /plan
5. 安全检查
   - 理解edit/bash权限控制
   - 建议新用户先设`edit: "ask"`, `bash: "ask"`
   - 配置.opencodeignore排除敏感目录

#### 核心概念
- **AGENTS.md是项目的"出生证明"**：第一次/init建立项目知识库，告诉Agent项目是什么、用什么技术、怎么运行。
- **Provider自由度意味着什么**：不锁定任何模型提供商，可以根据场景/成本灵活切换。
- **安全先行**：Harness Engineering的第一条原则是可控，权限控制是最基础的可控手段。

#### 代码/配置示例
- 3种平台的安装命令
- 3种Provider配置命令
- 完整的第一Session操作序列
- 基础权限配置（edit/bash设为ask）

#### Mermaid 图表
- 安装流程图（根据平台分支）

#### 关联章节
- → Article 3.2（基本安装后需要深入配置）
- ← Ch1-Ch2（前置概念理解）

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 包含3种平台的安装说明
- [ ] 包含至少2种Provider配置方式
- [ ] 包含完整的第一操作序列
- [ ] 所有命令可执行

---

### Article 3.2: OpenCode 配置深度解析
- **阅读时间**：25 min
- **学习目标**：
  - 理解opencode.json的完整结构
  - 掌握配置分层机制：全局→项目→环境变量→CLI flag
  - 理解类别路由（Category Routing）系统的工作原理
  - 掌握多层安全模型配置
- **前置知识**：Article 3.1
- **源材料映射**：OpenCode实战 02（三层架构-关键配置路径汇总、配置合并逻辑）+ OpenCode实战 03（Config + Agent + Skill三层配置覆盖）

#### 大纲
1. opencode.json完整结构
   - 配置范围：全局 ~/.config/opencode/config.json | 项目 .opencode/config.json | 托管配置 | 环境变量 | CLI flag
   - 合并逻辑：mergeDeep + 优先级覆盖
2. 关键配置段详解
   - agents：自定义Agent定义
   - commands：命令注册
   - skills：Skill权限和来源
   - plugins：插件配置
   - mcpServers：外部MCP服务
   - permissions：权限规则
   - profiles：工作状态切换
   - defaults：运行时默认值
3. 类别路由系统
   - 按任务复杂度/领域自动分派
   - 路由类别：quick / plan / research / review / deploy / document / security
   - 模型路由：visual-engineering / ultrabrain / artistry / deep / quick / writing
   - 自定义类别配置
4. 安全模型
   - 4层安全架构：权限分层→技能隔离→沙箱隔离→注入防御
   - Permission Rule引擎：allow/deny/ask + glob匹配 + 优先级
   - 敏感文件保护（默认deny .env, node_modules）
   - Bash白名单配置
5. 成本管控
   - Token预算与会话级上限
   - 模型降级链（Category-based Auto-downgrade）
   - 上下文压缩（Compaction）

#### 核心概念
- **配置即代码（Configuration as Code）**：opencode.json不仅是配置文件，更是一个声明式的工程流水线定义文件。团队可以把它纳入版本控制，实现配置可审计、可复现。
- **4层覆盖的设计哲学**：全局（个人偏好）→ 项目（团队标准）→ 环境变量（部署环境）→ CLI（临时覆盖），每层有不同职责。
- **权限规则的代价**：规则越细越安全，但越容易出错（漏写规则导致意外deny或allow）。需要平衡。

#### 代码/配置示例
- 完整的opencode.json示例（带注解）
- 类别路由配置示例
- 权限规则示例（glob匹配 + allow/deny/ask）
- 成本管控配置（Token预算 + 模型降级）

#### Mermaid 图表
- 配置合并流程图（4层优先级）
- 4层安全防御架构图
- 类别路由映射图

#### 关联章节
- ← Article 3.1（基础配置的深化）
- → Ch4（工作流模式依赖于正确的类别路由配置）
- → Article 6.3（性能调优依赖于成本管控配置）

### 团队角色评审补充
- **安全架构师需求（P0）**：Article 3.1 安全检查段增加edit/bash设为ask的完整配置示例；Article 3.2 安全模型段从配置说明升级为威胁建模分析（附STRIDE表），增加.opencodeignore的完整配置和Opencode默认拒绝的敏感文件路径列表，增加安全配置与NIST CSF/SOC2/等保2.0的映射说明。
- **架构顾问需求（P0）**：Article 3.2 增加企业级配置管理（Git管理的配置治理、环境隔离、密钥管理）；增加"企业集成架构"小节（CI/CD + Secret Store + 监控 + Issue Tracking）。
- **后端架构师需求**：Article 3.1 Provider配置段增加企业级管理（Kubernetes Secret管理、团队级Provider配置、多Provider故障切换）。
- **UI设计师需求**：Ch3 三篇Mermaid图需使用统一配色方案，所有图有Alt文本。

---

### Article 3.3: oh-my-openagent 集成
- **阅读时间**：20 min
- **学习目标**：
  - 理解OMO是什么、和OpenCode的关系
  - 能够安装和验证OMO
  - 理解OMO的双层架构：Plugin + 独立Agent系统
  - 掌握基本的OMO配置（oh-my-openagent.jsonc）
- **前置知识**：Article 3.2（理解opencode.json基础配置）
- **源材料映射**：OpenCode实战 02（OMO专栏：10+ Agent、类别路由、Ultrawork、Team Mode、版本演进）+ OpenCode实战 01（OMO扩展视角部分）

#### 大纲
1. OMO概览
   - 什么是oh-my-openagent（社区编排框架插件，GitHub 60K+ Stars）
   - OMO vs 原生OpenCode：能力对比表
   - 什么时候需要OMO（决策树）
2. 安装
   - bunx oh-my-opencode install
   - 安装向导问答
   - 验证：bunx oh-my-opencode doctor
3. OMO架构
   - 核心Agent：Sisyphus/Prometheus/Atlas/Hephaestus/Oracle
   - Plugin系统：OMO作为OpenCode Plugin运行
   - 类别路由系统（OMO的工作流路由 + 模型路由）
4. OMO基本配置
   - oh-my-openagent.jsonc位置（全局/项目）
   - agents配置（每个Agent的模型和参数）
   - categories配置（类别路由的模型映射）
   - skills配置（来源/禁用/覆盖）
   - Ultrawork/Prometheus模式配置
5. OMO版本演进与兼容性
   - v4.0→v4.5核心变化速览
   - 常见陷阱和排查方法

#### 核心概念
- **OMO是Plugin，不是替代品**：OMO以Plugin形式叠加在OpenCode之上，扩展而非替换。两者的关系类似于"操作系统内核"和"Shell增强工具"。
- **类别路由的双层设计**：OpenCode有基本的Agent路由（Build/Plan/@subagent），OMO在其上叠加工作流路由和模型路由。
- **13+ Agent的设计意图**：每个Agent对应一种工作模式（战略规划/任务执行/代码审计），人不需要切换context，Agents自行适应。

#### 代码/配置示例
- OMO安装命令
- oh-my-openagent.jsonc完整配置示例（带注解）
- Ultrawork模式配置示例
- Prometheus模式配置示例

#### Mermaid 图表
- OMO整体架构图（Sisyphus → Prometheus/Atlas/Hephaestus/Oracle）
- OMO vs 原生OpenCode对比图
- 类别路由双层面板图

#### 关联章节
- ← Article 3.2（需要在opencode.json配置OMO）(sic)
- → Ch4（OMO的工作流模式在Ch4中深入展开）
- → Article 6.1（OMO与MCP的集成）
- → Article 6.2（自定义Agent依赖OMO的扩展能力）

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 包含OMO安装和验证的完整步骤
- [ ] 包含OMO vs 原生OpenCode的对比表
- [ ] 包含完整的oh-my-openagent.jsonc配置示例
- [ ] 所有命令可执行

---

## 章节重构增补

### 修改标注（基于章节重构计划）

**Article 3.2（Opencode 配置详解）**：
- 增加 Category 路由配置详解
- 增加 OMO v4.5+ 新配置项（如自定义 Hook 配置）

**Article 3.3（oh-my-openagent 集成）**：
- 增加 OMO 11+ Agent 注册表引用
- 补充 Agent 类型与任务匹配的映射表

---

### Article 3.4: 国产模型配置
- **阅读时间**：15 min
- **学习目标**：
  - 掌握 DeepSeek/Kimi/Qwen 等国产模型的 API 配置方法
  - 理解国产模型与 OpenCode 的 Provider 集成方式
  - 了解国产模型的典型参数和注意事项
- **前置知识**：Article 3.1（OpenCode Provider 配置基础）
- **源材料映射**：HE实践 04，HE实践 README §国产环境

#### 大纲
1. 国产 AI 模型概览
   - DeepSeek（深度求索）：性价比之王
   - Kimi（月之暗面）：长上下文优势
   - Qwen（阿里通义千问）：生态完整
   - 其他国产 Provider
2. 配置方法
   - DeepSeek API 配置（Base URL + API Key）
   - Kimi API 配置
   - Qwen API 配置
3. 典型参数调优
   - 温度、top_p、max_tokens 的推荐值
   - 不同任务的最佳参数组合
4. 注意事项和常见问题
   - 国产模型的 Token 计算差异
   - 内容安全过滤对输出的影响
   - API 可用性和速率限制

#### 核心概念
- **Provider 无关性的工程价值**：OpenCode 的 Provider 抽象层让国产模型和国际模型无缝切换
- **国产模型的成本优势**：DeepSeek 等国产模型的 API 价格通常为 GPT-4 的 1/10 到 1/20

#### 代码/配置示例
- DeepSeek Provider 完整配置
- Qwen Provider 完整配置
- 国产模型与 GPT 的混合路由配置

#### Mermaid 图表
- 国产 Provider 配置流程图
- 国产模型与国际模型成本对比图

#### 关联章节
- ← Article 3.1（Provider 配置基础）
- → Ch6 §6.3（成本优化中使用国产模型降级）
- ↔ Article 1.5（国产 AI 生态的概念部分）

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 覆盖至少 3 个国产 Provider 的配置
- [ ] 包含典型参数调优说明
- [ ] 所有配置命令可运行

---

### Article 3.5: 多环境部署方案
- **阅读时间**：15 min
- **学习目标**：
  - 掌握本地 dev / CI / 生产三套环境的配置管理
  - 理解 Profile 切换在多环境中的最佳实践
  - 能够设计团队级的多环境部署方案
- **前置知识**：Article 3.2（opencode.json 配置基础）
- **源材料映射**：OpenCode实战 04 §Profile

#### 大纲
1. 多环境部署的挑战
   - 不同环境需要不同的模型、权限、Token 预算
   - 配置泄漏风险（生产环境的 API Key 保护）
2. Profile 切换的高级用法
   - $extends 继承机制实现 Base → Dev → CI → Production
   - 环境变量注入区分环境
   - CLI flag 临时覆盖
3. 三套环境模板
   - 本地开发（高权限、低成本模型）
   - CI/CD（低权限、快速模型）
   - 生产环境（严格权限、高 Token 预算）
4. 团队级配置管理
   - Git 管理的 opencode.json
   - Secret Store 集成
   - 多环境测试策略

#### 核心概念
- **Profile 继承的设计模式**：Base Profile 定义公共配置，各环境 Profile 通过 $extends 继承+覆盖
- **环境隔离是安全的基础**：不同环境使用不同的 API Key、不同的权限配置

#### 代码/配置示例
- 多环境 Profile 配置示例（Base → Dev → CI → Production）
- environment.json 环境变量配置
- .opencodeignore 环境相关排除规则

#### Mermaid 图表
- Profile 继承关系图
- 多环境部署架构图

#### 关联章节
- ← Article 3.2（Profile 配置基础）
- → Ch6 §6.3（环境相关的成本管控配置）
- → Ch4（不同环境使用不同的工作流模式）

#### 验证标准
- [ ] 文章 ≥ 200 行有效内容
- [ ] 包含至少 3 套环境的 Profile 配置示例
- [ ] 包含 $extends 继承机制的完整示例
- [ ] 包含 Secret 管理的最佳实践

---

## 团队协作工作流

### 团队分工

| 角色 | 职责 | 负责文章 |
|------|------|---------|
| **后端架构师**（BACKEND） | Provider 配置深入、国产模型 API 配置验证、多环境 Profile 配置示例、Secret 管理 | Article 3.2, Article 3.4, Article 3.5 |
| **安全架构师**（SECURITY） | 4 层安全模型配置、威胁建模（STRIDE）、合规映射（NIST/SOC2/等保）、.opencodeignore 配置 | Article 3.2(安全节), Article 3.1(安全检查) |
| **架构顾问**（SYSA） | 企业级配置管理、CI/CD+Secret Store+监控集成架构、类别路由详解 | Article 3.2(企业集成), Article 3.3 |
| **前端架构师**（FRONTEND） | OMO Agent 注册表引用、Agent 类型与任务映射表 | Article 3.3 |
| **UI设计师**（UX） | 三篇 Mermaid 图配色方案统一、环境拓扑图可视化 | Article 3.5 (拓扑图) |

### 流程规范（Superpowers 工作流映射）

| 阶段 | 本阶段活动 | 交付物 | 负责人 |
|------|-----------|--------|--------|
| **头脑风暴** | 收集安装/配置常见问题、识别安全配置缺口、确定国产模型覆盖范围 | 配置痛点清单、安全增强需求 | 后端架构师 + 安全架构师 |
| **计划** | 排序写作依赖（3.1→3.2→3.3→3.4→3.5）、确定安全配置示例范围、分配多环境模板 | 写作计划、安全配置清单 | 敏捷教练 |
| **实施** | 5 篇文章写作，重点 ensure 所有配置示例可运行，安装命令可执行 | 5 篇文章初稿 | 各角色按分工 |
| **评审** | 配置示例可运行性验证（重点）、安全配置完整性审查、Profile 继承链测试 | 评审报告、配置测试记录 | 测试工程师 + 安全架构师 |
| **验证** | `npx docsify serve` 无报错、所有配置命令在测试环境可执行、Mermaid 渲染 | 验证报告 | 测试工程师 |
| **交付** | 合并、更新示例配置文件到 `examples/` 目录、确认与 OpenCode v1.15.x 兼容 | 合入确认、示例更新 | 敏捷教练 |

### 评审要求

**检查点 1：配置示例可运行性（最重要的检查点）**
- Article 3.1 安装命令在 Mac/Windows/Linux 三种平台验证
- Article 3.2 的 `opencode.json` 完整示例格式正确（可通过 JSON 验证器）
- Article 3.4 国产 Provider 配置示例使用真实 API 端点格式
- Article 3.5 Profile 继承示例的 `$extends` 链无循环引用

**检查点 2：安全配置完整性**
- Article 3.1 安全检查段包含 `edit: "ask"`, `bash: "ask"` 完整示例
- Article 3.2 安全模型段包含 STRIDE 威胁建模表
- Article 3.2 包含合规映射表（至少 NIST CSF/SOC2/等保 2.0 之一）
- `.opencodeignore` 默认拒绝路径列表完整（`.env`, `node_modules`, `secrets/` 等）

**检查点 3：文章间依赖一致性**
- Article 3.2（配置）→ Article 3.3（OMO 集成）→ Article 3.4（国产模型）的配置依赖链正确
- Article 3.5 Profile 配置与 Article 3.2 的 Profile 段定义一致

### 质量验收要求

| 门禁类型 | 验收项 | 通过标准 |
|---------|--------|---------|
| 🔴 硬性 | 每篇文章有效行数 | ≥ 200 行 |
| 🔴 硬性 | 配置示例格式正确率 | 100%（JSON/YAML 验证通过） |
| 🔴 硬性 | 安装命令可执行 | 至少 1 种平台验证通过 |
| 🔴 硬性 | 威胁建模覆盖 | Article 3.2 包含 STRIDE 表 |
| 🟡 质量 | 多平台覆盖 | 安装说明覆盖 3 种平台 |
| 🟡 质量 | 安全配置完整性 | 4 层安全防御架构图 + 配置示例 |
| 🟡 质量 | Secret 管理方案 | 至少包含 1 种方案（环境变量/Secret Store/Git-crypt） |
| 📊 量化 | Mermaid 图表 | ≥ 6 张（配置图+安全图+架构图+拓扑图+继承图+路由图） |
| 📊 量化 | 配置示例 | ≥ 8 个完整可运行的配置块 |

### 特殊内容技能映射

| 特殊内容 | 所需技能 | 适用文章 | 说明 |
|---------|---------|---------|------|
| 安装流程图 | `bpmn` | Article 3.1 | 按平台分支的流程图 |
| 配置合并流程图 | `uml` / `graphviz` | Article 3.2 | 4 层优先级覆盖 |
| 4 层安全防御架构图 | `security` / `architecture` | Article 3.2 | 权限→技能→沙箱→注入 |
| 类别路由映射图 | `architecture` | Article 3.2 | 任务到类别的路由 |
| OMO 整体架构图 | `architecture` | Article 3.3 | Sisyphus→Agents 层级 |
| OMO vs 原生对比图 | `infographic` | Article 3.3 | 能力对比 |
| 国产 Provider 配置流程图 | `bpmn` | Article 3.4 | 配置步骤 |
| 国产模型 vs 国际模型成本对比图 | `chart-visualization` | Article 3.4 | 柱状图/对比图 |
| Profile 继承关系图 | `uml` / `graphviz` | Article 3.5 | $extends 继承链 |
| 多环境部署架构图 | `architecture` | Article 3.5 | Dev/CI/Production 三环境拓扑 |
