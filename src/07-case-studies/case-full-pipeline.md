# 案例：全流程自动化

> 从自然语言的需求描述到自动创建的 PR，构建一条端到端的 AI 驱动开发流水线。关键洞察：自动化不等于无人化，人的角色从"执行者"转变为"审核者"。

## 案例概述

本案例的目标是构建一条从需求到 PR 的全流程自动化流水线——产品经理输入自然语言需求，流水线自动完成用户故事编写、架构设计、代码实现、测试生成和 PR 创建。这不是一个"把开发者替换掉"的尝试，而是一个"让开发者聚焦于更高价值工作"的工程实践。读完本文，你将理解如何构建一条从自然语言需求到自动创建 PR 的端到端 AI 驱动开发流水线。

流水线按四个阶段串联：需求分析阶段将自然语言转化为结构化的用户故事，并经过自动评审；架构设计阶段由 **Agent（智能体）** 生成技术方案，记录 ADR（架构决策记录），经过人工或自动评审后进入开发阶段；代码实现阶段启用多 Agent 并行开发，每个 Agent 负责独立的模块，配合代码审查自动化；最后自动生成测试、集成到 CI/CD、创建 PR 并附上变更摘要。

这个案例的核心设计理念是**"交接点即风险点"**。每个阶段之间的交接（需求 → 设计 → 开发 → 测试 → PR）是最容易出问题的地方。流水线在每个交接点设置了格式校验、完整性检查和人工审核会签，确保上游输出的质量满足下游需求。案例还讨论了混合模型架构（→ [案例：国产模型混合架构](case-multi-model.md)）在全流程中的应用——简单任务用经济模型，复杂推理用高端模型。

> **⏱ 时间有限？先读这些：** 需求分析 → 架构设计 → 代码实现 → 测试与部署

## 1. 项目背景

### 为什么需要全流程自动化？

传统的软件开发流程像一个"三传手"链条：产品经理写 PRD → 技术经理转需求 → 架构师设计 → 开发编码 → 测试验证。信息每经过一个人，就损耗一次。一个需求从提出到上线，平均流转周期是 **5-10 个工作日**（来源：2023 年行业调查，Atlassian DevOps Trends Report），其中实际编码时间只占 20%，80% 花在沟通、等待和返工上。

本案例的目标团队是这样的：

```json:terminal
{
  "team_composition": {
    "product_manager": 1,
    "tech_lead": 1,
    "frontend_devs": 3,
    "backend_devs": 3,
    "qa_engineers": 2,
    "total": 10
  },
  "tech_stack": {
    "frontend": "React 18 + TypeScript + Next.js",
    "backend": "Node.js (NestJS) + Go (微服务)",
    "database": "PostgreSQL 15 + Redis 7",
    "ci_cd": "GitHub Actions + Docker + k8s",
    "monorepo": "Turborepo"
  },
  "pain_points": [
    "需求流转平均 3.2 天",
    "代码审查排队平均 1.5 天",
    "测试覆盖不全导致线上 bug 占比 35%",
    "新人上手周期 2-3 周"
  ]
}
```

### 解决思路

流水线不是要消灭人，而是要消灭"等待"。让 Agent 在每一个环节并行处理那些"计算机比人做得更快的事"：

| 环节 | 人做的事 | Agent 做的事 |
|------|---------|-------------|
| 需求 | 确认业务价值、设定优先级 | 写结构化用户故事、检查完整性 |
| 设计 | 做关键架构决策 | 生成方案草案、自动评审 |
| 开发 | 解决复杂逻辑 | 写 CRUD、API 接口、单元测试 |
| 测试 | 设计测试策略 | 生成测试用例、执行回归测试 |

每一次 PR 都是一次实践，PR review 是一次复盘。流水线加速了"实践 → 反馈 → 改进"的循环。

## 2. 阶段一：需求分析

### 2.1 自然语言 → 结构化用户故事

产品经理输入一段自然语言需求，Agent 自动转化为符合 **INVEST 原则**的用户故事：

```json:terminal
{
  "requirements_agent": {
    "input": "用户想通过微信扫码直接登录我们的电商平台，不用手动输账号密码。",
    "output": {
      "user_stories": [
        {
          "id": "US-001",
          "title": "微信扫码登录",
          "as_a": "已注册用户",
          "i_want": "通过微信扫码完成登录",
          "so_that": "不需要手动输入账号密码",
          "acceptance_criteria": [
            "登录页面显示微信二维码",
            "用户扫码后自动跳转到首页",
            "首次扫码需绑定已有账号",
            "扫码登录有效期 5 分钟"
          ],
          "invest_check": {
            "independent": true,
            "negotiable": true,
            "valuable": true,
            "estimable": "可估：2 SP",
            "small": "单个功能点，符合 Sprint 容量",
            "testable": "可测：E2E 测试覆盖"
          }
        }
      ],
      "epic_mapping": "EPIC-003: 第三方登录集成",
      "dependencies": ["OAuth 服务已部署", "微信开放平台 APP_ID 已申请"],
      "risks": ["微信支付回调兼容", "扫码后 session 状态管理"]
    }
  }
}
```

### 2.2 需求验证与一致性检查

Agent 自动检查需求质量：

