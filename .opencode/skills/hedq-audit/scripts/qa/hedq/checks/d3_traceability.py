"""D3: 读者角色覆盖与导航 — 追溯矩阵覆盖率（Reader role coverage and navigation）
子项：
  D3.1 追溯矩阵覆盖率检查（满分 6 分）
设计意图：确保 13 种读者角色的需求映射到具体章节，没有角色被遗漏。
矩阵文件位于 docs/planning/requirements/traceability-matrix.md，使用中文等级标注。
评分基于加权覆盖率公式，允许部分覆盖。
"""
import re
from pathlib import Path
from typing import List, Optional

from .base import BaseCheck, CheckResult


class D3TraceabilityCheck(BaseCheck):
    """检查 docs/ 中追溯矩阵的覆盖情况。"""

    # 中文覆盖率等级关键词（矩阵文件使用中文标注，非英文）
    # 完整=完全覆盖(5分), 部分=部分覆盖(1分), 缺失/延后=未覆盖(0分)
    COVERAGE_TERMS = r'完整|部分|缺失|延后'
    # 英文兼容（如果矩阵改用英文标注）
    COVERAGE_EN = r'COMPLETE|PARTIAL|MISSING'
    # 用户故事 ID 模式 — 用于排除汇总表行的干扰
    STORY_ID_PATTERN = r'\bUS-[A-Z]+-\d{2}\b'

    def run(self) -> List[CheckResult]:
        matrix = self._find_matrix()
        if matrix is None:
            return [CheckResult("D3", "D3.1", 0, 6, "追溯矩阵文件未找到")]

        complete = 0
        partial = 0
        missing = 0
        total = 0

        with open(matrix, "r", encoding="utf-8") as f:
            for line in f:
                if not line.startswith("|"):
                    continue
                # 只计数包含用户故事 ID 的有效数据行（排除汇总/统计表）
                if not re.search(self.STORY_ID_PATTERN, line):
                    continue
                if re.search(self.COVERAGE_TERMS, line):
                    total += 1
                    if re.search(r'完整', line):
                        complete += 1
                    elif re.search(r'部分', line):
                        partial += 1
                    elif re.search(r'缺失|延后', line):
                        missing += 1
                elif re.search(self.COVERAGE_EN, line):
                    total += 1
                    if re.search(r'COMPLETE', line):
                        complete += 1
                    elif re.search(r'PARTIAL', line):
                        partial += 1
                    elif re.search(r'MISSING', line):
                        missing += 1

        if total == 0:
            return [CheckResult("D3", "D3.1", 0, 6, "追溯矩阵：0 行数据（检查关键词匹配语言）")]

        # 加权覆盖率公式：完整(COMPLETE)=5分，部分(PARTIAL)=1分，缺失(MISSING)=0分
        # 满分为 total * 5（即所有行完整覆盖）
        # 人工调整：如果需要更严格的覆盖率要求，可降低部分权重或提高缺失惩罚
        weighted = (complete * 5) + (partial * 1)
        coverage = weighted / (total * 5) if total > 0 else 0
        score = round(6 * coverage, 1)

        return [CheckResult(
            "D3", "D3.1", score, 6,
            f"追溯矩阵：完整={complete} 部分={partial} 缺失={missing} "
            f"（覆盖率={coverage*100:.0f}%）"
        )]

    def _find_matrix(self) -> Optional[Path]:
        """在 docs/ 下搜索追溯矩阵文件。
        优先搜索 planning/requirements/ 目录，然后是 planning/，最后 rglob 模糊匹配。
        人工调整：如果矩阵文件放在了其他路径，在此添加候选路径即可。
        """
        candidates = [
            self.docs_dir / "planning" / "requirements" / "traceability-matrix.md",
            self.docs_dir / "planning" / "traceability-matrix.md",
        ]
        for c in candidates:
            if c.exists():
                return c
        from pathlib import Path as P
        return next(P(self.docs_dir).rglob("*traceability*"), None)
