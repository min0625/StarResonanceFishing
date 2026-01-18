#!/usr/bin/env python
"""
使用 setuptools-scm 生成 VERSION 文件的腳本
用於 CI/CD 打包時自動生成版本號

使用方式:
    python scripts/generate_version_scm.py
    python scripts/generate_version_scm.py --version 1.2.3
"""

import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="生成 VERSION 文件")
    parser.add_argument(
        "--version", help="指定版本號（如不指定則從 git 自動獲取）"
    )
    args = parser.parse_args()

    # 獲取版本號
    if args.version:
        version = args.version
    else:
        try:
            from setuptools_scm import get_version

            version = get_version(
                root=".",
                version_scheme="post-release",
                local_scheme="no-local-version",
            )
        except (ImportError, LookupError) as e:
            print(f"⚠ 無法從 git 獲取版本號: {e}")
            version = "0.0.0"

    # 移除可能的 'v' 前綴
    version = version.lstrip("v")

    # 寫入 VERSION 文件（放在工作目錄）
    version_file = Path.cwd() / "VERSION"
    with open(version_file, "w", encoding="utf-8") as f:
        f.write(version)

    print(f"✓ VERSION 文件已生成: {version}")


if __name__ == "__main__":
    main()
