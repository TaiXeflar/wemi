

# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

function test-cangjie {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [ValidateSet(
            "Environment",
            "Compile"
        )]
        [string]$Case,

        [Parameter(Mandatory)]
        [string]$InstallPrefix,

        [Parameter(Mandatory)]
        [string]$CangjieModule
    )

    $ErrorActionPreference = "Stop"

    Import-Module `
        (Join-Path $PSScriptRoot "..\common\modules-init.psm1") `
        -Force

    init-modules `
        -InstallPrefix $InstallPrefix

    . (Join-Path $InstallPrefix "init\pwsh.ps1")

    Get-Command modules -ErrorAction Stop | Out-Null

    modules load $CangjieModule

    if ($Case -eq "Environment") {
        modules list

        Get-Command `
            cjc.exe `
            -CommandType Application `
            -ErrorAction Stop |
            Out-Null

        & cjc.exe --version

        if ($LASTEXITCODE -ne 0) {
            throw "cjc --version failed."
        }

        Write-Host "Cangjie LTS module stack passed."
        return
    }

    if ($Case -eq "Compile") {
        $sourceRoot = Join-Path $PSScriptRoot "..\sources"
        $source = Join-Path $sourceRoot "hello.cj"

        $outputRoot = Join-Path `
            $env:RUNNER_TEMP `
            "wemi-test-cangjie"

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

        $output = Join-Path $outputRoot "hello.exe"

        & cjc.exe `
            $source `
            -o `
            $output

        if ($LASTEXITCODE -ne 0) {
            throw "Cangjie failed to compile/link hello.cj."
        }

        & $output

        if ($LASTEXITCODE -ne 0) {
            throw "The Cangjie test executable failed."
        }

        Write-Host "Cangjie compile/link/runtime test passed."
    }
}

Export-ModuleMember -Function test-cangjie
