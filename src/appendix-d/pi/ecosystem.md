# Pi **Agent（智能体）** 生态参考

本章节围绕 **Harness Engineering（驾驭工程）** 和 **Loop Engineering（循环工程）** 两大主线，将 Pi Agent 生态资源按工程价值分类组织，帮助你在实际工作中找到最相关的工具和实践参考。

Pi 的设计哲学是**极简但可工程化**——内置 4 个核心工具（read/write/edit/bash）、~1K token 系统提示、20+ Provider 自由切换。以下生态分类围绕这一哲学，聚焦如何用 Pi 构建可靠的生产环境工作流。

## 驾驭工程生态（Harness Engineering）

聚焦 Provider 策略、安全模型和 Extension 约束机制——让 Pi Agent 在可控范围内可靠执行。

### Provider 策略生态

Pi 提供 **20+ 内置 Provider**，覆盖 324 个模型，这是驾驭工程中"成本管控"和"模型路由"的基础能力。

| 类别 | Provider |
|------|----------|
| **前沿模型** | Anthropic（Claude 系列）、OpenAI（GPT-4o/o1/o3 系列）、Google（Gemini 系列） |
| **开源/国产** | DeepSeek、Mistral、Groq、Together AI、Fireworks AI |
| **云平台** | AWS Bedrock、GCP Vertex AI、Azure OpenAI |
| **代码助手** | GitHub Copilot、Codeium |
| **本地模型** | Ollama、LM Studio、vLLM |
| **其他** | xAI（Grok）、Perplexity、Anyscale、Replicate、OpenRouter |

**模型管理特性（直接对应 Harness Engineering 成本支柱）：**

- **统一流式 API**：所有 Provider 通过一致的流式接口调用，无需适配不同 SDK
- **自动认证解析**：支持 API Key、OAuth 等多种认证方式
- **Token 与成本追踪**：内置 Token 计数和成本估算，可实时监控消耗
- **跨 Provider 切换**：同一 Session 内可中途切换模型（`/model` 命令），适配不同任务复杂度
- **类型安全工具定义**：使用 TypeBox（`@sinclair/typebox`）Schema 定义工具参数
- **摇树优化**：可按需注册单个 Provider，减小打包体积
- **循环切换**：`Ctrl+P` / `Shift+Ctrl+P` 在已启用模型间轮换

**Thinking Budget 控制：**

| 等级 | 说明 |
|------|------|
| `off` | 不展示推理过程 |
| `minimal` | 最小推理 |
| `low` | 低推理预算 |
| `medium` | 中等推理预算（默认） |
| `high` | 高推理预算 |
| `xhigh` | 最大推理预算 |

### 安全模型

Pi 的安全哲学基于明确信任边界：

```text
Pi 将宿主机用户账户视为同一信任边界内的实体。
```

安全模型的 Harness Engineering 映射：

1. **用户信任边界**：Pi 默认具有宿主机用户的所有权限（L3 约束起点）
2. **无内置沙箱**：不提供内置权限弹窗或沙箱，需通过容器化方案隔离（L3 约束扩展）
3. **Project Trust**：通过 `/trust` 控制每个项目的信任决策（L3 访问控制）
4. **可信扩展**：Extensions 和 Skills 运行在 Agent 进程中，需从可信源安装（L3 供应链安全）
5. **Prompt 注入**：Pi 明确不对 AGENTS.md 及项目文件中的指令注入做防护（L3 风险认知）

