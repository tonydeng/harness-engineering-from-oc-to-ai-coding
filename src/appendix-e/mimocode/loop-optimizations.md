# 循环工程优化设计

> **适合读者**: Agent工程师(AE), 架构师(SYSA), 效率追求者

本章详细分析 MiMo Code 在 **Loop Engineering（循环工程）** 方面的深入优化设计。循环工程关注的核心问题是："我不在时工作如何继续？" MiMo Code 通过子智能体系统、Max Mode 并行采样、动态工作流和 Dream/Distill 机制，系统性地解决了这个问题。

## 循环工程的核心挑战

在 [Harness Engineering 理论框架](../../01-introduction/harness-engineering-theory.md) 中，我们定义了 L4 循环工程的失败模式：**Token 浪费/死循环**。具体表现为：

1. **单点瓶颈**：单个智能体串行执行所有任务，效率低下
2. **决策质量不稳定**：单次采样可能产生次优方案
3. **编排逻辑脆弱**：自然语言定义的工作流容易出错
4. **经验无法积累**：每次会话都从零开始

MiMo Code 针对每个挑战都设计了工程化的解决方案。

## 优化一：子智能体系统

### 问题描述

传统编码智能体采用单智能体架构，所有任务串行执行。当任务规模增大时，效率成为瓶颈。

### 解决方案

MiMo Code 实现了灵活的子智能体系统：

```
主智能体（Build/Plan/Compose）
    │
    ├── 子智能体 1（并行执行）
    ├── 子智能体 2（并行执行）
    └── 子智能体 3（并行执行）
```

### 核心特性

| 特性 | 说明 |
|------|------|
| **按需创建** | 主智能体可以根据任务需要创建子智能体 |
| **并行执行** | 多个子智能体可以同时工作 |
| **生命周期跟踪** | 系统跟踪每个子智能体的状态 |
| **取消支持** | 可以取消正在执行的子智能体 |
| **后台执行** | 子智能体可以在后台运行，不阻塞主智能体 |

### 使用示例

```bash
# 主智能体会自动创建子智能体处理并行任务
# 例如：同时实现登录、注册、密码重置三个接口

# 查看子智能体状态
/agents

# 取消特定子智能体
/cancel-agent <agent-id>
```

### 设计决策

MiMo Code 的子智能体系统与 OpenCode 的设计有显著差异：

| 维度 | OpenCode | MiMo Code |
|------|----------|-----------|
| **创建方式** | 显式配置 | 主智能体按需创建 |
| **上下文共享** | 独立上下文 | 共享当前会话上下文 |
| **生命周期** | 手动管理 | 系统自动跟踪 |
| **取消机制** | 有限支持 | 完整支持 |

## 优化二：Max Mode 并行采样

### 问题描述

单次采样可能产生次优方案。模型的推理具有随机性，同样的输入可能产生不同的输出。

### 解决方案

MiMo Code 引入了 Max Mode 并行采样机制：

```
用户输入
    │
    ↓
并行生成 N 个候选方案（默认 N=5）
    │
    ├── 候选 1：推理 + 工具调用规划
    ├── 候选 2：推理 + 工具调用规划
    ├── 候选 3：推理 + 工具调用规划
    ├── 候选 4：推理 + 工具调用规划
    └── 候选 5：推理 + 工具调用规划
    │
    ↓
独立判断器比较所有候选
    │
    ↓
选择最佳方案执行
```

### 设计细节

1. **并行生成**：5 个候选方案同时生成，不增加延迟
2. **独立判断**：使用同一模型作为判断者，比较推理过程和行动计划
3. **温度控制**：默认温度为 1，确保采样多样性
4. **成本权衡**：性能提升 10-20%，代价是约 4-5 倍 token 消耗

### 使用示例

```json
{
  "experimental": {
    "maxMode": true
  }
}
```

### 效果对比

| 场景 | 单次采样 | Max Mode |
|------|---------|----------|
| 决策质量 | 取决于单次运气 | 选择最佳方案 |
| 成本 | 1x | 4-5x |
| 适用场景 | 简单任务 | 复杂、高风险任务 |

### 与 Goal 的协同

Max Mode 和 Goal 代表测试时计算的两个正交方向：

