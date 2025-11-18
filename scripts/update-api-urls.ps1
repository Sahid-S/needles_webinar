# Update API URLs Script
# Run this script to switch between development and production API endpoints

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('dev', 'prod')]
    [string]$Environment
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$registerFile = Join-Path (Split-Path -Parent $scriptDir) "frontend\register.html"

if ($Environment -eq 'dev') {
    $newUrl = 'http://localhost:3000'
    Write-Host "Switching to DEVELOPMENT environment..." -ForegroundColor Yellow
} else {
    $prodUrl = Read-Host "Enter your production backend URL (e.g., https://webinar-backend.onrender.com)"
    $newUrl = $prodUrl
    Write-Host "Switching to PRODUCTION environment..." -ForegroundColor Yellow
}

# Backup the file
Copy-Item $registerFile "$registerFile.backup"
Write-Host "Created backup: $registerFile.backup" -ForegroundColor Green

# Read the file
$content = Get-Content $registerFile -Raw

# Replace all API endpoints
$patterns = @(
    'http://localhost:3000',
    'https://[^''"]+-[^''"]+\.onrender\.com'
)

foreach ($pattern in $patterns) {
    $content = $content -replace $pattern, $newUrl
}

# Save the file
$content | Set-Content $registerFile

Write-Host "`nUpdated API endpoints to: $newUrl" -ForegroundColor Green
Write-Host "File updated: $registerFile" -ForegroundColor Green
Write-Host "`nTo revert changes, restore from: $registerFile.backup" -ForegroundColor Cyan
