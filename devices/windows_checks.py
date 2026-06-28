

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
from utils import const


class WindowsCheck:
    pyver = VersionNum(tuple(sys.version_info)[0:2])
    pyitp = platform.python_implementation()
    wemiv = const.WEMI_VERSION

    def __init__(self):
        message(f" -- The Python Identification is {self.pyitp} {self.pyver}")
        wait(0.3)
        check_stat = {
            "Python Version":       self.check_python_version(self.pyver, "3.11.0", "3.15.15"),
            "Python Interps":       self.check_python_interps(allow_interps=["CPython",]),
            "Python Environ":       self.check_python_environ(),
            "Python winreg":        self.check_python_winreg(),
            "Tclsh Install":        self.check_tclsh_install(),
            "Code Page":            self.check_device_chcp(),
            "Everything Service":   self.check_everything_service(),
            "Everything CLI":       self.check_everything_cli(),
            "Envmodule version":    self.check_envmodule(),
            "wemi version":         self.check_wemi_version(),
        }

    def check_device_chcp(self):
        msg = ' -- Checking for Terminal current code page:'
        message(msg)
        c = subprocess.run('chcp', shell=True, capture_output=True, text=True, errors='ignore').stdout.strip().split(':')[-1].replace(' ', '')
        message(f'{msg:<74} -- {c}')

    def check_wemi_version(self):
        v = const.WEMI_VERSION
        message('')
        message(f' -- WEMI version: {v}')

        return v

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
            return True
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
        return True

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
            return True
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
        _1st_try = None
        message(msg)
        wait(0.3)

        q = subprocess.run(["cmd.exe", "/C", "sc query everything"], capture_output=True, text=True)

        if q.returncode == 0 and "RUNNING" in q.stdout:
            message(f"{msg:<74} -- Running")
            _1st_try = True
        else:
            message(f"{msg:<74} -- No")
            _1st_try = False

        if not _1st_try:
            message('WARNING', '[Warning] Try to install Everything service')

            # Deploy voidtools Everything
            try:
                sub_q = subprocess.run(['winget', 'install', 'voidtools.Everything'],
                                       capture_output=True, text=True)
            except PermissionError as e:
                raise PermissionError(dedent(f'''\
                        WEMI failed to install VoidTools Everything service.
                        Stop.'''))
            except Exception as e:
                raise e

            try:
                sub_r = subprocess.run(['C:/Program Files/Everything/everything.exe', '-start-service'])
            except Exception as e:
                raise e

            else:
                q = subprocess.run(["cmd.exe", "/C", "sc query everything"], capture_output=True, text=True)
                if sub_q == 0 or 2316632107:
                    message('Install complete')
                else:
                    message(dedent(f'''\
                        Install with exit code {sub_q.returncode}
                        {sub_q.stdout}
                        {sub_q.stderr}
                    '''))
            finally:
                if not (q.returncode == 0 and "RUNNING" in q.stdout):
                    message(f"{msg:<74} -- Running")
                else:
                    raise RuntimeError('WEMI failed to install VoidTools Everything service. Abort.')
        return True

    def check_everything_cli(self):
        msg = " -- Checking for Windows has Everything CLI"
        message(msg)
        wait(0.3)

        _1st_try = None

        es1 = shutil.which("es.exe")
        if es1:
            message(f"{msg:<74} -- Found")
            _1st_try = True
        else:
            message(f"{msg:<74} -- Failed")
            _1st_try = False

        if not _1st_try:
            message('WARNING', '[Warning] Try to install Everything CLI')
            try:
                sub_q = subprocess.run(['winget', 'install', 'voidtools.Everything.Cli'],
                                       capture_output=True, text=True)
            except PermissionError as e:
                raise PermissionError(dedent(f'''\
                        WEMI failed to install VoidTools Everything-CLI.
                        Stop.'''))
            except Exception as e:
                raise e
            else:
                q = subprocess.run(["cmd.exe", "/C", "sc query everything"], capture_output=True, text=True)
                if sub_q == 0 or 2316632107:
                    message('Install complete')
                else:
                    message(dedent(f'''\
                        Install with exit code {sub_q.returncode}
                        {sub_q.stdout}
                        {sub_q.stderr}
                    '''))
            finally:
                if not (q.returncode == 0 and "RUNNING" in q.stdout):
                    message(f"{msg:<74} -- Running")
                else:
                    raise RuntimeError('WEMI failed to install VoidTools Everything service. Abort.')
        return True

    def check_tclsh_install(self):
        msg = ' -- Checking for Tclsh executable'

        _1st_try = None
        tcl_ver = None

        if shutil.which('tclsh.exe'):

            tcl_ver = tcl_ver = VersionNum(subprocess.run(
                'echo puts [info patchlevel] | tclsh',
                shell=True,
                capture_output=True,
                text=True).stdout)

            _1st_try = True

        _1st_check = "Found" if _1st_try else "Failed"
        message(f"{msg:<74} -- {tcl_ver} -- {_1st_check}")


        if not _1st_try:
            message('WARNING', 'Try to install Magicsplat Tcl/Tk ...')
            try:
                sub_q = subprocess.run(['winget', 'install', 'Magicsplat.TclTk', '--force'],
                                       capture_output=True, text=True)
            except PermissionError as e:
                raise PermissionError(dedent(f'''\
                        WEMI failed to install Magicsplat Tcl/Tk.
                        Stop.'''))
            except Exception as e:
                raise e
            else:

                if sub_q.returncode == 0 or 2316632107:
                    message('Install complete')
                elif sub_q.returncode == 1063:
                    raise RuntimeError(dedent(f'''\
                        Install Magicsplat Tcl/Tk with exit code {sub_q.returncode}.
                        Please check if your device have broken Magicsplat Tcl/Tk install and clean it.
                    '''))
                else:
                    raise RuntimeError(dedent(f'''\
                        Install with exit code {sub_q.returncode}
                        {sub_q.stdout}
                        {sub_q.stderr}
                    '''))

        return True

    def check_envmodule(self):
        msg = ' -- Checking for device have Environment Modules installed'
        message(msg)
        modules_home = Path(p) if (p:=os.getenv("MODULESHOME", None)) else None
        modules_path = Path(p) if (p:=os.getenv("MODULEPATH",  None)) else None

        if modules_home and modules_path:
            files = [
                'bin/envml.cmd',
                'bin/ml.cmd',
                'bin/module.cmd',
                'init/cmd.cmd',
                'init/pwsh.ps1',
                'libexec/modulecmd.tcl'
            ]

            if all((modules_home/f).exists() for f in files):
                message(f'{msg:<74} -- {modules_home.as_posix()} -- Success')
                return True
        message(f'{msg:<74} -- {modules_home} -- Failed')
        # message(dedent(f'''\
        #         Cannot found Local machine have modules installed.
        #         You can visit https://github.com/envmodule/modules to get Windows specific release
        #             zip package and do decompress setup.
        #         '''))
