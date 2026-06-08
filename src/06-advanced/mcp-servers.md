# MCP 服务器

> MCP（Model Context Protocol）是 Agent 与外部系统通信的开放协议。理解它的工作原理、传输方式和安全模型，是扩展 AI 编程能力的关键一步。
> **适合读者**: 后端开发者 · Skill 作者

## 文章概述

MCP 是 OpenCode 生态中让 Agent 突破工具边界的基础设施。如果把 Agent 比作执行者，MCP 就是它的"触手"——让 Agent 能够查询数据库、调用 REST API、搜索网络、操作文件系统。与 Plugin 不同，MCP 走的是"外连接"路线：Agent 通过标准协议与外部服务通信，而不是直接在进程内加载扩展。

本文从 MCP 协议的核心模型出发，讲解三种传输类型（stdio、streamable-http、websocket）的适用场景，分析 MCP 如何与 ToolRegistry 无缝集成（对 LLM 而言，内置工具和 MCP 工具没有任何区别），最后深入安全配置——包括进程隔离、环境变量管理和 OAuth 认证。读完本文，你应该能独立配置并验证至少一个自定义 MCP 服务器。

> **⏱ 时间有限？先读这些：** MCP 协议概览 → MCP 配置详解 → ToolRegistry 集成 → 安全考虑

## 内容要点

1. **MCP 协议概览** — MCP 的核心概念：MCP 是 AI Agent 的"API 集成层"，定义了一套标准的工具/资源/提示接口。对比 Plugin（内扩展）与 MCP（外连接）的架构差异，展示 MCP 能做什么：数据库查询、API 调用、文件系统操作、搜索引擎、AI 服务调用等。

2. **MCP 配置详解** — 三种传输类型的配置方法与选型建议：stdio 适用于本地子进程（低延迟、高安全）、streamable-http 适用于远程服务（灵活部署、跨网络）、websocket 适用于全双工通信（实时推送、长连接）。配置格式围绕 `opencode.json` 中的 `mcpServers` 段展开，包括环境变量管理的最佳实践。

3. **MCP 与 ToolRegistry 集成** — 对 LLM 而言，内置 Tool 和 MCP Tool 完全无差别——它们共享同一套 ToolRegistry。解析 MCP Tool 的完整生命周期：注册、发现、调用、结果返回。介绍内置 OMO MCP 服务器（Exa WebSearch、Context7、Grep.app）作为参考实现。

4. **安全考虑** — MCP 服务器的进程隔离机制、环境变量分离原则（不共享 OpenCode 进程环境）、OAuth 认证配置。使用 STRIDE 方法分析 MCP 通信通道（stdio/SSE/WebSocket）的威胁面，重点关注中间人攻击和未授权访问风险。

5. **实战：配置一个自定义 MCP 服务器** — 从服务器端实现、客户端配置到功能验证的完整流程，涵盖服务端 SDK 的使用方式（Node.js/Python）。

## 关联章节

- ← [Agent 编排](../02-core-concepts/agent-orchestration.md)（Agent 的工具调用机制）
- ← [OpenCode 配置详解](../03-setup/opencode-config.md)（MCP 在 opencode.json 中的配置位置）
- → [性能调优与成本管理](performance-tuning.md)（MCP 调用的性能考量）

---

## MCP 协议概览

### MCP 是什么：AI Agent 的 "USB 接口"

MCP（Model Context Protocol）本质上做了一件事：**给 AI Agent 一个标准化的方式去连接外部服务**。这跟 USB 标准做的事一模一样——不管你是接鼠标、键盘还是外置硬盘，插上同一个接口就能工作。MCP 就是 AI 世界的 USB：Agent 通过它连接数据库、搜索引擎、文件系统、API 服务，甚至其他 AI 模型。

