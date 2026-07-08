# SPDX-License-Identifier: MIT
# Copyright (c) 2026 WEMI Contributors

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$InstallPrefix,

    [Parameter(Mandatory)]
    [string]$VsModule,

    [Parameter(Mandatory)]
    [string]$MsvcModule,

    [Parameter(Mandatory)]
    [string]$UcrtModule
)

$ErrorActionPreference = "Stop"

$installRoot = (Resolve-Path -LiteralPath $InstallPrefix).Path
$tclsh = Get-Command tclsh.exe -ErrorAction Stop
$tclBin = Split-Path -Path $tclsh.Source -Parent

$env:Path = "$installRoot\bin;$tclBin;$env:Path"

Remove-Item Env:MODULES_CMD -ErrorAction SilentlyContinue
Remove-Item Env:MODULESHOME -ErrorAction SilentlyContinue
Remove-Item Env:MODULEPATH -ErrorAction SilentlyContinue
Remove-Item Env:LOADEDMODULES -ErrorAction SilentlyContinue

. "$installRoot\init\pwsh.ps1"

Write-Host "Available modulefiles:"
envmodule avail

Write-Host "Loading Visual Studio profile: $VsModule"
envmodule load $VsModule

# Check VS/2022/Enterprise is working, and unlock MSVC
Write-Host "Available modulefiles:"
envmodule avail

Write-Host "Loading MSVC compiler profile: $MsvcModule"
envmodule load $MsvcModule


# Check msvc/v14X/<arch> is working, and ucrt
Write-Host "Available modulefiles:"
envmodule avail

Write-Host "Loading UCRT profile: $UcrtModule"
envmodule load $UcrtModule

Write-Host "Loaded modules:"
envmodule list


$workDir = Join-Path $PWD "msvc-compile-smoke-work"
New-Item -ItemType Directory -Force $workDir | Out-Null
Set-Location $workDir

@'
#include <stdio.h>
#include <windows.h>

int main(void) {
    puts("hello from msvc");
    return GetVersion() == 0 ? 1 : 0;
}
'@ | Set-Content -LiteralPath ".\hello.c" -Encoding ASCII

cl.exe .\hello.c /nologo

if ($LASTEXITCODE -ne 0) {
    throw "cl.exe failed. Exit code: $LASTEXITCODE"
}

if (-not (Test-Path -LiteralPath ".\hello.exe" -PathType Leaf)) {
    throw "hello.exe was not created."
}

.\hello.exe

if ($LASTEXITCODE -ne 0) {
    throw "hello.exe failed. Exit code: $LASTEXITCODE"
}
