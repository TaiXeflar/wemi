


from typing import Any, Literal, Union, overload

from utils.compare_functions import VersionNum
from tasks import ModulesObject
from tasks.objects.modulesobject import ModulesObject

class BaseModuleTemplate:
    def __init__(self, module_obj:ModulesObject): 

        self.module: ModulesObject

        ...

    def add_content(self, *contents:str) -> None: ...
    def add_splitline(self) -> None: ...
    def add_modules_help(self, *content:str): ...
    def add_module_whatis(self, *content:str): ...
    def add_deps(self, *deps: str): ...
    def add_conflict(self, *conflicts: str): ...
    def add_llvm_conflict(self, *conflicts: str): ...
    def add_hetero_conflict(self, *conflicts: str): ...
    def add_prereq(self, *req: str): ...
    def add_vcompact(self, *vcompare_list: dict[str, Any]): ...
    def set_root(self, root: str): ...
    def set_var(self, **var_dict): ...
    def set_env(self, **env_dict): ...

    @overload
    def prepend_path(self, 
                     var_name: Literal[
                        "PATH", 
                        "INCLUDE",
                        "LIB",
                        "LD_LIBRARY_PATH",
                        "RPATH",
                        "CPATH",
                        "C_INCLUDE_PATH",
                        "CPLUS_INCLUDE_PATH",
                        "CMAKE_PREFIX_PATH",
                        "PKG_CONFIG_PATH",
                        "NLSPATH",
                        "MODULEPATH"], /,
                     *paths: str): ...

    @overload
    def append_path(self, 
                    var_name: Literal[
                        "PATH", 
                        "INCLUDE",
                        "LIB",
                        "LD_LIBRARY_PATH",
                        "RPATH",
                        "CPATH",
                        "C_INCLUDE_PATH",
                        "CPLUS_INCLUDE_PATH",
                        "CMAKE_PREFIX_PATH",
                        "PKG_CONFIG_PATH",
                        "NLSPATH",
                        "MODULEPATH"], /,
                    *paths: str): ...

    def set_cmakefile_content(self, *content:str): ...

    def build(self) -> None: ...

    def render(self) -> str: ...