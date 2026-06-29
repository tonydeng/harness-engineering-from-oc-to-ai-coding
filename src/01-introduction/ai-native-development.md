# AI 原生开发实践

> 面向前端开发者和研究人员的 AI 编程实操指导。

## 文章概述

AI 编程工具并非万能。不同技术背景的开发者，适合让 AI 介入的工作环节差异很大。本文针对两类常见角色——前端开发者和研究人员，给出具体的 AI 辅助场景、prompt 示例和使用边界。读完本文，你将能够判断哪些日常任务适合交给 AI，哪些必须自己把关。
---

## 前端开发者的 AI 编程实践

前端开发中有大量重复性、模式化的任务，天然适合 AI 辅助。以下三个场景投入产出比最高。

### 场景一：组件生成
从设计稿描述或接口文档生成 React/Vue 组件代码，是 AI 辅助效率最高的前端任务。
```text:terminal
用户输入：
"创建一个 UserCard 组件，接收 name、avatar、role 三个 props。
React 18 + TypeScript，头像圆形 48px，admin 红色/editor 蓝色/viewer 灰色标签，hover 显示 email。"
AI 输出：→ 完整的 UserCard.tsx + 类型定义 + 样式 + hover 逻辑 + 测试骨架
```

关键是 prompt 中要明确技术栈版本、样式规范和交互细节。越具体，AI 生成的代码越接近可用状态。

#### OpenCode 工作流：三轮对话迭代

实际使用中，一次生成很少完美。通过 OpenCode 的多轮对话逐步迭代，效果远好于一次性要求"完美输出"。

```text:terminal
第 1 轮 — 生成基础组件：
"创建 UserCard 组件，React 18 + TypeScript，接收 name、avatar、role 三个 props。
头像圆形 48px，role 显示为彩色标签。"

第 2 轮 — 补充交互细节：
"给 UserCard 加 hover 效果：hover 时显示 email tooltip，tooltip 从下方滑入，
背景半透明黑色，白色文字。"

第 3 轮 — 样式微调：
"tooltip 距离头像底部 8px，箭头朝上，圆角 4px。
admin 标签改为 #EF4444，editor 为 #3B82F6，viewer 为 #9CA3AF。"
```

每轮只关注一个维度（结构 → 交互 → 样式），AI 的上下文负担更小，输出质量更高。

### 场景二：样式调试

CSS 布局问题（flex 对齐、grid 间隙、响应式断点）是前端开发者日常耗时最多的环节之一。
```text:terminal
用户输入：
"侧边栏在 768px 以下没有收起。父容器 flex; flex-direction:column;
侧边栏 240px; position:sticky。"
AI 输出：→ 分析 sticky + flex-direction:column 冲突 → media query 方案 + 过渡动画
```

#### Playwright **MCP（模型上下文协议）** 截图验证

OpenCode 集成了 Playwright MCP，可以在对话中直接截图验证布局效果：

```text:terminal
用户输入：
"打开 http://localhost:5173/dashboard，截图看下侧边栏在 768px 宽度下的表现。"

AI 通过 Playwright MCP 截图 → 用户确认问题 → AI 生成修复代码 → 再次截图验证
```

"看到问题 → 修复 → 确认修复"的闭环，比纯文字描述布局问题高效得多。

### 场景三：测试编写

组件单元测试和 E2E（端到端）测试的编写枯燥但必要。AI 能根据组件代码自动生成测试用例骨架。

```text:terminal
用户输入："为 UserCard 写 Vitest 测试，覆盖正常渲染、角色颜色、hover tooltip。"
AI 输出：→ 3-5 个 test case，@testing-library/react 标准写法，含 mock 逻辑
```

#### AGENTS.md 覆盖率配置

在项目的 AGENTS.md 中声明测试覆盖率要求，OpenCode 会自动检查生成的测试是否达标。

```text:agentsmd:AGENTS.md
## 测试要求

- 所有组件必须有对应的测试文件（`*.test.tsx`）
- 单行覆盖率 ≥ 80%，分支覆盖率 ≥ 70%
- 测试框架：Vitest + @testing-library/react
- 运行 `npm run test:coverage` 验证覆盖率
- 如果覆盖率不达标，AI 必须补充测试用例直到达标
```

