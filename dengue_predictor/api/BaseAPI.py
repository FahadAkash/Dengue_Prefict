from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import numpy as np
import pandas as pd
from typing import Dict, List, Optional
import sys
import os

# Setup paths for imports (works in both development and executable mode)
def setup_import_paths():
    """Setup sys.path for importing modules"""
    if getattr(sys, 'frozen', False):
        # Running as executable - use _MEIPASS
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
            # Add base path and subdirectories to sys.path
            if base_path not in sys.path:
                sys.path.insert(0, base_path)
        else:
            base_path = None
    else:
        # Running as script - add parent directory to path
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if base_path not in sys.path:
            sys.path.insert(0, base_path)
    
    return base_path

# Setup paths first
setup_import_paths()

# Import from PineconeDB - try multiple import strategies
add_case_to_vector_db = None
try:
    # Try 1: Direct import (when in sys.path)
    from db.PineconeDB import add_case_to_vector_db
except ImportError:
    try:
        # Try 2: Absolute import from package
        from db import PineconeDB
        add_case_to_vector_db = PineconeDB.add_case_to_vector_db
    except ImportError:
        try:
            # Try 3: Direct module import
            import db.PineconeDB as PineconeDB
            add_case_to_vector_db = PineconeDB.add_case_to_vector_db
        except ImportError:
            # Try 4: Import from file path
            import importlib.util
            if getattr(sys, 'frozen', False):
                db_file = os.path.join(sys._MEIPASS, 'db', 'PineconeDB.py')
            else:
                db_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'db', 'PineconeDB.py')
            if os.path.exists(db_file):
                spec = importlib.util.spec_from_file_location("PineconeDB", db_file)
                pinecone_db = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(pinecone_db)
                add_case_to_vector_db = pinecone_db.add_case_to_vector_db

if add_case_to_vector_db is None:
    raise ImportError("Could not import add_case_to_vector_db from PineconeDB")

# Import from AI_Agent - try multiple import strategies
chat_with_dengue_agent = None
try:
    # Try 1: Direct import (when in sys.path)
    from agents.AI_Agent import chat_with_dengue_agent
except ImportError:
    try:
        # Try 2: Absolute import from package
        from agents import AI_Agent
        chat_with_dengue_agent = AI_Agent.chat_with_dengue_agent
    except ImportError:
        try:
            # Try 3: Direct module import
            import agents.AI_Agent as AI_Agent
            chat_with_dengue_agent = AI_Agent.chat_with_dengue_agent
        except ImportError:
            # Try 4: Import from file path
            import importlib.util
            if getattr(sys, 'frozen', False):
                agent_file = os.path.join(sys._MEIPASS, 'agents', 'AI_Agent.py')
            else:
                agent_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'agents', 'AI_Agent.py')
            if os.path.exists(agent_file):
                spec = importlib.util.spec_from_file_location("AI_Agent", agent_file)
                ai_agent = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(ai_agent)
                chat_with_dengue_agent = ai_agent.chat_with_dengue_agent

if chat_with_dengue_agent is None:
    raise ImportError("Could not import chat_with_dengue_agent from AI_Agent")

app = FastAPI(title="Dengue Risk Prediction API")

# Load your trained model from the correct path
# Handle both development and PyInstaller executable paths
def get_model_path():
    """Get the model path, works for both development and executable"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        base_path = sys._MEIPASS
        return os.path.join(base_path, 'core', 'models', 'logistic_regression_model.joblib')
    else:
        # Running as script
        return os.path.join(os.path.dirname(__file__), '..', 'core', 'models', 'logistic_regression_model.joblib')

model_path = get_model_path()
model = joblib.load(model_path)

class PatientData(BaseModel):
    Age: int
    Gender: int  # 0=Female, 1=Male
    NS1: int  # 0=Negative, 1=Positive
    IgG: int
    IgM: int
    Area: str
    AreaType: str  # Urban/Rural/Undeveloped
    HouseType: str
    District: str

class PredictionResponse(BaseModel):
    probability: float
    risk_level: str
    confidence: str
    recommendation: str
    key_factors: Dict[str, str]

class ChatMessage(BaseModel):
    message: str
    conversation_history: List[Dict] = []
    risk_assessment: Optional[Dict] = None
    include_full_recommendations: bool = False

def get_risk_level(prob: float) -> str:
    if prob >= 0.7:
        return "High"
    elif prob >= 0.4:
        return "Medium"
    return "Low"

def get_recommendation(prob: float, area: str) -> str:
    if prob >= 0.7:
        return f"""HIGH RISK ({prob*100:.1f}%)

