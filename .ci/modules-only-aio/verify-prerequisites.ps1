# SPDX-License-Identifier: MIT
# Copyright (c) 2026 WEMI Contributors

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