这样配置后，AI 生成测试时会主动检查覆盖率，而不是只生成几个"看起来够了"的 case。

### AI 不擅长的前端领域
| 领域 | 原因 | 建议 |
|------|------|------|
| **复杂动画逻辑** | 涉及物理曲线、帧同步、性能约束 | AI 生成骨架，关键帧手动调优 |
| **浏览器兼容性** | 不同引擎渲染差异需实际验证 | AI 给已知 workaround，无法替代实测 |
| **性能优化** | 需要真实运行时数据 | AI 分析代码模式，profiler 数据人工解读 |

---

## OpenCode 实战配置

将上述场景落地到 OpenCode，需要三个层面的配置：项目级约束（AGENTS.md）、工作流 **Skill（技能）**、运行时配置（opencode.json）。

### AGENTS.md：项目级约束

```text:agentsmd:AGENTS.md
# 前端项目 AGENTS.md

## 技术栈
- React 18 + TypeScript 5.x
- Vite 构建，Tailwind CSS 样式
- Vitest + @testing-library/react 测试
- ESLint + Prettier 代码规范

## 角色定义
你是前端开发专家。生成组件时：
1. 始终使用 TypeScript，导出 Props 类型定义
2. 使用函数组件 + Hooks，禁止 class 组件
3. 样式优先用 Tailwind class，复杂样式才用 CSS Module
4. 每个组件必须附带对应测试文件

## 约束
- 不要修改 package.json 的依赖版本
- 不要删除已有测试
- 组件文件放在 src/components/ 下，按功能分子目录
- 导出方式：具名导出，不要 default export
```

### Skill 配置：组件生成工作流

封装为 Skill，AI 按固定模板产出一致的代码结构：

```text:json:opencode-configs/component-skill.json
{
  "name": "react-component",
  "description": "按标准模板生成 React 组件",
  "prompt_template": "按照以下模板生成 React 组件：\n1. 创建 {name}.tsx 在 src/components/{category}/\n2. 导出 Props 类型和组件\n3. 创建 {name}.test.tsx 测试文件\n4. 在 src/components/index.ts 中添加导出\n5. 运行类型检查 npm run type-check",
  "parameters": {
    "name": { "type": "string", "required": true },
    "category": { "type": "string", "default": "common" }
  }
}
```

### opencode.json：运行时配置

```text:json:opencode.json
{
  "provider": "anthropic",
  "model": "claude-sonnet-4-20250514",
  "mcp": {
    "playwright": {
      "command": "npx",
      "args": ["@anthropic/mcp-playwright"]
    }
  },
  "permissions": {
    "allow": ["read", "write", "bash"],
    "deny": ["bash(rm -rf *)"]
  }
}
```

---

## OpenCode **Prompt（提示词）** 进阶技巧

掌握 prompt 的组织方式，能显著提升 AI 输出质量。以下是几个实战中验证有效的模式。

### 多轮对话：上下文累积

不要在一个 prompt 里塞所有需求。分轮构建上下文，每轮聚焦一个主题：

```text:terminal
第 1 轮（背景）：
"我在做一个后台管理系统，技术栈是 React 18 + TypeScript + Tailwind。
现在需要一个数据表格组件，支持排序、筛选、分页。"

第 2 轮（细节）：
"表格数据来自 /api/users 接口，返回格式：
{ data: User[], total: number, page: number, pageSize: number }。
User 类型有 id、name、email、role、createdAt 字段。"

第 3 轮（实现）：
"先生成表格基础结构和类型定义，不要急着写排序筛选逻辑。"
```

前两轮帮 AI 理解业务背景，第三轮才进入具体实现。比一个 500 字的 prompt 效果好得多。

### MCP 工具调用

OpenCode 通过 MCP 协议连接外部工具，实现"边做边验证"：

```text:terminal
# Playwright：截图验证 UI
"用 Playwright 打开 http://localhost:5173，截图看下登录页面的布局。"

# 文件系统：读取现有代码作为上下文
"读一下 src/components/Header.tsx，我在它下面加一个下拉菜单。"

# 终端：执行命令验证结果
"运行 npm run build，看看有没有类型错误。"
```

### 错误恢复 Prompt

代码生成出错时，把错误信息贴给 AI 比重新描述需求更高效：

