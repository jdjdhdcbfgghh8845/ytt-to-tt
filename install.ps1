# YT ➜ TikTok Auto-uploader: ULTIMATE BOOTSTRAP
$ErrorActionPreference = "Stop"

# Force UTF-8 Encoding for Russian characters
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::InputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

function Show-Menu {
    param (
        [string]$Title,
        [string[]]$Options,
        [int]$SelectedIndex = 0
    )

    $startLine = [Console]::CursorTop
    $current = $SelectedIndex

    # Hide cursor for cleaner look
    $oldCursorSize = $Host.UI.RawUI.CursorSize
    $Host.UI.RawUI.CursorSize = 0

    try {
        while ($true) {
            [Console]::SetCursorPosition(0, $startLine)
            Write-Host "--- $Title ---`n" -ForegroundColor Cyan
            
            for ($i = 0; $i -lt $Options.Count; $i++) {
                if ($i -eq $current) {
                    Write-Host "  > $($Options[$i])  " -ForegroundColor White -BackgroundColor Blue
                }
                else {
                    Write-Host "    $($Options[$i])  " -ForegroundColor Gray
                }
            }

            if ([Console]::KeyAvailable) {
                $key = [Console]::ReadKey($true)
                if ($key.Key -eq "UpArrow") { $current = if ($current -gt 0) { $current - 1 } else { $Options.Count - 1 } }
                elseif ($key.Key -eq "DownArrow") { $current = if ($current -lt $Options.Count - 1) { $current + 1 } else { 0 } }
                elseif ($key.Key -eq "Enter") { return $current }
            }
            Start-Sleep -Milliseconds 50
        }
    }
    finally {
        $Host.UI.RawUI.CursorSize = $oldCursorSize
        Write-Host ""
    }
}

Clear-Host
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host "   YT ➜ TikTok: WORLD CLASS INSTALLER v2.0         " -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
Write-Host ""

# 1. Select Language
$langIdx = Show-Menu -Title "SELECT LANGUAGE / ВЫБЕРИТЕ ЯЗЫК" -Options @("English", "Русский")
$isRussian = ($langIdx -eq 1)

$msgFFmpeg = if ($isRussian) { "[*] Проверка FFmpeg..." } else { "[*] Checking for FFmpeg..." }
$msgDownload = if ($isRussian) { "[>] Автоматическая загрузка FFmpeg..." } else { "[>] Automatically downloading FFmpeg..." }
$msgDeps = if ($isRussian) { "[*] Установка зависимостей Python..." } else { "[*] Installing Python dependencies..." }
$msgBrowser = if ($isRussian) { "ВЫШ ОСНОВНОЙ БРАУЗЕР" } else { "YOUR PRIMARY BROWSER" }
$msgFinish = if ($isRussian) { "УСТАНОВКА ЗАВЕРШЕНА! ЗАПУСК..." } else { "SETUP COMPLETE! LAUNCHING..." }

Write-Host "`n$msgFFmpeg" -NoNewline
try {
    ffmpeg -version | Out-Null
    Write-Host " OK" -ForegroundColor Green
}
catch {
    Write-Host " NOT FOUND" -ForegroundColor Yellow
    Write-Host $msgDownload -ForegroundColor Cyan
    
    $ffmpegUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    $zipPath = "$env:TEMP\ffmpeg.zip"
    $destFolder = "$env:USERPROFILE\ffmpeg"
    
    if (-not (Test-Path $destFolder)) { New-Item -ItemType Directory -Path $destFolder | Out-Null }
    Invoke-WebRequest -Uri $ffmpegUrl -OutFile $zipPath
    Expand-Archive -Path $zipPath -DestinationPath $destFolder -Force
    $binPath = Get-ChildItem -Path $destFolder -Filter "bin" -Recurse | Select-Object -First 1
    if ($binPath) {
        $fullBinPath = $binPath.FullName
        $env:PATH += ";$fullBinPath"
        [Environment]::SetEnvironmentVariable("Path", $env:Path + ";$fullBinPath", "User")
    }
}

Write-Host "`n$msgDeps" -ForegroundColor Cyan
pip install -r requirements.txt | Out-Default

Write-Host "    [*] Installing Frontend dependencies (NPM)..." -ForegroundColor Cyan
Set-Location frontend
npm install | Out-Default
Set-Location ..

$browserIdx = Show-Menu -Title $msgBrowser -Options @("Firefox (Recommended/Рекомендуется)", "Google Chrome")
$choice = if ($browserIdx -eq 0) { "1" } else { "2" }
$browser = if ($browserIdx -eq 0) { "firefox" } else { "chromium" }

Write-Host "`n[*] Setting up $browser..." -ForegroundColor Cyan
playwright install $browser | Out-Default

# 4. Save config & update uploader
python -c "
import os, json
choice = '$choice'
is_ru = $isRussian
# Update language for frontend
with open('frontend/src/config.json', 'w') as f:
    json.dump({'lang': 'ru' if is_ru else 'en'}, f)

# Update uploader profile logic
uploader_path = 'uploader.py'
with open(uploader_path, 'r', encoding='utf-8') as f: lines = f.readlines()
app_data = os.environ.get('APPDATA', '')
new_lines = []
skip = False
for line in lines:
    if 'with sync_playwright() as p:' in line:
        new_lines.append(line)
        if choice == '1':
            ff_path = os.path.join(app_data, 'Mozilla', 'Firefox', 'Profiles')
            profile = 'default-release'
            if os.path.exists(ff_path):
                dirs = [d for d in os.listdir(ff_path) if 'default-release' in d]
                if dirs: profile = dirs[0]
            new_lines.append(f'            app_data = os.environ[\'APPDATA\']\n')
            new_lines.append(f'            user_data_dir = os.path.join(app_data, \'Mozilla\', \'Firefox\', \'Profiles\', \'{profile}\')\n')
            new_lines.append(f'            browser = p.firefox.launch_persistent_context(user_data_dir, headless=False, no_viewport=True, args=[\'--allow-downgrade\'])\n')
        else:
            new_lines.append(f'            user_data_dir = os.path.join(os.environ[\'LOCALAPPDATA\'], \'Google\', \'Chrome\', \'User Data\')\n')
            new_lines.append(f'            browser = p.chromium.launch_persistent_context(user_data_dir, channel=\'chrome\', headless=False, no_viewport=True)\n')
        skip = True
        continue
    if skip and 'page = browser.new_page()' in line: skip = False
    if not skip: new_lines.append(line)
with open(uploader_path, 'w', encoding='utf-8') as f: f.writelines(new_lines)
"

Write-Host ""
Write-Host "====================================================" -ForegroundColor Green
Write-Host "   $msgFinish         " -ForegroundColor Green
Write-Host "====================================================" -ForegroundColor Green
Write-Host ""

cmd /c "run_all.bat"
