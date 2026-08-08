

// # SPDX-License-Identifier: MIT
// # Copyright (c) 2026-${year} WEMI Contributors
// # This software is released under the MIT License.
// # https://opensource.org/licenses/MIT

#ifndef WEMI_SMOKE_LIBRARY_H
#define WEMI_SMOKE_LIBRARY_H

#if defined(_WIN32) && defined(WEMI_BUILD_DLL)
#  define WEMI_API __declspec(dllexport)
#elif defined(_WIN32) && defined(WEMI_USE_DLL)
#  define WEMI_API __declspec(dllimport)
#else
#  define WEMI_API
#endif

#ifdef __cplusplus
extern "C" {
#endif

WEMI_API int wemi_add(int a, int b);

#ifdef __cplusplus
}
#endif

#endif
