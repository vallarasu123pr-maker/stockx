@echo off
echo Installing minimal dependencies to get started...
echo.

REM Install only essential packages first
pip install --upgrade pip

echo Installing core packages...
pip install fastapi uvicorn yfinance pandas numpy pydantic python-multipart schedule --timeout 300

echo.
echo Minimal installation complete!
echo You can run the basic app now. Install TensorFlow and Gemini later if needed.
echo.
pause
