


from typing import Literal, get_args, Optional, Any
from pathlib import Path


from utils import *
from utils.compare_functions import VersionNum
from utils.cmake_analyzer import cmake_variable_finder

# ROCm software should update contents as phonebook does.
ROC_X_LIBS_TYPEHINT = Literal[
    "amd-llvm",
    "amd_comgr",
    "composable-kernel",
    "hip",
    "hip-lang",
    "hip-other",
    "hiprtc",
    "hipblas",
    "hipblas-common",
    "hipblaslt",
    "hipcub",
    "hipdnn",
    "hipify",
    "hipfft",
    "hiprand",
    "hipsolver",
    "hipsparse",
    "hipsparselt",
    "libhipcxx",
    "miOpen",
    "mxDataGenerator",
    "rocm-core",
    "rocm-cmake",
    "rocm-kpack",
    "rccl",
    "rdc",
    "rocalution",
    "rocclr",
    "rocblas",
    "rocfft",
    "rocgdb",
    "rocrand",
    "rocprim",
    "rocprofiler",
    "rocsparse",
    "rocsolver",
    "rocthrust",
    "roctracer",
    "rocwmma",
    "therock",
]

rocX_config_version_cmake_phonebook: dict[ROC_X_LIBS_TYPEHINT, str] = {
    # For NOTDEFINED/Wrong cmake versioning configure file
    #   "rocX-config-version.cmake" should fix.

    "therock": r".info/version",

    # https://github.com/ROCm/llvm-project/tree/amd-staging/amd/comgr
    "amd_comgr": r"lib/cmake/amd_comgr/amd_comgr-config-version.cmake",
    # https://github.com/ROCm/llvm-project
    "amd-llvm": r"lib/llvm/lib/cmake/llvm/LLVMConfigVersion.cmake",
    # https://github.com/ROCm/llvm-project/tree/amd-staging/amd/hipcc
    "hip": r"lib/cmake/hip/hip-config-version.cmake",
    "hip-lang": r"lib/cmake/hip-lang/hip-lang-config-verson.cmake",
    "hiprtc": r"lib/cmake/hiprtc/hiprtc-config-version.cmake",
    # https://github.com/ROCm/rocm-libraries/tree/develop/projects/hipblas
    "hipblas": r"lib/cmake/hipblas/hipblas-config-version.cmake",
    # https://github.com/ROCm/rocm-libraries/tree/develop/projects/hipblas-common
    "hipblas-common": r"lib/cmake/hipblas-common/hipblas-common-config-version.cmake",
    # https://github.com/ROCm/rocm-libraries/tree/develop/projects/hipblaslt
    "hipblaslt": r"lib/cmake/hipblaslt/hipblaslt-config-version.cmake",
    # https://github.com/ROCm/rocm-libraries/tree/develop/projects/hipcub
    "hipcub": r"lib/cmake/hipcub/hipcub-config-version.cmake",
    # https://github.com/ROCm/rocm-libraries/tree/develop/projects/hipdnn
    "hipdnn": r"lib/cmake/hipdnn_data_sdk/hipdnn_data_sdkConfigVersion.cmake",
    # https://github.com/ROCm/rocm-libraries/tree/develop/projects/hipfft
    "hipfft": r"lib/cmake/hipfft/hipfft-config-version.cmake",
    # https://github.com/ROCm/HIPIFY
    "hipify": r"bin/hipify-clang",
    # https://github.com/ROCm/rocm-libraries/tree/develop/projects/hiprand
    "hiprand": r"lib/cmake/hiprand/hiprand-config-version.cmake",
    # https://github.com/ROCm/rocm-libraries/tree/develop/projects/hipsolver
    "hipsolver": r"lib/cmake/hipsolver/hipsolver-config-version.cmake",
    # https://github.com/ROCm/rocm-libraries/tree/develop/projects/hipsparse
    "hipsparse": r"lib/cmake/hipsparse/hipsparse-config-version.cmake",
    # https://github.com/ROCm/rocm-libraries/tree/develop/projects/hipsparselt
    "hipsparselt": r"lib/cmake/hipsparselt/hipsparselt-config-version.cmake",
    # https://github.com/ROCm/rocm-libraries/tree/develop/projects/hiptensor
    "hiptensor": r"lib/cmake/hipsparselt/hiptensor-config-version.cmake",
    # https://github.com/ROCm/libhipcxx
    "libhipcxx": r"lib/cmake/libhipcxx/libhipcxx-config-version.cmake",
    # https://github.com/ROCm/rocm-libraries/tree/develop/projects/miopen
    "miopen": r"lib/cmake/miopen/miopen-config-version.cmake",
    # https://github.com/ROCm/rocm-libraries/tree/develop/shared/mxdatagenerator
    "mxdatagenerator": r"lib/cmake/mxDataGenerator/mxDataGeneratorConfig-version.cmake",
    # https://github.com/ROCm/rocm-systems/tree/develop/projects/rocm-core
    "rocm-core": r"lib/cmake/rocm-core/rocm-core-config-version.cmake",
    # https://github.com/ROCm/rocm-cmake
    "rocm-cmake": r"share/rocmcmakebuildtools/cmake/ROCMCMakeBuildToolsConfigVersion.cmake",
    # https://github.com/ROCm/rocm-kpack
    "rocm-kpack": r"lib/cmake/rocm-kpack/rocm-kpack-config-version.cmake",
    # https://github.com/ROCm/rocALUTION
    "rocalution": r"lib/cmake/rocalution/rocalution-config-version.cmake",
    # https://github.com/ROCm/rocm-libraries/tree/develop/projects/rocblas
    "rocblas": r"lib/cmake/rocblas/rocblas-config-version.cmake",
    # https://github.com/ROCm/rocm-libraries/tree/develop/projects/rocfft
    "rocfft": r"lib/cmake/rocfft/rocfft-config-version.cmake",
    # https://github.com/ROCm/rocgdb
    "rocgdb": r"bin/rocgdb",
    # https://github.com/ROCm/rocm-libraries/tree/develop/projects/rocprim
    "rocprim": r"lib/cmake/rocprim/rocprim-config-version.cmake",
    # https://github.com/ROCm/rocm-libraries/tree/develop/projects/rocrand
    "rocrand": r"lib/cmake/rocrand/rocrand-config-version.cmake",
    # https://github.com/ROCm/rocm-libraries/tree/develop/projects/rocsolver
    "rocsolver": r"lib/cmake/rocsolver/rocsolver-config-version.cmake",
    # https://github.com/ROCm/rocm-libraries/tree/develop/projects/rocsparse
    "rocsparse": r"lib/cmake/rocsparse/rocsparse-config-version.cmake",
    # https://github.com/ROCm/rocm-libraries/tree/develop/projects/rocthrust
    "rocthrust": r"lib/cmake/rocthrust/rocthrust-config-version.cmake",
    # https://github.com/ROCm/rocm-libraries/tree/develop/projects/rocwmma
    "rocwmma": r"lib/cmake/rocwmma/rocwmma-config-version.cmake",
    #
    #   (@TaiXeflar: actually idk where the config file or executable is    Orz)
    #   Additional projects will/could/should add into ROCm/TheRock integration.
    #
    #       Pending for analyzing that need find from other way.
    #       Pending for integration to rocm-systems/rocm-libraries or TheRock build.
    #       Pending for examine for next commit to remove/adjust.
    #
    #   If project is not found, will return NOTDEFINED/NOTFOUND for FindROCm class uses.
    #
    # https://github.com/ROCm/rocm-libraries/tree/develop/projects/composablekernel
    "composable-kernel": None,
    # https://github.com/ROCm/rocm-systems/tree/develop/projects/hipother
    "hip-other": None,
    # https://github.com/ROCm/rocm-systems/tree/develop/projects/clr
    "rocclr": None,
    # https://github.com/ROCm/rocm-systems/tree/develop/projects/rccl,
    "rccl": None,
    # https://github.com/ROCm/rocm-systems/tree/develop/projects/rocr-runtime
    "rocr-runtime": None,
    # https://github.com/ROCm/rocm-systems/tree/develop/projects/rdc
    "rdc": None,
    # https://github.com/ROCm/ROCgdb
    "rocgdb": r"bin/rocgdb",
    # https://github.com/ROCm/rocm-systems/tree/develop/projects/rocprofiler
    "rocprofiler": r"lib/cmake/rocprofiler/rocprofiler-config-version.cmake",
    # https://github.com/ROCm/rocm-libraries/tree/develop/shared/rocroller
    "rocroller": r"lib/cmake/rocroller/rocroller-config-version.cmake",
    # https://github.com/ROCm/rocm-systems/tree/develop/projects/roctracer
    "roctracer": r"lib/cmake/roctracer/roctracer-config-version.cmake",
}


