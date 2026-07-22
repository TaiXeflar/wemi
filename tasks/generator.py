# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from __future__ import annotations

import json
import math
import shutil
import sys
import time
from pathlib import Path
from textwrap import dedent
from typing import Literal

from utils import config, message, cstring
from tasks import seh

from .objects.modulesobject import ModulesObject
from .compiler import Compiler


class BuildProgress:
    """Render build progress in ninja-style or make-style output."""

    def __init__(
        self,
        total: int,
        style: Literal["ninja", "make"],
    ) -> None:
        self.total = max(total, 1)
        self.style = style
        self.interactive = sys.stdout.isatty()
        self._line_active = False

    def update(self, current: int, description: str) -> None:
        """Display the current build target."""
        if self.style == "ninja" and self.interactive:
            self._write_ninja(current, description)
            return

        # Keep redirected/CI output readable even when ninja style is selected.
        self._write_make(current, description)

    def clear(self) -> None:
        """Clear an active single-line ninja progress display."""
        if not self._line_active:
            return

        width = self._usable_width()

        if config.NO_ANSI_COLOR:
            sys.stdout.write("\r" + (" " * width) + "\r")
        else:
            sys.stdout.write("\r\033[2K")

        sys.stdout.flush()
        self._line_active = False

    def finish(self) -> None:
        """Terminate an active ninja progress line."""
        if self._line_active:
            sys.stdout.write("\n")
            sys.stdout.flush()
            self._line_active = False

    def _write_make(self, current: int, description: str) -> None:
        percentage = min(100, current * 100 // self.total)
        print(f"[{percentage:>3}%] {description}", flush=True)

    def _write_ninja(self, current: int, description: str) -> None:
        text = f"[{current}/{self.total}] {description}"
        width = self._usable_width()
        text = self._truncate(text, width)

        if config.NO_ANSI_COLOR:
            # Padding overwrites remnants from a longer previous target.
            sys.stdout.write("\r" + text.ljust(width))
        else:
            sys.stdout.write(f"\r\033[2K{text}")

        sys.stdout.flush()
        self._line_active = True

    @staticmethod
    def _usable_width() -> int:
        columns = shutil.get_terminal_size(fallback=(80, 24)).columns
        # Avoid filling the last terminal column, which can trigger wrapping.
        return max(columns - 1, 1)

    @staticmethod
    def _truncate(text: str, width: int) -> str:
        if len(text) <= width:
            return text

        if width <= 3:
            return text[:width]

        return text[: width - 3] + "..."


class Generator:
    def __init__(self):
        self.scheduler = self.schedule()

    def schedule(self):
        try:
            build_cache_list: list[ModulesObject] = [
                ModulesObject(tgt)
                for tgt in json.loads(Path("build/cache.json").read_text())
            ]
            build_schedule_dict: dict[str, ModulesObject] = {
                str(i + 1): tgt for i, tgt in enumerate(build_cache_list)
            }
        except FileNotFoundError:
            raise FileNotFoundError("Cannot Found generated build/cache.json")

        except json.JSONDecodeError:
            raise json.JSONDecodeError(
                "Cannot analyze build/cache.json with decode error"
            )

        return build_schedule_dict

    def build(self):
        failed = 0
        targets = list(self.scheduler.values())
        progress = BuildProgress(
            total=len(targets),
            style=config.GENERATOR_STYLE,
        )

        for idx, tgt in enumerate(targets, start=1):
            compiler = Compiler()

            if tgt.objtype == "File":
                description = f"Copying {tgt.MODULENAME}"
            else:
                description = (
                    f"Building {tgt.objtype} Modulefile Object {tgt.output}"
                )

            progress.update(idx, description)

            try:
                time.sleep(0.05)
                if tgt.objtype == "File":
                    compiler.copy(tgt)
                else:
                    compiler.compile(tgt)

            except KeyboardInterrupt as e:
                progress.clear()
                fail_hint = cstring("FAILED", (255, 0, 0), "BOLD")
                message("NOTICE", f"{fail_hint}: build/{tgt.MODULENAME}")

                seh.unwind(type(e), e, e.__traceback__)

                # Linux/UNIX SIGINT convention.
                sys.exit(130)

            except Exception as e:
                progress.clear()
                fail_hint = cstring("FAILED", (255, 0, 0), "BOLD")
                message("NOTICE", f"{fail_hint}: build/{tgt.MODULENAME}")
                message("ERROR", str(e))

                if not config.TOO_LONG_DIDNT_READ:
                    seh.unwind(type(e), e, e.__traceback__)

                if config.NO_COMPILE_FAIL_STOP:
                    message(
                        "ERROR",
                        dedent(f"""\
                        Warning: Modules Object {tgt.MODULENAME} compile failed with Python raised {e.__class__.__name__},
                        but wemi generator will continue with flag NO_COMPILE_FAIL_STOP is true.
                        """),
                    )
                    failed += 1
                    continue

                sys.exit(1)

        progress.finish()

        # FORCE_COMPILE_CONTINUE
        if failed:
            message("")
            message(
                "ERROR",
                dedent("""\

                WEMI generator have compilation errors while generating targeted Tcl Modulefiles.
                Please check on these information:
                 > The reported error type
                 > Your system have the correct SDK, Toolchain installation

                """).replace("compilation errors", f"{failed} compilation errors"),
            )

    def stop(self, e: Exception = None):
        message("ERROR", "Progress Terminated.")
        raise e if e else sys.exit(1)
