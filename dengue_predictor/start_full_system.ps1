Write-Host "========================================"
Write-Host "DENGUE RISK PREDICTOR - COMPLETE SYSTEM"
Write-Host "========================================"
Write-Host ""

Write-Host "Starting complete system..."
Write-Host "Ports configuration:"
Write-Host "  - Frontend server: http://localhost:8000"
Write-Host "  - Backend API: http://localhost:8001"
Write-Host ""

Write-Host "Starting backend API server..."
Start-Process python -ArgumentList "-m", "uvicorn", "BaseAPI:app", "--host", "localhost", "--port", "8001" -WorkingDirectory ".\api" -WindowStyle Normal

Write-Host "Starting frontend server..."
Start-Process python -ArgumentList "server.py" -WorkingDirectory ".\frontend" -WindowStyle Normal

Start-Sleep -Seconds 5

Write-Host "Opening browser..."
Start-Process "http://localhost:8000"

Write-Host ""
Write-Host "========================================"
Write-Host "SYSTEM IS NOW RUNNING!"
Write-Host "========================================"
Write-Host "Frontend URL: http://localhost:8000"
Write-Host "Backend API URL: http://localhost:8001"
Write-Host "Close both server windows to stop the system"
Write-Host "========================================"

Write-Host ""
Write-Host "Press Enter to exit this window (servers will continue running)..."
Read-Host