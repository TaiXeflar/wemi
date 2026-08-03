# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from __future__ import annotations

from collections.abc import Iterator, Mapping
from pathlib import Path
from typing import Any, Literal, TypeAlias, overload

from utils.compare_functions import VersionNum


ModuleType: TypeAlias = Literal["tcl", "cmake", "file"]
ModifyMode: TypeAlias = Literal["set", "add", "del"]

ProfileHint: TypeAlias = Literal[
    "modules",
    "amd/hip",
    "ROCm/TheRock",
    "intel",
    "intel/oneapi",
    "intel/compiler",
    "intel/dnnl",
    "intel/ocloc",
    "intel/mkl",
    "nvidia",
    "nvidia/cuda",
    "nvidia/cudnn",
    "nvidia/cudss",
    "nvidia/cutensor",
    "nvidia/cusparselt",
    "nvidia/tensorrt",
    "nvidia/cutlass",
    "nvidia/nvhpc",
    "nvidia/nvhpc-byo",
    "nvidia/cuquantum",
    "nvidia/cupqc",
    "nvidia/cangjie",
    "borland",
    "matlab",
    "gmt",
    "vs",
    "msvc",
    "ucrt",
    "llvm",
    "gcc",
]

VersionCompareEntry: TypeAlias = dict[str, VersionNum | str]


