@echo off
REM Simple batch script to build the executable
echo Building Dengue Risk Predictor Executable...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install PyInstaller if not installed
echo Checking for PyInstaller...
python -m pip install pyinstaller --quiet

REM Run the build script
echo.
echo Starting build process...
echo This may take several minutes...
echo.
python build_exe.py

echo.
echo Build complete!
echo Check the 'dist' folder for DengueRiskPredictor.exe
echo.
pause


