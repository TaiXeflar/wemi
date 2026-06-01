
from .refs import BaseModuleTemplate

class ModuleTemplate(BaseModuleTemplate):

    def build(self):
        ver = self.module.VERSION

        self.add_modules_help(*self.module.modules_help)
        self.add_module_whatis(*self.module.module_whatis)
        self.add_deps(*self.module.deps)
        self.add_conflict(*self.module.conflicts)
        self.set_root(self.module.root)
        self.set_var(**self.module.VARs)
        self.set_env(**self.module.ENVs)
        self.prepend_path("PATH", *self.module.PATH)
        self.prepend_path("INCLUDE", *self.module.INCLUDE)
        self.prepend_path("LIB", *self.module.LIB)