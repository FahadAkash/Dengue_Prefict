# 🦟 Dengue Risk Prediction System - Complete Setup & Run Instructions

## 📋 Project Overview

This is a **full-stack AI-powered Dengue Intelligence System** with:
- ✅ **ML Prediction Model** - Logistic Regression for dengue risk
- ✅ **FastAPI Backend** - REST API for predictions
- ✅ **Frontend Dashboard** - Web UI for user interaction
- ✅ **AI Agent** - Google Gemini-powered chatbot
- ✅ **Vector Database** - Pinecone for similarity search

---

## 🔧 System Requirements

- **Windows 10/11**
- **Python 3.8+** (Tested with Python 3.13.9)
- **Internet Connection** (for API calls)
- **Available Ports**: 8000 (Frontend), 8001 (Backend API)

Check if Python is installed:
```powershell
python --version
```

---

## 📦 Step 1: Install Dependencies

### Method A: Simple Installation
```powershell
cd f:\gihtub\Dengue_Prefict\dengue_predictor
pip install -r requirment.txt
```

### Method B: Using Virtual Environment (Recommended)
```powershell
# Navigate to project
cd f:\gihtub\Dengue_Prefict

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install -r dengue_predictor\requirment.txt
```

---

## 🔐 Step 2: Set Up API Keys

You need two free API keys:

### Get Google API Key (Gemini)
1. Go to: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy the key

### Get Pinecone API Key
1. Go to: https://app.pinecone.io/
2. Sign up (free tier available)
3. Create a project and get your API key

### Create .env File
In the `dengue_predictor` folder, create a `.env` file:

```env
GOOGLE_API_KEY=your_google_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
```

Or copy from example:
```powershell
cd f:\gihtub\Dengue_Prefict\dengue_predictor
Copy-Item .env.example .env
```
Then edit the `.env` file with your actual keys.

---

## 🚀 Step 3: Run the Project

### 🟢 EASIEST METHOD: Batch File (Windows)
Just double-click this file:
```
f:\gihtub\Dengue_Prefict\dengue_predictor\start_full_system.bat
```

This will:
- ✅ Start Backend API on `http://localhost:8001`
- ✅ Start Frontend on `http://localhost:8000`
- ✅ Open browser automatically

---

### 🔵 METHOD 2: PowerShell Commands (Manual)

#### Terminal 1 - Start Backend API
```powershell
cd f:\gihtub\Dengue_Prefict\dengue_predictor
python -m uvicorn api.BaseAPI:app --host localhost --port 8001 --reload
```

Wait for message: `Application startup complete`

#### Terminal 2 - Start Frontend Server
```powershell
cd f:\gihtub\Dengue_Prefict\dengue_predictor\frontend
python server.py
```

Wait for message: `Serving on`

#### Open Browser
- Frontend: http://localhost:8000
- API Docs: http://localhost:8001/docs

---

### 🟣 METHOD 3: Interactive Startup Menu
```powershell
cd f:\gihtub\Dengue_Prefict\dengue_predictor
python -m scripts.startup
```

Options:
1. **Start FastAPI server** - Backend API only
2. **Run AI agent demo** - Terminal chatbot
3. **Exit**

---

## 🧪 Step 4: Test the System

### Test Backend API
```powershell
# Check if API is running
curl http://localhost:8001/health

# Expected response:
# {"status": "healthy"}
```

### Test with API Docs
Open in browser: http://localhost:8001/docs
- Interactive Swagger UI
- Try out `/predict` endpoint

### Test Frontend
Open in browser: http://localhost:8000
- Fill in the dengue risk form
- Get predictions and AI recommendations

### Test AI Agent
```powershell
cd f:\gihtub\Dengue_Prefict\dengue_predictor
python -m scripts.startup
# Choose option 2
# Ask: "What is the dengue risk in Dhaka?"
```

---

## 📊 Project Structure

```
f:\gihtub\Dengue_Prefict\
├── dengue_predictor/
│   ├── api/
│   │   └── BaseAPI.py           # FastAPI REST endpoints
│   │       └── GET /health      # Health check
│   │       └── POST /predict    # Predictions
│   │       └── GET /stats       # Model info
│   │
│   ├── agents/
│   │   └── AI_Agent.py          # Gemini chatbot logic
│   │
│   ├── frontend/
│   │   ├── index.html           # Web UI
│   │   ├── server.py            # Frontend server
│   │   └── script.js            # Form handling
│   │
│   ├── core/
│   │   └── models/
│   │       └── logistic_regression_model.joblib  # Trained ML model
│   │
│   ├── db/
│   │   └── PineconeDB.py        # Vector database
│   │
│   ├── datasets/
│   │   └── dataset.csv          # Historical data
│   │
│   ├── scripts/
│   │   └── startup.py           # Main startup script
│   │
│   ├── tests/
│   │   └── test_*.py            # Test files
│   │
│   ├── start_full_system.bat    # Complete system launcher
│   ├── start_full_system.ps1    # PowerShell version
│   ├── requirment.txt           # Dependencies
│   ├── .env                     # API keys (create this!)
│   └── README.md
│
└── README.md
```

