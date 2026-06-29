# 综合评审：chinese-providers.md

> **目标文件**: `src/03-setup/chinese-providers.md`
> **评审日期**: 2026-06-06

---

## 评审概述

本文从三个独立视角对 `chinese-providers.md` 进行了交叉评审。

| 视角 | 评审人 | 核心关注 |
|------|--------|---------|
| **Karpathy（工程现实主义）** | Andrej Karpathy 视角 | 模型版本准确性、定价正确性、API 配置参数验证 |
| **Munger（投资视角 + 商业分析）** | Charlie Munger 视角 | 成本比率验算、定价可持续性、营销数学揭露、风险揭示 |
| **TechLead（配置架构审查）** | 技术负责人视角 | JSON 配置结构正确性、OpenCode schema 合规性、生产阻断问题 |

**总体结论**: 文章存在 **3 个严重模型版本错误**、**7 个配置结构错误** 和 **多个成本数据问题**。DeepSeek V3.2 已被 V4 取代且遗留 ID 将于 2026 年 7 月 24 日停止工作；成本比率"1/30"被自证为 1/17.9；配置结构中 `apiKey`/`baseURL` 处于错误嵌套层级。

---

## 各视角发现汇总

### Karpathy 视角：工程现实性审查

**核心结论**: 文章包含 **3 个关键错误**（会导致生产故障）、**4 个过时声明**（因 2026 年快速模型迭代）、**3 个缺失上下文**。

**🔴 关键错误（必须修复）**:

| # | 问题 | 文章声称 | 实际情况 | 影响 |
|---|------|---------|---------|------|
| 1 | **DeepSeek V3.2 已不存在** | 描述 V3.2（MoE 671B/37B）为当前版本 | V4 于 2026-04-24 发布；V4-Flash（284B/13B）、V4-Pro（1.6T/49B）；遗留 ID 2026-07-24 停止工作 | 文章展示已淘汰技术，配置将在月内失效 |
| 2 | **DeepSeek 定价错误** | `$0.28/$0.42` 每百万 token | V4-Flash 实际 `$0.14/$0.28`；无官方 SKU 匹配 `$0.28/$0.42` | 成本计算基于错误定价 |
| 3 | **Qwen3-Max USD 定价错误** | `$0.35/$1.40` | 国际定价实际 `$1.20/$6.00`（新加坡）；`$0.35/$1.40` 为 CNY→USD 粗略换算 | 对比表低估 Qwen 定价约 **3.4 倍** |

**额外关键错误**:

| # | 问题 | 实际情况 |
|---|------|---------|
| 4 | **DeepSeek Reasoner MaxOutput 错误**（Line 171） | 声称 `64000`，V3.2 实际 8K、V4-Flash 384K |
| 5 | **Reasoning Effort 值错误**（Lines 498-502） | 声称 `low/medium/high`，实际 `low/medium` 映射到 `high`，仅 `high/max` 有效 |

**⚠️ 过时声明**:

| # | 问题 | 实际情况 |
|---|------|---------|
| 6 | **Kimi K2.6 缺失** | 声称 K2.5 为旗舰；实际 K2.6 已发布（约 2026 年 5 月），定价 `$0.95/$4.00` |
| 7 | **DeepSeek 上下文窗口错误** | 声称 128K；V4 实际 1M |
| 8 | **Kimi 国际 API 端点缺失** | 仅列出 `api.moonshot.cn`；国际用户需 `api.moonshot.ai` |

**ℹ️ 缺失上下文**:
- Qwen 分级定价未说明（0-32K/32K-128K/128K-256K 三级）
- Codeforces 声明"超越所有非 o1 类模型"存在误导（GPT-5、Gemini 3.0 Pro 也是推理模型）

**✅ 验证正确的内容**:

