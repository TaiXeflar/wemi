# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import sys
import types
import traceback
from typing import TypeVar
from types import TracebackType
from pathlib import Path

from utils import cstring, message
from utils import config

E = TypeVar("E", bound=BaseException)


def unwind(exc_type: type[E], exc_value: E, tb: TracebackType):
    """
    Usage
    ```
    try: ...
    except Exception as e:
        unwind(type(e), e, e.__traceback__)
    ```
    """

    seh_style = config.SEH_STYLE.lower()

    if issubclass(exc_type, KeyboardInterrupt):
        message(
            "ERROR",
            f"WEMI stopped {config.DEFAULT_TASK.capitalize()} process by recieving user Keyboard Interrupt (Ctrl+C).",
        )
        sys.exit(130)

    # === 核心魔法：縫合被截斷的呼叫堆疊 ===
    # 因為使用了 try-except，tb 只記錄了從發生點到攔截點的路徑。
    # 我們從攔截點 (tb.tb_frame) 繼續往上一層 (f_back) 找回 main.py -> driver.py，
    # 並用 TracebackType 動態重組 C 級別的完整 Traceback 節點。
    if tb is not None:
        f = tb.tb_frame.f_back
        new_tb = tb
        while f:
            # 往上層層回推，建立完整的 traceback 鏈
            new_tb = types.TracebackType(new_tb, f, f.f_lasti, f.f_lineno)
            f = f.f_back
        tb = new_tb  # 將完整的 traceback 替換回去

        exc_value = exc_value.with_traceback(tb)

    # 使用縫合後的完整 tb 給 traceback 物件
    te = traceback.TracebackException(exc_type, exc_value, tb)

    if seh_style in ("python", "default"):
        # 呼叫 Python 最底層的原生彩色輸出
        sys.__excepthook__(exc_type, exc_value, tb)
        return

    elif seh_style in ("gcc", "clang"):
        message("")
        message("ERROR", f"Python traceback (most recent call last): {str(exc_value)}")
    else:
        print("Python traceback:")

    frames = te.stack
    formatted_frames = list(frames.format())

    for i, (frame, fmt_str) in enumerate(zip(frames, formatted_frames)):
        is_last = i == len(frames) - 1

        filename = Path(frame.filename).resolve().as_posix()
        lineno = frame.lineno
        func_name = frame.name if frame.name != "<module>" else "global scope"

        lines = fmt_str.rstrip("\n").split("\n")
        code_line = ""
        caret_line = ""

        if len(lines) >= 2:
            code_line = lines[1]
        if len(lines) >= 3:
            caret_line = lines[2]

        if code_line.startswith("    "):
            code_line = code_line[4:]
        if caret_line.startswith("    "):
            caret_line = caret_line[4:]

        col = (getattr(frame, "colno", 0) or 0) + 1

        # ==== 準備上色的字串元件 ====

        # 決定當前層級的主題色：最後一層(error)用 ERROR，前面呼叫堆疊(note)用 HINT

        # 1. 檔案路徑與位置 (粗體)
        file_loc = cstring(
            f"{filename}:{lineno}:{col}:",
        )
        file_loc_msvc = cstring(
            f"{filename}({lineno},{col}):",
        )

        # 2. 標籤與錯誤訊息
        if is_last:
            msg = cstring(f"error: {exc_type.__name__}", "ERROR", "BOLD")
            # err_type = cstring(exc_type.__name__, (165, 0, 165), "BOLD")
            # err_text = cstring(exc_value, (144, 0, 144))

            # msg = f"{tag} {err_type}: {err_text}"
        else:
            tag = cstring("note:", "HINT", "BOLD")
            msg = f"{tag} called from here"

        # 3. 原始碼精準高亮 (將 ~~~~^^ 涵蓋的範圍上色)
        colored_code_line = code_line
        if code_line and caret_line:
            # 取得波浪號的起點與終點索引
            start_idx = len(caret_line) - len(caret_line.lstrip(" "))
            end_idx = len(caret_line.rstrip(" "))

            # 安全防護，避免超出字串長度
            start_idx = min(start_idx, len(code_line))
            end_idx = min(end_idx, len(code_line))

            if start_idx < end_idx:
                before = code_line[:start_idx]
                target = code_line[start_idx:end_idx]
                after = code_line[end_idx:]

                # 將目標區塊加上主題色與粗體
                colored_target = cstring(target, "ERROR", "BOLD")
                colored_code_line = f"{before}{colored_target}{after}"

        colored_caret = cstring(caret_line, "Error", "BOLD") if caret_line else ""

        # ==== 根據風格輸出 ====
        if seh_style == "gcc":
            colored_file = cstring(
                filename,
            )
            colored_func = cstring(func_name, None, "BOLD")

            print(f"In Python file {colored_file}: In function {colored_func}()")
            print(f"In Python file {file_loc} {msg}")

            if code_line:
                print(f"{lineno:5} | {colored_code_line}")
                if caret_line:
                    print(f"      | {colored_caret}")

        elif seh_style == "clang":
            print(f"{file_loc} {msg}")
            if code_line:
                print(colored_code_line)
                if caret_line:
                    print(colored_caret)

        elif seh_style == "msvc":
            if is_last:
                pseudo_code = f"P{abs(hash(exc_type.__name__)) % 10000:04d}"
                msg_msvc = cstring("error:", "ERROR", "BOLD")
                # msg_msvc = f"{tag_msvc} {err_type}: {err_text}"
            else:
                msg_msvc = f"{tag} called from here"

            print(f"{file_loc_msvc} {msg_msvc}")
            if code_line:
                print(colored_code_line)
                if caret_line:
                    print(colored_caret)

        # print("WEMI Configure incomplete, errors occured!")
        print()


# 替換全域的例外處理 Hook


def setup_excepthook():
    sys.excepthook = unwind


# # =========================================
# # 測試區塊
# # =========================================
# def trigger_error():
#     my_dict = {"cpu": "Ryzen", "gpu": "Radeon"}
#     # 這裡會觸發 KeyError
#     print(my_dict["ram"])

# if __name__ == "__main__":
#     trigger_error()