class ModulesObject(Mapping[str, Any]):
    Module: str
    output: str

    type: ModuleType
    ref: str | None
    modules_help: str
    module_whatis: str
    cmakefile_content: str | None
    ver: VersionNum | None

    prereq: list[str]
    deps: list[str]
    conflict: list[str]
    conflict_llvm: list[str]
    conflict_hetero: list[str]
    vcompare: list[VersionCompareEntry]

    VAR: dict[str, Any]
    ENV: dict[str, Any]

    root: str | None

    PATH: list[str]
    INCLUDE: list[str]
    LIB: list[str]
    LD_LIBRARY_PATH: list[str]
    MANPATH: list[str]
    RPATH: list[str]
    CPATH: list[str]
    C_INCLUDE_PATH: list[str]
    CPLUS_INCLUDE_PATH: list[str]
    NLSPATH: list[str]
    MODULEPATH: list[str]

    CMAKE_PREFIX_PATH: list[str]
    CMAKE_INCLUDE_PATH: list[str]
    CMAKE_LIBRARY_PATH: list[str]
    CMAKE_PROGRAM_PATH: list[str]

    PKG_CONFIG_PATH: list[str]
    PKG_CONFIG_LIBDIR: list[str]
    PKG_CONFIG: str | None
    PKG_CONFIG_SYSROOT_DIR: str | None

    CC: str | None
    CXX: str | None
    FC: str | None
    RC: str | None
    OBJC: str | None
    OBJCXX: str | None
    CUDACXX: str | None
    CUDAHOSTCXX: str | None
    HIPCXX: str | None
    HIPHOSTCXX: str | None
    ISPC: str | None
    SWIFTC: str | None
    ASM: str | None
    MT: str | None

    CFLAGS: list[str]
    CXXFLAGS: list[str]
    CPPFLAGS: list[str]
    OBJCFLAGS: list[str]
    OBJCXXFLAGS: list[str]
    FCFLAGS: list[str]
    FFLAGS: list[str]
    RCFLAGS: list[str]
    CUDAFLAGS: list[str]
    HIPFLAGS: list[str]
    ISPCFLAGS: list[str]
    ASMFLAGS: list[str]
    LDFLAGS: list[str]

    metadata: dict[str, Any]

    @overload
    def __init__(
        self,
        source: None = None,
        /,
        *,
        Module: str,
        output: str,
        type: ModuleType = "tcl",
        ref: str | None = None,
        modules_help: str = "",
        module_whatis: str = "",
        ver: VersionNum | str | None = None,
        prereq: list[str] | None = None,
        deps: list[str] | None = None,
        conflict: list[str] | None = None,
        conflict_llvm: list[str] | None = None,
        conflict_hetero: list[str] | None = None,
        vcompare: list[VersionCompareEntry] | None = None,
        VAR: Mapping[str, Any] | None = None,
        ENV: Mapping[str, Any] | None = None,
        root: str | None = None,
        PATH: list[str] | str | None = None,
        INCLUDE: list[str] | str | None = None,
        LIB: list[str] | str | None = None,
        LD_LIBRARY_PATH: list[str] | str | None = None,
        MANPATH: list[str] | str | None = None,
        RPATH: list[str] | str | None = None,
        CPATH: list[str] | str | None = None,
        C_INCLUDE_PATH: list[str] | str | None = None,
        CPLUS_INCLUDE_PATH: list[str] | str | None = None,
        NLSPATH: list[str] | str | None = None,
        MODULEPATH: list[str] | str | None = None,
        CMAKE_PREFIX_PATH: list[str] | str | None = None,
        CMAKE_INCLUDE_PATH: list[str] | str | None = None,
        CMAKE_LIBRARY_PATH: list[str] | str | None = None,
        CMAKE_PROGRAM_PATH: list[str] | str | None = None,
        PKG_CONFIG_PATH: list[str] | str | None = None,
        PKG_CONFIG_LIBDIR: list[str] | str | None = None,
        PKG_CONFIG: str | None = None,
        PKG_CONFIG_SYSROOT_DIR: str | None = None,
        CC: str | None = None,
        CXX: str | None = None,
        FC: str | None = None,
        RC: str | None = None,
        OBJC: str | None = None,
        OBJCXX: str | None = None,
        CUDACXX: str | None = None,
        CUDAHOSTCXX: str | None = None,
        HIPCXX: str | None = None,
        HIPHOSTCXX: str | None = None,
        ISPC: str | None = None,
        SWIFTC: str | None = None,
        ASM: str | None = None,
        MT: str | None = None,
        CFLAGS: list[str] | str | None = None,
        CXXFLAGS: list[str] | str | None = None,
        CPPFLAGS: list[str] | str | None = None,
        OBJCFLAGS: list[str] | str | None = None,
        OBJCXXFLAGS: list[str] | str | None = None,
        FCFLAGS: list[str] | str | None = None,
        FFLAGS: list[str] | str | None = None,
        RCFLAGS: list[str] | str | None = None,
        CUDAFLAGS: list[str] | str | None = None,
        HIPFLAGS: list[str] | str | None = None,
        ISPCFLAGS: list[str] | str | None = None,
        ASMFLAGS: list[str] | str | None = None,
        LDFLAGS: list[str] | str | None = None,
        metadata: Mapping[str, Any] | None = None,
        **legacy_fields: Any,
    ) -> None: ...

    @overload
    def __init__(
        self,
        source: ModulesObject | Mapping[str, Any],
        /,
        **overrides: Any,
    ) -> None: ...

    def __getitem__(self, key: str) -> Any: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def __repr__(self) -> str: ...

    def get_canonical(
        self,
        key: str,
        default: Any = None,
        /,
    ) -> Any: ...

    def set_scalar(
        self,
        prop: str,
        value: str | None,
        /,
    ) -> None: ...

    def modify_list(
        self,
        prop: str,
        mode: ModifyMode,
        /,
        *values: Any,
    ) -> None: ...

    def modify_dict(
        self,
        prop: str,
        mode: ModifyMode,
        /,
        *keys: str,
        **values: Any,
    ) -> None: ...

    def set_CC(self, compiler: str | None, /) -> None: ...
    def set_CXX(self, compiler: str | None, /) -> None: ...
    def set_FC(self, compiler: str | None, /) -> None: ...
    def set_RC(self, compiler: str | None, /) -> None: ...
    def set_CUDACXX(self, compiler: str | None, /) -> None: ...
    def set_HIPCXX(self, compiler: str | None, /) -> None: ...
    def set_MT(self, executable: str | None, /) -> None: ...
    def set_CMAKE_MT(self, executable: str | None, /) -> None: ...
    def set_PKG_CONFIG(self, executable: str | None, /) -> None: ...

    def set_ENV(
        self,
        mode: ModifyMode,
        /,
        *names: str,
        **values: Any,
    ) -> None: ...

    def set_VAR(
        self,
        mode: ModifyMode,
        /,
        *names: str,
        **values: Any,
    ) -> None: ...

    def set_PATH(self, mode: ModifyMode, /, *values: str) -> None: ...
    def set_INCLUDE(self, mode: ModifyMode, /, *values: str) -> None: ...
    def set_LIB(self, mode: ModifyMode, /, *values: str) -> None: ...
    def set_CMAKE_PREFIX_PATH(
        self,
        mode: ModifyMode,
        /,
        *values: str,
    ) -> None: ...
    def set_PKG_CONFIG_PATH(
        self,
        mode: ModifyMode,
        /,
        *values: str,
    ) -> None: ...
    def set_PKG_CONFIG_LIBDIR(
        self,
        mode: ModifyMode,
        /,
        *values: str,
    ) -> None: ...

    def set_CFLAGS(self, mode: ModifyMode, /, *flags: str) -> None: ...
    def set_CXXFLAGS(self, mode: ModifyMode, /, *flags: str) -> None: ...
    def set_FCFLAGS(self, mode: ModifyMode, /, *flags: str) -> None: ...
    def set_FFLAGS(self, mode: ModifyMode, /, *flags: str) -> None: ...
    def set_RCFLAGS(self, mode: ModifyMode, /, *flags: str) -> None: ...
    def set_CUDAFLAGS(self, mode: ModifyMode, /, *flags: str) -> None: ...
    def set_CUDACXXFLAGS(
        self,
        mode: ModifyMode,
        /,
        *flags: str,
    ) -> None: ...
    def set_HIPFLAGS(self, mode: ModifyMode, /, *flags: str) -> None: ...
    def set_HIPCXXFLAGS(
        self,
        mode: ModifyMode,
        /,
        *flags: str,
    ) -> None: ...
    def set_LDFLAGS(self, mode: ModifyMode, /, *flags: str) -> None: ...

    def export(
        self,
        *,
        legacy: bool = False,
        exclude_none: bool = False,
    ) -> dict[str, Any]: ...

    def copy(self, **overrides: Any) -> ModulesObject: ...


