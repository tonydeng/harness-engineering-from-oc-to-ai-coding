#!/usr/bin/env python3
"""
ATT&CK RAG — Java 一键启动脚本（跨平台版）

功能:
  1. 检查 JDK 17+ / Maven 环境
  2. 确保 PostgreSQL 可用（Docker 或原生），创建数据库 + 应用 schema
  3. 检查 Ollama 服务 + 拉取模型
  4. Maven 编译验证
  5. 启动 Spring Boot 服务 (mvn spring-boot:run)

用法:
  python setup.py [--no-start] [--db-only]

选项:
  --no-start   仅检查环境 + 编译，不启动服务
  --db-only    仅检查数据库，跳过编译和启动

环境变量:
  OLLAMA_HOST — Ollama 服务地址 (默认 http://localhost:11434)
  PGHOST      — PostgreSQL 主机 (默认 localhost)
  PGPORT      — PostgreSQL 端口 (默认 5432)
  PGDATABASE  — PostgreSQL 数据库名 (默认 attck_rag)
  PGUSER      — PostgreSQL 用户 (默认 postgres)
  PGPASSWORD  — PostgreSQL 密码 (默认 postgres)

前置条件:
  - 已安装 JDK 17+ 和 Maven 3.9+
  - PostgreSQL 16+（推荐使用 python/install_env.py --db-only 安装）
  - Ollama（推荐使用 python/install_env.py --ollama-only 安装）
"""

import argparse
import os
import platform
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path


# ── 颜色 / 日志 ──────────────────────────────────────────────────────────────

def _c(code: str, text: str) -> str:
    return f"\033[{code}m{text}\033[0m"


OK      = lambda m: print(f"  {_c('92', '✓')} {m}")
STEP    = lambda m: print(f"\n▶ {_c('96', m)}")
SKIP    = lambda m: print(f"  {_c('93', '↻')} {m}")
WARN    = lambda m: print(f"  {_c('93', '!')} {m}")
FAIL    = lambda m: (_c('91', f"  ✗ {m}") for _ in [sys.exit(1)])
INFO    = lambda m: print(f"    {m}")


# ── 辅助函数 ─────────────────────────────────────────────────────────────────

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
    return platform.system()


def check_command(name: str) -> bool:
    return shutil.which(name) is not None


def java_version() -> str | None:
    if not check_command("java"):
        return None
    r = run(["java", "-version"])
    first = (r.stderr or "").splitlines()[0] if r.stderr else ""
    for part in first.split():
        for seg in part.split('"'):
            if seg and seg[0].isdigit():
                return seg
    return None


def maven_version() -> str | None:
    if not check_command("mvn"):
        return None
    r = run(["mvn", "--version"])
    first = (r.stdout or "").splitlines()[0] if r.stdout else ""
    for part in first.split():
        if part.startswith("3.") or part.startswith("4."):
            return part
    return None


# ── 项目路径 ──────────────────────────────────────────────────────────────────

SCRIPT_DIR = Path(__file__).resolve().parent           # java/
PROJECT_ROOT = SCRIPT_DIR.parent                        # examples/attck-rag/
PG_CMD_CACHE: list[str] | None = None                   # cached psql command


def detect_pg_cmd() -> list[str] | None:
    """检测 PostgreSQL 连接方式。缓存结果避免重复探测。"""
    global PG_CMD_CACHE
    if PG_CMD_CACHE is not None:
        return PG_CMD_CACHE

    pg_host = os.getenv("PGHOST", "localhost")
    pg_port = os.getenv("PGPORT", "5432")
    pg_user = os.getenv("PGUSER", "postgres")
    pg_pass = os.getenv("PGPASSWORD", "postgres")
    container = "attck-pgvector"

    # Docker 容器优先
    if check_command("docker"):
        r = run(["docker", "ps", "--filter", f"name={container}", "--format", "{{.Status}}"])
        if r.stdout.strip():
            PG_CMD_CACHE = ["docker", "exec", "-i", container, "psql", "-U", pg_user]
            return PG_CMD_CACHE

    # 原生 psql
    if check_command("psql"):
        r = run(["psql", "-h", pg_host, "-p", pg_port, "-U", pg_user, "-c", "SELECT 1;"],
                env={**os.environ, "PGPASSWORD": pg_pass}, timeout=5)
        if r.returncode == 0:
            PG_CMD_CACHE = ["psql", "-h", pg_host, "-p", pg_port, "-U", pg_user]
            return PG_CMD_CACHE

    return None


