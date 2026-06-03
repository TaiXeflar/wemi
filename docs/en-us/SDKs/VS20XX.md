

# Microsoft Visual Studio Support

WEMI support several Visual Studio installations:
- VS2017 Community, BuildTools
- VS2019 Community, BuildTools
- VS2022 Community, BuildTools
- VS2026 Community, BuildTools

WEMI takes level-access control to unlock its installed compoments. Usage:
```
 envmodule load vs/2026/BuildTools
 envmodule load msvc/v145_14.50.35717/x64
 envmodule load ucrt/10.0.22621.0

 cl.exe
 rc.exe
```

![image](./_pics/vs_hierarchy.png)

WEMI and its MSVC, CMake will not auto load Windows SDK/UCRTs.

## MSVC Compilers
WEMI will generates MSVC Tcl Modulefile rules with VS20XX pre-load level access.

- WEMI will set MSVC profiles, including (Assume) MSVC compiler have ATL/MFC library path. WEMI will not set Spectre profiles.

If MSVC target is ARMEC64, WEMI will generates a cmake toolchain file and combine it (specify `CMAKE_TOOLCHAIN_FILE`).

 - MSVC v141 (14.1X)
 - MSVC v142 (14.2X)
 - MSVC v143 (14.3X, 14.4X)
 - MSVC v145 (14.5X)

## MSVC Redistributables
WEMI will not generate MSVC redistributables modulefiles. 
  
## LLVM/Clang
WEMI will generates LLVM Tcl Modulefile rules with VS20XX pre-load level access.

WEMI will only generates targets specific to host device. For example, if your device is x64, tthis LLVM profile will only set x64 toolchains to your paths.

## MSBuild, CMake, Ninja-Build
As VS20XX installer set MSBuild, CMake support as optional, so WEMI will generate each file on it.

You can take seperating control with VS20XX contained CMake and Ninja-Build executables.


## Windows SDK / Universal CRT
Windows SDK will have its install directory. So Windows SDK will be independent to VS20XX profiles.


## \_\_future\_\_

 - Disscuss on Roslyn compilers.
 - Disscuss on MSVC redist.


