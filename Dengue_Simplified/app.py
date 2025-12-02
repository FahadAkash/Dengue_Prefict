"""
Simplified Dengue Risk Prediction System - Backend Server
A minimal Flask server with ML prediction and Google Gemini AI integration
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import numpy as np
import pandas as pd
import google.generativeai as genai
import os
from dotenv import load_dotenv
import traceback

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder='.')
CORS(app)

# Initialize Google Gemini
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    print("⚠️  WARNING: GOOGLE_API_KEY not found in .env file!")
    print("   The chat feature will not work without it.")
else:
    genai.configure(api_key=GOOGLE_API_KEY)
    gemini_model = genai.GenerativeModel('models/gemini-2.0-flash-exp')
    print("✅ Google Gemini AI initialized")

# Load ML model
try:
    model = joblib.load('logistic_regression_model.joblib')
    print("✅ ML model loaded successfully")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

# District-Area mapping
AREAS_BY_DISTRICT = {
    "Dhaka": ["Adabor", "Badda", "Banasree", "Bangshal", "Dhanmondi", "Gulshan", 
              "Jatrabari", "Mirpur", "Mohammadpur", "Motijheel", "Uttara"],
    "Chittagong": ["Agrabad", "Halishahar", "Khulshi", "Panchlaish", "Nasirabad"],
    "Khulna": ["Khalishpur", "Sonadanga", "Daulatpur"],
    "Rajshahi": ["Rajshahi Sadar", "Shah Mokdum", "Boalia"],
    "Barisal": ["Barisal Sadar", "Babuganj"],
    "Sylhet": ["Sylhet Sadar", "Jalalabad"],
    "Rangpur": ["Rangpur Sadar"],
    "Mymensingh": ["Mymensingh Sadar"]
}


def get_risk_level(probability):
    """Determine risk level from probability"""
    if probability >= 0.7:
        return "HIGH"
    elif probability >= 0.4:
        return "MEDIUM"
    else:
        return "LOW"


def get_basic_recommendation(risk_level, area):
    """Generate basic recommendation based on risk level"""
    recommendations = {
        "HIGH": f"⚠️ HIGH RISK detected in {area}. Seek immediate medical attention if you have symptoms. "
                "Consult a doctor for dengue testing. Practice strict mosquito prevention.",
        "MEDIUM": f"⚡ MEDIUM RISK in {area}. Monitor symptoms closely. "
                  "Use mosquito repellent and eliminate standing water. Consult doctor if symptoms worsen.",
        "LOW": f"✓ LOW RISK in {area}. Continue preventive measures. "
               "Stay vigilant and maintain mosquito control practices."
    }
    return recommendations.get(risk_level, "Monitor your health and practice prevention.")


def preprocess_input(data):
    """Preprocess input data for the ML model - creates one-hot encoded features"""
    try:
        # Create a dictionary with all required one-hot encoded features
        # Based on the model's feature_names_in_
        feature_data = {
            'Gender': data.get('Gender', 0),
            'Age': data.get('Age', 0),
            'NS1': data.get('NS1', 0),
            'IgG': data.get('IgG', 0),
            'IgM': data.get('IgM', 0),
            # One-hot encode Areas
            'Area_Adabor': 1 if data.get('Area') == 'Adabor' else 0,
            'Area_Badda': 1 if data.get('Area') == 'Badda' else 0,
            'Area_Banasree': 1 if data.get('Area') == 'Banasree' else 0,
            'Area_Bangshal': 1 if data.get('Area') == 'Bangshal' else 0,
            'Area_Biman Bandar': 1 if data.get('Area') == 'Biman Bandar' else 0,
            'Area_Bosila': 1 if data.get('Area') == 'Bosila' else 0,
            'Area_Cantonment': 1 if data.get('Area') == 'Cantonment' else 0,
            'Area_Chawkbazar': 1 if data.get('Area') == 'Chawkbazar' else 0,
            'Area_Demra': 1 if data.get('Area') == 'Demra' else 0,
            'Area_Dhanmondi': 1 if data.get('Area') == 'Dhanmondi' else 0,
            'Area_Gendaria': 1 if data.get('Area') == 'Gendaria' else 0,
            'Area_Gulshan': 1 if data.get('Area') == 'Gulshan' else 0,
            'Area_Hazaribagh': 1 if data.get('Area') == 'Hazaribagh' else 0,
            'Area_Jatrabari': 1 if data.get('Area') == 'Jatrabari' else 0,
            'Area_Kadamtali': 1 if data.get('Area') == 'Kadamtali' else 0,
            'Area_Kafrul': 1 if data.get('Area') == 'Kafrul' else 0,
            'Area_Kalabagan': 1 if data.get('Area') == 'Kalabagan' else 0,
            'Area_Kamrangirchar': 1 if data.get('Area') == 'Kamrangirchar' else 0,
            'Area_Keraniganj': 1 if data.get('Area') == 'Keraniganj' else 0,
            'Area_Khilgaon': 1 if data.get('Area') == 'Khilgaon' else 0,
            'Area_Khilkhet': 1 if data.get('Area') == 'Khilkhet' else 0,
            'Area_Lalbagh': 1 if data.get('Area') == 'Lalbagh' else 0,
            'Area_Mirpur': 1 if data.get('Area') == 'Mirpur' else 0,
            'Area_Mohammadpur': 1 if data.get('Area') == 'Mohammadpur' else 0,
            'Area_Motijheel': 1 if data.get('Area') == 'Motijheel' else 0,
            'Area_New Market': 1 if data.get('Area') == 'New Market' else 0,
            'Area_Pallabi': 1 if data.get('Area') == 'Pallabi' else 0,
            'Area_Paltan': 1 if data.get('Area') == 'Paltan' else 0,
            'Area_Ramna': 1 if data.get('Area') == 'Ramna' else 0,
            'Area_Rampura': 1 if data.get('Area') == 'Rampura' else 0,
            'Area_Sabujbagh': 1 if data.get('Area') == 'Sabujbagh' else 0,
            'Area_Shahbagh': 1 if data.get('Area') == 'Shahbagh' else 0,
            'Area_Sher-e-Bangla Nagar': 1 if data.get('Area') == 'Sher-e-Bangla Nagar' else 0,
            'Area_Shyampur': 1 if data.get('Area') == 'Shyampur' else 0,
            'Area_Sutrapur': 1 if data.get('Area') == 'Sutrapur' else 0,
            'Area_Tejgaon': 1 if data.get('Area') == 'Tejgaon' else 0,
            # One-hot encode AreaType
            'AreaType_Developed': 1 if data.get('AreaType') == 'Developed' else 0,
            'AreaType_Undeveloped': 1 if data.get('AreaType') == 'Undeveloped' else 0,
            # One-hot encode District
            'District_Dhaka': 1 if data.get('District') == 'Dhaka' else 0,
            # One-hot encode HouseType
            'HouseType_Building': 1 if data.get('HouseType') == 'Building' else 0,
            'HouseType_Other': 1 if data.get('HouseType') == 'Other' else 0,
            'HouseType_Tinshed': 1 if data.get('HouseType') == 'Tinshed' else 0,
        }
        
        # Create DataFrame in the exact order the model expects
        feature_df = pd.DataFrame([feature_data])
        
        # Ensure columns are in the correct order (matching model.feature_names_in_)
        expected_columns = [
            'Gender', 'Age', 'NS1', 'IgG', 'IgM',
            'Area_Adabor', 'Area_Badda', 'Area_Banasree', 'Area_Bangshal',
            'Area_Biman Bandar', 'Area_Bosila', 'Area_Cantonment', 'Area_Chawkbazar',
            'Area_Demra', 'Area_Dhanmondi', 'Area_Gendaria', 'Area_Gulshan',
            'Area_Hazaribagh', 'Area_Jatrabari', 'Area_Kadamtali', 'Area_Kafrul',
            'Area_Kalabagan', 'Area_Kamrangirchar', 'Area_Keraniganj',
            'Area_Khilgaon', 'Area_Khilkhet', 'Area_Lalbagh', 'Area_Mirpur',
            'Area_Mohammadpur', 'Area_Motijheel', 'Area_New Market', 'Area_Pallabi',
            'Area_Paltan', 'Area_Ramna', 'Area_Rampura', 'Area_Sabujbagh',
            'Area_Shahbagh', 'Area_Sher-e-Bangla Nagar', 'Area_Shyampur',
            'Area_Sutrapur', 'Area_Tejgaon',
            'AreaType_Developed', 'AreaType_Undeveloped',
            'District_Dhaka',
            'HouseType_Building', 'HouseType_Other', 'HouseType_Tinshed'
        ]
        
        feature_df = feature_df[expected_columns]
        
        return feature_df
        
    except Exception as e:
        print(f"Error in preprocessing: {e}")
        print(traceback.format_exc())
        raise


@app.route('/')
def index():
    """Serve the frontend HTML"""
    return send_from_directory('.', 'index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """ML prediction endpoint"""
    try:
        # Get JSON data
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Validate required fields
        required_fields = ['Age', 'Gender', 'Area', 'District', 'AreaType', 'HouseType']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Missing required fields: {missing_fields}'}), 400
        
        if model is None:
            return jsonify({'error': 'ML model not loaded'}), 500
        
        # Preprocess input
        features = preprocess_input(data)
        
        # Make prediction
        probability = float(model.predict_proba(features)[0][1])
        risk_level = get_risk_level(probability)
        recommendation = get_basic_recommendation(risk_level, data.get('Area', 'your area'))
        
        # Prepare response
        response = {
            'probability': round(probability, 3),
            'risk_level': risk_level,
            'recommendation': recommendation,
            'key_factors': {
                'Age': data.get('Age'),
                'Location': f"{data.get('Area')}, {data.get('District')}",
                'Test_Results': f"NS1: {'Positive' if data.get('NS1') else 'Negative'}, "
                               f"IgG: {'Positive' if data.get('IgG') else 'Negative'}, "
                               f"IgM: {'Positive' if data.get('IgM') else 'Negative'}"
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Prediction error: {e}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


@app.route('/chat', methods=['POST'])
def chat():
    """AI chat endpoint using Google Gemini"""
    try:
        if not GOOGLE_API_KEY:
            return jsonify({
                'response': 'AI chat is not configured. Please add your GOOGLE_API_KEY to the .env file.',
                'conversation_history': []
            }), 503
        
        # Get chat data
        data = request.get_json()
        user_message = data.get('message', '')
        conversation_history = data.get('conversation_history', [])
        risk_assessment = data.get('risk_assessment', None)
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Build context for Gemini
        system_context = """You are a helpful medical AI assistant specializing in dengue fever. 
