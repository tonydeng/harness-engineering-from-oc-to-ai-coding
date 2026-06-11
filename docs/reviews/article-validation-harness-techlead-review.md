# TechLead 架构评审报告

**目标文件**: `src/02-core-concepts/validation-harness.md` (1303 行)
**评审视角**: TechLead（架构完整性、配置准确性、技术可行性）
**评审日期**: 2026-06-06

---

## 一、核心发现摘要

### 架构完整性：概念合理，实现虚构
验证护栏作为"准入/准出"分层的概念设计是正确的，但大量具体实现描述在 OpenCode 中不存在。

### 配置准确性：16 个示例文件全部缺失
文中引用的所有示例文件在项目中都不存在，这是 credibility 问题。

### 技术可行性：过度工程化
STRIDE 威胁建模、验证结果签名等功能超出了 OpenCode CLI 工具的实际能力边界。

---

## 二、架构完整性分析

### 2.1 定位与分层：正确，但不完整

**正确的部分**：
- 验证护栏定位为"准出"系统，与约束系统的"准入"形成对偶关系 ✅
- LSP 验证链（语法→类型→Lint→语义）遵循了标准编译管线的自然顺序 ✅

**缺失的部分**：
- 缺少验证→反馈→约束更新的闭环
- 修复后的验证结果如何反向影响约束系统规则未说明

### 2.2 自动修复循环的拓扑问题

流程图显示修复循环回到 `E2 (Build Agent)`，意味着每次重试都调用一次 LLM。在 `max_attempts=3` 配置下，最坏情况是 **4 次 LLM 调用**。

**未讨论的问题**：
- 成本 implication（一次 lint 修复尝试约 $0.05-0.15）
- 在企业大规模部署时的隐性成本

---

## 三、配置准确性分析

### 3.1 关键发现：16 个示例文件全部不存在 ⚠️

| 引用路径 | 磁盘状态 |
|---------|---------|
| `examples/quality-gates/hard-gates.yaml` | ❌ 不存在 |
| `examples/quality-gates/quality-gates.yaml` | ❌ 不存在 |
| `examples/validation/metric-gates.yaml` | ❌ 不存在 |
| `examples/opencode-configs/quality-gates.jsonc` | ❌ 不存在 |
| `examples/validation/high-risk-rules.yaml` | ❌ 不存在 |
| `examples/validation/medium-risk-rules.yaml` | ❌ 不存在 |
| `examples/validation/low-risk-rules.yaml` | ❌ 不存在 |
| `.opencode/yolo-rules.yaml` | ❌ 不存在 |
| `examples/validation/eslint-rules.yaml` | ❌ 不存在 |
| `examples/quality-gates/test-config.yaml` | ❌ 不存在 |
| `examples/validation/arch-rules.yaml` | ❌ 不存在 |
| `examples/quality-gates/auto-fix-config.yaml` | ❌ 不存在 |
| `examples/audit-logs/fix-attempt.json` | ❌ 不存在 |
| `examples/validation/yolo-classifier.yaml` | ❌ 不存在 |
| `examples/validation/validation-signing.yaml` | ❌ 不存在 |
| `examples/quality-gates/fix-loop-protection.yaml` | ❌ 不存在 |
| `examples/validation/config-protection.yaml` | ❌ 不存在 |

**严重度：高** — 根据 AGENTS.md 约定的代码块格式规范，这些路径应该对应实际存在的示例文件。

### 3.2 门禁动作枚举不一致

文档定义了两种执行模式（`block` 和 `warn`），但 metric gates 引入了第三种模式 `review`，且从未解释其行为定义。

### 3.3 配置保护机制的循环依赖

`config_protection.yaml` 中配置 `0644` 权限对 Unix 有效，但对同一用户下的 Agent 毫无约束力。这是**软性安全**。

---

## 四、技术可行性分析

### 4.1 门禁阻断 vs 告警模式

**可行的部分**：
- 编译/语法/类型检查作为 `block` 模式 ✅
- ESLint 警告作为 `warn` 模式 ✅

**有问题的部分**：

`npm audit --audit-level=high` 作为硬性门禁（block）❌
- 大多数生产级 Node.js 项目（尤其是有 500+ 依赖的中大型项目）几乎不可能达到零 high-severity 审计警告
- 这会导致 CI 经常失败，破坏开发流程

### 4.2 风险分类器的现实局限性

