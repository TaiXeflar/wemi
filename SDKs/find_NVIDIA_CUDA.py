


import json
import re
import os
import subprocess
from pathlib import Path
from typing import Union

from .refs import FindSDK
from .refs._findCUDA import CUDA_X_TYPEHINT, cuda_components_phonebook
from .refs._findVS20XX import cpu_host_arch

from utils.cmake_analyzer import cmake_variable_finder
from utils import message
from tasks import ModulesObject

_WIN_PLATFORM_ = cpu_host_arch()

class FindCUDA(FindSDK):

    _name_desc = 'NVIDIA CUDA Toolkit'
    is_hetero_tgt = True
    is_llvm_infra = False

    blacklist = ["MATLAB", "Miniconda", "Anaconda", "Ollama", "Libmamba", "Epic Games"]

    def __init__(self):
        super().__init__()
        # Exclude SDKs will contain redistributed nvcc 

    def _is_blacklisted(self, path_str: str) -> bool:
        path_lower = path_str.lower()
        return any(bad_word.lower() in path_lower for bad_word in self.blacklist)

    def _verify_and_register(self, cuda_path: Path, seen_roots: set) -> bool:
        cuda_path = cuda_path.resolve()
        
        # Blacklists
        if cuda_path in seen_roots or self._is_blacklisted(cuda_path.as_posix()):
            return False

        # Fingerprint
        version_file = cuda_path / 'version.json'
        nvcc_exe = cuda_path / 'bin' / 'nvcc.exe'
        if not version_file.exists() or not nvcc_exe.exists():
            return False

        try:
            with open(version_file, "r", encoding="utf-8") as f:
                cuda_version_json: dict[str, dict[str, str]] = json.loads(f.read())
        except (json.JSONDecodeError, UnicodeDecodeError):
            message(f'    [Error] Corrupted version.json found at {cuda_path}. Skipping.')
            return False

        cuda_root_info = cuda_version_json.get("cuda", {})
        full_version = cuda_root_info.get("version", "")
        
        ver_match = re.match(r"^(\d+)\.(\d+)", full_version)
        if not ver_match:
            return False
            
        major, minor = ver_match.groups()
        verstr = f"{major}.{minor}"
        cuda_path_verstr = f"CUDA_PATH_V{major}_{minor}"

        seen_roots.add(cuda_path)
        message(f'    NVIDIA CUDA {verstr}:    {cuda_path.as_posix()}')
        
        cudax_stat: dict[CUDA_X_TYPEHINT, Union[str, None]] = { "Path": cuda_path.as_posix() }
        
        for cudaX, vv in cuda_components_phonebook.items():
            cudaX_version = None
            if vv is not None:
                file = (cuda_path / vv).resolve()
                if vv.endswith(".cmake") and file.exists():
                    cudaX_version_query = cmake_variable_finder(
                        file=file, hint=["PACKAGE_VERSION"], output="all"
                    )
                    cudaX_version = cudaX_version_query.get("PACKAGE_VERSION")
                else:
                    cudaX_dict = cuda_version_json.get(vv)
                    if isinstance(cudaX_dict, dict):
                        cudaX_version = cudaX_dict.get("version")

            message(f'\t{cudaX:<22} {cudaX_version}')
            cudax_stat[cudaX] = cudaX_version
            
        self.add_rule(ModulesObject(
            Module=f"nvidia/cuda/{verstr}",
            output=f"nvidia/cuda/{verstr}",
            mode='tcl',
            Include_file="template_nvidia_cuda_toolkit",
            Version=verstr,
            conflicts=["nvidia/cuda"],
            deps=[],
            ENVs={
                "CUDA_HOME": "$root", 
                "CUDA_PATH": "$root", 
                cuda_path_verstr: "$root",
                "CUDA_VERSION": verstr,
                "CUDA_MAJOR_VERSION": major,
                "CUDA_MINOR_VERSION": minor,
            },
            root=cuda_path.as_posix(),
            PATH=[
                f"$root/bin", 
                f"$root/bin/{_WIN_PLATFORM_}",
                f"$root/nvvm/bin/{_WIN_PLATFORM_}"
            ],
            INCLUDE=[
                "$root/include", 
                "$root/include/cccl"
            ],
            LIB=[
                f"$root/lib/",
                f"$root/lib/{_WIN_PLATFORM_}"
            ],
            LD_LIBRARY_PATH=[
                f"$root/bin", 
                f"$root/bin/{_WIN_PLATFORM_}"
            ],
            MODULEPATH=[
                f".deps/nvidia/cuda/{major}",
                f".deps/nvidia/cuda/cudaX"
            ]
        ))
        return True

    def __WINDOWS__(self):
        
        seen_roots = set()

        # Using $env:CUDA_PATH* = <PATH> (O(1) 命中) ---
        _cuda_ver_regex = re.compile(r"^CUDA_PATH_V(\d+)(?:_(\d+))?$", re.IGNORECASE)
        for k, v in os.environ.items():
            if _cuda_ver_regex.match(k):
                self._verify_and_register(Path(v), seen_roots)

        # Using 'C:/Program Files/NVIDIA GPU Computing Toolkit/CUDA'
        default_root = Path(r"C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA")
        if default_root.exists() and default_root.is_dir():
            for sub_dir in default_root.iterdir():
                if sub_dir.is_dir():
                    self._verify_and_register(sub_dir, seen_roots)

        # Using Everything CLI (es.exe)
        try:

            nvccs = self.everything(regex=r'bin\\nvcc\.exe$')
            
            for nvcc in nvccs:
                # nvcc_path = Path(nvcc.strip())
                if nvcc.exists():
                    cuda_root = nvcc.parent.parent
                    self._verify_and_register(cuda_root, seen_roots)
                    
        except FileNotFoundError:
            
            pass
        except subprocess.CalledProcessError as e:
            message(f"    [Warning] es.exe execution failed: {e}")