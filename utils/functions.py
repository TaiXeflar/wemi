
# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from typing import Literal
import platform
import os
import subprocess
import time
from functools import wraps
from pathlib import Path
from utils import config


def os_type() -> Literal["Windows", "Linux", "BSD", "macOS"]:
    name: str = platform.system()

    if name == "Windows":
        sysname = name
    elif name == "Linux":
        sysname = name
    elif name == "Darwin":
        sysname = "macOS"
    elif "BSD" in name:
        sysname = "BSD"
    else:
        sysname = name

    return sysname

def cpu_type() -> Literal['x64', 'ARM64']:
    arch = os.getenv('PROCESSOR_ARCHITECTURE')
    if arch == 'AMD64':
        return 'x64'
    elif arch == 'ARM64':
        return 'ARM64'
    else:
        raise RuntimeError(f'Invalid CPU Architecture {arch}.')

def subdirs(path: Path, leaf: bool = False) -> list[Path] | list[str]:
    if isinstance(path, str):
        path = Path(path)

    if not path.is_dir():
        return []
    folders = (
        [p.parts[-1] for p in path.iterdir() if p.is_dir()]
        if leaf
        else [p for p in path.iterdir() if p.is_dir()]
    )

    # if any(folder for folder in folders if folder in ['bin', 'include', 'lib']):
    #     excluded = [folder for folder in folders if folder in ['bin', 'include', 'lib']]
    #     raise RuntimeError(
    #         f"Expected {path} is full of versioning subfolders, but found {excluded}")

    return folders


def where(exe: str, /):
    from shutil import which

    return which(exe)


#   =======================================================================================================================================================================================
#       clear function for clear terminal.
#


def clear():
    import os
    import sys
    import subprocess

    if config.CLEAR_HOST:
        if sys.version_info < (3, 14):
            os.system("cls" if os_type() == "Windows" else "clear")
        else:
            sh = True if os_type() == "Windows" else False
            cmd = "cls" if os_type() == "Windows" else "clear"
            subprocess.run([cmd], shell=sh)
    else:
        pass


def tic_toc(message: str = ...):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tic = time.perf_counter()

            result = func(*args, **kwargs)

            toc = time.perf_counter()
            print(f" -- {message} ({(toc - tic):.1f}s)")
            return result

        return wrapper

    return decorator


def git_head():
    _head = subprocess.run(
        ["git", "rev-parse", "--short", "HEAD"], capture_output=True, text=True
    ).stdout.strip()
    return _head


def git_repo():
    finder = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True
    ).stdout.strip()
    return Path(finder).resolve()
