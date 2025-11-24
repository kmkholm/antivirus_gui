# Quick Installation Guide
**Advanced Antivirus Application**

## 🚀 **Quick Start**

### **Option 1: Use the Launcher (Recommended)**
```bash
python launcher.py
```

### **Option 2: Direct Installation**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python antivirus_gui.py
```

### **Option 3: Test First**
```bash
# Run the test script to check for issues
python test_antivirus.py
```

## 🔧 **Troubleshooting**

### **If you get the tkinter error:**
1. **Install tkinter** (usually comes with Python):
   - **Ubuntu/Debian:** `sudo apt-get install python3-tk`
   - **CentOS/RHEL:** `sudo yum install tkinter`
   - **Windows:** Reinstall Python with "tcl/tk and IDLE" option checked

2. **Test tkinter:**
   ```bash
   python -c "import tkinter; print('tkinter working')"
   ```

### **If you get dependency errors:**
1. **Install dependencies manually:**
   ```bash
   pip install filestack-python requests
   ```

2. **Update pip first:**
   ```bash
   python -m pip install --upgrade pip
   ```

### **If you get permission errors:**
- **Windows:** Run as Administrator
- **Linux/Mac:** Use `sudo` for installation or run:
  ```bash
  python launcher.py
  ```

## 📋 **System Requirements**

- **Python:** 3.7 or higher
- **Operating System:** Windows, macOS, or Linux
- **Memory:** 512MB RAM minimum
- **Disk Space:** 100MB free space
- **Internet:** Required for cloud features

## 🎯 **Features Available**

✅ **GUI Interface** with tabs for different functions  
✅ **Quick Scan** - Fast scanning of common directories  
✅ **Full Scan** - Comprehensive system scan  
✅ **Custom Scan** - User-selected directory scanning  
✅ **Cloud Upload** - Filestack API integration  
✅ **Real-time Protection** - File monitoring  
✅ **Quarantine Management** - Threat isolation  
✅ **Scan History** - Detailed reporting  

## 📞 **Support**

**Author:** Dr. Mohammed Tawfik  
**Email:** kmkhol01@gmail.com

If you continue to have issues, please contact support with:
1. Your operating system and Python version
2. The exact error message
3. Steps you've tried

## 🔐 **Security Note**

This antivirus uses your API key: `ACFLXThQSQruATO9yvqwKz`  
Your API key is securely stored and used only for legitimate virus detection through Filestack services.