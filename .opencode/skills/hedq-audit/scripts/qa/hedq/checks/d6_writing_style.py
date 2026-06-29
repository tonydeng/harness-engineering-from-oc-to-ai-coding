"""D6: 文风与可读性 — AI 腔检测（Writing style and readability）
子项：
  D6.3 AI 生成痕迹检测（满分 2 分）
设计意图：检测书中是否出现典型的 AI 生成文本特征（"空话/套话"），
这些表达方式在技术写作中应避免。
注意：已排除正常的过渡词（首先/其次/再次），
这些是中文写作的正常组成部分，不属于 AI 腔。
"""
import re
from typing import List

from .base import BaseCheck, CheckResult


class D6WritingStyleCheck(BaseCheck):
    """扫描全书，找出 AI 生成的高频空话套话模式。"""

    # 禁用词列表 — 中文 AI 腔典型废话
    # 排除说明：正常的过渡词（首先、其次、再次）已被移除，
    # 因为这些是中文写作的正常组成部分，不代表 AI 生成。
    # 新增 v3：增加了更多技术写作中常见的空话套话模式。
    # 人工调整：如果发现新的 AI 腔模式，直接在此列表追加；
    # 如果某些词在上下文中是正常的，从此列表移除。
    # 注意："显而易见"使用负向回视断言排除"非显而易见"（合法技术用语），
    # 因为 Python re 模块不支持变长回视，这里通过将正则写入 BANNED_PATTERNS 实现。
    BANNED = [
        "说白了",
        "换句话说",
        # "首先", "其次", "再次" — 已排除，中文正常过渡用词
        "综上所述",
        "综上",
        "值得注意的是",
        "不言而喻",
        "显而易见",
        "众所周知",
        "毫无疑问",
        "需要注意的是",
        "值得一提的是",
        "在一定程度上",
        "从某种角度来说",
        "基于此",
        "因此可以说",
        "不容忽视",
        "不可否认",
        # 以下为 v3 新增——技术写作中的空话/过度填充模式
        # 注意："深入分析"是正常技术用语，不会误报；"旨在"、"提供了一个"也是自然表达，不在此列。
        "具有重要意义",          # 空话
        "扮演着重要角色",        # 空话
        "不可或缺",              # 过度绝对
        # === v4 新增（2026-06-29）===
        # P0: 同步质量标准的文档-代码差距
        "不可置否",              # 文档中有但代码缺失
        "不得不承认",            # 文档中有但代码缺失
        "从本质上讲",            # 文档中有但代码缺失
        "从另一个角度",          # 文档中有但代码缺失
        # P1: 高频 AI 过渡用词
        "需要指出的是",          # 中英直译 "It should be noted that"
        "需要强调的是",          # AI 替代人强调时的标准句式
        "更为重要的是",          # LLM 论证升级的标准话术
        "换言之",                # "换句话说"的变体
        "简单来说",              # AI 总结段的标准开头
        # P2: AI 过度绝对化用语
        # 注："至关重要"已评估后移除——该词在技术写作中频繁合法使用
        # (e.g., "安全配置至关重要"、"理解边界至关重要")，8处命中全为合法表达。
        # 如需增强检测，建议匹配更具体的模式如 "起着至关重要的作用"。
        "极其重要",              # AI 的 extreme 形容词偏好
        "在某种程度上",          # AI 模糊话术
        "从某种意义上说",        # AI 模糊话术
    ]

    def run(self) -> List[CheckResult]:
        # 构建正则：对"显而易见"使用负向回视断言排除"非显而易见"
        # "非显而易见"是合法技术用语（如"非显而易见的优势"），不应被误报
        patterns = []
        for w in self.BANNED:
            if w == "显而易见":
                # 仅匹配前面不是"非"的"显而易见"
                patterns.append(r'(?<!非)显而易见')
            else:
                patterns.append(re.escape(w))
        pattern = re.compile("|".join(patterns))
        hits = 0

        for md_file in sorted(self.src_dir.rglob("*.md")):
            if "_book" in str(md_file):
                continue
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            # 排除代码块和注释中的内容（代码中的字符串可能包含这些词）
            cleaned = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
            cleaned = re.sub(r'<!--.*?-->', '', cleaned, flags=re.DOTALL)

            hits += len(pattern.findall(cleaned))

        # 扣分规则：每处 AI 腔扣 0.2 分，满分 2 分
        # 这意味着 10 处以上 hits 就会扣光此维度
        # 人工调整：如果觉得过于严格，将 0.2 改为 0.1
        score = max(0, 2 - (hits * 0.2))
        return [CheckResult("D6", "D6.3", score, 2, f"AI 腔命中：{hits} 处")]
