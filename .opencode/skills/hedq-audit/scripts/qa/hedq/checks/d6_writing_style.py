"""D6: 文风与可读性 — AI 腔检测（Writing style and readability）
子项：
  D6.3 AI 生成痕迹检测（满分 2 分）
设计意图：检测书中是否出现典型的 AI 生成文本特征（"空话/套话"），
这些表达方式在技术写作中应避免。
注意：已排除正常的过渡词（首先/其次/再次），
这些是中文写作的正常组成部分，不属于 AI 腔。

禁用词清单从独立文件加载：scripts/qa/hedq/config/banned_ai_speak.txt
这样做便于非开发人员维护禁用词列表，无需修改检测代码。
"""
import os
import re
from typing import List

from .base import BaseCheck, CheckResult


# 禁用词清单文件路径（相对于本文件所在目录）
_BANNED_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "config",
    "banned_ai_speak.txt",
)


def _load_banned_words(path: str = _BANNED_FILE) -> List[str]:
    """从 banned_ai_speak.txt 加载禁用词列表。

    文件格式：
    - 空行和 "#" 开头行视为注释，跳过
    - 其余每行作为一个禁用词/短语
    - 行首尾空格会被去除

    返回：禁用词字符串列表（去空、去重后的活跃模式）
    """
    words = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            words.append(stripped)
    # 去重（保持首次出现顺序）
    seen = set()
    unique = []
    for w in words:
        if w not in seen:
            seen.add(w)
            unique.append(w)
    return unique


class D6WritingStyleCheck(BaseCheck):
    """扫描全书，找出 AI 生成的高频空话套话模式。

    禁用词列表从独立配置文件加载，见 config/banned_ai_speak.txt。
    如需调整禁用词，直接修改该文件即可，无需改动此代码。
    """

    # 从独立文件加载禁用词列表
    # 人工调整：如需新增/移除禁用词，编辑 banned_ai_speak.txt 即可
    BANNED = _load_banned_words()

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
