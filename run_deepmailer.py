#!/usr/bin/env python3
"""
DeepMailer v1.0 - Startup Script

This script provides a convenient way to start DeepMailer with proper
environment setup and error handling for different platforms.
"""

import sys
import os
import subprocess
import platform
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("ERROR: DeepMailer requires Python 3.8 or higher")
        print(f"Current version: {sys.version}")
        return False
    return True

def install_dependencies():
    """Install required dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to install dependencies: {e}")
        return False

def main():
    """Main startup function"""
    print("="*60)
    print("DeepMailer v1.0 - Professional Email Marketing Software")
    print("="*60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check if requirements.txt exists
    if not Path("requirements.txt").exists():
        print("ERROR: requirements.txt not found")
        sys.exit(1)
    
    # Ask user if they want to install dependencies
    try:
        import PyQt6
        import faker
        import pandas
        import openpyxl
        import psutil
        print("✓ All dependencies are installed")
    except ImportError as e:
        print(f"Missing dependencies detected: {e}")
        response = input("Install missing dependencies? (y/n): ").lower().strip()
        if response == 'y':
            if not install_dependencies():
                sys.exit(1)
        else:
            print("Cannot continue without dependencies")
            sys.exit(1)
    
    # Start the application
    print("\nStarting DeepMailer...")
    try:
        # Import and run main
        from main import main as app_main
        app_main()
    except Exception as e:
        print(f"Failed to start DeepMailer: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()