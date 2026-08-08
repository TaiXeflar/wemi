# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""Dataclass-backed intermediate representation for WEMI modulefiles."""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field, fields, replace
from pathlib import Path
from typing import Any, ClassVar, Literal, TypeAlias

from utils.compare_functions import VersionNum

from ._modulesobj import *  # noqa


ModuleType: TypeAlias = Literal["tcl", "cmake", "file"]
VersionCompareEntry: TypeAlias = dict[str, VersionNum | str]


@dataclass(slots=True)
class ModulesObject:
    """WEMI modulefile IR using the historical constructor field names.

    Values are stored exactly as supplied. No post-init coercion or hidden
    normalization is performed.
    """

    Module: str
    output: str

    mode: ModuleType = "tcl"
    Include_file: str | None = None
    src: str | None = None
    alias: str | list[str] | None = None
    modules_help: str = ""
    module_whatis: str = ""
    cmakefile_content: str | None = None
    Version: VersionNum | str | None = None

    prereq: list[str] = field(default_factory=list)
    deps: list[str] = field(default_factory=list)
    conflicts: list[str] = field(default_factory=list)
    llvm_conflicts: list[str] = field(default_factory=list)
    hetero_conflicts: list[str] = field(default_factory=list)
    vcompare: list[VersionCompareEntry] = field(default_factory=list)

    VARs: dict[str, Any] = field(default_factory=dict)
    ENVs: dict[str, Any] = field(default_factory=dict)

    root: str | None = None

    PATH: list[str] = field(default_factory=list)
    INCLUDE: list[str] = field(default_factory=list)
    LIB: list[str] = field(default_factory=list)
    LD_LIBRARY_PATH: list[str] = field(default_factory=list)
    MANPATH: list[str] = field(default_factory=list)
    RPATH: list[str] = field(default_factory=list)
    CPATH: list[str] = field(default_factory=list)
    C_INCLUDE_PATH: list[str] = field(default_factory=list)
    CPLUS_INCLUDE_PATH: list[str] = field(default_factory=list)
    NLSPATH: list[str] = field(default_factory=list)
    MODULEPATH: list[str] = field(default_factory=list)

    CMAKE_PREFIX_PATH: list[str] = field(default_factory=list)
    CMAKE_INCLUDE_PATH: list[str] = field(default_factory=list)
    CMAKE_LIBRARY_PATH: list[str] = field(default_factory=list)
    CMAKE_PROGRAM_PATH: list[str] = field(default_factory=list)

    PKG_CONFIG_PATH: list[str] = field(default_factory=list)
    PKG_CONFIG_LIBDIR: list[str] = field(default_factory=list)
    PKG_CONFIG: str | None = None
    PKG_CONFIG_SYSROOT_DIR: str | None = None

    CC: CCompiler | str | None = None
    CXX: CXXCompiler | str | None = None
    FC: FCompiler | str | None = None
    RC: RCompiler | str | None = None
    OBJC: CCompiler | str | None = None
    OBJCXX: CXXCompiler | str | None = None
    CUDACXX: CUDACXXCompiler | str | None = None
    CUDAHOSTCXX: CXXCompiler | str | None = None
    HIPCXX: HIPCXXCompiler |str | None = None
    HIPHOSTCXX: CXXCompiler | str | None = None
    ISPC: str | None = None
    SWIFTC: SWIFTCompiler | str | None = None
    ASM: str | None = None
    CMAKE_MT: str | None = None

    CFLAGS: list[str] = field(default_factory=list)
    CXXFLAGS: list[str] = field(default_factory=list)
    CPPFLAGS: list[str] = field(default_factory=list)
    OBJCFLAGS: list[str] = field(default_factory=list)
    OBJCXXFLAGS: list[str] = field(default_factory=list)
    FCFLAGS: list[str] = field(default_factory=list)
    FFLAGS: list[str] = field(default_factory=list)
    RCFLAGS: list[str] = field(default_factory=list)
    CUDACXXFLAGS: list[str] = field(default_factory=list)
    HIPCXXFLAGS: list[str] = field(default_factory=list)
    ISPCFLAGS: list[str] = field(default_factory=list)
    ASMFLAGS: list[str] = field(default_factory=list)
    LDFLAGS: list[str] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    _CANONICAL_TO_LEGACY: ClassVar[dict[str, str]] = {
        "type": "mode",
        "ref": "Include_file",
        "ver": "Version",
        "VAR": "VARs",
        "ENV": "ENVs",
        "conflict": "conflicts",
        "conflict_llvm": "conflicts_llvm",
        "conflict_hetero": "conflicts_hetero",
        "MT": "CMAKE_MT",
        "CUDAFLAGS": "CUDACXXFLAGS",
        "HIPFLAGS": "HIPCXXFLAGS",
    }

    @property
    def type(self) -> ModuleType:
        return self.mode

    @type.setter
    def type(self, value: ModuleType) -> None:
        self.mode = value

    @property
    def ref(self) -> str | None:
        return self.Include_file

    @ref.setter
    def ref(self, value: str | None) -> None:
        self.Include_file = value

    @property
    def ver(self) -> VersionNum | str | None:
        return self.Version

    @ver.setter
    def ver(self, value: VersionNum | str | None) -> None:
        self.Version = value

    @property
    def VAR(self) -> dict[str, Any]:
        return self.VARs

    @VAR.setter
    def VAR(self, value: dict[str, Any]) -> None:
        self.VARs = value

    @property
    def ENV(self) -> dict[str, Any]:
        return self.ENVs

    @ENV.setter
    def ENV(self, value: dict[str, Any]) -> None:
        self.ENVs = value

    @property
    def conflict(self) -> list[str]:
        return self.conflicts

    @conflict.setter
    def conflict(self, value: list[str]) -> None:
        self.conflicts = value

    @property
    def conflict_llvm(self) -> list[str]:
        return self.conflicts_llvm

    @conflict_llvm.setter
    def conflict_llvm(self, value: list[str]) -> None:
        self.conflicts_llvm = value

    @property
    def conflict_hetero(self) -> list[str]:
        return self.conflicts_hetero

    @conflict_hetero.setter
    def conflict_hetero(self, value: list[str]) -> None:
        self.conflicts_hetero = value

    @property
    def MT(self) -> str | None:
        return self.CMAKE_MT

    @MT.setter
    def MT(self, value: str | None) -> None:
        self.CMAKE_MT = value

    @property
    def CUDAFLAGS(self) -> list[str]:
        return self.CUDACXXFLAGS

    @CUDAFLAGS.setter
    def CUDAFLAGS(self, value: list[str]) -> None:
        self.CUDACXXFLAGS = value

    @property
    def HIPFLAGS(self) -> list[str]:
        return self.HIPCXXFLAGS

    @HIPFLAGS.setter
    def HIPFLAGS(self, value: list[str]) -> None:
        self.HIPCXXFLAGS = value

    @property
    def module_whaits(self) -> str:
        return self.module_whatis

    @module_whaits.setter
    def module_whaits(self, value: str) -> None:
        self.module_whatis = value

    def copy(self, **overrides: Any) -> ModulesObject:
        translated = {
            self._CANONICAL_TO_LEGACY.get(name, name): deepcopy(value)
            for name, value in overrides.items()
        }
        return replace(self, **translated)

    def export(
        self,
        *,
        legacy: bool = True,
        exclude_none: bool = False,
    ) -> dict[str, Any]:
        # Do not use dataclasses.asdict() here. It recursively converts
        # VersionNum (also a dataclass) into a plain dict before the JSON
        # encoder gets a chance to serialize it as a version string.
        result = {
            field_info.name: deepcopy(getattr(self, field_info.name))
            for field_info in fields(self)
        }

        if not legacy:
            for canonical, historical in self._CANONICAL_TO_LEGACY.items():
                result[canonical] = result.pop(historical)

        if exclude_none:
            result = {
                name: value
                for name, value in result.items()
                if value is not None
            }

        return deepcopy(result)


def modules_object_json_encoder(
    obj: VersionNum | ModulesObject | Path,
) -> Any:
    if isinstance(obj, ModulesObject):
        return obj.export(legacy=True)
    if isinstance(obj, VersionNum):
        return str(obj)
    if isinstance(obj, Path):
        return obj.resolve().as_posix()
    raise TypeError(
        f"Object of type {type(obj).__name__} is not JSON serializable."
    )
