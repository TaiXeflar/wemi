
; SPDX-License-Identifier: MIT
; Copyright (c) 2026-${year} WEMI Contributors
; This software is released under the MIT License.
; https://opensource.org/licenses/MIT


option casemap:none

extern ExitProcess:proc

.code

main proc
    sub rsp, 40
    xor ecx, ecx
    call ExitProcess
main endp

end
