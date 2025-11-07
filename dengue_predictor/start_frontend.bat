@echo off
echo ========================================
echo DENGUE RISK PREDICTOR - FRONTEND STARTUP
echo ========================================
echo.
echo Starting server...
cd frontend
start python server.py
timeout /t 3 /nobreak >nul
echo Opening browser...
start http://localhost:8000
echo.
echo Server is running at http://localhost:8000
echo Press Ctrl+C in the server window to stop
pause