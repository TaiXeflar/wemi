
from pathlib import Path
import subprocess
from textwrap import dedent

from .refs import FindSDK
from .refs._findVS20XX import VS20XX_VERSIONS, VC_ARCHS, cpu_host_arch, _get_vswhere_install, _vc_ver_parser
from utils import subdirs, message
from utils.compare_functions import VersionNum
from tasks import ModulesObject


class FindVS20XX(FindSDK):

    _name_desc = 'Microsoft Visual Studio'
    is_llvm_infra = True

    def __init__(self):
        super().__init__()

    def __WINDOWS__(self):

        cpu_host = cpu_host_arch()
        vc_host_name = f"Host{cpu_host}" if cpu_host in ("x64", "x86") else cpu_host


        vs_install = _get_vswhere_install()

        # print(vs_install)

        if not vs_install:
            return

        for vs in vs_install:
            vs_ver = vs.get("Version")
            vs_dst = vs.get("Edition")
            vs_dir = Path(vs.get("Install"))

            vs_deps_name = f"{vs_ver}/{vs_dst}"

            vs_name_fmt = f'{vs_ver} {vs_dst}:'

            message(f'    {vs_name_fmt:<25}{vs_dir.as_posix()}')

            self.add_rule(Module=f"vs/{vs_ver}/{vs_dst}",
                          mode="tcl",
                          output=f"vs/{vs_ver}/{vs_dst}",
                          Include_file="template_VS20XX",
                          Version=vs_ver,
                          root=vs_dir.as_posix(),
                          deps=[],
                          conflicts=['vs'],
                          VARs=[],
                          ENVs={
                            f"VS{vs_ver}INSTALLDIR":  vs_dir.as_posix(),
                            "VSINSTALLDIR":         vs_dir.as_posix(),
                            "VCINSTALLDIR":         (vs_dir/"VC/Tools/MSVC").as_posix(),
                            "VCIDEInstallDir":      None,
                            "VCPKG_ROOT":           None,
                            "VS140COMNTOOLS":       None,
                            "VS170COMNTOOLS":       None,},
                          MODULEPATH=[
                              f".deps/{vs_deps_name}",
                          ]
            )
            

            # MSVC compilers
            vc_root = Path(vs_dir/"VC/Tools/MSVC")
            vc_compilers_versions = subdirs(vc_root, leaf=True)
            for vc in vc_compilers_versions:
                vc_archs_installed = [arch for arch in VC_ARCHS if (vc_root/vc/"lib"/arch).exists()]
                vc_ver = VersionNum(vc)
                vc_tag = _vc_ver_parser(vc_ver)

                vc_fmt = f'MSVC {vc_ver} ({vc_tag}),'

                message(f'\t{vc_fmt:<30}target: {vc_archs_installed}')

                self.add_rule([ModulesObject(
                    Module=f"msvc/{vc}({vc_tag})/{arch}",
                    mode="tcl",
                    output=f".deps/{vs_deps_name}/msvc/v{vc_tag}_{vc}/{arch}",
                    Include_file="template_VS20XX_msvc",
                    conflicts=['msvc'],
                    Version=vs_ver,
                    # deps=[vs_deps_name],
                    ENVs={
                            "MSVC_VERSION": f"{vc} ({vc_tag})",
                            "VCVersion": vc,
                            "VSCMD_ARG_TGT_ARCH": arch,
                            "VSCMD_ARG_HOST_ARCH": vc_host_name,
                            "CMAKE_TOOLCHAIN_FILE": f"msvc_{vc_tag}_arm64ec.cmake" 
                                if arch == "arm64ec" else ""
                        },
                    root=Path(vc_root/vc).resolve().as_posix(),
                    PATH=[f"$root/bin/{vc_host_name}/{arch}"],
                    INCLUDE=["$root/include", "$root/ATLMFC/include"],
                    LIB=[
                        f"$root/lib/{arch}", 
                        f"$root/ATLMFC/lib/{arch}" if arch in ("arm64", "arm64ec") else f"$root/ATLMFC/lib/{arch}"],
                    MODULEPATH=[
                        f'.deps/winsdk/{arch}/',
                    ]

                ) for arch in vc_archs_installed])

                self.add_rule([ModulesObject(
                    Module=f"msvc_{vc_tag}_arm64ec.cmake",
                    output=f".deps/{vs_deps_name}/msvc/{vc}_v{vc_tag}/msvc_{vc_tag}_arm64ec.cmake",
                    mode="cmake",
                    Include_file="template_cmakefile",
                    cmakefile_content=dedent(f'''\
                        set(CMAKE_C_FLAGS_INIT "/arm64EC /W3")
                        set(CMAKE_CXX_FLAGS_INIT "/arm64EC /W3 /EHsc")
                        
                        set(CMAKE_EXE_LINKER_FLAGS_INIT "/machine:arm64EC")
                        set(CMAKE_SHARED_LINKER_FLAGS_INIT "/machine:arm64EC")
                        set(CMAKE_STATIC_LINKER_FLAGS_INIT "/machine:arm64EC")
                        
                        set(CMAKE_FIND_ROOT_PATH_MODE_PROGRAM NEVER)
                        set(CMAKE_FIND_ROOT_PATH_MODE_LIBRARY ONLY)
                        set(CMAKE_FIND_ROOT_PATH_MODE_INCLUDE ONLY)
                        set(CMAKE_FIND_ROOT_PATH_MODE_PACKAGE ONLY)
                        ''')
                ) for arch in vc_archs_installed if arch == "arm64ec"])

            # MSVC Redistributable

            # vc_root = Path(vs_dir/"VC/Redist/MSVC")
            # vc_redist_versions = [v for v in subdirs(vc_root, leaf=True) if not v.startswith("v")]
            # self.add_rule([ModulesObject(
            #     Module=f"MSVC/Redist/{vc}",
            #     mode="tcl",
            #     output=f".deps/{vs_deps_name}/MSVC/Redist/{vc}_v{vc_tag}/",
            #     Include_file="template_VS20XX_msvc_redist",
            #     Version=vs_ver,
            #     deps=[vs_deps_name],
            #     ENVs={ },
            #     root=Path(vc_root/"Redist/MSVC"/vc).resolve().as_posix(),
            #     PATH=[f"$root/$env(VSCMD_ARG_TGT_ARCH)/Microsoft.VC{_vc_ver_parser(vc)}.{f}" 
            #           for f in ["CRT", "CXXAMP", "MFC", "MFCLOC", "OpenMP"]]
            # ) for vc in vc_redist_versions])



            # LLVM/Clang

            ll_root = Path(vs_dir/"VC/Tools/Llvm/x64") # Assume we use x64 as ususal

            if cpu_host == "x64":
                pass
            elif cpu_host == "x86":
                ll_root = Path(vs_dir/"VC/Tools/Llvm")
            else: # cpu_host == "arm64":
                ll_root = Path(vs_dir/"VC/Tools/Llvm/arm64")
            

            # LLVM/Clang
            if (ll_root/"bin/clang.exe").exists():
                llvm_version = self._find_version((ll_root/"bin/clang.exe").resolve(), "--version", "X.Y.Z")
                ll_target_triple = subprocess.run([(ll_root/"bin/clang.exe"), "-dumpmachine"],
                                                  capture_output=True,
                                                  text=True,
                                                  check=True).stdout.strip()
                
                ll_fmt = f'LLVM/Clang {llvm_version},'
                message(f'\t{ll_fmt:<30}target: {ll_target_triple}')

                self.add_rule(Module=f"llvm/{llvm_version}",
                              output=f".deps/{vs_deps_name}/llvm/{llvm_version}",
                              Include_file="template_VS20XX_llvm",
                              Version=llvm_version,
                            #   deps=[vs_deps_name],
                              conflicts=["LLVM", "AMD/HIP", "ROCm/TheRock"],
                              ENVs={"LLVM_DIR": "$root/lib/cmake/"},
                              root=ll_root.resolve().as_posix(),
                              PATH=["$root/bin"],
                              INCLUDE=["$root/include"],
                              LIB=["$root/lib"],
                              CMAKE_PREFIX_PATH=["$root"]) 
            else:
                llvm_version = None

            # CMake support on Windows
            vs_cmake_version = None,
            vs_cmake_exe = Path(vs_dir/r"Common7/IDE/CommonExtensions/Microsoft/CMake/CMake/bin/cmake.exe").resolve()
            if vs_cmake_exe.exists():
                vs_cmake_version = self._find_version(vs_cmake_exe, "--version", "X.Y.Z")
                vs_cmake_rootdir = vs_cmake_exe.parent.parent

                message(f'\tCMake {vs_cmake_version}')

                self.add_rule(Module=f"cmake/{vs_cmake_version}",
                              output=f".deps/{vs_deps_name}/cmake/{vs_cmake_version}",
                              Include_file="template_VS20XX_cmake",
                              Version=vs_cmake_version,
                            #   deps=[vs_deps_name],
                              conflicts=["CMake"].extend([]),
                              root=vs_cmake_rootdir.resolve().as_posix(),
                              PATH=["$root/bin"])

            # Ninja-Build
            vs_ninja_version = None
            vs_ninja_exe = Path(vs_dir/r"Common7/IDE/CommonExtensions/Microsoft/CMake/Ninja/ninja.exe").resolve()
            if vs_ninja_exe.exists():
                vs_ninja_version = self._find_version(vs_ninja_exe, "--version", "X.Y.Z")
                vs_ninja_dir = vs_ninja_exe.parent

                message(f'\tNinja-Build {vs_ninja_version}')

                self.add_rule(Module=f"ninja/{vs_ninja_version}",
                              output=f".deps/{vs_deps_name}/ninja/{vs_ninja_version}",
                              Include_file="template_VS20XX_ninja",
                              Version=vs_ninja_version,
                            #   deps=[vs_deps_name],
                              root=vs_ninja_dir.resolve().as_posix(),
                              PATH=["$root"]),

            # MSBuild
            msbuild_dir = Path(vs_dir/r"MSBuild/Current")
            if cpu_host == "x64":
                msbuild_bin_suffix = "Bin/amd64"
            elif cpu_host == "x86":
                msbuild_bin_suffix = "Bin"
            elif cpu_host == "arm64":
                msbuild_bin_suffix = "Bin/arm64"
            
            msbuild_exe = (msbuild_dir/msbuild_bin_suffix/"MSBuild.exe").resolve()
            msbuild_ver = None

            if msbuild_exe.exists():
                msbuild_ver = self._find_version(msbuild_exe, "/version", "X.Y.Z", line=1)

                message(f'\tMSBuild {msbuild_ver}')

                self.add_rule(Module=f"msbuild/{msbuild_ver}",
                              output=f".deps/{vs_deps_name}/msbuild/{msbuild_ver}",
                              Include_file="template_VS20XX_msbuild",
                              Version=msbuild_ver,
                            #   deps=[vs_deps_name],
                              conflicts=["MSBuild"],
                              root=msbuild_dir.resolve().as_posix(),
                              PATH=[f"$root/{msbuild_bin_suffix}"])
                


    