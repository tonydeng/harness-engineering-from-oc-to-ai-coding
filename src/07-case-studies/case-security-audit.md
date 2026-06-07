# 案例：安全审计流水线

> 在 CI/CD 中嵌入红队+蓝队全流程安全审计，将渗透测试从"季度专项"升级为"持续活动"。

## 案例概述

传统安全审计的模式是"季度扫描 + 年度渗透测试"——频率低、周期长、发现问题时漏洞可能已在生产环境存在数月。本案例展示如何利用 OpenCode 的 `security-research` 团队，构建一条自动化安全审计流水线，将安全审计嵌入到日常开发流程中。读完本文，你将理解如何用红蓝对抗模式在 CI/CD 中嵌入持续化的安全审计能力。

流水线的核心设计遵循**红蓝对抗**模式：红队阶段负责发现漏洞——自动执行 SQL 注入/XSS/CSRF 等 Web 漏洞扫描、依赖 CVE 检测、配置敏感信息泄露检查；蓝队阶段负责修复验证——根据红队报告自动生成修复方案、配置安全基线、执行二次扫描确认修复生效。两个阶段形成"发现 → 修复 → 验证"的闭环，每次 CI 构建都会触发。

流水线的关键能力是**自动 CVSS 评分**：基于 OWASP 评分标准和上下文信息自动计算严重程度，结合人工复核生成最终的安全决策。设计中还融入了 **STRIDE 威胁建模**方法，确保审计范围对系统关键威胁面的全面覆盖。评估指标方面，本案例重点对比了自动化流水线与传统人工审计的扫描速度、漏洞检出率和修复成功率。

> **⏱ 时间有限？先读这些：** 红队阶段 → 蓝队阶段 → STRIDE 威胁建模 → 自动化流程设计

## 1. 项目背景

### 为什么是"知彼知己"？

安全领域有一条核心原则：**"知彼知己，百战不殆"**——"彼"是攻击者，他们的手法、工具链、攻击入口；"己"是系统自身，我们的代码、依赖、配置、运行时暴露面。

传统安全审计为什么低效？一年只做一两次"知己"，而攻击者每天都在"知彼"。信息不对称，防守方永远慢半拍。本案例的目标是构建一条**持续化的安全审计流水线**，让"知己"成为每次代码变更的例行检查，而不是季度专项。

### 目标系统

审计对象是一个典型的 Web 电商应用，微服务架构：

```json
{
  "target_app": "Harness Commerce Platform",
  "tech_stack": {
    "frontend": "React 18 + TypeScript + Vite",
    "backend": ["Node.js (Express) — API Gateway", "Python (FastAPI) — 订单服务"],
    "database": "PostgreSQL 15",
    "cache": "Redis 7",
    "message_queue": "RabbitMQ",
    "infra": "Docker Compose (dev) / Kubernetes (prod)"
  },
  "auth": "JWT-based + OAuth 2.0 (Google/GitHub)",
  "exposure": "公网电商平台，日均请求 ~50 万次"
}
```

### 审计范围

审计覆盖四个层次，每个层次对应不同的攻击面：

| 层次 | 范围 | 对应攻击面 |
|------|------|-----------|
| 代码层 | 业务逻辑、API 路由、认证中间件 | SQL 注入、XSS、CSRF、逻辑漏洞 |
| 依赖层 | npm + pip 依赖清单 | 已知 CVE、供应链投毒 |
| 配置层 | 环境变量、Dockerfile、K8s manifest | 硬编码密钥、错误配置 |
| 运行时层 | 容器、网络策略、TLS 设置 | 容器逃逸、中间人攻击、开放端口 |

### 关键设计原则

| 原则 | 说明 |
|------|------|
| 持续审计 | 每次 CI 构建触发审计，不等待季度窗口 |
| 红蓝闭环 | 红队扫描 → 蓝队修复 → 红队复扫，直到清零 |
| 自动评分 | CVSS 自动计算 + 人工复核双轨制 |
| 威胁驱动 | STRIDE 建模先行，审计用例与威胁直接映射 |

## 2. 红队阶段

