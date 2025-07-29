#!/usr/bin/env python3
"""
DeepMailer v1.0 - Professional Email Marketing Software

Main entry point for the DeepMailer application.
A comprehensive email marketing and campaign management software
with Flask backend and web-based frontend embedded in desktop wrapper.

Author: DeepMailer Development Team
Version: 1.0
License: Commercial
"""

import sys
import os
import threading
import time
import logging
import webbrowser
from pathlib import Path

try:
    import webview
    WEBVIEW_AVAILABLE = True
except ImportError:
    WEBVIEW_AVAILABLE = False
    print("Warning: pywebview not installed. Application will open in default browser.")

# Import Flask application
try:
    from app import DeepMailerFlaskApp
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    from app_simple import DeepMailerSimpleApp
    print("Warning: Flask not available. Using simple HTTP server.")
from core.utils import setup_directories, load_config
from core.logger import setup_logging

class DeepMailerDesktopApp:
    """Main desktop application wrapper for DeepMailer v1.0"""
    
    def __init__(self):
        self.flask_app = None
        self.flask_thread = None
        self.config = {}
        self.server_port = 5000
        self.server_host = '127.0.0.1'
        
    def initialize(self):
        """Initialize the application"""
        # Setup directories
        setup_directories()
        
        # Setup logging
        setup_logging()
        
        # Load configuration
        self.config = load_config()
        
        # Get server configuration
        self.server_port = self.config.get('server', {}).get('port', 5000)
        self.server_host = self.config.get('server', {}).get('host', '127.0.0.1')
        
        logging.info("DeepMailer v1.0 desktop application initialized successfully")
        
    def start_flask_server(self):
        """Start the Flask server in a separate thread"""
        try:
            if FLASK_AVAILABLE:
                self.flask_app = DeepMailerFlaskApp()
                logging.info(f"Starting Flask server on {self.server_host}:{self.server_port}")
                
                # Run Flask server (this will block the thread)
                self.flask_app.run(
                    host=self.server_host, 
                    port=self.server_port, 
                    debug=False  # Disable debug mode for production
                )
            else:
                # Use simple HTTP server
                self.flask_app = DeepMailerSimpleApp()
                logging.info(f"Starting Simple HTTP server on {self.server_host}:{self.server_port}")
                
                # Run simple server (this will block the thread)
                self.flask_app.run(
                    host=self.server_host,
                    port=self.server_port
                )
        except Exception as e:
            logging.error(f"Failed to start server: {e}")
            
    def wait_for_server(self, timeout=30):
        """Wait for Flask server to be ready"""
        import requests
        url = f"http://{self.server_host}:{self.server_port}"
        
        for i in range(timeout):
            try:
                response = requests.get(url, timeout=1)
                if response.status_code == 200:
                    logging.info("Flask server is ready")
                    return True
            except requests.exceptions.RequestException:
                pass
            time.sleep(1)
            
        logging.error("Flask server failed to start within timeout")
        return False
        
    def create_webview_window(self):
        """Create and configure the webview window"""
        if not WEBVIEW_AVAILABLE:
            logging.warning("pywebview not available, opening in browser instead")
            url = f"http://{self.server_host}:{self.server_port}"
            webbrowser.open(url)
            return None
            
        try:
            # Set window properties
            window_width = self.config.get('window', {}).get('width', 1400)
            window_height = self.config.get('window', {}).get('height', 900)
            
            # Create webview window
            window = webview.create_window(
                title="DeepMailer v1.0 - Professional Email Marketing Software",
                url=f"http://{self.server_host}:{self.server_port}",
                width=window_width,
                height=window_height,
                min_size=(800, 600),
                resizable=True,
                fullscreen=False,
                minimized=False,
                on_top=False,
                shadow=True,
                focus=True,
                text_select=False
            )
            
            return window
            
        except Exception as e:
            logging.error(f"Failed to create webview window: {e}")
            return None
            
    def on_window_loaded(self):
        """Called when the webview window has loaded"""
        logging.info("WebView window loaded successfully")
        
    def on_window_closing(self):
        """Called when the webview window is closing"""
        logging.info("Application shutting down...")
        
        # Stop Flask server if running
        if self.flask_thread and self.flask_thread.is_alive():
            logging.info("Stopping Flask server...")
            # Note: Graceful shutdown could be improved with proper signal handling
            
        return True  # Allow window to close
        
    def run(self):
        """Run the application"""
        try:
            # Start Flask server in background thread
            self.flask_thread = threading.Thread(
                target=self.start_flask_server,
                daemon=True
            )
            self.flask_thread.start()
            
            # Wait for server to be ready
            if not self.wait_for_server():
                logging.error("Failed to start Flask server")
                return 1
                
            if WEBVIEW_AVAILABLE:
                # Create webview window
                window = self.create_webview_window()
                if not window:
                    logging.error("Failed to create webview window")
                    return 1
                    
                # Configure webview settings
                webview.settings = {
                    'ALLOW_DOWNLOADS': True,
                    'ALLOW_FILE_URLS': True,
                    'OPEN_EXTERNAL_LINKS_IN_BROWSER': True,
                    'OPEN_DEVTOOLS_IN_DEBUG': False
                }
                
                logging.info("Starting DeepMailer desktop application...")
                
                # Start the webview (this blocks until window is closed)
                webview.start(
                    debug=False,
                    http_server=False,  # We're using our own Flask server
                    menu=[],  # Custom menu can be added here
                    func=self.on_window_loaded
                )
            else:
                # Fallback: open in browser and keep server running
                url = f"http://{self.server_host}:{self.server_port}"
                print(f"DeepMailer v1.0 is running at: {url}")
                print("Press Ctrl+C to stop the server")
                
                try:
                    # Keep the server running
                    self.flask_thread.join()
                except KeyboardInterrupt:
                    print("\nShutting down server...")
                
            logging.info("Application closed successfully")
            return 0
            
        except Exception as e:
            logging.error(f"Failed to run application: {e}")
            return 1
            
    def cleanup(self):
        """Cleanup resources before exit"""
        logging.info("Cleaning up application resources...")
        
        # Additional cleanup can be added here
        
        logging.info("DeepMailer v1.0 application cleanup completed")

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import flask
        import webview
        import requests
        logging.info("All required dependencies are available")
        return True
    except ImportError as e:
        logging.error(f"Missing required dependency: {e}")
        print(f"Error: Missing required dependency: {e}")
        print("Please install required packages: pip install -r requirements.txt")
        return False

def main():
    """Main entry point"""
    try:
        # Check dependencies first
        if not check_dependencies():
            sys.exit(1)
            
        # Create and initialize the application
        deepmailer = DeepMailerDesktopApp()
        deepmailer.initialize()
        
        # Run the application
        exit_code = deepmailer.run()
        
        # Cleanup
        deepmailer.cleanup()
        
        sys.exit(exit_code)
        
    except KeyboardInterrupt:
        logging.info("Application interrupted by user")
        sys.exit(0)
    except Exception as e:
        logging.critical(f"Failed to start DeepMailer: {e}")
        print(f"Critical error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()