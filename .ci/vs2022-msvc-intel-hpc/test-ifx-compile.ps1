# SPDX-License-Identifier: MIT

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$InstallPrefix,

    [string]$VsModule = "vs/2022/Enterprise",

    [string]$MsvcModule = "msvc/v143_14.44.35207/x64",

    [string]$UcrtModule = "ucrt/10.0.26100.0",

    [string]$IntelCompilerModule = "intel/compiler/2025.1"
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

envmodule load intel/oneapi

Write-Host "Loading Intel compiler profile: $IntelCompilerModule"
envmodule load $IntelCompilerModule

Write-Host "Loaded modules:"
envmodule list

Write-Host "Compiler commands:"
Get-Command cl.exe
Get-Command link.exe
Get-Command ifx.exe

ifx.exe --version

$workDir = Join-Path $PWD "ifx-compile-smoke-work"
New-Item -ItemType Directory -Force $workDir | Out-Null
Set-Location $workDir

@'
program hello
    print *, "hello from ifx"
end program hello
'@ | Set-Content -LiteralPath ".\hello_ifx.f90" -Encoding ASCII

ifx.exe .\hello_ifx.f90 /nologo /exe:hello_ifx.exe

if ($LASTEXITCODE -ne 0) {
    throw "ifx.exe failed. Exit code: $LASTEXITCODE"
}

if (-not (Test-Path -LiteralPath ".\hello_ifx.exe" -PathType Leaf)) {
    throw "hello_ifx.exe was not created."
}

.\hello_ifx.exe

if ($LASTEXITCODE -ne 0) {
    throw "hello_ifx.exe failed. Exit code: $LASTEXITCODE"
}