- **Max Mode**：并行的，在同一步骤上花费 N 倍计算选择最佳选项
- **Goal**：串行的，在同一任务内花费更多时间进行自检和持续执行

两者可以同时启用，相互补充。

## 优化三：动态工作流（Dynamic Workflow）

### 问题描述

传统工作流使用自然语言定义（SKILL.md），存在以下问题：

| 问题 | 说明 |
|------|------|
| **上下文压缩吞没步骤** | 压缩时可能丢失关键步骤 |
| **模型跳过阶段** | 模型可能"认为"某些步骤不重要 |
| **分支逻辑依赖判断** | 模型的分支判断可能错误 |
| **重试逻辑不可靠** | 模型可能忘记重试 |
| **执行路径不一致** | 同一流程两次运行可能不同 |

### 解决方案

Dynamic Workflow 将编排逻辑从提示词转为代码：

```javascript
// 传统方式（自然语言）
// "先设计数据库，然后实现数据访问层，然后实现 API，最后写测试"

// Dynamic Workflow（代码）
await pipeline([
  agent({ prompt: "设计数据库 schema" }),
  agent({ prompt: "实现数据访问层" }),
  agent({ prompt: "实现 API 接口" }),
  agent({ prompt: "编写测试" })
]);
```

### 核心 API

| API | 说明 | 保证 |
|-----|------|------|
| `agent()` | 调度子智能体 | 原子性、可恢复性 |
| `parallel()` | 并行执行 | 并发控制、结果聚合 |
| `pipeline()` | 顺序执行 | 依赖管理、错误传播 |
| `workflow()` | 调用其他脚本 | 可复用、可组合 |

### 执行保证

Dynamic Workflow 提供以下保证：

1. **确定性**：相同的输入产生相同的输出
2. **原子性**：每个 agent() 调用要么完全成功，要么完全失败
3. **可恢复性**：每个 agent() 的结果同步写入磁盘，中断后可从日志恢复
4. **隔离性**：每个 agent() 在隔离沙箱中执行，互不干扰

### 与 Anthropic Dynamic Workflow 的兼容性

MiMo Code 的实现兼容 Anthropic Dynamic Workflow 的核心语义，并扩展了以下能力：

| 能力 | 说明 |
|------|------|
| **`workflow()` 原语** | 脚本可以调用其他脚本，实现可复用和组合 |
| **结果持久化** | 每个 `agent()` 调用的结果同步写入磁盘 |
| **沙箱文件操作** | 在沙箱内可以直接读写文件 |

### 使用示例

```javascript
// 项目迁移工作流
export default async function migrateProject() {
  // 1. 分析现有代码
  const analysis = await agent({
    prompt: "分析项目结构和依赖"
  });
  
  // 2. 并行迁移各个模块
  const modules = await parallel([
    agent({ prompt: `迁移用户模块：${analysis.userModule}` }),
    agent({ prompt: `迁移订单模块：${analysis.orderModule}` }),
    agent({ prompt: `迁移支付模块：${analysis.paymentModule}` })
  ]);
  
  // 3. 集成测试
  await agent({
    prompt: "运行集成测试并修复问题"
  });
  
  // 4. 部署
  await workflow("./scripts/deploy.js");
}
```

### Dynamic Workflow DSL 语法参考

Dynamic Workflow DSL 提供了完整的函数式编程接口，用于构建复杂的工作流编排逻辑。以下是完整的 DSL 函数列表及其使用说明：

#### `agent()`

**目的**：调度子智能体执行特定任务

**签名**：`agent(config: AgentConfig) => Promise<AgentResult>`

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| prompt | string | 是 | 智能体执行的任务描述 |
| context | object | 否 | 额外的上下文信息 |
| timeout | number | 否 | 超时时间（毫秒） |
| retry | number | 否 | 重试次数 |

**返回值**：

| 类型 | 说明 |
|------|------|
| Promise<AgentResult> | 智能体执行结果，包含执行状态、输出内容和元数据 |

**示例**：

```javascript
await agent({
  prompt: "分析项目结构和依赖",
  context: { projectPath: "/workspace/my-project" },
  timeout: 30000,
  retry: 2
});
```

#### `parallel()`

**目的**：并行执行多个智能体任务

