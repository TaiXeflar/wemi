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
module avail

Write-Host "Loading Visual Studio profile: $VsModule"
module load $VsModule

Write-Host "Loading MSVC compiler profile: $MsvcModule"
module load $MsvcModule

Write-Host "Loading UCRT profile: $UcrtModule"
module load $UcrtModule

Write-Host "Loaded modules:"
module list


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
