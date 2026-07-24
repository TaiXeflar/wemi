# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

[CmdletBinding()]
param(
    [Parameter()]
    [switch]$TclTk,

    [Parameter()]
    [switch]$Everything,

    [Parameter()]
    [switch]$EverythingCli
)

$ErrorActionPreference = "Stop"

$RepositoryRoot = (
    Resolve-Path -LiteralPath (
        Join-Path $PSScriptRoot "..\.."
    )
).Path

Import-Module `
    (Join-Path $RepositoryRoot ".ci\common\winget-functions.psm1") `
    -Force

Test-Winget

if ($TclTk) {
    Write-Host "Installing Tcl/Tk..."
    Install-TclTk
}

if ($Everything) {
    Write-Host "Installing Everything..."
    Install-Everything
}

if ($EverythingCli) {
    Write-Host "Installing Everything CLI..."
    Install-ES
}
