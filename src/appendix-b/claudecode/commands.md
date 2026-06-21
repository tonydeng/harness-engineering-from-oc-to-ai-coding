# Claude Code 命令参考

> Claude Code 内置命令的完整参考手册，按功能分类，方便快速查阅。所有命令在对话输入框中以 `/` 开头输入即可触发。

Claude Code 提供了两大类命令：**Slash 命令**（内置命令 + 捆绑 Skill），在交互式 TUI 中以 `/` 触发；**CLI 命令**（Shell 级别），在终端中直接运行。此外，Claude Code 支持通过 `.claude/commands/` 目录或 `.claude/skills/` 目录创建自定义命令。

→ [Claude Code 内置能力](./capabilities.md) 提供了全貌概览。
→ [Claude Code 扩展机制](./extensions.md) 详细讲解自定义命令和 Skills 系统。

---

## Slash 命令（交互式）

所有 Slash 命令在运行中的 Claude Code 会话内以 `/` 前缀输入。

### 会话管理

| 命令 | 别名 | 功能 | 典型场景 |
|------|------|------|----------|
| `/help` | — | 显示可用命令和快捷键列表 | 不确定命令时查看帮助 |
| `/clear` | `/reset`、`/new` | 新建空白会话，清除当前上下文 | 开始新任务，或上下文混乱时重置 |
| `/compact` | — | 压缩当前上下文，释放 Token 空间 | 上下文接近窗口上限时 |
| `/resume` | `/continue` | 按 ID 或名称恢复历史会话 | 中断工作后继续 |
| `/rename` | — | 重命名当前会话 | 方便后续通过名称恢复 |
| `/branch` | — | 在当前节点创建对话分支 | 尝试不同方向，不丢失原有路径 |
| `/fork` | — | 生成后台子 Agent 继承当前会话 | 并行处理独立子任务 |
| `/rewind` | — | 回滚代码和对话到上一个检查点 | 发现方向错误时快速回退 |
| `/export` | — | 将会话导出为纯文本 | 保存调试记录或分享排查过程 |
| `/copy` | — | 复制最近一次助手回复到剪贴板 | 快速提取生成结果 |
| `/exit` | `/quit` | 退出 CLI | 结束工作 |
| `/btw` | — | 快速旁路提问，不加入对话历史 | 临时查询不打断主任务 |
| `/cd` | — | 切换会话工作目录，保留 Prompt 缓存 | 多项目目录切换 |
| `/add-dir` | — | 添加额外工作目录用于文件访问 | 跨项目文件引用 |
| `/goal` | — | 设置完成条件，Claude 持续工作直到达标 | 长时间自主执行任务 |

**上下文压缩**（Compaction）是长会话管理的关键。`/compact` 会触发 Agent 分析当前对话，生成摘要并保留关键信息，释放 Token 空间。可通过可选参数传递压缩指令。

**分支与分叉**：`/branch` 创建对话分支（类似 Git 分支），适合尝试不同解决方案；`/fork`（v2.1.161+）生成独立后台子 Agent，结果完成后返回主会话。

### 模型与推理控制

| 命令 | 功能 | 典型场景 |
|------|------|----------|
| `/model` | 切换 AI 模型并保存为默认值 | 需要更强推理能力时切换到更强模型 |
| `/effort` | 设置推理深度：low / medium / high / xhigh / max / ultracode | 复杂问题提升推理深度 |
| `/fast` | 切换低延迟快速模式 | 简单任务不需深度推理 |
| `/plan` | 进入规划模式（只读） | 调研代码库、设计方案 |
| `/advisor` | 启用顾问工具，咨询第二个模型给出反馈 | 代码审查、方案评估 |
| `/focus` | 切换焦点视图（仅显示关键信息） | 全屏模式下减少视觉干扰 |

**Effort 级别**控制 Claude 的推理 Token 预算。`ultracode` 级别适合最复杂的架构和调试任务，`low` 级别适合快速代码补全。

### 项目设置与记忆

