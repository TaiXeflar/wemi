# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from pathlib import Path
from textwrap import dedent
import re
import subprocess

from .refs import FindSDK
from .refs._findIntel import intel_guess_dir, intel_target_arch, intel_compiler_version_grepper

from tasks import ModulesObject
from utils import subdirs, message


INTEL_ONEAPI_ROOT = intel_guess_dir()

INTEL_TARGET_ARCH = intel_target_arch()


class FindOneAPI(FindSDK):
    ONEAPI_ROOT = INTEL_ONEAPI_ROOT
    _name_desc = "Intel oneAPI"
    is_llvm_infra = True
    is_hetero_tgt = False

    def __init__(self):
        super().__init__()

    def __WINDOWS__(self):

        if not self.ONEAPI_ROOT:
            return

        self.add_rule(
            ModulesObject(
                Module="intel/oneapi",
                output="intel/oneapi",
                mode="tcl",
                Include_file="template_intel_oneapi",
                module_whaits="Intel oneAPI",
                root=self.ONEAPI_ROOT,
                ENVs={"ONEAPI_ROOT": "$root"},
                MODULEPATH=[".deps/intel/oneapi"],
            )
        )

        self.add_intel_compiler(self.ONEAPI_ROOT / "compiler")
        self.add_intel_mkl(self.ONEAPI_ROOT / "mkl")
        self.add_intel_tbb(self.ONEAPI_ROOT / "tbb")
        self.add_intel_tcm(self.ONEAPI_ROOT / "tcm")
        self.add_intel_dnnl(self.ONEAPI_ROOT / "dnnl")
        self.add_intel_mpi(self.ONEAPI_ROOT / "mpi")
        self.add_intel_gdb(self.ONEAPI_ROOT / "debugger")

    def add_intel_tbb(self, pth: Path) -> list[ModulesObject]:
        message(" -- Checking for Intel Thread Building Blocks (TBB) Library")
        tbb_list = []

        for tbb in (pth).iterdir():
            tbb_ver = tbb.name
            tbb_files = subdirs(tbb, leaf=True)

            message(f"\tIntel TBB   {tbb_ver}")

            tbb_tree_new = True if "bin" in tbb_files else False

            if tbb_tree_new:
                tbb_dist_dirs = ["", "vc_mt", "vc14_uwd", "vc14_uwp"]
            else:
                tbb_dist_dirs = ["vc_mt", "vc14", "vc14_uwd", "vc14_uwp"]

            tbb_list.extend(
                [
                    ModulesObject(
                        Module=f"intel/tbb/{tbb_ver} ({tbb_dist})"
                        if tbb_dist
                        else f"intel/tbb/{tbb_ver}",
                        output=".deps/intel/oneapi/"
                        + (
                            f"intel/tbb/{tbb_ver}.{tbb_dist}"
                            if tbb_dist
                            else f"intel/tbb/{tbb_ver}"
                        ),
                        mode="tcl",
                        Include_file="template_intel_tbb",
                        module_whaits=f"Intel oneAPI Thread Building Blocks {tbb_ver}",
                        Version=tbb_ver,
                        deps=["intel/tcm"],
                        conflicts=["Intel/tbb"],
                        VARs={
                            "root": self.ONEAPI_ROOT,
                            "tbb_root": "${root}/tbb/" + tbb.name,
                            "intel_target_arch": INTEL_TARGET_ARCH,
                        },
                        ENVs={"ONEAPI_ROOT": "${root}"},
                        PATH=[
                            "$tbb_root/bin" + f"/{tbb_dist}"
                            if tbb_tree_new
                            else f"$tbb_root/redist/intel64/{tbb_dist}"
                        ],
                        INCLUDE=["$tbb_root/include"],
                        LIB=[
                            "$tbb_root/lib" + f"/{tbb_dist}"
                            if tbb_tree_new
                            else f"$tbb_root/redist/intel64/{tbb_dist}"
                        ],
                    )
                    for tbb_dist in tbb_dist_dirs
                ]
            )

        self.add_rule(tbb_list)

    def add_intel_tcm(self, pth: Path) -> list[ModulesObject]:
        message(" -- Checking for Intel Thread Composability Manager (TCM)")
        tcm_list = []

        for tcm in subdirs(pth):
            tcm_list.append(
                ModulesObject(
                    Module=f"intel/tcm/{tcm.name}",
                    output=".deps/intel/oneapi/" + f"intel/tcm/{tcm.name}",
                    mode="tcl",
                    Include_file="template_intel_tcm",
                    VARs={
                        "root": tcm,
                        "intel_target_arch": INTEL_TARGET_ARCH,
                    },
                    ENVs={
                        "ONEAPI_ROOT": self.ONEAPI_ROOT,
                        "INTEL_TARGET_ARCH": "$intel_target_arch",
                    },
                    PATH=["$root/bin"],
                )
            )

            message(f"\tIntel tcm   {tcm.name}")

        self.add_rule(tcm_list)

    def add_intel_mpi(self, pth: Path) -> list[ModulesObject]:
        message(" -- Checking for Intel Message Passing Interface (Intel MPI)")
        mpi_vers = subdirs(pth)
        for mpi in mpi_vers:
            message(f"\tIntel MPI   {mpi.name}")

            if (mpi / "bin/impi.dll").exists():
                self.add_rule(
                    ModulesObject(
                        Module=f"intel/mpi/{mpi.name}",
                        output=".deps/intel/oneapi/" + f"intel/mpi/{mpi.name}",
                        mode="tcl",
                        Include_file="template_intel_mpi",
                        Version=mpi.name,
                        conflicts=[
                            "Microsoft/msmpi/mpiexec",
                            "Microsoft/msmpi/mpisdk",
                            "intel/mpi",
                        ],
                        VARs={"root": mpi.resolve().as_posix()},
                        ENVs={"ONEAPI_ROOT": self.ONEAPI_ROOT.as_posix()},
                        PATH=["$root/bin", "$root/opt/mpi/libfabric/bin"],
                        INCLUDE=["$root/include"],
                        LIB=["$root/lib"],
                        LD_LIBRARY_PATH=["$root/bin"],
                        PKG_CONFIG_PATH=["$root/lib/pkgconfig"],
                    )
                )
                self.add_rule(
                    ModulesObject(
                        Module=f"intel/mpi/{mpi.name}.debug",
                        output=".deps/intel/oneapi/" + f"intel/mpi/{mpi.name}.debug",
                        mode="tcl",
                        Include_file="template_intel_mpi",
                        Version=mpi.name,
                        conflicts=[
                            "Microsoft/msmpi/mpiexec",
                            "Microsoft/msmpi/mpisdk",
                            "intel/mpi",
                        ],
                        VARs={"root": mpi.resolve().as_posix()},
                        ENVs={"ONEAPI_ROOT": self.ONEAPI_ROOT.as_posix()},
                        PATH=[
                            "$root/bin",
                            "$root/bin/mpi/debug",
                            "$root/opt/mpi/libfabric/bin",
                        ],
                        INCLUDE=["$root/include"],
                        LIB=["$root/lib", "$root/lib/mpi/debug"],
                        LD_LIBRARY_PATH=["$root/bin"],
                        PKG_CONFIG_PATH=["$root/lib/pkgconfig"],
                    )
                )
            else:
                self.add_rule(
                    ModulesObject(
                        Module=f"intel/mpi/{mpi.name}",
                        output=".deps/intel/oneapi/" + f"intel/mpi/{mpi.name}",
                        mode="tcl",
                        Include_file="template_intel_mpi",
                        Version=mpi.name,
                        conflicts=[
                            "Microsoft/msmpi/mpiexec",
                            "Microsoft/msmpi/mpisdk",
                            "intel/mpi",
                        ],
                        VARs={"root": mpi.resolve().as_posix()},
                        ENVs={"ONEAPI_ROOT": self.ONEAPI_ROOT.as_posix()},
                        PATH=[
                            "$root/bin",
                            "$root/bin/release",
                            "$root/opt/mpi/libfabric/bin",
                        ],
                        INCLUDE=["$root/include"],
                        LIB=["$root/lib", "$root/lib/release"],
                        PKG_CONFIG_PATH=["$root/lib/pkgconfig"],
                    )
                )
                self.add_rule(
                    ModulesObject(
                        Module=f"intel/mpi/{mpi.name}",
                        output=".deps/intel/oneapi/" + f"intel/mpi/{mpi.name}",
                        mode="tcl",
                        Include_file="template_intel_mpi",
                        Version=mpi.name,
                        conflicts=[
                            "Microsoft/msmpi/mpiexec",
                            "Microsoft/msmpi/mpisdk",
                            "intel/mpi",
                        ],
                        VARs={"root": mpi.resolve().as_posix()},
                        ENVs={"ONEAPI_ROOT": self.ONEAPI_ROOT.as_posix()},
                        PATH=[
                            "$root/bin",
                            "$root/bin/debug",
                            "$root/opt/mpi/libfabric/bin",
                        ],
                        INCLUDE=["$root/include"],
                        LIB=["$root/lib", "$root/lib/debug"],
                        LD_LIBRARY_PATH=["$root/bin"],
                        PKG_CONFIG_PATH=["$root/lib/pkgconfig"],
                    )
                )

    def add_intel_compiler(self, pth: Path) -> list[ModulesObject]:
        message(" -- Checking for Intel C/C++/DPC++/Visual Fortran HPC compilers")

        compilers = []

        compiler_versions = subdirs(pth)

        for ver in compiler_versions:
            ver_install_items = subdirs(ver, leaf=True)

            if "windows" in ver_install_items:
                # LLVM Clang libdir = <path>/lib/clang/XX/...
                intel_llvm_ver_major = subdirs(ver / "")[0]

                icl = intel_compiler_version_grepper(
                    ver / "windows/bin/intel64/icl.exe"
                )
                icx = intel_compiler_version_grepper(ver / "windows/bin/icx.exe")
                ifort = intel_compiler_version_grepper(
                    ver / "windows/bin/intel64/ifort.exe"
                )
                ifx = intel_compiler_version_grepper(ver / "windows/bin/ifx.exe")
                dpcpp = intel_compiler_version_grepper(ver / "windows/bin/dpcpp.exe")
                icpx = intel_compiler_version_grepper(ver / "windows/bin/icpx.exe")

                llvm = self._find_version(
                    ver / "windows/bin-llvm/clang.exe", "--version", "X.Y.Z"
                )

                message(f"    Intel compiler     {ver.name}")
                message(f"\t - icl         {icl}")
                message(f"\t - icx         {icx}")
                message(f"\t - ifort       {ifort}")
                message(f"\t - ifx         {ifx}")
                message(f"\t - dpcpp       {dpcpp}")
                message(f"\t - icpx        {icpx}")
                message(f"\t - IntelLLVM   {llvm}")

                # Not include Intel LLVM
                compilers.append(
                    ModulesObject(
                        Module=f"intel/compiler/{ver.name}",
                        output=".deps/intel/oneapi/" + f"intel/compiler/{ver.name}",
                        mode="tcl",
                        Include_file="template_intel_compiler",
                        Version=ver.name,
                        prereq=["msvc", "ucrt"],
                        conflicts=["intel/compiler"],
                        llvm_conflicts=[
                            "amd/hip",
                            "ROCm/TheRock",
                            "cangjie",
                            "nvidia/nvhpc",
                            "nvidia/nvhpc-byo",
                        ],
                        hetero_conflicts=[
                            "amd/hip",
                            "ROCm/TheRock",
                        ],
                        vcompare=None,
                        VARs={
                            "root": self.ONEAPI_ROOT,
                            "compiler_root": "${root}/compiler/" + ver.name,
                            "intelLLVM_version": intel_llvm_ver_major,
                            "intel_target_arch": INTEL_TARGET_ARCH,
                        },
                        ENVs={
                            "ONEAPI_ROOT": "${root}",
                            "USE_INTEL_LLVM": 0,
                            "ONEAPI_CLANG_VERSION": "$intelLLVM_version",
                            "INTEL_TARGET_ARCH": "$intel_target_arch",
                            "OCL_ICD_FILENAMES": "$compiler_root/windows/compiler/lib/x64/intelocl64_emu.dll; $compiler_root/windows/lib/x64/intelocl64.dll",
                        },
                        PATH=[
                            "$compiler_root/windows/bin",  # $compiler_root/windows/bin
                            "$compiler_root/windows/bin/$intel_target_arch",  # $compiler_root/windows/bin\intel64
                            "$compiler_root/redist/windows/${intel_target_arch}_win/compiler",  # $compiler_root/windows/redist/${intel_target_arch}_win\compiler
                            "$compiler_root/lib/ocloc",  # $compiler_root/windows/libocloc,
                        ],
                        INCLUDE=[
                            "$compiler_root/windows/include",
                            "$compiler_root/windows/compiler/include",
                            "$compiler_root/windows/compiler/include/$intel_target_arch",
                        ],
                        CPATH=[
                            "$compiler_root/windows/include",
                            "$compiler_root/windows/compiler/include",
                            "$compiler_root/windows/compiler/include/$intel_target_arch",
                        ],
                        LIB=["$compiler_root/lib", "$compiler_root/opt/lib"],
                        CMAKE_PREFIX_PATH=["$compiler_root/windows/IntelDPCPP"],
                        PKG_CONFIG_PATH=["$compiler_root/lib/pkgconfig"],
                    )
                )

                # Include Intel LLVM
                compilers.append(
                    ModulesObject(
                        Module=f"intel/compiler/{ver.name}.llvm",
                        output=".deps/intel/oneapi/"
                        + f"intel/compiler/{ver.name}.llvm",
                        mode="tcl",
                        Include_file="template_intel_compiler",
                        Version=ver.name,
                        prereq=["msvc", "ucrt"],
                        conflicts=["intel/compiler"],
                        llvm_conflicts=[
                            "amd/hip",
                            "ROCm/TheRock",
                            "cangjie",
                            "nvidia/nvhpc",
                            "nvidia/nvhpc-byo",
                        ],
                        hetero_conflicts=[
                            "amd/hip",
                            "ROCm/TheRock",
                        ],
                        vcompare=None,
                        VARs={
                            "root": self.ONEAPI_ROOT,
                            "compiler_root": "${root}/compiler/" + ver.name,
                            "intelLLVM_version": intel_llvm_ver_major,
                            "intel_target_arch": INTEL_TARGET_ARCH,
                        },
                        ENVs={
                            "ONEAPI_ROOT": "${root}",
                            "USE_INTEL_LLVM": 1,
                            "ONEAPI_CLANG_VERSION": "$intelLLVM_version",
                            "INTEL_TARGET_ARCH": "$intel_target_arch",
                            "OCL_ICD_FILENAMES": "$compiler_root/windows/compiler/lib/x64/intelocl64_emu.dll;$compiler_root/windows/lib/x64/intelocl64.dll",
                        },
                        PATH=[
                            "$compiler_root/windows/bin",  # $compiler_root/windows/bin
                            "$compiler_root/windows/bin-llvm",  # $compiler_root/windows/bin-llvm
                            "$compiler_root/windows/bin/$intel_target_arch",  # $compiler_root/windows/bin\intel64
                            "$compiler_root/redist/windows/${intel_target_arch}_win/compiler",  # $compiler_root/windows/redist/${intel_target_arch}_win\compiler
                            "$compiler_root/lib/ocloc",  # $compiler_root/windows/libocloc,
                        ],
                        INCLUDE=[
                            "$compiler_root/windows/include",
                            "$compiler_root/windows/compiler/include",
                            "$compiler_root/windows/compiler/include/$intel_target_arch",
                        ],
                        CPATH=[
                            "$compiler_root/windows/include",
                            "$compiler_root/windows/compiler/include",
                            "$compiler_root/windows/compiler/include/$intel_target_arch",
                        ],
                        LIB=[
                            "$compiler_root/lib",
                            "$compiler_root/lib/clang/$intelLLVM_version/lib/windows",
                            "$compiler_root/opt/lib",
                        ],
                        CMAKE_PREFIX_PATH=["$compiler_root/windows/IntelDPCPP"],
                        PKG_CONFIG_PATH=["$compiler_root/lib/pkgconfig"],
                    )
                )

                continue

            elif "bin" in ver_install_items:
                intel_llvm_ver_major = subdirs(ver / "")[0]

                icx = intel_compiler_version_grepper(ver / "bin/icx.exe")
                ifx = self._find_version(
                    ver / "bin/ifx.exe",
                    "--version",
                    "X.Y.Z",
                    pattern=r"Version\s+([\d\.]+)",
                )
                icpx = self._find_version(ver / "bin/icpx.exe", "--version", "X.Y.Z")

                llvm = self._find_version(
                    ver / "bin/compiler/clang.exe", "--version", "X.Y.Z"
                )

                message(f"    Intel compiler     {ver.name}")
                message(f"\t - icx         {icx}")
                message(f"\t - ifx         {ifx}")
                message(f"\t - icpx        {icpx}")
                message(f"\t - IntelLLVM   {llvm}")

                # Not include Intel LLVM
                compilers.append(
                    ModulesObject(
                        Module=f"intel/compiler/{ver.name}",
                        output=".deps/intel/oneapi/" + f"intel/compiler/{ver.name}",
                        mode="tcl",
                        Include_file="template_intel_compiler",
                        Version=ver.name,
                        prereq=["msvc", "ucrt"],
                        conflicts=["intel/compiler"],
                        llvm_conflicts=[
                            "amd/hip",
                            "ROCm/TheRock",
                            "cangjie",
                            "nvidia/nvhpc",
                            "nvidia/nvhpc-byo",
                        ],
                        hetero_conflicts=[
                            "amd/hip",
                            "ROCm/TheRock",
                        ],
                        vcompare=None,
                        VARs={
                            "root": self.ONEAPI_ROOT,
                            "compiler_root": f"$root/compiler/{ver.name}",
                            "intelLLVM_version": intel_llvm_ver_major,
                            "intel_target_arch": INTEL_TARGET_ARCH,
                        },
                        ENVs={
                            "ONEAPI_ROOT": "$root",
                            "USE_INTEL_LLVM": 0,
                            "ONEAPI_CLANG_VERSION": "$intelLLVM_version",
                            "INTEL_TARGET_ARCH": "$intel_target_arch",
                            "OCL_ICD_FILENAMES": "$compiler_root/bin/intelocl64.dll",
                        },
                        PATH=["$compiler_root/bin", "$compiler_root/lib/ocloc"],
                        INCLUDE=[
                            "$compiler_root/include",
                        ],
                        C_INCLUDE_PATH=["$compiler_root/include"],
                        CPLUS_INCLUDE_PATH=["$compiler_root/include"],
                        LIB=["$compiler_root/lib", "$compiler_root/opt/compiler/lib"],
                        PKG_CONFIG_PATH=["$compiler_root/lib/pkgconfig"],
                        CMAKE_PREFIX_PATH=["$compiler_root"],
                    )
                )

                # Include Intel LLVM
                compilers.append(
                    ModulesObject(
                        Module=f"intel/compiler/{ver.name}.llvm",
                        output=".deps/intel/oneapi/"
                        + f"intel/compiler/{ver.name}.llvm",
                        mode="tcl",
                        Include_file="template_intel_compiler",
                        Version=ver.name,
                        prereq=["msvc", "ucrt"],
                        conflicts=["intel/compiler"],
                        llvm_conflicts=[
                            "amd/hip",
                            "ROCm/TheRock",
                            "cangjie",
                            "nvidia/nvhpc",
                            "nvidia/nvhpc-byo",
                        ],
                        hetero_conflicts=[
                            "amd/hip",
                            "ROCm/TheRock",
                        ],
                        vcompare=None,
                        VARs={
                            "root": self.ONEAPI_ROOT,
                            "compiler_root": f"$root/compiler/{ver.name}",
                            "intelLLVM_version": intel_llvm_ver_major,
                            "intel_target_arch": INTEL_TARGET_ARCH,
                        },
                        ENVs={
                            "ONEAPI_ROOT": "$root",
                            "USE_INTEL_LLVM": 1,
                            "ONEAPI_CLANG_VERSION": "$intelLLVM_version",
                            "INTEL_TARGET_ARCH": "$intel_target_arch",
                            "OCL_ICD_FILENAMES": "$compiler_root/bin/intelocl64.dll",
                        },
                        PATH=[
                            "$compiler_root/bin",
                            "$compiler_root/bin/compiler",
                            "$compiler_root/lib/ocloc",
                        ],
                        INCLUDE=[
                            "$compiler_root/include",
                        ],
                        C_INCLUDE_PATH=["$compiler_root/include"],
                        CPLUS_INCLUDE_PATH=["$compiler_root/include"],
                        LIB=[
                            "$compiler_root/lib",
                            "$compiler_root/lib/clang/$intelLLVM_version/lib/windows",
                            "$compiler_root/opt/compiler/lib",
                        ],
                        PKG_CONFIG_PATH=["$compiler_root/lib/pkgconfig"],
                        CMAKE_PREFIX_PATH=["$compiler_root"],
                    )
                )

                continue

            else:
                raise Exception(
                    dedent(f"""\
                    WEMI configure have an exception runtime error on Intel oneAPI compiler detection.

                     >>> traceback: Neither "windows" or "bin" folder found in Intel compiler search path:
                                    {ver.resolve().as_posix()}
                    """)
                )

        self.add_rule(compilers)

    def add_intel_mkl(self, pth: Path) -> list[ModulesObject]:
        message(" -- Checking for Intel Math Kernel Library (MKL)")
        mkl_ver_dirs = subdirs(pth)

        for mkl in mkl_ver_dirs:
            mkl_ver = mkl.name

            libdirs = (
                ["$root/lib", "$root/lib/intel64"]
                if (mkl / "lib/intel64").exists()
                else ["$root/lib"]
            )

            message(f"\tIntel MKL   {mkl_ver} (LP64)")

            # LP64
            self.add_rule(
                ModulesObject(
                    Module=f"intel/mkl/{mkl_ver}",
                    output=".deps/intel/oneapi/" + f"intel/mkl/{mkl_ver}",
                    mode="tcl",
                    Include_file="template_intel_mkl",
                    Version=mkl_ver,
                    conflicts=["intel/mkl"],
                    VARs={
                        "root": mkl,
                        "intel_target_arch": INTEL_TARGET_ARCH,
                    },
                    ENVs={
                        "ONEAPI_ROOT": self.ONEAPI_ROOT,
                        "INTEL_TARGET_ARCH": "$intel_target_arch",
                        "MKLROOT": "$root",
                    },
                    PATH=["$root/bin/intel64", "$root/redist/intel64"],
                    INCLUDE=["$root/include", "$root/include/intel64/lp64"],
                    LIB=libdirs,
                    CMAKE_PREFIX_PATH=["$root", "$root/lib/cmake"],
                    PKG_CONFIG_PATH=["$root/lib/pkgconfig"],
                    NLSPATH=libdirs,
                )
            )

            message(f"\tIntel MKL   {mkl_ver} (ILP64)")

            # ILP64
            self.add_rule(
                ModulesObject(
                    Module=f"intel/mkl/{mkl_ver}.ilp64",
                    output=".deps/intel/oneapi/" + f"intel/mkl/{mkl_ver}_ilp64",
                    mode="tcl",
                    Include_file="template_intel_mkl",
                    Version=mkl_ver,
                    conflicts="intel/mkl",
                    VARs={
                        "root": mkl,
                        "intel_target_arch": INTEL_TARGET_ARCH,
                    },
                    ENVs={
                        "ONEAPI_ROOT": self.ONEAPI_ROOT,
                        "INTEL_TARGET_ARCH": "$intel_target_arch",
                        "MKLROOT": "$root",
                    },
                    PATH=["$root/bin/intel64", "$root/redist/intel64"],
                    INCLUDE=["$root/include", "$root/include/intel64/ilp64"],
                    LIB=libdirs,
                    CMAKE_PREFIX_PATH=["$root", "$root/lib/cmake"],
                    PKG_CONFIG_PATH=["$root/lib/pkgconfig"],
                    NLSPATH=libdirs,
                )
            )

    def add_intel_dnnl(self, pth: Path) -> list[ModulesObject]:
        dnnl_list: list[ModulesObject] = []
        dnnl_dist: dict[str, str] = {}

        message(" -- Checking for Intel Deep Neural Networks Library (oneDNN/DNNL)")

        for dnnl in subdirs(pth):
            dnnl_ver = dnnl.name

            # dict:
            #   {
            #       "2022.1.0.cpu_dpcpp_gpu_dpcpp": "2022.1.0/cpu_dpcpp_gpu_dpcpp",
            #       "2022.1.0.cpu_iomp": "2022.1.0/cpu_iomp"
            #       "2022.1.0.cpu_tbb": "2022.1.0/cpu_tbb",
            #       "2022.1.0.cpu_vcomp": "2022.1.0/cpu_vcomp",
            #       "2025.1": "2025.1",
            #   }

            dnnl_subdir = subdirs(dnnl, leaf=True)
            if "bin" in dnnl_subdir:
                message(f"\tIntel DNNL  {dnnl_ver}")

                dnnl_dist.update({dnnl_ver: dnnl_ver})

                dnnl_list.append(
                    ModulesObject(
                        Module=f"intel/dnnl/{dnnl_ver}",
                        output=".deps/intel/oneapi/" + f"intel/dnnl/{dnnl_ver}",
                        mode="tcl",
                        Include_file="template_intel_dnnl",
                        module_whaits=f"Intel oneAPI Deep Neural Network Library (oneDNN/DNNL) -> {dnnl}",
                        conflicts=["intel/dnnl"],
                        VARs={
                            "root": self.ONEAPI_ROOT,
                            "dnnl_version": dnnl_ver,
                            "intel_target_arch": INTEL_TARGET_ARCH,
                        },
                        ENVs={
                            "ONEAPI_ROOT": "$root",
                            "INTEL_DNNL_VERSION": dnnl,
                            "INTEL_DNNL_PROFILE": dnnl,
                        },
                        PATH=[
                            "$root/$dnnl_version/bin",
                        ],
                        INCLUDE=[
                            "$root/$dnnl_version/include",
                        ],
                        LIB=[
                            "$root/$dnnl_version/lib",
                        ],
                        CMAKE_PREFIX_PATH=[
                            "$root/$dnnl_version/lib/cmake",
                        ],
                        PKG_CONFIG_PATH=[
                            "$root/$dnnl_version/lib/pkgconfig",
                        ],
                    )
                )

            else:
                dnnl_b = ["cpu_dpcpp_gpu_dpcpp", "cpu_iomp", "cpu_tbb", "cpu_vcomp"]

                for b in dnnl_b:
                    message(f"\tIntel DNNL  {dnnl_ver} ({b})")

                dnnl_list.extend(
                    [
                        ModulesObject(
                            Module=f"intel/dnnl/{dnnl_ver}.{b}",
                            output=".deps/intel/oneapi/" + f"intel/dnnl/{dnnl_ver}.{b}",
                            mode="tcl",
                            Include_file="template_intel_dnnl",
                            module_whaits=f"Intel oneAPI Deep Neural Network Library (oneDNN/DNNL) -> {dnnl}_{b}",
                            conflicts=["intel/dnnl"],
                            VARs={
                                "root": self.ONEAPI_ROOT,
                                "dnnl_version": dnnl_ver,
                                "intel_target_arch": INTEL_TARGET_ARCH,
                            },
                            ENVs={
                                "ONEAPI_ROOT": "$root",
                                "INTEL_DNNL_VERSION": dnnl,
                                "INTEL_DNNL_PROFILE": dnnl,
                            },
                            PATH=[
                                f"$root/$dnnl_version/{b}/bin",
                            ],
                            INCLUDE=[
                                f"$root/$dnnl_version/{b}/include",
                            ],
                            LIB=[
                                f"$root/$dnnl_version/{b}/lib",
                            ],
                            CMAKE_PREFIX_PATH=[
                                f"$root/$dnnl_version/{b}/lib/cmake",
                            ],
                        )
                        for b in dnnl_b
                    ]
                )

        self.add_rule(dnnl_list)

    def add_intel_gdb(self, pth: Path) -> list[ModulesObject]:
        message(" -- Checking for Intel Distribution for GDB")

        for gdb in subdirs(pth):
            message(f"\tIntel GDB   {gdb.name}")
            self.add_rule(
                ModulesObject(
                    Module=f"intel/gdb/{gdb.name}",
                    output=".deps/intel/oneapi/" + f"intel/gdb/{gdb.name}",
                    mode="tcl",
                    Include_file="template_intel_gdb",
                    conflicts=["intel/gdb"],
                    VARs={"root": gdb.resolve().as_posix()},
                    ENVs={"ONEAPI_ROOT": self.ONEAPI_ROOT.resolve().as_posix()},
                    PATH=["$root/opt/debugger"],
                )
            )
        ...

    def add_intel_dal(self, pth: Path) -> list[ModulesObject]: ...
    def add_intel_devutils(self, pth: Path) -> list[ModulesObject]: ...
    def add_intel_dpl(self, pth: Path) -> list[ModulesObject]: ...
    def add_intel_ipp(self, pth: Path) -> list[ModulesObject]: ...
    def add_intel_ippcp(self, pth: Path) -> list[ModulesObject]: ...
    # Intel oneAPI toolkit linking tool (tlt)
    def add_intel_tlt(self, pth: Path) -> list[ModulesObject]: ...
    def add_intel_ocloc(self, pth: Path) -> list[ModulesObject]: ...
    def add_intel_pti(self, pth: Path) -> list[ModulesObject]: ...
    def add_intel_ucm(self, pth: Path) -> list[ModulesObject]: ...
    def add_intel_vtune(self, pth: Path) -> list[ModulesObject]: ...
