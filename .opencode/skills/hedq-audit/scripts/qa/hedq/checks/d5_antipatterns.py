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
        # score = min(round(score_anti + score_fail + score_bound, 1), 10)  # unused, removed

        # --- D5.4 内容厚度检查 ---
        # 对于已识别到有相关章节的文章，检查章节下的段落数是否 >= 3
        # 如果章节标题下只有 1-2 段，说明内容可能较浅
        anti_shallow = 0
        fail_shallow = 0
        bound_shallow = 0
        shallow_details: List[str] = []

        for article in articles:
            with open(article, "r", encoding="utf-8") as f:
                content = f.read()
            rel = str(article.relative_to(self.src_dir.parent))

            # 按行逐段分析章节厚度
            lines = content.split("\n")
            current_section_depth = 0     # 0=无活跃 section，1=反模式，2=失败，3=边界
            section_para_count = 0
            in_thickness_check = False
            first_para_since_entry = True  # 标记标题后的首段（无论有无空行分隔）

            for i, line in enumerate(lines):
                stripped = line.rstrip()

                # 检测二级标题（##）
                if stripped.startswith("## "):
                    # 结束上一个活跃 section 的计数
                    if in_thickness_check and section_para_count < 3:
                        rel_label = f"{rel}:L{i+1}"
                        if current_section_depth == 1:
                            anti_shallow += 1
                            shallow_details.append(f"反模式浅层:{rel_label}")
                        elif current_section_depth == 2:
                            fail_shallow += 1
                            shallow_details.append(f"失败场景浅层:{rel_label}")
                        elif current_section_depth == 3:
                            bound_shallow += 1
                            shallow_details.append(f"边界条件浅层:{rel_label}")

                    # 判断新 section 类型
                    in_thickness_check = False
                    section_para_count = 0
                    current_section_depth = 0
                    first_para_since_entry = True

                    if anti_pat.search(stripped):
                        current_section_depth = 1
                        in_thickness_check = True
                    elif fail_pat.search(stripped):
                        current_section_depth = 2
                        in_thickness_check = True
                    elif bound_pat.search(stripped):
                        current_section_depth = 3
                        in_thickness_check = True
                    continue

                # 如果 in_thickness_check，统计段落
                if in_thickness_check:
                    # 遇到更高层级标题或分隔符则停止
                    if stripped.startswith("#") or stripped.startswith("---"):
                        if in_thickness_check and section_para_count < 3:
                            rel_label = f"{rel}:L{i+1}"
                            if current_section_depth == 1:
                                anti_shallow += 1
                                shallow_details.append(f"反模式浅层:{rel_label}")
                            elif current_section_depth == 2:
                                fail_shallow += 1
                                shallow_details.append(f"失败场景浅层:{rel_label}")
                            elif current_section_depth == 3:
                                bound_shallow += 1
                                shallow_details.append(f"边界条件浅层:{rel_label}")
                        in_thickness_check = False
                        section_para_count = 0
                        current_section_depth = 0
                        continue

                    # 空行分隔段落，连续非空行视为一段
                    if stripped == "":
                        # 空行不影响计数，但前一段已结束
                        first_para_since_entry = False  # 非首段位置了
                    else:
                        # 非空行计数：标题后首段始终计数（即使无空行），后续段落按空行分隔
                        if first_para_since_entry:
                            section_para_count += 1
                            first_para_since_entry = False
                        elif i == 0 or (lines[i-1].strip() == ""):
                            section_para_count += 1

            # 文件末尾的活跃 section 也需要结算
            if in_thickness_check and section_para_count < 3:
                if current_section_depth == 1:
                    anti_shallow += 1
                elif current_section_depth == 2:
                    fail_shallow += 1
                elif current_section_depth == 3:
                    bound_shallow += 1

        # D5.4 评分：满分 3 分，基于浅层章节占比
        total_d5_4_checks = anti + failure + bound  # 有内容章节总数
        shallow_total = anti_shallow + fail_shallow + bound_shallow
        d5_4_score = round(3 * (1 - shallow_total / max(total_d5_4_checks, 1)), 1)
        d5_4_detail = f"内容厚度：{shallow_total}/{total_d5_4_checks} 个章节浅层（段落<3）"
        if shallow_details:
            d5_4_detail += " — " + "; ".join(shallow_details[:5])
            if len(shallow_details) > 5:
                d5_4_detail += f" (+{len(shallow_details)-5} more)"

        # 注意：不要返回 total 汇总行！runner 会按维度累加所有 CheckResult 的 score，
        # 如果返回 total 行（= score_anti+score_fail+score_bound）会导致分数 double counting。
        return [
            CheckResult("D5", "D5.1", score_anti, 4,
                        f"反模式章节：{anti}/{total}"),
            CheckResult("D5", "D5.2", score_fail, 3,
                        f"失败场景章节：{failure}/{total}"),
            CheckResult("D5", "D5.3", score_bound, 3,
                        f"边界条件章节：{bound}/{total}"),
            CheckResult("D5", "D5.4", d5_4_score, 3,
                        d5_4_detail),
        ]
