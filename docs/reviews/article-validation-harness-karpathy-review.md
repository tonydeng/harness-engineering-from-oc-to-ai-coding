# Karpathy 技术评审报告

**目标文件**: `src/02-core-concepts/validation-harness.md` (1303 行)
**评审视角**: Karpathy（工程现实主义）
**评审日期**: 2026-06-06

---

## 一、核心结论

本文存在**严重的事实性失真**。大量描述的"验证护栏"功能在 OpenCode 原生实现中**根本不存在**。这是概念设计 vs 实际功能的典型混淆案例。

---

## 二、事实核查结果

### 1. "YOLO 分类"/Risk Classifier —— **完全失真**

**实际存在的**：OpenCode 确实有 YOLO mode，但极其简单——`"yolo": true` 布尔开关，auto-approves `ask` 权限提示，仍尊重 `deny` 规则。CLI 可用 `--yolo` 或 `/yolo` TUI 命令切换。这是 PR #7137 / #9073 / #9070 / #11833 / #27851 中实现的功能。

**书中描述的 Risk Classifier（风险分类器）不存在于 OpenCode 源码中**。具体来说：

| 书中声称 | 实际情况 | 判定 |
|---------|---------|------|
| 三级风险分类（高/中/低）+ 对应执行策略 | YOLO 只有 on/off，没有分类 | ❌ 虚构 |
| 规则引擎：正则匹配 + 模式分类 | OpenCode permission 系统有 allow/ask/deny 三级策略 | ❌ 张冠李戴 |
| `yolo.training` 配置项（learning_rate, min_samples, forget_after_days） | 实际 config schema 中的 `yolo` 字段是 `boolean`，不是对象 | ❌ 虚构 |
| `yolo.custom_rules` 配置对象 | 实际 `yolo` 字段只是 `boolean`，从无 `custom_rules` | ❌ 虚构 |
| 分类决策流程图 | 纯属想象 | ❌ 虚构 |
| 分类器"训练机制" | OpenCode 不做任何基于用户操作的学习 | ❌ 虚构 |

**根源问题**：作者把 YOLO mode（一个简单的权限绕过开关）错误地扩展成了一个带有规则引擎、机器学习训练的复杂风险分类系统。

### 2. "质量门禁"体系 —— **完全虚构**

OpenCode 官方配置 schema（`packages/opencode/src/config/config.ts`）**没有 `validation` 或 `gates` 字段**。

**虚构内容**：
- `validation.gates.hard` / `quality` / `metric` 配置块
- "硬性门禁"、"质量门禁"、"量化门禁"分级
- 自动修复循环（auto_fix）

### 3. "自动修复循环" —— **完全虚构**

OpenCode **没有**内置的 auto-fix loop。Agent 写完代码后不会自动执行 `npm run lint --fix` 或 `npm run build` 来验证并重试。

### 4. "验证结果签名" —— **完全虚构**

OpenCode 没有验证结果签名机制。RS256 签名、时间戳验证、会话绑定全部不存在。

### 5. 版本号 —— ✅ **正确**

| 版本 | 真实存在 | 证据 |
|------|---------|------|
| OpenCode v1.15.x | ✅ v1.15.6, v1.15.10-13 | GitHub Releases 确认 |
| OpenCode v1.16.x | ✅ v1.16.0 (2026-06-05) | GitHub Releases 确认 |
| OMO v4.5.x | ✅ v4.5.0, v4.5.12 | GitHub Releases 确认 |
| OMO v4.7.x | ✅ v4.7.4 (2026-06-03) | GitHub Releases 确认 |

### 6. 示例文件路径 —— ❌ **全部断裂**

文中引用了 **17 个示例文件**，全部 **不存在**：
- `examples/quality-gates/` - 目录不存在
- `examples/validation/` - 目录不存在
- `examples/audit-logs/` - 目录不存在
- `examples/opencode-configs/quality-gates.jsonc` - 不存在

---

## 三、关键问题

### 问题 1：把 YOLO mode 错误地扩展成了 Risk Classifier

