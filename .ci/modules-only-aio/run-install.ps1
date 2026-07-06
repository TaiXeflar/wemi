# SPDX-License-Identifier: MIT
# Copyright (c) 2026 WEMI Contributors

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
    -DMODULES_ONLY `
    --prefix $InstallPrefix `
    --aio

if ($LASTEXITCODE -ne 0) {
    throw "WEMI Modules-only AIO installation failed. Exit code: $LASTEXITCODE"
}
