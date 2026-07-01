#!/usr/bin/env python3
"""
下载 sentence-transformers embedding 模型到本地目录。

为什么需要这个脚本:
  python/query.py 和 python/index_builder.py 默认从 Hugging Face Hub
  自动下载 BAAI/bge-small-zh-v1.5。这在以下场景会有问题：
    - 内网/离线环境，无法访问 Hugging Face
    - 第一次运行耗时不可控（~80MB 下载）
    - 缓存位置不透明（默认在 ~/.cache/huggingface/hub/）

  运行此脚本后，模型文件显式存储在项目本地，配合 EMBED_MODEL_PATH
  环境变量使用，后续所有操作完全离线。

用法:
  python download_models.py                         # 下载到默认路径
  python download_models.py --path /custom/path     # 自定义路径
  python download_models.py --skip-if-exists        # 已存在则跳过（默认行为）

使用本地模型的完整流程:
  1. python download_models.py                      # 首次下载
  2. EMBED_MODEL_PATH=./models/bge-small-zh-v1.5 \\ # 后续完全离线
       python query.py "T1059 是什么"

前置条件:
  - pip install -r ../config/requirements.txt（需要 sentence-transformers）
"""

import argparse
import shutil
import sys
from pathlib import Path


def format_size(path: Path) -> str:
    """计算目录总大小"""
    total = sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
    if total < 1024 * 1024:
        return f"{total / 1024:.0f} KB"
    return f"{total / 1024 / 1024:.0f} MB"


def main():
    ap = argparse.ArgumentParser(description="下载 embedding 模型到本地")
    default_path = str(Path(__file__).parent / "models" / "bge-small-zh-v1.5")
    ap.add_argument("--path", default=default_path,
                    help=f"本地存储路径 (默认 {default_path})")
    ap.add_argument("--force", action="store_true",
                    help="强制重新下载（即使已存在）")
    args = ap.parse_args()

    local_path = Path(args.path)

    # ── 检查是否已存在 ──
    if local_path.exists() and not args.force:
        print(f"  ✓ 模型已存在: {local_path} ({format_size(local_path)})")
        print(f"  使用: EMBED_MODEL_PATH={local_path} python query.py")
        return

    # ── 如果 --force，删除旧目录 ──
    if local_path.exists() and args.force:
        print(f"  删除旧模型目录...")
        shutil.rmtree(local_path)

    # ── 从 Hugging Face Hub 下载并保存到本地 ──
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("  ✗ 需要先安装 sentence-transformers")
        print(f"    pip install -r {Path(__file__).parent.parent / 'config' / 'requirements.txt'}")
        sys.exit(1)

    print(f"  正在从 Hugging Face Hub 下载 BAAI/bge-small-zh-v1.5...")
    print(f"    目标: {local_path}")
    print(f"    (~80 MB，请保持网络畅通)")

    model = SentenceTransformer("BAAI/bge-small-zh-v1.5")
    model.save(str(local_path))

    print(f"  ✓ 下载完成: {local_path} ({format_size(local_path)})")
    print()
    print(f"  后续使用不需要联网，设环境变量即可:")
    print(f"    $env:EMBED_MODEL_PATH='{local_path}'; python query.py  # Windows PowerShell")
    print(f"    export EMBED_MODEL_PATH={local_path} && python query.py  # macOS/Linux")
    print(f"    EMBED_MODEL_PATH={local_path} python query.py          # 单次")


if __name__ == "__main__":
    main()
