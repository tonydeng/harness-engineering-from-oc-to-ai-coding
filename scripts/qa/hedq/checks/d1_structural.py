"""D1: 结构与元数据规范性（Structures and metadata compliance）
子项：
  D1.1 SUMMARY.md 路径检查（满分 3 分）
  D1.2 内部链接检查（满分 4 分）
  D1.4 品牌名拼写检查（满分 4 分）
总分上限 15，但此处 D1 子项满分合计 11，剩余 4 分由 runner 中 cap 控制。
"""
import re
from pathlib import Path
from typing import List, Set

from .base import BaseCheck, CheckResult


class D1StructuralCheck(BaseCheck):
    """检查 SUMMARY.md 路径有效性、内部链接是否断裂、品牌名拼写是否正确。"""

    def run(self) -> List[CheckResult]:
        results = []
        results.extend(self._check_summary_paths())
        results.extend(self._check_internal_links())
        results.extend(self._check_brand_names())
        return results

    def _check_summary_paths(self) -> List[CheckResult]:
        """D1.1: SUMMARY.md 中所有文件路径是否存在。
        评分规则：满分 3 分，每个断裂路径扣 1 分，最低 0 分。
        逻辑：解析 SUMMARY.md 中 (path.md) 格式的链接，
        验证文件在 src/ 下是否存在。
        人工调整：如果这本书不需要全部文件存在（如草稿），可将扣分改为 0.5/个。
        """
        summary = self.src_dir / "SUMMARY.md"
        if not summary.exists():
            return [CheckResult("D1", "D1.1", 0, 3, "SUMMARY.md 未找到")]

        total = 0
        broken = 0
        with open(summary, "r", encoding="utf-8") as f:
            for line in f:
                m = re.search(r'\(([^)]+\.md)\)', line)
                if m:
                    total += 1
                    target = self.src_dir / m.group(1)
                    if not target.exists():
                        broken += 1

        score = max(0, 3 - broken)
        return [CheckResult("D1", "D1.1", score, 3,
                            f"SUMMARY.md：{total} 条路径正常，{broken} 条断裂")]

    def _check_internal_links(self) -> List[CheckResult]:
        """D1.2: 全站 .md 内部链接是否可解析。
        评分规则：满分 4 分，每个断裂链接扣 1 分，最低 0 分。
        处理：
          - 跳过 http 外部链接
          - 跳过代码块内容（防误报 shell 命令中的 .md 路径）
          - 跳过行内代码（防误报 `file.md` 引用）
        人工调整：如果发现有大量代码块中的 .md 路径被误判，可加强 cleaned 的正则。
        """
        total = 0
        broken = 0
        details = []
        link_pat = re.compile(r'\]\(([^)]+\.md)\)')

        for md_file in sorted(self.src_dir.rglob("*.md")):
            if "SUMMARY.md" in str(md_file) or "_book" in str(md_file):
                continue
            rel = md_file.relative_to(self.src_dir.parent)
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            # 首先处理 4 反引号围栏 ````lang...````
            # 这种围栏内部可能嵌套 3 反引号块，先用 4 反引号匹配移除
            # 如果不处理，3 反引号的正则会吃掉 4 反引号围栏的部分反引号，
            # 导致反引号配对偏移（`[text](file.md)` 等内容逃逸）
            cleaned = re.sub(r'````.*?````', '', content, flags=re.DOTALL)
            # 剔除 3 反引号代码块内容
            cleaned = re.sub(r'```.*?```', '', cleaned, flags=re.DOTALL)
            # 剔除行内代码（确保反引号总数为偶数后再配对）
            cleaned = re.sub(r'`[^`]+`', '', cleaned)

            for m in link_pat.finditer(cleaned):
                total += 1
                target = m.group(1)
                if target.startswith("http"):
                    continue
                abs_target = (md_file.parent / target).resolve()
                if not abs_target.exists():
                    broken += 1
                    details.append(f"{target} (位于 {rel})")

        # 评分：用比例制代替线性扣分，避免"一条断链就扣光"的激进策略
        # 公式: 4 × (有效链接 / 总链接)，有效 = 总 - 断
        # 之前用 max(0, 4 - broken) 会导致大量 shell 模板误报时得分为 0
        # 注意: 这里 includes 了 false positives，真实评分应人工核验后判断
        score = round(4 * (total - broken) / total, 1) if total > 0 else 0
        detail_str = f"内部链接：共 {total} 条，{broken} 条断裂"
        if broken > 0 and details:
            detail_str += " — " + "; ".join(details[:5])
            if len(details) > 5:
                detail_str += f" (+{len(details)-5} more)"
        return [CheckResult("D1", "D1.2", score, 4, detail_str)]

    def _check_brand_names(self) -> List[CheckResult]:
        """D1.4: 品牌名拼写检查（与 D7 有重叠但更严格）。
        评分规则：满分 4 分，每个错误扣 0.5 分，最低 0 分。
        检查的品牌：
          - OpenCode：误写成 Opencode / opencode / Open Code
          - oh-my-openagent：误写成 Oh-My-Openagent / OH-MY-OPENAGENT / oh_my_openagent
          - MCP：误写成 Mcp（仅在散文中，不检查代码标识符中的 Mcp）
          - mdBook：误写成 mdbook / Mdbook（仅在散文中）
        跳过规则：代码块、行内代码（反引号）、URL、shell 命令、
                  已知 CLI 命令/包名（mdbook-mermaid, mdbook-toc 等）、
                  已知代码标识符（createOpencode, McpServer 等）。
        人工调整：如果新增一个品牌名，在条件中加对应的正则即可。
        """
        errors = 0

        for md_file in sorted(self.src_dir.rglob("*.md")):
            if "_book" in str(md_file):
                continue
            rel = str(md_file.relative_to(self.src_dir.parent))
            with open(md_file, "r", encoding="utf-8") as f:
                lines = f.readlines()

            in_code_block = False
            for lineno, line in enumerate(lines, 1):
                stripped = line.rstrip()

                # 跳过代码块内容
                if stripped.startswith("```"):
                    in_code_block = not in_code_block
                    continue
                if in_code_block:
                    continue

                # 跳过 URL 行
                if re.search(r'https?://', stripped):
                    continue

                # 跳过纯 shell 命令
                if re.match(r'^\s*\$ ', stripped):
                    continue

                # 剔除行内代码（反引号包围的内容），避免误报 CLI 命令/包名
                cleaned = re.sub(r'`[^`]+`', '', stripped)
                # 如果剔除行内代码后该行已无可检查内容，跳过
                if not cleaned.strip():
                    continue

                # 跳过包含已知 mdbook CLI 包名的行（mdbook-mermaid, mdbook-toc 等）
                # 这些是 cargo 包名/CLI 工具名，不是品牌名拼写错误
                if re.search(r'mdbook-(?:mermaid|toc|pagetoc|linkcheck|katex|mathjax|plantuml)', cleaned):
                    continue

                # OpenCode：检测 "Opencode" 但排除 createOpencode / Opencode-DCP 等标识符
                if re.search(r'Opencode', cleaned):
                    if not re.search(r'createOpencode|Opencode-DCP|@opencode', cleaned):
                        errors += 1

                # Open Code（两个单词）：排除 "Open Code Review" 工具名
                if re.search(r'Open Code(?!\s+Review)', cleaned):
                    errors += 1

                # oh-my-openagent：检测错误的大小写和下划线变体
                if re.search(r'Oh-My-Openagent|OH-MY-OPENAGENT|oh_my_openagent', cleaned):
                    errors += 1

                # Mcp：仅在散文中（排除路径如 /Mcp、标识符如 McpServer）
                if re.search(r'(?<![a-zA-Z])Mcp(?![a-zA-Z])', cleaned):
                    if not re.search(r'/[Mm]cp|[Mm]cp[./]|McpServer', cleaned):
                        errors += 1

                # mdbook：检测小写或驼峰变体（仅在散文中）
                # 注意：mdbook CLI 命令（如 "mdbook serve"）和 cargo 包名（如 mdbook-mermaid）
                # 已在前面跳过；此处只检测散文中误用小写 mdbook 的情况
                if re.search(r'(?<![a-zA-Z])mdbook(?![a-zA-Z-])', cleaned):
                    errors += 1
                if re.search(r'(?<![a-zA-Z])Mdbook(?![a-zA-Z-])', cleaned):
                    errors += 1

        score = max(0, 4 - (errors * 0.5))
        return [CheckResult("D1", "D1.4", score, 4,
                            f"品牌名错误：{errors} 处")]
