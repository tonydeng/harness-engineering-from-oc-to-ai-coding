"""D8: 图表与可视化质量 — Mermaid 语法与配色合规（Chart quality）
子项：
  D8.1 Mermaid 语法正确性（满分 2 分）— 已知踩坑点静态检查
  D8.2 配色方案合规（满分 1.5 分）— 元素颜色是否符合品牌规范
  D8.3 结构健全性（未评分）— 渲染质量的静态代理指标（仅供参考）
设计意图：确保所有 Mermaid 图表可正常渲染，并使用统一的品牌色。
配色规范：
  Agent = #4A90D9（蓝）
  Skill = #50C878（绿）
  Workflow = #FF9F43（橙）
  MCP = #A66CFF（紫）

v3 增强（2026-06-29）：
  - D8.1 新增：子图平衡检查、空节点检测、缩进敏感类型检查
  - D8.1 新增：类型推断 + 类型特定前置检查
  - D8.3 新增：结构健全性信息提示（不影响评分）
"""
import re
from collections import Counter
from typing import List, Dict, Tuple

from .base import BaseCheck, CheckResult


# ── 类型识别常量 ──────────────────────────────────────────────
TYPE_FLOWCHART = "flowchart"
TYPE_SEQUENCE  = "sequenceDiagram"
TYPE_TIMELINE  = "timeline"
TYPE_MINDMAP   = "mindmap"
TYPE_STATE     = "stateDiagram"
TYPE_GANTT     = "gantt"
TYPE_PIE       = "pie"
TYPE_QUADRANT  = "quadrantChart"
TYPE_CLASS     = "classDiagram"

# 缩进敏感的图表类型
INDENT_SENSITIVE_TYPES = {TYPE_MINDMAP, TYPE_TIMELINE}

# 可能包含子图的结构
SUBGRAPH_TYPES = {TYPE_FLOWCHART}

# ── 帮助函数 ──────────────────────────────────────────────────

def _infer_type(first_line: str) -> str:
    """从 Mermaid 块第一行推断图表类型。
    处理：type declaration（graph/flowchart/mindmap 等）、
    %%{init: ...}%% 前缀的包装语法。
    """
    fl = first_line.strip().lower()
    # 处理 %%{init: ...}%% 包装语法：跳过 init 行，取下一条
    # 注意：此处只处理单行 init，实际 _collect_mermaid_blocks 中
    # 会将整个块拆开，此处只是块内首行判断
    if fl.startswith("%%{init:"):
        return "init-wrapped"

    for t in [TYPE_FLOWCHART, TYPE_SEQUENCE, TYPE_MINDMAP,
              TYPE_STATE, TYPE_GANTT, TYPE_PIE, TYPE_QUADRANT]:
        if fl.startswith(t.lower()):
            return t
    # timeline 是单关键词
    if fl in ("timeline", "timeline:"):
        return TYPE_TIMELINE
    # graph → 同 flowchart
    if fl.startswith("graph"):
        return TYPE_FLOWCHART
    # sequenceDiagram-v2 → same as sequenceDiagram
    if fl.startswith("sequencediagram"):
        return TYPE_SEQUENCE
    # stateDiagram-v2 → same as stateDiagram  
    if fl.startswith("statediagram"):
        return TYPE_STATE
    return "unknown"


def _is_flowchart_decl(line: str) -> bool:
    """判断是否为合法的方向声明行。"""
    m = re.match(
        r'^(?:graph\s+|flowchart\s+)?(TB|BT|LR|RL|TD)\s*$', line.strip(), re.IGNORECASE
    )
    if m:
        return True
    return False


def _collect_mermaid_blocks(src_dir) -> List[dict]:
    """收集全书所有 Mermaid 代码块，返回结构化列表。"""
    blocks = []
    mblock_re = re.compile(r'```mermaid\n(.*?)```', re.DOTALL)
    for md_file in sorted(src_dir.rglob("*.md")):
        if "_book" in str(md_file) or "SUMMARY.md" in str(md_file):
            continue
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
        for b in mblock_re.findall(content):
            b = b.strip()
            lines = b.split("\n")
            first_line = lines[0] if lines else ""

            # 处理 %%{init: ...}%% 包裹：类型声明可能在第 2 行
            type_line = first_line
            if _infer_type(first_line) == "init-wrapped":
                for line in lines[1:]:
                    ls = line.strip()
                    if not ls or ls.startswith("%%{") or ls == "%%":
                        continue
                    type_line = line
                    break

            infer_type = _infer_type(type_line)
            blocks.append({
                "file": str(md_file.relative_to(src_dir)),
                "content": b,
                "lines": lines,
                "first_line": first_line,
                "type": infer_type,
            })
    return blocks


