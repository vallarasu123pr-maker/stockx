@echo off
echo Installing Python dependencies with increased timeout...
echo.

REM Upgrade pip first
python -m pip install --upgrade pip --timeout 300

REM Install packages one by one with increased timeout
echo Installing yfinance...
pip install yfinance==0.2.32 --timeout 300 --default-timeout=300

echo Installing fastapi...
pip install fastapi==0.104.1 --timeout 300

echo Installing uvicorn...
pip install uvicorn==0.24.0 --timeout 300

echo Installing pandas...
pip install pandas==2.1.3 --timeout 300

echo Installing numpy...
pip install numpy==1.26.2 --timeout 300

echo Installing scikit-learn...
pip install scikit-learn==1.3.2 --timeout 300

echo Installing tensorflow (this may take a while)...
pip install tensorflow==2.15.0 --timeout 600

echo Installing google-generativeai...
pip install google-generativeai==0.3.1 --timeout 300

echo Installing pydantic...
pip install pydantic==2.5.0 --timeout 300

echo Installing python-multipart...
pip install python-multipart==0.0.6 --timeout 300

echo Installing schedule...
pip install schedule==1.2.0 --timeout 300

echo.
echo Installation complete!
echo.
pause
