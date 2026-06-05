

# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import os
from pathlib import Path

from .refs import FindSDK
from utils import message

class FindMSMPISDK(FindSDK):

    _name_desc = 'Microsoft MPI SDK'

    def __init__(self):
        super().__init__()

    def __WINDOWS__(self):
        mpi_header_all = [
            Path(h).resolve() for h in self.everything(regex=r'^mpi\.h$')
                if h and not (p := Path(h).resolve()).parent.parent.joinpath("env", "vars.bat").exists()
            ]

        if not mpi_header_all:
            message("WARNING", "Warning: Failed to compile MSMPI SDK modulefile object due to no results.")
            return

        msmpi_dir = mpi_header_all[0].parent.parent.resolve()

        self.add_rule(Module="microsoft/msmpi/mpisdk",
                      mode="tcl",
                      Include_file="template_msmpi_mpisdk",
                      deps=["microsoft/msmpi/mpiexec"],
                      conflicts=['microsoft/msmpi/mpisdk','intel/oneapi'],
                      root=msmpi_dir.resolve().as_posix(),

                      ENVs={"MSMPI_INC":        "$root/Include",
                            "MSMPI_LIB32":      "$root/Lib/x86",
                            "MSMPI_LIB64":      "$root/Lib/x64",},
                      INCLUDE=["$root/Include"],
                      LIB=["$root/Lib/x64" if os.getenv("PROCESSOR_ARCHITECTURE") == "AMD64" else "$root/Lib/x86"])

        self.update(name="Microsoft MPI SDK",
                    info_dict= {
                        "Install Dir": msmpi_dir.resolve().as_posix()
                    })
