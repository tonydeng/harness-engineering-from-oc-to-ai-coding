# 5分钟快速体验

> 在深入阅读之前，先动手感受 OpenCode 的核心工作流。5分钟内完成安装、初始化、启动和验证，体验 AI 编程工程化的第一步。

---

## 前置条件

在开始之前，请确保你的环境满足以下要求：

| 工具 | 版本要求 | 验证命令 | 说明 |
|------|---------|---------|------|
| **Node.js** | >= 18 | `node --version` | OpenCode 运行环境 |
| **Python** | >= 3.10 | `python --version` | 可选，部分 Skill 需要 |
| **Git** | >= 2.x | `git --version` | 版本控制基础 |

```bash
# 一键验证所有前置条件
node --version && python --version && git --version
```

**预期输出**：

```
v18.x.x (或更高)
Python 3.10.x (或更高)
git version 2.x.x (或更高)
```

> **提示**：如果缺少 Node.js，推荐使用 [nvm](https://github.com/nvm-sh/nvm)（macOS/Linux）或 [nvm-windows](https://github.com/coreybutler/nvm-windows)（Windows）安装。

---

## 步骤一：安装 OpenCode

### macOS / Linux

```bash
# 使用 npm 全局安装
npm install -g @opencode-ai/opencode

# 或使用官方脚本（推荐）
curl -fsSL https://opencode.ai/install | bash
```

### Windows

```powershell
# 使用 npm 全局安装
npm install -g opencode-ai

# 或使用 Scoop（推荐）
scoop install opencode

# 或使用 Chocolatey
choco install opencode
```

### 验证安装

```bash
opencode --version
```

**预期输出**：

```
OpenCode v1.15.x
```

> **故障排查**：
> - **`command not found`**：确认 Node.js >= 18 已正确安装，并检查 npm 全局路径是否在 `PATH` 中。macOS/Linux 可运行 `echo $PATH` 确认 `/usr/local/bin` 或 `~/.npm-global/bin` 在路径中
> - **`EACCES: permission denied`**：npm 全局安装权限不足时，建议使用 nvm 管理 Node.js 版本（`nvm install --lts`），避免使用 `sudo npm install`
> - **`node --version` 版本过低**：使用 nvm（推荐）安装 Node.js 18+：`nvm install 18` 或 `nvm install --lts`
> - **`git not found`**：从 [git-scm.com](https://git-scm.com/) 下载安装，或 macOS 使用 `brew install git`

---

## 步骤二：初始化项目

### 创建测试项目

```bash
# 创建一个测试目录
mkdir opencode-demo && cd opencode-demo

# 初始化 Git 仓库（OpenCode 依赖 Git）
git init
```

### 运行 /init 命令

```bash
# 启动 OpenCode（首次启动会引导配置 Provider）
opencode

# 在 OpenCode 交互界面中执行
/init
```

**预期输出**：

```
✓ Created .opencode/AGENTS.md
✓ Created .opencode/config.json
✓ Project initialized successfully

Next steps:
1. Review .opencode/AGENTS.md for project context
2. Configure your AI provider (see .opencode/config.json)
3. Start your first task with /plan or /build
```

### 理解初始化产物

| 文件 | 作用 | 是否必须 |
|------|------|---------|
| `.opencode/AGENTS.md` | 项目上下文文件，告诉 AI 项目的技术栈、规范和约束 | ✓ 必须 |
| `.opencode/config.json` | OpenCode 配置文件，包含 Provider、权限、模型设置 | ✓ 必须 |
| `.opencodeignore` | 排除敏感目录（类似 `.gitignore`） | 可选 |

> **关键概念**：`.opencode/AGENTS.md` 是项目的"出生证明"，它定义了 AI 在这个项目中应该如何工作。后续章节会深入讲解如何编写高质量的 AGENTS.md。

---

## 步骤三：启动第一个 Session

### 配置 Provider（首次启动）

OpenCode 支持三种 Provider 接入方式：

| 方式 | 适合场景 | 配置难度 |
|------|---------|---------|
| **OpenCode Zen** | 新用户快速体验，无需 API Key | ⭐ 最简单 |
| **自有 API Key** | 已有 Anthropic/OpenAI/Gemini 账号 | ⭐⭐ 中等 |
| **GitHub Copilot** | 已订阅 Copilot 的用户 | ⭐⭐ 中等 |

**推荐新用户选择 OpenCode Zen**（首次启动会自动引导）。

### 执行第一个任务

在 OpenCode 交互界面中：

```
# 进入 Plan 模式（规划任务）
/plan

# 提问
帮我创建一个简单的 Python HTTP 服务器，监听 8080 端口，返回 "Hello OpenCode"

# 确认计划后，切换到 Build 模式执行
/build
```

**预期输出**：

```
[Plan Mode] Creating plan...
1. Create server.py with HTTP server code
2. Add requirements.txt (if needed)
3. Test the server

[Build Mode] Executing plan...
✓ Created server.py
✓ Server ready to run: python server.py

Test command: curl http://localhost:8080
```

### 验证结果

```bash
# 在另一个终端窗口中测试
python server.py &

# 测试 HTTP 服务
curl http://localhost:8080
```

**预期输出**：

```
Hello OpenCode
```

---

## 步骤四：验证核心功能

### 测试 /undo 回滚

```bash
# 在 OpenCode 中执行
/undo

# 查看文件是否恢复
cat server.py
```

**预期输出**：

```
File restored to previous state.
```

### 测试 /diff 查看变更

```bash
# 重新执行任务
/build

# 查看变更
/diff
```

**预期输出**：

```diff
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

### 常用命令速查

| 命令 | 作用 | 使用场景 |
|------|------|---------|
| `/help` | 查看帮助 | 忘记命令时 |
| `/plan` | 规划模式 | 复杂任务先规划再执行 |
| `/build` | 执行模式 | 直接执行任务 |
| `/undo` | 回滚操作 | 执行错误时恢复 |
| `/redo` | 重做操作 | 回滚后重新执行 |
| `/diff` | 查看变更 | 检查 AI 修改了什么 |
| `/share` | 分享 Session | 导出对话记录 |
| `/models` | 查看可用模型 | 切换 AI 模型 |

---

## 安全检查（重要）

### 权限控制

OpenCode 默认会询问敏感操作权限。首次使用建议：

```json:.opencode/config.json
{
  "permissions": {
    "edit": "ask",
    "bash": "ask"
  }
}
```

### 排除敏感目录

```bash
# 创建 .opencodeignore
cat > .opencodeignore << 'EOF'
.env
*.key
*.pem
secrets/
credentials/
EOF
```

> **安全原则**：永远不要让 AI 自动修改生产环境代码或执行危险命令。`ask` 权限模式是 Harness Engineering 的第一道防线。

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
| **效率开发者** | → [Agent 编排](../02-core-concepts/agent-orchestration.md) — 掌握高级工作流 |
| **技术负责人** | → [OpenCode 配置详解](../03-setup/opencode-config.md) — 深入配置和安全策略 |
| **Skill 作者** | → [Skill 系统](../02-core-concepts/skills-system.md) — 开始 Skill 开发 |

### 深入学习

- **配置详解**：[OpenCode 配置详解](../03-setup/opencode-config.md) — Provider、权限、模型高级配置
- **安全实践**：[安全总览](../06-advanced/security-overview.md) — 企业级安全策略
- **案例研究**：[从零搭建微服务](../07-case-studies/real-world-01.md) — 真实项目实战

---

> [下一页：多角色阅读路径 →](reading-paths.md)
