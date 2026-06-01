


from pathlib import Path
from typing import Any, Literal, Union
from textwrap import dedent

from utils import config
from utils.compare_functions import VersionNum

class ModulesObject:
    __slots__ = ('_raw_data',)

    def __new__(cls, *args, **kwargs):
        return super().__new__(cls)


    def __init__(self, obj: 'ModulesObject|dict' = None, /, **kwargs):
        if obj is not None and kwargs:
            raise KeyError("Cannot specify both obj (ModulesObject/dict) and kwargs.")

        if isinstance(obj, dict):
            self._raw_data = obj.copy()
        elif isinstance(obj, ModulesObject):
            self._raw_data = obj._raw_data.copy()
        else:
            self._raw_data = kwargs.copy()

        obj_type = self._raw_data.get("mode", 'tcl')

        if obj_type not in ("tcl", "cmake"):
            raise ValueError(f"Cannot compile {obj_type} type object")

        self._raw_data.update({
            flag: kwargs.get(flag)
            for flag in ("CFLAGS", "CXXFLAGS", "CPPFLAGS", "FFLAGS", "FCFLAGS", "LDFLAGS")
            if isinstance(flag, str)
        })

        if config.ENABLE_TCL_EXTENSION:
            self._raw_data.update({
                'output': kwargs.get('output') + '.tcl'
            })

        if config.FREE_FOR_ALL:
            self._raw_data.update({
                'conflicts': []
            })


    def __getitem__(self, key: str) -> Any:
        return self._raw_data[key]

    def keys(self):
        return self._raw_data.keys()

    def __iter__(self):
        return iter(self._raw_data)

    def __contains__(self, key: str) -> bool:
        return key in self._raw_data

    def items(self):
        return self._raw_data.items()

    def __repr__(self):
        return f"<ModulesObject(module='{self.MODULENAME or 'Unknown'}')>"

    @property
    def MODULENAME(self) -> str:
        return self._raw_data.get("Module")
    
    @property
    def objtype(self) -> str:
        o: str = self._raw_data.get("mode")
        return o.capitalize()
    
    @property
    def modules_help(self) -> list[str]:
        return self._raw_data.get("modules_help", "")
    
    @property
    def module_whatis(self) -> str:
        return self._raw_data.get("module_whatis", "")
    
    @property
    def include_file(self) -> str:
        return self._raw_data.get("Include_file") or self._raw_data.get("Include_File")
    
    @property
    def output(self) -> str:
        return self._raw_data.get("output")
    
    @property
    def VERSION(self) -> str:
        return self._raw_data.get("Version")
    
    @property
    def deps(self) -> list[str]:
        return self._raw_data.get("deps", [])
    
    @property
    def prereq(self) -> list[str]:
        return self._raw_data.get("prereq", [])
    
    @property
    def conflicts(self) -> list[str]:
        return self._raw_data.get("conflicts", [])
    
    @property
    def vcompare(self) -> list[dict[Literal["env", "compare", "ver"], Union[VersionNum, str]]]:
        return self._raw_data.get("vcompare")
    
    @property
    def VARs(self) -> dict[str, str]:
        return self._raw_data.get("VARs", {})
    
    @property
    def ENVs(self) -> dict[str, str]:
        return self._raw_data.get("ENVs", {})
    
    @property
    def root(self) -> list[str]:
        return self._raw_data.get("root")
    
    @property
    def PATH(self) -> list[str]:
        path: list[str] | str = self._raw_data.get("PATH", [])
        return path.split(";") if isinstance(path, str) else path
    
    @property
    def INCLUDE(self) -> list[str]:
        path: list[str] | str = self._raw_data.get("INCLUDE", [])
        return path.split(";") if isinstance(path, str) else path
    
    @property
    def LIB(self) -> list[str]:
        path: list[str] | str = self._raw_data.get("LIB", [])
        return path.split(";") if isinstance(path, str) else path
    
    @property
    def LD_LIBRARY_PATH(self) -> list[str]:
        path: list[str] | str = self._raw_data.get("LD_LIBRARY_PATH", [])
        return path.split(";") if isinstance(path, str) else path
    
    @property
    def RPATH(self) -> list[str]:
        path: list[str] | str = self._raw_data.get("RPATH", [])
        return path.split(";") if isinstance(path, str) else path
    
    @property
    def CPATH(self) -> list[str]:
        path: list[str] | str = self._raw_data.get("CPATH", [])
        return path.split(";") if isinstance(path, str) else path

    @property
    def C_INCLUDE_PATH(self) -> list[str]:
        path: list[str] | str = self._raw_data.get("C_INCLUDE_PATH", [])
        return path.split(";") if isinstance(path, str) else path
    
    @property
    def CPLUS_INCLUDE_PATH(self) -> list[str]:
        path: list[str] | str = self._raw_data.get("CPLUS_INCLUDE_PATH", [])
        return path.split(";") if isinstance(path, str) else path
    
    @property
    def MANPATH(self) -> list[str]:
        path: list[str] | str = self._raw_data.get("MANPATH", [])
        return path.split(";") if isinstance(path, str) else path
    
    @property
    def MODULEPATH(self) -> list[str]:
        path: list[str] | str = self._raw_data.get("MODULEPATH", [])
        return path.split(";") if isinstance(path, str) else path
    
    @property
    def CMAKE_PREFIX_PATH(self) -> list[str]:
        path: list[str] | str = self._raw_data.get("CMAKE_PREFIX_PATH", [])
        return path.split(";") if isinstance(path, str) else path
    
    @property
    def PKG_CONFIG_PATH(self) -> list[str]:
        path: list[str] | str = self._raw_data.get("PKG_CONFIG_PATH", [])
        return path.split(";") if isinstance(path, str) else path
    
    @property
    def NLSPATH(self) -> list[str]:
        path: list[str] | str = self._raw_data.get("NLSPATH", [])
        return path.split(";") if isinstance(path, str) else path
    

def modules_object_json_encoder(obj:VersionNum|ModulesObject|Path):

    if type(obj).__name__ == 'ModulesObject':
        return obj._raw_data
        
    if type(obj).__name__ == 'VersionNum':
        return str(obj)
    
    if type(obj).__name__ == 'Path' or type(obj).__name__ == 'WindowsPath':
        return obj.resolve().as_posix()
        
    raise TypeError(dedent(f"""\
            Object of type {obj.__class__.__name__} is not JSON serializable.
             >>> Debug: object is {obj} """))