# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from typing import Literal, List, Optional, Union, Any

from .color_string import cstring
from .functions import os_type

if os_type() == "Windows":
    import winreg


def regedit(
    root_key: Literal["HKLM", "HKCU"] = "HKLM",
    path: str = "",
    /,
    *,
    key_name: Optional[str] = None,
) -> Union[str, List[str], Any]:  # Any for NOTDEFINED
    # 對應 Root Key
    if root_key in ("HKEY_LOCAL_MACHINE", "HKLM"):
        _root = winreg.HKEY_LOCAL_MACHINE
    elif root_key in ("HKEY_CURRENT_USER", "HKCU"):
        _root = winreg.HKEY_CURRENT_USER
    else:
        raise TypeError(f"Unsupported Registry Root Key: {root_key}.")

    try:
        with winreg.OpenKey(_root, path) as hkey:
            if key_name is not None:
                value, _ = winreg.QueryValueEx(hkey, key_name)
                return str(value) if value else 0 if value == 0 else None

            else:
                num_subkeys, _, _ = winreg.QueryInfoKey(hkey)
                subkeys_list = [winreg.EnumKey(hkey, i) for i in range(num_subkeys)]
                return subkeys_list

    except (FileNotFoundError, OSError):
        return None

    except PermissionError:
        print(cstring("Hit No enough permission error.", "warn"))
        return None