# ── D8.1 增强检查 ────────────────────────────────────────────

def _check_tilde_quoting(lines: List[str]) -> int:
    """检查波浪号未加引号：Node[~path] 应为 Node["~path"]。"""
    count = 0
    for line in lines:
        if re.search(r'\[~[a-zA-Z]', line) and not re.search(r'\["~', line):
            count += 1
    return count


def _check_direction(lines: List[str]) -> int:
    """检查方向声明：TB/BT/LR/RL 合法，TD 非法。"""
    count = 0
    for line in lines:
        m = re.match(
            r'^(?:graph\s+|flowchart\s+)?(TB|BT|LR|RL|TD)\s*$',
            line.strip(), re.IGNORECASE
        )
        if m and m.group(1).upper() == "TD":
            count += 1
    return count


def _check_subgraph_balance(block: dict) -> int:
    """检查子图平衡：每个 `subgraph` 应有对应的 `end`。
    只对可能包含子图的类型做检查。返回子图不均衡的块数（0 或 1）。
    """
    if block["type"] not in SUBGRAPH_TYPES:
        return 0
    content = block["content"]
    subgraph_count = len(re.findall(r'^subgraph\b', content, re.MULTILINE))
    if subgraph_count == 0:
        return 0
    # 统计顶层的 end 数量（在 subgraph 外也可能有 end）
    end_count = len(re.findall(r'^end\s*$', content, re.MULTILINE))
    # 非子图场景下的 end 可能是 stateDiagram 的关键词，
    # 但既然已限定 SUBGRAPH_TYPES 为 flowchart，端到端应相等
    if subgraph_count != end_count:
        return 1
    return 0


def _check_empty_nodes(lines: List[str]) -> int:
    """检查空节点标签：Node[] 没有标签内容。"""
    # 匹配 A[] 或 A[""] 或 A[""] 等空标签
    count = 0
    for line in lines:
        if re.search(r'\b\w+\[\s*\]', line):
            count += 1
        if re.search(r'\b\w+\[\s*""\s*\]', line):
            count += 1
    return count


def _check_mindmap_indent(lines: List[str]) -> int:
    """检查 mindmap 缩进一致性（缩进敏感类型）。
    mindmap 是缩进敏感的：同层节点必须等深。
    此函数为 warning 级别——奇缩进可能导致渲染层级偏移，
    但不会直接导致解析失败。
    非 mindmap 类型返回 0。
    """
    if not lines:
        return 0
    # 检查类型行（第 1 行或 %%{init: 后的第 1 个可用行）
    type_line = lines[0].strip().lower()
    i = 0
    while type_line.startswith("%%{") and i < len(lines) - 1:
        i += 1
        type_line = lines[i].strip().lower()
    if "mindmap" not in type_line:
        return 0

    # 跳过所有声明和注释行，分析节点行缩进
    indent_levels = set()
    for line in lines[i+1:]:
        stripped = line.strip()
        if not stripped or stripped.startswith("%%"):
            continue
        indent = len(line) - len(stripped)
        indent_levels.add(indent)

    if not indent_levels:
        return 0

    # 检查：最低缩进应为偶数（2 的倍数，mindmap 标准）
    min_indent = min(indent_levels)
    if min_indent % 2 != 0:
        return 1

    # 检查：所有缩进间的差值应为偶数（保持 2 的倍数间隔）
    for level in indent_levels:
        if (level - min_indent) % 2 != 0:
            return 1

    return 0


def _check_unquoted_subgraph_label(lines: List[str]) -> int:
    """检查 subgraph 标签是否未引用包含特殊字符。
    中文括号 (（）) 在没有引号的 subgraph 标签中会导致 Mermaid 词法解析失败。
    有效的写法：
      subgraph "规划阶段（Prometheus）"   ✅ 双引号
      subgraph 阶段["阶段（Alias）"]      ✅ 方括号别名（特殊字符在 [] 内是安全的）
    无效的写法：
      subgraph 规划阶段（Prometheus）     ❌ 中文括号导致词法错误
    """
    count = 0
    for line in lines:
        if not line.strip():
            continue
        m = re.match(r'^\s*subgraph\s+(.*)$', line)
        if not m:
            continue
        rest = m.group(1).strip()
        # 双引号开头 → 已引用，安全
        if rest.startswith('"'):
            continue
        # 方括号开头 → 别名引用，安全
        if rest.startswith('['):
            continue
        # 提取引号/方括号前的标签文本（subgraph 标签名部分）
        # 去掉末尾的 [...] 或 {...} 别名
        label_only = re.sub(r'\s*[\[{].*$', '', rest).strip()
        # 检查标签文本中是否包含中文括号
        if '（' in label_only or '）' in label_only:
            count += 1
    return count