# ── 步骤实现 ─────────────────────────────────────────────────────────────────

def step_preflight():
    """Step 1: 检查 JDK + Maven"""
    STEP("检查 JDK + Maven 环境")
    OK(f"操作系统: {system()} {platform.machine()}")

    jv = java_version()
    if jv:
        major = int(jv.split(".")[0])
        if major >= 17:
            OK(f"JDK {jv}")
        else:
            FAIL(f"需要 JDK 17+，当前 {jv}")
    else:
        FAIL("未检测到 JDK，请先安装 JDK 17+ (https://adoptium.net/)")

    mv = maven_version()
    if mv:
        major = int(mv.split(".")[0])
        if major >= 3:
            OK(f"Maven {mv}")
        else:
            FAIL(f"需要 Maven 3.9+，当前 {mv}")
    else:
        FAIL("未检测到 Maven，请先安装 Maven 3.9+ (https://maven.apache.org/download.cgi)")


def step_postgres():
    """Step 2: 确保 PostgreSQL 可用"""
    STEP("确保 PostgreSQL 可用")

    pg_host = os.getenv("PGHOST", "localhost")
    pg_port = os.getenv("PGPORT", "5432")
    pg_user = os.getenv("PGUSER", "postgres")
    pg_pass = os.getenv("PGPASSWORD", "postgres")
    pg_db = os.getenv("PGDATABASE", "attck_rag")

    pg_cmd = detect_pg_cmd()
    if pg_cmd is None:
        WARN("无法连接到 PostgreSQL。尝试启动 Docker 容器...")
        # 尝试启动已有容器
        if check_command("docker"):
            r = run(["docker", "start", "attck-pgvector"])
            if r.returncode == 0:
                INFO("等待 PostgreSQL 就绪...")
                for _ in range(15):
                    if detect_pg_cmd():
                        OK("PostgreSQL 已启动")
                        pg_cmd = PG_CMD_CACHE
                        break
                    time.sleep(2)

    if pg_cmd is None:
        WARN("PostgreSQL 不可用。请先运行:")
        INFO("  cd .. && python python/install_env.py --db-only")
        INFO("或手动启动 PostgreSQL 并确保可连接。")
        return

    # 显示连接方式
    if pg_cmd[0] == "docker":
        OK(f"PostgreSQL 容器 attck-pgvector 运行正常")
    else:
        OK(f"PostgreSQL 连接正常 ({pg_host}:{pg_port})")

    # 验证 pgvector
    r = run([*pg_cmd, "-d", "postgres", "-t", "-c",
             "SELECT 1 FROM pg_available_extensions WHERE name='vector';"])
    if "1" not in r.stdout.strip():
        WARN("pgvector 扩展不可用。请参考: https://github.com/pgvector/pgvector#installation")
        return

    # 创建数据库
    r = run([*pg_cmd, "-d", "postgres", "-lqt"])
    if pg_db not in r.stdout:
        INFO(f"创建数据库 {pg_db}...")
        r = run([*pg_cmd, "-d", "postgres", "-c", f"CREATE DATABASE {pg_db};"])
        if r.returncode == 0:
            OK(f"数据库 {pg_db} 已创建")
        else:
            WARN(f"创建数据库失败: {r.stderr.strip()}")
            return
    else:
        SKIP(f"数据库 {pg_db} 已存在")

    # 应用 schema.sql
    schema_file = PROJECT_ROOT / "config" / "schema.sql"
    if schema_file.exists():
        STEP("  应用数据库表结构...")
        schema_sql = schema_file.read_text(encoding="utf-8")
        r = run([*pg_cmd, "-d", pg_db], input=schema_sql)
        if r.returncode == 0:
            OK("表结构已应用")
        else:
            WARN(f"schema.sql 应用失败: {r.stderr.strip()}")

    OK("PostgreSQL 环境就绪")


