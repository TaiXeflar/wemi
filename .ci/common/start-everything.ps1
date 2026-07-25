
# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $false

$EverythingPath = (
    Get-Command `
        Everything.exe `
        -CommandType Application `
        -ErrorAction Stop
).Source

$EsPath = (
    Get-Command `
        es.exe `
        -CommandType Application `
        -ErrorAction Stop
).Source

Write-Host "Everything executable: $EverythingPath"
Write-Host "ES executable:         $EsPath"

Start-Process `
    -FilePath $EverythingPath `
    -ArgumentList "-startup" `
    -WindowStyle Hidden

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
        Everything `
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
