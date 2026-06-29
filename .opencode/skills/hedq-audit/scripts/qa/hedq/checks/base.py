"""HEDQ 检查模块基类。
每个 check 模块继承 BaseCheck，实现 run() 方法返回一个或多个 CheckResult。
每个 CheckResult 对应一个子项（如 D1.1 链接检查、D1.2 品牌检查）。
"""
from pathlib import Path
from typing import List, Optional


class CheckResult:
    """单个检查子项的结果。
    属性：
        dim:       维度编号（如 "D1"）
        subitem:   子项编号（如 "D1.1"）
        score:     该子项实得分数
        max_score: 该子项满分（用于计算百分比）
        details:   详细发现文本，包含数量和示例
    """

    def __init__(self, dim: str, subitem: str, score: float, max_score: float, details: str):
        self.dim = dim
        self.subitem = subitem
        self.score = score
        self.max_score = max_score
        self.details = details

    def as_tsv(self) -> str:
        return f"{self.dim}\t{self.subitem}\t{self.score:.1f}\t{int(self.max_score)}\t{self.details}"


class BaseCheck:
    """质量检查基类。
    子类继承后实现 run() 方法，访问 self.src_dir（书籍源目录）和 self.docs_dir（文档目录）。
    """

    def __init__(self, src_dir: Path, docs_dir: Optional[Path] = None):
        self.src_dir = src_dir
        self.docs_dir = docs_dir or src_dir.parent / "docs"

    def run(self) -> List[CheckResult]:
        """执行检查，返回 CheckResult 列表。
        每个 CheckResult 包含一个子项的评分细节。
        """
        raise NotImplementedError