| 命令 | 功能 | 典型场景 |
|------|------|----------|
| `/init` | 初始化项目，生成 CLAUDE.md | 新项目首次打开 |
| `/memory` | 编辑 CLAUDE.md 记忆文件，管理自动记忆 | 更新项目规则或查看记忆条目 |
| `/config` | 打开设置界面 | 调整权限、主题等配置 |

**`/init`** 是 Claude Code 工程化的起点。执行后会扫描项目结构、识别技术栈、生成 CLAUDE.md 文件。设置 `CLAUDE_CODE_NEW_INIT=1` 环境变量可启用交互式初始化流程。

### 代码审查与质量

| 命令 | 功能 | 典型场景 |
|------|------|----------|
| `/code-review` | 审查分支 diff，检测正确性 Bug 和代码清理 | 提交前代码审查 |
| `/review` | 本地审查 Pull Request | 审查他人代码 |
| `/security-review` | 只读安全审查，检测安全问题 | 安全检查 |
| `/ultrareview` | 云端多 Agent 深度代码审查 | 重要代码变更的深度审查 |
| `/simplify` | 仅清理代码（不检测 Bug），自动应用修改 | 代码重构后的清理 |
| `/diff` | 查看未提交变更的交互式 diff | 提交前确认变更内容 |
| `/commit` | 生成提交信息并创建 Git 提交 | 提交代码 |
| `/commit-push-pr` | 提交、推送并创建 PR | 完整提交流程 |

**`/code-review`** 支持指定审慎级别：`low`、`medium`、`high`、`xhigh`、`max`、`ultra`。`--fix` 参数自动应用修复，`--comment` 参数在 GitHub PR 上发布评论。`ultra` 级别使用云端沙箱进行多 Agent 深度审查。

### 成本与用量

| 命令 | 功能 | 典型场景 |
|------|------|----------|
| `/cost` | 同 `/usage` | 查看当前会话费用 |
| `/usage` | 查看会话费用、用量限额、活动统计 | 监控用量和预算 |
| `/stats` | 同 `/usage` | 查看用量统计 |
| `/context` | 以彩色网格可视化上下文窗口使用情况 | 诊断上下文占用 |
| `/status` | 查看会话信息：模型、版本、账户、连接状态 | 确认当前环境配置 |
| `/insights` | 查看会话模式和瓶颈报告 | 优化工作流程 |

### MCP 与扩展管理

| 命令 | 功能 | 典型场景 |
|------|------|----------|
| `/mcp` | 管理 MCP 服务器连接和 OAuth | 添加或重连外部工具 |
| `/plugin` | 管理插件 | 安装或禁用插件 |
| `/skills` | 列出已安装的 Skills（支持按类型筛选） | 查看可用技能 |
| `/reload-plugins` | 重新加载所有插件 | 安装新插件后激活 |

### Agent 与后台任务

| 命令 | 功能 | 典型场景 |
|------|------|----------|
| `/agents` | 管理 Agent 配置 | 创建或切换自定义 Agent |
| `/tasks` | 列出和管理后台任务 | 监控后台执行进度 |
| `/background` | 将当前会话转为后台 Agent 运行 | 长时间独立执行任务 |
| `/batch` | 将大型变更分解为独立单元并行处理 | 大规模重构 |
| `/loop` | 按时间间隔执行周期性任务 | 定时检查 |
| `/schedule` | 云端定时任务 | 预约定时执行 |

### Git 与 GitHub

| 命令 | 功能 | 典型场景 |
|------|------|----------|
| `/commit` | 生成提交信息并提交 | 快速提交代码 |
| `/commit-push-pr` | 提交、推送并创建 PR | 全自动 PR 流程 |
| `/install-github-app` | 安装 Claude GitHub Actions 应用 | CI/CD 集成 |
| `/autofix-pr` | 启动云端 Agent 监控 PR，CI 失败时自动修复 | 自动化 CI 修复 |

### 配置与设置

