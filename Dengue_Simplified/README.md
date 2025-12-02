# 🦟 Dengue Risk Prediction System - Simplified Version

A **minimal, fully functional** Dengue Risk Prediction system with just **3 core files** while maintaining complete AI-powered functionality.

## ✨ Features

✅ **ML-Based Risk Prediction** - Logistic regression model for dengue risk assessment  
✅ **Google Gemini AI Integration** - Intelligent health recommendations  
✅ **Modern Web Interface** - Responsive design with real-time results  
✅ **Chat Assistant** - Interactive AI chatbot for health guidance  
✅ **Risk Visualization** - Beautiful charts and color-coded risk levels  

## 📁 Project Structure

```
Dengue_Simplified/
├── app.py                              # Backend server (Flask + ML + AI)
├── index.html                          # Frontend (HTML + CSS + JS)
├── logistic_regression_model.joblib    # Trained ML model
├── requirements.txt                    # Dependencies
├── .env.example                        # API key template
└── README.md                           # This file
```

**Total: Just 3 code files** (app.py, index.html, + ML model)

## 🚀 Quick Start

### Step 1: Install Dependencies

```bash
cd Dengue_Simplified
pip install -r requirements.txt
```

### Step 2: Get Google Gemini API Key

1. Visit: https://aistudio.google.com/app/apikey
2. Click "Create API Key"
3. Copy your API key

### Step 3: Create .env File

```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your API key
# GOOGLE_API_KEY=your_actual_api_key_here
```

Or create `.env` manually with:
```
GOOGLE_API_KEY=your_google_gemini_api_key_here
```

### Step 4: Run the Server

```bash
python app.py
```

The server will start on **http://localhost:5000**

### Step 5: Open in Browser

Open your browser and go to: **http://localhost:5000**

## 📖 How to Use

### 1. Risk Assessment
- Fill in the patient information form:
  - Age and Gender
  - Test Results (NS1, IgG, IgM)
  - Location (District and Area)
  - Area Type and House Type
- Click "Calculate Risk"
- View the risk percentage and level (LOW/MEDIUM/HIGH)

### 2. AI Health Assistant
- After getting a risk assessment, the AI assistant activates
- Ask questions like:
  - "What should I do?"
  - "What are the symptoms of dengue?"
  - "How can I prevent dengue?"
  - "What foods should I eat?"
- Get personalized recommendations based on your risk level

## 🔌 API Endpoints

### Health Check
```bash
GET http://localhost:5000/health
```

### Predict Risk
```bash
POST http://localhost:5000/predict
Content-Type: application/json

{
  "Age": 30,
  "Gender": 1,
  "NS1": 1,
  "IgG": 0,
  "IgM": 1,
  "Area": "Badda",
  "District": "Dhaka",
  "AreaType": "Urban",
  "HouseType": "Building"
}
```

### Chat with AI
```bash
POST http://localhost:5000/chat
Content-Type: application/json

{
  "message": "What should I do?",
  "conversation_history": [],
  "risk_assessment": {...}
}
```

## 🛠️ Troubleshooting

### Problem: Import errors
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Problem: AI not responding
**Solution:**
- Check that `.env` file exists in the same folder as `app.py`
- Verify your `GOOGLE_API_KEY` is correct
- Restart the server after changing `.env`

### Problem: Model not loading
**Solution:**
- Ensure `logistic_regression_model.joblib` is in the same folder as `app.py`
- The model file should be about 1-2 KB in size

### Problem: Port already in use
**Solution:**
```bash
# Find the process using port 5000
netstat -ano | findstr :5000

# Kill the process (replace PID with actual process ID)
taskkill /PID <PID> /F

# Or change the port in app.py (last line):
app.run(host='0.0.0.0', port=5001, debug=True)
```

## 🎯 Key Differences from Original

| Feature | Original | Simplified |
|---------|----------|------------|
| Files | 40+ files | 3 files |
| Lines of Code | ~5000+ | ~1000 |
| Dependencies | 30+ packages | 8 packages |
| Framework | FastAPI | Flask |
| Vector DB | Pinecone | In-memory |
| Setup Time | 10+ minutes | 2 minutes |
| Complexity | High | Minimal |
| **Functionality** | ✅ Full | ✅ **Full** |

## 📊 Technology Stack

- **Backend**: Flask (lightweight Python web framework)
- **ML**: Scikit-learn (Logistic Regression)
- **AI**: Google Gemini 2.0 Flash
- **Frontend**: Vanilla HTML/CSS/JavaScript
- **Charts**: Chart.js

## 🔒 Security Notes

- ⚠️ Never commit your `.env` file to version control
- ⚠️ Keep your API keys secret
- ⚠️ For production, use environment variables or a secure key management system

## 📝 License

This is a simplified educational version. Use for learning purposes.

## 👥 Credits

Based on the full Dengue Risk Prediction System by:
- Umme Hani Bithe (Roll 41)
- Jannat (Roll 14)

Simplified version created: December 2025

## 🆘 Need Help?

1. Check the server console for error messages
2. Verify all files are in the correct location
3. Ensure Python 3.8+ is installed
4. Make sure all dependencies are installed

---

**Enjoy the simplified Dengue Risk Prediction System!** 🦟✨
