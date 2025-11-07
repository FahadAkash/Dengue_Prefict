# Dengue Risk Prediction System - Complete Setup

This document explains how to run the complete Dengue Risk Prediction System with both frontend and backend components.

## System Architecture

The system consists of two main components:
1. **Frontend Server** - Runs on port 8000, serves the web interface
2. **Backend API** - Runs on port 8001, handles prediction requests

## Prerequisites

Make sure you have installed all required dependencies:
```bash
pip install -r requirment.txt
```

## Running the Complete System

### Option 1: Using the Batch File (Windows)
Double-click on `start_full_system.bat` to start both servers automatically.

### Option 2: Using the PowerShell Script (Windows)
Run the following command in PowerShell:
```powershell
.\start_full_system.ps1
```

### Option 3: Manual Start

1. **Start the Backend API Server:**
   ```bash
   cd api
   python -m uvicorn BaseAPI:app --host localhost --port 8001
   ```

2. **Start the Frontend Server:**
   ```bash
   cd frontend
   python server.py
   ```

3. **Open your browser:**
   Navigate to `http://localhost:8000`

## Ports Configuration

- **Frontend Server**: http://localhost:8000
- **Backend API**: http://localhost:8001

## Testing the System

You can test the backend API directly using the test script:
```bash
python test_backend_api.py
```

## Features

### Frontend Features:
- Beautiful responsive UI with medical theme
- Patient information form with validation
- Loading animation during risk calculation
- Real-time risk assessment display
- Color-coded risk levels (High/Medium/Low)
- Personalized recommendations
- AI assistant chat interface

### Backend Features:
- Machine learning model for dengue risk prediction
- RESTful API with JSON responses
- Integration with Pinecone vector database
- Detailed risk analysis and recommendations
- Error handling and logging

## How It Works

1. User enters patient information in the frontend form
2. Frontend sends data to backend API on port 8001
3. Backend processes data using ML model
4. Backend returns risk assessment and recommendations
5. Frontend displays results with loading animation
6. AI assistant provides additional guidance

## Troubleshooting

### If you see "Backend service unavailable":
- Make sure the backend API server is running on port 8001
- Check that no other process is using port 8001

### If the frontend doesn't load:
- Make sure the frontend server is running on port 8000
- Check that no other process is using port 8000

### If you get connection errors:
- Ensure both servers are running
- Check firewall settings
- Verify port configurations