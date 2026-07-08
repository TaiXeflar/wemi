# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

Write-Host "PowerShell 7:"
Get-Command pwsh.exe
pwsh.exe --version

Write-Host "Tcl:"
Get-Command tclsh.exe
'puts [info patchlevel]' | tclsh.exe

Write-Host "Everything CLI:"
Get-Command es.exe
es.exe -version

Write-Host "Visual Studio installations:"
$vswhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"

if (-not (Test-Path -LiteralPath $vswhere -PathType Leaf)) {
    throw "vswhere.exe was not found."
}

& $vswhere -all -products * -format json
