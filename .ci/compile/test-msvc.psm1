# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

function test-msvc {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [ValidateSet(
            "Environment",
            "C",
            "CXX",
            "LIB",
            "DLL",
            "ASM",
            "RC"
        )]
        [string]$Case,

        [Parameter(Mandatory)]
        [string]$InstallPrefix,

        [Parameter(Mandatory)]
        [string]$VisualStudioModule,

        [Parameter(Mandatory)]
        [string]$MsvcModule,

        [Parameter(Mandatory)]
        [string]$UcrtModule
    )

    $ErrorActionPreference = "Stop"

    $sourceRoot = Join-Path $PSScriptRoot "..\sources"
    $outputRoot = Join-Path $env:RUNNER_TEMP "wemi-test-msvc-$Case"

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

    # modules-init.psm1 performs WEMI's normal Environment Modules
    # initialization. Its dot-sourced pwsh.ps1 is patched by WEMI with:
    #   Set-Alias -Name modules -Value envmodule
    #
    # init-modules is itself a PowerShell function, so that injected alias
    # belongs to init-modules' local scope. Dot-source the installed script
    # once more in this test function's scope so every invocation below uses
    # WEMI's patched `modules` alias, never PowerShell's `module` name.
    Import-Module `
        (Join-Path $PSScriptRoot "..\common\modules-init.psm1") `
        -Force

    init-modules `
        -InstallPrefix $InstallPrefix

    . (Join-Path $InstallPrefix "init\pwsh.ps1")

    Get-Command modules -ErrorAction Stop | Out-Null

    modules load $VisualStudioModule
    modules load $MsvcModule
    modules load $UcrtModule

    if ($Case -eq "Environment") {
        modules list

        foreach ($Command in @(
            "cl.exe",
            "link.exe",
            "lib.exe",
            "ml64.exe",
            "rc.exe"
        )) {
            Get-Command `
                $Command `
                -CommandType Application `
                -ErrorAction Stop |
                Out-Null
        }

        Write-Host "VS2026 / MSVC v145 / UCRT module stack passed."
        return
    }

    switch ($Case) {
        "C" {
            $source = Join-Path $sourceRoot "hello.c"
            $output = Join-Path $outputRoot "hello-c.exe"

            & cl.exe `
                /nologo `
                /W4 `
                /WX `
                /TC `
                "/Fe:$output" `
                $source

            if ($LASTEXITCODE -ne 0) {
                throw "MSVC failed to compile/link hello.c."
            }

            & $output

            if ($LASTEXITCODE -ne 0) {
                throw "The MSVC C test executable failed."
            }

            Write-Host "MSVC C compile/link/runtime test passed."
        }

        "CXX" {
            $source = Join-Path $sourceRoot "hello.cc"
            $output = Join-Path $outputRoot "hello-cxx.exe"

            & cl.exe `
                /nologo `
                /W4 `
                /WX `
                /EHsc `
                /TP `
                "/Fe:$output" `
                $source

            if ($LASTEXITCODE -ne 0) {
                throw "MSVC failed to compile/link hello.cc."
            }

            & $output

            if ($LASTEXITCODE -ne 0) {
                throw "The MSVC C++ test executable failed."
            }

            Write-Host "MSVC C++ compile/link/runtime test passed."
        }

        "LIB" {
            $source = Join-Path $sourceRoot "hello.c"
            $object = Join-Path $outputRoot "hello.obj"
            $library = Join-Path $outputRoot "hello.lib"

            & cl.exe `
                /nologo `
                /W4 `
                /WX `
                /TC `
                /c `
                "/Fo:$object" `
                $source

            if ($LASTEXITCODE -ne 0) {
                throw "MSVC failed to compile the static-library object."
            }

            & lib.exe `
                /nologo `
                "/OUT:$library" `
                $object

            if ($LASTEXITCODE -ne 0) {
                throw "LIB failed to create hello.lib."
            }

            if (-not (
                Test-Path `
                    -LiteralPath $library `
                    -PathType Leaf
            )) {
                throw "Static library was not generated: $library"
            }

            Write-Host "MSVC static library compile/archive test passed."
        }

        "DLL" {
            $source = Join-Path $sourceRoot "hello.c"
            $object = Join-Path $outputRoot "hello.obj"
            $dll = Join-Path $outputRoot "hello.dll"

            & cl.exe `
                /nologo `
                /W4 `
                /WX `
                /TC `
                /c `
                "/Fo:$object" `
                $source

            if ($LASTEXITCODE -ne 0) {
                throw "MSVC failed to compile the DLL object."
            }

            & link.exe `
                /nologo `
                /DLL `
                "/OUT:$dll" `
                $object

            if ($LASTEXITCODE -ne 0) {
                throw "LINK failed to create hello.dll."
            }

            if (-not (
                Test-Path `
                    -LiteralPath $dll `
                    -PathType Leaf
            )) {
                throw "Dynamic library was not generated: $dll"
            }

            Write-Host "MSVC DLL compile/link test passed."
        }

        "ASM" {
            $source = Join-Path $sourceRoot "hello.asm"
            $output = Join-Path $outputRoot "hello-asm.exe"

            & ml64.exe `
                /nologo `
                "/Fe$output" `
                $source `
                /link `
                /subsystem:console `
                /entry:main `
                kernel32.lib

            if ($LASTEXITCODE -ne 0) {
                throw "ML64/MASM assembly or linking failed."
            }

            & $output

            if ($LASTEXITCODE -ne 0) {
                throw "The MASM test executable failed."
            }

            Write-Host "ML64/MASM assemble/link/runtime test passed."
        }

        "RC" {
            $source = Join-Path $sourceRoot "hello.rc"
            $resource = Join-Path $outputRoot "hello.res"

            & rc.exe `
                /nologo `
                "/fo$resource" `
                $source

            if ($LASTEXITCODE -ne 0) {
                throw "RC failed to compile hello.rc."
            }

            if (-not (
                Test-Path `
                    -LiteralPath $resource `
                    -PathType Leaf
            )) {
                throw "RC completed without producing hello.res."
            }

            Write-Host "Windows Resource Compiler test passed."
        }
    }
}

Export-ModuleMember -Function test-msvc