def _check_bracket_balance(content: str, chart_type: str) -> int:
    """检查方括号/圆括号基本平衡（只针对 flowchart 类）。"""
    if chart_type not in {TYPE_FLOWCHART, TYPE_CLASS, TYPE_QUADRANT}:
        return 0
    errors = 0
    # 统计所有方括号（排除 markdown 链接）
    if content.count("[") != content.count("]"):
        errors += 1
    if content.count("(") != content.count(")"):
        errors += 1
    if content.count("{") != content.count("}"):
        errors += 1
    return 1 if errors > 0 else 0


def get_d81_syntax_score(blocks: List[dict]) -> Tuple[float, List[str]]:
    """D8.1 评分：满分 2.0，按受影响块数比例扣分。
    每发现一个语法问题，该块计为"异常块"。
    score = 2.0 * (无异常块数 / 总块数)。
    返回 (score, issues_list)。
    """
    issues = []
    total_blocks = len(blocks)
    if total_blocks == 0:
        return 2.0, ["无 Mermaid 块"]

    bad_blocks = set()  # 用 set 去重：同一块有多个问题也只计一次
    total_tilde = 0
    total_direction = 0
    total_subgraph = 0
    total_empty = 0
    total_mindmap = 0
    total_bracket = 0
    total_subgraph_label = 0

    for idx, block in enumerate(blocks):
        lines = block["lines"]
        ct = block["type"]
        if _check_tilde_quoting(lines):
            bad_blocks.add(idx); total_tilde += 1
        if _check_direction(lines):
            bad_blocks.add(idx); total_direction += 1
        if _check_subgraph_balance(block):
            bad_blocks.add(idx); total_subgraph += 1
        if _check_empty_nodes(lines):
            bad_blocks.add(idx); total_empty += 1
        if _check_mindmap_indent(lines):
            bad_blocks.add(idx); total_mindmap += 1
        if _check_bracket_balance(block["content"], ct):
            bad_blocks.add(idx); total_bracket += 1
        if _check_unquoted_subgraph_label(lines):
            bad_blocks.add(idx); total_subgraph_label += 1

    if total_tilde:
        issues.append(f"波浪号引用错误 {total_tilde} 处")
    if total_direction:
        issues.append(f"方向声明问题 {total_direction} 处")
    if total_subgraph:
        issues.append(f"子图不平衡 {total_subgraph} 个块")
    if total_empty:
        issues.append(f"空节点标签 {total_empty} 处")
    if total_mindmap:
        issues.append(f"缩进问题 {total_mindmap} 个块")
    if total_bracket:
        issues.append(f"括号不平衡 {total_bracket} 个块")
    if total_subgraph_label:
        issues.append(f"subgraph 标签未引用特殊字符 {total_subgraph_label} 个块")

    num_bad = len(bad_blocks)
    score = round(2.0 * (total_blocks - num_bad) / total_blocks, 2) if total_blocks else 0.0
    return score, issues


# ── D8.2 配色检查（原版增强） ──────────────────────────────────

COLOR_MAP: Dict[str, str] = {
    "Agent": "#4A90D9",
    "Skill": "#50C878",
    "Workflow": "#FF9F43",
    "MCP": "#A66CFF",
}


def _element_in_block(block: str, element: str) -> bool:
    """检查 Mermaid 块中是否真正使用了某元素类型。"""
    if re.search(rf'\["?{element}"?\]', block):
        return True
    if re.search(rf'classDef\s+\w*{element}\w*', block):
        return True
    if re.search(rf'subgraph\s+.*{element}', block):
        return True
    return False


def _has_correct_color(block: str, element: str, expected: str) -> bool:
    """检查块中元素是否使用了正确的规范色。"""
    exact = re.search(rf'fill:\s*{re.escape(expected)}.*?\n', block, re.IGNORECASE)
    if exact:
        ctx = block[max(0, exact.start()-80):exact.end()+20]
        if element.lower() in ctx.lower():
            return True
    block_colors = set(re.findall(r'#[0-9A-Fa-f]{6}', block))
    if any(c.upper() == expected.upper() for c in block_colors):
        return True
    return False


