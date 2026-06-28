# Pi **Agent（智能体）** SDK 与程序化集成

Pi 提供最完善的原生 SDK——`@earendil-works/pi-coding-agent` 包不仅是 CLI 工具，也是一个完整的 TypeScript 库。你可以在 Node.js 应用中直接调用 Pi 的 Agent 能力，无需经过 CLI 子进程。

---

## SDK 总览

Pi SDK 包含三层 API：

| 层次 | 接口 | 灵活度 | 适用场景 |
|------|------|--------|---------|
| **Agent Session API** | `createAgentSession()` / `AgentSession` | ⭐⭐⭐⭐⭐ | 嵌入 Agent 能力到应用 |
| **Runtime API** | `createAgentSessionRuntime()` / `AgentSessionRuntime` | ⭐⭐⭐⭐⭐ | 多 Session 动态替换，服务端场景 |
| **RPC / JSON 模式** | `pi --mode rpc` / `pi --mode json` | ⭐⭐⭐ | 非 Node.js 语言集成 |

---

## 方式一：Agent Session API（核心）

### 安装

```bash
npm install @earendil-works/pi-coding-agent
```

### 核心 API 速查

```typescript
import {
  AuthStorage,
  createAgentSession,
  ModelRegistry,
  SessionManager,
} from "@earendil-works/pi-coding-agent";

// 1. 创建认证存储和模型注册表
const authStorage = AuthStorage.create();
const modelRegistry = ModelRegistry.create(authStorage);

// 2. 创建 Agent Session
const { session } = await createAgentSession({
  sessionManager: SessionManager.inMemory(),
  authStorage,
  modelRegistry,
});

// 3. 发送 Prompt
await session.prompt("列出当前目录的文件");

// 4. 关闭 Session
await session.close();
```

### 核心类

| 类 | 用途 |
|-----|-------|
| `AuthStorage` | 管理 API Key 和 OAuth 凭据，支持持久化 |
| `ModelRegistry` | Provider 与模型注册管理，维护工具调用模型列表 |
| `SessionManager` | Session 持久化管理（内存模式 / 文件模式） |
| `AgentSession` | Agent 会话实例，管理消息历史、模型状态、压缩和事件流 |
| `DefaultResourceLoader` | 自动发现 Extensions、Skills、Prompts、Themes |

### AgentSession 选项

```typescript
const { session } = await createAgentSession({
  sessionManager: SessionManager.inMemory(),
  authStorage,
  modelRegistry,
  // 可选：指定模型
  model: "claude-sonnet-4-20250514",
  // 可选：初始系统提示
  systemPrompt: "你是一个天气助手。",
  // 可选：自定义 ResourceLoader
  resourceLoader: customResourceLoader,
});
```

### 事件流

```typescript
// 监听 Agent 事件
session.on("message", (msg) => {
  console.log("新消息:", msg.role, msg.content);
});

session.on("tool_call", (event) => {
  console.log("工具调用:", event.toolName, event.args);
});

session.on("error", (err) => {
  console.error("Agent 错误:", err);
});
```

---

## 方式二：Runtime API（高级）

适用于需要动态替换 Session 的场景（如长时间运行的服务端应用）：

```typescript
import {
  createAgentSessionRuntime,
  AgentSessionRuntime,
} from "@earendil-works/pi-coding-agent";

const runtime = await createAgentSessionRuntime({
  // 运行时工厂函数
  runtimeFactory: async (effectiveCwd) => {
    const authStorage = AuthStorage.create();
    const modelRegistry = ModelRegistry.create(authStorage);
    return {
      sessionManager: SessionManager.fileSystem(effectiveCwd),
      authStorage,
      modelRegistry,
    };
  },
  cwd: process.cwd(),
});

// 替换当前 Session
await runtime.replaceSession();
```

---

## 方式三：RPC / JSON 模式

适用于非 Node.js 环境：

```bash
# RPC 模式 - 严格 JSONL 协议
pi --mode rpc

# JSON 事件流模式
pi --mode json -p "查询东京天气"

# 单次执行
pi -p "查询东京天气"
```

---

## 案例：全球天气预报智能体

以下案例演示如何用 Pi SDK 实现一个可嵌入的全球天气预报智能体。

### 案例架构

