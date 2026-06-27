# Claude Code SDK 与程序化集成

Claude Code 没有传统意义上的"SDK npm 包"，但它提供了多层程序化集成方式：**MCP 服务器**（外部工具）、**Hooks**（生命周期脚本）、**CLI 程序化调用**（子进程集成）。本章介绍这些程序化集成方式，并以天气预报智能体为例展示完整实现。

---

## SDK 总览

Claude Code 的"SDK"由三个层次组成：

| 层次 | 方式 | 灵活度 | 配置方式 | 适用场景 |
|------|------|--------|----------|---------|
| **MCP 服务器** | JSON-RPC 外部进程协议 | ⭐⭐⭐⭐ | `.claude/settings.json` | 外部工具集成、API 调用 |
| **Hooks** | Shell/LLM/Agent 脚本 | ⭐⭐⭐ | `.claude/settings.json` | 事件驱动自动化 |
| **CLI 程序化** | 子进程执行 | ⭐⭐ | Shell 脚本/CI | CI/CD 流水线 |

> **与 OpenCode 的区别**：Claude Code 没有代码级 Plugin API（如 `definePlugin`），所有扩展通过配置文件和外部进程实现。但 MCP 协议是 Anhtropic 主导的开放标准，生态最为成熟。

---

## 方式一：MCP 服务器集成

MCP（Model Context Protocol）是 Claude Code 推荐的程序化扩展方式。通过编写 MCP 服务器，你可以为 Claude Code 添加任意自定义工具。

### MCP 服务器基本结构

```typescript:mcp-weather-server/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server(
  { name: "weather-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// 注册工具
server.setRequestHandler("tools/list", async () => ({
  tools: [
    {
      name: "get_weather",
      description: "查询天气",
      inputSchema: {
        type: "object",
        properties: {
          city: { type: "string" },
        },
      },
    },
  ],
}));

server.setRequestHandler("tools/call", async (request) => {
  // 工具执行逻辑
  return {
    content: [{ type: "text", text: "天气结果" }],
  };
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

### 配置 MCP 服务器

```json:.claude/settings.json
{
  "mcpServers": {
    "weather": {
      "command": "node",
      "args": ["path/to/mcp-weather-server/index.js"],
      "env": {
        "WEATHER_API_KEY": "${WEATHER_API_KEY}"
      }
    }
  }
}
```

---

## 方式二：Hooks 脚本集成

Hooks 允许在 Claude Code 生命周期事件中执行 Shell 脚本：

```json:.claude/settings.json
{
  "hooks": {
    "PostToolUse": {
      "command": "node",
      "args": [".claude/hooks/validate-output.js"],
      "timeout": 10000
    },
    "PreToolUse": {
      "command": "node",
      "args": [".claude/hooks/normalize-input.js"],
      "timeout": 5000
    }
  }
}
```

Hook 脚本通过环境变量 `$TOOL_NAME`、`$TOOL_INPUT`、`$TOOL_OUTPUT` 等获取上下文。

---

## 方式三：CLI 程序化调用

```bash
# 非交互模式
claude -p "东京的天气如何？" --print

# 输出 JSON 格式
claude -p "东京天气" --json

# 管道输入
echo "查询东京、伦敦、纽约的天气" | claude --print

# 指定 CLAUDE.md 配置
claude -p "天气查询" --claude-md ./weather-config.md
```

---

## 案例：全球天气预报智能体

以下案例演示如何用 Claude Code 的 MCP 服务器和 Hooks 系统实现全球天气预报智能体。

### 案例架构

```
用户输入 "东京今天天气如何？"
       │
       ▼
┌───────────────────┐
│  Claude Code Agent  │
│  (MCP weather tool) │
└───────┬───────────┘
        │ MCP 协议调用
        ▼
┌───────────────────────┐
│  MCP Weather Server    │
│  (stdio 传输协议)      │
└───────┬───────────────┘
        │ 调用外部 API
        ▼
┌──────────────────┐
│  外部天气 API     │
│  (OpenWeatherMap)│
└───────┬──────────┘
        │ 原始数据
        ▼
┌──────────────────┐
│  normalize.js     │ 规范化 → 统一格式
└───────┬──────────┘
        │ 规范化数据
        ▼
┌──────────────────┐
│  validate.js      │ 验证 → 结果检查
└───────┬──────────┘
        │ 返回 Claude Code
        ▼
