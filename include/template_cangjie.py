


# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from .refs import BaseModuleTemplate
from utils import config

class ModuleTemplate(BaseModuleTemplate):

    def build(self):

        ver = self.module.VERSION

        self.add_module_whatis(f"Cangjie {ver} compiler SDK")

        self.add_llvm_conflict(
            'amd/hip', 'ROCm/TheRock', 'nvidia/nvhpc', 'intel/compiler', 'llvm', 'borland',
        )

        self.add_conflict(*self.module.conflicts)
        self.add_deps(*self.module.deps)
        self.set_root(self.module.root)
        self.set_env(**self.module.ENVs)
        self.prepend_path("PATH", *self.module.PATH)
