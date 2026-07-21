# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from typing import Literal
from pathlib import Path
from textwrap import dedent

from utils import config
from utils.functions import clear
from utils.color_string import message

from tasks.generator import Generator
from tasks.installer import Installer


class Driver:
    @staticmethod
    def run(task: Literal["configure", "build", "install"]):
        match task:
            case "configure":
                configure()

                if config.ALL_IN_ONE:
                    generate()
                    install()

            case "build":
                generate()

            case "install":
                install()

            case _:
                raise RuntimeError(dedent(f"""\
                        WEMI driver program received unspecified task {task}.
                        """
                    )
                )

def configure():
    clear()

    try:
        from devices.windows import WindowsNT

        device = WindowsNT(config.MODULES_ONLY)
        device.export()
    except Exception as e:
        raise e
    else:
        b = Path('build').resolve().as_posix()
        message(
            f' -- Build files have been written to: {b}'
        )

def generate():
    generator = Generator()
    generator.build()


def install():
    installer = Installer()
    installer.install()
