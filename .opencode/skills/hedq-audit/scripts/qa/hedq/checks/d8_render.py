"""D8.3 Render Validation — Batch render all Mermaid blocks via mmdc

Usage:
    python d8_render.py [--output DIR] [--parallel N] [--timeout N]
    python d8_render.py --files path/to/file1.md path/to/file2.md
    python d8_render.py --files-changed  # auto-detect from git diff HEAD~1

Output:
    - Renders each block to SVG in output dir
    - Prints summary: pass/fail/skip per block
    - Exit code: 0 if all pass (or --no-fail), 1 if any fail
"""
import re, os, sys, json, tempfile, subprocess, time, argparse, shutil
from pathlib import Path

PROJECT_ROOT = Path.cwd()

# Windows: npx is a .cmd script, subprocess.CreateProcess won't find it.
# Use shell=True on Win, or locate npx.cmd explicitly.
_use_shell = os.name == 'nt'
MMDC_CMD = "npx --yes @mermaid-js/mermaid-cli" if _use_shell else ["npx", "--yes", "@mermaid-js/mermaid-cli"]
MMDC_TIMEOUT = 60  # seconds per render (generous for first-run Chromium init)
MAX_PARALLEL = 1    # keep sequential for stability

BANNED_PATTERNS = [
    (r'```mermaid\s*\n(.*?)```', re.DOTALL),
]

def collect_blocks(src_dir, file_filter=None):
    """Collect all mermaid code blocks from src/ .md files.
    
    Args:
        src_dir: Root directory to scan.
        file_filter: Optional list of relative file paths to restrict scanning.
                     If None, scan all .md files in src_dir.
    """
    blocks = []
    
    if file_filter:
        for rel in file_filter:
            fp = os.path.join(src_dir, rel)
            if not os.path.isfile(fp):
                continue
            with open(fp, 'r', encoding='utf-8') as fh:
                content = fh.read()
            for i, m in enumerate(re.finditer(r'```mermaid\s*\n(.*?)```', content, re.DOTALL)):
                body = m.group(1).strip()
                if not body:
                    continue
                blocks.append({
                    'file': rel,
                    'idx': i,
                    'body': body,
                    'first_line': body.split('\n')[0][:80],
                    'is_empty': len(body.strip()) < 10,
                })
        return blocks
    
    for root, dirs, files in os.walk(src_dir):
        for f in sorted(files):
            if not f.endswith('.md'):
                continue
            fp = os.path.join(root, f)
            with open(fp, 'r', encoding='utf-8') as fh:
                content = fh.read()
            rel = os.path.relpath(fp, src_dir)
            for i, m in enumerate(re.finditer(r'```mermaid\s*\n(.*?)```', content, re.DOTALL)):
                body = m.group(1).strip()
                if not body:
                    continue
                blocks.append({
                    'file': rel,
                    'idx': i,
                    'body': body,
                    'first_line': body.split('\n')[0][:80],
                    'is_empty': len(body.strip()) < 10,
                })
    return blocks


