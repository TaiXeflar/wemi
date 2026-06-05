# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from pathlib import Path
import re

from .refs import FindSDK
from tasks import ModulesObject
from utils import message


class FindGMT(FindSDK):
    _name_desc = "Generic Mapping Tools (GMT)"

    def __init__(self):
        super().__init__()

    def __WINDOWS__(self):
        gmt_dir_list = [
            Path(gmt).parent.parent for gmt in self.everything(regex=r"^gmt.exe$")
        ]

        for gmt in gmt_dir_list:
            gmt_version = self.gmt_ver_extract(gmt / "include/gmt/gmt_version.h")
            gmt_major = gmt_version.split(".")[0]

            self.add_rule(
                ModulesObject(
                    Module=f"gmt/{gmt_version}",
                    output=f"gmt/{gmt_version}",
                    mode="tcl",
                    Include_file="template_gmt",
                    module_whaits=f"Generic Mapping Tools (GMT) {gmt_version}",
                    Version=gmt_version,
                    conflicts=["gmt"],
                    root=gmt.resolve().as_posix(),
                    PATH=["$root/bin"],
                    INCLUDE=["$root/include"],
                    LIB=["$root/lib"],
                    LD_LIBRARY_PATH=["$root/bin"],
                    CMAKE_PREFIX_PATH=["$root/lib/cmake"]
                    if (gmt / "lib/cmake").exists()
                    else [],
                )
            )

            message(f"    GMT{gmt_major} ({gmt_version})    {gmt.resolve().as_posix()}")

    def gmt_ver_extract(self, header: Path | str, /) -> str:
        if not header.exists() or not header.is_file():
            return

        try:
            content = header.read_text(encoding="utf-8", errors="ignore")

            # 分別匹配 Major, Minor, Patch
            major_match = re.search(r"#define\s+GMT_MAJOR_VERSION\s+(\d+)", content)
            minor_match = re.search(r"#define\s+GMT_MINOR_VERSION\s+(\d+)", content)
            patch_match = re.search(r"#define\s+GMT_RELEASE_VERSION\s+(\d+)", content)

            # Major 與 Minor 是必須的，Patch 若無則預設為 0
            if major_match and minor_match:
                major = major_match.group(1)
                minor = minor_match.group(1)
                patch = patch_match.group(1) if patch_match else "0"
                return f"{major}.{minor}.{patch}"

        except Exception:
            pass
