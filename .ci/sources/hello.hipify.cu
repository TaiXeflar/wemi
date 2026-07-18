
/*
    SPDX-License-Identifier: MIT
    Copyright (c) 2026-${year} WEMI Contributors
    This software is released under the MIT License.
    https://opensource.org/licenses/MIT
*/

#include <cuda_runtime.h>

__global__ void set_value(int* output)
{
    output[0] = 42;
}

int main()
{
    int* device_value = nullptr;

    cudaError_t result =
        cudaMalloc(reinterpret_cast<void**>(&device_value), sizeof(int));

    if (result != cudaSuccess) {
        return 1;
    }

    set_value<<<1, 1>>>(device_value);

    result = cudaDeviceSynchronize();

    cudaFree(device_value);

    return result == cudaSuccess ? 0 : 1;
}