**签名**：`parallel(tasks: AgentConfig[]) => Promise<ParallelResult>`

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| tasks | AgentConfig[] | 是 | 要并行执行的任务列表 |

**返回值**：

| 类型 | 说明 |
|------|------|
| Promise<ParallelResult> | 并行执行结果，包含每个任务的执行结果和执行统计 |

**示例**：

```javascript
const results = await parallel([
  agent({ prompt: "迁移用户模块" }),
  agent({ prompt: "迁移订单模块" }),
  agent({ prompt: "迁移支付模块" })
]);
```

#### `pipeline()`

**目的**：顺序执行多个智能体任务，前一个任务的结果可以传递给下一个任务

**签名**：`pipeline(tasks: PipelineTask[]) => Promise<PipelineResult>`

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| tasks | PipelineTask[] | 是 | 顺序执行的任务列表，每个任务可以包含输入映射 |

**返回值**：

| 类型 | 说明 |
|------|------|
| Promise<PipelineResult> | 流水线执行结果，包含每个阶段的执行结果和整个流程的状态 |

**示例**：

```javascript
await pipeline([
  { task: agent({ prompt: "设计数据库 schema" }) },
  { task: agent({ prompt: "实现数据访问层" }), input: "schema" },
  { task: agent({ prompt: "实现 API 接口" }), input: "database" },
  { task: agent({ prompt: "编写测试" }), input: "api" }
]);
```

#### `workflow()`

**目的**：调用其他脚本，实现工作流的复用和组合

**签名**：`workflow(scriptPath: string, config?: WorkflowConfig) => Promise<WorkflowResult>`

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| scriptPath | string | 是 | 要调用的脚本路径（相对于项目根目录） |
| config | WorkflowConfig | 否 | 额外的配置选项 |

**返回值**：

| 类型 | 说明 |
|------|------|
| Promise<WorkflowResult> | 工作流执行结果，包含脚本执行状态和输出 |

**示例**：

```javascript
await workflow("./scripts/deploy.js", {
  timeout: 60000,
  retry: 1
});
```

#### `foreach()`

**目的**：遍历集合，对每个元素执行指定的任务

**签名**：`foreach(items: any[], task: (item: any) => Promise<any>) => Promise<ForeachResult>`

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| items | any[] | 是 | 要遍历的集合 |
| task | function | 是 | 对每个元素执行的任务函数 |

**返回值**：

| 类型 | 说明 |
|------|------|
| Promise<ForeachResult> | 遍历结果，包含每个元素的执行结果和遍历统计 |

**示例**：

```javascript
await foreach(["用户模块", "订单模块", "支付模块"], async (module) => {
  return await agent({ prompt: `迁移${module}` });
});
```

#### `condition()`

**目的**：根据条件判断执行不同的任务分支

**签名**：`condition(test: () => boolean, then: () => Promise<any>, else?: () => Promise<any>) => Promise<ConditionResult>`

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| test | function | 是 | 条件测试函数，返回布尔值 |
| then | function | 是 | 满足条件时执行的任务 |
| else | function | 否 | 不满足条件时执行的任务（可选） |

**返回值**：

| 类型 | 说明 |
|------|------|
| Promise<ConditionResult> | 条件结果，包含执行分支和执行状态 |

**示例**：

```javascript
await condition(
  () => analysis.hasDatabase,
  () => agent({ prompt: "创建数据库" }),
  () => agent({ prompt: "跳过数据库创建" })
);
```

#### `retry()`

**目的**：对任务执行进行重试

**签名**：`retry(task: () => Promise<any>, options?: RetryOptions) => Promise<any>`

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| task | function | 是 | 要重试的任务 |
| options | RetryOptions | 否 | 重试选项，包括最大重试次数、延迟时间等 |

**返回值**：

| 类型 | 说明 |
|------|------|
| Promise<any> | 重试后的最终结果，如果所有重试都失败，则抛出最后一个错误 |

**示例**：

```javascript
await retry(
  () => agent({ prompt: "运行测试" }),
  { maxRetries: 3, delay: 1000 }
);
```

#### `timeout()`

**目的**：为任务设置超时时间

**签名**：`timeout(task: () => Promise<any>, ms: number) => Promise<any>`