def step_ollama():
    """Step 3: 检查 Ollama 服务 + 模型"""
    STEP("检查 Ollama 服务 + 模型")

    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    ollama_ready = check_command("ollama") and http_get(f"{ollama_host}/api/tags", timeout=3)

    if ollama_ready:
        OK(f"Ollama 服务运行中 ({ollama_host})")
    else:
        if check_command("ollama"):
            WARN("Ollama 已安装但未运行，正在启动...")
            if system() == "Windows":
                subprocess.Popen(["ollama", "serve"],
                                 creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.Popen(["ollama", "serve"],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            for _ in range(15):
                if http_get(f"{ollama_host}/api/tags", timeout=2):
                    ollama_ready = True
                    OK("Ollama 服务已启动")
                    break
                time.sleep(2)
        else:
            WARN("Ollama 未安装。请先安装:")
            if system() == "Windows":
                INFO("  https://ollama.com/download/windows")
            elif system() == "Darwin":
                INFO("  https://ollama.com/download/mac")
            else:
                INFO("  curl -fsSL https://ollama.com/install.sh | sh")
            return

    if not ollama_ready:
        return

    # 检查/拉取模型
    required_models = ["qwen2.5:7b-instruct-q4_K_M", "nomic-embed-text"]
    r = run(["ollama", "list"])
    existing = r.stdout if r.returncode == 0 else ""

    for model in required_models:
        if model in existing:
            SKIP(f"模型 {model} 已存在")
        else:
            INFO(f"正在拉取 {model}（首次下载较慢）...")
            r = run(["ollama", "pull", model], capture_output=False)
            if r.returncode == 0:
                OK(f"{model} 已就绪")
            else:
                WARN(f"拉取失败，稍后可手动运行: ollama pull {model}")

    OK("Ollama + 模型就绪")


def step_maven_compile():
    """Step 4: Maven 编译验证"""
    STEP("Maven 编译验证")

    pom_file = SCRIPT_DIR / "pom.xml"
    if not pom_file.exists():
        FAIL(f"pom.xml 未找到: {pom_file}")

    INFO("编译中 (mvn compile -q)...")
    r = run(["mvn", "compile", "-q", "-f", str(pom_file)],
            capture_output=False, timeout=300)

    if r.returncode == 0:
        OK("Maven 编译成功")
    else:
        FAIL("Maven 编译失败")


def step_start_server():
    """Step 5: 启动 Spring Boot"""
    STEP("启动 Spring Boot 服务")

    pom_file = SCRIPT_DIR / "pom.xml"
    INFO(f"执行: mvn spring-boot:run")
    INFO(f"服务端口: http://localhost:8000")
    INFO(f"API 端点: POST /api/v1/attck/query")
    INFO(f"健康检查: GET  /api/v1/attck/health")
    INFO("")

    # 阻塞式启动
    r = run(["mvn", "spring-boot:run", "-f", str(pom_file)],
            capture_output=False, timeout=0)  # 0 = no timeout, just block


# ── 主入口 ───────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="ATT&CK RAG — Java 一键启动")
    ap.add_argument("--no-start", action="store_true", help="仅检查环境 + 编译，不启动服务")
    ap.add_argument("--db-only", action="store_true", help="仅检查数据库")
    args = ap.parse_args()

    print("━" * 55)
    print("  ATT&CK RAG — Java 一键启动")
    print("━" * 55)

    step_preflight()

    if not args.db_only:
        step_postgres()
        step_ollama()
        step_maven_compile()
    else:
        step_postgres()

    if args.no_start or args.db_only:
        print(f"""
{'━' * 55}
  环境已就绪。启动服务:
    cd java/ && mvn spring-boot:run

  测试查询:
    curl -X POST http://localhost:8000/api/v1/attck/query \\
      -H "Content-Type: application/json" \\
      -d '{{"question": "T1059 是什么", "topK": 5}}'

  注意: Java 版需要 PostgreSQL 中已有数据。
  Python index_builder.py 目前仅支持 SQLite 输出，
  Java 数据加载脚本 (data_loader.py) 计划后续提供。
{'━' * 55}""")
        OK("全部完成")
    else:
        step_start_server()


if __name__ == "__main__":
    main()
