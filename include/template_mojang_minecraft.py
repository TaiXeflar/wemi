

from .refs import BaseModuleTemplate

class ModuleTemplate(BaseModuleTemplate):

    def build(self):
        self.add_module_whatis(*self.module.module_whatis)
        self.prepend_path(*self.module.PATH)