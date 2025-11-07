#!/usr/bin/env python3
"""
Test script to verify the organized project structure works correctly
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported correctly"""
    print("Testing imports...")
    
    try:
        # Test AI Agent import
        from agents.AI_Agent import chat_with_dengue_agent
        print("✅ AI Agent import successful")
    except Exception as e:
        print(f"❌ AI Agent import failed: {e}")
        return False
    
    try:
        # Test API import
        from api.BaseAPI import app
        print("✅ API import successful")
    except Exception as e:
        print(f"❌ API import failed: {e}")
        return False
    
    try:
        # Test DB import
        from db.PineconeDB import add_case_to_vector_db
        print("✅ DB import successful")
    except Exception as e:
        print(f"❌ DB import failed: {e}")
        return False
    
    try:
        # Test core import
        import joblib
        model_path = os.path.join(os.path.dirname(__file__), 'core', 'models', 'logistic_regression_model.joblib')
        model = joblib.load(model_path)
        print("✅ Core model import successful")
    except Exception as e:
        print(f"❌ Core model import failed: {e}")
        return False
    
    return True

def main():
    """Main test function"""
    print("🧪 Testing Organized Project Structure\n")
    
    if test_imports():
        print("\n🎉 All imports successful! Project structure is working correctly.")
    else:
        print("\n❌ Some imports failed. Please check the errors above.")

if __name__ == "__main__":
    main()