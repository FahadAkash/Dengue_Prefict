import google.generativeai as genai  
import joblib
import json
import os
import sys
import pandas as pd
from collections import Counter

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

# Load dataset for statistical analysis (but not for sending to Gemini)
dataset_path = os.path.join(os.path.dirname(__file__), '..', 'datasets', 'dataset.csv')
dataset_df = None
try:
    if os.path.exists(dataset_path):
        # Load only once and keep in memory
        dataset_df = pd.read_csv(dataset_path)
        print(f"Loaded dataset with {len(dataset_df)} records for statistical analysis")
except Exception as e:
    print(f"Could not load dataset for analysis: {e}")

# Initialize Gemini Flash model with correct model name
genai.configure(api_key=api_key)
llm = genai.GenerativeModel('models/gemini-2.0-flash')

def get_location_based_stats(area, district, n_samples=50):
    """
    Get location-based statistics without sending large amounts of data to Gemini.
    Returns a summarized view of the data for the specific location.
    """
    if dataset_df is None:
        return "No historical dataset available for analysis."
    
    # Filter data for the specific area and district
    location_data = dataset_df[
        (dataset_df['Area'] == area) & 
        (dataset_df['District'] == district)
    ]
    
    if len(location_data) == 0:
        # If no exact match, try just the district
        location_data = dataset_df[dataset_df['District'] == district]
        if len(location_data) == 0:
            return "No historical data available for this location."
    
    # If we have too much data, sample it
    if len(location_data) > n_samples:
        location_data = location_data.sample(n=n_samples, random_state=42)
    
    # Calculate key statistics
    total_cases = len(location_data)
    positive_cases = location_data['Outcome'].sum()
    positive_rate = positive_cases / total_cases if total_cases > 0 else 0
    
    # Age distribution
    avg_age = location_data['Age'].mean()
    age_groups = pd.cut(location_data['Age'], bins=[0, 18, 35, 50, 100], labels=['Child', 'Young Adult', 'Adult', 'Senior'])
    age_distribution = pd.Series(age_groups).value_counts().to_dict()
    
    # Gender distribution
    gender_distribution = pd.Series(location_data['Gender']).value_counts().to_dict()
    
    # Test result patterns
    ns1_positive = location_data[location_data['NS1'] == 1].shape[0]
    igg_positive = location_data[location_data['IgG'] == 1].shape[0]
    igm_positive = location_data[location_data['IgM'] == 1].shape[0]
    
    # Area type distribution
    area_type_distribution = pd.Series(location_data['AreaType']).value_counts().to_dict()
    
    # Create a concise summary
    summary = {
        "total_cases_analyzed": total_cases,
        "dengue_positive_rate": round(positive_rate * 100, 2),
        "average_age": round(avg_age, 1),
        "age_distribution": {str(k): int(v) for k, v in age_distribution.items()},
        "gender_distribution": {str(k): int(v) for k, v in gender_distribution.items()},
        "test_patterns": {
            "ns1_positive_rate": round(ns1_positive/total_cases * 100, 2) if total_cases > 0 else 0,
            "igg_positive_rate": round(igg_positive/total_cases * 100, 2) if total_cases > 0 else 0,
            "igm_positive_rate": round(igm_positive/total_cases * 100, 2) if total_cases > 0 else 0
        },
        "area_characteristics": {str(k): int(v) for k, v in area_type_distribution.items()}
    }
    
    return summary

