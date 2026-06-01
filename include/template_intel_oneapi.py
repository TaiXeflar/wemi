

from .refs import BaseModuleTemplate

class ModuleTemplate(BaseModuleTemplate):
    def build(self):
        self.add_module_whatis(self.module.module_whatis)
        self.set_root(self.module.root)
        self.set_env(**self.module.ENVs)
        self.prepend_path('MODULEPATH', *self.module.MODULEPATH)