def modules_object_json_encoder(
    obj: VersionNum | ModulesObject | Path,
) -> Any: ...


HashType: TypeAlias = Literal[
    "MD5",
    "CRC32",
    "CRC64",
    "SHA1",
    "SHA224",
    "SHA256",
    "SHA384",
    "SHA512",
    "SHA3_128",
    "SHA3_224",
    "SHA3_256",
    "SHA3_384",
    "SHA3_512",
]

ModulesVersion: TypeAlias = Literal[
    "5.0.0",
    "5.0.1",
    "5.1.0",
    "5.1.1",
    "5.2.0",
    "5.3.0",
    "5.4.0",
    "5.5.0",
    "5.6.0",
    "5.6.1",
    "latest",
]


class ModulesZip:
    def __init__(
        self,
        version: ModulesVersion = "latest",
        /,
    ) -> None: ...

    def ziphash(
        self,
        algorithm: HashType = "SHA256",
        /,
    ) -> str: ...

    def versions_list(self) -> list[str]: ...
    def download(self, /) -> Path | None: ...

    def examine(
        self,
        hash_type: HashType = "SHA256",
        chunk_size: int = 65536,
    ) -> bool: ...

    def unzip(
        self,
        dest: str | Path = ...,
    ) -> Path | None: ...

    @property
    def version(self) -> ModulesVersion: ...

    @property
    def zipname(self) -> str: ...

    @property
    def zipurl(self) -> str: ...

    @property
    def foldername(self) -> str: ...
