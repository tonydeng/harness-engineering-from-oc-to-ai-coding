# G3 运维安全视角评审报告

**评审日期**：2026-06-27
**评审范围**：src/03-setup/（6篇）、src/04-workflows/（7篇）、src/06-advanced/（16篇）
**评审视角**：运维/DevOps工程师 + 安全架构师

---

## 总览表

### src/03-setup/ 环境搭建

| 文章 | 运维实操 | 自动化 | 监控可观测 | 安全风险 | 故障恢复 | 综合 |
|------|---------|--------|-----------|---------|---------|------|
| README.md（章节导览） | 3 | 2 | 1 | 2 | 1 | 1.8 |
| quickstart.md（快速上手） | 4 | 2 | 1 | 3 | 2 | 2.4 |
| opencode-config.md（配置详解） | 4 | 3 | 2 | 4 | 2 | 3.0 |
| multi-env-setup.md（多环境部署） | 3 | 3 | 2 | 4 | 2 | 2.8 |
| chinese-providers.md（国产供应商） | 4 | 2 | 1 | 2 | 2 | 2.2 |
| oh-my-openagent-setup.md（OMO集成） | 3 | 2 | 1 | 2 | 2 | 2.0 |

### src/04-workflows/ 工作流实战

| 文章 | 运维实操 | 自动化 | 监控可观测 | 安全风险 | 故障恢复 | 综合 |
|------|---------|--------|-----------|---------|---------|------|
| README.md（章节导览） | 3 | 2 | 1 | 2 | 1 | 1.8 |
| ultrawork-mode.md（Ultrawork模式） | 3 | 3 | 2 | 3 | 3 | 2.8 |
| prometheus-mode.md（Prometheus规划） | 3 | 3 | 2 | 3 | 3 | 2.8 |
| multi-agent-collab.md（多Agent协作） | 4 | 4 | 3 | 4 | 3 | 3.6 |
| custom-workflows.md（自定义工作流） | 3 | 3 | 2 | 4 | 2 | 2.8 |
| agent-derivation.md（Agent派生） | 3 | 3 | 2 | 4 | 3 | 3.0 |
| teams-collaboration.md（Teams协作） | 4 | 3 | 3 | 4 | 3 | 3.4 |

### src/06-advanced/ 高级话题

| 文章 | 运维实操 | 自动化 | 监控可观测 | 安全风险 | 故障恢复 | 综合 |
|------|---------|--------|-----------|---------|---------|------|
| README.md（章节导览） | 3 | 2 | 2 | 3 | 2 | 2.4 |
| security-overview.md（安全总览） | 3 | 3 | 3 | 5 | 3 | 3.4 |
| observability.md（可观测性） | 4 | 4 | 5 | 3 | 4 | 4.0 |
| observability-reference.md（可观测性参考） | 4 | 4 | 4 | 2 | 3 | 3.4 |
| feature-flags.md（Feature Flags） | 3 | 3 | 2 | 2 | 2 | 2.4 |
| context-compression.md（上下文压缩） | 3 | 2 | 2 | 2 | 2 | 2.2 |
| context/performance-tuning.md（性能调优） | 4 | 3 | 3 | 2 | 3 | 3.0 |
| context/prompt-caching.md（提示词缓存） | 3 | 2 | 2 | 2 | 2 | 2.2 |
| context/context-injection-patterns.md（上下文注入） | 3 | 2 | 2 | 2 | 2 | 2.2 |
| context/dcp-advanced-plugins.md（DCP插件） | 3 | 2 | 2 | 2 | 2 | 2.2 |
| context/context-quality-metrics.md（质量度量） | 3 | 3 | 3 | 2 | 2 | 2.6 |
| memory-system.md（记忆系统） | 3 | 2 | 2 | 2 | 2 | 2.2 |
| agents-dot-md.md（AGENTS.md约定） | 3 | 2 | 1 | 3 | 2 | 2.2 |
| mcp-servers.md（MCP服务器） | 3 | 3 | 2 | 3 | 2 | 2.6 |
| custom-agents.md（自定义Agent） | 3 | 3 | 2 | 3 | 2 | 2.6 |
| sandbox-hooks.md（沙箱与Hook） | 3 | 3 | 2 | 4 | 3 | 3.0 |

