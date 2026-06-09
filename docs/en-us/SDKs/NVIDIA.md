
 <!-- SPDX-License-Identifier: MIT
 Copyright (c) 2026-${year} WEMI Contributors
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT -->

# NVIDIA SDK supported list

| NVIDIA Toolkit/SDK | Versions | Status | note |
| :----: | :----: | :----: | :---- |
|||||
| NVIDIA CUDA |
| CUDA 13       | 13.0 ~ 13.X   | ✅ |
| CUDA 12       | 12.0 ~ 12.9   | ✅ |
| CUDA 11       | 11.0 ~ 11.8   | ✅ |
| CUDA 10       | <= 10.X       | ❌ | WEMI not supported CUDA Major version
|||||
| CUDA-X |
|||||
| cuDNN         | 8.8 ~ 9.X     | ✅ | CUDA deps version >= 11.0
| cuDSS         | Any           | ✅ | CUDA deps version >= 11.0
| cuTENSOR      | Any           | ✅ | CUDA deps version >= 11.0
| cuSPARSELt    | Any           | ✅ | CUDA deps version >= 11.0
| cutlass       | Any           | ✅ | No specific CUDA dll deps
| tensorRT      | Any           | ✅ | CUDA deps version >= 11.0
| cuTile        |               | ❌ | Not supported CUDA Major version teardown
| AMGX          | Any           | ✅ | CUDA deps version >= 11.0
| NVTX          | ?             | ❌ | Pending test
| cuCollect     | ?             | ❌ | Pending test
| stdexec       | ?             | ❌ | Pending test
| cuda-gdb      | ?             | ❌ | Wait for NVIDIA release cuda-gdb binary package (MinGW-w64 target)
| MatX          | ?             | ❌ | Pending test
|||||
| NVIDIA HPC SDK |
|||||
| NVIDIA HPC SDK | ?             | ❌ | No available Windows x64 Release |
| PGI Compilers  | ?             | ❌ | No available Windows x64 Release |



## NVIDIA CUDA Toolkit

The possiable NVIDIA CUDA Toolkit configuration support range will be around over CUDA 11. CUDA 10 and lower version is not guranteed to support.

 - CUDA 11
 - CUDA 12
 - CUDA 13

Any CUDA-X Library(ies) will set with its required CUDA Major version dependicies, within a level-access module load progress.

![image](./_pics/nv_hierarchy.png)

WEMI will exclude 3rd-party contained GPU Toolkit, like MATLAB GPU Toolkit etc.


## NVIDIA cuDNN Library

Within CUDA Toolkit Version limitation mentioned above, most of cuDNN is supported if cuDNN's DLL `cudnn64_X.dll` is analyzable.
 - cuDNN 7
 - cuDNN 8
 - cuDNN 9

## NVIDIA cuDSS
 - cuDSS 0.X.Y

## NVIDIA cuTENSOR
 - cuTENSOR 1.X
 - cuTENSOR 2.X


## NVIDIA cuSPARSELt


## NVIDIA cuTENSOR
 - cuTENSOR 1.X
 - cuTENSOR 2.X


## NVIDIA TensorRT

## NVIDIA cutlass
NVIDIA cutlass is version analyzable and CUDA major version non-analyzable, so NVIDIA/cutlass will be a general unlock options.

When you load any `nvidia/cuda` profile, you can see unlocked `nvidia/cutlass` options.


## \_\_future\_\_
- NVIDIA cuTile (if independent build is analyzable)
- NVIDIA cuQuantum (if it is support to Windows)
- NVIDIA cuPQC (if it is support to Windows)
- NVIDIA HPC SDK (if is re-starts support to Windows x64/ARM64)
- NVIDIA CUDA Toolkit (Update patch on if Windows ARM64 release)