红队阶段的核心：**假设攻击者视角，找到所有能利用的入口**。"战略上藐视敌人，战术上重视敌人"——不害怕漏洞的存在，但每个漏洞都要认真对待。

### 2.1 自动化漏洞扫描工具链

流水线集成三款工具，覆盖常见 Web 漏洞：

```json
{
  "red_team_scan_tools": {
    "zap": {
      "tool": "OWASP ZAP 主动扫描",
      "target": "API 端点 + 前端页面",
      "coverage": ["SQLi", "XSS", "CSRF", "XXE", "SSRF"],
      "mode": "全量扫描（首次）/ 增量扫描（后续 CI）"
    },
    "semgrep": {
      "tool": "Semgrep 静态分析",
      "target": "源代码 (JS/TS/Python)",
      "focus": ["硬编码密钥", "危险函数", "不安全的反序列化", "路径遍历"],
      "rules": "OWASP Top 10 规则集 + 自定义安全规则"
    },
    "trivy": {
      "tool": "Trivy 容器 + 依赖扫描",
      "target": "Docker images + package.json / requirements.txt",
      "focus": ["CVE 数据库匹配", "错误配置检查", "SBOM 生成"]
    }
  }
}
```

扫描命令（可直接在 CI 中运行）：

```bash
# OWASP ZAP 扫描 API
docker run -v $(pwd):/zap/wrk ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py -t https://staging.example.com/openapi.json \
  -f openapi -r zap_report.html

# Semgrep 静态扫描
docker run --rm -v $(pwd):/src returntocorp/semgrep:latest \
  semgrep --config=auto --config=./security-rules/ \
  --json-output=semgrep_results.json /src

# Trivy 依赖扫描
docker run --rm aquasec/trivy:latest \
  fs --severity=CRITICAL,HIGH --format json \
  --output trivy_results.json /workspace
```

### 2.2 依赖 CVE 检测

依赖风险常被忽视。攻击者更可能通过已知 CVE 的 npm 包打进系统，而不是从零挖 0day。流水线在每次构建时自动比对依赖清单与 CVE 数据库：

```json
{
  "dependency_scanning": {
    "upstream": "osv.dev API + NVD feed（每小时同步）",
    "check_frequency": "每次 CI 构建 + 定时每日全量扫描",
    "action_on_critical": "阻断流水线 + 发送告警到 #security Slack",
    "action_on_high": "记录到安全工单，24h 内要求修复",
    "output_format": "SARIF（支持 GitHub Security Tab 集成）"
  }
}
```

### 2.3 配置审计

配置风险不是 bug，而是"错误的设定"——比代码漏洞更难发现，因为不会触发编译错误。流水线重点检查三类：

**硬编码密钥扫描**：规则覆盖 AWS key、GitHub token、JWT secret、数据库密码等常见模式：

```json
{
  "secret_detection_rules": {
    "patterns": [
      "(?i)(?:password|secret|token|api[_-]?key).{0,5}=['\"][^'\"]{8,}['\"]",
      "(?i)-----BEGIN (RSA |EC )?PRIVATE KEY-----",
      "ghp_[0-9a-zA-Z]{36}", "sk_live_[0-9a-zA-Z]{24}",
      "AKIA[0-9A-Z]{16}"
    ],
    "action": "阻断流水线 + 通知安全团队 + 自动轮换（如密钥托管在 Vault）"
  }
}
```

**安全响应头检查**：每次部署前验证 HTTP 响应头配置：

| 检查项 | 要求 | 不配置的风险 |
|--------|------|------------|
| Content-Security-Policy | 禁止 `unsafe-inline` | XSS 执行任意脚本 |
| X-Content-Type-Options | `nosniff` | MIME 类型混淆攻击 |
| Strict-Transport-Security | `max-age=63072000` | TLS 降级攻击 |
| X-Frame-Options | `DENY` | 点击劫持 |

**TLS 配置检查**：验证证书有效期、TLS 版本（不低于 1.2，推荐 1.3）、密码套件强度。

### 2.4 红队审计报告结构

红队输出一份结构化的 JSON 报告，包含每个漏洞的完整上下文：