---

## 差距清单

### GAP-G3-001: CI/CD集成指南缺失
- **影响角色**: DevOps工程师、技术负责人
- **问题类型**: 运维/自动化
- **严重度**: P0
- **具体问题**: multi-env-setup.md 的 CI/CD 模板过于简略，仅展示了一个 GitHub Actions 示例。缺少：(1) 完整的 CI/CD 流水线配置（从 checkout → install → config → run → report），(2) 多平台 CI 支持（GitLab CI、Jenkins、Azure DevOps），(3) OpenCode 在 CI 中的 headless 模式配置，(4) CI 中的权限配置（只读/低权限），(5) CI 中的 Secret 管理最佳实践
- **建议修改**: 扩展 multi-env-setup.md 的 CI/CD 部分，增加完整的流水线示例，涵盖主流 CI 平台
- **涉及文件**: src/03-setup/multi-env-setup.md（第229-264行）

### GAP-G3-002: 生产环境部署指南不足
- **影响角色**: DevOps工程师、SRE
- **问题类型**: 运维/故障恢复
- **严重度**: P0
- **具体问题**: 全书缺少生产环境部署的完整指南。openencode-config.md 提到托管配置（第59-69行），但没有说明如何在生产环境部署和管理 OpenCode。缺少：(1) 容器化部署方案（Dockerfile、K8s manifest），(2) 服务端部署架构（多实例、负载均衡），(3) 高可用配置，(4) 灾难恢复方案
- **建议修改**: 新增一篇"生产环境部署指南"文章，或在 multi-env-setup.md 中大幅扩展生产环境部分
- **涉及文件**: src/03-setup/multi-env-setup.md

### GAP-G3-003: 监控集成实操指南缺失
- **影响角色**: DevOps工程师、SRE
- **问题类型**: 监控可观测
- **严重度**: P1
- **具体问题**: observability.md 虽然详细介绍了三支柱体系和5层遥测架构，但缺少：(1) 从零搭建监控系统的 step-by-step 指南，(2) Prometheus + Grafana 的部署和配置脚本，(3) ELK/Loki 的日志采集配置，(4) 告警通知渠道配置（Slack、PagerDuty、钉钉），(5) 常见监控问题排查手册
- **建议修改**: 在 observability.md 或新增文章中提供完整的监控部署指南，包含可直接运行的配置文件
- **涉及文件**: src/06-advanced/observability.md

### GAP-G3-004: Secret 管理实操深度不足
- **影响角色**: 安全架构师、DevOps工程师
- **问题类型**: 安全风险
- **严重度**: P1
- **具体问题**: secret 管理在多处提及（multi-env-setup.md 第300-375行、security-overview.md 第376-509行），但缺少：(1) Vault/AWS Secrets Manager 的完整部署步骤，(2) Secret 轮换的自动化脚本，(3) Secret 泄露的应急响应流程，(4) 多环境 Secret 隔离的实操方案
- **建议修改**: 扩展 security-overview.md 的 Secret Store 部分，增加完整的部署和运维指南
- **涉及文件**: src/06-advanced/security-overview.md（第376-509行）

### GAP-G3-005: API 密钥生命周期管理缺失
- **影响角色**: 安全架构师
- **问题类型**: 安全风险
- **严重度**: P1
- **具体问题**: quickstart.md 和 opencode-config.md 提到 API Key 配置，但缺少：(1) API Key 的创建、分发、轮换、撤销全流程，(2) API Key 的权限范围控制，(3) API Key 泄露检测和应急响应，(4) 多 Provider Key 的统一管理策略
- **建议修改**: 在 security-overview.md 中增加 API 密钥生命周期管理章节
- **涉及文件**: src/03-setup/quickstart.md、src/06-advanced/security-overview.md