模式匹配（正则表达式）分类器有根本性局限：
- 字符串拼接 `"rm" + " -rf /"` 可绕过
- Base64 编码可绕过
- 通过脚本间接执行可绕过

### 4.3 沙箱机制的缺失

文档 6 次提到"沙箱"，但从未解释技术实现：
- 基于什么技术？（Docker? Firecracker? gVisor?）
- 跨平台兼容性？
- 启动延迟？
- 如果用户没装 Docker？

---

## 五、STRIDE 威胁建模评审

### 5.1 严重性评级争议

| 威胁 | 文档评级 | 建议评级 | 理由 |
|-----|---------|---------|------|
| **S - Spoofing** | 中 | **高** | 单点故障，验证系统是整个安全体系的最后一道防线 |
| **I - Information Disclosure** | 低 | **中** | 验证日志包含源代码差异、文件路径、错误栈等敏感信息 |
| **D - DoS（修复循环）** | 中 | **高** | Token 成本 = 直接经济损失 |

### 5.2 纵深防御架构评价

四层防护是**顺序依赖**的——单层穿透即意味着所有内层失效。缺乏**横向冗余**和**失效独立**设计。

---

## 六、建议修正

### P0 — 必须修复

1. **创建 16 个示例文件**：所有 `examples/quality-gates/`, `examples/validation/`, `examples/audit-logs/` 目录和文件必须落地。

2. **修复逻辑矛盾**：fix-loop-protection.yaml 中 `attempts: 5` 在 `max_attempts: 3` 配置下不可达。

3. **统一门禁动作枚举**：在"阻断模式 vs 告警模式"章节增加 `review` 动作定义。

### P1 — 强烈建议

4. **将 `npm audit --audit-level=high` 从硬性门禁降级为质量门禁**（或改为 `--audit-level=critical`）。

5. **STRIDE 严重性修正**：
   - Spoofing: 中 → **高**
   - Information Disclosure: 低 → **中**
   - DoS（修复循环）: 中 → **高**

6. **增加"假设与局限性"章节**：坦陈模式匹配分类器的局限性、沙箱机制属于设计阶段而非实现阶段。

---

## 七、总结评分

| 维度 | 评分 | 说明 |
|------|------|------|
| **架构设计合理性** | ⭐⭐⭐⭐ (4/5) | 准入/准出分层正确，验证链顺序合理 |
| **质量门禁分级设计** | ⭐⭐⭐ (3/5) | 三级分层合理，但 `review` 动作未定义 |
| **风险分类逻辑** | ⭐⭐ (2/5) | 理论框架还行，但纯模式匹配在实际攻击面前几乎无效 |
| **STRIDE 分析准确度** | ⭐⭐⭐ (3/5) | 覆盖完整但 2 项严重性误判 |
| **配置示例正确性** | ⭐⭐⭐ (3/5) | 语法全部正确，但 16 个文件全部缺失 |
| **技术可行性（落地）** | ⭐⭐ (2/5) | 沙箱未定义、配置保护存在循环依赖 |

**总体评价**：这是一篇**概念和架构设计非常棒的文档**——思路清晰、分层合理、覆盖面广。但它目前更接近一篇**架构设计白皮书**而非**工程实现指南**。

---

**评审者**: TechLead 架构评审 agent  
**评审时间**: 2026-06-06

---

## 附录：修复跟踪 (2026-06-06 第二次评审)

### 状态：✅ 全部修复

文章已在 commit `63dbfb4` 中大规模重写（1303行→363行），TechLead 评审中发现的所有问题已修正：

| 问题 | 修复方式 |
|------|---------|
| 16 个示例文件全部缺失 | 移除所有不存在的文件引用，仅引用已有文件 |
| Risk Classifier 虚构 | 替换为 OpenCode 实际 `permission` 系统 |
| 自动修复循环配置不真实 | 移除，改为"工具辅助修复" |
| STRIDE 威胁建模过度工程化 | 删除，改为简化的安全考虑章节 |
| 沙箱/签名/密钥轮换不可行 | 全部移除 |
| YOLO 配置项不准确 | 简化为 `"yolo": true` 布尔值 |

**本次 Sisyphus-Junior 二次评审**：`permission` 配置格式从 `{"allow": [...], "ask": [...]}` 修正为 per-tool 格式 `{"read": "allow", "bash": "ask"}`。
