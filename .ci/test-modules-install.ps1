# SPDX-License-Identifier: MIT
# Copyright (c) 2026 WEMI Contributors

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$InstallPath
)

$ErrorActionPreference = "Stop"

$installRoot = (Resolve-Path -Path $InstallPath).Path
$testDir = Join-Path $installRoot "test"

$requiredFiles = @(
    "bin\module.cmd",
    "bin\ml.cmd",
    "bin\envml.cmd",
    "init\cmd.cmd",
    "init\pwsh.ps1",
    "libexec\modulecmd.tcl",
    "modulefiles\null",
    "test\TESTINSTALL.bat",
    "test\TESTINSTALL_PWSH.ps1"
)

foreach ($relativePath in $requiredFiles) {
    $fullPath = Join-Path $installRoot $relativePath

    if (-not (Test-Path -LiteralPath $fullPath -PathType Leaf)) {
        throw "Missing installed Modules file: $relativePath"
    }
}

$officialTest = Join-Path $testDir "TESTINSTALL_PWSH.ps1"

Push-Location $testDir
try {
    Write-Host "Testing installed Modules prefix: $installRoot"
    Write-Host "Using Windows PowerShell:"
    & powershell.exe -NoLogo -NoProfile -Command '$PSVersionTable.PSVersion.ToString()'

    # 新行程避免 MODULES_CMD / MODULESHOME / MODULEPATH 汙染。
    & powershell.exe `
        -NoLogo `
        -NoProfile `
        -NonInteractive `
        -ExecutionPolicy Bypass `
        -File $officialTest `
        -installpath $installRoot

    if ($LASTEXITCODE -ne 0) {
        throw "TESTINSTALL_PWSH.ps1 failed. Exit code: $LASTEXITCODE"
    }
}
finally {
    Pop-Location
}
