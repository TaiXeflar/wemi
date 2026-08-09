

 <!-- SPDX-License-Identifier: MIT
 Copyright (c) 2026-${year} WEMI Contributors
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT -->

# WΣMI (Windows Environment Modulefiles Installer)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
![version](https://img.shields.io/badge/dynamic/json?url=https%3A%2F%2Fraw.githubusercontent.com%2FTaiXeflar%2FWEMI%2Fmaster%2Fversion.json&query=%24.version&label=version&color=orange)
![License](https://img.shields.io/badge/License-MIT-blue)

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
  <!-- <a href="https://benghuai.com/" target="_blank">
    <img src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSJgg8ThQup4mhDjvwv8WE7dE7Yd316UrrtEOxWxUkxow&s=10" height="50" alt="GGZ" title="GGZ" /></a> &nbsp; -->
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

As WEMI declared current development status is in Early State development and version is InfDev status,
WEMI will take several/lot of rolling destructable/refactoring changes, and not recieveng PR requests before a future stable release.

Issues and disscutions are open welcomed.

## CI status (Under maintainence: Refactoring CI Task)

CI Testing are based on `windows-2025` runner.

Status will be blank as the test case is pending for CI design.

- Windows Platform
    | Platform Support Status |
    | :--: |
    | ![Windows AMD64][badge-windows-amd64] |
    | ![Windows ARM64][badge-windows-arm64] |

  <!-- platform -->
  [badge-windows-amd64]: https://img.shields.io/badge/Windows%20AMD64-Enabled-blue?logo=windows11&logoColor=white&labelColor=555
  [badge-windows-arm64]: https://img.shields.io/badge/Windows%20ARM64-Disabled-black?logo=windows11&logoColor=white&labelColor=555

- pre-commit, Python 3 version test
    | task | information/details | status |
    | :-- | :-- | :-- |
    | pre-commit | pre-commit | [![pre-commit-ci-badge][pre-commit-ci-action]][pre-commit-ci-act]   |
    | Python test | uv, CPython 3.10.13     | [![python-310-badge][python-310-ci]][python-310-test] |
    | Python test | uv, CPython 3.11.9      | [![python-311-badge][python-311-ci]][python-311-test] |
    | Python test | uv, CPython 3.12.13     | [![python-312-badge][python-312-ci]][python-312-test] |
    | Python test | uv, CPython 3.13.12     | [![python-313-badge][python-313-ci]][python-313-test] |
    | Python test | uv, CPython 3.14.2      | [![python-314-badge][python-314-ci]][python-314-test] |
    | Python test | uv, CPython 3.15.0a     | [![python-315-badge][python-315-ci]][python-315-test] |

  <!-- CI: pre-commit -->
  [pre-commit-ci-action]: https://github.com/TaiXeflar/wemi/actions/workflows/pre-commit.yaml/badge.svg?branch=master
  [pre-commit-ci-act]:    https://github.com/TaiXeflar/wemi/actions/workflows/pre-commit.yaml

  <!-- CI: Python version case -->
  [python-310-ci]:   https://github.com/TaiXeflar/wemi/actions/workflows/python-310-test.yaml/badge.svg?branch=master
  [python-310-test]: https://github.com/TaiXeflar/wemi/actions/workflows/python-310-test.yaml

  [python-311-ci]: https://github.com/TaiXeflar/wemi/actions/workflows/python-311-test.yaml/badge.svg?branch=master
  [python-311-test]: https://github.com/TaiXeflar/wemi/actions/workflows/python-311-test.yaml

  [python-312-ci]:   https://github.com/TaiXeflar/wemi/actions/workflows/python-312-test.yaml/badge.svg?branch=master
  [python-312-test]: https://github.com/TaiXeflar/wemi/actions/workflows/python-312-test.yaml

  [python-313-ci]:   https://github.com/TaiXeflar/wemi/actions/workflows/python-313-test.yaml/badge.svg?branch=master
  [python-313-test]: https://github.com/TaiXeflar/wemi/actions/workflows/python-313-test.yaml

  [python-314-ci]:   https://github.com/TaiXeflar/wemi/actions/workflows/python-314-test.yaml/badge.svg?branch=master
  [python-314-test]: https://github.com/TaiXeflar/wemi/actions/workflows/python-314-test.yaml

  [python-315-ci]:   https://github.com/TaiXeflar/wemi/actions/workflows/python-315-test.yaml/badge.svg?branch=master
  [python-315-test]: https://github.com/TaiXeflar/wemi/actions/workflows/python-315-test.yaml

- Compiler smoke test

    | task              | toolchain                                   | status  |
    | :--               | :--                                         | :--     |
    | Visual C/C++      | MSVC v145                                   | [![msvc-badge][msvc-ci]][msvc-ci-test]  |
    | Intel C++         | MSVC v145, oneAPI latest                    | [![intel-badge][intel-ci]][intel-test]  |
    | NVIDIA CUDA Host  | MSVC v145, CUDA 13.2                        | [![cuda-badge][cuda-ci]][cuda-test]     |
    | AMD HIP SDK       | MSVC v145, HIP `???`                        | No avail release via winget             |
    | AMD ROCm/TheRock  | MSVC v145, TheRock `7.XX`                   | No avail release via winget             |
    | Cangjie Language  | Cangjie 1.1.0                               | [![cangjie-badge][cangjie-ci]][cj-test] |
    | Swift Language    | ----                                        | No ETA; Pending for develop test        |
    | Rust  Language    | ----                                        | No ETA                                  |
    | Zig   Language    | ----                                        | No ETA; Pending for develop test        |
    | Zen-C Language    | ----                                        | No ETA; Pending for develop test        |
    | Perl Languange    | ----                                        | No ETA; Pending for is Strawberry       |
    | Ruby Languange    | ----                                        | No ETA; Pending for develop test        |
    | Java Language     | ----                                        | No ETA; Pending for develop test        |
    | Go Language       | ----                                        | No ETA; Pending for develop test        |
    | Codon             | ----                                        | No ETA; Pending Exaloop release windows version |

    [msvc-ci]:      https://github.com/TaiXeflar/wemi/actions/workflows/vs2026-msvc-v145.yaml/badge.svg?branch=master
    [msvc-ci-test]: https://github.com/TaiXeflar/wemi/actions/workflows/vs2026-msvc-v145.yaml

    [intel-ci]:     https://github.com/TaiXeflar/wemi/actions/workflows/vs2026-intel-test.yaml/badge.svg?branch=master
    [intel-test]:   https://github.com/TaiXeflar/wemi/actions/workflows/vs2026-intel-test.yaml

    [cuda-ci]:      https://github.com/TaiXeflar/wemi/actions/workflows/vs2026-nvda-test.yaml/badge.svg?branch=master
    [cuda-test]:    https://github.com/TaiXeflar/wemi/actions/workflows/vs2026-nvda-test.yaml

    [cangjie-ci]:   https://github.com/TaiXeflar/wemi/actions/workflows/cangjie-105-test.yaml/badge.svg?branch=master
    [cj-test]:      https://github.com/TaiXeflar/wemi/actions/workflows/cangjie-105-test.yaml

- Build test, Recursive build examination (No eta)

    | task                | toolchain                           | condition | status   |
    | :--                 | :--                                 | :--       | :--     |
    | [ROCm/TheRock]      | VS2026, MSVC v145, Perl 5.42        | `-DTHEROCK_AMDGPU_FAMILIES = gfx1100;gfx1101;gfx1102;gfx1200;gfx1201` |
    | [NVIDIA/cutlass]    | VS2026, MSVC v145, CUDA 13.4        | `-DBUILD_TESTS=OFF`                                                   |
    | [pytorch/pytorch]   | VS2026, MSVC v145, CUDA 13.4        | `-DUSE_CUDA=1`, `-DUSE_CUDNN=1`, `-DUSE_CUDSS=1` |
    | [pytorch/pytorch]   | VS2026, MSVC v145, TheRock          | `-DUSE_ROCM=1` |
    | [python/cpython]    | VS2026, MSVC v145                   |
    | [exaloop/codon]     | VS2026, MSVC v145, CUDA 13.4        | `-DCODON_GPU=ON` |
    | [HDF/HDF4]          | VS2026, MSVC v145                   |
    | [HDF/HDF5]          | VS2026, MSVC v145                   |
    | [NetCDF]            | VS2026, MSVC v145                   |
    | [pNetCDF]           | VS2026, MSVC v145                   |
    | [GDAL]              | VS2026, MSVC v145                   |
    | [GMT]               | VS2026, MSVC v145                   |
    | [form-dev/form]     | VS2026, MSVC v145, MSMPI            |
    | etc.

    <!-- CI: Env build test, Recursive build Test -->
    <!-- ... -->

- Repository Sync Status

  There are other hosting platforms sync with GitHub as mirror site by CI action.

  GitHub repo is major develop upstream, other mirror site will sync every next day at 04:00 UTC+8.

  | Repo Server | type | status | link |
  | :--         | :--  | :--  | :-- |
  | GitHub      | main | upstream | [https://github.com/TaiXeflar/wemi](https://github.com/TaiXeflar/wemi) |
  | GitLab      | mirror | [![gitlab_badge][gitlab_action_badge]][gitlab_action] | [https://gitlab.com/TaiXeflar/wemi](https://gitlab.com/TaiXeflar/wemi) |
  | Gitea       | mirror | [![gitea_badge][gitea_action_badge]][gitea_action] | [https://gitea.com/TaiXeflar/wemi](https://gitea.com/TaiXeflar/wemi) |
  | Gitee       | mirror | [![gitee_badge][gitee_action_badge]][gitee_action] | [https://gitee.com/TaiXeflar/wemi](https://gitee.com/TaiXeflar/wemi) |
  | GitCode     | mirror | [![gitcode_badge][gitcode_action_badge]][gitcode_action] | [https://gitcode.com/TaiXeflar/wemi](https://gitcode.com/TaiXeflar/wemi) |

  [gitlab_action_badge]:  https://github.com/TaiXeflar/wemi/actions/workflows/sync-to-gitlab.yaml/badge.svg?branch=master
  [gitlab_action]:        https://github.com/TaiXeflar/wemi/actions/workflows/sync-to-gitlab.yaml
  [gitee_action_badge]:   https://github.com/TaiXeflar/wemi/actions/workflows/sync-to-gitee.yaml/badge.svg?branch=master
  [gitee_action]:         https://github.com/TaiXeflar/wemi/actions/workflows/sync-to-gitee.yaml
  [gitea_action_badge]:   https://github.com/TaiXeflar/wemi/actions/workflows/sync-to-gitea.yaml/badge.svg?branch=master
  [gitea_action]:         https://github.com/TaiXeflar/wemi/actions/workflows/sync-to-gitea.yaml
  [gitcode_action_badge]: https://github.com/TaiXeflar/wemi/actions/workflows/sync-to-gitcode.yaml/badge.svg?branch=master
  [gitcode_action]:       https://github.com/TaiXeflar/wemi/actions/workflows/sync-to-gitcode.yaml


## Requirements
 - Python environment, recommends with [Astral UV][] venv.
 - [Everything][]
 - [Everything CLI][]
 - [gsudo][] (optional)

    gsudo is a optional compoment, if you need elevate privileges.

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

 - Locale

    WEMI strongly not recommend set non Latin characters, full widith characters, half/full width spaces, dots, laft/right slashes as your user name, especially on these regions:

     - Traditional Chinese (ZH-TW, Big5): Complexed Chinese word character, common used by R.O.C.(Taiwan), Hong Kong, Macao.
     - Simplfied Chinese (ZH-CN, GBK): Simplfied Chinese word character, common used by Mainland China.
     - Japanese (JA, Shift-JIS): Japanese uses Kanji, Hiragana(平仮名) and Katakana(片仮名).
     - Korean (KR).

    This is not WEMI cases because most development toolchains are prefer English environment, include full english charcters path. Instead, PC users should keep their names to English based names, dashes and underscores to avoid any cross-platform program have not complete support to it. For example:
     - Avoid names like `C:/Users/三月七`, `C:/Users/琪亞娜　卡斯蘭娜`.
     - Recommend user names: `C:/Users/SilverWolf999`, `C:/Users/Miku39`, `C:/Users/OMNI_1206` etc.

 - Code formatter

    The code base is under Inf Dev status with possiable large changes there, the code format is not at the priority (not I'm f\*\*king lazy), with pre-commit feature only set SDPX License identifier only.

    In future plan will add black or ruff formater.

 - Cygwin/MSYS2

    WEMI requires Python Standard Module `win32` which is not available in Cygwin/MSYS2 based posix Python. And most
    of wemi supported SDKs, their ecosystem are MSVC based toolchains, with Microsoft or Intel/AMD/NVIDIA and other 3rd
    party provided environment setup support.

     The solution is:
      1. Run a Cygwin/MSYS2 bash and [Envmodules/modules][Environment Modules] build process as Linux/macOS does.
      2. Run run another `pwsh` process to run `wemi`, set install prefix to Cygwin/MSYS2 dir's modulefiles.
      3. Check installed modulefiles, if they need `dos2unix` to set `CRLF -> LF`.

    There's a future CI plan to play this environment.

 - GCC, GCC based LLVM

    GCC compilers with it's releases may be different, with target triple X MSVCRT/UCRT matrix, and also different SDKs will contain their gcc redistribution.

    This may need time to select what kind of GCC compilers and related SDKs to support. But wemi will have future plan to
    support them.


 - AMD ROCm

    1. HIP SDK will not be planned to CI test due it is not avail at winget.
    2. ROCm/TheRock will be planed to future case test, with a recursive build test.

 - Windows on ARM64

    I'm interested in this, such as Snapdragon Elite X platform (Qualcomm) and GB10 (NVIDIA + MediaTek). But I can only keep these platforms on watching list:

     - No experience on playing MSVC on ARM64/ARM64EC. But I'll try it.
     - Qualcomm's SDK is hard to get with is QPM and licenses problems.
     - GB10 chip has no existed MediaTek optimized compilers/SDKs and NVIDIA CUDA SDKs.

        \[Update\]: NVIDIA has released CUDA 13.4 developer version release with cross compilation support.

        CUDA SDKs will follow `$env(VSCMD_ARG_TGT_ARCH)` env variable. So I think this is effectness to
        NVIDIA CUDA that need refactoring, but NVIDIA CUDA-X is in plan.


 - CI test coverage limitation on SDKs

    This is the highlight and become a core to WEMI to prove that WEMI can handle environment setup
    coverage is enough to handle large compile/build tasks as Linux HPC systems. But with some limits
    here, to prevent or wait for future fix/add CI build test cases.

    1. Some SDKs are not avail with package managers like `winget`, `choco`:
        - NVIDIA CUDA-X Libraries
        - AMD HIP SDK
        - Qualcomm Snapdragon LLVM compiler
        - etc.

    2. Some SDKs is on my interested list but have no experience before:
        - Cangjie
        - Zig
        - Rust
        - Swift

    3. Some SDKs are meant to be examined to be built from source will take time:
        - ROCm/TheRock
        - Exaloop/codon
        - ROOT-Project/Cling
        - Swift
        - torch/libtorch
        - XGBoost
        - NetCDF/pNetCDF
        - GDAL
        - HDF4/HDF5
        - etc.

    4. Some SDKs will require Licenses to install:
        - MATLAB
        - Borland C++
        - Embarcadero C++

    5. Experimential SDKs:
        - MiHoYo/Hoyoverse GunsGirlsZ, GGZ/BH2
        - MiHoYo/Hoyoverse Honkai Impact 3
        - MiHoYo/Hoyoverse Genshin Impact
        - MiHoYo/Hoyoverse Honkai: Star Rail
        - MiHoYo/Hoyoverse Zenless Zone Zero, ZZZ
        - MiHoYo/Hoyoverse Nexus Anima
        - MiHoYo/Hoyoverse Varsapura
        - MiHoYo/Hoyoverse PetitPlanet

### Docs Language Localization
Currently main language will be written in English (US). With after updates, there will several languages updates to docunemtation and wemi program.

<!--    Websites    -->

[Astral UV]:                            https://docs.astral.sh/uv/getting-started/installation/#__tabbed_1_2

[Everything]:                           https://www.voidtools.com/downloads/

[Everything CLI]:                       https://github.com/voidtools/ES

[gsudo]:                                https://github.com/gerardog/gsudo

[Environment Modules]:                  https://github.com/envmodules/modules

### The idea/inventing monent
This project is based on my collage school lifetime thoughts.

The develop environment is have Youtube Music with listening [七見斷滅智論抄][Il Dottore] [Prajnaparamitopadesa to Quell Seven Calamities][Il Dottore].

<!-- links -->
[Il Dottore]:   https://youtu.be/jBfLW28avYU
