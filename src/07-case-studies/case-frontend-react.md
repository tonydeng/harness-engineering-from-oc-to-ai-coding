# 案例：前端 React 仪表板开发

> 使用 OpenCode + React 开发数据仪表板组件，从 Figma 设计稿到生产部署。AI 加速了 80% 的编码工作，但组件设计决策仍需人工把关。

## 案例概述

仪表板是前端开发中最常见的场景：图表、表格、筛选器、状态卡片，组件多、布局复杂。传统开发模式下一个包含 6 个图表和 3 个筛选器的仪表板需要 3 天，本案例使用 OpenCode + Claude Sonnet 4 + Playwright **MCP（模型上下文协议）** 将周期压缩到 0.5 天，测试覆盖率从 40% 提升到 85%。

核心经验：AI 擅长生成组件骨架和重复性代码，但 CSS 细节调整和组件 Props 设计仍需要人工判断。流程中设置了三个"人工检查点"，确保 AI 输出不偏离设计规范。

## 1. 项目背景

### 技术栈

| 层级 | 技术选型 |
|------|----------|
| 框架 | React 18 + TypeScript |
| 构建 | Vite 5 |
| UI 库 | shadcn/ui + Tailwind CSS |
| 图表 | Recharts |
| 测试 | Playwright（E2E）+ Vitest（单元） |
| 部署 | Vercel + GitHub Actions |

### 开发痛点

| 问题 | 数据 |
|------|------|
| 组件骨架搭建耗时 | 占总开发时间 30% |
| 图表配置重复 | 每个图表 40-60 行配置代码 |
| E2E 测试编写慢 | 一个完整流程测试 40-50 行 |
| 像素级还原耗时 | CSS 微调占前端工时 25% |

## 2. OpenCode 配置

在动手写代码之前，先配置好 OpenCode 的工作环境。这一步决定了 AI 的行为边界和可用工具。

### AGENTS.md 项目约束

在项目根目录创建 `AGENTS.md`，告诉 OpenCode 这个项目的角色和约束：

```markdown:AGENTS.md
# 前端仪表板项目

## 角色定位
你是前端开发工程师，负责 React 仪表板组件的开发。

## 技术约束
- UI 组件库：只用 shadcn/ui，不要引入其他 UI 库
- 样式方案：Tailwind CSS，遵循项目 Design Tokens（src/styles/tokens.css）
- 图表库：Recharts，不使用 ECharts 或 Chart.js
- 状态管理：React useState + useReducer，不引入 Redux
- 类型安全：所有 Props 必须定义 TypeScript interface

## 代码规范
- 组件文件使用 PascalCase（DashboardCard.tsx）
- 工具函数使用 camelCase（formatChartData.ts）
- 每个组件必须导出 Props interface
- 禁止使用 any 类型
- CSS 类名按 Tailwind 规范：间距用 gap/padding，不用 margin

## 文件结构
src/
  components/     # 可复用组件
  features/       # 业务功能模块
  hooks/          # 自定义 Hooks
  styles/         # Design Tokens 和全局样式
  types/          # 共享 TypeScript 类型
```

### opencode.json MCP 工具配置

启用 Playwright 和文件系统 MCP，让 OpenCode 能操作浏览器和管理文件：

```json:opencode.json
{
  "mcp": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    },
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "./src"]
    }
  }
}
```

Playwright MCP 让 OpenCode 能直接操作浏览器进行 E2E 测试，文件系统 MCP 则让它能读写项目文件，生成和修改组件代码。

## 3. 开发流程

### 设计阶段：Figma 截图 → 组件骨架

将 Figma 设计稿截图提供给 OpenCode，生成组件代码骨架。AI 输出了完整的 TypeScript interface 和组件结构，包括布局、占位图表和筛选器区域。

实际的 OpenCode 对话过程如下：

```
User: "根据这个 Figma 设计稿，创建 Dashboard 组件。
- 使用 React 18 + TypeScript
- UI: shadcn/ui + Tailwind CSS
- 图表: Recharts
- 布局: CSS Grid，响应式 3 列→1 列
- Props: { data: DashboardData, onFilterChange: (filters) => void }"

OpenCode: [读取 Figma 截图，生成 Dashboard.tsx，包含完整的 TypeScript interface
和 Grid 布局结构]

User: "Props 太扁平了，按关注点拆分：dataProps, layoutProps, callbackProps"

OpenCode: [重构 Props 接口，拆分为 DashboardDataProps、DashboardLayoutProps、
DashboardCallbackProps 三个独立 interface]
```

