# SPDX-License-Identifier: MIT

$ErrorActionPreference = "Stop"

winget install `
    --id Intel.OneAPI.HPCToolkit `
    --exact `
    --source winget `
    --silent `
    --disable-interactivity `
    --accept-package-agreements `
    --accept-source-agreements

if ($LASTEXITCODE -ne 0) {
    throw "Failed to install Intel.OneAPI.HPCToolkit. Exit code: $LASTEXITCODE"
}