```mermaid
flowchart TB
    subgraph Agent["AI Agent"]
        LLM["大语言模型<br/>推理核心"]
        TR["ToolRegistry<br/>工具注册中心"]
    end

    subgraph Builtin["内置工具（直接调用）"]
        BT1["文件操作工具"]
        BT2["命令执行工具"]
        BT3["搜索工具"]
    end

    subgraph MCP["MCP 协议层（标准接口）"]
        CP["MCP Client Protocol<br/>客户端协议"]
    end

    subgraph MCP_Servers["MCP 服务器（外部服务）"]
        DB_MCP[("Database MCP<br/>PostgreSQL/MySQL")]
        API_MCP["API MCP<br/>REST/GraphQL"]
        FS_MCP["Filesystem MCP<br/>远程文件系统"]
        SEARCH_MCP["Search MCP<br/>Web/Codesearch"]
    end

    subgraph External["外部世界"]
        DB[("Database")]
        API["REST API"]
        REMOTE_FS["Remote Storage"]
        WEB["Web/搜索引擎"]
    end

    LLM -->|"调用 Tool"| TR
    TR -->|"内置工具"| BT1
    TR -->|"内置工具"| BT2
    TR -->|"内置工具"| BT3
    TR -->|"MCP 协议"| CP
    CP -->|"stdio/HTTP/WS"| DB_MCP
    CP --> API_MCP
    CP --> FS_MCP
    CP --> SEARCH_MCP
    DB_MCP --> DB
    API_MCP --> API
    FS_MCP --> REMOTE_FS
    SEARCH_MCP --> WEB

    style Agent fill:#e8f0fe
    style Builtin fill:#e8f8e8
    style MCP fill:#f0e8ff
    style MCP_Servers fill:#f0e8ff
    style External fill:#f5f0ff
    style LLM fill:#4A90D9,color:#fff
    style TR fill:#4A90D9,color:#fff
    style BT1 fill:#50C878,color:#fff
    style BT2 fill:#50C878,color:#fff
    style BT3 fill:#50C878,color:#fff
    style CP fill:#A66CFF,color:#fff
    style DB_MCP fill:#A66CFF,color:#fff
    style API_MCP fill:#A66CFF,color:#fff
    style FS_MCP fill:#A66CFF,color:#fff
    style SEARCH_MCP fill:#A66CFF,color:#fff
    style DB fill:#d4c4f0
    style API fill:#d4c4f0
    style REMOTE_FS fill:#d4c4f0
    style WEB fill:#d4c4f0
```

**一句话总结**：MCP 把 Agent 的能力边界从"内置工具箱"扩展到"外面整个世界"。

### Plugin vs MCP：内扩展 vs 外连接

这两个概念容易混淆，最直接的理解方式：

| 维度 | Plugin | MCP |
|------|--------|-----|
| **运行位置** | Agent 进程内（同一内存空间） | 独立进程或远程服务器（进程隔离） |
| **协议** | 直接 API 调用（Plugin SDK） | 标准 MCP 协议（JSON-RPC over stdio/HTTP/WS） |
| **安全边界** | 依赖 Plugin 自身安全 | 进程级隔离 + 环境变量分离 |
| **扩展方向** | 修改 Agent 行为（Hook 点） | 连接外部工具/服务 |
| **典型场景** | 敏感信息嗅探、自定义指令处理 | 数据库查询、API 调用、网络搜索 |
| **性能开销** | 低（进程内调用） | 中（IPC 或网络 RPC） |
| **语言** | 仅 TypeScript（OpenCode SDK） | 任意语言（MCP SDK 支持 Node.js/Python/Java/Go/Rust） |

在实践中，Plugin 和 MCP 的关系是互补的：Plugin 改变 Agent 内部行为，MCP 扩展 Agent 外部能力。

### MCP 能干什么

MCP 服务器一旦注册，Agent 就能以 **Tool** 的形式调用它。以下是 OMO 生态中内置的 MCP 服务器参考实现：

| MCP 服务器 | 能力 | 传输类型 | 使用方式 |
|-----------|------|---------|---------|
| **Exa WebSearch** | 互联网搜索、新闻检索、内容抓取 | streamable-http | Agent 自动调用 |
| **Context7** | 文档查询（React/Vue/AWS/MongoDB 等） | streamable-http | @context7 子 Agent |
| **Grep.app** | 代码搜索（公共 GitHub 仓库） | streamable-http | Agent 自动调用 |
| **Filesystem MCP** | 远程文件系统操作 | stdio | 配置后可用 |
| **Database MCP** | SQL 数据库查询 | stdio | 配置后可用 |

