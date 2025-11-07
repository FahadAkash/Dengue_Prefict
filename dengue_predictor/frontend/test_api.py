import requests
import json

# Test data
test_data = {
    "Age": 30,
    "Gender": 1,
    "NS1": 0,
    "IgG": 1,
    "IgM": 1,
    "Area": "Badda",
    "AreaType": "Urban",
    "HouseType": "Building",
    "District": "Dhaka"
}

# Send POST request to the API
try:
    response = requests.post(
        'http://localhost:8000/predict',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(test_data)
    )
    
    if response.status_code == 200:
        result = response.json()
        print("API Response:")
        print(json.dumps(result, indent=2))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        
except Exception as e:
    print(f"Error connecting to API: {e}")