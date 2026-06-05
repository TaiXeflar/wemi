

# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from .refs import BaseModuleTemplate

class ModuleTemplate(BaseModuleTemplate):

    def build(self):

        ver = self.module.VERSION

        self.add_module_whatis(
            f""
        )

        self.add_conflict(*self.module.conflicts)
        self.add_deps(*self.module.deps)
        self.set_root(self.module.root)
        self.prepend_path("PATH", *self.module.PATH)
