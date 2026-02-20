# 🚀 YouTube Shorts ➜ TikTok Auto-Reposter

A professional, fully automated tool to repurpose YouTube Shorts for TikTok with advanced anti-copyright measures and a premium dashboard.

![UI Design](https://img.shields.io/badge/UI-Premium_Glassmorphism-blueviolet)
![Automation](https://img.shields.io/badge/Automation-Playwright-green)
![Processing](https://img.shields.io/badge/Processing-FFmpeg-orange)

## ✨ Key Features

- **Automated Download**: One-click download of YouTube Shorts in high quality.
- **Smart Metadata**: Automatically extracts titles, descriptions, and hashtags.
- **🛡️ Anti-Copyright Suite**: 
    - Automatic zooming/cropping.
    - Color and brightness adjustments.
    - Frequency-based audio/video speed variance (1.02x).
- **Session Integration**: Works with your existing Firefox or Chrome browser profiles—no password typing needed.
- **Premium Dashboard**: Sleek React-based UI with real-time status updates and status tracking.
- **Professional Installer**: Completely automated environment setup via PowerShell.

## 🛠️ Quick Start

### 1. Requirements
- **Windows OS**
- **Python 3.10+**
- **Node.js** (for the dashboard)

### 2. Installation & Run
Simply run the bootstrap script:
```cmd
START_HERE.bat
```
The script will:
1. Automatically download and configure **FFmpeg**.
2. Install all Python and Node.js dependencies.
3. Set up the automated browser engines.
4. Launch both the backend and frontend.

## 📖 How to Use

1. **Close your main browser** (Firefox or Chrome) before starting the upload process to allow the script to access your session.
2. Paste the **YouTube Short URL** into the dashboard.
3. Click **Start Automation**.
4. The tool will:
    - Download the video.
    - Apply anti-copyright filters.
    - Open TikTok Studio.
    - Upload the video, fill in the caption/hashtags.
    - Wait for TikTok's internal checks to pass.
    - **Automatically Publish** the video.

## ⚙️ Project Structure

- `main.py`: FastAPI server for job orchestration.
- `uploader.py`: Playwright-based TikTok automation.
- `downloader.py`: `yt-dlp` integration for YouTube.
- `processor.py`: FFmpeg video transformation logic.
- `frontend/`: React + Vite + TypeScript dashboard.
- `install.ps1`: Professional PowerShell bootstrap script.

## ⚠️ Disclaimer
This tool is for educational purposes. Use it responsibly and respect the terms of service of both YouTube and TikTok.
