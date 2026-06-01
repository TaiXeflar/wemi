

from typing import Literal

MIHOYO_PROJECTS_TYPEHINT = Literal[
    "FlyMeToTheMoon",
    "GunsGirlZ (CN)",
    "GunsGirlZ (JP)",
    "HonkaiImpact3 (ZH)",
    "HonkaiImpact3 (JP)",
    "HonkaiImpact3 (KR)",
    "HonkaiImpact3 (SEA)",
    "HonkaiImpact3 (EU_USA)",
    "GenshinImpact",
    "HonkaiStarRail",
    "ZenlessZoneZero",
    "HonkaiNexusAnima",
    "Varzapura",
    "TearsOfThemis",
]

mihoyo_app_registry_phonebook = {
    "FlyMeToTheMoon":           None,
    "GunsGirlZ (CN)":           None,
    "GunsGirlZ (JP)":           None,
    "HonkaiImpact3 (ZH)":       r"Software\Cognosphere\HYP\1_0\bh3_globalasia_official",
    "HonkaiImpact3 (JP)":       r"Software\Cognosphere\HYP\1_0\bh3_globaljp_official",
    "HonkaiImpact3 (KR)":       r"Software\Cognosphere\HYP\1_0\bh3_globalkr_official",
    "HonkaiImpact3 (SEA)":      r"Software\Cognosphere\HYP\1_0\bh3_globaloverseas_official",
    "HonkaiImpact3 (EU_USA)":   r"Software\Cognosphere\HYP\1_0\bh3_globalglb_official",
    "GenshinImpact":            r"Software\Cognosphere\HYP\1_0\hk4e_global",
    "HonkaiStarRail":           r"Software\Cognosphere\HYP\1_0\hkrpg_global",
    "ZenlessZoneZero":          r"Software\Cognosphere\HYP\1_0\nap_global",
    "HonkaiNexusAnima":         None,
    "Varzapura":                None,
    "TearsOfThemis":            None,
}

mihoyo_app_include_file_dict = {
    "FlyMeToTheMoon":           None,
    "GunsGirlZ (CN)":           r"template_mhy_bh2",
    "GunsGirlZ (JP)":           r"template_mhy_bh2",
    "HonkaiImpact3 (ZH)":       r"template_mhy_bh3",
    "HonkaiImpact3 (JP)":       r"template_mhy_bh3",
    "HonkaiImpact3 (KR)":       r"template_mhy_bh3",
    "HonkaiImpact3 (SEA)":      r"template_mhy_bh3",
    "HonkaiImpact3 (EU_USA)":   r"template_mhy_bh3",
    "GenshinImpact":            r"template_mhy_genshin",
    "HonkaiStarRail":           r"template_mhy_starrail",
    "ZenlessZoneZero":          r"template_mhy_zzz",
    "HonkaiNexusAnima":         r"template_mhy_nexusanima",
    "Varzapura":                r"template_mhy_varsapura",
    "TearsOfThemis":            r"template_mhy_tot",
}