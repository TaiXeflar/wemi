
# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

$ErrorActionPreference = 'Stop'

Set-StrictMode -Version Latest

function test-tclsh {
    $tclsh = Get-Command tclsh.exe -ErrorAction Stop

    $versionText = "puts [info patchlevel]" |
        & $tclsh.Source |
        Select-Object -Last 1

    if ($LASTEXITCODE -ne 0) {
        throw "tclsh failed with exit code $LASTEXITCODE."
    }

    $versionText = $versionText.Trim()

    try {
        $version = [version]$versionText
    }
    catch {
        throw "Unable to parse Tcl/Tk version: $versionText"
    }

    if ($version -lt [version]"8.6") {
        throw "Tcl/Tk 8.6 or newer is required. Found: $version"
    }

    Write-Host "Tcl/Tk test passed: $version"
}
function test-msvc {
    $sourceRoot = Join-Path $PSScriptRoot "..\sources"
    $outputRoot = Join-Path $env:RUNNER_TEMP "wemi-test-msvc"

    New-Item -ItemType Directory -Force -Path $outputRoot | Out-Null

    $cSource = Join-Path $sourceRoot "hello.c"
    $cppSource = Join-Path $sourceRoot "hello.cc"

    $cOutput = Join-Path $outputRoot "hello-c.exe"
    $cppOutput = Join-Path $outputRoot "hello-cpp.exe"

    Get-Command cl.exe -ErrorAction Stop | Out-Null

    & cl.exe /nologo /W4 /WX /TC "/Fe:$cOutput" $cSource

    if ($LASTEXITCODE -ne 0) {
        throw "MSVC failed to compile hello.c."
    }

    & $cOutput

    if ($LASTEXITCODE -ne 0) {
        throw "The MSVC C test executable failed."
    }

    & cl.exe /nologo /W4 /WX /EHsc /TP "/Fe:$cppOutput"  $cppSource

    if ($LASTEXITCODE -ne 0) {
        throw "MSVC failed to compile hello.cc."
    }

    & $cppOutput

    if ($LASTEXITCODE -ne 0) {
        throw "The MSVC C++ test executable failed."
    }

    Write-Host "MSVC C and C++ tests passed."
}

