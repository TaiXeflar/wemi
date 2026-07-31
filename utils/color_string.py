# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""ANSI color helpers and WEMI terminal-message output."""

from __future__ import annotations

import re
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from enum import Enum
from time import sleep
from typing import Any, ClassVar, Literal, Protocol, TextIO, TypeAlias, runtime_checkable
from warnings import warn

import utils.config as config

RGB: TypeAlias = tuple[int, int, int]
MessageMode: TypeAlias = Literal[
    "NOTICE", "REPRINT", "STATUS", "CHECK", "HINT", "WARNING",
    "ERROR", "DEPRECATED", "FATAL_ERROR",
]

ANSI_ESCAPE = "\033["
ANSI_RESET = f"{ANSI_ESCAPE}0m"
ANSI_CLEAR_LINE = f"{ANSI_ESCAPE}K"

_NAMED_COLORS: Mapping[str, RGB] = {
    "ERROR": (255, 70, 70),
    "WARNING": (184, 166, 48),
    "SUCCESS": (6, 171, 80),
    "HINT": (67, 245, 245),
    "MIKU": (57, 197, 187),
    "MIKU-PINK": (225, 40, 133),
    "ELYSIA": (255, 135, 255),
    "CYRENE": (255, 135, 255),
}

_HEX_COLOR_RE = re.compile(r"^#?(?P<hex>[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")


@runtime_checkable
class SupportsColorName(Protocol):
    color_name: str


ColorInput: TypeAlias = str | RGB | Sequence[int] | SupportsColorName | Enum


def _validate_rgb(value: Sequence[int], /) -> RGB:
    if len(value) != 3:
        raise ValueError("RGB color must contain exactly three components.")

    components: list[int] = []
    for component in value:
        if isinstance(component, bool):
            raise TypeError("RGB components must be integers, not bool.")
        try:
            integer = int(component)
        except (TypeError, ValueError) as error:
            raise TypeError(
                "RGB components must be integer-compatible; "
                f"received {component!r}."
            ) from error
        if not 0 <= integer <= 255:
            raise ValueError(
                "RGB components must be between 0 and 255; "
                f"received {integer}."
            )
        components.append(integer)

    return components[0], components[1], components[2]


def _named_color(name: str, /) -> RGB | None:
    return _NAMED_COLORS.get(name.strip().upper())


def parse_color(value: ColorInput, /) -> RGB:
    """Parse a named color, hexadecimal color, RGB sequence or status-like object."""

    if isinstance(value, str):
        text = value.strip()
        if not text:
            raise ValueError("Color name cannot be empty.")

        named = _named_color(text)
        if named is not None:
            return named

        match = _HEX_COLOR_RE.fullmatch(text)
        if match is None:
            raise ValueError(f"Invalid color: {value!r}")

        hex_value = match.group("hex")
        if len(hex_value) == 3:
            hex_value = "".join(character * 2 for character in hex_value)
        return (
            int(hex_value[0:2], 16),
            int(hex_value[2:4], 16),
            int(hex_value[4:6], 16),
        )

    if isinstance(value, SupportsColorName):
        named = _named_color(value.color_name)
        if named is not None:
            return named
        raise ValueError(f"Unknown named color: {value.color_name!r}")

    if isinstance(value, Enum):
        named = _named_color(value.name)
        if named is not None:
            return named

    object_name = getattr(value, "name", None)
    if isinstance(object_name, str):
        named = _named_color(object_name)
        if named is not None:
            return named

    if isinstance(value, Sequence) and not isinstance(
        value, (str, bytes, bytearray)
    ):
        return _validate_rgb(value)

    # Transitional compatibility with historical status objects that only
    # exposed their color name through repr(). New objects should expose
    # ``color_name`` or ``name`` instead.
    try:
        representation = repr(value)
    except Exception:
        representation = ""

    named = _named_color(representation)
    if named is not None:
        return named

    raise ValueError(f"Invalid color: {value!r}")


# Historical private name retained for internal imports.
_parse_color = parse_color


