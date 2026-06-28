"""D7: 术语与品牌一致性（Terminology and brand consistency）
子项：
  D7.1 品牌名一致性检查（满分 4 分）— 检查 OpenCode/MCP/mdBook/oh-my-openagent 拼写
  D7.2 核心术语大小写一致（满分 3 分）— 检查 Agent/Skill/Workflow/Plugin 在标题中大小写
  D7.3 交叉引用格式规范（满分 3 分）— 检查 → [章节名](path.md) 格式
设计意图：确保全书术语和品牌名一致性，增强专业感。
跳过大面积代码块、URL、shell 命令以减少误报。
"""
import re
from typing import List, Set

from .base import BaseCheck, CheckResult


class D7TerminologyCheck(BaseCheck):
    """检查品牌名拼写、核心术语大小写、交叉引用格式。"""

    # 品牌模式对照表：(正确写法, [错误变体列表])
    # 人工调整：新增品牌时在此追加元组即可
    BRANDS = [
        ("OpenCode", ["Opencode", "opencode", "Open Code"]),
        ("oh-my-openagent", ["Oh-My-Openagent", "OH-MY-OPENAGENT", "oh_my_openagent"]),
        ("MCP", ["Mcp"]),
        ("mdBook", ["mdbook", "Mdbook"]),
    ]

    # 核心术语（要求标题中首字母大写）
    # 正文中允许小写（技术性引用），但 H1/H2 标题中应大写
    # 人工调整：新增核心术语时在此列表追加
    TERMS = [
        "Agent", "Skill", "Workflow", "Plugin",
    ]

    # 需要跳过的不应触发误报的代码标识符
    # 这些是函数名/包名/路径/CLI 工具名，不是品牌名拼写错误
    SKIP_IDENTIFIERS = re.compile(
        r'createOpencode|OpencodeClient|Opencode-DCP|@opencode|'
        r'createSdkMcpServer|McpServer|McpClient|/Mcp|Mcp\.|'
        r'mdbook-(?:mermaid|toc|pagetoc|linkcheck|katex|mathjax|plantuml)'
    )

    def run(self) -> List[CheckResult]:
        results = []
        results.append(self._check_brand_names())
        results.append(self._check_term_cases())
        results.append(self._check_cross_refs())
        return results

    def _iter_prose_lines(self):
        """遍历所有 Markdown 文件的纯文本行（非代码、非 URL、非 shell 命令）。
        Yields: (文件相对路径, 行文本)
        跳过规则：代码块、URL、shell 命令、Markdown 链接 URL。
        """
        for md_file in sorted(self.src_dir.rglob("*.md")):
            if "_book" in str(md_file):
                continue
            rel = str(md_file.relative_to(self.src_dir.parent))
            with open(md_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            in_code_block = False
            for line in lines:
                stripped = line.rstrip()
                if stripped.lstrip().startswith("```"):
                    in_code_block = not in_code_block
                    continue
                if in_code_block:
                    continue
                if re.search(r'https?://', stripped):
                    continue
                # 跳过 shell 命令行（$ 开头）
                if re.match(r'^\s*\$ ', stripped):
                    continue
                # 跳过 Markdown 链接（URL 在 () 中）
                if re.match(r'^\s*\[.+\]\(https?://', stripped):
                    continue

                yield (rel, stripped)

    def _check_brand_names(self) -> CheckResult:
        """D7.1: 品牌名拼写检查。
        评分规则：满分 4 分，每个错误扣 0.15 分，最低 0 分（上限 4 分）。
        检查 4 个品牌：OpenCode、oh-my-openagent、MCP、mdBook 的错误变体。
        跳过规则：代码标识符（createOpencode, McpServer 等）、URL、shell 命令。
        人工调整：如果认为扣分太轻，将 0.15 改为 0.3 或更高。
        """
        errors = 0

        for rel, line in self._iter_prose_lines():
            # 剔除行内代码（`xxx`）后再检查
            clean = re.sub(r'`[^`]+`', '', line)

            # OpenCode：检测 Opencode（首字母大写但 C 小写）
            if re.search(r'(?<![a-zA-Z])Opencode(?![a-zA-Z])', clean):
                if not self.SKIP_IDENTIFIERS.search(clean):
                    errors += 1

            # Open Code（两个单词）：排除 "Open Code Review" 工具名
            if "Open Code" in clean and "Open Code Review" not in clean:
                errors += 1

            # oh-my-openagent 错误的大小写/分隔符变体
            if re.search(r'Oh-My-Openagent|OH-MY-OPENAGENT|oh_my_openagent', clean):
                errors += 1

            # MCP 的小写变体 Mcp（仅在散文语境中，排除路径/标识符）
            if re.search(r'(?<![a-zA-Z])Mcp(?![a-zA-Z])', clean):
                if not re.search(r'/[Mm]cp|McpServer|Mcp[./]', clean):
                    errors += 1

            # mdbook 小写变体（散文中应该用 mdBook）
            # 注意：mdbook-mermaid 等 cargo 包名已通过 SKIP_IDENTIFIERS 跳过
            # 此处的负向先行断言也排除连字符，避免 mdbook-xxx 被误报
            if re.search(r'(?<![a-zA-Z])mdbook(?![a-zA-Z-])', clean):
                if not self.SKIP_IDENTIFIERS.search(clean):
                    errors += 1
            if re.search(r'(?<![a-zA-Z])Mdbook(?![a-zA-Z-])', clean):
                if not self.SKIP_IDENTIFIERS.search(clean):
                    errors += 1

        score = max(0, 4 - (errors * 0.15))
        return CheckResult("D7", "D7.1", min(score, 4), 4,
                           f"品牌名错误：{errors} 处")

    def _check_term_cases(self) -> CheckResult:
        """D7.2: 核心术语在 H1/H2 标题中的大小写一致性。
        评分规则：满分 3 分，每个错误扣 0.05 分，最低 0 分。
        仅限于检查 H1/H2 标题（## 和 #），正文中的小写术语视为技术用法。
        人工调整：如果要扩展到正文检查，去掉 `if not re.search(r'^#{1,2}\s', clean): continue`。
        """
        errors = 0
        error_details = []

        for rel, line in self._iter_prose_lines():
            clean = re.sub(r'`[^`]+`', '', line)

            # 仅限于 H1/H2 标题 — 表格和正文中小写术语是正常的
            if not re.search(r'^#{1,2}\s', clean):
                continue

            for term in self.TERMS:
                lower = term.lower()
                for m in re.finditer(rf'(?<![a-zA-Z]){lower}(?![a-zA-Z])', clean):
                    errors += 1
                    if len(error_details) < 5:
                        error_details.append(f"{m.group()}({rel})"[:60])

        score = max(0, 3 - (errors * 0.05))
        return CheckResult("D7", "D7.2", min(score, 3), 3,
                           f"术语大小写错误：{errors} 处")

    def _check_cross_refs(self) -> CheckResult:
        """D7.3: 交叉引用格式检查。
        评分规则：满分 3 分，得分 = 3 * (正确数/总数)。
        正确格式：→ [章节名](路径.md)（→ 后有空格）
        错误格式：→[章节名](路径.md)（→ 后无空格）
        人工调整：如果需要检查更多格式约束，扩展 ref_pat 即可。
        """
        total = 0
        good = 0
        ref_pat = re.compile(r'→\s+\[([^\]]+)\]\(([^)]+)\)')  # 正确：→后有空格
        wrong_pat = re.compile(r'→\[')  # 错误：→后无空格

        for md_file in sorted(self.src_dir.rglob("*.md")):
            if "_book" in str(md_file) or "SUMMARY.md" in str(md_file):
                continue
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            for m in ref_pat.finditer(content):
                total += 1
                good += 1

            for m in wrong_pat.finditer(content):
                total += 1

        score = round(3 * good / total, 1) if total else 0
        return CheckResult("D7", "D7.3", score, 3,
                           f"交叉引用格式：{good}/{total} 正确")
