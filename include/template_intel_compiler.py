

# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from .refs import BaseModuleTemplate


class ModuleTemplate(BaseModuleTemplate):
    def build(self):
        ver = self.module.VERSION

        self.add_module_whatis(f"Intel compiler {ver}")

        self.add_llvm_conflict("amd/hip", "")

        self.add_content(
            r"if { [info exists env(VSCMD_ARG_TGT_ARCH)] } {",
            r'    if { $env(VSCMD_ARG_TGT_ARCH) ne "x64" } {',
            r'        puts stderr "  Error Architecture mismatch for Intel Compiler."',
            r'        puts stderr "  Intel oneAPI compiler requires MSVC target architecture to be x64."',
            r'        puts stderr "  But your current VSCMD_ARG_TGT_ARCH is: $env(VSCMD_ARG_TGT_ARCH)"',
            r'        puts stderr "  Please load a compatible MSVC (x64) environment first."',
            r"        break",
            r"    }",
            r"}",
        )
        self.add_deps(*self.module.deps)
        self.set_root(self.module.root)
        self.set_var(**self.module.VARs)
        self.set_env(**self.module.ENVs)
        self.prepend_path("PATH", *self.module.PATH)
        self.prepend_path("CPATH", *self.module.CPATH)
        self.prepend_path("C_INCLUDE_PATH", *self.module.C_INCLUDE_PATH)
        self.prepend_path("CPLUS_INCLUDE_PATH", *self.module.CPLUS_INCLUDE_PATH)
        self.prepend_path("INCLUDE", *self.module.INCLUDE)
        self.prepend_path("LIB", *self.module.LIB)
        self.prepend_path("PKG_CONFIG_PATH", *self.module.PKG_CONFIG_PATH)
        self.prepend_path("CMAKE_PREFIX_PATH", *self.module.CMAKE_PREFIX_PATH)
