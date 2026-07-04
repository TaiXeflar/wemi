# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import sys
import importlib.util
import shutil
from pathlib import Path
from textwrap import dedent

from .objects.modulesobject import ModulesObject
from include.refs._template import BaseModuleTemplate

# from excepts import


class Compiler:
    def __init__(self):
        """
        ### 初始化編譯器

        :param include_dir: 存放 template (???.py) 的根目錄
        :param output_dir:  生成的 Tcl modulefile 輸出的根目錄
        """
        self.include_dir = Path("include")
        self.output_dir = Path("build/modulefiles/")
        self._template_cache = {}

    def _load_template_class(self, include_path_str: str):
        """
        根據 Include File 的值 (例如 'NVIDIA/CUDA') 動態載入對應的 .py 檔案
        並回傳裡面的 Template 類別。
        """
        if include_path_str in self._template_cache:
            return self._template_cache[include_path_str]

        module_file_path = self.include_dir / f"{include_path_str}.py"

        if not module_file_path.exists():
            raise FileNotFoundError(
                f"Error: Cannot find required include file: {module_file_path}"
            )

        module_name = f"include.{include_path_str.replace('/', '.')}"
        spec = importlib.util.spec_from_file_location(module_name, module_file_path)
        module = importlib.util.module_from_spec(spec)

        sys.modules[module_name] = module
        spec.loader.exec_module(module)

        if not hasattr(module, "ModuleTemplate"):
            raise NotImplementedError(
                f"Error: In {module_file_path.as_posix()} ModuleTemplate class has not defined"
            )

        template_class = getattr(module, "ModuleTemplate")

        self._template_cache[include_path_str] = template_class
        return template_class

    def compile(self, module_obj: ModulesObject):
        include_val = module_obj.include_file
        if not include_val:
            raise FileNotFoundError(
                dedent(
                    f"Error: ModulesObject {module_obj.MODULENAME} cannot find required Tclsh template Python header"
                )
            )

        TemplateClass = self._load_template_class(include_val)
        template_instance: BaseModuleTemplate = TemplateClass(module_obj)

        tcl_context = template_instance.render()
        out_path = self.output_dir / module_obj.output

        out_path.parent.mkdir(parents=True, exist_ok=True)

        with open(out_path, "w", encoding="utf-8") as f:
            f.write(tcl_context)

        return out_path

    def copy(self, module_obj: ModulesObject):
        output = module_obj.output
        src = module_obj._raw_data.get("src")

        srcfile = Path(src)
        out_path = self.output_dir / output
        out_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copyfile(src=srcfile, dst=out_path)
        return out_path
