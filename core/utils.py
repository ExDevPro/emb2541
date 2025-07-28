"""
Utility functions for DeepMailer v1.0

This module contains common utility functions used throughout the application
including directory setup, configuration management, and file operations.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Default configuration
DEFAULT_CONFIG = {
    "theme": "dark",
    "pagination": {
        "leads_per_page": 100,
        "smtp_per_page": 25,
        "subjects_per_page": 50,
        "templates_per_page": 25,
        "campaigns_per_page": 25
    },
    "window": {
        "width": 1200,
        "height": 800,
        "maximized": False
    },
    "email": {
        "retry_count": 3,
        "timeout": 30
    },
    "placeholders": {
        "counter_start": 1,
        "domains": [
            "example.com",
            "mydomain.com",
            "company.org"
        ],
        "campaigns": [
            "SummerSale2025",
            "BlackFridayPromo",
            "WelcomeSeries"
        ],
        "batch_names": [
            "Batch1",
            "Batch2", 
            "Batch3"
        ],
        "custom_strings": [
            "Custom1",
            "Custom2",
            "Custom3"
        ],
        "list_names": [
            "List1",
            "List2",
            "List3"
        ]
    },
    "spintext": {
        "struggling": "struggling|having trouble|facing challenges|finding it hard",
        "offer": "offer|deal|promotion|special|discount",
        "business": "business|company|organization|enterprise|firm"
    },
    "unsubscribe_formats": [
        "<mailto:unsubscribe@{{domain}}>",
        "<https://{{domain}}/unsubscribe?email={email}>",
        "<https://{{domain}}/unsubscribe/{{token}}>"
    ]
}

def setup_directories():
    """Create all necessary directories for the application"""
    directories = [
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
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        
    logging.info("Application directories created successfully")

def get_config_path() -> Path:
    """Get the path to the configuration file"""
    return Path("Data/Settings/config.json")

def load_config() -> Dict[str, Any]:
    """Load application configuration from file"""
    config_path = get_config_path()
    
    if not config_path.exists():
        # Create default config
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Merge with defaults for any missing keys
        merged_config = DEFAULT_CONFIG.copy()
        merged_config.update(config)
        
        return merged_config
        
    except Exception as e:
        logging.error(f"Failed to load config: {e}")
        return DEFAULT_CONFIG.copy()

def save_config(config: Dict[str, Any]) -> bool:
    """Save application configuration to file"""
    config_path = get_config_path()
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        logging.info("Configuration saved successfully")
        return True
        
    except Exception as e:
        logging.error(f"Failed to save config: {e}")
        return False

def get_data_path(module: str) -> Path:
    """Get the data directory path for a specific module"""
    paths = {
        'leads': Path("Data/Leads"),
        'smtp': Path("Data/SMTP"),
        'subject': Path("Data/Subject"),
        'message': Path("Data/Message"),
        'campaigns': Path("Data/Campaigns"),
        'settings': Path("Data/Settings"),
        'logs': Path("Data/Logs")
    }
    
    return paths.get(module.lower(), Path("Data"))

def get_resource_path(resource_type: str) -> Path:
    """Get the resource directory path for a specific type"""
    paths = {
        'images': Path("Resource/Images"),
        'theme': Path("Resource/Theme"),
        'fonts': Path("Resource/Fonts")
    }
    
    return paths.get(resource_type.lower(), Path("Resource"))

def safe_filename(filename: str) -> str:
    """Convert a string to a safe filename"""
    # Remove or replace invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Ensure filename is not empty
    if not filename:
        filename = "unnamed"
    
    return filename

def load_json_file(file_path: Path) -> Optional[Dict[str, Any]]:
    """Load a JSON file safely"""
    try:
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load JSON file {file_path}: {e}")
    
    return None

def save_json_file(file_path: Path, data: Dict[str, Any]) -> bool:
    """Save data to a JSON file safely"""
    try:
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        return True
        
    except Exception as e:
        logging.error(f"Failed to save JSON file {file_path}: {e}")
        return False

def format_number(number: int) -> str:
    """Format a number with thousand separators"""
    return f"{number:,}"

def validate_email(email: str) -> bool:
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def get_file_size(file_path: Path) -> str:
    """Get human-readable file size"""
    try:
        size = file_path.stat().st_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    except Exception:
        return "Unknown"