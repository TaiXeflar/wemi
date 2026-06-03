

AMD SDKs is supposed to support AMD developer website released HIP SDK and ROCm/TheRock project.

![image](./_pics/amd_hierarchy.png)

## AMD HIP SDK

AMD HIP SDK contains pre-built HIP/ROCm library and hip compiler.

WEMI follows environment variable `HIP_PATH*` to find possiable HIP SDK installation.

- HIP 5.X
- HIP 6.X
- HIP 7.X

## ROCm/TheRock

ROCm/TheRock is a lightweight "The HIP Environment and ROCm Kit" build system for Windows/Linux x64/gfx target. 

WEMI finds the installation configuration on `hipcc.exe` that different then AMD HIP SDK.

- ROCm/TheRock 6.5
- ROCm/TheRock 7.X
- ROCm/TheRock 7.11
- ROCm/TheRock 7.12
- ROCm/TheRock 7.13
- ROCm/TheRock 7.X

## \_\_future\_\_
 - Integrate AMD HIP profile `amd/hip/X.Y` and ROCm/TheRock profile `ROCm/TheRock/X.Y` with major AMD profile and level-access.
 - AOCC compilers (If AOCC is available on Windows x64)