# 2026-06-06: 修复 OpenCode GitHub 登录认证问题

> [TAG: agile-coach]

## 基本信息

| 项目 | 内容 |
|------|------|
| Session ID | ses_... |
| 问题类型 | OpenCode 启动时 GitHub 认证卡住 |
| 风险等级 | 中 |
| 主模型 | deepseek-v4-flash-free |

## 1. 问题描述（输入）

### 1.1 原始问题
OpenCode 启动时自动弹出 GitHub 登录窗口，用户完成浏览器认证后，OpenCode 仍然卡在 "please complete authentication in your browser..." 状态，无法完成登录流程。

### 1.2 环境信息
- **操作系统**: Windows
- **OpenCode 版本**: 1.16.2
- **安装方式**: npm 全局安装
- **当前认证状态**: 仅配置了 OpenCode Zen API Key，未配置 GitHub Copilot

## 2. 诊断过程

### 2.1 检查本机 OpenCode 安装

| 项目 | 结果 |
|------|------|
| 安装路径 | `C:\Users\Administrator\AppData\Roaming\npm\opencode` |
| 版本 | 1.16.2 |
| 启动器 | `opencode.ps1` (npm 全局安装) |

### 2.2 检查认证状态存储

| 项目 | 结果 |
|------|------|
| 数据目录 | `C:\Users\Administrator\.local\share\opencode\` |
| `auth.json` | 存在，仅包含 OpenCode Zen API Key |
| `account.json` | 存在，版本 v2，已激活一个 OpenCode 账户 |
| GitHub 认证 | **未找到任何 GitHub 认证信息** |

**关键发现**: 当前 `auth.json` 中只配置了 OpenCode Zen 的 API Key，没有任何 GitHub 相关的 OAuth Token 或 Device Code 认证记录。

### 2.3 检查系统环境

| 项目 | 结果 |
|------|------|
| HTTP_PROXY / HTTPS_PROXY 环境变量 | 未设置 |
| Windows 注册表代理 | ProxyEnable=0，但 ProxyServer 被配置为 `http://proxy.lfk.qianxin-inc.cn:3128` |
| 防火墙规则 | 未找到针对 opencode 的专用规则 |

**注意**: 系统中残留了奇安信（Qianxin）的企业代理配置。

### 2.4 网络连通性测试

| 目标 | 结果 |
|------|------|
| `https://github.com/login/device` | HTTP/1.1 302 Found ✅ |
| `https://api.github.com` | HTTP/1.1 200 OK ✅ |

**结论**: 本机到 GitHub 的网络连通性正常，无网络阻断问题。

### 2.5 进程和端口检查

| 项目 | 结果 |
|------|------|
| opencode 进程 | PID 17400 正在运行 ✅ |
| Node.js 进程 | 4 个 node 进程在运行 ✅ |
| 本地监听端口 (3000/5000/8000/8080/9000) | **无相关端口监听** ❌ |

## 3. 根因分析

### 3.1 直接原因
**当前 OpenCode 并未配置任何 GitHub 认证凭据**，系统中只存在 OpenCode Zen 的 API Key 认证。这不是"认证失败"，而是"尚未进行 GitHub 认证"。

### 3.2 认证流程分析

根据调研，OpenCode 的 GitHub Copilot 认证使用 **OAuth 2.0 Device Flow** 或 **本地 HTTP 回调** 机制：

1. **Device Flow**: 生成 device code，用户访问 `https://github.com/login/device` 输入代码授权
2. **OAuth 回调**: 启动本地 HTTP 服务（如 `http://127.0.0.1:51121`），等待浏览器回调携带 code 参数

### 3.3 可能的问题场景

1. **从未执行 GitHub 登录**: 用户可能只配置了 OpenCode Zen 的 API Key，没有运行过 `opencode auth login github-copilot`
2. **Device Flow 未完成**: 如果之前尝试登录，可能在浏览器端未完成授权，或 Device Code 已过期（默认 15 分钟）
3. **回调端口被占用**: 本地 HTTP 回调端口（如 51121）被其他进程占用
4. **企业代理干扰**: 系统中残留的企业代理配置可能干扰 OAuth 回调

## 4. 修复方案

