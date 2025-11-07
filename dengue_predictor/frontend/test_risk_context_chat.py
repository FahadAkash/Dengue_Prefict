import requests
import json

# Test chat functionality with risk assessment context
def test_risk_context_chat():
    # Test data with risk assessment context
    chat_data = {
        "message": "What specific foods should I eat given my risk level?",
        "conversation_history": [],
        "risk_assessment": {
            "probability": 0.75,
            "risk_level": "High",
            "age": 35,
            "gender": "Male",
            "ns1": "Positive",
            "igg": "Positive",
            "igm": "Negative",
            "area": "Badda",
            "district": "Dhaka"
        }
    }
    
    # Send POST request to the chat endpoint
    try:
        response = requests.post(
            'http://localhost:8000/chat',
            headers={'Content-Type': 'application/json'},
            data=json.dumps(chat_data)
        )
        
        if response.status_code == 200:
            result = response.json()
            print("Chat Response with Risk Context:")
            print(json.dumps(result, indent=2))
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error connecting to chat API: {e}")

if __name__ == "__main__":
    test_risk_context_chat()