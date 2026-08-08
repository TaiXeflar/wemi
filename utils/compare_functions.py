
# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from functools import total_ordering
from operator import eq, ge, gt, le, lt, ne
from typing import Any, Literal, TypeAlias, overload


VersionInput: TypeAlias = (
    "VersionNum | str | Sequence[int | str | None]"
)
VersionOperator: TypeAlias = Literal[
    "=",
    "≠",
    "!=",
    "<",
    "<=",
    ">",
    ">=",
]
CompatibilityMode: TypeAlias = Literal[
    "STRICT",
    "MINOR",
    "MAJOR",
    "FUZZY",
]

# VersionNum models vendor/toolchain numeric versions rather than SemVer or
# PEP 440 versions. Search the first numeric version token from arbitrary text:
#   "CUDA Version 13.0"       -> "13.0"
#   "MSVC 14.51.36231_v145"  -> "14.51.36231_v145"
_VERSION_SEARCH_PATTERN = re.compile(
    r"(?P<numeric>\d+(?:\.\d+)*)(?P<suffix>[^\s]*)"
)


@total_ordering
@dataclass(frozen=True, slots=True, init=False)
class VersionNum:
    """Immutable vendor/toolchain numeric version.

    The source text is retained for compatibility/debugging, while ``str()``
    returns only the version token parsed from that source.

    Comparison uses numeric components only, ignores suffix text, and treats
    trailing zeros as insignificant. Therefore ``1.2``, ``1.2.0`` and
    ``1.2.0.0`` compare equal.

    This is not a SemVer or PEP 440 parser.
    """

    source: str
    value: str
    parts: tuple[int, ...]
    suffix: str

    def __init__(self, version_input: VersionInput, /) -> None:
        if isinstance(version_input, VersionNum):
            source = version_input.source
            value = version_input.value
            parts = version_input.parts
            suffix = version_input.suffix

        elif isinstance(version_input, str):
            source = version_input.strip()
            if not source:
                raise ValueError("Version string cannot be empty.")

            match = _VERSION_SEARCH_PATTERN.search(source)
            if match is None:
                raise ValueError(
                    f"No numeric version could be found in {version_input!r}."
                )

            value = match.group(0)
            parts = tuple(
                int(component)
                for component in match.group("numeric").split(".")
            )
            suffix = match.group("suffix").strip("._-+ ")

        elif isinstance(version_input, Sequence) and not isinstance(
            version_input,
            (str, bytes, bytearray),
        ):
            if not version_input:
                raise ValueError("Version sequence cannot be empty.")

            parsed: list[int] = []
            for component in version_input:
                if component is None:
                    parsed.append(0)
                    continue

                try:
                    number = int(component)
                except (TypeError, ValueError) as error:
                    raise ValueError(
                        "Version sequence must contain only integer-compatible "
                        f"components; received {component!r}."
                    ) from error

                if number < 0:
                    raise ValueError(
                        "Version components cannot be negative; "
                        f"received {number}."
                    )

                parsed.append(number)

            parts = tuple(parsed)
            value = ".".join(map(str, parts))
            source = value
            suffix = ""

        else:
            raise TypeError(
                "VersionNum expects a version string, a sequence of numeric "
                "components, or another VersionNum; received "
                f"{type(version_input).__name__}."
            )

        object.__setattr__(self, "source", source)
        object.__setattr__(self, "value", value)
        object.__setattr__(self, "parts", parts)
        object.__setattr__(self, "suffix", suffix)

    @classmethod
    def try_parse(cls, value: Any, /) -> VersionNum | None:
        """Return a parsed version or ``None`` for unsupported/invalid input."""

        try:
            return cls(value)
        except (TypeError, ValueError):
            return None

    @classmethod
    def search(cls, text: str, /) -> VersionNum | None:
        """Search arbitrary text for its first numeric version."""

        return cls.try_parse(text)

    @property
    def comparison_key(self) -> tuple[int, ...]:
        """Numeric key with insignificant trailing zeros removed."""

        end = len(self.parts)
        while end > 1 and self.parts[end - 1] == 0:
            end -= 1
        return self.parts[:end]

    @property
    def normalized(self) -> str:
        """Return only numeric components joined by dots."""

        return ".".join(map(str, self.parts))

    @property
    def major(self) -> int:
        return self.parts[0]

    @property
    def minor(self) -> int:
        return self.parts[1] if len(self.parts) > 1 else 0

    @property
    def patch(self) -> int:
        return self.parts[2] if len(self.parts) > 2 else 0

    @property
    def version_tuple(self) -> tuple[int, ...]:
        return self.parts

    @property
    def verTuple(self) -> tuple[int, ...]:
        """Compatibility alias for the historical API."""

        return self.parts

    @property
    def original(self) -> str:
        """Compatibility alias for the original source text."""

        return self.source

    @property
    def fullname(self) -> str:
        """Compatibility alias for the historical API."""

        return self.source

    @property
    def valid(self) -> bool:
        """Compatibility property; constructed VersionNum objects are valid."""

        return True

    def starts_with(self, other: VersionInput, /) -> bool:
        """Return whether this numeric version starts with another version."""

        prefix = VersionNum(other).parts
        return self.parts[: len(prefix)] == prefix

    @staticmethod
    def _coerce_other(other: object) -> VersionNum | None:
        if isinstance(other, VersionNum):
            return other
        return VersionNum.try_parse(other)

    def __eq__(self, other: object) -> bool:
        converted = self._coerce_other(other)
        if converted is None:
            return False
        return self.comparison_key == converted.comparison_key

    def __lt__(self, other: object) -> bool:
        converted = self._coerce_other(other)
        if converted is None:
            return NotImplemented
        return self.comparison_key < converted.comparison_key

    def __hash__(self) -> int:
        return hash(self.comparison_key)

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.value!r})"

    def __format__(self, format_spec: str) -> str:
        return format(str(self), format_spec)


