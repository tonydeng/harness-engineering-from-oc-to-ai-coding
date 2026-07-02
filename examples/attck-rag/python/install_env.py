#!/usr/bin/env python3
"""
ATT&CK RAG — 完整环境安装脚本（跨平台版）

安装以下组件:
  1. Docker PostgreSQL 16 + pgvector (pgvector/pgvector:pg16 镜像)
  2. Ollama + qwen2.5 本地模型 (原生安装)
  3. Python venv + 依赖

用法:
  python install_env.py [--ollama-only] [--db-only] [--model 3b|7b]

选项:
  --ollama-only   仅安装 Ollama + 模型，跳过数据库
  --db-only       仅安装数据库，跳过 Ollama
  --model 3b|7b   选择模型规模 (默认 7b)
  --pg-port PORT  PostgreSQL 映射端口 (默认 5432)
  --pg-pass PASS  PostgreSQL 密码 (默认 postgres)
  --help           显示帮助信息

前置条件:
  - Docker Desktop 已安装且运行中
  - Python 3.10+
  - macOS 需安装 Homebrew (/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)")
"""

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


# ═══════════════════════════════════════════════════════════════════════════════
# 配置
# ═══════════════════════════════════════════════════════════════════════════════

class Config:
    pg_container = "attck-pgvector"
    pg_port = "5432"
    pg_password = "postgres"
    pg_db = "attck_rag"
    pg_image = "pgvector/pgvector:pg16"

    # Ollama
    ollama_dir = {
        "Windows": str(Path("D:/Program Files/Ollama")),
        "Darwin": "/usr/local/bin",
        "Linux": "/usr/local/bin",
    }
    ollama_models = {
        "Windows": "D:/Ollama/Models",
        "Darwin": str(Path.home() / ".ollama/models"),
        "Linux": str(Path.home() / ".ollama/models"),
    }

    model_choice = "7b"  # or "3b"


# ═══════════════════════════════════════════════════════════════════════════════
# 日志工具
# ═══════════════════════════════════════════════════════════════════════════════

def _c(code, text):
    return f"\033[{code}m{text}\033[0m"

OK    = lambda m: print(f"  {_c('92', '✓')} {m}")
STEP  = lambda m: print(f"\n▶ {_c('96', m)}")
SKIP  = lambda m: print(f"  {_c('93', '↻')} {m}")
WARN  = lambda m: print(f"  {_c('93', '!')} {m}")
FAIL  = lambda m: (_c('91', f"  ✗ {m}") for _ in [sys.exit(1)])
INFO  = lambda m: print(f"    {m}")
SEP   = lambda: print(f"{'─' * 55}")


# ═══════════════════════════════════════════════════════════════════════════════
# 辅助函数
# ═══════════════════════════════════════════════════════════════════════════════

def run(cmd: list[str], **kwargs) -> subprocess.CompletedProcess:
    default = {"capture_output": True, "text": True}
    default.update(kwargs)
    return subprocess.run(cmd, **default)


def http_get(url: str, timeout: int = 5) -> bool:
    try:
        r = urllib.request.urlopen(url, timeout=timeout)
        return r.status == 200
    except Exception:
        return False


def system() -> str:
    """返回操作系统类型: Windows / Darwin / Linux"""
    return platform.system()


def is_admin() -> bool:
    """检测是否以管理员/root 权限运行"""
    if system() == "Windows":
        try:
            return run(["net", "session"], capture_output=True).returncode == 0
        except Exception:
            return False
    return os.geteuid() == 0


def check_command(name: str) -> bool:
    """检查系统命令是否存在"""
    return shutil.which(name) is not None


# ═══════════════════════════════════════════════════════════════════════════════
# 步骤 1: 系统预检
# ═══════════════════════════════════════════════════════════════════════════════

