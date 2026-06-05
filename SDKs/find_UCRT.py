# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from pathlib import Path

from .refs import FindSDK
from .refs._findVS20XX import cpu_host_arch
from utils import regedit, subdirs, message
from tasks import ModulesObject

arch = cpu_host_arch()


class FindUCRT(FindSDK):
    _name_desc = "Universal CRT / Windows SDK"

    def __init__(self):
        super().__init__()

    def __WINDOWS__(self):
        super().__WINDOWS__()

        # Windows SDK (UCRT)
        ucrt_root = regedit(
            r"HKLM",
            r"SOFTWARE\Microsoft\Windows Kits\Installed Roots",
            key_name=r"KitsRoot10",
        )
        if ucrt_root:
            ucrt_root = Path(ucrt_root).resolve()

            ucrt_versions = regedit(
                r"HKLM", r"SOFTWARE\Microsoft\Windows Kits\Installed Roots"
            )
            for ucrt in ucrt_versions:
                archs = subdirs(ucrt_root / "Lib" / ucrt / "ucrt", leaf=True)

                message(f"\tUCRT {ucrt}")

                self.add_rule(
                    [
                        ModulesObject(
                            Module=f"winsdk/{arch}/ucrt/{ucrt}",
                            mode="tcl",
                            output=f".deps/winsdk/{arch}/ucrt/{ucrt}",
                            Include_file="template_ucrt",
                            Version=ucrt,
                            root=ucrt_root.as_posix(),
                            deps=[],
                            conflicts=["UCRT"],
                            VARs={
                                "UCRT_VERSION": ucrt,
                                "UCRT_ROOT": ucrt_root,
                                "UCRT_ARCH": arch,
                            },
                            ENVs={
                                "UCRTVersion": "$UCRT_VERSION",
                                "UniversalCRTSdkDir": "$UCRT_ROOT",
                                "WindowsSDKVersion": "$UCRT_VERSION",
                                "WindowsSDKLibVersion": "$UCRT_VERSION",
                                "WindowsLibPath": "$UCRT_ROOT/UnionMetadata/$UCRT_VERSION; $UCRT_ROOT/References/$UCRT_VERSION",
                                "WindowsSdkVerBinPath": "$UCRT_ROOT/bin/$UCRT_VERSION",
                            },
                            PATH=[
                                "$root/bin/$UCRT_ARCH",
                                "$root/bin/$UCRT_VERSION/$UCRT_ARCH",
                            ],
                            INCLUDE=[
                                "$root/include/$UCRT_VERSION/ucrt",
                                "$root/include/$UCRT_VERSION/um",
                                "$root/include/$UCRT_VERSION/winrt",
                                "$root/include/$UCRT_VERSION/shared",
                                "$root/include/$UCRT_VERSION/cppwinrt",
                            ],
                            LIB=[
                                "$root/lib/$UCRT_VERSION/ucrt/$UCRT_ARCH",
                                "$root/lib/$UCRT_VERSION/um/$UCRT_ARCH",
                            ],
                        )
                        for arch in archs
                    ]
                )

            for ucrt in ucrt_versions:
                self.update(
                    f"Windows SDK {ucrt}",
                    {"Path": f"{Path(ucrt_root/ucrt).resolve().as_posix()}"},
                )

        else:
            pass
