import os
import sys
import subprocess
import shutil
import json
import msvcrt
import requests
import zipfile

# Force UTF-8 for everything
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    os.system('chcp 65001 > nul')

# Enable ANSI colors for Windows console
os.system("")

# Constants for colors
BLUE = "\033[94m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

def show_menu(title, options):
    current = 0
    while True:
        os.system('cls')
        print(f"{CYAN}===================================================={RESET}")
        print(f"{CYAN}   YT -> TikTok: {BOLD}{title}{RESET}")
        print(f"{CYAN}===================================================={RESET}\n")
        
        for i, option in enumerate(options):
            if i == current:
                print(f"  {BLUE}> {BOLD}{option}{RESET}")
            else:
                print(f"    {option}")
        
        print(f"\n{CYAN}(Use arrows to navigate, Enter to select){RESET}")
        
        key = msvcrt.getch()
        if key == b'\r': # Enter key
            return current
        elif key == b'\x00' or key == b'\xe0': # Arrow key prefix
            key = msvcrt.getch()
            if key == b'H': # Up
                current = (current - 1) % len(options)
            elif key == b'P': # Down
                current = (current + 1) % len(options)

def run_setup():
    # 1. Select Language
    lang_idx = show_menu("SELECT LANGUAGE / ВЫБЕРИТЕ ЯЗЫК", ["English", "Русский"])
    is_ru = (lang_idx == 1)
    
    t = {
        'ffmpeg_check': "Checking for FFmpeg..." if not is_ru else "Проверка FFmpeg...",
        'ffmpeg_download': "Downloading FFmpeg (this can take a minute)..." if not is_ru else "Загрузка FFmpeg (это может занять минуту)...",
        'deps_install': "Installing core dependencies..." if not is_ru else "Установка основных зависимостей...",
        'browser_select': "SELECT YOUR PRIMARY BROWSER" if not is_ru else "ВЫБЕРИТЕ ВАШ ОСНОВНОЙ БРАУЗЕР",
        'setup_complete': "SETUP COMPLETE! LAUNCHING..." if not is_ru else "УСТАНОВКА ЗАВЕРШЕНА! ЗАПУСК...",
        'browser_setup': "Setting up {} for automation..." if not is_ru else "Настройка {} для автоматизации...",
    }

    print(f"\n{CYAN}[*] {t['ffmpeg_check']}{RESET}", end=" ", flush=True)
    
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True)
        print(f"{GREEN}OK{RESET}")
    except:
        print(f"{YELLOW}NOT FOUND{RESET}")
        print(f"{CYAN}[>] {t['ffmpeg_download']}{RESET}")
        ffmpeg_url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
        zip_path = os.path.join(os.environ['TEMP'], "ffmpeg_setup.zip")
        dest_folder = os.path.join(os.environ['USERPROFILE'], "ffmpeg")
        
        if not os.path.exists(dest_folder): os.makedirs(dest_folder)
        
        r = requests.get(ffmpeg_url, stream=True)
        with open(zip_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): f.write(chunk)
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref: zip_ref.extractall(dest_folder)
            
        for root, dirs, files in os.walk(dest_folder):
            if "bin" in dirs:
                bin_path = os.path.join(root, "bin")
                os.environ["PATH"] += os.pathsep + bin_path
                subprocess.run(f'powershell -Command "[Environment]::SetEnvironmentVariable(\'Path\', [Environment]::GetEnvironmentVariable(\'Path\', \'User\') + \';{bin_path}\', \'User\')"', shell=True)
                break
        print(f"{GREEN}[+] FFmpeg installed!{RESET}")

    print(f"\n{CYAN}[*] {t['deps_install']}{RESET}")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    if os.path.exists("frontend"):
        print(f"    [*] Installing Frontend dependencies (NPM)...")
        subprocess.run("npm install", cwd="frontend", shell=True)

    browser_idx = show_menu(t['browser_select'], ["Firefox (Recommended/Рекомендуется)", "Google Chrome"])
    choice = "1" if browser_idx == 0 else "2"
    browser_type = "firefox" if browser_idx == 0 else "chromium"
    
    print(f"\n{CYAN}[*] {t['browser_setup'].format(browser_type)}{RESET}")
    subprocess.run(["playwright", "install", browser_type], check=True)

    with open(os.path.join("frontend", "src", "config.json"), "w") as f:
        json.dump({"lang": "ru" if is_ru else "en"}, f)
        
    update_uploader_config(choice)

    print(f"\n{GREEN}===================================================={RESET}")
    print(f"{GREEN}   {t['setup_complete']}         {RESET}")
    print(f"{GREEN}===================================================={RESET}\n")
    subprocess.run("run_all.bat", shell=True)

def update_uploader_config(choice):
    uploader_path = "uploader.py"
    if not os.path.exists(uploader_path): return
    with open(uploader_path, "r", encoding="utf-8") as f: lines = f.readlines()
    app_data = os.environ.get('APPDATA', '')
    new_lines = []
    skip = False
    for line in lines:
        if "with sync_playwright() as p:" in line:
            new_lines.append(line)
            if choice == "1":
                ff_path = os.path.join(app_data, 'Mozilla', 'Firefox', 'Profiles')
                profile = "default-release"
                if os.path.exists(ff_path):
                    dirs = [d for d in os.listdir(ff_path) if "default-release" in d]
                    if dirs: profile = dirs[0]
                new_lines.append(f"            app_data = os.environ['APPDATA']\n")
                new_lines.append(f"            user_data_dir = os.path.join(app_data, 'Mozilla', 'Firefox', 'Profiles', '{profile}')\n")
                new_lines.append(f"            browser = p.firefox.launch_persistent_context(user_data_dir, headless=False, no_viewport=True, args=['--allow-downgrade'])\n")
            else:
                new_lines.append(f"            user_data_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data')\n")
                new_lines.append(f"            browser = p.chromium.launch_persistent_context(user_data_dir, channel='chrome', headless=False, no_viewport=True)\n")
            skip = True
            continue
        if skip and "page = browser.new_page()" in line: skip = False
        if not skip: new_lines.append(line)
    with open(uploader_path, "w", encoding="utf-8") as f: f.writelines(new_lines)

if __name__ == "__main__":
    try:
        run_setup()
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Setup cancelled by user.{RESET}")
