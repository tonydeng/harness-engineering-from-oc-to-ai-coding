"""D8: 图表与可视化质量 — Mermaid 语法与配色合规（Chart quality）
子项：
  D8.1 Mermaid 语法正确性（满分 2 分）— 检查波浪号引用、方向声明
  D8.2 配色方案合规（满分 1.5 分）— 检查元素颜色是否符合规范
设计意图：确保所有 Mermaid 图表可正常渲染，并使用统一的品牌色。
配色规范：
  Agent = #4A90D9（蓝）
  Skill = #50C878（绿）
  Workflow = #FF9F43（橙）
  MCP = #A66CFF（紫）
"""
import re
from typing import List, Dict

from .base import BaseCheck, CheckResult


class D8MermaidCheck(BaseCheck):
    """检查 Mermaid 图表语法正确性和配色规范遵守情况。"""

    # 元素类型 → 规范颜色映射表（书籍品牌色）
    # 参考 AGENTS.md 中 Mermaid 图表颜色规范
    COLOR_MAP: Dict[str, str] = {
        "Agent": "#4A90D9",
        "Skill": "#50C878",
        "Workflow": "#FF9F43",
        "MCP": "#A66CFF",
    }

    def run(self) -> List[CheckResult]:
        results = []
        results.append(self._check_syntax())
        results.append(self._check_colors())
        return results

    def _check_syntax(self) -> CheckResult:
        """D8.1: Mermaid 语法正确性。
        评分规则：满分 2 分，有语法错误则得 0 分（all-or-nothing）。
        检查项：
          1. 波浪号引用：`[~path]` 必须写成 `["~path"]`（否则 Mermaid v9 解析失败）
          2. 方向声明：仅允许 TB/BT/LR/RL，支持 graph/flowchart 前缀形式
        注意：不验证 Mermaid 完整语法（过于复杂），只检查已知踩坑点。
        人工调整：如果要放宽语法检查，改为按错误比例扣分而非全扣。
        """
        total = 0
        errors = 0

        # 方向声明匹配：支持以下形式
        #   TB / BT / LR / RL        （纯方向声明，独占一行）
        #   graph TB / flowchart TB  （带图类型前缀，方向后无其他内容）
        # 错误形式：TD（应使用 TB）、其他未知方向
        # 注意：不匹配 T2B/B2T 等变体，因为容易与节点 ID（如 T2B[标签]）混淆
        direction_pat = re.compile(
            r'^(?:graph\s+|flowchart\s+)?(TB|BT|LR|RL|TD)\s*$',
            re.IGNORECASE
        )

        for md_file in sorted(self.src_dir.rglob("*.md")):
            if "_book" in str(md_file) or "SUMMARY.md" in str(md_file):
                continue
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            # 查找所有 Mermaid 代码块
            blocks = re.findall(r'```mermaid\n(.*?)```', content, re.DOTALL)
            for block in blocks:
                lines = block.strip().split("\n")
                for line in lines:
                    total += 1
                    # 检查未加引号的波浪号：Node[~path] 是错误的，必须 Node["~path"]
                    if re.search(r'\[~[a-zA-Z]', line) and not re.search(r'\["~', line):
                        errors += 1
                    # 检查方向声明：仅允许 TB/BT/LR/RL
                    # 支持 graph TB / flowchart TB 形式，TD 等同于 TB 但不在白名单中
                    m = direction_pat.match(line.strip())
                    if m and m.group(1).upper() not in ("TB", "BT", "LR", "RL"):
                        errors += 1

        syntax_score = 2 if errors == 0 else 0
        return CheckResult("D8", "D8.1", syntax_score, 2,
                           f"Mermaid 块：共 {total} 行，语法错误 {errors} 处")

    def _element_in_block(self, block: str, element: str) -> bool:
        """检查 Mermaid 块中是否真正使用了某元素类型（而非仅文本提及）。
        匹配 NodeLabel[Element] 或 classDef className 中的元素名，
        避免跨子图文本提及的误报。
        """
        # 在 Mermaid 节点标签中匹配：如 A[Agent] 或 B["Agent"]
        if re.search(rf'\["?{element}"?\]', block):
            return True
        # 在 classDef 定义中匹配
        if re.search(rf'classDef\s+\w*{element}\w*', block):
            return True
        # 在子图标题中匹配
        if re.search(rf'subgraph\s+.*{element}', block):
            return True
        return False

    def _has_correct_color(self, block: str, element: str, expected: str) -> bool:
        """检查块中元素是否使用了正确的规范色。
        优先检查 classDef/style 声明中的颜色赋值（精确匹配），
        若找不到则回退到检查块内是否包含该色值。
        """
        # 精确模式：查找 fill:{expected} 且附近有元素名
        exact = re.search(rf'fill:\s*{re.escape(expected)}.*?\n', block, re.IGNORECASE)
        if exact:
            # 确认该 fill 声明附近有元素名
            ctx = block[max(0, exact.start()-80):exact.end()+20]
            if element.lower() in ctx.lower():
                return True

        # 回退：块内出现规范色
        block_colors = set(re.findall(r'#[0-9A-Fa-f]{6}', block))
        if any(c.upper() == expected.upper() for c in block_colors):
            return True
        return False

    def _check_colors(self) -> CheckResult:
        """D8.2: 配色方案合规检查。
        评分规则：得分 = 1.5 * (正确使用规范色的元素数 / 总元素数)。
        检查：每个 Mermaid 块中，如果出现了 Agent/Skill/Workflow/MCP 等元素，
        其使用的颜色是否符合 COLOR_MAP 规范。
        改进 v2：使用 _element_in_block() 精确匹配节点标签而非全文扫描，
        用 _has_correct_color() 优先检查 fill: 声明而非仅色值存在性。
        局限性：
          - 仍无法解析完整的 Mermaid AST（跨子图边连接仍有少量误报可能）
          - 回退模式（fallback color check）可能引入略高计数
        人工调整：如需更高精度，需引入 Mermaid 解析器。
        """
        correct = 0
        total = 0

        for md_file in sorted(self.src_dir.rglob("*.md")):
            if "_book" in str(md_file) or "SUMMARY.md" in str(md_file):
                continue
            with open(md_file, "r", encoding="utf-8") as f:
                content = f.read()

            blocks = re.findall(r'```mermaid\n(.*?)```', content, re.DOTALL)
            for block in blocks:
                for element, expected in self.COLOR_MAP.items():
                    # 只有在块中真正使用了该元素类型才检查
                    if not self._element_in_block(block, element):
                        continue
                    total += 1
                    if self._has_correct_color(block, element, expected):
                        correct += 1

        score = round(1.5 * correct / total, 1) if total else 0
        return CheckResult("D8", "D8.2", min(score, 1.5), 1.5,
                           f"配色合规：{correct}/{total} 正确")
