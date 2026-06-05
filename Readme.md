

 <!-- SPDX-License-Identifier: MIT
 Copyright (c) 2026-${year} WEMI Contributors
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT -->

# Windows Environment Modulefiles Installer (WEMI)

![version](https://img.shields.io/badge/dynamic/yaml?url=https%3A%2F%2Fraw.githubusercontent.com%2FTaiXeflar%2FWEMI%2Fmaster%2Fversion&query=%24&label=version&color=orange) [![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
![Platform](https://img.shields.io/badge/platform-Windows-blue)

WEMI is a Experimential, Python based Environment Modules generator and installer, targeting on Windows 10/11 systems to solving enviromnent setups.

WEMI will scan, compile and install tcl Modulefiles to your Environment Modules system on your device.

## Early State development

As WEMI declared current development status is in Early State development and version is InfDev 0.0.1, WEMI will take several/lot of destructable/refactoring changes, and not recieveng PR requests after a stable release.

Issues and disscutions are open welcomed (Exclude toxic topics).

## Requirements
 - Python environment, recommends with [Astral UV][] venv.
 - [Everything][]
 - [Everything CLI][]
 - [gsudo][]
 - A installed [Environment Modules][] environment

## Usage

1. Clone this repo and build a venv.
- PowerShell / CMD
    ```
    PS X:\> git clone https://github/TaiXeflar/wemi.git --depth=1 wemi

    PS X:\> cd wemi

    PS X:\wemi> uv venv .venv --python 3.11/3.12/3.13/3.14

    PS X:\wemi> .venv/Scripts/Activate.ps1
    ```
2. Run `wemi.py`. WEMI allows (some) Unix-style flags `-flag`/`--flags`, DOS-style flags `/flags`, and cmake-style cache flags `-DFLAGS...`.
- PowerShell
    ```
    # Configure     (generates build/cache.json.)
    (.venv) PS X:\wemi> python ./wemi.py configure --<flags/options> -D<FLAGS/OPTIONS>

    # Build         (based on build/cache.json.)
    (.venv) PS X:\wemi> python ./wemi.py build

    # Install       (based on build/cache.json.)
    (.venv) PS X:\wemi> python ./wemi.py install --prefix "C:/Developer/Modules"
    ```

## Limitations

Cygwin/MSYS2 Environment is not available to run wemi with their Python executables are `posix` model, doesn't contain `winreg` in Python Standard Library.

The solution is open a venv with `win32` based Python model, with `uv` is the fastest way to run it. The installation doesn't effected with Python `posix`/`win32` differences, by you can just set a install prefix.


### Caveats

WEMI have not tested Path with non Latin charcters languages yet:
 - Traditional Chinese (ZH-TW, Big5): Complexed Chinese word character, common used by Taiwan, Hong Kong, Macao.
 - Simplfied Chinese (ZH-CN, GBK): Simplfied Chinese word character, common used by Mainland China area.
 - Japanese (JA, Shift-JIS): Japanese uses Kanji, Hiragana and Katakana.
 - Korean (KR).

WEMI strongly not recommend set non Latin characters, full widith characters, half/full width spaces, dots, laft/right slashes as your user name.

Instead, PC users should keep their names to English based names, dashes and underscores to avoid any cross-platform program
 have not complete support to it.

 For example:
 - Avoid names like `C:/Users/三月七`, `C:/Users/琪亞娜　卡斯蘭娜`.
 - Recommend user names: `C:/Users/SilverWolf999`, `C:/Users/Miku39`, `C:/Users/OMNI_1206` etc.


WEMI have not tested on Cygwin/MSYS2 environment yet. I will do later tests by trying compile several projects.


### Language Localization
Currently main language will be written in English (US). With after updates, there will several languages updates to docunemtation and wemi program.

<!--    Websites    -->

[Astral UV]:                            https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_2

[Everything]:                           https://www.voidtools.com/downloads/

[Everything CLI]:                       https://github.com/voidtools/ES

[gsudo]:                                https://github.com/gerardog/gsudo

[Environment Modules]:                  https://github.com/envmodules/modules

### The idea/inventing monent
This project is based on my collage school lifetime thoughts and with listening [七見斷滅智論抄][Il Dottore] [Prajnaparamitopadesa to Quell Seven Calamities][Il Dottore].



<!-- links -->
[Il Dottore]:   https://youtu.be/jBfLW28avYU
