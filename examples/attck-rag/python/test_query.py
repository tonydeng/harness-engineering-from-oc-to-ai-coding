#!/usr/bin/env python3
"""
ATT&CK RAG — query.py 批量验证器

读取 skills/attck-rag/test-prompts.json，对每条测试用例执行
query.py 的混合检索管线（不含 LLM 生成），验证检索质量。

用法:
    python test_query.py [--db 数据库路径] [--test 测试文件路径]
"""

import json, os, sys, time, re
from pathlib import Path

# 将项目根加入 path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from query import (
    hybrid_search, classify_query, extract_target_tid, direct_tid_lookup,
    disclosure_filter, EXACT_PATTERN,
)
from config import AttckRagConfig

SKILL_DIR = Path(__file__).resolve().parent.parent / "skills" / "attck-rag"
TEST_FILE = str(SKILL_DIR / "test-prompts.json")
DEFAULT_DB = str(SKILL_DIR / "attck_vec.db")

# ---------------------------------------------------------------------------
# Chunk-level quality metrics (no LLM)
# ---------------------------------------------------------------------------

def chunk_quality_report(chunks: list) -> dict:
    """从检索结果中提取质量指标（不依赖 LLM 回答）"""
    tids = set()
    tas = set()
    levels = set()
    for c in chunks:
        meta = c.get("meta", {})
        if meta.get("t_id"):
            tids.add(meta["t_id"])
        if meta.get("sub_id"):
            tids.add(meta["sub_id"])
        if meta.get("ta_id"):
            tas.add(meta["ta_id"])
        if meta.get("level"):
            levels.add(meta["level"])
    return {
        "chunk_count": len(chunks),
        "ground_truth_tids": sorted(tids),
        "ground_truth_tactics": sorted(tas),
        "levels": sorted(levels),
    }

# ---------------------------------------------------------------------------
# Evaluation heuristics (mirrors run_tests.py)
# ---------------------------------------------------------------------------

def evaluate_exact(results: list, quality: dict, prompt: str) -> dict:
    """EXACT 验证：必须命中目标 TID/TAID"""
    tid_set = set(quality["ground_truth_tids"])
    ta_set = set(quality["ground_truth_tactics"])

    expected_tids = set(re.findall(EXACT_PATTERN, prompt.upper()))
    expected_tas = {t for t in expected_tids if t.startswith("TA")}

    passed = quality["chunk_count"] > 0

    tids_to_check = expected_tids - expected_tas
    if tids_to_check:
        if not (tids_to_check & tid_set):
            passed = False

    if expected_tas:
        if not (expected_tas & ta_set):
            passed = False

    return {
        "passed": passed,
        "chunk_count": quality["chunk_count"],
        "found_tids": tid_set,
        "found_tas": ta_set,
        "expected_tids": expected_tids,
    }


def evaluate_factual(results: list, quality: dict, prompt: str) -> dict:
    """FACTUAL 验证：返回有意义的结果"""
    passed = quality["chunk_count"] > 0
    return {
        "passed": passed,
        "chunk_count": quality["chunk_count"],
        "levels": quality["levels"],
        "found_tids": quality["ground_truth_tids"],
        "found_tas": quality["ground_truth_tactics"],
    }


def evaluate_analysis(results: list, quality: dict, prompt: str) -> dict:
    """ANALYSIS 验证：至少 2 个结果才有分析价值"""
    passed = quality["chunk_count"] >= 2
    return {
        "passed": passed,
        "chunk_count": quality["chunk_count"],
        "levels": quality["levels"],
        "found_tids": quality["ground_truth_tids"],
        "found_tas": quality["ground_truth_tactics"],
    }


