# SPDX-License-Identifier: MIT

[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$InstallPrefix
)

$ErrorActionPreference = "Stop"

. ".\.ci\common\modules-init.ps1" `
    -InstallPrefix $InstallPrefix

envmodule av

envmodule load intel/oneapi

envmodule av

throw "Pick the generated Intel module name and pass it in next."