| 检查项 | 方法 | 通过标准 |
|--------|------|---------|
| 完整性 | 检查是否存在歧义、缺失的边界条件 | 无"待定""后续讨论"等模糊词 |
| 冲突检测 | 比对存量需求库 | 与已有功能不冲突 |
| 可行性 | 评估实现难度和前置依赖 | 依赖项都有明确状态 |
| INVEST 评分 | 逐条评分 | 全部 7 项通过 |

### 2.3 交接校验（需求 → 设计）

需求阶段输出的用户故事通过 JSON Schema 校验后，才能流入架构设计阶段：

```json:terminal
{
  "handoff_quality_gate": {
    "gate_name": "需求到设计的交接门禁",
    "checks": [
      {"check": "user_story_count > 0", "type": "必填"},
      {"check": "每个 US 都有 acceptance_criteria", "type": "必填"},
      {"check": "每个 US 都有 INVEST 评分", "type": "建议"},
      {"check": "dependencies 列完整", "type": "必填"},
      {"check": "不存在 'TODO' 或 'TBD' 占位符", "type": "阻塞"}
    ],
    "action_on_fail": "返回产品经理补充，不走下个阶段"
  }
}
```

## 3. 阶段二：架构设计

### 3.1 Agent 生成技术方案

需求确认后，Architecture Agent 自动生成技术方案，包含 API 设计、数据模型和组件图：

```json:terminal
{
  "architecture_agent": {
    "input": "US-001: 微信扫码登录",
    "output": {
      "api_design": [
        {"method": "POST", "path": "/api/auth/wechat/qrcode", "desc": "生成微信登录二维码"},
        {"method": "GET", "path": "/api/auth/wechat/callback?code=&state=", "desc": "微信回调处理"},
        {"method": "POST", "path": "/api/auth/wechat/bind", "desc": "首次扫码后绑定已有账号"}
      ],
      "data_model": {
        "tables": [
          {"name": "wechat_bindings", "fields": [
            "id UUID PK", "user_id UUID FK", "open_id VARCHAR(128) UNIQUE",
            "union_id VARCHAR(128)", "created_at TIMESTAMP", "updated_at TIMESTAMP"
          ]}
        ]
      },
      "sequence": "用户扫码 → 前端轮询 qrcode_id → 微信回调 → 后端验证 code → 查询/创建绑定 → 下发 JWT"
    }
  }
}
```

### 3.2 ADR（架构决策记录）

每次重大决策都要记录 **ADR**，确保决策可追溯：

```json:terminal
{
  "adr": {
    "id": "ADR-2024-003",
    "title": "微信登录状态存储方案选择",
    "status": "Accepted",
    "context": "用户扫码登录后，前端需要轮询登录状态。需要选择一种实时的状态同步方案。",
    "options": [
      {"option": "WebSocket 长连接", "pros": ["实时性高"], "cons": ["扫码页可能使用量巨大，连接成本高", "增加基础设施复杂度"]},
      {"option": "轮询 + Redis", "pros": ["实现简单", "无需额外基础设施"], "cons": ["延迟 ~2s", "短时请求量集中", "需要设计超时清理"]},
      {"option": "SSE (Server-Sent Events)", "pros": ["单工通道，资源占用少", "浏览器原生支持"], "cons": ["微信内置浏览器兼容性不确定"]}
    ],
    "decision": "采用方案 2：轮询 + Redis",
    "rationale": "扫码登录页面是低频页面，实时性要求不高（~2s 可接受）。轮询方式对基础设施改动最小，适合第一个迭代。如有性能问题，后续可升级为 WebSocket。",
    "consequences": ["需设计二维码过期清理机制（TTL 5min）", "轮询接口需限流（10 req/min per qrcode_id）"],
    "reviewed_by": "Tech Lead"
  }
}
```

### 3.3 方案自动评审

Agent 对技术方案执行多维评分：

```json:terminal
{
  "architecture_review": {
    "scores": {
      "performance": "8/10 - 轮询方案延迟可控，Redis 抗压能力强",
      "security": "9/10 - OAuth code 交换流程标准，无额外攻击面",
      "scalability": "7/10 - 单次扫码高峰（618/双11）需关注 Redis 连接数",
      "maintainability": "9/10 - 逻辑集中在 auth service，不污染其他服务"
    },
    "overall": "Pass (8.25/10)",
    "reviewer": "Architecture Review Agent",
    "human_escalation": "不需要——方案设计清晰，无争议决策"
  }
}
```

### 3.4 交接校验（设计 → 开发）

```json:terminal
{
  "handoff_quality_gate": {
    "gate_name": "设计到开发的交接门禁",
    "checks": [
      {"check": "API 设计完整（路径/方法/参数/响应）", "type": "必填"},
      {"check": "数据模型完整（字段/类型约束/索引）", "type": "必填"},
      {"check": "序列图或流程图清晰", "type": "必填"},
      {"check": "关键决策有 ADR 记录", "type": "必填"},
      {"check": "架构评审评分 ≥ 7/10", "type": "建议"}
    ],
    "action_on_fail": "Architecture Agent 补充不完整项后重新提交评审"
  }
}
```

## 4. 阶段三：代码实现

代码阶段是流水线最复杂的部分。流水线启用多 Agent 并行开发——不同 Agent 负责不同模块，同时运行。

### 4.1 任务分解与分配

