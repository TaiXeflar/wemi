# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from pathlib import Path
import argparse
import sys

from . import config
from .functions import *


def args_update():
    class CustomFormatter(argparse.HelpFormatter):
        def __init__(self, prog):

            super().__init__(prog, max_help_position=100, width=150)

    parser = argparse.ArgumentParser(
        description="Windows Environment Modulefile Installer help message",
        add_help=False,
        prefix_chars="-/",
        formatter_class=CustomFormatter,
    )

    options_general = parser.add_argument_group("General options")
    options_config  = parser.add_argument_group("Configure options")
    options_build   = parser.add_argument_group("Build options")
    options_install = parser.add_argument_group("Install options")
    options_exprmnt = parser.add_argument_group("Experiment options")

    options_general.add_argument(
        "DEFAULT_TASK",
        type=str,
        choices=["configure", "build", "install"],
        metavar="<task>",
        help="Specify the task to execute: configure, build, or install"
    )

    options_general.add_argument(
        "--help",
        "-help",
        "/help",
        "-?",
        "/?",
        action="store_true",
        help="Show this help message and exit",
    )
    options_general.add_argument(
        "--seh",
        '-seh',
        '/seh',
        '-DSEH_STYLE',
        type=str,
        choices=['python', 'gcc', 'msvc', 'clang'],
        # metavar='<seh>',
        dest='SEH_STYLE',
        help='Select Error exception style',
    )
    options_general.add_argument(
        '-L',
        '-l',
        type=str,
        choices=['auto', 'local', 'tw', 'en'],
        default=argparse.SUPPRESS,
        dest='LOCALE',
        help='WEMI project localized language'
    )
    options_general.add_argument(
        "--cls",
        '-cls',
        '/cls',
        action="store_true",
        dest="CLEAR_HOST",
        help="Enable clear terminal and output",
    )
    options_general.add_argument(
        "--no-color",
        '-DNO_ANSI_COLOR',
        action="store_true",
        dest="NO_ANSI_COLOR",
        help="Disable ANSI escape coded colot string output",
    )
    options_config.add_argument(
        "--sdks",
        "-sdks",
        '--projects',
        '--project',
        '-DENABLED_SDKS',
        nargs="+",
        type=str,
        dest="ENABLE_SDKS",
        default=[],
        help="Specify which SDKs to configure. If empty, configure all."
    )
    options_config.add_argument(
        "--tldr",
        "-tldr",
        '/tldr',
        action="store_true",
        dest="TOO_LONG_DIDNT_READ",
        default=argparse.SUPPRESS,
        help="Disable Fail error seh messages",
    )
    options_config.add_argument(
        '--no-llvm-conflict',
        '-DNO_LLVM_CONFLICT',
        action='store_false',
        dest='LLVM_CONFLICT',
        help='Disable LLVM based projects conflict rule'
    )
    options_config.add_argument(
        '--no-gpu-conflict',
        '-DNO_GPU_CONFLICT',
        action='store_false',
        dest='GPU_CONFLICT',
        help='Disable GPU compilers projects conflict rule'
    )
    options_config.add_argument(
        '--free-for-all',
        '-DFREE_FOR_ALL',
        action='store_true',
        dest='FREE_FOR_ALL',
        help='Disable ALL SDK self/other conflicts'
    )
    options_config.add_argument(
        '--tcl-ext',
        '-DENABLE_TCL_EXTENSION',
        action='store_true',
        dest='ENABLE_TCL_EXTENSION',
        help='Enable Modulefiles forcing with tclsh file extension (*.tcl)'
    )


    options_build.add_argument(
        '-G',
        type=str,
        choices=['ninja','make'],
        dest='GENERATOR_STYLE',
        help='Select Generator progress style'
    )
    options_build.add_argument(
        '--force',
        '-DNO_COMPILE_FAIL_STOP',
        action='store_true',
        dest='ENABLE_COMPILE_FORCE_CONTINUE',
        help='Forcing Modulefile compile continues with compile failed'
    )
    options_install.add_argument(
        '--prefix',
        '--install',
        type=str,
        dest='MODULE_INSTALL_PREFIX',
        help='Moulefiles install directory'
    )

    options_exprmnt.add_argument(
        '--exp-cygwin-as-windows',
        '-DEXP_CYGWIN_AS_WINDOWS',
        action='store_true',
        dest='EXPERIMENTIAL_CYGWIN_AS_WINDOWS',
        help='Enable Modulefiles forcing with tclsh file extension (*.tcl)'
    )

    help_flags = {"--help", "-help", "-?", "/?", "/help"}

    if any(flag in sys.argv for flag in help_flags):

        if "--cls" in sys.argv:
            config.CLEAR_HOST = True

        if "--no-color" in sys.argv:
            config.NO_ANSI_COLOR= True

        if config.CLEAR_HOST:
            clear()

        print(parser.format_help())
        sys.exit(0)

    args = parser.parse_args()

    for key, value in vars(args).items():
        if value is not None:
            setattr(config, key, value)
