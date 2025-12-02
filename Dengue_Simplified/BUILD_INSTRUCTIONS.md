# Building the Dengue Risk Predictor Executable

## Prerequisites

- Python 3.8 or higher installed
- All dependencies from `requirements.txt` installed
- PyInstaller (will be auto-installed by build script if missing)

## Quick Build

Run the build script:

```bash
cd Dengue_Simplified
python build_exe.py
```

The script will:
1. Check for PyInstaller (install if missing)
2. Verify required files exist
3. Build the executable
4. Display the output location

## Output

The executable will be created in the `dist/` folder:
- **Windows:** `dist/DengueRiskPredictor.exe`
- **Size:** ~50-100 MB (includes all dependencies)

## Running the Executable

### First Time Setup

1. Copy `DengueRiskPredictor.exe` from `dist/` folder to your desired location
2. (Optional) Create a `.env` file in the same directory with your API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

### Running

Simply double-click `DengueRiskPredictor.exe` or run from command line:

```bash
./DengueRiskPredictor.exe
```

The application will:
- Start the Flask server on port 5000
- Automatically open your default browser to `http://localhost:5000`
- Display status in the console window

## Features Included

✅ **ML Prediction** - Works without internet or API key  
✅ **Browser Auto-Launch** - Opens automatically on startup  
✅ **Standalone** - No Python installation needed  
✅ **AI Chat** - Works if `.env` file with API key is present

## Troubleshooting

### Port Already in Use

If port 5000 is already in use:
1. Close other applications using port 5000
2. Or run from command line with environment variable:
   ```bash
   set FLASK_RUN_PORT=5001
   DengueRiskPredictor.exe
   ```

### Browser Doesn't Open

The executable will print the URL. Manually navigate to `http://localhost:5000`

### AI Chat Not Working

Make sure you have a `.env` file in the same directory as the executable with:
```
GOOGLE_API_KEY=your_actual_api_key_here
```

### Slow First Launch

The first run extracts files to a temporary folder, which may take 5-10 seconds.

## Distribution

To share the application:
1. Copy `DengueRiskPredictor.exe` from the `dist/` folder
2. Include a sample `.env.example` file
3. Recipients don't need Python installed!

## Clean Build

To rebuild from scratch:

```bash
# Remove build artifacts
rmdir /s /q build dist
del DengueRiskPredictor.spec

# Rebuild
python build_exe.py
```

## Technical Details

- **Bundler:** PyInstaller 6.x
- **Bundled Libraries:** Flask, scikit-learn, Google Generative AI, NumPy, Pandas
- **ML Model:** logistic_regression_model.joblib (bundled)
- **Frontend:** index.html (bundled)
- **Mode:** Single-file executable (--onefile)
