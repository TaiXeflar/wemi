
# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

function Install-Everything {
    winget install `
        --id voidtools.Everything `
        --exact `
        --silent `
        --accept-package-agreements `
        --accept-source-agreements `
        --disable-interactivity

    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install Everything."
    }

    $service = Get-Service `
        -Name "Everything" `
        -ErrorAction SilentlyContinue

    if (-not $service) {
        throw "Everything was installed, but the Everything service was not found."
    }

    if ($service.Status -ne "Running") {
        Start-Service -Name "Everything"
    }

    $service = Get-Service -Name "Everything"

    if ($service.Status -ne "Running") {
        throw "Everything service failed to start."
    }

    $EverythingDirectory = Join-Path `
        $env:ProgramFiles `
        "Everything"

    $EverythingExecutable = Join-Path `
        $EverythingDirectory `
        "Everything.exe"

    if (-not (
        Test-Path `
            -LiteralPath $EverythingExecutable `
            -PathType Leaf
    )) {
        throw (
            "Everything was installed, but Everything.exe " +
            "was not found at: $EverythingExecutable"
        )
    }

    $env:PATH = "$EverythingDirectory;$env:PATH"

    if ($env:GITHUB_PATH) {
        Add-Content `
            -LiteralPath $env:GITHUB_PATH `
            -Value $EverythingDirectory `
            -Encoding utf8
    }

    Write-Host "Everything executable:"
    Write-Host "  $EverythingExecutable"
}

function Install-ES {
    [CmdletBinding()]
    param()

    $PackageId = "voidtools.Everything.Cli"

    Write-Host "Installing Everything CLI..."

    winget install `
        --id $PackageId `
        --exact `
        --source winget `
        --accept-package-agreements `
        --accept-source-agreements `
        --disable-interactivity `
        --silent

    # WinGet installs the package under:
    #
    # %LOCALAPPDATA%\Microsoft\WinGet\Packages\
    # voidtools.Everything.Cli_Microsoft.Winget.Source_8wekyb3d8bbwe\
    # es.exe

    $WinGetPackagesRoot = Join-Path `
        $env:LOCALAPPDATA `
        "Microsoft\WinGet\Packages"

    $PackageDirectory = Join-Path `
        $WinGetPackagesRoot `
        "voidtools.Everything.Cli_Microsoft.Winget.Source_8wekyb3d8bbwe"

    $EsExecutable = Join-Path `
        $PackageDirectory `
        "es.exe"

    if (-not (
        Test-Path `
            -LiteralPath $EsExecutable `
            -PathType Leaf
    )) {
        throw (
            "Everything CLI installation completed, " +
            "but es.exe was not found at: $EsExecutable"
        )
    }

    # Make es.exe available inside the current PowerShell process.
    if (
        $env:PATH -notlike "*$PackageDirectory*"
    ) {
        $env:PATH = "$PackageDirectory;$env:PATH"
    }

    # Make es.exe available to following GitHub Actions steps.
    if ($env:GITHUB_PATH) {
        Add-Content `
            -LiteralPath $env:GITHUB_PATH `
            -Value $PackageDirectory `
            -Encoding utf8
    }

    Write-Host "Everything CLI installed:"
    Write-Host "  $EsExecutable"

    $EsCommand = Get-Command `
        $EsExecutable `
        -CommandType Application `
        -ErrorAction Stop

    Write-Host "Everything CLI executable:"
    Write-Host "  $($EsCommand.Source)"
}


function Test-Winget {
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        throw "winget is not available."
    }
}

function Install-TclTk {
    winget install `
        --id Magicsplat.TclTk `
        --exact `
        --silent `
        --accept-package-agreements `
        --accept-source-agreements `
        --disable-interactivity

    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install Magicsplat Tcl/Tk."
    }
}

function Install-oneAPI {
    winget install `
        --id Intel.OneAPI.HPCToolkit `
        --exact `
        --silent `
        --accept-package-agreements `
        --accept-source-agreements `
        --disable-interactivity

    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install Intel oneAPI HPC Toolkit."
    }
}

function Install-CUDA118 {
    winget install `
        --id Nvidia.CUDA `
        --exact `
        --version '11.8' `
        --silent `
        --accept-package-agreements `
        --accept-source-agreements `
        --disable-interactivity

    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install NVIDIA CUDA 11.8."
    }
}

function Install-CUDA126 {
    winget install `
        --id Nvidia.CUDA `
        --exact `
        --version '12.6' `
        --silent `
        --accept-package-agreements `
        --accept-source-agreements `
        --disable-interactivity

    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install NVIDIA CUDA 12.6."
    }
}

function Install-CUDA132 {
    winget install `
        --id Nvidia.CUDA `
        --exact `
        --version '13.2' `
        --silent `
        --accept-package-agreements `
        --accept-source-agreements `
        --disable-interactivity

    if ($LASTEXITCODE -ne 0) {
        throw "Failed to install NVIDIA CUDA 13.2."
    }
}

Export-ModuleMember -Function   `
    Test-Winget,                `
    Install-Everything,         `
    Install-ES,                 `
    Install-TclTk,              `
    Install-oneAPI,             `
    Install-CUDA11,             `
    Install-CUDA12,             `
    Install-CUDA13
