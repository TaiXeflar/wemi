# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$InstallPrefix,

    [string]$VsModule = "vs/2026/Enterprise",

    [string]$MsvcModule = "msvc/v145_14.51.36231/x64",

    [string]$UcrtModule = "ucrt/10.0.26100.0"
)

$ErrorActionPreference = "Stop"

. ".\.ci\common\modules-init.ps1" `
    -InstallPrefix $InstallPrefix

Write-Host "Available modulefiles:"
envmodule avail

Write-Host "Before loading toolchain modules:"

$clBefore = Get-Command cl.exe -ErrorAction SilentlyContinue
if ($clBefore) {
    Write-Warning "cl.exe was already visible before module load: $($clBefore.Source)"
}
else {
    Write-Host "cl.exe is not visible before module load, as expected."
}

Write-Host "Loading Visual Studio profile: $VsModule"
envmodule load $VsModule

Write-Host "Loading MSVC profile: $MsvcModule"
envmodule load $MsvcModule

Write-Host "Loading UCRT profile: $UcrtModule"
envmodule load $UcrtModule

Write-Host "Loaded modules:"
envmodule list

Write-Host "Compiler commands after module load:"

$cl = Get-Command cl.exe -ErrorAction Stop
$link = Get-Command link.exe -ErrorAction Stop
$rc = Get-Command rc.exe -ErrorAction Stop
$mt = Get-Command mt.exe -ErrorAction Stop

$cl
$link
$rc
$mt

# 避免誤用 Git for Windows 的 link.exe。
if ($link.Source -match "\\Git\\usr\\bin\\link\.exe$") {
    throw "Resolved the wrong link.exe: $($link.Source)"
}

cl.exe /Bv

if ($LASTEXITCODE -ne 0) {
    throw "cl.exe /Bv failed. Exit code: $LASTEXITCODE"
}

$workDir = Join-Path $PWD "vs2026-msvc-compile-smoke-work"

if (Test-Path -LiteralPath $workDir) {
    Remove-Item -LiteralPath $workDir -Recurse -Force
}

New-Item -ItemType Directory -Force $workDir | Out-Null

Push-Location $workDir

try {
    @'
#include <stdio.h>
#include <windows.h>

int main(void)
{
    printf("hello from VS2026 MSVC v145\n");
    printf("Windows SDK is available: %lu\n", (unsigned long)GetVersion());
    return 0;
}
'@ | Set-Content `
        -LiteralPath ".\hello_vs2026.c" `
        -Encoding ASCII

    cl.exe `
        .\hello_vs2026.c `
        /nologo `
        /W4 `
        /Fe:hello_vs2026.exe

    if ($LASTEXITCODE -ne 0) {
        throw "cl.exe failed. Exit code: $LASTEXITCODE"
    }

    if (-not (
        Test-Path `
            -LiteralPath ".\hello_vs2026.exe" `
            -PathType Leaf
    )) {
        throw "hello_vs2026.exe was not created."
    }

    .\hello_vs2026.exe

    if ($LASTEXITCODE -ne 0) {
        throw "hello_vs2026.exe failed. Exit code: $LASTEXITCODE"
    }
}
finally {
    Pop-Location
}