```text:terminal
用户输入：
"上次生成的 UserCard 组件有类型错误：
Type '{ name: string; }' is missing the following properties
from type 'UserCardProps': avatar, role。修复一下。"

AI 输出：→ 定位到遗漏的 props → 补充默认值或修改调用处
```

关键是要包含完整的错误信息（类型、行号、上下文），AI 才能精准定位。

---

## 研究人员的 AI 辅助工作流

研究人员的核心工作——文献梳理、数据分析、论文写作——都可以用 AI 提速，但使用方式和前端开发截然不同。

### 文献综述辅助

面对 10-20 篇论文，AI 能快速提取核心观点、方法论和结论，生成结构化对比表格。

```text:terminal
用户输入："阅读以下 5 篇 federated learning 论文摘要，提取研究方法、数据集、主要结论，生成对比表格。"
AI 输出：→ Markdown 表格（论文名 | 方法 | 数据集 | 结论 | 局限性）+ 方法演进脉络总结
```

AI 只能处理你提供的摘要文本，无法替你完成全文精读。综述的深度判断仍然依赖研究者本身。

### 数据分析辅助

Python 数据处理脚本（pandas 清洗、matplotlib 可视化）是 AI 辅助效率最高的环节。

```text:terminal
用户输入："用 pandas 读取 survey_results.csv，按 department 分组计算 salary 中位数，seaborn 画箱线图。"
AI 输出：→ 完整 Python 脚本（数据清洗 + 分组统计 + 绑图）+ 缺失值检查建议
```

### 论文写作辅助

AI 擅长改进学术写作的清晰度和逻辑性，但不适合生成原创论点。

```text:terminal
用户输入："改进这段方法论的学术表达：'我们用了 federated learning，让各节点不传原始数据，最后合参数。'"
AI 输出：→ "We employ federated learning to enable distributed model training without transmitting raw data..." + 修改说明
```

### 学术诚信注意事项

使用 AI 辅助学术工作时，三条红线不能碰：

1. **引用必须验证**。AI 可能编造不存在的论文和引用，每条引用都要回溯原文确认。
2. **生成内容必须标注**。多数期刊和会议已要求声明 AI 工具的使用范围。
3. **核心论点不能外包**。AI 可以润色表达、整理数据，但研究假设和分析结论必须由研究者独立完成。

---

## 使用边界与最佳实践

AI 编程工具威力大，但用错场景反而添乱。

### 什么时候不该用 AI

| 场景 | 风险 | 原因 |
|------|------|------|
| **安全敏感代码**（认证、加密、权限校验） | AI 可能遗漏边界条件 | 安全逻辑需要人工审计，AI 缺乏安全上下文 |
| **性能关键路径**（热循环、渲染管线） | AI 生成的代码可能引入不必要的抽象 | 性能优化依赖 profiler 数据，不是代码模式 |
| **数据库迁移脚本** | AI 可能生成破坏性操作 | 数据丢失不可逆，必须人工 review |
| **法律合规相关** | AI 不了解具体法规要求 | 合规判断需要专业法务支持 |

简单原则：**代码出错能回滚，数据丢失不可逆，安全漏洞影响全局**。遇到这三类场景，AI 只能辅助（生成初稿、建议方案），最终决策必须人工完成。

### Token 预算与上下文优化
长对话快速消耗 context window。实用技巧：

1. **及时总结**。对话超过 10 轮时，让 AI 总结进展，然后开新对话继续。
2. **分离关注点**。样式问题和逻辑问题不要混在同一个对话里。
3. **利用 AGENTS.md**。项目规范写进 AGENTS.md，每轮不用重复说明技术栈。
4. **精确指定文件和行号**。"读 src/components/UserCard.tsx 第 20-40 行" 比 "帮我看下 UserCard" 省得多。
5. **大文件分段**。超过 500 行的文件，让 AI 只读需要修改的部分。

> **进一步阅读**：→ [**Harness Engineering（驾驭工程）** 理论框架](harness-engineering-theory.md) 介绍了 AI 编程工程化的三大原则，同样适用于研究场景。

---

## 关联章节

- → [什么是 Harness Engineer](what-is-harness-engineer.md)
- → [AI 编程工具生态对比](ecosystem-comparison.md)
- → [多角色阅读路径](../00-guide/reading-paths.md)
