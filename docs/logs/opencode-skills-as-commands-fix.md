# PR: opencode-skills-as-commands — Fix missing skill path + export format

> **目标仓库**: `github:cesumilo/opencode-skills-as-commands`
> **基于版本**: v1.0.0
> **提交人建议**: 两个独立 commit，一个修改一个修复

---

## 问题 1: 缺少 OpenCode 主要全局技能路径

### 现状

`src/scanner.ts` 中 `SKILL_PATHS` 数组扫描以下路径：

```typescript
join(worktree, ".opencode/skills")     // 项目级技能
join(home, ".config/opencode/skills")  // 遗留用户配置路径
join(worktree, ".claude/skills")       // Claude 兼容路径
join(home, ".claude/skills")
join(worktree, ".agents/skills")       // Agent 兼容路径
join(home, ".agents/skills")
```

### 问题

OpenCode 的**主要全局技能目录** `~/.opencode/skills/` **缺失**。这是 OpenCode 用户在 `opencode.json` 中配置技能时的默认安装位置，也是绝大多数用户技能实际存放的位置。

结果：用户安装的 76 个技能（位于 `~/.opencode/skills/`）不会被扫描，`/` 命令列表为空。

### 修复

在 `join(worktree, ".opencode/skills")` 之后插入：

```typescript
join(home, ".opencode/skills"),   // 用户级全局技能 — OpenCode 主要位置
```

### 修改文件

**`src/scanner.ts`** — `SKILL_PATHS` 数组增加一行。

完整修改后：

```typescript
export const SKILL_PATHS = (worktree: string) => [
  // Project-level skills (`.opencode/skills` in worktree root)
  join(worktree, ".opencode/skills"),
  // User-level global skills (`~/.opencode/skills`) — the primary location
  join(home, ".opencode/skills"),
  // Legacy OpenCode user config path
  join(home, ".config/opencode/skills"),
  // Claude Code compatibility paths
  join(worktree, ".claude/skills"),
  join(home, ".claude/skills"),
  // Generic agents compatibility paths
  join(worktree, ".agents/skills"),
  join(home, ".agents/skills"),
];
```

---

## 问题 2: 插件导出格式不符合 OpenCode 规范

### 现状

`src/index.ts` 使用**命名导出**：

```typescript
export const SkillsAsCommands = async ({ worktree, fs }) => { ... };
```

### 问题

OpenCode 的插件加载器通过 `import()` 动态加载插件模块，通常期望：

1. **默认导出** — `export default async function(input) { ... }`
2. **或者 `PluginModule` 格式** — `{ server: Plugin }`

当插件通过 `github:cesumilo/opencode-skills-as-commands` 在 `opencode.json` 中注册时：

```json
{ "plugin": ["github:cesumilo/opencode-skills-as-commands"] }
```

OpenCode 会 `import()` 该模块并查找 `default` 导出。命名导出 `export const SkillsAsCommands` **不会被自动发现**，导致插件加载成功但不会调用 `config` 钩子，命令不会注册。

### 修复

将导出改为**同时提供命名导出和默认导出**：

```typescript
const SkillsAsCommands = async ({ worktree, fs }) => { ... };

export { SkillsAsCommands };
export default SkillsAsCommands;
```

这样既保留了命名导出（供其他模块 `import { SkillsAsCommands } from "..."` 使用），又新增了默认导出（供 OpenCode 插件加载器发现）。

### 修改文件

**`src/index.ts`** — 导出方式从一行改为三行。

---

## 附加建议：`package.json` 中 `main` 字段

当前 `"main": "src/index.ts"` 指向 TypeScript 源文件。如果 OpenCode 不支持内置 TypeScript 加载，插件会因语法错误而加载失败。

**建议**：增加 `"exports"` 字段或迁移到编译后的 JS 入口：

```json
{
  "main": "src/index.ts",
  "exports": {
    ".": {
      "import": "./dist/index.js",
      "types": "./src/index.ts"
    }
  }
}
```

或者添加 `tsx` / `ts-node` 作为运行时依赖，指示加载器处理 TypeScript。

---

## 验证方法

```bash
# 1. 确认所有标准技能路径被扫描
grep -n "opencode/skills\|claude/skills\|agents/skills" src/scanner.ts

# 2. 确认默认导出存在
grep "export default" src/index.ts

# 3. 本地安装后测试
# 在 opencode.json 中添加 "plugin": ["github:cesumilo/opencode-skills-as-commands"]
# 启动 opencode，输入 / 查看是否显示技能命令
```
