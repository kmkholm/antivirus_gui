#!/bin/bash
# Advanced Antivirus Installation Script
# Author: Dr. Mohammed Tawfik
# Email: kmkhol01@gmail.com

echo "🚀 Advanced Antivirus Installation"
echo "=================================="
echo "Author: Dr. Mohammed Tawfik"
echo "Email: kmkhol01@gmail.com"
echo "=================================="

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1)
echo "Found: $python_version"

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3.7 or higher."
    exit 1
fi

# Check pip
echo "Checking pip..."
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip is required but not installed."
    echo "Please install pip for Python 3."
    exit 1
fi

echo "✅ Python 3 and pip are available"

# Install required packages
echo "Installing required packages..."
echo "Required packages: filestack-python, requests"

pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Test import
echo "Testing imports..."
python3 -c "
try:
    import filestack
    import requests
    import tkinter
    print('✅ All imports successful')
except ImportError as e:
    print(f'❌ Import failed: {e}')
    exit(1)
"

echo ""
echo "🎉 Installation completed successfully!"
echo ""
echo "To run the antivirus application:"
echo "  python3 antivirus_gui.py"
echo ""
echo "To run the demo:"
echo "  python3 demo.py"
echo ""
echo "To use the launcher:"
echo "  python3 launcher.py"
echo ""
echo "Enjoy your advanced antivirus protection!"