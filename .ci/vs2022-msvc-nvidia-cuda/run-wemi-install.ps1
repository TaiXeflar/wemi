# SPDX-License-Identifier: MIT

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
    --sdk="VS20XX;UCRT;CUDA" `
    --prefix $InstallPrefix `
    --aio

if ($LASTEXITCODE -ne 0) {
    throw "WEMI CUDA AIO installation failed. Exit code: $LASTEXITCODE"
}
