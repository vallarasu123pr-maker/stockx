# Installation Help

## Problem: Timeout errors when installing dependencies

### Solution 1: Use the batch installer (Recommended)

Run this command in the `backend` folder:

```bash
install_dependencies.bat
```

This installs packages one by one with increased timeout.

### Solution 2: Install minimal dependencies first

```bash
install_minimal.bat
```

This installs only the essential packages to get started. You can add TensorFlow and Gemini AI later.

### Solution 3: Manual installation with timeout

```bash
pip install --timeout 300 --default-timeout=300 -r requirements.txt
```

### Solution 4: Install packages individually

If you're still having timeout issues, install one at a time:

```bash
pip install yfinance --timeout 300
pip install fastapi --timeout 300
pip install uvicorn --timeout 300
pip install pandas --timeout 300
pip install numpy --timeout 300
pip install scikit-learn --timeout 300
pip install pydantic --timeout 300
pip install python-multipart --timeout 300
pip install schedule --timeout 300
```

Skip TensorFlow and Gemini AI for now if they're causing issues:

```bash
# Install these later when you need predictions
pip install tensorflow --timeout 600
pip install google-generativeai --timeout 300
```

### Solution 5: Use a different mirror (if in China or slow network)

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --timeout 300
```

Or use Aliyun mirror:

```bash
pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --timeout 300
```

### Solution 6: Download wheels manually

If pip keeps timing out, download the `.whl` files manually:

1. Go to https://pypi.org/
2. Search for each package
3. Download the appropriate `.whl` file for your Python version
4. Install using: `pip install path/to/package.whl`

## Running without all dependencies

You can run a basic version without TensorFlow and Gemini AI:

1. Install minimal dependencies:
```bash
pip install fastapi uvicorn yfinance pandas numpy pydantic python-multipart schedule
```

2. Comment out prediction and AI features in `main.py`:
   - Comment out the `/api/predict/{ticker}` endpoint
   - Comment out Gemini imports

3. The technical indicators and alerts will still work!

## Verify installation

Check which packages are installed:

```bash
pip list
```

Check for missing packages:

```bash
python -c "import yfinance; import fastapi; import pandas; print('Core packages OK')"
```

## Still having issues?

1. Check your internet connection
2. Try using a VPN if you're behind a firewall
3. Check if your antivirus is blocking pip
4. Try upgrading pip: `python -m pip install --upgrade pip`
5. Clear pip cache: `pip cache purge`
