# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import re
from pathlib import Path

from utils import regedit, message
from .refs import FindSDK
from .refs._findMHY import (
    MIHOYO_PROJECTS_TYPEHINT,
    mihoyo_app_registry_phonebook,
    mihoyo_app_include_file_dict,
)


class FindMiHoYo(FindSDK):
    _name_desc = "MiHoYo/HoYoVerse"

    def __init__(self):
        super().__init__()

        self.info: dict[MIHOYO_PROJECTS_TYPEHINT, dict]

    def __WINDOWS__(self):
        k: MIHOYO_PROJECTS_TYPEHINT

        for k, v in mihoyo_app_registry_phonebook.items():
            install_dir = regedit("HKCU", v, key_name="GameInstallPath")

            if install_dir is None:
                continue
            else:
                install_dir = Path(install_dir).resolve()
                pth = install_dir.as_posix()
                version_file = Path(install_dir / "config.ini").resolve()

                with open(version_file, "r", encoding="utf-8") as f:
                    config_content = f.read().strip()
                    version_info = re.search(
                        r"version=(\d+\.\d+\.\d+)", config_content
                    ).group(1)
                    major, minor, _ = map(int, version_info.split("."))
                    version = (
                        f"{major}.{minor}" + f" (Luna-{minor+1})"
                        if major == 6 and k == "GenshinImpact"
                        else f"{major}.{minor}"
                    )

            _fmt = "    Project " + f"{k:<15}" + f"{version:<15}" + pth
            message(_fmt)
            self.add_rule(
                Module=f"miHoYo/{k}",
                mode="tcl",
                Include_file=mihoyo_app_include_file_dict[k],
                root=pth,
                PATH=["$root"],
            )
