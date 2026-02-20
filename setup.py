import os
import subprocess
import sys
import shutil
import json

def run_command(command, description):
    print(f"\n[+] {description}...")
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"[-] Error: {description} failed.")
        return False
    return True

def setup_environment():
    print("====================================================")
    print("   YT ➜ TikTok Auto-uploader: Universal Setup       ")
    print("====================================================\n")

    # 1. Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        return

    # 2. Browser Selection
    print("\n[?] Which browser do you use for TikTok?")
    print("1) Firefox (Recommended)")
    print("2) Google Chrome")
    choice = input("Enter 1 or 2: ").strip()

    browser = "firefox" if choice == "1" else "chromium"
    channel = "" if choice == "1" else "chrome"

    # 3. Install Playwright browser
    install_cmd = f"playwright install {browser}"
    run_command(install_cmd, f"Installing {browser} for Playwright")

    # 4. Check/Install FFmpeg (simple check)
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True)
        print("[+] FFmpeg is already installed.")
    except FileNotFoundError:
        print("[!] FFmpeg not found! Please install it manually from https://ffmpeg.org/download.html")
        print("    Or ensure it's in your PATH.")

    # 5. Update uploader.py structure based on choice (dynamic profile detection)
    update_uploader_config(choice)

    # 6. Final Launch
    print("\n[!] Setup Complete!")
    print("[>] Starting the application...")
    subprocess.run("run_all.bat", shell=True)

def update_uploader_config(choice):
    uploader_path = "uploader.py"
    with open(uploader_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    app_data = os.environ.get('APPDATA', '')
    local_app_data = os.environ.get('LOCALAPPDATA', '')

    new_lines = []
    skip = False
    for line in lines:
        if "with sync_playwright() as p:" in line:
            new_lines.append(line)
            if choice == "1": # Firefox
                # Try to find default profile
                ff_path = os.path.join(app_data, 'Mozilla', 'Firefox', 'Profiles')
                profile = "default-release"
                if os.path.exists(ff_path):
                    dirs = [d for d in os.listdir(ff_path) if "default-release" in d]
                    if dirs: profile = dirs[0]
                
                new_lines.append(f"            app_data = os.environ['APPDATA']\n")
                new_lines.append(f"            user_data_dir = os.path.join(app_data, 'Mozilla', 'Firefox', 'Profiles', '{profile}')\n")
                new_lines.append(f"            browser = p.firefox.launch_persistent_context(user_data_dir, headless=False, no_viewport=True, args=['--allow-downgrade'])\n")
            else: # Chrome
                new_lines.append(f"            user_data_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data')\n")
                new_lines.append(f"            browser = p.chromium.launch_persistent_context(user_data_dir, channel='chrome', headless=False, no_viewport=True)\n")
            skip = True
            continue
        
        if skip and "page = browser.new_page()" in line:
            skip = False
        
        if not skip:
            new_lines.append(line)

    with open(uploader_path, "w", encoding="utf-8") as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    setup_environment()
