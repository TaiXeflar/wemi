

# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
import sys
import platform
import subprocess
import shutil
from pathlib import Path
from time import sleep as wait
from typing import Literal, Sequence
from textwrap import dedent

from utils.compare_functions import VersionNum, VERSION, VERSION_IN_RANGE
from utils import message


class WindowsCheck:
    pyver = VersionNum(tuple(sys.version_info)[0:2])
    pyitp = platform.python_implementation()

    def __init__(self):
        message(f" -- The Python Identification is {self.pyitp} {self.pyver}")
        wait(0.3)
        self.check_python_version(self.pyver, "3.11.0", "3.14.15")
        self.check_python_interps(
            allow_interps=[
                "CPython",
            ]
        )
        self.check_python_environ()
        self.check_python_winreg()
        self.check_everything_service()
        self.check_everything_cli()

    def check_python_version(
        self,
        tgt: VersionNum,
        ver: VersionNum | None = ...,
        MAX: VersionNum | None = ...,
        /,
    ):
        msg = " -- Checking for Python version compatiable"
        message(msg)
        wait(0.3)
        if ver and not MAX:
            _v = VERSION(ver, "<=", tgt)
        elif ver and MAX:
            _v = VERSION_IN_RANGE(ver, "<=", tgt, "<=", MAX)

        if _v:
            message(f"{msg:<60} -- {tgt:<10} -- Success")
        else:
            message(f"{msg:<60} -- {tgt:<10} -- Failed")
            message(
                "WARNING",
                dedent(f"""\
                Warning: WEMI found incompatiable Python version {tgt}. Please select another Python version.

                    traceback: Required versions is {ver} <= Version <= {MAX}, but found {tgt}"""),
            )

    def check_python_interps(
        self,
        allow_interps: Sequence[
            Literal[
                "CPython",
                "PyPy",
                "Jython",
                "IronPython",
                "MicroPython",
                "GraalPy",
                "RustPython",
            ]
        ] = ["CPython"],
    ):
        msg = " -- Checking for Python Interpreter is supported type"
        message(msg)
        wait(0.3)
        if self.pyitp not in allow_interps:
            message(f"{msg:<60} -- {self.pyitp} -- Failed")
            raise RuntimeError(
                dedent(f"""\
                WEMI has not support Python '{self.pyitp:<10}' interpreter type runtime.

                    traceback: Required Python type: {allow_interps}""")
            )
        message(f"{msg:<60} -- {self.pyitp:<10} -- Success")

    def check_python_environ(self):
        msg = " -- Checking for Python executable environment type"
        message(msg)
        wait(0.3)

        v = os.getenv("VIRTUAL_ENV")
        c = os.getenv("CONDA_PREFIX")

        if c:
            message(f"{msg:<74} -- Conda")

        if v:
            with open(Path(v) / "pyvenv.cfg") as f:
                v_content = f.read()

            if "uv" in v_content:
                message(f"{msg:<74} -- Astral UV")
            else:
                message(f"{msg:<74} -- Python VENV")
        else:
            if (Path(sys.executable).parent / "LICENSE.txt").exists():
                message(f"{msg:<74} -- Global ENV")
            else:
                message("HINT", (Path(sys.executable).parent / "LICENSE.txt"))

    def check_python_winreg(self):
        msg = " -- Checking for Python Standard Library have winreg module"
        message(msg)
        wait(0.3)

        try:
            import winreg

            message(f"{msg:<74} -- Success")
        except ImportError:
            message(f"{msg:<74} -- Failed")
            raise ImportError(
                dedent("""\
                WEMI cannot import winreg module. Please make sure your Python executable is win32
                releases. e.g. Cygwin/MSYS2 etc POSIX dependency required Python is incompatiable.""")
            )
        finally:
            pass

    def check_everything_service(self):
        msg = " -- Checking for Windows has Everything service"
        message(msg)
        wait(0.3)

        q = subprocess.run(
            ["cmd.exe", "/C", "sc query everything"], capture_output=True, text=True
        )

        if q.returncode == 0 and "RUNNING" in q.stdout:
            message(f"{msg:<74} -- Running")
        else:
            message(f"{msg:<74} -- No")
            raise RuntimeError(
                "WEMI requires voidtools Everything service. Please install it."
            )

    def check_everything_cli(self):
        msg = " -- Checking for Windows has Everything CLI"
        message(msg)
        wait(0.3)

        es1 = Path(shutil.which("es.exe"))
        es2 = Path(".deps/es.exe")
        if es1.exists():
            message(f"{msg:<74} -- Found")
        else:
            message(f"{msg:<74} -- Failed")
            msg = " -- Checking for WEMI .deps/es.exe exists\t"
            message(msg)
            if es2.exists():
                message(f"{msg:<74} -- Found")
            else:
                message(f"{msg:<74} Not Found")
                raise RuntimeError(
                    dedent(
                        "WEMI requires voidtools Everything CLI. Please download it and unzip to .deps/ folder."
                    )
                )
