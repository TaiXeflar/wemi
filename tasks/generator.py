


import sys
import json
import time
from pathlib import Path
from textwrap import dedent
import math


from utils import config, message, cstring
from tasks import seh

from .objects.modulesobject import ModulesObject
from .compiler import Compiler


class Generator():

    def __init__(self):
        self.scheduler = self.schedule()

    def schedule(self):
        try: 
            build_cache_list: list[ModulesObject] = [
                ModulesObject(tgt) for tgt in json.loads(Path("build/cache.json").read_text())]
            build_schedule_dict: dict[str, ModulesObject] = {
                str(i+1): tgt for i, tgt in enumerate(build_cache_list)
            }
        except FileNotFoundError:
            raise FileNotFoundError(f'Cannot Found generated build/cache.json')
        
        except json.JSONDecodeError:
            raise json.JSONDecodeError(f'Cannot analyze build/cache.json with decode error')

        return build_schedule_dict

    def build(self):
        failed = 0

        total = len(self.scheduler)
        for idx, tgt in self.scheduler.items():
            idx = int(idx)
            compiler = Compiler()

            if config.GENERATOR_STYLE == "ninja":
                compile_tgt_disp = f"[{idx}/{total}] Building {tgt.objtype} Modulefile Object {tgt.output}"
                sys.stdout.write(dedent(f'''\r{compile_tgt_disp:<150}'''))
                sys.stdout.flush()

            elif config.GENERATOR_STYLE == "make":
                per = math.floor((idx/total* 100)) 
                compile_tgt_disp = f"[{per:>4}%] Building {tgt.objtype} Modulefile Object {tgt.output}"
                sys.stdout.write(f"{compile_tgt_disp:<120}\n")
                sys.stdout.flush()
                

            try:
                time.sleep(0.05)
                compiler.compile(tgt)

            except KeyboardInterrupt as e:
                # Ctrl + C
                print("")
                fail_hint = cstring("FAILED", (255, 0, 0), "BOLD")
                message("NOTICE", dedent(f"{fail_hint}: build/{tgt.MODULENAME}"))

                seh.unwind(type(e), e, e.__traceback__)
                
                # Linux/UNIX sigint 130
                sys.exit(130)

            except Exception as e:
                print("")
                fail_hint = cstring("FAILED", (255, 0, 0), "BOLD")
                message("NOTICE", dedent(f"{fail_hint}: build/{tgt.MODULENAME}"))
                message("ERROR", dedent(f'{str(e)}'))
                
                if not config.TOO_LONG_DIDNT_READ:
                    seh.unwind(type(e), e, e.__traceback__)
                
                if config.NO_COMPILE_FAIL_STOP:
                    message("ERROR", dedent(f"""\
                        Warning: Modules Object {tgt.MODULENAME} compile failed with Python raised {e.__class__.__name__}, 
                        but wemi generator will continue with flag NO_COMPILE_FAIL_STOP is true.
                        """))
                    failed += 1
                    continue
                else:
                    sys.exit(1)
        
        # FORCE_COMPILE_CONTINUE
        if failed:
            message("")
            message("ERROR", dedent(f"""\
                                    
                WEMI generator have {failed} compilation errors while generating targeted Tcl Modulefiles. 
                Please check on these information:
                 > The reported error type
                 > Your system have the correct SDK, Toolchain installation
                
                """))                            

    def stop(self, e:Exception=None):
        import sys
        message("ERROR", f"Progress Terminated.")
        
        raise e if e else sys.exit(1)

            
    