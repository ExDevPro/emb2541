#!/usr/bin/env python3
"""
Comprehensive Test Suite for DeepMailer v1.0

This script runs all available tests to verify the complete functionality.
"""

import sys
import os
import subprocess
import time

def run_test_script(script_name):
    """Run a test script and return the result"""
    print(f"🔄 Running {script_name}...")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name], 
            capture_output=True, 
            text=True, 
            timeout=120
        )
        
        if result.returncode == 0:
            print(f"✅ {script_name} PASSED")
            return True
        else:
            print(f"❌ {script_name} FAILED")
            print("STDOUT:", result.stdout[-500:] if len(result.stdout) > 500 else result.stdout)
            print("STDERR:", result.stderr[-500:] if len(result.stderr) > 500 else result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {script_name} TIMED OUT")
        return False
    except Exception as e:
        print(f"💥 {script_name} ERROR: {e}")
        return False

def test_directory_structure():
    """Test that all required directories exist"""
    print("\n🧪 Testing Directory Structure")
    
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
        "Resource/Fonts",
        "core",
        "modules",
        "ui/modules",
        "ui/widgets"
    ]
    
    all_exist = True
    for directory in required_dirs:
        if os.path.exists(directory):
            print(f"✅ {directory}")
        else:
            print(f"❌ {directory} - Missing")
            all_exist = False
            
    return all_exist

def test_file_structure():
    """Test that all required files exist"""
    print("\n🧪 Testing File Structure")
    
    required_files = [
        "main.py",
        "requirements.txt",
        "core/__init__.py",
        "core/utils.py",
        "core/logger.py",
        "core/main_window.py",
        "modules/__init__.py",
        "modules/data_manager.py",
        "modules/placeholders.py",
        "ui/__init__.py",
        "ui/modules/__init__.py",
        "ui/modules/dashboard.py",
        "ui/modules/leads.py",
        "ui/modules/smtp.py",
        "ui/modules/subjects.py",
        "ui/modules/messages.py",
        "ui/modules/campaigns.py",
        "ui/modules/configurations.py",
        "ui/modules/settings.py",
        "Resource/Theme/dark.qss"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing")
            all_exist = False
            
    return all_exist

def test_imports():
    """Test that all modules can be imported"""
    print("\n🧪 Testing Module Imports")
    
    imports_to_test = [
        ("core.utils", "setup_directories, load_config"),
        ("core.logger", "setup_logging"),
        ("modules.data_manager", "DataManager"),
        ("modules.placeholders", "PlaceholderEngine"),
        ("ui.modules.dashboard", "DashboardWidget"),
        ("ui.modules.leads", "LeadsWidget"),
        ("ui.modules.smtp", "SMTPWidget")
    ]
    
    all_passed = True
    for module_name, objects in imports_to_test:
        try:
            exec(f"from {module_name} import {objects}")
            print(f"✅ {module_name}")
        except Exception as e:
            print(f"❌ {module_name} - {e}")
            all_passed = False
            
    return all_passed

def display_project_stats():
    """Display project statistics"""
    print("\n📊 Project Statistics")
    
    # Count Python files
    python_files = []
    for root, dirs, files in os.walk("."):
        # Skip hidden directories and __pycache__
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
                
    print(f"📄 Python files: {len(python_files)}")
    
    # Count total lines of code
    total_lines = 0
    total_characters = 0
    
    for file_path in python_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.count('\n')
                total_lines += lines
                total_characters += len(content)
        except:
            pass
            
    print(f"📝 Total lines of code: {total_lines:,}")
    print(f"🔤 Total characters: {total_characters:,}")
    
    # Count data files
    data_files = []
    resource_files = []
    
    for root, dirs, files in os.walk("Data"):
        for file in files:
            data_files.append(os.path.join(root, file))
            
    for root, dirs, files in os.walk("Resource"):
        for file in files:
            resource_files.append(os.path.join(root, file))
            
    print(f"💾 Data files: {len(data_files)}")
    print(f"🎨 Resource files: {len(resource_files)}")
    
    # Calculate project size
    total_size = 0
    for root, dirs, files in os.walk("."):
        for file in files:
            if not file.startswith('.'):
                try:
                    total_size += os.path.getsize(os.path.join(root, file))
                except:
                    pass
                    
    print(f"📦 Project size: {total_size / 1024:.1f} KB")

def main():
    """Run all tests"""
    print("🧪 DeepMailer v1.0 - Comprehensive Test Suite")
    print("=" * 50)
    
    start_time = time.time()
    
    # Test scripts to run
    test_scripts = [
        "test_core.py",
        "test_leads.py", 
        "test_placeholders.py",
        "test_smtp.py"
    ]
    
    # Individual tests
    individual_tests = [
        ("Directory Structure", test_directory_structure),
        ("File Structure", test_file_structure),
        ("Module Imports", test_imports)
    ]
    
    # Run individual tests
    passed_individual = 0
    total_individual = len(individual_tests)
    
    for test_name, test_func in individual_tests:
        if test_func():
            passed_individual += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
            
    # Run test scripts
    passed_scripts = 0
    total_scripts = len(test_scripts)
    
    print(f"\n🔄 Running {total_scripts} test scripts...")
    print("-" * 40)
    
    for script in test_scripts:
        if os.path.exists(script):
            if run_test_script(script):
                passed_scripts += 1
        else:
            print(f"⚠️  {script} not found - skipping")
            
    # Calculate results
    total_tests = total_individual + total_scripts
    total_passed = passed_individual + passed_scripts
    
    elapsed_time = time.time() - start_time
    
    # Display results
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    print(f"Individual Tests: {passed_individual}/{total_individual} passed")
    print(f"Test Scripts: {passed_scripts}/{total_scripts} passed")
    print(f"Total Tests: {total_passed}/{total_tests} passed")
    print(f"Success Rate: {(total_passed/total_tests)*100:.1f}%")
    print(f"Execution Time: {elapsed_time:.2f} seconds")
    
    # Display project stats
    display_project_stats()
    
    # Final verdict
    print("\n" + "=" * 50)
    if total_passed == total_tests:
        print("🎉 ALL TESTS PASSED! DeepMailer v1.0 is functioning correctly.")
        print("✅ Core functionality verified")
        print("✅ Data management working")
        print("✅ Placeholders system operational")
        print("✅ SMTP management functional")
        print("✅ Application structure solid")
        
        print("\n🚀 Ready for continued development!")
        return 0
    else:
        print(f"⚠️  {total_tests - total_passed} tests failed.")
        print("❌ Some functionality may not be working correctly.")
        print("🔧 Please review the failed tests above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())