# SPDX-License-Identifier: MIT

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$InstallPrefix,

    [string]$VsModule = "vs/2022/Enterprise",

    [string]$MsvcModule = "msvc/v143_14.44.35207/x64",

    [string]$UcrtModule = "ucrt/10.0.26100.0",

    [string]$CudaModule = "nvidia/cuda/12.6"
)

$ErrorActionPreference = "Stop"

. ".\.ci\common\modules-init.ps1" `
    -InstallPrefix $InstallPrefix

Write-Host "Available modulefiles:"
envmodule avail

Write-Host "Loading Visual Studio profile: $VsModule"
envmodule load $VsModule

Write-Host "Loading MSVC profile: $MsvcModule"
envmodule load $MsvcModule

Write-Host "Loading UCRT profile: $UcrtModule"
envmodule load $UcrtModule

Write-Host "Loading CUDA profile: $CudaModule"
envmodule load $CudaModule

Write-Host "Loaded modules:"
envmodule list

Write-Host "Compiler commands:"
Get-Command cl.exe
Get-Command link.exe
Get-Command nvcc.exe

nvcc.exe --version

$workDir = Join-Path $PWD "cuda-host-compile-smoke-work"
New-Item -ItemType Directory -Force $workDir | Out-Null
Set-Location $workDir

@'
#include <iostream>

int main() {
    std::cout << "hello from cuda host compile" << std::endl;
    return 0;
}
'@ | Set-Content -LiteralPath ".\hello_cuda_host.cu" -Encoding ASCII

nvcc.exe .\hello_cuda_host.cu -o hello_cuda_host.exe -Xcompiler="/nologo"

if ($LASTEXITCODE -ne 0) {
    throw "nvcc.exe host-only compile failed. Exit code: $LASTEXITCODE"
}

if (-not (Test-Path -LiteralPath ".\hello_cuda_host.exe" -PathType Leaf)) {
    throw "hello_cuda_host.exe was not created."
}

.\hello_cuda_host.exe

if ($LASTEXITCODE -ne 0) {
    throw "hello_cuda_host.exe failed. Exit code: $LASTEXITCODE"
}
