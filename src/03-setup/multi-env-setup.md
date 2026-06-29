# 多环境部署方案

> 开发、CI/CD、生产环境的配置分离与 **Agent（智能体）** 配置最佳实践。
>
> **本文适用于团队负责人和 DevOps 工程师。如果只是个人使用 OpenCode，可以暂时跳过本章。**

> **前置条件**
> - 已完成 [快速上手](quickstart.md) 的基础配置，OpenCode 可正常运行
> - 已了解 [OpenCode 配置深度解析](opencode-config.md) 中 `opencode.json` 的基本结构
> - 本节目标：为开发、CI/CD、生产三套环境配置独立的 Agent 和权限策略

## 文章概述

个人开发者在笔记本上跑 OpenCode 和团队在生产环境中运行 OpenCode 是两回事。不同环境对模型选择、权限级别、Token 预算、安全策略有完全不同的需求。本地开发可能用低成本模型加高权限，CI/CD 需要低权限加快速模型，生产环境则要求严格权限控制和高 Token 预算。读完本文，你将能够为开发、CI/CD、生产三套环境创建完整的 Agent 配置模板，并实现团队级配置治理与 Secret Store 集成。

OpenCode 的配置系统通过 **Agent 配置**和**Provider 配置**灵活地解决了这个问题。你可以定义全局默认配置，然后为不同的 Agent（如 `build`, `plan`, `code-reviewer`）配置不同的模型和权限设置。这篇文章从 Agent 配置的灵活特性出发，给出本地开发、CI/CD、生产环境三套完整模板，并讨论团队级 Git 管理的配置治理、Secret Store 集成和多环境测试策略。

