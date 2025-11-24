@echo off
REM Advanced Antivirus Installation Script for Windows
REM Author: Dr. Mohammed Tawfik
REM Email: kmkhol01@gmail.com

echo.
echo 🚀 Advanced Antivirus Installation
echo ==================================
echo Author: Dr. Mohammed Tawfik
echo Email: kmkhol01@gmail.com
echo ==================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://python.org
    pause
    exit /b 1
)

echo ✅ Python is available
python --version

REM Check pip
echo Checking pip...
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not available
    echo Please ensure pip is installed with Python
    pause
    exit /b 1
)

echo ✅ pip is available

REM Install dependencies
echo.
echo Installing required packages...
echo filestack-python, requests

pip install -r requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully

REM Test imports
echo Testing imports...
python -c "import filestack, requests, tkinter; print('✅ All imports successful')"

if errorlevel 1 (
    echo ❌ Import test failed
    pause
    exit /b 1
)

echo.
echo 🎉 Installation completed successfully!
echo.
echo To run the antivirus application:
echo   python antivirus_gui.py
echo.
echo To run the demo:
echo   python demo.py
echo.
echo To use the launcher:
echo   python launcher.py
echo.
echo Enjoy your advanced antivirus protection!
echo.
pause