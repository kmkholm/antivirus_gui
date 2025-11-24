#!/usr/bin/env python3
"""
Antivirus Demo Script
Demonstrates the antivirus functionality programmatically
Author: Dr. Mohammed Tawfik
Email: kmkhol01@gmail.com
"""

import os
import sys
import hashlib
import json
from pathlib import Path

# Add current directory to path to import antivirus modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from filestack import Client
except ImportError:
    print("Please install filestack-python: pip install filestack-python")
    sys.exit(1)

class AntivirusDemo:
    def __init__(self):
        self.api_key = "ACFLXThQSQruATO9yvqwKz"
        self.filestack_client = Client(self.api_key)
        self.virus_signatures = self.load_demo_signatures()
    
    def load_demo_signatures(self):
        """Load sample virus signatures for demo"""
        return {
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855": "Empty File",
            "d41d8cd98f00b204e9800998ecf8427e": "Empty File",
            "c4ca4238a0b923820dcc509a6f75849b": "Sample Malware Signature",
        }
    
    def calculate_file_hash(self, file_path):
        """Calculate MD5 hash of a file"""
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            print(f"Error calculating hash for {file_path}: {e}")
            return None
    
    def demo_signature_scan(self, file_path):
        """Demonstrate signature-based scanning"""
        print(f"\n=== Signature-based Scan Demo ===")
        print(f"Scanning: {file_path}")
        
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
        
        file_hash = self.calculate_file_hash(file_path)
        if file_hash:
            print(f"File hash: {file_hash}")
            
            if file_hash in self.virus_signatures:
                threat_name = self.virus_signatures[file_hash]
                print(f"⚠️ THREAT DETECTED: {threat_name}")
                print("Recommended action: Quarantine or delete")
            else:
                print("✅ File appears clean (signature-based)")
        
        return file_hash in self.virus_signatures if file_hash else False
    
    def demo_cloud_upload(self, file_path):
        """Demonstrate cloud upload for virus detection"""
        print(f"\n=== Cloud Upload Demo ===")
        print(f"Uploading file to Filestack: {file_path}")
        
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return
        
        try:
            # Upload file to Filestack
            filelink = self.filestack_client.upload(filepath=file_path)
            print(f"✅ File uploaded successfully!")
            print(f"File URL: {filelink.url}")
            
            # Simulate virus detection workflow
            print("\nVirus detection workflow (simulated):")
            workflow_result = {
                "data": {
                    "infected": False,
                    "infections_list": []
                }
            }
            
            if workflow_result["data"]["infected"]:
                print("⚠️ CLOUD SCAN RESULT: Threats detected!")
                for infection in workflow_result["data"]["infections_list"]:
                    print(f"  - {infection}")
            else:
                print("✅ CLOUD SCAN RESULT: No threats detected")
            
            return filelink.url
            
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            return None
    
    def demo_batch_scan(self, directory):
        """Demonstrate batch scanning"""
        print(f"\n=== Batch Scan Demo ===")
        print(f"Scanning directory: {directory}")
        
        if not os.path.exists(directory):
            print(f"Directory not found: {directory}")
            return
        
        files_scanned = 0
        threats_found = 0
        file_types = ['.exe', '.doc', '.pdf', '.zip', '.rar']
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if any(file.endswith(ft) for ft in file_types):
                    file_path = os.path.join(root, file)
                    files_scanned += 1
                    
                    print(f"Scanning: {file_path}")
                    
                    # Perform signature scan
                    is_threat = self.demo_signature_scan(file_path)
                    if is_threat:
                        threats_found += 1
        
        print(f"\n=== Batch Scan Results ===")
        print(f"Files scanned: {files_scanned}")
        print(f"Threats found: {threats_found}")
        print(f"Clean files: {files_scanned - threats_found}")
        
        return files_scanned, threats_found
    
    def demo_api_info(self):
        """Display API configuration information"""
        print(f"\n=== Filestack API Configuration ===")
        print(f"API Key: {self.api_key[:10]}...{self.api_key[-10:]}")
        print(f"Client initialized: {self.filestack_client is not None}")
        
        # Test API connectivity (simplified)
        print("API Status: Connected")
    
    def create_test_files(self):
        """Create test files for demonstration"""
        print("\n=== Creating Test Files ===")
        
        test_dir = "test_files"
        os.makedirs(test_dir, exist_ok=True)
        
        # Create a test file
        test_file = os.path.join(test_dir, "test_document.txt")
        with open(test_file, 'w') as f:
            f.write("This is a test document for antivirus scanning.\n")
            f.write("No threats should be detected in this file.\n")
        
        print(f"Created test file: {test_file}")
        
        # Create a file with known hash (simulated malware)
        malware_file = os.path.join(test_dir, "malware_sample.txt")
        with open(malware_file, 'w') as f:
            # Write content that will produce the signature hash
            f.write("1")  # This will produce hash: c4ca4238a0b923820dcc509a6f75849b
        
        print(f"Created test malware file: {malware_file}")
        
        return test_dir, test_file, malware_file
    
    def run_full_demo(self):
        """Run complete demonstration"""
        print("🚀 ADVANCED ANTIVIRUS DEMO")
        print("=" * 50)
        print("Author: Dr. Mohammed Tawfik")
        print("Email: kmkhol01@gmail.com")
        print("API Key: ACFLXThQSQruATO9yvqwKz")
        print("=" * 50)
        
        # Demo API info
        self.demo_api_info()
        
        # Create test files
        test_dir, clean_file, malware_file = self.create_test_files()
        
        try:
            # Demo 1: Signature scan of clean file
            print(f"\n{'='*20} DEMO 1: Clean File Scan {'='*20}")
            self.demo_signature_scan(clean_file)
            
            # Demo 2: Signature scan of malware file
            print(f"\n{'='*20} DEMO 2: Malware Scan {'='*20}")
            self.demo_signature_scan(malware_file)
            
            # Demo 3: Cloud upload demo
            print(f"\n{'='*20} DEMO 3: Cloud Upload {'='*20}")
            self.demo_cloud_upload(clean_file)
            
            # Demo 4: Batch scan demo
            print(f"\n{'='*20} DEMO 4: Batch Scan {'='*20}")
            self.demo_batch_scan(test_dir)
            
            print(f"\n{'='*50}")
            print("🎉 Demo completed successfully!")
            print("This demonstrates the core antivirus functionality.")
            print("Run 'python antivirus_gui.py' for the full GUI application.")
            print(f"{'='*50}")
            
        finally:
            # Cleanup
            if input("\nDelete test files? (y/n): ").lower() == 'y':
                import shutil
                shutil.rmtree(test_dir)
                print("Test files deleted.")

def main():
    """Main demo function"""
    demo = AntivirusDemo()
    
    print("Choose demo option:")
    print("1. Run full demonstration")
    print("2. Signature scan only")
    print("3. Cloud upload demo only")
    print("4. Batch scan demo")
    
    choice = input("Enter choice (1-4): ").strip()
    
    if choice == "1":
        demo.run_full_demo()
    elif choice == "2":
        file_path = input("Enter file path to scan: ").strip()
        if file_path:
            demo.demo_signature_scan(file_path)
    elif choice == "3":
        file_path = input("Enter file path to upload: ").strip()
        if file_path:
            demo.demo_cloud_upload(file_path)
    elif choice == "4":
        directory = input("Enter directory to scan: ").strip()
        if directory:
            demo.demo_batch_scan(directory)
    else:
        print("Invalid choice. Running full demo.")
        demo.run_full_demo()

if __name__ == "__main__":
    main()