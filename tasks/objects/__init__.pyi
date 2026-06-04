

from pathlib import Path
from typing import Any, Literal, Union, overload, List
from utils.compare_functions import VersionNum

from modulesobject import PROFILES_HINT

class ModulesObject:
    __slots__ = ('_raw_data',)

    def __new__(cls, *args, **kwargs): ...
    
    # ==========================================
    # Type Hint Overloads
    # ==========================================

    @overload
    def __init__(
        self, 
        obj:str = ...,
        /,
        *, 
        Module:str = ...,
        output:str = ...,
        mode:Literal['tcl', 'cmake'] = ...,
        Include_file:str = ...,
        modules_help:str = ...,
        module_whaits:str = ...,
        Version: str | VersionNum = ..., 
        prereq: list[PROFILES_HINT] = ...,
        deps: list[PROFILES_HINT] = ..., 
        conflicts: list[PROFILES_HINT] = ...,
        llvm_conflicts:list[PROFILES_HINT] = ...,
        hetero_conflicts:list[PROFILES_HINT] = ...,
        # dict 的語法正確，因為 dict 需要 Key 和 Value 兩個型別
        vcompare: list[dict[Literal['env', 'compare', 'ver'], Union[VersionNum | str]]] = ...,
        VARs: dict[str, str] = ..., 
        ENVs: dict[str, str] = ...,
        root: str = ...,
        
        PATH: list[Literal['$root/bin']] = ..., 
        INCLUDE: list[Literal['$root/include']] = ..., 
        LIB: list[Literal['$root/lib']] = ..., 
        LD_LIBRARY_PATH: list[Literal['$root/bin', '$root/lib']] = ..., 
        RPATH: list[str] | None = ...,
        CPATH: list[Literal['$root/include']] = ...,
        C_INCLUDE_PATH: list[Literal['$root/include']] = ...,
        CPLUS_INCLUDE_PATH: list[Literal['$root/include']] = ...,
        CMAKE_PREFIX_PATH: list[Literal['$root', '$root/lib/cmake']] = ...,
        PKG_CONFIG_PATH: list[Literal['$root/lib/pkgconfig']] = ...,
        NLSPATH: list[str] = ...,
        MODULEPATH: list[str] = ...,
        MANPATH: list[str] = ...,
        CFLAGS: list[str]= ...,
        CXXFLAGS: list[str]= ...,
        CPPFLAGS: list[str]= ...,
        FFLAGS: list[str]= ...,
        FCFLAGS: list[str]= ...,
        LDFLAGS: list[str]= ...,
        cmakefile_content: str = ...,
        **kwargs: Any
    ):
        ...


    @overload
    def __init__(self, obj: 'ModulesObject', /): ...

    @overload
    def __init__(self, obj: dict, /): ...

    def __getitem__(self, key: str) -> Any: ...

    def keys(self): ...
    def __iter__(self): ...
    def __contains__(self, key: str) -> bool: ...

    def items(self): ...
    def __repr__(self): ...

    @property
    def MODULENAME(self) -> str: ...

    @property
    def modules_help(self) -> list[str]: ...
    
    @property
    def module_whatis(self) -> str: ...
    
    @property
    def include_file(self) -> str: ...
    
    @property
    def output(self) -> str: ...
    
    @property
    def VERSION(self) -> str: ...
    
    @property
    def deps(self) -> list[str]: ...

    @property
    def prereq(self) -> list[str]: ...
    
    @property
    def conflicts(self) -> list[str]: ...

    @property
    def conflicts_llvm(self) -> list[str]: ...

    @property
    def conflicts_hetero(self) -> list[str]: ...
    
    @property
    def vcompare(self) -> list[dict[Literal['env', 'compare', 'ver'], Union[VersionNum, str]]]: ...
    
    @property
    def VARs(self) -> dict[str, str]: ...
    
    @property
    def ENVs(self) -> dict[str, str]: ...
    
    @property
    def root(self) -> list[str]: ...
    
    @property
    def PATH(self) -> list[str]: ...
    
    @property
    def INCLUDE(self) -> list[str]: ...
    
    @property
    def LIB(self) -> list[str]: ...
    
    @property
    def LD_LIBRARY_PATH(self) -> list[str]: ...
    
    @property
    def RPATH(self) -> list[str]: ...
    
    @property
    def CPATH(self) -> list[str]: ...

    @property
    def C_INCLUDE_PATH(self) -> list[str]: ...

    @property
    def CPLUS_INCLUDE_PATH(self) -> list[str]: ...
    
    @property
    def MANPATH(self) -> list[str]: ...

    @property
    def NLSPATH(self) -> list[str]: ...
    
    @property
    def MODULEPATH(self) -> list[str]: ...

    @property
    def CMAKE_PREFIX_PATH(self) -> list[str]: ...

    @property
    def PKG_CONFIG_PATH(self) -> list[str]: ...

def modules_object_json_encoder(obj:VersionNum|ModulesObject|Path): ...