import os
import google.generativeai as genai
from pinecone import Pinecone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_google_api():
    """Test Google Gemini Flash API key"""
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ GOOGLE_API_KEY not found in environment variables")
            return False
            
        genai.configure(api_key=api_key)
        
        # Use a working model from the list
        model = genai.GenerativeModel('models/gemini-2.0-flash')
        
        # Test the model
        response = model.generate_content("Explain how AI works in a few words")
        print("✅ Google Gemini Flash API test passed")
        print(f"   Sample response: {response.text[:100]}...")
        return True
    except Exception as e:
        print(f"❌ Google Gemini Flash API test failed: {e}")
        return False

def test_pinecone_api():
    """Test Pinecone API key"""
    try:
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            print("❌ PINECONE_API_KEY not found in environment variables")
            return False
            
        # Use the correct initialization method
        pc = Pinecone(api_key=api_key)
        indexes = pc.list_indexes()
        print("✅ Pinecone API test passed")
        print(f"   Available indexes: {indexes.names()}")
        return True
    except Exception as e:
        print(f"❌ Pinecone API test failed: {e}")
        return False

def main():
    """Test both API keys"""
    print("🧪 Testing API Keys\n")
    
    tests = [
        ("Google Gemini Flash", test_google_api),
        ("Pinecone", test_pinecone_api)
    ]
    
    passed = 0
    total = len(tests)
    
    for name, test_func in tests:
        print(f"🔍 Testing {name} API...")
        if test_func():
            passed += 1
    
    print(f"\n🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All API tests passed! Your keys are working correctly.")
    else:
        print("⚠️  Some API tests failed. Please check your keys.")

if __name__ == "__main__":
    main()