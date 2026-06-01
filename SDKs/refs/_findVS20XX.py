

import subprocess
import json
from pathlib import Path
from typing import Literal

from utils.compare_functions import VersionNum, VERSION, VERSION_IN_RANGE

VS20XX_VERSIONS = [
    "VS2012", "VS2015", "VS2017", "VS2019", "VS2022", "VS2026"
]

VS20XX_COMPOMENTS_TYPEHINT = Literal[
    "MSVC", "UCRT", "MSBuild", "LLVM", "CMake", "Ninja"
]

VC_ARCHS = ['x86', 'x64', 'arm', 'arm64', 'arm64ec']

def cpu_host_arch():
    import platform
    
    if platform.machine().strip().lower().startswith(("amd64", "intel64", "em64t", "x86_64", "x86-64")):
        host = "x64"
    elif platform.machine().strip().lower().startswith(("arm64", "aarch64", "armv8")):
        host = "arm64"
    elif platform.machine().strip().lower().startswith(("x86", "i686", "i386")):
        host = "x86"
    elif platform.machine().strip().lower().startswith(("arm", "aarch", "armv7")):
        host = "arm"
    else:
        raise RuntimeError(f"Unsupported CPU architecture: {platform.machine()} ({platform.processor()})")

    return host

def _get_vswhere_install() -> list[dict[Literal["Version", "Edition", "Install"], str]] | None: 
    vswhere = Path(r"C:/Program Files (x86)/Microsoft Visual Studio/Installer/vswhere.exe").resolve()
    if vswhere.exists():
        try:
            vsquery = subprocess.run([vswhere, "-all", "-prerelease", "-products", "*", "-format", "json"],
                                     capture_output=True,
                                     text=True,
                                     check=True).stdout
            vs_instances: list[dict[str, str]] = json.loads(vsquery)

            installations = []
            for instance in vs_instances:
                # 1. 抓取年份 (例如: 2022)
                catalog_dict = instance.get("catalog", {})
                version = catalog_dict.get("productLineVersion", "Unknown")
                
                # 2. 抓取產品 ID 並取出最後的單字 (例如: Microsoft...Product.BuildTools -> BuildTools)
                product_id = instance.get("productId", "")
                edition = product_id.split(".")[-1] if product_id else "Unknown"
                
                # 3. 抓取安裝路徑
                install_path = instance.get("installationPath", "Unknown")

                # 5. 組合成單一字典並加入清單
                installations.append({
                    "Version": _vs_ver_parser(version),
                    "Edition": edition,
                    "Install": install_path
                })
            
            return installations
        
        except subprocess.CalledProcessError as e:
            print(f"Execute vswhere.exe have error: {e}")
            return []
        except json.JSONDecodeError:
            print("Failed Decode vswhere JSON output.")
            return []
    else:
        print(f"Not found vswhere program.")
        return []
    

def _vc_ver_parser(vc_ver:str|VersionNum):
    if VERSION(vc_ver, ">=", "14.50"):
        vc_tag = "145"
    elif VERSION_IN_RANGE("14.30", "<=", vc_ver, "<", "14.50"):
        vc_tag = "143"
    elif VERSION_IN_RANGE("14.20", "<=", vc_ver, "<", "14.30"):
        vc_tag = "142"
    elif VERSION_IN_RANGE("14.10", "<=", vc_ver, "<", "14.20"):
        vc_tag = "141"
    else:
        raise Exception(f"WEMI doesn't support MSVC v140 and lower versions.")
    
    return vc_tag

def _vs_ver_parser(vs_ver:str|int):
    return "2026" if str(vs_ver) == "18" else str(vs_ver)