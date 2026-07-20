# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$RepositoryRoot,

    [Parameter(Mandatory)]
    [string]$PythonVersion
)

$ErrorActionPreference = "Stop"

$RepositoryRoot = (Resolve-Path -LiteralPath $RepositoryRoot).Path
$InstallPrefix = Join-Path $env:RUNNER_TEMP "wemi-python-$PythonVersion"

Set-Location $RepositoryRoot

Import-Module `
    (Join-Path $RepositoryRoot ".ci\common\prepare-uv-venv.psm1") `
    -Force

Import-Module `
    (Join-Path $RepositoryRoot ".ci\common\winget-functions.psm1") `
    -Force

Import-Module `
    (Join-Path $RepositoryRoot ".ci\common\modules-init.psm1") `
    -Force

Write-Host "Python test version: $PythonVersion"
Write-Host "WEMI install prefix: $InstallPrefix"

Test-Winget

Install-Everything
Install-TclTk

set-uvpython `
    -RepositoryRoot $RepositoryRoot `
    -PythonVersion $PythonVersion

$Python = Join-Path $RepositoryRoot ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $Python -PathType Leaf)) {
    throw "Virtual environment Python was not found: $Python"
}

Remove-Item `
    -LiteralPath (Join-Path $RepositoryRoot "build") `
    -Recurse `
    -Force `
    -ErrorAction SilentlyContinue

Remove-Item `
    -LiteralPath $InstallPrefix `
    -Recurse `
    -Force `
    -ErrorAction SilentlyContinue

& $Python `
    (Join-Path $RepositoryRoot "wemi.py") `
    configure `
    --modules-only `
    --aio `
    --prefix $InstallPrefix

if ($LASTEXITCODE -ne 0) {
    throw "WEMI AIO test failed with Python $PythonVersion."
}

if (-not (Test-Path -LiteralPath $InstallPrefix -PathType Container)) {
    throw "WEMI install prefix was not created: $InstallPrefix"
}

$InitScript = Join-Path $InstallPrefix "init\pwsh.ps1"

if (-not (Test-Path -LiteralPath $InitScript -PathType Leaf)) {
    throw "Environment Modules PowerShell initialization script was not installed: $InitScript"
}

init-modules -InstallPrefix $InstallPrefix

Get-Command module -ErrorAction Stop | Out-Null

Write-Host "Python $PythonVersion WEMI modules-only AIO test passed."