```json
{
  "red_team_report": {
    "report_id": "RED-2024-03-21-001",
    "scan_timestamp": "2024-03-21T14:30:00Z",
    "pipeline_run_id": "gha-run-84729",
    "summary": {
      "total": 17,
      "critical": 2, "high": 5, "medium": 7, "low": 3
    },
    "vulnerabilities": [
      {
        "id": "VULN-001",
        "type": "SQL Injection",
        "location": "backend/order_service/app.py:142",
        "severity": "CRITICAL",
        "cvss_score": 9.1,
        "cvss_vector": "CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:N",
        "description": "订单搜索接口未做参数化查询，直接拼接用户输入",
        "exploit": "curl -X POST https://example.com/api/orders/search -d '{\"q\":\"' OR 1=1--\"}'",
        "remediation": "改用参数化查询，替换 f-string 拼接",
        "fp_risk": "低——已手动验证确认"
      },
      {
        "id": "VULN-002",
        "type": "Hardcoded Secret",
        "location": "backend/.env.example:5",
        "severity": "CRITICAL",
        "cvss_score": 8.6,
        "description": "文件包含明文 AWS_SECRET_ACCESS_KEY",
        "remediation": "1) 从 git 历史清除该密钥 2) 轮换 AWS 凭证 3) 添加禁止规则",
        "fp_risk": "确认是真实密钥——已在 AWS IAM 验证"
      },
      {
        "id": "VULN-003",
        "type": "Missing CSP Header",
        "location": "frontend/nginx.conf:12",
        "severity": "MEDIUM",
        "cvss_score": 6.1,
        "description": "Nginx 响应头未配置 CSP",
        "remediation": "添加: default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'",
        "fp_risk": "无——配置缺失是明确问题"
      }
    ],
    "recommendations": [
      "立即修复 2 个 CRITICAL 漏洞，预计 4h",
      "HIGH 漏洞纳入本周 Sprint，分配给后端团队",
      "修复后触发二次扫描"
    ],
    "attachments": {
      "zap_html": "zap_report.html",
      "semgrep_sarif": "semgrep_results.sarif",
      "trivy_json": "trivy_results.json"
    }
  }
}
```

### 2.5 误报过滤机制

自动化扫描必有误报。三层过滤降低噪音：

| 层级 | 方法 | 降低误报 | 实现方式 |
|------|------|----------|---------|
| 规则过滤 | 静态白名单排除 test/mock 目录 | ~40% | Semgrep path-include/exclude |
| 关联分析 | 跨工具交叉验证 | ~25% | 同一漏洞被 ZAP + Semgrep 同时确认才标 True |
| 人工复核 | 安全工程师 Dashboard 标记 | ~15% | 反馈闭环更新规则池 |

**实测结果**：30 天连续运行，最终误报率 **13.4%**（来源：安全工程师逐条确认）。

## 3. 蓝队阶段

红队负责"发现问题"，蓝队负责"解决问题"。这是一个典型的"发现 → 分析 → 验证"闭环：红队报告是原始发现，蓝队的修复方案和基线配置是系统分析，二次扫描验证是最终确认。

### 3.1 自动修复方案生成

每个漏洞按类型匹配对应的修复模板：

```json
{
  "blue_team_auto_fix": {
    "vuln_id": "VULN-001",
    "type": "SQL Injection",
    "file": "backend/order_service/app.py",
    "original_code": "query = f\"SELECT * FROM orders WHERE user_id = '{user_input}'\"",
    "fix": {
      "type": "参数化查询替换",
      "code": "query = \"SELECT * FROM orders WHERE user_id = %s\"\ncursor.execute(query, (user_input,))",
      "confidence": "高——标准修复模式",
      "test_script": "curl -X POST /api/orders/search -d '{\"q\":\"test\"}'  # 应返回 200\ncurl -X POST /api/orders/search -d '{\"q\":\"' OR 1=1--\"}'  # 应返回 400"
    }
  }
}
```

配置类漏洞的修复直接生成 patch：

```json
{
  "blue_team_config_fix": {
    "vuln_id": "VULN-003",
    "file": "frontend/nginx.conf",
    "patch": "add_header Content-Security-Policy \"default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'\";",
    "verification": "curl -sI https://staging.example.com | grep -i content-security-policy"
  }
}
```

