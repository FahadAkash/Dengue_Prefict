#!/usr/bin/env python3
"""
Build script to create standalone executable for Dengue Risk Prediction System
Uses PyInstaller to bundle Python code, dependencies, frontend files, and ML model
"""

import os
import sys
import subprocess
import shutil

def check_pyinstaller():
    """Check if PyInstaller is installed, install if not"""
    try:
        import PyInstaller
        version = PyInstaller.__version__ if hasattr(PyInstaller, '__version__') else "unknown"
        print(f"✅ PyInstaller is installed (version: {version})")
        return True
    except ImportError:
        print("⚠️  PyInstaller is not installed")
        print("Installing PyInstaller...")
        try:
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', 'pyinstaller'],
                check=True
            )
            print("✅ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install PyInstaller: {e}")
            print("\nPlease install PyInstaller manually:")
            print("  pip install pyinstaller")
            return False

def build_executable():
    """Build the executable using PyInstaller"""
    try:
        import PyInstaller.__main__
    except ImportError:
        print("❌ PyInstaller is not available")
        return False
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(base_dir, 'app.py')
    
    # Check required files
    required_files = [
        'app.py',
        'index.html',
        'logistic_regression_model.joblib'
    ]
    
    for file in required_files:
        if not os.path.exists(os.path.join(base_dir, file)):
            print(f"❌ Required file not found: {file}")
            return False
    
    # Build PyInstaller command
    sep = ';' if sys.platform == 'win32' else ':'
    
    cmd = [
        main_script,
        '--name=DengueRiskPredictor',
        '--onefile',
        '--console',  # Show console for debugging
        '--noupx',  # Don't use UPX compression (can cause extraction errors)
        '--icon=NONE',  # No icon for now
        # Add data files
        f'--add-data=index.html{sep}.',
        f'--add-data=logistic_regression_model.joblib{sep}.',
        f'--add-data=.env.example{sep}.',
        # Hidden imports
        '--hidden-import=flask',
        '--hidden-import=flask_cors',
        '--hidden-import=joblib',
        '--hidden-import=numpy',
        '--hidden-import=pandas',
        '--hidden-import=sklearn',
        '--hidden-import=sklearn.linear_model',
        '--hidden-import=sklearn.linear_model._logistic',
        '--hidden-import=google.generativeai',
        '--hidden-import=dotenv',
        '--hidden-import=webbrowser',
        '--hidden-import=threading',
        # Collect all submodules
        '--collect-all=flask',
        '--collect-all=sklearn',
        '--collect-all=google.generativeai',
    ]
    
    print("\n" + "=" * 60)
    print("BUILDING EXECUTABLE")
    print("=" * 60)
    print(f"Base directory: {base_dir}")
    print(f"Main script: {main_script}")
    print("=" * 60)
    print("\nBuilding executable...")
    print("This may take several minutes...\n")
    
    try:
        PyInstaller.__main__.run(cmd)
        print("\n" + "=" * 60)
        print("✅ BUILD COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        exe_name = 'DengueRiskPredictor.exe' if sys.platform == 'win32' else 'DengueRiskPredictor'
        exe_path = os.path.join(base_dir, 'dist', exe_name)
        
        if os.path.exists(exe_path):
            file_size = os.path.getsize(exe_path) / (1024 * 1024)  # Size in MB
            print(f"Executable location: {exe_path}")
            print(f"Executable size: {file_size:.2f} MB")
            print("\n📦 Next steps:")
            print("1. Copy the executable from the 'dist' folder")
            print("2. (Optional) Create a .env file next to the executable with GOOGLE_API_KEY for AI chat")
            print("3. Run the executable - it will auto-open your browser!")
            print("\n⚠️  Note: The first run may take a few seconds as it extracts files")
        else:
            print("⚠️  Warning: Executable not found at expected location")
            print(f"   Check the 'dist' folder: {os.path.join(base_dir, 'dist')}")
        
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ BUILD FAILED")
        print("=" * 60)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("DENGUE RISK PREDICTOR - EXECUTABLE BUILDER")
    print("=" * 60)
    print(f"Python: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print("=" * 60)
    
    if not check_pyinstaller():
        print("\n" + "=" * 60)
        print("❌ Cannot proceed without PyInstaller")
        print("=" * 60)
        sys.exit(1)
    
    print("=" * 60)
    success = build_executable()
    
    if success:
        print("\n✅ Build process completed successfully!")
    else:
        print("\n❌ Build process failed. Please check the errors above.")
        sys.exit(1)
