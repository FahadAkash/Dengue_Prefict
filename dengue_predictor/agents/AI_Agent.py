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
    
    # Enhanced system prompt that lets Gemini generate responses based on data
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
    - Suggest nearby healthcare facilities and government resources
    - Recommend specific foods and dietary supplements
    - Provide information about local market availability for prevention items
    
    Always be clear, actionable, and evidence-based in your responses.
    Focus on helping the user understand their situation and what they should do.
    
    When risk assessment context is provided, use it to give highly personalized advice.
    Include specific recommendations based on the risk level, patient demographics, and location.
    
    Structure your responses in a clear, organized format with:
    1. Risk Level Analysis
    2. Immediate Actions Required
    3. Dietary Recommendations
    4. Lifestyle Modifications
    5. Prevention Measures
    6. Medical Guidance
    7. Local Resources (if requested)
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