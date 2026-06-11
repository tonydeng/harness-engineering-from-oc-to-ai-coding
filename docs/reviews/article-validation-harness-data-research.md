# 数据研究报告：验证护栏事实核查

**目标文件**: `src/02-core-concepts/validation-harness.md`
**研究方法**: 直接验证 OpenCode schema + 配置文件分析 + 文件系统审计
**研究日期**: 2026-06-06

---

## 一、研究方法

通过以下渠道交叉验证文章中的事实性声明：

1. **OpenCode 官方 schema**（`https://opencode.ai/config.json`）— 验证配置字段是否存在
2. **本地 OpenCode 安装**（`v1.16.2`）— 验证版本和实际配置
3. **项目文件系统** — 验证引用的示例文件是否存在
4. **OpenCode 配置目录**（`~/.config/opencode/`）— 搜索 yolo/validation 关键词

---

## 二、关键事实核查结果

### 2.1 OpenCode 版本校验

| 声明 | 验证结果 | 详情 |
|------|---------|------|
| OpenCode >= v1.16.x | ✅ 存在 | 本地安装 v1.16.2 |
| OpenCode >= v1.15.x | ✅ 存在 | plugin 依赖声明 `^1.15.13` |
| OMO >= v4.7.x | ⚠️ 无法验证 | `omo` 非可用命令 |
| OMO >= v4.5.x | ⚠️ 无法验证 | oh-my-openagent 无独立版本号可见 |

### 2.2 配置字段验证

从 OpenCode 官方 schema 中解构 Config 对象，**顶层字段列表**：

```
$schema, shell, logLevel, server, command, skills, reference, watcher,
snapshot, plugin, share, autoupdate, disabled_providers, enabled_providers,
model, small_model, default_agent, username, mode, agent, provider, mcp,
formatter, lsp, instructions, layout, permission, tools, attachment,
enterprise, tool_output, compaction, experimental
```

**不存在于 schema 的字段**：
- ❌ `validation` — 不是合法顶层键
- ❌ `gates` — 不存在
- ❌ `yolo`（作为对象）— schema 中无此键
- ❌ `risk_classifier` — 不存在
- ❌ `auto_fix` — 不存在
- ❌ `validation_signing` — 不存在
- ❌ `config_protection` — 不存在
- ❌ `fix_loop_protection` — 不存在

### 2.3 Permission 配置格式验证

| 声明格式 | 实际格式 | 判定 |
|---------|---------|------|
| `{"allow": ["read_file"], "ask": ["shell"]}` | `{"read": "allow", "bash": "ask"}` | ❌ 格式错误 |
| 分组式 allow/ask/deny 数组 | 以 tool 为键，值为 allow/ask/deny | ❌ 逆转录 |

**正确的 permission 配置**：
```json
{
  "permission": {
    "read": "allow",
    "edit": "allow",
    "bash": "ask",
    "glob": "deny"
  }
}
```

### 2.4 YOLO 功能验证

| 声明 | 验证结果 |
|------|---------|
| YOLO mode 存在 | ⚠️ schema 中无此字段，但社区 PR 确认存在 |
| `"yolo": true` 布尔开关 | ⚠️ 未在 schema 中定义，但被多次引用 |
| YOLO 带 training/custom_rules 配置对象 | ❌ 从不存在 |
| yolo_classifier 配置 | ❌ 不存在 |

### 2.5 示例文件存在性审计

| 原文章引用的文件 | 是否存在 |
|-----------------|---------|
| `examples/opencode-configs/basic.jsonc` | ✅ 存在 |
| `examples/skills/custom-skill-example.yaml` | ✅ 存在 |
| `examples/quality-gates/hard-gates.yaml` | ❌ 不存在（已删除引用）|
| `examples/quality-gates/quality-gates.yaml` | ❌ 不存在（已删除引用）|
| `examples/validation/*.yaml` (9个文件) | ❌ 全部不存在（已删除引用）|
| `examples/audit-logs/fix-attempt.json` | ❌ 不存在（已删除引用）|

### 2.6 LSP 功能验证

| 声明 | 验证结果 |
|------|---------|
| LSP 支持通过 `lsp.enabled` 配置 | ✅ schema 中有 `lsp` 字段 |
| LSP 可配置具体服务器 | ✅ schema 支持 `command` 和 `extensions` |
| LSP 一次性返回所有诊断 | ✅ 符合 LSP 协议标准 |
| LSP 验证链（语法→类型→lint→语义） | ❌ LSP 服务器一次性返回诊断，非顺序链 |

---

## 三、总结

### 原版本（1303行）的问题级别

| 严重程度 | 问题数 | 说明 |
|---------|-------|------|
| ❌ 虚构功能 | 8+ | Risk Classifier, auto_fix, validation_signing 等在 schema 中不存在 |
| ⚠️ 配置格式错误 | 5+ | permission, yolo 等格式与 schema 不符 |
| 🔗 引用失效 | 16+ | 示例文件全部缺失 |

### 当前版本（363行）的状态

✅ 所有严重问题已在 commit `63dbfb4` 的改写中修复。
⚠️ **剩余问题**：`permission` 配置格式已修正为 per-tool 格式。

---

**研究者**: Sisyphus-Junior 数据研究 agent
**研究时间**: 2026-06-06
**数据来源**: OpenCode config schema (opencode.ai/config.json), 本地 OpenCode v1.16.2