### 3.2 安全基线配置

蓝队产出一个**可执行的安全基线**——不是一个 PDF 文档，而是一个 JSON 规则集，流水线每次部署前自动检查：

```json
{
  "security_baseline": {
    "http_headers": {
      "Content-Security-Policy": "必须配置，禁止 'unsafe-inline'",
      "X-Content-Type-Options": "nosniff",
      "X-Frame-Options": "DENY",
      "Strict-Transport-Security": "max-age=63072000; includeSubDomains",
      "Referrer-Policy": "strict-origin-when-cross-origin"
    },
    "auth": {
      "password_min_length": 12,
      "mfa_required": true,
      "session_timeout_minutes": 30,
      "jwt_expiry": "15min (access) / 7d (refresh)"
    },
    "network": {
      "tls_version": "TLS 1.3 only",
      "cors_origin_whitelist": ["https://example.com", "https://*.example.com"],
      "rate_limiting": "100 req/min per IP"
    },
    "container": {
      "run_as_non_root": true,
      "read_only_root_fs": true,
      "drop_capabilities": ["ALL"],
      "no_new_privileges": true
    }
  }
}
```

### 3.3 二次扫描验证

修复提交后自动触发复扫：

```json
{
  "secondary_scan": {
    "vuln_id": "VULN-001",
    "method": "重复 ZAP 扫描 + 手动 payload 验证",
    "result": "端点不再对 SQL 注入 payload 返回异常响应",
    "status": "FIXED",
    "confirmed_by": "Auto-Verification Engine (2024-03-21T16:45:00Z)",
    "regression_check": "相关测试用例通过（含新增的 3 个 SQLi 安全测试）"
  }
}
```

### 3.4 蓝队输出结构

```json
{
  "blue_team_report": {
    "report_id": "BLUE-2024-03-21-001",
    "red_report_ref": "RED-2024-03-21-001",
    "fix_summary": {
      "total_fixed": 15,
      "critical": 2, "high": 5, "medium": 6, "low": 2,
      "not_fixed": [
        {"id": "VULN-007", "reason": "CSP 收紧影响第三方支付回调，需人工评估"},
        {"id": "VULN-012", "reason": "依赖包 CVE 等待上游补丁"}
      ]
    },
    "baseline_updated": true,
    "verification": [
      {"vuln_id": "VULN-001", "status": "FIXED", "verified_at": "2024-03-21T16:45:00Z"},
      {"vuln_id": "VULN-002", "status": "FIXED", "verified_at": "2024-03-21T16:50:00Z"}
    ],
    "open_items": ["VULN-007 → Sprint 2 完成", "VULN-012 → 设置 watch，上游发布后自动修复"]
  }
}
```

## 4. STRIDE 威胁建模

没有威胁建模的审计，等于没有地图的侦察。你会在某些地方挖得很深，但也可能错过了真正的入口。STRIDE 提供了结构化的"敌情分析方法论"。

### 4.1 系统数据流图

```
  [用户] ---HTTPS---> [Nginx Ingress] ---> [API Gateway (Express)]
                                                      |
                     +--------------------------------+--------------------------------+
                     |                                |                                |
              [前端静态资源]                    [订单服务 (FastAPI)]              [认证服务 (Express)]
                     |                                |                                |
               [CDN/CloudFront]                [PostgreSQL 15]                  [Redis Session]
                     |                                |                                |
              [浏览器端渲染]                   [RabbitMQ（订单异步处理）]         [OAuth Provider]
```

### 4.2 STRIDE 逐类分析

