#!/usr/bin/env python3
"""
DeepMailer v1.0 - Installation Verification Script

This script verifies that all dependencies and system requirements
are properly installed and configured for running DeepMailer.
"""

import sys
import os
import platform
import subprocess
from pathlib import Path

def print_header(title):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def check_mark(success):
    """Return checkmark or X based on success"""
    return "✓" if success else "✗"

def check_python_version():
    """Check Python version compatibility"""
    version = sys.version_info
    compatible = version >= (3, 8)
    print(f"{check_mark(compatible)} Python {version.major}.{version.minor}.{version.micro}")
    if not compatible:
        print("   ⚠️  Python 3.8+ required")
    return compatible

def check_dependency(module_name, import_name=None):
    """Check if a dependency is installed"""
    if import_name is None:
        import_name = module_name
    
    try:
        __import__(import_name)
        print(f"✓ {module_name}")
        return True
    except ImportError as e:
        print(f"✗ {module_name} - {e}")
        return False

def check_system_libraries():
    """Check system libraries (Linux specific)"""
    if platform.system().lower() != 'linux':
        print("✓ System libraries (Windows/macOS - not applicable)")
        return True
    
    # Try to import PyQt6 to test system libraries
    try:
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'  # Force offscreen for testing
        from PyQt6.QtWidgets import QApplication
        app = QApplication([])
        print("✓ PyQt6 system libraries")
        return True
    except Exception as e:
        print(f"✗ PyQt6 system libraries - {e}")
        return False

def check_file_structure():
    """Check if required files exist"""
    required_files = [
        'main.py',
        'requirements.txt',
        'core/__init__.py',
        'ui/__init__.py',
        'modules/__init__.py'
    ]
    
    all_present = True
    for file_path in required_files:
        exists = Path(file_path).exists()
        print(f"{check_mark(exists)} {file_path}")
        if not exists:
            all_present = False
    
    return all_present

def check_data_directories():
    """Check if data directories can be created"""
    try:
        from core.utils import setup_directories
        setup_directories()
        print("✓ Data directories")
        return True
    except Exception as e:
        print(f"✗ Data directories - {e}")
        return False

def run_basic_functionality_test():
    """Test basic application functionality"""
    try:
        # Set headless mode
        os.environ['QT_QPA_PLATFORM'] = 'offscreen'
        
        # Test core imports
        from core.utils import load_config
        from core.logger import setup_logging
        from modules.data_manager import DataManager
        
        # Test configuration
        config = load_config()
        print("✓ Configuration system")
        
        # Test logging
        setup_logging()
        print("✓ Logging system")
        
        # Test data manager
        dm = DataManager()
        print("✓ Data management")
        
        return True
    except Exception as e:
        print(f"✗ Basic functionality - {e}")
        return False

def provide_recommendations(issues):
    """Provide recommendations based on found issues"""
    if not issues:
        print_header("🎉 ALL CHECKS PASSED!")
        print("DeepMailer is ready to run!")
        print("\nTo start the application:")
        print("  Windows: run_deepmailer.bat")
        print("  Linux/Mac: python run_deepmailer.py")
        return
    
    print_header("⚠️  ISSUES FOUND")
    
    for issue in issues:
        if "Python" in issue:
            print("📝 Install Python 3.8+ from https://python.org")
        
        elif "PyQt6" in issue:
            print("📝 Install PyQt6 dependencies:")
            print("   pip install PyQt6")
            if platform.system().lower() == 'linux':
                print("   sudo apt-get install libgl1 libxkbcommon-x11-0 libxcb-cursor0")
        
        elif any(dep in issue for dep in ['Faker', 'pandas', 'openpyxl', 'psutil']):
            print("📝 Install missing Python packages:")
            print("   pip install -r requirements.txt")
        
        elif "system libraries" in issue:
            print("📝 Install system libraries (Linux):")
            print("   sudo apt-get install libgl1 libxkbcommon-x11-0 libxcb-cursor0")
            print("   sudo apt-get install libfontconfig1 libx11-xcb1 libegl1")
        
        elif "file structure" in issue:
            print("📝 Ensure you're in the correct DeepMailer directory")
        
        elif "directories" in issue:
            print("📝 Check file permissions and available disk space")

def main():
    """Main verification function"""
    print_header("DeepMailer v1.0 - Installation Verification")
    print(f"System: {platform.system()} {platform.release()}")
    print(f"Architecture: {platform.machine()}")
    
    issues = []
    
    # Check Python version
    print_header("Python Version")
    if not check_python_version():
        issues.append("Python version")
    
    # Check file structure
    print_header("File Structure")
    if not check_file_structure():
        issues.append("File structure")
    
    # Check Python dependencies
    print_header("Python Dependencies")
    dependencies = [
        ('PyQt6', 'PyQt6.QtWidgets'),
        ('Faker', 'faker'),
        ('Pandas', 'pandas'),
        ('OpenPyXL', 'openpyxl'),
        ('Requests', 'requests'),
        ('PSUtil', 'psutil')
    ]
    
    for dep_name, import_name in dependencies:
        if not check_dependency(dep_name, import_name):
            issues.append(f"{dep_name} dependency")
    
    # Check system libraries
    print_header("System Libraries")
    if not check_system_libraries():
        issues.append("PyQt6 system libraries")
    
    # Check data directories
    print_header("Data Directories")
    if not check_data_directories():
        issues.append("Data directories")
    
    # Run functionality test
    print_header("Basic Functionality")
    if not run_basic_functionality_test():
        issues.append("Basic functionality")
    
    # Provide recommendations
    provide_recommendations(issues)

if __name__ == "__main__":
    main()