### GAP-G3-006: 故障排查手册缺失
- **影响角色**: DevOps工程师、开发者
- **问题类型**: 故障恢复
- **严重度**: P1
- **具体问题**: 故障排查仅散见于各篇文章的"常见问题"部分，缺少统一的故障排查手册。oh-my-openagent-setup.md 有部分排查内容（第676-719行），但覆盖面有限。缺少：(1) 常见错误码和解决方案速查表，(2) 性能问题排查流程，(3) 连接问题排查流程，(4) 权限问题排查流程
- **建议修改**: 新增一篇"故障排查手册"文章，或在各章节末尾统一添加故障排查附录
- **涉及文件**: src/03-setup/、src/04-workflows/、src/06-advanced/

### GAP-G3-007: 国产模型数据主权风险分析缺失
- **影响角色**: 安全架构师、合规负责人
- **问题类型**: 安全风险
- **严重度**: P1
- **具体问题**: chinese-providers.md 详细介绍了 DeepSeek、Kimi、Qwen 的配置，但完全缺少安全风险分析：(1) 数据跨境传输的合规风险，(2) 国产模型 API 的数据保留政策，(3) 敏感代码发送到国产模型的安全影响，(4) 国产模型的内容安全过滤对工作流的影响
- **建议修改**: 在 chinese-providers.md 中增加安全风险章节，分析数据主权和合规问题
- **涉及文件**: src/03-setup/chinese-providers.md

### GAP-G3-008: OMO 安全加固指南缺失
- **影响角色**: 安全架构师
- **问题类型**: 安全风险
- **严重度**: P1
- **具体问题**: oh-my-openagent-setup.md 介绍了 OMO 的安装和配置，但缺少安全加固指南：(1) OMO 的默认权限配置评估，(2) 类别路由的安全边界分析，(3) 多 Agent 编排的信任模型，(4) OMO 遥测数据的安全处理（telemetry.enabled: true 但未说明数据去向）
- **建议修改**: 在 oh-my-openagent-setup.md 中增加安全配置章节，或在 security-overview.md 中增加 OMO 安全模型
- **涉及文件**: src/03-setup/oh-my-openagent-setup.md

### GAP-G3-009: 审计日志实操指南不足
- **影响角色**: 安全架构师、合规负责人
- **问题类型**: 安全风险/监控可观测
- **严重度**: P1
- **具体问题**: security-overview.md 定义了审计日志格式和事件类型（第294-375行），但缺少：(1) 审计日志的收集和存储部署，(2) 审计日志的查询和分析工具配置，(3) 合规审计的自动化报告生成，(4) 审计日志的保留和归档策略
- **建议修改**: 扩展 security-overview.md 的审计部分，增加实操部署指南
- **涉及文件**: src/06-advanced/security-overview.md（第294-375行）

### GAP-G3-010: 多环境配置隔离验证缺失
- **影响角色**: DevOps工程师、安全架构师
- **问题类型**: 运维/安全风险
- **严重度**: P2
- **具体问题**: multi-env-setup.md 提供了三套环境模板，但缺少：(1) 配置隔离的验证方法，(2) 环境间配置漂移的检测，(3) 配置变更的审计追踪，(4) 配置回滚机制
- **建议修改**: 在 multi-env-setup.md 中增加配置治理和验证章节
- **涉及文件**: src/03-setup/multi-env-setup.md

### GAP-G3-011: 网络安全配置指南缺失
- **影响角色**: 安全架构师、DevOps工程师
- **问题类型**: 安全风险
- **严重度**: P2
- **具体问题**: 全书缺少网络层面的安全配置指南：(1) 代理服务器配置的安全影响，(2) TLS/SSL 证书管理，(3) 防火墙规则配置，(4) VPN/Zero Trust 网络集成
- **建议修改**: 在 security-overview.md 或单独文章中增加网络安全配置指南
- **涉及文件**: src/06-advanced/security-overview.md

### GAP-G3-012: 性能基线和容量规划缺失
- **影响角色**: DevOps工程师、SRE
- **问题类型**: 运维/监控可观测
- **严重度**: P2
- **具体问题**: performance-tuning.md 讨论了性能优化策略，但缺少：(1) 硬件配置建议（CPU/内存/网络），(2) 并发用户容量规划，(3) Token 配额规划，(4) 性能测试方法和工具
- **建议修改**: 在 performance-tuning.md 中增加容量规划章节
- **涉及文件**: src/06-advanced/context/performance-tuning.md

