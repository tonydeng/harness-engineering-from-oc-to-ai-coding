# OpenCode SDK 与程序化集成

OpenCode 提供多种程序化集成方式，允许开发者将 Agent 能力嵌入到自己的应用和流水线中。本章涵盖 OpenCode 的 Plugin SDK、npm 包 SDK、以及命令行程序化调用。

---

## SDK 总览

OpenCode 有三层 SDK/API，对应不同的集成深度：

| 层次 | 方式 | 灵活度 | 运行位置 | 适用场景 |
|------|------|--------|----------|---------|
| **Plugin SDK** | `import { definePlugin } from "opencode"` | ⭐⭐⭐⭐⭐ | Agent 进程内 | 自定义工具、Hook 拦截、Agent 行为扩展 |
| **npm SDK** | `@opencode-ai/sdk` / `github.com/sst/opencode-sdk-go` | ⭐⭐⭐⭐ | 独立进程 | 外部应用集成，服务端 Agent 调用 |
| **CLI 程序化** | `opencode --json` / MCP 协议 | ⭐⭐⭐ | Shell/子进程 | CI/CD 流水线，脚本集成 |

---

## 方式一：Plugin SDK（进程内扩展）

Plugin SDK 通过 `definePlugin` API 在 Agent 进程内注册自定义逻辑，是 OpenCode 最强大的扩展方式。

### 安装

```bash
npm install opencode            # TypeScript 类型定义
```

### 核心 API

```typescript
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

```typescript
import { OpenCodeClient } from "@opencode-ai/sdk";

// 创建客户端
const client = new OpenCodeClient({
  apiKey: process.env.OPENCODE_API_KEY,
});

// 创建会话并执行任务
const session = await client.createSession({
  model: "claude-sonnet-4",
  projectDir: "/path/to/project",
});

const result = await session.execute("列出当前目录的文件");
console.log(result.text);
await session.close();
```

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
