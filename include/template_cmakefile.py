

# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from .refs import BaseModuleTemplate


class ModuleTemplate(BaseModuleTemplate):
    def build(self):
        self.set_cmakefile_content(self.module._raw_data.get("cmakefile_content"))