| 声明 | 状态 |
|------|------|
| DeepSeek-V3.2 MoE 671B/37B（V3.2 纸面参数） | ✅ 正确 |
| API endpoint `https://api.deepseek.com` | ✅ 确认 |
| API endpoint `https://api.moonshot.cn/v1` | ✅ 中国区正确 |
| API endpoint `https://dashscope.aliyuncs.com/compatible-mode/v1` | ✅ 确认 |
| Kimi 256K 上下文窗口 | ✅ 262,144 tokens |
| `enable_thinking` for Qwen | ✅ 正确参数 |
| Temperature/top_p 推荐 | ✅ 实用建议 |
| 缓存折扣百分比 | ✅ 大致正确 |

---

### Munger 视角：成本与商业价值分析

**总体等级**: **D（不可靠）** — 有基本正确的事实基础，但存在优化偏差。

**发现 1：成本比率营销数学**

文章声称"API 价格约为 GPT-4o 的 1/30，Claude 的 1/20"。

**自身体数据验算**（使用文章表格 $0.28/$0.42 vs GPT-4o $2.50/$10.00 vs Claude $3.00/$15.00）：

| 比例 | 仅输入 | 仅输出 | 50/50 混合（文章自身） | 现实 80/20 |
|------|--------|--------|---------------------|-----------|
| DeepSeek : GPT-4o | 1/8.9 | 1/23.8 | **1/17.9** | **1/13.0** |
| DeepSeek : Claude | 1/10.7 | 1/35.7 | **1/25.7** | **1/17.7** |

**芒格式结论**: "1/30"和"1/20"**不成立**。编码工作负载输入占主导（70-90%），80/20 比例下实际为 **1/13.0**（GPT-4o）和 **1/17.7**（Claude）。

**发现 2：定价过时**
- DeepSeek V4 于 2026 年 4 月 24 日发布，文章仍引用 V3.2 定价
- Legacy ID 将于 2026 年 7 月 24 日停止工作
- V4-Flash 实际 `$0.14/$0.28` 的定价模式不同

**发现 3：上下文窗口夸大不是实质优势**
- OpenAI 数据显示大多数用户使用 <32K 上下文
- V4 Flash 有 1M 上下文，256K 规格完全过时
- 真正的限制是**输出**而非输入

**发现 4：Codeforces 声明问题**
- "非 o1 类"限定词排除了最相关竞争对手
- Codeforces Elo 评分被 2026 年学术论文证明根本上不可靠（±1,348 分差异）
- Codeforces 表现与实际软件工程技能关联不强

**发现 5：价格战不可持续**
- DeepSeek 于 2024 年 12 月至 2026 年 4 月期间**四次**降价
- V4 Pro 75% 折扣后来**永久化**
- 低价难以覆盖推理成本

**发现 6：内容审查风险被最小化**
- 文章声称"技术场景通常不受影响"
- 学术证据显示中国 LLM 存在系统性政治审查，不准确性达 22%
- 2026 CAC 法规进一步收紧

**发现 7：跨文档不一致**

| 文档 | 声称比率 |
|------|---------|
| chinese-providers.md 第 5 行 | 1/10 到 1/20 |
| chinese-providers.md 第 23 行 | 1/30 |
| opencode-config.md 第 1099 行 | 1/10–1/30 |
| chinese-ecosystem.md 第 84 行 | 1/5~1/10 |

**芒格式评论**: "同一比率有四份不同版本。如果连成本对比这么简单的事情都搞不定，为什么我要相信你对复杂事情的分析？"

**可用场景判断**:
- ✅ 初步概念探讨
- ❌ 投资级成本研究
- ❌ 供应商选择依据
- ❌ 长期预算分析

---

### TechLead 视角：配置架构审查

**核心结论**: JSON 配置块包含 **7 个关键结构错误**，会导致生产故障。

**🔴 关键配置问题（生产阻断级）**:

