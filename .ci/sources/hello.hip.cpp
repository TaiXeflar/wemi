
/*
    SPDX-License-Identifier: MIT
    Copyright (c) 2026-${year} WEMI Contributors
    This software is released under the MIT License.
    https://opensource.org/licenses/MIT
*/

#include <hip/hip_runtime.h>

#include <cstdio>

__global__ void hello_kernel()
{
}

int main()
{
    std::puts("Hello from the HIP host compiler.");
    return 0;
}
