#!/usr/bin/env python3
"""
ATT&CK RAG — 一键设置脚本（跨平台版）

功能:
  1. 检查 Python/Ollama 环境
  2. 安装 Python 依赖
  3. 检查/拉取 Ollama 模型
  4. 构建向量索引（如果还没建过）
  5. 进入交互查询模式

用法:
  python setup.py [--src <attck-knowledge/src>] [--db <path>] [--no-query]

环境变量:
  ATTCK_SRC   — attck-knowledge 的 src/ 目录路径
  OLLAMA_HOST — Ollama 服务地址 (默认 http://localhost:11434)
  DB_PATH     — SQLite 向量库路径 (默认 ./attck_vec.db)
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


# ── 颜色 / 日志 ──────────────────────────────────────────────────────────────

def _c(code: str, text: str) -> str:
    """返回带 ANSI 颜色的文本（Windows 10+ 支持）"""
    return f"\033[{code}m{text}\033[0m"


OK      = lambda m: print(f"  {_c('92', '✓')} {m}")
STEP    = lambda m: print(f"\n§ {_c('96', m)}")
WARN    = lambda m: print(f"  {_c('93', '!')} {m}")
FAIL    = lambda m: (_c('91', f"  ✗ {m}") for _ in [sys.exit(1)])
INFO    = lambda m: print(f"    {m}")


# ── 辅助函数 ─────────────────────────────────────────────────────────────────

def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    """运行命令并返回结果。默认不抛异常。"""
    default = {"capture_output": True, "text": True}
    default.update(kwargs)
    return subprocess.run(cmd, **default)


def http_get(url: str, timeout: int = 5) -> bool:
    """简单 HTTP GET 探测服务是否在线"""
    try:
        r = urllib.request.urlopen(url, timeout=timeout)
        return r.status == 200
    except Exception:
        return False


def confirm(prompt: str, default: str = "y") -> bool:
    """交互式确认"""
    hint = f"[{default}]" if default else ""
    ans = input(f"{prompt} {hint} ").strip().lower()
    if not ans:
        ans = default
    return ans.startswith("y")


# ── 步骤实现 ─────────────────────────────────────────────────────────────────

def step_check_python():
    """Step 1: 检查 Python 环境"""
    STEP("检查 Python 环境")
    v = sys.version_info
    if v.major < 3 or (v.major == 3 and v.minor < 10):
        FAIL(f"需要 Python 3.10+，当前 {v.major}.{v.minor}.{v.micro}")
    OK(f"Python {v.major}.{v.minor}.{v.micro}")


def step_install_deps(project_root: Path):
    """Step 2: 安装 Python 依赖"""
    STEP("安装 Python 依赖")
    req_file = project_root / "config" / "requirements.txt"
    if not req_file.exists():
        WARN(f"requirements.txt 未找到: {req_file}")
        return

    r = run([sys.executable, "-m", "pip", "install", "-r", str(req_file)])
    if r.returncode == 0:
        OK("依赖安装完成")
    else:
        WARN(f"pip install 返回非零退出码 ({r.returncode})")
        if not confirm("继续执行?", "y"):
            sys.exit(1)


def step_check_ollama():
    """Step 3: 检查 Ollama 服务"""
    STEP("检查 Ollama 服务")
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")

    if http_get(f"{ollama_host}/api/tags"):
        OK(f"Ollama 服务运行中 ({ollama_host})")
        return True
    else:
        WARN("Ollama 未运行或未安装")
        INFO("Windows: https://ollama.com/download/windows")
        INFO("macOS:   brew install ollama")
        INFO("Linux:   curl -fsSL https://ollama.com/install.sh | sh")
        INFO("安装后启动: ollama serve")
        return False


def step_pull_models():
    """Step 4: 拉取/检查 Ollama 模型"""
    STEP("检查 Ollama 模型")

    required = ["qwen2.5:latest"]

    r = run(["ollama", "list"])
    existing = r.stdout if r.returncode == 0 else ""

    for model in required:
        if model in existing:
            OK(f"模型 {model} 已存在")
        else:
            STEP(f"  拉取 {model}（首次下载约 4.7 GB，请保持网络畅通）...")
            r = run(["ollama", "pull", model], capture_output=False)
            if r.returncode == 0:
                OK(f"模型 {model} 已就绪")
            else:
                WARN(f"拉取失败，稍后可手动运行: ollama pull {model}")


def step_ensure_attck_src() -> Path:
    """Step 5: 确定 attck-knowledge 源码路径"""
    STEP("检查 ATT&CK 知识库源码")
    src = os.getenv("ATTCK_SRC")

    if not src:
        # 尝试几个常见位置
        candidates = [
            Path.cwd() / "attck-knowledge" / "src",
            Path.cwd().parent / "attck-knowledge" / "src",
            Path.home() / "projects" / "attck-knowledge" / "src",
            Path.home() / "github" / "attck-knowledge" / "src",
        ]
        for c in candidates:
            if c.is_dir():
                src = str(c)
                break

    if not src or not Path(src).is_dir():
        WARN("ATT&CK 源码目录未找到")
        INFO("请设置环境变量 ATTCK_SRC 或使用 --src 参数")
        if sys.stdin.isatty():
            src = input("请输入 attck-knowledge 的 src/ 目录路径: ").strip()
        if not src or not Path(src).is_dir():
            FAIL(f"目录不存在: {src}")

    OK(f"ATT&CK 源码: {src}")
    return Path(src)


def step_build_index(src: Path, db_path: Path, project_root: Path):
    """Step 6: 构建索引（如尚未构建）"""
    STEP("构建向量索引")
    if db_path.exists():
        OK(f"索引已存在: {db_path}")
        return

    index_script = project_root / "python" / "index_builder.py"
    if not index_script.exists():
        FAIL(f"索引构建脚本未找到: {index_script}")

    r = run([sys.executable, str(index_script), "--src", str(src), "--db", str(db_path)])
    if r.returncode == 0:
        OK(f"索引构建完成: {db_path}")
    else:
        FAIL("索引构建失败，请检查路径和依赖")


def step_query_mode(db_path: Path, project_root: Path):
    """Step 7: 进入交互查询模式"""
    STEP("启动交互查询模式")
    INFO("输入问题查询 ATT&CK 知识库，输入 'exit' 退出\n")

    query_script = project_root / "python" / "query.py"
    if not query_script.exists():
        WARN(f"查询脚本未找到: {query_script}")
        return

    env = os.environ.copy()
    env["DB_PATH"] = str(db_path)
    r = run([sys.executable, str(query_script)], env=env, capture_output=False)
    if r.returncode == 0:
        OK("查询已退出")
    else:
        WARN(f"查询脚本异常退出 (code={r.returncode})")


# ── 主入口 ───────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="ATT&CK RAG — 一键设置")
    ap.add_argument("--src", help="attck-knowledge 的 src/ 目录路径")
    ap.add_argument("--db", default="", help="向量库路径")
    ap.add_argument("--no-query", action="store_true", help="跳过交互查询模式")
    args = ap.parse_args()

    if args.src:
        os.environ["ATTCK_SRC"] = args.src

    # 项目根 = examples/attck-rag/
    project_root = Path(__file__).resolve().parent.parent

    # 确定数据库路径
    db_path = Path(args.db) if args.db else (project_root / "attck_vec.db")

    print("━" * 50)
    print("  ATT&CK RAG — 一键设置")
    print("━" * 50)

    step_check_python()
    step_install_deps(project_root)
    ollama_ok = step_check_ollama()
    if ollama_ok:
        step_pull_models()
    src = step_ensure_attck_src()
    step_build_index(src, db_path, project_root)

    if not args.no_query:
        step_query_mode(db_path, project_root)

    print(f"\n{'━' * 50}")
    OK("全部完成")
    INFO(f"索引文件: {db_path}")
    INFO(f"查询命令: python {project_root / 'python' / 'query.py'} \"T1059 是什么\"")


if __name__ == "__main__":
    main()
