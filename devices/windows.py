

# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from pathlib import Path
import json
from textwrap import dedent

from SDKs.refs import FindSDK
from SDKs import *

from utils import message, tic_toc, config


from tasks import seh, ModulesObject, modules_object_json_encoder
from .windows_checks import WindowsCheck


class WindowsNT:
    _SDK_REGISTRY: dict[str, FindSDK] = {
        "TheRock": FindTheRock,
        "HIP": FindHIPSDK,
        "CUDA": FindCUDA,
        "CUDA-X": FindCUDAX,
        "oneAPI": FindOneAPI,
        "VS20XX": FindVS20XX,
        "UCRT": FindUCRT,
        # "MSMPI": FindMSMPI,
        # "MPISDK": FindMSMPISDK,
        "Cangjie": FindCangjie,
        "GMT": FindGMT,
        "MATLAB": FindMATLAB,
        "Strawberry": FindStrawberryPerl,
    }

    @tic_toc("Configuring Done")
    def __init__(self):
        WindowsCheck()

        self.info: dict[str, FindSDK] = {}

        raw_target_sdks = getattr(config, "ENABLE_SDKS", [])
        registry_lower = {k.lower(): v for k, v in self._SDK_REGISTRY.items()}

        if not raw_target_sdks:
            target_sdks = list(self._SDK_REGISTRY.keys())
            message(" -- WEMI Enabled All SDK scanning.")
        else:
            target_sdks = raw_target_sdks
            message(f" -- WEMI Selected SDKs: {target_sdks}")

        for sdk_name in target_sdks:

            sdk_class = registry_lower.get(sdk_name.lower())
            if sdk_class:
                self.info[sdk_name] = sdk_class()
            else:
                message(f"[Warning] Cannot Find SDK type'{sdk_name}'.")

        # Experimential
        if config.EXP_MIHOYO_SDK:
            self.info["MiHoYo"] = FindMiHoYo()

        if config.ADD_MODULES or not config.NO_MODULES:
            self.info['Modules'] = AddModules(config.MODULE_ZIP_VERSION)

        self.rules: list[ModulesObject] = []
        try:
            for sdk in self.info.values():
                if sdk.rules:
                    self.rules.extend(sdk.rules)

        except KeyboardInterrupt as e:
            seh.unwind(type(e), e, e.__traceback__)

    @tic_toc("Generating Done")
    def export(self):
        cache = Path("build/cache.json")
        cache.parent.mkdir(parents=True, exist_ok=True)

        try:
            with cache.open("w", encoding="utf-8") as f:
                f.write(
                    json.dumps(
                        self.rules, default=modules_object_json_encoder, indent=4
                    )
                )

        except PermissionError:
            raise PermissionError(
                dedent("""\
                WEMI cannot export build rules with Permission error occured.
                """)
            )
        except Exception as e:
            print(e)