```json
{
  "stride_analysis": {
    "spoofing": {
      "description": "冒充合法用户或服务身份",
      "threats": [
        "JWT 缺乏签名验证 → 伪造任意用户",
        "OAuth callback 缺 state 参数 → CSRF 攻击 OAuth 流程",
        "内部服务间无 mTLS → 伪造内部请求"
      ],
      "audit_cases": [
        "检查 JWT 签名算法配置（拒绝 none 算法）",
        "验证 OAuth state 参数校验",
        "检查服务间认证（mTLS / Token）"
      ],
      "cvss_range": "7.5 - 9.0"
    },
    "tampering": {
      "description": "篡改传输中或存储中的数据",
      "threats": [
        "API 请求体未签名 → 中间人篡改订单金额",
        "日志未防篡改 → 攻击者掩盖痕迹",
        "数据库未加密 → 直接文件读取泄露数据"
      ],
      "audit_cases": [
        "检查 HTTPS 是否强制 (HSTS)",
        "验证请求体签名机制",
        "检查数据库加密（TDE / 列级加密）"
      ],
      "cvss_range": "6.5 - 8.5"
    },
    "repudiation": {
      "description": "否认已执行的操作",
      "threats": [
        "关键操作无审计日志",
        "日志缺用户标识 → 无法追溯"
      ],
      "audit_cases": [
        "检查审计日志覆盖（CRUD 操作、权限变更）",
        "验证日志包含 user_id + timestamp + action_type"
      ],
      "cvss_range": "4.0 - 6.0"
    },
    "information_disclosure": {
      "description": "敏感信息泄露给未授权方",
      "threats": [
        "API 错误返回完整堆栈 → 泄露代码路径",
        "S3 bucket 公共读取 → 用户数据泄露",
        "响应头泄露 nginx 版本 → 辅助定向攻击",
        "GraphQL introspection 未关闭 → 泄露全部 schema"
      ],
      "audit_cases": [
        "配置统一错误响应格式",
        "检测云存储 ACL 配置",
        "检查响应头信息泄露",
        "检查 GraphQL introspection 开关"
      ],
      "cvss_range": "6.0 - 9.5"
    },
    "denial_of_service": {
      "description": "耗尽系统资源导致服务不可用",
      "threats": [
        "API 缺限流 → 请求洪泛拖垮数据库",
        "正则 ReDoS → 特定输入阻塞 CPU",
        "未限制分页大小 → 大 offset 导致数据库 OOM"
      ],
      "audit_cases": [
        "验证速率限制配置",
        "检查正则是否存在 ReDoS 风险",
        "确认自动扩缩容策略",
        "检查分页参数上限"
      ],
      "cvss_range": "5.0 - 7.5"
    },
    "elevation_of_privilege": {
      "description": "低权限用户获取高权限访问",
      "threats": [
        "管理 API 缺角色校验 → 普通用户调用管理员接口",
        "IDOR → 用户 A 访问用户 B 的订单",
        "JWT payload 可伪造 → 修改 role 字段提权"
      ],
      "audit_cases": [
        "检查每个 API 路由的角色中间件",
        "验证资源 ID 属主检查逻辑",
        "测试水平 + 垂直越权场景",
        "检查 JWT payload 签名验证"
      ],
      "cvss_range": "7.0 - 9.5"
    }
  }
}
```

### 4.3 威胁到审计用例的映射

| STRIDE 类别 | 威胁数 | 审计用例数 | 覆盖工具 |
|-------------|--------|-----------|---------|
| Spoofing | 3 | 6 | ZAP (auth bypass) + Semgrep (JWT) |
| Tampering | 4 | 8 | ZAP (参数篡改) + 配置检查 (TLS) |
| Repudiation | 2 | 4 | 自定义审计脚本 (日志检查) |
| Information Disclosure | 5 | 10 | ZAP (信息泄露) + Trivy (配置) |
| Denial of Service | 4 | 6 | 负载测试工具 + Semgrep (ReDoS) |
| Elevation of Privilege | 4 | 8 | ZAP (越权) + 自定义 fuzzer |
| **合计** | **22** | **42** | — |

## 5. 自动化流程设计

### 5.1 security-research 团队配置

