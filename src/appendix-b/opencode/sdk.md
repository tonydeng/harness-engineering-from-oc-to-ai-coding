# OpenCode SDK 与程序化集成

OpenCode 提供多种程序化集成方式，允许开发者将 **Agent（智能体）** 能力嵌入到自己的应用和流水线中。本章涵盖 OpenCode 的 **Plugin（插件）** SDK、npm 包 SDK、以及命令行程序化调用。

> **SDK 深入参考**：如果你只关心 `@opencode-ai/sdk` npm 包的深入使用（生产级配置、上下文管理、错误重试等），见 [OpenCode SDK：编程式 **Agent（智能体）** 开发](./agent-sdk.md)。

---

## SDK 总览

OpenCode 有三层 SDK/API，对应不同的集成深度：

| 层次 | 方式 | 灵活度 | 运行位置 | 适用场景 |
|------|------|--------|----------|---------|
| **Plugin SDK** | `import { definePlugin } from "opencode"` | ⭐⭐⭐⭐⭐ | Agent 进程内 | 自定义工具、Hook 拦截、Agent 行为扩展 |
| **npm SDK** | `@opencode-ai/sdk` / `github.com/sst/opencode-sdk-go` | ⭐⭐⭐⭐ | 独立进程 | 外部应用集成，服务端 Agent 调用 |
| **CLI 程序化** | `opencode --json` / **MCP（模型上下文协议）** 协议 | ⭐⭐⭐ | Shell/子进程 | CI/CD 流水线，脚本集成 |

---

## 方式一：Plugin SDK（进程内扩展）

Plugin SDK 通过 `definePlugin` API 在 Agent 进程内注册自定义逻辑，是 OpenCode 最强大的扩展方式。

### 安装

```bash
npm install opencode            # TypeScript 类型定义
```

### 核心 API

```typescript:src/appendix-b/opencode/sdk.md
import { definePlugin } from "opencode";

export default definePlugin({
  name: "my-plugin",
  description: "插件描述",
  tools: [
    {
      name: "tool_name",
      description: "工具描述",
      parameters: { /* JSON Schema */ },
      handler: async (params) => {
        // 工具逻辑
        return result;
      },
    },
  ],
  hooks: {
    "tool:before": async (event) => {
      // 工具调用前拦截
    },
    "llm:after": async (event) => {
      // LLM 响应后处理
    },
  },
});
```

### API 速查

| API | 用途 |
|-----|------|
| `definePlugin({ name, hooks?, tools? })` | 定义插件，返回 Plugin 对象 |
| `plugin.tools` | 注册自定义 Tool（可覆盖内置工具） |
| `plugin.hooks["hook:name"]` | 注册 Hook 处理器 |

→ 完整 Plugin API 参考见 [Plugin 系统参考](./plugins.md)

---

## 方式二：npm SDK（@opencode-ai/sdk）

`@opencode-ai/sdk` 是 OpenCode 的 JavaScript/TypeScript SDK，用于在外部应用中**调用 OpenCode Agent**。

### 安装

```bash
npm install @opencode-ai/sdk
```

### 核心 API

```typescript:src/appendix-b/opencode/sdk.md
import { createOpencodeClient } from "@opencode-ai/sdk";

// 创建客户端（连接已有 OpenCode Server）
const client = createOpencodeClient({
  baseUrl: "http://localhost:4096",   // Server 地址
  throwOnError: true,                  // 生产环境建议启用
});

// 创建会话并执行任务
const { data: session } = await client.session.create({
  body: { title: "文件列表", model: "claude-sonnet-4" },
});

const { data: result } = await client.session.prompt({
  path: { id: session.id },
  body: { parts: [{ type: "text", text: "列出当前目录的文件" }] },
});

console.log(result.text);
```

> **API 版本提示**：早期版本的 `@opencode-ai/sdk` 使用 `new OpenCodeClient()` 类构造器方式，当前推荐使用 `createOpencodeClient()` 工厂函数。两种方式可共存，建议新项目使用工厂函数。

Go SDK (`github.com/sst/opencode-sdk-go`) 提供类似的 API，适用于 Go 后端服务集成。

---

## 方式三：CLI 程序化调用

适合 CI/CD 流水线或脚本场景：

