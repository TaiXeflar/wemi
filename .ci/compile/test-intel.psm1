# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

function test-intel {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [ValidateSet(
            "Environment",
            "ICX_CL_C",
            "ICX_CL_CXX",
            "ICPX_CXX",
            "IFX"
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
        [string]$OneApiModule,

        [Parameter(Mandatory)]
        [string]$CompilerModule
    )

    $ErrorActionPreference = "Stop"

    $sourceRoot = Join-Path $PSScriptRoot "..\sources"
    $outputRoot = Join-Path $env:RUNNER_TEMP "wemi-test-intel-$Case"

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
    # alias remains visible for all modulefile operations below.
    . (Join-Path $InstallPrefix "init\pwsh.ps1")

    Get-Command modules -ErrorAction Stop | Out-Null

    # Intel compiler modulefiles require an x64 MSVC/UCRT environment.
    modules load $VisualStudioModule
    modules load $MsvcModule
    modules load $UcrtModule

    # intel/compiler/* is exposed through intel/oneapi MODULEPATH.
    modules load $OneApiModule
    modules load $CompilerModule

    if ($Case -eq "Environment") {
        modules list

        foreach ($Command in @(
            "icx-cl.exe",
            "icpx.exe",
            "ifx.exe"
        )) {
            Get-Command `
                $Command `
                -CommandType Application `
                -ErrorAction Stop |
                Out-Null
        }

        Write-Host "Intel oneAPI compiler module stack passed."
        return
    }

    switch ($Case) {
        "ICX_CL_C" {
            $source = Join-Path $sourceRoot "hello.c"
            $output = Join-Path $outputRoot "hello-icx-cl-c.exe"

            & icx-cl.exe `
                /nologo `
                /W4 `
                /WX `
                /TC `
                "/Fe:$output" `
                $source

            if ($LASTEXITCODE -ne 0) {
                throw "icx-cl failed to compile/link hello.c."
            }

            & $output

            if ($LASTEXITCODE -ne 0) {
                throw "The icx-cl C test executable failed."
            }

            Write-Host "Intel icx-cl C compile/link/runtime test passed."
        }

        "ICX_CL_CXX" {
            $source = Join-Path $sourceRoot "hello.cc"
            $output = Join-Path $outputRoot "hello-icx-cl-cxx.exe"

            & icx-cl.exe `
                /nologo `
                /W4 `
                /WX `
                /EHsc `
                /TP `
                "/Fe:$output" `
                $source

            if ($LASTEXITCODE -ne 0) {
                throw "icx-cl failed to compile/link hello.cc."
            }

            & $output

            if ($LASTEXITCODE -ne 0) {
                throw "The icx-cl C++ test executable failed."
            }

            Write-Host "Intel icx-cl C++ compile/link/runtime test passed."
        }

        "ICPX_CXX" {
            $source = Join-Path $sourceRoot "hello.cc"
            $output = Join-Path $outputRoot "hello-icpx.exe"

            & icpx.exe `
                -Wall `
                -Werror `
                $source `
                -o `
                $output

            if ($LASTEXITCODE -ne 0) {
                throw "icpx failed to compile/link hello.cc."
            }

            & $output

            if ($LASTEXITCODE -ne 0) {
                throw "The icpx C++ test executable failed."
            }

            Write-Host "Intel icpx C++ compile/link/runtime test passed."
        }

        "IFX" {
            $source = Join-Path $sourceRoot "hello.f90"
            $output = Join-Path $outputRoot "hello-ifx.exe"

            & ifx.exe `
                /nologo `
                "/exe:$output" `
                $source

            if ($LASTEXITCODE -ne 0) {
                throw "ifx failed to compile/link hello.f90."
            }

            & $output

            if ($LASTEXITCODE -ne 0) {
                throw "The ifx Fortran test executable failed."
            }

            Write-Host "Intel ifx Fortran compile/link/runtime test passed."
        }
    }
}

Export-ModuleMember -Function test-intel
