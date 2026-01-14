#!/usr/bin/env python
"""
打包腳本 - 自動化打包流程

依賴安裝：
    pip install -r requirements-pack.txt

使用方式：
    python pack.py                    # 基本打包
    python pack.py --version 1.0.0    # 指定版本號
    python pack.py --clean            # 清理後打包
    python pack.py --icon icon.ico    # 指定圖標
"""

import subprocess
import argparse
import shutil
from pathlib import Path
import sys


def clean_build():
    """清理舊的打包文件"""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = ['*.spec']

    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"清理 {dir_name}/ ...")
            shutil.rmtree(dir_path)

    for pattern in files_to_clean:
        for file_path in Path('.').glob(pattern):
            print(f"刪除 {file_path} ...")
            file_path.unlink()


def generate_version(version=None):
    """生成 VERSION 文件"""
    print("=" * 50)
    print("步驟 1: 生成 VERSION 文件")
    print("=" * 50)

    cmd = [sys.executable, 'generate_version.py']
    if version:
        cmd.extend(['--version', version])

    result = subprocess.run(cmd)
    if result.returncode != 0:
        print("❌ 生成 VERSION 文件失敗")
        return False

    return True


def pack_exe(icon=None):
    """執行 PyInstaller 打包"""
    print("\n" + "=" * 50)
    print("步驟 2: 使用 PyInstaller 打包")
    print("=" * 50)

    spec_file = Path('StarResonanceFishing.spec')

    if not spec_file.exists():
        print(f"❌ 找不到 {spec_file}")
        return False

    cmd = [
        sys.executable, '-m', 'PyInstaller',
        'StarResonanceFishing.spec'
    ]

    print(f"執行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("❌ 打包失敗")
        return False

    return True


def main():
    parser = argparse.ArgumentParser(description='自動化打包腳本')
    parser.add_argument('--version', help='指定版本號')
    parser.add_argument('--clean', action='store_true', help='打包前清理舊文件')
    parser.add_argument('--icon', help='指定圖標文件路徑')
    args = parser.parse_args()

    try:
        # 清理（如果指定）
        if args.clean:
            print("=" * 50)
            print("清理舊的打包文件")
            print("=" * 50)
            clean_build()
            print()

        # 生成版本
        if not generate_version(args.version):
            sys.exit(1)

        # 打包
        if not pack_exe(args.icon):
            sys.exit(1)

        # 成功
        print("\n" + "=" * 50)
        print("✓ 打包成功！")
        print("=" * 50)
        print(f"輸出文件: {Path('dist').absolute() / 'StarResonanceFishing.exe'}")

    except KeyboardInterrupt:
        print("\n\n用戶中斷打包")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 打包過程發生錯誤: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
