

import re
from pathlib import Path
from typing import Iterable, Union, Any

def header_variable_finder(
    file: str | Path,
    hint: str | Iterable[str],  # 修正：支援單一字串或字串的 Iterable (例如 list, set)
    output: str | Iterable[str],
) -> dict[str, Any]:
    
    file_path = Path(file).resolve()
    
    # 1. 處理 hint 並轉為 set 以提升比對效率
    if isinstance(hint, str):
        hint_set = {hint}
    else:
        hint_set = set(hint) # 如果原本是 Iterable[list[str]] 這裡會報錯，所以改為 Iterable[str]

    # 2. 處理 output 並驗證變數是否在 hint 範圍內
    if output == "all":
        target_vars = hint_set
    else:
        output_set = {output} if isinstance(output, str) else set(output)
        invalid_vars = output_set - hint_set
        if invalid_vars:
            raise ValueError(
                f"Error: variables in output is not allowed in hint range -> {invalid_vars}"
            )
        target_vars = output_set

    # 3. 建立初始化 state (將 CMake 替換為 Header 適用的路徑變數)
    state = {
        "HEADER_CURRENT_FILE": file_path.as_posix(),
        "HEADER_CURRENT_DIR": file_path.parent.as_posix(),
    }

    # 4. 準備儲存結果的字典
    result_dict: dict[str, Any] = {}

    # --- 以下為讀取檔案與解析變數的邏輯 ---
    if not file_path.exists():
        raise FileNotFoundError(f"找不到檔案: {file_path}")

    content = file_path.read_text(encoding="utf-8")

    # 建立正則表達式來尋找 Header 中的變數 
    # (此處以 C/C++ 的 #define 為例，若你的 Header 是其他語言可再調整)
    define_pattern = re.compile(r'^\s*#define\s+([A-Za-z0-9_]+)\s+(.*)$', re.MULTILINE)

    for match in define_pattern.finditer(content):
        var_name = match.group(1)
        var_value = match.group(2).strip()

        if var_name in target_vars:
            # 在這裡可以直接賦值，或者呼叫類似左側未寫完的 resolve_value() 進行後續處理
            result_dict[var_name] = var_value

    return result_dict