```bash
# 直接执行（非交互模式）
opencode -p "列出文件" --json

# 指定模型和 Agent
opencode -p "重构此函数" --model claude-sonnet-4 --agent build

# 管道输入
echo "审查当前代码" | opencode --json

# 从文件读取 prompt
opencode -p "$(cat prompt.txt)" --json
```

输出可通过 `--json` 标志获取结构化 JSON，便于后续脚本处理。

---

## 案例：全球天气预报智能体

以下案例演示如何用 OpenCode Plugin SDK 实现一个全球天气预报智能体，包含完整的外部 API 调用、数据规范化和结果验证。

### 案例架构

```
用户输入 "东京今天天气如何？"
       │
       ▼
┌───────────────────┐
│  OpenCode Agent    │
│  (get_weather tool)│
└───────┬───────────┘
        │ 调用 Tool
        ▼
┌───────────────────┐     ┌──────────────────┐
│  get_weather.ts    │────▶│  外部天气 API     │
│  (Plugin SDK)      │◀────│  (OpenWeatherMap) │
└───────┬───────────┘     └──────────────────┘
        │ 原始数据
        ▼
┌───────────────────┐
│  normalize.ts      │  规范化 → 统一格式
└───────┬───────────┘
        │ 规范化数据
        ▼
┌───────────────────┐
│  validate.ts       │  验证 → 结果正确性检查
└───────┬───────────┘
        │ 验证结果
        ▼
┌───────────────────┐
│  返回给用户         │
└───────────────────┘
```

### 1. 数据模型定义

首先定义统一的天气预报数据规范：

```typescript:plugins/weather-agent/weather-schema.ts
// 统一的天气预报数据规范
export interface WeatherData {
  city: string;           // 城市名（中文）
  country: string;        // 国家代码 (ISO 3166-1 alpha-2)
  coordinates: {
    lat: number;
    lon: number;
  };
  temperature: {
    current: number;      // 当前温度 (°C)
    feels_like: number;   // 体感温度 (°C)
    min: number;          // 当日最低温 (°C)
    max: number;          // 当日最高温 (°C)
  };
  humidity: number;       // 湿度 (%)
  pressure: number;       // 气压 (hPa)
  wind: {
    speed: number;        // 风速 (m/s)
    direction: string;    // 风向 (中文)
  };
  conditions: string;     // 天气状况 (晴/多云/雨/雪等)
  description: string;    // 详细描述
  visibility: number;     // 能见度 (km)
  timestamp: string;      // ISO 8601 时间戳
  source: string;         // 数据来源
}

// 查询参数
export interface WeatherQuery {
  city: string;
  country?: string;
  units?: "metric" | "imperial";
}
```

### 2. 外部 API 客户端

```typescript:plugins/weather-agent/api-client.ts
// 外部天气 API 客户端
const WEATHER_API_BASE = "https://api.openweathermap.org/data/2.5";

export interface ApiRawResponse {
  name: string;
  sys: { country: string };
  coord: { lat: number; lon: number };
  main: {
    temp: number;
    feels_like: number;
    temp_min: number;
    temp_max: number;
    humidity: number;
    pressure: number;
  };
  wind: { speed: number; deg: number };
  weather: Array<{ main: string; description: string }>;
  visibility: number;
  dt: number;
}

/**
 * 调用外部天气 API
 * 支持 OpenWeatherMap、WeatherAPI 等标准接口
 */
export async function fetchWeatherFromApi(
  city: string,
  apiKey: string
): Promise<ApiRawResponse> {
  const url = `${WEATHER_API_BASE}/weather?q=${encodeURIComponent(city)}&appid=${apiKey}&units=metric`;

  const response = await fetch(url);
  if (!response.ok) {
    const errorBody = await response.text();
    throw new Error(
      `天气 API 请求失败 [${response.status}]: ${errorBody}`
    );
  }

  return response.json() as Promise<ApiRawResponse>;
}
```

### 3. 数据规范化