┌──────────────────┐
│  格式化回复给用户  │
└──────────────────┘
```

### 1. 数据模型与规范化

```javascript:weather-agent/weather-schema.js
// 统一的天气预报数据规范
const WEATHER_SCHEMA = {
  city: "",         // 城市名
  country: "",      // 国家代码
  temperature: {
    current: 0,     // 当前温度 (°C)
    feels_like: 0,  // 体感温度
    min: 0,         // 当日最低
    max: 0,         // 当日最高
  },
  humidity: 0,      // 湿度 (%)
  pressure: 0,      // 气压 (hPa)
  wind: {
    speed: 0,       // 风速 (m/s)
    direction: "",  // 风向
  },
  conditions: "",   // 天气状况
  description: "",  // 详细描述
  visibility: 0,    // 能见度 (km)
  timestamp: "",    // ISO 8601
  source: "",       // 数据来源
};
```

### 2. MCP Weather Server（含规范化和验证）

```javascript:weather-agent/mcp-server.js
#!/usr/bin/env node

import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

// ─── 步骤 1: 外部 API 调用 ───
async function fetchWeatherFromApi(city, apiKey) {
  const url = `https://api.openweathermap.org/data/2.5/weather?q=${encodeURIComponent(city)}&appid=${apiKey}&units=metric`;

  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`API 请求失败: ${response.status}`);
  }
  return response.json();
}

// ─── 步骤 2: 数据规范化 ───
function normalizeWeatherData(raw) {
  const directions = ["北", "东北", "东", "东南", "南", "西南", "西", "西北"];
  const windDir = directions[Math.round((raw.wind.deg || 0) / 45) % 8];

  return {
    city: raw.name,
    country: raw.sys.country,
    temperature: {
      current: Math.round(raw.main.temp * 10) / 10,
      feels_like: Math.round(raw.main.feels_like * 10) / 10,
      min: Math.round(raw.main.temp_min * 10) / 10,
      max: Math.round(raw.main.temp_max * 10) / 10,
    },
    humidity: raw.main.humidity,
    pressure: raw.main.pressure,
    wind: { speed: Math.round(raw.wind.speed * 10) / 10, direction: windDir },
    conditions: raw.weather[0]?.main || "未知",
    description: raw.weather[0]?.description || "",
    visibility: Math.round((raw.visibility || 0) / 1000),
    timestamp: new Date(raw.dt * 1000).toISOString(),
    source: "OpenWeatherMap",
  };
}

// ─── 步骤 3: 数据验证 ───
function validateWeatherData(data) {
  const checks = [];

  const addCheck = (name, passed, message) => {
    checks.push({ name, passed, message });
  };

  addCheck("城市名称", data.city.length > 0, `城市: ${data.city}`);

  addCheck("温度范围",
    data.temperature.current >= -89 && data.temperature.current <= 57,
    `温度 ${data.temperature.current}°C ${data.temperature.current >= -89 && data.temperature.current <= 57 ? "合理" : "异常"}`
  );

  addCheck("湿度",
    data.humidity >= 0 && data.humidity <= 100,
    `湿度 ${data.humidity}%`
  );

  addCheck("气压",
    data.pressure >= 870 && data.pressure <= 1085,
    `气压 ${data.pressure}hPa`
  );

  addCheck("风速",
    data.wind.speed >= 0 && data.wind.speed <= 120,
    `风速 ${data.wind.speed}m/s`
  );

  addCheck("能见度",
    data.visibility >= 0 && data.visibility <= 100,
    `能见度 ${data.visibility}km`
  );

  const allPassed = checks.every((c) => c.passed);
  return { passed: allPassed, checks };
}