**参数**：

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| task | function | 是 | 要设置超时的任务 |
| ms | number | 是 | 超时时间（毫秒） |

**返回值**：

| 类型 | 说明 |
|------|------|
| Promise<any> | 任务执行结果，如果超时则抛出超时错误 |

**示例**：

```javascript
await timeout(
  () => agent({ prompt: "复杂分析任务" }),
  30000
);
```

#### 完整工作流示例

以下是一个完整的动态工作流示例，展示了如何结合多种 DSL 函数构建一个真实的项目迁移工作流：

```javascript
export default async function migrateProject() {
  // 1. 分析现有代码（串行执行）
  const analysis = await agent({
    prompt: "分析项目结构和依赖",
    timeout: 30000
  });
  
  // 2. 检查是否有数据库（条件判断）
  await condition(
    () => analysis.hasDatabase,
    () => agent({ prompt: "创建数据库 schema" }),
    () => agent({ prompt: "跳过数据库创建" })
  );
  
  // 3. 并行迁移各个模块
  const modules = await parallel([
    agent({ prompt: `迁移用户模块：${analysis.userModule}` }),
    agent({ prompt: `迁移订单模块：${analysis.orderModule}` }),
    agent({ prompt: `迁移支付模块：${analysis.paymentModule}` })
  ]);
  
  // 4. 运行集成测试（带重试机制）
  await retry(
    () => agent({ prompt: "运行集成测试并修复问题" }),
    { maxRetries: 2, delay: 2000 }
  );
  
  // 5. 部署（带超时控制）
  await timeout(
    () => workflow("./scripts/deploy.js"),
    60000
  );
  
  // 6. 生成迁移报告
  await agent({
    prompt: `生成迁移报告，包含模块迁移结果和部署状态`
  });
  
  return {
    status: "completed",
    modules: modules,
    analysis: analysis
  };
}
```

## 优化四：Dream 和 Distill 机制

### 问题描述

传统编码智能体在会话结束后丢失所有经验。用户每次开始新会话时，智能体必须重新学习相同的工作模式。

### 解决方案

MiMo Code 实现了自动化的经验积累机制：

```
历史会话数据
    │
    ├── Dream（每 7 天）
    │   ├── 合并零散记忆
    │   ├── 去重重复条目
    │   ├── 验证文件路径
    │   └── 压缩为紧凑表示
    │
    └── Distill（每 30 天）
        ├── 识别重复工作模式
        ├── 固化为可复用技能
        ├── 生成 CLI 命令
        └── 编写 SOP 文档
```

### Dream 详解

**触发频率**：每 7 天自动触发

**执行者**：独立智能体

**功能**：
1. **合并**：将零散的记忆条目合并为连贯的知识
2. **去重**：删除重复的条目，保留最准确的版本
3. **验证**：检查文件路径是否仍然有效
4. **压缩**：将冗长的记忆压缩为紧凑表示
5. **更新**：将稳定的观察提升到项目记忆

**示例**：

```markdown
# Dream 前
- 用户喜欢使用 TypeScript
- 项目使用 TypeScript
- TypeScript 是主要语言

# Dream 后
- 项目主要使用 TypeScript（用户偏好，已验证）
```

### Dream 扩展点

Dream 机制提供了丰富的扩展点，允许 Skill 生态系统集成自定义的记忆处理逻辑。以下是完整的钩子系统及其使用说明：

#### 钩子系统

| 钩子名称 | 触发时间 | 回调签名 | 说明 |
|----------|----------|------------|------|
| `preDream` | Dream 开始前 | `() => Promise<void>` | 在 Dream 过程开始前执行，可用于初始化资源 |
| `onMemorySelect` | 选择记忆条目时 | `(memories: MemoryItem[]) => Promise<MemoryItem[]>` | 自定义记忆选择逻辑，可过滤或重新排序记忆 |
| `onMemoryCompress` | 压缩记忆时 | `(memories: MemoryItem[]) => Promise<CompressedMemory>` | 自定义记忆压缩算法 |
| `postDream` | Dream 完成后 | `(result: DreamResult) => Promise<void>` | Dream 完成后执行，可用于清理或通知 |

#### 钩子使用示例