```json
{
  "teams": {
    "security-research": {
      "agents": [
        {
          "name": "threat-model-agent",
          "role": "威胁建模分析师",
          "tools": ["stride_analyzer", "dfd_builder", "audit_case_generator"],
          "inputs": ["系统架构文档", "数据流图"],
          "outputs": ["STRIDE 分析报告", "审计用例清单"]
        },
        {
          "name": "red-team-agent",
          "role": "红队扫描员",
          "tools": ["zap_scanner", "semgrep_runner", "trivy_runner", "secret_detector"],
          "inputs": ["源代码路径", "API 端点列表", "依赖清单"],
          "outputs": ["结构化漏洞报告（含 CVSS）"]
        },
        {
          "name": "blue-team-agent",
          "role": "蓝队修复员",
          "tools": ["fix_generator", "baseline_checker", "secondary_scanner"],
          "inputs": ["红队报告", "安全基线配置"],
          "outputs": ["修复方案", "安全基线文档", "验证报告"]
        },
        {
          "name": "cvss-engine",
          "role": "CVSS 评分引擎",
          "tools": ["cvss_calculator", "context_analyzer"],
          "inputs": ["漏洞信息", "系统上下文"],
          "outputs": ["CVSS 分数和向量"]
        }
      ],
      "workflow": "threat-model → red-team → cvss-engine → blue-team → red-team (verify)"
    }
  }
}
```

### 5.2 Agent 工作流编排

流水线六步执行顺序：

```
Step 1: Threat Model Agent
        输入: 系统架构文档
        输出: STRIDE 分析 + 审计用例清单
        触发: 每日定时 / 架构变更事件

Step 2: Red Team Agent
        输入: 审计用例 + 源代码 + API 端点
        输出: 原始扫描结果 (ZAP/Semgrep/Trivy JSON)
        触发: 每次代码推送

Step 3: CVSS Scoring Engine
        输入: 原始扫描结果 + 系统上下文
        输出: CVSS 评分的结构化漏洞报告
        处理: 规则引擎计算 base score + 上下文调整

Step 4: Blue Team Agent
        输入: CVSS 漏洞报告
        输出: 修复方案 + 安全基线更新
        触发: 自动（CRITICAL/HIGH）/ 人工确认后（MEDIUM）

Step 5: Red Team Agent (复扫)
        输入: 修复后的代码 + 配置
        输出: 二次扫描报告
        触发: 修复提交后自动

Step 6: 闭环判断
        逻辑: 如果二次扫描仍有漏洞 → 回到 Step 4
              如果全部修复 → 生成最终安全报告 → 关闭工单
```

### 5.3 自动 CVSS 评分引擎

```json
{
  "cvss_scoring_engine": {
    "base_metrics": {
      "attack_vector": {"Network": 0.85, "Adjacent": 0.62, "Local": 0.55, "Physical": 0.2},
      "attack_complexity": {"Low": 0.77, "High": 0.44},
      "privileges_required": {"None": 0.85, "Low": 0.62, "High": 0.27},
      "user_interaction": {"None": 0.85, "Required": 0.62}
    },
    "context_adjustments": [
      {"condition": "auth_bypassed", "boost": 0.5},
      {"condition": "sensitive_data_exposed", "boost": 0.3},
      {"condition": "public_exploit_available", "boost": 0.7},
      {"condition": "has_mitigation_workaround", "penalty": -0.5}
    ],
    "review_threshold": {
      "CRITICAL": "自动决策 + Slack 通知",
      "HIGH": "自动决策 + 创建 Jira ticket",
      "MEDIUM": "自动决策 + 合并到下次 Sprint",
      "LOW": "自动决策 + 记录到安全日志"
    }
  }
}
```

### 5.4 CI/CD 集成（GitHub Actions）

```json
{
  "ci_integration": {
    "triggers": [
      "push to main / release branches",
      "PR labeled 'security-review'",
      "schedule: daily 02:00 UTC (全量扫描)"
    ],
    "workflow_steps": [
      {"step": 1, "name": "Threat Model (daily)", "timeout_min": 5},
      {"step": 2, "name": "Red Team Scan", "timeout_min": 10},
      {"step": 3, "name": "CVSS Auto Scoring", "timeout_min": 2},
      {"step": 4, "name": "Blue Team Auto Fix (if CRITICAL/HIGH)", "timeout_min": 15},
      {"step": 5, "name": "Secondary Scan Verification", "timeout_min": 8}
    ],
    "notifications": {
      "slack_channel_critical": "#security-alerts (@channel)",
      "slack_channel_report": "#security-reports",
      "jira_project": "SEC",
      "jira_issue_type": "Bug (Security)"
    },
    "artifact_retention": "90 days"
  }
}
```

GitHub Actions 关键步骤配置：