def step_preflight(cfg: Config):
    STEP("1/6 — 系统预检")
    OK(f"操作系统: {system()} {platform.machine()}")

    # Python
    v = sys.version_info
    if v.major >= 3 and v.minor >= 10:
        OK(f"Python {v.major}.{v.minor}.{v.micro}")
    else:
        FAIL(f"需要 Python 3.10+，当前 {v.major}.{v.minor}.{v.micro}")

    # Docker
    if check_command("docker"):
        r = run(["docker", "--version"])
        if r.returncode == 0:
            OK(f"Docker: {r.stdout.strip()}")

        r2 = run(["docker", "info"])
        if r2.returncode == 0:
            OK("Docker 守护进程运行中")
        else:
            FAIL("Docker 守护进程未运行。请启动 Docker Desktop")
    else:
        FAIL("Docker 未安装。请先安装 Docker Desktop (https://www.docker.com/products/docker-desktop/)")

    # 管理员权限（Windows 提示）
    if system() == "Windows" and not is_admin():
        WARN("建议以管理员身份运行此脚本以获得完整权限")


# ═══════════════════════════════════════════════════════════════════════════════
# 步骤 2: Docker PostgreSQL + pgvector
# ═══════════════════════════════════════════════════════════════════════════════

def _has_container(name: str) -> str | None:
    """检查容器是否存在，返回状态文本或 None"""
    r = run(["docker", "ps", "-a", "--filter", f"name={name}", "--format", "{{.Status}}"])
    status = r.stdout.strip()
    return status if status else None


def _container_running(name: str) -> bool:
    r = run(["docker", "ps", "--filter", f"name={name}", "--format", "{{.Status}}"])
    return bool(r.stdout.strip())