```
外部应用 / CI 流水线
       │
       ▼
┌─────────────────────────┐
│  Node.js App (嵌入 SDK)  │
│  createAgentSession()    │
└───────┬─────────────────┘
        │ prompt("东京天气")
        ▼
┌─────────────────────────┐
│  Pi Agent (SDK 模式)     │
│  @earendil-works/pi-     │
│  coding-agent            │
└───────┬─────────────────┘
        │ 调用工具 (Extension)
        ▼
┌──────────────────────┐
│  Weather Extension    │
│  (T具 + 规范化 + 验证)│
└───────┬──────────────┘
        │ fetch → normalize → validate
        ▼
┌──────────────────┐
│  外部天气 API     │
└──────────────────┘
```

### 1. 数据模型

```typescript:weather-agent/weather-schema.ts
// 统一的天气预报数据规范
export interface WeatherData {
  city: string;
  country: string;
  coordinates: { lat: number; lon: number };
  temperature: {
    current: number;
    feels_like: number;
    min: number;
    max: number;
  };
  humidity: number;
  pressure: number;
  wind: { speed: number; direction: string };
  conditions: string;
  description: string;
  visibility: number;
  timestamp: string;
  source: string;
}
```

### 2. External API 客户端 + 规范化 + 验证

```typescript:weather-agent/weather-utils.ts
import { WeatherData } from "./weather-schema";

// ─── 外部 API 调用 ───
export async function fetchWeatherFromApi(
  city: string,
  apiKey: string
): Promise<any> {
  const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&appid=${apiKey}&units=metric`;
  const resp = await fetch(url);
  if (!resp.ok) throw new Error(`API 错误: ${resp.status}`);
  return resp.json();
}

// ─── 规范化 ───
export function normalize(raw: any): WeatherData {
  const dirs = ["北", "东北", "东", "东南", "南", "西南", "西", "西北"];
  return {
    city: raw.name,
    country: raw.sys.country,
    coordinates: raw.coord,
    temperature: {
      current: Math.round(raw.main.temp * 10) / 10,
      feels_like: Math.round(raw.main.feels_like * 10) / 10,
      min: Math.round(raw.main.temp_min * 10) / 10,
      max: Math.round(raw.main.temp_max * 10) / 10,
    },
    humidity: raw.main.humidity,
    pressure: raw.main.pressure,
    wind: {
      speed: Math.round(raw.wind.speed * 10) / 10,
      direction: dirs[Math.round((raw.wind.deg || 0) / 45) % 8],
    },
    conditions: raw.weather[0]?.main || "未知",
    description: raw.weather[0]?.description || "",
    visibility: Math.round((raw.visibility || 0) / 1000),
    timestamp: new Date(raw.dt * 1000).toISOString(),
    source: "OpenWeatherMap",
  };
}

// ─── 验证 ───
export interface ValidationResult {
  passed: boolean;
  checks: Array<{ name: string; passed: boolean; message: string }>;
}

export function validate(data: WeatherData): ValidationResult {
  const checks = [
    { name: "城市名", passed: data.city.length > 0, message: `城市: ${data.city}` },
    { name: "温度范围", passed: data.temperature.current >= -89 && data.temperature.current <= 57,
      message: `温度 ${data.temperature.current}°C` },
    { name: "湿度", passed: data.humidity >= 0 && data.humidity <= 100,
      message: `湿度 ${data.humidity}%` },
    { name: "气压", passed: data.pressure >= 870 && data.pressure <= 1085,
      message: `气压 ${data.pressure}hPa` },
    { name: "风速", passed: data.wind.speed >= 0 && data.wind.speed <= 120,
      message: `风速 ${data.wind.speed}m/s` },
    { name: "能见度", passed: data.visibility >= 0 && data.visibility <= 100,
      message: `能见度 ${data.visibility}km` },
  ];
  return { passed: checks.every((c) => c.passed), checks };
}

// ─── 格式化 ───
export function formatWeather(data: WeatherData, validated: boolean): string {
  return [
    `🌍 ${data.city}, ${data.country}`,
    `**天气**: ${data.conditions} - ${data.description}`,
    `**温度**: ${data.temperature.current}°C (体感 ${data.temperature.feels_like}°C)`,
    `  最低 ${data.temperature.min}°C / 最高 ${data.temperature.max}°C`,
    `**湿度**: ${data.humidity}% | **气压**: ${data.pressure}hPa`,
    `**风速**: ${data.wind.speed}m/s (${data.wind.direction}风)`,
    `**能见度**: ${data.visibility}km`,
    `**数据验证**: ${validated ? "✅ 通过" : "❌ 失败"}`,
  ].join("\n");
}
```

### 3. Pi Extension（自定义工具）

```typescript:weather-agent/pi-extension.ts
import { fetchWeatherFromApi, normalize, validate, formatWeather } from "./weather-utils";

