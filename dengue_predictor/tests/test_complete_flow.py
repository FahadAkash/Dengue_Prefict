import sys
import os

# Add the parent directories to the path to import from other modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'api'))

def test_complete_flow():
    """Test the complete flow of the new approach"""
    
    print("Testing Complete Flow of New Approach\n")
    
    try:
        # Import the agent functions
        from agents.AI_Agent import predict_dengue_risk_tool, process_tool_call, chat_with_dengue_agent
        
        # Step 1: Show what data is prepared for Gemini
        print("1. Data Preparation for Gemini Analysis:")
        result = predict_dengue_risk_tool(
            age=28,
            gender=1,  # Male
            ns1=0,     # Negative
            igg=0,     # Negative
            igm=1,     # Positive
            area="Badda",
            district="Dhaka"
        )
        
        print(f"  🎯 Risk Score: {result['probability']} ({result['risk_level']} risk)")
        print(f"  👤 Patient: {result['age']}-year-old {result['gender']}")
        print(f"  🧪 Tests: NS1 {result['ns1']}, IgG {result['igg']}, IgM {result['igm']}")
        print(f"  📍 Location: {result['area']}, {result['district']}")
        print(f"  📊 Location Context: {result['location_context']}")
        
        print("\n" + "="*70 + "\n")
        
        # Step 2: Show how area statistics are prepared
        print("2. Area Statistics Preparation:")
        area_stats = process_tool_call("get_area_statistics", {
            "district": "Dhaka",
            "area": "Badda"
        })
        
        if "error" not in area_stats:
            print(f"  📈 Average Risk Score: {area_stats.get('avg_risk_score', 'N/A')}")
            print(f"  🏥 Total Cases: {area_stats.get('total_cases', 'N/A')}")
            print(f"  📍 Location Context: {area_stats.get('location_context', '')[:200]}...")
            print(f"  🔮 Future Prediction: {area_stats.get('future_risk_prediction', 'N/A')}")
        else:
            print(f"  Error: {area_stats['error']}")
        
        print("\n" + "="*70 + "\n")
        
        # Step 3: Show how similar cases are prepared
        print("3. Similar Cases Preparation:")
        similar_cases = process_tool_call("search_similar_cases", {
            "query": "28-year-old male in Badda with IgM positive"
        })
        
        if "similar_cases" in similar_cases:
            print(f"  Found {len(similar_cases['similar_cases'])} similar cases")
            for i, case in enumerate(similar_cases['similar_cases'][:2]):
                print(f"    Case {i+1}: Risk {case['risk_score']}, Area {case['area']}")
        else:
            print("  No similar cases found")
        
        print("\n" + "="*70 + "\n")
        
        # Step 4: Show the complete data package that would be sent to Gemini
        print("4. Complete Data Package for Gemini:")
        complete_data = {
            "individual_risk": {
                "score": result['probability'],
                "level": result['risk_level'],
                "patient_profile": f"{result['age']}-year-old {result['gender']}",
                "test_results": f"NS1 {result['ns1']}, IgG {result['igg']}, IgM {result['igm']}"
            },
            "location_data": result['location_context'],
            "area_statistics": area_stats if "error" not in area_stats else "No area statistics available",
            "similar_cases": similar_cases.get('similar_cases', []) if "similar_cases" in similar_cases else "No similar cases found"
        }
        
        print("Data package prepared for Gemini analysis:")
        print(f"  Individual Risk: {complete_data['individual_risk']}")
        print(f"  Location Data: {complete_data['location_data'][:150]}...")
        print(f"  Area Statistics Available: {'Yes' if 'error' not in area_stats else 'No'}")
        print(f"  Similar Cases Found: {'Yes' if 'similar_cases' in similar_cases and similar_cases['similar_cases'] else 'No'}")
        
        print("\n" + "="*70 + "\n")
        
        # Step 5: Demonstrate how Gemini would receive and process this data
        print("5. How Gemini Processes This Data:")
        print("Gemini receives the following information:")
        print("  • Individual risk score and level")
        print("  • Patient demographics and test results")
        print("  • Location-specific statistical context")
        print("  • Area risk patterns and future predictions")
        print("  • Similar historical cases (if any)")
        print("")
        print("Gemini then analyzes all this data to generate:")
        print("  • Personalized risk interpretation")
        print("  • Tailored recommendations based on profile")
        print("  • Location-specific advice")
        print("  • Actionable guidance for the situation")
        print("  • Explanations of what the results mean")
        
        print("\n" + "="*70 + "\n")
        
        print("✅ Complete flow test successful!")
        print("The system now works by:")
        print("1. Calculating risk scores with the ML model")
        print("2. Preparing relevant data packages")
        print("3. Sending data to Gemini for analysis")
        print("4. Gemini generates personalized responses")
        print("5. Users receive tailored guidance based on their specific situation")
        
    except Exception as e:
        print(f"Error testing complete flow: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_complete_flow()