### GAP-G3-013: 合规实施指南不足
- **影响角色**: 安全架构师、合规负责人
- **问题类型**: 安全风险
- **严重度**: P2
- **具体问题**: security-overview.md 提供了合规映射表（NIST/SOC2/等保），但缺少：(1) 合规差距分析方法，(2) 合规整改实施步骤，(3) 合规审计准备指南，(4) 持续合规监控方案
- **建议修改**: 扩展 security-overview.md 的合规部分，增加实施指南
- **涉及文件**: src/06-advanced/security-overview.md（第41-54行）

### GAP-G3-014: 依赖安全扫描集成缺失
- **影响角色**: DevOps工程师、安全架构师
- **问题类型**: 安全风险
- **严重度**: P2
- **具体问题**: multi-agent-collab.md 提到了安全门禁中的依赖漏洞扫描（第1302-1317行），但缺少：(1) SCA 工具集成指南（Snyk、Trivy、OWASP Dependency-Check），(2) 漏洞修复策略，(3) 供应链攻击防御，(4) SBOM 生成和管理
- **建议修改**: 在 security-overview.md 或安全门禁相关文章中增加依赖安全扫描指南
- **涉及文件**: src/04-workflows/multi-agent-collab.md（第1302-1317行）

---

## 安全风险清单

### 1. API密钥管理
| 风险点 | 覆盖状态 | 评价 |
|--------|---------|------|
| API Key 环境变量注入 | ✅ 已覆盖 | quickstart.md 和 opencode-config.md 详细说明了 `{env:VAR_NAME}` 语法 |
| .env 文件保护 | ✅ 已覆盖 | quickstart.md 的 .ignore 配置和 opencode-config.md 的敏感文件保护 |
| Secret Store 集成 | ⚠️ 部分覆盖 | security-overview.md 有 Vault/AWS 配置示例，但缺少部署步骤 |
| API Key 轮换 | ⚠️ 部分覆盖 | multi-env-setup.md 提到90天轮换建议，但缺少自动化方案 |
| API Key 泄露检测 | ❌ 未覆盖 | 无泄露检测和应急响应指南 |

### 2. 代码数据外泄
| 风险点 | 覆盖状态 | 评价 |
|--------|---------|------|
| 代码发送到 LLM API | ⚠️ 部分覆盖 | ultrawork-mode.md 提到"除了发送给 LLM API"，但未深入分析风险 |
| 国产模型数据主权 | ❌ 未覆盖 | chinese-providers.md 完全缺少安全风险分析 |
| MCP 数据流安全 | ⚠️ 部分覆盖 | opencode-config.md 有 MCP 配置，但缺少数据流安全分析 |
| 敏感文件排除 | ✅ 已覆盖 | quickstart.md 的 .ignore 配置和 opencode-config.md 的 deny 规则 |

### 3. 权限最小化
| 风险点 | 覆盖状态 | 评价 |
|--------|---------|------|
| 三级权限模型（allow/ask/deny） | ✅ 已覆盖 | quickstart.md 和 opencode-config.md 详细说明 |
| Per-Agent 权限隔离 | ✅ 已覆盖 | opencode-config.md 和 agent-derivation.md 有详细配置 |
| 子 Agent 权限继承 | ✅ 已覆盖 | agent-derivation.md 详细分析了权限继承行为 |
| 生产环境零信任 | ⚠️ 部分覆盖 | multi-env-setup.md 有零信任配置模板，但缺少验证方法 |

### 4. 审计日志
| 风险点 | 覆盖状态 | 评价 |
|--------|---------|------|
| 审计事件定义 | ✅ 已覆盖 | security-overview.md 定义了事件类型和格式 |
| 审计日志配置 | ✅ 已覆盖 | security-overview.md 有配置示例 |
| 审计日志存储和查询 | ❌ 未覆盖 | 缺少日志收集、存储、查询的实操指南 |
| 合规审计报告 | ⚠️ 部分覆盖 | security-overview.md 有报告模板，但缺少自动化生成 |

