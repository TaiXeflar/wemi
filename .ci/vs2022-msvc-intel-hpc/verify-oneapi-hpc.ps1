# SPDX-License-Identifier: MIT

$ErrorActionPreference = "Stop"

$oneapiRoot = "C:\Program Files (x86)\Intel\oneAPI"

if (-not (Test-Path $oneapiRoot)) {
    throw "Intel oneAPI root was not found: $oneapiRoot"
}

Get-ChildItem $oneapiRoot

Write-Host "Searching for icx.exe / ifx.exe..."
Get-ChildItem $oneapiRoot -Recurse -Filter icx.exe -ErrorAction SilentlyContinue |
    Select-Object -First 10 FullName

Get-ChildItem $oneapiRoot -Recurse -Filter ifx.exe -ErrorAction SilentlyContinue |
    Select-Object -First 10 FullName
