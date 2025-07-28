#!/usr/bin/env python3
"""
DeepMailer v1.0 - Professional Email Marketing Software

This is the main entry point for the DeepMailer application.
A comprehensive Windows-based email marketing and campaign management software
built with Python PyQt6 and featuring QSS-based theme customization.

Author: DeepMailer Development Team
Version: 1.0
License: Commercial
"""

import sys
import os
import json
import logging
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
from PyQt6.QtCore import Qt, QThread, QTimer
from PyQt6.QtGui import QIcon, QFont

# Import core modules
from core.main_window import MainWindow
from core.utils import setup_directories, load_config, save_config
from core.logger import setup_logging

class DeepMailerApp:
    """Main application class for DeepMailer v1.0"""
    
    def __init__(self):
        self.app = None
        self.main_window = None
        self.config = {}
        
    def initialize(self):
        """Initialize the application"""
        # Setup directories
        setup_directories()
        
        # Setup logging
        setup_logging()
        
        # Load configuration
        self.config = load_config()
        
        # Create QApplication
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("DeepMailer v1.0")
        self.app.setApplicationVersion("1.0")
        self.app.setOrganizationName("DeepMailer")
        
        # Set application icon if available
        icon_path = Path("Resource/Images/app_icon.ico")
        if icon_path.exists():
            self.app.setWindowIcon(QIcon(str(icon_path)))
        
        # Apply theme
        self.apply_theme()
        
        # Create main window
        self.main_window = MainWindow()
        
        logging.info("DeepMailer v1.0 application initialized successfully")
        
    def apply_theme(self):
        """Apply the current theme to the application"""
        theme_name = self.config.get('theme', 'dark')
        theme_path = Path(f"Resource/Theme/{theme_name}.qss")
        
        if theme_path.exists():
            try:
                with open(theme_path, 'r', encoding='utf-8') as f:
                    stylesheet = f.read()
                self.app.setStyleSheet(stylesheet)
                logging.info(f"Applied theme: {theme_name}")
            except Exception as e:
                logging.error(f"Failed to load theme {theme_name}: {e}")
        else:
            logging.warning(f"Theme file not found: {theme_path}")
            
    def run(self):
        """Run the application"""
        if not self.main_window:
            raise RuntimeError("Application not initialized")
            
        self.main_window.show()
        return self.app.exec()
        
    def cleanup(self):
        """Cleanup resources before exit"""
        if self.main_window:
            self.main_window.cleanup()
        logging.info("DeepMailer v1.0 application cleaned up")

def main():
    """Main entry point"""
    try:
        # Create and initialize the application
        deepmailer = DeepMailerApp()
        deepmailer.initialize()
        
        # Run the application
        exit_code = deepmailer.run()
        
        # Cleanup
        deepmailer.cleanup()
        
        sys.exit(exit_code)
        
    except Exception as e:
        logging.critical(f"Failed to start DeepMailer: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()