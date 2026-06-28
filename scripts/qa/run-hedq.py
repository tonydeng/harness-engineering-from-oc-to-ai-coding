#!/usr/bin/env python3
"""HEDQ 质量审计 CLI（跨平台入口）
用法：
  python scripts/qa/run-hedq.py              # 完整审计
  python scripts/qa/run-hedq.py --quick       # 快速模式（D1+D6+D7，~10s）
  python scripts/qa/run-hedq.py --json        # JSON 输出
  python scripts/qa/run-hedq.py --no-save     # 不写磁盘
"""
import argparse
import sys
from pathlib import Path
from hedq.runner import HEDQRunner, DEFAULT_REPORT_DIR


def main():
    parser = argparse.ArgumentParser(
        description="HEDQ 质量审计 — 8 维度评估书籍质量"
    )
    parser.add_argument(
        "--quick", action="store_true",
        help="快速模式：仅跑 D1 结构 + D6 文风 + D7 术语（约 10 秒）"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="以 JSON 格式输出报告（默认是 Markdown）"
    )
    parser.add_argument(
        "--src", type=str, default=None,
        help="源目录（默认：<项目>/src）"
    )
    parser.add_argument(
        "--docs", type=str, default=None,
        help="文档目录（默认：<项目>/docs）"
    )
    parser.add_argument(
        "--report-dir", type=str, default=None,
        help="报告输出目录（默认：<脚本目录>/reports）"
    )
    parser.add_argument(
        "--no-save", action="store_true",
        help="不保存报告到磁盘（默认自动保存）"
    )
    args = parser.parse_args()

    # 定位项目根目录：本脚本位于 <root>/scripts/qa/run-hedq.py
    # 因此 root = script_dir / ../../
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent.parent

    src_dir = Path(args.src) if args.src else project_root / "src"
    docs_dir = Path(args.docs) if args.docs else project_root / "docs"
    report_dir = Path(args.report_dir) if args.report_dir else DEFAULT_REPORT_DIR

    if not src_dir.exists():
        print(f"错误：源目录未找到：{src_dir}", file=sys.stderr)
        sys.exit(1)

    runner = HEDQRunner(
        src_dir=src_dir,
        docs_dir=docs_dir,
        quick=args.quick,
        json_mode=args.json,
        report_dir=report_dir,
    )
    results, total_score, total_max = runner.run()

    # 生成并打印报告（Markdown 或 JSON）
    report = runner.generate_report(results, total_score, total_max)
    print(report)

    # 保存结果到磁盘（JSON 快照 + results.tsv 趋势记录）
    if not args.no_save:
        runner.save_report(results, total_score, total_max)

    # 在 stderr 打印汇总
    pct = (total_score / total_max * 100) if total_max > 0 else 0
    print(f"\n总分：{total_score:.1f}/{total_max}（{pct:.1f}%）", file=sys.stderr)


if __name__ == "__main__":
    main()
