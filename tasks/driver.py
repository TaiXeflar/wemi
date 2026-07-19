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
        if config.ALL_IN_ONE:
            generate()
            install()

def configure():
    clear()

    try:
        device = WindowsNT(config.MODULES_ONLY)
        device.export()
    except Exception as e:
        from tasks import seh
        # 把被吞掉的錯誤交給你的錯誤處理器印出來
        seh.unwind(type(e), e, e.__traceback__)
    else:
        b = Path('build').resolve().as_posix()
        message(
            f' -- Build files have been written to: {b}'
        )
    finally:
        ...


def generate():
    generator = Generator()
    generator.build()


def install():
    installer = Installer()
    installer.install()