```typescript:plugins/weather-agent/normalize.ts
import { WeatherData, WeatherQuery } from "./weather-schema";
import { ApiRawResponse } from "./api-client";

/**
 * 将 API 原始响应规范化为统一格式
 * 支持多种 API 来源，此处以 OpenWeatherMap 为例
 */
export function normalizeWeatherData(
  raw: ApiRawResponse,
  query: WeatherQuery
): WeatherData {
  // 将风向角度转为中文描述
  function windDirection(deg: number): string {
    const directions = ["北", "东北", "东", "东南", "南", "西南", "西", "西北"];
    const index = Math.round(deg / 45) % 8;
    return directions[index];
  }

  return {
    city: raw.name,
    country: raw.sys.country,
    coordinates: {
      lat: raw.coord.lat,
      lon: raw.coord.lon,
    },
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
      direction: windDirection(raw.wind.deg || 0),
    },
    conditions: raw.weather[0]?.main || "未知",
    description: raw.weather[0]?.description || "",
    visibility: Math.round((raw.visibility || 0) / 1000),
    timestamp: new Date(raw.dt * 1000).toISOString(),
    source: "OpenWeatherMap",
  };
}
```

### 4. 结果验证

```typescript:plugins/weather-agent/validate.ts
import { WeatherData } from "./weather-schema";

export interface ValidationResult {
  passed: boolean;
  checks: Array<{
    name: string;
    passed: boolean;
    message: string;
  }>;
}

/**
 * 验证天气预报数据的完整性和合理性
 */
export function validateWeatherData(data: WeatherData): ValidationResult {
  const checks: ValidationResult["checks"] = [];

  // 检查必填字段
  checks.push({
    name: "城市名称",
    passed: data.city.length > 0,
    message: data.city.length > 0 ? `城市: ${data.city}` : "城市名称为空",
  });

  // 检查温度范围（地球极端温度 -89°C ~ 57°C）
  const tempValid = data.temperature.current >= -89 && data.temperature.current <= 57;
  checks.push({
    name: "温度范围",
    passed: tempValid,
    message: tempValid
      ? `当前温度 ${data.temperature.current}°C 在合理范围内`
      : `温度 ${data.temperature.current}°C 超出地球极端范围`,
  });

  // 检查湿度
  const humidityValid = data.humidity >= 0 && data.humidity <= 100;
  checks.push({
    name: "湿度",
    passed: humidityValid,
    message: humidityValid
      ? `湿度 ${data.humidity}% 在合理范围内`
      : `湿度 ${data.humidity}% 超出 0-100% 范围`,
  });

  // 检查气压
  const pressureValid = data.pressure >= 870 && data.pressure <= 1085;
  checks.push({
    name: "气压",
    passed: pressureValid,
    message: pressureValid
      ? `气压 ${data.pressure}hPa 在合理范围内`
      : `气压 ${data.pressure}hPa 超出 870-1085 hPa 范围`,
  });

  // 检查风速
  const windValid = data.wind.speed >= 0 && data.wind.speed <= 120;
  checks.push({
    name: "风速",
    passed: windValid,
    message: windValid
      ? `风速 ${data.wind.speed}m/s 在合理范围内`
      : `风速 ${data.wind.speed}m/s 超出 0-120 m/s 范围`,
  });

  // 检查能见度
  const visValid = data.visibility >= 0 && data.visibility <= 100;
  checks.push({
    name: "能见度",
    passed: visValid,
    message: visValid
      ? `能见度 ${data.visibility}km 在合理范围内`
      : `能见度 ${data.visibility}km 异常`,
  });

  // 检查时间戳
  const tsValid = !isNaN(Date.parse(data.timestamp));
  checks.push({
    name: "时间戳",
    passed: tsValid,
    message: tsValid ? `数据时间: ${data.timestamp}` : "时间戳格式无效",
  });

  const allPassed = checks.every((c) => c.passed);
  return { passed: allPassed, checks };
}

/**
 * 格式化验证结果为可读字符串
 */
export function formatValidationResult(result: ValidationResult): string {
  const lines = result.checks.map(
    (c) => `${c.passed ? "✅" : "❌"} ${c.name}: ${c.message}`
  );
  lines.unshift(`\n## 数据验证 ${result.passed ? "通过" : "失败"}`);
  return lines.join("\n");
}
```

### 5. 集成 Plugin

```typescript:plugins/weather-agent/index.ts
import { definePlugin } from "opencode";
import { fetchWeatherFromApi } from "./api-client";
import { normalizeWeatherData } from "./normalize";
import { validateWeatherData, formatValidationResult } from "./validate";