这些 MCP 服务器被 Agent 调用时，跟调用内置的 `read_file`、`grep` 在 LLM 眼中是同一回事——后面会在 [ToolRegistry 集成](#mcp-与-toolregistry-集成) 详细解释。

## MCP 配置详解

### 三种传输类型

MCP 支持三种传输方式，分别对应不同的部署场景。理解它们的差异是正确配置的第一步。

```mermaid
flowchart LR
    subgraph stdio["stdio（本地子进程）"]
        A1[OpenCode Agent]
        P1[[stdin/stdout]]
        M1[MCP 服务器进程]
        A1 -->|启动子进程| M1
        M1 -->|JSON-RPC over stdio| A1
    end

    subgraph streamable["streamable-http（远程 HTTP）"]
        A2[OpenCode Agent]
        P2[[HTTP SSE]]
        M2[MCP HTTP Server]
        A2 -->|POST /message| M2
        M2 -->|SSE stream / 单响应| A2
    end

    subgraph websocket["WebSocket（全双工）"]
        A3[OpenCode Agent]
        P3[[WebSocket]]
        M3[MCP WS Server]
        A3 <-->|全双工 JSON-RPC| M3
    end

    style stdio fill:#f5f0ff
    style streamable fill:#f0e8ff
    style websocket fill:#ebe0ff
    style A1 fill:#4A90D9,color:#fff
    style A2 fill:#4A90D9,color:#fff
    style A3 fill:#4A90D9,color:#fff
    style M1 fill:#A66CFF,color:#fff
    style M2 fill:#A66CFF,color:#fff
    style M3 fill:#A66CFF,color:#fff
    style P1 fill:#C9B8FF,color:#333
    style P2 fill:#C9B8FF,color:#333
    style P3 fill:#C9B8FF,color:#333
```

#### stdio（本地子进程）

最常用也最安全的传输方式。OpenCode 启动一个子进程运行 MCP 服务器，通过标准输入输出（stdin/stdout）传递 JSON-RPC 消息。Agent 进程和 MCP 服务器进程之间完全隔离。

```json:opencode.json
{
  "mcp": {
    "postgres": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-postgres", "--connection-string", "{env:DATABASE_URL}"],
      "environment": {
        "PGAPPNAME": "opencode-mcp"
      },
      "enabled": true,
      "timeout": 30000
    }
  }
}
```

**适用场景**：本地数据库查询、文件系统操作、代码分析工具。延迟最低（无需网络往返），安全性最高（进程隔离）。

#### streamable-http（远程服务）

OpenCode 通过 HTTP POST 请求向远程 MCP 服务器发送消息，服务器可以返回 SSE 流式响应或单次 JSON 响应。适合部署在独立服务器上的 MCP 服务。

```json:opencode.json
{
  "mcp": {
    "internal-api": {
      "type": "remote",
      "url": "https://mcp.internal.company.com/api",
      "headers": {
        "Authorization": "Bearer {env:MCP_API_TOKEN}",
        "X-Request-Id": "{session:id}"
      },
      "oauth": {
        "tokenUrl": "https://auth.company.com/oauth/token",
        "clientId": "{env:MCP_CLIENT_ID}",
        "clientSecret": "{env:MCP_CLIENT_SECRET}"
      },
      "timeout": 15000,
      "enabled": true
    }
  }
}
```

**适用场景**：企业内部 API 网关、团队共享的 MCP 服务、第三方 MCP 提供商。需要网络可达，适合微服务架构。

#### WebSocket（全双工通信）

WebSocket 连接建立后，Agent 和 MCP 服务器可以双向实时通信。适合需要服务器推送的场景（如日志流、实时数据订阅）。

```json:opencode.json
{
  "mcp": {
    "event-stream": {
      "type": "remote",
      "url": "wss://events.internal.company.com/mcp",
      "headers": {
        "Authorization": "Bearer {env:MCP_WS_TOKEN}"
      },
      "enabled": true,
      "timeout": 60000
    }
  }
}
```

**适用场景**：实时事件流处理、监控数据推送、长连接交互。注意：WebSocket 在网络不稳定时可能断连，需要配置重连策略。

### 传输类型对比与选型决策

| 维度 | stdio | streamable-http | WebSocket |
|------|-------|----------------|-----------|
| **网络需求** | 无（本地 IPC） | 需要 HTTP 可达 | 需要 WS 可达 |
| **延迟** | 微秒级 | 毫秒级（受网络影响） | 毫秒级（建立后低延迟） |
| **进程隔离** | 是（独立子进程） | 是（独立服务器） | 是（独立服务器） |
| **状态管理** | 进程生命周期内 | 无状态（每次请求独立） | 有状态（长连接） |
| **部署复杂度** | 低（随命令行启动） | 中（需要 HTTP 服务器） | 中（需要 WS 服务器） |
| **日志/调试** | 子进程 stdout/stderr | HTTP 日志 | WS 帧日志 |
| **推荐场景** | 本地开发、个人工具 | 团队共享、CI/CD 集成 | 实时监控、事件驱动 |

### 环境变量管理

MCP 服务器有**独立的环境变量作用域**，不会继承 OpenCode 进程的环境变量。这既是安全设计（防止敏感信息泄露），也是管理挑战（需要显式传递配置）：

```json:opencode.json
{
  "mcp": {
    "openai-proxy": {
      "type": "local",
      "command": ["node", "mcp-openai"],
      "environment": {
        "OPENAI_API_KEY": "{env:OPENAI_API_KEY}",
        "OPENAI_BASE_URL": "{env:OPENAI_BASE_URL}",
        "LOG_LEVEL": "debug"
      },
      "enabled": true
    }
  }
}
```

最佳实践：
1. 使用 `{env:VAR_NAME}` 语法引用宿主环境变量，不硬编码密钥
2. 每个 MCP 服务器只传递它需要的环境变量，最小化暴露面
3. 不要使用 `.env` 文件自动加载——显式配置更可控
4. 敏感环境变量在 MCP 进程启动后不可见（通过 `/proc` 或 `tasklist` 查看进程环境变量的攻击已被 OpenCode 阻止）

## MCP 与 ToolRegistry 集成

### 统一的工具接口

对 LLM 而言，内置 Tool 和 MCP Tool **完全无差别**。它们共享同一套 ToolRegistry，在 Agent 的推理过程中，所有可用工具被打平成一个列表交给 LLM 选择。LLM 看到的工具定义格式完全一致：

```json:terminal
{
  "tools": [
    { "name": "read_file", "description": "读取文件内容", "builtin": true },
    { "name": "execute_command", "description": "执行 shell 命令", "builtin": true },
    { "name": "postgres_query", "description": "执行 SQL 查询", "mcp": "postgres" },
    { "name": "web_search", "description": "搜索互联网", "mcp": "exa-websearch" },
    { "name": "jira_search", "description": "查询 Jira 问题", "mcp": "jira" }
  ]
}
```

LLM 只需要知道工具的名称、描述和参数签名，不需要知道它来自内置系统还是 MCP 服务器。

### MCP Tool 生命周期

一个 MCP 工具从注册到结果返回经历四个阶段：

```text:terminal
注册（Registration）
  ↓
发现（Discovery）
  ↓
调用（Invocation）
  ↓
返回（Response）
```

#### 阶段 1：注册（Registration）

OpenCode 启动时，读取 `opencode.json` 中的 `mcp` 配置段，为每个启用的 MCP 服务器创建 MCP Client 实例。对于 `type: "local"` 的服务器，启动子进程并建立 stdio 连接。

#### 阶段 2：发现（Discovery）

MCP Client 向服务器发送 `tools/list` 请求，获取服务器提供的所有工具列表。返回的工具定义包含名称、描述和参数 Schema（JSON Schema 格式）。这些工具定义被注册到 ToolRegistry，与内置工具合并。

#### 阶段 3：调用（Invocation）

Agent 的 LLM 输出工具调用请求（Function Calling），ToolRegistry 根据工具名称路由到对应的执行器：
- 内置工具 → 直接调用实现函数
- MCP 工具 → 通过 MCP Client 发送 `tools/call` 请求

#### 阶段 4：返回（Response）

MCP 服务器执行完工具后返回结果。结果通过 JSON-RPC 响应传递给 MCP Client，再返回给 ToolRegistry，最终回到 LLM 的上下文。

### 内置 OMO MCP 参考实现

OpenCode 内置了三个 OMO MCP 服务器，它们的实现可以作为自定义 MCP 的参考：

| MCP 服务器 | 实现语言 | 核心功能 | 参考价值 |
|-----------|---------|---------|---------|
| **Exa WebSearch** | TypeScript | 搜索互联网、抓取网页内容、新闻检索 | 远程 HTTP MCP、OAuth 集成 |
| **Context7** | TypeScript | 查询技术框架文档（版本感知） | 远程 HTTP MCP、知识库集成 |
| **Grep.app** | TypeScript | 搜索公共 GitHub 代码 | 远程 HTTP MCP、代码搜索 |

## 安全考虑

### 进程隔离

`type: "local"` 的 MCP 服务器作为独立子进程运行，不共享 Agent 进程的内存空间。这意味着：
- Agent 或 MCP 服务器的崩溃不会影响对方
- MCP 服务器无法直接访问 Agent 的内存
- 如果 MCP 服务器被攻陷，攻击者只能访问 MCP 进程自身的资源和环境变量

### 环境变量分离

MCP 服务器的环境变量通过 `environment` 字段显式指定，不会继承宿主环境。这是防止敏感信息泄露的关键设计——一个恶意的 MCP 服务器无法读取宿主的环境变量（除非你显式传递）。

### OAuth 认证

对于远程 MCP 服务器，OAuth 2.0 是推荐的认证方式。OpenCode 支持自动的 OAuth 授权码流程：

```json:opencode.json
{
  "mcp": {
    "github-issues": {
      "type": "remote",
      "url": "https://mcp.github.com/issues",
      "oauth": {
        "authorizationUrl": "https://github.com/login/oauth/authorize",
        "tokenUrl": "https://github.com/login/oauth/access_token",
        "clientId": "{env:GITHUB_MCP_CLIENT_ID}",
        "clientSecret": "{env:GITHUB_MCP_CLIENT_SECRET}",
        "scopes": ["repo", "issues"]
      },
      "enabled": true
    }
  }
}
```

OAuth 流程会在首次连接时自动触发浏览器授权，Token 被安全存储在本地密钥链中。

### STRIDE 威胁分析

基于 STRIDE 模型分析 MCP 通信通道的安全威胁面：

| 威胁类型 | stdio 通道 | HTTP/SSE 通道 | WebSocket 通道 | 缓解措施 |
|----------|-----------|--------------|---------------|---------|
| **S**poofing | 本地进程 PID 可信 | 无认证可伪造请求 | WS 无认证可伪造 | `headers` + OAuth + TLS |
| **T**ampering | 管道数据不可篡改 | HTTP 中间人可篡改 | WS 中间人可篡改 | HTTPS/WSS + 签名 |
| **R**epudiation | 无日志审计 | 可添加 HTTP 日志 | 可添加 WS 日志 | 启用审计日志 |
| **I**nformation Disclosure | 进程环境变量可被读取 | 传输未加密泄露数据 | 传输未加密泄露数据 | 最小环境变量 + TLS |
| **D**enial of Service | 子进程资源耗尽 | 远程服务器被打满 | 连接数耗尽 | 设置 `timeout` + 速率限制 |
| **E**levation of Privilege | 子进程权限提升 | API 未授权访问 | WS 未授权连接 | 最小权限原则 + RBAC |

实际操作建议：
- **生产环境**所有远程 MCP 必须使用 HTTPS/WSS
- **敏感 MCP**（访问数据库、代码仓库等）优先使用 stdio 类型
- **远程 MCP** 必须配置认证（API Token 或 OAuth）
- 为每个 MCP 设置合理的 `timeout` 值，防止无限等待
- 定期审查启用的 MCP 服务器列表，移除不需要的

## 实战：配置自定义 MCP 服务器

### 完整流程：从创建到验证

下面以一个 PostgreSQL 数据库 MCP 服务器为例，走一遍完整的配置流程。

#### 步骤 1：安装 MCP 服务器

```bash:terminal
# 使用 npm 全局安装 PostgreSQL MCP 服务器
npm install -g @modelcontextprotocol/server-postgres

# 或者使用 npx（无需安装，随用随取）
npx -y @modelcontextprotocol/server-postgres --help
```

#### 步骤 2：配置 opencode.json

```json:opencode.json
{
  "mcp": {
    "production-db": {
      "type": "local",
      "command": ["npx", "-y", "@modelcontextprotocol/server-postgres", "--connection-string", "{env:PROD_DATABASE_URL}"],
      "environment": {
        "PGSSLMODE": "require",
        "PGAPPNAME": "opencode-mcp-prod"
      },
      "enabled": true,
      "timeout": 30000
    }
  }
}
```

#### 步骤 3：设置环境变量

```bash:terminal
# 在 shell 中设置（或写入 .bashrc/.zshrc）
export PROD_DATABASE_URL="postgresql://user:password@host:5432/mydb"
```

#### 步骤 4：启动并验证

```bash:terminal
# 启动 OpenCode，检查 MCP 是否注册成功
opencode

# 在对话中测试
# 输入：@build 查询 production-db 中 users 表的前 5 条记录
```

Agent 会自动调用 `production-db` MCP 服务器执行 SQL 查询。如果配置正确，你会看到类似这样的工具调用：

```text:terminal
[production-db] 查询 users 表结构...
[production-db] 执行: SELECT * FROM users LIMIT 5
[production-db] 返回 5 条记录
```

#### 步骤 5：故障排查

如果 MCP 服务器未生效，按以下顺序排查：

```bash:terminal
# 1. 检查 opencode.json 格式
opencode --validate-config

# 2. 检查环境变量是否设置
echo $PROD_DATABASE_URL

# 3. 检查命令是否可执行
npx -y @modelcontextprotocol/server-postgres --version

# 4. 查看 OpenCode 日志
# Windows: %APPDATA%\opencode\logs\
# macOS/Linux: ~/.local/share/opencode/logs/
```

### 一个完整的 Python MCP 服务器示例

如果官方 MCP SDK 不满足需求，你可以自己实现 MCP 服务器。以下是一个简单的文件搜索 MCP 服务器的 Python 实现：

```python:mcp-file-search/server.py
# mcp-file-search/server.py
from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types
import os
import fnmatch

server = Server("file-search")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="search_files",
            description="在指定目录中搜索匹配模式的文件",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "glob 模式，如 **/*.py"},
                    "root_dir": {"type": "string", "description": "搜索根目录"},
                    "max_results": {"type": "integer", "description": "最大返回数量，默认 50"}
                },
                "required": ["pattern", "root_dir"]
            }
        ),
        types.Tool(
            name="count_lines",
            description="统计匹配文件的总行数",
            inputSchema={
                "type": "object",
                "properties": {
                    "pattern": {"type": "string", "description": "glob 模式"},
                    "root_dir": {"type": "string", "description": "搜索根目录"}
                },
                "required": ["pattern", "root_dir"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "search_files":
        pattern = arguments["pattern"]
        root_dir = arguments["root_dir"]
        max_results = arguments.get("max_results", 50)

        matches = []
        for root, dirs, files in os.walk(root_dir):
            for f in files:
                if fnmatch.fnmatch(f, pattern):
                    matches.append(os.path.join(root, f))
                    if len(matches) >= max_results:
                        break
            if len(matches) >= max_results:
                break

        return [types.TextContent(
            type="text",
            text=f"找到 {len(matches)} 个匹配文件:\n" + "\n".join(matches)
        )]

    elif name == "count_lines":
        pattern = arguments["pattern"]
        root_dir = arguments["root_dir"]

        total_lines = 0
        file_counts = {}
        for root, dirs, files in os.walk(root_dir):
            for f in files:
                if fnmatch.fnmatch(f, pattern):
                    filepath = os.path.join(root, f)
                    with open(filepath, "r", errors="ignore") as fp:
                        lines = len(fp.readlines())
                    total_lines += lines
                    file_counts[filepath] = lines

        return [types.TextContent(
            type="text",
            text=f"总行数: {total_lines}\n"
                 f"文件数: {len(file_counts)}\n"
                 + "\n".join(f"{k}: {v} 行" for k, v in file_counts.items())
        )]

    raise ValueError(f"未知工具: {name}")

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="file-search",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

配置到 opencode.json：

```json:opencode.json
{
  "mcp": {
    "file-search": {
      "type": "local",
      "command": ["python", "/path/to/mcp-file-search/server.py"],
      "enabled": true,
      "timeout": 10000
    }
  }
}
```

验证：

```bash:terminal
# 启动 OpenCode 后，Agent 自动发现 file-search 的 2 个工具
# 输入：@build 用 file-search 在 src/ 目录下搜索所有 .ts 文件，然后统计总行数
```

### 自定义 MCP 服务器开发要点

1. **工具命名**：名称使用 snake_case，不超过 64 字符，不包含特殊符号
2. **参数 Schema**：必须包含 `type` 和 `properties`，推荐 `required` 标记必填参数
3. **错误处理**：抛出的异常会被 MCP 协议包装为错误响应，Agent 会重试或通知用户
4. **超时控制**：为耗时操作设置合理超时，避免阻塞 Agent

### Node.js MCP SDK 快速入门

如果你更习惯 Node.js/TypeScript，MCP 官方提供了同等的 `@modelcontextprotocol/sdk`。下面以一个 SQLite 数据库查询工具为例，覆盖 Tool、Resource 定义和错误处理模式——相比前面的 Python 示例，这个例子更贴近真实的后端开发场景。

#### 项目初始化

```bash:terminal
mkdir mcp-sqlite && cd mcp-sqlite
npm init -y
npm install @modelcontextprotocol/sdk better-sqlite3 zod
npm install -D typescript @types/better-sqlite3 @types/node tsx
```

#### 完整服务器代码

```typescript:mcp-sqlite/src/server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";
import Database from "better-sqlite3";

const dbPath = process.env.DB_PATH || "./data.db";
const db = new Database(dbPath);
db.pragma("journal_mode = WAL");

const server = new Server(
  { name: "mcp-sqlite", version: "1.0.0" },
  { capabilities: { tools: {}, resources: {} } }
);

// --- Tool 声明 ---
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "query",
      description: "执行 SQL 查询并返回 JSON 结果",
      inputSchema: {
        type: "object",
        properties: {
          sql: { type: "string", description: "SELECT 查询语句" },
          params: {
            type: "array",
            items: { type: "string" },
            description: "查询参数（可选）",
          },
        },
        required: ["sql"],
      },
    },
    {
      name: "list_tables",
      description: "列出数据库中所有表",
      inputSchema: {
        type: "object",
        properties: {},
        required: [],
      },
    },
  ],
}));

