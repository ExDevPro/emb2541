#!/usr/bin/env python3
"""
DeepMailer v1.0 - Simple HTTP Server (Development Mode)

Lightweight HTTP server for development when Flask is not available.
This serves the frontend and provides basic API endpoints.

Author: DeepMailer Development Team
Version: 1.0
License: Commercial
"""

import os
import sys
import json
import logging
import mimetypes
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler

# Import core modules
from core.utils import setup_directories, load_config, save_config
from core.logger import setup_logging
from modules.data_manager import DataManager
from modules.placeholders import PlaceholderManager

class DeepMailerHTTPHandler(BaseHTTPRequestHandler):
    """HTTP request handler for DeepMailer"""
    
    def __init__(self, *args, data_manager=None, placeholder_manager=None, config=None, **kwargs):
        self.data_manager = data_manager
        self.placeholder_manager = placeholder_manager
        self.config = config or {}
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # Serve main page
        if path == '/' or path == '':
            self.serve_file('frontend/templates/index.html', 'text/html')
        
        # Serve static files
        elif path.startswith('/static/'):
            file_path = path[1:]  # Remove leading slash
            self.serve_file(file_path)
        
        # API endpoints
        elif path == '/api/dashboard/stats':
            self.serve_dashboard_stats()
        elif path == '/api/leads/lists':
            self.serve_lead_lists()
        elif path.startswith('/api/leads/list/'):
            list_name = path.split('/')[-1]
            self.serve_lead_list(list_name, parsed_url.query)
        elif path == '/api/smtp/servers':
            self.serve_smtp_servers()
        elif path == '/api/subjects/lists':
            self.serve_subject_lists()
        elif path == '/api/templates':
            self.serve_templates()
        elif path == '/api/campaigns':
            self.serve_campaigns()
        elif path == '/api/placeholders':
            self.serve_placeholders()
        elif path == '/api/config':
            self.serve_config()
        else:
            self.send_error(404, 'Not Found')
    
    def do_POST(self):
        """Handle POST requests"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        # Get request data
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8')) if post_data else {}
        except json.JSONDecodeError:
            data = {}
        
        # API endpoints
        if path == '/api/config':
            self.save_config(data)
        elif path == '/api/smtp/server':
            self.save_smtp_server(data)
        elif path == '/api/smtp/test':
            self.test_smtp_server(data)
        else:
            self.send_error(404, 'Not Found')
    
    def serve_file(self, file_path, content_type=None):
        """Serve a static file"""
        try:
            full_path = Path(file_path)
            if not full_path.exists():
                self.send_error(404, 'File not found')
                return
            
            # Determine content type
            if content_type is None:
                content_type, _ = mimetypes.guess_type(str(full_path))
                content_type = content_type or 'application/octet-stream'
            
            # Read and serve file
            with open(full_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            self.send_header('Content-Type', content_type)
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
            
        except Exception as e:
            logging.error(f"Error serving file {file_path}: {e}")
            self.send_error(500, 'Internal Server Error')
    
    def send_json_response(self, data, status_code=200):
        """Send JSON response"""
        json_data = json.dumps(data, indent=2)
        json_bytes = json_data.encode('utf-8')
        
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(json_bytes))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json_bytes)
    
    # API endpoint handlers
    def serve_dashboard_stats(self):
        """Get dashboard statistics"""
        try:
            stats = {
                'leads': {
                    'total': self.data_manager.count_total_leads(),
                    'valid_emails': self.data_manager.count_valid_emails(),
                    'lists': self.data_manager.count_lead_lists()
                },
                'smtps': {
                    'total': self.data_manager.count_smtp_servers(),
                    'active': self.data_manager.count_active_smtps(),
                    'inactive': self.data_manager.count_inactive_smtps()
                },
                'subjects': {
                    'total': self.data_manager.count_total_subjects(),
                    'lists': self.data_manager.count_subject_lists()
                },
                'templates': {
                    'total': self.data_manager.count_message_templates(),
                    'with_attachments': self.data_manager.count_templates_with_attachments()
                },
                'campaigns': {
                    'total': self.data_manager.count_total_campaigns(),
                    'active': self.data_manager.count_active_campaigns(),
                    'completed': self.data_manager.count_completed_campaigns(),
                    'emails_sent': self.data_manager.count_total_emails_sent(),
                    'emails_failed': self.data_manager.count_total_emails_failed()
                }
            }
            self.send_json_response({'success': True, 'data': stats})
        except Exception as e:
            logging.error(f"Error getting dashboard stats: {e}")
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def serve_lead_lists(self):
        """Get all lead lists"""
        try:
            lists = self.data_manager.get_lead_lists()
            self.send_json_response({'success': True, 'data': lists})
        except Exception as e:
            logging.error(f"Error getting lead lists: {e}")
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def serve_lead_list(self, list_name, query_string):
        """Get specific lead list data"""
        try:
            params = parse_qs(query_string)
            page = int(params.get('page', [1])[0])
            per_page = int(params.get('per_page', [100])[0])
            search = params.get('search', [''])[0]
            
            leads = self.data_manager.get_leads(list_name, page, per_page, search)
            self.send_json_response({'success': True, 'data': leads})
        except Exception as e:
            logging.error(f"Error getting lead list {list_name}: {e}")
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def serve_smtp_servers(self):
        """Get all SMTP server configurations"""
        try:
            servers = self.data_manager.get_smtp_servers()
            self.send_json_response({'success': True, 'data': servers})
        except Exception as e:
            logging.error(f"Error getting SMTP servers: {e}")
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def serve_subject_lists(self):
        """Get all subject lists"""
        try:
            lists = self.data_manager.get_subject_lists()
            self.send_json_response({'success': True, 'data': lists})
        except Exception as e:
            logging.error(f"Error getting subject lists: {e}")
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def serve_templates(self):
        """Get all message templates"""
        try:
            templates = self.data_manager.get_message_templates()
            self.send_json_response({'success': True, 'data': templates})
        except Exception as e:
            logging.error(f"Error getting templates: {e}")
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def serve_campaigns(self):
        """Get all campaigns"""
        try:
            campaigns = self.data_manager.get_campaigns()
            self.send_json_response({'success': True, 'data': campaigns})
        except Exception as e:
            logging.error(f"Error getting campaigns: {e}")
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def serve_placeholders(self):
        """Get all available placeholders"""
        try:
            placeholders = self.placeholder_manager.get_all_placeholders()
            self.send_json_response({'success': True, 'data': placeholders})
        except Exception as e:
            logging.error(f"Error getting placeholders: {e}")
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def serve_config(self):
        """Get application configuration"""
        try:
            self.send_json_response({'success': True, 'data': self.config})
        except Exception as e:
            logging.error(f"Error getting config: {e}")
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def save_config(self, data):
        """Save application configuration"""
        try:
            self.config.update(data)
            save_config(self.config)
            self.send_json_response({'success': True, 'message': 'Configuration saved'})
        except Exception as e:
            logging.error(f"Error saving config: {e}")
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def save_smtp_server(self, data):
        """Save SMTP server configuration"""
        try:
            result = self.data_manager.save_smtp_server(data)
            self.send_json_response({'success': True, 'data': result})
        except Exception as e:
            logging.error(f"Error saving SMTP server: {e}")
            self.send_json_response({'success': False, 'error': str(e)}, 500)
    
    def test_smtp_server(self, data):
        """Test SMTP server connection"""
        try:
            result = self.data_manager.test_smtp_connection(data)
            self.send_json_response({'success': True, 'data': result})
        except Exception as e:
            logging.error(f"Error testing SMTP server: {e}")
            self.send_json_response({'success': False, 'error': str(e)}, 500)

class DeepMailerSimpleApp:
    """Simple HTTP server application for DeepMailer v1.0"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.placeholder_manager = PlaceholderManager()
        self.config = {}
        self.server = None
        
        # Setup
        self.setup_app()
        
    def setup_app(self):
        """Setup application directories and configuration"""
        # Setup directories
        setup_directories()
        
        # Setup logging
        setup_logging()
        
        # Load configuration
        self.config = load_config()
        
        logging.info("DeepMailer Simple HTTP server initialized successfully")
    
    def create_handler(self):
        """Create HTTP handler with injected dependencies"""
        def handler(*args, **kwargs):
            return DeepMailerHTTPHandler(*args, 
                                       data_manager=self.data_manager,
                                       placeholder_manager=self.placeholder_manager,
                                       config=self.config,
                                       **kwargs)
        return handler
    
    def run(self, host='127.0.0.1', port=5000):
        """Run the HTTP server"""
        try:
            handler = self.create_handler()
            self.server = HTTPServer((host, port), handler)
            
            logging.info(f"Starting DeepMailer HTTP server on {host}:{port}")
            print(f"DeepMailer v1.0 is running at: http://{host}:{port}")
            print("Press Ctrl+C to stop the server")
            
            self.server.serve_forever()
            
        except KeyboardInterrupt:
            logging.info("Server stopped by user")
            print("\nShutting down server...")
        except Exception as e:
            logging.error(f"Server error: {e}")
            print(f"Server error: {e}")
        finally:
            if self.server:
                self.server.server_close()

def create_app():
    """Create and return application instance"""
    return DeepMailerSimpleApp()

if __name__ == "__main__":
    # Create and run the application
    app = DeepMailerSimpleApp()
    app.run()