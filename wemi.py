
# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import sys
sys.dont_write_bytecode = True

def main():

    from utils.argparse_handler import args_update
    from tasks.driver import Driver
    from utils import config
    from tasks import seh

    args_update()
    seh.setup_excepthook()

    try:
        Driver.run(config.DEFAULT_TASK)
    except Exception as e:
        seh.unwind(type(e), e, e.__traceback__)
        raise SystemExit(1)

if __name__ == "__main__":
    main()
