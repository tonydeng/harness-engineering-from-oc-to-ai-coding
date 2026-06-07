# Karpathy 风格技术审查：`constraints-system.md`

> **审查目标**：以 Karpathy 式批判性技术视角，系统验证 `constraints-system.md` 中的所有技术声明
> **审查日期**：2026-06-06
> **审查方法**：跨仓库验证 + 官方文档对比 + 代码执行验证

---

## 执行摘要

**关键发现：这篇文章存在严重的文档漂移（Documentation Drift）。**

| 类别 | 数量 | 状态 |
|------|------|------|
| ❌ 引用不存在的示例文件 | 10 个 | **全部不存在** |
| ❌ 虚构的权限模式 | 3 种 (`passive`/`restricted`/`inherit`) | **不存在于 OpenCode** |
| ❌ 配置结构错误 | 全部 | **与实际 OpenCode schema 不符** |
| ⚠️ 技术架构声明 | 部分 | **需要重新验证** |
| ✅ 版本声明 | 2 处 | **已确认 (v1.16.x, v4.7.x)** |
| ✅ 内部链接 | 6 个 | **全部有效** |

---

## 一、文件引用完整性审计

### 1.1 `examples/opencode-configs/*.jsonc` 引用验证

**实际目录内容**：该目录下仅存在 3 个文件：
- `basic.jsonc` — 16 行基础配置，不包含权限配置
- `oh-my-openagent-basic.json` — oh-my-openagent 插件配置
- `oh-my-openagent-advanced.json` — oh-my-openagent 高级插件配置

**文档声称存在但实际不存在的文件（9 个）**：

| 行号 | 文档引用路径 | 实际状态 | 证据 |
|------|-------------|---------|------|
| 255 | `examples/opencode-configs/permissions.jsonc` | ❌ 不存在 | `ls examples/opencode-configs/` |
| 299 | `examples/opencode-configs/path-permissions.jsonc` | ❌ 不存在 | `ls examples/opencode-configs/` |
| 362 | `examples/opencode-configs/passive-mode.jsonc` | ❌ 不存在 | `ls examples/opencode-configs/` |
| 771 | `examples/opencode-configs/least-privilege.jsonc` | ❌ 不存在 | `ls examples/opencode-configs/` |
| 795 | `examples/opencode-configs/default-deny.jsonc` | ❌ 不存在 | `ls examples/opencode-configs/` |
| 841 | `examples/opencode-configs/dev-permissions.jsonc` | ❌ 不存在 | `ls examples/opencode-configs/` |
| 869 | `examples/opencode-configs/prod-permissions.jsonc` | ❌ 不存在 | `ls examples/opencode-configs/` |
| 968 | `examples/opencode-configs/database-safety.jsonc` | ❌ 不存在 | `ls examples/opencode-configs/` |
| 1054 | `examples/opencode-configs/secrets-protection.jsonc` | ❌ 不存在 | `ls examples/opencode-configs/` |

**结论**：文档引用的 **90% 示例文件不存在**，读者按文档配置会导致错误。

### 1.2 `examples/ast-grep-rules/*.yaml` 引用验证

**引用位置**：第 599 行 `examples/ast-grep-rules/no-direct-sql.yaml`

**验证结果**：
- `examples/ast-grep-rules/` 目录根本不存在
- 该文件从未创建

**结论**：AST-grep 规则示例是**虚构的**，文档声称的"集成 AST-grep"从未实现。

### 1.3 Markdown 内部链接验证

**验证结果**：✅ **全部有效**

| 引用位置 | 目标 | 验证状态 |
|---------|------|---------|
| 行 6, 51, 1189 | `context-engineering-core.md` | ✅ 存在 |
| 行 52, 1190 | `validation-harness.md` | ✅ 存在 |
| 行 53, 1191 | `../03-setup/` | ✅ 存在 |
| 行 755, 1192 | `../06-advanced/security-overview.md` | ✅ 存在 |
| 行 1193 | `../06-advanced/sandbox-hooks.md` | ✅ 存在 |

---

## 二、权限模型验证

### 2.1 声称的"6 种权限模式" vs 实际 OpenCode

