# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

from .add_Modules import AddModules

from .find_AMD_HIP import FindHIPSDK
from .find_AMD_ROCm import FindTheRock
from .find_NVIDIA_CUDA import FindCUDA
from .find_NVIDIA_CUDAX import (
    FindCUDAX,
)  # FindCUDNN, FindCUDSS, FindCUTENSOR, FindCUSPARSTLT, Findcutile, Findcutlass, FindTensorRT #, FindcuQuantum
from .find_INTEL_ONEAPI import FindOneAPI
from .find_MSMPI_MPI import FindMSMPI
from .find_MSMPI_SDK import FindMSMPISDK
from .find_VS20XX import FindVS20XX
from .find_UCRT import FindUCRT
from .find_Cangjie import FindCangjie
from .find_Strawberry_Perl import FindStrawberryPerl
from .find_GMT import FindGMT

from .find_MATLAB import FindMATLAB

from .find_MiHoYo import FindMiHoYo

__all__ = [
    'AddModules',
    "FindHIPSDK",
    "FindTheRock",
    "FindCUDA",
    "FindCUDAX",
    "FindVS20XX",
    "FindUCRT",
    "FindCangjie",
    "FindMATLAB",
    "FindGMT",
    "FindMSMPI",
    "FindMSMPISDK",
    "FindStrawberryPerl",
    "FindOneAPI",
    "FindMiHoYo",
]
