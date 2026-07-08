
# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

Write-Host "Windows:"
Get-ComputerInfo |
    Select-Object WindowsProductName, WindowsVersion, OsBuildNumber |
    Format-List

Write-Host "PowerShell:"
$PSVersionTable
pwsh.exe --version

Write-Host "uv:"
uv --version
