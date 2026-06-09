
# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

import json
from typing import Literal

with open(r'version.json') as f:
    v:dict[Literal['version'], str] = json.loads(f.read())

WEMI_VERSION = v.get('version')

MODULES_ZIP_VERSION_HASH = {
    '5.6.1': r'sha256:99a9c1dd8fd4ad4dc44538aa3df390c7b47ebd0f3ffe31a0eb18eae5148d330b',
    '5.6.0': r'sha256:5b9469fc19b69168b2555d1b9d39074d6024f029fa193bfb259c57b165e16ef3',
}
