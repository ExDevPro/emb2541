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
import platform
from pathlib import Path

def check_and_setup_qt_environment():
    """Check and setup Qt environment for different platforms"""
    system = platform.system().lower()
    
    # Set QT platform for headless environments (Linux servers, CI, etc.)
    if system == 'linux':
        # Check if we're in a headless environment
        display = os.environ.get('DISPLAY')
        if not display or not os.path.exists('/usr/bin/X11'):
            print("INFO - Detected headless Linux environment, using offscreen rendering")
            os.environ['QT_QPA_PLATFORM'] = 'offscreen'
        elif display and ':99' in display:
            print("INFO - Detected virtual display, using offscreen rendering")
            os.environ['QT_QPA_PLATFORM'] = 'offscreen'
    
    return True

def check_dependencies():
    """Check if all required dependencies are available"""
    missing_deps = []
    
    # Check PyQt6
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt, QThread, QTimer
        from PyQt6.QtGui import QIcon, QFont
    except ImportError as e:
        missing_deps.append(f"PyQt6: {e}")
    
    # Check other dependencies
    try:
        import faker
    except ImportError:
        missing_deps.append("Faker")
    
    try:
        import pandas
    except ImportError:
        missing_deps.append("pandas")
    
    try:
        import openpyxl
    except ImportError:
        missing_deps.append("openpyxl")
    
    try:
        import psutil
    except ImportError:
        missing_deps.append("psutil")
    
    if missing_deps:
        print("\n" + "="*60)
        print("MISSING DEPENDENCIES DETECTED")
        print("="*60)
        print("\nThe following dependencies are missing:")
        for dep in missing_deps:
            print(f"  - {dep}")
        print("\nTo install missing dependencies, run:")
        print("  pip install -r requirements.txt")
        print("\nIf you're on Linux and getting PyQt6 errors, you may need:")
        print("  sudo apt-get install libgl1 libxkbcommon-x11-0 libxcb-cursor0")
        print("  sudo apt-get install libfontconfig1 libx11-xcb1 libegl1")
        print("\n" + "="*60)
        return False
    
    return True

# Check environment and dependencies before importing Qt modules
if not check_dependencies():
    sys.exit(1)

check_and_setup_qt_environment()

# Now safely import PyQt6 modules
try:
    from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout
    from PyQt6.QtCore import Qt, QThread, QTimer
    from PyQt6.QtGui import QIcon, QFont
except ImportError as e:
    print(f"\nERROR: Failed to import PyQt6 modules: {e}")
    print("\nThis could be due to:")
    print("1. Missing system libraries (see installation instructions above)")
    print("2. Incompatible Qt platform plugin")
    print("3. Missing X11 or display server")
    print(f"\nYour system: {platform.system()} {platform.release()}")
    print(f"Python version: {sys.version}")
    sys.exit(1)

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
        try:
            # Setup directories
            setup_directories()
            
            # Setup logging
            setup_logging()
            
            # Load configuration
            self.config = load_config()
            
            # Create QApplication with error handling
            print("INFO - Initializing Qt Application...")
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
            
            # Create main window with error handling
            print("INFO - Creating main window...")
            self.main_window = MainWindow()
            
            print("INFO - DeepMailer v1.0 application initialized successfully")
            logging.info("DeepMailer v1.0 application initialized successfully")
            
        except Exception as e:
            print(f"ERROR - Failed to initialize application: {e}")
            self.show_initialization_error(e)
            raise
    def show_initialization_error(self, error):
        """Show detailed error information for initialization failures"""
        print("\n" + "="*60)
        print("APPLICATION INITIALIZATION ERROR")
        print("="*60)
        print(f"\nError: {error}")
        print(f"\nSystem Information:")
        print(f"  - Operating System: {platform.system()} {platform.release()}")
        print(f"  - Python Version: {sys.version}")
        print(f"  - Qt Platform: {os.environ.get('QT_QPA_PLATFORM', 'default')}")
        print(f"  - Display: {os.environ.get('DISPLAY', 'not set')}")
        
        print(f"\nTroubleshooting:")
        if platform.system().lower() == 'linux':
            print("  For Linux users:")
            print("    1. Install required system libraries:")
            print("       sudo apt-get install libgl1 libxkbcommon-x11-0 libxcb-cursor0")
            print("    2. Ensure X11 or Wayland is running")
            print("    3. Try setting: export QT_QPA_PLATFORM=offscreen")
        elif platform.system().lower() == 'windows':
            print("  For Windows users:")
            print("    1. Ensure Visual C++ Redistributable is installed")
            print("    2. Try running as administrator")
            print("    3. Check Windows version compatibility")
        print("\n" + "="*60)
        
    def apply_theme(self):
        """Apply the current theme to the application"""
        try:
            theme_name = self.config.get('theme', 'professional')
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
        except Exception as e:
            logging.warning(f"Theme application failed: {e}")
            
    def run(self):
        """Run the application"""
        if not self.main_window:
            raise RuntimeError("Application not initialized")
        
        try:
            print("INFO - Starting DeepMailer application...")
            print("INFO - Window will appear shortly...")
            
            # Show main window
            self.main_window.show()
            
            # For offscreen mode, provide additional info
            if os.environ.get('QT_QPA_PLATFORM') == 'offscreen':
                print("INFO - Running in headless mode (offscreen rendering)")
                print("INFO - GUI functionality is available but not visible")
            
            return self.app.exec()
            
        except Exception as e:
            print(f"ERROR - Application execution failed: {e}")
            logging.error(f"Application execution failed: {e}")
            raise
        
    def cleanup(self):
        """Cleanup resources before exit"""
        try:
            if self.main_window:
                self.main_window.cleanup()
            logging.info("DeepMailer v1.0 application cleaned up")
            print("INFO - Application cleanup completed")
        except Exception as e:
            print(f"WARNING - Cleanup error: {e}")
            logging.warning(f"Cleanup error: {e}")

def show_startup_info():
    """Show application startup information"""
    print("="*60)
    print("DeepMailer v1.0 - Professional Email Marketing Software")  
    print("="*60)
    print(f"System: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Platform: {os.environ.get('QT_QPA_PLATFORM', 'default')}")
    print("="*60)

def main():
    """Main entry point"""
    try:
        # Show startup information
        show_startup_info()
        
        # Create and initialize the application
        print("INFO - Creating DeepMailer application...")
        deepmailer = DeepMailerApp()
        deepmailer.initialize()
        
        # Run the application
        print("INFO - Starting application event loop...")
        exit_code = deepmailer.run()
        
        # Cleanup
        deepmailer.cleanup()
        
        print(f"INFO - Application exited with code: {exit_code}")
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        print("\nINFO - Application interrupted by user")
        sys.exit(0)
    except ImportError as e:
        print(f"\nERROR - Import failed: {e}")
        print("Please ensure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"\nCRITICAL ERROR - Failed to start DeepMailer: {e}")
        logging.critical(f"Failed to start DeepMailer: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()