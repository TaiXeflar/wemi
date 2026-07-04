# SPDX-License-Identifier: MIT
# Copyright (c) 2026 WEMI Contributors

[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

function Add-ProcessAndGitHubPath {
    param(
        [Parameter(Mandatory)]
        [string]$PathToAdd
    )

    if (-not (Test-Path $PathToAdd)) {
        return
    }

    if (($env:Path -split ";") -notcontains $PathToAdd) {
        $env:Path = "$PathToAdd;$env:Path"
    }

    if ($env:GITHUB_PATH) {
        Add-Content -Path $env:GITHUB_PATH -Value $PathToAdd
    }
}

function Install-WingetPackage {
    param(
        [Parameter(Mandatory)]
        [string]$Id
    )

    Write-Host "Installing $Id ..."
    & winget install `
        --id $Id `
        --exact `
        --silent `
        --disable-interactivity `
        --accept-package-agreements `
        --accept-source-agreements

    if ($LASTEXITCODE -ne 0) {
        throw "winget failed to install $Id. Exit code: $LASTEXITCODE"
    }
}

if (-not (Get-Command winget.exe -ErrorAction SilentlyContinue)) {
    throw "winget.exe was not found on this runner."
}

# WEMI prerequisites
Install-WingetPackage -Id "voidtools.Everything"
Install-WingetPackage -Id "voidtools.Everything.Cli"
Install-WingetPackage -Id "Magicsplat.TclTk"

# winget aliases are normally placed here.
$wingetLinks = Join-Path $env:LOCALAPPDATA "Microsoft\WinGet\Links"
Add-ProcessAndGitHubPath -PathToAdd $wingetLinks

# Everything's normal installation location.
$everythingDir = "C:\Program Files\Everything"
Add-ProcessAndGitHubPath -PathToAdd $everythingDir

# Tcl/Tk commonly exposes tclsh.exe from this directory.
$tclBin = "C:\Program Files\Tcl\bin"
Add-ProcessAndGitHubPath -PathToAdd $tclBin

# Ensure Everything service is running before WEMI begins.
$service = Get-Service -Name "Everything" -ErrorAction Stop
if ($service.Status -ne "Running") {
    Start-Service -Name "Everything"
}

$deadline = (Get-Date).AddSeconds(30)
do {
    Start-Sleep -Seconds 1
    $service = Get-Service -Name "Everything"
} while ($service.Status -ne "Running" -and (Get-Date) -lt $deadline)

if ($service.Status -ne "Running") {
    throw "Everything service did not enter the Running state."
}

if (-not (Get-Command es.exe -ErrorAction SilentlyContinue)) {
    throw "es.exe was not found after Everything CLI installation."
}

if (-not (Get-Command tclsh.exe -ErrorAction SilentlyContinue)) {
    throw "tclsh.exe was not found after Tcl/Tk installation."
}

Write-Host "Everything service:"
Get-Service -Name "Everything"

Write-Host "Everything CLI:"
& es.exe -version

Write-Host "Tcl:"
echo 'puts [info patchlevel]' | tclsh.exe