// 预定义全球主要城市列表
const MAJOR_CITIES = [
  "Tokyo", "Beijing", "Shanghai", "Singapore", "Dubai",
  "London", "Paris", "Berlin", "Moscow", "New York",
  "Los Angeles", "Sydney", "Mumbai", "Seoul", "Bangkok",
  "São Paulo", "Cairo", "Cape Town", "Toronto", "Mexico City",
];

export default definePlugin({
  name: "weather-agent",
  description: "全球天气预报智能体，支持数据规范化和结果验证",
  tools: [
    {
      name: "get_weather",
      description: "查询指定城市的当前天气。支持全球主要城市，返回规范化数据",
      parameters: {
        type: "object",
        properties: {
          city: {
            type: "string",
            description: "城市名称（支持中英文，如 东京/Tokyo）",
          },
          units: {
            type: "string",
            enum: ["metric", "imperial"],
            default: "metric",
          },
        },
        required: ["city"],
      },
      handler: async (params) => {
        const apiKey = process.env.WEATHER_API_KEY;
        if (!apiKey) {
          return "错误: 未设置 WEATHER_API_KEY 环境变量";
        }

        try {
          // 步骤 1: 调用外部 API
          const rawData = await fetchWeatherFromApi(params.city, apiKey);

          // 步骤 2: 规范化数据
          const normalized = normalizeWeatherData(rawData, {
            city: params.city,
            units: params.units || "metric",
          });

          // 步骤 3: 验证数据
          const validation = validateWeatherData(normalized);
          const validationMsg = formatValidationResult(validation);

          // 步骤 4: 格式化输出
          const tempUnit = params.units === "imperial" ? "°F" : "°C";
          const windUnit = params.units === "imperial" ? "mph" : "m/s";

          return [
            `## 🌍 ${normalized.city}, ${normalized.country}\n`,
            `**天气状况**: ${normalized.conditions} - ${normalized.description}`,
            `**温度**: ${normalized.temperature.current}${tempUnit}`,
            `  (体感 ${normalized.temperature.feels_like}${tempUnit}，`,
            `  最低 ${normalized.temperature.min}${tempUnit}，`,
            `  最高 ${normalized.temperature.max}${tempUnit})`,
            `**湿度**: ${normalized.humidity}%`,
            `**气压**: ${normalized.pressure} hPa`,
            `**风速**: ${normalized.wind.speed} ${windUnit} (${normalized.wind.direction}风)`,
            `**能见度**: ${normalized.visibility} km`,
            `**数据来源**: ${normalized.source}`,
            `**数据时间**: ${normalized.timestamp}`,
            validationMsg,
          ].join("\n");
        } catch (error) {
          return `查询失败: ${error instanceof Error ? error.message : String(error)}`;
        }
      },
    },
    {
      name: "list_supported_cities",
      description: "列出天气预报智能体支持查询的全球主要城市",
      parameters: {
        type: "object",
        properties: {},
      },
      handler: async () => {
        const cityList = MAJOR_CITIES.map(
          (city, i) => `${i + 1}. ${city}`
        ).join("\n");
        return `支持查询以下全球主要城市的天气：\n\n${cityList}\n\n共 ${MAJOR_CITIES.length} 个城市。`;
      },
    },
    {
      name: "batch_weather_check",
      description: "批量查询多个城市的天气并验证数据质量",
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
      handler: async (params) => {
        const apiKey = process.env.WEATHER_API_KEY;
        if (!apiKey) return "错误: 未设置 WEATHER_API_KEY";

        const results: string[] = [];
        let passCount = 0;
        let failCount = 0;

        for (const city of params.cities) {
          results.push(`\n--- ${city} ---`);
          try {
            const raw = await fetchWeatherFromApi(city, apiKey);
            const normalized = normalizeWeatherData(raw, { city });
            const validation = validateWeatherData(normalized);

            if (validation.passed) {
              passCount++;
            } else {
              failCount++;
            }

            results.push(
              `天气: ${normalized.conditions}, ${normalized.temperature.current}°C` +
              ` | 验证: ${validation.passed ? "✅" : "❌"}`
            );
          } catch (err) {
            failCount++;
            results.push(`查询失败: ${err instanceof Error ? err.message : String(err)}`);
          }
        }

        results.push(
          `\n## 批量检查完成\n通过: ${passCount}/${params.cities.length}, 失败: ${failCount}/${params.cities.length}`
        );
        return results.join("\n");
      },
    },
  ],
});
```

### 6. 使用方式

**注册 Plugin**：在 `opencode.json` 中启用：

```json:opencode.json
{
  "plugins": [
    {
      "path": "./plugins/weather-agent",
      "enabled": true
    }
  ]
}
```

**设置 API Key**：

```bash
export WEATHER_API_KEY="your_openweathermap_api_key"
```

**在 Agent 中使用**：

```
用户: 东京今天天气怎么样？顺便查一下伦敦和悉尼的天气。

