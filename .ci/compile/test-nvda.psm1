# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

function test-nvda {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [ValidateSet(
            "Environment",
            "NVCC"
        )]
        [string]$Case,

        [Parameter(Mandatory)]
        [string]$InstallPrefix,

        [Parameter(Mandatory)]
        [string]$VisualStudioModule,

        [Parameter(Mandatory)]
        [string]$MsvcModule,

        [Parameter(Mandatory)]
        [string]$UcrtModule,

        [Parameter(Mandatory)]
        [string]$CudaModule
    )

    $ErrorActionPreference = "Stop"

    $sourceRoot = Join-Path $PSScriptRoot "..\sources"
    $outputRoot = Join-Path $env:RUNNER_TEMP "wemi-test-nvda-$Case"

    Remove-Item `
        -LiteralPath $outputRoot `
        -Recurse `
        -Force `
        -ErrorAction SilentlyContinue

    New-Item `
        -ItemType Directory `
        -Force `
        -Path $outputRoot |
        Out-Null

    Import-Module `
        (Join-Path $PSScriptRoot "..\common\modules-init.psm1") `
        -Force

    init-modules `
        -InstallPrefix $InstallPrefix

    # WEMI patches the installed Environment Modules PowerShell init script
    # with the `modules` alias. Dot-source it in this function scope so the
    # alias remains visible for the modulefile operations below.
    . (Join-Path $InstallPrefix "init\pwsh.ps1")

    Get-Command modules -ErrorAction Stop | Out-Null

    # FindCUDA declares MSVC and UCRT prerequisites on Windows.
    modules load $VisualStudioModule
    modules load $MsvcModule
    modules load $UcrtModule
    modules load $CudaModule

    if ($Case -eq "Environment") {
        modules list

        foreach ($Command in @(
            "cl.exe",
            "link.exe",
            "nvcc.exe"
        )) {
            Get-Command `
                $Command `
                -CommandType Application `
                -ErrorAction Stop |
                Out-Null
        }

        & nvcc.exe --version

        if ($LASTEXITCODE -ne 0) {
            throw "nvcc --version failed."
        }

        Write-Host "NVIDIA CUDA 13.2 module stack passed."
        return
    }

    if ($Case -eq "NVCC") {
        $source = Join-Path $sourceRoot "hello.cu"
        $output = Join-Path $outputRoot "hello-cuda.exe"

        & nvcc.exe `
            -ccbin cl.exe `
            -Xcompiler=/Zc:preprocessor `
            -o $output `
            $source

        if ($LASTEXITCODE -ne 0) {
            throw "NVCC failed to compile/link hello.cu."
        }

        if (-not (
            Test-Path `
                -LiteralPath $output `
                -PathType Leaf
        )) {
            throw "CUDA test executable was not generated: $output"
        }

        & $output

        if ($LASTEXITCODE -ne 0) {
            throw "The CUDA host test executable failed."
        }

        Write-Host "NVIDIA CUDA 13.2 NVCC compile/link/runtime test passed."
    }
}

Export-ModuleMember -Function test-nvda
