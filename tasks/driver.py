# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from typing import Literal
from pathlib import Path
from textwrap import dedent

from utils.functions import clear
from utils.color_string import message
from devices.windows import WindowsNT
from tasks.generator import Generator
from tasks.installer import Installer


class Driver:
    @staticmethod
    def run(task: Literal["configure", "build", "install"]):
        match task:
            case "configure":
                configure()
            case "build":
                generate()
            case "install":
                install()

            case _:
                raise RuntimeError(
                    dedent(f"""\
                        WEMI driver program recieved unspecified task {task}.
                        """)
                )


def configure():
    clear()

    try:
        device = WindowsNT()
        device.export()
    except:
        ...
    else:
        message(
            f' -- Build files have been written to: {Path('build').resolve().as_posix()}'
        )
    finally:
        ...


def generate():
    generator = Generator()
    generator.build()


def install():
    installer = Installer()
    installer.install()
