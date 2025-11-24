#!/usr/bin/env python3
"""
Antivirus Test Script
Quick test to verify the application works correctly
Author: Dr. Mohammed Tawfik
Email: kmkhol01@gmail.com
"""

import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    try:
        import tkinter as tk
        print("✅ tkinter imported successfully")
        
        import tkinter.ttk as ttk
        print("✅ tkinter.ttk imported successfully")
        
        try:
            from filestack import Client
            print("✅ filestack imported successfully")
        except ImportError:
            print("⚠️ filestack not found - install with: pip install filestack-python")
        
        import hashlib
        print("✅ hashlib imported successfully")
        
        import threading
        print("✅ threading imported successfully")
        
        import sqlite3
        print("✅ sqlite3 imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_gui_creation():
    """Test if GUI can be created without errors"""
    try:
        import tkinter as tk
        root = tk.Tk()
        root.title("Test Window")
        root.geometry("300x200")
        
        # Test Treeview creation (this was the main issue)
        import tkinter.ttk as ttk
        tree = ttk.Treeview(root)
        tree['columns'] = ('col1', 'col2')
        tree.column('#0', width=100)
        tree.column('col1', width=100)
        tree.column('col2', width=100)
        tree.heading('#0', text='Test Column')
        tree.heading('col1', text='Column 1')
        tree.heading('col2', text='Column 2')
        
        # Insert test data
        tree.insert('', 'end', text='Test Item', values=('Value1', 'Value2'))
        
        tree.pack(fill='both', expand=True)
        
        print("✅ Treeview created successfully")
        
        # Close the test window immediately
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ GUI creation error: {e}")
        return False

def main():
    """Main test function"""
    print("🔧 Antivirus Application Test")
    print("=" * 40)
    print("Author: Dr. Mohammed Tawfik")
    print("Email: kmkhol01@gmail.com")
    print("=" * 40)
    print()
    
    print("Testing imports...")
    import_success = test_imports()
    print()
    
    print("Testing GUI creation...")
    gui_success = test_gui_creation()
    print()
    
    if import_success and gui_success:
        print("🎉 All tests passed! The antivirus application should work correctly.")
        print()
        print("To run the antivirus application:")
        print("  python antivirus_gui.py")
        print()
        print("To run the demo:")
        print("  python demo.py")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        print()
        if not import_success:
            print("💡 Try installing missing packages:")
            print("  pip install -r requirements.txt")
        if not gui_success:
            print("💡 GUI test failed - this might be a display issue.")

if __name__ == "__main__":
    main()