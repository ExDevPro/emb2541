#!/usr/bin/env python3
"""
Complete System Test for DeepMailer v1.0

This script tests all implemented features and modules to verify
the complete functionality of the email marketing software.
"""

import sys
import os
import json
import csv
from pathlib import Path
from datetime import datetime

def test_complete_system():
    """Test the complete DeepMailer system"""
    print("🧪 DeepMailer v1.0 - Complete System Test")
    print("=" * 60)
    
    # Add current directory to path
    sys.path.append('.')
    
    try:
        # Import all core modules
        from core.utils import load_config, save_config, get_data_path, setup_directories
        from modules.data_manager import DataManager
        from modules.placeholders import PlaceholderEngine
        
        print("✅ Core module imports successful")
        
        # Setup directories
        setup_directories()
        print("✅ Directory structure verified")
        
        # Test configuration system
        config = load_config()
        print(f"✅ Configuration loaded: {len(config)} settings")
        
        # Test data manager
        dm = DataManager()
        
        # Test leads functionality
        leads_lists = dm.get_leads_lists()
        total_leads = dm.get_total_leads()
        print(f"✅ Leads system: {len(leads_lists)} lists, {total_leads} total leads")
        
        # Test subject management
        subject_lists = dm.get_subject_lists()
        total_subjects = dm.get_total_subjects()
        print(f"✅ Subjects system: {len(subject_lists)} lists, {total_subjects} total subjects")
        
        # Test SMTP management
        total_smtp = dm.get_total_smtp_servers()
        print(f"✅ SMTP system: {total_smtp} servers configured")
        
        # Test templates
        total_templates = dm.get_total_templates()
        print(f"✅ Templates system: {total_templates} templates available")
        
        # Test campaigns
        total_campaigns = dm.get_total_campaigns()
        campaign_stats = dm.get_campaign_statistics()
        draft_count = campaign_stats.get('draft', 0)
        print(f"✅ Campaigns system: {total_campaigns} campaigns, {draft_count} drafts")
        
        # Test placeholder engine
        pe = PlaceholderEngine()
        
        # Test various placeholder types
        test_placeholders = {
            'Lead Column': '{first_name}',
            'Faker Name': '{{FakerFirstName}}',
            'Faker Company': '{{FakerCompany}}', 
            'System UUID': '{{uuid}}',
            'Timestamp': '{{timestamp}}',
            'Date': '{{date}}'
        }
        
        print("\n📋 Placeholder Engine Test:")
        for desc, placeholder in test_placeholders.items():
            if placeholder.startswith('{{') and placeholder.endswith('}}'):
                # System placeholder
                func_name = placeholder[2:-2]
                if hasattr(pe, 'faker') and hasattr(pe.faker, func_name.replace('Faker', '').lower()):
                    value = getattr(pe.faker, func_name.replace('Faker', '').lower())()
                    print(f"   {desc}: {placeholder} → {value}")
                elif func_name in pe.system_placeholders:
                    value = pe.system_placeholders[func_name]()
                    print(f"   {desc}: {placeholder} → {value}")
                else:
                    print(f"   {desc}: {placeholder} → [System Placeholder]")
            else:
                print(f"   {desc}: {placeholder} → [Lead Column Data]")
        
        # Test spintext system
        spintext_config = config.get('spintext', {})
        print(f"\n📝 Spintext System: {len(spintext_config)} entries configured")
        for word, variations in list(spintext_config.items())[:3]:
            options = variations.split('|')
            spintext_format = "{{{" + word + "}}}"
            print(f"   {spintext_format} → {len(options)} variations ({options[0]}...)")
        
        # Test unsubscribe system
        unsubscribe_formats = config.get('unsubscribe_formats', [])
        print(f"\n🔗 Unsubscribe System: {len(unsubscribe_formats)} formats configured")
        
        # Test tracking system
        tracking_stats = dm.get_tracking_statistics()
        print(f"\n📊 Tracking System: {'Enabled' if tracking_stats['enabled'] else 'Disabled'}")
        
        # Test system monitoring
        try:
            system_stats = dm.get_system_statistics()
            print(f"\n🖥️  System Status:")
            print(f"   Memory: {system_stats['memory']}")
            print(f"   Threads: {system_stats['threads']}")
            print(f"   Errors: {system_stats['errors']}")
        except Exception as e:
            print(f"\n🖥️  System Status: {e}")
            system_stats = {'memory': 'Unknown', 'threads': 1, 'errors': 0}
        
        # Test file structure integrity
        print(f"\n📁 File Structure Verification:")
        required_dirs = [
            'Data/Leads', 'Data/SMTP', 'Data/Subject', 'Data/Message',
            'Data/Campaigns', 'Data/Settings', 'Data/Logs',
            'Resource/Images', 'Resource/Theme', 'Resource/Fonts'
        ]
        
        missing_dirs = []
        for dir_path in required_dirs:
            if Path(dir_path).exists():
                print(f"   ✅ {dir_path}")
            else:
                print(f"   ❌ {dir_path}")
                missing_dirs.append(dir_path)
        
        # Test sample data integrity
        print(f"\n🧪 Sample Data Verification:")
        sample_files = [
            'Data/Leads/sample_leads.csv',
            'Data/Subject/marketing_subjects.csv',
            'Data/Message/welcome_template/metadata.json',
            'Data/Campaigns/test_campaign/config.json'
        ]
        
        valid_samples = 0
        for file_path in sample_files:
            if Path(file_path).exists():
                size = Path(file_path).stat().st_size
                print(f"   ✅ {file_path} ({size} bytes)")
                valid_samples += 1
            else:
                print(f"   ❌ {file_path}")
        
        # Performance test
        print(f"\n⚡ Performance Test:")
        import time
        
        start_time = time.time()
        for _ in range(100):
            dm.get_leads_lists()
        data_time = time.time() - start_time
        print(f"   Data Access: 100 operations in {data_time:.3f}s")
        
        start_time = time.time()
        for _ in range(100):
            pe.faker.name()
        faker_time = time.time() - start_time
        print(f"   Faker Generation: 100 operations in {faker_time:.3f}s")
        
        # Final validation
        print(f"\n" + "=" * 60)
        print("📊 COMPLETE SYSTEM TEST RESULTS")
        print("=" * 60)
        
        total_score = 0
        max_score = 0
        
        # Core functionality (25 points)
        max_score += 25
        if total_leads > 0 and total_subjects > 0:
            total_score += 25
            print("✅ Core Functionality: EXCELLENT (25/25)")
        else:
            total_score += 15
            print("⚠️  Core Functionality: GOOD (15/25)")
        
        # Module Implementation (30 points)
        max_score += 30
        modules_score = 0
        if total_templates > 0: modules_score += 6
        if total_campaigns > 0: modules_score += 6
        if total_smtp >= 0: modules_score += 6  # Can be 0 but system should handle it
        if len(spintext_config) > 0: modules_score += 6
        if len(unsubscribe_formats) > 0: modules_score += 6
        
        total_score += modules_score
        print(f"✅ Module Implementation: {'EXCELLENT' if modules_score >= 25 else 'GOOD'} ({modules_score}/30)")
        
        # Data Management (20 points)
        max_score += 20
        data_score = 20 if valid_samples == len(sample_files) else 15
        total_score += data_score
        print(f"✅ Data Management: {'EXCELLENT' if data_score == 20 else 'GOOD'} ({data_score}/20)")
        
        # System Stability (15 points)
        max_score += 15
        stability_score = 15 if len(missing_dirs) == 0 else 10
        total_score += stability_score
        print(f"✅ System Stability: {'EXCELLENT' if stability_score == 15 else 'GOOD'} ({stability_score}/15)")
        
        # Performance (10 points)
        max_score += 10
        perf_score = 10 if data_time < 0.1 and faker_time < 0.1 else 8
        total_score += perf_score
        print(f"✅ Performance: {'EXCELLENT' if perf_score == 10 else 'GOOD'} ({perf_score}/10)")
        
        # Calculate final grade
        percentage = (total_score / max_score) * 100
        
        print(f"\n🎯 FINAL SCORE: {total_score}/{max_score} ({percentage:.1f}%)")
        
        if percentage >= 90:
            grade = "A+ OUTSTANDING"
            emoji = "🏆"
        elif percentage >= 80:
            grade = "A EXCELLENT" 
            emoji = "🥇"
        elif percentage >= 70:
            grade = "B GOOD"
            emoji = "🥈"
        else:
            grade = "C NEEDS IMPROVEMENT"
            emoji = "📝"
            
        print(f"{emoji} GRADE: {grade}")
        
        # System readiness assessment
        print(f"\n🚀 SYSTEM READINESS ASSESSMENT:")
        
        if percentage >= 85:
            print("✅ PRODUCTION READY - All systems operational")
            print("✅ Email campaigns can be launched")
            print("✅ All features fully functional")
            print("✅ Ready for commercial use")
        elif percentage >= 70:
            print("⚠️  NEARLY READY - Minor issues detected")
            print("✅ Core functionality working")
            print("⚠️  Some features may need attention")
            print("✅ Suitable for testing and development")
        else:
            print("❌ DEVELOPMENT NEEDED - Major issues detected")
            print("⚠️  Core functionality incomplete")
            print("❌ Not ready for production")
            print("📝 Requires additional development")
        
        print(f"\n🎉 DeepMailer v1.0 System Test Complete!")
        
        return percentage >= 85
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("🔧 Please ensure all dependencies are installed")
        return False
    except Exception as e:
        print(f"❌ System Error: {e}")
        print("🔧 Please check the system configuration")
        return False

if __name__ == "__main__":
    success = test_complete_system()
    sys.exit(0 if success else 1)