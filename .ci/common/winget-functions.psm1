
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

function Install-CUDA11 {
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

function Install-CUDA12 {
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

function Install-CUDA13 {
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
    Install-TclTk,              `
    Install-oneAPI,             `
    Install-CUDA11,             `
    Install-CUDA12,             `
    Install-CUDA13