### 5. 合规要求
| 风险点 | 覆盖状态 | 评价 |
|--------|---------|------|
| NIST/SOC2/等保映射 | ✅ 已覆盖 | security-overview.md 有合规映射表 |
| 合规实施指南 | ❌ 未覆盖 | 缺少差距分析、整改、审计准备的实操指南 |
| 持续合规监控 | ❌ 未覆盖 | 缺少持续合规监控方案 |
| 数据保留策略 | ⚠️ 部分覆盖 | observability.md 有日志保留策略，但缺少合规视角 |

---

## 运维空白

### 缺少指导的运维场景

| 场景 | 优先级 | 说明 |
|------|--------|------|
| **生产环境部署** | P0 | 缺少容器化部署、K8s 配置、高可用架构指南 |
| **CI/CD 集成** | P0 | 仅有简略示例，缺少完整流水线和多平台支持 |
| **监控系统搭建** | P1 | 有理论框架，缺少从零搭建的 step-by-step 指南 |
| **告警配置** | P1 | 有告警规则定义，缺少通知渠道配置和响应流程 |
| **灾难恢复** | P1 | 完全缺失，无备份、恢复、故障切换方案 |
| **多环境管理** | P2 | 有配置模板，缺少配置漂移检测和回滚机制 |
| **容量规划** | P2 | 缺少硬件配置、并发容量、Token 配额规划 |
| **性能测试** | P2 | 缺少性能测试方法、工具和基线建立指南 |
| **安全扫描集成** | P2 | 有概念提及，缺少 SCA/SAST/DAST 工具集成指南 |
| **依赖管理** | P2 | 缺少依赖更新、漏洞修复、供应链安全指南 |

---

## 评审总结

### 优势

1. **安全架构设计完善**：security-overview.md 的四层安全模型（权限/分类/隔离/防御）和 STRIDE 威胁建模为安全架构提供了扎实的理论基础
2. **可观测性体系完整**：observability.md 的三支柱体系（日志/指标/追踪）和5层遥测架构设计专业，OTel 对齐考虑前瞻
3. **权限模型清晰**：三级权限（allow/ask/deny）配合 glob 模式的细粒度控制，覆盖了从全局到工具级别的完整权限谱系
4. **安全门禁概念先进**：multi-agent-collab.md 中的 Quality Gate 和 Security Gate 概念为 CI/CD 安全集成提供了设计思路
5. **合规映射有价值**：NIST/SOC2/等保的映射表为合规审计提供了参考框架

### 主要差距

1. **实操深度不足**：理论框架完整，但缺少从零搭建的 step-by-step 指南和可直接运行的配置文件
2. **生产环境覆盖薄弱**：多环境配置有模板，但生产环境部署、高可用、灾难恢复等运维关键场景几乎空白
3. **监控落地困难**：可观测性理论完整，但从部署 Prometheus/Grafana 到配置告警通知的实操路径缺失
4. **安全实操断层**：安全模型和合规映射完整，但 Secret 管理部署、审计日志运维、合规实施等实操环节缺失
5. **国产模型安全盲区**：chinese-providers.md 完全缺少数据主权和合规风险分析

### 建议优先级

| 优先级 | 建议 | 预期工作量 |
|--------|------|-----------|
| P0 | 新增"生产环境部署指南"文章 | 大 |
| P0 | 扩展 multi-env-setup.md 的 CI/CD 部分 | 中 |
| P1 | 新增"监控系统搭建指南"文章 | 大 |
| P1 | 扩展 security-overview.md 的 Secret 管理实操部分 | 中 |
| P1 | 新增"故障排查手册"文章 | 中 |
| P1 | chinese-providers.md 增加安全风险章节 | 小 |
| P2 | 扩展 security-overview.md 的合规实施指南 | 中 |
| P2 | 新增"依赖安全扫描集成"指南 | 小 |
