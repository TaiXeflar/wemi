# SPDX-License-Identifier: MIT
# Copyright (c) 2026 WEMI Contributors

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$InstallPrefix
)

$ErrorActionPreference = "Stop"

$installRoot = (Resolve-Path -LiteralPath $InstallPrefix).Path
$testDirectory = Join-Path $installRoot "test"

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
        throw "Missing installed file: $relativePath"
    }

    Write-Host "Found: $relativePath"
}

$tclsh = Get-Command tclsh.exe -ErrorAction Stop
$tclBin = Split-Path -Path $tclsh.Source -Parent

# 確保 CMD 和 pwsh 都優先使用這次 WEMI 安裝的 Modules。
$env:Path = "$installRoot\bin;$tclBin;$env:Path"

# 避免本機已有 Modules 初始化時污染測試。
Remove-Item Env:MODULES_CMD -ErrorAction SilentlyContinue
Remove-Item Env:MODULESHOME -ErrorAction SilentlyContinue
Remove-Item Env:MODULEPATH -ErrorAction SilentlyContinue
Remove-Item Env:LOADEDMODULES -ErrorAction SilentlyContinue

Write-Host "Testing CMD shell environment..."

& cmd.exe /d /c "cd /d ""$testDirectory"" && call TESTINSTALL.bat ""$installRoot"""

if ($LASTEXITCODE -ne 0) {
    throw "TESTINSTALL.bat failed. Exit code: $LASTEXITCODE"
}

Write-Host "Testing PowerShell 7 environment..."

Push-Location $testDirectory
try {
    & pwsh.exe `
        -NoLogo `
        -NoProfile `
        -NonInteractive `
        -ExecutionPolicy Bypass `
        -File ".\TESTINSTALL_PWSH.ps1" `
        -installpath $installRoot

    if ($LASTEXITCODE -ne 0) {
        throw "TESTINSTALL_PWSH.ps1 failed. Exit code: $LASTEXITCODE"
    }
}
finally {
    Pop-Location
}
