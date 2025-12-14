@echo off
echo ==========================================
echo   GigaPulse Network Intelligence Platform
echo ==========================================
echo.
echo [1/3] Checking Python environment...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in your PATH.
    echo Please install Python 3.8+ and try again.
    pause
    exit /b
)

echo [2/3] Installing dependencies...
pip install -r backend/requirements.txt
if %errorlevel% neq 0 (
    echo Warning: Some dependencies might have failed to install.
    echo Attempting to run anyway...
)

echo [3/3] Starting GigaPulse Server...
echo.
echo The application will open in your default browser automatically.
echo Press Ctrl+C to stop the server.
echo.

cd backend
python main.py
pause