```javascript
// 注册 Dream 钩子
await dream({
  hooks: {
    preDream: async () => {
      console.log("开始 Dream 过程");
      // 初始化 Dream 所需资源
    },
    
    onMemorySelect: async (memories) => {
      // 自定义记忆选择逻辑
      // 例如，只选择最近 30 天内的记忆
      const recentMemories = memories.filter(m => 
        Date.now() - m.timestamp < 30 * 24 * 60 * 60 * 1000
      );
      return recentMemories;
    },
    
    onMemoryCompress: async (memories) => {
      // 自定义压缩算法
      // 例如，使用 TF-IDF 算法提取关键词
      const compressed = await compressMemories(memories, {
        algorithm: "tf-idf",
        maxLength: 1000
      });
      return compressed;
    },
    
    postDream: async (result) => {
      console.log("Dream 完成");
      // 更新项目记忆
      await updateProjectMemory(result.compressedMemory);
    }
  }
});
```

#### 在 Skill 生态系统中注册自定义钩子

要将自定义 Dream 钩子注册到 Skill 生态系统中，可以在 Skill 的初始化阶段进行配置：

```javascript
// 在 Skill 初始化时注册 Dream 钩子
export class CustomDreamSkill {
  async initialize() {
    // 注册 preDream 钩子
    await registerDreamHook('preDream', async (context) => {
      // 在 Dream 开始前执行自定义逻辑
      await this.validateDreamPrerequisites(context);
    });
    
    // 注册 onMemorySelect 钩子
    await registerDreamHook('onMemorySelect', async (memories) => {
      // 应用 Skill 特定的记忆过滤逻辑
      return this.filterMemoriesForSkill(memories);
    });
    
    // 注册 onMemoryCompress 钩子
    await registerDreamHook('onMemoryCompress', async (memories) => {
      // 使用 Skill 专有的压缩算法
      return this.compressMemoriesWithSkillLogic(memories);
    });
    
    // 注册 postDream 钩子
    await registerDreamHook('postDream', async (result) => {
      // 在 Dream 完成后更新 Skill 状态
      await this.updateSkillState(result);
    });
  }
  
  async validateDreamPrerequisites(context) {
    // 验证 Dream 执行的前置条件
    // 例如，检查是否有足够的计算资源
    if (!this.hasEnoughResources()) {
      throw new Error("没有足够的计算资源执行 Dream");
    }
  }
  
  filterMemoriesForSkill(memories) {
    // 应用 Skill 特定的记忆过滤逻辑
    // 例如，只保留与当前 Skill 相关的记忆
    return memories.filter(memory => 
      memory.tags.includes(this.skillId) || 
      memory.priority >= this.minPriority
    );
  }
  
  async compressMemoriesWithSkillLogic(memories) {
    // 使用 Skill 专有的压缩算法
    // 例如，结合 Skill 特定的语义表示进行压缩
    return this.semanticCompression(memories);
  }
  
  async updateSkillState(result) {
    // 在 Dream 完成后更新 Skill 状态
    // 例如，更新 Skill 的记忆缓存
    await this.updateMemoryCache(result.compressedMemory);
    await this.notifySkillUsers(result);
  }
}
```

#### 钩子系统集成模式

```javascript
// 高级用法：组合多个 Skill 的 Dream 钩子
export class CompositeDreamSkill {
  constructor() {
    this.hookRegistry = new Map(); // 钩子名称 -> 钩子函数数组
  }
  
  // 注册钩子
  registerHook(hookName, hookFn) {
    if (!this.hookRegistry.has(hookName)) {
      this.hookRegistry.set(hookName, []);
    }
    this.hookRegistry.get(hookName).push(hookFn);
  }
  
  // 执行钩子
  async executeHook(hookName, ...args) {
    const hooks = this.hookRegistry.get(hookName) || [];
    let result = args[0]; // 第一个参数通常是输入
    
    for (const hook of hooks) {
      result = await hook(result, ...args.slice(1));
    }
    
    return result;
  }
  
  // 示例：注册 Dream 钩子
  async setupDreamHooks() {
    // 注册 preDream 钩子
    this.registerHook('preDream', async () => {
      console.log("Composite Dream: 初始化资源");
    });
    
    // 注册 onMemorySelect 钩子
    this.registerHook('onMemorySelect', async (memories) => {
      console.log("Composite Dream: 选择记忆");
      return memories; // 返回处理后的记忆
    });
    
    // 注册 onMemoryCompress 钩子
    this.registerHook('onMemoryCompress', async (memories) => {
      console.log("Composite Dream: 压缩记忆");
      return memories; // 返回压缩后的记忆
    });
    
    // 注册 postDream 钩子
    this.registerHook('postDream', async (result) => {
      console.log("Composite Dream: Dream 完成");
    });
  }
}
```

