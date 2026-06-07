# 自定义 Agent 与 Plugin

> 从 Agent 定义到 Plugin 扩展，掌握 OpenCode 生态中最灵活的定制能力——让 AI 编程工作流完全为你所用。
> **适合读者**: Skill 作者 · 技术负责人

## 文章概述

OpenCode 的内置 Agent 已经足够强大，但在真实工程场景中，你几乎总是需要定制。也许是需要一个专门处理安全审计的 Agent（安全工具集 + 严格的权限策略），也许是想在每次文件读写前自动检查敏感信息泄露。这些需求催生了 OpenCode 的两个扩展维度：**自定义 Agent**（配置层面的组合）和 **Plugin**（代码层面的扩展）。

本文先讲解自定义 Agent 的完整流程——从 `agent.json` 或 `opencode.json` 的 `agents` 段定义，到指定角色、Skill、工具集、温度和最大轮次，再到通过 Tab 切换或 Command 指定使用。然后深入 Plugin 开发：`definePlugin` API、添加自定义 Tool（Tool 定义、注册、Agent 使用）、工具优先级（Plugin Tool > MCP Tool > Built-in Tool）、覆盖内置工具。最后以 Env Guard Plugin 作为完整示例，展示 Hook 点如何拦截和保护敏感信息。读完本文，你将能够独立定义自定义 Agent 配置、开发自己的 Plugin 并实现安全 Hook 拦截。

> **⏱ 时间有限？先读这些：** 自定义 Agent 流程 → Plugin 开发基础 → Plugin Hook 点体系 → Env Guard Plugin 示例

## 内容要点

1. **自定义 Agent** — Agent 定义方式（`agent.json` / `opencode.json` `agents` 段），指定角色、Skill、工具集、温度、最大轮次等参数。探讨三种 Agent 派生模式，以及 Effort/Fast Mode/Thinking 等配置选项。自定义 Agent 的使用方式：Tab 切换或 Command 指定。OMO 自定义 Agent 配置示例。

2. **Plugin 开发基础** — `definePlugin` API 的使用，添加自定义 Tool 的三步流程：Tool 定义、注册、Agent 使用。工具优先级机制（Plugin Tool > MCP Tool > Built-in Tool）和同名覆盖内置工具的策略，分析覆盖内置工具的风险与最佳实践。

3. **Plugin Hook 点体系** — OpenCode 内置 20+ Hook 点全景（session:start/end、tool:before/after、command:before/after、permission:check），OMO 扩展的 53+ Hook 点（onWorkflowStart、onAgentSelect、onContextAssemble、onLLMRequest、onQualityGate）。Pipeline 模式的设计哲学——上一个 Hook 的输出是下一个 Hook 的输入。

4. **完整 Plugin 示例：Env Guard** — 实现一个防止敏感信息泄露的安全守卫 Plugin。使用 `preReadFile` + `preWriteFile` Hook 点，通过正则检测 AWS Key、Private Key、GitHub Token、OpenAI Key 等敏感信息。三种处理策略：mask（遮盖）、reject（拒绝）、audit（记录）。

5. **Plugin 部署和管理** — Plugin 的安装、启用/禁用、版本管理和日志调试。

## 关联章节

- ← [Agent 编排](../02-core-concepts/agent-orchestration.md)（Agent 系统基础）
- ← [Skill 系统](../02-core-concepts/skills-system.md)（Plugin 概念初探）
- ← [OpenCode 配置详解](../03-setup/opencode-config.md)（在配置中注册 Plugin）
- → [案例研究](../07-case-studies/)（自定义 Agent 在案例中的应用）

---

## 自定义 Agent 流程

### Agent 的定义方式

自定义 Agent 可以理解为 "给 AI 请一个专业承包商" —— 你需要告诉它："你是负责安全的审计员，我只给你读文件的权限，你每次最多思考 10 轮。" 定义 Agent 有两种方式：

#### 方式一：agent.json（独立文件）