ROC_X_LIBRARIES_LIST: ROC_X_LIBS_TYPEHINT = list(get_args(ROC_X_LIBS_TYPEHINT))


def _test_phonebook():
    _test_phonebook_list = list(rocX_config_version_cmake_phonebook.keys()).sort()
    _test_typehint_list = [rocX.lower() for rocX in ROC_X_LIBRARIES_LIST].sort()

    if _test_phonebook_list != _test_typehint_list:
        message("FATAL_ERROR", f"""Found ROCm Libraries record have error.""")

_test_phonebook()

class RocXParserMixin:
    """專門用來解析 AMD rocX 元件版本的擴充包"""
    
    def _get_rocx_version(self, rocX: str, value_rule: Optional[str], base_path: Path) -> Optional[Any]:
        if not value_rule:
            return None

        if value_rule.startswith("Same as"):
            ref_key = value_rule.split("Same as")[-1].strip()
            subdir = rocX_config_version_cmake_phonebook.get(ref_key)
        else:
            subdir = value_rule

        if not subdir:
            return None

        configure_actual_filename = (base_path / subdir).resolve()
        if not configure_actual_filename.exists():
            return None

        if configure_actual_filename.suffix == ".cmake":
            query = cmake_variable_finder(
                file=configure_actual_filename,
                hint=["PACKAGE_VERSION"],
                output="all"
            )
            return query.get("PACKAGE_VERSION")
        
        elif rocX in ("rocgdb", "hipify"):
            # 因為 Mixin 最終會和 FindSDK 結合，所以這裡可以直接呼叫 FindSDK 的方法
            return self._find_version(configure_actual_filename)
        
        elif rocX == "therock":
            with open(configure_actual_filename, "r", encoding="utf-8") as f:
                return VersionNum(f.read().strip())
                
        return None
    
    def _hip_is_from_therock(self, hipcc: Path | str, /) -> bool:
        hip = Path(hipcc)
        if not hip.exists() or hip is None:
            raise ValueError(f'Unknown error on configure hipcc where value is None.')
        
        hip_bin_dir = hip.parent
        hip_dir = hip.parent.parent

        if (hip_bin_dir/'clang.exe').exists() and (hip_dir/'amdgcn').exists():
            return False
        elif (hip_dir/'lib/llvm/bin/clang.exe').exists():
            return True
        else:
            raise RuntimeError("Configuring hipcc have errors where identifying hipcc release is out of cases")
