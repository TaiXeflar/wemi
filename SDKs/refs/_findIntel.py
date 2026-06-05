

# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from typing import Literal
from textwrap import dedent


INTEL_ONEAPI_ROOT_REG_ROOT = ...

INTEL_ONEAPI_PROJECTS = (
    "advisor", "compiler", "dal", "dnnl", "debugger", "dev-utilities", "dpcpp-ct", "dpl", "ipp", "ippcp", "mkl",
    "mpi", "ocloc", "pti", "tbb", "tcm", "umf", "vtune",
)

INTEL_ONEAPI_PROJECTS_TYPEHINT = Literal[
    "advisor", "compiler", "dal", "dnnl", "debugger", "dev-utilities", "dpcpp-ct", "dpl", "ipp", "ippcp", "mkl",
    "mpi", "ocloc", "pti", "tbb", "tcm", "umf", "vtune",
]

def intel_target_arch():
    from ._findVS20XX import cpu_host_arch

    vc_tgt_arch = cpu_host_arch()

    if vc_tgt_arch == "x86":
        return "ia32"
    elif vc_tgt_arch == "x64":
        return "intel64"
    else:
        raise ValueError(dedent(f'''\
            Intel Target platform requires AMD64/EMT64 architecture, not ARM/RISC/PPC based CPU
            Expected value:     "x64" --> "intel64"
                                "x86" --> "ia32"
            Found Archtecture:  {vc_tgt_arch}
            '''))
