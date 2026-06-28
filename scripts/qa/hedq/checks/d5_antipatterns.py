"""D5: 反面案例与边界条件覆盖（Anti-pattern and boundary condition coverage）
子项：
  D5.1 反模式章节覆盖率（满分 4 分）— 含"不要这样做/反模式/错误做法/Anti-Pattern/反例/黑名单"
  D5.2 失败场景章节覆盖率（满分 3 分）— 含"失败/什么情况下会失败/常见错误/失败案例/陷阱/避免/注意"
  D5.3 边界条件章节覆盖率（满分 3 分）— 含"限制/不适用/边界/局限/约束/适用场景/Not Applicable"
设计意图：鼓励每个实操章节都包含反模式和边界条件讨论，这是 technical writing 的最佳实践。
评分基于覆盖率百分比：% 的章节有对应章节 = % 的分数。
排除基础/介绍性章节（00-guide, 01-introduction, README）。
"""
import re
from typing import List, Set

from .base import BaseCheck, CheckResult


class D5AntipatternsCheck(BaseCheck):
    """检查实操性文章是否包含反模式、失败场景、边界条件章节。"""

    # 排除非实操性章节：目录、介绍、封面
    EXCLUDE_DIRS = {"SUMMARY.md", "_book", "00-guide", "01-introduction", "README.md"}

    def run(self) -> List[CheckResult]:
        articles = []
        for md_file in sorted(self.src_dir.rglob("*.md")):
            rel = str(md_file.relative_to(self.src_dir.parent))
            if any(x in rel for x in self.EXCLUDE_DIRS):
                continue
            articles.append(md_file)

        total = len(articles)
        anti = 0      # 有反模式章节的文章数
        failure = 0   # 有失败场景章节的文章数
        bound = 0     # 有边界条件章节的文章数

        # 反模式章节标题关键词（支持中文/英文）
        anti_pat = re.compile(r'##.*(不要这样做|反模式|错误做法|Anti-Pattern|反例|黑名单|常见反模式)')
        # 失败场景章节标题关键词
        fail_pat = re.compile(r'##.*(失败|什么情况下会失败|常见错误|失败案例|陷阱|避免|注意)')
        # 边界条件章节标题关键词
        bound_pat = re.compile(r'##.*(限制|不适用|边界|局限|约束|适用场景|Not Applicable|Considerations)')

        for article in articles:
            with open(article, "r", encoding="utf-8") as f:
                content = f.read()

            if anti_pat.search(content):
                anti += 1
            if fail_pat.search(content):
                failure += 1
            if bound_pat.search(content):
                bound += 1

        # 覆盖率评分：linear percentage
        # D5.1 满分 4：反模式章节覆盖率（anti/total * 4）
        # D5.2 满分 3：失败场景覆盖率（failure/total * 3）
        # D5.3 满分 3：边界条件覆盖率（bound/total * 3）
        # 人工调整：如果认为某些类型章节不重要，可直接降低对应的满分权重
        score_anti = round(4 * anti / total, 1) if total else 0
        score_fail = round(3 * failure / total, 1) if total else 0
        score_bound = round(3 * bound / total, 1) if total else 0
        score = min(round(score_anti + score_fail + score_bound, 1), 10)

        # 注意：不要返回 total 汇总行！runner 会按维度累加所有 CheckResult 的 score，
        # 如果返回 total 行（= score_anti+score_fail+score_bound）会导致分数 double counting。
        return [
            CheckResult("D5", "D5.1", score_anti, 4,
                        f"反模式章节：{anti}/{total}"),
            CheckResult("D5", "D5.2", score_fail, 3,
                        f"失败场景章节：{failure}/{total}"),
            CheckResult("D5", "D5.3", score_bound, 3,
                        f"边界条件章节：{bound}/{total}"),
        ]
