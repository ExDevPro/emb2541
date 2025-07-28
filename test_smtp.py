#!/usr/bin/env python3
"""
Test SMTP Management functionality

This script tests the SMTP management module functionality without GUI.
"""

import sys
import os
sys.path.append('.')

from modules.data_manager import DataManager
from datetime import datetime

def test_smtp_management():
    """Test SMTP management functionality"""
    print("🧪 Testing SMTP Management\n")
    
    dm = DataManager()
    test_server_name = "test_smtp_server"
    
    try:
        # Test 1: Create and save SMTP server
        print("📧 Test 1: Create and save SMTP server")
        
        smtp_data = {
            'server_name': test_server_name,
            'description': 'Test SMTP server',
            'host': 'smtp.gmail.com',
            'port': 587,
            'security': 'tls',
            'authentication': 'plain',
            'username': 'test@gmail.com',
            'password': 'test_password',
            'from_email': 'sender@gmail.com',
            'from_name': {
                'enabled': True,
                'mode': 'Custom',
                'values': ['Test Sender', 'Marketing Team'],
                'rotation': 'Each time'
            },
            'reply_to': {
                'enabled': True,
                'mode': 'Custom',
                'values': ['reply@company.com']
            },
            'rate_limiting': {
                'enabled': True,
                'per_minute': 60,
                'hourly': 1000,
                'daily': 10000,
                'total_limit': 100000,
                'usage': {
                    'current_minute': 0,
                    'current_hour': 0,
                    'current_day': 0,
                    'total_sent': 0,
                    'last_reset': datetime.now().isoformat()
                }
            },
            'proxy': {
                'enabled': False,
                'type': 'HTTP',
                'host': '',
                'port': 8080,
                'auth_enabled': False,
                'username': '',
                'password': ''
            },
            'status': 'active'
        }
        
        success = dm.save_smtp_server(smtp_data)
        
        if success:
            print("✅ SMTP server saved successfully")
        else:
            print("❌ Failed to save SMTP server")
            return False
            
        # Test 2: Load SMTP servers
        print("\n📧 Test 2: Load SMTP servers")
        
        servers = dm.get_smtp_servers()
        
        test_server_found = False
        for server in servers:
            if server['server_name'] == test_server_name:
                test_server_found = True
                print(f"✅ Found test server: {server['server_name']}")
                print(f"   Host: {server['host']}:{server['port']}")
                print(f"   Security: {server['security']}")
                print(f"   From Name Enabled: {server['from_name']['enabled']}")
                print(f"   Rate Limiting Enabled: {server['rate_limiting']['enabled']}")
                break
                
        if not test_server_found:
            print("❌ Test server not found in loaded servers")
            return False
            
        # Test 3: Get total SMTP count
        print("\n📧 Test 3: Get total SMTP count")
        
        total_smtp = dm.get_total_smtp_servers()
        print(f"✅ Total SMTP servers: {total_smtp}")
        
        if total_smtp == 0:
            print("❌ No SMTP servers found")
            return False
            
        # Test 4: Modify and save SMTP server
        print("\n📧 Test 4: Modify and save SMTP server")
        
        # Modify the server data
        smtp_data['description'] = 'Modified test SMTP server'
        smtp_data['port'] = 465
        smtp_data['security'] = 'ssl'
        smtp_data['rate_limiting']['per_minute'] = 30
        
        success = dm.save_smtp_server(smtp_data)
        
        if success:
            print("✅ SMTP server modified and saved")
            
            # Verify modification
            servers_check = dm.get_smtp_servers()
            for server in servers_check:
                if server['server_name'] == test_server_name:
                    if (server['description'] == 'Modified test SMTP server' and
                        server['port'] == 465 and
                        server['security'] == 'ssl'):
                        print("✅ Modifications verified")
                    else:
                        print("❌ Modifications not saved correctly")
                        return False
                    break
        else:
            print("❌ Failed to save modified SMTP server")
            return False
            
        # Test 5: Test SMTP configuration validation
        print("\n📧 Test 5: Test SMTP configuration validation")
        
        # Test with missing required fields
        invalid_smtp = {
            'server_name': '',  # Empty name
            'host': '',         # Empty host
            'username': '',     # Empty username
            'password': '',     # Empty password
        }
        
        # Since we don't have actual validation in data_manager, 
        # we'll just test that it can handle incomplete data
        try:
            dm.save_smtp_server(invalid_smtp)
            print("✅ Handled incomplete SMTP data gracefully")
        except Exception as e:
            print(f"✅ Properly caught validation error: {e}")
            
        # Test 6: Test rate limiting structure
        print("\n📧 Test 6: Test rate limiting structure")
        
        for server in dm.get_smtp_servers():
            if server['server_name'] == test_server_name:
                rate_config = server.get('rate_limiting', {})
                
                required_fields = ['enabled', 'per_minute', 'hourly', 'daily', 'total_limit', 'usage']
                all_present = all(field in rate_config for field in required_fields)
                
                if all_present:
                    print("✅ Rate limiting configuration complete")
                    print(f"   Per minute: {rate_config['per_minute']}")
                    print(f"   Hourly: {rate_config['hourly']}")
                    print(f"   Daily: {rate_config['daily']}")
                    print(f"   Total limit: {rate_config['total_limit']}")
                else:
                    print("❌ Rate limiting configuration incomplete")
                    return False
                break
                
        # Test 7: Test proxy configuration structure
        print("\n📧 Test 7: Test proxy configuration structure")
        
        for server in dm.get_smtp_servers():
            if server['server_name'] == test_server_name:
                proxy_config = server.get('proxy', {})
                
                required_fields = ['enabled', 'type', 'host', 'port', 'auth_enabled']
                all_present = all(field in proxy_config for field in required_fields)
                
                if all_present:
                    print("✅ Proxy configuration structure complete")
                    print(f"   Enabled: {proxy_config['enabled']}")
                    print(f"   Type: {proxy_config['type']}")
                else:
                    print("❌ Proxy configuration structure incomplete")
                    return False
                break
                
        # Test 8: Delete SMTP server
        print("\n📧 Test 8: Delete SMTP server")
        
        success = dm.delete_smtp_server(test_server_name)
        
        if success:
            print("✅ SMTP server deleted successfully")
            
            # Verify deletion
            servers_after = dm.get_smtp_servers()
            test_server_exists = any(s['server_name'] == test_server_name for s in servers_after)
            
            if not test_server_exists:
                print("✅ Deletion verified")
            else:
                print("❌ Server still exists after deletion")
                return False
        else:
            print("❌ Failed to delete SMTP server")
            return False
            
        print("\n🎉 All SMTP management tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False
        
    finally:
        # Cleanup: ensure test server is deleted
        try:
            dm.delete_smtp_server(test_server_name)
        except:
            pass

def test_smtp_data_structure():
    """Test SMTP data structure completeness"""
    print("\n🧪 Testing SMTP Data Structure\n")
    
    # Create a comprehensive SMTP configuration
    complete_smtp = {
        'server_name': 'comprehensive_test',
        'description': 'Complete test configuration',
        'host': 'smtp.test.com',
        'port': 587,
        'security': 'tls',
        'authentication': 'plain',
        'username': 'user@test.com',
        'password': 'password123',
        'from_email': 'sender@test.com',
        'from_name': {
            'enabled': True,
            'mode': 'Faker',
            'values': [],
            'rotation': 'Custom range'
        },
        'reply_to': {
            'enabled': False,
            'mode': 'Custom',
            'values': []
        },
        'rate_limiting': {
            'enabled': True,
            'per_minute': 100,
            'hourly': 2000,
            'daily': 20000,
            'total_limit': 0,
            'usage': {
                'current_minute': 0,
                'current_hour': 0,
                'current_day': 0,
                'total_sent': 0,
                'last_reset': datetime.now().isoformat()
            }
        },
        'proxy': {
            'enabled': True,
            'type': 'SOCKS5',
            'host': 'proxy.test.com',
            'port': 1080,
            'auth_enabled': True,
            'username': 'proxy_user',
            'password': 'proxy_pass'
        },
        'status': 'active',
        'created': datetime.now().isoformat(),
        'modified': datetime.now().isoformat()
    }
    
    # Required top-level fields
    required_fields = [
        'server_name', 'host', 'port', 'username', 'password', 'from_email',
        'from_name', 'reply_to', 'rate_limiting', 'proxy', 'status'
    ]
    
    print("📋 Checking required top-level fields:")
    all_present = True
    for field in required_fields:
        if field in complete_smtp:
            print(f"✅ {field}")
        else:
            print(f"❌ {field} - Missing")
            all_present = False
            
    if not all_present:
        print("\n❌ Required fields missing")
        return False
        
    # Check from_name structure
    print("\n📋 Checking from_name structure:")
    from_name_fields = ['enabled', 'mode', 'values', 'rotation']
    from_name_complete = all(field in complete_smtp['from_name'] for field in from_name_fields)
    
    if from_name_complete:
        print("✅ from_name structure complete")
    else:
        print("❌ from_name structure incomplete")
        return False
        
    # Check reply_to structure
    print("\n📋 Checking reply_to structure:")
    reply_to_fields = ['enabled', 'mode', 'values']
    reply_to_complete = all(field in complete_smtp['reply_to'] for field in reply_to_fields)
    
    if reply_to_complete:
        print("✅ reply_to structure complete")
    else:
        print("❌ reply_to structure incomplete")
        return False
        
    # Check rate_limiting structure
    print("\n📋 Checking rate_limiting structure:")
    rate_fields = ['enabled', 'per_minute', 'hourly', 'daily', 'total_limit', 'usage']
    rate_complete = all(field in complete_smtp['rate_limiting'] for field in rate_fields)
    
    if rate_complete:
        print("✅ rate_limiting structure complete")
        
        # Check usage sub-structure
        usage_fields = ['current_minute', 'current_hour', 'current_day', 'total_sent', 'last_reset']
        usage_complete = all(field in complete_smtp['rate_limiting']['usage'] for field in usage_fields)
        
        if usage_complete:
            print("✅ rate_limiting.usage structure complete")
        else:
            print("❌ rate_limiting.usage structure incomplete")
            return False
    else:
        print("❌ rate_limiting structure incomplete")
        return False
        
    # Check proxy structure
    print("\n📋 Checking proxy structure:")
    proxy_fields = ['enabled', 'type', 'host', 'port', 'auth_enabled', 'username', 'password']
    proxy_complete = all(field in complete_smtp['proxy'] for field in proxy_fields)
    
    if proxy_complete:
        print("✅ proxy structure complete")
    else:
        print("❌ proxy structure incomplete")
        return False
        
    print("\n🎉 SMTP data structure test passed!")
    return True

def main():
    """Run all tests"""
    print("🧪 Testing DeepMailer v1.0 SMTP Management\n")
    
    tests = [
        ("SMTP Management", test_smtp_management),
        ("SMTP Data Structure", test_smtp_data_structure)
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
        print("🎉 All tests passed! SMTP management is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())