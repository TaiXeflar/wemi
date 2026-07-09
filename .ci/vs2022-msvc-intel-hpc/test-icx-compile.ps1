# SPDX-License-Identifier: MIT

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$InstallPrefix,

    [string]$VsModule = "vs/2022/Enterprise",
    [string]$MsvcModule = "msvc/v143_14.44.35207/x64",
    [string]$UcrtModule = "ucrt/10.0.26100.0",
    [string]$IntelCompilerModule = "intel/compiler/2025.1.llvm"
)

$ErrorActionPreference = "Stop"

. ".\.ci\common\modules-init.ps1" `
    -InstallPrefix $InstallPrefix

Write-Host "Available modulefiles:"
envmodule avail

Write-Host "Loading required modules..."
envmodule load $VsModule
envmodule load $MsvcModule
envmodule load $UcrtModule
envmodule load intel/oneapi
envmodule load $IntelCompilerModule

Write-Host "Loaded modules:"
envmodule list

Write-Host "Compiler commands:"
Get-Command icx.exe
Get-Command link.exe

$workDir = Join-Path $PWD "icx-compile-smoke-work"
New-Item -ItemType Directory -Force $workDir | Out-Null
Set-Location $workDir

@'
#include <stdio.h>

int main(void) {
    puts("hello from icx");
    return 0;
}
'@ | Set-Content -LiteralPath ".\hello.c" -Encoding ASCII

icx.exe .\hello.c -o .\hello.exe

if ($LASTEXITCODE -ne 0) {
    throw "icx.exe failed. Exit code: $LASTEXITCODE"
}

if (-not (Test-Path -LiteralPath ".\hello.exe" -PathType Leaf)) {
    throw "hello.exe was not created."
}

.\hello.exe

if ($LASTEXITCODE -ne 0) {
    throw "hello.exe failed. Exit code: $LASTEXITCODE"
}
