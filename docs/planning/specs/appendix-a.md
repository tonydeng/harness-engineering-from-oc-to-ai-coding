# 附录规格说明（Appendices A-D）

## 1. 概述

全书包含 4 个附录，为读者提供不同层次的参考内容：术语与参考资料（A）、OpenCode 内置能力参考（B）、Claude Code 竞品对照参考（C）、Pi Agent 生态扩展参考（D）。

**章节规模**：4 个附录共 21 篇文章（2 + 7 + 7 + 5），不含各目录 README。

## 2. 附录 A — 术语 & 参考资料

### 2.1 概述

附录 A 收录全书的参考资料和辅助内容，为读者提供快速查阅的参考手册。

- **术语表** (glossary.md) — 全书核心术语的完整索引，按拼音字母排序，包含定义、人话解释、首次出现章节
- **参考资料** (references.md) — 全书引用资源汇总，含书籍、论文、工具文档、社区资源等

### 2.2 已完成

- 术语表涵盖 Agent、Skill、Workflow、MCP、Plugin 等 30+ 核心术语
- 参考资料按工具文档、学术论文、社区资源、书籍分类排列

## 3. 附录 B — OpenCode 内置能力与生态（7 篇）

### 3.1 概述

附录 B 作为 OpenCode 核心能力参考手册，涵盖内置能力、命令参考、Plugin 系统、Agent 架构、SDK、Agent SDK 以及生态参考。

> 该附录的内容源自原单一附录 B（拆分前），与新增的附录 C（Claude Code）和附录 D（Pi Agent）共同构成工具生态参考系列。

### 3.2 文章清单

| 文章 | 文件 | 说明 |
|------|------|------|
| OpenCode 内置能力 | `capabilities.md` | OpenCode 内置能力全景概览：工具集、Provider 集成、Agent 体系 |
| OpenCode 内置命令 | `commands.md` | 内置命令速查手册：核心命令、OMO 扩展命令、自定义命令 |
| OpenCode Plugin 系统 | `plugins.md` | Plugin API 参考、20+ Hook 点、配置管理、安全考虑 |
| OpenCode Agent 架构 | `agent-architecture.md` | Agent 架构设计与编排模型：Build/Plan/Explore/Agent 调用链 |
| OpenCode SDK 参考 | `sdk.md` | Plugin SDK 与 npm SDK：definePlugin API、Tool 定义 Schema |
| OpenCode Agent SDK 编程 | `agent-sdk.md` | Agent SDK 编程接口：自定义 Agent 开发、事件处理、工具注册 |
| OpenCode 生态参考 | `ecosystem.md` | 社区项目、Skill 推荐、MCP 服务器、资源汇总 |

### 3.3 目标读者

- 需要快速查阅 OpenCode 命令和配置的高级用户
- 需要开发 Plugin 或扩展 OpenCode 功能的开发者
- 希望了解 OpenCode 生态全貌的架构师和技术负责人

### 3.4 格式要求

- 使用 Markdown 表格展示命令列表、API 参考、Hook 点
- 代码示例使用 TypeScript/JSON 格式
- 使用 `→ [章节名称](相对路径.md)` 格式添加交叉引用
- OMO 特性需标注"oh-my-openagent 特有"免责声明

## 4. 附录 C — Claude Code 内置能力与生态（7 篇）

### 4.1 概述

附录 C 作为竞品对照参考手册，系统整理 Claude Code 的内置能力、命令参考、扩展机制、SDK、Agent SDK、Agent 设计指南以及生态参考，方便读者对比 OpenCode 与 Claude Code 的设计差异。

### 4.2 文章清单

| 文章 | 文件 | 说明 |
|------|------|------|
| Claude Code 内置能力 | `capabilities.md` | Claude Code 内置能力与工具集：Agent 工具、文件系统、MCP、Shell |
| Claude Code 命令参考 | `commands.md` | Slash 命令与 CLI 命令速查：内置命令、Hook、权限设置 |
| Claude Code 扩展机制 | `extensions.md` | 扩展机制概览：自定义 Slash Command、Hook 配置文件 |
| Claude Code Plugin 系统 | `plugins.md` | 六层扩展体系详解：CLAUDE.md、Hook、Command 等 |
| Claude Code SDK 参考 | `sdk.md` | MCP 服务器与 CLI 程序化集成：SDK 安装、服务器开发 |
| Claude Code Agent SDK 编程 | `agent-sdk.md` | Agent SDK 编程接口：Agent 配置、工具定义、会话管理 |
| Claude Code Agent 设计指南 | `agent-architecture.md` | Agent 设计模式与架构：CLAUDE.md、工具/模型路由、MCP |
| Claude Code 生态参考 | `ecosystem.md` | 社区扩展与最佳实践：常用 MCP 服务器、CLI 集成、团队实践 |

### 4.3 目标读者

- 正在评估 OpenCode vs Claude Code 的技术选型者
- 从 Claude Code 迁移到 OpenCode 的开发者
- 需要了解竞品架构差异的 AI 编程工具研究者

### 4.4 格式要求

- 使用 Markdown 表格展示命令、API 和扩展点
- 代码示例使用 TypeScript/JSON/YAML 格式
- 每个条目标注与 OpenCode 的对应关系（相同、不同、独有）
- 使用 `对比：→ [OpenCode 对应章节](相对路径.md)` 格式做交叉对照

## 5. 附录 D — Pi Agent（5 篇）

### 5.1 概述

附录 D 作为生态扩展与竞品参考手册，涵盖 Pi Agent 的核心能力：概述与核心概念、CLI 命令与交互模式、扩展体系、SDK 以及生态参考。

### 5.2 文章清单

| 文章 | 文件 | 说明 |
|------|------|------|
| Pi Agent 概述与核心概念 | `overview.md` | Pi 设计哲学与核心架构：文件映射架构、Rule 系统、Provider 模型 |
| CLI 命令与交互模式参考 | `commands.md` | 交互模式编辑器（Vim/Nano/Emacs）、Slash 命令、CLI 命令 |
| 扩展体系详解 | `customization.md` | 四层扩展体系详解：CLI 配置、Rule 系统、Provider、MCP |
| Pi Agent SDK 参考 | `sdk.md` | Agent Session API 与 RPC 模式：会话管理、远程 Agent |
| 生态与集成场景 | `ecosystem.md` | Provider 生态（Anthropic/OpenAI/GCP Vertex/OpenRouter）与集成场景 |

### 5.3 目标读者

- 正在评估 OpenCode vs Pi Agent 的技术选型者
- 对多 Agent 编程工具有兴趣的开发者
- 需要了解 Pi Agent 独特架构（文件映射、Rule 系统）的研究者

### 5.4 格式要求

- 使用 Markdown 表格展示命令、配置和 API
- 代码示例使用 TypeScript/JSON/YAML 格式
- 每个条目标注与 OpenCode 的对应关系（相同、不同、独有）
- 使用 `对比：→ [OpenCode 对应章节](相对路径.md)` 格式做交叉对照

## 6. 验证标准

- [ ] 附录 A 术语表覆盖全书 30+ 核心术语
- [ ] 附录 B 内置命令完整列出，Plugin Hook 点完整
- [ ] 附录 C Claude Code 能力完整覆盖，与 OpenCode 做交叉引用
- [ ] 附录 D Pi Agent 架构准确描述，对比标注正确
- [ ] 所有 4 个附录与 SUMMARY.md 导航一致
- [ ] 跨附录交叉引用格式统一（`→ [章节](路径.md)`）
- [ ] mdbook build 通过
- [ ] 内部链接无 404
