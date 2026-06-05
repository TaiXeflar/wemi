# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

# For pre-commit use version badge on README.md

import re
import sys
from pathlib import Path

# 設定檔案路徑 (請依據你專案的實際狀況調整)
VERSION_FILE = Path("version")
README_FILE = Path("README.md")

def main():
    if not VERSION_FILE.exists() or not README_FILE.exists():
        print("找不到 version 或 README.md 檔案")
        sys.exit(1)

    # 讀取 version 檔案內容並清理換行空白
    current_version = VERSION_FILE.read_text(encoding="utf-8").strip()

    # 讀取目前的 README 內容
    readme_content = README_FILE.read_text(encoding="utf-8")

    # 使用正規表達式尋找並替換版本徽章的 URL
    # 尋找目標: https://img.shields.io/badge/version-<任何字元>-orange
    pattern = r"https://img\.shields\.io/badge/version-[^-\s]+-orange"
    new_url = f"https://img.shields.io/badge/version-{current_version}-orange"

    new_readme_content, count = re.subn(pattern, new_url, readme_content)

    # 如果內容有改變，寫回 README 並報錯讓 pre-commit 攔截
    if readme_content != new_readme_content:
        README_FILE.write_text(new_readme_content, encoding="utf-8")
        print(f"[更新] README.md 的版本徽章已更新為 {current_version}")
        sys.exit(1) # 回傳 1 讓 pre-commit 知道檔案被修改了，要求 user 重新 add

    print("[通過] README.md 版本徽章已是最新。")
    sys.exit(0)

if __name__ == "__main__":
    main()