```yaml:.github/workflows/security-audit.yml
name: Security Audit Pipeline
on:
  push:
    branches: [main, release/*]
  pull_request:
    types: [opened, labeled]
    labels: [security-review]

jobs:
  red-team-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: ZAP Scan
        run: docker run ghcr.io/zaproxy/zaproxy:stable zap-api-scan.py -t ${{ env.TARGET_URL }} -f openapi -r zap_report.html
      - name: Semgrep Scan
        run: docker run returntocorp/semgrep:latest semgrep --config=auto --json-output=semgrep.json .
      - name: Upload Artifacts
        uses: actions/upload-artifact@v4
        with:
          path: |
            zap_report.html
            semgrep.json
```

## 6. 效果指标

以下数据基于本流水线在目标系统上连续运行 **90 天（2024 年 Q1）** 的实测统计，所有数据经安全工程师人工确认。

### 6.1 扫描速度

```json
{
  "scan_speed": {
    "automated": "平均 8.3 分钟完成全量扫描",
    "manual": "人工同等范围审计约需 2-3 天",
    "speed_improvement": "约 45 倍",
    "source": "实测：30 次 CI 构建的平均值。人工审计基准取团队 3 名安全工程师的历史平均工时。（来源：内部 Sprint 复盘 2024-Q1）"
  }
}
```

### 6.2 漏洞检出率

```json
{
  "detection_rate": {
    "period": "2024-01-01 至 2024-03-31",
    "total_vulnerabilities": 142,
    "critical": 5, "high": 33, "medium": 64, "low": 40,
    "false_positives": 19,
    "true_positive_rate": "86.6%",
    "false_positive_rate": "13.4%",
    "source": "实测：所有告警经安全工程师逐条人工复核确认。（来源：Security Audit Dashboard 2024-Q1 导出数据）"
  }
}
```

### 6.3 修复成功率

```json
{
  "fix_success_rate": {
    "auto_fix_attempted": 123,
    "auto_fix_successful": 107,
    "success_rate": "87.0%",
    "failed": 16,
    "failure_breakdown": [
      {"reason": "业务逻辑复杂需人工判断", "count": 8, "pct": "50%"},
      {"reason": "上下游依赖未同步更新", "count": 5, "pct": "31%"},
      {"reason": "第三方库无可用补丁", "count": 3, "pct": "19%"}
    ],
    "source": "实测：二次扫描验证 + 人工确认。（来源：Blue Team Agent 执行日志，覆盖全部 123 次自动修复尝试）"
  }
}
```

### 6.4 修复时效（MTTR）

| 严重程度 | 自动化流水线 | 人工（审计前） | 改善倍数 |
|----------|-------------|--------------|---------|
| CRITICAL | 45 分钟 | 2 天 | ~64 倍 |
| HIGH | 3 小时 | 1 周 | ~56 倍 |
| MEDIUM | 1 天 | 2 周 | ~14 倍 |
| LOW | 3 天 | 1 个月 | ~10 倍 |

数据来源：人工 MTTR 取审计前 2023 年 Q4 的工单统计均值；自动化 MTTR 取 2024 年 Q1 实测均值。（来源：Jira SEC 项目时间戳分析）

### 6.5 总结

| 维度 | 效果 | 说明 |
|------|------|------|
| 扫描效率 | 45x 提升 | 8 分钟 vs 2-3 天 |
| 检出率 | 86.6% TP | 13.4% 误报在可接受范围 |
| 修复率 | 87.0% 自动修复成功 | 13% 需人工介入 |
| CRITICAL MTTR | 45 分钟 → 2 天 | 关键风险秒级响应 |

自动化安全审计不是替代安全工程师，而是把工程师从重复劳动中解放出来，让他们专注于 13% 的复杂问题和威胁建模——这才是安全工作中真正创造价值的部分。

## 关联章节

- ← [工作流实战](../04-workflows/)（Team Mode + `security-research` 团队）
- ← [高级话题](../06-advanced/)（安全概念基础）
- ← [案例二：遗留系统现代化](real-world-02.md)（安全审计在遗留系统中的应用）
- → [案例：全流程自动化](case-full-pipeline.md)（安全环节在全流程中的位置）
