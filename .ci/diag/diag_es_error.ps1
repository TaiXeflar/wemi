# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

$ErrorActionPreference = "Stop"

$EsPath = (
    Get-Command `
        es.exe `
        -CommandType Application `
        -ErrorAction Stop
).Source

$EverythingCommand = Get-Command `
    Everything.exe `
    -CommandType Application `
    -ErrorAction SilentlyContinue

if ($null -ne $EverythingCommand) {
    $EverythingPath = $EverythingCommand.Source
}
else {
    $EverythingPath = @(
        "$env:ProgramFiles\Everything\Everything.exe",
        "${env:ProgramFiles(x86)}\Everything\Everything.exe"
    ) |
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

Write-Host "Everything executable: $EverythingPath"
Write-Host "ES executable:         $EsPath"

& $EsPath -version

if ($LASTEXITCODE -ne 0) {
    throw "es.exe could not be executed."
}

Write-Host "Starting Everything search client..."

Start-Process `
    -FilePath $EverythingPath `
    -ArgumentList @(
        "-startup"
    ) `
    -WindowStyle Hidden

$Ready = $false

for ($Attempt = 1; $Attempt -le 30; $Attempt++) {
    $VersionOutput = & $EsPath `
        -get-everything-version `
        2>&1

    if ($LASTEXITCODE -eq 0) {
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
        "exit code $LASTEXITCODE"
    )

    Start-Sleep -Milliseconds 500
}

Get-Process `
    Everything `
    -ErrorAction SilentlyContinue |
    Format-Table `
        Id, `
        SessionId, `
        Path

if (-not $Ready) {
    throw (
        "Everything IPC did not become ready after " +
        "30 attempts."
    )
}

Write-Host "Testing a known existing file..."

$ExistingOutput = & $EsPath "Everything.exe"
$ExistingExitCode = $LASTEXITCODE

Write-Host (
    "Existing search exit code: " +
    $ExistingExitCode
)

$ExistingOutput |
    Select-Object -First 10 |
    ForEach-Object {
        Write-Host "  $_"
    }

Write-Host "Testing an impossible file..."

$MissingOutput = & $EsPath `
    "__WEMI_FILE_THAT_MUST_NOT_EXIST_7A8F29E1__"

$MissingExitCode = $LASTEXITCODE

Write-Host (
    "Missing search exit code: " +
    $MissingExitCode
)

Write-Host "Testing an impossible file with -no-result-error..."

& $EsPath `
    -no-result-error `
    "__WEMI_FILE_THAT_MUST_NOT_EXIST_7A8F29E1__"

Write-Host (
    "Missing search with -no-result-error exit code: " +
    $LASTEXITCODE
)