---

## 🔌 API Endpoints

### Health Check
```
GET http://localhost:8001/health
```
Response: `{"status": "healthy"}`

### Predict Risk
```
POST http://localhost:8001/predict
Content-Type: application/json

{
  "age": 35,
  "area": "Badda",
  "district": "Dhaka",
  "fever": 1,
  "rash": 0,
  "joint_pain": 1,
  "month": 6
}
```

Response:
```json
{
  "risk_probability": 0.82,
  "risk_level": "HIGH",
  "message": "Increased dengue risk in this area"
}
```

### Model Stats
```
GET http://localhost:8001/stats
```

---

## 🤖 AI Agent Features

Ask the agent questions like:
- "What is the dengue risk in Dhaka?"
- "Which areas have the highest risk?"
- "What should I do if I have dengue symptoms?"
- "Show me statistics for Badda"

The agent will:
- Call the ML model for predictions
- Search historical cases
- Provide intelligent recommendations
- Answer in natural language

---

## ⚠️ Troubleshooting

### Problem: "Module not found" errors
**Solution:**
```powershell
# Make sure you're in the right directory
cd f:\gihtub\Dengue_Prefict\dengue_predictor

# Reinstall dependencies
pip install -r requirment.txt --force-reinstall
```

### Problem: Ports already in use
```powershell
# Find what's using port 8001
Get-NetTCPConnection -LocalPort 8001

# Kill the process (if needed)
Stop-Process -Id <PID> -Force
```

### Problem: API keys not working
- Double-check keys in `.env` file
- Make sure `.env` is in `dengue_predictor` folder (not root)
- Restart servers after changing `.env`

### Problem: Frontend won't connect to backend
- Make sure backend is running on `localhost:8001`
- Check browser console for CORS errors
- Verify firewall isn't blocking localhost

### Problem: "GOOGLE_API_KEY environment variable not set"
```powershell
# Verify .env exists and has correct key
cd f:\gihtub\Dengue_Prefict\dengue_predictor
Get-Content .env
```

---

## 📝 Key Files & Their Purpose

| File | Purpose |
|------|---------|
| `api/BaseAPI.py` | FastAPI backend with `/predict` endpoint |
| `agents/AI_Agent.py` | Google Gemini AI chatbot |
| `frontend/server.py` | Frontend web server |
| `frontend/index.html` | Web interface |
| `db/PineconeDB.py` | Vector database operations |
| `core/models/logistic_regression_model.joblib` | Trained ML model |
| `scripts/startup.py` | Interactive startup menu |
| `start_full_system.bat` | One-click system launcher |
| `.env` | API keys (YOU MUST CREATE THIS) |

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Install deps | `pip install -r requirment.txt` |
| Start full system | Run `start_full_system.bat` |
| Start backend only | `python -m uvicorn api.BaseAPI:app --host localhost --port 8001` |
| Start frontend only | `cd frontend && python server.py` |
| Run AI agent | `python -m scripts.startup` → choose option 2 |
| Check API docs | Open `http://localhost:8001/docs` |
| Access frontend | Open `http://localhost:8000` |

---

## ✅ Success Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirment.txt`)
- [ ] `.env` file created with API keys
- [ ] Backend running on `localhost:8001`
- [ ] Frontend running on `localhost:8000`
- [ ] Can access `http://localhost:8000` in browser
- [ ] Can access `http://localhost:8001/docs` API docs
- [ ] Prediction form works
- [ ] AI agent responds to queries

---

## 🆘 Need Help?

1. **Check logs** - Both servers print errors to console
2. **Test API** - Use `http://localhost:8001/docs` to test endpoints
3. **Browser console** - Open DevTools (F12) to see frontend errors
4. **Verify files** - Make sure `.env` exists in `dengue_predictor` folder

---

## 🎉 You're Ready!

Your Dengue Risk Prediction System is now running and ready to use!

### Access Points:
- 🌐 **Frontend**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8001/docs
- 🤖 **AI Agent**: Terminal via `python -m scripts.startup`

**Enjoy the system!** 🦟
