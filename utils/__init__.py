# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from .compare_functions import (
    VERSION,
    VERSION_IN_RANGE,
    VERSION_EXCLUDE_RANGE,
    VERSION_WHITELIST,
    VERSION_BLACKLIST,
    STREQUAL,
    STRMATCH,
    VersionNum,
)

from .color_string import cstring, message


from .Registry import regedit

from .cmake_analyzer import cmake_variable_finder
from .header_analyzer import header_variable_finder

from .functions import (
    subdirs,
    os_type,
    tic_toc,
    clear,
)

from . import config

__all__ = [
    "VersionNum",
    "VERSION",
    "VERSION_IN_RANGE",
    "VERSION_EXCLUDE_RANGE",
    "VERSION_WHITELIST",
    "VERSION_BLACKLIST",
    "STREQUAL",
    "STRMATCH",
    "cstring",
    "message",
    "cmake_variable_finder",
    "header_variable_finder",
    "regedit",
    "subdirs",
    "os_type",
    "tic_toc",
    "clear",
    "config",
]