| 命令 | 功能 | 典型场景 |
|------|------|----------|
| `/config` | 打开设置界面 | 调整配置 |
| `/permissions` | 管理 allow/ask/deny 权限规则 | 配置工具权限白名单 |
| `/hooks` | 查看工具事件 Hook 配置 | 审计自动化的 Hook 规则 |
| `/theme` | 切换颜色主题 | 个性化界面 |
| `/color` | 设置 Prompt 栏颜色 | 区分不同会话 |
| `/keybindings` | 打开快捷键配置文件 | 自定义快捷键 |
| `/fewer-permission-prompts` | 扫描日志，自动添加白名单减少权限提示 | 优化权限流程 |

### 诊断与帮助

| 命令 | 功能 | 典型场景 |
|------|------|----------|
| `/doctor` | 诊断安装状态，自动修复问题 | 安装后检查 |
| `/debug` | 启用调试日志，排查问题 | 诊断异常行为 |
| `/feedback` | 提交反馈或 Bug 报告 | 报告问题 |
| `/release-notes` | 交互式版本日志查看器 | 查看新版本特性 |

### 远程与会话管理

| 命令 | 功能 | 典型场景 |
|------|------|----------|
| `/desktop` | 切换到 Claude Code 桌面应用继续会话 | 从终端切换到桌面 |
| `/teleport` | 从 claude.ai 恢复远程会话 | 远程办公 |
| `/web` | 设置 Web 版 Claude Code | 浏览器中使用 |
| `/session` | 显示会话 URL 和 QR 码 | 分享会话 |
| `/remote-control` | 连接到 claude.ai/code 远程控制 | 远程控制 |

### 账户与认证

| 命令 | 功能 | 典型场景 |
|------|------|----------|
| `/login` | 登录 Anthropic 账户 | 首次使用或重新登录 |
| `/logout` | 退出登录 | 切换账户 |
| `/upgrade` | 查看升级方案 | Pro/Max 用户升级 |

---

## CLI 命令（Shell 级别）

在终端中直接运行，不在 Claude Code 会话内。

### 会话启动

| 命令 | 说明 | 示例 |
|------|------|------|
| `claude` | 启动交互式会话 | `claude` |
| `claude "query"` | 启动会话并传入初始 Prompt | `claude "解释这个项目"` |
| `claude -p "query"` | 非交互式模式，执行后退出 | `claude -p "解释这个函数"` |
| `claude -c` | 继续最近一次会话 | `claude -c` |
| `claude -r "name" "query"` | 恢复指定会话 | `claude -r "auth-refactor" "完成这个 PR"` |

### 管理命令

| 命令 | 说明 |
|------|------|
| `claude update` | 更新到最新版本 |
| `claude install [version]` | 安装/重装原生二进制 |
| `claude auth login` | 登录（支持 `--email`、`--sso`、`--console`）|
| `claude auth logout` | 退出登录 |
| `claude auth status` | 显示认证状态 |
| `claude project purge [path]` | 删除项目本地状态 |

### 后台会话管理

| 命令 | 说明 |
|------|------|
| `claude agents` | 打开 Agent 视图（监控/调度后台会话）|
| `claude attach <id>` | 连接到后台会话 |
| `claude stop <id>` | 停止后台会话 |
| `claude respawn <id>` | 重新启动后台会话，保留对话 |
| `claude logs <id>` | 查看后台会话日志 |
| `claude daemon status` | 查看后台守护进程状态 |

### MCP 管理

| 命令 | 说明 |
|------|------|
| `claude mcp add <name> <command-or-url>` | 添加 MCP 服务器 |
| `claude mcp remove <name>` | 移除 MCP 服务器 |
| `claude mcp list` | 列出所有已配置服务器 |
| `claude mcp get <name>` | 查看服务器配置详情 |
| `claude mcp serve` | 将 Claude Code 自身作为 MCP 服务器启动 |

### 关键 CLI 标志

