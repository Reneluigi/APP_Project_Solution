# Sync local changes to Git remote (add, commit if needed, push).
# Usage:
#   .\git-sync.ps1
#   .\git-sync.ps1 "Your commit message"

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Test-Path -Path ".git" -PathType Container)) {
    Write-Error "Not a git repository. Run this script from the project root."
    exit 1
}

$message = ($args -join " ").Trim()
if ([string]::IsNullOrWhiteSpace($message)) {
    $message = "Update $(Get-Date -Format 'yyyy-MM-dd HHmm')"
}

git add -A

git diff --cached --quiet 2>$null
$hasStagedChanges = $LASTEXITCODE -eq 1

if ($hasStagedChanges) {
    git commit -m $message
    if ($LASTEXITCODE -ne 0) {
        exit $LASTEXITCODE
    }
} else {
    Write-Host "Nothing to commit (working tree clean after staging)."
}

git push
if ($LASTEXITCODE -ne 0) {
    exit $LASTEXITCODE
}

Write-Host "Done: remote is up to date."
