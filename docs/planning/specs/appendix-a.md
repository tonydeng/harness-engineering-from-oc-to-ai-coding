# Appendix A: 参考资料规格说明

## 1. 概述

附录 A 收录全书的参考资料和辅助内容，为读者提供快速查阅的参考手册。

## 2. 内容架构

### 2.1 现有内容

- **术语表** (glossary.md) — 全书核心术语的完整索引，按拼音字母排序

### 2.2 新增内容

| 文章 | 说明 | 优先级 |
|------|------|--------|
| Built-in Commands Reference（内置命令参考） | OpenCode 所有内置命令的完整参考手册 | P0 |
| Plugin System Reference（Plugin 系统参考） | OpenCode Plugin 系统的完整参考手册 | P0 |

## 3. Built-in Commands Reference 规格

### 3.1 目标读者

所有 OpenCode 用户，特别是需要快速查阅命令用法的开发者。

### 3.2 内容要求

#### 3.2.1 Core Commands（核心命令）

必须包含以下 OpenCode 原生命令：

| Command | 功能 | 分类 |
|---------|------|------|
| `/init` | 生成 AGENTS.md 项目知识库 | 项目初始化 |
| `/undo` | 撤销上一步操作 | 会话管理 |
| `/redo` | 重做撤销的操作 | 会话管理 |
| `/share` | 导出会话 | 会话管理 |
| `/help` | 显示帮助 | 系统 |
| `/new` (alias: `/clear`) | 新建会话 | 会话管理 |
| `/sessions` (aliases: `/resume`, `/continue`) | 会话管理 | 会话管理 |
| `/compact` (alias: `/summarize`) | 上下文压缩 | 上下文管理 |
| `/export` | 导出会话为 Markdown | 会话管理 |
| `/connect` | 添加 LLM Provider | 配置 |
| `/models` | 模型列表 | 配置 |
| `/themes` | 主题切换 | 配置 |
| `/editor` | 编辑器 | 配置 |
| `/details` | 工具详情 | 系统 |
| `/thinking` | 推理显示 | 配置 |
| `/exit` | 退出 | 系统 |

#### 3.2.2 oh-my-openagent Extended Commands（OMO 扩展命令）

必须包含以下 OMO 扩展命令：

| Command | 功能 | 分类 |
|---------|------|------|
| `/ralph-loop` | 自引用开发循环 | 自动化循环 |
| `/ulw-loop` | Ultrawork 模式循环 | 自动化循环 |
| `/cancel-ralph` | 取消活跃的 Ralph Loop | 自动化循环 |
| `/refactor` | 智能重构 | 代码质量 |
| `/start-work` | 从 Prometheus 计划开始工作 | 工作流 |
| `/stop-continuation` | 停止所有续接机制 | 会话管理 |
| `/remove-ai-slops` | 移除 AI 生成的代码异味 | 代码质量 |
| `/handoff` | 创建上下文摘要用于新会话续接 | 会话管理 |
| `/hyperplan` | 对抗性多 Agent 规划 | 工作流 |

#### 3.2.3 Custom Commands（自定义命令）

必须包含：
- 两种创建方式：Markdown 文件（推荐）vs opencode.json 配置
- 模板语法：`$ARGUMENTS`, `!shell`, `@file`
- 高级特性：frontmatter 指定 agent/model，子命令
- 团队共享命令库

### 3.3 格式要求

- 使用 Markdown 表格展示命令列表
- 每个命令包含：名称、功能描述、使用场景、示例
- 使用 `→ [章节名称](相对路径.md)` 格式添加交叉引用
- 代码块使用 `language:path` 格式

## 4. Plugin System Reference 规格

### 4.1 目标读者

需要扩展 OpenCode 功能的高级用户和 Plugin 开发者。

### 4.2 内容要求

#### 4.2.1 Plugin 概述

- 什么是 Plugin
- Plugin vs Skill vs MCP 的区别
- 何时使用 Plugin

#### 4.2.2 Plugin API Reference

- `definePlugin` API
- Plugin 配置选项
- Tool 定义 schema

#### 4.2.3 Hook Points Reference

必须包含所有 20+ 内置 Hook 点：

| Hook Name | 触发时机 | 参数 | 典型用途 |
|-----------|---------|------|---------|
| `session:start` | Session 创建时 | `session` 对象 | 初始化资源 |
| `session:end` | Session 结束时 | `session` 对象 | 清理资源 |
| `message:before` | 消息处理前 | `message` 内容 | 内容过滤 |
| `message:after` | 消息处理后 | `response` 内容 | 结果后处理 |
| `tool:before` | 工具调用前 | `tool, params` | 审计、权限检查 |
| `tool:after` | 工具调用后 | `tool, result, duration` | 结果验证 |
| `command:before` | Command 执行前 | `command, args` | 指令拦截 |
| `command:after` | Command 执行后 | `command, result` | 指令日志 |
| `permission:check` | 权限校验时 | `action, resource` | 自定义权限规则 |
| `file:beforeRead` | 文件读取前 | `filePath` | 敏感文件拦截 |
| `file:afterRead` | 文件读取后 | `filePath, content` | 内容过滤 |
| `file:beforeWrite` | 文件写入前 | `filePath, content` | 内容安全审查 |
| `file:afterWrite` | 文件写入后 | `filePath` | 文件变更通知 |
| `llm:before` | LLM 请求前 | `messages, options` | Prompt 注入 |
| `llm:after` | LLM 响应后 | `response` | 响应校验 |
| `agent:before` | Agent 切换前 | `from, to` | 切换逻辑 |
| `agent:after` | Agent 切换后 | `agent` | 切换通知 |
| `hook:error` | Hook 异常时 | `hook, error` | 错误处理 |
| `context:assemble` | 上下文组装时 | `context` 对象 | 注入额外信息 |
| `provider:before` | Provider 请求前 | `provider, request` | 请求修改 |

#### 4.2.4 OMO Extended Hooks

必须包含 OMO 扩展的 53+ Hook 点列表。

#### 4.2.5 Plugin Configuration

必须包含 opencode.json 配置格式和路径加载规则。

#### 4.2.6 Plugin Management

必须包含管理命令和版本管理。

#### 4.2.7 Security Considerations

必须包含：
- Hook 风险分级
- 权限提升风险
- 安全最佳实践

### 4.3 格式要求

- 使用 Markdown 表格展示 Hook 点列表
- 代码示例使用 TypeScript 格式
- 使用 `→ [章节名称](相对路径.md)` 格式添加交叉引用
- OMO 特性需标注免责声明

## 5. 术语表更新

### 5.1 新增术语

必须在术语表中添加以下术语：

| 术语 | 英文 | 定义 |
|------|------|------|
| 插件 | Plugin | OpenCode 中代码层面的扩展点，通过 Hook 系统拦截和修改 Agent 的行为 |

### 5.2 格式要求

- 按拼音字母排序
- 包含定义、人话解释、首次出现章节
- 添加到术语索引表

## 6. 导航更新

### 6.1 appendix-a/README.md

更新内容导航，添加新文章链接。

### 6.2 src/SUMMARY.md

在附录 A 部分添加新文章条目。

## 7. 验证标准

- [ ] 所有内置命令完整列出
- [ ] 所有 Hook 点完整列出
- [ ] 术语表更新完成
- [ ] 导航更新完成
- [ ] mdbook build 通过
- [ ] 内部链接无 404
