# TechLead 代码审计：`constraints-system.md`

> **审计目标**：验证文档中所有引用、版本声明、配置示例的技术准确性
> **审计日期**：2026-06-06
> **审计方法**：文件系统验证 + 官方文档对比 + 代码结构分析

---

## 一、文件引用审计

### 1.1 实际存在的示例文件

**`examples/opencode-configs/` 目录实际内容**：
```
examples/opencode-configs/
├── basic.jsonc                        ✅ 存在（16 行基础配置）
├── oh-my-openagent-advanced.json     ✅ 存在（插件配置）
└── oh-my-openagent-basic.json        ✅ 存在（插件配置）
```

**总数**：仅 3 个文件，均**不包含**文档引用的权限配置示例。

### 1.2 文档声称存在但实际不存在的文件（10 个）

| 行号 | 引用路径 | 状态 |
|------|---------|------|
| 255 | `examples/opencode-configs/permissions.jsonc` | ❌ 不存在 |
| 299 | `examples/opencode-configs/path-permissions.jsonc` | ❌ 不存在 |
| 362 | `examples/opencode-configs/passive-mode.jsonc` | ❌ 不存在 |
| 771 | `examples/opencode-configs/least-privilege.jsonc` | ❌ 不存在 |
| 795 | `examples/opencode-configs/default-deny.jsonc` | ❌ 不存在 |
| 841 | `examples/opencode-configs/dev-permissions.jsonc` | ❌ 不存在 |
| 869 | `examples/opencode-configs/prod-permissions.jsonc` | ❌ 不存在 |
| 968 | `examples/opencode-configs/database-safety.jsonc` | ❌ 不存在 |
| 1054 | `examples/opencode-configs/secrets-protection.jsonc` | ❌ 不存在 |
| 599 | `examples/ast-grep-rules/no-direct-sql.yaml` | ❌ 不存在 |

**结论**：文档引用的 **90% 示例文件不存在**。

### 1.3 Markdown 内部链接验证

| 引用 | 目标 | 状态 |
|------|------|------|
| 行 6, 51, 1189 | `context-engineering-core.md` | ✅ |
| 行 52, 1190 | `validation-harness.md` | ✅ |
| 行 53, 1191 | `../03-setup/` | ✅ |
| 行 755, 1192 | `../06-advanced/security-overview.md` | ✅ |
| 行 1193 | `../06-advanced/sandbox-hooks.md` | ✅ |

**结论**：所有 Markdown 链接有效。

---

## 二、权限模型验证

### 2.1 文档声称 vs 实际 OpenCode

**文档声称**（行 42, 188-223）：
> OpenCode 提供 6 种权限模式：allow / deny / ask / passive / restricted / inherit

**OpenCode 实际权限系统**：
- 实际只有 **3 种** 权限动作：`allow` / `ask` / `deny`
- OpenCode 源码：`export const Action = z.enum(["allow", "deny", "ask"])`

**验证表**：

| 模式 | 文档 | 实际 | 状态 |
|------|------|------|------|
| allow | ✅ | ✅ | 真实 |
| ask | ✅ | ✅ | 真实 |
| deny | ✅ | ✅ | 真实 |
| passive | ✅ | ❌ | **虚构** |
| restricted | ✅ | ❌ | **虚构** |
| inherit | ✅ | ❌ | **虚构** |

**结论**：`passive` / `restricted` / `inherit` **3 种模式完全不存在**。

### 2.2 "Passive Mode" 验证

**文档声称**（行 331-370）：
> Passive 模式是一种特殊权限模式，配置为 `"mode": "passive"`

**OpenCode 实际配置**：
- `agent.mode` 取值：`"primary"` / `"subagent"` / `"all"`
- **不存在** `"mode": "passive"`
- **不存在** `"allowedOperations"` / `"deniedOperations"`

**正确实现只读模式的方式**：
```json
{
  "permission": {
    "edit": "deny",
    "bash": "deny"
  }
}
```

**结论**：第 331-370 行整节**完全虚构**。

---

## 三、配置结构验证

### 3.1 OpenCode 实际 schema vs 文档

**文档使用的配置**（行 65-71）：
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

**实际 OpenCode schema**：
```json
{
  "permission": {
    "read": "allow",
    "edit": "ask",
    "bash": {
      "git *": "allow"
    }
  }
}
```

### 3.2 关键差异

| 配置键 | 文档 | 实际 | 状态 |
|--------|------|------|------|
| 根键 | `"permissions"`（复数） | `"permission"`（单数） | ❌ 错误 |
| `"tools"` 子键 | 存在 | 不存在 | ❌ 不存在 |
| `"paths"` 子键 | 存在 | 不存在 | ❌ 不存在 |
| `"commands"` 子键 | 存在 | 不存在 | ❌ 不存在 |
| `"pathPermissions"` | 存在 | 不存在 | ❌ 不存在 |
| 工具名 | `read_file` / `write_file` | `read` / `edit` | ❌ 错误 |