def create_location_context(area, district):
    """
    Create a concise context for Gemini based on location data.
    This significantly reduces token usage while preserving key insights.
    """
    stats = get_location_based_stats(area, district)
    
    if isinstance(stats, str):
        return stats  # Error message
    
    context = f"""
LOCATION ANALYSIS FOR {area}, {district}:
- Dengue Positive Rate: {stats['dengue_positive_rate']}% ({stats['total_cases_analyzed']} cases analyzed)
- Average Patient Age: {stats['average_age']} years
- Age Distribution: {stats['age_distribution']}
- Gender Distribution: {stats['gender_distribution']}
- Common Test Patterns: NS1 {stats['test_patterns']['ns1_positive_rate']}%, IgG {stats['test_patterns']['igg_positive_rate']}%, IgM {stats['test_patterns']['igm_positive_rate']}%
- Area Type: {stats['area_characteristics']}

This summary is based on statistical analysis of historical data and provides key insights 
without sending raw patient data to the AI model, significantly reducing token usage.
"""
    
    return context

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
    
    # List of all areas from the model
    all_areas = ['Adabor', 'Badda', 'Banasree', 'Bangshal', 'Biman Bandar', 'Bosila', 
                 'Cantonment', 'Chawkbazar', 'Demra', 'Dhanmondi', 'Gendaria', 'Gulshan', 
                 'Hazaribagh', 'Jatrabari', 'Kadamtali', 'Kafrul', 'Kalabagan', 'Kamrangirchar',
                 'Keraniganj', 'Khilgaon', 'Khilkhet', 'Lalbagh', 'Mirpur', 'Mohammadpur', 
                 'Motijheel', 'New Market', 'Pallabi', 'Paltan', 'Ramna', 'Rampura', 'Sabujbagh', 
                 'Shahbagh', 'Sher-e-Bangla Nagar', 'Shyampur', 'Sutrapur', 'Tejgaon']
    
    # Create a dataframe with all the required features
    # Based on the feature names we discovered
    feature_data = {
        'Gender': [gender],
        'Age': [age],
        'NS1': [ns1],
        'IgG': [igg],
        'IgM': [igm]
    }
    
    # Add area features (one-hot encoded)
    for area_name in all_areas:
        feature_data[f'Area_{area_name}'] = [1 if area == area_name else 0]
    
    # Add other categorical features
    feature_data['AreaType_Developed'] = [0]  # Default value
    feature_data['AreaType_Undeveloped'] = [1]  # Default value
    feature_data['District_Dhaka'] = [1 if district == 'Dhaka' else 0]
    feature_data['HouseType_Building'] = [1]  # Default value
    feature_data['HouseType_Other'] = [0]  # Default value
    feature_data['HouseType_Tinshed'] = [0]  # Default value
    
    # Create DataFrame
    feature_df = pd.DataFrame(feature_data)
    
    # Get probability
    probability = float(model.predict_proba(feature_df)[0][1])
    
    risk_level = "High" if probability >= 0.7 else "Medium" if probability >= 0.4 else "Low"
    
    # Get location-based context for Gemini
    location_context = create_location_context(area, district)
    
    # Return data for Gemini to analyze and generate response
    return {
        "probability": round(probability, 3),
        "risk_level": risk_level,
        "age": age,
        "gender": "Male" if gender == 1 else "Female",
        "ns1": "Positive" if ns1 == 1 else "Negative",
        "igg": "Positive" if igg == 1 else "Negative",
        "igm": "Positive" if igm == 1 else "Negative",
        "area": area,
        "district": district,
        "location_context": location_context
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
        
        # Enhance statistics with future risk predictions
        if stats:
            # Simple prediction based on current statistics
            avg_risk = stats.get("avg_risk_score", 0)
            if avg_risk >= 0.7:
                future_risk = "High risk expected to continue for the next 2-4 months. Enhanced prevention measures strongly recommended."
            elif avg_risk >= 0.4:
                future_risk = "Moderate risk likely to persist over the next 2-4 months. Maintain preventive practices."
            else:
                future_risk = "Low risk expected to continue for the next 2-4 months. Continue routine monitoring."
            
            stats["future_risk_prediction"] = future_risk
            
            # Add location context for Gemini to analyze
            location_context = create_location_context(tool_input["area"], tool_input["district"])
            stats["location_context"] = location_context
        
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
    
    # Simplified system prompt that lets Gemini generate responses based on data
    system_prompt = """You are a Dengue Intelligence Assistant helping health officials and medical staff 
    assess dengue risk and make data-driven decisions.

    You have access to:
    1. A machine learning model that predicts dengue risk based on patient data
    2. A historical database of similar cases
    3. Area-level statistics and trends
    4. Location-based statistical summaries

    Your task is to:
    - Analyze the provided dengue risk prediction data
    - Interpret the meaning of the risk score in context
    - Provide personalized recommendations based on the individual's profile
    - Use the location context to give area-specific advice
    - Explain what the test results mean for this person
    - Suggest appropriate actions based on the risk level
    - Recommend when to seek medical attention
    - Provide lifestyle, dietary, and prevention guidance
    - Offer insights about future risk patterns if relevant
    
    Always be clear, actionable, and evidence-based in your responses.
    Focus on helping the user understand their situation and what they should do.
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