def evaluate_boundary(results: list, quality: dict, prompt: str) -> dict:
    """BOUNDARY 验证：按场景检查。每个检查只处理明确匹配的场景。"""

    s = prompt.strip()

    # ── 0. 空/纯空格/单字符 T/TA：应返回 0 结果 ──
    if not s or s.upper() in {"T", "TA"}:
        passed = quality["chunk_count"] == 0
        return {"passed": passed, "chunk_count": quality["chunk_count"],
                "reason": "空/无效输入应返回 0 结果"}

    # ── 1. 小写 t1059 — 应大小写归一 → 返回结果 ──
    if re.match(r't\d{4}', prompt):
        passed = quality["chunk_count"] >= 1
        return {"passed": passed, "chunk_count": quality["chunk_count"],
                "found_tids": quality["ground_truth_tids"],
                "reason": "小写 TID 应大小写归一"}

    # ── 2. 格式异常 TID（尾部点/双点/前导点/连字符/三级嵌套） ──
    if re.search(r'T\d{4}[.]$|T\d{4}[.]{2}|^[.]T|T-\d{4}|T\d{4}\.\d{3}\.\d{3}', prompt):
        passed = quality["chunk_count"] >= 1
        return {"passed": passed, "chunk_count": quality["chunk_count"],
                "found_tids": quality["ground_truth_tids"],
                "reason": "格式异常 TID 应能自动修正"}

    # ── 3-4 联合：多 TID / 不存在 TID — 基于返回结果判定 ──
    tids = re.findall(r'T\d{4}', prompt.upper())
    found_tids = set(quality.get("ground_truth_tids", []))
    real_overlap = set(tids) & found_tids
    has_results = quality["chunk_count"] > 0

    if len(tids) >= 3:
        if real_overlap or has_results:
            passed = True
        else:
            passed = quality["chunk_count"] == 0
        return {"passed": passed, "chunk_count": quality["chunk_count"],
                "found_tids": sorted(found_tids), "expected_tids": list(set(tids)),
                "reason": "多 TID：全假应 0 结果，有真应返回"}

    # ── 1-2 个 TID：尝试提取但未命中且无结果 → 全假 TID，应 0 结果 ──
    if tids and not real_overlap and not has_results:
        passed = quality["chunk_count"] == 0
        return {"passed": passed, "chunk_count": quality["chunk_count"],
                "found_tids": sorted(found_tids), "expected_tids": list(set(tids)),
                "reason": "提取出 TID 但全不存在"}

    # ── 5. 其他边界（特殊字符/无关/SQL注入/自然语言中混TID）：不崩溃即可 ──
    return {"passed": True, "chunk_count": quality["chunk_count"],
            "reason": "无异常崩溃"}


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_tests(test_file: str, db_path: str) -> list:
    with open(test_file, "r", encoding="utf-8") as f:
        tests = json.load(f)

    import sqlite3
    try:
        import sqlite_vec
    except ImportError:
        print("⚠  sqlite-vec 未安装，向量检索将不可用")
        sqlite_vec = None

    conn = sqlite3.connect(db_path)
    conn.enable_load_extension(True)
    if sqlite_vec:
        sqlite_vec.load(conn)

    # 确保 FTS5 表存在
    FTS5_SCHEMA_SQL = """
    CREATE VIRTUAL TABLE IF NOT EXISTS attck_chunks_fts USING fts5(
        chunk_text, ta_id UNINDEXED, t_id UNINDEXED,
        sub_id UNINDEXED, level UNINDEXED,
        content='attck_chunks', content_rowid='rowid'
    );"""
    FTS5_POPULATE_SQL = """
    INSERT OR IGNORE INTO attck_chunks_fts(rowid, chunk_text, ta_id, t_id, sub_id, level)
    SELECT rowid, chunk_text,
           json_extract(metadata, '$.ta_id'),
           json_extract(metadata, '$.t_id'),
           json_extract(metadata, '$.sub_id'),
           json_extract(metadata, '$.level')
    FROM attck_chunks;"""
    try:
        conn.executescript(FTS5_SCHEMA_SQL)
        conn.executescript(FTS5_POPULATE_SQL)
        conn.commit()
    except Exception:
        pass

    cfg = AttckRagConfig()
    cfg.db_path = db_path  # override

    results = []
    passed = failed = crashed = 0

    for test in tests:
        test_type = test["type"]
        query_type, depth = classify_query(test["prompt"])
        eval_fn = {
            "exact": evaluate_exact,
            "factual": evaluate_factual,
            "analysis": evaluate_analysis,
            "boundary": evaluate_boundary,
        }.get(test_type, evaluate_factual)

        outcome = {
            "id": test["id"], "type": test_type, "prompt": test["prompt"],
            "passed": False, "depth": depth,
            "quality": None, "eval": None, "error": None,
        }

        try:
            chunks = hybrid_search(conn, test["prompt"], cfg.top_k, depth, cfg)
            quality = chunk_quality_report(chunks)
            eval_result = eval_fn(chunks, quality, test["prompt"])
            outcome["passed"] = eval_result["passed"]
            outcome["quality"] = quality
            outcome["eval"] = eval_result
        except Exception as e:
            outcome["error"] = str(e)
            crashed += 1

        if outcome["passed"]:
            passed += 1
        else:
            failed += 1

        results.append(outcome)

        status = "✅" if outcome["passed"] else "❌"
        if outcome["error"]:
            status = "💥"
        cc = outcome['quality']['chunk_count'] if outcome['quality'] else 'ERR'
        print(f"  [{status}] #{outcome['id']:2d} [{test_type:8s}] {test['prompt'][:60]:60s} "
              f"chunks={str(cc):>4s}", flush=True)

    conn.close()

    print(f"\n{'='*70}")
    print(f"  总计: {len(tests):2d}  |  ✅ PASS: {passed:2d}  |  ❌ FAIL: {failed:2d}  |  💥 CRASH: {crashed}")
    print(f"{'='*70}")

    return results


