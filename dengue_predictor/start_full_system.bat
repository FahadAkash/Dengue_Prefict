@echo off
echo ========================================
echo DENGUE RISK PREDICTOR - COMPLETE SYSTEM
echo ========================================
echo.

echo Starting complete system...
echo Ports configuration:
echo   - Frontend server: http://localhost:8000
echo   - Backend API: http://localhost:8001
echo.

echo Starting backend API server...
start "Backend API" /D "api" cmd /c "python -m uvicorn BaseAPI:app --host localhost --port 8001"

echo Starting frontend server...
start "Frontend" /D "frontend" cmd /c "python server.py"

timeout /t 5 /nobreak >nul
echo Opening browser...
start http://localhost:8000

echo.
echo ========================================
echo SYSTEM IS NOW RUNNING!
echo ========================================
echo Frontend URL: http://localhost:8000
echo Backend API URL: http://localhost:8001
echo Close both server windows to stop the system
echo ========================================
echo.

echo Press any key to exit this window (servers will continue running)...
pause >nul