import json
import shutil
from pathlib import Path
from textwrap import dedent

from tasks import ModulesObject
from utils import message, config

class Installer:

    def install(self): 

        dest = config.MODULE_INSTALL_PREFIX

        if not dest:  # 直接檢查 None 或空字串更簡潔
            raise ValueError(dedent('''\
                Install prefix cannot be None or empty.
            '''))
        
        dest = self._path_fixer(dest)
        # 決定最終的安裝目標目錄 (假設你要放在 dest 下的 modulefiles)
        # 如果你還是想用 config.MODULE_INSTALL_PREFIX，請把這裡的 dest 換掉
        install_dir = dest / 'modulefiles'

        cache_file = Path("build/cache.json")

        if not cache_file.exists():
            raise FileNotFoundError('Cannot find build rules from build/cache.json')
        
        # 優化：利用 Path.read_text() 直接讀取並解碼，省去 .open().read() 的繁瑣
        cache_data = json.loads(cache_file.read_text(encoding='utf-8'))
        cache = [ModulesObject(obj) for obj in cache_data]
        cache_n = len(cache)

        message('[1/1] Install build Tcl Modulefiles ...')

        inst_msg = []
        for i, obj in enumerate(cache):
            try:
                src_file = Path('build/modulefiles') / obj.output
                dst_file = install_dir / obj.output
                
                dst_file.parent.mkdir(parents=True, exist_ok=True)

                # 【關鍵修改】放棄 copy2，改用最輕量的 copyfile
                shutil.copyfile(src_file, dst_file)

                inst_msg.append(f' -- Installing: {dst_file.as_posix()}')
                
                # message('STATUS', f'Installing: {dst_file.as_posix()}')

            except FileNotFoundError:
                raise FileNotFoundError(dedent(f'''\
                    Installing Modulefile {obj.output} ({i}/{cache_n}) raised FileNotFoundError:
                    Expected Modulefile {obj.output} is not in build/ directory.
                    Please check for it and re-build.'''))

            except PermissionError:
                raise PermissionError(dedent(f'''\
                    Installing Modulefile {obj.output} ({i}/{cache_n}) raised PermissionError:
                    Installation to directory {dst_file.parent} has been denied.'''))

        message("NOTICE", "\n".join(inst_msg))
            

    def _path_fixer(self, pth: Path | str, /) -> Path:
        if isinstance(pth, (Path, str)):
            return Path(pth)
        else:
            raise TypeError(f'Found invalid type/value of install directory with {pth} ({type(pth).__name__})')