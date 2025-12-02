@echo off
echo ============================================================
echo    Dengue Risk Prediction System - Simplified Version
echo ============================================================
echo.

REM Check if .env file exists
if not exist .env (
    echo [!] Creating .env file from template...
    copy .env.example .env
    echo.
    echo [!] WARNING: You need to add your Google Gemini API key to .env file
    echo [!] Get it from: https://aistudio.google.com/app/apikey
    echo.
    echo Press any key to open .env file in notepad...
    pause >nul
    notepad .env
    echo.
)

REM Check if dependencies are installed
echo [*] Checking dependencies...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo [!] Installing dependencies...
    pip install -r requirements.txt
    echo.
)

echo [*] Starting server...
echo [*] Access the application at: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

python app.py
