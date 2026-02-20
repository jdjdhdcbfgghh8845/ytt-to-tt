# YT -> TikTok: REMOTE BOOTSTRAP
# Run this via: iwr -useb https://raw.githubusercontent.com/jdjdhdcbfgghh8845/ytt-to-tt/main/bootstrap.ps1 | iex

$ErrorActionPreference = "Stop"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$repoUrl = "https://github.com/jdjdhdcbfgghh8845/ytt-to-tt.git"
$destDir = "ytt-to-tt"

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "   YT -> TikTok: REMOTE SETUP                       " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

if (Test-Path $destDir) {
    Write-Host "[*] Updating repository..." -ForegroundColor Cyan
    cd $destDir
    git pull
}
else {
    Write-Host "[*] Cloning repository..." -ForegroundColor Cyan
    git clone $repoUrl $destDir
    cd $destDir
}

Write-Host "[*] Starting Python Installer..." -ForegroundColor Green
python setup.py
