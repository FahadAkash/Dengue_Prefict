#!/usr/bin/env python3
"""
Dengue Risk Prediction System Demo
This script demonstrates all components of the system working together.
"""

import requests
import time
import sys
import os

# Add the parent directory to the path to import from agents
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))

from agents.AI_Agent import chat_with_dengue_agent

def test_api_endpoints():
    """Test all API endpoints"""
    print("=== Testing API Endpoints ===")
    
    # Test health endpoint
    print("\n1. Testing /health endpoint:")
    response = requests.get('http://127.0.0.1:8000/health')
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test stats endpoint
    print("\n2. Testing /stats endpoint:")
    response = requests.get('http://127.0.0.1:8000/stats')
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.json()}")
    
    # Test predict endpoint
    print("\n3. Testing /predict endpoint:")
    patient_data = {
        "Age": 28,
        "Gender": 1,  # Male
        "NS1": 0,     # Negative
        "IgG": 1,     # Positive
        "IgM": 1,     # Positive
        "Area": "Badda",
        "AreaType": "Urban",
        "HouseType": "Building",
        "District": "Dhaka"
    }
    
    response = requests.post('http://127.0.0.1:8000/predict', json=patient_data)
    print(f"   Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"   Probability: {result['probability']}")
        print(f"   Risk Level: {result['risk_level']}")
        print(f"   Recommendation: {result['recommendation']}")
    else:
        print(f"   Error: {response.text}")

def test_ai_agent():
    """Test the AI agent"""
    print("\n=== Testing AI Agent ===")
    
    queries = [
        "What is the dengue risk for a 28-year-old male in Badda, Dhaka with NS1 negative but IgM positive?",
        "Compare risk levels between Mirpur and Badda in Dhaka",
        "What interventions do you recommend for high-risk areas?"
    ]
    
    conversation = None
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. Query: {query}")
        response, conversation = chat_with_dengue_agent(query, conversation)
        print(f"   Response: {response[:200]}...")
        time.sleep(1)  # Small delay to avoid rate limiting

def main():
    """Run the complete demo"""
    print("🦟 Dengue Risk Prediction System Demo")
    print("=" * 50)
    
    try:
        test_api_endpoints()
        test_ai_agent()
        print("\n🎉 Demo completed successfully!")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")

if __name__ == "__main__":
    main()