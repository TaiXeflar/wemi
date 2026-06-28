
# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from typing import Literal

from .refs import FindSDK
from tasks.objects import ModulesObject, ModulesZip

_VERLIST = Literal[
    '5.0.0', '5.0.1',
    '5.1.0', '5.1.1',
    '5.2.0',
    '5.3.0',
    '5.4.0',
    '5.5.0',
    '5.6.0', '5.6.1',
    'latest']

class AddModules(FindSDK):

    _name_desc = 'Environment Modules'

    def __init__(self, version:_VERLIST=None):

        self._v = version if version else 'latest'
        super().__init__()

    def __WINDOWS__(self):
        self.add_module_zip()
        self.add_module_scripts()

    def add_module_zip(self):
        z = ModulesZip(self._v)
        z.download()
        z.examine(hash_type='SHA256', chunk_size=65535)
        z.unzip('.deps')

    def add_module_scripts(self):
        print(' -- Generating Modules rules')

        modules_dir_files = [ # Modules/*/
            'bin/envml.cmd',
            'bin/ml.cmd',
            'bin/module.cmd',
            'init/cmd.cmd',
            'init/pwsh.ps1',
            'libexec/modulecmd.tcl',
            'modulefiles/module-git',
            'modulefiles/module-info',
            'modulefiles/null',

            'doc/ChangeLog.gz',
            'doc/CONTRIBUTING.txt',
            'doc/COPYING.GPLv2',
            'doc/envml.txt',
            'doc/INSTALL-win.rst',
            'doc/MIGRATING.txt',
            'doc/ml.txt',
            'doc/module.txt',
            'doc/modulefile.txt',
            'doc/NEWS.txt',
            'doc/README',
        ]
        modules_test_files = [ # Modules/test/
            'TESTINSTALL_PWSH.ps1',
            'TESTINSTALL.bat',
        ]

        self.add_rule([ModulesObject(
            Module=f,
            output=f,
            mode='file',
            Include_file='template_modulefile',
            src='.deps'
        ) for f in modules_dir_files])

        self.add_rule([ModulesObject(
            Module=f,
            output='test/'+f,
            mode='file',
            Include_file='template_modulefile',
            src='.deps'
        ) for f in modules_test_files])

        print(' -- Generating Modules rules')
