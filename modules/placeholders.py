"""
Faker Placeholders System for DeepMailer v1.0

This module provides 80+ built-in placeholders using the Faker library
for generating realistic test data in email campaigns.
"""

import logging
import random
import hashlib
import uuid
from datetime import datetime
from typing import Dict, Any, List

# Use built-in data instead of Faker for now
try:
    from faker import Faker
    FAKER_AVAILABLE = True
except ImportError:
    FAKER_AVAILABLE = False

class PlaceholderEngine:
    """Engine for processing all types of placeholders"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        if FAKER_AVAILABLE:
            self.faker = Faker()
        else:
            self.faker = None
        self.counter = 1
        self.config = {}
        
        # Initialize supported placeholders
        self._init_faker_placeholders()
        self._init_system_placeholders()
        
    def _init_faker_placeholders(self):
        """Initialize Faker-based placeholders"""
        if FAKER_AVAILABLE and self.faker:
            self.faker_placeholders = {
                # Personal Data
                'FakerFirstName': lambda: self.faker.first_name(),
                'FakerLastName': lambda: self.faker.last_name(),
                'FakerFullName': lambda: self.faker.name(),
                'FakerGender': lambda: random.choice(['Male', 'Female']),
                'FakerEmail': lambda: self.faker.email(),
                'FakerUsername': lambda: self.faker.user_name(),
                'FakerPassword': lambda: self.faker.password(),
                
                # Company & Professional
                'FakerCompany': lambda: self.faker.company(),
                'FakerCompanySuffix': lambda: self.faker.company_suffix(),
                'FakerJobTitle': lambda: self.faker.job(),
                
                # Contact Information
                'FakerPhone': lambda: self.faker.phone_number(),
                'FakerPhoneNumber': lambda: self.faker.phone_number(),
            }
        else:
            # Fallback placeholders without Faker
            sample_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Lisa', 'Robert', 'Emma']
            sample_last_names = ['Smith', 'Johnson', 'Brown', 'Davis', 'Miller', 'Wilson', 'Moore', 'Taylor']
            sample_companies = ['Tech Corp', 'Innovation Inc', 'Global Solutions', 'Future Systems', 'Digital Ventures']
            sample_cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia']
            sample_states = ['NY', 'CA', 'IL', 'TX', 'AZ', 'PA']
            sample_countries = ['United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'Australia']
            
            self.faker_placeholders = {
                # Personal Data  
                'FakerFirstName': lambda: random.choice(sample_names),
                'FakerLastName': lambda: random.choice(sample_last_names),
                'FakerFullName': lambda: f"{random.choice(sample_names)} {random.choice(sample_last_names)}",
                'FakerGender': lambda: random.choice(['Male', 'Female']),
                'FakerEmail': lambda: f"{random.choice(sample_names).lower()}.{random.choice(sample_last_names).lower()}@example.com",
                'FakerUsername': lambda: f"user{random.randint(1000, 9999)}",
                'FakerPassword': lambda: f"pass{random.randint(1000, 9999)}",
                
                # Company & Professional
                'FakerCompany': lambda: random.choice(sample_companies),
                'FakerCompanySuffix': lambda: random.choice(['Inc', 'Corp', 'LLC', 'Ltd']),
                'FakerJobTitle': lambda: random.choice(['Manager', 'Developer', 'Analyst', 'Director', 'Specialist']),
                
                # Contact Information
                'FakerPhone': lambda: f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                'FakerPhoneNumber': lambda: f"+1-555-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
                
                # Location Data
                'FakerCity': lambda: random.choice(sample_cities),
                'FakerState': lambda: random.choice(sample_states),
                'FakerCountry': lambda: random.choice(sample_countries),
                'FakerCountryCode': lambda: random.choice(['US', 'CA', 'UK', 'DE', 'FR', 'AU']),
                'FakerAddress': lambda: f"{random.randint(100, 999)} Main St",
                'FakerStreetName': lambda: random.choice(['Main St', 'Oak Ave', 'First St', 'Second Ave']),
                'FakerStreetAddress': lambda: f"{random.randint(100, 999)} {random.choice(['Main St', 'Oak Ave'])}",
                'FakerBuildingNumber': lambda: str(random.randint(1, 999)),
                'FakerPostcode': lambda: f"{random.randint(10000, 99999)}",
                'FakerLatitude': lambda: f"{random.uniform(-90, 90):.6f}",
                'FakerLongitude': lambda: f"{random.uniform(-180, 180):.6f}",
                
                # Date & Time
                'FakerDate': lambda: datetime.now().strftime('%Y-%m-%d'),
                'FakerTime': lambda: datetime.now().strftime('%H:%M:%S'),
                'FakerDateTime': lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'FakerDayOfWeek': lambda: datetime.now().strftime('%A'),
                'FakerMonthName': lambda: datetime.now().strftime('%B'),
                'FakerYear': lambda: str(datetime.now().year),
                
                # Internet & Technology
                'FakerUrl': lambda: f"https://example{random.randint(1, 100)}.com",
                'FakerUUID': lambda: str(uuid.uuid4()),
                'FakerUserAgent': lambda: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'FakerIPv4': lambda: f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}",
                'FakerIPv6': lambda: '2001:db8::1',
                'FakerMACAddress': lambda: ':'.join([f"{random.randint(0, 255):02x}" for _ in range(6)]),
                
                # Design & Content
                'FakerColor': lambda: random.choice(['red', 'blue', 'green', 'yellow', 'purple', 'orange']),
                'FakerHexColor': lambda: f"#{random.randint(0, 16777215):06x}",
                'FakerSlug': lambda: f"sample-slug-{random.randint(1, 1000)}",
                
                # Localization
                'FakerLocale': lambda: random.choice(['en_US', 'en_GB', 'fr_FR', 'de_DE', 'es_ES']),
                'FakerTimezone': lambda: random.choice(['UTC', 'EST', 'PST', 'GMT', 'CET']),
                'FakerLanguageCode': lambda: random.choice(['en', 'fr', 'de', 'es', 'it']),
                
                # Financial
                'FakerCurrencyCode': lambda: random.choice(['USD', 'EUR', 'GBP', 'CAD', 'AUD']),
                'FakerIBAN': lambda: f"GB{random.randint(10, 99)} ABCD {random.randint(1000, 9999)} {random.randint(1000, 9999)} {random.randint(10, 99)}",
                'FakerBIC': lambda: f"ABCD{random.choice(['US', 'GB', 'DE'])}XX",
                
                # Email Types
                'FakerAsciiSafeEmail': lambda: f"user{random.randint(1, 999)}@example.com",
                'FakerFreeEmail': lambda: f"user{random.randint(1, 999)}@{random.choice(['gmail.com', 'yahoo.com', 'hotmail.com'])}",
                'FakerSafeEmail': lambda: f"user{random.randint(1, 999)}@example.org",
                
                # Data & Boolean
                'FakerBoolean': lambda: random.choice(['true', 'false']),
                
                # Text Generation
                'FakerWord': lambda: random.choice(['lorem', 'ipsum', 'dolor', 'sit', 'amet', 'consectetur']),
                'FakerWords': lambda: ' '.join(random.choices(['lorem', 'ipsum', 'dolor', 'sit', 'amet'], k=3)),
                'FakerSentence': lambda: 'Lorem ipsum dolor sit amet consectetur.',
                'FakerParagraph': lambda: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore.',
                'FakerText': lambda: 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                
                # Numbers
                'FakerRandomNumber': lambda: str(random.randint(1, 9999)),
                'FakerDigit': lambda: str(random.randint(0, 9)),
                'FakerNumberBetween': lambda: str(random.randint(1, 100)),
            }
        
    def _init_system_placeholders(self):
        """Initialize system placeholders"""
        self.system_placeholders = {
            # Date & Time
            'timestamp': lambda: str(int(datetime.now().timestamp())),
            'date': lambda: datetime.now().strftime('%Y-%m-%d'),
            'year': lambda: str(datetime.now().year),
            'month': lambda: str(datetime.now().month),
            'day': lambda: str(datetime.now().day),
            'hour': lambda: str(datetime.now().hour),
            'minute': lambda: str(datetime.now().minute),
            'second': lambda: str(datetime.now().second),
            
            # Unique IDs
            'uuid': lambda: str(uuid.uuid4()),
            'token': lambda: hashlib.md5(f"{uuid.uuid4()}{datetime.now()}".encode()).hexdigest(),
            'counter': lambda: str(self.counter),
            'sequence': lambda: str(self.counter),  # Alias for counter
            
            # Email related
            'subject': lambda: self.config.get('current_subject', ''),
            'email': lambda: self.config.get('current_email', ''),
            'user_id': lambda: hashlib.md5(self.config.get('current_email', '').encode()).hexdigest()[:8],
        }
        
    def set_config(self, config: Dict[str, Any]):
        """Set configuration for placeholders"""
        self.config = config
        
    def set_counter(self, value: int):
        """Set the counter value"""
        self.counter = value
        
    def increment_counter(self):
        """Increment the counter"""
        self.counter += 1
        
    def get_custom_placeholders(self) -> Dict[str, List[str]]:
        """Get custom placeholders from config"""
        placeholders = self.config.get('placeholders', {})
        return {
            'domain': placeholders.get('domains', []),
            'campaign': placeholders.get('campaigns', []),
            'batch': placeholders.get('batch_names', []),
            'custom_string': placeholders.get('custom_strings', []),
            'list_name': placeholders.get('list_names', []),
        }
        
    def process_placeholder(self, placeholder: str, lead_data: Dict[str, str] = None) -> str:
        """
        Process a single placeholder and return its value
        
        Args:
            placeholder: The placeholder name (without {{ }})
            lead_data: Lead data for column placeholders
            
        Returns:
            The processed value
        """
        placeholder = placeholder.strip()
        
        # Lead column placeholders (format: {column_name})
        if lead_data and placeholder in lead_data:
            return lead_data[placeholder]
            
        # Case-insensitive lead column lookup
        if lead_data:
            for key, value in lead_data.items():
                if key.lower() == placeholder.lower():
                    return value
                    
        # Faker placeholders
        if placeholder in self.faker_placeholders:
            try:
                return self.faker_placeholders[placeholder]()
            except Exception as e:
                self.logger.error(f"Error generating Faker placeholder {placeholder}: {e}")
                return f"[Error: {placeholder}]"
                
        # System placeholders
        if placeholder in self.system_placeholders:
            try:
                return self.system_placeholders[placeholder]()
            except Exception as e:
                self.logger.error(f"Error generating system placeholder {placeholder}: {e}")
                return f"[Error: {placeholder}]"
                
        # Custom placeholders
        custom_placeholders = self.get_custom_placeholders()
        
        if placeholder in custom_placeholders:
            values = custom_placeholders[placeholder]
            if values:
                return random.choice(values)
            else:
                return f"[Empty: {placeholder}]"
                
        # Hash placeholder with configuration
        if placeholder == 'hash':
            hash_type = self.config.get('hash_algorithm', 'md5')
            data = f"{uuid.uuid4()}{datetime.now()}"
            
            if hash_type == 'md5':
                return hashlib.md5(data.encode()).hexdigest()
            elif hash_type == 'sha256':
                return hashlib.sha256(data.encode()).hexdigest()
            else:
                return hashlib.md5(data.encode()).hexdigest()  # Default to MD5
                
        # Random placeholder
        if placeholder == 'random':
            length = self.config.get('random_length', 8)
            return ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=length))
            
        # Random alphanumeric
        if placeholder == 'random_alphanum':
            min_length = self.config.get('random_min_length', 5)
            max_length = self.config.get('random_max_length', 10)
            length = random.randint(min_length, max_length)
            return ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=length))
            
        # Unsubscribe link
        if placeholder == 'unsubscribe':
            formats = self.config.get('unsubscribe_formats', [])
            if formats:
                format_str = random.choice(formats)
                return self.process_text(format_str, lead_data)
            else:
                return f"mailto:unsubscribe@{self.process_placeholder('domain', lead_data)}"
                
        # Encoded URL (for tracking)
        if placeholder == 'ENCODED_URL':
            # This would be implemented based on the tracking system
            return f"https://track.{self.process_placeholder('domain', lead_data)}/click/{self.process_placeholder('token', lead_data)}"
            
        # Unknown placeholder
        return f"[Unknown: {placeholder}]"
        
    def process_text(self, text: str, lead_data: Dict[str, str] = None) -> str:
        """
        Process text with all types of placeholders
        
        Args:
            text: Text containing placeholders
            lead_data: Lead data for column placeholders
            
        Returns:
            Text with placeholders replaced
        """
        if not text:
            return text
            
        result = text
        
        # Process default placeholders {{placeholder}}
        import re
        
        # Pattern for {{placeholder}}
        default_pattern = r'\{\{([^}]+)\}\}'
        matches = re.finditer(default_pattern, result)
        
        for match in matches:
            full_match = match.group(0)
            placeholder = match.group(1)
            value = self.process_placeholder(placeholder, lead_data)
            result = result.replace(full_match, value, 1)
            
        # Process lead column placeholders {column}
        column_pattern = r'\{([^}]+)\}'
        matches = re.finditer(column_pattern, result)
        
        for match in matches:
            full_match = match.group(0)
            column = match.group(1)
            
            # Skip if it's a spintext placeholder (contains {{{}})
            if full_match.count('{') > 1:
                continue
                
            if lead_data and column in lead_data:
                result = result.replace(full_match, lead_data[column], 1)
            elif lead_data:
                # Case-insensitive lookup
                for key, value in lead_data.items():
                    if key.lower() == column.lower():
                        result = result.replace(full_match, value, 1)
                        break
                        
        return result
        
    def process_spintext(self, text: str) -> str:
        """
        Process spintext placeholders {{{word}}}
        
        Args:
            text: Text containing spintext placeholders
            
        Returns:
            Text with spintext processed
        """
        if not text:
            return text
            
        import re
        
        spintext_config = self.config.get('spintext', {})
        result = text
        
        # Pattern for {{{word}}}
        pattern = r'\{\{\{([^}]+)\}\}\}'
        matches = re.finditer(pattern, result)
        
        for match in matches:
            full_match = match.group(0)
            word = match.group(1).strip()
            
            if word in spintext_config:
                options = spintext_config[word].split('|')
                if options:
                    selected = random.choice(options).strip()
                    result = result.replace(full_match, selected, 1)
                else:
                    result = result.replace(full_match, word, 1)
            else:
                # Unknown spintext - keep original word
                result = result.replace(full_match, word, 1)
                
        return result
        
    def process_all(self, text: str, lead_data: Dict[str, str] = None) -> str:
        """
        Process all types of placeholders in text
        
        Args:
            text: Text to process
            lead_data: Lead data for column placeholders
            
        Returns:
            Fully processed text
        """
        if not text:
            return text
            
        # Process in order: spintext, then placeholders
        result = self.process_spintext(text)
        result = self.process_text(result, lead_data)
        
        return result
        
    def get_available_placeholders(self) -> Dict[str, List[str]]:
        """Get all available placeholders organized by category"""
        return {
            'Faker Placeholders': list(self.faker_placeholders.keys()),
            'System Placeholders': list(self.system_placeholders.keys()),
            'Custom Placeholders': list(self.get_custom_placeholders().keys()),
            'Special Placeholders': ['hash', 'random', 'random_alphanum', 'unsubscribe', 'ENCODED_URL']
        }
        
    def test_placeholder(self, placeholder: str, lead_data: Dict[str, str] = None) -> str:
        """Test a placeholder and return its generated value"""
        return self.process_placeholder(placeholder, lead_data)

class PlaceholderManager:
    """Manager class for placeholder operations"""
    
    def __init__(self):
        self.engine = PlaceholderEngine()
        self.logger = logging.getLogger(__name__)
    
    def get_all_placeholders(self) -> Dict[str, Any]:
        """Get all available placeholders organized by category"""
        try:
            return self.engine.get_available_placeholders()
        except Exception as e:
            self.logger.error(f"Error getting placeholders: {e}")
            return {}
    
    def process_text(self, text: str, lead_data: Dict[str, str] = None) -> str:
        """Process text with placeholders"""
        try:
            return self.engine.process_all(text, lead_data)
        except Exception as e:
            self.logger.error(f"Error processing text: {e}")
            return text
    
    def test_placeholder(self, placeholder: str, lead_data: Dict[str, str] = None) -> str:
        """Test a placeholder and return its generated value"""
        try:
            return self.engine.test_placeholder(placeholder, lead_data)
        except Exception as e:
            self.logger.error(f"Error testing placeholder: {e}")
            return f"Error: {e}"