```json:agent.json
{
  "agent": {
    "security-auditor": {
      "description": "安全审计专家，审查代码中的安全漏洞",
      "model": "anthropic/claude-sonnet-4-5",
      "small_model": "anthropic/claude-haiku-4-5",
      "prompt": "你是一名资深安全审计工程师。\n重点关注：\n1. OWASP Top 10 漏洞\n2. 敏感信息泄露\n3. 认证和授权缺陷\n4. 配置安全",
      "skills": ["security-review"],
      "permission": {
        "edit": "deny",
        "read": "allow",
        "bash": {
          "git diff*": "allow",
          "npm audit*": "allow",
          "docker scan*": "allow",
          "*": "ask"
        }
      },
      "temperature": 0.3,
      "max_rounds": 15,
      "color": "#e74c3c"
    }
  }
}
```

#### 方式二：opencode.json agents 段

```json:opencode.json
{
  "agent": {
    "api-designer": {
      "description": "REST API 设计专家，专注 OpenAPI 规范和最佳实践",
      "model": "anthropic/claude-sonnet-4-5",
      "prompt": "你是一名 API 设计专家。专注于：\n1. OpenAPI 3.x 规范\n2. RESTful 设计原则\n3. API 安全性设计\n4. 错误处理策略",
      "skills": ["api-design", "openapi"],
      "permission": {
        "edit": "allow",
        "bash": {
          "npm run openapi*": "allow",
          "*": "deny"
        }
      },
      "temperature": 0.5,
      "max_rounds": 20
    }
  }
}
```

### Agent 配置字段详解

| 字段 | 类型 | 说明 |
|------|------|------|
| `description` | string | 简短描述，用于 Tab 切换时显示 |
| `model` | string | 主模型，影响推理质量和成本 |
| `small_model` | string | 轻量模型，用于简单子任务 |
| `prompt` | string | 角色设定（System Prompt），定义 Agent 的行为 |
| `skills` | string[] | 加载的 Skill 列表 |
| `permission` | object | 权限规则（替代废弃的 `tools` 字段） |
| `temperature` | number | 生成温度 0-1，0.1-0.3 适合精确任务，0.7-0.9 适合创意 |
| `max_rounds` | number | 最大执行轮次，防止无限循环 |
| `color` | string | Tab 和 UI 中显示的颜色 |
| `model_hint` | string | 模型提示，影响路由决策 |

### 使用自定义 Agent

定义完成后，有两种方式使用：

**Tab 切换**：在 OpenCode 聊天界面按 Tab，会列出所有可用 Agent，包括自定义的。选择 `security-auditor` 后，后续对话由该 Agent 处理。

**Command 指定**：在对话中使用 `/agent security-auditor` 切换到指定 Agent。或者在消息中通过 `@security-auditor` 临时调用。

### 三种 Agent 派生模式

| 模式 | 定义位置 | 适用场景 | 优点 |
|------|---------|---------|------|
| **直接定义** | opencode.json | 永久性团队 Agent | 纳入版本控制，可共享 |
| **文件定义** | agent.json | 项目独立的专业 Agent | 模块化，减少主配置 |
| **内联 Prompt** | 对话中 | 一次性临时定义 | 零配置，快速验证 |

### Effort / Fast Mode / Thinking 配置

```json:opencode.json
{
  "agent": {
    "deep-analyst": {
      "description": "深度分析型 Agent，不急于给出结论",
      "model": "anthropic/claude-sonnet-4-5",
      "prompt": "...",
      "effort": 3,
      "fast_mode": false,
      "thinking": true,
      "thinking_budget_tokens": 8000
    },
    "quick-fixer": {
      "description": "快速修复型 Agent，追求效率",
      "model": "anthropic/claude-haiku-4-5",
      "fast_mode": true,
      "thinking": false,
      "temperature": 0.1
    }
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `effort` | 1-5 | 努力程度，越大模型推理越深入但耗时越长 |
| `fast_mode` | boolean | 跳过不必要的确认步骤，直接执行 |
| `thinking` | boolean | 启用思维链（Chain of Thought），提升复杂推理 |
| `thinking_budget_tokens` | number | Thinking 模式下预分配的 Token 预算 |

## Plugin 开发基础

### 什么是 Plugin

Plugin 是 OpenCode 中 **代码层面的扩展点**。如果说自定义 Agent 是 "换一个角色"，Plugin 就是 "改角色的行为逻辑"。Plugin 运行在 Agent 进程内，通过 Hook 系统拦截和修改 Agent 的行为。

### 一个 Plugin 的核心结构

```typescript:plugin-hello-world.ts
import { definePlugin } from "opencode";

