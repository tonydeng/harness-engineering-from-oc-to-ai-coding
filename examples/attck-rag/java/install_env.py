#!/usr/bin/env python3
"""
ATT&CK RAG — Java 环境安装脚本（跨平台版）

为 Java 版 Spring Boot 服务准备运行环境，包含：
  1. JDK 17+ 检查
  2. Maven 检查
  3. PostgreSQL 16+ 连接检查 + pgvector 验证
  4. attck_rag 数据库创建 + schema.sql 应用
  5. Ollama 服务 + 模型检查/拉取
  6. Maven 编译验证

用法:
  python install_env.py [--ollama-only] [--db-only] [--no-compile]

选项:
  --ollama-only   仅检查 Ollama + 模型，跳过数据库
  --db-only       仅检查数据库，跳过 Ollama + 编译
  --no-compile    跳过 Maven 编译验证
  --help          显示帮助信息

前置条件:
  - 已安装 JDK 17+ 和 Maven 3.9+
  - PostgreSQL 16+ 运行中（Docker 容器或原生安装均可），含 pgvector 扩展
  - 已安装 Ollama

也可以先运行 python/install_env.py 安装 Docker PostgreSQL + Ollama：
  cd examples/attck-rag
  python python/install_env.py --db-only     # 仅安装数据库
  python python/install_env.py --ollama-only  # 仅安装 Ollama + 模型
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
    pg_container = "attck-pgvector"          # 与 python/install_env.py 一致
    pg_host = "localhost"
    pg_port = "5432"
    pg_user = "postgres"
    pg_password = "postgres"
    pg_db = "attck_rag"

    # Ollama
    ollama_models = {
        "qwen2.5:7b-instruct-q4_K_M": "7B 量化模型（分析/推理查询）",
        "nomic-embed-text": "Embedding 模型",
    }

    # 项目路径（脚本所在目录的父目录 = java/）
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent           # examples/attck-rag/


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
    return platform.system()


def check_command(name: str) -> bool:
    return shutil.which(name) is not None


def java_version() -> str | None:
    """获取 JDK 版本号 (如 '21.0.1')"""
    java_path = shutil.which("java")
    if not java_path:
        return None
    try:
        r = run([java_path, "-version"])  # 用完整路径避免 Windows PATH 解析歧义
    except FileNotFoundError:
        return None
    # java -version 输出到 stderr
    first = r.stderr.splitlines()[0] if r.stderr else ""
    for part in first.split():
        for seg in part.split('"'):
            if seg and seg[0].isdigit():
                return seg
    return None


def maven_version() -> str | None:
    """获取 Maven 版本号 (如 '3.9.6')"""
    mvn_path = shutil.which("mvn")
    if not mvn_path:
        return None
    try:
        r = run([mvn_path, "--version"])  # 用完整路径避免 Windows PATH 解析歧义
    except FileNotFoundError:
        return None
    first = r.stdout.splitlines()[0] if r.stdout else ""
    for part in first.split():
        if part.startswith("3.") or part.startswith("4."):
            return part
    return None


def pg_connect_cmd(cfg: Config) -> list[str] | None:
    """
    检测 PostgreSQL 连接方式，返回可用的 psql 命令前缀。
    优先级: Docker 容器 → 原生 psql
    返回 None 表示无法连接。
    """
    # 尝试 Docker 容器
    if check_command("docker"):
        r = run(["docker", "ps", "--filter", f"name={cfg.pg_container}",
                 "--format", "{{.Status}}"])
        if r.stdout.strip():
            return ["docker", "exec", "-i", cfg.pg_container,
                    "psql", "-U", cfg.pg_user]

    # 尝试原生 psql
    if check_command("psql"):
        # 尝试无密码连接
        r = run(["psql", "-h", cfg.pg_host, "-p", cfg.pg_port,
                 "-U", cfg.pg_user, "-c", "SELECT 1;"],
                timeout=5)
        if r.returncode == 0:
            return ["psql", "-h", cfg.pg_host, "-p", cfg.pg_port,
                    "-U", cfg.pg_user]

        # 尝试带密码环境变量（PGPASSWORD）
        r = run(["psql", "-h", cfg.pg_host, "-p", cfg.pg_port,
                 "-U", cfg.pg_user, "-c", "SELECT 1;"],
                env={**os.environ, "PGPASSWORD": cfg.pg_password},
                timeout=5)
        if r.returncode == 0:
            return ["psql", "-h", cfg.pg_host, "-p", cfg.pg_port,
                    "-U", cfg.pg_user]

    return None


def db_exists(cfg: Config, pg_cmd: list[str]) -> bool:
    """检查数据库是否已存在"""
    r = run([*pg_cmd, "-lqt"], timeout=10)
    return cfg.pg_db in r.stdout


# ═══════════════════════════════════════════════════════════════════════════════
# 步骤 1: 系统预检（JDK + Maven）
# ═══════════════════════════════════════════════════════════════════════════════

def step_preflight(cfg: Config):
    STEP("1/5 — 系统预检")
    OK(f"操作系统: {system()} {platform.machine()}")

    # JDK
    jv = java_version()
    if jv:
        major = int(jv.split(".")[0])
        if major >= 17:
            OK(f"JDK {jv}")
        else:
            FAIL(f"需要 JDK 17+，当前 {jv}。请先安装 JDK 17+ (https://adoptium.net/)")
    else:
        FAIL("未检测到 JDK。请先安装 JDK 17+ (https://adoptium.net/)")

    # Maven
    mv = maven_version()
    if mv:
        major = int(mv.split(".")[0])
        if major >= 3:
            OK(f"Maven {mv}")
        else:
            FAIL(f"需要 Maven 3.9+，当前 {mv}")
    else:
        FAIL("未检测到 Maven。请先安装 Maven 3.9+ (https://maven.apache.org/download.cgi)")


# ═══════════════════════════════════════════════════════════════════════════════
# 步骤 2: PostgreSQL 连接 + 初始化
# ═══════════════════════════════════════════════════════════════════════════════

def step_postgres(cfg: Config):
    STEP("2/5 — PostgreSQL 16+ 连接检查")

    # 检测连接方式
    pg_cmd = pg_connect_cmd(cfg)
    if pg_cmd is None:
        WARN("无法连接到 PostgreSQL。")
        INFO("请确保 PostgreSQL 已启动:")
        INFO(f"  - 若已运行 python/install_env.py: docker start {cfg.pg_container}")
        INFO(f"  - 若首次安装: python python/install_env.py --db-only")
        INFO("跳过数据库步骤。稍后手动执行 schema.sql:")
        INFO(f"  psql -U {cfg.pg_user} -d {cfg.pg_db} < config/schema.sql")
        return

    # 显示连接方式
    if pg_cmd[0] == "docker":
        OK(f"PostgreSQL 容器 {cfg.pg_container} 运行正常")
    else:
        OK(f"PostgreSQL 连接正常 ({cfg.pg_host}:{cfg.pg_port})")

    # 验证 pgvector 扩展
    STEP("  验证 pgvector 扩展...")
    r = run([*pg_cmd, "-d", "postgres", "-t", "-c",
             "SELECT 1 FROM pg_available_extensions WHERE name='vector';"])
    if "1" in r.stdout.strip():
        OK("pgvector 扩展可用")
    else:
        WARN("pgvector 扩展不可用。请参考: https://github.com/pgvector/pgvector#installation")
        return

    # 创建数据库（如不存在）
    STEP("  检查 attck_rag 数据库...")
    if db_exists(cfg, pg_cmd):
        SKIP(f"数据库 {cfg.pg_db} 已存在")
    else:
        INFO(f"数据库 {cfg.pg_db} 不存在，正在创建...")
        r = run([*pg_cmd, "-d", "postgres", "-c", f"CREATE DATABASE {cfg.pg_db};"])
        if r.returncode == 0:
            OK(f"数据库 {cfg.pg_db} 已创建")
        else:
            WARN(f"创建数据库失败: {r.stderr.strip()}")
            return

    # 应用 schema.sql
    schema_file = cfg.project_root / "config" / "schema.sql"
    if schema_file.exists():
        STEP("  应用数据库表结构...")
        schema_sql = schema_file.read_text(encoding="utf-8")
        r = run([*pg_cmd, "-d", cfg.pg_db], input=schema_sql)
        if r.returncode == 0:
            OK("表结构已应用")
        else:
            WARN(f"schema.sql 应用失败: {r.stderr.strip()}")
    else:
        WARN(f"schema.sql 未找到: {schema_file}")

    OK("PostgreSQL 环境就绪")


# ═══════════════════════════════════════════════════════════════════════════════
# 步骤 3: Ollama 服务 + 模型
# ═══════════════════════════════════════════════════════════════════════════════

def step_ollama(cfg: Config):
    STEP("3/5 — Ollama + 模型检查")

    # 检查 Ollama 服务
    ollama_ready = check_command("ollama") and http_get("http://localhost:11434/api/tags", timeout=3)
    if ollama_ready:
        OK("Ollama 服务运行中 (localhost:11434)")
    else:
        if check_command("ollama"):
            WARN("Ollama 已安装但未运行，正在启动...")
            if system() == "Windows":
                subprocess.Popen(["ollama", "serve"],
                                 creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.Popen(["ollama", "serve"],
                                 stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            for i in range(15):
                if http_get("http://localhost:11434/api/tags", timeout=2):
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
            INFO("或运行: python python/install_env.py --ollama-only")
            return

    if not ollama_ready:
        WARN("Ollama 未就绪，跳过模型检查")
        return

    # 检查/拉取模型
    STEP("  检查模型...")
    r = run(["ollama", "list"])
    existing_models = r.stdout.lower() if r.returncode == 0 else ""

    for model_name, purpose in cfg.ollama_models.items():
        if model_name.lower() in existing_models:
            SKIP(f"模型 {model_name} 已存在")
        else:
            INFO(f"正在拉取 {model_name} ({purpose})...")
            INFO("首次下载较慢，请保持网络畅通")
            r2 = run(["ollama", "pull", model_name], capture_output=False)
            if r2.returncode == 0:
                OK(f"{model_name} 已就绪")
            else:
                WARN(f"拉取 {model_name} 失败，稍后可手动运行: ollama pull {model_name}")

    OK("Ollama + 模型就绪")


# ═══════════════════════════════════════════════════════════════════════════════
# 步骤 4: Maven 编译验证
# ═══════════════════════════════════════════════════════════════════════════════

def step_maven_compile(cfg: Config):
    STEP("4/5 — Maven 编译验证")

    java_dir = cfg.script_dir  # java/
    pom_file = java_dir / "pom.xml"

    if not pom_file.exists():
        WARN(f"pom.xml 未找到: {pom_file}")
        return

    INFO("执行 mvn compile -q ...")
    mvn = shutil.which("mvn") or "mvn"
    r = run([mvn, "compile", "-q", "-f", str(pom_file)], capture_output=False,
            timeout=300)  # 5 分钟超时

    if r.returncode == 0:
        OK("Maven 编译成功，无错误")
    else:
        FAIL("Maven 编译失败。请检查 pom.xml 和源代码")


# ═══════════════════════════════════════════════════════════════════════════════
# 步骤 5: 验证与报告
# ═══════════════════════════════════════════════════════════════════════════════

def step_verify(cfg: Config):
    STEP("5/5 — 最终验证报告")

    results = {}
    pg_ver_str = ""

    # PostgreSQL
    pg_cmd = pg_connect_cmd(cfg)
    if pg_cmd:
        r = run([*pg_cmd, "-d", cfg.pg_db, "-c", "SELECT 1 AS ok;"])
        if "1 row" in r.stdout:
            results["PostgreSQL"] = f"✅ {cfg.pg_host}:{cfg.pg_port}"

            # pgvector
            r2 = run([*pg_cmd, "-d", cfg.pg_db, "-t", "-c",
                      "SELECT extversion FROM pg_extension WHERE extname='vector';"])
            pgv = r2.stdout.strip()
            results["pgvector"] = f"✅ {pgv}" if pgv else "❌ 未启用"

            # 数据库存在性
            if db_exists(cfg, pg_cmd):
                results["attck_rag"] = f"✅ {cfg.pg_db} 已存在"
        else:
            results["PostgreSQL"] = "❌ 无法连接"
            pg_cmd = None
    else:
        results["PostgreSQL"] = "❌ 未检测到连接"

    # Ollama
    ollama_ok = check_command("ollama") and http_get("http://localhost:11434/api/tags", timeout=3)
    results["Ollama 服务"] = "✅" if ollama_ok else "❌"

    # 模型
    if ollama_ok:
        model_out = run(["ollama", "list"]).stdout
        for m in cfg.ollama_models:
            results[m] = "✅" if m in model_out else "❌ 未拉取"

    # Maven 编译
    java_dir = cfg.script_dir
    pom_file = java_dir / "pom.xml"
    if pom_file.exists():
        # 检查 target/classes 是否存在作为编译通过的信号
        classes_dir = java_dir / "target" / "classes"
        compiled = classes_dir.exists() and any(Path(classes_dir).iterdir())
        results["Maven 编译"] = "✅ 已编译" if compiled else "⚠️ 未编译（执行 mvn compile）"
    else:
        results["Maven 编译"] = "❌ pom.xml 未找到"

    # JDK
    jv = java_version()
    results["JDK"] = f"✅ {jv}" if jv else "❌"

    # Maven
    mv = maven_version()
    results["Maven"] = f"✅ {mv}" if mv else "❌"

    # ── 报告 ──
    print(f"""
{'━' * 55}
  📋 ATT&CK RAG — Java 环境报告
{'━' * 55}""")
    for k, v in results.items():
        print(f"  {k:22} {v}")
    print(f"{'━' * 55}")

    print(f"""
