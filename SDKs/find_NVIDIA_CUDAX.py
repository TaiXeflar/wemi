# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from pathlib import Path
import ctypes
import os

from .refs import FindSDK
from .refs._findCUDAX import NVIDIA_CUDAX_EXTENSION
from .refs._findVS20XX import cpu_host_arch
from tasks import ModulesObject
from utils import message


class FindCUDAX(NVIDIA_CUDAX_EXTENSION, FindSDK):
    _name_desc = "NVIDIA CUDA-X Library"

    def __init__(self):
        super().__init__()

    def __WINDOWS__(self):
        self.add_nvidia_cudnn()
        self.add_nvidia_cudss()
        self.add_nvidia_cutensor()
        self.add_nvidia_cusparselt()
        self.add_nvidia_cutlass()

        self.add_nvidia_tensorrt()
        self.add_nvidia_amgx()
        self.add_nvidia_libmathdx()

        # self.add_nvidia_cutile()

        # experimential
        # self.add_nvidia_cudagdb()
        # self.add_nvidia_cuquantum()
        # self.add_nvidia_cupqc()
        # self.add_nvidia_nvtx()
        # self.add_nvidia_matx()
        # self.add_nvidia_stdexec()
        # self.add_nvidia_cucollect()

    def add_nvidia_cudnn(self) -> None:
        message(" -- Checking for NVIDIA cuDNN SDK/backend library")

        cudnn_h_list = [Path(h) for h in self.everything("cudnn_version.h")]

        for cudnn_h in cudnn_h_list:
            cudnn_ver = self.cudnn_ver_extract(cudnn_h)
            if cudnn_ver is None:
                continue

            suffixed: bool
            if cudnn_h.parent.name == "include":
                cudnn_dir = cudnn_h.parent.parent
                cudnn_bin = Path(cudnn_dir / "bin")
                suffixed = False

            else:
                cudnn_dir = cudnn_h.parent.parent.parent
                tmp = cudnn_h.parent.name
                cudnn_bin = Path(cudnn_dir / "bin" / tmp)
                suffixed = True

            arch = cpu_host_arch()

            if (cudnn_bin / arch).exists():
                cudnn_bin = cudnn_bin / arch

            cudnn_engines_precompiled64_X_DLLs = list(
                cudnn_bin.glob("cudnn_engines_precompiled64_*.dll")
            )
            if not cudnn_engines_precompiled64_X_DLLs:
                continue

            cudnn_engines_precompiled64_X_DLL = cudnn_engines_precompiled64_X_DLLs[0]
            if not cudnn_engines_precompiled64_X_DLL.exists():
                continue

            cuda_deps_ver = self.cudaX_cuda_deps(
                cudnn_engines_precompiled64_X_DLL
            ).split(".")[0]
            if cuda_deps_ver is None:
                continue

            self.add_rule(
                ModulesObject(
                    module_whaits=f"NVIDIA CUDNN {cudnn_ver} SDK (CUDA {cuda_deps_ver})",
                    Module=f"nvidia/cudnn/{cudnn_ver}",
                    output=f".deps/nvidia/cuda/{cuda_deps_ver}/nvidia/cuDNN/{cudnn_ver}",
                    mode="tcl",
                    Include_file="template_nvidia_cudnn",
                    Version=cudnn_ver,
                    deps=[f"nvidia/cuda/{cuda_deps_ver}"],
                    conflicts=["nvidia/cudnn"],
                    vcompare=[
                        {"env": "CUDA_VERSION", "compare": "!=", "ver": cuda_deps_ver}
                    ],
                    root=cudnn_dir.resolve().as_posix(),
                    PATH=[f"$root/bin/{tmp}/{arch}" if suffixed else "$root/bin"],
                    INCLUDE=[f"$root/include/{tmp}" if suffixed else "$root/include"],
                    LIB=[f"$root/lib/{tmp}/{arch}" if suffixed else "$root/lib"],
                    LD_LIBRARY_PATH=[
                        f"$root/bin/{tmp}/{arch}" if suffixed else "$root/bin"
                    ],
                    CMAKE_PREFIX_PATH=["$root"],
                )
            )

            message(
                f"    NVIDIA cuDNN {cudnn_ver:<7}(cu{cuda_deps_ver})    {cudnn_dir.resolve().as_posix()}"
            )

    def add_nvidia_cudss(self) -> None:
        message(" -- Checking for NVIDIA cuDSS library")

        cudss_dlls = [Path(dll) for dll in self.everything("cudss64*.dll")]

        for dll in cudss_dlls:
            cuda_deps_ver = self.cudaX_cuda_deps(dll).split(".")[0]

            if (dll.parent.parent / "include").exists():
                suffixed = True
                cudss_dir = dll.parent.parent
            else:
                suffixed = False
                cudss_dir = dll.parent.parent.parent

            cudss_h = cudss_dir / "include/cudss.h"
            cudss_ver = self.cudss_ver_extract(cudss_h)
            arch = cpu_host_arch()

            self.add_rule(
                Module=f"nvidia/cudss/{cudss_ver}",
                output=f".deps/nvidia/cuda/{cuda_deps_ver}/nvidia/cudss/{cudss_ver}",
                mode="tcl",
                Include_file="template_nvidia_cudss",
                Version=cudss_ver,
                module_whaits=f"NVIDIA CUDSS {cudss_ver} SDK (CUDA {cuda_deps_ver})",
                deps=[f"nvidia/cuda/{cuda_deps_ver}"],
                conflicts=["nvidia/cudss"],
                vcompare=[
                    {"env": "CUDA_VERSION", "compare": "!=", "ver": cuda_deps_ver}
                ],
                root=cudss_dir.resolve().as_posix(),
                PATH=[f"$root/bin/{cuda_deps_ver}" if suffixed else "$root/bin"],
                INCLUDE=[
                    f"$root/include/{cuda_deps_ver}" if suffixed else "$root/include"
                ],
                LIB=[f"$root/lib/{cuda_deps_ver}/{arch}" if suffixed else "$root/lib"],
                LD_LIBRARY_PATH=[
                    f"$root/bin/{cuda_deps_ver}" if suffixed else "$root/bin"
                ],
                CMAKE_PREFIX_PATH=[
                    f"$root/lib/{cuda_deps_ver}/cmake"
                    if suffixed
                    else "$root/lib/cmake"
                ],
            )

            message(
                f"    NVIDIA cuDSS {cudss_ver:<7}(cu{cuda_deps_ver})    {cudss_dir.resolve().as_posix()}"
            )

        ...

    def add_nvidia_cutensor(self):
        message(" -- Checking for NVIDIA cuTENSOR library")
        dlls = [Path(dll) for dll in self.everything("cutensor.dll")]

        for dll in dlls:
            cuda_deps_ver = self.cudaX_cuda_deps(dll).split(".")[0]

            if (dll.parent.parent / "include").exists():
                suffixed = True
                cutensor_dir = dll.parent.parent
            else:
                suffixed = False
                cutensor_dir = dll.parent.parent.parent

            cutensor_h = cutensor_dir / "include/cutensor.h"
            cutensor_ver = self.cutensor_ver_extract(cutensor_h)

            self.add_rule(
                Module=f"nvidia/cutensor/{cutensor_ver}",
                output=f".deps/nvidia/cuda/{cuda_deps_ver}/nvidia/cutensor/{cutensor_ver}",
                mode="tcl",
                Include_file="template_nvidia_cutensor",
                Version=cutensor_ver,
                module_whaits=f"NVIDIA cuTENSOR {cutensor_ver} SDK (CUDA {cuda_deps_ver})",
                deps=[f"nvidia/cuda/{cuda_deps_ver}"],
                conflicts=["nvidia/cutensor"],
                vcompare=[
                    {"env": "CUDA_VERSION", "compare": "!=", "ver": cuda_deps_ver}
                ],
                root=cutensor_dir.resolve().as_posix(),
                PATH=[f"$root/bin/{cuda_deps_ver}" if suffixed else "$root/bin"],
                INCLUDE=[
                    f"$root/include/{cuda_deps_ver}" if suffixed else "$root/include"
                ],
                LIB=[f"$root/lib/{cuda_deps_ver}/" if suffixed else "$root/lib"],
                LD_LIBRARY_PATH=[
                    f"$root/bin/{cuda_deps_ver}" if suffixed else "$root/bin"
                ],
            )

            message(
                f"    NVIDIA cuTENSOR {cutensor_ver:<7}(cu{cuda_deps_ver})    {cutensor_dir.resolve().as_posix()}"
            )

    def add_nvidia_cusparselt(self):
        message(" -- Checking for NVIDIA cuSPARSELt library")
        dlls = [Path(dll) for dll in self.everything("cusparseLt.dll")]

        for dll in dlls:
            cuda_deps_ver = self.cudaX_cuda_deps(dll).split(".")[0]

            if (dll.parent.parent / "include").exists():
                suffixed = True
                cusparselt_dir = dll.parent.parent
            else:
                suffixed = False
                cusparselt_dir = dll.parent.parent.parent

            cusparselt_h = cusparselt_dir / "include/cusparseLt.h"
            cusparselt_ver = self.cusparselt_ver_extract(cusparselt_h)

            self.add_rule(
                Module=f"nvidia/cusparselt/{cusparselt_ver}",
                output=f".deps/nvidia/cuda/{cuda_deps_ver}/nvidia/cusparselt/{cusparselt_ver}",
                mode="tcl",
                Include_file="template_nvidia_cusparselt",
                Version=cusparselt_ver,
                module_whaits=f"NVIDIA cuSPARSELt {cusparselt_ver} SDK (CUDA {cuda_deps_ver})",
                deps=[f"nvidia/cuda/{cuda_deps_ver}"],
                conflicts=["nvidia/cusparselt"],
                vcompare=[
                    {"env": "CUDA_VERSION", "compare": "!=", "ver": cuda_deps_ver}
                ],
                root=cusparselt_dir.resolve().as_posix(),
                PATH=[f"$root/bin/{cuda_deps_ver}" if suffixed else "$root/bin"],
                INCLUDE=[
                    f"$root/include/{cuda_deps_ver}" if suffixed else "$root/include"
                ],
                LIB=[f"$root/lib/{cuda_deps_ver}/" if suffixed else "$root/lib"],
                LD_LIBRARY_PATH=[
                    f"$root/bin/{cuda_deps_ver}" if suffixed else "$root/bin"
                ],
            )

            message(
                f"    NVIDIA cuTENSOR {cusparselt_ver:<7}(cu{cuda_deps_ver})    {cusparselt_dir.resolve().as_posix()}"
            )

    def add_nvidia_cutlass(self):
        message(" -- Checking for NVIDIA cutlass C++ Library")
        dlls = [
            Path(dll) for dll in self.everything("cutlass.*dll")
        ]  # Include cutlass.dll and cutlass.debug.dll etc.
        for dll in dlls:
            cutlass_dir = dll.parent.parent
            if not (cutlass_dir / "include").exists():
                continue

            cutlass_ver_h = cutlass_dir / "include/cutlass/version.h"
            cutlass_ver = self.cutlass_ver_extract(cutlass_ver_h)

            self.add_rule(
                ModulesObject(
                    Module=f"nvidia/cutlass/{cutlass_ver}",
                    output=f".deps/nvidia/cuda/cudaX/nvidia/cutlass/{cutlass_ver}",
                    mode="tcl",
                    Include_file="template_nvidia_cutlass",
                    module_whaits=f"NVIDIA cutlass {cutlass_ver} C++ Library",
                    root=cutlass_dir,
                    PATH=["$root/bin"],
                    INCLUDE=["$root/include"],
                    LIB=["$root/lib"],
                    LD_LIBRARY_PATH=["$root/bin"],
                    CMAKE_PREFIX_PATH=["$root/lib/cmake"],
                )
            )

            message(
                f"    NVIDIA cutlass {cutlass_ver:<4}    {cutlass_dir.resolve().as_posix()}"
            )

    def add_nvidia_tensorrt(self):
        message(" -- Checking for NVIDIA TensorRT")
        dlls = [
            Path(dll)
            for dll in self.everything(regex=r"nvinfer_\d+\.dll")
            if (Path(dll).parent / "trtexec.exe").exists()
        ]

        for dll in dlls:
            cuda_deps_ver = self.cudaX_cuda_deps(dll).split(".")[0]

            if (dll.parent.parent / "include").exists():
                tensorrt_dir = dll.parent.parent
            else:
                continue

            nvinfer_h = tensorrt_dir / "include/NvInferVersion.h"
            nvinfer_ver = self.nvinfer_ver_extract(nvinfer_h)
            nvinfer_ver_major = nvinfer_ver.split(".")[0]

            self.add_rule(
                ModulesObject(
                    Module=f"nvidia/tensorrt/{nvinfer_ver}",
                    output=f".deps/nvidia/cuda/{cuda_deps_ver}/nvidia/tensorrt/{nvinfer_ver}",
                    mode="tcl",
                    Include_file="template_nvidia_tensorrt",
                    module_whaits=f"NVIDIA TensorRT {nvinfer_ver} (CUDA {cuda_deps_ver})",
                    root=tensorrt_dir,
                    PATH=["$root/bin"],
                    INCLUDE=["$root/include"],
                    LIB=["$root/lib"],
                    LD_LIBRARY_PATH=["$root/bin"],
                )
            )

            message(
                f"    NVIDIA TensorRT {nvinfer_ver_major:<4}(cuda{cuda_deps_ver})    {tensorrt_dir.resolve().as_posix()}"
            )

    def add_nvidia_amgx(self):
        message(" -- Checking for NVIDIA AmgX")
        dlls = [Path(dll) for dll in self.everything(regex=r'^amgxsh.dll$')]

        host = cpu_host_arch()

        for dll in dlls:
            # print(dll.as_posix())
            cuda_deps_ver = self.cudaX_cuda_deps(dll)
            req_cublas_dll = self.everything(f'cublas64_{cuda_deps_ver}.dll')[0]
            req_vcruntime140_1_dll = self.everything(f'vcruntime140_1.dll')[0]

            deps_dll_paths: list[Path] = [
                req_cublas_dll.parent.resolve(),
                req_vcruntime140_1_dll.parent.resolve(),
                Path(f'C:/Windows/system32/downlevel'),
                Path(f'C:/Program Files (x86)/Windows Kits/10/Redist/ucrt/DLLs/{host}'),
                Path(rf'C:/Program Files (x86)/Windows Kits/10/Windows Performance Toolkit')
            ]

            for d in deps_dll_paths:
                os.add_dll_directory(str(d))

            if (dll.parent/'CMakeCache.txt').exists():
                continue

            try:
                amgxsh = ctypes.CDLL(dll.as_posix())
                ver_ptr = ctypes.c_char_p()
                date_ptr = ctypes.c_char_p()
                time_ptr = ctypes.c_char_p()

                rc_build = amgxsh.AMGX_get_build_info_strings(
                    ctypes.byref(ver_ptr),
                    ctypes.byref(date_ptr),
                    ctypes.byref(time_ptr))
                if rc_build == 0:
                    version_str = ver_ptr.value.decode('utf-8') if ver_ptr.value else None
                else:
                    version_str = None

            except Exception as e:
                print(e)
                return

            if version_str:
                message(f'    NVIDIA AmgX {version_str} (CUDA {cuda_deps_ver}) {dll.as_posix()}')
                self.add_rule(ModulesObject(
                    Module=f'nvidia/amgx/{version_str}',
                    output=f'.deps/nvidia/cuda/{cuda_deps_ver}/nvidia/amgx/{version_str}',
                    mode='tcl',
                    Include_file='template_nvidia_amgx',
                    module_whaits=f'NVIDIA Algebraic Multigrid Solver Library',
                    prereq='nvidia/cuda',
                    conflicts=['nvidia/amgx'],
                    root=dll.parent.parent.resolve().as_posix(),
                    PATH=['$root/lib'],
                    INCLUDE=['$root/include'],
                    LIB=['$root/lib'],
                    LD_LIBRARY_PATH=['$root/lib'],
                ))

            else:
                continue

    def add_nvidia_libmathdx(self):
        message(' -- Checking for NVIDIA LibMathDx')
        dlls = [dll for dll in self.everything(regex=r'^mathdx64\_\d+.dll')]

        if not dlls:
            return

        for dll in dlls:
            root = dll.parent.parent
            cuda_dep = self.cudaX_cuda_deps(dll)
            ver = self.libmathdx_ver_extract(root/'include/libmathdx.h')

            message(f'    NVIDIA libmathdx {ver} (CUDA {cuda_dep})')
            self.add_rule(ModulesObject(
                Module=f'nvidia/libmathdx/{ver}',
                output=f'.deps/nvidia/cuda/{cuda_dep}/nvidia/libmathdx/{ver}',
                mode='tcl',
                Include_file='template_nvidia_libmathdx',
                module_whaits=f'NVIDIA LibMathDx Library',
                prereq=f'nvidia/cuda/{cuda_dep}',
                conflicts='nvidia/libmathdx',
                root=root,
                PATH=['$root/bin'],
                INCLUDE=['$root/include'],
                LIB=['$root/lib/$env(VSCMD_ARG_TGT_ARCH)'],
            ))


    # CUDA Tile IR C/C++ Library doesn't contain binary or include header version information and cmake modules
    def add_nvidia_cutile(self): ...

    # Experimental, Identity items
    def add_nvidia_cuquantum(self): ...
    def add_nvidia_cupqc(self): ...
    def add_nvidia_cudagdb(self): ...
    def add_nvidia_matx(self): ...
    def add_nvidia_cucollect(self): ...
    def add_nvidia_nvtx(self): ...
    def add_nvidia_stdexec(self): ...
