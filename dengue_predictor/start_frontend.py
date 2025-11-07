#!/usr/bin/env python3
"""
Startup script for the Dengue Risk Predictor Frontend
This script will start the web server and open the browser automatically
"""

import os
import sys
import webbrowser
import time
import subprocess
import threading

def main():
    """Main function to start everything"""
    print("=" * 50)
    print("DENGUE RISK PREDICTOR - FRONTEND STARTUP")
    print("=" * 50)
    
    # Get the frontend directory
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend')
    server_script = os.path.join(frontend_dir, 'server.py')
    
    print(f"Frontend directory: {frontend_dir}")
    print(f"Server script: {server_script}")
    
    # Check if files exist
    if not os.path.exists(frontend_dir):
        print("Error: Frontend directory not found!")
        return
        
    if not os.path.exists(server_script):
        print("Error: Server script not found!")
        return
    
    server_process = None
    try:
        # Start the server
        print("Starting Dengue Risk Predictor Frontend Server...")
        server_process = subprocess.Popen([
            sys.executable, 'server.py'
        ], cwd=frontend_dir)
        
        # Wait a moment for server to start
        time.sleep(2)
        
        # Open browser
        try:
            webbrowser.open('http://localhost:8000')
            print("Opening browser at http://localhost:8000")
        except Exception as e:
            print(f"Could not open browser automatically: {e}")
            print("Please manually navigate to http://localhost:8000")
        
        print("\nServer is running. Press Ctrl+C to stop.")
        print("Frontend URL: http://localhost:8000")
        
        # Wait for the server process
        server_process.wait()
        
    except KeyboardInterrupt:
        print("\nShutting down server...")
        if server_process:
            server_process.terminate()
            server_process.wait()
        print("Server stopped.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()