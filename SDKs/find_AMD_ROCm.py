
from typing import Any
from pathlib import Path
import json
from pathlib import Path
from typing import Dict, Any
from textwrap import dedent

from .refs import FindSDK
from .refs._findROCm import RocXParserMixin, rocX_config_version_cmake_phonebook
from utils import config, message
from tasks import ModulesObject


class FindTheRock(RocXParserMixin, FindSDK):

    _name_desc = 'ROCm/TheRock'
    is_llvm_infra = True
    is_hetero_tgt = True

    @property
    def SDK_NAME(self) -> str:
        return "ROCm/TheRock"
    
    def __init__(self):
        super().__init__()

    # --- 主流程 ---
    def __WINDOWS__(self):
        
        hip_dirs = [Path(hip) for hip in self.everything('hipcc.exe')]

        if not hip_dirs:
            return
        
        hip_dirs_therock = [hip.parent.parent for hip in hip_dirs if self._hip_is_from_therock(hip)]

        for dist in hip_dirs_therock:
            rocm_config: Dict[str, Any] = {
                'Path': dist.as_posix(),
                'Path of LLVM': (dist/"lib/llvm").as_posix()
            }
            rocm_ver = (dist/'.info/version').read_text('utf-8').strip()
            message(f'    ROCm/TheRock {rocm_ver}    {dist.resolve().as_posix()}')

            dist_info_path = dist/"share/therock/dist_info.json"
            if dist_info_path.exists():
                with open(dist_info_path, "r", encoding="utf-8") as f:
                    gfx_str: str = json.load(f).get("dist_amdgpu_targets", "")
                    rocm_config["__GFX__"] = gfx_str.split(";") if gfx_str else []
            else:
                rocm_config["__GFX__"] = []


            for rocX, v_rule in rocX_config_version_cmake_phonebook.items():
                rocm_config[rocX] = self._get_rocx_version(rocX, v_rule, dist)
                message(f'\t{rocX:<22}{rocm_config[rocX]}')

            rocm_version = rocm_config.get('therock')
            if not rocm_version or rocm_version != rocm_ver:
                message("WARNING", dedent(f'''\
                Warning: skipping ROCm/TheRock {rocm_ver} profile with version cinfigure incorrect.'''))
                continue

            
            self.add_rule(ModulesObject(
                Module=f"ROCm/TheRock/{rocm_version}",
                output=f"ROCm/TheRock/{rocm_version}",
                mode="tcl",
                Include_file="template_amd_rocm_therock",
                Version=rocm_version,
                deps=["UCRT"],
                conflicts=['ROCm/TheRock'],
                root=dist.as_posix(),
                ENVs={"ROCM_HOME": "$root", "ROCM_PATH": "$root", "LLVM_DIR": "$root/lib/llvm"},
                PATH=["$root/bin", "$root/lib/llvm/bin"],
                INCLUDE=["$root/include", "$root/lib/llvm/include"],
                LIB=["$root/lib", "$root/lib/llvm/lib"],
                LD_LIBRARY_PATH=["$root/bin", "$root/lib/llvm/bin"],
                CMAKE_PREFIX_PATH=["$root", "$root/lib/llvm"]
            ))
