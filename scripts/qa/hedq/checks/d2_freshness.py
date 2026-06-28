"""D2: 内容准确性与时效性 — 版本号新鲜度检测（Content accuracy and freshness）
子项：
  D2.2 版本号新鲜度检查（满分 6 分）
设计思路：对齐 HEDQ 标准的 P1 扣分规则（版本过旧 = P1，子项扣 4 分）。
首个过期版本引用按 P1 级别扣 4 分，后续每个追加扣 1 分；
缺少"新鲜度提醒"机制按 P2 级别扣 1 分。
技术书籍引用旧版本有历史记录需求，但若全书存在多处过期引用，
说明内容维护跟不上版本迭代，应予以较强惩罚。
"""
import re
from typing import List, Dict

from .base import BaseCheck, CheckResult


class D2FreshnessCheck(BaseCheck):
    """扫描全书版本号，找出明显过时的技术版本引用。"""

    # 已知最新版本（截至 2026-06-28）
    # 格式：正则模式 -> "最新版本（版本说明）"
    # 注意：
    #   - 正则需避免匹配到代码样例中的虚构版本号
    #   - OMO v4.x 是 oh-my-openagent 版本，不是 Claude Code
    #   - 当前 Claude Code 已重编号为 v2.x 系列
    # 人工调整：当版本继续更新时，在此字典追加/修改条目即可
    LATEST: Dict[str, str] = {
        # OpenCode：v1.10~v1.15 已过期，当前最新 v1.17.11
        r"v1\.1[0-5]\.": "v1.17+（OpenCode v1.17.11 latest）",
        # oh-my-openagent（OMO）：v4.0~v4.11 已过期，当前最新 v4.12.0
        r"OMO\s+v4\.[0-9]\.|OMO\s+v4\.1[01]\.": "v4.12+（OMO v4.12.0 latest）",
        # Node.js：v1x 已过期，当前 Active LTS 为 v24
        r"node\s+v?1[0-7]\.": "Node 20+（当前 LTS v24）",
        r"node\s+v?18\.[0-9]": "Node 22+（当前 LTS v24）",
        # Python：3.7/3.8/3.9 已过期，当前最新 3.14.6
        r"Python\s+3\.(?:7|8|9)": "Python 3.11+（当前 3.14）",
        # Node.js 20 已在接近 EOL（2026-10），建议升级
        r"Node\.js\s+20\b": "Node 22+（v20 将于 2026-10 EOL）",
        # Python 3.10 已在接近 EOL（2026-10），建议升级
        r"Python\s+3\.10": "Python 3.11+（3.14 latest）",
    }

    def run(self) -> List[CheckResult]:
        version_errors = 0
        found_versions: List[str] = []

        for md_file in sorted(self.src_dir.rglob("*.md")):
            if "_book" in str(md_file):
                continue
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            # 跳过代码块中的版本号（可能是示例代码中的虚构版本）
            cleaned = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
            cleaned = re.sub(r'`[^`]+`', '', cleaned)

            for pattern, latest in self.LATEST.items():
                for m in re.finditer(pattern, cleaned, re.IGNORECASE):
                    version_errors += 1
                    rel = str(md_file.relative_to(self.src_dir.parent))
                    found_versions.append(f"{m.group()}（{rel}）")

        # 检查是否存在"新鲜度提醒"章节或标记
        # 这是鼓励书籍维护者定期更新的机制（P2 级别）
        has_reminder = False
        for md_file in self.src_dir.rglob("*.md"):
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()
                if re.search(r"每月检查|last.*check.*date|freshness.*check", content, re.IGNORECASE):
                    has_reminder = True
                    break

        # 扣分规则（对齐 HEDQ 标准）：
        # - 首个过期版本引用：P1 级别，扣 4 分
        # - 后续每个过期版本：追加扣 1 分
        # - 缺少新鲜度提醒机制：P2 级别，扣 1 分
        # 最低 0 分，无底分保护
        penalty = 0
        if version_errors > 0:
            penalty += 4 + (version_errors - 1) * 1  # 首个 4 分，后续每个 1 分
        if not has_reminder:
            penalty += 1

        score = max(0, 6 - penalty)

        found_str = f"过期版本引用：{version_errors} 处"
        if not has_reminder:
            found_str += "；缺少新鲜度提醒机制"
        if found_versions:
            found_str += " — " + "; ".join(found_versions[:8])
            if len(found_versions) > 8:
                found_str += f" （+{len(found_versions)-8} more）"

        return [CheckResult("D2", "D2.2", score, 6, found_str)]
