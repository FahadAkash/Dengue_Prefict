# Quick Start Script for Dengue Risk Prediction System

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   Dengue Risk Prediction System - Simplified Version" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env file exists
if (-not (Test-Path ".env")) {
    Write-Host "[!] Creating .env file from template..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host ""
    Write-Host "[!] WARNING: You need to add your Google Gemini API key to .env file" -ForegroundColor Red
    Write-Host "[!] Get it from: https://aistudio.google.com/app/apikey" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Opening .env file in notepad..." -ForegroundColor Yellow
    Start-Process notepad ".env"
    Write-Host "Press Enter after adding your API key..." -ForegroundColor Yellow
    Read-Host
}

# Check if dependencies are installed
Write-Host "[*] Checking dependencies..." -ForegroundColor Green
try {
    python -c "import flask" 2>$null
    if ($LASTEXITCODE -ne 0) {
        throw "Flask not installed"
    }
    Write-Host "[✓] Dependencies already installed" -ForegroundColor Green
} catch {
    Write-Host "[!] Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host ""
}

Write-Host ""
Write-Host "[*] Starting server..." -ForegroundColor Green
Write-Host "[*] Access the application at: http://localhost:5000" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Start the server
python app.py
