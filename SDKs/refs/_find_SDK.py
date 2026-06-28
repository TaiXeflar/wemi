# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from abc import ABC, abstractmethod
import platform
from pathlib import Path
from typing import Union, Literal, Any
from shutil import which as where
import subprocess
import sys
import re
import os


from utils.compare_functions import VersionNum
from utils import message
from tasks.objects.modulesobject import ModulesObject


def os_type() -> (
    Literal[
        "Windows",
        "Linux",
        "BSD",
        "macOS",
        "AIX",
        "Harmony",
        "Cygwin",
        "MSYS2/msys",
        "MSYS2/mingw32",
        "MSYS2/mingw64",
        "MSYS2/ucrt64",
        "MSYS2/clang32",
        "MSYS2/clang64",
    ]
):
    msystem = os.getenv("MSYSTEM")

    if msystem:
        return f"MSYS2/{msystem.lower()}"

    if sys.platform.startswith("cygwin"):
        return "Cygwin"

    name: str = platform.system()

    if name == "Windows":
        sysname = name
        if sys.platform.startswith("cygwin"):
            sysname = "Cygwin"
        if msys := os.getenv("MSYSTEM"):
            sysname = f"MSYS2/{msys}"
    elif name == "Linux":
        sysname = name
        # if D
    elif name == "Darwin":
        sysname = "macOS"
    elif "BSD" in name:
        sysname = "BSD"
    elif name == "AIX":
        sysname = name
    else:
        sysname = name

    return sysname


