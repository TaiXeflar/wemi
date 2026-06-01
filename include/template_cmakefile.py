

from .refs import BaseModuleTemplate

class ModuleTemplate(BaseModuleTemplate):
    
    def build(self):

        self.set_cmakefile_content(
            self.module._raw_data.get("cmakefile_content")
        )