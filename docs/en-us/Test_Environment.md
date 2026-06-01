

WEMI is developed on my PC with these working configuration.

# Hardware Device

- ### Hatsune Miku: Powered by AMD/NVIDIA/ROG
    ```
    CPU:    AMD Ryzen 9 9950X 16C/32T 80MB L3 @4.3GHz
    GPU0:   ROG Astral RTX 5080 Hatsune Miku Edition (NVIDIA GeForce RTX 5080)
    MB:     ROG Strix X870-H Gaming WiFi7 S Hatsune Miku Edition
    DRAM:   Asgard 6400MT/CL34 48GBx2 UDIMM DDR5 set ROG Strix Fubuki Edition
    SSD0:   Micron Crucial T500 2TB TLC PCIe 4.0 SSD (2GB DDR4 Cache)
    SSD1:   WD Blue SN5000 2TB PCIe 4.0 SSD (DRAM Less)
    PSU:    ROG THOR III 1200W Hatsune Miku Edition
    AIO:    ROG RYUO IV SLC Hatsune Miku Edition
    CASE:   ROG Helios II Hatsune Miku Edition
    DISP:   ROG Strix XG27ACMEG-G 27" 2K 260Hz*/0.3ms Fast IPS Hatsune Miku Edition
    MICE:   ASUS TX Gaming Mouse Mini Hatsune Miku Edition
    KB:     ROG Falchion RX Low Profile

    Hatsune Miku: Specified ROG x Miku [Mainland China Version] ROG SE7EN x Hatsune Miku
    ```

- ### ROG Zephyrus S15 (2020)
    ```
    CPU:    Intel Core i7-10875H 8C/16T @2.3GHz with Intel UHD Graphics
    GPU:    NVIDIA GeForce RTX 2080 Super with Max-Q design @8GB GDDR6
    DRAM:   32GB 3200MHz DDR4 SO-DIMM
    SSD0:   Samsung 970 EVO Plus 2TB TLC NVMe PCIe SSD
    SSD1:   Samsung 970 EVO Plus 2TB TLC NVMe PCIe SSD
    ```

# Software
Tested SDKs:

| SDK Name              | SDK version   | build type    |
| :----:                | :----         | :----         |
| Windows               | 25H2          | 24H2 install, patch update |
| Windows Terminal      | 1.24.11321.0  | System contain
|
| Python 3              | 3.14.0        | PSF Installer |
| Python 3              | 3.14.2        | Astral UV install
| Astral uv             | 0.11.2        | pwsh -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
| PowerShell 7          | 7.5.2         | GitHub release Installer
| Everything            | 1.4.1.1032    | VoidTools website release Installer
| Everything CLI        | 1.1.0.36      | zip decompress install
| VSCode                | latest        | 
| 
| AMD HIP SDK           | 7.1           | Installer     |
| ROCm/TheRock          | 7.12          | -DCMAKE_BUILD_TYPE=Release |
|                       |               | -THEROCK_DIST_AMDGPU_TARGETS='gfx1100;gfx1101;gfx1102;gfx1151;gfx1201;gfx1202'
| Intel oneAPI          | 2022.2        | Installer
|                       | 2023.0        | Installer
|                       | 2025.1        | Installer
|                       | 2025.3        | Installer
| NVIDIA CUDA Toolkit   | 12.6          | Installer
|                       | 13.0          | Installer
|                       | 13.2          | Installer
| NVIDIA cuDNN SDK      | 9.13.0 (cuda 12.6) | Installer
|                       | 9.9.0 (cuda 12.9, cuda11.8) | Installer
| NVIDIA cuDNN SDK      | 9.20.0 (cuda 13.2, cuda12.9) | Installer
| NVIDIA cuDSS SDK      | 0.6.0 (cuda12) | zip decompress install
|                       | 0.7.1 (cuda12, cuda13) | Installer 
| NVIDIA cuTENSOR SDK   | 2.3.1 (cuda12) | zip compress
|                       | 2.5.0 (cuda12, cuda13) | Installer 
|                       | 2.6.0 (cuda12, cuda13) | Installer
| NVIDIA cuSPARSELt SDK | 0.8.1 (cuda12) | zip decompress install
| NVIDIA cutlass        | 4.4.1         | -DCMAKE_BUILD_TYPE=Release -DCMAKE_OBJECT_PATH_MAX=320
|                       |               | -DCUTLASS_NVCC_ARCHS="75" -DCUTLASS_ENABLE_TESTS=OFF
|                       |               | -DCUTLASS_ENABLE_EXAMPLES=OFF -DCUTLASS_ENABLE_LIBRARY=ON 
|                       |               | -DCUTLASS_ENABLE_TOOLS=ON -DCUTLASS_ENABLE_PROFILER=ON
| VS2026 BuildTools     | --            | online install
| MSVC v145             | latest        | Installer, ATL Library, target x86/x64, ARM64/ARM64EC
| MSVC v143             | latest        | Installer, ATL Library, target x86/x64, ARM64, ARM
| MSVC v142             | latest        | Installer, ATL Library, target x86/x64, ARM64, ARM
| MSVC v141             | latest        | Installer, ATL Library, target x86/x64, ARM64, ARM
| LLVM/Clang            | latest (21.1.8)| Installer
| VS2022 BuildTools     | --            | online install
| MSVC v143             | latest        | Installer, ATL Library, target x86/x64, ARM64, ARM
| MSVC v142             | latest        | Installer, ATL Library, target x86/x64, ARM64, ARM
| MSVC v141             | latest        | Installer, ATL Library, target x86/x64, ARM64, ARM
| CMake support         | latest        | Installer
| Windows SDK           | 10.0.17763.0  | Installer
|                       | 10.0.19041.0  | Installer
|                       | 10.0.20348.0  | Installer
|                       | 10.0.22621.0  | Installer
|                       | 10.0.28000.0  | Installer
| MATLAB                | R2025a        | Installer
| Cangjie Lang          | 1.0.3         | zip decompress install
|                       | 1.0.5         | zip decompress install
|                       | 1.1.0         | zip decompress install
| 


## Project Develop Environment
 - ### YT Music
 - 七見斷滅智論抄 Prajnaparamitopadesa to Quell Seven Calamities (HoYo-Mix, 2026)
 - Upgrade (Slizzy McGuire, 2025)
 - edamame (bbno$ & Rich Brian, 2021)
 - There's nothing holding me back (Shawn mendes, 2016)