
# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

$EsPath = (
    Get-Command `
        es.exe `
        -CommandType Application `
        -ErrorAction Stop
).Source

Write-Host "ES executable: $EsPath"

& $EsPath -version
Write-Host "ES version exit code: $LASTEXITCODE"

& $EsPath -get-everything-version
Write-Host "Everything version exit code: $LASTEXITCODE"

Write-Host "Testing a known existing file..."
& $EsPath "Everything.exe"
Write-Host "Existing search exit code: $LASTEXITCODE"

Write-Host "Testing an impossible file..."
& $EsPath "__WEMI_FILE_THAT_MUST_NOT_EXIST_7A8F29E1__"
Write-Host "Missing search exit code: $LASTEXITCODE"

Write-Host "Testing an impossible file with no-result-error..."
& $EsPath `
    -no-result-error `
    "__WEMI_FILE_THAT_MUST_NOT_EXIST_7A8F29E1__"

Write-Host (
    "Missing search with -no-result-error exit code: " +
    $LASTEXITCODE
)
