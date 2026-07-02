"""HEDQ runner — orchestrates all checks and produces reports.
包含 run-hedq.py 的调度逻辑、评分汇总、报告生成（Markdown/JSON）、
审计历史记录（results.tsv + JSON 快照）。
"""
import json
import logging
import sys
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional

from .checks import ALL_CHECKS, DIM_NAMES, DIM_MAX, BaseCheck, CheckResult

logger = logging.getLogger(__name__)

# 快速模式只跑 D1（结构）+ D6（文风）+ D7（术语），耗时 ~10s
QUICK_CHECKS = {"D1", "D6", "D7"}

# 百分制缩放：所有总分统一为 /100 输出
# raw ΣDIM_MAX = 14+6+6+4+13+2+10+3.5 = 58.5（full）/ 14+2+10 = 26（quick）
_FULL_RAW_MAX = sum(DIM_MAX[d] for d in DIM_MAX)  # 58.5
_QUICK_RAW_MAX = sum(DIM_MAX[d] for d in QUICK_CHECKS)  # 26

def _scale_factor(quick: bool) -> float:
    """返回将 raw 总分缩放到 100 的系数。"""
    return 100.0 / (_QUICK_RAW_MAX if quick else _FULL_RAW_MAX)

# 审计报告默认输出目录
DEFAULT_REPORT_DIR = Path(__file__).resolve().parent.parent / "reports"


