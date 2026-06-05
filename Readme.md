<!-- # SPDX-License-Identifier: MIT -->    
<!-- # Copyright (c) 2026 TaiXeflar  -->

# Windows Environment Modulefiles Installer (WEMI)

WEMI is a Experimential, Python based Environment Modules generator and installer, targeting on Windows 10/11 PowerShell systems to solving enviromnent setups.

If you have problems like:
 - Many CUDA_PATH_VXXX and dont know how to set it get false CUDA path setups
 - Developer Prompt for Visual Studio is not working
 - Have path management problems ...
 - From macOS/Linux/BSDs Environment Modules develop to Windows

Then you can try have a WEMI setup, to make your Windows device have toolchains control like Linux HPC clusters.

## Requirements
 - Python environment, recommends with [Astral UV][] venv.
 - [Everything][]
 - [Everything CLI][]
 - [gsudo][]
 - A installed [Environment Modules][] environment

## Limitations

Cygwin/MSYS2 Environment is not available to run wemi with their Python executables are `posix` model, doesn't contain `winreg` in Python Standard Library.

The solution is open a venv with `win32` based Python model, with `uv` is the fastest way to run it. The installation doesn't effected with Python `posix`/`win32` differences, by you can just set a install prefix.


## Usage

1. Clone this repo and build a venv.

- PowerShell / CMD
    ```
    PS X:\> git clone https://github/TaiXeflar/wemi.git --depth=1 wemi

    PS X:\> cd wemi

    PS X:\wemi> uv venv .venv --python 3.11/3.12/3.13/3.14

    PS X:\wemi> .venv/Scripts/Activate.ps1
    ```
2. Do configuration Steps. Run `wemi.py`, generate a intermediate information/configuration result cache JSON format file named `cache.json`.
- PowerShell
    ```
    (.venv) PS X:\wemi> python ./wemi.py configure --<flags/options> -D<FLAGS/OPTIONS>
    ```

3. Base on `cache.json`, make WEMI start compile target Tcl Modulefiles.
- PowerShell
    ```
    (.venv) PS X:\wemi> python ./wemi.py build
    ```

4. Install the modulefiles. For system level installation can use gsudo.
- PowerShell
    ```
    (.venv) PS X:\wemi> python ./wemi.py install --prefix "C:/Developer/Modules"
    ```

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