这是全篇文章最严重的问题。YOLO mode 的完整实现就是：
```json
{ "yolo": true }
```
一行搞定。作者把它扩展成了一个带有规则引擎、机器学习训练的复杂系统。

### 问题 2：虚构完整的"质量门禁"系统

OpenCode 的权限系统只有三级策略（allow/ask/deny）和四种作用域（全局/项目/会话/工具）。文中描述的三级门禁（硬性/质量/量化）不存在。

### 问题 3：虚构"自动修复循环"

OpenCode 没有自动修复循环。Agent 写完代码后不会自动执行 `npm run lint --fix`。

### 问题 4：例文件全为空引用

文中 17 个指向 `examples/` 目录的代码块引用全部是空路径。

---

## 四、建议修正

### 高优先级（必须修改）

1. **删除整个"风险分类器"部分**（424-686 行）。把 YOLO mode 描述为一个简单的权限绕过开关即可。

2. **删除"三级质量门禁"部分**（180-422 行）。OpenCode 不存在硬性/质量/量化三级门禁。

3. **删除"自动修复循环"部分**（886-1000 行）。该功能在 OpenCode 中不存在。

4. **删除"验证结果签名"相关章节**（1100-1200 行）。OpenCode 不支持验证结果签名。

5. **所有引用到 `examples/quality-gates/`, `examples/validation/`, `examples/audit-logs/` 的代码块路径必须修正或删除**。

### 中优先级

6. **LSP 验证链改写**。OpenCode 的 LSP 是一次性诊断，不是"语法→类型→Lint→语义"的链条式检查。

7. **`security-overview.md` 同步修正**。该文中的 `yolo` 配置对象必须改为 `"yolo": true` 布尔值形式。

8. **`sandbox-hooks.md` 中 `yolo-classify` hook 点改正**。真实的 YOLO mode 不会触发一个叫做 `yolo-classify` 的 hook。

---

## 五、预计修复工作量

- 删除虚构功能文字：约 600 行
- 替换为 OpenCode 实际 permission 系统说明：约 200 行
- 修正跨章节引用：3 个文件
- **总重写比例约 50-60%**

---

## 六、总体评价

这是一篇**概念框架好但工程实现完全失真**的文章。"验证护栏"作为一个概念是好设计（分级门禁 + 风险分类 + 修复循环都是合理的工程模式），但内容被错误地包装成了 OpenCode 的现有功能来讲述。

**建议**：要么重写为"最佳实践建议"而非"现有功能说明"，要么完全删除虚构内容，仅保留 OpenCode 实际存在的功能描述。

---

**评审者**: Karpathy 视角技术评审 agent  
**评审时间**: 2026-06-06  
**版本**: OpenCode v1.16.0 / oh-my-openagent v4.7.4

---

## 附录：修复跟踪 (2026-06-06 第二次评审)

### 状态：✅ 全部修复

文章已在 commit `63dbfb4` 中进行大规模重写（1303行→363行），评审中发现的所有问题已修正：

| 问题 | 修复方式 |
|------|---------|
| YOLO/Risk Classifier 虚构 | 删除，替换为 OpenCode 原生 `permission` 系统描述 |
| 三级风险分类虚构 | 移除，改为架构设计建议 |
| YOLO configuration 对象虚构 | 简化为 `"yolo": true` 布尔开关 |
| 分类决策流程图虚构 | 移除 |
| 自动修复循环与成功率数据虚构 | 移除，改为"工具辅助修复" |
| STRIDE 威胁模型过度工程化 | 移除，改为简化的安全考虑 |
| 验证结果签名/RS256 不可行 | 移除 |
| 沙箱预执行虚构 | 移除 |
| 16+ 缺失示例文件 | 移除引用，改为引用已有文件 |
| OMO 版本号无依据 | 移除 |

**本次 Sisyphus-Junior 二次评审发现**：当前版本中 `permission` 配置格式使用了 `{"allow": [...], "ask": [...]}` 逆转录格式，已修正为 OpenCode 实际 schema 的 per-tool 格式 `{"read": "allow", "bash": "ask"}`。
