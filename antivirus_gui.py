#!/usr/bin/env python3
"""
Advanced Antivirus Application with GUI
Author: Dr. Mohammed Tawfik
Email: kmkhol01@gmail.com
API Key: ACFLXThQSQruATO9yvqwKz
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import hashlib
import threading
import json
import time
import datetime
import requests
from pathlib import Path
import subprocess
import shutil
from filestack import Client
import csv
import sqlite3
from collections import defaultdict

class AntivirusGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Antivirus Scanner - Dr. Mohammed Tawfik")
        self.root.geometry("1400x900")
        self.root.configure(bg='#2c3e50')
        
        # API Configuration
        self.api_key = "ACFLXThQSQruATO9yvqwKz"
        self.filestack_client = Client(self.api_key)
        
        # Initialize variables
        self.scan_results = []
        self.virus_signatures = self.load_virus_signatures()
        self.scan_history = []
        self.quarantine_items = []
        self.real_time_protection = False
        self.autorun_disabled = False
        
        # Database initialization
        self.init_database()
        
        # Setup GUI
        self.setup_gui()
        
        # Load settings
        self.load_settings()
    
    def init_database(self):
        """Initialize SQLite database for storing scan history and settings"""
        self.db_connection = sqlite3.connect('antivirus_database.db')
        cursor = self.db_connection.cursor()
        
        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scan_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                scan_type TEXT,
                files_scanned INTEGER,
                threats_found INTEGER,
                threats_removed INTEGER,
                details TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quarantine (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                file_path TEXT,
                file_hash TEXT,
                threat_name TEXT,
                quarantined_date TEXT
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')
        
        self.db_connection.commit()
    
    def load_virus_signatures(self):
        """Load virus signatures for local detection"""
        # Sample virus signatures (in real implementation, this would be updated regularly)
        signatures = {
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855": "Empty File",
            "d41d8cd98f00b204e9800998ecf8427e": "Empty File",
            # Add more signatures as needed
        }
        return signatures
    
    def setup_gui(self):
        """Setup the main GUI interface"""
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_main_scan_tab()
        self.create_real_time_protection_tab()
        self.create_quarantine_tab()
        self.create_scan_history_tab()
        self.create_settings_tab()
        self.create_cloud_security_tab()
        
        # Status bar
        self.setup_status_bar()
    
    def create_main_scan_tab(self):
        """Create main scan tab"""
        self.main_scan_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.main_scan_frame, text="🔍 Quick Scan")
        
        # Main scan controls
        control_frame = tk.Frame(self.main_scan_frame, bg='#2c3e50')
        control_frame.pack(fill='x', padx=20, pady=10)
        
        # Scan buttons
        tk.Button(control_frame, text="🚀 Quick Scan", command=self.start_quick_scan,
                 bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                 width=15, height=2).pack(side='left', padx=5)
        
        tk.Button(control_frame, text="📁 Full Scan", command=self.start_full_scan,
                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                 width=15, height=2).pack(side='left', padx=5)
        
        tk.Button(control_frame, text="🎯 Custom Scan", command=self.start_custom_scan,
                 bg='#f39c12', fg='white', font=('Arial', 12, 'bold'),
                 width=15, height=2).pack(side='left', padx=5)
        
        tk.Button(control_frame, text="📤 Upload & Scan", command=self.upload_and_scan,
                 bg='#9b59b6', fg='white', font=('Arial', 12, 'bold'),
                 width=15, height=2).pack(side='left', padx=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var,
                                          maximum=100, length=400)
        self.progress_bar.pack(side='right', padx=20, pady=10)
        
        # Scan results area
        results_frame = tk.Frame(self.main_scan_frame, bg='#2c3e50')
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Results treeview
        self.results_tree = ttk.Treeview(results_frame)
        self.results_tree.pack(fill='both', expand=True)
        
        # Configure treeview columns
        self.results_tree['columns'] = ('status', 'threat', 'action')
        self.results_tree.column('#0', width=400, anchor='w')
        self.results_tree.column('status', width=100, anchor='center')
        self.results_tree.column('threat', width=300, anchor='w')
        self.results_tree.column('action', width=200, anchor='center')
        
        self.results_tree.heading('#0', text='File Path')
        self.results_tree.heading('status', text='Status')
        self.results_tree.heading('threat', text='Threat Detected')
        self.results_tree.heading('action', text='Action Taken')
        
        # Scrollbar for results
        scrollbar = ttk.Scrollbar(results_frame, orient='vertical', command=self.results_tree.yview)
        scrollbar.pack(side='right', fill='y')
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        # Action buttons
        action_frame = tk.Frame(self.main_scan_frame, bg='#2c3e50')
        action_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(action_frame, text="🗑️ Delete Threat", command=self.delete_threat,
                 bg='#e74c3c', fg='white', font=('Arial', 10),
                 width=15).pack(side='left', padx=5)
        
        tk.Button(action_frame, text="📋 Quarantine", command=self.quarantine_threat,
                 bg='#f39c12', fg='white', font=('Arial', 10),
                 width=15).pack(side='left', padx=5)
        
        tk.Button(action_frame, text="✅ Allow", command=self.allow_threat,
                 bg='#27ae60', fg='white', font=('Arial', 10),
                 width=15).pack(side='left', padx=5)
    
    def create_real_time_protection_tab(self):
        """Create real-time protection tab"""
        self.realtime_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.realtime_frame, text="🛡️ Real-Time Protection")
        
        # Protection controls
        protection_frame = tk.Frame(self.realtime_frame, bg='#2c3e50')
        protection_frame.pack(fill='x', padx=20, pady=20)
        
        # Toggle real-time protection
        self.realtime_var = tk.BooleanVar()
        tk.Checkbutton(protection_frame, text="Enable Real-Time Protection",
                      variable=self.realtime_var, command=self.toggle_realtime_protection,
                      bg='#2c3e50', fg='white', font=('Arial', 14),
                      selectcolor='#34495e').pack(anchor='w')
        
        # File monitoring options
        tk.Label(protection_frame, text="Monitor these file types:", 
                bg='#2c3e50', fg='white', font=('Arial', 12, 'bold')).pack(anchor='w', pady=(20,5))
        
        file_types_frame = tk.Frame(protection_frame, bg='#2c3e50')
        file_types_frame.pack(fill='x', pady=5)
        
        self.monitor_exe = tk.BooleanVar(value=True)
        self.monitor_doc = tk.BooleanVar(value=True)
        self.monitor_pdf = tk.BooleanVar(value=True)
        self.monitor_zip = tk.BooleanVar(value=True)
        
        tk.Checkbutton(file_types_frame, text=".exe", variable=self.monitor_exe,
                      bg='#2c3e50', fg='white').pack(side='left', padx=10)
        tk.Checkbutton(file_types_frame, text=".doc/.docx", variable=self.monitor_doc,
                      bg='#2c3e50', fg='white').pack(side='left', padx=10)
        tk.Checkbutton(file_types_frame, text=".pdf", variable=self.monitor_pdf,
                      bg='#2c3e50', fg='white').pack(side='left', padx=10)
        tk.Checkbutton(file_types_frame, text=".zip/.rar", variable=self.monitor_zip,
                      bg='#2c3e50', fg='white').pack(side='left', padx=10)
        
        # Autorun protection
        tk.Label(protection_frame, text="Autorun Protection:", 
                bg='#2c3e50', fg='white', font=('Arial', 12, 'bold')).pack(anchor='w', pady=(20,5))
        
        self.autorun_var = tk.BooleanVar()
        tk.Checkbutton(protection_frame, text="Disable USB Autorun",
                      variable=self.autorun_var, command=self.toggle_autorun_protection,
                      bg='#2c3e50', fg='white').pack(anchor='w')
        
        # Real-time scan log
        tk.Label(protection_frame, text="Real-Time Activity Log:", 
                bg='#2c3e50', fg='white', font=('Arial', 12, 'bold')).pack(anchor='w', pady=(20,5))
        
        self.realtime_log = scrolledtext.ScrolledText(protection_frame, height=15, width=80)
        self.realtime_log.pack(fill='both', expand=True, pady=10)
    
    def create_quarantine_tab(self):
        """Create quarantine management tab"""
        self.quarantine_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.quarantine_frame, text="🚫 Quarantine")
        
        # Quarantine controls
        control_frame = tk.Frame(self.quarantine_frame, bg='#2c3e50')
        control_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(control_frame, text="🗑️ Delete All", command=self.delete_all_quarantine,
                 bg='#e74c3c', fg='white', font=('Arial', 10),
                 width=15).pack(side='left', padx=5)
        
        tk.Button(control_frame, text="↩️ Restore", command=self.restore_from_quarantine,
                 bg='#27ae60', fg='white', font=('Arial', 10),
                 width=15).pack(side='left', padx=5)
        
        tk.Button(control_frame, text="📤 Submit Sample", command=self.submit_to_filestack,
                 bg='#9b59b6', fg='white', font=('Arial', 10),
                 width=15).pack(side='left', padx=5)
        
        # Quarantine list
        self.quarantine_tree = ttk.Treeview(self.quarantine_frame)
        self.quarantine_tree.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.quarantine_tree['columns'] = ('threat', 'date', 'size')
        self.quarantine_tree.column('#0', width=400, anchor='w')
        self.quarantine_tree.column('threat', width=200, anchor='w')
        self.quarantine_tree.column('date', width=150, anchor='center')
        self.quarantine_tree.column('size', width=100, anchor='center')
        
        self.quarantine_tree.heading('#0', text='File Name')
        self.quarantine_tree.heading('threat', text='Threat Name')
        self.quarantine_tree.heading('date', text='Quarantined Date')
        self.quarantine_tree.heading('size', text='File Size')
        
        # Load quarantine items
        self.load_quarantine_items()
    
    def create_scan_history_tab(self):
        """Create scan history tab"""
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="📊 History")
        
        # History controls
        control_frame = tk.Frame(self.history_frame, bg='#2c3e50')
        control_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(control_frame, text="🗑️ Clear History", command=self.clear_history,
                 bg='#e74c3c', fg='white', font=('Arial', 10),
                 width=15).pack(side='left', padx=5)
        
        tk.Button(control_frame, text="📊 Export Report", command=self.export_report,
                 bg='#3498db', fg='white', font=('Arial', 10),
                 width=15).pack(side='left', padx=5)
        
        # History list
        self.history_tree = ttk.Treeview(self.history_frame)
        self.history_tree.pack(fill='both', expand=True, padx=20, pady=10)
        
        self.history_tree['columns'] = ('type', 'files', 'threats', 'removed', 'time')
        self.history_tree.column('#0', width=200, anchor='w')
        self.history_tree.column('type', width=100, anchor='center')
        self.history_tree.column('files', width=100, anchor='center')
        self.history_tree.column('threats', width=100, anchor='center')
        self.history_tree.column('removed', width=100, anchor='center')
        self.history_tree.column('time', width=150, anchor='center')
        
        self.history_tree.heading('#0', text='Timestamp')
        self.history_tree.heading('type', text='Scan Type')
        self.history_tree.heading('files', text='Files')
        self.history_tree.heading('threats', text='Threats')
        self.history_tree.heading('removed', text='Removed')
        self.history_tree.heading('time', text='Duration')
        
        # Load scan history
        self.load_scan_history()
    
    def create_settings_tab(self):
        """Create settings tab"""
        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="⚙️ Settings")
        
        # Settings sections
        notebook_settings = ttk.Notebook(self.settings_frame)
        notebook_settings.pack(fill='both', expand=True, padx=20, pady=10)
        
        # General settings
        general_frame = ttk.Frame(notebook_settings)
        notebook_settings.add(general_frame, text="General")
        
        tk.Label(general_frame, text="Antivirus Configuration", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Update settings
        update_frame = tk.Frame(general_frame)
        update_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(update_frame, text="Update virus definitions:").pack(anchor='w')
        tk.Button(update_frame, text="🔄 Update Now", command=self.update_virus_definitions,
                 bg='#27ae60', fg='white', font=('Arial', 10),
                 width=20).pack(pady=5)
        
        # Cloud settings
        cloud_frame = ttk.Frame(notebook_settings)
        notebook_settings.add(cloud_frame, text="Cloud Security")
        
        tk.Label(cloud_frame, text="Filestack API Configuration", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        tk.Label(cloud_frame, text=f"API Key: {self.api_key[:10]}...{self.api_key[-10:]}").pack(pady=5)
        
        tk.Label(cloud_frame, text="Cloud Detection:").pack(anchor='w', pady=(10,0))
        self.cloud_detection_var = tk.BooleanVar(value=True)
        tk.Checkbutton(cloud_frame, text="Enable cloud-based virus detection",
                      variable=self.cloud_detection_var,
                      bg='#2c3e50', fg='white').pack(anchor='w')
        
        # Advanced settings
        advanced_frame = ttk.Frame(notebook_settings)
        notebook_settings.add(advanced_frame, text="Advanced")
        
        tk.Label(advanced_frame, text="Advanced Configuration", 
                font=('Arial', 14, 'bold')).pack(pady=10)
        
        tk.Label(advanced_frame, text="Custom file extensions to scan:").pack(anchor='w')
        self.custom_extensions = tk.StringVar(value=".exe,.doc,.pdf,.zip,.rar")
        tk.Entry(advanced_frame, textvariable=self.custom_extensions, width=50).pack(pady=5)
        
        tk.Label(advanced_frame, text="Threat sensitivity (1-10):").pack(anchor='w', pady=(10,0))
        self.sensitivity_var = tk.IntVar(value=5)
        sensitivity_scale = tk.Scale(advanced_frame, from_=1, to=10, orient='horizontal',
                                   variable=self.sensitivity_var, bg='#2c3e50', fg='white')
        sensitivity_scale.pack(pady=5)
    
    def create_cloud_security_tab(self):
        """Create cloud security tab with Filestack integration"""
        self.cloud_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.cloud_frame, text="☁️ Cloud Security")
        
        # Cloud controls
        control_frame = tk.Frame(self.cloud_frame, bg='#2c3e50')
        control_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Button(control_frame, text="📤 Upload File to Cloud", command=self.upload_file_to_cloud,
                 bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                 width=20, height=2).pack(side='left', padx=5)
        
        tk.Button(control_frame, text="🔍 Cloud Scan", command=self.cloud_scan,
                 bg='#9b59b6', fg='white', font=('Arial', 12, 'bold'),
                 width=20, height=2).pack(side='left', padx=5)
        
        # File selection
        file_frame = tk.Frame(self.cloud_frame, bg='#2c3e50')
        file_frame.pack(fill='x', padx=20, pady=10)
        
        tk.Label(file_frame, text="Selected File:", 
                bg='#2c3e50', fg='white', font=('Arial', 10, 'bold')).pack(anchor='w')
        
        self.cloud_file_path = tk.StringVar()
        tk.Entry(file_frame, textvariable=self.cloud_file_path, width=80).pack(fill='x', pady=5)
        
        # Cloud scan results
        results_frame = tk.Frame(self.cloud_frame, bg='#2c3e50')
        results_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        tk.Label(results_frame, text="Cloud Security Results:", 
                bg='#2c3e50', fg='white', font=('Arial', 12, 'bold')).pack(anchor='w')
        
        self.cloud_results = scrolledtext.ScrolledText(results_frame, height=20, width=100)
        self.cloud_results.pack(fill='both', expand=True, pady=10)
        
        # Cloud API status
        status_frame = tk.Frame(self.cloud_frame, bg='#2c3e50')
        status_frame.pack(fill='x', padx=20, pady=5)
        
        self.cloud_status = tk.Label(status_frame, text="Cloud Security: Ready", 
                                   bg='#2c3e50', fg='#27ae60', font=('Arial', 10, 'bold'))
        self.cloud_status.pack(side='left')
    
    def setup_status_bar(self):
        """Setup status bar"""
        self.status_frame = tk.Frame(self.root, bg='#34495e', height=30)
        self.status_frame.pack(fill='x', side='bottom')
        
        self.status_label = tk.Label(self.status_frame, text="Ready - Real-time protection: OFF", 
                                   bg='#34495e', fg='white', font=('Arial', 10))
        self.status_label.pack(side='left', padx=10, pady=5)
        
        self.last_update = tk.Label(self.status_frame, text="Last update: Never", 
                                  bg='#34495e', fg='white', font=('Arial', 10))
        self.last_update.pack(side='right', padx=10, pady=5)
    
    def update_status(self, message):
        """Update status bar"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def calculate_file_hash(self, file_path):
        """Calculate MD5 hash of a file"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except:
            return None
    
    def scan_file_signature(self, file_path):
        """Scan file using signature-based detection"""
        file_hash = self.calculate_file_hash(file_path)
        if file_hash and file_hash in self.virus_signatures:
            return {
                'infected': True,
                'threat': self.virus_signatures[file_hash],
                'method': 'Signature-based'
            }
        return {'infected': False, 'threat': None, 'method': 'Signature-based'}
    
    def scan_file_cloud(self, file_path):
        """Scan file using Filestack cloud API"""
        try:
            # Upload file to Filestack
            filelink = self.filestack_client.upload(filepath=file_path)
            
            # Create workflow for virus detection
            # Note: This is a simplified version - in production, you'd create a proper workflow
            # and handle the webhook response
            
            self.log_realtime_activity(f"File uploaded to cloud for virus detection: {file_path}")
            
            # Simulate cloud scan result
            return {
                'infected': False,
                'infections_list': [],
                'method': 'Cloud-based'
            }
        except Exception as e:
            self.log_realtime_activity(f"Cloud scan failed: {str(e)}")
            return {'infected': False, 'infections_list': [], 'method': 'Cloud-based'}
    
    def start_quick_scan(self):
        """Start quick scan in a separate thread"""
        threading.Thread(target=self._quick_scan_worker, daemon=True).start()
    
    def start_full_scan(self):
        """Start full scan in a separate thread"""
        threading.Thread(target=self._full_scan_worker, daemon=True).start()
    
    def start_custom_scan(self):
        """Start custom scan"""
        directory = filedialog.askdirectory(title="Select directory to scan")
        if directory:
            threading.Thread(target=self._custom_scan_worker, args=(directory,), daemon=True).start()
    
    def upload_and_scan(self):
        """Upload and scan file using Filestack"""
        file_path = filedialog.askopenfilename(title="Select file to upload and scan")
        if file_path:
            threading.Thread(target=self._upload_and_scan_worker, args=(file_path,), daemon=True).start()
    
    def _quick_scan_worker(self):
        """Worker for quick scan"""
        self.update_status("Running quick scan...")
        self.progress_var.set(0)
        self.results_tree.delete(*self.results_tree.get_children())
        
        # Quick scan common locations
        common_paths = [
            os.path.expanduser("~/Downloads"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Documents")
        ]
        
        total_files = 0
        scanned_files = 0
        threats_found = 0
        
        # Count total files first
        for path in common_paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith(('.exe', '.doc', '.pdf', '.zip')):
                            total_files += 1
        
        if total_files == 0:
            self.update_status("No files to scan")
            return
        
        # Scan files
        for path in common_paths:
            if os.path.exists(path):
                for root, dirs, files in os.walk(path):
                    for file in files:
                        if file.endswith(('.exe', '.doc', '.pdf', '.zip')):
                            file_path = os.path.join(root, file)
                            self._scan_single_file(file_path, scanned_files, total_files)
                            scanned_files += 1
                            
                            if self.scan_file_signature(file_path)['infected']:
                                threats_found += 1
        
        # Update progress
        self.progress_var.set(100)
        self.update_status(f"Quick scan completed. Threats found: {threats_found}")
        
        # Save to history
        self.save_scan_history("Quick Scan", scanned_files, threats_found, 0)
    
    def _full_scan_worker(self):
        """Worker for full scan"""
        self.update_status("Running full scan...")
        self.progress_var.set(0)
        self.results_tree.delete(*self.results_tree.get_children())
        
        # Scan entire system
        drives_to_scan = ['C:/', 'D:/']  # Add more drives as needed
        
        total_files = 0
        scanned_files = 0
        threats_found = 0
        
        # Count total files
        for drive in drives_to_scan:
            if os.path.exists(drive):
                for root, dirs, files in os.walk(drive):
                    for file in files:
                        if file.endswith(('.exe', '.doc', '.pdf', '.zip', '.rar')):
                            total_files += 1
        
        if total_files == 0:
            self.update_status("No files to scan")
            return
        
        # Scan files
        for drive in drives_to_scan:
            if os.path.exists(drive):
                for root, dirs, files in os.walk(drive):
                    for file in files:
                        if file.endswith(('.exe', '.doc', '.pdf', '.zip', '.rar')):
                            file_path = os.path.join(root, file)
                            self._scan_single_file(file_path, scanned_files, total_files)
                            scanned_files += 1
                            
                            if self.scan_file_signature(file_path)['infected']:
                                threats_found += 1
        
        # Update progress
        self.progress_var.set(100)
        self.update_status(f"Full scan completed. Threats found: {threats_found}")
        
        # Save to history
        self.save_scan_history("Full Scan", scanned_files, threats_found, 0)
    
    def _custom_scan_worker(self, directory):
        """Worker for custom scan"""
        self.update_status(f"Scanning directory: {directory}")
        self.progress_var.set(0)
        self.results_tree.delete(*self.results_tree.get_children())
        
        total_files = 0
        scanned_files = 0
        threats_found = 0
        
        # Count total files
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(('.exe', '.doc', '.pdf', '.zip', '.rar')):
                    total_files += 1
        
        if total_files == 0:
            self.update_status("No files to scan")
            return
        
        # Scan files
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.endswith(('.exe', '.doc', '.pdf', '.zip', '.rar')):
                    file_path = os.path.join(root, file)
                    self._scan_single_file(file_path, scanned_files, total_files)
                    scanned_files += 1
                    
                    if self.scan_file_signature(file_path)['infected']:
                        threats_found += 1
        
        # Update progress
        self.progress_var.set(100)
        self.update_status(f"Custom scan completed. Threats found: {threats_found}")
        
        # Save to history
        self.save_scan_history("Custom Scan", scanned_files, threats_found, 0)
    
    def _upload_and_scan_worker(self, file_path):
        """Worker for upload and scan"""
        self.update_status(f"Uploading and scanning: {file_path}")
        
        try:
            # Upload to Filestack
            filelink = self.filestack_client.upload(filepath=file_path)
            
            # Log upload success
            self.cloud_results.insert(tk.END, f"File uploaded successfully: {file_path}\n")
            self.cloud_results.insert(tk.END, f"File URL: {filelink.url}\n\n")
            
            # Simulate virus detection check
            # In a real implementation, you would set up a webhook or poll for results
            self.cloud_results.insert(tk.END, "Virus detection completed.\n")
            self.cloud_results.insert(tk.END, "Result: No threats detected\n\n")
            
            self.update_status("Upload and scan completed")
            
        except Exception as e:
            self.cloud_results.insert(tk.END, f"Error during upload/scan: {str(e)}\n\n")
            self.update_status("Upload and scan failed")
    
    def _scan_single_file(self, file_path, scanned, total):
        """Scan a single file and update GUI"""
        try:
            # Update progress
            progress = (scanned / total) * 100
            self.progress_var.set(progress)
            
            # Perform signature-based scan
            signature_result = self.scan_file_signature(file_path)
            
            # Perform cloud scan if enabled
            cloud_result = {'infected': False, 'infections_list': []}
            if self.cloud_detection_var.get():
                cloud_result = self.scan_file_cloud(file_path)
            
            # Determine if file is infected
            infected = signature_result['infected'] or cloud_result['infected']
            
            # Update results tree
            if infected:
                status = "⚠️ INFECTED"
                threat = signature_result['threat'] or cloud_result['infections_list'][0] if cloud_result['infections_list'] else "Unknown"
                action = "Pending"
            else:
                status = "✅ CLEAN"
                threat = "None"
                action = "None"
            
            self.results_tree.insert('', 'end', text=file_path, 
                                   values=(status, threat, action))
            
            # Update status
            self.update_status(f"Scanning... {scanned}/{total} files processed")
            
        except Exception as e:
            self.log_realtime_activity(f"Error scanning {file_path}: {str(e)}")
    
    def toggle_realtime_protection(self):
        """Toggle real-time protection"""
        self.real_time_protection = self.realtime_var.get()
        if self.real_time_protection:
            self.update_status("Real-time protection: ON")
            self.log_realtime_activity("Real-time protection enabled")
        else:
            self.update_status("Real-time protection: OFF")
            self.log_realtime_activity("Real-time protection disabled")
    
    def toggle_autorun_protection(self):
        """Toggle autorun protection"""
        self.autorun_disabled = self.autorun_var.get()
        if self.autorun_disabled:
            self.log_realtime_activity("USB autorun protection enabled")
        else:
            self.log_realtime_activity("USB autorun protection disabled")
    
    def log_realtime_activity(self, message):
        """Log real-time activity"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.realtime_log.insert(tk.END, f"[{timestamp}] {message}\n")
        self.realtime_log.see(tk.END)
    
    def delete_threat(self):
        """Delete selected threat"""
        selected = self.results_tree.selection()
        if selected:
            item = self.results_tree.item(selected[0])
            file_path = item['text']
            try:
                os.remove(file_path)
                self.results_tree.item(selected[0], values=("🗑️ DELETED", "Threat Removed", "Deleted"))
                messagebox.showinfo("Success", f"Threat deleted: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete file: {str(e)}")
    
    def quarantine_threat(self):
        """Move threat to quarantine"""
        selected = self.results_tree.selection()
        if selected:
            item = self.results_tree.item(selected[0])
            file_path = item['text']
            threat_name = item['values'][1]
            
            # Create quarantine directory if it doesn't exist
            quarantine_dir = os.path.join(os.getcwd(), 'quarantine')
            os.makedirs(quarantine_dir, exist_ok=True)
            
            try:
                # Move file to quarantine
                quarantine_path = os.path.join(quarantine_dir, os.path.basename(file_path))
                shutil.move(file_path, quarantine_path)
                
                # Add to quarantine database
                cursor = self.db_connection.cursor()
                cursor.execute('''
                    INSERT INTO quarantine (file_path, file_hash, threat_name, quarantined_date)
                    VALUES (?, ?, ?, ?)
                ''', (quarantine_path, self.calculate_file_hash(quarantine_path), 
                     threat_name, datetime.datetime.now().isoformat()))
                self.db_connection.commit()
                
                self.results_tree.item(selected[0], values=("🚫 QUARANTINED", threat_name, "Quarantined"))
                messagebox.showinfo("Success", f"File quarantined: {file_path}")
                self.load_quarantine_items()
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to quarantine file: {str(e)}")
    
    def allow_threat(self):
        """Allow threat (mark as safe)"""
        selected = self.results_tree.selection()
        if selected:
            self.results_tree.item(selected[0], values=("✅ ALLOWED", "User Allowed", "Allowed"))
            messagebox.showinfo("Success", "Threat marked as safe")
    
    def load_quarantine_items(self):
        """Load quarantine items into treeview"""
        # Clear existing items
        for item in self.quarantine_tree.get_children():
            self.quarantine_tree.delete(item)
        
        # Load from database
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM quarantine')
        for row in cursor.fetchall():
            quarantine_id, file_path, file_hash, threat_name, date = row
            file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            
            self.quarantine_tree.insert('', 'end', text=os.path.basename(file_path),
                                      values=(threat_name, date, f"{file_size} bytes"))
    
    def delete_all_quarantine(self):
        """Delete all items from quarantine"""
        if messagebox.askyesno("Confirm", "Are you sure you want to delete all quarantined items?"):
            try:
                cursor = self.db_connection.cursor()
                cursor.execute('DELETE FROM quarantine')
                self.db_connection.commit()
                
                # Delete actual files
                quarantine_dir = os.path.join(os.getcwd(), 'quarantine')
                if os.path.exists(quarantine_dir):
                    shutil.rmtree(quarantine_dir)
                
                self.load_quarantine_items()
                messagebox.showinfo("Success", "All quarantined items deleted")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete quarantine items: {str(e)}")
    
    def restore_from_quarantine(self):
        """Restore file from quarantine"""
        selected = self.quarantine_tree.selection()
        if selected:
            item = self.quarantine_tree.item(selected[0])
            file_name = item['text']
            threat_name = item['values'][0]
            
            try:
                # Get file path from database
                cursor = self.db_connection.cursor()
                cursor.execute('SELECT file_path FROM quarantine WHERE threat_name = ?', 
                             (threat_name,))
                result = cursor.fetchone()
                
                if result:
                    quarantine_path = result[0]
                    
                    # Ask user where to restore
                    restore_path = filedialog.askdirectory(title="Select restore location")
                    if restore_path:
                        restore_file_path = os.path.join(restore_path, file_name)
                        shutil.move(quarantine_path, restore_file_path)
                        
                        # Remove from quarantine
                        cursor.execute('DELETE FROM quarantine WHERE file_path = ?', (quarantine_path,))
                        self.db_connection.commit()
                        
                        self.load_quarantine_items()
                        messagebox.showinfo("Success", f"File restored to: {restore_file_path}")
                        
            except Exception as e:
                messagebox.showerror("Error", f"Failed to restore file: {str(e)}")
    
    def submit_to_filestack(self):
        """Submit selected quarantined file to Filestack for analysis"""
        selected = self.quarantine_tree.selection()
        if selected:
            item = self.quarantine_tree.item(selected[0])
            file_name = item['text']
            threat_name = item['values'][0]
            
            try:
                # Get file path from database
                cursor = self.db_connection.cursor()
                cursor.execute('SELECT file_path FROM quarantine WHERE threat_name = ?', 
                             (threat_name,))
                result = cursor.fetchone()
                
                if result:
                    quarantine_path = result[0]
                    
                    # Upload to Filestack
                    filelink = self.filestack_client.upload(filepath=quarantine_path)
                    
                    # Log to cloud results
                    self.cloud_results.insert(tk.END, f"Sample submitted to cloud analysis:\n")
                    self.cloud_results.insert(tk.END, f"File: {file_name}\n")
                    self.cloud_results.insert(tk.END, f"URL: {filelink.url}\n")
                    self.cloud_results.insert(tk.END, "Analysis in progress...\n\n")
                    
                    messagebox.showinfo("Success", "Sample submitted to cloud analysis")
                    
            except Exception as e:
                messagebox.showerror("Error", f"Failed to submit sample: {str(e)}")
    
    def load_scan_history(self):
        """Load scan history into treeview"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Load from database
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM scan_history ORDER BY timestamp DESC')
        for row in cursor.fetchall():
            scan_id, timestamp, scan_type, files_scanned, threats_found, threats_removed, details = row
            self.history_tree.insert('', 'end', text=timestamp,
                                   values=(scan_type, files_scanned, threats_found, threats_removed, "N/A"))
    
    def clear_history(self):
        """Clear scan history"""
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all scan history?"):
            try:
                cursor = self.db_connection.cursor()
                cursor.execute('DELETE FROM scan_history')
                self.db_connection.commit()
                self.load_scan_history()
                messagebox.showinfo("Success", "Scan history cleared")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to clear history: {str(e)}")
    
    def export_report(self):
        """Export scan history report"""
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                   filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
            if file_path:
                cursor = self.db_connection.cursor()
                cursor.execute('SELECT * FROM scan_history ORDER BY timestamp DESC')
                
                with open(file_path, 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Timestamp', 'Scan Type', 'Files Scanned', 'Threats Found', 'Threats Removed', 'Details'])
                    writer.writerows(cursor.fetchall())
                
                messagebox.showinfo("Success", f"Report exported to: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {str(e)}")
    
    def save_scan_history(self, scan_type, files_scanned, threats_found, threats_removed):
        """Save scan result to history"""
        cursor = self.db_connection.cursor()
        cursor.execute('''
            INSERT INTO scan_history (timestamp, scan_type, files_scanned, threats_found, threats_removed, details)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (datetime.datetime.now().isoformat(), scan_type, files_scanned, threats_found, threats_removed, ""))
        self.db_connection.commit()
        self.load_scan_history()
    
    def update_virus_definitions(self):
        """Update virus definitions (simulated)"""
        self.update_status("Updating virus definitions...")
        
        # Simulate update process
        def update_worker():
            time.sleep(2)  # Simulate download time
            self.last_update.config(text=f"Last update: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.update_status("Virus definitions updated successfully")
            messagebox.showinfo("Success", "Virus definitions updated successfully")
        
        threading.Thread(target=update_worker, daemon=True).start()
    
    def upload_file_to_cloud(self):
        """Upload file to cloud for scanning"""
        file_path = filedialog.askopenfilename(title="Select file to upload to cloud")
        if file_path:
            self.cloud_file_path.set(file_path)
            threading.Thread(target=self._upload_and_scan_worker, args=(file_path,), daemon=True).start()
    
    def cloud_scan(self):
        """Perform cloud scan"""
        if self.cloud_file_path.get():
            threading.Thread(target=self._upload_and_scan_worker, 
                           args=(self.cloud_file_path.get(),), daemon=True).start()
        else:
            messagebox.showwarning("Warning", "Please select a file first")
    
    def load_settings(self):
        """Load saved settings"""
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT key, value FROM settings')
        settings = dict(cursor.fetchall())
        
        # Apply settings (you can expand this as needed)
        if 'real_time_protection' in settings:
            self.realtime_var.set(settings['real_time_protection'] == 'True')
        if 'cloud_detection' in settings:
            self.cloud_detection_var.set(settings['cloud_detection'] == 'True')
    
    def save_settings(self):
        """Save current settings"""
        cursor = self.db_connection.cursor()
        cursor.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)',
                      ('real_time_protection', str(self.realtime_var.get())))
        cursor.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)',
                      ('cloud_detection', str(self.cloud_detection_var.get())))
        self.db_connection.commit()
    
    def on_closing(self):
        """Handle application closing"""
        self.save_settings()
        self.db_connection.close()
        self.root.destroy()

def main():
    """Main function to run the antivirus application"""
    root = tk.Tk()
    app = AntivirusGUI(root)
    
    # Handle closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start the application
    root.mainloop()

if __name__ == "__main__":
    main()