> 完整的安全策略见 [SECURITY.md](https://github.com/earendil-works/pi/blob/main/SECURITY.md)

### 容器化沙箱方案

对于需要安全隔离的场景，Pi 提供 3 种容器化方案，构成 Harness Engineering 的隔离层：

| 方案 | 隔离对象 | 最佳场景 | 要求 |
|------|---------|---------|------|
| **Gondolin** | 内置工具 + `!` 命令 | 本地微 VM 隔离，保留宿主机认证 | Node >=23.6.0 + QEMU |
| **Plain Docker** | 整个 Pi 进程 | 简单本地隔离 | Docker |
| **OpenShell** | 整个 Pi 进程 | 策略控制沙箱 | OpenShell Gateway |

**Gondolin（推荐）：**

Gondolin 是一个本地 Linux 微 VM，通过 Extension 机制将 Pi 的内置工具路由到 VM 中执行，同时保留宿主机上的 Provider API 认证信息。

```bash
cp -R packages/coding-agent/examples/extensions/gondolin ~/.pi/agent/extensions/gondolin
cd ~/.pi/agent/extensions/gondolin
npm install --ignore-scripts

# 启动
pi -e ~/.pi/agent/extensions/gondolin
```

工作区目录自动挂载到 VM 的 `/workspace`，文件变更双向同步。

**Plain Docker：**

```dockerfile
FROM node:24-bookworm-slim
RUN apt-get update && apt-get install -y bash ca-certificates git ripgrep
RUN npm install -g --ignore-scripts @earendil-works/pi-coding-agent
WORKDIR /workspace
ENTRYPOINT ["pi"]
```

**OpenShell：**

基于 NVIDIA OpenShell 的策略控制沙箱，支持文件系统、进程、网络、认证和推理的策略管控：

```bash
openshell sandbox create --name pi-sandbox --from pi -- pi
```

OpenShell 提供远程网关模式，可让沙箱在远端运行而 Provider API Key 保留在本地网关。

---

## 循环工程生态（Loop Engineering）

聚焦 SDK 嵌入、RPC 自动化、Session 持久化和分支管理——"我不在时工作如何继续"。

### 程序化集成（4 种模式）

Pi 提供 4 种集成方式，适应从单次执行到持续循环的不同粒度的嵌入需求。

#### SDK 模式（Node.js 嵌入）

通过 `@earendil-works/pi-agent-core` 在 Node.js 应用中直接嵌入 Agent 能力：

```typescript:src/appendix-d/pi/ecosystem.md
import { Agent } from "@earendil-works/pi-agent-core";
import { agentLoop } from "@earendil-works/pi-agent-core/agent-loop";

const agent = new Agent({
  model: "anthropic:claude-sonnet-4-20250514",
  systemPrompt: "你是一个代码助手",
});

// 直接使用底层事件流
for await (const event of agentLoop(agent, [
  { role: "user", content: "解释这段代码" },
])) {
  // 处理流式事件
}
```

SDK 模式提供对 Agent 的完全控制，包括：
- 自定义工具注册
- 状态管理（AgentState）
- 事件流处理
- 上下文预处理（`transformContext`）
- 工具调用前/后钩子（对应 Loop Engineering 中的 Hook 点）

#### RPC 模式（跨语言 IPC）

RPC 模式通过 stdin/stdout 的 JSONL 协议，让非 Node.js 进程也能集成 Pi：

```bash
pi --mode rpc
```

协议使用 LF 分隔的 JSONL 帧，支持以下请求类型：
- `chat` — 发送消息并接收流式响应
- `execute` — 执行单次工具调用
- `get_state` — 获取当前状态
- `reset` — 重置会话

适合 Python、Rust、Go 等语言编写的工具或 IDE 插件集成（对应 Loop Engineering 中的跨语言编排）。

#### Print 模式（单次执行）

```bash
pi -p "列出当前目录的文件"              # 执行后返回结果
pi -p "解释这个函数" --source file.ts   # 附带源文件
```

适合 CI/CD 脚本、自动化任务中的单次查询场景（对应 Loop Engineering 中的批处理模式）。

#### JSON Event Stream 模式

```bash
pi --mode json -p "重构这个函数"
```

输出结构化 JSON 事件流，每行一个事件，适合需要精确跟踪 Agent 执行过程的场景（对应 Loop Engineering 中的可观测性）。

### Session 管理

Pi 的 Session 系统支持完整的分支和恢复能力，是 Loop Engineering 中持久化和分支管理的基础。

**存储格式：**

Session 以 JSONL 格式存储在 `~/.pi/agent/sessions/` 目录。每条消息独立一行，包含完整的时间戳和元数据。

| 消息类型 | 角色 | 说明 |
|----------|------|------|
| `user` | 用户 | 用户输入 |
| `assistant` | 助手 | AI 回复 |
| `toolResult` | 工具 | 工具执行结果 |
| `bashExecution` | bash | Bash 命令执行记录（含退出码、输出截断标记） |
| `custom` | 自定义 | Extension 自定义消息（含 `customType` 区分） |
| `branchSummary` | 分支 | Git 分支切换时的上下文摘要 |
| `compactionSummary` | 压缩 | 上下文压缩时的摘要 |

**Session Tree（分支管理）：**

Session 支持树状分支结构，是 Loop Engineering 中"会话隔离"和"并行探索"的关键能力：

- **Fork**：从当前分支的用户消息处创建新的 Session 文件
- **Clone**：复制当前完整活动分支为新 Session
- **Tree**：通过 `/tree` 在分支树中导航，可从任意历史点继续
- **Export/Import**：通过 `/export`、`/import` 导出和导入 Session 文件
- **Share**：通过 `/share` 以私有 GitHub Gist 分享 Session

**上下文压缩：**

Pi 内置自动和手动两种压缩机制：

- **自动压缩**：上下文窗口接近上限时自动触发
- **手动压缩**：`/compact [prompt]` 命令，可附带自定义压缩指令
- **分支摘要**：Git 分支切换时，原分支上下文自动摘要后注入到新分支

---

## 扩展集成生态

### Extension 体系

Pi 的 Extension 系统是其扩展能力的核心，支持自定义工具、命令和事件处理：

| 资源 | 地址 |
|------|------|
| Extensions 示例 | [`packages/coding-agent/examples/extensions/`](https://github.com/earendil-works/pi/tree/main/packages/coding-agent/examples/extensions) |
| Pi Packages | npm 分发，`@earendil-works/pi-coding-agent` |

Extension 类型：
- **工具扩展**：新增 Agent 可调用的工具
- **命令扩展**：新增 `/command` 类命令
- **事件处理**：监听 Agent 生命周期事件
- **Hook 扩展**：工具调用前/后执行自定义逻辑

详见 → [Extensions 详解](./customization.md)

### 跨工具生态对比

| 维度 | Pi Agent | OpenCode | Claude Code |
|------|----------|----------|-------------|
| Provider 数量 | 20+ (324 模型) | 75+ | 仅 Claude |
| SDK 集成 | 原生 TypeScript API + RPC | **Plugin（插件）** Hook 系统 | CLI 调用 |
| 容器化方案 | Gondolin / Docker / OpenShell | Docker | Docker（官方镜像） |
| Session 分享 | GitHub Gist + OSS 社区 | 本地文件 | 无 |
| 扩展分发 | Pi Packages (npm) | npm Plugin | 无标准机制 |
| 社区规模 | 65K+ Stars, 210 万周下载 | 开源社区 | Claude Code 用户群 |
| 本地模型 | Ollama / LM Studio / vLLM | Ollama / vLLM | 不支持 |

---

## 迁移指南

从其他工具迁移到 Pi Agent 时，需要关注以下关键差异：

### 从 Claude Code 迁移

- **模型灵活性**：Claude Code 仅支持 Claude 系列模型，Pi 支持 20+ Provider/324 个模型。迁移后可通过 `/model` 命令随时切换模型，无需配置多套环境
- **扩展机制**：Claude Code 的六层扩展体系（CLAUDE.md + Skills + **MCP（模型上下文协议）** + Subagent + Hook + Plugin）对应 Pi 的四层体系（Extensions/Skills/**Prompt（提示词）** Templates/Themes）。自定义工具需按 Pi 的 Extension API 用 TypeScript 重写，而非 Shell 脚本 Hook
- **安全模型**：Claude Code 内置权限审批弹窗，Pi 无内置沙箱——如需安全隔离必须使用 Gondolin/Docker/OpenShell 容器化方案
- **命令差异**：部分 Slash 命令名称不同，如 Pi 的 `/compact` 行为类似但参数不同，建议查阅 [CLI 命令参考](./commands.md) 逐一确认

### 从 OpenCode 迁移

- **SDK 差异**：OpenCode 使用 REST API（`@opencode-ai/sdk`）通信，Pi 使用原生 TypeScript API（`@earendil-works/pi-agent-core`）或 RPC JSONL 协议。需将 HTTP 调用模式替换为直接函数调用或 stdio 消息
- **Plugin → Extension**：OpenCode 的 Plugin/Hook 机制在 Pi 中对应 Extension 体系，API 模式不同。已有 Plugin 需按 [Extensions 指南](./customization.md) 重写
- **Provider 配置**：OpenCode 通过 `opencode.json` 管理 Provider；Pi 通过环境变量或 `~/.pi/config.yaml` 配置，迁移时需转换格式
- **Session 模型**：OpenCode Session 通过 REST API 创建管理；Pi Session 存储在本地 JSONL 文件，支持 `fork`/`clone`/`tree` 等高级分支操作

### 通用注意事项

1. **Provider 差异**：不同 Provider 的 API 响应格式和 Token 计价方式各异，迁移后需重新评估成本
2. **Extension 信任**：Extensions 运行在 Agent 进程中（同一信任边界），安装前需审计代码来源
3. **工具集覆盖**：Pi 内置 4 个核心工具（read/write/edit/bash），其他能力通过 Extension 提供——迁移前检查 workflow 依赖的工具是否都已覆盖

---

## 社区精选项目

### 官方资源

| 资源 | 地址 |
|------|------|
| 官方文档 | [pi.dev/docs/latest](https://pi.dev/docs/latest) |
| GitHub 仓库 | [github.com/earendil-works/pi](https://github.com/earendil-works/pi) |
| GitHub Issues | [github.com/earendil-works/pi/issues](https://github.com/earendil-works/pi/issues) |
| npm | `@earendil-works/pi-coding-agent` |
| OSS Session 分享 | [pi.dev/sessions](https://pi.dev/sessions) |
| Extensions 示例 | [`packages/coding-agent/examples/extensions/`](https://github.com/earendil-works/pi/tree/main/packages/coding-agent/examples/extensions) |

### Extension 生态列表

| 类别 | 说明 |
|------|------|
| Gondolin | 微 VM 沙箱 Extension，推荐的安全隔离方案 |
| 自定义工具 | 通过 Extension API 添加新工具 |
| 自定义命令 | 通过 Extension API 添加 `/command` |
| Pi Packages | 通过 npm 分发的 Extension 包 |

### 推荐学习资源

| 资源 | 说明 |
|------|------|
| 官方文档 | [pi.dev/docs/latest](https://pi.dev/docs/latest) |
| GitHub 源码 | [github.com/earendil-works/pi](https://github.com/earendil-works/pi) |
| OSS 社区 Session | [pi.dev/sessions](https://pi.dev/sessions) |

## 相关章节

- → [Extensions 详解](./customization.md) — 四层扩展体系详解
- → [Pi Agent 概述](./overview.md) — 设计哲学和核心架构
- → [生态对比](../../01-introduction/ecosystem-comparison.md) — AI 编程工具生态全景

> 数据来源：Pi Agent 官方文档、GitHub 仓库、npm 统计。数据截止 2026 年 6 月。

---

## 读者视角

### 适用读者角色
- 入门开发者 — Pi 的生态资源丰富，降低了使用门槛，适合快速上手
- 智能体开发工程师 — Pi 的 SDK 和 Extension API 为深度定制提供支持
- 效率开发者 — Pi 的 Provider 策略和模型路由支持快速迭代
- 技术负责人 — Pi 的容器化方案（Gondolin/Docker/OpenShell）满足企业安全要求
- **Skill（技能）** 作者 — Pi 的 Skills 系统遵循标准化，易于创建和分享
- 系统架构师 — Pi 的安全模型和信任机制，便于架构评估
- 安全工程师 — Pi 的安全模型透明，易于威胁建模和合规评估

### 典型使用场景
- 通过 Provider 策略实现多模型切换，适应不同任务复杂度
- 通过容器化方案实现安全隔离，满足企业需求
- 通过 Session 管理实现持久化和分支管理，支持长时间运行的应用
- 通过 Extension 体系实现自定义工具和命令，满足特定领域需求
- 通过 Pi Packages 实现扩展分发和共享，实现团队协作
- 通过安全模型实现威胁建模和合规评估，实现企业级安全合规
- 通过模型路由实现不同复杂度任务的模型自动选择，实现高效工作流

### 使用示例
```bash
# 安装 Pi Core
npm install -g @earendil-works/pi-coding-agent

# 启动 Pi
pi

# 使用 Provider 策略
/model

# 使用容器化方案
pi -e ~/.pi/agent/extensions/gondolin

# 使用 Session 管理
/new
/tree

# 使用 Extension
pi -e ./my-extension.ts

# 安装 Pi Package
pi packages install my-pi-package
```

### 工程化示例

**配置顺序检查表：**

1. **安装 Pi Core**
   ```bash
   npm install -g @earendil-works/pi-coding-agent
   ```

2. **创建项目目录**
   ```bash
   mkdir -p my-project
   cd my-project
   ```

3. **启动 Pi**
   ```bash
   pi --name "my task"
   ```

4. **使用 Provider 策略**
   ```bash
   /model
   ```

5. **使用容器化方案**
   ```bash
   pi -e ~/.pi/agent/extensions/gondolin
   ```

6. **使用 Session 管理**
   ```bash
   /new
   # 输入提示词
   ```

### 与前/后文章的衔接
- ← [Pi Agent 概述与核心概念](../overview.md) — 提供 Pi 的设计哲学和核心架构
- → [Pi Agent SDK 参考](./sdk.md) — 学习 Pi 的程序化集成和 SDK 使用