def get_d82_color_score(src_dir) -> Tuple[float, str]:
    """D8.2 配色合规评分。满分 1.5，按比例扣分。"""
    correct = 0
    total = 0
    for md_file in sorted(src_dir.rglob("*.md")):
        if "_book" in str(md_file) or "SUMMARY.md" in str(md_file):
            continue
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
        blocks = re.findall(r'```mermaid\n(.*?)```', content, re.DOTALL)
        for block in blocks:
            for element, expected in COLOR_MAP.items():
                if not _element_in_block(block, element):
                    continue
                total += 1
                if _has_correct_color(block, element, expected):
                    correct += 1
    score = round(1.5 * correct / total, 1) if total else 0
    detail = f"配色合规：{correct}/{total} 正确" if total else "无色元素需要检查"
    return min(score, 1.5), detail


# ── D8.3 结构健全性（信息提示，不影响评分） ──────────────────

def get_d83_structural(blocks: List[dict]) -> str:
    """D8.3 静态结构代理指标（信息提示，不评分）。
    当 mermaid-cli 不可用时，作为渲染质量的粗略代理。
    报告：
      - 总块数 / 总行数 / 平均行数
      - 类型分布
      - 节点引用异常（边引用的节点不存在）
      - 注释占比
      - 最大/最小/平均节点数
    """
    if not blocks:
        return "无 Mermaid 块"

    type_counter: Counter = Counter()
    total_lines = 0
    total_comments = 0
    node_ref_issues = 0
    block_densities = []

    for block in blocks:
        ct = block["type"]
        type_counter[ct] += 1
        lines = block["lines"]
        total_lines += len(lines)
        comment_lines = sum(1 for l in lines if l.strip().startswith("%%"))
        total_comments += comment_lines
        block_densities.append((len(lines), ct))

        # 节点引用检查：查找边定义中箭头右端的节点 ID，
        # 检查该 ID 在块内是否有对应声明
        content = block["content"]
        # 声明节点：Node[Label] 或 Node("Label") 或 Node{Label}
        declared = set()
        for m in re.finditer(r'^([A-Za-z_]\w*)\s*[\[({]', content, re.MULTILINE):
            declared.add(m.group(1))
        # 也收集子图标题
        for m in re.finditer(r'subgraph\s+(\w+)', content):
            declared.add(m.group(1))

        # 箭头右侧引用的节点
        referenced = set()
        for m in re.finditer(r'-->\s*([A-Za-z_]\w*)', content):
            referenced.add(m.group(1))
        for m in re.finditer(r'-->\s*\w+\[([A-Za-z_]\w*)\]', content):
            referenced.add(m.group(1))
        # 双向箭头左侧
        for m in re.finditer(r'([A-Za-z_]\w*)\s*<-->', content):
            referenced.add(m.group(1))

        # 排除标准关键词
        keywords = {"TB", "BT", "LR", "RL", "TD", "end", "subgraph",
                    "direction", "yes", "no"}
        undeclared = referenced - declared - keywords
        if undeclared:
            node_ref_issues += 1

    # 密度报告
    dens_report = f"总数 {len(blocks)} 块 / {total_lines} 行 / 平均 {total_lines//max(1,len(blocks))} 行/块"
    type_report = " | ".join(f"{t}: {c}" for t, c in type_counter.most_common())
    comment_ratio = f"注释 {total_comments} 行 / {total_lines} 行 ({total_comments*100//max(1,total_lines)}%)"

    # 节点引用异常
    ref_report = f"潜在引用异常 {node_ref_issues} 个块" if node_ref_issues else "节点引用正常"

    return f"{dens_report} | {type_report} | {comment_ratio} | {ref_report}"


# ── 主入口 ────────────────────────────────────────────────────

class D8MermaidCheck(BaseCheck):
    """检查 Mermaid 图表语法正确性和配色规范遵守情况。"""

    def run(self) -> List[CheckResult]:
        results = []

        # D8.1
        blocks = _collect_mermaid_blocks(self.src_dir)
        d81_score, d81_issues = get_d81_syntax_score(blocks)
        d81_detail = f"语法检查：{'全部通过' if not d81_issues else '; '.join(d81_issues)}（{len(blocks)} 个块）"
        results.append(CheckResult("D8", "D8.1", d81_score, 2.0, d81_detail))

        # D8.2
        d82_score, d82_detail = get_d82_color_score(self.src_dir)
        results.append(CheckResult("D8", "D8.2", d82_score, 1.5, d82_detail))

        # D8.3（信息提示，max_score=0 表示不参与评分）
        d83_detail = get_d83_structural(blocks)
        results.append(CheckResult("D8", "D8.3", 0, 0, d83_detail))

        return results