// Pi Extension - 注册为自定义工具
export default function (pi: ExtensionAPI) {
  const MAJOR_CITIES = [
    "Tokyo", "Beijing", "Shanghai", "Singapore", "Dubai",
    "London", "Paris", "Berlin", "Moscow", "New York",
    "Los Angeles", "Sydney", "Mumbai", "Seoul", "Bangkok",
    "São Paulo", "Cairo", "Cape Town", "Toronto", "Mexico City",
  ];

  // 工具 1: 单城市查询
  pi.registerTool({
    name: "get_weather",
    description: "查询指定城市的当前天气，自动规范化和验证数据",
    parameters: {
      type: "object",
      properties: {
        city: { type: "string", description: "城市名称" },
      },
      required: ["city"],
    },
    execute: async ({ city }) => {
      const apiKey = process.env.WEATHER_API_KEY;
      if (!apiKey) return "错误: 未设置 WEATHER_API_KEY";

      try {
        const raw = await fetchWeatherFromApi(city, apiKey);
        const normalized = normalize(raw);
        const validation = validate(normalized);
        return formatWeather(normalized, validation.passed);
      } catch (err) {
        return `查询失败: ${err instanceof Error ? err.message : String(err)}`;
      }
    },
  });

  // 工具 2: 批量查询
  pi.registerTool({
    name: "batch_weather",
    description: "批量查询多个城市的天气",
    parameters: {
      type: "object",
      properties: {
        cities: {
          type: "array",
          items: { type: "string" },
          description: "城市名称数组",
        },
      },
      required: ["cities"],
    },
    execute: async ({ cities }) => {
      const apiKey = process.env.WEATHER_API_KEY;
      if (!apiKey) return "错误: 未设置 WEATHER_API_KEY";

      const results: string[] = [];
      let pass = 0, fail = 0;

      for (const city of cities) {
        try {
          const raw = await fetchWeatherFromApi(city, apiKey);
          const normalized = normalize(raw);
          const validation = validate(normalized);
          if (validation.passed) pass++; else fail++;
          results.push(formatWeather(normalized, validation.passed));
        } catch (err) {
          fail++;
          results.push(`## ${city}\n❌ 查询失败: ${err instanceof Error ? err.message : String(err)}`);
        }
      }

      results.push(`\n---\n✅ 通过: ${pass} | ❌ 失败: ${fail} | 总计: ${cities.length}`);
      return results.join("\n\n");
    },
  });

  // 工具 3: 列出支持的城市
  pi.registerTool({
    name: "list_cities",
    description: "列出支持的全球主要城市",
    parameters: { type: "object", properties: {} },
    execute: async () => {
      const list = MAJOR_CITIES.map((c, i) => `${i + 1}. ${c}`).join("\n");
      return `支持以下 ${MAJOR_CITIES.length} 个全球主要城市：\n\n${list}`;
    },
  });
}
```

### 4. SDK 嵌入示例（可运行）

以下代码演示如何在任意 Node.js 应用中使用 Pi SDK 查询天气：

```typescript:weather-agent/embed-example.ts
import {
  AuthStorage,
  createAgentSession,
  ModelRegistry,
  SessionManager,
} from "@earendil-works/pi-coding-agent";
import { fetchWeatherFromApi, normalize, validate, formatWeather } from "./weather-utils";

/**
 * 方式 A: 使用 Pi Agent SDK 嵌入（Agent 自动选择工具）
 */
async function weatherAgentExample() {
  const authStorage = AuthStorage.create();
  const modelRegistry = ModelRegistry.create(authStorage);

  const { session } = await createAgentSession({
    sessionManager: SessionManager.inMemory(),
    authStorage,
    modelRegistry,
    systemPrompt: `你是一个全球天气预报助手。
当你需要查询天气时，使用 get_weather 工具。
查询完成后，对数据进行验证并展示结果。`,
  });

  // 查询天气 - Agent 自动调用工具
  const result = await session.prompt("东京今天的天气如何？");
  console.log(result.content);
}

