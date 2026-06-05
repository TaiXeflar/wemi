

# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from .refs import BaseModuleTemplate


class ModuleTemplate(BaseModuleTemplate):
    def build(self):
        self.add_modules_help(self.module.modules_help)
        self.add_module_whatis(self.module.module_whatis)

        self.add_llvm_conflict(
            "intel/compiler",
            "nvidia/nvhpc",
            "cangjie",
            "llvm",
            "borland",
        )

        self.add_hetero_conflict("ROCm/TheRock", "intel/ocloc", "nvidia/cuda")

        self.add_conflict(*self.module.conflicts)
        self.add_deps(*self.module.deps)
        self.set_root(self.module.root)
        self.set_env(**self.module.ENVs)
        self.prepend_path("PATH", *self.module.PATH)
        self.prepend_path("INCLUDE", *self.module.INCLUDE)
        self.prepend_path("LIB", *self.module.LIB)