注意第二轮对话的作用。AI 第一版生成的 Props 往往是一个扁平的大对象，这在小项目里能用，但组件复用时会很痛苦。通过一轮追问，让 AI 按关注点拆分，后续维护成本大幅降低。

**人工检查点 1**：审查 Props 设计是否合理。AI 倾向于把所有数据塞进一个大 Props 对象，需要拆分为更细粒度的子组件 Props（数据 Props、样式 Props、回调 Props）。

### Figma → React 转换：更详细的流程

实际项目中，从 Figma 设计稿到可运行的 React 组件需要经过多个环节。以下是完整的转换流程和对应的 **Prompt（提示词）** 示例。

#### 第 1 步：设计稿分析

先让 AI 分析 Figma 截图，输出组件拆分方案，而不是直接生成代码：

```
User: "分析这个 Figma 设计稿，列出所有可见组件、它们的层级关系和交互方式。
不要写代码，只输出组件拆分方案。"

OpenCode: [输出组件树结构]
- DashboardLayout（Grid 容器）
  - StatsCard × 4（顶部统计卡片）
  - ChartCard × 3（图表容器，含标题和筛选器）
    - Recharts 图表（Bar/Line/Pie）
  - FilterPanel（日期范围 + 部门筛选 + 排序）
  - DataTable（底部数据表格）
```

这一步的价值在于：AI 拆分的组件粒度往往比你想的更细或更粗，先确认拆分方案再写代码，避免后面大面积重构。

#### 第 2 步：逐组件生成

确认拆分方案后，逐个组件生成代码。每个组件单独一轮对话，避免上下文污染：

```
User: "创建 StatsCard 组件。
Props: { title: string; value: number; change: number; icon: LucideIcon }
功能：显示标题、数值、变化百分比（正数绿色，负数红色），
变化超过 10% 时加粗显示。
使用 shadcn/ui 的 Card 组件。"

OpenCode: [生成 StatsCard.tsx，包含完整的 Props interface、
条件样式逻辑和 shadcn Card 集成]

User: "change 为 0 时应该显示灰色，不是绿色。另外 icon 要支持
传入自定义 size prop。"

OpenCode: [修正颜色逻辑：>0 绿色，<0 红色，=0 灰色；
icon 增加 size?: number prop，默认 20]
```

#### 第 3 步：组合与布局

所有子组件生成完毕后，组合成完整的 Dashboard：

```
User: "把所有子组件组合到 Dashboard 中。
布局规则：
- 顶部：4 个 StatsCard，grid-cols-4，间距 gap-4
- 中部：3 个 ChartCard，grid-cols-2（第一个占两列）
- 底部：DataTable，占满宽度
- 响应式：sm:grid-cols-2，md:grid-cols-3，lg:grid-cols-4"

OpenCode: [生成 Dashboard.tsx 主文件，组合所有子组件，
应用 Grid 布局和响应式断点]
```

### 实现阶段：AI 生成 + 手动调整

AI 负责约 80% 的编码工作：

| 任务 | AI 完成度 | 说明 |
|------|----------|------|
| 组件骨架 | 95% | 布局、占位、基本结构 |
| 图表配置 | 85% | Recharts 的 ResponsiveContainer + 基础配置 |
| 筛选器逻辑 | 80% | 状态管理、事件绑定 |
| 响应式布局 | 70% | Tailwind 断点，但细节需调整 |
| 无障碍属性 | 60% | aria-label 等基本属性 |

需要人工调整的部分（约 20%）：CSS 间距和对齐的像素级微调、组件间数据流的设计决策、图表 Tooltip 的自定义格式化、加载状态和空状态的交互细节。

**人工检查点 2**：逐个组件检查 CSS 输出，确保与设计稿一致。

### 性能优化：AI 辅助 + 人工判断

仪表板组件数量多，性能容易成为瓶颈。以下是 AI 辅助优化的具体过程和优化前后的对比数据：

#### 优化前的性能基线

```
User: "分析 Dashboard 的性能问题。当前状态：
- 6 个图表组件同时渲染
- 筛选器切换时全部图表重绘
- 首屏加载时间约 3.2 秒
- FCP (First Contentful Paint) 1.8 秒
请给出优化方案。"

OpenCode: [分析代码，识别出 5 个优化点]
1. 图表组件未使用 React.memo，每次父组件渲染都重新创建
2. 筛选器状态变更触发全量重绘
3. 图表数据未做 useMemo 缓存
4. Recharts 的 ResponsiveContainer 每次 resize 触发重绘
5. 首屏加载了全部 6 个图表的 ECharts 库（约 800KB）
```

