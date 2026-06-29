"""HEDQ 检查模块注册表。
定义 8 个质量维度（D1-D8）及其自动化检测满分权重。

注意：此处 DIM_MAX 是"自动化检测口径"满分（非标准定义的完整维度满分）。
- 标准定义 D1=15, D2=20, D3=15, D4=15, D5=10, D6=10, D7=10, D8=5 = 100 分
- 自动化检测实际覆盖的子项满分：D1.1+D1.2+D1.4+D1.5=14, D2.2=6, D3.1=6, D4.1=4,
  D5.1+D5.2+D5.3+D5.4=13, D6.3=2, D7.1+D7.2+D7.3=10, D8.1+D8.2=3.5 = 58.5 分
- 未自动化覆盖的子项（D1.3/D2.1/D2.3/D3.2/D3.3/D4.2/D4.3/D4.4/D6.1/D6.2/D6.4/D8.3）
  共 41.5 分需人工审核。

如需扩展自动化覆盖范围，实现对应 check 子项后同步更新此处的 DIM_MAX 值。

v2.0 变更（2026-06-29）：
  - D1 新增 D1.5（链接文字与目标 H1 一致性），D1 max 11→14
  - D5 新增 D5.4（反模式/失败场景/边界条件内容厚度），D5 max 10→13
  - D4.1 重构：三层检查体系（白名单warn + 路径存在性 + 自引用检测）
  总分：52.5 → 58.5
"""
from .base import BaseCheck, CheckResult
from .d1_structural import D1StructuralCheck
from .d2_freshness import D2FreshnessCheck
from .d3_traceability import D3TraceabilityCheck
from .d4_codeblocks import D4CodeblocksCheck
from .d5_antipatterns import D5AntipatternsCheck
from .d6_writing_style import D6WritingStyleCheck
from .d7_terminology import D7TerminologyCheck
from .d8_mermaid import D8MermaidCheck

# 所有检查模块注册表。按维度编号排序，runner 依次执行。
ALL_CHECKS = [
    ("D1", D1StructuralCheck),
    ("D2", D2FreshnessCheck),
    ("D3", D3TraceabilityCheck),
    ("D4", D4CodeblocksCheck),
    ("D5", D5AntipatternsCheck),
    ("D6", D6WritingStyleCheck),
    ("D7", D7TerminologyCheck),
    ("D8", D8MermaidCheck),
]

DIM_NAMES = {
    "D1": "结构与元数据规范性",
    "D2": "内容准确性与时效性",
    "D3": "读者角色覆盖与导航",
    "D4": "代码块格式",
    "D5": "反面案例与边界条件",
    "D6": "文风与可读性",
    "D7": "术语与品牌一致性",
    "D8": "图表与可视化质量",
}

# 各维度自动化检测满分（与 check 模块实际产出的子项满分加总一致）。
# 总分 = 14+6+6+4+13+2+10+3.5 = 58.5
# 注意：此处 max 必须与各 check 模块返回的 CheckResult.max_score 加总一致，
#       否则会导致百分比失真。修改 check 模块时务必同步更新此处。
DIM_MAX = {
    "D1": 14,    # D1.1(3)+D1.2(4)+D1.4(4)+D1.5(3)，D1.3 未自动化
    "D2": 6,     # 仅 D2.2，D2.1/D2.3 未自动化
    "D3": 6,     # 仅 D3.1，D3.2/D3.3 未自动化
    "D4": 4,     # 仅 D4.1（三层检查：缺:path/路径无效/自引用/白名单warn），D4.2/D4.3/D4.4 未自动化
    "D5": 13,    # D5.1(4)+D5.2(3)+D5.3(3)+D5.4(3) 全部自动化
    "D6": 2,     # 仅 D6.3，D6.1/D6.2/D6.4 未自动化
    "D7": 10,    # D7.1+D7.2+D7.3 全部自动化
    "D8": 3.5,   # D8.1(2)+D8.2(1.5)，D8.3 未自动化
}
