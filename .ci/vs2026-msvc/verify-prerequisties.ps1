# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

Write-Host "PowerShell 7:"
Get-Command pwsh.exe
pwsh.exe --version

Write-Host "winget:"
Get-Command winget.exe
winget.exe --version

Write-Host "Tcl:"
Get-Command tclsh.exe
'puts [info patchlevel]' | tclsh.exe

Write-Host "Everything CLI:"
Get-Command es.exe
es.exe -version

Write-Host "Visual Studio 2026:"

$vswhere = Join-Path `
    ${env:ProgramFiles(x86)} `
    "Microsoft Visual Studio\Installer\vswhere.exe"

if (-not (Test-Path -LiteralPath $vswhere -PathType Leaf)) {
    throw "vswhere.exe was not found: $vswhere"
}

$vsPath = & $vswhere `
    -products * `
    -version "[18.0,19.0)" `
    -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 `
    -property installationPath `
    -latest

if ([string]::IsNullOrWhiteSpace($vsPath)) {
    throw "Visual Studio 2026 with C++ tools was not found."
}

Write-Host "VS2026 installation: $vsPath"

$msvcRoot = Join-Path $vsPath "VC\Tools\MSVC"
$expectedMsvc = Join-Path $msvcRoot "14.51.36231"
$expectedCl = Join-Path $expectedMsvc "bin\Hostx64\x64\cl.exe"

if (-not (Test-Path -LiteralPath $expectedCl -PathType Leaf)) {
    throw "Expected MSVC v145 compiler was not found: $expectedCl"
}

$windowsSdkRoot = "C:\Program Files (x86)\Windows Kits\10"
$windowsSdkVersion = "10.0.26100.0"

$requiredSdkPaths = @(
    "Include\$windowsSdkVersion",
    "Lib\$windowsSdkVersion",
    "bin\$windowsSdkVersion"
)

foreach ($relativePath in $requiredSdkPaths) {
    $fullPath = Join-Path $windowsSdkRoot $relativePath

    if (-not (Test-Path -LiteralPath $fullPath)) {
        throw "Required Windows SDK path was not found: $fullPath"
    }

    Write-Host "Found Windows SDK path: $fullPath"
}
