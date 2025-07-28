#!/usr/bin/env python3
"""
Test Placeholders System functionality

This script tests the 80+ placeholders system without GUI.
"""

import sys
import os
sys.path.append('.')

from modules.placeholders import PlaceholderEngine
from core.utils import load_config

def test_faker_placeholders():
    """Test Faker placeholders"""
    print("🧪 Testing Faker Placeholders\n")
    
    engine = PlaceholderEngine()
    
    # Test some key Faker placeholders
    faker_tests = [
        'FakerFirstName',
        'FakerLastName', 
        'FakerFullName',
        'FakerEmail',
        'FakerCompany',
        'FakerCity',
        'FakerCountry',
        'FakerPhone',
        'FakerDate',
        'FakerUrl',
        'FakerIPv4',
        'FakerColor',
        'FakerWord',
        'FakerSentence'
    ]
    
    all_passed = True
    
    for placeholder in faker_tests:
        try:
            value = engine.process_placeholder(placeholder)
            if value and not value.startswith('[Error:'):
                print(f"✅ {placeholder}: {value}")
            else:
                print(f"❌ {placeholder}: {value}")
                all_passed = False
        except Exception as e:
            print(f"❌ {placeholder}: Error - {e}")
            all_passed = False
            
    return all_passed

def test_system_placeholders():
    """Test system placeholders"""
    print("\n🧪 Testing System Placeholders\n")
    
    engine = PlaceholderEngine()
    
    # Test system placeholders
    system_tests = [
        'timestamp',
        'date',
        'year',
        'month',
        'day',
        'hour',
        'minute',
        'second',
        'uuid',
        'token',
        'counter',
        'sequence'
    ]
    
    all_passed = True
    
    for placeholder in system_tests:
        try:
            value = engine.process_placeholder(placeholder)
            if value and not value.startswith('[Error:'):
                print(f"✅ {placeholder}: {value}")
            else:
                print(f"❌ {placeholder}: {value}")
                all_passed = False
        except Exception as e:
            print(f"❌ {placeholder}: Error - {e}")
            all_passed = False
            
    return all_passed

def test_custom_placeholders():
    """Test custom placeholders"""
    print("\n🧪 Testing Custom Placeholders\n")
    
    engine = PlaceholderEngine()
    
    # Load config with custom placeholders
    config = load_config()
    engine.set_config(config)
    
    # Test custom placeholders
    custom_tests = ['domain', 'campaign', 'batch', 'custom_string', 'list_name']
    
    all_passed = True
    
    for placeholder in custom_tests:
        try:
            value = engine.process_placeholder(placeholder)
            if value and not value.startswith('[Empty:'):
                print(f"✅ {placeholder}: {value}")
            else:
                print(f"⚠️  {placeholder}: {value} (empty config)")
        except Exception as e:
            print(f"❌ {placeholder}: Error - {e}")
            all_passed = False
            
    return all_passed

def test_special_placeholders():
    """Test special placeholders"""
    print("\n🧪 Testing Special Placeholders\n")
    
    engine = PlaceholderEngine()
    config = load_config()
    engine.set_config(config)
    
    # Test special placeholders
    special_tests = ['hash', 'random', 'random_alphanum', 'unsubscribe']
    
    all_passed = True
    
    for placeholder in special_tests:
        try:
            value = engine.process_placeholder(placeholder)
            if value and not value.startswith('[Error:'):
                print(f"✅ {placeholder}: {value}")
            else:
                print(f"❌ {placeholder}: {value}")
                all_passed = False
        except Exception as e:
            print(f"❌ {placeholder}: Error - {e}")
            all_passed = False
            
    return all_passed

def test_lead_column_placeholders():
    """Test lead column placeholders"""
    print("\n🧪 Testing Lead Column Placeholders\n")
    
    engine = PlaceholderEngine()
    
    # Test data
    lead_data = {
        'email': 'test@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'company': 'Test Corp'
    }
    
    # Test lead column placeholders
    column_tests = ['email', 'first_name', 'last_name', 'company', 'EMAIL', 'First_Name']  # Test case-insensitive
    
    all_passed = True
    
    for placeholder in column_tests:
        try:
            value = engine.process_placeholder(placeholder, lead_data)
            if value and not value.startswith('[Unknown:'):
                print(f"✅ {placeholder}: {value}")
            else:
                print(f"❌ {placeholder}: {value}")
                all_passed = False
        except Exception as e:
            print(f"❌ {placeholder}: Error - {e}")
            all_passed = False
            
    return all_passed

def test_text_processing():
    """Test full text processing"""
    print("\n🧪 Testing Text Processing\n")
    
    engine = PlaceholderEngine()
    config = load_config()
    engine.set_config(config)
    
    lead_data = {
        'email': 'john@example.com',
        'first_name': 'John',
        'last_name': 'Doe'
    }
    
    # Test cases
    test_cases = [
        # Basic placeholder replacement
        ("Hello {{FakerFirstName}}", "Should contain a first name"),
        ("Today is {{date}}", "Should contain today's date"),
        ("Your email is {email}", "Should contain john@example.com"),
        
        # Multiple placeholders
        ("Hello {first_name} {last_name}, your email {email} is registered with {{FakerCompany}}", 
         "Should contain John Doe john@example.com and a company"),
        
        # Mixed case
        ("Hello {First_Name}", "Should work with mixed case"),
        
        # Counter
        ("Order #{{counter}}", "Should contain counter value"),
    ]
    
    all_passed = True
    
    for i, (template, description) in enumerate(test_cases, 1):
        try:
            result = engine.process_text(template, lead_data)
            print(f"✅ Test {i}: {template}")
            print(f"   Result: {result}")
            print(f"   Expected: {description}")
            print()
            
            # Basic validation - check if placeholders were replaced
            if '{{' in result or ('{' in result and '}' in result and 'email' in template):
                if 'john@example.com' not in result:  # Expected email replacement didn't happen
                    print(f"   ⚠️  Warning: Some placeholders may not have been replaced")
                    
        except Exception as e:
            print(f"❌ Test {i}: Error - {e}")
            all_passed = False
            
    return all_passed