Agent: 正在查询三个城市...

🌍 Tokyo, JP
天气状况: Clear - 晴空万里
温度: 24.5°C (体感 22.8°C, 最低 20.1°C, 最高 27.3°C)
湿度: 65% | 气压: 1013 hPa
风速: 3.1 m/s (南风) | 能见度: 10 km

🌍 London, GB
天气状况: Clouds - 多云
温度: 15.2°C (体感 14.1°C, 最低 12.8°C, 最高 17.6°C)
湿度: 78% | 气压: 1008 hPa
风速: 5.6 m/s (西风) | 能见度: 8 km

🌍 Sydney, AU
天气状况: Rain - 小雨
温度: 18.9°C (体感 17.5°C, 最低 16.2°C, 最高 21.4°C)
湿度: 82% | 气压: 1018 hPa
风速: 4.2 m/s (东南风) | 能见度: 6 km

数据验证全部通过 ✅
```

### 验证流程说明

```
原始 API 响应（JSON）
       │
       ▼
  规范化 (normalize.ts)
  ├── 字段重命名 (main.temp → temperature.current)
  ├── 单位转换 (开尔文 → 摄氏度)
  ├── 角度转换 (风向角度 → 中文方向)
  └── 精度控制 (四舍五入到小数点后一位)
       │
       ▼
  验证 (validate.ts)
  ├── 温度范围检查 (-89°C ~ 57°C)
  ├── 湿度范围检查 (0% ~ 100%)
  ├── 气压范围检查 (870 ~ 1085 hPa)
  ├── 风速范围检查 (0 ~ 120 m/s)
  ├── 能见度范围检查 (0 ~ 100 km)
  └── 时间戳格式检查
       │
       ▼
  格式化输出 + Agent 回复
```

---

## 三种集成方式的对比

| 维度 | Plugin SDK | npm SDK | CLI 程序化 |
|------|-----------|---------|-----------|
| 集成深度 | 进程内（最强） | 进程外 | Shell 级别 |
| 是否可自定义 Tool | ✅ | ❌ | ❌ |
| Hook 拦截 | ✅ | ❌ | ❌ |
| 外部应用嵌入 | ✅（直接 import） | ✅（独立进程） | ✅（子进程） |
| 调试难度 | 中等 | 低 | 低 |
| 典型场景 | Agent 能力扩展 | 后端服务集成 | CI/CD 流水线 |

---

## 相关资源

- [Plugin 系统参考](./plugins.md) — 完整的 Plugin API 和 Hook 点参考
- [OpenCode 生态参考](./ecosystem.md) — @opencode-ai/sdk、github.com/sst/opencode-sdk-go 等社区项目

---

## 读者视角

### 适用读者角色
- 入门开发者 — 适合快速上手 OpenCode 的基础能力，了解核心概念和常用命令
- 智能体开发工程师 — 需要设计、调试、进化 AI 编码智能体，建立系统化的 Agent 工程体系
- 效率开发者 — 已用 AI 工具，想掌握 Agent 编排和工作流模式，提升日常开发效率 2x+
- 技术负责人 — 团队技术决策者，关注标准化，建立团队级 **Harness Engineering（驾驭工程）** 体系
- **Skill（技能）** 作者 — 有 AI 使用经验，想开发高质量、可复用的 Skill
- 工程经理 — 评估团队工具选型，判断 OpenCode 的投资回报率
- 需求分析师/产品经理 — 验证需求覆盖完整性，评估内容价值主张
- 系统架构师/技术顾问 — 评估 OpenCode 的技术可行性、架构集成与安全合规
- 后端开发者/API 工程师 — 将 AI Agent 嵌入后端开发工作流，掌握 MCP 服务端集成
- 前端开发者/UI 工程师 — 将 Agent 编排应用到前端场景，类比理解 Skill 系统
- 文档 UX 专家 — 确保文档可读性、Mermaid 规范、移动端/无障碍体验
- 技术审校/QA 编辑 — 建立质量门禁，验证代码示例可运行性、术语一致性
- 安全工程师/架构师 — 建立 OpenCode 安全基线，评估企业级合规
- 安全研究人员/红队成员 — 评估 AI Agent 攻击面，利用 Agent 自动化安全测试

### 典型使用场景
- 快速上手 OpenCode，完成第一个成功的尝试
- 设计和调试 AI 智能体，建立系统化的 Agent 工程体系
- 掌握 Agent 编排和工作流模式，提升日常开发效率
- 建立团队级 Harness Engineering 体系，进行技术决策
- 开发高质量、可复用的 Skill，封装领域知识
- 评估 OpenCode 的投资回报率，进行工具选型决策
- 验证需求覆盖完整性，评估内容价值主张
- 评估 OpenCode 的技术可行性，进行架构集成与安全合规
- 将 AI Agent 嵌入后端开发工作流，实现 MCP 服务端集成
- 将 Agent 编排应用到前端场景，类比理解 Skill 系统
- 确保文档可读性、Mermaid 规范、移动端/无障碍体验
- 建立质量门禁，验证代码示例可运行性、术语一致性
- 建立 OpenCode 安全基线，评估企业级合规
- 评估 AI Agent 攻击面，利用 Agent 自动化安全测试

### 使用示例
```bash
# 快速上手 OpenCode
opencode serve

