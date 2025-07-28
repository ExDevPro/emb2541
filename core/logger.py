"""
Logging setup for DeepMailer v1.0

This module sets up comprehensive logging for the application with both
file and console outputs, rotation, and appropriate formatting.
"""

import logging
import logging.handlers
from pathlib import Path
from datetime import datetime

def setup_logging(log_level: str = "INFO") -> None:
    """
    Setup logging configuration for the application
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    
    # Create logs directory if it doesn't exist
    log_dir = Path("Data/Logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Setup log file path with timestamp
    timestamp = datetime.now().strftime("%Y%m%d")
    log_file = log_dir / f"deepmailer_{timestamp}.log"
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Setup root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    
    # Clear any existing handlers
    root_logger.handlers.clear()
    
    # Setup file handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Setup console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(levelname)s - %(name)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)
    
    # Setup specific loggers for different modules
    setup_module_loggers()
    
    logging.info("Logging system initialized successfully")

def setup_module_loggers():
    """Setup specific loggers for different application modules"""
    
    # SMTP logger
    smtp_logger = logging.getLogger('smtp')
    smtp_logger.setLevel(logging.INFO)
    
    # Campaign logger  
    campaign_logger = logging.getLogger('campaign')
    campaign_logger.setLevel(logging.INFO)
    
    # Email sending logger
    email_logger = logging.getLogger('email')
    email_logger.setLevel(logging.INFO)
    
    # Database logger
    data_logger = logging.getLogger('data')
    data_logger.setLevel(logging.INFO)
    
    # UI logger
    ui_logger = logging.getLogger('ui')
    ui_logger.setLevel(logging.WARNING)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger for a specific module
    
    Args:
        name: Logger name (typically module name)
        
    Returns:
        Logger instance
    """
    return logging.getLogger(name)