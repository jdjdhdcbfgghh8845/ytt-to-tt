import os
import sys
import subprocess
import json
import msvcrt

# Force UTF-8 for everything
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    os.system('chcp 65001 > nul')

# Enable ANSI colors
os.system("")

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
        
        print(f"\n{CYAN}(Arrows: Move, Enter: Select){RESET}")
        
        key = msvcrt.getch()
        if key == b'\r': return current
        elif key == b'\x00' or key == b'\xe0':
            key = msvcrt.getch()
            if key == b'H': current = (current - 1) % len(options)
            elif key == b'P': current = (current + 1) % len(options)

def run_setup():
    # Use escapes for Russian to avoid ANY encoding issues in the source file
    # "Русский" = \u0420\u0443\u0441\u0441\u043a\u0438\u0439
    options = ["English", "\u0420\u0443\u0441\u0441\u043a\u0438\u0439"]
    title = "SELECT LANGUAGE / \u0412\u042b\u0411\u0415\u0420\u0418\u0422\u0415 \u042f\u0417\u042b\u041a"
    
    lang_idx = show_menu(title, options)
    is_ru = (lang_idx == 1)
    
    # Translation map using escapes
    t = {
        'ffmpeg': "Checking FFmpeg..." if not is_ru else "\u041f\u0440\u043e\u0432\u0435\u0440\u043a\u0430 FFmpeg...",
        'deps': "Installing dependencies..." if not is_ru else "\u0423\u0441\u0442\u0430\u043d\u043e\u0432\u043a\u0430 \u0437\u0430\u0432\u0438\u0441\u0438\u043c\u043e\u0441\u0442\u0435\u0439...",
        'browser': "CHOOSE BROWSER" if not is_ru else "\u0412\u042b\u0411\u0415\u0420\u0418\u0422\u0415 \u0411\u0420\u0410\u0423\u0417\u0415\u0420",
        'finish': "FINISHING..." if not is_ru else "\u0417\u0410\u0412\u0415\u0420\u0428\u0415\u041d\u0418\u0415...",
    }

    print(f"\n{CYAN}[*] {t['ffmpeg']}{RESET}")
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    if os.path.exists("frontend"):
        print(f"    [*] npm install...")
        subprocess.run("npm install", cwd="frontend", shell=True)

    browser_idx = show_menu(t['browser'], ["Firefox", "Chrome"])
    choice = "1" if browser_idx == 0 else "2"
    
    print(f"\n{CYAN}[*] Playwright install...{RESET}")
    subprocess.run(["playwright", "install", "firefox" if choice == "1" else "chromium"], check=True)

    os.makedirs("frontend/src", exist_ok=True)
    with open("frontend/src/config.json", "w") as f:
        json.dump({"lang": "ru" if is_ru else "en"}, f)
        
    # Launch app
    print(f"\n{GREEN}{t['finish']}{RESET}")
    subprocess.run("run_all.bat", shell=True)

if __name__ == "__main__":
    run_setup()