### 3.3 不存在的配置键

| 配置键 | 位置 | 状态 |
|--------|------|------|
| `"defaultAction"` | 行 796 | ❌ 不存在 |
| `"allowedTools"` | 行 799 | ❌ 不存在 |
| `"deniedTools"` | 行 807 | ❌ 不存在 |
| `"environment"` | 行 843 | ❌ 不存在 |
| `"audit"` | 行 891 | ❌ 不存在 |
| `"preview"` | 行 991 | ❌ 不存在 |
| `"outputFilter"` | 行 1066 | ❌ 不存在 |
| `"warnings"` | 行 1077 | ❌ 不存在 |
| `"database"` | 行 982 | ❌ 不存在 |

### 3.4 缺失的实际权限键

文档从未提及这些 OpenCode 实际存在的权限：
- `list` — 列出目录
- `glob` — 文件通配
- `grep` — 内容搜索
- `codesearch` — 代码搜索
- `lsp` — LSP 查询
- `task` — 任务管理
- `todo` / `todowrite` — todo 列表
- `skill` — Skill 加载
- `webfetch` / `websearch` — 网络访问
- `question` — 用户对话
- `external_directory` — 外部路径
- `doom_loop` — 循环检测

---

## 四、AST-grep 集成验证

**文档声称**（行 44, 594-637）：
> AST-grep 是 OpenCode 集成的约束工具

**验证**：
- `examples/ast-grep-rules/` 目录**不存在**
- AST-grep 在文档中仅作为"推荐安装的本地工具"
- OpenCode **没有** 原生集成的 AST-grep 约束

**结论**：AST-grep **不是** OpenCode 内置功能，文档声称是虚构的。

---

## 五、版本验证

**行 256, 772**：`// Requires OpenCode >= v1.16.x, OMO >= v4.7.x`

**验证**：
- `src/00-guide/README.md` 行 322-323：OpenCode v1.16.x (当前 v1.16.2)，oh-my-openagent v4.7.x (当前 v4.7.5)
- 多个 review 确认这些版本

**结论**：✅ **正确**

---

## 六、案例真实性验证

### 6.1 生产数据库误删事故（行 920-996）

**问题**：
- 无 CVE 引用
- 无公开报告链接
- 时间线过于戏剧化（14:32 → 14:35）
- "已脱敏"无法验证

**结论**：❌ **疑似虚构的教育叙事**

### 6.2 密钥泄露事故（行 1005-1088）

**问题**：
- 无 CVE 引用
- AWS $12,000 是典型的戏剧化数字
- 时间线过于紧凑（09:15 → 09:30）

**结论**：❌ **疑似虚构**

### 6.3 ROI 表格（行 1122-1127）

**问题**：
- ROI 2400x+ 的计算无依据
- 5 分钟配置成本假设不明

**结论**：❌ **数字编造**

---

## 七、建议修正

### 7.1 必须修复（高优先级）

1. **删除或重写所有配置示例**（行 65-71, 255-279, 299-328, 362-369, 771-1088）
   - 改为 OpenCode 实际 schema
   - 删除不存在的子键

2. **删除 "Passive Mode" 整节**（行 331-370）
   - 改为正确的只读配置说明

3. **删除 "六种权限模式" 章节**（行 188-223）
   - 改为 3 种实际权限（allow/ask/deny）

4. **删除 AST-grep 引用**（行 599）
   - 或明确说明是外部工具

5. **重写案例**（行 920-1088）
   - 改为"虚构教学示例"或提供 CVE 引用

### 7.2 次要修复（中优先级）

1. 修复 STRIDE 表格格式（行 754-759）
2. 删除学习检查清单中的 `passive/restricted/inherit`（行 1181）
3. 删除 ROI 表格数字或添加计算假设

---

## 八、总结

| 类别 | 数量 | 状态 |
|------|------|------|
| 不存在的文件引用 | 10 | ❌ 全部不存在 |
| 虚构的权限模式 | 3 | ❌ 不存在 |
| 配置结构错误 | 全部 | ❌ 不符合 OpenCode |
| 版本声明 | 2 | ✅ 正确 |
| Markdown 链接 | 6 | ✅ 全部有效 |

**总体评分**：3/10（技术准确性）

**审计结论**：文档存在严重的文档漂移（Documentation Drift），配置示例全部基于虚构的 schema，需要实质性重写以匹配 OpenCode v1.16.x 的实际实现。

---

*审计完成于 2026-06-06*
*审计方法：文件系统验证 + 官方文档对比 + 代码结构分析*