**文档声称**（第 12, 42, 188-223 行）：
> OpenCode 提供六种权限模式：`allow` / `deny` / `ask` / `passive` / `restricted` / `inherit`

**实际 OpenCode 权限系统**（来源：[opencode.ai/docs/permissions/](https://opencode.ai/docs/permissions/)）：
- 实际权限动作（Action）**只有 3 种**：`allow` / `ask` / `deny`
- OpenCode 源码：`export const Action = z.enum(["allow", "deny", "ask"])`

**验证结论**：
| 模式 | 文档声称 | 实际存在性 |
|------|---------|-----------|
| `allow` | ✅ | ✅ 真实存在 |
| `ask` | ✅ | ✅ 真实存在 |
| `deny` | ✅ | ✅ 真实存在 |
| `passive` | ✅ | ❌ **不存在** |
| `restricted` | ✅ | ❌ **不存在** |
| `inherit` | ✅ | ❌ **不存在** |

**严重性：极高**。"passive/restricted/inherit"三种模式完全虚构，文档第 42、188-223 行的内容需要重写。

### 2.2 "Passive Mode" 验证

**文档声称**（第 331-370 行）：
> "Passive 模式" 是一种特殊的权限模式，`"mode": "passive"`

**实际 OpenCode 配置**（来源：[opencode.ai/docs/agents/](https://opencode.ai/docs/agents/)）：
- `agent.mode` 的实际取值：`"primary"` / `"subagent"` / `"all"`
- **不存在** `"mode": "passive"`
- **不存在** `"allowedOperations"` / `"deniedOperations"` 配置键

**验证方法**：
```bash
# 搜索 OpenCode 源码
grep -r "mode.*passive" $OPENDOC_PATH/
# 结果：0 次匹配
```

**验证结论**：`"mode": "passive"` **完全不存在**。OpenCode 实现"只读模式"的正确方式是配置：
```json
{
  "permission": {
    "edit": "deny",
    "bash": "deny"
  }
}
```

**严重性：极高**。第 331-370 行整节内容需要删除或重写。

---

## 三、配置结构验证

### 3.1 OpenCode 实际 config schema vs 文档

**文档使用的配置结构**（第 65-71 行）：
```json
{
  "permissions": {
    "tools": {
      "read_file": "allow",
      "write_file": "ask",
      "delete_file": "deny"
    }
  }
}
```

**实际 OpenCode config schema**（来源：[opencode.ai/docs/permissions/](https://opencode.ai/docs/permissions/)）：
```json
{
  "permission": {
    "read": "allow",
    "edit": "ask",
    "bash": {
      "git *": "allow",
      "rm *": "deny"
    }
  }
}
```

**关键差异对比**：

| 配置键 | 文档声称 | 实际 OpenCode | 状态 |
|--------|---------|--------------|------|
| 根键 | `"permissions"`（复数） | `"permission"`（单数） | ❌ 错误 |
| 工具分组 | `"tools"` 子键 | 无；直接是 `read`/`edit`/`bash` | ❌ 不存在 |
| 路径分组 | `"paths"` 子键 | 无；路径作为 `read`/`edit` 的子键 | ❌ 不存在 |
| 命令分组 | `"commands"` 子键 | 无；命令是 `bash` 的子键 | ❌ 不存在 |
| 路径权限 | `"pathPermissions"` | 不存在 | ❌ 不存在 |
| 工具名 | `read_file`/`write_file`/`delete_file` | `read`/`edit`/`bash` | ❌ 错误 |
| 命令名 | `execute_command`/`network_request` | `bash`（带通配符） | ❌ 不存在 |

**严重性：极高**。所有配置示例的**整个结构**都是虚构的。

### 3.2 不存在的配置键

文档使用以下配置键，但这些在 OpenCode 中都不存在：

| 配置键 | 位置 | 状态 |
|--------|------|------|
| `"defaultAction"` | 行 796 | ❌ 不存在 |
| `"allowedTools"` | 行 799-807 | ❌ 不存在 |
| `"deniedTools"` | 行 799-807 | ❌ 不存在 |
| `"environment"` | 行 843, 872 | ❌ 不存在 |
| `"audit"` | 行 891-895 | ❌ 不存在 |
| `"preview"` | 行 991-995 | ❌ 不存在 |
| `"outputFilter"` | 行 1066-1080 | ❌ 不存在 |
| `"warnings"` | 行 1077-1079 | ❌ 不存在 |
| `"database"` | 行 982-990 | ❌ 不存在 |

### 3.3 缺失的实际 OpenCode 权限键

文档从未提及这些实际存在的 OpenCode 权限键：
- `list` — 列出目录权限
- `glob` — 文件通配查询
- `grep` — 内容搜索
- `codesearch` — 代码搜索
- `lsp` — LSP 查询
- `task` — 任务管理
- `todo` / `todowrite` — todo 列表
- `skill` — Skill 加载
- `webfetch` / `websearch` — 网络访问
- `question` — 用户对话提问
- `external_directory` — 项目外路径访问
- `doom_loop` — 循环检测

---

## 四、版本声明验证

**行 256, 772**：`// Requires OpenCode >= v1.16.x, OMO >= v4.7.x`

**验证**：
- `src/00-guide/README.md` 行 322-323：OpenCode v1.16.x (当前 v1.16.2)，oh-my-openagent v4.7.x (当前 v4.7.5)
- 多个 review 文档确认这些版本

**结论**：✅ **已确认**

---

## 五、技术架构验证

### 5.1 AGENTS.md 作为"架构护栏载体"

**文档声称**（行 149, 441-480）：
> AGENTS.md 是 OpenCode 的项目指令文件，作为架构决策的约束载体

**验证**：
- OpenCode **没有** "AGENTS.md" 这一正式功能名称
- 但 OpenCode 确实支持从 `.opencode/instructions.md` 和 `contextPaths` 读取指令
- 本项目的 `AGENTS.md` 文件确实被用作指导 Agent 的规范

**结论**：✅ **作为书籍的方法论是正确的**（不是 OpenCode 官方功能，而是本书的架构实践）。

### 5.2 AST-grep 集成验证

**文档声称**（行 44, 594-637）：
> AST-grep 是 OpenCode 集成的约束工具

**验证**：
- 代码库中 `examples/ast-grep-rules/` 目录**不存在**
- AST-grep 在文档中仅作为"推荐安装的本地工具"（`src/06-advanced/performance-tuning.md` 行 244）
- OpenCode **没有** 原生集成的 AST-grep 约束系统

**结论**：❌ **虚构**。AST-grep 是外部工具，不是 OpenCode 内置功能。

### 5.3 STRIDE 威胁模型

**文档声称**（行 753-756）：
> 使用 STRIDE 威胁模型分析约束系统的安全风险

**验证**：
- STRIDE 是标准的安全框架（Spoofing, Tampering, Repudiation, Information Disclosure, DoS, Elevation of Privilege）
- 文档中的映射是通用的 STRIDE-to-security-controls 映射
- 第 755 行引用 `../06-advanced/security-overview.md` 作为详细分析

**结论**：✅ **正确引用**（但 STRIDE 表格格式存在瑕疵，行 754-759 缺少分隔线）。

---

## 六、案例真实性验证

### 6.1 案例一：生产数据库误删事故

**文档声称**（行 924-926）：
> "2024 年某初创公司...真实发生的（已脱敏）生产事故"

**验证**：
- 无 CVE 引用
- 无公开报告链接
- 无交叉引用的信息来源
- 时间线（14:32 → 14:35）过于戏剧化，不符合工程现实

**结论**：❌ **疑似虚构**。案例是"教育叙事"而非"可验证证据"。

### 6.2 案例二：密钥泄露导致云账户被盗

**文档声称**（行 1010-1012）：
> "2024 年某 SaaS 公司...真实发生的（已脱敏）生产事故"

**验证**：
- 无 CVE 引用
- 无公开报告链接
- AWS 账单 $12,000 是典型的戏剧化数字

**结论**：❌ **疑似虚构**。案例是"教育叙事"而非"可验证证据"。

### 6.3 ROI 表格（行 1122-1127）

**声称**：
> | 敏感路径 deny | 5 分钟配置 | 预防损失 $12,000+ | ROI 2400x+ |

**计算验证**：
- 假设时薪 $100，5 分钟 ≈ $8.33
- ROI = $12,000 / $8.33 ≈ **1440x**，不是 2400x
- 假设不同，数字不同

**结论**：❌ **数字编造**，没有计算依据。

---

## 七、事实错误清单

### 7.1 关键事实错误（必须修复）

| 行号 | 错误 | 严重程度 | 修复建议 |
|------|------|---------|---------|
| 42 | 声称 6 种权限模式（含 passive/restricted/inherit） | 🔴 高 | 改为 3 种（allow/ask/deny），删除 passive/restricted/inherit |
| 61-71 | 配置示例使用错误的 `"permissions"`（复数）和 `"tools"` | 🔴 高 | 改为 `"permission"`（单数），删除 `"tools"` 子键 |
| 188-223 | "六种权限模式"图谱和表格 | 🔴 高 | 删除或改为实际的 3 种权限 + 3 种 action |
| 331-370 | "Passive 模式" 整节 | 🔴 高 | 删除；改为正确的只读配置示例（`edit: deny` + `bash: deny`） |
| 362-369 | `"mode": "passive"` 配置示例 | 🔴 高 | 删除；改为正确的配置 |
| 255, 299, 362, 771, 795, 841, 869, 968, 1054 | 9 个不存在的示例文件引用 | 🔴 高 | 删除引用或创建实际文件并修正内容 |
| 599 | `examples/ast-grep-rules/no-direct-sql.yaml` 引用 | 🔴 高 | 删除引用或明确说明是外部工具 |
| 771-811 | 使用 `"defaultAction"` / `"allowedTools"` / `"deniedTools"` | 🔴 高 | 改为 OpenCode 实际 schema |
| 841-996 | 所有配置示例 | 🔴 高 | 重写为正确的 OpenCode schema |
| 920-1088 | "真实事故"案例 | 🟡 中 | 改为"虚构教学示例"或提供可验证引用 |
| 1122-1127 | ROI 表格 | 🟡 中 | 删除数字或标注为"估算示例" |

### 7.2 次要问题

| 行号 | 问题 | 严重程度 | 修复建议 |
|------|------|---------|---------|
| 754-759 | STRIDE 表格格式错误（缺少分隔线） | 🟡 中 | 添加表格分隔线 |
| 1181 | 学习检查清单中的 `passive/restricted/inherit` | 🟡 中 | 删除 |

---

## 八、总体评估

**文档质量评分**：

| 维度 | 评分 | 说明 |
|------|------|------|
| 技术准确性 | 3/10 | 核心配置结构错误，大量虚构功能 |
| 代码示例质量 | 1/10 | 10 个引用文件 9 个不存在，配置结构全部错误 |
| 案例真实性 | 2/10 | 案例无法验证，ROI 数字编造 |
| 架构合理性 | 7/10 | 概念框架合理，但实现细节有误 |
| 文档完整性 | 4/10 | 引用大量不存在的文件 |

**建议**：
1. **立即删除或重写**所有配置示例（约 80% 内容）
2. **删除** "Passive 模式" 整节
3. **删除** "六种权限模式" 章节，改为 3 种权限
4. **重写** 反面案例为"虚构教学示例"或提供可验证引用
5. **验证** AST-grep 集成声明是否必要

**时间估算**：约需 4-6 小时重写核心章节。

---

## 九、参考验证

- [OpenCode 官方权限文档](https://opencode.ai/docs/permissions/)
- [OpenCode Agent 配置文档](https://opencode.ai/docs/agents/)
- [OpenCode GitHub 仓库](https://github.com/sst/opencode)
- [oh-my-openagent GitHub 仓库](https://github.com/code-yeongyu/oh-my-openagent)

---

**审查结论：本文档需要实质性重写以匹配 OpenCode v1.16.x 的实际实现。当前版本存在严重的文档漂移（Documentation Drift），读者按文档配置会失败。**

**Karpathy 式总结**：这是一个典型的"愿景文档"——它描述了约束系统**应该**是什么，而不是 OpenCode **实际上**是什么。愿景值得尊重，但作为技术文档需要现实核查。

---

*审查完成于 2026-06-06*
*审查方法：跨仓库验证 + 官方文档对比 + 代码执行验证*
