
# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$RepositoryRoot,

    [string]$PythonVersion = "3.13.2"
)

$ErrorActionPreference = "Stop"

Set-Location $RepositoryRoot

New-Item -ItemType Directory -Force ".deps" | Out-Null

uv venv ".venv" --python $PythonVersion --seed

$python = Join-Path $RepositoryRoot ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $python -PathType Leaf)) {
    throw "Virtual environment Python was not created: $python"
}

& $python --version

if ($LASTEXITCODE -ne 0) {
    throw "Virtual environment Python failed."
}
