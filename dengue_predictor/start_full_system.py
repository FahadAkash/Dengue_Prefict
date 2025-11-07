#!/usr/bin/env python3
"""
Startup script for the complete Dengue Risk Prediction System
This script will start both the backend API (port 8001) and frontend server (port 8000)
"""

import os
import sys
import subprocess
import time
import threading
import webbrowser

def start_backend():
    """Start the backend API server on port 8001"""
    try:
        # Change to the api directory
        api_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'api')
        print(f"Starting backend API server in: {api_dir}")
        
        # Start the backend server
        backend_process = subprocess.Popen([
            sys.executable, '-m', 'uvicorn', 'BaseAPI:app', '--host', 'localhost', '--port', '8001'
        ], cwd=api_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        return backend_process
    except Exception as e:
        print(f"Error starting backend server: {e}")
        return None

def start_frontend():
    """Start the frontend server on port 8000"""
    try:
        # Change to the frontend directory
        frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend')
        print(f"Starting frontend server in: {frontend_dir}")
        
        # Start the frontend server
        frontend_process = subprocess.Popen([
            sys.executable, 'server.py'
        ], cwd=frontend_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        return frontend_process
    except Exception as e:
        print(f"Error starting frontend server: {e}")
        return None

def open_browser():
    """Open the browser after a short delay"""
    # Wait for servers to start
    time.sleep(5)
    
    # Open browser
    try:
        webbrowser.open('http://localhost:8000')
        print("Opening browser at http://localhost:8000")
    except Exception as e:
        print(f"Could not open browser automatically: {e}")
        print("Please manually navigate to http://localhost:8000")

def main():
    """Main function to start everything"""
    print("=" * 60)
    print("DENGUE RISK PREDICTOR - COMPLETE SYSTEM STARTUP")
    print("=" * 60)
    print("Ports configuration:")
    print("  - Frontend server: http://localhost:8000")
    print("  - Backend API: http://localhost:8001")
    print("=" * 60)
    
    backend_process = None
    frontend_process = None
    
    try:
        # Start the backend server
        print("Starting backend API server...")
        backend_process = start_backend()
        if not backend_process:
            print("Failed to start backend server")
            return
            
        # Start the frontend server
        print("Starting frontend server...")
        frontend_process = start_frontend()
        if not frontend_process:
            print("Failed to start frontend server")
            if backend_process:
                backend_process.terminate()
            return
            
        # Open browser in a separate thread
        browser_thread = threading.Thread(target=open_browser)
        browser_thread.daemon = True
        browser_thread.start()
        
        print("\n" + "=" * 60)
        print("SYSTEM IS NOW RUNNING!")
        print("=" * 60)
        print("Frontend URL: http://localhost:8000")
        print("Backend API URL: http://localhost:8001")
        print("Press Ctrl+C to stop both servers")
        print("=" * 60)
        
        # Wait for both processes
        while True:
            if backend_process.poll() is not None:
                print("Backend server has stopped")
                break
            if frontend_process.poll() is not None:
                print("Frontend server has stopped")
                break
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down servers...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean shutdown
        if backend_process:
            try:
                backend_process.terminate()
                backend_process.wait(timeout=5)
                print("Backend server stopped.")
            except subprocess.TimeoutExpired:
                backend_process.kill()
                print("Backend server force killed.")
                
        if frontend_process:
            try:
                frontend_process.terminate()
                frontend_process.wait(timeout=5)
                print("Frontend server stopped.")
            except subprocess.TimeoutExpired:
                frontend_process.kill()
                print("Frontend server force killed.")

if __name__ == "__main__":
    main()