
# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from typing import Literal
from pathlib import Path


CLEAR_HOST = True

DEFAULT_TASK = ""

NO_ANSI_COLOR = True
NO_NETWORK_REQUEST = False
LLVM_CONFLICT = True
HETERO_CONFLICT = True
FREE_FOR_ALL = False
NO_COMPILE_FAIL_STOP = False
TOO_LONG_DIDNT_READ = False
ENABLE_TCL_EXTENSION = False
ENABLE_SDKS: list[str] = []

SEH_STYLE: Literal["default", "python", "gcc", "clang", "msvc"] = "gcc"
GENERATOR_STYLE: Literal["ninja", "make"] = "ninja"

LOCALE: Literal["local", "global", "en", "tw"] = "global"

MODULE_INSTALL_PREFIX: Path | str = None
MODULE_ZIP_HASH_TYPE: Literal['SHA1', 'SHA224','SHA256', 'SHA384', 'SHA512',
                              'SHA3_128', 'SHA3_224','SHA3_256', 'SHA3_384', 'SHA3_512',
                              'MD5', 'CRC32', 'CRC64'] = 'SHA256'
MODULE_ZIP_VERSION = 'latest'


if SEH_STYLE.lower() not in ("default", "python", "gcc", "clang", "msvc"):
    SEH_STYLE = "default"


EXP_MIHOYO_SDK = False
ALL_IN_ONE = False

ADD_MODULES = True
NO_MODULES = False
MODULES_ONLY = False
MODULES_ALIAS = 'modules'
