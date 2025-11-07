# Dengue Risk Prediction System

A full-stack AI-powered Dengue Intelligence System using Google Gemini Flash and Pinecone Vector Database.

## 🎯 System Overview

This system provides dengue risk prediction and intelligence through:

1. **ML Prediction API** - REST API exposing a trained Logistic Regression model
2. **Pinecone Vector Database** - Stores dengue cases with predictions for similarity search
3. **AI Agent** - Natural language interface powered by Google Gemini Flash
4. **FastAPI Backend** - Web framework for API endpoints

## 🚀 Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirment.txt
   ```

2. **Set up environment variables:**
   - Copy `.env.example` to `.env`
   - Add your `GOOGLE_API_KEY` and `PINECONE_API_KEY`

3. **Run the system:**
   ```bash
   python -m scripts.startup
   ```

## 📁 Project Structure

```
├── agents/
│   └── AI_Agent.py          # AI agent with Gemini Flash integration
├── api/
│   └── BaseAPI.py           # FastAPI REST endpoints
├── core/
│   ├── main.py              # ML model inference example
│   └── models/
│       └── logistic_regression_model.joblib  # Trained model
├── db/
│   ├── PineconeDB.py        # Pinecone vector database implementation
│   └── ChromaDB.py          # Legacy ChromaDB implementation
├── scripts/
│   ├── startup.py           # Main startup script
│   └── install_deps.py      # Dependency installation script
├── tests/
│   ├── test_system.py       # System testing script
│   ├── demo.py              # System demonstration
│   └── test_api_keys.py     # API key testing
├── utils/
├── requirment.txt           # Python dependencies
└── README.md                # This file
```

## 🧠 Key Components

### 1. ML Prediction API (`api/BaseAPI.py`)
- `POST /predict` - Get dengue risk prediction
- `GET /health` - Check if API is running
- `GET /stats` - Model metadata

### 2. Pinecone Vector Database (`db/PineconeDB.py`)
- `add_case_to_vector_db()` - Store new case with prediction
- `search_similar_cases()` - Find past cases with similar patterns
- `get_area_statistics()` - Get stats for specific district/area
- `batch_load_dataset()` - Import entire CSV dataset

### 3. AI Agent (`agents/AI_Agent.py`)
- Natural language interface to the system
- Uses Google Gemini Flash to understand questions
- Calls tools automatically and gives intelligent responses

## 🛠️ Usage Examples

### For Health Officials:
```python
# Query high-risk areas
high_risk = get_high_risk_areas(threshold=0.7)
```

### For Clinics:
```python
# API call with patient data
response = requests.post("/predict", json=patient_data)
```

### For Public (via AI Agent):
```
User: "Is it safe to visit Badda this week?"
Agent: Checks current risk, recent cases, trends
Agent: "Badda shows 82% dengue risk with 47 cases last week. 
       Recommend postponing or taking extra precautions..."
```

## 📊 Data Flow

1. Patient data + area information
2. ML model predicts risk probability
3. Results stored in Pinecone vector database
4. AI agent retrieves predictions + historical context
5. Returns intelligent, actionable insights

## 🔧 Environment Variables

- `GOOGLE_API_KEY` - For Gemini Flash API access
- `PINECONE_API_KEY` - For Pinecone vector database

## 🎯 Real-World Use Cases

| Stakeholder | Use Case | System Component |
|-------------|----------|------------------|
| **Hospital** | Triage patients by risk | API `/predict` endpoint |
| **Health Dept** | Identify outbreak zones | Database `get_high_risk_areas()` |
| **City Planner** | Allocate spraying resources | Database area statistics |
| **Researcher** | Analyze risk factors | Database queries + Model insights |
| **Public** | Check area safety | AI Agent chatbot |
| **Emergency Response** | Early warning alerts | API + Database monitoring |