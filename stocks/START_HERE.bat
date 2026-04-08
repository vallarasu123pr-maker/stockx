@echo off
cls
echo ============================================================
echo    AI Stock Analyzer - Quick Start
echo ============================================================
echo.
echo This script will help you get started quickly!
echo.
echo Choose an option:
echo.
echo 1. Check dependencies (see what's installed)
echo 2. Install minimal version (fast, no AI predictions)
echo 3. Install full version (includes AI predictions)
echo 4. Start backend (minimal version)
echo 5. Start backend (full version)
echo 6. Start frontend
echo 7. Open installation help
echo 8. Exit
echo.
set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" goto check
if "%choice%"=="2" goto install_minimal
if "%choice%"=="3" goto install_full
if "%choice%"=="4" goto start_minimal
if "%choice%"=="5" goto start_full
if "%choice%"=="6" goto start_frontend
if "%choice%"=="7" goto help
if "%choice%"=="8" goto end

:check
echo.
echo Checking dependencies...
cd backend
python check_dependencies.py
pause
goto menu

:install_minimal
echo.
echo Installing minimal dependencies...
cd backend
call install_minimal.bat
echo.
echo Installation complete!
echo Run option 4 to start the backend.
pause
goto menu

:install_full
echo.
echo Installing full dependencies (this may take 10-30 minutes)...
cd backend
call install_dependencies.bat
echo.
echo Installation complete!
echo Run option 5 to start the backend.
pause
goto menu

:start_minimal
echo.
echo Starting backend (minimal version - no AI predictions)...
cd backend
python main_minimal.py
pause
goto menu

:start_full
echo.
echo Starting backend (full version with AI predictions)...
cd backend
python main.py
pause
goto menu

:start_frontend
echo.
echo Starting frontend...
echo Make sure backend is running first!
echo.
cd frontend
start cmd /k "npm run dev"
echo.
echo Frontend starting in new window...
pause
goto menu

:help
echo.
echo Opening installation help...
start backend\INSTALL_HELP.md
pause
goto menu

:menu
cls
echo ============================================================
echo    AI Stock Analyzer - Quick Start
echo ============================================================
echo.
echo Choose an option:
echo.
echo 1. Check dependencies (see what's installed)
echo 2. Install minimal version (fast, no AI predictions)
echo 3. Install full version (includes AI predictions)
echo 4. Start backend (minimal version)
echo 5. Start backend (full version)
echo 6. Start frontend
echo 7. Open installation help
echo 8. Exit
echo.
set /p choice="Enter your choice (1-8): "

if "%choice%"=="1" goto check
if "%choice%"=="2" goto install_minimal
if "%choice%"=="3" goto install_full
if "%choice%"=="4" goto start_minimal
if "%choice%"=="5" goto start_full
if "%choice%"=="6" goto start_frontend
if "%choice%"=="7" goto help
if "%choice%"=="8" goto end

:end
echo.
echo Thanks for using AI Stock Analyzer!
echo.
pause
