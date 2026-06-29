"""D4: 代码块格式与注释覆盖率（Code block format compliance）
子项：
  D4.1 代码块 language:path 注释覆盖率（满分 4 分）

v2.0 三层检查体系（上下文感知）：
  Layer 1 — 缺 :path 检测（原核心检查，-0.3/个）：非白名单代码块必须有 language:path 注释
  Layer 2 — 自引用检测（仅报告，不计扣分）：:path 指向代码块所在文件自身（技术书籍中属合理设计约束）
  Layer 3 — 白名单约定路径报告（仅报告，不计扣分）：统计全书 :terminal 等设计约定路径数量
  
  设计理念：本检查面向"技术书籍"场景。全书大量使用 :terminal、:opencode.json 等
  设计约定/示意路径，它们不属于质量缺陷。D4.1 聚焦于：
  ① 非白名单块真正缺失 :path（最严重，-0.3/个）
  ② 统计并报告自引用、约定路径、示意路径（提供可见性但不影响评分）

规范要求：非白名单类型的代码块必须有 language:path 注释（如 python:src/example.py）。
白名单类型（无需 path）：mermaid（图表）、bash/sh/shell/console（终端命令）、
text/json/csv/toml/yaml/yml（数据配置片段）、markdown（展示 markdown 语法本身）、
dockerfile（路径通常隐含）、html/css（原型展示）。
"""
import re
from pathlib import Path
from typing import List

from .base import BaseCheck, CheckResult


class D4CodeblocksCheck(BaseCheck):
    """检查代码块的 :path 注释格式、自引用、约定路径报告。"""

    # 不需要 path 注释的代码块类型白名单
    NO_PATH_ALLOWED = {
        "mermaid", "bash", "sh", "shell", "console",
        "text", "json", "csv", "toml", "yaml", "yml",
        "markdown", "dockerfile", "html", "css",
    }

    # 全书统一的设计约定路径（风格约定而非真实文件路径）
    DESIGN_CONVENTIONS = {
        "terminal", "terminal-session", "terminal-session.md",
    }

    def run(self) -> List[CheckResult]:
        total = 0
        missing = 0          # 非白名单块缺 :path（最严重）
        self_ref = 0          # 非白名单块自引用路径（冗余信息）
        convention_hits = 0   # 使用设计约定路径的块数（仅统计/报告）
        white_pedantic = 0    # 白名单块带有非约定路径（如 json:opencode.json，仅报告）

        missing_details: List[str] = []
        self_ref_details: List[str] = []
        white_pedantic_details: List[str] = []

        for md_file in sorted(self.src_dir.rglob("*.md")):
            if "SUMMARY.md" in str(md_file) or "_book" in str(md_file):
                continue
            rel = str(md_file.relative_to(self.src_dir.parent))
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            # 查找所有代码块起始行
            for m in re.finditer(r'^```(\S*)', content, re.MULTILINE):
                lang = m.group(1)
                if not lang or lang == "``":
                    continue
                if lang.strip() == "" or lang == "\n":
                    continue

                total += 1
                base_lang = lang.split(":")[0].lower()
                lineno = content[:m.start()].count("\n") + 1

                has_path = ":" in lang
                path_part = ""
                if has_path:
                    path_part = lang.split(":", 1)[1]

                # --- Layer 1: 缺 :path 检测（非白名单块）---
                if base_lang in self.NO_PATH_ALLOWED:
                    # 白名单块：统计路径使用情况（不计扣分）
                    if has_path:
                        if path_part in self.DESIGN_CONVENTIONS:
                            convention_hits += 1
                        else:
                            white_pedantic += 1
                            white_pedantic_details.append(
                                f"{rel}:L{lineno}（{base_lang}:{path_part}）"
                            )
                    continue

                # 非白名单块：检查是否缺 :path
                if not has_path:
                    missing += 1
                    missing_details.append(f"{rel}:L{lineno}（{base_lang}）")
                    continue

                # --- Layer 2: 自引用检测 ---
                # 如果路径以 src/ 开头，说明是相对项目根的路径
                # 检查是否指向代码块所在文件自身
                if not path_part or path_part in self.DESIGN_CONVENTIONS:
                    continue

                # 尝试从 src/ 父目录（项目根）解析路径
                candidate = self.src_dir.parent / path_part
                if candidate.exists() and candidate.resolve() == md_file.resolve():
                    self_ref += 1
                    self_ref_details.append(
                        f"{rel}:L{lineno}（{path_part}）"
                    )

        # --- 评分计算 ---
        # 缺 :path: -0.3/个（原核心检查，最严重）
        # 自引用：不计扣分（技术书籍中自引用是合理的设计约束，使代码块可独立复制使用）
        # 白名单约定路径与示意路径：不计扣分，仅在报告中呈现
        deductions = missing * 0.3
        score = max(0, round(4.0 - deductions, 1))

        # --- 构建详情字符串 ---
        parts = [f"代码块：共 {total} 个"]
        if missing:
            parts.append(f"{missing} 个缺 :path（-{missing*0.3:.1f}）")
        if self_ref:
            parts.append(f"{self_ref} 个自引用（仅报告）")
        if convention_hits:
            parts.append(f"{convention_hits} 个约定路径(:terminal)")
        if white_pedantic:
            parts.append(f"{white_pedantic} 个白名单示意路径（仅报告）")

        detail = "，".join(parts)

        # 添加各类型示例
        examples = []
        for label, items in [
            ("缺:path", missing_details),
            ("自引用", self_ref_details),
            ("白名单示意路径", white_pedantic_details),
        ]:
            if items:
                short = items[:4]
                examples.append(f"{label}: " + "; ".join(short))
                if len(items) > 4:
                    examples[-1] += f"（+{len(items)-4} more）"

        if examples:
            detail += " — " + " | ".join(examples)

        return [CheckResult("D4", "D4.1", score, 4, detail)]
