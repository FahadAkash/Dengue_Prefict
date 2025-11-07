import requests
import json

# Test chat functionality
def test_chat():
    # Test data
    chat_data = {
        "message": "What should I do if I have a high dengue risk?",
        "conversation_history": []
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
            print("Chat Response:")
            print(json.dumps(result, indent=2))
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error connecting to chat API: {e}")

if __name__ == "__main__":
    test_chat()