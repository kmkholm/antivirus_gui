#!/usr/bin/env python3
"""
Antivirus Launcher Script with Error Handling
Author: Dr. Mohammed Tawfik
Email: kmkhol01@gmail.com
"""

import os
import sys
import subprocess
import tkinter as tk
from tkinter import messagebox

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = ['filestack', 'requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'filestack':
                import filestack
            elif package == 'requests':
                import requests
        except ImportError:
            missing_packages.append(package)
    
    return missing_packages

def install_dependencies():
    """Install missing dependencies"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "filestack-python", "requests"])
        return True
    except subprocess.CalledProcessError:
        return False

def test_tkinter():
    """Test if tkinter works correctly"""
    try:
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the window
        root.destroy()
        return True
    except Exception as e:
        print(f"Tkinter test failed: {e}")
        return False

def show_gui_error(message):
    """Show error message in GUI if possible"""
    try:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Antivirus Error", message)
        root.destroy()
    except:
        print(f"GUI Error: {message}")

def launch_antivirus():
    """Launch the antivirus application with enhanced error handling"""
    print("🚀 Advanced Antivirus Launcher")
    print("=" * 50)
    print("Author: Dr. Mohammed Tawfik")
    print("Email: kmkhol01@gmail.com")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 7):
        error_msg = "Error: Python 3.7 or higher is required. Current version: {}.{}.{}".format(*sys.version_info[:3])
        print(error_msg)
        show_gui_error(error_msg)
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    # Test tkinter
    print("Testing GUI framework...")
    if not test_tkinter():
        error_msg = "Error: Tkinter GUI framework is not available"
        print(error_msg)
        show_gui_error(error_msg)
        sys.exit(1)
    print("✅ GUI framework working")
    
    # Check dependencies
    print("Checking dependencies...")
    missing_packages = check_dependencies()
    if missing_packages:
        print(f"⚠️ Missing packages: {', '.join(missing_packages)}")
        print("Attempting to install missing packages...")
        if not install_dependencies():
            error_msg = f"Error: Failed to install missing packages: {', '.join(missing_packages)}"
            print(error_msg)
            show_gui_error(error_msg)
            sys.exit(1)
        print("✅ Dependencies installed")
    else:
        print("✅ All dependencies available")
    
    # Verify antivirus file exists
    if not os.path.exists('antivirus_gui.py'):
        error_msg = "Error: antivirus_gui.py file not found. Please ensure all files are in the same directory."
        print(error_msg)
        show_gui_error(error_msg)
        sys.exit(1)
    
    print("Starting antivirus application...")
    print("API Key: ACFLXThQSQruATO9yvqwKz")
    print("-" * 50)
    
    try:
        # Import and run the antivirus
        from antivirus_gui import main
        main()
    except ImportError as e:
        error_msg = f"Error importing antivirus module: {e}"
        print(error_msg)
        show_gui_error(error_msg)
        sys.exit(1)
    except Exception as e:
        error_msg = f"Error running antivirus: {e}"
        print(error_msg)
        show_gui_error(error_msg)
        sys.exit(1)

if __name__ == "__main__":
    launch_antivirus()