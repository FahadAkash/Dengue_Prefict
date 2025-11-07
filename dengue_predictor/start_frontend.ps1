Write-Host "========================================"
Write-Host "DENGUE RISK PREDICTOR - FRONTEND STARTUP"
Write-Host "========================================"
Write-Host ""

Write-Host "Starting server..."
Set-Location -Path "frontend"
Start-Process python -ArgumentList "server.py"
Start-Sleep -Seconds 3

Write-Host "Opening browser..."
Start-Process "http://localhost:8000"

Write-Host ""
Write-Host "Server is running at http://localhost:8000"
Write-Host "Press Enter to stop the server..."
Read-Host