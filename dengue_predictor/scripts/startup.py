import os
import subprocess
import sys

# Add the parent directories to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents'))

def check_env_vars():
    """Check if required environment variables are set"""
    google_api_key = os.getenv("GOOGLE_API_KEY")
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    
    missing_vars = []
    if not google_api_key:
        missing_vars.append("GOOGLE_API_KEY")
    if not pinecone_api_key:
        missing_vars.append("PINECONE_API_KEY")
    
    if missing_vars:
        print("⚠️  Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nPlease set these variables in your .env file or environment.")
        return False
    
    return True

def run_tests():
    """Run system tests"""
    print("🧪 Running system tests...")
    try:
        # Run test from the tests directory
        result = subprocess.run([sys.executable, "-m", "tests.test_system"], 
                              capture_output=True, text=True, cwd=os.path.join(os.path.dirname(__file__), '..'))
        print(result.stdout)
        if result.stderr:
            print("Errors:", result.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def start_api():
    """Start the FastAPI server"""
    print("🚀 Starting FastAPI server...")
    try:
        # Run API from the api directory
        subprocess.run([sys.executable, "-m", "uvicorn", "api.BaseAPI:app", "--reload"], 
                      cwd=os.path.join(os.path.dirname(__file__), '..'))
    except Exception as e:
        print(f"❌ Error starting API: {e}")

def main():
    """Main startup function"""
    print("🦟 Dengue Risk Prediction System Startup")
    print("=" * 50)
    
    # Check environment variables
    if not check_env_vars():
        response = input("\nContinue anyway? (y/N): ")
        if response.lower() != 'y':
            return
    
    # Run tests
    print("\n1. Running system tests...")
    if run_tests():
        print("✅ Tests passed!")
    else:
        print("❌ Tests failed!")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            return
    
    # Ask user what to do next
    print("\n2. What would you like to do?")
    print("   1. Start FastAPI server")
    print("   2. Run AI agent demo")
    print("   3. Exit")
    
    choice = input("Enter choice (1-3): ")
    
    if choice == "1":
        start_api()
    elif choice == "2":
        print("🤖 Starting AI agent demo...")
        try:
            from agents.AI_Agent import chat_with_dengue_agent
            conversation = None
            while True:
                query = input("\n🗣️  Ask a question (or 'quit' to exit): ")
                if query.lower() == 'quit':
                    break
                response, conversation = chat_with_dengue_agent(query, conversation)
                print(f"\n🤖 Agent: {response}")
        except Exception as e:
            print(f"❌ Error running AI agent: {e}")
    elif choice == "3":
        print("👋 Goodbye!")
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()