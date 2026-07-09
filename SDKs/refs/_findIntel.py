# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from typing import Literal
from pathlib import Path
from textwrap import dedent

import re
import subprocess

from utils import regedit


INTEL_ONEAPI_ROOT_REG_ROOT = ...

INTEL_ONEAPI_PROJECTS = (
    "advisor",
    "compiler",
    "dal",
    "dnnl",
    "debugger",
    "dev-utilities",
    "dpcpp-ct",
    "dpl",
    "ipp",
    "ippcp",
    "mkl",
    "mpi",
    "ocloc",
    "pti",
    "tbb",
    "tcm",
    "umf",
    "vtune",
)

INTEL_ONEAPI_PROJECTS_TYPEHINT = Literal[
    "advisor",
    "compiler",
    "dal",
    "dnnl",
    "debugger",
    "dev-utilities",
    "dpcpp-ct",
    "dpl",
    "ipp",
    "ippcp",
    "mkl",
    "mpi",
    "ocloc",
    "pti",
    "tbb",
    "tcm",
    "umf",
    "vtune",
]


def intel_target_arch():
    from ._findVS20XX import cpu_host_arch

    vc_tgt_arch = cpu_host_arch()

    if vc_tgt_arch == "x86":
        return "ia32"
    elif vc_tgt_arch == "x64":
        return "intel64"
    else:
        raise ValueError(
            dedent(f"""\
            Intel Target platform requires AMD64/EMT64 architecture, not ARM/RISC/PPC based CPU
            Expected value:     "x64" --> "intel64"
                                "x86" --> "ia32"
            Found Archtecture:  {vc_tgt_arch}
            """)
        )

def intel_guess_dir() -> Path | None:
    raw_paths = (
        regedit(
            "HKLM",
            r"SOFTWARE\WOW6432Node\Intel\Products\IntelOneAPI",
            key_name="ProductDir",
        ),
        r"C:\Program Files (x86)\Intel\oneAPI",
        r"C:\Program Files\Intel\oneAPI",
    )

    for raw_path in raw_paths:
        if raw_path and (path := Path(raw_path) / "compiler").exists():
            return path.parent

    return None

def intel_compiler_version_grepper(compiler: Path | str) -> str:
    if not isinstance(compiler, (Path, str)):
        raise TypeError

    compiler = Path(compiler).resolve()
    if not compiler.exists():
        return

    q = subprocess.run(
        [compiler.as_posix(), "--version"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    ).stdout.splitlines()[0]

    match = re.search(r"Version\s+([\d\.]+)", q)

    if match:
        return match.group(1)
    else:
        return
