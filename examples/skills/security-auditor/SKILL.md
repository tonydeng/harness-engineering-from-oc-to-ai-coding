---
name: security-auditor
description: "安全漏洞扫描和审计专家，在需要进行安全审计、漏洞扫描、合规检查时使用"
allowed-tools:
  - read
  - grep
  - bash
target_agent: security-audit
license: MIT
metadata:
  version: "1.0.0"
  author: security-team
---

# Security Auditor Skill

## 审计范围

1. **代码安全**
   - SQL 注入
   - XSS 漏洞
   - CSRF 漏洞
   - 敏感信息泄露

2. **配置安全**
   - 默认凭证
   - 不安全配置
   - 权限过度

3. **依赖安全**
   - 已知漏洞
   - 过时依赖

## 输出规范

使用 `templates/vulnerability-report.md.tmpl` 生成报告。
