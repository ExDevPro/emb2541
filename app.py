#!/usr/bin/env python3
"""
DeepMailer v1.0 - Flask Backend Server

Main Flask application server providing REST API endpoints for the 
email marketing software. Replaces PyQt6 backend with web-based architecture.

Author: DeepMailer Development Team
Version: 1.0
License: Commercial
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit

# Import core modules
from core.utils import setup_directories, load_config, save_config
from core.logger import setup_logging
from modules.data_manager import DataManager
from modules.placeholders import PlaceholderManager

class DeepMailerFlaskApp:
    """Flask application for DeepMailer v1.0"""
    
    def __init__(self):
        self.app = Flask(__name__, 
                        template_folder='frontend/templates',
                        static_folder='frontend/static')
        self.app.config['SECRET_KEY'] = 'deepmailer-v1-secret-key-2024'
        
        # Enable CORS for frontend
        CORS(self.app, resources={r"/api/*": {"origins": "*"}})
        
        # Initialize SocketIO for real-time updates
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        # Initialize components
        self.data_manager = DataManager()
        self.placeholder_manager = PlaceholderManager()
        self.config = {}
        
        # Setup
        self.setup_app()
        self.register_routes()
        self.register_socketio_events()
        
    def setup_app(self):
        """Setup application directories and configuration"""
        # Setup directories
        setup_directories()
        
        # Setup logging
        setup_logging()
        
        # Load configuration
        self.config = load_config()
        
        logging.info("DeepMailer Flask backend initialized successfully")
        
    def register_routes(self):
        """Register all API routes"""
        
        # Main application route
        @self.app.route('/')
        def index():
            """Serve the main application page"""
            return render_template('index.html')
            
        # Static file routes
        @self.app.route('/static/<path:filename>')
        def static_files(filename):
            """Serve static files"""
            return send_from_directory('frontend/static', filename)
            
        # API Routes
        
        # Dashboard API
        @self.app.route('/api/dashboard/stats')
        def get_dashboard_stats():
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
                return jsonify({'success': True, 'data': stats})
            except Exception as e:
                logging.error(f"Error getting dashboard stats: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
                
        # Leads API
        @self.app.route('/api/leads/lists')
        def get_lead_lists():
            """Get all lead lists"""
            try:
                lists = self.data_manager.get_lead_lists()
                return jsonify({'success': True, 'data': lists})
            except Exception as e:
                logging.error(f"Error getting lead lists: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
                
        @self.app.route('/api/leads/list/<list_name>')
        def get_lead_list(list_name):
            """Get specific lead list data"""
            try:
                page = int(request.args.get('page', 1))
                per_page = int(request.args.get('per_page', 100))
                search = request.args.get('search', '')
                
                leads = self.data_manager.get_leads(list_name, page, per_page, search)
                return jsonify({'success': True, 'data': leads})
            except Exception as e:
                logging.error(f"Error getting lead list {list_name}: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
                
        @self.app.route('/api/leads/import', methods=['POST'])
        def import_leads():
            """Import leads from uploaded file"""
            try:
                if 'file' not in request.files:
                    return jsonify({'success': False, 'error': 'No file uploaded'}), 400
                    
                file = request.files['file']
                list_name = request.form.get('list_name')
                duplicate_handling = request.form.get('duplicate_handling', 'skip')
                
                if not list_name:
                    return jsonify({'success': False, 'error': 'List name required'}), 400
                    
                result = self.data_manager.import_leads_file(file, list_name, duplicate_handling)
                return jsonify({'success': True, 'data': result})
            except Exception as e:
                logging.error(f"Error importing leads: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
                
        # SMTP API
        @self.app.route('/api/smtp/servers')
        def get_smtp_servers():
            """Get all SMTP server configurations"""
            try:
                servers = self.data_manager.get_smtp_servers()
                return jsonify({'success': True, 'data': servers})
            except Exception as e:
                logging.error(f"Error getting SMTP servers: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
                
        @self.app.route('/api/smtp/server', methods=['POST'])
        def save_smtp_server():
            """Save SMTP server configuration"""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({'success': False, 'error': 'No data provided'}), 400
                    
                result = self.data_manager.save_smtp_server(data)
                return jsonify({'success': True, 'data': result})
            except Exception as e:
                logging.error(f"Error saving SMTP server: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
                
        @self.app.route('/api/smtp/test', methods=['POST'])
        def test_smtp_server():
            """Test SMTP server connection"""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({'success': False, 'error': 'No data provided'}), 400
                    
                result = self.data_manager.test_smtp_connection(data)
                return jsonify({'success': True, 'data': result})
            except Exception as e:
                logging.error(f"Error testing SMTP server: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
                
        # Subjects API
        @self.app.route('/api/subjects/lists')
        def get_subject_lists():
            """Get all subject lists"""
            try:
                lists = self.data_manager.get_subject_lists()
                return jsonify({'success': True, 'data': lists})
            except Exception as e:
                logging.error(f"Error getting subject lists: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
                
        # Templates API
        @self.app.route('/api/templates')
        def get_templates():
            """Get all message templates"""
            try:
                templates = self.data_manager.get_message_templates()
                return jsonify({'success': True, 'data': templates})
            except Exception as e:
                logging.error(f"Error getting templates: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
                
        # Campaigns API
        @self.app.route('/api/campaigns')
        def get_campaigns():
            """Get all campaigns"""
            try:
                campaigns = self.data_manager.get_campaigns()
                return jsonify({'success': True, 'data': campaigns})
            except Exception as e:
                logging.error(f"Error getting campaigns: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
                
        # Placeholders API
        @self.app.route('/api/placeholders')
        def get_placeholders():
            """Get all available placeholders"""
            try:
                placeholders = self.placeholder_manager.get_all_placeholders()
                return jsonify({'success': True, 'data': placeholders})
            except Exception as e:
                logging.error(f"Error getting placeholders: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
                
        # Configuration API
        @self.app.route('/api/config')
        def get_config():
            """Get application configuration"""
            try:
                return jsonify({'success': True, 'data': self.config})
            except Exception as e:
                logging.error(f"Error getting config: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
                
        @self.app.route('/api/config', methods=['POST'])
        def save_config_api():
            """Save application configuration"""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({'success': False, 'error': 'No data provided'}), 400
                    
                self.config.update(data)
                save_config(self.config)
                return jsonify({'success': True, 'message': 'Configuration saved'})
            except Exception as e:
                logging.error(f"Error saving config: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
                
    def register_socketio_events(self):
        """Register SocketIO events for real-time updates"""
        
        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection"""
            logging.info(f"Client connected: {request.sid}")
            emit('connected', {'message': 'Connected to DeepMailer server'})
            
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection"""
            logging.info(f"Client disconnected: {request.sid}")
            
        @self.socketio.on('dashboard_update_request')
        def handle_dashboard_update():
            """Handle dashboard update request"""
            try:
                # Get fresh stats and emit to client
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
                    'campaigns': {
                        'active': self.data_manager.count_active_campaigns(),
                        'emails_sent': self.data_manager.count_total_emails_sent(),
                        'emails_failed': self.data_manager.count_total_emails_failed()
                    }
                }
                emit('dashboard_stats_update', stats)
            except Exception as e:
                logging.error(f"Error handling dashboard update: {e}")
                emit('error', {'message': str(e)})
                
    def run(self, host='127.0.0.1', port=5000, debug=False):
        """Run the Flask application"""
        logging.info(f"Starting DeepMailer Flask server on {host}:{port}")
        self.socketio.run(self.app, host=host, port=port, debug=debug)

def create_app():
    """Create and return Flask application instance"""
    deepmailer_app = DeepMailerFlaskApp()
    return deepmailer_app.app, deepmailer_app.socketio

if __name__ == "__main__":
    # Create and run the application
    deepmailer_app = DeepMailerFlaskApp()
    deepmailer_app.run(debug=True)