export default definePlugin({
  name: "hello-world",
  description: "一个简单的 Plugin 示例",
  hooks: {
    "session:start": async (session) => {
      console.log(`Session 开始: ${session.id}`);
    },
    "tool:before": async (params) => {
      console.log(`即将调用工具: ${params.tool}`);
    },
    "tool:after": async (params) => {
      console.log(`工具调用完成: ${params.tool}, 耗时 ${params.duration}ms`);
    }
  }
});
```

### 添加自定义 Tool

Plugin 的核心能力之一是定义新的 Tool。流程分三步：

**步骤 1：定义 Tool**

```typescript:plugin-weather-tool.ts
import { definePlugin } from "opencode";

export default definePlugin({
  name: "weather-tool",
  description: "添加天气查询工具",
  tools: [
    {
      name: "get_weather",
      description: "查询指定城市的当前天气",
      parameters: {
        type: "object",
        properties: {
          city: { type: "string", description: "城市名称（中文）" },
          units: { type: "string", enum: ["celsius", "fahrenheit"], default: "celsius" }
        },
        required: ["city"]
      },
      handler: async (params) => {
        const apiKey = process.env.WEATHER_API_KEY;
        const resp = await fetch(
          `https://api.weather.com/v1/current?city=${encodeURIComponent(params.city)}&key=${apiKey}`
        );
        const data = await resp.json();
        return `当前 ${params.city} 天气: ${data.condition}，温度: ${data.temperature}°${params.units === "celsius" ? "C" : "F"}`;
      }
    }
  ]
});
```

**步骤 2：在 opencode.json 中注册 Plugin**

```json:opencode.json
{
  "plugin": {
    "weather-tool": {
      "path": "./plugins/weather-tool/index.ts",
      "enabled": true
    }
  }
}
```

**步骤 3：在自定义 Agent 中使用**

```json:opencode.json
{
  "agent": {
    "weather-bot": {
      "description": "天气查询助手",
      "model": "anthropic/claude-haiku-4-5",
      "prompt": "你是一个天气助手。当用户询问天气时，使用 get_weather 工具查询。",
      "permission": {
        "edit": "deny",
        "bash": {
          "*": "deny"
        }
      }
    }
  }
}
```

### 工具优先级机制

当多个来源定义了同名工具时，优先级规则如下：

```
Plugin Tool > MCP Tool > Built-in Tool
```

这意味着你可以用 Plugin 覆盖内置的 `read_file`、`web_search` 等工具：

```typescript:plugin-audit-reader.ts
import { definePlugin } from "opencode";

