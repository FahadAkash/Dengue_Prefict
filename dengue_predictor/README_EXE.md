# Dengue Risk Predictor - Executable Version

## Quick Start Guide for End Users

### Step 1: Download and Extract
1. Download the `DengueRiskPredictor.exe` file
2. Extract it to a folder (e.g., `C:\DengueRiskPredictor\`)

### Step 2: Set Up API Keys
1. Create a file named `.env` in the same folder as `DengueRiskPredictor.exe`
2. Add your API keys to the `.env` file:

```
GOOGLE_API_KEY=your_google_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
```

**Important**: Without these API keys, the application will not work properly.

### Step 3: Run the Application
1. Double-click `DengueRiskPredictor.exe`
2. Wait for the application to start (this may take 10-30 seconds)
3. Your web browser will automatically open to `http://localhost:8000`
4. If the browser doesn't open automatically, navigate to `http://localhost:8000` manually

### Step 4: Use the Application
- Fill in the patient information form
- Click "Calculate Risk" to get dengue risk assessment
- Chat with the AI assistant for detailed recommendations

### Step 5: Close the Application
- Press `Enter` in the console window to stop the servers
- Or close the console window (servers will stop automatically)

## Troubleshooting

### Application won't start
- Make sure you have the `.env` file with valid API keys
- Check that ports 8000 and 8001 are not already in use
- Try running as Administrator

### Browser doesn't open
- Manually navigate to `http://localhost:8000`
- Check that the console shows "SYSTEM IS NOW RUNNING!"

### API errors
- Verify your API keys are correct in the `.env` file
- Check your internet connection
- Ensure you have credits/quota for Google Gemini and Pinecone APIs

### Port already in use
- Close any other applications using ports 8000 or 8001
- Restart your computer if needed

## System Requirements
- Windows 10 or later
- Internet connection (for API calls)
- 200 MB free disk space
- At least 4 GB RAM recommended

## Support
For issues or questions, please contact the development team.

## Project Team
- **Umme Hani Bithe** - Roll 41
- **Jannat** - Roll 14

---

**Note**: This is a standalone executable. You do not need Python installed to run it.