def test_spintext_processing():
    """Test spintext processing"""
    print("\n🧪 Testing Spintext Processing\n")
    
    engine = PlaceholderEngine()
    config = load_config()
    engine.set_config(config)
    
    # Test spintext
    test_cases = [
        "We have a great {{{offer}}} for you!",
        "Your {{{business}}} is {{{struggling}}} with sales.",
        "This is a {{{offer}}} you can't refuse for your {{{business}}}."
    ]
    
    all_passed = True
    
    for i, template in enumerate(test_cases, 1):
        try:
            # Process multiple times to see variation
            results = []
            for _ in range(3):
                result = engine.process_spintext(template)
                results.append(result)
                
            print(f"✅ Spintext Test {i}: {template}")
            for j, result in enumerate(results, 1):
                print(f"   Variation {j}: {result}")
            print()
            
        except Exception as e:
            print(f"❌ Spintext Test {i}: Error - {e}")
            all_passed = False
            
    return all_passed

def test_complete_processing():
    """Test complete processing with all placeholder types"""
    print("\n🧪 Testing Complete Processing\n")
    
    engine = PlaceholderEngine()
    config = load_config()
    engine.set_config(config)
    
    lead_data = {
        'email': 'john.doe@example.com',
        'first_name': 'John',
        'last_name': 'Doe',
        'company': 'Example Corp'
    }
    
    # Complex template with all types
    template = """
    Hi {first_name} {last_name},
    
    Your email {email} has been registered with {{FakerCompany}}.
    We have a special {{{offer}}} for your {{{business}}}.
    
    Your unique ID: {{uuid}}
    Generated on: {{date}} at {{timestamp}}
    
    Visit: {{FakerUrl}}
    Contact: {{FakerPhone}}
    
    Best regards,
    {{FakerFullName}}
    {{FakerJobTitle}} at {{FakerCompany}}
    """
    
    try:
        result = engine.process_all(template, lead_data)
        print("✅ Complete Processing Test:")
        print("Template:")
        print(template)
        print("\nProcessed Result:")
        print(result)
        print()
        
        # Check if key replacements happened
        if 'John' in result and 'Doe' in result and 'john.doe@example.com' in result:
            print("✅ Lead data placeholders processed correctly")
        else:
            print("❌ Lead data placeholders not processed correctly")
            return False
            
        # Check if Faker placeholders were processed (no more {{}} patterns)
        remaining_faker = result.count('{{')
        if remaining_faker == 0:
            print("✅ All Faker placeholders processed")
        else:
            print(f"⚠️  {remaining_faker} Faker placeholders remain unprocessed")
            
        # Check if spintext was processed (no more {{{}} patterns)
        remaining_spintext = result.count('{{{')
        if remaining_spintext == 0:
            print("✅ All spintext processed")
        else:
            print(f"⚠️  {remaining_spintext} spintext patterns remain unprocessed")
            
        return True
        
    except Exception as e:
        print(f"❌ Complete Processing Test: Error - {e}")
        return False

def test_placeholder_listing():
    """Test placeholder listing functionality"""
    print("\n🧪 Testing Placeholder Listing\n")
    
    engine = PlaceholderEngine()
    
    try:
        available = engine.get_available_placeholders()
        
        print("Available placeholder categories:")
        for category, placeholders in available.items():
            print(f"\n📋 {category} ({len(placeholders)} items):")
            for placeholder in placeholders[:5]:  # Show first 5
                print(f"   • {placeholder}")
            if len(placeholders) > 5:
                print(f"   ... and {len(placeholders) - 5} more")
                
        # Verify we have all expected categories
        expected_categories = ['Faker Placeholders', 'System Placeholders', 'Custom Placeholders', 'Special Placeholders']
        
        for category in expected_categories:
            if category in available:
                print(f"✅ {category} category found")
            else:
                print(f"❌ {category} category missing")
                return False
                
        return True
        
    except Exception as e:
        print(f"❌ Placeholder Listing Test: Error - {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Testing DeepMailer v1.0 Placeholders System\n")
    
    tests = [
        ("Faker Placeholders", test_faker_placeholders),
        ("System Placeholders", test_system_placeholders),
        ("Custom Placeholders", test_custom_placeholders),
        ("Special Placeholders", test_special_placeholders),
        ("Lead Column Placeholders", test_lead_column_placeholders),
        ("Text Processing", test_text_processing),
        ("Spintext Processing", test_spintext_processing),
        ("Complete Processing", test_complete_processing),
        ("Placeholder Listing", test_placeholder_listing)
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
        print("🎉 All tests passed! Placeholders system is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())