import subprocess
import sys
import os

def install_dependencies():
    """Install all required dependencies"""
    try:
        # Read requirements file from the parent directory
        requirements_path = os.path.join(os.path.dirname(__file__), '..', 'requirment.txt')
        with open(requirements_path, "r") as f:
            requirements = f.read().splitlines()
        
        # Filter out comments and empty lines
        packages = [line.strip() for line in requirements 
                   if line.strip() and not line.startswith("#")]
        
        print("Installing dependencies...")
        for package in packages:
            print(f"Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        
        print("✅ All dependencies installed successfully!")
        
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")

if __name__ == "__main__":
    install_dependencies()