### Distill 详解

**触发频率**：每 30 天自动触发

**执行者**：独立智能体

**功能**：
1. **模式识别**：从历史会话中识别重复的工作模式
2. **技能固化**：将高置信度的模式固化为可复用技能
3. **命令生成**：生成 CLI 命令简化重复操作
4. **SOP 编写**：编写标准操作流程文档

**示例**：

```markdown
# Distill 发现的模式
用户经常执行以下步骤：
1. 创建新模块
2. 编写单元测试
3. 实现功能
4. 运行测试
5. 提交代码

# Distill 固化的技能
/new-module <name> - 自动创建模块结构、测试文件、实现骨架
```

### 效果对比

| 场景 | 无 Dream/Distill | 有 Dream/Distill |
|------|-----------------|-----------------|
| 重复工作 | 每次手动执行 | 自动识别并固化 |
| 知识积累 | 会话间丢失 | 跨会话持续积累 |
| 技能复用 | 每次重新编写 | 自动提取可复用技能 |

### Max Mode 配置参考

Max Mode 是 MiMo Code 中用于并行采样和决策优化的高级配置系统。以下是完整的 Max Mode 配置参数参考，包括所有可用参数、默认值和使用说明：

#### 配置参数表

| 参数 | 类型 | 默认值 | 必填 | 说明 |
|------|------|---------|------|------|
| parallelism | number | 5 | 否 | 并行生成的候选方案数量 |
| temperature_range | object | {"min": 0.1, "max": 2.0} | 否 | 候选方案生成的温度范围 |
| judge_model | string | "auto" | 否 | 判断模型名称，"auto" 表示自动选择最佳模型 |
| timeout_per_candidate | number | 30000 | 否 | 每个候选方案的最大执行时间（毫秒） |
| aggregation_strategy | string | "weighted" | 否 | 候选方案的聚合策略，可选值："weighted"、"majority"、"best" |
| enable_cache | boolean | true | 否 | 是否启用候选方案缓存 |
| cache_size | number | 100 | 否 | 候选方案缓存的最大大小 |
| max_tokens_per_candidate | number | 4000 | 否 | 每个候选方案的最大 Token 数 |
| min_quality_score | number | 0.5 | 否 | 候选方案的最低质量分数阈值 |

#### 参数详细说明

##### `parallelism`

**类型**：number

**默认值**：5

**说明**：并行生成的候选方案数量。值越大，生成的候选方案越多，但计算成本也越高。建议根据任务复杂性和计算资源进行调整。

**适用场景**：

- 简单任务：3-5
- 中等复杂度任务：5-8
- 复杂任务：8-12

##### `temperature_range`

**类型**：object

**默认值**：{"min": 0.1, "max": 2.0}

**说明**：候选方案生成的温度范围。温度控制生成的多样性，较低的温度产生更确定的结果，较高的温度产生更多样化的结果。

**参数结构**：

| 子参数 | 类型 | 默认值 | 说明 |
|----------|------|---------|------|
| min | number | 0.1 | 最小温度值 |
| max | number | 2.0 | 最大温度值 |

**使用示例**：

```yaml
maxMode:
  temperature_range:
    min: 0.5
    max: 1.5
```

##### `judge_model`

**类型**：string

**默认值**："auto"

**说明**：判断模型名称，用于比较和选择最佳候选方案。"auto" 表示系统自动选择最佳模型，"custom" 表示使用指定的自定义模型。

**可选值**：

- "auto"：自动选择
- "gpt-4"：使用 GPT-4 模型
- "claude-3"：使用 Claude 3 模型
- "custom"：使用自定义模型

##### `timeout_per_candidate`

**类型**：number

**默认值**：30000