| # | 问题 | 说明 | 位置 |
|---|------|------|------|
| 1 | **`apiKey`/`baseURL` 嵌套层级错误** | 文档设为顶层属性；OpenCode schema 要求放在 `options` 对象内 | Lines 158-159, 228-229, 307-308, 375-376, 384-385 |
| 2 | **Model 字段结构错误** | 文档使用 `context`/`maxOutput` 顶层字段；需 `limit.context`/`limit.output` | Lines 163-171, 231-257, 310-341 |
| 3 | **Qwen 缺少 `npm` 字段** | Qwen 非内置 provider，需 `"npm": "@ai-sdk/openai-compatible"` | Line 305 |
| 4 | **Kimi `/connect` 流程错误** | 文档说"选择 Custom Provider"；实际 Moonshot AI 是内置 provider 可直接搜索 | Line 211 |
| 5 | **`fallback` 字段无效** | `"fallback": "balanced-model"` 非 OpenCode 合法配置键 | Line 407 |
| 6 | **多 Provider 混合使用虚假模型名** | `"balanced-model"`/`"best-capability-model"` 非真实 Anthropic 模型 ID | Lines 368-370 |
| 7 | **`proxy` 字段不支持** | Provider 配置不支持 `proxy` 字段，需通过环境变量设置 | Lines 628-632 |

**🟡 中等问题**:

| # | 问题 | 建议 |
|---|------|------|
| 8 | **缺少 `env` 字段** | OpenCode 模式包含 `"env": ["DEEPSEEK_API_KEY"]` 用于启动验证 |
| 9 | **`deepseek-reasoner` MaxOutput 值存疑** | 声称 64000，V3.2 API 实际最多 8K |
| 10 | **定价表混用货币** | Qwen 用 CNY（¥）vs DeepSeek/Kimi 用 USD（$），缺说明 |

**✅ 正确的内容**:
| 项目 | 状态 |
|------|------|
| `{env:VAR}` 语法 | ✅ 正确 |
| `/connect` TUI 命令 | ✅ 正确 |
| `/models` 验证命令 | ✅ 正确 |
| Base URLs（DeepSeek、Kimi、Qwen） | ✅ 正确 |
| 成本计算（Lines 549-555） | ✅ 正确 |
| Mermaid 流程图 | ✅ 正确 |
| 环境变量导出 | ✅ 正确 |

**TechLead 提供的修正配置模板**:

**DeepSeek（内置 Provider）**:
```json
{
  "provider": {
    "deepseek": {
      "env": ["DEEPSEEK_API_KEY"],
      "options": {
        "apiKey": "{env:DEEPSEEK_API_KEY}",
        "baseURL": "https://api.deepseek.com"
      },
      "models": {
        "deepseek-v4-flash": {
          "name": "DeepSeek V4 Flash",
          "limit": { "context": 1000000, "output": 384000 }
        }
      }
    }
  }
}
```

**Moonshot/Kimi（内置 Provider）**:
```json
{
  "provider": {
    "moonshot": {
      "env": ["MOONSHOT_API_KEY"],
      "models": {
        "kimi-k2.6": {
          "name": "Kimi K2.6",
          "limit": { "context": 262144, "output": 8192 }
        }
      }
    }
  }
}
```

**Qwen（自定义 Provider）**:
```json
{
  "provider": {
    "qwen": {
      "npm": "@ai-sdk/openai-compatible",
      "env": ["DASHSCOPE_API_KEY"],
      "name": "Qwen",
      "options": {
        "baseURL": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "apiKey": "{env:DASHSCOPE_API_KEY}"
      },
      "models": {
        "qwen3-max": {
          "name": "Qwen3 Max",
          "limit": { "context": 262144, "output": 8192 }
        }
      }
    }
  }
}
```

---

## 问题与建议

### 问题优先级矩阵

