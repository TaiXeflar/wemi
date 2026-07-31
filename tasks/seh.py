# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""Structured exception handling and compiler-style diagnostics for WEMI."""

from __future__ import annotations

import difflib
import re
import sys
import traceback
from dataclasses import dataclass
from pathlib import Path
from types import TracebackType
from typing import Literal, TextIO, TypeAlias

from utils import cstring, message
from utils import config


SEHStyle: TypeAlias = Literal[
    "python",
    "default",
    "gcc",
    "clang",
    "msvc",
]

_SUPPORTED_STYLES = frozenset(
    {"python", "default", "gcc", "clang", "msvc"}
)

_UNKNOWN_FIELD_RE = re.compile(
    r"Unknown\s+(?P<object>[A-Za-z_][A-Za-z0-9_]*)\s+"
    r"field(?:\(s\))?:\s*(?P<fields>.+)",
    re.IGNORECASE,
)
_UNEXPECTED_KEYWORD_RE = re.compile(
    r"unexpected keyword argument ['\"](?P<name>[^'\"]+)['\"]",
    re.IGNORECASE,
)
_NAME_ERROR_RE = re.compile(
    r"name ['\"](?P<name>[^'\"]+)['\"] is not defined",
    re.IGNORECASE,
)
_ATTRIBUTE_ERROR_RE = re.compile(
    r"object has no attribute ['\"](?P<name>[^'\"]+)['\"]",
    re.IGNORECASE,
)


@dataclass(frozen=True, slots=True)
class DiagnosticFrame:
    """Normalized traceback frame for compiler-style output."""

    filename: str
    lineno: int
    column: int | None
    end_column: int | None
    function: str
    source: str
    is_origin: bool

    @property
    def location(self) -> str:
        if self.column is None:
            return f"{self.filename}:{self.lineno}"
        return f"{self.filename}:{self.lineno}:{self.column}"

    @property
    def msvc_location(self) -> str:
        if self.column is None:
            return f"{self.filename}({self.lineno})"
        return f"{self.filename}({self.lineno},{self.column})"

    @property
    def caret_line(self) -> str:
        if not self.source or self.column is None:
            return ""

        start = max(self.column - 1, 0)
        end = self.end_column or self.column
        width = max(end - self.column, 1)
        return (" " * start) + ("^" * width)


def _normalize_style(value: str) -> SEHStyle:
    style = value.strip().lower()

    if style not in _SUPPORTED_STYLES:
        raise ValueError(
            f"Unsupported SEH style {value!r}. "
            f"Expected one of: {', '.join(sorted(_SUPPORTED_STYLES))}."
        )

    return style  # type: ignore[return-value]


def _display_filename(filename: str) -> str:
    if filename.startswith("<") and filename.endswith(">"):
        return filename

    try:
        return Path(filename).resolve().as_posix()
    except (OSError, RuntimeError):
        return Path(filename).as_posix()


def _collect_frames(
    exception: BaseException,
) -> list[DiagnosticFrame]:
    trace = traceback.TracebackException.from_exception(
        exception,
        capture_locals=False,
    )
    stack = list(trace.stack)
    result: list[DiagnosticFrame] = []

    for index, frame in enumerate(stack):
        column = (
            frame.colno + 1
            if frame.colno is not None
            else None
        )
        end_column = (
            frame.end_colno + 1
            if frame.end_colno is not None
            else None
        )

        result.append(
            DiagnosticFrame(
                filename=_display_filename(frame.filename),
                lineno=frame.lineno,
                column=column,
                end_column=end_column,
                function=(
                    "global scope"
                    if frame.name == "<module>"
                    else frame.name
                ),
                source=(frame.line or "").rstrip(),
                is_origin=index == len(stack) - 1,
            )
        )

    return result


def _exception_message(exception: BaseException) -> str:
    text = str(exception).strip()

    if text:
        return f"{type(exception).__name__}: {text}"

    return type(exception).__name__


def _candidate_names(exception: BaseException) -> list[str]:
    """Read explicit suggestion candidates from an exception.

    Supported attributes:
    - ``suggestions``
    - ``candidates``

    This avoids inventing candidates by scanning unrelated runtime state.
    """

    candidates = getattr(exception, "suggestions", None)

    if candidates is None:
        candidates = getattr(exception, "candidates", None)

    if candidates is None:
        return []

    try:
        return [
            str(item)
            for item in candidates
            if str(item)
        ]
    except TypeError:
        return []


def _misspelled_name(exception: BaseException) -> str | None:
    text = str(exception)

    for pattern in (
        _UNEXPECTED_KEYWORD_RE,
        _NAME_ERROR_RE,
        _ATTRIBUTE_ERROR_RE,
    ):
        match = pattern.search(text)
        if match is not None:
            return match.group("name")

    match = _UNKNOWN_FIELD_RE.search(text)
    if match is None:
        return None

    first = match.group("fields").split(",", 1)[0]
    return first.strip().strip("'\"")


def _clang_suggestion(exception: BaseException) -> str | None:
    """Create a conservative Clang-style ``Did you mean`` suggestion."""

    bad_name = _misspelled_name(exception)
    candidates = _candidate_names(exception)

    if bad_name is None or not candidates:
        return None

    matches = difflib.get_close_matches(
        bad_name,
        candidates,
        n=1,
        cutoff=0.72,
    )

    if not matches:
        return None

    return f"Did you mean {matches[0]!r}?"