Architecture Agent 输出 PRD 后，Planning Agent 将任务拆解并分配给不同的 Dev Agent：

```json:terminal
{
  "task_decomposition": {
    "us_id": "US-001",
    "tasks": [
      {
        "task_id": "T001",
        "description": "实现二维码生成 API (POST /api/auth/wechat/qrcode)",
        "assigned_to": "dev-agent-backend-1",
        "depends_on": [],
        "estimated_hours": 2,
        "files": ["src/auth/wechat.controller.ts", "src/auth/wechat.service.ts"]
      },
      {
        "task_id": "T002",
        "description": "实现微信回调处理 (GET /api/auth/wechat/callback)",
        "assigned_to": "dev-agent-backend-1",
        "depends_on": ["T001"],
        "estimated_hours": 3,
        "files": ["src/auth/wechat.service.ts", "src/auth/wechat.guard.ts"]
      },
      {
        "task_id": "T003",
        "description": "实现登录状态轮询接口 (GET /api/auth/wechat/status)",
        "assigned_to": "dev-agent-backend-2",
        "depends_on": ["T001"],
        "estimated_hours": 2,
        "files": ["src/auth/wechat.controller.ts"]
      },
      {
        "task_id": "T004",
        "description": "实现扫码页面前端组件",
        "assigned_to": "dev-agent-frontend-1",
        "depends_on": ["T001", "T003"],
        "estimated_hours": 4,
        "files": ["src/components/WechatQRCode.tsx", "src/pages/login.tsx"]
      }
    ]
  }
}
```

### 4.2 多 Agent 并行开发

三个 Dev Agent 并行工作：

```mermaid
timeline:

T001 (dev-agent-backend-1)  ████████░░░░  80%
T002 (dev-agent-backend-1)  ░░░░░░░░████  0% (需等 T001 完成)
T003 (dev-agent-backend-2)  ██████░░░░░░  60%
T004 (dev-agent-frontend-1) ░░░░░░░░░░░░  0% (需等 T001 + T003)

并行率: 2/3 (67%)  —— 两个 backend agent 可并行
```

### 4.3 自动代码审查

每个 Dev Agent 完成代码后，Code Review Agent 执行审查：

```json:terminal
{
  "code_review": {
    "task_id": "T001",
    "status": "PASSED",
    "reviews": [
      {
        "category": "style",
        "tool": "ESLint + Prettier",
        "result": "PASS",
        "issues": ["无需调整——代码风格符合项目规范"]
      },
      {
        "category": "types",
        "tool": "TypeScript strict mode",
        "result": "PASS",
        "issues": []
      },
      {
        "category": "security",
        "tool": "Semgrep",
        "result": "PASS",
        "issues": ["Auth guard 已正确应用——评分: 9/10"]
      },
      {
        "category": "logic",
        "tool": "Code Review Agent (LLM)",
        "result": "PASS_WITH_SUGGESTION",
        "issues": [
          "建议: 二维码 TTL 从硬编码 300s 改为从配置读取",
          "建议: 添加重试逻辑——微信 API 可能返回 5xx"
        ]
      }
    ]
  }
}
```

### 4.4 Agent 间依赖协调

当一个 Agent 依赖另一个 Agent 的输出时（如 T003 依赖 T001），流水线自动管理依赖图：

```json:terminal
{
  "dependency_coordination": {
    "strategy": "Interface Contract First",
    "detail": "T001 先输出接口定义（TypeScript interface），T003 根据接口定义开始开发，无需等 T001 全部完成。",
    "contract": {
      "exported_by": "T001",
      "consumed_by": "T003",
      "interface_name": "WechatAuthService",
      "methods": [
        {"name": "generateQRCode", "params": "()", "returns": "{ qrcode_id: string, qrcode_url: string, expires_in: number }"}
      ]
    }
  }
}
```

### 4.5 交接校验（开发 → 测试）

```json:terminal
{
  "handoff_quality_gate": {
    "gate_name": "开发到测试的交接门禁",
    "checks": [
      {"check": "所有代码通过类型检查", "type": "阻塞"},
      {"check": "所有代码通过 lint", "type": "阻塞"},
      {"check": "每个文件有对应的单元测试", "type": "必填"},
      {"check": "代码审查无 BLOCKER 级别问题", "type": "阻塞"},
      {"check": "测试覆盖率 ≥ 80%", "type": "必填"}
    ]
  }
}
```

## 5. 阶段四：测试与部署

### 5.1 自动测试生成

Test Agent 根据源代码和用户故事自动生成测试用例：

```json:terminal
{
  "test_generation": {
    "us_id": "US-001",
    "generated_tests": {
      "unit_tests": [
        {"file": "tests/unit/wechat.service.test.ts", "test_count": 8},
        {"file": "tests/unit/wechat.controller.test.ts", "test_count": 6}
      ],
      "integration_tests": [
        {"file": "tests/integration/wechat-auth-flow.test.ts", "test_count": 3}
      ],
      "e2e_tests": [
        {"file": "cypress/e2e/wechat-login.cy.ts", "test_count": 2}
      ]
    },
    "coverage": {
      "lines": "92%",
      "branches": "85%",
      "functions": "100%"
    }
  }
}
```

### 5.2 CI/CD 集成

测试通过后自动进入部署流水线：