/**
 * 方式 B: 直接调用天气工具（无 Agent，纯函数式）
 */
async function directWeatherCall() {
  const apiKey = process.env.WEATHER_API_KEY;
  if (!apiKey) throw new Error("请设置 WEATHER_API_KEY");

  const cities = ["Tokyo", "London", "New York", "Sydney", "Beijing"];

  for (const city of cities) {
    try {
      // 步骤 1: 调用外-API
      const raw = await fetchWeatherFromApi(city, apiKey);

      // 步骤 2: 规范化
      const normalized = normalize(raw);

      // 步骤 3: 验证
      const result = validate(normalized);

      // 输出
      console.log(formatWeather(normalized, result.passed));

      // 如果验证失败，输出详细信息
      if (!result.passed) {
        console.log("验证失败详情:");
        result.checks
          .filter((c) => !c.passed)
          .forEach((c) => console.log(`  ❌ ${c.name}: ${c.message}`));
      }
    } catch (err) {
      console.error(`${city} 查询失败:`, err);
    }
  }
}

// 运行
// weatherAgentExample();
directWeatherCall();
```

### 5. RPC 模式示例

通过 RPC 模式从非 Node.js 应用调用：

```python
# weather_client.py
import subprocess
import json

proc = subprocess.Popen(
    ["pi", "--mode", "rpc"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True,
)

def query_weather(city):
    request = {
        "type": "prompt",
        "prompt": f"查询{city}的天气，使用 get_weather 工具并验证结果"
    }
    proc.stdin.write(json.dumps(request) + "\n")
    proc.stdin.flush()

    # 读取响应
    response = proc.stdout.readline()
    return json.loads(response)

# 使用示例
result = query_weather("Tokyo")
print(result)
```

### 6. 配置与运行

```bash
# 安装 Pi
npm install -g --ignore-scripts @earendil-works/pi-coding-agent

# 安装天气工具依赖
npm install @earendil-works/pi-coding-agent

# 设置 API Key
export WEATHER_API_KEY="your_openweathermap_api_key"

# 注册 Extension
cp -r weather-agent ~/.pi/agent/extensions/

# 运行 SDK 嵌入示例
npx ts-node weather-agent/embed-example.ts

# 或通过 Pi CLI
pi
> /reload  # 重载扩展
> 东京天气如何？
```

---

## 使用示例

### 通过 Pi CLI

```
用户: 东京今天天气如何？顺便查一下伦敦和悉尼的天气。

Agent: 正在使用 get_weather 和 batch_weather 工具查询...

🌍 Tokyo, JP
天气: Clear - 晴空万里
温度: 24.5°C (体感 22.8°C)  最低 20.1°C / 最高 27.3°C
湿度: 65% | 气压: 1013hPa
风速: 3.1m/s (南风) | 能见度: 10km
数据验证: ✅ 通过

🌍 London, GB
天气: Clouds - 多云
温度: 15.2°C (体感 14.1°C)  最低 12.8°C / 最高 17.6°C
湿度: 78% | 气压: 1008hPa
风速: 5.6m/s (西风) | 能见度: 8km
数据验证: ✅ 通过

🌍 Sydney, AU
天气: Rain - 小雨
温度: 18.9°C (体感 17.5°C)  最低 16.2°C / 最高 21.4°C
湿度: 82% | 气压: 1018hPa
风速: 4.2m/s (东南风) | 能见度: 6km
数据验证: ✅ 通过
```

### 通过 SDK 嵌入（Node.js 应用）

```typescript
import { weatherAgent } from "./weather-agent/embed-example";

// 在 Express 路由中使用
app.get("/api/weather/:city", async (req, res) => {
  const result = await directWeatherCall(req.params.city);
  res.json(result);
});
```

---

## 验证流程

所有三种集成方式共享相同的验证逻辑：

```
原始 API 响应
    │
    ▼
规范化 (normalize.ts)
├── 温度: 开尔文 → 摄氏度
├── 风向: 角度 → 中文方向
├── 精度: 保留一位小数
└── 字段: 重映射为统一名称
    │
    ▼
验证 (validate.ts)
├── 温度: [-89, 57]°C
├── 湿度: [0, 100]%
├── 气压: [870, 1085]hPa
├── 风速: [0, 120]m/s
├── 能见度: [0, 100]km
└── 时间戳: ISO 8601 格式
    │
    ▼
格式化 → 输出
```

---

## 三种集成方式的对比

| 维度 | Agent Session API | Runtime API | RPC / JSON 模式 |
|------|------------------|-------------|----------------|
| 类型安全 | ✅ TypeScript | ✅ TypeScript | ❌ JSON 协议 |
| 事件/流支持 | ✅ | ✅ | ❌ |
| 多 Session 管理 | ⚠️ 手动 | ✅ 自动 | ❌ |
| 非 Node.js 集成 | ❌ | ❌ | ✅ Python/Go/Rust |
| 调试体验 | 最好 | 好 | 一般 |
| 性能 | 最佳（同进程） | 最佳 | 中等（进程间） |

---

## 相关资源

- [扩展体系详解](./customization.md) — Pi Extensions 的完整开发指南
- [生态与集成场景](./ecosystem.md) — Provider、容器化、社区生态
- Pi SDK 官方文档：[pi.dev/docs/latest/sdk](https://pi.dev/docs/latest/sdk)

---

## 读者视角

### 适用读者角色
- 入门开发者 — Pi 的 SDK 提供简单的 API，让新手无需面对复杂配置即可上手
- 智能体开发工程师 — SDK 为深度定制提供 TypeScript 支持，实现高级 Agent 编排
- 效率开发者 — SDK 嵌入支持，实现自动化工作流，提升 2x+ 效率
- 技术负责人 — SDK 集成支持，实现团队级 **Harness Engineering（驾驭工程）** 体系
- **Skill（技能）** 作者 — SDK 支持 Skill 开发，实现高质量 Skill 的创建
- 系统架构师 — SDK 集成支持，实现架构评估和安全合规
- 安全工程师 — SDK 集成支持，实现安全基线建立和威胁建模

### 典型使用场景
- 通过 SDK 嵌入 Pi Agent 到 Node.js 应用中，实现自动化工作流
- 通过 SDK 实现自定义工具和命令，满足特定领域需求
- 通过 SDK 实现多 Session 管理和动态替换，支持长时间运行的服务端应用
- 通过 SDK 实现事件流处理，实现可观测性和监控
- 通过 SDK 实现上下文管理和压缩，支持长时间运行的应用
- 通过 SDK 实现安全认证和权限控制，实现企业级安全合规
- 通过 SDK 实现模型管理和路由，实现不同复杂度任务的模型自动选择

### 使用示例
```typescript
// 安装 Pi SDK
npm install @earendil-works/pi-coding-agent

// 创建 Agent Session
import { createAgentSession, AuthStorage, ModelRegistry, SessionManager } from "@earendil-works/pi-coding-agent";

const { session } = await createAgentSession({
  sessionManager: SessionManager.inMemory(),
  authStorage: AuthStorage.create(),
  modelRegistry: ModelRegistry.create(AuthStorage.create()),
});

// 发送提示词
await session.prompt("列出当前目录的文件");

// 关闭 Session
await session.close();
```

### 工程化示例

**配置顺序检查表：**

1. **安装 Pi SDK**
   ```bash
   npm install @earendil-works/pi-coding-agent
   ```

2. **创建项目目录**
   ```bash
   mkdir -p my-project
   cd my-project
   ```

3. **创建 SDK 嵌入文件**
   ```typescript
   // embed-example.ts
   import { createAgentSession, AuthStorage, ModelRegistry, SessionManager } from "@earendil-works/pi-coding-agent";
   
   async function weatherAgentExample() {
     const { session } = await createAgentSession({
       sessionManager: SessionManager.inMemory(),
       authStorage: AuthStorage.create(),
       modelRegistry: ModelRegistry.create(AuthStorage.create()),
       systemPrompt: "你是一个全球天气预报助手。",
     });
     
     const result = await session.prompt("东京今天的天气如何？");
     console.log(result.content);
   }
   ```

4. **运行 SDK 嵌入示例**
   ```bash
   npx ts-node embed-example.ts
   ```

### 与前/后文章的衔接
- ← [Pi Agent 概述与核心概念](../overview.md) — 提供 Pi 的设计哲学和核心架构
- → [生态与集成场景](./ecosystem.md) — 学习 Pi 的生态和集成场景
