

# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from .refs import BaseModuleTemplate


class ModuleTemplate(BaseModuleTemplate):
    def build(self):
        self.add_module_whatis("")

        self.add_conflict(*self.module.conflict)
        self.add_deps(*self.module.deps)
        self.set_root(self.module.root)
        self.set_var(**self.module.VAR)
        self.set_env(**self.module.ENV)
        self.prepend_path("PATH", *self.module.PATH)