#### 优化实施

```
User: "按优先级执行优化：
1. 给所有图表组件添加 React.memo，只在 data prop 变化时重绘
2. 把筛选器状态提升到 Dashboard 级别，用 useReducer 管理
3. 图表数据用 useMemo 缓存，依赖筛选条件
4. 首屏只加载前 3 个图表，剩余用 IntersectionObserver 懒加载"

OpenCode: [逐项实施优化，生成修改后的组件代码]
```

#### 优化前后对比数据

| 指标 | 优化前 | 优化后 | 提升幅度 |
|------|--------|--------|----------|
| 首屏加载时间 | 3.2s | 1.4s | -56% |
| FCP | 1.8s | 0.9s | -50% |
| TTI (Time to Interactive) | 4.1s | 2.0s | -51% |
| 筛选器切换重绘时间 | 800ms | 120ms | -85% |
| JS Bundle 大小 | 1.2MB | 680KB | -43% |
| 筛选器切换重绘组件数 | 6 个 | 2 个 | -67% |

关键优化手段是懒加载和 React.memo。AI 能快速生成 IntersectionObserver 的懒加载代码，但"哪些组件优先加载"这个决策需要人工判断。

### 测试阶段：Playwright MCP 集成

Playwright MCP 让 OpenCode 能直接操控浏览器进行测试，而不是仅生成测试代码。以下是具体的配置和使用方式。

#### Playwright MCP 配置详解

```json:opencode.json
{
  "mcp": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"],
      "env": {
        "PLAYWRIGHT_BROWSERS_PATH": "~/.cache/ms-playwright",
        "HEADLESS": "true"
      }
    }
  }
}
```

配置完成后，OpenCode 可以通过 Playwright MCP 执行以下操作：

- 打开浏览器，导航到本地开发服务器
- 截取页面截图，与 Figma 设计稿对比
- 执行点击、输入、滚动等交互操作
- 检查元素的可见性、属性值和样式
- 运行 E2E 测试并收集结果

#### 实际测试对话

让 AI 基于组件代码生成端到端测试，覆盖页面加载、筛选器切换、响应式布局 3 个核心场景，每个场景 15-25 行 Playwright 代码。

```
User: "用 Playwright 测试 Dashboard：
- 页面加载后 3 个图表可见
- 筛选器切换后图表数据更新
- 移动端 768px 以下布局变为单列"

OpenCode: [调用 Playwright MCP，生成 dashboard.spec.ts，包含三个 test 块，
每个块有具体的 viewport 断言和元素可见性检查]

User: "图表数据更新的断言太弱了，不只是检查 visible，要验证数据内容变化。
比如切换日期范围后，图表的 tooltip 数值应该不同"

OpenCode: [增强断言逻辑，添加 tooltip 文本内容比对，
用 page.locator 获取具体数据值而非仅检查元素存在]
```

关键在于第二轮追问。AI 第一版测试通常只检查元素是否存在，这跟没测差不多。要求它验证数据内容的变化，测试才算真正有效。

**人工检查点 3**：验证测试断言是否真正检验了业务逻辑，而不只是检查元素存在。

#### Playwright MCP 的可视化回归测试

利用 Playwright MCP 的截图能力，可以做像素级的视觉回归测试：

```
User: "用 Playwright 截取 Dashboard 的桌面端和移动端截图，
对比设计稿的布局差异。桌面端 viewport 1440px，移动端 375px。"

OpenCode: [调用 Playwright MCP 打开浏览器，分别设置 viewport，
截取两张截图并输出尺寸、间距差异报告]
```

这种方式比手动截图再对比高效得多。AI 能自动发现间距偏差、字体大小不一致、颜色差异等问题，生成可视化的差异报告。

### 团队协作配置

多人协作时，AGENTS.md 需要包含团队级的规范，确保所有成员（包括 AI）生成的代码风格一致。

#### 团队级 AGENTS.md 配置

