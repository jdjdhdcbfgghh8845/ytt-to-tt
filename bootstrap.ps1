# YT ➜ TikTok Auto-uploader: REMOTE BOOTSTRAP
# Run this via: iwr -useb https://raw.githubusercontent.com/jdjdhdcbfgghh8845/ytt-to-tt/main/bootstrap.ps1 | iex

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$repoUrl = "https://github.com/jdjdhdcbfgghh8845/ytt-to-tt.git"
$destDir = "ytt-to-tt"

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "   YT -> TikTok: STARTING REMOTE INSTALLATION        " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

# 1. Check for Git
if (!(Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "[!] Git is not installed! Please install Git from https://git-scm.com/" -ForegroundColor Red
    return
}

# 2. Clone the repository
if (Test-Path $destDir) {
    Write-Host "[*] Directory $destDir already exists. Updating..." -ForegroundColor Cyan
    Set-Location $destDir
    git pull
}
else {
    Write-Host "[*] Cloning repository..." -ForegroundColor Cyan
    git clone $repoUrl $destDir
    Set-Location $destDir
}

# 3. Run the pro installer (New Python Setup)
Write-Host "[*] Launching Internal Installer..." -ForegroundColor Green
python setup.py