> **注意**: OpenCode 使用 provider/model ID 格式标识模型（如 `anthropic/claude-opus-4-7`），具体映射请参考 [OpenCode 官方文档的模型支持列表](https://opencode.ai/docs/models/)。

> **⏱ 时间有限？先读这些：** Agent 配置详解 → 三套环境完整模板 → Secret 管理最佳实践 → 团队级配置管理

## 多环境部署的挑战

### 环境差异的本质

在 AI 辅助编程的工程实践中，不同环境面临截然不同的约束条件：

| 维度 | 本地开发 | CI/CD 流水线 | 生产环境 |
|------|---------|-------------|---------|
| **模型选择** | 低成本、快速响应 | 快速模型、确定性输出 | 高质量、高 Token 预算 |
| **权限级别** | 高权限（开发者可控） | 低权限（自动化执行） | 严格限制（审计合规） |
| **Token 预算** | 灵活、可超支 | 固定预算、快速失败 | 高预算、成本可控 |
| **安全策略** | 开发者自决 | 最小权限原则 | 零信任、审计日志 |
| **失败容忍** | 高（可手动干预） | 低（阻塞流水线） | 极低（影响业务） |

### 配置泄漏的风险

多环境配置管理最危险的陷阱是**敏感信息泄漏**。生产环境的 API Key、数据库凭证、签名密钥一旦提交到版本控制，即使后续删除也会永久留在 Git 历史中。常见的泄漏路径包括：

1. **硬编码凭证**：将 API Key 直接写入 `opencode.json`
2. **环境混淆**：开发环境配置意外部署到生产
3. **日志泄露**：调试信息中包含敏感参数
4. **依赖供应链**：第三方 **Skill（技能）** 或 **Plugin（插件）** 窃取配置

### 配置管理的工程目标

一个成熟的多环境配置方案应该实现：

- **配置即代码**：所有非敏感配置纳入版本控制，可审计、可复现
- **环境隔离**：不同环境使用不同的凭证和权限边界
- **Agent 配置复用**：公共配置只定义一次，各 Agent 复用
- **安全注入**：敏感信息通过 Secret Store 或环境变量注入，永不落盘

## Agent 配置详解

### Agent 配置结构

OpenCode 的配置系统通过 `agent` 字段配置不同 Agent 的行为。Agent 配置支持：

1. **模型选择**：指定 Agent 使用的模型
2. **权限控制**：配置 Agent 的工具权限（edit, bash, glob 等）
3. **自定义提示**：为特定 Agent 设置系统提示词
4. **环境特定配置**：针对不同场景配置不同的 Agent 行为

OpenCode 内置的 Agent 包括：

- `build` - 主要构建 Agent（mode: primary）
- `plan` - 规划 Agent（mode: primary）
- `general` - 通用 Agent（mode: subagent）
- `explore` - 代码探索 Agent（mode: subagent）
- 用户自定义 Agent

下文示例中的 `code-reviewer` 是一个自定义 Agent 示例。

### Agent 配置示例

下面展示一个完整的开发环境 Agent 配置示例。

```json:opencode.json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "build": {
      "mode": "primary",
      "model": "anthropic/claude-sonnet-4-6",
      "prompt": "You are a helpful coding assistant focused on building software.",
      "permission": {
        "edit": "ask",
        "bash": "ask",
        "glob": "allow"
      }
    },
    "plan": {
      "model": "anthropic/claude-haiku-4",
      "permission": {
        "edit": "deny",
        "bash": "deny"
      }
    },
    "code-reviewer": {
      "model": "anthropic/claude-sonnet-4-6",
      "mode": "subagent",
      "permission": {
        "edit": "deny"
      }
    }
  },
  "provider": {
    "anthropic": {
      "options": {
        "apiKey": "{env:ANTHROPIC_API_KEY}"
      }
    }
  }
```

**Agent 配置设计原则**：

- 定义不同 Agent 的角色和权限
- 通过环境变量注入敏感信息
- 使用 wildcard 模式配置工具权限

**注意**: OpenCode 使用环境变量插值 `{env:ENV_VAR}` 来注入敏感信息，避免硬编码。

### 权限控制详解

```json:opencode.json
{
  "agent": {
    "build": {
      "permission": {
        "edit": "ask",
        "bash": "ask",
        "glob": "allow",
        "read": "allow"
      }
    },
    "production": {
      "permission": {
        "edit": "deny",
        "bash": "deny",
        "glob": "deny"
      }
    }
  }
}
```

**权限配置要点**：

- `ask`: 每次操作需要用户确认
- `allow`: 自动执行，无需确认
- `deny`: 禁止操作

Wildcard 模式支持通配符匹配工具名称，如 `"npm *": "allow"` 允许所有 npm 命令。

### 模型配置

```json:opencode.json
{
  "provider": {
    "anthropic": {
      "options": {
        "apiKey": "{env:ANTHROPIC_API_KEY}"
      }
    },
    "openai": {
      "options": {
        "apiKey": "{env:OPENAI_API_KEY}"
      }
    },
    "google": {
      "options": {
        "apiKey": "{env:GOOGLE_API_KEY}"
      }
    }
  },
  "agent": {
    "build": {
      "model": "anthropic/claude-sonnet-4-6"
    }
  }
}
```

**模型配置要点**：

- 使用 `provider/model_id` 格式
- 通过环境变量管理 API Key
- 支持多提供者配置

## 三套环境完整模板

### 本地开发环境

本地开发环境追求**开发效率**和**成本控制**的平衡。

```json:opencode.json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "build": {
      "mode": "primary",
      "model": "anthropic/claude-sonnet-4-6",
      "permission": {
        "edit": "ask",
        "bash": "ask",
        "glob": "allow",
        "read": "allow"
      }
    }
  },
  "provider": {
    "anthropic": {
      "options": {
        "apiKey": "{env:ANTHROPIC_API_KEY}"
      }
    }
  },
  "compaction": {
    "auto": true,
    "prune": false,
    "reserved": 10000
  }
}
```

**配置解读**：

- **模型选择**: `anthropic/claude-sonnet-4-6` 提供良好的质量和速度平衡
- **权限策略**: 编辑和命令执行需要确认 (`ask`)
- **上下文压缩**: 开启自动压缩（`auto: true`），不启用 Prune（`prune: false`）

### CI/CD 流水线环境

CI/CD 环境追求**确定性**和**安全边界**。

```yaml:.github/workflows/opencode-ci.yml
# .github/workflows/opencode-ci.yml
name: OpenCode CI

on: [push, pull_request]

jobs:
  opencode:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Run OpenCode
        env:
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
        run: |
          OPENCODE_PERMISSION='{"edit": "deny", "bash": "deny"}' \
          opencode --model anthropic/claude-sonnet-4-6 \
            "Analyze this code and suggest improvements"
```

**配置解读**：

- **权限策略**: 只读权限，禁止编辑和命令执行
- **确定性输出**: 使用稳定的模型配置
- **安全边界**: 通过环境变量注入 API Key，不提交到仓库

**注意事项**:

- OpenCode **不支持** `--profile` 参数
- 在 CI 中应使用完全指定的命令行参数
- 通过 GitHub Secrets 管理 API Key

### 生产环境

生产环境追求**安全性**和**可审计性**。

```json:opencode.json
{
  "$schema": "https://opencode.ai/config.json",
  "agent": {
    "build": {
      "mode": "primary",
      "model": "anthropic/claude-opus-4-7",
      "permission": {
        "edit": "deny",
        "bash": "deny",
        "glob": "deny"
      }
    }
  },
  "provider": {
    "anthropic": {
      "options": {
        "apiKey": "{env:ANTHROPIC_API_KEY}"
      }
    }
  }
}
```

**配置解读**：

- **零信任权限**: 默认拒绝所有编辑和命令操作
- **高质量模型**: 使用最高质量的 `claude-opus-4-7`
- **日志记录**: 通过 CLI 的 `--log-level` 参数控制日志级别（DEBUG/INFO/WARN/ERROR）

## Secret 管理最佳实践

### 方案一：环境变量（推荐入门）

最简单的 Secret 管理方式是使用环境变量。OpenCode 支持通过环境变量注入配置：

```bash:terminal
# Anthropic API Key
export ANTHROPIC_API_KEY="sk-ant-..."

# OpenAI API Key
export OPENAI_API_KEY="sk-..."

# Google Gemini API Key
export GOOGLE_API_KEY="..."
```

OpenCode 配置文件中使用 `{env:ENV_VAR}` 插值：

```json:opencode.json
{
  "provider": {
    "anthropic": {
      "options": {
        "apiKey": "{env:ANTHROPIC_API_KEY}"
      }
    }
  }
}
```

**优点**: 简单直接，无需额外工具  
**缺点**: 环境变量可能被进程列表泄露，不适合生产环境

### 方案二：.env 文件（推荐本地开发）

使用 `.env` 文件管理本地开发的 Secret：

```bash:terminal
# .env - 不要提交到 Git！
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
LOG_LEVEL=debug
```

**务必将 `.env` 添加到 `.gitignore`**：

```text:terminal
# .gitignore
.env
.env.local
.env.*.local
```

OpenCode 会自动读取配置文件中的环境变量插值。

### 方案三：Secret Store（推荐企业）

企业环境应使用专业的 Secret Store：

**HashiCorp Vault**:

```bash:terminal
# 从 Vault 读取 API Key
export ANTHROPIC_API_KEY=$(vault kv get -field=api_key secret/opencode/anthropic)
```

**AWS Secrets Manager**:

```bash:terminal
# 使用 AWS CLI 读取
export ANTHROPIC_API_KEY=$(aws secretsmanager get-secret-value \
  --secret-id opencode/anthropic-api-key \
  --query SecretString --output text)
```

### 安全检查清单

在部署多环境配置前，请确认：

- [ ] API Key 未硬编码在 `opencode.json` 中
- [ ] `.env` 文件已添加到 `.gitignore`
- [ ] 生产环境使用 Secret Store 而非环境变量
- [ ] 不同环境使用不同的 API Key
- [ ] API Key 定期轮换（建议 90 天）
- [ ] 有 API Key 泄露的应急响应流程

## 团队级配置管理

### Git 管理的配置治理

将 `opencode.json` 纳入版本控制，实现配置即代码：

```text:terminal
project/
├── opencode.json          # 项目级配置（提交到 Git）
├── .env.example           # 环境变量模板（提交到 Git）
├── .env                   # 实际环境变量（不提交）
└── .gitignore             # 排除 .env
```

**配置审查流程**：

1. 开发者创建配置变更 PR
2. 自动化检查：JSON 格式验证
3. 代码审查：安全架构师审核权限变更
4. 合并后自动部署到各环境

### 多环境配置策略

使用不同的配置文件管理不同环境：

```text:terminal
config/
├── dev.json              # 开发环境配置
├── ci.json               # CI/CD 配置
└── production.json       # 生产环境配置
```

通过 `OPENCODE_CONFIG` 环境变量指定配置路径：

```bash:terminal
# 开发环境
export OPENCODE_CONFIG="./config/dev.json"
opencode

# CI 环境
export OPENCODE_CONFIG="./config/ci.json"
opencode
```

## 关联章节

- ← [OpenCode 配置深度解析](opencode-config.md) — Agent 配置基础
- → [性能调优与成本管理](../06-advanced/context/performance-tuning.md) — 环境相关的成本管控配置
- → [工作流实战](../04-workflows/) — 不同环境使用不同的工作流模式

---

## 参考资料

- [OpenCode Config Documentation](https://opencode.ai/docs/config/)
- [OpenCode CLI Reference](https://opencode.ai/docs/cli/)
- [OpenCode Agents Reference](https://opencode.ai/docs/agents/)
- [OpenCode Providers Reference](https://opencode.ai/docs/providers/)