# 创建项目知识库
opencode /init

# 使用自定义 Skill
opencode "分析代码质量"

# 执行自动化安全审计
opencode /ralph-loop

# 并行执行多个任务
opencode /hyperplan
```

### 工程化示例

**配置顺序检查表：**

1. **第1步：初始化项目**
   ```bash
   opencode /init
   ```

2. **第2步：配置 Provider**
   ```json
   {
     "providers": {
       "anthropic": {
         "apiKey": "sk-ant-...",
         "defaultModel": "claude-3-5-sonnet-20241022"
       }
     }
   }
   ```

3. **第3步：加载 Skill**
   ```bash
   opencode skills add myorg/my-skill
   ```

### 与前/后文章的衔接
- ← [OpenCode 内置能力](./capabilities.md) — 了解 OpenCode 的核心功能和能力
- → [OpenCode 内置命令参考](./commands.md) — 详细了解每个命令的用法和参数

---

## 常见反模式

### 不区分三层 SDK 的适用场景

OpenCode 有三种集成方式：Plugin SDK（进程内）、npm SDK（进程外 HTTP）、CLI 程序化（Shell 子进程）。最常见的错误是不管场景一律用 CLI 方式（`opencode -p "..." --json`）。CLI 方式每次调用都启动一个新的 OpenCode 进程，冷启动延迟高（2-5 秒），且无法复用会话上下文。如果你的场景需要多轮对话或上下文累积，应该用 npm SDK 创建持久化的 Session；如果需要自定义 Tool 或 Hook 拦截，应该用 Plugin SDK。

### 在 Plugin SDK 中引入外部依赖而不声明

Plugin SDK 运行在 Agent 进程内，可以 import 任何 npm 包。但很多开发者在 Plugin 中使用了 `axios`、`lodash`、`ws` 等外部依赖，却没有在 `package.json` 中声明。在开发环境中，这些依赖可能恰好存在于 `node_modules` 中（被其他包间接安装），但在生产环境或 CI 中可能因为依赖树不同而报 `MODULE_NOT_FOUND` 错误。所有 Plugin 依赖都必须显式声明在 `package.json` 中。

### CLI 调用不处理 `--json` 输出格式

通过 `opencode -p "..." --json` 调用时，输出是 JSON 格式，包含结构化的消息内容、Token 消耗、工具调用记录等。但很多脚本直接把 `--json` 的输出当作纯文本处理（如 `echo $(opencode -p "..." --json)`），当输出包含多行 JSON 时会截断或解析失败。应该用 `jq` 或编程语言的 JSON 解析器处理输出，而不是字符串操作。

### 用 Plugin SDK 实现本该用 npm SDK 解决的问题

Plugin SDK 适合在 Agent 进程内扩展行为（添加 Tool、Hook 拦截），但有些开发者用它来实现"从外部系统获取数据"的需求——在 Plugin 的 Tool Handler 中调用外部 REST API，把结果返回给 Agent。这虽然可行，但 Plugin 运行在 Agent 进程中，外部 API 调用的延迟和失败会影响 Agent 的响应时间。这种场景更适合用 MCP 服务器实现，MCP 运行在独立进程中，Agent 可以异步调用而不会阻塞自身执行。

---

## 适用场景与限制

### Plugin SDK 只能在 Agent 进程内使用

Plugin SDK 通过 `import { definePlugin } from "opencode"` 在 Agent 进程内注册自定义逻辑。它无法在独立的 Node.js 脚本、CI Runner、Web 服务器中使用。如果你的场景是"在 CI 中调用 OpenCode Agent"，应该用 npm SDK（`createOpencodeClient`）或 CLI 程序化方式。Plugin SDK 的运行时环境是 OpenCode 的 Agent 进程，生命周期与 Session 绑定。

### npm SDK 无法定义新 Agent

`@opencode-ai/sdk` 提供的 REST API 可以创建 Session、发送 prompt、管理文件，但无法定义新的 Agent 类型。Agent 的定义（模型选择、温度、工具权限、System Prompt）仍需在 `opencode.json` 或 OMO 的 `oh-my-openagent.jsonc` 中配置。SDK 只能使用已经存在的 Agent，通过 `app.agents()` 查看可用列表。如果你的场景需要动态创建不同行为的 Agent，应在配置层预定义多个 Category，SDK 层按需选择。

### CLI 程序化方式的输出格式不稳定

`opencode -p "..." --json` 的 JSON 输出格式没有严格的 Schema 约束，不同版本的 OpenCode 可能调整输出结构。脚本依赖特定的 JSON 字段（如 `output.text`）时，OpenCode 升级后字段名变更会导致脚本静默失败。建议对 CLI 输出做宽松的字段存在性检查，使用默认值兜底，并在 CI 中用固定版本的 OpenCode。

### 天气 Agent 案例的 API 限速

本章的天气预报智能体案例使用 OpenWeatherMap API，免费版有 60 次/分钟的调用限制。`batch_weather_check` 工具一次性查询多个城市时，如果城市数量超过 60 个，会触发 API 限速返回 429 错误。在生产环境中应实现请求限速（如每秒最多 5 次调用）和重试逻辑，或使用付费版 API 获取更高的配额。

---

## 常见失败与陷阱

### OpenCode Server 未启动导致连接失败

npm SDK（`createOpencodeClient`）和 CLI 方式都依赖 OpenCode Server 正在运行。新手最常见的错误是直接运行 SDK 脚本而忘记先启动 Server，导致 `ECONNREFUSED` 错误。`createOpencodeClient` 默认不抛出 HTTP 错误（`throwOnError: false`），连接失败时返回空响应而不是异常，脚本可能静默跳过错误继续执行。生产环境应设 `throwOnError: true`，并在脚本开头检查 Server 连接状态（`client.global.health()`）。

### `!shell` 模板语法的执行环境差异

自定义命令中的 `!shell` 语法在 OpenCode 的进程环境中执行 Shell 命令。这个环境可能与你的终端环境不同——环境变量、工作目录、PATH 都可能有差异。例如，`!git branch --show-current` 在终端中正常工作，但在 CI Runner 中可能因为 `git` 不在 PATH 中而失败。建议 `!shell` 只用于轻量级的快速命令，并在 AGENTS.md 中说明命令的环境依赖。

### 结构化输出与模型能力不匹配

`format` 参数请求 JSON Schema 格式输出时，并非所有模型都支持。Claude Sonnet 和 GPT-4 系列模型支持良好，但一些小型模型或本地部署的模型可能不支持结构化输出，会忽略 `format` 参数并返回自然语言文本。此时 SDK 的 `structuredOutput` 字段为空，需要从文本内容中回退解析 JSON。在使用结构化输出前，应确认目标模型支持此功能。

### 多实例并行时的端口冲突

在 CI/CD 中并行运行多个 SDK Agent 时，如果都使用默认端口（4096），会发生端口冲突。`createOpencode()` 自动启动 Server 实例时会绑定端口，第二个实例启动失败。解决方案是为每个实例分配不同的端口（从环境变量或随机端口获取），或使用预启动的 Server 池（所有实例连接同一个 Server，用不同 Session 隔离任务）。
