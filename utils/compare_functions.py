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
from typing import Any, Literal, Self, TypeAlias, overload


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

# VersionNum intentionally models vendor/toolchain numeric versions rather
# than SemVer or PEP 440 versions.
#
# The pattern searches for the first numeric version in a string to preserve
# compatibility with existing WEMI callers such as:
#   "CUDA Version 13.0"
#   "MSVC 14.51.36231_v145"
_VERSION_SEARCH_PATTERN = re.compile(
    r"(?P<numeric>\d+(?:\.\d+)*)(?P<suffix>[^\s]*)"
)


@total_ordering
@dataclass(frozen=True, slots=True, init=False)
class VersionNum:
    """Immutable numeric vendor/toolchain version.

    ``VersionNum`` preserves the original input text while extracting an
    arbitrary number of numeric components for comparisons.

    Comparison ignores suffix text and treats trailing zero components as
    insignificant. Therefore ``1.2``, ``1.2.0`` and ``1.2.0.0`` compare equal.

    This is not a SemVer or PEP 440 parser.
    """

    original: str
    parts: tuple[int, ...]
    suffix: str

    def __init__(
        self,
        version_input: VersionNum | str | Sequence[int | str | None],
        /,
    ) -> None:
        if isinstance(version_input, VersionNum):
            original = version_input.original
            parts = version_input.parts
            suffix = version_input.suffix
        elif isinstance(version_input, str):
            original, parts, suffix = self._parse_string(version_input)
        elif isinstance(version_input, Sequence) and not isinstance(
            version_input,
            (str, bytes, bytearray),
        ):
            original, parts, suffix = self._parse_sequence(version_input)
        else:
            raise TypeError(
                "VersionNum expects a version string, a sequence of numeric "
                "components, or another VersionNum; received "
                f"{type(version_input).__name__}."
            )

        object.__setattr__(self, "original", original)
        object.__setattr__(self, "parts", parts)
        object.__setattr__(self, "suffix", suffix)

    @staticmethod
    def _parse_string(
        value: str,
    ) -> tuple[str, tuple[int, ...], str]:
        original = value.strip()

        if not original:
            raise ValueError("Version string cannot be empty.")

        match = _VERSION_SEARCH_PATTERN.search(original)
        if match is None:
            raise ValueError(
                f"No numeric version could be found in {value!r}."
            )

        parts = tuple(
            int(component)
            for component in match.group("numeric").split(".")
        )
        suffix = match.group("suffix").strip("._-+ ")

        return original, parts, suffix

    @staticmethod
    def _parse_sequence(
        value: Sequence[int | str | None],
    ) -> tuple[str, tuple[int, ...], str]:
        if not value:
            raise ValueError("Version sequence cannot be empty.")

        parts: list[int] = []

        for component in value:
            if component is None:
                parts.append(0)
                continue

            try:
                integer = int(component)
            except (TypeError, ValueError) as error:
                raise ValueError(
                    "Version sequence must contain only integer-compatible "
                    f"components; received {component!r}."
                ) from error

            if integer < 0:
                raise ValueError(
                    "Version components cannot be negative; "
                    f"received {integer}."
                )

            parts.append(integer)

        original = ".".join(str(component) for component in parts)
        return original, tuple(parts), ""

    @classmethod
    def try_parse(
        cls,
        value: Any,
        /,
    ) -> Self | None:
        """Return a parsed version or ``None`` for unsupported/invalid input."""

        try:
            return cls(value)
        except (TypeError, ValueError):
            return None

    @classmethod
    def search(
        cls,
        text: str,
        /,
    ) -> Self | None:
        """Search arbitrary text for its first numeric version."""

        return cls.try_parse(text)

    @property
    def comparison_key(self) -> tuple[int, ...]:
        """Numeric comparison key with insignificant trailing zeros removed."""

        parts = list(self.parts)
        while len(parts) > 1 and parts[-1] == 0:
            parts.pop()
        return tuple(parts)

    @property
    def normalized(self) -> str:
        """Return all parsed numeric components joined by dots."""

        return ".".join(str(component) for component in self.parts)

    @property
    def major(self) -> int:
        return self.parts[0] if self.parts else 0

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
    def fullname(self) -> str:
        """Compatibility alias for the historical API."""

        return self.original

    @property
    def valid(self) -> bool:
        """Compatibility property.

        Invalid versions are no longer represented by a VersionNum instance;
        construction raises ``TypeError`` or ``ValueError`` instead.
        """

        return True

    def starts_with(
        self,
        other: VersionNum | str | Sequence[int | str | None],
        /,
    ) -> bool:
        """Return whether this numeric version starts with another version."""

        prefix = VersionNum(other).parts
        return self.parts[: len(prefix)] == prefix

    @staticmethod
    def _coerce_other(other: object) -> VersionNum | None:
        if isinstance(other, VersionNum):
            return other

        if isinstance(other, str):
            return VersionNum.try_parse(other)

        if isinstance(other, Sequence) and not isinstance(
            other,
            (str, bytes, bytearray),
        ):
            return VersionNum.try_parse(other)

        return None

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
        # Objects that compare equal must have the same hash.
        return hash(self.comparison_key)

    def __str__(self) -> str:
        # Preserve vendor suffixes and the original display spelling.
        return self.original

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.original!r})"

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

    if obj is None or compare is None:
        return False

    operation = _VERSION_OPERATORS.get(op)
    if operation is None:
        raise ValueError(f"Unsupported version operator: {op!r}")

    try:
        left = VersionNum(obj)
        right = VersionNum(compare)
    except (TypeError, ValueError):
        return False

    result = operation(left, right)

    if result and blacklist is not None:
        return VERSION_BLACKLIST(
            left,
            blacklist,
            fuzzy=fuzzy,
        )

    return result


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

    if version is None:
        return False

    if not VERSION(minimum, op1, version):
        return False

    if not VERSION(version, op2, maximum):
        return False

    if blacklist is not None:
        return VERSION_BLACKLIST(
            version,
            blacklist,
            fuzzy=fuzzy,
        )

    return True


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

    if version is None:
        return False

    in_safe_zone = (
        VERSION(version, op1, minimum)
        or VERSION(version, op2, maximum)
    )

    if not in_safe_zone:
        return False

    if blacklist is not None:
        return VERSION_BLACKLIST(
            version,
            blacklist,
            fuzzy=fuzzy,
        )

    return True


