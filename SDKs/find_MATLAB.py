# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from pathlib import Path
from typing import Literal


from .refs import FindSDK
from utils import regedit, message
from tasks import ModulesObject


class FindMATLAB(FindSDK):
    _name_desc = "MATLAB"

    def __init__(self):
        super().__init__()

    def __WINDOWS__(self):
        super().__WINDOWS__()

        matlab_versions = regedit("HKLM", r"SOFTWARE\MathWorks\MATLAB")
        matlab_versioning = [
            self._matlab_version_analyzer(ver) for ver in matlab_versions
        ]

        matlab_install_dirs = [
            Path(
                regedit(
                    "HKLM", rf"SOFTWARE\MathWorks\MATLAB\{ver}", key_name="MATLABROOT"
                )
            ).resolve()
            for ver in matlab_versions
        ]

        matlab_binary_dirs = [
            Path(
                regedit("HKLM", rf"SOFTWARE\MathWorks\{ver}\MATLAB", key_name="")
            ).resolve()
            for ver in matlab_versioning
        ]

        self.add_rule(
            [
                ModulesObject(
                    Module=f"matlab/{ver}",
                    output=f"matlab/{ver}",
                    conflicts=["matlab"],
                    mode="tcl",
                    Include_file="template_matlab",
                    Version=ver,
                    root=root.as_posix(),
                    PATH=[
                        Path(b).resolve().as_posix().replace(root.as_posix(), "$root/")
                    ],
                )
                for ver, root, b in zip(
                    matlab_versioning, matlab_install_dirs, matlab_binary_dirs
                )
            ]
        )

        for ver, pth in zip(matlab_versioning, matlab_install_dirs):
            message(f"\tMATLAB {ver}:   {pth.as_posix()}")

    def _matlab_version_analyzer(self, version: str):
        ab: Literal["1", "2"]

        if not version:
            return

        yr, ab = version.split(".")
        yr = int(yr) + 2000

        if ab == "1":
            ab = "a"
        elif ab == "2":
            ab = "b"
        else:
            raise ValueError(
                f"Unsupported Matlab version with {version} -> R {yr} {ab} where float should be .1/.2"
            )

        return f"R{yr}{ab}"
