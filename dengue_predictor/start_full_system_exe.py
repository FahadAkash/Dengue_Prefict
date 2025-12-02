#!/usr/bin/env python3
"""
Executable version of the startup script for the Dengue Risk Prediction System
This version handles resource paths correctly when bundled as an executable
"""

import os
import sys
import subprocess
import time
import threading
import webbrowser

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    
    return os.path.join(base_path, relative_path)

def get_base_dir():
    """Get the base directory of the application"""
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        return os.path.dirname(sys.executable)
    else:
        # Running as script
        return os.path.dirname(os.path.abspath(__file__))

def start_backend():
    """Start the backend API server on port 8001"""
    try:
        base_dir = get_base_dir()
        
        # For executable, we need to run uvicorn differently
        if getattr(sys, 'frozen', False):
            # Running as executable - need to use the bundled Python
            import uvicorn
            
            # Setup paths for executable mode
            # In frozen mode, modules are in sys._MEIPASS
            if hasattr(sys, '_MEIPASS'):
                meipass = sys._MEIPASS
                # Add all necessary paths
                if meipass not in sys.path:
                    sys.path.insert(0, meipass)
                # Add subdirectories
                api_path = os.path.join(meipass, 'api')
                db_path = os.path.join(meipass, 'db')
                agents_path = os.path.join(meipass, 'agents')
                
                for path in [api_path, db_path, agents_path]:
                    if path not in sys.path and os.path.exists(path):
                        sys.path.insert(0, path)
            
            # Also add base_dir to path (for .env file access)
            if base_dir not in sys.path:
                sys.path.insert(0, base_dir)
            
            # Import needs to happen after path is set
            try:
                # Try importing from api package
                from api.BaseAPI import app
            except ImportError:
                try:
                    # Try direct import from api directory
                    import importlib.util
                    api_file = os.path.join(meipass, 'api', 'BaseAPI.py')
                    if os.path.exists(api_file):
                        spec = importlib.util.spec_from_file_location("BaseAPI", api_file)
                        base_api = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(base_api)
                        app = base_api.app
                    else:
                        raise ImportError(f"BaseAPI.py not found at {api_file}")
                except Exception as e:
                    print(f"Failed to import BaseAPI: {e}")
                    import traceback
                    traceback.print_exc()
                    return None
            
            # Change working directory to base_dir (for .env file)
            os.chdir(base_dir)
            
            # Run uvicorn directly
            config = uvicorn.Config(
                app=app,
                host="localhost",
                port=8001,
                log_level="info"
            )
            server = uvicorn.Server(config)
            
            # Run in a thread
            def run_server():
                try:
                    server.run()
                except Exception as e:
                    print(f"Backend server error: {e}")
                    import traceback
                    traceback.print_exc()
            
            thread = threading.Thread(target=run_server, daemon=True)
            thread.start()
            return thread
        else:
            # Running as script - use subprocess
            # Add the base directory to Python path
            if base_dir not in sys.path:
                sys.path.insert(0, base_dir)
            
            api_dir = os.path.join(base_dir, 'api')
            backend_process = subprocess.Popen(
                [sys.executable, '-m', 'uvicorn', 'BaseAPI:app', '--host', 'localhost', '--port', '8001'],
                cwd=api_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            return backend_process
            
    except Exception as e:
        print(f"Error starting backend server: {e}")
        import traceback
        traceback.print_exc()
        return None

def start_frontend():
    """Start the frontend server on port 8000"""
    try:
        base_dir = get_base_dir()
        
        # Add the base directory to Python path
        if base_dir not in sys.path:
            sys.path.insert(0, base_dir)
        
        if getattr(sys, 'frozen', False):
            # Running as executable
            try:
                from frontend.server import run_server as run_frontend_server
            except ImportError:
                # Try alternative import
                sys.path.insert(0, os.path.join(base_dir, 'frontend'))
                from server import run_server as run_frontend_server
            
            # Run in a thread
            def run_frontend():
                try:
                    run_frontend_server()
                except Exception as e:
                    print(f"Frontend server error: {e}")
                    import traceback
                    traceback.print_exc()
            
            thread = threading.Thread(target=run_frontend, daemon=True)
            thread.start()
            return thread
        else:
            # Running as script
            frontend_dir = os.path.join(base_dir, 'frontend')
            frontend_process = subprocess.Popen(
                [sys.executable, 'server.py'],
                cwd=frontend_dir,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            )
            return frontend_process
            
    except Exception as e:
        print(f"Error starting frontend server: {e}")
        import traceback
        traceback.print_exc()
        return None

def open_browser():
    """Open the browser after a short delay"""
    time.sleep(5)
    
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
    print("\n⚠️  IMPORTANT: Make sure to set up your .env file with:")
    print("   - GOOGLE_API_KEY")
    print("   - PINECONE_API_KEY")
    print("=" * 60)
    
    # Check for .env file
    base_dir = get_base_dir()
    env_file = os.path.join(base_dir, '.env')
    if not os.path.exists(env_file):
        print(f"\n⚠️  Warning: .env file not found at {env_file}")
        print("   The application may not work without API keys.")
        response = input("\nContinue anyway? (y/N): ")
        if response.lower() != 'y':
            return
    
    backend_process = None
    frontend_process = None
    
    try:
        # Start the backend server
        print("\nStarting backend API server...")
        backend_process = start_backend()
        if not backend_process:
            print("Failed to start backend server")
            input("Press Enter to exit...")
            return
        
        time.sleep(2)  # Wait for backend to start
        
        # Start the frontend server
        print("Starting frontend server...")
        frontend_process = start_frontend()
        if not frontend_process:
            print("Failed to start frontend server")
            input("Press Enter to exit...")
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
        print("\nPress Enter to stop the servers and exit")
        print("=" * 60)
        
        # Wait for user input to exit
        input()
            
    except KeyboardInterrupt:
        print("\nShutting down servers...")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
    finally:
        # Clean shutdown
        print("\nShutting down servers...")
        if backend_process:
            if isinstance(backend_process, subprocess.Popen):
                try:
                    backend_process.terminate()
                    backend_process.wait(timeout=5)
                    print("Backend server stopped.")
                except subprocess.TimeoutExpired:
                    backend_process.kill()
                    print("Backend server force killed.")
        
        if frontend_process:
            if isinstance(frontend_process, subprocess.Popen):
                try:
                    frontend_process.terminate()
                    frontend_process.wait(timeout=5)
                    print("Frontend server stopped.")
                except subprocess.TimeoutExpired:
                    frontend_process.kill()
                    print("Frontend server force killed.")

if __name__ == "__main__":
    main()