🔴 IMMEDIATE ACTIONS REQUIRED:
- Consult a healthcare provider immediately, especially if experiencing fever, headache, or joint pain
- Avoid outdoor activities during peak mosquito hours (dawn & dusk)
- Stay in air-conditioned or well-screened areas
- Eliminate standing water around your home (flower pots, containers, gutters)
- Wear long-sleeved shirts and long pants in light colors

💊 HEALTH RECOMMENDATIONS:
- Stay hydrated with clean, boiled water
- Take vitamin C supplements to boost immunity
- Consider papaya leaf extract (consult doctor first)
- Avoid aspirin or ibuprofen (may increase bleeding risk)

🚫 AVOID:
- Stagnant water bodies
- Dark clothing (attracts mosquitoes)
- Perfumes or scented products
- Leaving windows/doors open without screens

🌡️ SEEK IMMEDIATE MEDICAL HELP IF:
- High fever develops
- Severe headache or pain behind eyes
- Joint/muscle pain
- Nausea or vomiting

📅 2-4 MONTH OUTLOOK: Historically, {area} shows continued elevated risk during this period. Enhanced vigilance required."""
    elif prob >= 0.4:
        return f"""MEDIUM RISK ({prob*100:.1f}%)

🟡 ENHANCED PREVENTION NEEDED:
- Take preventive measures against mosquito bites
- Check and repair window/door screens
- Use mosquito repellent when outdoors
- Clear any standing water weekly

🥗 DIETARY GUIDELINES:
- Increase vitamin C intake (citrus fruits, berries)
- Consume papaya, pomegranate, and kiwi for platelet support
- Stay well-hydrated
- Include garlic and neem in your diet for natural mosquito repellent properties

💪 DAILY LIFESTYLE:
- Wear protective clothing during peak mosquito hours
- Use mosquito nets while sleeping
- Install or check window screens
- Exercise regularly to boost immunity

📅 2-4 MONTH OUTLOOK: {area} shows moderate risk trends. Continue preventive measures."""
    else:
        return f"""LOW RISK ({prob*100:.1f}%)

🟢 GENERAL PREVENTION:
- Maintain basic mosquito prevention habits
- Regularly check for and eliminate standing water
- Use mosquito repellent during peak hours

🥗 HEALTHY HABITS:
- Balanced diet rich in vitamins and minerals
- Adequate sleep (7-8 hours) for strong immunity
- Regular exercise
- Stay hydrated

💊 SUPPLEMENTS:
- Daily multivitamin
- Vitamin D if limited sun exposure