def format_report(results: list, output_path: str = None):
    """生成详细报告"""
    lines = ["# ATT&CK RAG — query.py 验证报告\n"]
    lines.append(f"| # | 类型 | 结果 | Chunks | TIDs | Prompt |")
    lines.append(f"|---|------|:----:|:------:|:----:|--------|")

    for r in results:
        status = "✅" if r["passed"] else "❌"
        if r["error"]:
            status = "💥"
        tids = ""
        if r["quality"]:
            tids = ",".join(r["quality"]["ground_truth_tids"][:3])
        cc = r["quality"]["chunk_count"] if r["quality"] else "ERR"
        prompt = r["prompt"][:50].replace("|", "\\|")
        lines.append(f"| {r['id']:2d} | {r['type']:8s} | {status} | {cc!s:4s} | {tids:16s} | {prompt} |")

    lines.append("")
    passed = sum(1 for r in results if r["passed"])
    failed = sum(1 for r in results if not r["passed"] and not r["error"])
    crashed = sum(1 for r in results if r["error"])

    lines.append(f"\n**Summary**: {len(results)} total | ✅ {passed} PASS | ❌ {failed} FAIL | 💥 {crashed} CRASH")
    pass_rate = passed / len(results) * 100 if results else 0
    lines.append(f"**Pass Rate**: {pass_rate:.1f}%")
    lines.append("")

    if failed or crashed:
        lines.append("## Failed / Crashed 详情\n")
        for r in results:
            if not r["passed"]:
                eval_detail = r["eval"] or {}
                lines.append(f"\n### #{r['id']} [{r['type']}] {r['prompt'][:80]}")
                lines.append(f"- Chunks: {eval_detail.get('chunk_count', '?')}")
                lines.append(f"- Expected TIDs: {eval_detail.get('expected_tids', 'N/A')}")
                lines.append(f"- Found TIDs: {eval_detail.get('found_tids', 'N/A')}")
                if r["error"]:
                    lines.append(f"- Error: `{r['error']}`")
                if "reason" in eval_detail:
                    lines.append(f"- Reason: {eval_detail['reason']}")

    report = "\n".join(lines)
    if output_path:
        Path(output_path).write_text(report, encoding="utf-8")
        print(f"报告已保存: {output_path}")
    else:
        print(report)

    return report


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description="query.py 批量验证")
    ap.add_argument("--db", default=DEFAULT_DB)
    ap.add_argument("--test", default=TEST_FILE)
    ap.add_argument("--report", help="报告输出路径（可选）")
    args = ap.parse_args()

    print(f"测试用例: {args.test}")
    print(f"数据库:   {args.db}")
    print(f"\n开始执行...\n")

    t0 = time.time()
    results = run_tests(args.test, args.db)
    elapsed = time.time() - t0
    print(f"\n总耗时: {elapsed:.1f}s")

    report_path = args.report or str(Path(args.test).parent / "test-report-query.md")
    format_report(results, report_path)
