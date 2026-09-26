from __future__ import annotations

import sys

from dataclasses import dataclass
from threading import Lock
from typing import TextIO


_GREEN = "\x1b[32m"
_GRAY = "\x1b[90m"
_RESET = "\x1b[0m"

_CLEAR_LINE = "\x1b[2K"


@dataclass
class _ProgressState:
    name: str
    total: int
    completed: int = 0
    stage: str = ""


class ProgressTask:
    """One active row owned by a ProgressDisplay."""

    def __init__(self, display: ProgressDisplay, state: _ProgressState) -> None:
        
        self._display: ProgressDisplay = display
        self._state: _ProgressState = state
        self._closed: bool = False

    def update(self, *, completed: int | None = None, stage: str | None = None) -> None:
        if self._closed:
            return

        self._display._update(
            self._state,
            completed=completed,
            stage=stage,
        )

    def advance(self, amount: int = 1, *, stage: str | None = None) -> None:
        if self._closed:
            return

        self._display._advance(
            self._state,
            amount=amount,
            stage=stage,
        )

    def close(self) -> None:
        if self._closed:
            return

        self._display._remove(self._state)
        self._closed = True


class ProgressDisplay:
    """Owns and renders all active progress rows."""

    def __init__(self, *, width: int = 24, name_width: int = 18, stream: TextIO = sys.stdout) -> None:
        self.width: int = width
        self.name_width: int = name_width
        self.stream: TextIO = stream

        self._tasks: list[_ProgressState] = []
        self._lock: Lock = Lock()
        self._rendered_lines: int = 0

    def add(self, name: str, /, total: int, *, stage: str = "") -> ProgressTask:
        
        state = _ProgressState(
            name=name,
            total=max(total, 1),
            stage=stage,
        )

        with self._lock:
            self._tasks.append(state)
            self._render()

        return ProgressTask(self, state)

    def close(self) -> None:
        with self._lock:
            self._tasks.clear()
            self._render()

    def _update(self, state: _ProgressState, *, completed: int | None = None, stage: str | None = None) -> None:
        with self._lock:
            if completed is not None:
                state.completed = min(
                    max(completed, 0),
                    state.total,
                )

            if stage is not None:
                state.stage = stage

            self._render()

    def _advance(self, state: _ProgressState, *, amount: int, stage: str | None = None) -> None:
        with self._lock:
            state.completed = min(
                max(state.completed + amount, 0),
                state.total,
            )

            if stage is not None:
                state.stage = stage

            self._render()

    def _remove(self, state: _ProgressState) -> None:
        with self._lock:
            try:
                self._tasks.remove(state)
            except ValueError:
                return

            self._render()

    def _format_task(self, task: _ProgressState) -> str:
        ratio = task.completed / task.total

        done = round(self.width * ratio)
        remaining = self.width - done
        percent = round(ratio * 100)

        bar = (
            f"{_GREEN}{'━' * done}{_RESET}"
            f"{_GRAY}{'─' * remaining}{_RESET}"
        )

        stage = f" ({task.stage})" if task.stage else ""

        return (
            f"SDK: {task.name:<{self.name_width}} "
            f"{bar} "
            f"{percent:>3}%"
            f"{stage}"
        )

    def _render(self) -> None:
        if not self.stream.isatty():
            return

        lines = [self._format_task(task) for task in self._tasks]

        old_count = self._rendered_lines
        new_count = len(lines)

        if old_count:
            self.stream.write(f"\x1b[{old_count}A")

        for line in lines:
            self.stream.write(f"\r{_CLEAR_LINE}{line}\n")

        stale_lines = max(old_count - new_count, 0)

        for _ in range(stale_lines):
            self.stream.write(f"\r{_CLEAR_LINE}\n")

        if stale_lines:
            self.stream.write(f"\x1b[{stale_lines}A")

        self.stream.flush()
        self._rendered_lines = new_count