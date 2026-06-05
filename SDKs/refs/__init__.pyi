# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union, Any, overload
from typing_extensions import Literal
from utils import VersionNum
from tasks import ModulesObject

class FindSDK(ABC):
    _name_desc: str = ...
    is_llvm_infra: bool = ...
    is_hetero_tgt: bool = ...

    @property
    def SDK_NAME(self) -> str:
        return str

    def __init__(self): ...
    @abstractmethod
    def __WINDOWS__(self):
        ...
        # raise NotImplementedError("WEMI requires '__WINDOWS__' method implementation.")
    # @abstractmethod
    def __LINUX__(self): ...

    # @abstractmethod
    def __BSD__(self): ...

    # @abstractmethod
    def __MACOS__(self): ...

    # @abstractmethod
    def __AIX__(self): ...

    # @abstractmethod
    def __CYGWIN__(self): ...

    # @abstractmethod
    def __MSYS2__(self): ...

    # @abstractmethod
    def __HARMONY__(self): ...
    @property
    def version(self): ...
    @property
    def rules(self) -> list[ModulesObject]: ...
    def where(self, *args: str): ...
    @overload
    def everything(self, file: str, /) -> list[Path] | None: ...
    @overload
    def everything(self, file: str, /, precise: bool = True) -> list[Path] | None: ...
    @overload
    def everything(self, regex: str = ...) -> list[Path] | None: ...
    @overload
    def everything(self, cmd: list[str], /) -> list[Path] | None: ...
    @overload
    def everything(self, *args: str) -> list[str] | None: ...
    def __where__(self, *args: str) -> Path | None: ...
    def __es__(self, file: str, /, *args: str) -> list[str] | None: ...
    def _find_program(self, *args) -> Path | None: ...
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
    ): ...
    @overload
    def add_rule(
        self,
        *,
        Module: str = None,
        output: str = None,
        mode: Literal["tcl", "cmake"] = "tcl",
        Include_file: str = None,
        Version: str | VersionNum = "0.0.0",
        modules_help: str = ...,
        module_whaits: str = ...,
        deps: list[str] = [],
        conflicts: list[str] = [],
        vcompare: list[dict[str, Any]] = None,
        VARs: dict[str, str] = {},
        ENVs: dict[str, str] = {},
        root: str,
        PATH: str | list[Literal["$root/bin", "$root"], str] = [],
        INCLUDE: str | list[Literal["$root/include"], str] = [],
        LIB: str | list[Literal["$root/lib"], str] = [],
        LD_LIBRARY_PATH: str | list[Literal["$root/bin",], str] = [],
        RPATH: str | list[str] = [],
        CPATH: str | list[Literal["$root/include"], str] = [],
        C_INCLUDE_PATH: str | list[Literal["$root/include"], str] = [],
        CPLUS_INCLUDE_PATH: str | list[Literal["$root/include"], str] = [],
        CMAKE_PREFIX_PATH: str | list[Literal["$root"], str] = [],
        NLSPATH: str | list[str] = [],
        MANPATH: str | list[str] = [],
        MODULEPATH: str | list[str] = [],
        cmake_file_content: list[str] = [],
        **kwargs,
    ): ...
    @overload
    def add_rule(self, obj: list[ModulesObject]): ...
    @overload
    def add_rule(self, obj: ModulesObject): ...
    @overload
    def add_rule(self, obj: list[dict]): ...
    @overload
    def add_rule(self, obj: dict): ...
    def update(self, name: str, info_dict: dict): ...
