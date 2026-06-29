---
name: data-pipeline
description: |
  数据处理管道 Skill。
  提供：采集 → 清洗 → 转换 → 验证 → 输出的完整流程。
  适用：ETL 任务、数据迁移、报表生成。
pipeline:
  - stage: collect
    skill: data-collector
    input: source_config
    output: raw_data
  - stage: clean
    skill: data-cleaner
    input: raw_data
    output: cleaned_data
  - stage: transform
    skill: data-transformer
    input: cleaned_data
    output: transformed_data
  - stage: validate
    skill: data-validator
    input: transformed_data
    output: validated_data
  - stage: export
    skill: data-exporter
    input: validated_data
    output: final_result
---

# Data Pipeline Skill

## 管道配置

你是一位数据工程师，负责执行数据处理管道。

### 管道阶段

每个阶段的输入输出格式：

```json:terminal
{
  "stage": "collect",
  "input": {
    "source_type": "database",
    "connection_string": "{env:DB_URL}",
    "query": "SELECT * FROM users"
  },
  "output": {
    "format": "json",
    "records": 1000,
    "schema": ["id", "name", "email", "created_at"]
  }
}
```markdown:terminal

### 数据流转

| 阶段 | 输入格式 | 输出格式 | 处理逻辑 |
|------|----------|----------|----------|
| collect | 数据源配置 | JSON 数组 | 从数据源读取数据 |
| clean | JSON 数组 | JSON 数组 | 去重、填充缺失值 |
| transform | JSON 数组 | JSON 数组 | 字段映射、格式转换 |
| validate | JSON 数组 | JSON 数组 | 数据校验、异常过滤 |
| export | JSON 数组 | 文件/数据库 | 写入目标位置 |

### 错误处理

管道支持两种错误处理策略：

1. **快速失败（Fail Fast）**：任何阶段失败，立即终止管道
2. **容错继续（Continue on Error）**：记录错误，继续执行后续阶段

```yaml:examples/skills/skill-example.yaml
error_handling: fail_fast  # 或 continue_on_error
```markdown:terminal

## 性能优化

- 并行执行无依赖的阶段
- 流式处理大数据集
- 缓存中间结果
