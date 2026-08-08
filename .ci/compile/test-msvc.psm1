# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$script:SourceRoot = Join-Path $PSScriptRoot "..\sources"

if ($env:RUNNER_TEMP) {
    $script:OutputRoot = Join-Path $env:RUNNER_TEMP "wemi-test-msvc"
}
else {
    $script:OutputRoot = Join-Path ([System.IO.Path]::GetTempPath()) "wemi-test-msvc"
}


function new-msvc-test-directory {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Name
    )

    $Path = Join-Path $script:OutputRoot $Name

    Remove-Item `
        -LiteralPath $Path `
        -Recurse `
        -Force `
        -ErrorAction SilentlyContinue

    New-Item `
        -ItemType Directory `
        -Force `
        -Path $Path |
        Out-Null

    return $Path
}


function assert-msvc-command {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Name
    )

    $Command = Get-Command `
        $Name `
        -CommandType Application `
        -ErrorAction Stop

    Write-Host (
        "{0,-12} {1}" -f `
        $Name, `
        $Command.Source
    )
}


function assert-native-success {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Message
    )

    if ($LASTEXITCODE -ne 0) {
        throw "$Message Exit code: $LASTEXITCODE"
    }
}


function invoke-msvc-test-executable {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Path,

        [Parameter(Mandatory)]
        [string]$Message
    )

    if (-not (
        Test-Path `
            -LiteralPath $Path `
            -PathType Leaf
    )) {
        throw "Expected executable was not generated: $Path"
    }

    & $Path

    if ($LASTEXITCODE -ne 0) {
        throw "$Message Exit code: $LASTEXITCODE"
    }
}


function write-utf8-source {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$Path,

        [Parameter(Mandatory)]
        [string]$Content
    )

    [System.IO.File]::WriteAllText(
        $Path,
        $Content,
        [System.Text.UTF8Encoding]::new($false)
    )
}


function initialize-msvc-environment {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$InstallPrefix,

        [Parameter(Mandatory)]
        [string]$VisualStudioModule,

        [Parameter(Mandatory)]
        [string]$MsvcModule,

        [Parameter(Mandatory)]
        [string]$UcrtModule
    )

    $ModulesInit = Join-Path `
        $PSScriptRoot `
        "..\common\modules-init.psm1"

    Import-Module `
        $ModulesInit `
        -Force

    init-modules `
        -InstallPrefix $InstallPrefix

    Write-Host "Loading module: $VisualStudioModule"
    module load $VisualStudioModule

    Write-Host "Loading module: $MsvcModule"
    module load $MsvcModule

    Write-Host "Loading module: $UcrtModule"
    module load $UcrtModule

    Write-Host "Loaded module stack:"
    module list

    Write-Host "MSVC development commands:"

    foreach ($Command in @(
        "cl.exe",
        "link.exe",
        "lib.exe",
        "ml64.exe",
        "rc.exe"
    )) {
        assert-msvc-command $Command
    }
}


function test-msvc-cc {
    [CmdletBinding()]
    param()

    $OutputRoot = new-msvc-test-directory "c"

    $Source = Join-Path $script:SourceRoot "hello.c"
    $Executable = Join-Path $OutputRoot "hello-c.exe"

    Push-Location $OutputRoot

    try {
        & cl.exe `
            /nologo `
            /W4 `
            /WX `
            /TC `
            "/Fe:$Executable" `
            $Source

        assert-native-success `
            "MSVC failed to compile/link hello.c."

        invoke-msvc-test-executable `
            -Path $Executable `
            -Message "The MSVC C test executable failed."
    }
    finally {
        Pop-Location
    }

    Write-Host "MSVC C compile/link/runtime test passed."
}


function test-msvc-cxx {
    [CmdletBinding()]
    param()

    $OutputRoot = new-msvc-test-directory "cxx"

    $Source = Join-Path $script:SourceRoot "hello.cc"
    $Executable = Join-Path $OutputRoot "hello-cxx.exe"

    Push-Location $OutputRoot

    try {
        & cl.exe `
            /nologo `
            /W4 `
            /WX `
            /EHsc `
            /TP `
            "/Fe:$Executable" `
            $Source

        assert-native-success `
            "MSVC failed to compile/link hello.cc."

        invoke-msvc-test-executable `
            -Path $Executable `
            -Message "The MSVC C++ test executable failed."
    }
    finally {
        Pop-Location
    }

    Write-Host "MSVC C++ compile/link/runtime test passed."
}


