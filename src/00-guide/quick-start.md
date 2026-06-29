# 5分钟快速体验

> 在深入阅读之前，先动手感受 OpenCode 的核心工作流。5分钟内完成安装、初始化、启动和验证，体验 AI 编程工程化的第一步。

---

读完本文，你将在 5 分钟内完成 OpenCode 的安装、初始化和首次 AI 编程体验。

> **⏱ 时间有限？先读这些：** 安装 → 初始化配置 → 运行第一个任务 → 验证安装 → 下一步

## 前置条件

在开始之前，请确保你的环境满足以下要求：

| 工具 | 版本要求 | 验证命令 | 说明 |
|------|---------|---------|------|
| **Node.js** | >= 18 | `node --version` | npm 安装方式所需（curl/brew 安装不需要） |
| **Python** | >= 3.10 | `python --version` | 可选，部分 **Skill（技能）** 需要 |
| **Git** | >= 2.x | `git --version` | 版本控制基础 |

```bash:terminal
# 一键验证所有前置条件
node --version && python --version && git --version
```

**预期输出**：

```text:terminal
v22.x.x (或更高)
Python 3.11.x (或更高)
git version 2.x.x (或更高)
```

> **提示**：如果缺少 Node.js，推荐使用 [nvm](https://github.com/nvm-sh/nvm)（macOS/Linux）或 [nvm-windows](https://github.com/coreybutler/nvm-windows)（Windows）安装。

---

## 步骤一：安装 OpenCode

### macOS / Linux

```bash:terminal
# 使用 Homebrew（推荐，macOS）
brew install anomalyco/tap/opencode

# 或使用 npm 全局安装
npm install -g opencode-ai

# 或使用官方脚本
curl -fsSL https://opencode.ai/install | bash
```

### Windows

```powershell:terminal
# 使用 npm 全局安装
npm install -g opencode-ai

# 或使用 Scoop（推荐）
scoop install opencode

# 或使用 Chocolatey
choco install opencode
```

### 验证安装

```bash:terminal
opencode --version
```

**预期输出**：

```text:terminal
OpenCode v1.17.11
```

> **故障排查**：
> - **`command not found`**：确认 Node.js >= 18 已正确安装，并检查 npm 全局路径是否在 `PATH` 中。macOS/Linux 可运行 `echo $PATH` 确认 `/usr/local/bin` 或 `~/.npm-global/bin` 在路径中
> - **`EACCES: permission denied`**：npm 全局安装权限不足时，建议使用 nvm 管理 Node.js 版本（`nvm install --lts`），避免使用 `sudo npm install`
> - **`node --version` 版本过低**：使用 nvm（推荐）安装 Node.js 18+：`nvm install 18` 或 `nvm install --lts`
> - **`git not found`**：从 [git-scm.com](https://git-scm.com/) 下载安装，或 macOS 使用 `brew install git`

---

## 步骤二：初始化项目

### 创建测试项目

```bash:terminal
# 创建一个测试目录
mkdir opencode-demo && cd opencode-demo

# 初始化 Git 仓库（OpenCode 依赖 Git）
git init
```

### 启动 OpenCode

```bash:terminal
# 启动 OpenCode TUI 界面
opencode

# 首次启动需要配置 Provider
# 编辑 ~/.config/opencode/opencode.json 添加 API 配置
```

### 第一个任务

在 TUI 界面中：

1. **输入任务描述**：
   ```
   帮我创建一个简单的 Python HTTP 服务器，监听 8080 端口，返回 "Hello OpenCode"
   ```

2. **按 Tab 键切换 Plan/Build 模式**：
   - Plan 模式：让 AI 生成执行计划
   - Build 模式：直接执行任务

3. **使用 @ 引用文件**：
   - 输入 `@` 按 Tab 可以看到可用文件列表
   - 可用于引用现有代码文件作为上下文

---

> **安全检查**：首次使用前，建议先设置敏感操作权限为 `ask` 模式（见下方安全说明），避免 AI 自动执行危险命令。完整安全策略见 → [安全总览](../06-advanced/security-overview.md)。

## 步骤三：启动第一个 Session

### 配置 Provider（首次启动）

OpenCode 支持多种 AI 模型 Provider，通过编辑 `~/.config/opencode/opencode.json` 配置：

| Provider | 适合场景 | 配置难度 |
|----------|----------|----------|
| **自有 API Key** | 已有 Anthropic/OpenAI/Gemini 账号 | ⭐⭐ 中等 |

**配置步骤**：
1. 编辑 `~/.config/opencode/opencode.json`
2. 添加 Provider 配置（参考文档配置章节）
3. 重启 OpenCode 生效

### 执行第一个任务

在 TUI 界面中：

```text:terminal
1. 输入任务描述
   帮我创建一个简单的 Python HTTP 服务器，监听 8080 端口，返回 "Hello OpenCode"

2. 按 Tab 键切换 Plan/Build 模式
   - Plan 模式：生成执行计划
   - Build 模式：直接执行任务

3. 确认执行
   查看生成的计划或代码，按 Enter 确认执行
```

**预期输出**：

```text:terminal
✓ Created server.py
✓ Server ready to run: python server.py

Test command: curl http://localhost:8080
```

### 验证结果

```bash:terminal
# 在另一个终端窗口中测试
python server.py &

# 测试 HTTP 服务
curl http://localhost:8080
```

**预期输出**：

```text:terminal
Hello OpenCode
```

---

## 步骤四：验证核心功能

### 验证核心功能

OpenCode 的核心特性：

- **文件快照**：自动保存文件变更历史，可回溯修改
- **Tab 切换模式**：Plan 模式（规划）↔ Build 模式（执行）
- **@ 文件引用**：按 Tab 可查看可用文件并引用作为上下文

**预期输出**：

```text:terminal
File restored to previous state.
```

### 测试 /diff 查看变更

```bash:terminal
# 重新执行任务
/build

# 查看变更
/diff
```

**预期输出**：

```diff:terminal
--- /dev/null
+++ b/server.py
@@ -0,0 +1,10 @@
+from http.server import HTTPServer, BaseHTTPRequestHandler
+
+class HelloHandler(BaseHTTPRequestHandler):
+    def do_GET(self):
+        self.send_response(200)
+        self.send_header('Content-type', 'text/plain')
+        self.end_headers()
+        self.wfile.write(b'Hello OpenCode')
+
+if __name__ == '__main__':
+    server = HTTPServer(('', 8080), HelloHandler)
+    print('Server running on port 8080...')
+    server.serve_forever()
```

### 常用操作

| 操作 | 说明 | 使用场景 |
|------|------|----------|
| **Tab** | 切换模式/查看文件列表 | Plan↔Build 模式切换，@ 引用文件 |
| **@** | 引用文件 | 按 Tab 查看可用文件并引用 |
| **CLI** | 命令行操作 | `opencode run [message]` 运行任务 |
| **~/.config/opencode/** | 配置文件目录 | 编辑 `opencode.json` 配置 Provider |

---

## 安全检查（重要）

### 权限控制

OpenCode 默认会询问敏感操作权限。首次使用建议：

```json:opencode.json
{
  "permission": {
    "*": "ask"
  }
}
```

### 排除敏感目录

```bash:terminal
# 创建 .opencodeignore
cat > .opencodeignore << 'EOF'
.env
*.key
*.pem
secrets/
credentials/
EOF
```

> **安全原则**：永远不要让 AI 自动修改生产环境代码或执行危险命令。`ask` 权限模式是 **Harness Engineering（驾驭工程）** 的第一道防线。

---

## 下一步

恭喜你完成了 OpenCode 的第一次实践！现在你已经掌握了：

- ✓ OpenCode 的安装和验证
- ✓ 项目初始化和 AGENTS.md 的作用
- ✓ Plan/Build 模式的基本工作流
- ✓ /undo、/diff 等核心命令
- ✓ 基本的安全权限控制

### 推荐阅读路径

| 你的角色 | 下一步 |
|---------|--------|
| **入门开发者** | → [什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md) — 理解核心理念 |
| **效率开发者** | → [**Agent（智能体）** 编排](../02-core-concepts/agent-orchestration.md) — 掌握高级工作流 |
| **技术负责人** | → [OpenCode 配置深度解析](../03-setup/opencode-config.md) — 深入配置和安全策略 |
| **Skill 作者** | → [Skill 系统](../02-core-concepts/skills-system.md) — 开始 Skill 开发 |

### 深入学习

- **配置详解**：[OpenCode 配置深度解析](../03-setup/opencode-config.md) — Provider、权限、模型高级配置
- **安全实践**：[安全总览](../06-advanced/security-overview.md) — 企业级安全策略
- **案例研究**：[从零搭建微服务](../07-case-studies/real-world-01.md) — 真实项目实战

---

> [下一页：多角色阅读路径 →](reading-paths.md)
