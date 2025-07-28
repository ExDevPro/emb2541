#!/usr/bin/env python3
"""
Test script for DeepMailer v1.0 without GUI

This script tests the core modules and data structures without requiring a display.
"""

import sys
import os
sys.path.append('.')

def test_imports():
    """Test all module imports"""
    try:
        # Test core utilities
        from core.utils import setup_directories, load_config, save_config
        print("✅ Core utilities imported successfully")
        
        # Test data manager
        from modules.data_manager import DataManager
        print("✅ Data manager imported successfully")
        
        # Test setup directories
        setup_directories()
        print("✅ Directories created successfully")
        
        # Test config loading
        config = load_config()
        print(f"✅ Configuration loaded: {len(config)} settings")
        
        # Test data manager
        dm = DataManager()
        leads_count = dm.get_total_leads()
        smtp_count = dm.get_total_smtp_servers()
        print(f"✅ Data manager initialized - {leads_count} leads, {smtp_count} SMTPs")
        
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_directory_structure():
    """Test directory structure"""
    required_dirs = [
        "Data/Leads",
        "Data/SMTP", 
        "Data/Subject",
        "Data/Message",
        "Data/Campaigns",
        "Data/Settings",
        "Data/Logs",
        "Resource/Images",
        "Resource/Theme", 
        "Resource/Fonts"
    ]
    
    all_exist = True
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}")
        else:
            print(f"❌ {directory} - Missing")
            all_exist = False
            
    return all_exist

def test_config_management():
    """Test configuration management"""
    try:
        from core.utils import load_config, save_config
        
        # Load config
        config = load_config()
        original_theme = config.get('theme', 'dark')
        
        # Modify and save
        config['test_value'] = 'test'
        save_config(config)
        
        # Reload and verify
        new_config = load_config()
        if new_config.get('test_value') == 'test':
            print("✅ Configuration save/load works")
            
            # Clean up
            del new_config['test_value']
            save_config(new_config)
            return True
        else:
            print("❌ Configuration save/load failed")
            return False
            
    except Exception as e:
        print(f"❌ Configuration test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing DeepMailer v1.0 Core Components\n")
    
    tests = [
        ("Module Imports", test_imports),
        ("Directory Structure", test_directory_structure),
        ("Configuration Management", test_config_management)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Testing {test_name}:")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Core functionality is working.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())