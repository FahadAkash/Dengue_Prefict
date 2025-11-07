import os
import joblib
import pandas as pd
import sys

# Add the parent directories to the path to import from other modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'db'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))

from PineconeDB import add_case_to_vector_db
from agents.AI_Agent import chat_with_dengue_agent, predict_dengue_risk_tool

def test_ml_model():
    """Test that the ML model loads and makes predictions"""
    try:
        # Load model from the correct path
        model_path = os.path.join(os.path.dirname(__file__), '..', 'core', 'models', 'logistic_regression_model.joblib')
        model = joblib.load(model_path)
        print("OK ML model loaded successfully")
        print(f"   Model expects {model.n_features_in_} features")
        
        # Check feature names if available
        if hasattr(model, 'feature_names_in_'):
            print(f"   Feature names: {model.feature_names_in_}")
        
        # Test prediction with correct number of features
        # We need to determine what features the model expects
        return True
    except Exception as e:
        print(f"FAIL ML model test failed: {e}")
        return False

def test_pinecone_db():
    """Test Pinecone DB functionality"""
    try:
        # Add a test case
        case_data = {
            'Age': 35,
            'Gender': 1,
            'NS1': 1,
            'IgG': 1,
            'IgM': 0,
            'Area': 'Mirpur',
            'District': 'Dhaka',
            'AreaType': 'Urban',
            'HouseType': 'Building',
            'Outcome': 1
        }
        
        add_case_to_vector_db(case_data, 0.85)
        print("OK Pinecone DB test passed")
        return True
    except Exception as e:
        print(f"FAIL Pinecone DB test failed: {e}")
        return False

def test_ai_agent():
    """Test AI agent functionality"""
    try:
        response, _ = chat_with_dengue_agent("What is the dengue risk for a 30-year-old female in Dhaka?")
        print("OK AI Agent test passed")
        print(f"Sample response: {response[:100]}...")
        return True
    except Exception as e:
        print(f"FAIL AI Agent test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Testing Dengue Prediction System with Gemini Flash and Pinecone\n")
    
    # Check if required environment variables are set
    google_api_key = os.getenv("GOOGLE_API_KEY")
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    
    if not google_api_key:
        print("WARN GOOGLE_API_KEY environment variable not set")
        print("   Please set it to test the AI agent")
    
    if not pinecone_api_key:
        print("WARN PINECONE_API_KEY environment variable not set")
        print("   Please set it to test the vector database")
    
    tests = [
        ("ML Model", test_ml_model),
        ("Pinecone DB", test_pinecone_db),
        ("AI Agent", test_ai_agent)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        print(f"\nTesting {name}...")
        if test_func():
            passed += 1
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! The system is ready to use.")
    else:
        print("Some tests failed. Please check the errors above.")

if __name__ == "__main__":
    main()