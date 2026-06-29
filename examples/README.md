# examples/ — 示例文件导航

本目录存放书籍中所有 `examples/` 路径引用的配置文件和代码示例，按功能类别组织。

## 目录结构

```
examples/
├── opencode-configs/      ← OpenCode 配置（权限、Provider、路由、合规）
├── skills/                ← Skill 示例（SKILL.md + 辅助文件）
├── workflows/             ← 工作流定义
├── quality-gates/         ← 质量门禁规则
├── audit-logs/            ← 审计日志示例
├── validation/            ← 安全/输入验证规则
├── ast-grep-rules/        ← AST 模式匹配规则
├── case-study/            ← 案例研究数据
└── this README
```

## 按章节索引

| 章节 | 关联目录 | 说明 |
|------|---------|------|
| ch01-introduction | `opencode-configs/`, `workflows/`, `quality-gates/`, `audit-logs/`, `validation/` | 初始配置、安全防护、国产模型集成 |
| ch02-core-concepts | `opencode-configs/`, `ast-grep-rules/`, `skills/` | 权限系统、Profile、Skill 结构 |
| ch05-skills | `skills/` | Skill 清单、模板、插件模式 |
| ch07-case-studies | `opencode-configs/`, `skills/`, `case-study/` | 真实案例配置 |

> ch03-setup、ch04-workflows、ch06-advanced 使用 `:terminal` 代码块（无 `examples/` 引用）。

## 使用方式

示例文件被书籍正文的代码块直接引用（格式 `language:examples/.../file`）。所有文件保持**扁平结构**，不按章节嵌套目录，避免跨章节引用时需要更新大量路径。

新增代码块时，若引用 `examples/` 路径，请确保目标文件存在，并在此 README 中更新索引。