📅 2-4 MONTH OUTLOOK: {area} historically shows low risk. Continue routine monitoring."""

@app.post("/predict", response_model=PredictionResponse)
async def predict_dengue(data: PatientData):
    try:
        # Create a dataframe with all the required features
        # Based on the feature names we discovered
        feature_data = {
            'Gender': [data.Gender],
            'Age': [data.Age],
            'NS1': [data.NS1],
            'IgG': [data.IgG],
            'IgM': [data.IgM],
            'Area_Adabor': [1 if data.Area == 'Adabor' else 0],
            'Area_Badda': [1 if data.Area == 'Badda' else 0],
            'Area_Banasree': [1 if data.Area == 'Banasree' else 0],
            'Area_Bangshal': [1 if data.Area == 'Bangshal' else 0],
            'Area_Biman Bandar': [1 if data.Area == 'Biman Bandar' else 0],
            'Area_Bosila': [1 if data.Area == 'Bosila' else 0],
            'Area_Cantonment': [1 if data.Area == 'Cantonment' else 0],
            'Area_Chawkbazar': [1 if data.Area == 'Chawkbazar' else 0],
            'Area_Demra': [1 if data.Area == 'Demra' else 0],
            'Area_Dhanmondi': [1 if data.Area == 'Dhanmondi' else 0],
            'Area_Gendaria': [1 if data.Area == 'Gendaria' else 0],
            'Area_Gulshan': [1 if data.Area == 'Gulshan' else 0],
            'Area_Hazaribagh': [1 if data.Area == 'Hazaribagh' else 0],
            'Area_Jatrabari': [1 if data.Area == 'Jatrabari' else 0],
            'Area_Kadamtali': [1 if data.Area == 'Kadamtali' else 0],
            'Area_Kafrul': [1 if data.Area == 'Kafrul' else 0],
            'Area_Kalabagan': [1 if data.Area == 'Kalabagan' else 0],
            'Area_Kamrangirchar': [1 if data.Area == 'Kamrangirchar' else 0],
            'Area_Keraniganj': [1 if data.Area == 'Keraniganj' else 0],
            'Area_Khilgaon': [1 if data.Area == 'Khilgaon' else 0],
            'Area_Khilkhet': [1 if data.Area == 'Khilkhet' else 0],
            'Area_Lalbagh': [1 if data.Area == 'Lalbagh' else 0],
            'Area_Mirpur': [1 if data.Area == 'Mirpur' else 0],
            'Area_Mohammadpur': [1 if data.Area == 'Mohammadpur' else 0],
            'Area_Motijheel': [1 if data.Area == 'Motijheel' else 0],
            'Area_New Market': [1 if data.Area == 'New Market' else 0],
            'Area_Pallabi': [1 if data.Area == 'Pallabi' else 0],
            'Area_Paltan': [1 if data.Area == 'Paltan' else 0],
            'Area_Ramna': [1 if data.Area == 'Ramna' else 0],
            'Area_Rampura': [1 if data.Area == 'Rampura' else 0],
            'Area_Sabujbagh': [1 if data.Area == 'Sabujbagh' else 0],
            'Area_Shahbagh': [1 if data.Area == 'Shahbagh' else 0],
            'Area_Sher-e-Bangla Nagar': [1 if data.Area == 'Sher-e-Bangla Nagar' else 0],
            'Area_Shyampur': [1 if data.Area == 'Shyampur' else 0],
            'Area_Sutrapur': [1 if data.Area == 'Sutrapur' else 0],
            'Area_Tejgaon': [1 if data.Area == 'Tejgaon' else 0],
            'AreaType_Developed': [1 if data.AreaType == 'Developed' else 0],
            'AreaType_Undeveloped': [1 if data.AreaType == 'Undeveloped' else 0],
            'District_Dhaka': [1 if data.District == 'Dhaka' else 0],
            'HouseType_Building': [1 if data.HouseType == 'Building' else 0],
            'HouseType_Other': [1 if data.HouseType == 'Other' else 0],
            'HouseType_Tinshed': [1 if data.HouseType == 'Tinshed' else 0]
        }
        
        # Create DataFrame
        feature_df = pd.DataFrame(feature_data)
        
        # Get probability
        prob = float(model.predict_proba(feature_df)[0][1])
        risk_level = get_risk_level(prob)
        
        # Analyze key factors
        key_factors = {}
        if data.NS1 == 1:
            key_factors["NS1_Status"] = "Positive (strong indicator)"
        if data.IgM == 1:
            key_factors["IgM_Status"] = "Positive (recent infection)"
        if prob >= 0.7:
            key_factors["Area_Risk"] = f"{data.Area} in {data.District} shows elevated risk"
        
        # Store the case in Pinecone vector database
        case_data = {
            'Age': data.Age,
            'Gender': data.Gender,
            'NS1': data.NS1,
            'IgG': data.IgG,
            'IgM': data.IgM,
            'Area': data.Area,
            'AreaType': data.AreaType,
            'HouseType': data.HouseType,
            'District': data.District
        }
        
        try:
            add_case_to_vector_db(case_data, prob)
        except Exception as e:
            # Log the error but don't fail the prediction
            print(f"Warning: Could not store case in vector DB: {e}")
        
        # Return minimal recommendation - AI agent will provide detailed recommendations
        recommendation = f"Risk Level: {risk_level} ({prob*100:.1f}% probability). For detailed recommendations, please consult with the AI assistant."
        
        return PredictionResponse(
            probability=round(prob, 3),
            risk_level=risk_level,
            confidence="High" if abs(prob - 0.5) > 0.3 else "Medium",
            recommendation=recommendation,
            key_factors=key_factors
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat")
async def chat_with_agent(chat_data: ChatMessage):
    """Chat endpoint that connects to the Gemini AI agent with risk assessment context"""
    try:
        # If risk assessment data is provided, include it in the message context
        history = chat_data.conversation_history or []
        normalized_history = []
        for message in history:
            if isinstance(message, dict) and 'role' in message and 'content' in message:
                normalized_history.append({
                    "role": message['role'],
                    "content": message['content']
                })

        enhanced_message = chat_data.message
        if chat_data.risk_assessment:
            context_summary = f"""
