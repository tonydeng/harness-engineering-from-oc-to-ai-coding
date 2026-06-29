# 参考资料

本页收录全书引用的所有外部资料，按类别整理。每条资料标注了在正文中的引用位置，方便读者查阅原始来源。

---

## GitHub 仓库

**OpenCode** ([anomalyco/opencode](https://github.com/anomalyco/opencode)) 是本书的核心研究对象，一个基于 AI 的编程引擎，提供 **Agent（智能体）** 编排、**Skill（技能）** 系统、**MCP（模型上下文协议）** 集成等能力。本书围绕 OpenCode 的架构和最佳实践展开，在[读者导航](../00-guide/README.md)等多个章节中被引用。

**oh-my-openagent** ([code-yeongyu/oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent)) 是一个 Agent 编排套件（简称 OMO），为 OpenCode 提供多 Agent 协作能力。在[读者导航](../00-guide/README.md)和[oh-my-openagent 集成](../03-setup/oh-my-openagent-setup.md)中被引用。

**mdBook** ([rust-lang/mdBook](https://github.com/rust-lang/mdBook)) 是一个基于 Markdown 的书籍渲染工具，本书使用 mdBook 生成静态网站。在[读者导航](../00-guide/README.md)中被引用。

**Mermaid** ([mermaid-js/mermaid](https://github.com/mermaid-js/mermaid)) 是一个基于文本的图表生成工具，本书使用 Mermaid 绘制架构图和流程图。在[读者导航](../00-guide/README.md)中被引用。

**nvm** ([nvm-sh/nvm](https://github.com/nvm-sh/nvm)) 是 Node.js 版本管理工具，用于管理多个 Node.js 版本。在[5 分钟快速体验](../00-guide/quick-start.md)和[快速上手](../03-setup/quickstart.md)中被引用。

**nvm-windows** ([coreybutler/nvm-windows](https://github.com/coreybutler/nvm-windows)) 是 Windows 平台的 Node.js 版本管理工具。在[5 分钟快速体验](../00-guide/quick-start.md)中被引用。

**opencode-mem** ([tickernelz/opencode-mem](https://github.com/tickernelz/opencode-mem)) 是一个 OpenCode 记忆插件，为 AI Agent 提供持久化记忆能力。在[记忆系统设计](../06-advanced/memory-system.md)中被引用。

**opencode-claude-memory** ([kuitos/opencode-claude-memory](https://github.com/kuitos/opencode-claude-memory)) 是一个兼容 Claude 格式的记忆插件。在[记忆系统设计](../06-advanced/memory-system.md)中被引用。

**agentmemory** ([rohitg00/agentmemory](https://github.com/rohitg00/agentmemory)) 是一个通用的 Agent 记忆框架。在[记忆系统设计](../06-advanced/memory-system.md)中被引用。

**true-mem** ([rizal72/true-mem](https://github.com/rizal72/true-mem)) 是另一个记忆插件实现。在[记忆系统设计](../06-advanced/memory-system.md)中被引用。

**DCP Plugin** ([Opencode-DCP/opencode-dynamic-context-pruning](https://github.com/Opencode-DCP/opencode-dynamic-context-pruning)) 是一个动态上下文裁剪插件，用于优化 Token 使用。在[上下文压缩与Token 预算](../06-advanced/context-compression.md)中被引用。

**OpenCode Issue #18100** ([anomalyco/opencode#18100](https://github.com/anomalyco/opencode/issues/18100)) 是 OpenCode 项目的一个 Issue，讨论了 Agent 派生模式的相关问题。在[Agent 派生模式](../04-workflows/agent-derivation.md)中被引用。

**Book Repository** ([tonydeng/harness-engineering-from-oc-to-ai-coding](https://github.com/tonydeng/harness-engineering-from-oc-to-ai-coding)) 是本书的源码仓库。在[Harness Engineering](../README.md)和[如何使用本书](../00-guide/how-to-read.md)中被引用。

**Skill example** ([opencode/skills/frontend-architect](https://github.com/opencode/skills/frontend-architect)) 是一个 Skill 示例，展示了如何创建前端架构师 Skill。在[创建 Skill](../05-skills/creating-skills.md)中被引用。

---

## 官方文档与网站

**OpenCode 官方网站** ([opencode.ai](https://opencode.ai)) 是 OpenCode 项目的官方网站，提供产品介绍和入口。在多个文件中被引用。

**OpenCode 官方文档** ([opencode.ai/docs](https://opencode.ai/docs)) 是 OpenCode 的完整文档站点，涵盖配置、CLI、Agent、Provider 等内容。在[如何使用本书](../00-guide/how-to-read.md)中被引用。

**OpenCode 配置参考** ([opencode.ai/docs/config/](https://opencode.ai/docs/config/)) 详细说明了 OpenCode 的配置选项。在[多环境部署方案](../03-setup/multi-env-setup.md)中被引用。

**OpenCode CLI 参考** ([opencode.ai/docs/cli/](https://opencode.ai/docs/cli/)) 是 OpenCode 命令行工具的参考文档。在[多环境部署方案](../03-setup/multi-env-setup.md)中被引用。

**OpenCode Agents 参考** ([opencode.ai/docs/agents/](https://opencode.ai/docs/agents/)) 说明了 OpenCode 的 Agent 系统。在[多环境部署方案](../03-setup/multi-env-setup.md)中被引用。

**OpenCode Providers 参考** ([opencode.ai/docs/providers/](https://opencode.ai/docs/providers/)) 列出了 OpenCode 支持的 AI 模型供应商。在[多环境部署方案](../03-setup/multi-env-setup.md)中被引用。

**OpenCode 模型支持列表** ([opencode.ai/docs/models/](https://opencode.ai/docs/models/)) 列出了 OpenCode 支持的 AI 模型。在[多环境部署方案](../03-setup/multi-env-setup.md)中被引用。

**OpenCode JSON Schema** ([opencode.ai/config.json](https://opencode.ai/config.json)) 是 OpenCode 配置文件的 JSON Schema 定义。在多个文件中被引用。

**OpenCode Zen 认证** ([opencode.ai/auth](https://opencode.ai/auth)) 是 OpenCode 的认证服务。在[快速上手](../03-setup/quickstart.md)中被引用。

**OpenCode 安装脚本** ([opencode.ai/install](https://opencode.ai/install)) 提供了一键安装 OpenCode 的脚本。在多个文件中被引用。

**Node.js 官方网站** ([nodejs.org](https://nodejs.org/)) 是 Node.js 运行时的官方网站。在[读者导航](../00-guide/README.md)中被引用。

**Git 官方网站** ([git-scm.com](https://git-scm.com/)) 是 Git 版本控制系统的官方网站。在[5 分钟快速体验](../00-guide/quick-start.md)中被引用。

**Bun.js 官方网站** ([bun.sh](https://bun.sh/)) 是一个高性能的 JavaScript 运行时。在[oh-my-openagent 集成](../03-setup/oh-my-openagent-setup.md)中被引用。

---

## 书籍与学术参考

**Mitchell Hashimoto, "My AI Adoption Journey"** ([mitchellh.com](https://mitchellh.com/writing/ai-adoption-journey)) 是 HashiCorp 联合创始人 Mitchell Hashimoto 于 2026 年 2 月发布的博客文章，分享了他采用 AI 编程工具的经验和思考。在[什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md)中被引用。

**Harrison Chase, "Harness Engineering: The Missing Piece in AI Development"** 是 LangChain 创始人 Harrison Chase 在 VentureBeat 播客（2026 年 3 月 7 日）中的访谈，讨论了 **Harness Engineering（驾驭工程）** 在 AI 开发中的重要性。在[什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md)中被引用。

**《驾驭工程：从 Claude Code 源码到 AI 编码最佳实践》**（简称《马书》）是一本技术书籍，深入分析了 Claude Code 的源码架构和 AI 编程的最佳实践。在[Agent 编排](../02-core-concepts/agent-orchestration.md)和[记忆系统设计](../06-advanced/memory-system.md)中被引用。

**《Working Effectively with Legacy Code》** ([O'Reilly](https://www.oreilly.com/library/view/working-effectively-with/0131177052/)) by Michael Feathers 是一本经典的软件工程书籍，介绍了如何在遗留代码库中有效工作。在[案例二：遗留系统现代化](../07-case-studies/real-world-02.md)中被引用。

**Standish Group CHAOS Report** ([standishgroup.com](https://www.standishgroup.com/)) 是 Standish Group 发布的年度软件项目报告，提供了软件项目成功率等关键数据。在[案例二：遗留系统现代化](../07-case-studies/real-world-02.md)中被引用。

**《代码大全》(Code Complete)** ([O'Reilly](https://www.oreilly.com/library/view/code-complete-second/0735619670/)) by Steve McConnell 是一本经典的软件工程书籍，涵盖了软件构建的方方面面。在[读者导航](../00-guide/README.md)中被引用。

**《持续交付》(Continuous Delivery)** ([continuousdelivery.com](https://continuousdelivery.com/)) by Jez Humble & David Farley 是 DevOps 领域的经典著作，介绍了如何实现可靠的软件发布。在[读者导航](../00-guide/README.md)中被引用。

**《DevOps 手册》(The DevOps Handbook)** ([IT Revolution](https://itrevolution.com/product/the-devops-handbook-second-edition/)) by Gene Kim et al. 是 DevOps 实践的权威指南。在[读者导航](../00-guide/README.md)中被引用。

---

## 开源工具与框架

**OpenCode** (v1.17.x) 是一个 AI 编程引擎，提供 Agent 编排、Skill 系统、MCP 集成等能力。在[读者导航](../00-guide/README.md)中被引用。

**oh-my-openagent (OMO)** (v4.13.x) 是一个 Agent 编排套件，为 OpenCode 提供多 Agent 协作能力。在[读者导航](../00-guide/README.md)中被引用。

**mdBook** (v0.5.x) ([rust-lang/mdBook](https://github.com/rust-lang/mdBook)) 是一个基于 Markdown 的书籍渲染工具。在[读者导航](../00-guide/README.md)中被引用。

**Mermaid** (v10+) ([mermaid-js/mermaid](https://github.com/mermaid-js/mermaid)) 是一个基于文本的图表生成工具。在[读者导航](../00-guide/README.md)中被引用。

**Node.js** (>=18) ([nodejs.org](https://nodejs.org/)) 是一个基于 V8 引擎的 JavaScript 运行时。在[读者导航](../00-guide/README.md)中被引用。

**React** (18.x) ([react.dev](https://react.dev/)) 是一个用于构建用户界面的 JavaScript 库。在多个文件中被引用。

**TypeScript** (4.9/5.x) ([typescriptlang.org](https://www.typescriptlang.org/)) 是 JavaScript 的超集，添加了静态类型支持。在多个文件中被引用。

**Express** (4.17.1) ([expressjs.com](https://expressjs.com/)) 是一个流行的 Node.js Web 框架。在[案例一：从零搭建微服务](../07-case-studies/real-world-01.md)中被引用。

**Next.js** (14/App Router) ([nextjs.org](https://nextjs.org/)) 是一个 React 全栈框架。在[AGENTS.md 约定系统](../06-advanced/agents-dot-md.md)中被引用。

**NestJS** ([nestjs.com](https://nestjs.com/)) 是一个用于构建高效、可扩展的 Node.js 服务端应用程序的框架。在[案例：全流程自动化](../07-case-studies/case-full-pipeline.md)中被引用。

**Fastify** ([fastify.dev](https://fastify.dev/)) 是一个高性能的 Node.js Web 框架。在[AGENTS.md 约定系统](../06-advanced/agents-dot-md.md)中被引用。

**FastAPI** ([fastapi.tiangolo.com](https://fastapi.tiangolo.com/)) 是一个现代的、快速的 Python Web 框架。在[案例：安全审计流水线](../07-case-studies/case-security-audit.md)中被引用。

**Prisma** ([prisma.io](https://www.prisma.io/)) 是一个现代化的数据库 ORM，支持多种数据库。在[案例一：从零搭建微服务](../07-case-studies/real-world-01.md)中被引用。

**Vitest** ([vitest.dev](https://vitest.dev/)) 是一个基于 Vite 的极速单元测试框架。在[案例一：从零搭建微服务](../07-case-studies/real-world-01.md)中被引用。

**Vite** ([vite.dev](https://vite.dev/)) 是一个现代化的前端构建工具。在[快速上手](../03-setup/quickstart.md)中被引用。

**Zustand** ([zustand-demo.pmnd.rs](https://zustand-demo.pmnd.rs/)) 是一个轻量级的 React 状态管理库。在[什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md)中被引用。

**Tailwind CSS** ([tailwindcss.com](https://tailwindcss.com/)) 是一个实用优先的 CSS 框架。在[约束系统解析](../02-core-concepts/constraints-system.md)中被引用。

**ESLint** ([eslint.org](https://eslint.org/)) 是一个 JavaScript/TypeScript 代码检查工具。在[案例二：遗留系统现代化](../07-case-studies/real-world-02.md)中被引用。

**Prettier** ([prettier.io](https://prettier.io/)) 是一个代码格式化工具。在[OpenCode 配置深度解析](../03-setup/opencode-config.md)中被引用。

**AST-grep** ([ast-grep.github.io](https://ast-grep.github.io/)) 是一个基于 AST 的代码搜索和替换工具。在[约束系统解析](../02-core-concepts/constraints-system.md)中被引用。

**Playwright** ([playwright.dev](https://playwright.dev/)) 是一个浏览器自动化工具，用于端到端测试。在[多 Agent 协作](../04-workflows/multi-agent-collab.md)中被引用。

**Storybook** ([storybook.js.org](https://storybook.js.org/)) 是一个 UI 组件开发和展示工具。在[多 Agent 协作](../04-workflows/multi-agent-collab.md)中被引用。

**Secretlint** ([secretlint.github.io](https://secretlint.github.io/)) 是一个密钥扫描工具，用于检测代码中的敏感信息。在[案例二：遗留系统现代化](../07-case-studies/real-world-02.md)中被引用。

**Snyk** ([snyk.io](https://snyk.io/)) 是一个开发者安全平台，提供漏洞扫描和修复建议。在[案例二：遗留系统现代化](../07-case-studies/real-world-02.md)中被引用。

**ZAP (Zed Attack Proxy)** ([zaproxy.org](https://www.zaproxy.org/)) 是 OWASP 维护的 Web 应用安全扫描工具。在[案例：安全审计流水线](../07-case-studies/case-security-audit.md)中被引用。

**Docker** ([docker.com](https://www.docker.com/)) 是一个容器化平台。在多个文件中被引用。

**Kubernetes** ([kubernetes.io](https://kubernetes.io/)) 是一个容器编排平台。在[案例：全流程自动化](../07-case-studies/case-full-pipeline.md)中被引用。

**Loki** ([grafana.com/oss/loki](https://grafana.com/oss/loki/)) 是 Grafana Labs 开发的日志聚合系统。在[可观测性参考](../06-advanced/observability-reference.md)中被引用。

**Elasticsearch** ([elastic.co/elasticsearch](https://www.elastic.co/elasticsearch/)) 是一个分布式搜索和分析引擎。在[可观测性参考](../06-advanced/observability-reference.md)中被引用。

**Kibana** ([elastic.co/kibana](https://www.elastic.co/kibana/)) 是 Elasticsearch 的可视化工具。在[可观测性参考](../06-advanced/observability-reference.md)中被引用。

---

## npm 包

**opencode-ai** ([npmjs.com](https://www.npmjs.com/package/opencode-ai)) 是 OpenCode 的 npm 包，提供 CLI 工具。在[快速上手](../03-setup/quickstart.md)中被引用。

**@modelcontextprotocol/server-filesystem** ([npmjs.com](https://www.npmjs.com/package/@modelcontextprotocol/server-filesystem)) 是 MCP 的文件系统服务器，允许 AI 访问本地文件。在[OpenCode 配置深度解析](../03-setup/opencode-config.md)中被引用。

**@modelcontextprotocol/server-postgres** ([npmjs.com](https://www.npmjs.com/package/@modelcontextprotocol/server-postgres)) 是 MCP 的 PostgreSQL 服务器，允许 AI 查询数据库。在[OpenCode 配置深度解析](../03-setup/opencode-config.md)中被引用。

**@modelcontextprotocol/sdk** ([npmjs.com](https://www.npmjs.com/package/@modelcontextprotocol/sdk)) 是 MCP 的 Node.js SDK，用于开发 MCP 服务器。在[MCP 服务器](../06-advanced/mcp-servers.md)中被引用。

**@github/github-mcp-server** ([npmjs.com](https://www.npmjs.com/package/@github/github-mcp-server)) 是 GitHub 的 MCP 服务器，允许 AI 访问 GitHub API。在[Skill-MCP 桥接](../05-skills/skill-mcp-bridge.md)中被引用。

**@agentmemory/agentmemory** ([npmjs.com](https://www.npmjs.com/package/@agentmemory/agentmemory)) 是一个 Agent 记忆框架的 npm 包。在[记忆系统设计](../06-advanced/memory-system.md)中被引用。

**@agentmemory/mcp** ([npmjs.com](https://www.npmjs.com/package/@agentmemory/mcp)) 是 Agent 记忆的 MCP 服务器。在[记忆系统设计](../06-advanced/memory-system.md)中被引用。

**@ai-sdk/openai-compatible** ([npmjs.com](https://www.npmjs.com/package/@ai-sdk/openai-compatible)) 是一个 OpenAI 兼容适配器，用于连接国产模型供应商。在[国产模型供应商配置](../03-setup/chinese-providers.md)中被引用。

**@prisma/client** ([npmjs.com](https://www.npmjs.com/package/@prisma/client)) 是 Prisma ORM 的客户端。在[案例一：从零搭建微服务](../07-case-studies/real-world-01.md)中被引用。

**@ast-grep/cli** ([npmjs.com](https://www.npmjs.com/package/@ast-grep/cli)) 是 AST-grep 的命令行工具。在[约束系统解析](../02-core-concepts/constraints-system.md)中被引用。

**opencode-mem** ([npmjs.com](https://www.npmjs.com/package/opencode-mem)) 是一个 OpenCode 记忆插件。在[记忆系统设计](../06-advanced/memory-system.md)中被引用。

**opencode-claude-memory** ([npmjs.com](https://www.npmjs.com/package/opencode-claude-memory)) 是一个兼容 Claude 格式的记忆插件。在[记忆系统设计](../06-advanced/memory-system.md)中被引用。

**true-mem** ([npmjs.com](https://www.npmjs.com/package/true-mem)) 是另一个记忆插件实现。在[记忆系统设计](../06-advanced/memory-system.md)中被引用。

**better-sqlite3** ([npmjs.com](https://www.npmjs.com/package/better-sqlite3)) 是一个 SQLite3 的 Node.js 绑定。在[MCP 服务器](../06-advanced/mcp-servers.md)中被引用。

**eslint-plugin-security** ([npmjs.com](https://www.npmjs.com/package/eslint-plugin-security)) 是 ESLint 的安全规则插件。在[案例：团队级 Skill 市场](../07-case-studies/case-skills-marketplace.md)中被引用。

---

## 数据来源与基准测试

**SWE-bench** ([swebench.com](https://www.swebench.com/)) 是一个用于评估 AI 编程能力的基准测试，测试 AI 解决真实 GitHub Issue 的能力。书中引用了 Claude Code 80.9%+ 和 Opus 4.8 at 88.6% 的数据。SWE-bench 已成为评估 AI 编程工具能力的事实标准，被广泛用于比较不同 AI 模型的代码生成能力。在[为什么选择 OpenCode](../01-introduction/why-opencode.md)中被引用。

**Codeforces** ([codeforces.com](https://codeforces.com/)) 是全球最知名的在线编程竞赛平台之一，其评分系统被广泛用于评估编程能力。书中引用了 DeepSeek-V4 的评分数据（2386 standard, 2701 Speciale），表明该模型已达到世界级编程竞赛选手水平。在[国产模型供应商配置](../03-setup/chinese-providers.md)中被引用。

**LMSYS Chatbot Arena** ([lmarena.ai](https://lmarena.ai/)) 是一个 AI 聊天机器人竞技场，通过 Elo 评分系统评估模型能力。用户可以与两个匿名模型对话并投票选择更好的回答，从而生成客观的模型排名。书中引用了 GPT-5.5-high 约 1506 Elo 和 DeepSeek-V4 Pro 约 1462 Elo 的数据。在[国产 AI 编程生态适配](../01-introduction/chinese-ecosystem.md)中被引用。

**IDC MarketScape: China AI Code Assistants 2025** ([idc.com](https://www.idc.com/)) 是 IDC 发布的 2025 年中国 AI 代码助手市场评估报告。该报告对中国市场的主要 AI 编程工具进行了全面评估，书中引用了 Trae 41.2% 市场份额和文心快码 8 项满分的数据，反映了中国 AI 编程工具市场的竞争格局。在[国产 AI 编程生态适配](../01-introduction/chinese-ecosystem.md)中被引用。

**Gartner Magic Quadrant for AI Code Assistants** ([gartner.com](https://www.gartner.com/)) 是全球知名的 IT 研究和咨询公司 Gartner 发布的 AI 代码助手魔力象限报告。书中引用了通义灵码进入 Gartner Challenger 象限的数据，这是中国 AI 编程工具在国际权威评估中的重要突破。在[国产 AI 编程生态适配](../01-introduction/chinese-ecosystem.md)中被引用。

**LangChain Experiments** ([langchain.com](https://www.langchain.com/)) 是 LangChain 框架团队进行的 AI Agent 能力实验。书中引用了 Agent 准确率从 52.8% 提升到 66.5% 的数据（通过 Harness 层），证明了结构化编排对 AI Agent 性能的显著提升。在[什么是 Harness Engineer](../01-introduction/what-is-harness-engineer.md)中被引用。

**GPT-4 Technical Report** ([cdn.openai.com](https://cdn.openai.com/papers/gpt-4.pdf)) 是 OpenAI 于 2023 年 3 月发布的 GPT-4 技术报告，详细介绍了 GPT-4 的架构、训练方法和性能评估。书中引用了 Self-attention O(n²) 复杂度和 50K→200K 上下文窗口导致 ~16x 推理时间的数据，说明了长上下文处理的性能挑战。在[性能调优与成本管理](../06-advanced/context/performance-tuning.md)中被引用。

**Context7** ([context7.dev](https://context7.dev/)) 是一个上下文管理工具，帮助 AI 编程工具更好地理解项目上下文。书中引用了使用 **Context（上下文）**7 可以减少 30-50% 试错工具调用的数据，说明了上下文管理对 AI 编程效率的重要性。在[性能调优与成本管理](../06-advanced/context/performance-tuning.md)中被引用。

**Prisma Case Studies** ([prisma.io/case-studies](https://www.prisma.io/case-studies)) 是 Prisma ORM 的官方案例研究集合，展示了不同规模项目使用 Prisma 的经验和成果。书中引用了使用 Prisma 可以减少 30-40% 运行时错误的数据，说明了类型安全 ORM 对代码质量的提升。在[案例一：从零搭建微服务](../07-case-studies/real-world-01.md)中被引用。

**Standish Group CHAOS Report** ([standishgroup.com](https://www.standishgroup.com/)) 是 Standish Group 自 1994 年以来持续发布的软件项目成功率报告，是软件工程领域最权威的行业数据来源之一。书中引用了完全重写成功率 <30% 的数据，强调了渐进式现代化相比完全重写的风险优势。在[案例二：遗留系统现代化](../07-case-studies/real-world-02.md)中被引用。

---

## CVE 参考

**CVE-2020-15095** ([NVD](https://nvd.nist.gov/vuln/detail/CVE-2020-15095)) 是 iconv-lite 0.4.24 中的一个漏洞。在[案例二：遗留系统现代化](../07-case-studies/real-world-02.md)中被引用。

**CVE-2020-12256** ([NVD](https://nvd.nist.gov/vuln/detail/CVE-2020-12256)) 是 safer-buffer 2.1.2 中的一个漏洞。在[案例二：遗留系统现代化](../07-case-studies/real-world-02.md)中被引用。

**CVE-2020-8203** ([NVD](https://nvd.nist.gov/vuln/detail/CVE-2020-8203)) 是 lodash 中的原型污染漏洞。在[案例二：遗留系统现代化](../07-case-studies/real-world-02.md)中被引用。

**CVE-2022-24999** ([NVD](https://nvd.nist.gov/vuln/detail/CVE-2022-24999)) 是 express 中的拒绝服务漏洞。在[案例二：遗留系统现代化](../07-case-studies/real-world-02.md)中被引用。

**CVE-2022-23529** ([NVD](https://nvd.nist.gov/vuln/detail/CVE-2022-23529)) 是 jsonwebtoken 中的未验证签名漏洞。在[案例二：遗留系统现代化](../07-case-studies/real-world-02.md)中被引用。

---

## 协议与标准

**MCP (Model Context Protocol)** ([modelcontextprotocol.io](https://modelcontextprotocol.io/)) 是 Anthropic 提出的模型上下文协议，基于 JSON-RPC over stdio/HTTP/WS，用于 AI 模型与外部工具的标准化通信。在[MCP 服务器](../06-advanced/mcp-servers.md)中被引用。

**LSP (Language Server Protocol)** ([microsoft.github.io](https://microsoft.github.io/language-server-protocol/)) 是微软提出的语言服务器协议，用于编辑器与语言服务器之间的标准化通信。在[验证护栏体系](../02-core-concepts/validation-harness.md)中被引用。

**OpenAPI 3.x** ([spec.openapis.org](https://spec.openapis.org/oas/latest.html)) 是 API 规范标准，用于描述 RESTful API。在[自定义 Agent 与 **Plugin（插件）**](../06-advanced/custom-agents.md)中被引用。

**STRIDE** ([Microsoft Learn](https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats)) 是微软提出的威胁分类模型，用于安全威胁建模。在[MCP 服务器](../06-advanced/mcp-servers.md)中被引用。

**CVSS** ([first.org](https://www.first.org/cvss/)) 是通用漏洞评分系统，用于评估漏洞的严重性。在[案例：安全审计流水线](../07-case-studies/case-security-audit.md)中被引用。

**SemVer 2.0.0** ([semver.org](https://semver.org/)) 是语义化版本规范，定义了版本号的命名规则。在[案例：团队级 Skill 市场](../07-case-studies/case-skills-marketplace.md)中被引用。

**OAuth 2.0** ([oauth.net/2](https://oauth.net/2/)) 是一个开放标准的授权协议。在[MCP 服务器](../06-advanced/mcp-servers.md)中被引用。

**JSON Schema** ([json-schema.org](https://json-schema.org/)) 是 JSON 数据的模式定义语言，用于验证 JSON 数据。在[OpenCode 配置深度解析](../03-setup/opencode-config.md)中被引用。

---

## 补充参考链接

以下链接为书中引用的关键数据、报告和研究提供可验证的互联网来源：

### 行业报告与数据

**GitHub Octoverse 2024** ([github.blog](https://github.blog/news-insights/octoverse/octoverse-2024/)) 是 GitHub 发布的年度开发者报告，涵盖了全球开发者趋势、编程语言流行度、AI 工具使用情况等数据。2024 年报告指出 Python 超越 JavaScript 成为 GitHub 上最流行的编程语言，AI 驱动的开发成为主流。

**Stack Overflow Developer Survey 2025** ([survey.stackoverflow.co](https://survey.stackoverflow.co/2025/)) 是 Stack Overflow 发布的年度开发者调查，提供了全球开发者的技术栈、工具偏好、薪资等数据。2025 年调查于 2025 年 6 月发布，涵盖了 AI 工具使用趋势、开发者满意度等最新数据。

**DORA State of DevOps 2025** ([dora.dev](https://dora.dev/research/2025/)) 是 Google DORA 团队发布的 DevOps 状态报告，提供了 DevOps 实践与软件交付性能的关系数据。2025 年报告聚焦于 AI 在软件工程中的应用、平台工程和开发者体验。

**ThoughtWorks Technology Radar** ([thoughtworks.com/radar](https://www.thoughtworks.com/radar)) 是 ThoughtWorks 发布的技术雷达，提供了技术趋势和推荐实践。

**JetBrains State of Developer Ecosystem 2025** ([jetbrains.com](https://devecosystem-2025.jetbrains.com/)) 是 JetBrains 发布的开发者生态调查，提供了开发者工具使用情况的数据。2025 年调查涵盖了编程语言趋势、IDE 偏好、AI 工具采用率等最新数据。

**OWASP Top 10 for LLM Applications 2025** ([owasp.org](https://owasp.org/www-project-top-10-for-large-language-model-applications/)) 是 OWASP 发布的 LLM 应用安全 Top 10，列出了 LLM 应用中最常见的安全风险。2025 年版本涵盖了提示注入、数据泄露、不安全的输出处理等关键风险，为 AI 应用安全提供了权威指南。

### 学术研究与论文

**SWE-bench: Can Language Models Resolve Real-World GitHub Issues?** ([arxiv.org/abs/2310.06770](https://arxiv.org/abs/2310.06770)) 是 SWE-bench 基准测试的论文，提出了评估 AI 解决真实 GitHub Issue 能力的方法。

**SWE-Lancer: Can Frontier LLMs Earn $1M from Real-World Freelance Software Engineering?** ([arxiv.org/abs/2503.11453](https://arxiv.org/abs/2503.11453)) 是 SWE-Lancer 基准测试的论文，评估了 AI 在真实自由职业软件工程任务上的表现。

**GPT-4 Technical Report** ([cdn.openai.com/papers/gpt-4.pdf](https://cdn.openai.com/papers/gpt-4.pdf)) 是 OpenAI 发布的 GPT-4 技术报告，详细介绍了 GPT-4 的架构和能力。

**Sleeper Agents: Training Deceptive LLMs that Persist through Safety Training** ([arxiv.org/abs/2401.05566](https://arxiv.org/abs/2401.05566)) 是 Anthropic 发布的研究论文，探讨了 LLM 中欺骗性行为的问题。

**Chain-of-Thought Prompting Elicits Reasoning in Large Language Models** ([arxiv.org/abs/2201.11903](https://arxiv.org/abs/2201.11903)) 是思维链提示的开创性论文，证明了通过逐步推理可以提升 LLM 的能力。

### 技术博客与文章

**Mitchell Hashimoto - My AI Adoption Journey** ([mitchellh.com](https://mitchellh.com/writing/ai-adoption-journey)) 是 HashiCorp 联合创始人分享的 AI 采用经验。

**Martin Fowler - Exploring Generative AI** ([martinfowler.com](https://martinfowler.com/articles/exploring-gen-ai.html)) 是 Martin Fowler 关于生成式 AI 在软件开发中应用的探索。

**ThoughtWorks - What We Learned from a Year of Building with LLMs** ([thoughtworks.com](https://www.thoughtworks.com/insights/blog/generative-ai/what-we-learned-from-a-year-of-building-with-llms)) 是 ThoughtWorks 分享的一年 LLM 开发经验。

**GitHub - How GitHub Copilot is Getting Better at Understanding Your Code** ([github.blog](https://github.blog/ai-and-ml/github-copilot/how-github-copilot-is-getting-better-at-understanding-your-code/)) 是 GitHub 关于 Copilot 代码理解能力提升的博客。

**Anthropic - Science of Alignment** ([anthropic.com/research](https://www.anthropic.com/research)) 是 Anthropic 关于 AI 对齐科学研究的页面。

**Simon Willison - Here's How I Use LLMs** ([simonwillison.net](https://simonwillison.net/2025/Mar/6/here-is-how-i-use-llms/)) 是 Simon Willison 分享的 LLM 使用方式。

### 开源项目与工具

**OpenAI Codex CLI** ([github.com/openai/codex](https://github.com/openai/codex)) 是 OpenAI 发布的 Codex 命令行工具。

**Claude Code by Anthropic** ([docs.anthropic.com](https://docs.anthropic.com/en/docs/claude-code)) 是 Anthropic 发布的 Claude Code 官方文档。

**LangChain** ([github.com/langchain-ai/langchain](https://github.com/langchain-ai/langchain)) 是一个 LLM 应用开发框架。

**CrewAI** ([github.com/joaomdmoura/crewAI](https://github.com/joaomdmoura/crewAI)) 是一个多 Agent 编排框架。

**Microsoft AutoGen** ([github.com/microsoft/autogen](https://github.com/microsoft/autogen)) 是微软发布的多 Agent 对话框架。

**DeepSeek-V4** ([github.com/deepseek-ai/DeepSeek-V4](https://github.com/deepseek-ai/DeepSeek-V4)) 是 DeepSeek 发布的 V3 模型。

**Qwen** ([github.com/QwenLM/Qwen](https://github.com/QwenLM/Qwen)) 是阿里云发布的通义千问模型。

**RAGFlow** ([github.com/infiniflow/ragflow](https://github.com/infiniflow/ragflow)) 是一个 RAG 引擎。

### AI 编码工具

**GitHub Copilot** ([github.com/features/copilot](https://github.com/features/copilot)) 是 GitHub 发布的 AI 编程助手。

**Cursor** ([cursor.com](https://cursor.com/)) 是一个 AI 代码编辑器。

**Windsurf (Codeium)** ([codeium.com/windsurf](https://codeium.com/windsurf)) 是 Codeium 发布的 AI 编程 IDE。

**Devin** ([devin.ai](https://devin.ai/)) 是一个 AI 软件工程师。

**Amazon Q Developer** ([aws.amazon.com/q/developer](https://aws.amazon.com/q/developer/)) 是 AWS 发布的 AI 编程助手。

**Tabnine** ([tabnine.com](https://www.tabnine.com/)) 是一个 AI 代码助手。

---

## 引用统计

| 类别 | 数量 |
|------|------|
| GitHub 仓库 | 14 |
| 官方文档与网站 | 13 |
| 书籍与学术参考 | 8 |
| 开源工具与框架 | 30 |
| npm 包 | 15 |
| 数据来源与基准测试 | 10 |
| CVE 参考 | 5 |
| 协议与标准 | 8 |
| **合计** | **103** |

---

## 版本新鲜度检查

> **最后检查日期**：2026-06-28
> **建议频率**：每月检查一次

本书涉及的关键工具版本（每月检查 freshness check）：

| 工具 | 当前推荐版本 | 本书引用版本 | 检查方式 |
|------|------------|------------|---------|
| OpenCode | v1.17.11 | v1.17+ | `opencode --version` |
| oh-my-openagent | v4.12.0 | v4.12+ | `omo --version` |
| Node.js | 22+ | 22+ | `node --version` |
| Python | 3.11+ | 3.11+ | `python3 --version` |
| mdBook | latest | latest | `mdbook --version` |

### 更新指引

当工具发布新版本时：

1. 运行 `python scripts/qa/run-hedq.py` 检查 D2.2 维度
2. 更新本书中的版本引用
3. 更新本表的"最后检查日期"（last check date）
4. 提交变更并说明版本升级原因
