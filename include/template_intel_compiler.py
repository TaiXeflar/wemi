

from .refs import BaseModuleTemplate

class ModuleTemplate(BaseModuleTemplate):
    
    def build(self):

        ver = self.module.VERSION

        self.add_module_whatis("")

        self.add_llvm_conflict(
            'amd/hip', ''
        )

        self.add_conflict(*self.module.conflicts)
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