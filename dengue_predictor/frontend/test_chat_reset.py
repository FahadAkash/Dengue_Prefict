import requests
import json

def test_chat_reset():
    """Test that chat responses are not cached"""
    
    # Test data with risk assessment context
    chat_data1 = {
        "message": "Should I drink coconut water?",
        "conversation_history": [],
        "risk_assessment": {
            "probability": 0.36,
            "risk_level": "Low",
            "age": 20,
            "gender": "Male",
            "ns1": "Positive",
            "igg": "Negative",
            "igm": "Negative",
            "area": "Badda",
            "district": "Dhaka"
        }
    }
    
    # Send first request
    print("Sending first chat request...")
    response1 = requests.post(
        'http://localhost:8000/chat',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(chat_data1)
    )
    
    if response1.status_code == 200:
        result1 = response1.json()
        print("First Response:")
        print(result1["response"][:200] + "..." if len(result1["response"]) > 200 else result1["response"])
    else:
        print(f"Error in first request: {response1.status_code}")
        print(response1.text)
        return
    
    # Send second request with same data but different question
    chat_data2 = chat_data1.copy()
    chat_data2["message"] = "What foods should I avoid?"
    
    print("\nSending second chat request with different question...")
    response2 = requests.post(
        'http://localhost:8000/chat',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(chat_data2)
    )
    
    if response2.status_code == 200:
        result2 = response2.json()
        print("Second Response:")
        print(result2["response"][:200] + "..." if len(result2["response"]) > 200 else result2["response"])
        
        # Check if responses are different
        if result1["response"] != result2["response"]:
            print("\n✅ SUCCESS: Responses are different (not cached)")
        else:
            print("\n❌ ISSUE: Responses are identical (possibly cached)")
    else:
        print(f"Error in second request: {response2.status_code}")
        print(response2.text)

if __name__ == "__main__":
    test_chat_reset()