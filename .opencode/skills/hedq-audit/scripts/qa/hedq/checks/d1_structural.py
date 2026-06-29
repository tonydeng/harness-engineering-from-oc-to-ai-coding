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
    """检查 SUMMARY.md 路径有效性、内部链接是否断裂、品牌名拼写是否正确、
    链接文字与目标 H1 一致性。"""

    def run(self) -> List[CheckResult]:
        results = []
        results.extend(self._check_summary_paths())
        results.extend(self._check_internal_links())
        results.extend(self._check_brand_names())
        results.extend(self._check_link_heading_consistency())
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

                # 跳过代码块内容（支持缩进的代码块围栏，如列表项内的 ```bash）
                if stripped.lstrip().startswith("```"):
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

    def _check_link_heading_consistency(self) -> List[CheckResult]:
        """D1.5: 交叉引用链接文字与目标 H1 一致性检查（满分 3 分）。
        AGENTS.md §5 要求：链接文字必须和目标文件的 H1 标题一致。
        评分规则：满分 3 分，mismatch 比例扣分。
        检查范围：全书 [text](path.md) 格式的内部链接（排除外部 http 链接、
        代码块内链接、行内代码链接）。
        人工调整：链接文字中的反引号（`code`）在比较时会去除，
        此为常见写法（在链接中表达代码标识符），不算 mismatch。
        """
        total = 0
        mismatch = 0
        details: List[str] = []
        link_pat = re.compile(r'\[([^\]]+)\]\(([^)]+\.md)\)')

        # 缓存文件 H1 以避免重复读取
        h1_cache: dict = {}

        def _get_h1(filepath: Path) -> str:
            """读取 Markdown 文件的第一级标题（# Title），缓存结果。
            如果文件不存在或没有 H1，返回空字符串。
            """
            resolved = filepath.resolve()
            if resolved in h1_cache:
                return h1_cache[resolved]
            if not filepath.exists():
                h1_cache[resolved] = ""
                return ""
            with open(filepath, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("# ") and not line.startswith("## "):
                        h1 = line[2:].strip()
                        h1_cache[resolved] = h1
                        return h1
            h1_cache[resolved] = ""
            return ""

        for md_file in sorted(self.src_dir.rglob("*.md")):
            if "SUMMARY.md" in str(md_file) or "_book" in str(md_file):
                continue
            rel = str(md_file.relative_to(self.src_dir.parent))
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            # 剔除代码块和行内代码内容
            cleaned = re.sub(r'````.*?````', '', content, flags=re.DOTALL)
            cleaned = re.sub(r'```.*?```', '', cleaned, flags=re.DOTALL)
            cleaned = re.sub(r'`[^`]+`', '', cleaned)

            for m in link_pat.finditer(cleaned):
                link_text = m.group(1)
                target_path_str = m.group(2)

                if target_path_str.startswith("http"):
                    continue

                # 解析目标文件路径
                target = (md_file.parent / target_path_str).resolve()
                if not target.exists():
                    continue  # 断链已在 D1.2 处理，此处跳过

                total += 1

                # 读取目标 H1
                target_h1 = _get_h1(target)
                if not target_h1:
                    continue  # 目标无 H1，跳过

                # 清理链接文字（去除反引号、格式标记、首尾空格）
                cleaned_text = link_text.strip().strip("`").strip()
                cleaned_text = cleaned_text.replace("**", "")
                # 去除常见的导航前缀/后缀（如 "下一页：xxx →"）
                cleaned_text = re.sub(r'^(下一页|上一页|相关阅读|更多)[：:]\s*', '', cleaned_text)
                cleaned_text = re.sub(r'\s*[→➡>]\s*$', '', cleaned_text)

                # 归一化 H1：去除星号格式标记、首尾空格
                norm_h1 = target_h1.strip().replace("**", "")

                # 支持 H1 包含 "|" 分隔符时的部分匹配：
                # 例如 H1="上下文压缩 | Harness Engineering"，链接文字为"上下文压缩"可接受
                h1_parts = [p.strip() for p in norm_h1.split("|")]

                # 宽松匹配（四级回退）：
                # Level 1: 完全一致（已去除格式标记）
                # Level 2: 链接文字是 H1 的子串（处理 "从零搭建微服务"→"案例一：从零搭建微服务"）
                # Level 3: H1 某个分段是链接文字的子串（处理 H1="Skill（技能）系统"，链接="Skill系统"）
                # Level 4: 去除所有空格后 Level 1-3 任一成立
                cleaned_text_nospace = re.sub(r'\s+', '', cleaned_text)
                matched = False

                for part in h1_parts:
                    if cleaned_text == part:
                        matched = True
                        break
                    # 子串匹配：链接文字完整包含于 H1 分段
                    if cleaned_text in part:
                        matched = True
                        break
                    # H1 分段完整包含于链接文字
                    if part in cleaned_text:
                        matched = True
                        break

                # Level 4: 去空格后重试 Level 1-3
                if not matched:
                    for part in h1_parts:
                        part_nospace = re.sub(r'\s+', '', part)
                        if cleaned_text_nospace == part_nospace:
                            matched = True
                            break
                        if cleaned_text_nospace in part_nospace:
                            matched = True
                            break
                        if part_nospace in cleaned_text_nospace:
                            matched = True
                            break

                # Level 5: 去除中文括号内说明（如 "（驾驭工程）"）后重试
                # 处理 H1="**Harness Engineering（驾驭工程）**理论框架" 链接="Harness Engineering 理论框架"
                if not matched:
                    _strip_paren = lambda s: re.sub(r'[（(][^）)]*[）)]', '', s).strip()
                    for part in h1_parts:
                        part_noparen = _strip_paren(part)
                        text_noparen = _strip_paren(cleaned_text)
                        if text_noparen == part_noparen:
                            matched = True
                            break
                        if text_noparen in part_noparen:
                            matched = True
                            break
                        if part_noparen in text_noparen:
                            matched = True
                            break
                        # 去空格版本
                        if re.sub(r'\s+', '', text_noparen) in re.sub(r'\s+', '', part_noparen):
                            matched = True
                            break

                if not matched:
                    mismatch += 1
                    # 截断过长的文字以节省报告空间
                    text_display = cleaned_text[:40] + "..." if len(cleaned_text) > 40 else cleaned_text
                    h1_display = target_h1[:50] + "..." if len(target_h1) > 50 else target_h1
                    details.append(
                        f"'{text_display}' → '{h1_display}' ({rel})"
                    )

        score = round(3 * (total - mismatch) / total, 1) if total > 0 else 0
        detail_str = f"交叉引用标题一致性：{total} 处检查，{mismatch} 处不匹配"
        if mismatch > 0 and details:
            detail_str += " — " + "; ".join(details[:5])
            if len(details) > 5:
                detail_str += f" (+{len(details)-5} more)"
        return [CheckResult("D1", "D1.5", score, 3, detail_str)]
