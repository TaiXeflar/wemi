# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from pathlib import Path
from utils import message
import subprocess

from .refs._find_SDK import FindSDK
from tasks import ModulesObject


class FindStrawberryPerl(FindSDK):
    _name_desc = "Strawberry Perl"

    def __init__(self):
        super().__init__()

    def __WINDOWS__(self):
        try:
            perl_lst = [
                Path(perl).resolve()
                for perl in subprocess.run(
                    [self.es, r"\perl.exe"], check=True, capture_output=True, text=True
                ).stdout.splitlines()
                if (Path(perl).parent.parent.parent / "README.txt").exists()
            ]
        except Exception:
            return

        for perl in perl_lst:
            perl_v = self._find_version(perl, "--version", "X.Y.Z")
            perl_gcc = self._find_version(
                perl.parent.parent.parent / "c/bin/gcc.exe", "--version", "X.Y.Z"
            )
            perl_gcct = subprocess.run(
                [perl.parent.parent.parent / "c/bin/gcc.exe", "-dumpmachine"],
                text=True,
                capture_output=True,
                check=True,
            ).stdout.strip()
            perl_cmake = self._find_version(
                perl.parent.parent.parent / "c/bin/cmake.exe", "--version", "X.Y.Z"
            )
            perl_ninja = self._find_version(
                perl.parent.parent.parent / "c/bin/ninja.exe", "--version", "X.Y.Z"
            )

            message(f"    Perl {perl_v}     {perl.parent.parent.resolve().as_posix()}")
            message(f"\tGCC             {perl_gcc}, target {perl_gcct}")
            message(f"\tCMake           {perl_cmake}")
            message(f"\tNinja-build     {perl_ninja}")

            self.add_rule(
                ModulesObject(
                    Module=f"strawberry/{perl_v}",
                    output=f"strawberry/{perl_v}",
                    mode="tcl",
                    Include_file="template_strawberry",
                    Version=perl_v,
                    module_whaits=f"strawberry Perl {perl_v}",
                    conflicts=["strawberry"],
                    root=perl.resolve().as_posix(),
                    PATH=[
                        "$root/perl/bin",
                        "$root/perl/site/bin",
                        "$root/c/bin",
                        "$root/c/x86_64-w64-mingw32/bin",
                    ],
                    INCLUDE=["$root/c/include", "$root/c/x86_64-w64-mingw32/include"],
                    LIB=["$root/c/lib", "$root/c/x86_64-w64-mingw32/lib"],
                )
            )