@dataclass(frozen=True, slots=True)
class ColorString:
    """A lazily rendered ANSI-colored string."""

    content: str
    rgb: RGB | None = None
    bold: bool | Literal["BOLD"] = False

    _BOLD_CODE: ClassVar[str] = "1"

    def __post_init__(self) -> None:
        if not isinstance(self.content, str):
            object.__setattr__(self, "content", str(self.content))
        if self.rgb is not None:
            object.__setattr__(self, "rgb", _validate_rgb(self.rgb))
        if self.bold not in {False, True, "BOLD"}:
            raise TypeError(
                "bold must be bool or the compatibility value 'BOLD'; "
                f"received {self.bold!r}."
            )

    @property
    def is_bold(self) -> bool:
        return self.bold is True or self.bold == "BOLD"

    def render(self, *, ansi: bool | None = None) -> str:
        if ansi is None:
            ansi = not config.NO_ANSI_COLOR
        if not ansi:
            return self.content

        codes: list[str] = []
        if self.is_bold:
            codes.append(self._BOLD_CODE)
        if self.rgb is not None:
            red, green, blue = self.rgb
            codes.append(f"38;2;{red};{green};{blue}")
        if not codes:
            return self.content

        return (
            f"{ANSI_ESCAPE}{';'.join(codes)}m"
            f"{self.content}"
            f"{ANSI_RESET}"
        )

    def __str__(self) -> str:
        return self.render()

    def __repr__(self) -> str:
        return (
            "ColorString("
            f"content={self.content!r}, rgb={self.rgb!r}, bold={self.is_bold!r}"
            ")"
        )

    def __add__(self, other: Any) -> str:
        return str(self) + str(other)

    def __radd__(self, other: Any) -> str:
        return str(other) + str(self)


def cstring(
    text: str | ColorString,
    color: ColorInput | None = None,
    bold: bool | Literal["BOLD"] = False,
) -> ColorString | str:
    """Create a lazily rendered colored string.

    Plain, unstyled text remains ``str`` for compatibility.
    """

    raw_text = text.content if isinstance(text, ColorString) else str(text)
    if color is None and not bold:
        return raw_text

    rgb = None if color is None else parse_color(color)
    return ColorString(raw_text, rgb=rgb, bold=bold)


def _stream_supports_ansi(stream: TextIO, /) -> bool:
    if config.NO_ANSI_COLOR:
        return False
    isatty = getattr(stream, "isatty", None)
    if callable(isatty):
        try:
            return bool(isatty())
        except OSError:
            return False
    return False


def _print_colored(text: Any, color: ColorInput, *, stream: TextIO) -> None:
    rendered = ColorString(
        str(text), rgb=parse_color(color)
    ).render(ansi=_stream_supports_ansi(stream))
    print(rendered, file=stream)


def message(
    mode: MessageMode | str,
    text: Any | None = None,
    latency: float = 0.05,
    *,
    stream: TextIO | None = None,
    exit_code: int = 1,
) -> None:
    """Print a WEMI terminal message.

    The historical positional interface remains supported. ``stream`` and
    ``exit_code`` are keyword-only for testing and output redirection.
    """

    if stream is None:
        stream = sys.stdout
    if text is None:
        text = mode
        mode = "NOTICE"

    normalized_mode = str(mode).upper()
    if latency < 0:
        raise ValueError("latency cannot be negative.")

    if normalized_mode == "NOTICE":
        print(str(text), file=stream)
        return

    if normalized_mode == "REPRINT":
        clear_line = ANSI_CLEAR_LINE if _stream_supports_ansi(stream) else ""
        print(f"\r{text}", end=clear_line, flush=True, file=stream)
        return

    if normalized_mode in {"STATUS", "CHECK"}:
        if latency:
            sleep(latency)
        formatted = f" -- {text}:"
        print(f"{formatted:<60}", flush=True, file=stream)
        if latency:
            sleep(latency)
        return

    if normalized_mode in {"HINT", "WARNING", "ERROR"}:
        _print_colored(text, normalized_mode, stream=stream)
        return

    if normalized_mode == "DEPRECATED":
        warn(str(text), DeprecationWarning, stacklevel=2)
        return

    if normalized_mode == "FATAL_ERROR":
        _print_colored(text, "ERROR", stream=stream)
        _print_colored("Progress Terminated.", "ERROR", stream=stream)
        raise SystemExit(exit_code)

    raise ValueError(f"Invalid message mode {mode!r}.")