```json:terminal
{
  "ci_cd_pipeline": {
    "steps": [
      {"step": 1, "name": "Lint + Type Check", "parallel": true},
      {"step": 2, "name": "Unit Tests", "parallel": true},
      {"step": 3, "name": "Integration Tests", "depends_on": ["step 2"]},
      {"step": 4, "name": "E2E Tests", "depends_on": ["step 3"]},
      {"step": 5, "name": "Build", "depends_on": ["step 1"], "parallel": true},
      {"step": 6, "name": "Deploy to Staging", "depends_on": ["step 4", "step 5"]},
      {"step": 7, "name": "Smoke Tests", "depends_on": ["step 6"]},
      {"step": 8, "name": "Create PR to main", "depends_on": ["step 7"]}
    ],
    "coverage_gate": {
      "threshold": 80,
      "action_below": "阻断部署，生成测试覆盖报告"
    }
  }
}
```

### 5.3 PR 自动创建

流水线最后一步——自动创建 PR，附带完整变更摘要：

```json:terminal
{
  "auto_pr": {
    "title": "[US-001] 微信扫码登录功能",
    "body": {
      "summary": "实现微信扫码登录功能，用户可通过微信扫码直接登录平台",
      "changes": [
        "新增 API: POST /api/auth/wechat/qrcode — 生成二维码",
        "新增 API: GET /api/auth/wechat/callback — 微信回调",
        "新增 API: GET /api/auth/wechat/status — 轮询登录状态",
        "新增组件: WechatQRCode.tsx — 扫码弹窗组件",
        "新增数据表: wechat_bindings — 微信号绑定关系"
      ],
      "testing": {
        "unit_tests": 14,
        "integration_tests": 3,
        "e2e_tests": 2,
        "coverage": "92%"
      },
      "adr_ref": ["ADR-2024-003: 微信登录状态存储方案选择"],
      "reviewers": ["@tech-lead", "@frontend-lead"],
      "impact_analysis": {
        "new_dependencies": ["wechatify (v2.1.0)"],
        "config_changes": "需在 .env 中添加 WECHAT_APP_ID, WECHAT_APP_SECRET, WECHAT_QRCODE_TTL",
        "migration_required": true,
        "migration_file": "2024-03-21-create-wechat-bindings.sql"
      }
    }
  }
}
```

### 5.4 交接校验（PR 创建前）

```json:terminal
{
  "handoff_quality_gate": {
    "gate_name": "PR 最终门禁",
    "checks": [
      {"check": "所有测试通过", "type": "阻塞"},
      {"check": "测试覆盖率 ≥ 80%", "type": "阻塞"},
      {"check": "代码审查通过（无 BLOCKER）", "type": "阻塞"},
      {"check": "ADR 已记录本次变更的架构决策", "type": "必填"},
      {"check": "PR 包含变更摘要和影响分析", "type": "必填"},
      {"check": "新配置项在文档中注明", "type": "建议"}
    ],
    "auto_assign_reviewers": ["tech-lead", "根据 changed_files 自动匹配 owner"]
  }
}
```

### 5.5 上下文传递：隐形的流水线润滑剂

上述四道交接门禁保证了"格式正确"，但还有一个更隐蔽的问题：**上下文在阶段间传递时如何不被稀释或污染？** 需求阶段的业务背景、设计阶段的决策理由、开发阶段的实现约束——这些信息在流水线向前推进时容易丢失，导致下游 Agent 需要重复推理或产生理解偏差。

以下是三条来自上下文工程的实践原则，适用于流水线的每个交接点：

1. **决策理由优先于决策结果**。交接时传递的不只是"做了什么"，更是"为什么这么做"。例如，设计阶段的 ADR 记录（→ §3.2）不仅仅是一份归档文档，更是上下文工程的核心载体——它压缩了一个决策的完整推理链，下游 Agent 读 ADR 而不是读全部设计对话。一个 ADR 的 `rationale` 字段通常 50-100 字，却能替代数页的讨论记录。

2. **每个阶段只接收它需要的上下文（渐进式披露）**。需求 Agent 不需要知道数据库索引策略，实现 Agent 不需要知道用户访谈细节。在交接门禁的校验规则中，可以增加一条"上下文必要性检查"——检查传递信息中是否包含与目标阶段无关的上下文。无关上下文不仅是噪音，还会稀释 Agent 的注意力（上下文窗口有限，每 Token 都是成本）。

3. **模型切换时注入上下文摘要而非原始对话**。当流水线在不同阶段使用不同模型时（如需求用 DeepSeek、架构用 GPT-4o），直接传递完整前序对话会导致新模型的上下文被无关信息占满。应该在切换点生成一个结构化的上下文摘要（包含：已完成目标、关键决策、待办事项、风险项），摘要控制在 200 Token 以内。这与 → [案例：国产模型混合架构](case-multi-model.md) 中"模型切换上下文丢失"的应对策略一致，但适用范围更广——即使不切换模型，跨阶段交接时做上下文压缩也能显著减少 Token 消耗并提高 Agent 输出质量。

## 6. 效果指标与最佳实践

### 6.1 开发周期缩短

以下数据基于本流水线在目标团队运行 **6 个月（2024 年 H1）** 的实测统计：

