# SPDX-License-Identifier: MIT

[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

Write-Host "Installing NVIDIA CUDA Toolkit 12.6..."

winget install `
    --id Nvidia.CUDA `
    --exact `
    -v "12.6" `
    --source winget `
    --silent `
    --disable-interactivity `
    --accept-package-agreements `
    --accept-source-agreements

if ($LASTEXITCODE -ne 0) {
    throw "Failed to install NVIDIA CUDA Toolkit. Exit code: $LASTEXITCODE"
}
