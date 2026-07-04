

# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from .refs import BaseModuleTemplate

class ModuleTemplate(BaseModuleTemplate):
    def __init__(self, module_obj):
        self.module_obj = module_obj

    def build(self):
        None
