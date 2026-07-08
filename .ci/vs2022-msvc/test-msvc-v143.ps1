# SPDX-License-Identifier: MIT

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$InstallPrefix,
)

$ErrorActionPreference = "Stop"

$installRoot = (Resolve-Path -LiteralPath $InstallPrefix).Path

# Ensure WEMI-installed Modules is used first.
$env:Path = "$installRoot\bin;$env:Path"

# Avoid polluted module environment.
Remove-Item Env:MODULES_CMD -ErrorAction SilentlyContinue
Remove-Item Env:MODULESHOME -ErrorAction SilentlyContinue
Remove-Item Env:MODULEPATH -ErrorAction SilentlyContinue
Remove-Item Env:LOADEDMODULES -ErrorAction SilentlyContinue

Write-Host "Initializing Environment Modules from: $installRoot"
. "$installRoot\init\pwsh.ps1"

Write-Host "Available modules:"
envmodule avail

envmodule load vs/2022/Enterprise
envmodule load msvc/v143_14.44.35207/x64
envmodule load ucrt/10.0.22621.0


Write-Host "Loaded modules:"
envmodule list

Write-Host "Checking compiler commands..."
Get-Command cl.exe
Get-Command link.exe

Write-Host "MSVC version:"
cl.exe /Bv

$workDir = Join-Path $PWD "build\msvc-compile-smoke"
New-Item -ItemType Directory -Force $workDir | Out-Null
Set-Location $workDir

@'
#include <stdio.h>

int main(void) {
    puts("hello from msvc");
    return 0;
}
'@ | Set-Content -LiteralPath ".\hello.c" -Encoding ASCII

Write-Host "Compiling hello.c..."
cl.exe .\hello.c /nologo

if ($LASTEXITCODE -ne 0) {
    throw "cl.exe failed. Exit code: $LASTEXITCODE"
}

if (-not (Test-Path -LiteralPath ".\hello.exe" -PathType Leaf)) {
    throw "hello.exe was not created."
}

Write-Host "Running hello.exe..."
.\hello.exe

if ($LASTEXITCODE -ne 0) {
    throw "hello.exe failed. Exit code: $LASTEXITCODE"
}
