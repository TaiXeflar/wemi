

 <!-- SPDX-License-Identifier: MIT
 Copyright (c) 2026-${year} WEMI Contributors
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT -->

# WΣMI (Windows Environment Modulefiles Installer)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
![version](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FTaiXeflar%2FWEMI%2Fmaster%2Fversion.json&query=%24.version&label=version&color=orange)
![License](https://img.shields.io/badge/License-MIT-blue)
![Platform](https://img.shields.io/badge/platform-Windows-blue)

| CI Stats | Status |
| :-- | :-- |
| Modules Only, AIO | [![Modules AIO Install Test](https://github.com/TaiXeflar/wemi/actions/workflows/modules-aio.yml/badge.svg?branch=master)](https://github.com/TaiXeflar/wemi/actions/workflows/modules-only-aio.yml) |

WEMI is a Experimential, Python based Environment Modules generator and installer, targeting on Windows 10/11 systems to solving enviromnent setups.

WEMI will scan, compile and install tcl Modulefiles to your Environment Modules system on your device.

<!-- SDK profiles -->
<div align="left">
  <a href="https://www.intel.com/content/www/us/en/developer/tools/oneapi/oneapi-toolkit.html" target="_blank">
    <img src="https://intel-corporation.gallerycdn.vsassets.io/extensions/intel-corporation/oneapi-samples/0.0.65/1777041053250/Microsoft.VisualStudio.Services.Icons.Default" height="50" alt="Intel oneAPI" title="Intel oneAPI" /></a> &nbsp;
  <a href="https://www.amd.com/en/developer/resources/rocm-hub/hip-sdk.html" target="_blank">
    <img src="https://cdn-icons-png.flaticon.com/512/5969/5969036.png" height="50" alt="AMD HIP SDK" title="AMD HIP SDK" /></a> &nbsp;
  <a href="https://github.com/ROCm/TheRock" target="_blank">
    <img src="https://avatars.githubusercontent.com/u/21157610?s=280&v=4" height="50" alt="ROCm/TheRock" title="ROCm/TheRock" /></a> &nbsp;
  <a href="https://developer.nvidia.com/downloads" target="_blank">
    <img src="https://avatars.githubusercontent.com/u/1728152?s=200&v=4" height="50" alt="NVIDIA CUDA/CUDA-X" title="NVIDIA CUDA/CUDA-X"/></a> &nbsp;
  <a href="https://visualstudio.microsoft.com/" target="_blank">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/Visual_Studio_2017_Logo.svg/3840px-Visual_Studio_2017_Logo.svg.png" height="50" alt="VS2017" title="VS2017" /></a> &nbsp;
  <a href="https://visualstudio.microsoft.com/" target="_blank">
    <img src="https://pics.computerbase.de/9/1/3/4/2/logo-256.png" height="50" alt="VS2019" title="VS2019" /></a> &nbsp;
  <a href="https://visualstudio.microsoft.com/" target="_blank">
    <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/2/2c/Visual_Studio_Icon_2022.svg/250px-Visual_Studio_Icon_2022.svg.png" height="50" alt="VS2022" title="VS2022" /></a> &nbsp;
  <a href="https://visualstudio.microsoft.com/" target="_blank">
    <img src="https://upload.wikimedia.org/wikipedia/commons/2/20/Visual_Studio_Icon_2026.svg"
    height="50" alt="VS2026" title="VS2026" /></a> &nbsp;
  <a href="https://mathworks.com/products/matlab.html" target="_blank">
    <img src="https://upload.wikimedia.org/wikipedia/commons/2/21/Matlab_Logo.png" height="50" alt="MATLAB" title="MATLAB" /></a> &nbsp;
  <a href="https://github.com/StrawberryPerl/Perl-Dist-Strawberry" target="_blank">
    <img src="https://images.emojiterra.com/google/noto-emoji/unicode-17.0/color/1024px/1f353.png" height="50" alt="Strawberry Perl" title="Strawberry Perl" /></a> &nbsp;
  <a href="https://cangjie-lang.cn/en" target="_blank">
    <img src="https://ide-innovation-lab.gallerycdn.vsassets.io/extensions/ide-innovation-lab/cangjie/1.1.0/1776234936844/Microsoft.VisualStudio.Services.Icons.Default" height="50" alt="Cangjie-Lang" title="Cangjie-Lang" /></a> &nbsp;

  <br>
  <a href="https://benghuai.com/" target="_blank">
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJgg8ThQup4mhDjvwv8WE7dE7Yd316UrrtEOxWxUkxow&s=10" height="50" alt="GGZ" title="GGZ" /></a> &nbsp;
  <a href="https://honkaiimpact3.hoyoverse.com/global/en-us/fab" target="_blank">
    <img src="https://play-lh.googleusercontent.com/hTMlfgsf_lKP7URBWrrdpoqL_AhXwuvIbeU-5Gn2R-8RE58z4Y28mfduo6MkfEBpP7Mtef7bnrXo5R9g1puG"
    height="50" alt="Honkai Impact 3" title="Honkai Impact 3" /></a> &nbsp;
  <a href="https://genshin.hoyoverse.com/" target="_blank">
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSoZLgx6Q1t60FoQIor6iW6P4VzN7X3_o_pNi5UPBr75g&s=10"
    height="50" alt="Genshin Impact" title="Genshin Impact" /></a> &nbsp;
  <a href="https://hsr.hoyoverse.com/" target="_blank">
    <img src="https://play-lh.googleusercontent.com/aWrGocSA7hEuk1qAPe7L4T57LvLKrwwH26cK2_LOqxRQMQX7j3uHYojC-EKWgYEV2PdrmE0ahqvvhLhXrAGk6Q"
    height="50" alt="Honkai: Star Rail" title="Honkai: Star Rail" /></a> &nbsp;
  <a href="https://zenless.hoyoverse.com/" target="_blank">
    <img src="https://play-lh.googleusercontent.com/X6TCjPjr0nhZqeBDn8TWB-gavRdDx42_S7xVkJ5SmAHefIFKIl7xPoob-MZXJZG5U4E"
    height="50" alt="ZZZ" title="ZZZ" /></a> &nbsp;
  <a href="https://hna.hoyoverse.com/" target="_blank">
    <img src="https://pbs.twimg.com/profile_images/2068894455588098048/Q__sajpM_400x400.jpg"
    height="50" alt="Honkai: Nexus Anima" title="Honkai: Nexus Anima" /></a> &nbsp;
  <a href="https://planet.hoyoverse.com/" target="_blank">
    <img src="https://pbs.twimg.com/profile_images/1970744550714155012/RiwrOC0N_400x400.jpg"
    height="50" alt="Petit Planet" title="Petit Planet" />
  </a>
</div>
<!-- SDK profiles -->

## Early State development

As WEMI declared current development status is in Early State development and version is InfDev status, WEMI will take several/lot of rolling destructable/refactoring changes, and not recieveng PR requests before a future stable release.

Issues and disscutions are open welcomed.

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
    ```
    # Configure All-In-One command     (generates build/cache.json.)
    (.venv) PS X:\wemi> python ./wemi.py configure --aio/-D_ALL_IN_ONE --<flags/options> -D<FLAGS/OPTIONS>
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

WEMI strongly not recommend set non Latin characters, full widith characters, half/full width spaces, dots, laft/right slashes as your user name. This is not WEMI cases because most development toolchains are prefer English environment, include full english charcters path.

Instead, PC users should keep their names to English based names, dashes and underscores to avoid any cross-platform program have not complete support to it.

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
