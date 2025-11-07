import google.generativeai as genai  
import joblib
import json
import os
import sys

# Add the parent directory to the path to import from db
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'db'))

# Import from PineconeDB
try:
    from PineconeDB import search_similar_cases, get_area_statistics, add_case_to_vector_db
except ImportError:
    # If direct import fails, try with full path
    from ..db.PineconeDB import search_similar_cases, get_area_statistics, add_case_to_vector_db

# Initialize
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")

# Load model from the correct path
model_path = os.path.join(os.path.dirname(__file__), '..', 'core', 'models', 'logistic_regression_model.joblib')
model = joblib.load(model_path)

# Initialize Gemini Flash model with correct model name
genai.configure(api_key=api_key)
llm = genai.GenerativeModel('models/gemini-2.0-flash')

# Define tools for the AI agent
tools = [
    {
        "name": "predict_dengue_risk",
        "description": "Predicts dengue risk for a specific case based on patient and area data. Returns probability score and risk level.",
        "parameters": {
            "type": "object",
            "properties": {
                "age": {"type": "integer", "description": "Patient age"},
                "gender": {"type": "integer", "description": "0=Female, 1=Male"},
                "ns1": {"type": "integer", "description": "NS1 test result (0=Negative, 1=Positive)"},
                "igg": {"type": "integer", "description": "IgG antibody (0=Negative, 1=Positive)"},
                "igm": {"type": "integer", "description": "IgM antibody (0=Negative, 1=Positive)"},
                "area": {"type": "string", "description": "Area name"},
                "district": {"type": "string", "description": "District name"}
            },
            "required": ["age", "gender", "ns1", "igg", "igm", "area", "district"]
        }
    },
    {
        "name": "search_similar_cases",
        "description": "Searches historical dengue cases with similar characteristics. Useful for finding patterns and precedents.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Natural language description of case to search for"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_area_statistics",
        "description": "Gets historical dengue statistics for a specific area including average risk, case counts, and positive rates.",
        "parameters": {
            "type": "object",
            "properties": {
                "district": {"type": "string", "description": "District name"},
                "area": {"type": "string", "description": "Area name"}
            },
            "required": ["district", "area"]
        }
    }
]

def predict_dengue_risk_tool(age, gender, ns1, igg, igm, area, district):
    """Execute prediction using the ML model"""
    import numpy as np
    import pandas as pd
    
    # Create a dataframe with all the required features
    # Based on the feature names we discovered
    feature_data = {
        'Gender': [gender],
        'Age': [age],
        'NS1': [ns1],
        'IgG': [igg],
        'IgM': [igm],
        'Area_Adabor': [1 if area == 'Adabor' else 0],
        'Area_Badda': [1 if area == 'Badda' else 0],
        'Area_Banasree': [1 if area == 'Banasree' else 0],
        'Area_Bangshal': [1 if area == 'Bangshal' else 0],
        'Area_Biman Bandar': [1 if area == 'Biman Bandar' else 0],
        'Area_Bosila': [1 if area == 'Bosila' else 0],
        'Area_Cantonment': [1 if area == 'Cantonment' else 0],
        'Area_Chawkbazar': [1 if area == 'Chawkbazar' else 0],
        'Area_Demra': [1 if area == 'Demra' else 0],
        'Area_Dhanmondi': [1 if area == 'Dhanmondi' else 0],
        'Area_Gendaria': [1 if area == 'Gendaria' else 0],
        'Area_Gulshan': [1 if area == 'Gulshan' else 0],
        'Area_Hazaribagh': [1 if area == 'Hazaribagh' else 0],
        'Area_Jatrabari': [1 if area == 'Jatrabari' else 0],
        'Area_Kadamtali': [1 if area == 'Kadamtali' else 0],
        'Area_Kafrul': [1 if area == 'Kafrul' else 0],
        'Area_Kalabagan': [1 if area == 'Kalabagan' else 0],
        'Area_Kamrangirchar': [1 if area == 'Kamrangirchar' else 0],
        'Area_Keraniganj': [1 if area == 'Keraniganj' else 0],
        'Area_Khilgaon': [1 if area == 'Khilgaon' else 0],
        'Area_Khilkhet': [1 if area == 'Khilkhet' else 0],
        'Area_Lalbagh': [1 if area == 'Lalbagh' else 0],
        'Area_Mirpur': [1 if area == 'Mirpur' else 0],
        'Area_Mohammadpur': [1 if area == 'Mohammadpur' else 0],
        'Area_Motijheel': [1 if area == 'Motijheel' else 0],
        'Area_New Market': [1 if area == 'New Market' else 0],
        'Area_Pallabi': [1 if area == 'Pallabi' else 0],
        'Area_Paltan': [1 if area == 'Paltan' else 0],
        'Area_Ramna': [1 if area == 'Ramna' else 0],
        'Area_Rampura': [1 if area == 'Rampura' else 0],
        'Area_Sabujbagh': [1 if area == 'Sabujbagh' else 0],
        'Area_Shahbagh': [1 if area == 'Shahbagh' else 0],
        'Area_Sher-e-Bangla Nagar': [1 if area == 'Sher-e-Bangla Nagar' else 0],
        'Area_Shyampur': [1 if area == 'Shyampur' else 0],
        'Area_Sutrapur': [1 if area == 'Sutrapur' else 0],
        'Area_Tejgaon': [1 if area == 'Tejgaon' else 0],
        'AreaType_Developed': [0],  # Default value
        'AreaType_Undeveloped': [1],  # Default value
        'District_Dhaka': [1 if district == 'Dhaka' else 0],
        'HouseType_Building': [1],  # Default value
        'HouseType_Other': [0],  # Default value
        'HouseType_Tinshed': [0]  # Default value
    }
    
    # Create DataFrame
    feature_df = pd.DataFrame(feature_data)
    
    # Get probability
    probability = float(model.predict_proba(feature_df)[0][1])
    
    risk_level = "High" if probability >= 0.7 else "Medium" if probability >= 0.4 else "Low"
    
    return {
        "probability": round(probability, 3),
        "risk_level": risk_level,
        "area": area,
        "district": district
    }

