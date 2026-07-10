# SPDX-License-Identifier: MIT

[CmdletBinding()]
param(
    [string]$ExpectedCudaVersion = "12.6"
)

$ErrorActionPreference = "Stop"

Write-Host "Searching CUDA installations..."

$cudaRoots = @()

$envCuda = Get-ChildItem Env:CUDA_PATH* -ErrorAction SilentlyContinue
foreach ($item in $envCuda) {
    if (Test-Path -LiteralPath $item.Value) {
        $cudaRoots += $item.Value
    }
}

$defaultRoot = "C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA"
if (Test-Path -LiteralPath $defaultRoot) {
    Get-ChildItem -LiteralPath $defaultRoot -Directory |
        ForEach-Object { $cudaRoots += $_.FullName }
}

$cudaRoots = $cudaRoots | Sort-Object -Unique

if (-not $cudaRoots) {
    throw "No CUDA installation root was found."
}

foreach ($root in $cudaRoots) {
    Write-Host "CUDA root: $root"

    $nvcc = Join-Path $root "bin\nvcc.exe"
    $versionJson = Join-Path $root "version.json"

    if (Test-Path -LiteralPath $nvcc) {
        & $nvcc --version
    }

    if (Test-Path -LiteralPath $versionJson) {
        Get-Content -LiteralPath $versionJson -TotalCount 20
    }
}

$expectedRoot = Join-Path $defaultRoot "v$ExpectedCudaVersion"
$expectedNvcc = Join-Path $expectedRoot "bin\nvcc.exe"

if (-not (Test-Path -LiteralPath $expectedNvcc -PathType Leaf)) {
    throw "Expected CUDA $ExpectedCudaVersion nvcc.exe was not found: $expectedNvcc"
}

Write-Host "Found expected CUDA $ExpectedCudaVersion nvcc.exe:"
Write-Host $expectedNvcc
& $expectedNvcc --version
