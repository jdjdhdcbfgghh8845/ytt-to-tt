@echo off
echo Starting YouTube to TikTok Auto-uploader...

:: Start Backend
start cmd /k "python main.py"

:: Start Frontend
cd frontend
start cmd /k "npm run dev"

echo App started! 
echo Frontend: http://localhost:5173
echo Backend:  http://localhost:8000
echo.
echo IMPORTANT: Close Google Chrome before starting the upload process!
pause
