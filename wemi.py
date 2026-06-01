# SPDX-License-Identifier: MIT
# Copyright (c) 2026 TaiXeflar

import sys
sys.dont_write_bytecode = True


from utils.functions import clear
from utils.argparse_handler import args_update

from pprint import pprint

from tasks.driver import Driver
from utils import config
from tasks import seh


def main():
    args_update()
    seh.setup_excepthook()
    Driver.run(config.DEFAULT_TASK)

    
if __name__ == "__main__":
    main()