
# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from typing import Any
from pathlib import Path

import re
import os

from .refs import FindSDK
from .refs._findROCm import RocXParserMixin, rocX_config_version_cmake_phonebook
from tasks import ModulesObject
from utils import message, config



class FindHIPSDK(RocXParserMixin, FindSDK):

    _name_desc = "AMD HIP SDK"
    is_hetero_tgt = True
    is_llvm_infra = True

    @property
    def SDK_NAME(self) -> str:
        return "ROCm/HIP-SDK"

    def __init__(self):
        super().__init__()


    # --- 主流程 ---
    def __WINDOWS__(self):
        _hip_ver_regex = re.compile(r"^HIP_PATH_(\d+)$", re.IGNORECASE)

        conflict_rule = ["AMD/HIP", "ROCm/TheRock"]
        if config.LLVM_CONFLICT:
            conflict_rule.extend(['llvm', 'intel/compiler', 'cangjie', 'nvidia/nvhpc'])

        if config.HETERO_CONFLICT:
            conflict_rule.extend(['nvidia/cuda'])

        for env_key, env_val in os.environ.items():
            m = _hip_ver_regex.match(env_key)
            if not m:
                continue

            hip_path = Path(env_val).resolve()
            if not hip_path.exists():
                continue

            s = m.group(1)
            major = int(s[0]) if len(s) >= 1 else 0
            minor = int(s[1]) if len(s) >= 2 else 0

            verstr = f"{major}.{minor}"
            hipverXY = f"HIP_PATH_{major}{minor}"

            message(f'    {self._name_desc} {verstr:<12} {hip_path.as_posix()}')

            rocm_stat: dict[str, Any] = {
                'Path': hip_path.as_posix(),
                'Path of LLVM': hip_path.as_posix()
            }

            for rocX, v_rule in rocX_config_version_cmake_phonebook.items():
                if rocX == "therock":
                    rocm_stat[rocX] = None
                    continue

                rocm_stat[rocX] = self._get_rocx_version(rocX, v_rule, hip_path)

                message(f'\t{rocX:<22}{rocm_stat[rocX]}')

            self.add_rule(ModulesObject(
                Module=f"amd/hip/{verstr}",
                output=f"amd/hip/{verstr}",
                mode="tcl",
                Include_file="template_amd_hipsdk",
                module_whaits=f"AMD HIP {verstr} SDK",
                modules_help= f"AMD HIP {verstr} SDK",
                Version=verstr,
                deps=[],
                prereq=['msvc', 'ucrt'],
                conflicts=['amd/hip'],
                llvm_conflicts=['llvm', 'cangjie', 'intel/compiler'],
                hetero_conflicts=[
                    'ROCm/TheRock',
                    'intel/ocloc', 'intel/mkl',
                    'nvidia/cuda', 'nvidia/cudnn', 'nvidia/cudss', 'nvidia/cusparselt', 'nvidia/cutensor',

                ],
                ENVs={
                    "HIP_PATH": "$root",
                    hipverXY: "$root"
                },
                root=hip_path.as_posix(),
                PATH=["$root/bin"],
                INCLUDE=["$root/include"],
                LIB=["$root/lib"],
                LD_LIBRARY_PATH=["$root/bin"]
            ))