export default definePlugin({
  name: "audit-reader",
  description: "审计所有文件读取操作",
  tools: [
    {
      name: "read_file",  // 同名覆盖内置 read_file
      description: "读取文件（带审计日志）",
      parameters: {
        type: "object",
        properties: {
          path: { type: "string", description: "文件路径" }
        },
        required: ["path"]
      },
      handler: async (params) => {
        // 先记录审计日志
        await logAudit("read_file", params);
        // 再调用内置的 read_file（通过内置工具 API）
        return await originalReadFile(params.path);
      }
    }
  ]
});
```

**覆盖内置工具的注意事项**：

1. 确保新实现的行为与用户预期一致——如果 LLM 期望 `read_file` 返回文件内容，你也应该返回文件内容
2. 不要改变工具的输入输出 Schema——LLM 学会了怎么调用原版，突然改格式会导致调用失败
3. 覆盖前先思考：是真的需要改行为，还是添加一个不同名称的新工具就够了？

## Plugin Hook 点体系

### Hook 执行模型

Hook 是 Plugin 的核心机制。可以把 Hook 想象成"事件监听器"——Agent 执行到某个阶段时，触发一个事件，所有注册了这个事件的 Plugin 依次执行。

```mermaid
flowchart LR
    subgraph Agent_Pipeline["Agent 执行工作流"]
        S[Session 创建]
        UK[用户输入到达]
        TOOL_B[工具调用前]
        TOOL_A[工具调用后]
        LLM_REQ[LLM 请求前]
        LLM_RESP[LLM 响应后]
        CMD_B[Command 执行前]
        CMD_A[Command 执行后]
        PERM[权限检查]
        S_END[Session 结束]
    end

    subgraph Hook_Pipeline["Hook 链式执行"]
        direction TB
        H1[Hook 1: Plugin A]
        H2[Hook 2: Plugin B]
        H3[Hook 3: Plugin C]
        H1 --> H2 --> H3
    end

    S -->|"session:start"| H1
    UK -->|"message:before"| H1
    TOOL_B -->|"tool:before"| H1
    TOOL_A -->|"tool:after"| H1
    LLM_REQ -->|"llm:before"| H1
    LLM_RESP -->|"llm:after"| H1
    CMD_B -->|"command:before"| H1
    CMD_A -->|"command:after"| H1
    PERM -->|"permission:check"| H1
    S_END -->|"session:end"| H1

    style Agent_Pipeline fill:#e3f2fd
    style Hook_Pipeline fill:#fff3e0
    style H1 fill:#50C878,color:#fff
    style H2 fill:#50C878,color:#fff
    style H3 fill:#50C878,color:#fff
```

每个 Hook 的返回值可以修改传递到下一个 Hook 的参数，形成 **Pipeline 模式**——上一个 Hook 的输出是下一个 Hook 的输入。这使得多个 Plugin 可以串联协作。

### OpenCode 内置 20+ Hook 点

| Hook 名称 | 触发时机 | 参数 | 典型用途 |
|-----------|---------|------|---------|
| `session:start` | Session 创建时 | `session` 对象 | 初始化资源、加载配置 |
| `session:end` | Session 结束时 | `session` 对象 | 清理资源、发送摘要 |
| `message:before` | 消息处理前 | `message` 内容 | 内容过滤、注入检测 |
| `message:after` | 消息处理后 | `response` 内容 | 结果后处理 |
| `tool:before` | 工具调用前 | `tool, params` | 审计、权限检查 |
| `tool:after` | 工具调用后 | `tool, result, duration` | 结果验证、缓存 |
| `command:before` | Command 执行前 | `command, args` | 指令拦截、修改 |
| `command:after` | Command 执行后 | `command, result` | 指令日志 |
| `permission:check` | 权限校验时 | `action, resource` | 自定义权限规则 |
| `file:beforeRead` | 文件读取前 | `filePath` | 敏感文件拦截 |
| `file:afterRead` | 文件读取后 | `filePath, content` | 内容过滤 |
| `file:beforeWrite` | 文件写入前 | `filePath, content` | 内容安全审查 |
| `file:afterWrite` | 文件写入后 | `filePath` | 文件变更通知 |
| `llm:before` | LLM 请求前 | `messages, options` | Prompt 注入、修改 |
| `llm:after` | LLM 响应后 | `response` | 响应校验、格式化 |
| `agent:before` | Agent 切换前 | `from, to` | 切换逻辑 |
| `agent:after` | Agent 切换后 | `agent` | 切换通知 |
| `hook:error` | Hook 异常时 | `hook, error` | 错误处理与恢复 |
| `context:assemble` | 上下文组装时 | `context` 对象 | 注入额外信息 |
| `provider:before` | Provider 请求前 | `provider, request` | 请求修改 |

### OMO 扩展 Hook 点（53+）

在 OMO 开源版本中，Hook 体系被大幅扩展，覆盖工作流执行的每个阶段：

| Hook 名称 | 触发时机 | 说明 |
|-----------|---------|------|
| `onWorkflowStart` | 工作流开始 | 工作流级预处理 |
| `onWorkflowEnd` | 工作流结束 | 工作流级后处理 |
| `onAgentSelect` | Agent 选择 | 自定义 Agent 路由 |
| `onContextAssemble` | 上下文组装 | 注入团队知识库 |
| `onLLMRequest` | LLM 请求 | 自定义 Prompt 模板 |
| `onLLMResponse` | LLM 响应 | 响应解析与校验 |
| `onToolCall` | 工具调用 | 集中的 Tool 调度 |
| `onQualityGate` | 质量门禁 | 自定义质量检查 |
| `onSkillLoad` | Skill 加载 | Skill 预处理 |
| `onPermissionCheck` | 权限校验 | 细粒度权限控制 |

### Pipeline 模式详解

Pipeline 的核心价值在于 **多个 Plugin 可以有序协作**。例如在文件写入场景中：

```mermaid
flowchart TB
    subgraph Pipeline["Plugin Pipeline: 文件写入"]
        direction TB
        P1[Plugin: Env Guard<br/>检查敏感信息]
        P2[Plugin: Audit Logger<br/>记录操作日志]
        P3[Plugin: Format Check<br/>检查代码格式]
        P4[Plugin: Commit Prep<br/>准备提交信息]
    end

    WRITE[Agent 发起文件写入] --> P1
    P1 -->|通过| P2
    P2 -->|通过| P3
    P3 -->|通过| P4
    P4 -->|通过| DONE[文件写入完成]
    P1 -->|拒绝| BLOCKED[操作被阻止]
    P2 -->|拒绝| BLOCKED
    P3 -->|拒绝| BLOCKED

    style WRITE fill:#e3f2fd
    style P1 fill:#e74c3c,color:#fff
    style P2 fill:#f39c12,color:#fff
    style P3 fill:#3498db,color:#fff
    style P4 fill:#2ecc71,color:#fff
    style DONE fill:#e8f5e9
    style BLOCKED fill:#ffebee