def _wait_pg_ready(container: str, timeout: int = 60) -> bool:
    """等待 PostgreSQL 就绪 (最多 timeout 秒)"""
    for i in range(timeout // 2):
        r = run(["docker", "exec", container, "pg_isready", "-U", "postgres"])
        if r.returncode == 0:
            return True
        time.sleep(2)
    return False


def step_docker_postgres(cfg: Config):
    STEP("2/6 — Docker PostgreSQL 16 + pgvector")

    container = cfg.pg_container
    existing = _has_container(container)

    if existing:
        if _container_running(container):
            SKIP(f"PostgreSQL 容器 {container} 已在运行")
        else:
            WARN(f"容器 {container} 存在但未运行，正在启动...")
            r = run(["docker", "start", container])
            if r.returncode == 0:
                OK("容器已启动")
            else:
                WARN("启动失败，将删除重建")
                run(["docker", "rm", container])

    if not _container_running(container):
        # 拉取镜像
        STEP("  拉取 pgvector/pgvector:pg16 镜像...")
        r = run(["docker", "pull", cfg.pg_image], capture_output=False)
        if r.returncode == 0:
            OK("镜像拉取完成")
        else:
            FAIL("镜像拉取失败，请检查网络连接")

        # 检查端口冲突
        if system() == "Windows":
            r = run(["netstat", "-ano"], capture_output=True, text=True)
            if f":{cfg.pg_port} " in r.stdout:
                WARN(f"端口 {cfg.pg_port} 可能已被占用")
        elif system() == "Linux":
            r = run(["ss", "-tlnp"], capture_output=True, text=True)
            if f":{cfg.pg_port}" in r.stdout:
                WARN(f"端口 {cfg.pg_port} 可能已被占用")

        # 创建并启动容器
        STEP("  创建并启动 PostgreSQL 容器...")
        r = run([
            "docker", "run", "-d",
            "--name", container,
            "-e", f"POSTGRES_USER=postgres",
            "-e", f"POSTGRES_PASSWORD={cfg.pg_password}",
            "-e", f"POSTGRES_DB={cfg.pg_db}",
            "-p", f"{cfg.pg_port}:5432",
            "-v", "attck_pgdata:/var/lib/postgresql/data",
            "--restart", "unless-stopped",
            cfg.pg_image,
        ], capture_output=False)
        if r.returncode == 0:
            OK("容器创建成功")
        else:
            FAIL("容器创建失败")

        # 等待就绪
        STEP("  等待 PostgreSQL 就绪...")
        if _wait_pg_ready(container):
            OK(f"PostgreSQL 就绪 (localhost:{cfg.pg_port})")
        else:
            WARN("PostgreSQL 未能在预期时间内就绪，请稍后手动检查")

    # 验证 pgvector
    STEP("  验证 pgvector 扩展...")
    r = run(["docker", "exec", "-i", container, "psql", "-U", "postgres", "-d", cfg.pg_db,
             "-t", "-c", "SELECT extversion FROM pg_extension WHERE extname='vector';"])
    pgv_ver = r.stdout.strip()
    if pgv_ver:
        OK(f"pgvector {pgv_ver} 已启用")
    else:
        run(["docker", "exec", "-i", container, "psql", "-U", "postgres", "-d", cfg.pg_db,
             "-c", "CREATE EXTENSION IF NOT EXISTS vector;"])
        r = run(["docker", "exec", "-i", container, "psql", "-U", "postgres", "-d", cfg.pg_db,
                 "-t", "-c", "SELECT extversion FROM pg_extension WHERE extname='vector';"])
        pgv_ver = r.stdout.strip()
        if pgv_ver:
            OK(f"pgvector {pgv_ver} 已启用")
        else:
            WARN("pgvector 启用失败，请稍后手动执行: CREATE EXTENSION vector;")

    # 应用 schema.sql
    project_root = Path(__file__).resolve().parent.parent
    schema_file = project_root / "config" / "schema.sql"
    if schema_file.exists():
        STEP("  应用数据库表结构...")
        schema_sql = schema_file.read_text(encoding="utf-8")
        r = run(["docker", "exec", "-i", container, "psql", "-U", "postgres", "-d", cfg.pg_db],
                input=schema_sql)
        if r.returncode == 0:
            OK("表结构已创建")
        else:
            WARN("表结构创建失败，请稍后手动执行: psql -d attck_rag < schema.sql")
    else:
        WARN(f"schema.sql 未找到: {schema_file}")

    OK("PostgreSQL + pgvector 环境就绪")


# ═══════════════════════════════════════════════════════════════════════════════
# 步骤 3-4: Ollama 安装 + 模型拉取
# ═══════════════════════════════════════════════════════════════════════════════

def step_ollama(cfg: Config):
    STEP("3/6 — Ollama 安装")

    os_type = system()
    ollama_bin = "ollama.exe" if os_type == "Windows" else "ollama"
    install_dir = cfg.ollama_dir.get(os_type, "/usr/local/bin")
    ollama_path = os.path.join(install_dir, ollama_bin)

    # 检查是否已安装
    if check_command("ollama") or Path(ollama_path).exists():
        SKIP(f"Ollama 已安装")
    else:
        if os_type == "Windows":
            STEP("  下载 Ollama Windows 安装包...")
            setup_path = Path(os.environ.get("TEMP", "C:/Temp")) / "OllamaSetup.exe"
            if not setup_path.exists():
                url = "https://ollama.com/download/OllamaSetup.exe"
                INFO(f"  从 {url} 下载...")
                urllib.request.urlretrieve(url, setup_path)
                OK("下载完成")
            else:
                SKIP("安装包已存在，跳过下载")

            STEP(f"  安装 Ollama 到 {install_dir}...")
            r = run([str(setup_path), "/S", f"/D={install_dir}"], capture_output=False)
            if r.returncode == 0:
                OK("Ollama 安装完成")
            else:
                WARN(f"安装退出码: {r.returncode}，请手动检查")

        elif os_type == "Darwin":
            STEP("  通过 Homebrew 安装 Ollama...")
            if check_command("brew"):
                r = run(["brew", "install", "ollama"], capture_output=False)
                if r.returncode == 0:
                    OK("Ollama 安装完成")
                else:
                    WARN("brew install 失败")
            else:
                WARN("Homebrew 未安装，请手动安装: https://ollama.com/download/mac")

        else:  # Linux
            STEP("  通过安装脚本安装 Ollama...")
            WARN("Linux 安装需要 curl 和 sudo 权限")
            r = run(["curl", "-fsSL", "https://ollama.com/install.sh"], capture_output=True)
            if r.returncode == 0:
                r2 = run(["sh", "-c", "curl -fsSL https://ollama.com/install.sh | sh"], capture_output=False)
                if r2.returncode == 0:
                    OK("Ollama 安装完成")
                else:
                    WARN("安装脚本执行失败")
            else:
                WARN("无法下载安装脚本，请手动安装: https://ollama.com/download/linux")

    # ── 配置 Ollama 模型存储路径 ──
    models_dir = cfg.ollama_models.get(os_type, str(Path.home() / ".ollama/models"))
    if os_type == "Windows":
        SEP = os.sep
        os.environ["OLLAMA_MODELS"] = models_dir
        Path(models_dir).mkdir(parents=True, exist_ok=True)
        INFO(f"模型存储: {models_dir}")

    # 启动 Ollama
    STEP("  启动 Ollama 服务...")
    ollama_ready = http_get("http://localhost:11434/api/tags", timeout=2)
    if ollama_ready:
        SKIP("Ollama 服务已在运行")
    else:
        if os_type == "Windows":
            subprocess.Popen([ollama_path, "serve"],
                             creationflags=subprocess.CREATE_NO_WINDOW)
        elif os_type == "Darwin":
            run(["open", "-a", "Ollama"])
        else:
            subprocess.Popen(["ollama", "serve"],
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 等待就绪
        STEP("  等待 Ollama 就绪...")
        for i in range(30):
            if http_get("http://localhost:11434/api/tags", timeout=2):
                OK("Ollama 服务就绪 (localhost:11434)")
                ollama_ready = True
                break
            time.sleep(2)
        if not ollama_ready:
            WARN("Ollama 未能在预期时间内响应，请稍后手动检查")

    # ── 拉取模型 ──
    STEP("4/6 — 拉取本地模型")
    if ollama_ready:
        models = [("qwen2.5:latest", "~4.7 GB", "默认模型（所有查询类型）")]

        for name, size, purpose in models:
            r = run(["ollama", "list"])
            if name in r.stdout:
                SKIP(f"模型 {name} ({purpose}) 已存在")
                continue

            STEP(f"  拉取 {name} ({purpose}, {size})...")
            INFO("首次下载较慢，请保持网络畅通")
            r = run(["ollama", "pull", name], capture_output=False)
            if r.returncode == 0:
                OK(f"{name} 已就绪")
            else:
                WARN(f"拉取失败，稍后可手动运行: ollama pull {name}")
    else:
        WARN("Ollama 未就绪，跳过模型拉取")


# ═══════════════════════════════════════════════════════════════════════════════
# 步骤 5: Python venv + 依赖
# ═══════════════════════════════════════════════════════════════════════════════

def step_python_venv(cfg: Config):
    STEP("5/6 — Python 虚拟环境 + 依赖")

    project_root = Path(__file__).resolve().parent.parent
    venv_dir = project_root / ".venv"
    req_file = project_root / "config" / "requirements.txt"

    # 检查 venv 是否存在
    venv_python = venv_dir / ("Scripts" if system() == "Windows" else "bin") / "python.exe" if system() == "Windows" else venv_dir / "bin" / "python3"
    if not system() == "Windows":
        venv_python = venv_dir / "bin" / "python3"

    if venv_python.exists():
        SKIP(f"Python 虚拟环境已存在: {venv_dir}")
    else:
        STEP("  创建虚拟环境...")
        r = run([sys.executable, "-m", "venv", str(venv_dir)])
        if r.returncode == 0:
            OK(f"虚拟环境已创建: {venv_dir}")
        else:
            WARN("虚拟环境创建失败")
            return

    # 安装依赖
    STEP("  安装 Python 依赖...")
    pip_cmd = [str(venv_python), "-m", "pip"]
    if req_file.exists():
        r = run([*pip_cmd, "install", "-r", str(req_file)], capture_output=False)
        if r.returncode == 0:
            OK("Python 依赖安装完成")
        else:
            WARN("pip install 返回非零退出码，请检查 requirements.txt")
    else:
        WARN(f"requirements.txt 未找到: {req_file}")


# ═══════════════════════════════════════════════════════════════════════════════
# 步骤 6: 验证与报告
# ═══════════════════════════════════════════════════════════════════════════════

def step_verify(cfg: Config):
    STEP("6/6 — 最终验证")

    project_root = Path(__file__).resolve().parent.parent
    results = {}

    # PostgreSQL
    pg_ok = False
    r = run(["docker", "exec", "-i", cfg.pg_container, "psql", "-U", "postgres",
             "-d", cfg.pg_db, "-c", "SELECT 1 AS ok;"])
    if "1 row" in r.stdout:
        pg_ok = True
    pg_ver = run(["docker", "exec", "-i", cfg.pg_container, "psql", "-U", "postgres",
                  "-d", cfg.pg_db, "-t", "-c", "SELECT version();"]).stdout.strip()

    results["PostgreSQL"] = ("✅" if pg_ok else "❌") + f" {cfg.pg_container}"

    # pgvector
    pgv_ver = run(["docker", "exec", "-i", cfg.pg_container, "psql", "-U", "postgres",
                   "-d", cfg.pg_db, "-t", "-c",
                   "SELECT extversion FROM pg_extension WHERE extname='vector';"]).stdout.strip()
    results["pgvector"] = f"✅ {pgv_ver}" if pgv_ver else "❌"

    # Database
    results["attck_rag 数据库"] = f"✅ {cfg.pg_db}" if pg_ok else "❌"

    # Ollama
    ollama_ok = http_get("http://localhost:11434/api/tags", timeout=3)
    results["Ollama"] = "✅" if ollama_ok else "❌"

    # Models
    model_list = run(["ollama", "list"]).stdout if ollama_ok else ""
    results["qwen2.5"] = "✅" if "qwen2.5" in model_list else "❌"

    # Python venv
    venv_dir = project_root / ".venv"
    py_ok = venv_dir.exists()
    results["Python venv"] = f"✅ {venv_dir}" if py_ok else "❌"

    # ── 报告 ──
    print(f"""
{'━' * 55}
  📋 ATT&CK RAG 环境安装报告
{'━' * 55}""")
    for k, v in results.items():
        print(f"  {k:18} {v}")
    if pg_ver:
        print(f"    {pg_ver[:50]}...")
    print(f"{'━' * 55}")

    print(f"""
使用说明:
  # 1. 验证 PostgreSQL 连接
      docker exec -it {cfg.pg_container} psql -U postgres -d {cfg.pg_db} \\
        -c "SELECT extversion FROM pg_extension WHERE extname='vector';"

  # 2. 激活 Python 环境并构建索引
      python {project_root / 'python' / 'setup.py'} --src /path/to/attck-knowledge/src

  # 3. 运行查询 CLI
      python {project_root / 'python' / 'query.py'}

  # 4. 停止 PostgreSQL 容器
      docker stop {cfg.pg_container}

  # 5. 重新启动
      docker start {cfg.pg_container}

  # 6. 完全清理（删除数据卷）
      docker rm -v {cfg.pg_container}
""")


# ═══════════════════════════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="ATT&CK RAG — 完整环境安装")
    ap.add_argument("--ollama-only", action="store_true", help="仅安装 Ollama")
    ap.add_argument("--db-only", action="store_true", help="仅安装数据库")
    ap.add_argument("--model", choices=["3b", "7b"], default="7b", help="模型规模")
    ap.add_argument("--pg-port", default="5432", help="PostgreSQL 端口")
    ap.add_argument("--pg-pass", default="postgres", help="PostgreSQL 密码")
    args = ap.parse_args()

    cfg = Config()
    cfg.model_choice = args.model
    cfg.pg_port = args.pg_port
    cfg.pg_password = args.pg_pass

    print(f"{'━' * 55}")
    print("  ATT&CK RAG — 完整环境安装")
    print(f"{'━' * 55}")

    if not args.db_only:
        step_preflight(cfg)
    if not args.ollama_only:
        step_docker_postgres(cfg)
    if not args.db_only:
        step_ollama(cfg)
        step_python_venv(cfg)
    step_verify(cfg)

    OK("全部完成")


if __name__ == "__main__":
    main()