// --- Tool 调用实现 ---
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    if (name === "query") {
      const sql = String(args?.sql ?? "");
      const params = (args?.params as string[]) ?? [];

      // 超时保护：拒绝耗时超过阈值的查询
      const timer = setTimeout(() => {
        throw new Error(`Query timed out after 5000ms: ${sql}`);
      }, 5000);

      const stmt = db.prepare(sql);
      const rows = params.length > 0 ? stmt.all(...params) : stmt.all();
      clearTimeout(timer);

      return {
        content: [{ type: "text", text: JSON.stringify(rows, null, 2) }],
      };
    }

    if (name === "list_tables") {
      const rows = db
        .prepare("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        .all();

      return {
        content: [{
          type: "text",
          text: (rows as any[]).map((r) => `- ${r.name}`).join("\n"),
        }],
      };
    }

    throw new Error(`Unknown tool: ${name}`);
  } catch (error) {
    // MCP 协议自动将 Error 包装为 JSON-RPC 错误响应
    throw new Error(
      error instanceof Error ? error.message : String(error)
    );
  }
});

// --- Resource 声明 ---
server.setRequestHandler(ListResourcesRequestSchema, async () => ({
  resources: [
    {
      uri: `sqlite://${dbPath}/stats`,
      name: "Database Statistics",
      description: "数据库概要信息（表数量、总记录数）",
      mimeType: "application/json",
    },
  ],
}));

