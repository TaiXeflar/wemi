

# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


$script:SourceRoot = Join-Path $PSScriptRoot "..\sources"
$script:OutputRoot = Join-Path $env:RUNNER_TEMP "wemi-test-msvc"


function New-MsvcSmokeDirectory {
    param(
        [Parameter(Mandatory)]
        [string]$Name
    )

    $path = Join-Path $script:OutputRoot $Name

    Remove-Item `
        -Recurse `
        -Force `
        -ErrorAction SilentlyContinue `
        $path

    New-Item `
        -ItemType Directory `
        -Force `
        -Path $path |
        Out-Null

    return $path
}


function Assert-Command {
    param(
        [Parameter(Mandatory)]
        [string]$Name
    )

    Get-Command $Name -ErrorAction Stop | Out-Null
}


function Assert-LastExitCode {
    param(
        [Parameter(Mandatory)]
        [string]$Message
    )

    if ($LASTEXITCODE -ne 0) {
        throw "$Message Exit code: $LASTEXITCODE"
    }
}


function Invoke-SmokeExecutable {
    param(
        [Parameter(Mandatory)]
        [string]$Path,

        [Parameter(Mandatory)]
        [string]$Message
    )

    if (-not (Test-Path $Path)) {
        throw "Expected executable was not generated: $Path"
    }

    & $Path

    if ($LASTEXITCODE -ne 0) {
        throw "$Message Exit code: $LASTEXITCODE"
    }
}


function Test-MsvcC {
    $outputRoot = New-MsvcSmokeDirectory "c"

    $source = Join-Path $script:SourceRoot "hello.c"
    $executable = Join-Path $outputRoot "hello-c.exe"

    Assert-Command "cl.exe"

    & cl.exe `
        /nologo `
        /W4 `
        /WX `
        /TC `
        "/Fe:$executable" `
        $source

    Assert-LastExitCode "MSVC failed to compile/link hello.c."

    Invoke-SmokeExecutable `
        -Path $executable `
        -Message "MSVC C executable failed."

    Write-Host "MSVC C compile/link/runtime smoke test passed."
}


function Test-MsvcCxx {
    $outputRoot = New-MsvcSmokeDirectory "cxx"

    $source = Join-Path $script:SourceRoot "hello.cc"
    $executable = Join-Path $outputRoot "hello-cxx.exe"

    Assert-Command "cl.exe"

    & cl.exe `
        /nologo `
        /W4 `
        /WX `
        /EHsc `
        /TP `
        "/Fe:$executable" `
        $source

    Assert-LastExitCode "MSVC failed to compile/link hello.cc."

    Invoke-SmokeExecutable `
        -Path $executable `
        -Message "MSVC C++ executable failed."

    Write-Host "MSVC C++ compile/link/runtime smoke test passed."
}


function Test-MsvcStaticLibrary {
    $outputRoot = New-MsvcSmokeDirectory "static-library"

    $librarySource = Join-Path $script:SourceRoot "library.c"
    $testSource = Join-Path $script:SourceRoot "library-test.c"

    $object = Join-Path $outputRoot "library.obj"
    $library = Join-Path $outputRoot "wemi-smoke.lib"
    $executable = Join-Path $outputRoot "static-library-test.exe"

    Assert-Command "cl.exe"
    Assert-Command "lib.exe"

    & cl.exe `
        /nologo `
        /W4 `
        /WX `
        /TC `
        /c `
        "/Fo:$object" `
        $librarySource

    Assert-LastExitCode "MSVC failed to compile the static-library object."

    & lib.exe `
        /nologo `
        "/OUT:$library" `
        $object

    Assert-LastExitCode "LIB failed to create the static library."

    if (-not (Test-Path $library)) {
        throw "Static library was not generated: $library"
    }

    & cl.exe `
        /nologo `
        /W4 `
        /WX `
        /TC `
        "/I$script:SourceRoot" `
        $testSource `
        $library `
        "/Fe:$executable"

    Assert-LastExitCode "MSVC failed to link against the static library."

    Invoke-SmokeExecutable `
        -Path $executable `
        -Message "Static-library consumer failed."

    Write-Host "MSVC static library smoke test passed."
}


function Test-MsvcDynamicLibrary {
    $outputRoot = New-MsvcSmokeDirectory "dynamic-library"

    $librarySource = Join-Path $script:SourceRoot "library.c"
    $testSource = Join-Path $script:SourceRoot "library-test.c"

    $dll = Join-Path $outputRoot "wemi-smoke.dll"
    $importLibrary = Join-Path $outputRoot "wemi-smoke.lib"
    $executable = Join-Path $outputRoot "dynamic-library-test.exe"

    Assert-Command "cl.exe"

    & cl.exe `
        /nologo `
        /W4 `
        /WX `
        /TC `
        /LD `
        /DWEMI_BUILD_DLL `
        $librarySource `
        "/Fe:$dll" `
        /link `
        "/IMPLIB:$importLibrary"

    Assert-LastExitCode "MSVC failed to build the DLL."

    if (-not (Test-Path $dll)) {
        throw "DLL was not generated: $dll"
    }

    if (-not (Test-Path $importLibrary)) {
        throw "DLL import library was not generated: $importLibrary"
    }

    & cl.exe `
        /nologo `
        /W4 `
        /WX `
        /TC `
        /DWEMI_USE_DLL `
        "/I$script:SourceRoot" `
        $testSource `
        $importLibrary `
        "/Fe:$executable"

    Assert-LastExitCode "MSVC failed to link against the DLL import library."

    Invoke-SmokeExecutable `
        -Path $executable `
        -Message "DLL consumer failed."

    Write-Host "MSVC dynamic library smoke test passed."
}


function Test-MsvcMasm {
    $outputRoot = New-MsvcSmokeDirectory "masm"

    $source = Join-Path $script:SourceRoot "hello.asm"
    $executable = Join-Path $outputRoot "hello-asm.exe"

    Assert-Command "ml64.exe"

    & ml64.exe `
        /nologo `
        "/Fe$executable" `
        $source `
        /link `
        /subsystem:console `
        /entry:main `
        kernel32.lib

    Assert-LastExitCode "ML64/MASM assembly or linking failed."

    Invoke-SmokeExecutable `
        -Path $executable `
        -Message "MASM executable failed."

    Write-Host "ML64/MASM assemble/link/runtime smoke test passed."
}


function Test-MsvcResource {
    $outputRoot = New-MsvcSmokeDirectory "resource"

    $source = Join-Path $script:SourceRoot "hello.rc"
    $resource = Join-Path $outputRoot "hello.res"

    Assert-Command "rc.exe"

    & rc.exe `
        /nologo `
        "/fo$resource" `
        $source

    Assert-LastExitCode "RC failed to compile hello.rc."

    if (-not (Test-Path $resource)) {
        throw "RC completed without producing hello.res."
    }

    Write-Host "Windows Resource Compiler smoke test passed."
}


Export-ModuleMember -Function `
    Test-MsvcC, `
    Test-MsvcCxx, `
    Test-MsvcStaticLibrary, `
    Test-MsvcDynamicLibrary, `
    Test-MsvcMasm, `
    Test-MsvcResource
