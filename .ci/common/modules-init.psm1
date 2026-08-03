
# SPDX-License-Identifier: MIT
# Copyright (c) 2026-${year} WEMI Contributors
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT


function init-modules {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)]
        [string]$InstallPrefix
    )

    $ErrorActionPreference = "Stop"

    $installRoot = (Resolve-Path -LiteralPath $InstallPrefix).Path

    $tclsh = Get-Command tclsh.exe -ErrorAction Stop
    $tclBin = Split-Path -Path $tclsh.Source -Parent

    $env:Path = "$installRoot\bin;$tclBin;$env:Path"

    Remove-Item Env:MODULES_CMD -ErrorAction SilentlyContinue
    Remove-Item Env:MODULESHOME -ErrorAction SilentlyContinue
    Remove-Item Env:MODULEPATH -ErrorAction SilentlyContinue
    Remove-Item Env:LOADEDMODULES -ErrorAction SilentlyContinue

    . "$installRoot\init\pwsh.ps1"
}

Export-ModuleMember -Function init-modules