```markdown:AGENTS.md (团队协作版)
# 团队协作规范

## Git 工作流
- 分支命名：feat/xxx、fix/xxx、chore/xxx
- 提交信息格式：type(scope): description
  - 示例：feat(dashboard): 添加日期范围筛选器
  - 示例：fix(chart): 修复 Recharts 响应式容器高度问题
- PR 必须关联 Issue，描述变更内容和测试结果

## Code Review 清单
- [ ] 组件 Props 是否按关注点拆分
- [ ] 是否使用了 any 类型
- [ ] 图表组件是否包裹在 ResponsiveContainer 中
- [ ] 交互元素是否有 aria-label
- [ ] 新增组件是否添加了对应的单元测试

## 组件文档
- 每个公开组件必须有 README.md，说明用途、Props、使用示例
- 复杂组件（图表、表格）必须有 Storybook stories
- 组件修改必须更新对应的文档和 stories

## 设计 Token 同步
- 颜色、间距、字体等值从 src/styles/tokens.css 读取
- 禁止在组件中硬编码颜色值（如 #000、#fff）
- 新增 Token 必须在 tokens.css 中定义，不在组件内新增
```

#### 代码风格自动检查

在 opencode.json 中配置 lint 规则，让 AI 生成的代码自动通过 ESLint 检查：

```json:opencode.json (补充配置)
{
  "context": {
    "files": ["AGENTS.md", ".eslintrc.js", "tailwind.config.ts"]
  },
  "mcp": {
    "playwright": {
      "command": "npx",
      "args": ["@playwright/mcp@latest"]
    }
  }
}
```

把 `.eslintrc.js` 和 `tailwind.config.ts` 加入上下文文件，OpenCode 在生成代码时会自动参考这些配置，减少后期 lint 修复工作量。

### 部署阶段：CI/CD 自动化

GitHub Actions 自动运行 lint、Vitest 单元测试（含覆盖率报告）、Playwright E2E 测试。覆盖率低于 80% 时构建失败。

CI 配置示例：

```yaml:.github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npm run lint
      - run: npm run test:unit -- --coverage
      - run: npx playwright install --with-deps
      - run: npm run test:e2e
      - name: Coverage check
        run: |
          COVERAGE=$(cat coverage/coverage-summary.json | jq '.total.lines.pct')
          if [ $(echo "$COVERAGE < 80" | bc) -eq 1 ]; then
            echo "Coverage below 80%, failing build"
            exit 1
          fi
```

### AGENTS.md 约束配置：代码质量防线

在项目根目录的 `AGENTS.md` 中添加代码质量规则，让 OpenCode 在生成代码时自动遵守：

```markdown:AGENTS.md
# 代码质量约束

## 强制规则（违反则拒绝生成）
- 组件必须导出 Props interface，禁止内联类型定义
- 禁止使用 any，必须明确类型
- 每个组件文件不超过 200 行，超过则拆分子组件
- 图表组件必须包裹在 ResponsiveContainer 中
- 所有交互元素必须有 aria-label

## 风格偏好（优先遵守，但可覆盖）
- 使用 const function 声明组件，不用 function 关键字
- 事件处理函数命名：handle + 事件名（handleFilterChange）
- 状态变量命名：is + 形容词（isLoading）或 动词 + 名词（selectedFilter）

## 禁止操作
- 不要引入 lodash，用原生 JS 方法替代
- 不要使用 class component，全部函数组件
- 不要在组件内直接 fetch 数据，通过 Props 传入
```

这些约束通过 AGENTS.md 注入 OpenCode 的上下文，AI 生成代码时会自动遵守。比口头告诉它"不要用 any"可靠得多，因为约束是持久化的，每次对话都生效。

## 4. 效果数据

| 指标 | 实施前 | 实施后 | 变化 |
|------|--------|--------|------|
| 开发时间 | 3 天 | 0.5 天 | -83% |
| 测试覆盖率 | 40% | 85% | +45% |
| E2E 测试用例数 | 2 个 | 8 个 | +300% |
| CSS 还原度 | 85% | 92% | +7% |
| 组件复用率 | 30% | 65% | +35% |

## 5. 经验教训

1. **AI 生成的 CSS 需要手动微调**。Tailwind 类名组合经常出现间距偏差，尤其是 gap、padding 的数值选择。建议在 AI 生成后用浏览器 DevTools 逐项检查。

2. **组件 Props 设计需要人工审查**。AI 倾向于扁平化 Props 结构，实际项目中应按关注点拆分（数据 Props、样式 Props、回调 Props）。

3. **Figma 截图的质量直接影响生成质量**。高分辨率、标注清晰的截图比模糊截图的生成效果好 3 倍以上。

4. **E2E 测试生成有天花板**。AI 能生成基础流程测试，但复杂的条件分支和异步等待逻辑仍需手动补充。

## 关联章节

- → [全流程自动化](case-full-pipeline.md)（前端在全流程中的应用）
- → [**Skill（技能）** 开发](../05-skills/)（自定义前端开发 Skill）
- → [环境搭建](../03-setup/)（Playwright MCP 配置）