// --- 启动 ---
const transport = new StdioServerTransport();
await server.connect(transport);
```

> **⏱ 提示：** `inputSchema` 使用标准 JSON Schema 格式——它既是 MCP 的参数声明，也是 LLM 理解工具调用的依据。描述字段写得越清晰，Agent 的调用准确率越高。

#### Tool vs Resource：什么时候用什么

| 维度 | Tool | Resource |
|------|------|----------|
| **语义** | 动作（做点什么） | 数据（读点什么） |
| **副作用** | 允许（创建、更新、删除） | 禁止（只读） |
| **参数** | 需要输入参数 | 无参数，URI 即标识 |
| **返回** | 任意内容 | 结构化文本/二进制 |
| **适合场景** | SQL 写入、API 调用、文件修改 | 配置读取、状态快照、文档查询 |

#### 配置与验证

```json:opencode.json
{
  "mcp": {
    "sqlite-db": {
      "type": "local",
      "command": ["npx", "tsx", "/path/to/mcp-sqlite/src/server.ts"],
      "environment": {
        "DB_PATH": "./data.db"
      },
      "enabled": true,
      "timeout": 10000
    }
  }
}
```

```bash:terminal
# 验证：启动后 Agent 应自动发现 sqlite-db 的 2 个 Tool + 1 个 Resource
# 输入：@build 用 sqlite-db 的 list_tables 查看有哪些表，再用 query 查数据
```

---

### 将 Express/Fastify 服务转换为 MCP 服务器

如果你已经有现成的 Express 或 Fastify 服务，与其重新实现一套 MCP，不如将现有路由"蒙皮"成 MCP 工具。MCP 的三个核心原语跟 REST 端点之间存在清晰的映射：

| MCP 原语 | REST 对应 | 说明 |
|----------|----------|------|
| **Tool** | `POST /api/*` 等 | 有副作用的操作（创建、更新、删除） |
| **Resource** | `GET /api/*` | 只读数据查询，通过 URI 定位 |
| **Prompt** | `GET /templates/*` | 预定义的提示模板（较少用） |

#### 核心模式：提取业务逻辑，路由与 MCP 共享

不要把 MCP 的 Tool 实现写成 Express handler 的"远程调用"——更好的做法是**将业务逻辑从路由中提取出来**，让 Express 和 MCP 共同调用同一份函数：

```typescript:mcp-user-service/src/business-logic.ts
// 业务逻辑层：不与 Express 或 MCP 耦合
export interface User {
  id: string;
  name: string;
  email: string;
}

const users = new Map<string, User>();

export function createUser(data: User): { success: true } {
  users.set(data.id, data);
  return { success: true };
}

export function getUser(id: string): User | null {
  return users.get(id) ?? null;
}

export function listUsers(): User[] {
  return Array.from(users.values());
}
```

```typescript:mcp-user-service/src/express-routes.ts
// Express 路由层：薄薄的适配器
import express from "express";
import { createUser, getUser, listUsers } from "./business-logic.js";

const app = express();
app.use(express.json());

app.post("/api/users", (req, res) => {
  const user = createUser(req.body);
  res.json(user);
});

app.get("/api/users/:id", (req, res) => {
  const user = getUser(req.params.id);
  if (!user) return res.status(404).json({ error: "Not found" });
  res.json(user);
});

app.get("/api/users", (_req, res) => {
  res.json(listUsers());
});
```

```typescript:mcp-user-service/src/mcp-server.ts
// MCP 层：复用同一份业务逻辑
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { createUser, getUser, listUsers } from "./business-logic.js";

const server = new Server(
  { name: "user-api", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "create_user",
      description: "创建新用户",
      inputSchema: {
        type: "object",
        properties: {
          id: { type: "string", description: "用户 ID" },
          name: { type: "string", description: "用户名称" },
          email: { type: "string", description: "电子邮箱" },
        },
        required: ["id", "name", "email"],
      },
    },
    {
      name: "get_user",
      description: "查询单个用户信息",
      inputSchema: {
        type: "object",
        properties: {
          id: { type: "string" },
        },
        required: ["id"],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "create_user": {
      const result = createUser(args as any);
      return { content: [{ type: "text", text: JSON.stringify(result) }] };
    }
    case "get_user": {
      const { id } = args as any;
      const user = getUser(id);
      if (!user) throw new Error("User not found");
      return { content: [{ type: "text", text: JSON.stringify(user) }] };
    }
    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

这种「共享业务逻辑层」的架构让你可以**逐步**将路由转换为 MCP 工具，而不会破坏已有的 Express 服务。

#### 认证中间件集成

如果现有服务需要鉴权，MCP 层同样需要保护。最直接的方式是在 Tool 调用中校验 Token：

```typescript:mcp-user-service/src/mcp-server.ts
// 在 CallToolRequestSchema handler 中注入认证逻辑
import { IncomingMessage } from "http";

// MCP stdio 传输的认证通过环境变量传递
const EXPECTED_TOKEN = process.env.MCP_API_TOKEN;

// 如果是 streamable-http 传输，可以从请求头提取 Token
async function authenticateRequest(request: any): Promise<void> {
  const token = request?.headers?.authorization?.replace("Bearer ", "");
  if (!token || token !== EXPECTED_TOKEN) {
    throw new Error("Unauthorized: invalid or missing API token");
  }
}
```

在 opencode.json 中配置：

```json:opencode.json
{
  "mcp": {
    "user-api": {
      "type": "local",
      "command": ["node", "/path/to/mcp-user-service/dist/mcp-server.js"],
      "environment": {
        "MCP_API_TOKEN": "{env:USER_API_TOKEN}"
      },
      "enabled": true,
      "timeout": 15000
    }
  }
}
```

#### Fastify 的特殊优势：Schema 复用

Fastify 的 JSON Schema 声明可以**直接映射**到 MCP 的 `inputSchema`，实现一次定义、两处复用：

```typescript:mcp-user-service/fastify-schema.ts
// Fastify 的 Schema 声明
const createUserSchema = {
  type: "object",
  properties: {
    id: { type: "string" },
    name: { type: "string" },
    email: { type: "string" },
  },
  required: ["id", "name", "email"],
} as const;

// 同时用于 Fastify 路由校验
fastify.post<{ Body: { id: string; name: string; email: string } }>(
  "/api/users",
  { schema: { body: createUserSchema } },
  async (request) => createUser(request.body)
);

// 和 MCP inputSchema
tools: [{
  name: "create_user",
  description: "创建新用户",
  inputSchema: createUserSchema, // 同一个对象
}]
```

#### 转换决策速查

| 你的现状 | 推荐做法 |
|----------|---------|
| 已有 Express/Fastify 项目 | 提取业务逻辑层，路由与 MCP 共享同一份代码 |
| 服务需要独立部署 | MCP 使用 streamable-http 传输，指向同一套后端 |
| API 需要严格访问控制 | 业务逻辑层统一做鉴权，Express 和 MCP 共用 |
| 想逐步迁移 | 先暴露 2-3 个核心路由为 MCP Tool，验证后再扩展 |

> **⏱ 提示：** 不需要把全部 API 端点映射到 MCP。只选择 Agent 会频繁调用的那些操作——通常是查询、搜索、创建等核心能力。读多写少的操作集最适合先上车。

## 验证标准

完成本文学习后，你应该能：

1. 在 `opencode.json` 中正确配置至少一个 MCP 服务器（任意传输类型），并验证 `tools/list` 返回的工具列表
2. 区分 stdio、streamable-http、WebSocket 三种传输类型的适用场景，并能根据部署环境做出选择
3. 解释 MCP 与 Plugin 的架构差异，以及在 ToolRegistry 中内置工具和 MCP 工具的等效性
4. 配置远程 MCP 服务器的 OAuth 认证，并验证 Token 生命周期
5. 使用 STRIDE 方法分析 MCP 通信通道的安全威胁，并实施至少一种缓解措施
6. 使用 Python 或 Node.js MCP SDK 编写一个自定义 MCP 服务器，包含至少 2 个 Tool 定义
