
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
$InstallPrefix = Join-Path $env:RUNNER_TEMP "wemi-all-sdk-observation"

Set-Location $RepositoryRoot

Import-Module `
    (Join-Path $RepositoryRoot ".ci\common\prepare-uv-venv.psm1") `
    -Force

Import-Module `
    (Join-Path $RepositoryRoot ".ci\common\show-runner.psm1") `
    -Force

Import-Module `
    (Join-Path $RepositoryRoot ".ci\common\winget-functions.psm1") `
    -Force

show-runner

Test-Winget
Install-Everything
Install-ES
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

Write-Host "Running WEMI configure with all SDK scanners."
Write-Host "Install prefix: $InstallPrefix"

& $Python `
    (Join-Path $RepositoryRoot "wemi.py") `
    configure `
    --prefix $InstallPrefix

if ($LASTEXITCODE -ne 0) {
    throw "WEMI all-SDK configure failed."
}

$CacheFile = Join-Path $RepositoryRoot "build\cache.json"

if (-not (Test-Path -LiteralPath $CacheFile -PathType Leaf)) {
    throw "WEMI configure completed without creating build\cache.json."
}

Write-Host "All SDK configure observation completed."
Write-Host "Generated cache: $CacheFile"
