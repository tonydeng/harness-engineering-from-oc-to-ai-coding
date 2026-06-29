#!/usr/bin/env python3
"""
Fix term first-occurrence format across book files (v2 - fixed bugs).

Requirement (from AGENTS.md):
  英文术语首次出现：用 **English（中文翻译）** 格式，例如 **Agent（智能体）**

Bugs fixed from v1:
1. Compound terms already formatted (e.g. **Context Engineering（上下文工程）**)
   should not cause sub-terms to be double-formatted
2. Terms inside inline code backticks should be skipped
3. Terms already inside **bold** should not be re-formatted
"""

import os
import re
import sys
import shutil

SRC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src')

# Terms to process: (exact_match, translation)
# Process LONGER compound terms FIRST to avoid partial matches
TERMS = [
    ('Agent Engineer', '智能体工程师'),
    ('Harness Engineering', '驾驭工程'),
    ('Loop Engineering', '循环工程'),
    ('Context Engineering', '上下文工程'),
    ('Agent', '智能体'),
    ('Skill', '技能'),
    ('Workflow', '工作流'),
    ('Plugin', '插件'),
    ('MCP', '模型上下文协议'),
    ('Context', '上下文'),
    ('Prompt', '提示词'),
]

SKIP_FILES = {'SUMMARY.md', 'book.toml'}


def find_term_in_line(line, term):
    """
    Find position of bare `term` in line, skipping:
    - inline code (backtick spans)
    - already-formatted patterns like **Term（...）**
    - already-bold patterns like **...Term...**
    Returns char index or -1.
    """
    idx = 0
    while True:
        pos = line.find(term, idx)
        if pos == -1:
            return -1

        # Check if inside inline code
        in_code = False
        for i, ch in enumerate(line):
            if ch == '`':
                if i < pos:
                    in_code = not in_code
                else:
                    break
        if in_code:
            idx = pos + 1
            continue

        # Check if already inside **Term（...）** (formatted)
        before_2 = line[max(0, pos-2):pos]
        after = line[pos+len(term):]
        if before_2 == '**' and after.startswith('（'):
            close = after.find('）**')
            if close != -1:
                idx = pos + 1
                continue

        # Check if already inside **...Term...** (bold, not formatted)
        # Find the last ** before the term position
        before_text = line[:pos]
        last_bold_open = before_text.rfind('**')
        if last_bold_open != -1:
            # Check it's not part of *** (which could be bold+italic)
            before_char = line[max(0, last_bold_open-1):last_bold_open]
            if before_char != '*':
                # Check if there's a matching ** after the term
                after_bold = line[pos+len(term):]
                closer_pos = after_bold.find('**')
                if closer_pos != -1:
                    # We're inside **...**, skip this occurrence
                    idx = pos + 1
                    continue

        # Check if term is part of a camelCase identifier
        # e.g., "onWorkflowStart" should not have "Workflow" formatted
        before_char = line[pos-1] if pos > 0 else ''
        after_char = line[pos+len(term)] if pos+len(term) < len(line) else ''
        if before_char.islower() or after_char.islower():
            # This is part of a camelCase identifier
            idx = pos + 1
            continue

        return pos

    return -1


def has_longer_formatted_term(line, term):
    """
    Check if term appears inside a longer formatted term.
    E.g., 'Context' inside '**Context Engineering（上下文工程）**'
    """
    for m in re.finditer(r'\*\*([^）]+)（[^）]+）\*\*', line):
        full_content = m.group(1)
        if term in full_content and term != full_content:
            return True
    return False


def process_file(filepath):
    """Process a single .md file, fixing first occurrences of terms."""
    basename = os.path.basename(filepath)
    if basename in SKIP_FILES:
        return 0

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    in_block = False
    terms_done = set()
    modified_count = 0
    new_lines = list(lines)

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_block = not in_block
            continue

        if in_block:
            continue

        if not stripped:
            continue

        for term, translation in TERMS:
            if term in terms_done:
                continue

            if term not in line:
                continue

            # Skip if term is inside a longer formatted term
            if has_longer_formatted_term(line, term):
                terms_done.add(term)
                continue

            # Skip if already has **Term（...）**
            pattern = r'\*\*' + re.escape(term) + r'（[^）]*）\*\*'
            if re.search(pattern, line):
                terms_done.add(term)
                continue

            # Find first bare occurrence
            pos = find_term_in_line(line, term)
            if pos == -1:
                continue

            replacement = f'**{term}（{translation}）**'
            new_line = line[:pos] + replacement + line[pos+len(term):]
            if new_line != line:
                new_lines[i] = new_line
                line = new_line
                modified_count += 1
                terms_done.add(term)

    if modified_count > 0:
        backup_path = filepath + '.bak'
        shutil.copy2(filepath, backup_path)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))

        return modified_count

    return 0


def main():
    total_changes = 0
    total_files = 0

    for root, dirs, files in os.walk(SRC_DIR):
        for f in sorted(files):
            if not f.endswith('.md'):
                continue
            if f in SKIP_FILES:
                continue

            filepath = os.path.join(root, f)
            relpath = os.path.relpath(filepath, os.path.dirname(SRC_DIR))

            changes = process_file(filepath)
            if changes > 0:
                total_files += 1
                total_changes += changes
                print(f"  ✓ {relpath} ({changes} changes)")
            else:
                print(f"  · {relpath} (no changes)")

    print(f"\n{'='*60}")
    print(f"Done! Modified {total_files} files with {total_changes} total changes.")


if __name__ == '__main__':
    main()
