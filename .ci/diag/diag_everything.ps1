


$EverythingCommand = Get-Command `
Everything.exe `
-CommandType Application `
-ErrorAction SilentlyContinue

if ($null -eq $EverythingCommand) {
    $Candidates = @(
        "$env:ProgramFiles\Everything\Everything.exe",
        "${env:ProgramFiles(x86)}\Everything\Everything.exe",
        "$env:LOCALAPPDATA\Everything\Everything.exe"
    )

    $EverythingPath = $Candidates |
        Where-Object {
        $_ -and (
            Test-Path `
            -LiteralPath $_ `
            -PathType Leaf
        )
        } |
        Select-Object -First 1
} else {
    $EverythingPath = $EverythingCommand.Source
}

if (-not $EverythingPath) {
    throw "Everything.exe was not found."
}

$EsPath = (
Get-Command `
    es.exe `
    -CommandType Application `
    -ErrorAction Stop
).Source

Write-Host "Everything: $EverythingPath"
Write-Host "ES: $EsPath"

Start-Process `
-FilePath $EverythingPath `
-ArgumentList "-startup" `
-WindowStyle Hidden

$Ready = $false

for ($Attempt = 1; $Attempt -le 20; $Attempt++) {
& $EsPath `
    -timeout 1000 `
    -get-everything-version

if ($LASTEXITCODE -eq 0) {
    $Ready = $true
    break
}

Write-Host (
    "Waiting for Everything IPC, " +
    "attempt $Attempt, exit code $LASTEXITCODE"
)

Start-Sleep -Milliseconds 500
}

Get-Process Everything `
-ErrorAction SilentlyContinue |
Format-Table `
    Id, `
    SessionId, `
    Path

if (-not $Ready) {
throw (
    "Everything IPC did not become ready. " +
    "Last ES exit code: $LASTEXITCODE"
)
}
