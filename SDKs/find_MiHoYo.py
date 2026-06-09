# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import re
from pathlib import Path

from utils import regedit, message
from tasks import ModulesObject
from .refs import FindSDK
from .refs._findMHY import (
    MIHOYO_PROJECTS_TYPEHINT,
    mihoyo_app_registry_phonebook,
    mihoyo_cn_app_registry_phonebook,
    mihoyo_app_include_file_dict,
)


class FindMiHoYo(FindSDK):
    _name_desc = "MiHoYo/HoYoVerse"

    def __init__(self):
        super().__init__()

        self.info: dict[MIHOYO_PROJECTS_TYPEHINT, dict]

    def __WINDOWS__(self):
        k: MIHOYO_PROJECTS_TYPEHINT

        hoyo_launcher_path = regedit("HKCU", r'Software\Cognosphere\HYP\1_0', key_name='InstallPath')
        hoyo_mi_launcher_path = regedit("HKCU", r'Software\miHoYo\HYP\1_1', key_name='InstallPath')

        if hoyo_launcher_path:
            _pth = Path(hoyo_launcher_path).as_posix()
            message(f'    Found MiHoYo/HoYoVerse Launcher (Global)      {_pth}')
            self.add_rule(ModulesObject(
                Module='miHoYo/HoYoVerse',
                output='miHoYo/HoYoVerse',
                mode='tcl',
                module_whaits='MiHoYo/HoYoVerse Launcher (Global)',
                Include_file='template_mihoyo_hoyoverse',
                root=_pth,
                PATH=['$root'],
                MODULEPATH=['.deps/miHoYo/HoYoVerse']
            ))

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
                proj, _, server = k.partition('.')
                server = 'global' if not server else server
                self.add_rule(
                    Module=f"miHoYo/{proj}/{server}",
                    output=f'.deps/miHoYo/HoYoVerse/miHoYo/{proj}/{server}',
                    mode="tcl",
                    Include_file=mihoyo_app_include_file_dict[proj],
                    root=pth,
                    PATH=["$root"],
                )

        if hoyo_mi_launcher_path:
            _pth = Path(hoyo_mi_launcher_path).as_posix()
            message(f'    Found MiHoYo/MiHoYo Launcher (Mainland China)     {_pth}')
            self.add_rule(ModulesObject(
                Module='miHoYo/miHoYo',
                output='miHoYo/miHoYo',
                mode='tcl',
                module_whaits='MiHoYo/MiHoYo Launcher (Mainland China)',
                Include_file='template_mihoyo_hoyoverse',
                root=_pth,
                PATH=['$root'],
                MODULEPATH=['.deps/miHoYo/miHoYo']
            ))
            for k, v in mihoyo_cn_app_registry_phonebook.items():
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
                proj, _, server = k.partition('.')
                server = 'global' if not server else server
                self.add_rule(
                    Module=f"miHoYo/{proj}/{server}",
                    output=f'.deps/miHoYo/miHoYo/miHoYo/{proj}/{server}',
                    mode="tcl",
                    Include_file=mihoyo_app_include_file_dict[proj],
                    root=pth,
                    PATH=["$root"],
                )