class HEDQRunner:
    """HEDQ 审计调度器。
    按维度依次执行 8 个 check 模块，汇总得分，生成并保存报告。
    """

    def __init__(
        self,
        src_dir: Path,
        docs_dir: Path,
        quick: bool = False,
        json_mode: bool = False,
        report_dir: Path = DEFAULT_REPORT_DIR,
    ):
        self.src_dir = src_dir
        self.docs_dir = docs_dir
        self.quick = quick
        self.json_mode = json_mode
        self.report_dir = report_dir

    @staticmethod
    def _get_git_commit() -> str:
        """获取当前 git HEAD 的短 hash，用于 results.tsv 记录。
        如果不在 git 仓库中，返回 'unknown'。
        """
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True, text=True, timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
            logger.warning("git rev-parse failed: %s", result.stderr)
            return "unknown"
        except (subprocess.SubprocessError, OSError) as e:
            logger.warning("git command error: %s", e)
            return "unknown"

    def _scale(self, raw: float) -> float:
        """将 raw 分数缩放到百分制（/100）。"""
        return raw * _scale_factor(self.quick)

    def _scale_dim(self, raw_score: float, raw_max: float) -> tuple:
        """将维度原始得分/满分缩放到百分制贡献值。"""
        return (round(self._scale(raw_score), 1), round(self._scale(raw_max), 1))

    def _calc_dim_scores(self, results: List[CheckResult]) -> Dict[str, float]:
        """将各维度子项得分合并为该维度总分。
        例如 D1 的 D1.1(链接)+D1.2(路径)+D1.4(品牌) 加总为 D1 总分。
        """
        dim_scores: Dict[str, float] = {}
        for r in results:
            dim_scores.setdefault(r.dim, 0.0)
            dim_scores[r.dim] += r.score
        return dim_scores

    def run(self) -> Tuple[List[CheckResult], float, float]:
        """Run checks, return (results, total_score, total_max).

        异常隔离：单个 check 抛异常时记录 0 分并继续，不影响其他 check。
        total_max 仅统计实际运行的维度（quick 模式下不包含未跑的维度）。
        """
        results: List[CheckResult] = []
        ran_dims: set = set()

        for dim_id, check_cls in ALL_CHECKS:
            if self.quick and dim_id not in QUICK_CHECKS:
                continue
            ran_dims.add(dim_id)
            try:
                check: BaseCheck = check_cls(self.src_dir, self.docs_dir)
                results.extend(check.run())
            except Exception as e:
                logger.error("Check %s 失败: %s", dim_id, e)
                results.append(CheckResult(
                    dim_id, f"{dim_id}.ERROR", 0, 0, f"check 异常: {e}"
                ))

        dim_scores = self._calc_dim_scores(results)

        # total_max 仅统计实际运行的维度，避免 quick 模式下百分比失真
        total_score = sum(min(dim_scores.get(d, 0), DIM_MAX[d]) for d in DIM_MAX if d in ran_dims)
        total_max = sum(DIM_MAX[d] for d in DIM_MAX if d in ran_dims)

        return (results, total_score, total_max)

    def generate_report(self, results: List[CheckResult], total_score: float, total_max: float) -> str:
        """Generate Markdown or JSON report."""
        if self.json_mode:
            return self._generate_json(results, total_score, total_max)
        return self._generate_markdown(results, total_score, total_max)

    def _generate_markdown(self, results: List[CheckResult], total_score: float, total_max: float) -> str:
        lines = []
        lines.append("# HEDQ 质量审计报告\n")
        lines.append(f"| 元数据 | 值 |")
        lines.append(f"|--------|-----|")
        lines.append(f"| 审计时间 | {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} |")
        lines.append(f"| 审计模式 | {'快速' if self.quick else '完整'} |")
        lines.append(f"| 检查维度数 | {len(set(r.dim for r in results))} |\n")

        # Dimension scores
        lines.append("## 维度评分\n")
        lines.append("| 维度 | 名称 | 得分 | 关键发现 |")
        lines.append("|------|------|:----:|----------|")

        dim_scores: Dict[str, float] = {}
        dim_details: Dict[str, str] = {}
        for r in results:
            dim_scores[r.dim] = dim_scores.get(r.dim, 0.0) + r.score
            if r.dim not in dim_details:
                dim_details[r.dim] = r.details
            else:
                sep = "; " if dim_details[r.dim] and r.details else ""
                dim_details[r.dim] += sep + r.details

        for dim in sorted(DIM_MAX.keys()):
            raw_score = dim_scores.get(dim, 0.0)
            max_s = DIM_MAX[dim]
            score = min(raw_score, max_s)
            name = DIM_NAMES.get(dim, dim)
            details = dim_details.get(dim, "-")
            pct = (score / max_s * 100) if max_s > 0 else 0

            if pct >= 90:
                icon = "🟢"
            elif pct >= 70:
                icon = "🟡"
            elif pct >= 50:
                icon = "🟠"
            else:
                icon = "🔴"

            # 百分制：显示缩放后的 /100 贡献值
            score_100, max_100 = self._scale_dim(score, max_s)
            lines.append(f"| {dim} | {name} | {icon} {score_100:.1f}/{max_100:.1f} | {details} |")

        lines.append("")
        total_100 = round(self._scale(total_score), 1)
        grade, grade_emoji = self._get_grade(total_100)

        lines.append("## 总分\n")
        lines.append(f"| 指标 | 值 |")
        lines.append(f"|------|-----|")
        lines.append(f"| 总分 | {total_100:.1f} / 100 |")
        lines.append(f"| 评级 | {grade_emoji} **{grade}** |\n")

        lines.append("## 详细检查结果\n")
        lines.append("| 维度 | 子项 | 得分 | 满分 | 详情 |")
        lines.append("|------|------|:----:|:----:|------|")

        for r in results:
            # 保留 float 精度，避免 1.5 被截断为 1
            max_display = r.max_score if isinstance(r.max_score, float) and r.max_score != int(r.max_score) else int(r.max_score)
            lines.append(f"| {r.dim} | {r.subitem} | {r.score:.1f} | {max_display} | {r.details} |")

        lines.append("")
        lines.append("---")
        lines.append("*报告由 HEDQ 质量审计框架自动生成 | 入口: scripts/qa/run-hedq.py*\n")
        return "\n".join(lines)

    def _generate_json(self, results: List[CheckResult], total_score: float, total_max: float) -> str:
        dim_scores: Dict[str, float] = {}
        for r in results:
            dim_scores[r.dim] = dim_scores.get(r.dim, 0.0) + r.score

        dims = []
        for dim in sorted(DIM_MAX.keys()):
            raw_score = dim_scores.get(dim, 0.0)
            max_s = DIM_MAX[dim]
            score = min(raw_score, max_s)
            score_100, max_100 = self._scale_dim(score, max_s)
            dims.append({
                "dimension": dim,
                "name": DIM_NAMES.get(dim, dim),
                "score": score_100,
                "max": max_100,
            })

        total_100 = round(self._scale(total_score), 1)
        grade, grade_emoji = self._get_grade(total_100)

        report = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mode": "quick" if self.quick else "full",
            "dimensions": dims,
            "total_score": total_100,
            "total_max": 100.0,
            "percentage": total_100,
            "grade": grade,
            "grade_emoji": grade_emoji,
        }
        return json.dumps(report, ensure_ascii=False, indent=2)

    def _get_grade(self, pct: float) -> Tuple[str, str]:
        """根据总分百分比判定质量等级。
        规则：
          >= 90% → READY（可发布）
          >= 75% → CONDITIONAL（有条件发布）
          >= 60% → NEEDS WORK（需修改）
          < 60%  → DRAFT（草稿，不可发布）
        """
        if pct >= 90:
            return ("READY", "🟢")
        elif pct >= 75:
            return ("CONDITIONAL", "🟡")
        elif pct >= 60:
            return ("NEEDS WORK", "🟠")
        else:
            return ("DRAFT", "🔴")

    def save_report(self, results: List[CheckResult], total_score: float, total_max: float):
        """保存运行报告到磁盘。
        1. 保存完整 JSON 快照（含子项详情、每条发现）
        2. 追加一条记录到 results.tsv（紧凑趋势行）
        3. 打印本次得分变化（与上一次 full 模式对比）
        """
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M%S")
        ts_human = now.strftime("%Y-%m-%d %H:%M:%S")

        self.report_dir.mkdir(parents=True, exist_ok=True)

        # --- 收集各维度得分 ---
        dim_scores: Dict[str, float] = {}
        for r in results:
            dim_scores[r.dim] = dim_scores.get(r.dim, 0.0) + r.score

        mode = "quick" if self.quick else "full"
        total_100 = round(self._scale(total_score), 1)
        grade, grade_emoji = self._get_grade(total_100)
        commit = self._get_git_commit()

        # --- 构建维度得分表（百分制）---
        dimensions = []
        dim_values: Dict[str, float] = {}
        for dim in sorted(DIM_MAX.keys()):
            raw = dim_scores.get(dim, 0.0)
            max_s = DIM_MAX[dim]
            capped = min(raw, max_s)
            score_100, max_100 = self._scale_dim(capped, max_s)
            dimensions.append({
                "dimension": dim,
                "name": DIM_NAMES.get(dim, dim),
                "score": score_100,
                "max": max_100,
            })
            dim_values[dim] = score_100

        # --- 1) 保存 JSON 快照（完整详情）---
        snapshot = {
            "timestamp": ts_human,
            "commit": commit,
            "mode": mode,
            "total_score": total_100,
            "total_max": 100.0,
            "grade": grade,
            "grade_emoji": grade_emoji,
            "dimensions": dimensions,
            # 子项级别详情，每条 CheckResult 一条
            "details": [
                {"dim": r.dim, "subitem": r.subitem,
                 "score": round(self._scale(r.score), 1),
                 "max": round(self._scale(
                     r.max_score if isinstance(r.max_score, float) and r.max_score != int(r.max_score) else int(r.max_score)
                 ), 1),
                 "details": r.details}
                for r in results
            ],
        }
        snapshot_file = self.report_dir / f"{timestamp}_{mode}.json"
        with open(snapshot_file, "w", encoding="utf-8") as f:
            json.dump(snapshot, f, ensure_ascii=False, indent=2)

        # --- 2) 追加 results.tsv（百分制趋势）---
        # v3.0 变更：2026-06-30 起所有值为百分制（/100）
        tsv_file = self.report_dir / "results.tsv"
        is_new = not tsv_file.exists()

        with open(tsv_file, "a", encoding="utf-8") as f:
            if is_new:
                f.write("# HEDQ Quality Audit — Trend History (百分制 v3.0)\n")
                f.write("# Each row = one audit run, all scores scaled to /100\n")
                f.write("# columns: timestamp\tcommit\tmode\t"
                        "d1\td2\td3\td4\td5\td6\td7\td8\t"
                        "total\tmax\tgrade\n")
            row = (
                f"{ts_human}\t{commit}\t{mode}\t"
                f"{dim_values.get('D1', 0):.1f}\t{dim_values.get('D2', 0):.1f}\t"
                f"{dim_values.get('D3', 0):.1f}\t{dim_values.get('D4', 0):.1f}\t"
                f"{dim_values.get('D5', 0):.1f}\t{dim_values.get('D6', 0):.1f}\t"
                f"{dim_values.get('D7', 0):.1f}\t{dim_values.get('D8', 0):.1f}\t"
                f"{total_100}\t100.0\t{grade}\n"
            )
            f.write(row)

        # --- 3) 打印摘要到 stderr ---
        print(f"\n  Report saved: {snapshot_file}", file=sys.stderr)
        print(f"  Results TSV:  {tsv_file}", file=sys.stderr)
        prev = self._get_previous_score(tsv_file)
        if prev is not None:
            # 如果上一条是旧版（58.5 制），缩放到百分制再对比
            delta = round(total_100 - prev, 1)
            sign = "+" if delta >= 0 else ""
            print(f"  Score change: {sign}{delta} pts from previous full run", file=sys.stderr)

    @staticmethod
    def _get_previous_score(tsv_file: Path) -> Optional[float]:
        """从 results.tsv 倒序读取最近一次 full 模式的总分（已缩放到百分制）。
        兼容 v2.0（58.5 制）和 v3.0（100 制）TSV 行。
        """
        if not tsv_file.exists():
            return None
        try:
            with open(tsv_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in reversed(lines):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split("\t")
                if len(parts) >= 14 and parts[2] == "full":
                    total = float(parts[11])
                    max_val = float(parts[12])
                    # v2.0: max=58.5, 缩放为百分制
                    # v3.0: max=100.0, 已是百分制
                    if max_val == 58.5:
                        total = round(total / 58.5 * 100, 1)
                    return total
        except (ValueError, IndexError, OSError):
            return None
        return None