You provide accurate, compassionate health advice while emphasizing the importance of professional medical care.

Key Guidelines:
- Provide clear, actionable health advice
- Always recommend consulting healthcare professionals for serious symptoms
- Be empathetic and supportive
- Include preventive measures when relevant
- Format your responses with clear structure using bullet points when appropriate
"""
        
        # Add risk assessment context if available
        if risk_assessment:
            context_msg = f"""
Current Patient Assessment:
- Risk Level: {risk_assessment.get('risk_level', 'Unknown')}
- Risk Probability: {int(risk_assessment.get('probability', 0) * 100)}%
- Age: {risk_assessment.get('age')} years
- Gender: {risk_assessment.get('gender')}
- Test Results: NS1 {risk_assessment.get('ns1')}, IgG {risk_assessment.get('igg')}, IgM {risk_assessment.get('igm')}
- Location: {risk_assessment.get('area')}, {risk_assessment.get('district')}

Based on this assessment, provide personalized advice.
"""
            system_context += context_msg
        
        # Build conversation for Gemini
        full_prompt = system_context + "\n\nUser: " + user_message
        
        # Get response from Gemini
        response = gemini_model.generate_content(full_prompt)
        ai_response = response.text
        
        # Update conversation history
        conversation_history.append({
            'role': 'user',
            'content': user_message
        })
        conversation_history.append({
            'role': 'assistant',
            'content': ai_response
        })
        
        # Keep only last 10 messages to manage context
        if len(conversation_history) > 10:
            conversation_history = conversation_history[-10:]
        
        return jsonify({
            'response': ai_response,
            'conversation_history': conversation_history
        })
        
    except Exception as e:
        print(f"Chat error: {e}")
        print(traceback.format_exc())
        return jsonify({
            'response': f'Sorry, I encountered an error: {str(e)}',
            'conversation_history': conversation_history
        }), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None,
        'ai_configured': GOOGLE_API_KEY is not None
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🦟 Dengue Risk Prediction System - Simplified Version")
    print("="*60)
    print("\n📊 Status:")
    print(f"   ML Model: {'✅ Loaded' if model else '❌ Not loaded'}")
    print(f"   AI Agent: {'✅ Configured' if GOOGLE_API_KEY else '❌ Not configured'}")
    print("\n🌐 Server starting...")
    print("   URL: http://localhost:5000")
    print("   API Health: http://localhost:5000/health")
    print("\n💡 Press Ctrl+C to stop the server")
    print("="*60 + "\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
