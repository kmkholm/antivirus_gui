# Advanced Antivirus Application
**Author: Dr. Mohammed Tawfik**  
**Email: kmkhol01@gmail.com**  
**API Key: ACFLXThQSQruATO9yvqwKz**

## Overview

This is a comprehensive GUI-based antivirus application built with Python Tkinter, featuring signature-based detection and cloud-based virus scanning using Filestack API. The application provides multiple scanning options, real-time protection, quarantine management, and detailed reporting capabilities.

## Features

### 🔍 Core Scanning Capabilities
- **Quick Scan**: Fast scanning of common directories (Downloads, Desktop, Documents)
- **Full System Scan**: Comprehensive scanning of entire drives
- **Custom Scan**: Targeted scanning of user-selected directories
- **Signature-based Detection**: Local virus signature matching
- **Cloud-based Detection**: Filestack API integration for advanced threat detection

### 🛡️ Real-time Protection
- Real-time file monitoring
- USB autorun protection
- Configurable file type monitoring (.exe, .doc, .pdf, .zip, .rar)
- Activity logging and monitoring

### 🚫 Quarantine System
- Automatic threat quarantine
- File restoration from quarantine
- Threat management and deletion
- Database storage for quarantine items

### ☁️ Cloud Security Integration
- File upload to Filestack for cloud analysis
- Advanced virus detection via cloud services
- Sample submission for threat analysis
- Webhook support for real-time results

### 📊 Reporting & History
- Comprehensive scan history
- Export capabilities (CSV reports)
- Threat statistics and analytics
- Detailed activity logs

### ⚙️ Advanced Configuration
- Custom file extension scanning
- Threat sensitivity adjustment
- Cloud detection settings
- Automatic virus definition updates

## Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager
- Internet connection for cloud features

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python antivirus_gui.py
```

## How to Use

### 1. Starting the Application
1. Run the Python script: `python antivirus_gui.py`
2. The main interface will open with multiple tabs
3. Configure your preferences in the Settings tab

### 2. Basic Scanning

#### Quick Scan
- Click "🚀 Quick Scan" button
- Scans common download and document locations
- Fast results with threat identification

#### Full Scan
- Click "📁 Full Scan" button
- Comprehensive system scan
- Covers all drives and file types
- Takes longer but provides complete coverage

#### Custom Scan
- Click "🎯 Custom Scan" button
- Select specific directories to scan
- Targeted scanning for specific areas

### 3. File Upload and Cloud Scanning

#### Upload Single File
- Click "📤 Upload & Scan" button
- Select file from your system
- File is uploaded to Filestack for cloud analysis
- Results displayed in Cloud Security tab

#### Cloud Security Tab
- Upload files manually via "📤 Upload File to Cloud"
- Monitor cloud scan progress and results
- Real-time threat analysis using Filestack API

### 4. Threat Management

#### During Scan
- Threats appear in the main results area
- Each threat shows:
  - File path
  - Status (Clean/Infected)
  - Threat type
  - Recommended action

#### Available Actions
- **🗑️ Delete Threat**: Permanently remove infected file
- **📋 Quarantine**: Move file to quarantine folder
- **✅ Allow**: Mark as safe (user discretion)

### 5. Real-time Protection

#### Enable Protection
- Go to "🛡️ Real-Time Protection" tab
- Check "Enable Real-time Protection"
- Configure monitored file types
- Enable USB autorun protection

#### Monitoring
- Real-time activity log shows all monitoring events
- Automatic threat detection as files are accessed
- Configurable sensitivity levels

### 6. Quarantine Management

#### Access Quarantine
- Go to "🚫 Quarantine" tab
- View all quarantined files
- See threat details and quarantine dates

#### Actions
- **↩️ Restore**: Return file to original location
- **🗑️ Delete All**: Remove all quarantined items
- **📤 Submit Sample**: Send to Filestack for advanced analysis

### 7. Settings and Configuration

#### General Settings
- Update virus definitions
- Configure scan frequency
- Set auto-cleanup options

#### Cloud Security
- API key management (pre-configured)
- Cloud detection toggle
- Webhook configuration for real-time results

#### Advanced Settings
- Custom file extensions
- Threat sensitivity (1-10 scale)
- Performance optimization

### 8. Reports and History

#### Scan History
- View all previous scans
- See statistics and threat counts
- Export reports in CSV format

#### Activity Logs
- Real-time protection events
- Cloud scan results
- System monitoring logs

## API Integration Details

### Filestack API Usage
The application uses your Filestack API key (ACFLXThQSQruATO9yvqwKz) for:

1. **File Upload**: Secure file upload to Filestack storage
2. **Virus Detection**: Integration with Filestack's intelligence tasks
3. **Workflow Processing**: Automated threat detection workflows
4. **Webhook Handling**: Real-time results via webhooks

### Cloud Workflow Configuration
```python
# Example workflow response for virus detection
{
    "data": {
        "infected": false,
        "infections_list": []
    }
}
```

### Webhook Integration
- Configure webhooks in Filestack dashboard
- Real-time threat detection results
- Automated quarantine actions

## Database Features

The application uses SQLite database for:
- **Scan History**: Store all scan results
- **Quarantine Records**: Manage quarantined files
- **Settings Persistence**: Remember user preferences
- **Threat Analytics**: Track threat patterns

## Security Features

### Signature-based Detection
- MD5 hash comparison with known virus signatures
- Regular signature updates
- Custom signature addition

### Cloud-based Analysis
- Filestack API integration
- Advanced threat detection
- Real-time malware analysis

### Real-time Monitoring
- File system monitoring
- USB device protection
- Autorun prevention

## Troubleshooting

### Common Issues

#### Cloud Upload Fails
- Check internet connection
- Verify API key configuration
- Ensure file is not corrupted

#### Scan Performance
- Adjust sensitivity settings
- Exclude large system directories
- Enable performance mode

#### Real-time Protection Issues
- Check file permissions
- Verify monitoring directories
- Restart application

### Error Messages
- **"API Key Invalid"**: Verify Filestack API key
- **"Network Error"**: Check internet connection
- **"Permission Denied"**: Run as administrator

## Advanced Usage

### Custom Threat Signatures
Add new signatures to the `load_virus_signatures()` function:
```python
signatures = {
    "your_hash_here": "Your threat name"
}
```

### Webhook Configuration
1. Create webhook URL in Filestack dashboard
2. Configure virus detection workflow
3. Add webhook to application settings

### Performance Optimization
- Adjust file size limits
- Configure parallel scanning
- Set up exclusions

## Support and Contact

**Author**: Dr. Mohammed Tawfik  
**Email**: kmkhol01@gmail.com  

For technical support, feature requests, or bug reports, please contact the author.

## License

This antivirus application is provided as-is for educational and personal use. Please ensure compliance with applicable laws when scanning systems you don't own.

## Version Information

- **Version**: 1.0.0
- **Last Updated**: 2025-11-24
- **Python Compatibility**: 3.7+
- **API Integration**: Filestack v1.0.0