**说明**：每个候选方案的最大执行时间（毫秒）。如果候选方案在指定时间内未完成，将被取消并生成新的候选方案。

**建议值**：

- 简单任务：10000-20000
- 中等复杂度任务：20000-40000
- 复杂任务：40000-60000

##### `aggregation_strategy`

**类型**：string

**默认值**："weighted"

**说明**：候选方案的聚合策略。不同的策略适用于不同的任务类型。

**可选值**：

- "weighted"：加权平均，根据质量分数和性能指标加权
- "majority"：多数投票，根据多个判断指标选择
- "best"：选择最佳方案，选择质量分数最高的方案

##### `enable_cache`

**类型**：boolean

**默认值**：true

**说明**：是否启用候选方案缓存。启用缓存可以减少重复计算，提高效率，但会增加内存占用。

##### `cache_size`

**类型**：number

**默认值**：100

**说明**：候选方案缓存的最大大小。如果缓存大小超过此值，将自动清理最旧的条目。

##### `max_tokens_per_candidate`

**类型**：number

**默认值**：4000

**说明**：每个候选方案的最大 Token 数。限制 Token 数可以控制计算成本，但可能影响任务质量。

##### `min_quality_score`

**类型**：number

**默认值**：0.5

**说明**：候选方案的最低质量分数阈值。质量分数低于此值的候选方案将被过滤掉。

#### 示例配置

##### YAML 配置示例

```yaml
maxMode:
  parallelism: 8
  temperature_range:
    min: 0.5
    max: 1.5
  judge_model: "auto"
  timeout_per_candidate: 45000
  aggregation_strategy: "weighted"
  enable_cache: true
  cache_size: 200
  max_tokens_per_candidate: 6000
  min_quality_score: 0.6
```

##### JSON 配置示例

```json
{
  "maxMode": {
    "parallelism": 8,
    "temperature_range": {
      "min": 0.5,
      "max": 1.5
    },
    "judge_model": "auto",
    "timeout_per_candidate": 45000,
    "aggregation_strategy": "weighted",
    "enable_cache": true,
    "cache_size": 200,
    "max_tokens_per_candidate": 6000,
    "min_quality_score": 0.6
  }
}
```

##### JavaScript 配置示例

```javascript
const maxModeConfig = {
  parallelism: 8,
  temperature_range: {
    min: 0.5,
    max: 1.5
  },
  judge_model: "auto",
  timeout_per_candidate: 45000,
  aggregation_strategy: "weighted",
  enable_cache: true,
  cache_size: 200,
  max_tokens_per_candidate: 6000,
  min_quality_score: 0.6
};
```

#### 性能调优建议

##### 并行度优化

1. **根据任务复杂度调整**：简单任务可以设置较低的并行度，复杂任务可以设置较高的并行度
2. **考虑计算资源**：在计算资源充足的情况下，可以设置较高的并行度
3. **避免过度并行**：并行度过高可能导致资源竞争，影响整体性能

##### 温度范围优化

1. **任务类型匹配**：创造性任务使用较高的温度范围，分析性任务使用较低的温度范围
2. **动态调整**：根据任务反馈动态调整温度范围
3. **避免极端温度**：过低的温度可能导致结果过于确定，过高的温度可能导致结果过于随机

##### 判断模型优化

1. **模型选择**：根据任务需求选择合适的判断模型
2. **模型切换**：根据任务复杂度动态切换判断模型
3. **模型缓存**：缓存判断模型结果，减少重复计算

##### 超时设置优化

1. **任务估计**：根据任务估计设置合理的超时时间
2. **动态调整**：根据任务执行情况动态调整超时时间
3. **优先级处理**：为高优先级任务设置较长的超时时间

##### 聚合策略优化

1. **策略选择**：根据任务类型选择合适的聚合策略
2. **混合策略**：结合多种聚合策略，获得更好的结果
3. **自适应策略**：根据任务反馈自适应聚合策略

#### 高级配置示例

##### 高性能配置

```yaml
maxMode:
  parallelism: 12
  temperature_range:
    min: 0.8
    max: 1.8
  judge_model: "gpt-4"
  timeout_per_candidate: 60000
  aggregation_strategy: "weighted"
  enable_cache: true
  cache_size: 300
  max_tokens_per_candidate: 8000
  min_quality_score: 0.7
```

