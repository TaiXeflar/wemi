# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$RepositoryRoot,

    [Parameter(Mandatory)]
    [string]$InstallPrefix
)

$ErrorActionPreference = "Stop"

Set-Location $RepositoryRoot

$python = Join-Path $RepositoryRoot ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $python -PathType Leaf)) {
    throw "Virtual environment Python was not found: $python"
}

& $python ".\wemi.py" configure `
    --sdk "VS20XX;UCRT" `
    --prefix $InstallPrefix `
    --aio

if ($LASTEXITCODE -ne 0) {
    throw "WEMI VS2026/MSVC AIO installation failed. Exit code: $LASTEXITCODE"
}
