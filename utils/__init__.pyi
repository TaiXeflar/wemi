# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from pathlib import Path

from .color_string import ColorString
from typing import List, Union, Iterable, overload
from typing_extensions import Literal

@overload
def cstring(
    text: Union[str, ColorString],
    color: Literal["SUCCESS", "WARNING", "ERROR", "HINT"],
    bold: Literal["BOLD", None] = None,
    /,
) -> ColorString: ...
@overload
def cstring(
    text: Union[str, ColorString],
    color: Union[Iterable[int], str],
    bold: Literal["BOLD", None] = None,
    /,
) -> ColorString: ...
@overload
def cstring(
    text: Union[str, ColorString],
    color: None = None,
    bold: Literal["BOLD", None] = None,
    /,
) -> str: ...

@overload
def os_type() -> Literal["Windows", "Linux", "BSD", "macOS"]: ...

@overload
def cpu_type() -> Literal['x64', 'ARM64']: ...

@overload
def message(text: str, /) -> None: ...
@overload
def message(mode: Literal["NOTICE"], /, text: str) -> None: ...
@overload
def message(mode: Literal["STATUS"], /, text: str, latency: float = 0.05) -> None: ...
@overload
def message(mode: Literal["REPRINT"], /, text: str) -> None: ...
@overload
def message(mode: Literal["HINT", "WARNING", "ERROR"], /, text: str) -> None: ...
@overload
def message(mode: Literal["DEPRECATED"], /, text: str) -> None: ...
@overload
def message(mode: Literal["FATAL_ERROR"], /, text: str) -> None: ...

@overload
def regedit(root_key: Literal["HKLM", "HKCU"], path: str, /, *, key_name: str) -> str | None: ...
@overload
def regedit(root_key: Literal["HKLM", "HKCU"], path: str, /, ) -> List[str] | None: ...

@overload
def subdirs(path: Path, leaf: bool = False) -> list[Path]: ...
@overload
def subdirs(path: Path, leaf: bool = True) -> list[str]: ...

@overload
def tic_toc(message: str) -> None: ...
