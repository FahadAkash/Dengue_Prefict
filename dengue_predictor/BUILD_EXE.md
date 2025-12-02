# Building Executable Binary (.exe) for Dengue Risk Predictor

This guide explains how to build a standalone executable (.exe) file from the Dengue Risk Predictor project.

## Prerequisites

1. **Python 3.8+** installed on Windows
2. **All project dependencies** installed (from `requirment.txt`)
3. **PyInstaller** (will be installed automatically if not present)

## Quick Build

### Step 1: Install PyInstaller

```bash
pip install pyinstaller
```

### Step 2: Run the Build Script

```bash
cd dengue_predictor
python build_exe.py
```

This will create the executable in the `dist` folder.

## Manual Build (Alternative)

If you prefer to build manually:

```bash
pyinstaller --name=DengueRiskPredictor ^
    --onefile ^
    --windowed ^
    --add-data "frontend;frontend" ^
    --add-data "core/models;core/models" ^
    --add-data "datasets;datasets" ^
    --hidden-import uvicorn ^
    --hidden-import fastapi ^
    --hidden-import google.generativeai ^
    --hidden-import pinecone ^
    start_full_system_exe.py
```

## What Gets Bundled

The executable includes:
- ✅ Python runtime
- ✅ All Python dependencies
- ✅ Frontend files (HTML, CSS, JS)
- ✅ ML model (logistic_regression_model.joblib)
- ✅ Dataset files
- ✅ Application code

## Important Notes

### 1. Environment Variables (.env file)

The executable **does NOT** include your `.env` file for security reasons. You need to:

**Option A: Place .env file next to executable**
```
dist/
  ├── DengueRiskPredictor.exe
  └── .env  (create this file with your API keys)
```

**Option B: Set environment variables in Windows**
```bash
set GOOGLE_API_KEY=your_key_here
set PINECONE_API_KEY=your_key_here
```

### 2. File Structure for Distribution

When distributing the executable, include:

```
DengueRiskPredictor/
  ├── DengueRiskPredictor.exe
  ├── .env (user needs to create this)
  └── README.txt (instructions for users)
```

### 3. Creating .env File Template

Create a `.env.example` file that users can copy:

```env
GOOGLE_API_KEY=your_google_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
```

## Distribution

### For End Users

1. **Extract the executable** to a folder
2. **Create a `.env` file** in the same folder with API keys
3. **Run `DengueRiskPredictor.exe`**
4. The application will:
   - Start backend server on port 8001
   - Start frontend server on port 8000
   - Automatically open browser

### Creating an Installer (Optional)

You can use **Inno Setup** or **NSIS** to create a professional installer:

1. **Inno Setup** (Recommended)
   - Download from: https://jrsoftware.org/isinfo.php
   - Create installer script that:
     - Installs the .exe
     - Creates .env template
     - Creates desktop shortcut
     - Adds to Start Menu

2. **NSIS**
   - Download from: https://nsis.sourceforge.io/
   - Similar functionality to Inno Setup

## Troubleshooting

### Issue: "Module not found" errors

**Solution**: Add the missing module to `--hidden-import` in `build_exe.py`

### Issue: Frontend files not loading

**Solution**: Check that frontend files are included in `--add-data` paths

### Issue: ML model not found

**Solution**: Ensure model path is correct and included in `--add-data`

### Issue: Large executable size

**Solution**: This is normal. PyInstaller bundles Python and all dependencies.
- Typical size: 100-200 MB
- Consider using `--exclude-module` to remove unused packages

### Issue: Antivirus flags the executable

**Solution**: This is common with PyInstaller executables. Options:
1. Submit to antivirus vendors for whitelisting
2. Code sign the executable (requires certificate)
3. Use `--onefile` creates a single file (larger but simpler)

## Advanced Options

### Console Version (for debugging)

Change `--windowed` to `--console` in `build_exe.py` to see console output:

```python
'--console',  # Instead of --windowed
```

### Custom Icon

Add an icon file and include it:

```python
'--icon=path/to/icon.ico',
```

### Code Signing (for production)

```bash
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com DengueRiskPredictor.exe
```

## File Size Optimization

To reduce executable size:

```python
--exclude-module matplotlib
--exclude-module pandas.tests
--exclude-module numpy.tests
```

## Testing the Executable

1. Build the executable
2. Copy to a test folder (without source code)
3. Create `.env` file with test API keys
4. Run the executable
5. Verify:
   - Backend starts on port 8001
   - Frontend starts on port 8000
   - Browser opens automatically
   - All features work correctly

## Support

If you encounter issues:
1. Check the PyInstaller documentation: https://pyinstaller.org/
2. Review build logs for errors
3. Test with `--console` flag to see error messages
4. Check that all dependencies are installed

## License

Same as the main project license.


