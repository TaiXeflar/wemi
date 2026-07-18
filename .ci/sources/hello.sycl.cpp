
/*
    SPDX-License-Identifier: MIT
    Copyright (c) 2026-${year} WEMI Contributors
    This software is released under the MIT License.
    https://opensource.org/licenses/MIT
*/

#include <sycl/sycl.hpp>

#include <iostream>

int main()
{
    sycl::queue queue;

    int value = 0;

    {
        sycl::buffer<int, 1> buffer(&value, sycl::range<1>(1));

        queue.submit([&](sycl::handler& handler) {
            auto output = buffer.get_access<sycl::access::mode::write>(handler);

            handler.single_task([=]() {
                output[0] = 42;
            });
        });
    }

    std::cout << "Hello from SYCL: " << value << '\n';

    return value == 42 ? 0 : 1;
}
