

# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import subprocess
from pathlib import Path

from .refs import FindSDK
from utils import config, regedit, message
from utils.functions import subdirs
from utils.compare_functions import VERSION
from tasks import ModulesObject


class FindCangjie(FindSDK):

    _name_desc = 'Huawei/Cangjie-Lang'

    is_llvm_infra = True

    def __init__(self):
        super().__init__()

    def __WINDOWS__(self):

        cjc_list = [Path(cjc) for cjc in self.everything(regex=r'^cjc.exe$')]

        for cjc in cjc_list:
            cjc_ver = self._find_version(cjc, "--version", "X.Y.Z", 0)

            cjc_dir = cjc.parent.parent

            cangjie_llvm = (cjc_dir/"third_party/llvm/bin")
            if not cangjie_llvm.exists():
                message('WARNING', f'[Warning] Found Cangjie {cjc_ver} have no llvm dist. Skip.')
                continue

            cangjie_llvm_ver = self._find_version(cjc_dir/"third_party/llvm/bin/llvm-ar.exe", "--version", "X.Y.Z")
            cangjie_llvm_tgt = subprocess.run([(cjc_dir/"third_party/llvm/bin/llc.exe"), '--version'],
                                                capture_output=True,
                                                text=True,
                                                check=True).stdout.splitlines()[3].strip().split('Default target: ')[-1]
            cangjie_mingw_ld = (cjc_dir/'third_party/mingw/bin/ld.exe')
            if cangjie_mingw_ld.exists():
                cangjie_mingw_ver = self._find_version(cjc_dir/"third_party/mingw/bin/ld.exe", "--version", "X.Y")
            else:
                cangjie_mingw_ver = None

            message(f'    Cangjie Lang {cjc_ver}')
            message(f'\tcjc:    {cjc_ver}')
            message(f'\tLLVM:   {cangjie_llvm_ver}, target {cangjie_llvm_tgt}')
            message(f'\tMinGW:  {cangjie_mingw_ver}')

            self.add_rule(ModulesObject(
                Module=f"cangjie/{cjc_ver}",
                output=f"cangjie/{cjc_ver}",
                mode="tcl",
                module_whaits=f'Cangjie Language {cjc_ver}',
                Include_file="template_cangjie",
                Version=cjc_ver,
                conflicts=["cangjie"],
                llvm_conflicts=['llvm', 'amd/hip', 'intel/compiler', 'msvc'],
                root=cjc_dir.resolve().as_posix(),
                ENVs={"CANGJIE_HOME": "$root", "CANGJIE_PATH": "$root"},
                PATH=[
                    "$root/bin",
                    "$root/tools/lib",
                    "$root/tools/bin",
                    "$root/lib/windows_x86_64_cjnative",
                    "$root/runtime/lib/windows_x86_64_cjnative",
                    "~/.cjpm/bin"
                ]
            ))
