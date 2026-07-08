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

& $python ".\wemi.py" configure `
    --sdk="VS20XX;UCRT;ONEAPI" `
    --prefix $InstallPrefix `
    --aio

if ($LASTEXITCODE -ne 0) {
    throw "WEMI Intel oneAPI AIO installation failed. Exit code: $LASTEXITCODE"
}