def process_tool_call(tool_name, tool_input):
    """Route tool calls to appropriate functions"""
    
    if tool_name == "predict_dengue_risk":
        return predict_dengue_risk_tool(**tool_input)
    
    elif tool_name == "search_similar_cases":
        results = search_similar_cases(tool_input["query"], n_results=3)
        matches = results.get('matches', [])
        return {
            "similar_cases": [
                {
                    "description": match['metadata'].get('description', '')[:200],
                    "risk_score": match['metadata'].get('risk_score', 0),
                    "outcome": match['metadata'].get('outcome', 0),
                    "area": match['metadata'].get('area', ''),
                    "district": match['metadata'].get('district', '')
                }
                for match in matches
            ]
        }
    
    elif tool_name == "get_area_statistics":
        stats = get_area_statistics(
            tool_input["district"],
            tool_input["area"]
        )
        return stats or {"error": "No historical data found for this area"}

def chat_with_dengue_agent(user_message, conversation_history=None):
    """
    Main chat interface with the AI agent
    """
    if conversation_history is None:
        conversation_history = []
    
    # Add user message
    conversation_history.append({
        "role": "user",
        "content": user_message
    })
    
    # System prompt
    system_prompt = """You are a Dengue Intelligence Assistant helping health officials and medical staff 
    assess dengue risk and make data-driven decisions.

    You have access to:
    1. A machine learning model that predicts dengue risk based on patient data
    2. A historical database of similar cases
    3. Area-level statistics and trends

    When answering:
    - Be clear and actionable
    - Cite risk scores and statistics
    - Provide specific recommendations
    - Explain your reasoning
    - Use the tools to gather data before responding
    """
    
    full_prompt = system_prompt + "\nUser query: " + user_message
    
    # Call Gemini Flash
    try:
        response = llm.generate_content(full_prompt)
        final_response = response.text
    except Exception as e:
        final_response = f"Error generating response: {str(e)}"
    
    # Add to history
    conversation_history.append({
        "role": "assistant",
        "content": final_response
    })
    
    return final_response, conversation_history

# Example usage
if __name__ == "__main__":
    print("🦟 Dengue Intelligence Agent Started\n")
    
    # Example queries
    queries = [
        "What's the dengue risk for a 28-year-old male in Badda, Dhaka with NS1 negative but IgM positive?",
        "Compare risk levels between Mirpur and Badda in Dhaka",
        "What interventions do you recommend for high-risk areas?"
    ]
    
    conversation = None
    
    for query in queries:
        print(f"\n{'='*60}")
        print(f"🗣️  User: {query}")
        print(f"{'='*60}")
        
        response, conversation = chat_with_dengue_agent(query, conversation)
        
        print(f"\n🤖 Agent: {response}\n")