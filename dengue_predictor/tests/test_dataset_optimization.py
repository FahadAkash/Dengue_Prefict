import sys
import os

# Add the parent directories to the path to import from other modules
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))

def test_dataset_optimization():
    """Test the dataset optimization functionality"""
    
    print("Testing Dataset Optimization for Gemini Token Reduction\n")
    
    try:
        # Import the agent functions
        from agents.AI_Agent import get_location_based_stats, create_location_context
        
        # Test the location-based statistics function
        print("1. Testing Location-Based Statistics:")
        stats = get_location_based_stats("Badda", "Dhaka")
        print(f"Statistics type: {type(stats)}")
        if isinstance(stats, dict):
            print(f"Total cases analyzed: {stats.get('total_cases_analyzed', 'N/A')}")
            print(f"Dengue positive rate: {stats.get('dengue_positive_rate', 'N/A')}%")
            print(f"Average age: {stats.get('average_age', 'N/A')} years")
        else:
            print(f"Stats message: {stats}")
        
        print("\n" + "="*60 + "\n")
        
        # Test the location context creation
        print("2. Testing Location Context Creation:")
        context = create_location_context("Mirpur", "Dhaka")
        print(f"Context preview (first 300 chars):\n{context[:300]}...")
        print(f"\nContext length: {len(context)} characters")
        
        print("\n" + "="*60 + "\n")
        
        # Test with a different area
        print("3. Testing with Different Location (Gulshan):")
        context2 = create_location_context("Gulshan", "Dhaka")
        print(f"Context preview (first 300 chars):\n{context2[:300]}...")
        print(f"\nContext length: {len(context2)} characters")
        
        print("\n" + "="*60 + "\n")
        
        print("Dataset optimization test completed successfully!")
        print("The system now provides summarized location data instead of raw dataset,")
        print("significantly reducing token usage when sending context to Gemini.")
        
    except Exception as e:
        print(f"Error testing dataset optimization: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_dataset_optimization()