def _write_source(
    frame: DiagnosticFrame,
    *,
    stream: TextIO,
    color: str,
) -> None:
    if not frame.source:
        return

    print(frame.source, file=stream)

    if frame.caret_line:
        print(
            cstring(
                frame.caret_line,
                color,
                bold=True,
            ),
            file=stream,
        )


def _render_gcc(
    exception: BaseException,
    frames: list[DiagnosticFrame],
    *,
    stream: TextIO,
) -> None:
    print(file=stream)
    print(
        cstring(
            "Python traceback (most recent call last): "
            + _exception_message(exception),
            "ERROR",
        ),
        file=stream,
    )

    for frame in frames:
        if frame.is_origin:
            diagnostic = cstring(
                f"error: {_exception_message(exception)}",
                "ERROR",
                bold=True,
            )
            color = "ERROR"
        else:
            diagnostic = (
                f"{cstring('note:', 'HINT', bold=True)} "
                "called from here"
            )
            color = "HINT"

        function = cstring(
            frame.function,
            bold=True,
        )

        print(
            f"In Python file {frame.filename}: "
            f"In function {function}()",
            file=stream,
        )
        print(
            f"{frame.location}: {diagnostic}",
            file=stream,
        )

        if frame.source:
            print(
                f"{frame.lineno:5} | {frame.source}",
                file=stream,
            )

            if frame.caret_line:
                print(
                    "      | "
                    + str(
                        cstring(
                            frame.caret_line,
                            color,
                            bold=True,
                        )
                    ),
                    file=stream,
                )

        print(file=stream)


def _render_clang(
    exception: BaseException,
    frames: list[DiagnosticFrame],
    *,
    stream: TextIO,
) -> None:
    print(file=stream)

    for frame in frames:
        if frame.is_origin:
            diagnostic = cstring(
                f"error: {_exception_message(exception)}",
                "ERROR",
                bold=True,
            )
            color = "ERROR"
        else:
            diagnostic = (
                f"{cstring('note:', 'HINT', bold=True)} "
                "called from here"
            )
            color = "HINT"

        print(
            f"{frame.location}: {diagnostic}",
            file=stream,
        )
        _write_source(
            frame,
            stream=stream,
            color=color,
        )

        if frame.is_origin:
            suggestion = _clang_suggestion(exception)

            if suggestion is not None:
                print(
                    f"{frame.location}: "
                    f"{cstring('note:', 'HINT', bold=True)} "
                    f"{suggestion}",
                    file=stream,
                )

        print(file=stream)


def _render_msvc(
    exception: BaseException,
    frames: list[DiagnosticFrame],
    *,
    stream: TextIO,
) -> None:
    print("Python traceback:", file=stream)

    for frame in frames:
        if frame.is_origin:
            diagnostic = cstring(
                f"error: {_exception_message(exception)}",
                "ERROR",
                bold=True,
            )
            color = "ERROR"
        else:
            diagnostic = (
                f"{cstring('note:', 'HINT', bold=True)} "
                "called from here"
            )
            color = "HINT"

        print(
            f"{frame.msvc_location}: {diagnostic}",
            file=stream,
        )
        _write_source(
            frame,
            stream=stream,
            color=color,
        )
        print(file=stream)


def render_exception(
    exception: BaseException,
    *,
    style: SEHStyle | str,
    stream: TextIO | None = None,
) -> None:
    """Render an exception without terminating the process."""

    if stream is None:
        stream = sys.stderr

    normalized_style = _normalize_style(style)

    if normalized_style in {"python", "default"}:
        traceback.print_exception(
            type(exception),
            exception,
            exception.__traceback__,
            file=stream,
        )
        return

    frames = _collect_frames(exception)

    if normalized_style == "gcc":
        _render_gcc(
            exception,
            frames,
            stream=stream,
        )
        return

    if normalized_style == "clang":
        _render_clang(
            exception,
            frames,
            stream=stream,
        )
        return

    _render_msvc(
        exception,
        frames,
        stream=stream,
    )


def unwind(
    exc_type: type[BaseException],
    exc_value: BaseException,
    tb: TracebackType | None,
) -> None:
    """WEMI ``sys.excepthook`` implementation.

    The historical name is retained. Python's original traceback is used
    directly; no synthetic traceback frames or pseudo error codes are added.
    """

    if isinstance(exc_value, KeyboardInterrupt):
        message(
            "ERROR",
            "WEMI stopped "
            f"{config.DEFAULT_TASK.capitalize()} process after receiving "
            "a keyboard interrupt (Ctrl+C).",
            stream=sys.stderr,
        )
        raise SystemExit(130)

    style = _normalize_style(config.SEH_STYLE)

    if style in {"python", "default"}:
        sys.__excepthook__(
            exc_type,
            exc_value,
            tb,
        )
        return

    if tb is not None and exc_value.__traceback__ is not tb:
        exc_value = exc_value.with_traceback(tb)

    render_exception(
        exc_value,
        style=style,
        stream=sys.stderr,
    )


def setup_excepthook() -> None:
    """Install WEMI's structured exception hook."""

    sys.excepthook = unwind
