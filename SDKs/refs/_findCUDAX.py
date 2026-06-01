


import os
import re
from pathlib import Path

from utils import message
from tasks import ModulesObject

# Individual NVIDIA Library installation via installer/cmake install

class NVIDIA_CUDAX_EXTENSION:

    @staticmethod
    def cudaX_cuda_deps(dll_path: Path, /) -> str | None:
        """
        Extrat DLLs from redistributable from NVIDIA CUDA-X Libraries.

        ## Usage
        ```
        cudaX_targeted_DLL = Path(r'/path/to/dll')
        cuda_dep_version = self.cudaX_cuda_deps(cudaX_targeted_DLL)
        ```
        """
        if not dll_path.exists() or not dll_path.is_file():
            return 

        try:
            # 以二進位模式讀取 DLL，依賴現代作業系統與 Python 的記憶體管理
            with open(dll_path, "rb") as f:
                binary_data = f.read()

            # 優先權 1：抓取 NVRTC (最精準，能給出 Major.Minor，如 130 -> 13.0)
            match_nvrtc = re.search(rb"nvrtc64_(\d+)_0\.dll", binary_data, re.IGNORECASE)
            if match_nvrtc:
                ver_code = match_nvrtc.group(1).decode("ascii")
                if len(ver_code) >= 2:
                    return f"{ver_code[:-1]}.{ver_code[-1]}"

            # 優先權 2：抓取傳統 CUDART (向下相容 cuDNN 7/8 架構)
            match_cudart = re.search(rb"cudart64_(\d+)\.dll", binary_data, re.IGNORECASE)
            if match_cudart:
                cudart_ver = match_cudart.group(1).decode("ascii")
                if cudart_ver.startswith("12"): return "12"
                if cudart_ver == "110": return "11"
                if cudart_ver == "102": return "10.2"
                return cudart_ver

            # 優先權 3：抓取 cuBLAS (最終兜底方案)
            match_cublas = re.search(rb"cublas(?:Lt)?64_(\d+)\.dll", binary_data, re.IGNORECASE)
            if match_cublas:
                return match_cublas.group(1).decode("ascii")

        except Exception:
            pass # 遇到權限鎖定或讀取異常，安全略過

        return

    @staticmethod
    def cudnn_ver_extract(header_path: Path) -> str | None:
        """
        分析 cudnn_version.h 或 cudnn.h,
        提取 CUDNN_MAJOR, CUDNN_MINOR, CUDNN_PATCHLEVEL 並組合為標準版本號。
        """
        if not header_path.exists() or not header_path.is_file():
            return None

        try:
            content = header_path.read_text(encoding="utf-8", errors='ignore')

            # 分別匹配 Major, Minor, Patch
            major_match = re.search(r"#define\s+CUDNN_MAJOR\s+(\d+)", content)
            minor_match = re.search(r"#define\s+CUDNN_MINOR\s+(\d+)", content)
            patch_match = re.search(r"#define\s+CUDNN_PATCHLEVEL\s+(\d+)", content)

            # Major 與 Minor 是必須的，Patch 若無則預設為 0
            if major_match and minor_match:
                major = major_match.group(1)
                minor = minor_match.group(1)
                patch = patch_match.group(1) if patch_match else "0"
                return f"{major}.{minor}.{patch}"

        except Exception as e:
            pass

    @staticmethod
    def cudss_ver_extract(header_path: Path) -> str | None:
        """
        分析 cudnn_version.h 或 cudnn.h,
        提取 CUDNN_MAJOR, CUDNN_MINOR, CUDNN_PATCHLEVEL 並組合為標準版本號。
        """
        if not header_path.exists() or not header_path.is_file():
            return None

        try:
            content = header_path.read_text(encoding="utf-8", errors='ignore')

            # 分別匹配 Major, Minor, Patch
            major_match = re.search(r"#define\s+CUDSS_VERSION_MAJOR\s+(\d+)", content)
            minor_match = re.search(r"#define\s+CUDSS_VERSION_MINOR\s+(\d+)", content)
            patch_match = re.search(r"#define\s+CUDSS_VERSION_PATCH\s+(\d+)", content)

            # Major 與 Minor 是必須的，Patch 若無則預設為 0
            if major_match and minor_match:
                major = major_match.group(1)
                minor = minor_match.group(1)
                patch = patch_match.group(1) if patch_match else "0"
                return f"{major}.{minor}.{patch}"

        except Exception as e:
            pass

    @staticmethod
    def cutensor_ver_extract(header_path: Path) -> str | None:
        """
        分析 cudnn_version.h 或 cudnn.h,
        提取 CUDNN_MAJOR, CUDNN_MINOR, CUDNN_PATCHLEVEL 並組合為標準版本號。
        """
        if not header_path.exists() or not header_path.is_file():
            return None

        try:
            content = header_path.read_text(encoding="utf-8", errors='ignore')

            # 分別匹配 Major, Minor, Patch
            major_match = re.search(r"#define\s+CUTENSOR_MAJOR\s+(\d+)", content)
            minor_match = re.search(r"#define\s+CUTENSOR_MINOR\s+(\d+)", content)
            patch_match = re.search(r"#define\s+CUTENSOR_PATCH\s+(\d+)", content)

            # Major 與 Minor 是必須的，Patch 若無則預設為 0
            if major_match and minor_match:
                major = major_match.group(1)
                minor = minor_match.group(1)
                patch = patch_match.group(1) if patch_match else "0"
                return f"{major}.{minor}.{patch}"

        except Exception as e:
            pass

    @staticmethod
    def cusparselt_ver_extract(header_path: Path) -> str | None:
        """
        分析 cudnn_version.h 或 cudnn.h,
        提取 CUDNN_MAJOR, CUDNN_MINOR, CUDNN_PATCHLEVEL 並組合為標準版本號。
        """
        if not header_path.exists() or not header_path.is_file():
            return None

        try:
            content = header_path.read_text(encoding="utf-8", errors='ignore')

            # 分別匹配 Major, Minor, Patch
            major_match = re.search(r"#define\s+CUSPARSELT_VER_MAJOR\s+(\d+)", content)
            minor_match = re.search(r"#define\s+CUSPARSELT_VER_MINOR\s+(\d+)", content)
            patch_match = re.search(r"#define\s+CUSPARSELT_VER_PATCH\s+(\d+)", content)

            # Major 與 Minor 是必須的，Patch 若無則預設為 0
            if major_match and minor_match:
                major = major_match.group(1)
                minor = minor_match.group(1)
                patch = patch_match.group(1) if patch_match else "0"
                return f"{major}.{minor}.{patch}"

        except Exception as e:
            pass

    @staticmethod
    def nvinfer_ver_extract(header_path: Path) -> str | None:
        """
        分析 cudnn_version.h 或 cudnn.h,
        提取 CUDNN_MAJOR, CUDNN_MINOR, CUDNN_PATCHLEVEL 並組合為標準版本號。
        """
        if not header_path.exists() or not header_path.is_file():
            return 

        try:
            content = header_path.read_text(encoding="utf-8", errors='ignore')

            # 分別匹配 Major, Minor, Patch
            major_match = re.search(r"#define\s+TRT_MAJOR_ENTERPRISE\s+(\d+)", content)
            minor_match = re.search(r"#define\s+TRT_MINOR_ENTERPRISE\s+(\d+)", content)
            patch_match = re.search(r"#define\s+TRT_PATCH_ENTERPRISE\s+(\d+)", content)

            # Major 與 Minor 是必須的，Patch 若無則預設為 0
            if major_match and minor_match:
                major = major_match.group(1)
                minor = minor_match.group(1)
                patch = patch_match.group(1) if patch_match else "0"
                return f"{major}.{minor}.{patch}"

        except Exception as e:
            pass

    @staticmethod
    def cutlass_ver_extract(header_path: Path, /):
        if not header_path.exists() or not header_path.is_file():
            return 

        try:
            content = header_path.read_text(encoding="utf-8", errors='ignore')

            # 分別匹配 Major, Minor, Patch
            major_match = re.search(r"#define\s+CUTLASS_MAJOR\s+(\d+)", content)
            minor_match = re.search(r"#define\s+CUTLASS_MINOR\s+(\d+)", content)
            patch_match = re.search(r"#define\s+CUTLASS_PATCH\s+(\d+)", content)

            # Major 與 Minor 是必須的，Patch 若無則預設為 0
            if major_match and minor_match:
                major = major_match.group(1)
                minor = minor_match.group(1)
                patch = patch_match.group(1) if patch_match else "0"
                return f"{major}.{minor}.{patch}"

        except Exception as e:
            pass