| 优先级 | 问题 | 涉及视角 | 影响 |
|--------|------|---------|------|
| **🔴 P0** | DeepSeek V3.2 已被 V4 取代，遗留 ID 2026-07-24 停止工作 | Karpathy、Munger | 配置月内失效 |
| **🔴 P0** | DeepSeek 定价使用已淘汰的 V3.2 价格 | Karpathy、Munger | 成本计算全错 |
| **🔴 P0** | Qwen USD 定价低估约 3.4 倍 | Karpathy | 对比表严重偏差 |
| **🔴 P0** | `apiKey`/`baseURL` 嵌套层级错误（需 `options` 包裹） | TechLead | 配置运行时静默失败 |
| **🔴 P0** | Model 字段结构错误（需 `limit.context`/`limit.output`） | TechLead | 模型限制被忽略 |
| **🔴 P0** | Qwen 缺少 `npm` 字段 | TechLead | OpenCode 不知道用哪个 adapter |
| **🔴 P0** | Kimi `/connect` 流程错误 | TechLead | 用户操作路径错误 |
| **🔴 P0** | `fallback`/`proxy` 字段无效 | TechLead | 配置被静默忽略 |
| **🟡 P1** | 成本比率"1/30"自证为 1/17.9（80/20 比例下 1/13.0） | Munger | 营销数学误导 |
| **🟡 P1** | Reasoning Effort 值错误（`low`/`medium` 映射到 `high`） | Karpathy | 参数无效 |
| **🟡 P1** | Kimi K2.6 缺失、K2.5 已属上一代 | Karpathy | 模型信息过时 |
| **🟡 P1** | 缺少 `env` 字段 | TechLead | 启动时无法验证环境变量 |
| **🟡 P1** | 跨文档成本比率不一致（4 个版本） | Munger | 可信度问题 |
| **🟢 P2** | DeepSeek 上下文窗口 128K→1M | Karpathy | 规格过时 |
| **🟢 P2** | Kimi 国际 API 端点缺失 | Karpathy | 国际用户受阻 |
| **🟢 P2** | Qwen 分级定价未说明 | Karpathy | 信息不完整 |
| **🟢 P2** | Codeforces 声明需更精确 | Karpathy、Munger | 选择性呈现 |
| **🟢 P2** | 内容审查风险被最小化 | Munger | 风险披露不足 |
| **🟢 P2** | 定价表混用货币（CNY vs USD） | TechLead | 对比困惑 |

### 各视角独特建议

**Karpathy 视角特有建议**:
- 增加 V4 作为当前世代，标注 V3.2 为历史参考
- 增加遗留模型 ID 废弃警告
- 添加 Kimi 国际 API 端点 `api.moonshot.ai`
- Codeforces 声明改为精确表述

**Munger 视角特有建议**:
- 忽略所有营销比率，用真实输入产出比（70/30 或 80/20）自算
- 长期成本压力测试：V4 Pro 上架价 $1.74/$3.48
- "不要基于此做供应商选择决策"
- 审查测试：用敏感查询验证"技术场景不受影响"

**TechLead 视角特有建议**:
- 提供完整的修正配置模板（已提供 DeepSeek/Moonshot/Qwen 三份）
- 所有 provider 配置块增加 `env` 数组
- 验证 `deepseek-reasoner` maxOutput 官方规格

---

## 综合评分

| 维度 | 评分 | 说明 |
|------|------|------|
| **模型版本准确性** | ★★☆☆☆ | V3.2 已淘汰，V4 未提及，K2.6 缺失 |
| **定价数据准确性** | ★★☆☆☆ | 3 项关键定价错误，比率夸大 |
| **配置结构正确性** | ★☆☆☆☆ | 7 个配置结构错误，全部会导致生产故障 |
| **风险披露完整性** | ★★☆☆☆ | 审查风险最小化，价格可持续性未讨论 |
| **内部一致性** | ★★★☆☆ | 自身公式自证矛盾，跨文档 4 个版本 |
| **实用性** | ★★★★☆ | Base URLs、命令、流程图等基础信息正确 |

**综合评定**: 三个视角产生了截然不同但互补的发现——Karpathy 发现模型版本过时，Munger 揭露了营销数学，TechLead 发现了根本性的配置结构错误。文章在基础信息（Base URLs、命令操作）方面可靠，但在**模型版本、定价和配置语法**三个维度存在严重问题。建议在发布前进行全面的模型版本更新和配置语法修正。

---

*合并自：Karpathy 工程审查、Munger 投资视角审计、TechLead 配置架构审查（2026-06-06）*