_VERSION_OPERATORS = {
    "=": eq,
    "≠": ne,
    "!=": ne,
    "<": lt,
    "<=": le,
    ">": gt,
    ">=": ge,
}


def VERSION(
    obj: VersionNum | str,
    op: VersionOperator,
    compare: VersionNum | str,
    /,
    *,
    blacklist: Iterable[str | VersionNum] | None = None,
    fuzzy: bool = False,
) -> bool:
    """Compare two versions and optionally reject blacklisted versions."""

    operation = _VERSION_OPERATORS.get(op)
    if operation is None:
        raise ValueError(f"Unsupported version operator: {op!r}")

    left = VersionNum.try_parse(obj)
    right = VersionNum.try_parse(compare)
    if left is None or right is None:
        return False

    result = operation(left, right)
    return (
        VERSION_BLACKLIST(left, blacklist, fuzzy=fuzzy)
        if result and blacklist is not None
        else result
    )


def VERSION_IN_RANGE(
    minimum: str | VersionNum,
    op1: Literal["<", "<="],
    version: str | VersionNum,
    op2: Literal["<", "<="],
    maximum: str | VersionNum,
    /,
    *,
    blacklist: Iterable[str | VersionNum] | None = None,
    fuzzy: bool = False,
) -> bool:
    """Return whether ``minimum op1 version op2 maximum`` is true."""

    if not (
        VERSION(minimum, op1, version)
        and VERSION(version, op2, maximum)
    ):
        return False

    return (
        VERSION_BLACKLIST(version, blacklist, fuzzy=fuzzy)
        if blacklist is not None
        else True
    )


def VERSION_EXCLUDE_RANGE(
    version: str | VersionNum,
    op1: Literal["<", "<="],
    minimum: str | VersionNum,
    op2: Literal[">", ">="],
    maximum: str | VersionNum,
    /,
    *,
    blacklist: Iterable[str | VersionNum] | None = None,
    fuzzy: bool = False,
) -> bool:
    """Return whether a version lies outside an excluded range."""

    if not (
        VERSION(version, op1, minimum)
        or VERSION(version, op2, maximum)
    ):
        return False

    return (
        VERSION_BLACKLIST(version, blacklist, fuzzy=fuzzy)
        if blacklist is not None
        else True
    )


def _version_matches(
    target: VersionNum,
    item: VersionNum,
    mode: CompatibilityMode,
) -> bool:
    if mode == "STRICT":
        return target == item
    if mode == "MINOR":
        return (target.major, target.minor) == (item.major, item.minor)
    if mode == "MAJOR":
        return target.major == item.major
    if mode == "FUZZY":
        return target.starts_with(item)
    raise ValueError(f"Unsupported compatibility mode: {mode!r}")


def VERSION_WHITELIST(
    version: str | VersionNum,
    find_list: Iterable[str | VersionNum],
    /,
    *,
    compatibility: CompatibilityMode = "STRICT",
) -> bool:
    """Return whether a version matches the requested compatibility policy."""

    target = VersionNum.try_parse(version)
    if target is None:
        return False

    mode = compatibility.upper()
    if mode not in {"STRICT", "MINOR", "MAJOR", "FUZZY"}:
        raise ValueError(
            f"Unsupported compatibility mode: {compatibility!r}"
        )

    return any(
        _version_matches(target, item, mode)
        for raw_item in find_list
        if (item := VersionNum.try_parse(raw_item)) is not None
    )


def VERSION_BLACKLIST(
    version: str | VersionNum,
    prohibited: Iterable[str | VersionNum],
    /,
    *,
    fuzzy: bool = False,
) -> bool:
    """Return ``False`` when a version appears in the prohibited list."""

    target = VersionNum.try_parse(version)
    if target is None:
        return False

    return not any(
        (
            target.starts_with(item)
            if fuzzy
            else target == item
        )
        for raw_item in prohibited
        if (item := VersionNum.try_parse(raw_item)) is not None
    )


@overload
def STREQUAL(obj1: str, obj2: str) -> bool: ...


@overload
def STREQUAL(obj1: VersionNum, obj2: VersionNum) -> bool: ...


def STREQUAL(
    obj1: str | VersionNum,
    obj2: str | VersionNum,
) -> bool:
    if obj1 is None or obj2 is None:
        return False

    if isinstance(obj1, VersionNum) or isinstance(obj2, VersionNum):
        left = VersionNum.try_parse(obj1)
        right = VersionNum.try_parse(obj2)
        return (
            left is not None
            and right is not None
            and left == right
        )

    return str(obj1) == str(obj2)


@overload
def STRMATCH(obj: str, find: str) -> bool: ...


@overload
def STRMATCH(
    obj: str,
    find: Iterable[str],
) -> bool: ...


def STRMATCH(
    obj: str,
    find: str | Iterable[str],
) -> bool:
    target = str(obj)

    if isinstance(find, str):
        return find in target

    return any(str(keyword) in target for keyword in find)