##### 平衡配置

```yaml
maxMode:
  parallelism: 6
  temperature_range:
    min: 0.5
    max: 1.5
  judge_model: "auto"
  timeout_per_candidate: 30000
  aggregation_strategy: "weighted"
  enable_cache: true
  cache_size: 150
  max_tokens_per_candidate: 5000
  min_quality_score: 0.6
```

##### 低延迟配置

```yaml
maxMode:
  parallelism: 3
  temperature_range:
    min: 0.2
    max: 1.0
  judge_model: "auto"
  timeout_per_candidate: 15000
  aggregation_strategy: "best"
  enable_cache: true
  cache_size: 100
  max_tokens_per_candidate: 3000
  min_quality_score: 0.4
```

#### 配置验证

在应用 Max Mode 配置之前，建议进行配置验证，确保配置参数的有效性和合理性：

```javascript
function validateMaxModeConfig(config) {
  // 验证并行度
  if (config.parallelism < 1 || config.parallelism > 20) {
    throw new Error("并行度必须在 1 到 20 之间");
  }
  
  // 验证温度范围
  if (config.temperature_range.min < 0 || config.temperature_range.max > 3) {
    throw new Error("温度范围必须在 0 到 3 之间");
  }
  
  if (config.temperature_range.min >= config.temperature_range.max) {
    throw new Error("最小温度必须小于最大温度");
  }
  
  // 验证超时时间
  if (config.timeout_per_candidate < 5000 || config.timeout_per_candidate > 300000) {
    throw new Error("超时时间必须在 5000 到 300000 毫秒之间");
  }
  
  // 验证缓存大小
  if (config.cache_size < 10 || config.cache_size > 1000) {
    throw new Error("缓存大小必须在 10 到 1000 之间");
  }
  
  // 验证 Token 限制
  if (config.max_tokens_per_candidate < 1000 || config.max_tokens_per_candidate > 20000) {
    throw new Error("Token 限制必须在 1000 到 20000 之间");
  }
  
  // 验证质量分数
  if (config.min_quality_score < 0 || config.min_quality_score > 1) {
    throw new Error("质量分数必须在 0 到 1 之间");
  }
  
  console.log("Max Mode 配置验证通过");
}
```

## 综合效果

MiMo Code 的四项循环工程优化共同解决了自动化工作流的核心挑战：

| 挑战 | 优化方案 | 效果 |
|------|---------|------|
| **单点瓶颈** | 子智能体系统 | 并行执行，提升效率 |
| **决策质量不稳定** | Max Mode 并行采样 | 选择最佳方案 |
| **编排逻辑脆弱** | 动态工作流 | 代码化，确定性执行 |
| **经验无法积累** | Dream/Distill | 自动化经验积累 |

这些优化使得 MiMo Code 在长周期自动化任务中具有显著优势。

## 与 OpenCode 的对比

| 维度 | OpenCode | MiMo Code |
|------|----------|-----------|
| **子智能体** | 基础支持 | 按需创建、并行执行、生命周期跟踪 |
| **并行采样** | 无内置机制 | Max Mode 并行采样+判断器选择 |
| **工作流编排** | 自然语言（SKILL.md） | 代码化（Dynamic Workflow） |
| **经验积累** | 无内置机制 | Dream/Distill 自动化 |

## 最佳实践

### 何时使用 Max Mode

- **复杂决策**：需要选择最佳方案的场景
- **高风险任务**：错误成本高的场景
- **创意生成**：需要多样性的场景

### 何时使用 Dynamic Workflow

- **确定性流程**：每步必须执行的场景
- **复杂分支**：有条件逻辑的场景
- **可复用流程**：需要多次执行的场景

### 何时使用 Dream/Distill

- **长期项目**：需要跨会话积累的场景
- **重复工作**：有固定模式的场景
- **团队协作**：需要共享知识的场景

## 下一步

- 想了解驾驭工程优化？→ [驾驭工程优化设计](./harness-optimizations.md)
- 想了解架构全景？→ [MiMo Code 架构深度解析](./agent-architecture.md)
- 想对比 OpenCode？→ [MiMo Code vs OpenCode 对比分析](./comparison.md)