```json:terminal
{
  "cycle_time": {
    "metric": "从需求确认到 PR 创建的平均时长",
    "before": "6.8 个工作日",
    "after": "1.2 个工作日",
    "improvement": "82.4% 缩短",
    "source": "对比：流水线前（2023 年 H2）从 Jira 需求状态 'Ready' 到 PR merged 的时间戳中位数；流水线后（2024 年 H1）同口径统计。（来源：Jira + GitHub API 数据导出）"
  },
  "human_effort": {
    "metric": "人工编码占开发总工时的比例",
    "before": "75%（写代码 + 审查 + 测试）",
    "after": "35%（审查 + 处理 Agent 无法独立完成的任务）",
    "source": "基于团队时间追踪工具 Toggl 的周报数据聚合。（来源：2024 年 Q1 团队 Sprint 复盘报告）"
  }
}
```

### 6.2 交付质量提升

```json:terminal
{
  "quality": {
    "test_coverage": {
      "before": "62% (line coverage)",
      "after": "89% (line coverage)",
      "improvement": "+27%",
      "source": "实测：Codecov 统计对比流水线前后各 3 个月的数据。（来源：Codecov dashboard 导出）"
    },
    "production_bugs": {
      "before": "平均每月 4.2 个线上 bug（P0+P1）",
      "after": "平均每月 1.1 个线上 bug（P0+P1）",
      "improvement": "73.8% 减少",
      "source": "实测：PagerDuty 告警 + Sentry error tracking 汇总。排除基础设施故障导致的告警。（来源：SRE 月度报告 2024-Q1 对比 2023-Q4）"
    },
    "revert_rate": {
      "before": "8.3% 的 PR 需要 revert",
      "after": "2.1% 的 PR 需要 revert",
      "source": "实测：git revert log 统计。（来源：仓库 git 日志分析脚本）"
    }
  }
}
```

### 6.3 人工介入频率

```json:terminal
{
  "human_intervention": {
    "total_prs": 186,
    "fully_automatic": 112,
    "pct_fully_automatic": "60.2%",
    "needed_minor_fix": 57,
    "pct_minor_fix": "30.6%",
    "needed_major_rewrite": 17,
    "pct_major_rewrite": "9.1%",
    "source": "实测：统计全部 186 个由流水线创建的 PR。'minor fix' 指审查者评论 < 5 条且无结构性修改；'major rewrite' 指需要大幅重写或重新设计的 PR。（来源：GitHub PR review 记录分析）"
  }
}
```

### 6.4 混合模型应用情况

```json:terminal
{
  "model_distribution": {
    "total_tokens_consumed": "4.2B tokens（6 个月累计）",
    "model_split": {
      "high_end": "28%（GPT-4 / Claude 3 Opus）— 用于架构设计、代码审查、复杂 bug 修复",
      "cost_effective": "72%（GPT-4o-mini / Claude 3 Haiku）— 用于测试生成、简单 CRUD、lint 修复"
    },
    "cost_savings": "相比全量使用高端模型节约约 65% 成本",
    "source": "实测：OpenCode 用量统计 Dashboard。（来源：2024 年 H1 基础设施费用报告）"
  },
  "recommendation": "经验法则：设计评审、安全审查、复杂重构用高端模型；测试生成、简单实现、格式化等常规任务用经济模型。门槛判断由 Agent 自动完成——检测到复杂度超过阈值后自动切换模型。"
}
```

### 6.5 最佳实践总结

```json:terminal
{
  "best_practices": [
    {
      "practice": "接口契约先行",
      "why": "多 Agent 并行时，先定义接口再各自实现，避免依赖阻塞",
      "example": "Backend Agent 先输出 TypeScript interface，Frontend Agent 立即开始 mock 开发"
    },
    {
      "practice": "交接点设质量门禁",
      "why": "每个阶段的输出质量影响下游效率",
      "example": "需求阶段输出 JSON Schema 校验不通过 → 不走下个阶段"
    },
    {
      "practice": "人工审核聚焦关键决策",
      "why": "不是所有决定都要人看，但架构设计、安全敏感变更必须人确认",
      "example": "ADR 中 'security' 标签的决策自动标记为需人工审核"
    },
    {
      "practice": "渐进式推广，不要一步到位",
      "why": "全流程自动化需要每个环节先稳定运行，逐个阶段上线",
      "example": "先跑通测试生成阶段（风险最小），再逐步引入代码生成和架构设计"
    }
  ],
  "common_traps": [
    {"trap": "一次性引入全流程", "consequence": "一个环节出问题阻塞整个流水线"},
    {"trap": "忽略模型 token 成本", "consequence": "月度 AI 成本超出预期 3-5 倍"},
    {"trap": "没有人工兜底机制", "consequence": "Agent 生成错误代码直接上线"},
    {"trap": "跳过需求验证直接编码", "consequence": "开发到一半发现需求理解偏差"},
    {"trap": "过度依赖自动生成测试", "consequence": "测试覆盖所有行但没覆盖任何业务逻辑"}
  ]
}
```

### 6.6 总结

| 维度 | 流水线前 | 流水线后 | 改善 |
|------|---------|---------|------|
| 需求 → PR 周期 | 6.8 天 | 1.2 天 | 82% 缩短 |
| 测试覆盖率 | 62% | 89% | +27% |
| 线上 P0/P1 bug | 4.2/月 | 1.1/月 | 74% 减少 |
| 人工编码工时 | 75% | 35% | 减轻 |
| 全自动 PR | — | 60.2% | — |

