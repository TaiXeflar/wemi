


import sys
import importlib.util
from pathlib import Path
from textwrap import dedent

from utils import config
from utils.color_string import message
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
        self._template_cache = {}  # 用來快取已經載入的 template 類別

    def _load_template_class(self, include_path_str: str):
        """
        根據 Include File 的值 (例如 'NVIDIA/CUDA') 動態載入對應的 .py 檔案
        並回傳裡面的 Template 類別。
        """
        # 如果已經載入過，直接從快取拿
        if include_path_str in self._template_cache:
            return self._template_cache[include_path_str]

        # 將 'NVIDIA/CUDA' 轉換為路徑 'include/NVIDIA/CUDA.py'
        module_file_path = self.include_dir / f"{include_path_str}.py"
        
        if not module_file_path.exists():
            raise FileNotFoundError(f"錯誤: 找不到對應的 Template 檔案: {module_file_path}")

        # 動態 Import 的標準寫法
        module_name = f"include.{include_path_str.replace('/', '.')}" 
        spec = importlib.util.spec_from_file_location(module_name, module_file_path)
        module = importlib.util.module_from_spec(spec)
        
        # 將該模組暫時加入 sys.modules 以防內部有相對 import
        sys.modules[module_name] = module 
        spec.loader.exec_module(module)

        # 假設你的 template 檔案裡面都統一將類別命名為 `ModuleTemplate`
        # 例如: class ModuleTemplate: ...
        if not hasattr(module, 'ModuleTemplate'):
            raise NotImplementedError(f"錯誤: 標頭檔 {module_file_path.as_posix()} 中未定義 'ModuleTemplate' 類別")

        template_class = getattr(module, 'ModuleTemplate')
        
        # 存入快取
        self._template_cache[include_path_str] = template_class
        return template_class

    def compile(self, module_obj:ModulesObject):
        """
        核心編譯邏輯
        """

        # 1. 取得對應的 Include File 路徑 (例如 'NVIDIA/CUDA')
        include_val = module_obj.include_file
        if not include_val:
            raise FileNotFoundError(
                dedent(f'錯誤: 環境模組物件 {module_obj.MODULENAME} 找不到指定的 Tcl 模板 Python 標頭檔'))

        # 2. 動態載入 Template 類別並實例化 (把 module_obj 丟進去)
        TemplateClass = self._load_template_class(include_val)
        template_instance:BaseModuleTemplate = TemplateClass(module_obj)

        # 3. 取得渲染後的 Tcl 內容 (假設 template 有實作 render() 方法)
        tcl_context = template_instance.render()

        # 4. 準備輸出檔案
        # 這裡的邏輯可以自訂，例如根據 Module: "NVIDIA/CUDA/13.2.0"
        # 輸出到 output/NVIDIA/CUDA/13.2.0 檔案中
        out_path = self.output_dir / module_obj.output

        out_path.parent.mkdir(parents=True, exist_ok=True) # 確保父目錄存在

        # 5. 寫入檔案
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(tcl_context)
        
        return out_path