class FindSDK(ABC):
    _name_desc = "SDK"
    is_llvm_infra = False
    is_hetero_tgt = False

    @property
    def SDK_NAME(self) -> str:
        return str

    def __init__(self):
        message(f" -- Checking for {self._name_desc}")

        self.os = os_type()

        self.es: Path = es if (es := self.__where__("es.exe")) else Path(".deps/es.exe")

        self.info: list[ModulesObject] = []
        self.stat: dict[str, Any] = {}

        super().__init__()

        if self.os.upper() == "WINDOWS":
            self.__WINDOWS__()

        elif self.os.upper() == "LINUX":
            self.__LINUX__()

        elif self.os.upper() == "BSD":
            self.__BSD__()

        elif self.os.upper() == "MACOS":
            self.__MACOS__()

        elif self.os.upper() == "AIX":
            self.__AIX__()

        elif self.os.upper() == "HARMONY":
            self.__HARMONY__()

        elif self.os.upper() == "CYGWIN":
            self.__CYGWIN__()

        elif self.os.startswith("MSYS"):
            self.__MSYS__()

        else:
            message("FATAL_ERROR", f"Unknown OS platform {platform.system()}")

    @abstractmethod
    def __WINDOWS__(self):
        ...
        # raise NotImplementedError("WEMI requires '__WINDOWS__' method implementation.")

    # @abstractmethod
    def __LINUX__(self):
        message("FATAL_ERROR", "Linux Platform is not supported")

    # @abstractmethod
    def __BSD__(self):
        message("FATAL_ERROR", "BSD Platform is not supported")

    # @abstractmethod
    def __MACOS__(self):
        message("FATAL_ERROR", "macOS Platform is not supported")

    # @abstractmethod
    def __AIX__(self):
        message("FATAL_ERROR", "AIX Platform is not supported")

    # @abstractmethod
    def __CYGWIN__(self):
        message("FATAL_ERROR", "Cygwin Platform is not supported")

    # @abstractmethod
    def __MSYS__(self):
        message("FATAL_ERROR", "MSYS2 Platform is not supported")

    # @abstractmethod
    def __HARMONY__(self):
        message("FATAL_ERROR", "Harmony Platform is not supported")

    @property
    def version(self): ...

    @property
    def rules(self) -> list[ModulesObject]:
        return self.info

    def __where__(self, *args: str) -> Path | None:
        if not args:
            return

        executable = Path(*args)

        if executable is None:
            return

        _phony = where(str(executable))
        if not _phony:
            return
        return Path(_phony).resolve()

    def where(self, *args: str):
        return self.__where__(self, *args)

    # 1. 統一的對外接口：負責「解析不同型態的輸入」並組裝成 list
    import re
    from typing import Any

    def everything(self, *args: Any, precise: bool = True, **kwargs: Any) -> list[Path]:
        cmd_args: list[str] = []

        # 情況 A: 傳入的是一個 list
        if len(args) == 1 and isinstance(args[0], list):
            cmd_args.extend(args[0])

        # 情況 B: 傳入的是字串 (包含一般字串、萬用字元、或是正則表達式)
        elif args and all(isinstance(a, str) for a in args):
            if kwargs.get("regex"):
                cmd_args.append("-r")
                cmd_args.extend(args)

            elif kwargs.get("precise"):
                cmd_args.append("-r")  # precise 也改用正規表達式模式
                # 將每一個傳入的字串轉換為嚴格的全字匹配正則表達式
                # 例如 "cjc.exe" -> "^cjc\.exe$"
                for arg in args:
                    safe_str = re.escape(arg)
                    cmd_args.append(f"^{safe_str}$")

            else:
                # 一般搜尋或萬用字元
                cmd_args.extend(args)

        # 情況 C: 如果 args 為空，處理純 kwargs 的情況
        elif not args:
            if isinstance(kwargs.get("regex"), str):
                cmd_args.extend(["-r", kwargs["regex"]])
            elif isinstance(kwargs.get("template"), str):
                cmd_args.append(kwargs["template"])
            else:
                return None

        else:
            return None

        # 將整理好的乾淨 list 傳給 __es__ 執行
        return self.__es__(cmd_args)

    # 2. 內部執行方法：只負責處理 subprocess 和 例外捕捉
    def __es__(self, cmd_args: list[str]):
        if not self.es:
            return []

        # 組裝最終的命令列陣列
        full_cmd = [self.es] + cmd_args

        try:
            # 加入 capture_output=True 才能抓到回傳值，text=True 讓回傳值變成字串而非 bytes
            # encoding 建議設為 utf-8 避免中文檔名亂碼
            result = subprocess.run(
                full_cmd, capture_output=True, text=True, check=True, encoding="utf-8"
            )

            # 將 es.exe 輸出的多行文字，切割成 list 回傳
            if result.stdout:
                # 移除頭尾空白後以換行符號切割
                return [Path(pth) for pth in result.stdout.strip().split("\n")]
            return []

        except subprocess.CalledProcessError as e:
            # 可以在這裡加入你的 logging
            print(f"Everything 執行錯誤: {e}")
            return []
        except Exception as e:
            print(f"未知的錯誤: {e}")
            return []

    def _find_program(self, *args) -> Path | None:
        if not args:
            return

        executable = Path(*args)

        if executable is None:
            return

        _phony = where(str(executable))
        if not _phony:
            return
        return Path(_phony).resolve()

    def _find_version(
        self,
        executable: Union[Path, str] = None,
        args: Union[Literal["--version", "/version"], list[str], str] = "--version",
        vertemp: Literal["X.Y.Z", "X.Y"] = None,
        /,
        line: int = None,
        *,
        input: str = None,
        pattern: str = None,
    ):
        # 0. 基礎檢查
        if executable is None or not Path(executable).exists():
            return None

        # 1. 定義樣板 Regex
        templates = {"X.Y.Z": r"(\d+)\.(\d+)\.(\d+)", "X.Y": r"(\d+)\.(\d+)"}

        # 2. 建立候選策略清單
        candidates = []
        if vertemp is not None:
            if vertemp in templates:
                candidates.append(templates[vertemp])
            else:
                raise ValueError(f"Unknown vertemp: {vertemp}")

        if pattern is not None:
            candidates.append(pattern)

        if not candidates:
            candidates.append(templates["X.Y.Z"])
            candidates.append(templates["X.Y"])

        # 3. 執行指令取得輸出
        if isinstance(args, str):
            args = args.split(" ")
        cmd = [str(executable), *args] if args else [str(executable)]

        try:
            result = subprocess.run(
                cmd,
                errors='ignore',
                input=input,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            query_run = result.stdout.strip()
        except subprocess.SubprocessError as e:
            print(f"Error executing {executable}: {e}")
            return None

        # --- 4. 處理行數過濾 ---
        # 如果有指定 line，則只取那一行；否則搜尋整個字串
        search_target = query_run
        if line is not None:
            lines = query_run.splitlines()
            if 0 <= line < len(lines):
                search_target = lines[line]
            else:
                raise IndexError(
                    f"Requested line {line}, but output only has {len(lines)} lines."
                )

        # 5. 依序嘗試匹配
        for pat in candidates:
            match = re.search(pat, search_target)
            if match:
                # 優先使用 groups (精確捕獲)，如果沒有 groups 則使用整個字串
                val = match.groups() if match.groups() else match.group(0)
                return VersionNum(val)

        # 6. 都沒抓到 -> Raise Error
        raise RuntimeError(
            f"Failed to parse version for '{executable}'. \n"
            f"Target text was: {search_target[:100]}... \n"
            f"Tried patterns: {candidates}"
        )

    def add_rule(
        self,
        obj: list[ModulesObject] | ModulesObject | list[dict] | dict = None,
        /,
        Module: str = None,
        output: str = None,
        mode: Literal["tcl", "cmake"] = "tcl",
        Include_file: str = None,
        Version: str | VersionNum = "0.0.0",
        modules_help: str = "",
        module_whaits: str = "",
        deps: list[str] = [],
        conflicts: list[str] = [],
        llvm_conflicts: list[str] = [],
        hetero_conflicts: list[str] = [],
        vcompare: list[dict[str, Any]] = None,
        VARs: dict[str, str] = {},
        ENVs: dict[str, str] = {},
        root: str = None,
        PATH: list[Literal["$root/bin"]] = [],
        INCLUDE: list[Literal["$root/include"]] = [],
        LIB: list[Literal["$root/lib"]] = [],
        LD_LIBRARY_PATH: list[Literal["$root/bin", "$root"]] = [],
        RPATH: list[str] = [],
        CPATH: list[Literal["$root/include"]] = [],
        C_INCLUDE_PATH: list[Literal["$root/include"]] = [],
        CPLUS_INCLUDE_PATH: list[Literal["$root/include"]] = [],
        CMAKE_PREFIX_PATH: list[Literal["$root", "$root/lib/cmake"]] = [],
        PKG_CONFIG_PATH: list[str] = [],
        NLSPATH: list[str] = [],
        MANPATH: list[str] = [],
        MODULEPATH: list[str] = [],
        cmake_file_content: list[str] = [],
        **kwargs,
    ):
        if obj is None:
            # 1. 將所有明確定義的參數收集回字典
            data = {
                "Module": Module,
                "output": output or Module,
                "mode": mode,
                "Include_file": Include_file,
                "Version": Version,
                "modules_help": modules_help,
                "module_whaits": module_whaits,
                "deps": deps,
                "conflicts": conflicts,
                "llvm_conflicts": llvm_conflicts,
                "hetero_conflicts": hetero_conflicts,
                "vcompare": vcompare,
                "VARs": VARs,
                "ENVs": ENVs,
                "root": root,
                "PATH": PATH,
                "INCLUDE": INCLUDE,
                "LIB": LIB,
                "LD_LIBRARY_PATH": LD_LIBRARY_PATH,
                "RPATH": RPATH,
                "CPATH": CPATH,
                "C_INCLUDE_PATH": C_INCLUDE_PATH,
                "CPLUS_INCLUDE_PATH": CPLUS_INCLUDE_PATH,
                "CMAKE_PREFIX_PATH": CMAKE_PREFIX_PATH,
                "PKG_CONFIG_PATH": PKG_CONFIG_PATH,
                "NLSPATH": NLSPATH,
                "MANPATH": MANPATH,
                "MODULEPATH": MODULEPATH,
                "cmake_file_content": cmake_file_content,
            }

            # 2. 把剩下的 kwargs (例如 MODULEPATH) 也合併進來
            data.update(kwargs)

            # 3. (選擇性) 過濾掉空字串或空列表，保持 cache.json 乾淨
            clean_data = {k: v for k, v in data.items() if v}

            self.info.append(ModulesObject(clean_data))
        else:
            if isinstance(obj, list) and all(
                isinstance(item, ModulesObject) for item in obj
            ):
                self.info.extend(obj)

            elif isinstance(obj, list) and all(isinstance(item, dict) for item in obj):
                self.info.extend([ModulesObject(item) for item in obj])

            elif isinstance(obj, dict):
                self.info.append(ModulesObject(obj))

            elif isinstance(obj, ModulesObject):
                self.info.append(obj)

    def update(self, name: str, info_dict: dict):
        self.stat.update({name: info_dict})
