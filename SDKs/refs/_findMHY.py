# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

# SPDX-License-Identifier: MIT
# Copyright.c 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from typing import Literal

MIHOYO_PROJECTS_TYPEHINT = Literal[
    "FlyMeToTheMoon",
    "BH2.CN",
    "BH2.JP",
    "BH3.ZH",
    "BH3.JP",
    "BH3.KR",
    "BH3.SEA",
    "BH3.EU_USA",
    "Genshin",
    "HKSR",
    "ZZZ",
    "HNA",
    "PPT",
    "Varzapura",
]

mihoyo_app_registry_phonebook = {
    "FlyMeToTheMoon": None,
    "BH2.CN": None,
    "BH2.JP": None,
    "BH3.ZH": r"Software\Cognosphere\HYP\1_0\bh3_globalasia_official",
    "BH3.JP": r"Software\Cognosphere\HYP\1_0\bh3_globaljp_official",
    "BH3.KR": r"Software\Cognosphere\HYP\1_0\bh3_globalkr_official",
    "BH3.SEA": r"Software\Cognosphere\HYP\1_0\bh3_globaloverseas_official",
    "BH3.EU_USA": r"Software\Cognosphere\HYP\1_0\bh3_globalglb_official",
    "Genshin": r"Software\Cognosphere\HYP\1_0\hk4e_global",
    "HKSR": r"Software\Cognosphere\HYP\1_0\hkrpg_global",
    "ZZZ": r"Software\Cognosphere\HYP\1_0\nap_global",
    "HNA": None,
    "PPT": None,
    "Varzapura": None,
}

mihoyo_cn_app_registry_phonebook = {
    "FlyMeToTheMoon": None,
    "BH2.CN": None,
    "BH2.JP": None,
    "BH3.CN": r"Software\miHoYo\HYP\1_1\bh3_cn",
    "Genshin": r"Software\Cognosphere\HYP\1_0\hk4e_cn",
    "HKSR": r"Software\Cognosphere\HYP\1_0\hkrpg_cn",
    "ZZZ": r"Software\Cognosphere\HYP\1_0\nap_cn",
    "HNA": None,
    "PPT": None,
    "Varzapura": None,
}


mihoyo_app_include_file_dict = {
    "FlyMeToTheMoon": None,
    "BH2.CN": r"template_mhy_bh2",
    "BH2.JP": r"template_mhy_bh2",
    "BH3.ZH": r"template_mhy_bh3",
    "BH3.JP": r"template_mhy_bh3",
    "BH3.KR": r"template_mhy_bh3",
    "BH3.SEA": r"template_mhy_bh3",
    "BH3.EU_USA": r"template_mhy_bh3",
    "Genshin": r"template_mhy_genshin",
    "HKSR": r"template_mhy_starrail",
    "ZZZ": r"template_mhy_zzz",
    "HNA": r"template_mhy_nexusanima",
    "PPT": r'template_mhy_petitplanet',
    "Varzapura": r"template_mhy_varsapura",
}
