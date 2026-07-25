
# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

# ES may temporarily return a non-zero code while Everything is starting.
$PSNativeCommandUseErrorActionPreference = $false

$EverythingCommand = Get-Command `
    "Everything.exe" `
    -CommandType Application `
    -ErrorAction SilentlyContinue

if ($null -ne $EverythingCommand) {
    $EverythingPath = $EverythingCommand.Source
}
else {
    $EverythingCandidates = @(
        (Join-Path $env:ProgramFiles "Everything\Everything.exe"),
        (
            if (${env:ProgramFiles(x86)}) {
                Join-Path `
                    ${env:ProgramFiles(x86)} `
                    "Everything\Everything.exe"
            }
        ),
        (
            Join-Path `
                $env:LOCALAPPDATA `
                "Everything\Everything.exe"
        )
    )

    $EverythingPath = $EverythingCandidates |
        Where-Object {
            $_ -and (
                Test-Path `
                    -LiteralPath $_ `
                    -PathType Leaf
            )
        } |
        Select-Object -First 1
}

if (-not $EverythingPath) {
    throw "Everything.exe was not found."
}

$EsCommand = Get-Command `
    "es.exe" `
    -CommandType Application `
    -ErrorAction SilentlyContinue

if ($null -ne $EsCommand) {
    $EsPath = $EsCommand.Source
}
else {
    $WinGetPackagesRoot = Join-Path `
        $env:LOCALAPPDATA `
        "Microsoft\WinGet\Packages"

    $EsFile = Get-ChildItem `
        -LiteralPath $WinGetPackagesRoot `
        -Filter "es.exe" `
        -File `
        -Recurse `
        -ErrorAction SilentlyContinue |
        Where-Object {
            $_.FullName -like `
                "*voidtools.Everything.Cli_*"
        } |
        Select-Object -First 1

    if ($null -ne $EsFile) {
        $EsPath = $EsFile.FullName
    }
}

if (-not $EsPath) {
    throw "es.exe was not found."
}

Write-Host "Everything executable: $EverythingPath"
Write-Host "ES executable:         $EsPath"

# Avoid starting another user-session client if one already exists.
$CurrentSessionId = (Get-Process -Id $PID).SessionId

$EverythingClient = Get-Process `
    "Everything" `
    -ErrorAction SilentlyContinue |
    Where-Object {
        $_.SessionId -eq $CurrentSessionId
    } |
    Select-Object -First 1

if ($null -eq $EverythingClient) {
    Write-Host "Starting Everything search client..."

    Start-Process `
        -FilePath $EverythingPath `
        -ArgumentList "-startup" `
        -WindowStyle Hidden
}
else {
    Write-Host (
        "Everything search client is already running " +
        "in session $CurrentSessionId."
    )
}

$Ready = $false
$LastProbeExitCode = $null

for ($Attempt = 1; $Attempt -le 30; $Attempt++) {
    $VersionOutput = & $EsPath `
        -get-everything-version `
        2>&1

    $LastProbeExitCode = $LASTEXITCODE

    if ($LastProbeExitCode -eq 0) {
        $Ready = $true

        Write-Host (
            "Everything IPC is ready: " +
            ($VersionOutput -join " ")
        )

        break
    }

    Write-Host (
        "Waiting for Everything IPC, " +
        "attempt $Attempt, " +
        "exit code $LastProbeExitCode"
    )

    Start-Sleep -Milliseconds 500
}

if (-not $Ready) {
    Get-Process `
        "Everything" `
        -ErrorAction SilentlyContinue |
        Format-Table `
            Id, `
            SessionId, `
            Path

    throw (
        "Everything IPC did not become ready. " +
        "Last ES exit code: $LastProbeExitCode"
    )
}