def VERSION_WHITELIST(
    version: str | VersionNum,
    find_list: Iterable[str | VersionNum],
    /,
    *,
    compatibility: CompatibilityMode = "STRICT",
) -> bool:
    """Return whether a version matches the requested compatibility policy.

    ``STRICT`` compares the full numeric version.
    ``MINOR`` compares major and minor components.
    ``MAJOR`` compares only the major component.
    ``FUZZY`` performs a numeric prefix comparison.
    """

    if version is None:
        return False

    target = VersionNum.try_parse(version)
    if target is None:
        return False

    mode = compatibility.upper()
    if mode not in {"STRICT", "MINOR", "MAJOR", "FUZZY"}:
        raise ValueError(
            f"Unsupported compatibility mode: {compatibility!r}"
        )

    for raw_item in find_list:
        item = VersionNum.try_parse(raw_item)
        if item is None:
            continue

        if mode == "STRICT" and target == item:
            return True

        if mode == "MINOR" and (
            target.major,
            target.minor,
        ) == (
            item.major,
            item.minor,
        ):
            return True

        if mode == "MAJOR" and target.major == item.major:
            return True

        if mode == "FUZZY" and target.starts_with(item):
            return True

    return False


def VERSION_BLACKLIST(
    version: str | VersionNum,
    prohibited: Iterable[str | VersionNum],
    /,
    *,
    fuzzy: bool = False,
) -> bool:
    """Return ``False`` when a version appears in the prohibited list.

    With ``fuzzy=True``, prohibited entries are treated as numeric prefixes.
    """

    if version is None:
        return False

    target = VersionNum.try_parse(version)
    if target is None:
        return False

    for raw_item in prohibited:
        item = VersionNum.try_parse(raw_item)
        if item is None:
            continue

        if fuzzy:
            if target.starts_with(item):
                return False
        elif target == item:
            return False

    return True


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
