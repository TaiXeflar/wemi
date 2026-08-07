

# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from typing import Literal, TypeAlias, Union, Optional
from dataclasses import dataclass

LLVM_DIST_PROFILE: TypeAlias = Literal[
    r'llvm-org/llvm',       # LLVM Project release build
    r'llvm',                # Visual Studio LLVM profile
    r'amd/hip',             # AMD HIP SDK
    r'ROCm/TheRock',        # AMD ROCm/TheRock
    r'intel/compiler',      # Intel LLVM
    r'nvidia/nvhpc',        # NVIDIA NVHPC SDK
    r'nvidia/nvhpc-byo',    # NVIDIA NVHPC SDK
    r'nvidia/pgi',          # NVIDIA/PGI Compilers
    r'qualcomm/llvm'        # Qualcomm LLVM compiler SDK
    r'cangjie', r'lfortran', r'rust', r'swift', r'zig', r'exaloop/codon', r'root-project/cling'
]

HETERO_DIST_PROFILE: TypeAlias = Literal[
    r'amd/hip',
    r'ROCm/TheRock',
    r'nvidia/cuda',
    r'nvidia/nvhpc',
    r'nvidia/nvhpc-byo',
    r'nvidia/pgi',
    r'intel/ocloc',
    r'qualcomm/llvm',
]

PATH_HINT: TypeAlias = Literal[
    r'$root',
    r'$root/bin',
    r'$root/bin64',
    r'$root/bin/x64',
    r'$root/bin/arm64',
    r'$root/bin/$env(VSCMD_ARG_TGT_ARCH)',
    r'$root/libexec',
]

INCLUDE_HINT: TypeAlias = Literal[
    r'$root/include',
]

LIB_HINT: TypeAlias = Literal[
    r'$root/lib',
    r'$root/lib64',
    r'$root/lib/x64',
    r'$root/lib/arm64',
    r'$root/lib/$env(VSCMD_ARG_TGT_ARCH)',
]

LD_LIBRARY_PATH_HINT: TypeAlias = Literal[
    r'$root',
    r'$root/bin',
    r'$root/bin64',
    r'$root/bin/x64',
    r'$root/bin/arm64',
    r'$root/bin/$env(VSCMD_ARG_TGT_ARCH)',
    r'$root/libexec',
]

MANPATH_HINT: TypeAlias = Literal[
    r'$root/man',
]

CPATH: TypeAlias = Literal[
    r'$root/include',
]

C_INCLUDE_PATH: TypeAlias = Literal[
    r'$root/include',
]

CPLUS_INCLUDE_PATH: TypeAlias = Literal[
    r'$root/include',
]

NLSPATH: TypeAlias = Literal[
    r'$root/lib',
    r'$root/lib64',
    r'$root/lib/x64',
    r'$root/lib/arm64',
    r'$root/lib/$env(VSCMD_ARG_TGT_ARCH)',
]

CCompiler: TypeAlias = Literal[
    'cl.exe',           # MSVC, Visual C/C++ compiler driver
    'clang.exe',        # LLVM/Clang C language frontend with GNU command like
    'clang-cl.exe',     # LLVM/Clang C language frontend with MSVC command like
    'gcc.exe',          # GNU GCC compiler C language frontend
    'bcc32.exe',        # Borland 32bit C/C++ Compiler
    'bcc32c.exe',       # Borland 32bit C/C++ Compiler
    'bcc32x.exe',       # Borland 32bit C/C++ Compiler
    'bcc64.exe',        # Borland 64bit C/C++ Compiler
    'bcc64x.exe',       # Embarcadero optimized C/C++ Compiler
    'tcc.exe',          # Tiny C compiler
    'nvc.exe',          # NVHPC C compiler
    'pgcc.exe',         # PGI C compiler
    'icl.exe',          # Intel C compiler classic
    'icc.exe',          # Intel C compiler classic
    'icpc.exe',
    'icx-cl.exe',       # Intel C compiler (IntelLLVM)
    'dpcpp.exe',
    'dpcpp-cl.exe',
    'amdclang.exe',
]

CXXCompiler: TypeAlias = Literal[
    'cl.exe',           # MSVC, Visual C/C++ compiler driver
    'clang++.exe',      # LLVM/Clang C++ language frontend with GNU command like
    'clang-cl.exe',     # LLVM/Clang C++ language frontend with MSVC command like
    'g++.exe',          # GNU GCC compiler C++ language frontend
    'bcc32.exe',        # Borland 32bit C/C++ Compiler
    'bcc32c.exe',       # Borland 32bit C/C++ Compiler
    'bcc32x.exe',       # Borland 32bit C/C++ Compiler
    'bcc64.exe',        # Borland 64bit C/C++ Compiler
    'bcc64x.exe',       # Embarcadero optimized C/C++ Compiler
    'nvc++.exe',        # NVHPC C++ compiler
    'pgc++.exe',        # PGI C++ compiler
    'icc.exe',          # Intel C++ compiler classic
    'icx.exe',
    'icx-cc.exe',
    'icpx.exe',
    'dpcpp.exe',
    'dpcpp-cl.exe',
    'amdclang++.exe',

]

CUDACXXCompiler: TypeAlias = Literal['nvcc.exe']
HIPCXXCompiler: TypeAlias = Literal['hipcc.exe']


# Todo: Flags etc.
...