使用说明:
  # 1. 验证数据库连接
      psql -U {cfg.pg_user} -d {cfg.pg_db} -c "SELECT count(*) FROM attck_chunks;"

  # 2. 编译 Java 项目
      cd java/ && mvn compile -q

  # 3. 启动 Spring Boot 服务
      cd java/ && mvn spring-boot:run

  # 4. 测试查询 API
      curl -X POST http://localhost:8000/api/v1/attck/query \\
        -H "Content-Type: application/json" \\
        -d '{{"question": "T1059 是什么", "topK": 5}}'

  # 5. 健康检查
      curl http://localhost:8000/api/v1/attck/health

  # 6. 停止 PostgreSQL 容器
      docker stop {cfg.pg_container}

前置条件（数据加载）:
  Java 版需要 PostgreSQL 中已有数据。Python index_builder.py
  目前仅支持 SQLite 输出，Java 需要独立的数据加载脚本。
  计划后续提供 java/data_loader.py。
""")


# ═══════════════════════════════════════════════════════════════════════════════
# 主入口
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    ap = argparse.ArgumentParser(description="ATT&CK RAG — Java 环境安装")
    ap.add_argument("--ollama-only", action="store_true", help="仅检查 Ollama")
    ap.add_argument("--db-only", action="store_true", help="仅检查数据库")
    ap.add_argument("--no-compile", action="store_true", help="跳过 Maven 编译")
    args = ap.parse_args()

    cfg = Config()

    print(f"{'━' * 55}")
    print("  ATT&CK RAG — Java 环境安装")
    print(f"{'━' * 55}")

    if not args.ollama_only:
        step_preflight(cfg)
        step_postgres(cfg)
    if not args.db_only:
        step_ollama(cfg)
    if not args.no_compile and not args.ollama_only and not args.db_only:
        step_maven_compile(cfg)
    step_verify(cfg)

    OK("全部完成")
    print("现在可以启动项目: cd java/ && mvn spring-boot:run")


if __name__ == "__main__":
    main()