function test-ml64 {
    $sourceRoot = Join-Path $PSScriptRoot "..\sources"
    $outputRoot = Join-Path $env:RUNNER_TEMP "wemi-test-ml64"

    New-Item -ItemType Directory -Force -Path $outputRoot | Out-Null

    $source = Join-Path $sourceRoot "hello.asm"
    $executable = Join-Path $outputRoot "hello-asm.exe"

    Get-Command ml64.exe -ErrorAction Stop | Out-Null

    & ml64.exe `
        /nologo `
        "/Fe$executable" `
        $source `
        /link `
        /subsystem:console `
        /entry:main `
        kernel32.lib

    if ($LASTEXITCODE -ne 0) {
        throw "ML64/MASM assembly or linking failed."
    }

    & $executable

    if ($LASTEXITCODE -ne 0) {
        throw "The MASM test executable failed."
    }

    Write-Host "ML64/MASM test passed."
}

function test-rc {
    $sourceRoot = Join-Path $PSScriptRoot "..\sources"
    $outputRoot = Join-Path $env:RUNNER_TEMP "wemi-test-rc"

    New-Item -ItemType Directory -Force -Path $outputRoot | Out-Null

    $source = Join-Path $sourceRoot "hello.rc"
    $resource = Join-Path $outputRoot "hello.res"

    Get-Command rc.exe -ErrorAction Stop | Out-Null

    & rc.exe /nologo "/fo$resource" $source

    if ($LASTEXITCODE -ne 0) {
        throw "RC failed to compile hello.rc."
    }

    if (-not (Test-Path $resource)) {
        throw "RC completed without producing hello.res."
    }

    Write-Host "Windows Resource Compiler test passed."
}

function test-icx {
    $sourceRoot = Join-Path $PSScriptRoot "..\sources"
    $outputRoot = Join-Path $env:RUNNER_TEMP "wemi-test-icx"

    New-Item -ItemType Directory -Force -Path $outputRoot | Out-Null

    $source = Join-Path $sourceRoot "hello.c"
    $executable = Join-Path $outputRoot "hello-icx.exe"

    Get-Command icx.exe -ErrorAction Stop | Out-Null

    & icx.exe  $source -Wall  -Werror -o $executable

    if ($LASTEXITCODE -ne 0) {
        throw "icx failed to compile hello.c."
    }

    & $executable

    if ($LASTEXITCODE -ne 0) {
        throw "The icx test executable failed."
    }

    Write-Host "Intel icx test passed."
}

function test-ifx {
    $sourceRoot = Join-Path $PSScriptRoot "..\sources"
    $outputRoot = Join-Path $env:RUNNER_TEMP "wemi-test-ifx"

    New-Item -ItemType Directory -Force -Path $outputRoot | Out-Null

    $source = Join-Path $sourceRoot "hello.f90"
    $executable = Join-Path $outputRoot "hello-ifx.exe"

    Get-Command ifx.exe -ErrorAction Stop | Out-Null

    & ifx.exe $source "/exe:$executable"

    if ($LASTEXITCODE -ne 0) {
        throw "IFX failed to compile hello.f90."
    }

    & $executable

    if ($LASTEXITCODE -ne 0) {
        throw "The IFX test executable failed."
    }

    Write-Host "Intel IFX test passed."
}

function test-icpx {
    $sourceRoot = Join-Path $PSScriptRoot "..\sources"
    $outputRoot = Join-Path $env:RUNNER_TEMP "wemi-test-icpx"

    New-Item -ItemType Directory -Force -Path $outputRoot | Out-Null

    $source = Join-Path $sourceRoot "hello.sycl.cpp"
    $executable = Join-Path $outputRoot "hello-icpx.exe"

    Get-Command icpx.exe -ErrorAction Stop | Out-Null

    & icpx.exe -fsycl $source -o $executable

    if ($LASTEXITCODE -ne 0) {
        throw "ICPX failed to compile the SYCL source."
    }

    & $executable

    if ($LASTEXITCODE -ne 0) {
        throw "The ICPX/SYCL test executable failed."
    }

    Write-Host "Intel ICPX/SYCL test passed."
}

function test-nvcc {
    $sourceRoot = Join-Path $PSScriptRoot "..\sources"
    $outputRoot = Join-Path $env:RUNNER_TEMP "wemi-test-nvcc"

    New-Item -ItemType Directory -Force -Path $outputRoot | Out-Null

    $source = Join-Path $sourceRoot "hello.cu"
    $executable = Join-Path $outputRoot "hello-nvcc.exe"

    Get-Command nvcc.exe -ErrorAction Stop | Out-Null

    & nvcc.exe $source -Werror all-warnings -o $executable

    if ($LASTEXITCODE -ne 0) {
        throw "NVCC failed to compile hello.cu."
    }

    & $executable

    if ($LASTEXITCODE -ne 0) {
        throw "The NVCC host test executable failed."
    }

    Write-Host "NVIDIA NVCC host compilation test passed."
}

function test-hip {
    $sourceRoot = Join-Path $PSScriptRoot "..\sources"
    $outputRoot = Join-Path $env:RUNNER_TEMP "wemi-test-hip"

    New-Item -ItemType Directory -Force -Path $outputRoot | Out-Null

    $source = Join-Path $sourceRoot "hello.hip.cpp"
    $executable = Join-Path $outputRoot "hello-hip.exe"

    Get-Command hipcc.exe -ErrorAction Stop | Out-Null

    & hipcc.exe $source -Wall -Werror -o $executable

    if ($LASTEXITCODE -ne 0) {
        throw "HIPCC failed to compile hello.hip.cpp."
    }

    & $executable

    if ($LASTEXITCODE -ne 0) {
        throw "The HIP host test executable failed."
    }

    Write-Host "HIP host compilation test passed."
}

function test-hipify {
    $sourceRoot = Join-Path $PSScriptRoot "..\sources"
    $outputRoot = Join-Path $env:RUNNER_TEMP "wemi-test-hipify"

    New-Item -ItemType Directory -Force -Path $outputRoot | Out-Null

    $source = Join-Path $sourceRoot "hello-hipify.cu"
    $output = Join-Path $outputRoot "hello-hipified.cpp"
    $errorLog = Join-Path $outputRoot "hipify-error.log"

    Get-Command hipify-clang.exe -ErrorAction Stop | Out-Null

    if ([string]::IsNullOrWhiteSpace($env:CUDA_PATH)) {
        throw "CUDA_PATH is not defined."
    }

    & hipify-clang.exe `
        $source `
        "--cuda-path=$env:CUDA_PATH" `
        -- `
        -std=c++17 `
        2> $errorLog |
        Set-Content -Path $output -Encoding utf8

    if ($LASTEXITCODE -ne 0) {
        if (Test-Path $errorLog) {
            Get-Content $errorLog | Write-Host
        }

        throw "hipify-clang failed to translate hello-hipify.cu."
    }

    if (-not (Test-Path $output)) {
        throw "hipify-clang did not produce an output file."
    }

    $content = Get-Content $output -Raw

    if ($content -notmatch "hip/hip_runtime") {
        throw "The hipified source does not include the HIP runtime header."
    }

    if ($content -notmatch "hipMalloc") {
        throw "cudaMalloc was not translated to hipMalloc."
    }

    Write-Host "HIPIFY translation test passed."
}

Export-ModuleMember -Function `
    test-tclsh, `
    test-msvc, `
    test-ml64, `
    test-rc, `
    test-icx, `
    test-ifx, `
    test-icpx, `
    test-nvcc, `
    test-hip, `
    test-hipify
