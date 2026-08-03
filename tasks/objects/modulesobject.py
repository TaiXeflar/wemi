# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""Dataclass-backed intermediate representation for WEMI modulefiles."""

from __future__ import annotations

from collections.abc import Iterator, Mapping
from copy import deepcopy
from dataclasses import MISSING, dataclass, field, fields
from textwrap import dedent
from pathlib import Path
from typing import Any, ClassVar, Literal, TypeAlias

from utils.compare_functions import VersionNum


ModuleType: TypeAlias = Literal["tcl", "cmake", "file"]
ModifyMode: TypeAlias = Literal["set", "add", "del"]
VersionCompareEntry: TypeAlias = dict[str, VersionNum | str]


class UnknownModulesObjectFieldError(TypeError):
    """Raised when constructor input contains unsupported field names."""

    def __init__(
        self,
        unknown: list[str],
        candidates: list[str],
    ) -> None:
        self.unknown = tuple(unknown)
        self.suggestions = tuple(candidates)

        super().__init__(
            "Unknown ModulesObject field(s): "
            + ", ".join(unknown)
        )


@dataclass(init=False, slots=True)
class ModulesObject(Mapping[str, Any]):
    """Intermediate representation used to generate WEMI modulefiles.

    Supported construction forms::

        ModulesObject(Module="llvm/22", output="llvm/22")
        ModulesObject({"Module": "llvm/22", "output": "llvm/22"})
        ModulesObject(existing_object)
        ModulesObject(existing_object, output="llvm/22-debug")

    Keyword arguments override values obtained from ``source``. Input values
    are deep-copied so mutable data is not shared between instances.

    Canonical field names are used internally. Historical WEMI field names are
    accepted as constructor aliases and can be restored with
    ``export(legacy=True)``.
    """

    # ------------------------------------------------------------------
    # Module identity and renderer information
    # ------------------------------------------------------------------
    Module: str
    output: str

    type: ModuleType = "tcl"
    ref: str | None = None
    src: str | None = None
    alias: str | list[str] | None = None
    modules_help: str = ""
    module_whatis: str = ""
    cmakefile_content: str | None = None
    ver: VersionNum | None = None

    # ------------------------------------------------------------------
    # Dependencies, conflicts and version checks
    # ------------------------------------------------------------------
    prereq: list[str] = field(default_factory=list)
    deps: list[str] = field(default_factory=list)
    conflict: list[str] = field(default_factory=list)
    conflict_llvm: list[str] = field(default_factory=list)
    conflict_hetero: list[str] = field(default_factory=list)
    vcompare: list[VersionCompareEntry] = field(default_factory=list)

    # ------------------------------------------------------------------
    # Template-local variables and exported environment variables
    # ------------------------------------------------------------------
    VAR: dict[str, Any] = field(default_factory=dict)
    ENV: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Root and path-like environment variables
    # ------------------------------------------------------------------
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

    # CMake search paths.
    CMAKE_PREFIX_PATH: list[str] = field(default_factory=list)
    CMAKE_INCLUDE_PATH: list[str] = field(default_factory=list)
    CMAKE_LIBRARY_PATH: list[str] = field(default_factory=list)
    CMAKE_PROGRAM_PATH: list[str] = field(default_factory=list)

    # pkg-config search and cross-compilation settings.
    PKG_CONFIG_PATH: list[str] = field(default_factory=list)
    PKG_CONFIG_LIBDIR: list[str] = field(default_factory=list)
    PKG_CONFIG: str | None = None
    PKG_CONFIG_SYSROOT_DIR: str | None = None

    # ------------------------------------------------------------------
    # Compiler and language-tool selectors
    # ------------------------------------------------------------------
    CC: str | None = None
    CXX: str | None = None
    FC: str | None = None
    RC: str | None = None
    OBJC: str | None = None
    OBJCXX: str | None = None
    CUDACXX: str | None = None
    CUDAHOSTCXX: str | None = None
    HIPCXX: str | None = None
    HIPHOSTCXX: str | None = None
    ISPC: str | None = None
    SWIFTC: str | None = None
    ASM: str | None = None

    # Windows Manifest Tool executable. This is unrelated to MSVC /MT.
    MT: str | None = None

    # ------------------------------------------------------------------
    # Compiler and linker flags
    # ------------------------------------------------------------------
    CFLAGS: list[str] = field(default_factory=list)
    CXXFLAGS: list[str] = field(default_factory=list)
    CPPFLAGS: list[str] = field(default_factory=list)
    OBJCFLAGS: list[str] = field(default_factory=list)
    OBJCXXFLAGS: list[str] = field(default_factory=list)
    FCFLAGS: list[str] = field(default_factory=list)
    FFLAGS: list[str] = field(default_factory=list)
    RCFLAGS: list[str] = field(default_factory=list)
    CUDAFLAGS: list[str] = field(default_factory=list)
    HIPFLAGS: list[str] = field(default_factory=list)
    ISPCFLAGS: list[str] = field(default_factory=list)
    ASMFLAGS: list[str] = field(default_factory=list)
    LDFLAGS: list[str] = field(default_factory=list)

    # Renderer-, finder- or SDK-specific values that are not part of the
    # common modulefile schema.
    metadata: dict[str, Any] = field(default_factory=dict)

    # ------------------------------------------------------------------
    # Compatibility and schema metadata
    # ------------------------------------------------------------------
    _FIELD_ALIASES: ClassVar[dict[str, str]] = {
        "mode": "type",
        "Include_file": "ref",
        "Version": "ver",
        "module_whaits": "module_whatis",
        "VARs": "VAR",
        "ENVs": "ENV",
        "conflicts": "conflict",
        "conflicts_llvm": "conflict_llvm",
        "llvm_conflicts": "conflict_llvm",
        "conflicts_hetero": "conflict_hetero",
        "hetero_conflicts": "conflict_hetero",
        "CMAKE_MT": "MT",
        "CUDACXXFLAGS": "CUDAFLAGS",
        "HIPCXXFLAGS": "HIPFLAGS",
    }

    _LEGACY_EXPORT_NAMES: ClassVar[dict[str, str]] = {
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

    _LIST_FIELDS: ClassVar[frozenset[str]] = frozenset(
        {
            "prereq",
            "deps",
            "conflict",
            "conflict_llvm",
            "conflict_hetero",
            "vcompare",
            "PATH",
            "INCLUDE",
            "LIB",
            "LD_LIBRARY_PATH",
            "MANPATH",
            "RPATH",
            "CPATH",
            "C_INCLUDE_PATH",
            "CPLUS_INCLUDE_PATH",
            "NLSPATH",
            "MODULEPATH",
            "CMAKE_PREFIX_PATH",
            "CMAKE_INCLUDE_PATH",
            "CMAKE_LIBRARY_PATH",
            "CMAKE_PROGRAM_PATH",
            "PKG_CONFIG_PATH",
            "PKG_CONFIG_LIBDIR",
            "CFLAGS",
            "CXXFLAGS",
            "CPPFLAGS",
            "OBJCFLAGS",
            "OBJCXXFLAGS",
            "FCFLAGS",
            "FFLAGS",
            "RCFLAGS",
            "CUDAFLAGS",
            "HIPFLAGS",
            "ISPCFLAGS",
            "ASMFLAGS",
            "LDFLAGS",
        }
    )

    _DICT_FIELDS: ClassVar[frozenset[str]] = frozenset(
        {"VAR", "ENV", "metadata"}
    )

    _SCALAR_TOOL_FIELDS: ClassVar[frozenset[str]] = frozenset(
        {
            "CC",
            "CXX",
            "FC",
            "RC",
            "OBJC",
            "OBJCXX",
            "CUDACXX",
            "CUDAHOSTCXX",
            "HIPCXX",
            "HIPHOSTCXX",
            "ISPC",
            "SWIFTC",
            "ASM",
            "MT",
            "PKG_CONFIG",
            "PKG_CONFIG_SYSROOT_DIR",
        }
    )

    _FIELD_NAMES: ClassVar[frozenset[str] | None] = None

    # ------------------------------------------------------------------
    # Construction and normalization
    # ------------------------------------------------------------------
    def __init__(
        self,
        source: ModulesObject | Mapping[str, Any] | None = None,
        /,
        **overrides: Any,
    ) -> None:
        data = self._collect_data(source, overrides)
        normalized = self._normalize_aliases(data)
        self._initialize_fields(normalized)
        self.__post_init__()

    @staticmethod
    def _collect_data(
        source: ModulesObject | Mapping[str, Any] | None,
        overrides: Mapping[str, Any],
    ) -> dict[str, Any]:
        if source is None:
            data: dict[str, Any] = {}
        elif isinstance(source, ModulesObject):
            data = source.export()
        elif isinstance(source, Mapping):
            data = deepcopy(dict(source))
        else:
            raise TypeError(
                "source must be a ModulesObject, mapping, or None; "
                f"received {type(source).__name__}."
            )

        data.update(deepcopy(dict(overrides)))
        return data

    @classmethod
    def _normalize_aliases(
        cls,
        data: Mapping[str, Any],
    ) -> dict[str, Any]:
        normalized: dict[str, Any] = {}
        original_names: dict[str, str] = {}

        for original_name, value in data.items():
            canonical_name = cls._FIELD_ALIASES.get(
                original_name,
                original_name,
            )

            if canonical_name in normalized:
                previous_name = original_names[canonical_name]
                raise TypeError(
                    f"Both {previous_name!r} and {original_name!r} specify "
                    f"ModulesObject field {canonical_name!r}."
                )

            normalized[canonical_name] = value
            original_names[canonical_name] = original_name

        return normalized

    @classmethod
    def _known_field_names(cls) -> frozenset[str]:
        cached = cls._FIELD_NAMES
        if cached is None:
            cached = frozenset(spec.name for spec in fields(cls))
            cls._FIELD_NAMES = cached
        return cached

    def _initialize_fields(
        self,
        data: Mapping[str, Any],
    ) -> None:
        field_specs = {
            spec.name: spec
            for spec in fields(type(self))
        }

        unknown = sorted(set(data) - set(field_specs))
        if unknown:
            raise UnknownModulesObjectFieldError(
                unknown,
                sorted(field_specs),
            )

        for name, spec in field_specs.items():
            if name in data:
                value = deepcopy(data[name])
            elif spec.default is not MISSING:
                value = deepcopy(spec.default)
            elif spec.default_factory is not MISSING:
                value = spec.default_factory()
            else:
                raise TypeError(
                    f"Missing required ModulesObject field: {name}"
                )

            object.__setattr__(self, name, value)

    def __post_init__(self) -> None:
        self.Module = self._require_nonempty_string(
            "Module",
            self.Module,
        )
        self.output = self._require_nonempty_string(
            "output",
            self.output,
        )

        if self.type not in {"tcl", "cmake", "file"}:
            raise ValueError(
                f"Unsupported module type: {self.type!r}"
            )

        self.modules_help = self._require_string(
            "modules_help",
            self.modules_help,
        )
        self.module_whatis = self._require_string(
            "module_whatis",
            self.module_whatis,
        )

        if self.ref is not None:
            self.ref = self._require_nonempty_string(
                "ref",
                self.ref,
            )

        if self.src is not None:
            self.src = self._require_nonempty_string(
                "src",
                self.src,
            )

        if self.alias is not None:
            if isinstance(self.alias, str):
                self.alias = self._require_nonempty_string(
                    "alias",
                    self.alias,
                )
            else:
                self.alias = [
                    self._require_nonempty_string(
                        "alias",
                        item,
                    )
                    for item in self._coerce_list(
                        "alias",
                        self.alias,
                    )
                ]

        if self.root is not None:
            self.root = self._require_nonempty_string(
                "root",
                self.root,
            )

        self.ver = self._coerce_version(self.ver)

        for name in self._LIST_FIELDS:
            setattr(
                self,
                name,
                self._coerce_list(name, getattr(self, name)),
            )

        for name in self._DICT_FIELDS:
            setattr(
                self,
                name,
                self._coerce_dict(name, getattr(self, name)),
            )

        for name in self._SCALAR_TOOL_FIELDS:
            value = getattr(self, name)
            if value is not None:
                setattr(
                    self,
                    name,
                    self._require_nonempty_string(name, value),
                )

        self._normalize_vcompare()

        if self.cmakefile_content is not None:
            self.cmakefile_content = self._require_string(
                "cmakefile_content",
                self.cmakefile_content,
            )

    @staticmethod
    def _require_string(
        name: str,
        value: Any,
    ) -> str:
        if not isinstance(value, str):
            raise TypeError(
                f"{name} must be str; received "
                f"{type(value).__name__}."
            )
        return value

    @classmethod
    def _require_nonempty_string(
        cls,
        name: str,
        value: Any,
    ) -> str:
        normalized = cls._require_string(name, value).strip()
        if not normalized:
            raise ValueError(f"{name} cannot be empty.")
        return normalized

    @staticmethod
    def _coerce_version(
        value: VersionNum | str | None,
    ) -> VersionNum | None:
        if value is None or value is Ellipsis:
            return None
        if isinstance(value, VersionNum):
            return value
        if isinstance(value, str):
            return VersionNum(value)
        raise TypeError(
            "ver must be VersionNum, str, None, or Ellipsis; "
            f"received {type(value).__name__}."
        )

    @staticmethod
    def _coerce_list(
        name: str,
        value: Any,
    ) -> list[Any]:
        if value is None:
            return []

        if isinstance(value, str):
            return [
                item.strip()
                for item in value.split(";")
                if item.strip()
            ]

        if isinstance(value, (bytes, bytearray, Mapping)):
            raise TypeError(
                f"{name} must be a string, iterable collection, or None; "
                f"received {type(value).__name__}."
            )

        try:
            return list(value)
        except TypeError as error:
            raise TypeError(
                f"{name} must be a string, iterable collection, or None; "
                f"received {type(value).__name__}."
            ) from error

    @staticmethod
    def _coerce_dict(
        name: str,
        value: Any,
    ) -> dict[str, Any]:
        if value is None:
            return {}

        if isinstance(value, Mapping):
            return deepcopy(dict(value))

        raise TypeError(
            f"{name} must be a mapping or None; received "
            f"{type(value).__name__}."
        )

    def _normalize_vcompare(self) -> None:
        normalized: list[VersionCompareEntry] = []

        for index, entry in enumerate(self.vcompare):
            if not isinstance(entry, Mapping):
                raise TypeError(
                    "vcompare entries must be mappings; "
                    f"entry {index} is {type(entry).__name__}."
                )

            copied = deepcopy(dict(entry))
            version = copied.get("ver")

            if version is not None and not isinstance(
                version,
                VersionNum,
            ):
                copied["ver"] = VersionNum(version)

            normalized.append(copied)

        self.vcompare = normalized

    # ------------------------------------------------------------------
    # Mapping interface
    # ------------------------------------------------------------------
    def __getitem__(self, key: str) -> Any:
        canonical = self._FIELD_ALIASES.get(key, key)
        if canonical not in self._known_field_names():
            raise KeyError(key)
        return getattr(self, canonical)

    def __iter__(self) -> Iterator[str]:
        return iter(self._known_field_names())

    def __len__(self) -> int:
        return len(self._known_field_names())

    def get_canonical(
        self,
        key: str,
        default: Any = None,
        /,
    ) -> Any:
        """Get a canonical or historical field name without raising."""

        try:
            return self[key]
        except KeyError:
            return default

    # ------------------------------------------------------------------
    # Generic mutation helpers
    # ------------------------------------------------------------------
    def set_scalar(
        self,
        prop: str,
        value: str | None,
        /,
    ) -> None:
        canonical = self._FIELD_ALIASES.get(prop, prop)

        if canonical not in self._SCALAR_TOOL_FIELDS:
            raise ValueError(
                f"{prop!r} is not a scalar tool property."
            )

        if value is None:
            setattr(self, canonical, None)
            return

        setattr(
            self,
            canonical,
            self._require_nonempty_string(canonical, value),
        )

    def modify_list(
        self,
        prop: str,
        mode: ModifyMode,
        /,
        *values: Any,
    ) -> None:
        canonical = self._FIELD_ALIASES.get(prop, prop)

        if canonical not in self._LIST_FIELDS:
            raise ValueError(
                f"{prop!r} is not a list-like property."
            )

        if mode == "set":
            setattr(
                self,
                canonical,
                self._coerce_list(canonical, values),
            )
            return

        current = list(getattr(self, canonical))

        if mode == "add":
            for value in values:
                if value not in current:
                    current.append(value)
            setattr(self, canonical, current)
            return

        if mode == "del":
            removal = list(values)
            setattr(
                self,
                canonical,
                [
                    value
                    for value in current
                    if value not in removal
                ],
            )
            return

        raise ValueError(
            f"Unsupported modification mode: {mode!r}"
        )

    def modify_dict(
        self,
        prop: str,
        mode: ModifyMode,
        /,
        *keys: str,
        **values: Any,
    ) -> None:
        canonical = self._FIELD_ALIASES.get(prop, prop)

        if canonical not in self._DICT_FIELDS:
            raise ValueError(
                f"{prop!r} is not a mapping property."
            )

        if mode == "set":
            setattr(self, canonical, deepcopy(dict(values)))
            return

        current = deepcopy(dict(getattr(self, canonical)))

        if mode == "add":
            current.update(deepcopy(values))
            setattr(self, canonical, current)
            return

        if mode == "del":
            for key in keys:
                current.pop(key, None)
            setattr(self, canonical, current)
            return

        raise ValueError(
            f"Unsupported modification mode: {mode!r}"
        )

    # ------------------------------------------------------------------
    # Compatibility setters
    # ------------------------------------------------------------------
    def set_CC(self, compiler: str | None, /) -> None:
        self.set_scalar("CC", compiler)

    def set_CXX(self, compiler: str | None, /) -> None:
        self.set_scalar("CXX", compiler)

    def set_FC(self, compiler: str | None, /) -> None:
        self.set_scalar("FC", compiler)

    def set_RC(self, compiler: str | None, /) -> None:
        self.set_scalar("RC", compiler)

    def set_CUDACXX(self, compiler: str | None, /) -> None:
        self.set_scalar("CUDACXX", compiler)

    def set_HIPCXX(self, compiler: str | None, /) -> None:
        self.set_scalar("HIPCXX", compiler)

    def set_MT(self, executable: str | None, /) -> None:
        self.set_scalar("MT", executable)

    def set_CMAKE_MT(
        self,
        executable: str | None,
        /,
    ) -> None:
        self.set_MT(executable)

    def set_PKG_CONFIG(
        self,
        executable: str | None,
        /,
    ) -> None:
        self.set_scalar("PKG_CONFIG", executable)

    def set_ENV(
        self,
        mode: ModifyMode,
        /,
        *names: str,
        **values: Any,
    ) -> None:
        self.modify_dict("ENV", mode, *names, **values)

    def set_VAR(
        self,
        mode: ModifyMode,
        /,
        *names: str,
        **values: Any,
    ) -> None:
        self.modify_dict("VAR", mode, *names, **values)

    def set_PATH(
        self,
        mode: ModifyMode,
        /,
        *values: str,
    ) -> None:
        self.modify_list("PATH", mode, *values)

    def set_INCLUDE(
        self,
        mode: ModifyMode,
        /,
        *values: str,
    ) -> None:
        self.modify_list("INCLUDE", mode, *values)

    def set_LIB(
        self,
        mode: ModifyMode,
        /,
        *values: str,
    ) -> None:
        self.modify_list("LIB", mode, *values)

    def set_CMAKE_PREFIX_PATH(
        self,
        mode: ModifyMode,
        /,
        *values: str,
    ) -> None:
        self.modify_list(
            "CMAKE_PREFIX_PATH",
            mode,
            *values,
        )

    def set_PKG_CONFIG_PATH(
        self,
        mode: ModifyMode,
        /,
        *values: str,
    ) -> None:
        self.modify_list(
            "PKG_CONFIG_PATH",
            mode,
            *values,
        )

    def set_PKG_CONFIG_LIBDIR(
        self,
        mode: ModifyMode,
        /,
        *values: str,
    ) -> None:
        self.modify_list(
            "PKG_CONFIG_LIBDIR",
            mode,
            *values,
        )

    def set_CFLAGS(
        self,
        mode: ModifyMode,
        /,
        *flags: str,
    ) -> None:
        self.modify_list("CFLAGS", mode, *flags)

    def set_CXXFLAGS(
        self,
        mode: ModifyMode,
        /,
        *flags: str,
    ) -> None:
        self.modify_list("CXXFLAGS", mode, *flags)

    def set_FCFLAGS(
        self,
        mode: ModifyMode,
        /,
        *flags: str,
    ) -> None:
        self.modify_list("FCFLAGS", mode, *flags)

    def set_FFLAGS(
        self,
        mode: ModifyMode,
        /,
        *flags: str,
    ) -> None:
        self.modify_list("FFLAGS", mode, *flags)

    def set_RCFLAGS(
        self,
        mode: ModifyMode,
        /,
        *flags: str,
    ) -> None:
        self.modify_list("RCFLAGS", mode, *flags)

    def set_CUDAFLAGS(
        self,
        mode: ModifyMode,
        /,
        *flags: str,
    ) -> None:
        self.modify_list("CUDAFLAGS", mode, *flags)

    def set_CUDACXXFLAGS(
        self,
        mode: ModifyMode,
        /,
        *flags: str,
    ) -> None:
        self.set_CUDAFLAGS(mode, *flags)

    def set_HIPFLAGS(
        self,
        mode: ModifyMode,
        /,
        *flags: str,
    ) -> None:
        self.modify_list("HIPFLAGS", mode, *flags)

    def set_HIPCXXFLAGS(
        self,
        mode: ModifyMode,
        /,
        *flags: str,
    ) -> None:
        self.set_HIPFLAGS(mode, *flags)

    def set_LDFLAGS(
        self,
        mode: ModifyMode,
        /,
        *flags: str,
    ) -> None:
        self.modify_list("LDFLAGS", mode, *flags)

    # ------------------------------------------------------------------
    # Export and copying
    # ------------------------------------------------------------------
    @staticmethod
    def _export_value(value: Any) -> Any:
        if isinstance(value, VersionNum):
            return value.original

        if isinstance(value, list):
            return [
                ModulesObject._export_value(item)
                for item in value
            ]

        if isinstance(value, tuple):
            return [
                ModulesObject._export_value(item)
                for item in value
            ]

        if isinstance(value, Mapping):
            return {
                str(key): ModulesObject._export_value(item)
                for key, item in value.items()
            }

        return deepcopy(value)

    def export(
        self,
        *,
        legacy: bool = False,
        exclude_none: bool = False,
    ) -> dict[str, Any]:
        """Export this object as a deep-copied dictionary.

        ``legacy=True`` restores historical WEMI key names.
        ``exclude_none=True`` removes unset scalar values.
        """

        result: dict[str, Any] = {}

        for spec in fields(type(self)):
            canonical_name = spec.name
            value = getattr(self, canonical_name)

            if exclude_none and value is None:
                continue

            export_name = (
                self._LEGACY_EXPORT_NAMES.get(
                    canonical_name,
                    canonical_name,
                )
                if legacy
                else canonical_name
            )

            result[export_name] = self._export_value(value)

        return result

    def copy(
        self,
        **overrides: Any,
    ) -> ModulesObject:
        return ModulesObject(self, **overrides)

    def __repr__(self) -> str:
        return (
            "ModulesObject("
            f"Module={self.Module!r}, "
            f"output={self.output!r}, "
            f"type={self.type!r}, "
            f"ver={self.ver!r}"
            ")"
        )

def modules_object_json_encoder(obj: VersionNum | ModulesObject | Path):
    if isinstance(obj, ModulesObject):
        return obj.export(legacy=True)

    if isinstance(obj, VersionNum):
        return obj.original

    if isinstance(obj, Path):
        return obj.resolve().as_posix()

    raise TypeError(
        dedent(f"""\
            Object of type {obj.__class__.__name__} is not JSON serializable.
             >>> Debug: object is {obj} """)
    )
