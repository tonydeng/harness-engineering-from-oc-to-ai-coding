# Skills 系统参考

> OpenCode Skills 系统的完整技术参考文档，涵盖内置 Skills、配置结构、MCP 集成和加载机制。
> 维护者：当 Skills 系统更新或新增内置 Skill 时，请同步更新本文档。

---

## 第一节：内置 Skills 清单

OpenCode 提供一组内置 Skills，覆盖常见的开发场景：

| Skill | 功能 | 典型用途 |
|-------|------|----------|
| `playwright` | 浏览器自动化测试 | E2E 测试、页面交互自动化 |
| `playwright-cli` | Playwright 命令行工具 | 测试脚本执行、调试 |
| `agent-browser` | Agent 浏览器控制 | AI 驱动的网页操作 |
| `dev-browser` | 开发浏览器工具 | 开发调试、页面检查 |
| `git-master` | Git 操作增强 | 复杂 Git 操作、冲突解决 |
| `frontend-ui-ux` | 前端 UI/UX 开发 | 界面设计、用户体验优化 |

### 内置 Skills 调用方式

```bash
# 直接调用内置 Skill
opencode --skill playwright "测试登录流程"

# 在 AGENTS.md 中配置默认 Skill
skills:
  - git-master
  - frontend-ui-ux
```

---

## 第二节：Skills 配置结构

### 完整配置模板

```yaml
# SKILL.md - Skill 定义文件

name: my-skill
description: 自定义技能描述，清晰说明 Skill 的用途和能力边界
template: |
  你是 {skill_name} 专家...
  
  ## 任务
  {task}
  
  ## 输出要求
  - 格式规范
  - 完整性检查

model: custom/model          # 可选：指定使用的模型
agent: custom-agent          # 可选：指定 Agent 类型
subtask: true                # 可选：是否作为子任务运行
argument-hint: 使用提示      # 可选：参数提示信息
license: MIT                 # 可选：许可证
compatibility: ">= 3.0.0"    # 可选：兼容性要求

metadata:
  author: Your Name
  version: 1.0.0
  tags: [automation, testing]

allowed-tools:
  - read
  - bash
  - write
  - grep
```

### 配置字段详解

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `name` | string | 是 | Skill 唯一标识符，kebab-case 格式 |
| `description` | string | 是 | 功能描述，用于 Skill 选择界面 |
| `template` | string | 是 | 提示词模板，支持变量插值 |
| `model` | string | 否 | 指定模型，如 `openai/gpt-4` |
| `agent` | string | 否 | 指定 Agent 类型，如 `planner` |
| `subtask` | boolean | 否 | 是否作为子任务运行，默认 `false` |
| `argument-hint` | string | 否 | 参数使用提示 |
| `license` | string | 否 | 许可证类型 |
| `compatibility` | string | 否 | 版本兼容性要求 |
| `metadata` | object | 否 | 元数据（作者、版本、标签等） |
| `allowed-tools` | array | 否 | 允许使用的工具列表 |

### 模板变量

Skill 模板支持以下内置变量：

| 变量 | 说明 | 示例 |
|------|------|------|
| `{skill_name}` | Skill 名称 | `my-skill` |
| `{task}` | 用户输入的任务 | `实现用户登录功能` |
| `{context}` | 当前上下文 | 文件内容、对话历史 |
| `{workspace}` | 工作目录路径 | `/home/user/project` |

---

## 第三节：Skills 与 MCP 集成

### 集成架构

Skill 可嵌入 MCP（Model Context Protocol）服务器，实现与外部工具的无缝对接：

```
┌─────────────────────────────────────────────────────┐
│                    OpenCode Agent                    │
├─────────────────────────────────────────────────────┤
│  ┌─────────────┐    ┌─────────────┐                │
│  │    Skill    │───▶│ MCP Client  │                │
│  └─────────────┘    └──────┬──────┘                │
│                            │                        │
│                     ┌──────▼──────┐                │
│                     │ MCP Server  │                │
│                     │ (External)  │                │
│                     └─────────────┘                │
└─────────────────────────────────────────────────────┘
```

### 会话隔离机制

使用复合键模式隔离不同会话的 MCP 状态：

```
${sessionID}:${skillName}:${serverName}
```

**示例**：