// ─── 步骤 4: MCP 服务器 ───
const server = new Server(
  { name: "global-weather-agent", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// 支持的全球城市
const MAJOR_CITIES = [
  "Tokyo", "Beijing", "Shanghai", "Singapore", "Dubai",
  "London", "Paris", "Berlin", "Moscow", "New York",
  "Los Angeles", "Sydney", "Mumbai", "Seoul", "Bangkok",
  "São Paulo", "Cairo", "Cape Town", "Toronto", "Mexico City",
];

server.setRequestHandler("tools/list", async () => ({
  tools: [
    {
      name: "get_weather",
      description: "查询指定城市的当前天气，包含数据规范化和验证",
      inputSchema: {
        type: "object",
        properties: {
          city: {
            type: "string",
            description: "城市名称（支持中英文）",
          },
        },
        required: ["city"],
      },
    },
    {
      name: "list_supported_cities",
      description: "列出支持的全球主要城市",
      inputSchema: {
        type: "object",
        properties: {},
      },
    },
    {
      name: "batch_weather",
      description: "批量查询多个城市天气并验证",
      inputSchema: {
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
    },
  ],
}));

server.setRequestHandler("tools/call", async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "list_supported_cities") {
    const list = MAJOR_CITIES.map((c, i) => `${i + 1}. ${c}`).join("\n");
    return {
      content: [{ type: "text", text: `支持以下城市：\n${list}\n共 ${MAJOR_CITIES.length} 个城市。` }],
    };
  }

  if (name === "get_weather" || name === "batch_weather") {
    const apiKey = process.env.WEATHER_API_KEY;
    if (!apiKey) {
      return { content: [{ type: "text", text: "错误: 未设置 WEATHER_API_KEY" }] };
    }

    const citiesToQuery = name === "batch_weather" ? args.cities : [args.city];
    const results = [];

    for (const city of citiesToQuery) {
      try {
        // 调用 API → 规范化 → 验证
        const raw = await fetchWeatherFromApi(city, apiKey);
        const normalized = normalizeWeatherData(raw);
        const validation = validateWeatherData(normalized);

        // 格式化输出
        const lines = [
          `## ${normalized.city}, ${normalized.country}`,
          `**天气**: ${normalized.conditions} - ${normalized.description}`,
          `**温度**: ${normalized.temperature.current}°C (体感 ${normalized.temperature.feels_like}°C)`,
          `  最低 ${normalized.temperature.min}°C / 最高 ${normalized.temperature.max}°C`,
          `**湿度**: ${normalized.humidity}% | **气压**: ${normalized.pressure}hPa`,
          `**风速**: ${normalized.wind.speed}m/s (${normalized.wind.direction}风)`,
          `**能见度**: ${normalized.visibility}km`,
        ];

        // 验证结果
        const failedChecks = validation.checks.filter((c) => !c.passed);
        if (failedChecks.length > 0) {
          lines.push(`**数据验证**: ❌ ${failedChecks.length} 项异常`);
          failedChecks.forEach((c) => lines.push(`  - ${c.name}: ${c.message}`));
        } else {
          lines.push("**数据验证**: ✅ 全部通过");
        }

        results.push(lines.join("\n"));
      } catch (err) {
        results.push(`## ${city}\n**错误**: ${err.message}`);
      }
    }

    return {
      content: [{ type: "text", text: results.join("\n\n---\n\n") }],
    };
  }

  throw new Error(`未知工具: ${name}`);
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

### 3. MCP 服务器 Hook 验证脚本

以下 Hook 脚本可配置为在每次工具调用后运行，验证 MCP 返回的数据质量：

```javascript:.claude/hooks/weather-validator.js
#!/usr/bin/env node

// Claude Code Hook 脚本：验证天气数据
// 在 PostToolUse 事件中触发

const toolName = process.env.TOOL_NAME;
const toolOutput = process.env.TOOL_OUTPUT;

if (toolName === "get_weather" || toolName === "batch_weather") {
  if (toolOutput.includes("错误")) {
    console.error("⚠️ 天气查询返回了错误");
    process.exit(1);
  }

  if (toolOutput.includes("数据验证: ✅")) {
    console.log("✅ 天气数据已验证通过");
  } else if (toolOutput.includes("数据验证: ❌")) {
    console.warn("⚠️ 部分天气数据验证未通过");
  }
}
```

### 4. CLAUDE.md 配置

```markdown:.claude/CLAUDE.md
# 天气智能体项目

## 可用工具
- `get_weather`: 查询城市天气（含数据验证）
- `list_supported_cities`: 列出支持的城市
- `batch_weather`: 批量查询

## 使用示例
- "东京今天天气如何？"
- "对比一下伦敦和纽约的天气"
- "查询东京、新加坡、悉尼三个城市的天气"

## 数据验证说明
每次天气查询会自动执行 6 项验证：
温度(-89~57°C)、湿度(0~100%)、气压(870~1085hPa)、
风速(0~120m/s)、能见度(0~100km)、时间戳格式
```

### 5. 配置与运行

```json:.claude/settings.json
{
  "mcpServers": {
    "global-weather": {
      "command": "node",
      "args": [".claude/mcp/weather-server.mjs"],
      "env": {
        "WEATHER_API_KEY": "${WEATHER_API_KEY}"
      }
    }
  },
  "hooks": {
    "PostToolUse": {
      "command": "node",
      "args": [".claude/hooks/weather-validator.js"],
      "timeout": 5000
    }
  }
}
```

```bash
# 安装依赖
npm install @modelcontextprotocol/sdk

# 设置 API Key
export WEATHER_API_KEY="your_openweathermap_api_key"

# 启动 Claude Code
claude
```

### 6. 使用示例

```
用户: 帮我查一下东京、伦敦和悉尼今天的天气，并验证数据质量。

Claude: 正在通过天气 MCP 服务器查询三个城市...

🌍 Tokyo, JP
天气: Clear - 晴空万里
温度: 24.5°C (体感 22.8°C)  最低 20.1°C / 最高 27.3°C
湿度: 65% | 气压: 1013hPa
风速: 3.1m/s (南风) | 能见度: 10km
数据验证: ✅ 全部通过

🌍 London, GB
天气: Clouds - 多云
温度: 15.2°C (体感 14.1°C)  最低 12.8°C / 最高 17.6°C
湿度: 78% | 气压: 1008hPa
风速: 5.6m/s (西风) | 能见度: 8km
数据验证: ✅ 全部通过

🌍 Sydney, AU
天气: Rain - 小雨
温度: 18.9°C (体感 17.5°C)  最低 16.2°C / 最高 21.4°C
湿度: 82% | 气压: 1018hPa
风速: 4.2m/s (东南风) | 能见度: 6km
数据验证: ✅ 全部通过

三城市数据均通过完整性验证，无异常值。
```

---

## 三种集成方式的对比

| 维度 | MCP 服务器 | Hooks | CLI 程序化 |
|------|-----------|-------|-----------|
| 可添加自定义工具 | ✅ | ❌（仅验证/脚本） | ❌ |
| 支持编程逻辑 | ✅（任意 Node.js） | ✅（Shell/Node） | ❌ |
| 事件驱动 | ❌（按需调用） | ✅（生命周期事件） | ❌ |
| 外部进程隔离 | ✅ | ✅ | ❌（同进程） |
| 调试难度 | 中 | 低 | 低 |
| MCP 生态互通 | ✅（可复用社区 MCP） | ❌ | ❌ |

---

## 相关资源

- [Claude Code Agent SDK 编程](./agent-sdk.md) — `@anthropic-ai/claude-agent-sdk` 深入参考（生产级配置、上下文管理、错误重试）
- [扩展机制参考](./plugins.md) — Claude Code 六层扩展体系详解
- [MCP 服务器](../../06-advanced/mcp-servers.md) — MCP 协议在 OpenCode 中的配置和实践（跨工具参考）
- [Claude Code 生态参考](./ecosystem.md) — 社区扩展和最佳实践

---

## 读者视角

### 适用读者角色
- 入门开发者 — 需要快速上手 Claude Code 的 Agent 体系
- 智能体开发工程师 — 需要设计、调试、进化 Claude Code 中的自定义 Agent 和 Subagent
- 效率开发者 — 已有 AI 工具经验，想通过 Claude Code 提升 2x+ 效率
- 技术负责人 — 需要评估 Claude Code 的技术可行性和团队级 Harness Engineering 体系
- Skill作者 — 需要开发自定义 Skill 和 MCP 桥接，实现团队最佳实践复用

### 典型使用场景
- 需要编程式驱动 Agent 引擎
- 需要嵌入 Claude Code 到自定义应用中
- 需要实现 CI/CD 流水线集成
- 需要开发自定义工具和 MCP 服务器
- 需要实现生产级 Agent 配置和管理

### 使用示例
```bash
# 安装 MCP 服务器
claude mcp add --transport http notion https://mcp.notion.com/mcp

# 配置 Hook
claude /hooks

# 打包插件
claude plugin validate ./my-plugin --strict

# 启动 Claude Code
claude
```

### 工程化示例

**配置顺序检查表：**

1. **第1步：MCP 服务器配置**
   ```json
   // .claude/settings.json
   {
     "mcpServers": {
       "github": {
         "command": "npx",
         "args": ["-y", "@modelcontextprotocol/server-github"],
         "env": {
           "GITHUB_TOKEN": "ghp_..."
         }
       }
     }
   }
   ```

2. **第2步：Hook 配置**
   ```json
   // .claude/settings.json
   {
     "hooks": {
       "PostToolUse": {
         "command": "node",
         "args": [".claude/hooks/validate-output.js"],
         "timeout": 10000
       }
     }
   }
   ```

3. **第3步：插件打包**
   ```bash
   # 验证插件
   claude plugin validate ./my-plugin --strict
   
   # 安装插件
   claude plugin install ./my-plugin
   ```

### 与前/后文章的衔接
- ← [Claude Code Agent SDK 编程](./agent-sdk.md) — `@anthropic-ai/claude-agent-sdk` 深入参考
- → [Claude Code 生态参考](./ecosystem.md) — 社区扩展和最佳实践