def render_mermaid(body, output_path, timeout=MMDC_TIMEOUT):
    """Render a single mermaid block to SVG. Returns (success, stdout, stderr)."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.mmd', delete=False, encoding='utf-8') as f:
        f.write(body)
        mmd_path = f.name
    
    try:
        cmd = f"{MMDC_CMD} -i {mmd_path} -o {output_path} -q" if _use_shell else [*MMDC_CMD, "-i", mmd_path, "-o", str(output_path), "-q"]
        result = subprocess.run(
            cmd,
            capture_output=True, text=True, timeout=timeout,
            cwd=PROJECT_ROOT, shell=_use_shell
        )
        success = result.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 100
        stderr = result.stderr.strip()
        return success, result.stdout.strip(), stderr
    except subprocess.TimeoutExpired:
        return False, "", "TIMEOUT"
    except Exception as e:
        return False, "", str(e)
    finally:
        try:
            os.unlink(mmd_path)
        except:
            pass


def main():
    parser = argparse.ArgumentParser(description='Batch render Mermaid blocks')
    parser.add_argument('--output', '-o', default='_mermaid_renders',
                        help='Output directory for SVG renders')
    parser.add_argument('--timeout', '-t', type=int, default=MMDC_TIMEOUT,
                        help=f'Timeout per render in seconds (default: {MMDC_TIMEOUT})')
    parser.add_argument('--files', nargs='*', default=None,
                        help='Specific .md files (relative to src/) to scan')
    parser.add_argument('--files-changed', action='store_true',
                        help='Auto-detect changed files via git diff HEAD~1')
    parser.add_argument('--no-fail', action='store_true',
                        help='Exit with 0 even if renders fail')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Show all output')
    parser.add_argument('--resume', '-r', action='store_true',
                        help='Skip already-rendered files')
    parser.add_argument('--report-only', action='store_true',
                        help='Only generate report from existing renders (no new renders)')
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    src_dir = PROJECT_ROOT / "src"
    if not src_dir.exists():
        print(f"ERROR: src/ not found at {src_dir}")
        sys.exit(1)

    file_filter = None
    if args.files_changed:
        try:
            result = subprocess.run(
                ['git', 'diff', '--name-only', 'HEAD~1'],
                capture_output=True, text=True, timeout=30, cwd=PROJECT_ROOT
            )
            changed = [l.strip() for l in result.stdout.split('\n') if l.strip().endswith('.md') and l.strip().startswith('src/')]
            file_filter = [os.path.relpath(f, str(src_dir)) for f in changed]
            print(f"Auto-detected {len(file_filter)} changed .md files via git diff")
            if file_filter:
                for f in file_filter:
                    print(f"  - {f}")
        except Exception as e:
            print(f"git diff failed: {e}, falling back to full scan")
    elif args.files:
        file_filter = args.files
        print(f"Scanning {len(file_filter)} specified files")

    print(f"Collecting mermaid blocks from {src_dir} ...")
    blocks = collect_blocks(str(src_dir), file_filter=file_filter)
    print(f"Found {len(blocks)} mermaid blocks in {len(set(b['file'] for b in blocks))} files")

    # Check mmdc availability
    try:
        ver_cmd = f"{MMDC_CMD} --version" if _use_shell else [*MMDC_CMD, "--version"]
        subprocess.run(ver_cmd, capture_output=True, timeout=60, shell=_use_shell)
        print("mmdc available ✓\n")
    except Exception as e:
        print(f"mmdc not available: {e}")
        print("Install: npx @mermaid-js/mermaid-cli")
        sys.exit(1 if not args.no_fail else 0)

    results = []
    failures = []
    
    if args.report_only:
        print("Report-only mode: checking existing renders...\n")
        for b in blocks:
            safe_name = f"{b['file'].replace('/', '_').replace('\\', '_')}_{b['idx']}"
            svg_path = output_dir / f"{safe_name}.svg"
            exists = svg_path.exists()
            results.append({
                **b,
                'svg_path': str(svg_path),
                'rendered': exists,
                'success': exists,
            })
            if not exists:
                failures.append(b)
    else:
        for i, b in enumerate(blocks):
            safe_name = f"{b['file'].replace('/', '_').replace('\\', '_')}_{b['idx']}"
            svg_path = output_dir / f"{safe_name}.svg"
            
            if args.resume and svg_path.exists():
                results.append({**b, 'svg_path': str(svg_path), 'rendered': True, 'success': True})
                continue

            # Empty blocks
            if b['is_empty']:
                results.append({**b, 'svg_path': str(svg_path), 'rendered': False, 'success': False, 'error': 'EMPTY_BODY'})
                failures.append(b)
                continue

            print(f"  [{i+1}/{len(blocks)}] {b['file']}#{b['idx']}: {b['first_line']}", end='')
            sys.stdout.flush()

            success, stdout, stderr = render_mermaid(b['body'], svg_path, timeout=args.timeout)

            result = {**b, 'svg_path': str(svg_path), 'rendered': True, 'success': success}
            if not success:
                result['error'] = stderr[:200] if stderr else 'UNKNOWN'
                failures.append(b)
                print(f" ❌ {result.get('error', '')}")
            else:
                svg_size = os.path.getsize(svg_path) if svg_path.exists() else 0
                result['svg_size'] = svg_size
                print(f" ✅ ({svg_size/1024:.1f}KB)")

            results.append(result)
        
    # Summary
    passed = sum(1 for r in results if r.get('success'))
    failed = sum(1 for r in results if not r.get('success') and r.get('rendered'))
    skipped = sum(1 for r in results if not r.get('rendered') and not r.get('is_empty'))
    empty = sum(1 for r in results if r.get('is_empty'))
    
    print(f"\n{'='*60}")
    print(f"RENDER SUMMARY")
    print(f"{'='*60}")
    print(f"  Total blocks: {len(results)}")
    print(f"  Passed:       {passed}")
    print(f"  Failed:       {failed}")
    print(f"  Empty (skip): {empty}")
    if skipped:
        print(f"  Skipped:      {skipped}")
    print(f"  Renders dir:  {output_dir.resolve()}")
    
    if failures:
        print(f"\n{'='*60}")
        print(f"FAILURES ({len(failures)})")
        print(f"{'='*60}")
        for f in failures:
            r = [x for x in results if x['file'] == f['file'] and x['idx'] == f['idx']]
            if r:
                print(f"  ❌ {r[0]['file']}#{r[0]['idx']}: {r[0]['first_line']}")
                if 'error' in r[0]:
                    for line in r[0]['error'].split('\n')[:3]:
                        print(f"     {line}")

    # Save report
    report_path = output_dir / "render_report.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({
            'total': len(results),
            'passed': passed,
            'failed': failed,
            'empty': empty,
            'skipped': skipped,
            'results': results,
        }, f, ensure_ascii=False, indent=2)
    print(f"\nReport saved to: {report_path}")

    # Save failures list
    if failures:
        fail_path = output_dir / "render_failures.json"
        with open(fail_path, 'w', encoding='utf-8') as f:
            json.dump(failures, f, ensure_ascii=False, indent=2)
        print(f"Failures list: {fail_path}")

    if args.no_fail:
        sys.exit(0)
    sys.exit(1 if failed > 0 else 0)


if __name__ == '__main__':
    main()