function test-msvc-lib {
    [CmdletBinding()]
    param()

    $OutputRoot = new-msvc-test-directory "static-lib"

    $LibrarySource = Join-Path $OutputRoot "wemi-static.c"
    $ConsumerSource = Join-Path $OutputRoot "wemi-static-consumer.c"

    $Object = Join-Path $OutputRoot "wemi-static.obj"
    $Library = Join-Path $OutputRoot "wemi-static.lib"
    $Executable = Join-Path $OutputRoot "wemi-static-test.exe"

    write-utf8-source `
        -Path $LibrarySource `
        -Content @'
int wemi_add(int a, int b)
{
    return a + b;
}
'@

    write-utf8-source `
        -Path $ConsumerSource `
        -Content @'
#include <stdio.h>

int wemi_add(int a, int b);

int main(void)
{
    int result = wemi_add(20, 22);

    if (result != 42) {
        fprintf(stderr, "Unexpected static-library result: %d\n", result);
        return 1;
    }

    puts("MSVC static library consumer passed.");
    return 0;
}
'@

    Push-Location $OutputRoot

    try {
        & cl.exe `
            /nologo `
            /W4 `
            /WX `
            /TC `
            /c `
            "/Fo:$Object" `
            $LibrarySource

        assert-native-success `
            "MSVC failed to compile the static-library object."

        & lib.exe `
            /nologo `
            "/OUT:$Library" `
            $Object

        assert-native-success `
            "LIB failed to create the static library."

        if (-not (
            Test-Path `
                -LiteralPath $Library `
                -PathType Leaf
        )) {
            throw "Static library was not generated: $Library"
        }

        & cl.exe `
            /nologo `
            /W4 `
            /WX `
            /TC `
            $ConsumerSource `
            $Library `
            "/Fe:$Executable"

        assert-native-success `
            "MSVC failed to link the static-library consumer."

        invoke-msvc-test-executable `
            -Path $Executable `
            -Message "The static-library consumer failed."
    }
    finally {
        Pop-Location
    }

    Write-Host "MSVC static library build/link/runtime test passed."
}


function test-msvc-dll {
    [CmdletBinding()]
    param()

    $OutputRoot = new-msvc-test-directory "dll"

    $LibrarySource = Join-Path $OutputRoot "wemi-dll.c"
    $ConsumerSource = Join-Path $OutputRoot "wemi-dll-consumer.c"

    $Dll = Join-Path $OutputRoot "wemi-smoke.dll"
    $ImportLibrary = Join-Path $OutputRoot "wemi-smoke.lib"
    $Executable = Join-Path $OutputRoot "wemi-dll-test.exe"

    write-utf8-source `
        -Path $LibrarySource `
        -Content @'
__declspec(dllexport)
int wemi_add(int a, int b)
{
    return a + b;
}
'@

    write-utf8-source `
        -Path $ConsumerSource `
        -Content @'
#include <stdio.h>

__declspec(dllimport)
int wemi_add(int a, int b);

int main(void)
{
    int result = wemi_add(20, 22);

    if (result != 42) {
        fprintf(stderr, "Unexpected DLL result: %d\n", result);
        return 1;
    }

    puts("MSVC DLL consumer passed.");
    return 0;
}
'@

    Push-Location $OutputRoot

    try {
        & cl.exe `
            /nologo `
            /W4 `
            /WX `
            /TC `
            /LD `
            $LibrarySource `
            "/Fe:$Dll" `
            /link `
            "/IMPLIB:$ImportLibrary"

        assert-native-success `
            "MSVC failed to build the DLL."

        foreach ($Artifact in @(
            $Dll,
            $ImportLibrary
        )) {
            if (-not (
                Test-Path `
                    -LiteralPath $Artifact `
                    -PathType Leaf
            )) {
                throw "Expected DLL artifact was not generated: $Artifact"
            }
        }

        & cl.exe `
            /nologo `
            /W4 `
            /WX `
            /TC `
            $ConsumerSource `
            $ImportLibrary `
            "/Fe:$Executable"

        assert-native-success `
            "MSVC failed to link the DLL consumer."

        invoke-msvc-test-executable `
            -Path $Executable `
            -Message "The DLL consumer failed."
    }
    finally {
        Pop-Location
    }

    Write-Host "MSVC DLL build/link/runtime test passed."
}


function test-ml64 {
    [CmdletBinding()]
    param()

    $OutputRoot = new-msvc-test-directory "masm"

    $Source = Join-Path $script:SourceRoot "hello.asm"
    $Executable = Join-Path $OutputRoot "hello-asm.exe"

    Push-Location $OutputRoot

    try {
        & ml64.exe `
            /nologo `
            "/Fe$Executable" `
            $Source `
            /link `
            /subsystem:console `
            /entry:main `
            kernel32.lib

        assert-native-success `
            "ML64/MASM assembly or linking failed."

        invoke-msvc-test-executable `
            -Path $Executable `
            -Message "The MASM test executable failed."
    }
    finally {
        Pop-Location
    }

    Write-Host "ML64/MASM assemble/link/runtime test passed."
}


function test-rc {
    [CmdletBinding()]
    param()

    $OutputRoot = new-msvc-test-directory "resource"

    $Source = Join-Path $script:SourceRoot "hello.rc"
    $Resource = Join-Path $OutputRoot "hello.res"

    Push-Location $OutputRoot

    try {
        & rc.exe `
            /nologo `
            "/fo$Resource" `
            $Source

        assert-native-success `
            "RC failed to compile hello.rc."

        if (-not (
            Test-Path `
                -LiteralPath $Resource `
                -PathType Leaf
        )) {
            throw "RC completed without producing hello.res."
        }
    }
    finally {
        Pop-Location
    }

    Write-Host "Windows Resource Compiler test passed."
}


Export-ModuleMember -Function `
    initialize-msvc-environment, `
    test-msvc-cc, `
    test-msvc-cxx, `
    test-msvc-lib, `
    test-msvc-dll, `
    test-ml64, `
    test-rc
