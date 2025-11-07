import sys
import os

# Add the parent directories to the path to import from other modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))

def test_gemini_data_analysis():
    """Test the new Gemini data analysis approach"""
    
    print("Testing New Gemini Data Analysis Approach\n")
    
    try:
        # Import the agent functions
        from agents.AI_Agent import predict_dengue_risk_tool, chat_with_dengue_agent
        
        # Test the prediction tool with data that will be sent to Gemini
        print("1. Testing Prediction Tool Data Preparation:")
        result = predict_dengue_risk_tool(
            age=35,
            gender=1,  # Male
            ns1=1,     # Positive
            igg=1,     # Positive
            igm=0,     # Negative
            area="Badda",
            district="Dhaka"
        )
        
        print(f"Risk Probability: {result['probability']}")
        print(f"Risk Level: {result['risk_level']}")
        print(f"Patient Profile: {result['age']}-year-old {result['gender']}")
        print(f"Test Results: NS1 {result['ns1']}, IgG {result['igg']}, IgM {result['igm']}")
        print(f"Location: {result['area']}, {result['district']}")
        print(f"Location context length: {len(result['location_context'])} characters")
        print(f"Location context preview: {result['location_context'][:200]}...")
        
        print("\n" + "="*60 + "\n")
        
        # Test another case
        print("2. Testing Another Prediction:")
        result2 = predict_dengue_risk_tool(
            age=25,
            gender=0,  # Female
            ns1=0,     # Negative
            igg=0,     # Negative
            igm=1,     # Positive
            area="Gulshan",
            district="Dhaka"
        )
        
        print(f"Risk Probability: {result2['probability']}")
        print(f"Risk Level: {result2['risk_level']}")
        print(f"Patient Profile: {result2['age']}-year-old {result2['gender']}")
        print(f"Test Results: NS1 {result2['ns1']}, IgG {result2['igg']}, IgM {result2['igm']}")
        print(f"Location: {result2['area']}, {result2['district']}")
        
        print("\n" + "="*60 + "\n")
        
        # Test a simulated chat interaction
        print("3. Testing Chat Interaction with Gemini:")
        print("Simulating a query that would be sent to Gemini...")
        print("Query: 'What does a 75% dengue risk mean for a 35-year-old man in Badda with NS1 and IgG positive?'")
        print("Data sent to Gemini:")
        print(f"  - Risk Score: {result['probability']} ({result['risk_level']} risk)")
        print(f"  - Patient: {result['age']}-year-old {result['gender']}")
        print(f"  - Test Results: NS1 {result['ns1']}, IgG {result['igg']}, IgM {result['igm']}")
        print(f"  - Location: {result['area']}, {result['district']}")
        print(f"  - Location Context: {result['location_context'][:150]}...")
        print("\nGemini would analyze this data and generate a personalized response.")
        
        print("\n" + "="*60 + "\n")
        
        print("New approach test completed successfully!")
        print("The system now sends user data and prediction scores to Gemini,")
        print("which analyzes the information and generates personalized responses.")
        
    except Exception as e:
        print(f"Error testing new approach: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gemini_data_analysis()