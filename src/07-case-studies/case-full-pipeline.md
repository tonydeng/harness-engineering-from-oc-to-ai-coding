# 案例：全流程自动化

> 从自然语言的需求描述到自动创建的 PR，构建一条端到端的 AI 驱动开发流水线。关键洞察：自动化不等于无人化，人的角色从"执行者"转变为"审核者"。

## 案例概述

本案例的目标是构建一条从需求到 PR 的全流程自动化流水线——产品经理输入自然语言需求，流水线自动完成用户故事编写、架构设计、代码实现、测试生成和 PR 创建。这不是一个"把开发者替换掉"的尝试，而是一个"让开发者聚焦于更高价值工作"的工程实践。读完本文，你将理解如何构建一条从自然语言需求到自动创建 PR 的端到端 AI 驱动开发流水线。

流水线按四个阶段串联：需求分析阶段将自然语言转化为结构化的用户故事，并经过自动评审；架构设计阶段由 Agent 生成技术方案，记录 ADR（架构决策记录），经过人工或自动评审后进入开发阶段；代码实现阶段启用多 Agent 并行开发，每个 Agent 负责独立的模块，配合代码审查自动化；最后自动生成测试、集成到 CI/CD、创建 PR 并附上变更摘要。

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

## 关联章节

- ← [案例一：从零搭建微服务](real-world-01.md)（本案例的流程模板来源）
- → [案例：国产模型混合架构](case-multi-model.md)（混合架构在全流程中的应用）
- ← [工作流实战](../04-workflows/)（多 Agent 协作基础）
- ← [Skill 开发](../05-skills/)（自定义 Skill 在流水线各环节的应用）