Risk Level: {chat_data.risk_assessment.get('risk_level', 'Unknown')}
Probability: {chat_data.risk_assessment.get('probability', 'Unknown')}%
Patient: {chat_data.risk_assessment.get('age', 'Unknown')} years old, {chat_data.risk_assessment.get('gender', 'Unknown')}
Lab Results: NS1 {chat_data.risk_assessment.get('ns1', 'Unknown')}, IgG {chat_data.risk_assessment.get('igg', 'Unknown')}, IgM {chat_data.risk_assessment.get('igm', 'Unknown')}
Location: {chat_data.risk_assessment.get('area', 'Unknown')}, {chat_data.risk_assessment.get('district', 'Unknown')}
"""

            include_full = chat_data.include_full_recommendations or len(normalized_history) == 0
            if include_full:
                enhanced_message = f"""
Risk Assessment Context:
- Risk Level: {chat_data.risk_assessment.get('risk_level', 'Unknown')}
- Probability: {chat_data.risk_assessment.get('probability', 'Unknown')}%
- Patient Age: {chat_data.risk_assessment.get('age', 'Unknown')}
- Patient Gender: {chat_data.risk_assessment.get('gender', 'Unknown')}
- Test Results: NS1 {chat_data.risk_assessment.get('ns1', 'Unknown')}, IgG {chat_data.risk_assessment.get('igg', 'Unknown')}, IgM {chat_data.risk_assessment.get('igm', 'Unknown')}
- Location: {chat_data.risk_assessment.get('area', 'Unknown')}, {chat_data.risk_assessment.get('district', 'Unknown')}

User Question: {chat_data.message}

Please provide detailed, personalized advice based on this risk assessment context.
"""
            else:
                enhanced_message = f"""
Patient Context:
{context_summary}

User Question: {chat_data.message}

Please answer concisely while considering the patient's current risk assessment.
"""
        
        response, updated_history = chat_with_dengue_agent(
            enhanced_message,
            normalized_history
        )
        return {
            "response": response,
            "conversation_history": updated_history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.get("/stats")
async def get_stats():
    # Return model metadata
    return {
        "model_type": "Logistic Regression",
        "features": model.n_features_in_,
        "version": "1.0"
    }

# Run with: uvicorn BaseAPI:app --reload