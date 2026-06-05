

# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from .refs import BaseModuleTemplate

class ModuleTemplate(BaseModuleTemplate):
    def build(self):
        self.add_module_whatis(self.module.module_whatis)
        self.set_root(self.module.root)
        self.set_env(**self.module.ENVs)
        self.prepend_path('MODULEPATH', *self.module.MODULEPATH)