### 4.1 方案一：使用 Device Flow 重新认证（推荐）

```bash
# 清除可能存在的旧认证数据
rm ~/.local/share/opencode/auth.json

# 重新执行 GitHub Copilot 认证
opencode auth login -p github-copilot

# 选择 GitHub.com (Public) 或 GitHub Enterprise
# 按提示在浏览器中完成授权
```

### 4.2 方案二：检查并释放回调端口

如果 Device Flow 卡住，可能是本地回调端口被占用：

```powershell
# Windows: 查找占用端口的进程
netstat -ano | findstr :51121

# 结束占用端口的进程
taskkill /PID <PID> /F

# 重新认证
opencode auth login -p github-copilot
```

### 4.3 方案三：禁用代理后认证

```powershell
# 临时禁用代理
$env:HTTP_PROXY = ""
$env:HTTPS_PROXY = ""

# 重新认证
opencode auth login -p github-copilot
```

### 4.4 方案四：使用 Personal Access Token（备用）

如果 OAuth 流程始终无法完成，可以使用 GitHub Personal Access Token：

1. 访问 https://github.com/settings/tokens?type=beta
2. 创建 Fine-grained PAT，授予 Copilot 相关权限
3. 配置到 OpenCode：

```json
// ~/.config/opencode/copilot-quota-token.json
{
  "token": "github_pat_xxx...",
  "username": "你的用户名"
}
```

## 5. 验证结果

### 5.1 当前状态确认
- OpenCode 版本 1.16.2 运行正常
- OpenCode Zen API Key 认证有效
- 可正常使用 OpenCode Zen 提供的模型（如 deepseek-v4-flash-free, big-pickle 等）

### 5.2 可用模型列表
当前通过 OpenCode Zen 可使用的模型包括：
- `opencode/deepseek-v4-flash-free`
- `opencode/big-pickle`
- `opencode/nemotron-3-super-free`
- `opencode/mimo-v2.5-free`
- 以及 Claude、GPT、Gemini 等系列模型

## 6. 经验教训与改进建议

### 6.1 诊断经验
| # | 经验 | 说明 |
|---|------|------|
| 1 | **先查认证状态** | 遇到认证问题首先检查 `auth.json`，确认是否已配置相关凭据 |
| 2 | **区分"未认证"和"认证失败"** | 本案例是未配置 GitHub 认证，不是认证流程失败 |
| 3 | **检查代理配置** | Windows 注册表中的残留代理配置可能干扰 OAuth 回调 |
| 4 | **端口占用排查** | OAuth 回调需要本地端口，被占用会导致认证卡住 |

### 6.2 预防措施
1. 首次安装 OpenCode 时，明确选择需要使用的 Provider
2. 如果使用 GitHub Copilot，确保在 `opencode auth login` 时选择 `github-copilot`
3. 企业网络环境下，注意代理配置对 OAuth 流程的影响

### 6.3 后续建议
- 如果用户确实需要使用 GitHub Copilot，建议按照"方案一"重新执行认证流程
- 如果认证流程仍然卡住，可尝试"方案二"释放端口或"方案三"禁用代理
- 作为备用，可使用"方案四"的 Personal Access Token 方式

## 附录

### A.1 关键文件路径

| 文件 | 路径 |
|------|------|
| OpenCode 可执行文件 | `C:\Users\Administrator\AppData\Roaming\npm\opencode` |
| 认证文件 `auth.json` | `C:\Users\Administrator\.local\share\opencode\auth.json` |
| 账户文件 `account.json` | `C:\Users\Administrator\.local\share\opencode\account.json` |
| 配置文件目录 | `C:\Users\Administrator\.config\opencode\` |
| 日志目录 | `C:\Users\Administrator\.local\share\opencode\log\` |

### A.2 常用诊断命令

```bash
# 查看版本
opencode --version

# 查看已配置的认证
opencode auth list

# 启用调试日志
opencode --log-level DEBUG --print-logs

# 查看日志文件
ls -lt ~/.local/share/opencode/log/ | head
```

---

> **协调人**: Sisyphus
> **日期**: 2026-06-06
> **核心教训**: 区分"未认证"和"认证失败"，先查状态再诊断流程
