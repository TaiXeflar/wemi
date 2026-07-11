# SPDX-License-Identifier: MIT

[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

$reportDir = Join-Path $PWD "windows-2025-report"
New-Item -ItemType Directory -Force $reportDir | Out-Null

function Save-CommandOutput {
    param(
        [Parameter(Mandatory)]
        [string]$Name,

        [Parameter(Mandatory)]
        [scriptblock]$Command
    )

    Write-Host "`n===== $Name ====="

    $output = & $Command 2>&1
    $output | Tee-Object -FilePath (Join-Path $reportDir "$Name.txt")
}

Save-CommandOutput "runner-environment" {
    Get-ChildItem Env: |
        Sort-Object Name |
        Format-Table -AutoSize
}

Save-CommandOutput "windows" {
    Get-ComputerInfo |
        Select-Object WindowsProductName, WindowsVersion, OsBuildNumber,
            OsArchitecture, CsProcessors, CsTotalPhysicalMemory |
        Format-List
}

Save-CommandOutput "powershell" {
    $PSVersionTable
}

Save-CommandOutput "installed-commands" {
    Get-Command `
        winget.exe, git.exe, python.exe, uv.exe, cmake.exe, ninja.exe,
        msbuild.exe, cl.exe, link.exe, rc.exe, mt.exe `
        -ErrorAction SilentlyContinue |
        Select-Object Name, Version, Source |
        Format-Table -AutoSize
}

$vswhere = "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe"

Save-CommandOutput "visual-studio" {
    if (Test-Path -LiteralPath $vswhere) {
        & $vswhere -all -products * -format json
    }
    else {
        "vswhere.exe not found"
    }
}

Save-CommandOutput "visual-studio-components" {
    if (Test-Path -LiteralPath $vswhere) {
        & $vswhere `
            -all `
            -products * `
            -format json `
            -property installationPath
    }
}

Save-CommandOutput "vs-dev-scripts" {
    Get-ChildItem `
        "${env:ProgramFiles}\Microsoft Visual Studio",
        "${env:ProgramFiles(x86)}\Microsoft Visual Studio" `
        -Recurse `
        -Include VsDevCmd.bat, vcvarsall.bat `
        -ErrorAction SilentlyContinue |
        Select-Object FullName
}

Save-CommandOutput "windows-sdks" {
    Get-ChildItem `
        "C:\Program Files (x86)\Windows Kits\10" `
        -ErrorAction SilentlyContinue |
        Select-Object Name, FullName
}

Save-CommandOutput "msvc-toolsets" {
    Get-ChildItem `
        "C:\Program Files\Microsoft Visual Studio\18\Enterprise\VC\Tools\MSVC" `
        -Directory `
        -ErrorAction SilentlyContinue |
        Select-Object Name, FullName
}

Save-CommandOutput "cmake-generators" {
    cmake.exe --help
}

Save-CommandOutput "runner-image-metadata" {
    @(
        "ImageOS=$env:ImageOS"
        "ImageVersion=$env:ImageVersion"
        "RUNNER_OS=$env:RUNNER_OS"
        "RUNNER_ARCH=$env:RUNNER_ARCH"
    )
}

Write-Host "Windows SDK Include versions:"
Get-ChildItem `
    "C:\Program Files (x86)\Windows Kits\10\Include" `
    -Directory `
    -ErrorAction SilentlyContinue |
    Select-Object Name, FullName

Write-Host "Windows SDK Lib versions:"
Get-ChildItem `
    "C:\Program Files (x86)\Windows Kits\10\Lib" `
    -Directory `
    -ErrorAction SilentlyContinue |
    Select-Object Name, FullName

Write-Host "Windows SDK bin versions:"
Get-ChildItem `
    "C:\Program Files (x86)\Windows Kits\10\bin" `
    -Directory `
    -ErrorAction SilentlyContinue |
    Select-Object Name, FullName