全流程自动化的本质不是机器代替人，而是机器承担标准化、重复性的劳动，让人专注于创造性的、需要判断力的工作。流水线在每个交接点设置的"门禁"就是"调查研究"——在做出下一个决策之前，先确保当前阶段的输出是可靠的。

## 7. CI/CD 集成

全流程自动化流水线需要与 CI/CD 系统集成，才能在生产中持续运行。以下是 GitHub Actions 和 GitLab CI 中使用 OpenCode headless 模式的完整配置。

### 7.1 GitHub Actions 集成

```yaml:src/07-case-studies/case-full-pipeline.md
# .github/workflows/opencode-pipeline.yml
name: OpenCode Full Pipeline

on:
  push:
    branches: [main]
  issue_comment:
    types: [created]

env:
  OPENCODE_API_KEY: ${{ secrets.OPENCODE_API_KEY }}
  ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}

jobs:
  ai-pipeline:
    runs-on: ubuntu-latest
    if: contains(github.event.comment.body, '/oc-run')
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Install OpenCode
        run: |
          curl -fsSL https://opencode.ai/install.sh | sh
          echo "$HOME/.local/bin" >> $GITHUB_PATH

      - name: Extract task from comment
        id: task
        run: |
          TASK=$(echo "${{ github.event.comment.body }}" | sed 's|/oc-run ||')
          echo "task=$TASK" >> $GITHUB_OUTPUT

      - name: Run OpenCode pipeline (headless)
        run: |
          opencode --headless \
            --model claude-sonnet-4-20250514 \
            --task "${{ steps.task.outputs.task }}" \
            --output-format json \
            > pipeline-result.json

      - name: Upload pipeline artifacts
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: opencode-pipeline-result
          path: |
            pipeline-result.json
            .opencode/audit.log

      - name: Create PR from result
        if: hashFiles('pipeline-result.json') != ''
        run: |
          BRANCH="oc/auto-$(date +%Y%m%d-%H%M%S)"
          git checkout -b "$BRANCH"
          # 根据 pipeline-result.json 中的变更创建 commit
          git add -A && git commit -m "feat: AI pipeline auto changes"
          git push origin "$BRANCH"
          gh pr create --fill --body "Auto-generated by OpenCode pipeline"
```

headless 模式（`--headless`）是 CI/CD 集成的关键，它跳过交互式 UI，直接执行任务并将结果输出为 JSON，适合在无人值守的流水线中运行。

### 7.2 GitLab CI 集成

```yaml:src/07-case-studies/case-full-pipeline.md
# .gitlab-ci.yml
stages:
  - ai-generate
  - build
  - test

ai-pipeline:
  stage: ai-generate
  image: opencode/opencode:latest
  variables:
    OPENCODE_API_KEY: $OPENCODE_API_KEY
    ANTHROPIC_API_KEY: $ANTHROPIC_API_KEY
  script:
    - |
      opencode --headless \
        --model claude-sonnet-4-20250514 \
        --task "根据 spec/$CI_MERGE_REQUEST_IID.md 生成实现代码" \
        --output-format json \
        > pipeline-result.json
  artifacts:
    paths:
      - pipeline-result.json
    expire_in: 30 days
  rules:
    - if: $CI_MERGE_REQUEST_IID
```

