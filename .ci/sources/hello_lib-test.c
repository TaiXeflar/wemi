

// # SPDX-License-Identifier: MIT
// # Copyright (c) 2026-${year} WEMI Contributors
// # This software is released under the MIT License.
// # https://opensource.org/licenses/MIT

#include <stdio.h>
#include "hello_lib.h"

int main(void)
{
    const int result = wemi_add(20, 22);

    if (result != 42) {
        fprintf(stderr, "Unexpected result: %d\n", result);
        return 1;
    }

    puts("WEMI MSVC library smoke test passed.");
    return 0;
}