```
# 会话 A 的 Skill 实例
sess-abc123:my-skill:database-server

# 会话 B 的 Skill 实例（完全隔离）
sess-def456:my-skill:database-server
```

### 防止跨会话污染

1. **状态隔离**：每个会话拥有独立的 MCP 连接池
2. **资源清理**：会话结束时自动释放 MCP 资源
3. **权限边界**：Skill 只能访问其声明的 MCP 服务器

### MCP 配置示例

```yaml
# opencode.json 中的 MCP 配置
{
  "mcpServers": {
    "database": {
      "command": "uvx",
      "args": ["mcp-server-postgres"],
      "env": {
        "DATABASE_URL": "postgresql://localhost/mydb"
      }
    }
  }
}
```

---

## 第四节：Skills 加载优先级

Skills 按以下优先级顺序加载（高优先级覆盖低优先级）：

```
project > opencode > user > builtin
```

### 优先级详解

| 优先级 | 位置 | 路径示例 | 说明 |
|--------|------|----------|------|
| 1 (最高) | project | `.opencode/skills/my-skill/` | 项目级 Skill，覆盖全局配置 |
| 2 | opencode | `~/.opencode/skills/my-skill/` | OpenCode 全局 Skill |
| 3 | user | `~/.config/opencode/skills/` | 用户自定义 Skill |
| 4 (最低) | builtin | OpenCode 内置 | 系统内置 Skill |

### 加载流程

```
1. 扫描 .opencode/skills/ (project)
   └─ 找到 my-skill → 加载并停止

2. 未找到 → 扫描 ~/.opencode/skills/ (opencode)
   └─ 找到 my-skill → 加载并停止

3. 未找到 → 扫描 ~/.config/opencode/skills/ (user)
   └─ 找到 my-skill → 加载并停止

4. 未找到 → 使用内置 builtin Skills
```

### 覆盖示例

假设存在以下 Skill 定义：

```
# 项目级 Skill（优先级最高）
.opencode/skills/git-master/SKILL.md

# 用户级 Skill
~/.config/opencode/skills/git-master/SKILL.md

# 内置 Skill
OpenCode 内置的 git-master
```

**结果**：项目级 Skill 覆盖用户级和内置 Skill。

---

## 第五节：Skill 开发最佳实践

### 命名规范

- 使用 kebab-case：`my-skill`（非 `mySkill` 或 `my_skill`）
- 语义化命名：`security-audit`、`api-generator`
- 避免与内置 Skill 重名（除非有意覆盖）

### 模板设计原则

1. **清晰的职责边界**：一个 Skill 只做一件事
2. **完整的上下文说明**：模板中包含必要的背景信息
3. **结构化输出要求**：明确输出格式和验收标准
4. **错误处理指导**：包含异常情况的处理方式

### 工具权限最小化

```yaml
# 推荐：只声明必需的工具
allowed-tools:
  - read
  - grep

# 避免：过度授权
allowed-tools:
  - read
  - write
  - bash
  - delete  # 危险操作
```

### 版本兼容性声明

```yaml
# 明确兼容性要求
compatibility: ">= 3.0.0 < 4.0.0"

# 使用特定功能时声明依赖
metadata:
  requires:
    - mcp-server-postgres >= 1.2.0
```

---

## 第六节：常见问题

### Q: 如何调试 Skill？

```bash
# 启用详细日志
opencode --skill my-skill --verbose "测试任务"

# 检查 Skill 加载路径
opencode --skill my-skill --debug-path
```

### Q: Skill 与 Plugin 的区别？

| 特性 | Skill | Plugin |
|------|-------|--------|
| 主要用途 | 封装领域知识 | 扩展系统能力 |
| 配置方式 | SKILL.md | 代码实现 |
| 触发方式 | 显式调用 | Hook 事件 |
| 状态管理 | 无状态 | 可有状态 |

### Q: 如何共享 Skill？

1. **团队共享**：放入项目 `.opencode/skills/` 目录
2. **社区共享**：发布到 Skills Marketplace（OMO）
3. **个人复用**：放入 `~/.config/opencode/skills/`

---

> 维护者注：此文档应在以下情况更新：
> - OpenCode 发布新版本，新增或修改内置 Skills
> - Skills 配置结构发生变化
> - MCP 集成机制更新
> - 加载优先级规则调整
>
> 最后更新：2026-06-02 | 初始版本 — 基于 OpenCode Skills 系统规范创建
