import requests
import time

def test_server():
    """Test if the server is serving files correctly"""
    try:
        # Test accessing the main page
        print("Testing server access...")
        response = requests.get('http://localhost:8000', timeout=5)
        print(f"Status Code: {response.status_code}")
        print(f"Content Length: {len(response.text)}")
        print(f"Content Preview: {response.text[:100]}...")
        
        if response.status_code == 200:
            print("✅ Server is serving files correctly!")
        else:
            print("❌ Server returned an error")
            
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to server. Make sure it's running on port 8000")
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_server()