```

每个 Hook 的返回值中的 `skip` 或 `modify` 字段可以终止或修改 Pipeline 的执行。

## 完整示例：Env Guard Plugin

Env Guard 是一个防止敏感信息泄露的安全守卫 Plugin。它拦截文件读写操作，检测内容中的敏感信息模式，并根据策略执行遮蔽、拒绝或审计。

### 完整实现

```typescript:plugins/env-guard/index.ts
// plugins/env-guard/index.ts
import { definePlugin } from "opencode";

// 敏感信息检测模式
const SENSITIVE_PATTERNS = [
  {
    name: "AWS Access Key",
    pattern: /AKIA[0-9A-Z]{16}/g,
    severity: "critical"
  },
  {
    name: "AWS Secret Key",
    pattern: /(?<![A-Za-z0-9+\/=])[A-Za-z0-9+\/=]{40}(?![A-Za-z0-9+\/=])/g,
    severity: "critical"
  },
  {
    name: "Private Key",
    pattern: /-----BEGIN (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----[\s\S]*?-----END (RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----/g,
    severity: "critical"
  },
  {
    name: "GitHub Token",
    pattern: /gh[pousr]_[A-Za-z0-9_]{36,}/g,
    severity: "high"
  },
  {
    name: "OpenAI API Key",
    pattern: /sk-[A-Za-z0-9]{32,}/g,
    severity: "high"
  },
  {
    name: "Generic API Key",
    pattern: /(['"](?:api[_-]?key|apikey|secret|token)['"]\s*:\s*['"])(?!\{env:)[A-Za-z0-9_\-]{16,}['"]/gi,
    severity: "medium"
  },
  {
    name: "Connection String",
    pattern: /(?:postgres|mysql|mongodb|redis|amqp):\/\/[^:]+:[^@]+@/g,
    severity: "high"
  }
];

type Policy = "mask" | "reject" | "audit";

const POLICY: Record<string, Policy> = {
  "critical": "reject",
  "high": "mask",
  "medium": "audit"
};

function checkContent(content: string, filePath: string) {
  const findings: Array<{ name: string; severity: string; matches: string[]; policy: Policy }> = [];

  for (const rule of SENSITIVE_PATTERNS) {
    const matches = content.match(rule.pattern);
    if (matches) {
      const policy = POLICY[rule.severity] || "audit";
      findings.push({
        name: rule.name,
        severity: rule.severity,
        matches,
        policy
      });
    }
  }

  return findings;
}

function maskContent(content: string): string {
  let masked = content;
  for (const rule of SENSITIVE_PATTERNS) {
    masked = masked.replace(rule.pattern, (match) => {
      // 保留首尾 4 个字符，中间用 **** 替代
      if (match.length <= 8) return "****";
      return match.slice(0, 4) + "****" + match.slice(-4);
    });
  }
  return masked;
}

export default definePlugin({
  name: "env-guard",
  description: "敏感信息泄露防护守卫",

  hooks: {
    "file:beforeRead": async ({ filePath }) => {
      // 对 .env 和 secrets 目录的文件读取发出警告
      if (filePath.includes(".env") || filePath.includes("/secrets/")) {
        return {
          warning: `正在读取敏感文件: ${filePath}，请确认意图`,
          proceed: true  // 允许继续但记录
        };
      }
    },

    "file:afterRead": async ({ filePath, content }) => {
      const findings = checkContent(content, filePath);
      if (findings.length > 0) {
        console.warn(`[Env Guard] 文件 ${filePath} 包含 ${findings.length} 个敏感信息`);
        findings.forEach(f => {
          console.warn(`  [${f.severity}] ${f.name}: ${f.policy} 策略`);
        });
      }
    },

    "file:beforeWrite": async ({ filePath, content }) => {
      const findings = checkContent(content, filePath);

      for (const finding of findings) {
        switch (finding.policy) {
          case "reject":
            return {
              reject: true,
              reason: `检测到 ${finding.severity} 级别敏感信息: ${finding.name}。` +
                      `请在环境变量或 Secret Store 中存储，不要硬编码到文件中。`
            };

          case "mask":
            return {
              modify: true,
              content: maskContent(content),
              warning: `已自动遮蔽 ${finding.name} (${finding.matches.length} 处)`
            };

          case "audit":
            console.warn(`[Env Guard 审计] 文件 ${filePath} 包含 ${finding.name}`);
            break;
        }
      }
    },

    "tool:before": async ({ tool, params }) => {
      if (tool === "execute_command") {
        const cmd = params.command || "";
        // 检查命令中是否包含明文密钥
        for (const rule of SENSITIVE_PATTERNS) {
          if (rule.pattern.test(cmd)) {
            return {
              reject: true,
              reason: `命令中包含 ${rule.name}，请使用环境变量替代。`
            };
          }
        }
      }
    },

    "permission:check": async ({ action, resource }) => {
      // 自定义权限规则：阻止对包含敏感信息的文件进行编辑
      if (action === "edit" && /\.(env|pem|key|secret)$/i.test(resource)) {
        return { allow: false, reason: "Env Guard 阻止了敏感文件的编辑操作" };
      }
    }
  }
});
```

### 注册 Env Guard

```json:opencode.json
{
  "plugin": {
    "env-guard": {
      "path": "./plugins/env-guard/index.ts",
      "enabled": true,
      "config": {
        "policies": {
          "critical": "reject",
          "high": "mask",
          "medium": "audit"
        },
        "exclude_paths": ["**/test/**", "**/mock/**"]
      }
    }
  }
}
```

### 验证 Env Guard

开启 Env Guard 后，尝试在文件中写入 AWS Key：

```typescript:example.ts
// Agent 会尝试写这个文件
const awsConfig = {
  accessKeyId: "AKIAIOSFODNN7EXAMPLE"  // 会被 Env Guard 拦截
};
```

结果：Agent 的操作被拒绝，并提示使用环境变量。

```
✗ Env Guard: 检测到 critical 级别敏感信息: AWS Access Key
  请在环境变量或 Secret Store 中存储，不要硬编码到文件中。
```

### 三种处理策略对比

| 策略 | 行为 | 适用场景 |
|------|------|---------|
| **mask** | 遮蔽敏感内容，保留其他部分继续执行 | 测试数据、演示代码 |
| **reject** | 拒绝操作，返回错误原因 | 生产代码、CI/CD 流程 |
| **audit** | 允许操作，但记录审计日志 | 调试期、白名单场景 |

## Plugin 部署和管理

### 安装方式

```json:opencode.json
{
  "plugin": {
    "my-plugin": {
      "path": "./plugins/my-plugin/index.ts",
      "enabled": true
    }
  }
}
```

Plugin 路径可以是：
- **本地文件**：`./plugins/my-plugin/index.ts`
- **npm 包**：`opencode-plugin-sentry`
- **远程 URL**：`https://plugins.company.com/my-plugin.js`

### 启用/禁用

```bash
# 临时禁用 Plugin（在 opencode.json 中设置 enabled: false）
# 或通过 /command 动态切换

/plugin disable env-guard
/plugin enable env-guard
/plugin list  # 查看所有 Plugin 状态
```

### 版本管理

Plugin 作为 npm 包发布时，遵循 Semantic Versioning：

```json:opencode.json
{
  "plugin": {
    "sentry-integration": {
      "path": "opencode-plugin-sentry@^2.1.0",
      "enabled": true
    }
  }
}
```

### 日志调试

```bash
# 查看 Plugin 日志（使用 OpenCode 的日志系统）
opencode --log-level debug

# 日志输出示例
# [Plugin] 加载 env-guard (./plugins/env-guard/index.ts)
# [Plugin] 注册 5 个 Hook 点
# [Plugin] Hook file:beforeWrite 触发
# [Plugin] 检测到 AWS Access Key，执行 reject 策略
```

### Plugin 开发规范

1. **命名**：使用 kebab-case，不超过 50 字符
2. **体积**：单文件 Plugin 建议不超过 200 行，过于复杂的拆分为模块
3. **错误处理**：所有 Hook 必须用 try-catch 包裹，异常会被 `hook:error` 捕获
4. **性能**：避免在 Hook 中执行耗时操作（如同步网络请求），异步操作使用 `await`
5. **依赖声明**：在 `package.json` 中声明所有依赖

```json:package.json
{
  "name": "opencode-plugin-env-guard",
  "version": "1.0.0",
  "description": "敏感信息泄露防护守卫",
  "main": "dist/index.js",
  "opencode": {
    "plugin": true,
    "min_version": "2.0.0",
    "hooks": ["file:beforeRead", "file:afterRead", "file:beforeWrite", "tool:before", "permission:check"]
  },
  "dependencies": {
    "opencode": "^2.0.0"
  }
}
```

## 验证标准

完成本文学习后，你应该能：

1. 在 `opencode.json` 或独立的 `agent.json` 中定义一个自定义 Agent，指定角色、模型、Skill、权限和温度，并通过 Tab 切换或 `/agent` 命令使用
2. 使用 `definePlugin` API 创建一个 Plugin，包含至少 2 个自定义 Tool，并在自定义 Agent 中调用
3. 至少使用 5 个 Hook 点（如 `file:beforeRead`、`file:beforeWrite`、`tool:before`、`permission:check`、`session:start`）拦截和修改 Agent 行为
4. 实现一个 Env Guard 级别的安全 Plugin，覆盖 3 种处理策略（mask / reject / audit）
5. 解释 Plugin Tool、MCP Tool 和 Built-in Tool 之间的优先级关系，并能通过同名覆盖扩展内置工具
6. 在 opencode.json 中正确注册 Plugin，并能通过 `/plugin` 命令进行启用、禁用和查看状态
