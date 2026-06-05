
# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import sys
from utils.argparse_handler import args_update
from tasks.driver import Driver
from utils import config
from tasks import seh

sys.dont_write_bytecode = True


def main():
    args_update()
    seh.setup_excepthook()
    Driver.run(config.DEFAULT_TASK)


if __name__ == "__main__":
    main()