两种 CI 系统的关键差异：GitHub Actions 使用 `secrets` 管理敏感信息，GitLab CI 使用 `variables`。生产环境中务必通过 CI 系统的 Secret 管理功能注入 API Key，不要硬编码在配置文件中（→ [Secret 管理实践](../06-advanced/security-overview.md#secret-管理实践)）。

## 8. 生产环境部署指南

### 8.1 部署前检查清单

在生产环境运行流水线之前，逐项确认以下检查点：

| 检查项 | 验证命令 | 通过标准 |
|--------|----------|----------|
| API Key 有效 | `curl -s -H "Authorization: Bearer $KEY" https://api.anthropic.com/v1/messages -d '{}' \| jq .error` | 无 error 字段 |
| 模型访问权限 | `opencode --headless --task "echo hello" --model claude-sonnet-4-20250514` | 返回正常结果 |
| 磁盘空间充足 | `df -h /var/log/opencode` | 可用空间 > 5GB |
| 网络连通性 | `curl -s -o /dev/null -w "%{http_code}" https://api.anthropic.com` | 返回 200 |
| Git 凭证配置 | `git push --dry-run origin main` | 推送成功 |
| opencode.json 语法 | `python -m json.tool opencode.json > /dev/null` | 无语法错误 |

### 8.2 生产环境配置差异

开发环境和生产环境的 `opencode.json` 有几个关键区别需要调整：

```json:src/07-case-studies/case-full-pipeline.md
{
  "production_overrides": {
    "permission": {
      "read": "allow",
      "edit": "ask",
      "commands": {
        "git": "allow",
        "npm test": "allow",
        "rm -rf": "deny"
      }
    },
    "telemetry": {
      "logging": {
        "level": "warn",
        "format": "json",
        "output": "/var/log/opencode/opencode.log"
      }
    },
    "limits": {
      "maxTokensPerSession": 500000,
      "maxToolCallsPerSession": 500,
      "sessionTimeoutMinutes": 60
    },
    "security": {
      "yolo": { "enabled": false },
      "prompt_injection": { "enabled": true }
    }
  }
}
```

生产环境的三处关键调整：权限从 `ask` 收紧为选择性 `allow`/`deny`；日志级别从 `info` 调为 `warn` 减少噪音；限制单次 Session 的 Token 和工具调用上限，防止 Agent 循环耗尽资源。

### 8.3 常见部署故障排查

| 故障现象 | 可能原因 | 排查步骤 |
|----------|----------|----------|
| `API key not valid` | Key 过期或环境变量未注入 | 1. 检查 `echo $ANTHROPIC_API_KEY` 2. 在模型提供商控制台确认 Key 状态 |
| `Permission denied` | 权限配置阻止操作 | 检查 `opencode.json` 中 `permission` 配置，确认目标操作不在 deny 列表中 |
| `Session timeout` | 任务复杂度超过超时限制 | 调大 `sessionTimeoutMinutes` 或拆分任务 |
| `Token quota exceeded` | 配额用尽 | 检查 `maxTokensPerSession` 设置，在模型提供商控制台查看用量 |
| 磁盘写满 | 审计日志或遥测数据未轮转 | 配置 `retention_days` 和 `logrotate`，确保日志有清理策略 |

## 常见反模式

**反模式一：试图自动化一切，完全消除人工环节。** 全流程自动化流水线的设计初衷是让机器承担重复性工作，但有些团队在实践中走向极端——试图连架构评审、安全审查、需求确认等需要判断力的环节也完全自动化。本案例的数据显示，即使流水线运行成熟后，仍有约 9% 的 PR 需要大幅重写（§6.3），这说明存在一类问题是当前 Agent 能力无法独立处理的。去掉人工审核环节后，这些 PR 的错误代码会直接进入主干分支。正确做法是为每个交接门禁设置人工会签条件：涉及安全敏感变更、架构决策、或 Agent 评分低于阈值时，自动标记为需人工审核。

**反模式二：在单个环节未验证前就搭建完整流水线。** 流水线四个阶段（需求→设计→开发→测试→PR）是串行依赖关系——上游的缺陷会逐级放大到下游。跳过阶段性验证直接搭建全链条，会导致需求理解偏差被传递到代码阶段才发现，返工成本比单阶段迭代高出 5-10 倍。本案例的实践顺序是：先单独跑通测试生成阶段（风险最低，收益可量化），再引入代码生成和架构设计，最后才接入需求分析。每接入一个阶段，都运行至少两周观察其输出质量，再决定是否串联到下一级。

**反模式三：流水线拓扑过度复杂。** 在项目中看到过一些团队设计了高度复杂的多 Agent 协作拓扑——角色 Agent、路由 Agent、仲裁 Agent、审计 Agent 一应俱全，结果光 Agent 间的通信和协调就占了总 Token 消耗的 40% 以上（来源：本案例 6 个月运行实测，Telemetry 数据分析）。实际上本案例只用了一个扁平结构（需求 Agent→架构 Agent→多 Dev Agent→审查 Agent），没有多级路由和仲裁层。复杂度增加并不会线性提升输出质量，反而提高了故障排查难度。一条好流水线的判断标准是：新成员能在 30 分钟内理解全流程拓扑。

**反模式四：忽略上下文传递成本。** 每个阶段交接时，如果直接将前序 Agent 的完整对话历史传给下游 Agent，会导致两个问题：一是无关上下文稀释注意力，二是 Token 消耗急剧上升。本案例实测数据显示，不经压缩的完整对话传递，阶段间 Token 消耗增加 3-5 倍。解决方案是在每个交接点做上下文摘要压缩（见 §5.5），将关键信息提炼为结构化摘要而非原始对话。

## 常见错误与陷阱

**陷阱一：需求含混不清，导致级联失效。** 流水线的起点是自然语言需求，如果产品经理输入的需求本身存在歧义或遗漏边界条件，这个缺陷会被每一级 Agent 放大。例如，某次实践中产品经理说"支持用户通过微信扫码登录"，但没有说明"已注册用户"和"未注册用户"的处理差异。架构 Agent 生成的方案只覆盖了已注册场景，代码 Agent 没处理异常路径，直到测试阶段才发现微信回调后无法区分新老用户。修复成本从需求阶段的 5 分钟澄清变成了跨三个阶段的 PR 重开。解决方案是需求阶段的 INVEST 检查（§2.2）必须严格执行，尤其关注"缺失的边界条件"这个检查项——团队规定任何包含"未定义行为"的 US 不得流向下游。

**陷阱二：AI 生成代码通过所有测试但存在逻辑缺陷。** 这是全流程自动化中最隐蔽的问题。代码 Agent 生成的方法可能会覆盖所有测试路径，但实现了一个"错误的正确版本"——接口符合预期，行为也通过了单元测试，但业务逻辑的隐含假设是错误的。本案例中发生过一次：测试 Agent 生成的测试代码延续了实现 Agent 相同的错误假设，导致双方"互相印证"，人工审查者也没有注意到深层逻辑问题。后来在集成测试阶段才发现微信回调的 state 参数校验逻辑不完整。解决方案是在代码审查 Agent 的评分规则中加入"业务逻辑合理性"维度，并要求每个 PR 至少有一位了解业务上下文的开发者人工审查。

**陷阱三：Prompt 随时间漂移——Agent 行为退化。** 流水线运行数月后，可能会出现 Agent 输出质量逐步下降的现象。原因不是 Agent 本身变了，而是上游的 Prompt 指令被多次调整后产生了语义漂移。例如，团队为了修复某个特定 bug 在需求 Agent 的 system prompt 中加了一条"注意：微信扫码登录需要考虑苹果手机兼容性"，几周后又加了"注意：异常日志级别设为 debug"，这些临时补丁式的 Prompt 修改相互叠加，让 Agent 越来越倾向于输出过度保守的实现，反而忽略了用户故事的核心路径。本案例的经验是：对 Prompt 变更使用版本管理（Git 跟踪），每季度做一次 Prompt 清理，移除已过时的指令。

**陷阱四：成本失控——Token 消耗比预期高出 3-5 倍。** §6.4 的模型分配数据（高端模型 28%、经济模型 72%）来自本案例运行 6 个月后的优化结果。在运行初期，团队没有做模型路由，所有阶段使用同一款高端模型，月度 AI 成本直接透支了预算。同样容易忽略的是重试成本：流水线中某个 Agent 执行失败后自动重试，如果不设置重试次数上限，一次故障可能触发 10+ 次重试，消耗数万 Token。建议在 opencode.json 中设置 `maxRetriesPerTask: 3`，并为每个阶段设置独立的 Token 预算上限。

**陷阱五：测试覆盖率数值好看但实际覆盖不足。** 自动生成的测试倾向于覆盖"容易覆盖的路径"——正常路径、单参数边界值、常规错误处理。但业务最关心的异常组合场景、并发冲突、资源泄露等深层问题，自动测试很难覆盖。本案例初期测试覆盖率达到 92%，但线上 bug 中仍有 30% 是由组合条件触发的。团队后来采取的策略是：自动测试覆盖 80% 基础路径，剩余 20% 的边界条件由人工编写集成测试，并作为"PR 门禁"的必选项（§5.4）。

## 适用场景与限制

**不适合场景一：高度创新或探索性工作。** 全流程自动化的核心优势在于标准化和效率，这在需求明确、实现路径清晰的场景下表现突出。但对于需要创新设计、探索未知技术方案、或者"不知道正确路径是什么"的任务，流水线的线性结构反而会成为束缚。本案例中遇到过一个问题：一个涉及新支付渠道集成的任务，架构 Agent 生成了标准的 OAuth 方案，但业务实际需要一个创新的"先交易后绑定"模式，Agent 无法跳出常见模式来设计。对于这类任务，建议的做法是先由人工完成探索和原型设计，再交给流水线执行标准化的实现部分。

**不适合场景二：需要深度领域知识的专业领域。** 金融合规计算、医疗数据处理、法律条款解析等需要深厚领域知识的任务，当前 Agent 的能力边界决定了它容易遗漏一些"从业者一眼就能看出的问题"。例如，在合规相关的需求上，Agent 可能会生成符合技术规范但违反监管要求的代码。如果团队中缺乏具备对应领域知识的人来做复审，流水线上线这类功能的返工风险很高。本案例的建议是：在流水线中加入"领域知识门禁"——对于标记为合规/财务/医疗的 PR，自动增加一名有对应领域背景的审核人，且该审核人不能省略。

**不适合场景三：团队规模小于 5 人。** 全流程自动化的收益与团队规模呈正相关——一个 10 人团队（本案例的目标团队规模）通过流水线节省了 40% 的编码工时，这些节省的时间被重新分配给审核和架构决策。但一个 3-5 人的小团队面临的情况不同：流水线本身的维护成本（Prompt 管理、故障排查、质量监控）占用了本就不多的工程资源，而团队小型化意味着人工审核环节的瓶颈更严重。本案例的经验阈值是：团队至少需要一个人全职负责流水线的运维和持续优化，这在 10 人团队中占 10%，但在 5 人团队中占 20%——不划算。小团队更适合从单个环节（如自动测试生成）开始，而非全流程。

**不适合场景四：高度合规或审计密集型环境。** 金融、医疗、政务等行业的合规要求通常涉及严格的变更审批流程和审计追溯——每一次代码变更都需要对应审批记录，每个决策都需要人工签名。全流程自动化追求的"效率最大化"与合规环境的"审批完整性"之间存在根本张力。本案例在 CI/CD 集成部分（§7）展示了如何将流水线嵌入已有的合规流程，但对于"每次部署都需要合规官签字"的场景，自动化流水线的加速效果会被合规审批流程完全抵消。在这些环境中，更实际的做法是只自动化那些"合规上无争议"的环节（如测试生成、代码格式化），而保留完整的审批链条。

## 关联章节

- ← [案例一：从零搭建微服务](real-world-01.md)（本案例的流程模板来源）
- → [案例：国产模型混合架构](case-multi-model.md)（混合架构在全流程中的应用）
- ← [工作流实战](../04-workflows/)（多 Agent 协作基础）
- ← [**Skill（技能）** 开发](../05-skills/)（自定义 Skill 在流水线各环节的应用）
