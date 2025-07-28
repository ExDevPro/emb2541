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

from faker import Faker

class PlaceholderEngine:
    """Engine for processing all types of placeholders"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.faker = Faker()
        self.counter = 1
        self.config = {}
        
        # Initialize supported placeholders
        self._init_faker_placeholders()
        self._init_system_placeholders()
        
    def _init_faker_placeholders(self):
        """Initialize Faker-based placeholders"""
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
            
            # Location Data
            'FakerCity': lambda: self.faker.city(),
            'FakerState': lambda: self.faker.state(),
            'FakerCountry': lambda: self.faker.country(),
            'FakerCountryCode': lambda: self.faker.country_code(),
            'FakerAddress': lambda: self.faker.address(),
            'FakerStreetName': lambda: self.faker.street_name(),
            'FakerStreetAddress': lambda: self.faker.street_address(),
            'FakerBuildingNumber': lambda: self.faker.building_number(),
            'FakerPostcode': lambda: self.faker.postcode(),
            'FakerLatitude': lambda: str(self.faker.latitude()),
            'FakerLongitude': lambda: str(self.faker.longitude()),
            
            # Date & Time
            'FakerDate': lambda: self.faker.date(),
            'FakerTime': lambda: self.faker.time(),
            'FakerDateTime': lambda: self.faker.date_time().strftime('%Y-%m-%d %H:%M:%S'),
            'FakerDayOfWeek': lambda: self.faker.day_name(),
            'FakerMonthName': lambda: self.faker.month_name(),
            'FakerYear': lambda: str(self.faker.year()),
            
            # Internet & Technology
            'FakerUrl': lambda: self.faker.url(),
            'FakerUUID': lambda: self.faker.uuid4(),
            'FakerUserAgent': lambda: self.faker.user_agent(),
            'FakerIPv4': lambda: self.faker.ipv4(),
            'FakerIPv6': lambda: self.faker.ipv6(),
            'FakerMACAddress': lambda: self.faker.mac_address(),
            
            # Design & Content
            'FakerColor': lambda: self.faker.color_name(),
            'FakerHexColor': lambda: self.faker.hex_color(),
            'FakerSlug': lambda: self.faker.slug(),
            
            # Localization
            'FakerLocale': lambda: self.faker.locale(),
            'FakerTimezone': lambda: str(self.faker.timezone()),
            'FakerLanguageCode': lambda: self.faker.language_code(),
            
            # Financial
            'FakerCurrencyCode': lambda: self.faker.currency_code(),
            'FakerIBAN': lambda: self.faker.iban(),
            'FakerBIC': lambda: self.faker.swift(),
            
            # Email Types
            'FakerAsciiSafeEmail': lambda: self.faker.ascii_safe_email(),
            'FakerFreeEmail': lambda: self.faker.free_email(),
            'FakerSafeEmail': lambda: self.faker.safe_email(),
            
            # Data & Boolean
            'FakerBoolean': lambda: str(self.faker.boolean()),
            
            # Text Generation
            'FakerWord': lambda: self.faker.word(),
            'FakerWords': lambda: ' '.join(self.faker.words(3)),
            'FakerSentence': lambda: self.faker.sentence(),
            'FakerParagraph': lambda: self.faker.paragraph(),
            'FakerText': lambda: self.faker.text(200),
            
            # Numbers
            'FakerRandomNumber': lambda: str(self.faker.random_int(min=1, max=9999)),
            'FakerDigit': lambda: str(self.faker.random_digit()),
            'FakerNumberBetween': lambda: str(self.faker.random_int(min=1, max=100)),
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