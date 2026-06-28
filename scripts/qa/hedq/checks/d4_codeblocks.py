"""D4: 代码块格式与注释覆盖率（Code block format compliance）
子项：
  D4.1 代码块 language:path 注释覆盖率（满分 4 分）
规范要求：非白名单类型的代码块必须有 language:path 注释（如 python:src/example.py）。
这确保读者知道代码块的上下文和作用。
注意：此维度原名"实操可执行性"，但自动化检测仅覆盖代码块 path 注释格式
（而非代码示例是否可运行），故名称改为"代码块格式"。完整实操检测需人工介入。
白名单类型（无需 path）：mermaid（图表）、bash/sh/shell/console（终端命令）、
text/json/csv/toml/yaml/yml（数据配置片段）、markdown（展示 markdown 语法本身）、
dockerfile（路径通常隐含）、html/css（原型展示）。
"""
import re
from typing import List

from .base import BaseCheck, CheckResult


class D4CodeblocksCheck(BaseCheck):
    """检查非平凡代码块是否包含 language:path 注释。"""

    # 不需要 path 注释的代码块类型白名单
    # mermaid: 图表（路径无意义）
    # bash/sh/shell/console: 终端交互命令
    # text/json/csv/toml/yaml/yml: 配置片段（不需要文件路径上下文）
    # markdown: 展示 markdown 语法本身
    # dockerfile: 路径通常从上下文可推断
    # html/css: 原型展示类
    # 人工调整：如果有其他类型不需要 path，在此集合添加即可
    NO_PATH_ALLOWED = {
        "mermaid", "bash", "sh", "shell", "console",
        "text", "json", "csv", "toml", "yaml", "yml",
        "markdown", "dockerfile", "html", "css",
    }

    def run(self) -> List[CheckResult]:
        total = 0
        missing = 0
        missing_details: List[str] = []

        for md_file in sorted(self.src_dir.rglob("*.md")):
            if "SUMMARY.md" in str(md_file) or "_book" in str(md_file):
                continue
            rel = str(md_file.relative_to(self.src_dir.parent))
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            # 查找所有代码块起始行，如 ```python, ```mermaid, ```python:src/main.py
            for m in re.finditer(r'^```(\S*)', content, re.MULTILINE):
                lang = m.group(1)
                # 跳过空语言声明和纯 ``` 结束标记
                if not lang or lang == "``":
                    continue
                if lang.strip() == "" or lang == "\n":
                    continue

                total += 1
                # 提取冒号前的语言名（如 python:src/main.py → python）
                base_lang = lang.split(":")[0].lower()

                # 白名单类型的代码块不需要 path 注释
                if base_lang in self.NO_PATH_ALLOWED:
                    continue

                # 检查是否包含 :path 注释
                if ":" not in lang:
                    missing += 1
                    lineno = content[:m.start()].count("\n") + 1
                    missing_details.append(f"{rel}:L{lineno}（{base_lang}）")

        # 评分：每个缺少 path 的代码块扣 0.3 分，最低 0 分
        # 满分 4 分意味着允许约 13 个代码块缺少 path（4/0.3）
        # 人工调整：如果希望更严格，将扣分改为 0.5/个
        score = max(0, 4 - (missing * 0.3))
        detail = f"代码块：共 {total} 个，{missing} 个缺少 :path 注释"
        if missing_details:
            detail += " — " + "; ".join(missing_details[:8])
            if len(missing_details) > 8:
                detail += f" （+{len(missing_details)-8} more）"
        return [CheckResult("D4", "D4.1", score, 4, detail)]
