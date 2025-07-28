#!/usr/bin/env python3
"""
Test Leads Management functionality

This script tests the leads management module functionality without GUI.
"""

import sys
import os
import csv
import tempfile
from pathlib import Path
sys.path.append('.')

from modules.data_manager import DataManager

def create_test_csv():
    """Create a test CSV file"""
    test_data = [
        ['email', 'first_name', 'last_name', 'company'],
        ['john@example.com', 'John', 'Doe', 'Example Corp'],
        ['jane@test.com', 'Jane', 'Smith', 'Test Inc'],
        ['bob@sample.org', 'Bob', 'Johnson', 'Sample LLC'],
        ['invalid-email', 'Invalid', 'User', 'No Company']
    ]
    
    temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False)
    writer = csv.writer(temp_file)
    writer.writerows(test_data)
    temp_file.close()
    
    return temp_file.name

def test_leads_management():
    """Test leads management functionality"""
    print("🧪 Testing Leads Management\n")
    
    dm = DataManager()
    test_list_name = "test_leads_list"
    
    try:
        # Test 1: Create a test CSV and import it
        print("📋 Test 1: Import leads from CSV")
        csv_file = create_test_csv()
        
        success, message, count = dm.import_leads_from_file(csv_file, test_list_name)
        
        if success:
            print(f"✅ Import successful: {message}")
            print(f"   Imported {count} leads")
        else:
            print(f"❌ Import failed: {message}")
            return False
            
        # Clean up test file
        os.unlink(csv_file)
        
        # Test 2: Load the imported list
        print("\n📋 Test 2: Load imported leads list")
        headers, data = dm.load_leads_list(test_list_name)
        
        if headers and data:
            print(f"✅ List loaded successfully")
            print(f"   Headers: {headers}")
            print(f"   Data rows: {len(data)}")
            
            # Verify data
            expected_headers = ['email', 'first_name', 'last_name', 'company']
            if headers == expected_headers:
                print("✅ Headers match expected")
            else:
                print(f"❌ Headers mismatch. Expected: {expected_headers}, Got: {headers}")
                
            if len(data) == 4:  # Should have 4 data rows (excluding header)
                print("✅ Data count correct")
            else:
                print(f"❌ Data count mismatch. Expected: 4, Got: {len(data)}")
        else:
            print("❌ Failed to load list")
            return False
            
        # Test 3: Get leads lists info
        print("\n📋 Test 3: Get leads lists information")
        lists = dm.get_leads_lists()
        
        test_list_found = False
        for list_info in lists:
            if list_info['name'] == test_list_name:
                test_list_found = True
                print(f"✅ Found test list: {list_info['name']}")
                print(f"   Row count: {list_info['row_count']}")
                print(f"   Size: {list_info['size']} bytes")
                break
                
        if not test_list_found:
            print("❌ Test list not found in lists")
            return False
            
        # Test 4: Modify and save leads list
        print("\n📋 Test 4: Modify and save leads list")
        
        # Add a new lead
        new_lead = ['new@example.com', 'New', 'User', 'New Company']
        data.append(new_lead)
        
        success = dm.save_leads_list(test_list_name, headers, data)
        
        if success:
            print("✅ List saved successfully after modification")
            
            # Verify the modification
            headers_check, data_check = dm.load_leads_list(test_list_name)
            if len(data_check) == 5:  # Should now have 5 rows
                print("✅ Modification verified")
            else:
                print(f"❌ Modification not saved. Expected 5 rows, got {len(data_check)}")
                return False
        else:
            print("❌ Failed to save modified list")
            return False
            
        # Test 5: Get total leads count
        print("\n📋 Test 5: Get total leads count")
        total_leads = dm.get_total_leads()
        print(f"✅ Total leads across all lists: {total_leads}")
        
        # Test 6: Delete the test list
        print("\n📋 Test 6: Delete test list")
        success = dm.delete_leads_list(test_list_name)
        
        if success:
            print("✅ List deleted successfully")
            
            # Verify deletion
            lists_after = dm.get_leads_lists()
            test_list_exists = any(lst['name'] == test_list_name for lst in lists_after)
            
            if not test_list_exists:
                print("✅ Deletion verified")
            else:
                print("❌ List still exists after deletion")
                return False
        else:
            print("❌ Failed to delete list")
            return False
            
        print("\n🎉 All leads management tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False
        
    finally:
        # Cleanup: ensure test list is deleted
        try:
            dm.delete_leads_list(test_list_name)
        except:
            pass

def test_validation():
    """Test email validation"""
    print("\n🧪 Testing Email Validation\n")
    
    from core.utils import validate_email
    
    test_emails = [
        ('john@example.com', True),
        ('test.email+tag@domain.org', True),
        ('user@sub.domain.com', True),
        ('invalid-email', False),
        ('user@', False),
        ('@domain.com', False),
        ('user@domain', False),
        ('', False)
    ]
    
    all_passed = True
    
    for email, expected in test_emails:
        result = validate_email(email)
        if result == expected:
            print(f"✅ '{email}' -> {result} (correct)")
        else:
            print(f"❌ '{email}' -> {result} (expected {expected})")
            all_passed = False
            
    return all_passed

def main():
    """Run all tests"""
    print("🧪 Testing DeepMailer v1.0 Leads Management\n")
    
    tests = [
        ("Leads Management", test_leads_management),
        ("Email Validation", test_validation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED\n")
        else:
            print(f"❌ {test_name} FAILED\n")
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Leads management is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())