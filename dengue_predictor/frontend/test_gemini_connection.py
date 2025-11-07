import sys
import os

# Add the agents directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))

# Test the AI agent connection
try:
    from AI_Agent import chat_with_dengue_agent
    
    print("Testing AI Agent Connection...")
    
    # Test a simple question
    test_message = "Should I drink coconut water if I have dengue?"
    response, history = chat_with_dengue_agent(test_message)
    
    print("Test Message:", test_message)
    print("\nAI Response:")
    print("=" * 50)
    print(response)
    print("=" * 50)
    print("\nConversation History Length:", len(history))
    
except Exception as e:
    print(f"Error testing AI agent: {e}")
    import traceback
    traceback.print_exc()