# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import json
import shutil
from pathlib import Path
from textwrap import dedent

from tasks import ModulesObject
from utils import message, config


class Installer:
    def install(self):
        dest = config.MODULE_INSTALL_PREFIX

        if not dest:
            raise ValueError(
                dedent("""\
                Install prefix cannot be None or empty.
            """)
            )

        dest = self._path_fixer(dest)

        install_dir = dest / "modulefiles"

        cache_file = Path("build/cache.json")

        if not cache_file.exists():
            raise FileNotFoundError("Cannot find build rules from build/cache.json")

        cache_data = json.loads(cache_file.read_text(encoding="utf-8"))
        cache = [ModulesObject(obj) for obj in cache_data]
        cache_n = len(cache)

        message("[1/1] Install build Tcl Modulefiles ...")

        inst_msg = []
        for i, obj in enumerate(cache):
            try:
                src_file = Path("build/modulefiles") / obj.output
                dst_file = install_dir / obj.output

                dst_file.parent.mkdir(parents=True, exist_ok=True)

                shutil.copyfile(src_file, dst_file)

                inst_msg.append(f" -- Installing: {dst_file.as_posix()}")

            except FileNotFoundError:
                raise FileNotFoundError(
                    dedent(f"""\
                    Installing Modulefile {obj.output} ({i}/{cache_n}) raised FileNotFoundError:
                    Expected Modulefile {obj.output} is not in build/ directory.
                    Please check for it and re-build.""")
                )

            except PermissionError:
                raise PermissionError(
                    dedent(f"""\
                    Installing Modulefile {obj.output} ({i}/{cache_n}) raised PermissionError:
                    Installation to directory {dst_file.parent} has been denied.""")
                )

        message("NOTICE", "\n".join(inst_msg))

    def _path_fixer(self, pth: Path | str, /) -> Path:
        if isinstance(pth, (Path, str)):
            return Path(pth)
        else:
            raise TypeError(
                f"Found invalid type/value of install directory with {pth} ({type(pth).__name__})"
            )