| 标志 | 说明 | 示例 |
|------|------|------|
| `-p` / `--print` | 非交互模式 | `claude -p "query"` |
| `-c` / `--continue` | 继续最近会话 | `claude -c` |
| `-r` / `--resume [id]` | 恢复特定会话 | `claude -r abc123` |
| `--model` | 指定模型 | `claude --model claude-opus-4` |
| `--effort` | 推理深度 | `claude --effort high` |
| `--permission-mode` | 权限模式 | `claude --permission-mode plan` |
| `--agent` | 指定 Agent 配置 | `claude --agent my-agent` |
| `--output-format` | 输出格式（text/json/stream-json）| `claude -p "q" --output-format json` |
| `--system-prompt` | 替换默认系统 Prompt | `claude --system-prompt "你是 Python 专家"` |
| `--append-system-prompt` | 追加到系统 Prompt | `claude --append-system-prompt "始终用 TypeScript"` |
| `--allowedTools` | 免除权限提示的工具 | `claude --allowedTools "Read" "Bash(git *)"` |
| `--max-turns` | 限制非交互模式的最大轮次 | `claude -p --max-turns 3 "query"` |
| `--bare` | 最小模式（跳过 hooks/skills/plugins/MCP）| `claude --bare -p "query"` |
| `--bg` | 后台 Agent 模式 | `claude --bg "分析测试失败原因"` |

### 权限模式

| 模式 | 说明 |
|------|------|
| `default` | 标准模式，首次使用工具时提示 |
| `acceptEdits` | 自动接受文件编辑和常用文件系统命令 |
| `plan` | 规划模式，只读，不能修改文件 |
| `auto` | 自动批准，后台安全检查（研究预览）|
| `dontAsk` | 自动拒绝，除非通过 `/permissions` 预批准 |
| `bypassPermissions` | 跳过所有权限提示（仅限沙箱 CI 使用）|

### 键盘快捷键

| 按键 | 功能 |
|------|------|
| `Enter` | 提交消息 |
| `Shift+Enter` | 换行 |
| `Up/Down` | 导航历史消息 |
| `Tab` | 自动补全命令和路径 |
| `Esc`（连按两次）| 取消 / 回滚到检查点 |
| `Shift+Tab` / `Alt+M` | 切换权限模式 |
| `Ctrl+C` | 中断当前工具执行 |
| `Ctrl+R` | 搜索命令历史 |
| `!command` | 内联执行 Shell 命令 |
| `@` | 文件引用 |

---

## 配置参考

### 配置文件层级

| 文件 | 作用域 | 说明 |
|------|--------|------|
| `~/.claude/settings.json` | 全局用户 | 所有项目的个人设置 |
| `.claude/settings.json` | 项目共享 | 团队共享，提交到 Git |
| `.claude/settings.local.json` | 项目本地 | 个人覆盖，Gitignore |
| `.mcp.json` | 项目 MCP | MCP 服务器配置 |
| `~/.claude.json` | 用户状态 | OAuth、MCP、项目状态 |

### 命令配置速查

| 类别 | 数量 | 说明 |
|------|------|------|
| Slash 命令 | ~70+ | 含内置命令和捆绑 Skill |
| CLI 命令 | ~25+ | Shell 级别管理命令 |
| CLI 标志 | ~40+ | 启动选项和配置参数 |
| 键盘快捷键 | ~15+ | 交互式操作快捷键 |
| 权限模式 | 6 | default / acceptEdits / plan / auto / dontAsk / bypassPermissions |

## 相关章节

- → [Claude Code 内置能力](./capabilities.md) — 命令、工具集、配置方式的完整参考
- → [Claude Code 扩展机制](./extensions.md) — Skills、Subagent、Hook、MCP 等扩展体系
- → [Claude Code 生态参考](./ecosystem.md) — 社区项目、最佳实践和集成工作流
- → [OpenCode 内置命令参考](../opencode/commands.md) — OpenCode 命令系统对比参考

> 数据来源：Anthropic 官方文档 code.claude.com/docs。命令列表基于 Claude Code v2.1.x（2026 年 6 月）。
