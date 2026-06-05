# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from pathlib import Path
import subprocess

from .refs import FindSDK
from utils import message


class FindMinecraft(FindSDK):
    _name_desc = "Mojang Minecraft"

    def __init__(self):
        super().__init__()

    def __WINDOWS__(self):
        minecraft_classic = self.everything("MinecraftLauncher.exe", precise=True)[0]
        minecraft_modern = self.everything("minecraft.exe", precise=True)[0]

        # 2 assert:
        # ASSERT MinecraftLauncher.exe is first in SYSTEM
        # ASSERT minecraft.exe is unique/singleton in SYSTEM

        if minecraft_classic:
            v = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    f'(Get-Item "{minecraft_classic}").VersionInfo.FileVersion',
                ],
                capture_output=True,
                text=True,
                check=True,
            ).stdout.strip()

            message(f"    Found Classic Minecraft Launcher {v}")

            self.add_rule(
                Module="mojang/minecraft/classic",
                mode="tcl",
                Include_file="template_mojang_minecraft",
                module_whaits="Minecraft Classic Launcher",
                root=Path(minecraft_classic).parent,
                PATH=["$root"],
            )

        if minecraft_modern:
            message("    Found New version Minecraft Launcher")
            self.add_rule(
                Module="mojang/minecraft/modern",
                mode="tcl",
                Include_file="template_mojang_minecraft",
                module_whaits="Minecraft Launcher",
                root=Path(minecraft_modern).parent,
                PATH=["$root"],
            )
