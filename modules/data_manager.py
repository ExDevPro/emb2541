"""
Data Manager for DeepMailer v1.0

This module handles all data operations including leads, SMTPs, subjects,
templates, campaigns, and provides centralized data access for the application.
"""

import os
import json
import csv
import logging
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

# Remove pandas and openpyxl imports for now
# import pandas as pd
# import openpyxl

from core.utils import (
    get_data_path, safe_filename, load_json_file, 
    save_json_file, validate_email
)

class DataManager:
    """Centralized data manager for all application data"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self._lock = threading.Lock()
        self._cache = {}
        self._cache_timeout = 60  # seconds
        
    def _get_cache_key(self, operation: str, *args) -> str:
        """Generate cache key"""
        return f"{operation}:{':'.join(map(str, args))}"
        
    def _is_cache_valid(self, key: str) -> bool:
        """Check if cache entry is valid"""
        if key not in self._cache:
            return False
        timestamp, _ = self._cache[key]
        return (datetime.now().timestamp() - timestamp) < self._cache_timeout
        
    def _set_cache(self, key: str, value: Any):
        """Set cache value"""
        self._cache[key] = (datetime.now().timestamp(), value)
        
    def _get_cache(self, key: str) -> Any:
        """Get cache value"""
        if self._is_cache_valid(key):
            return self._cache[key][1]
        return None
    
    # Dashboard Statistics Methods
    def count_total_leads(self) -> int:
        """Count total leads across all lists"""
        try:
            leads_dir = get_data_path('leads')
            total = 0
            for file_path in leads_dir.glob("*.csv"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        row_count = sum(1 for row in reader) - 1  # Exclude header
                        total += max(0, row_count)
                except Exception as e:
                    self.logger.error(f"Error counting leads in {file_path}: {e}")
            return total
        except Exception as e:
            self.logger.error(f"Error counting total leads: {e}")
            return 0
    
    def count_valid_emails(self) -> int:
        """Count valid emails across all lists"""
        try:
            leads_dir = get_data_path('leads')
            valid_count = 0
            for file_path in leads_dir.glob("*.csv"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            # Find email column (case insensitive)
                            email = None
                            for key, value in row.items():
                                if key.lower() in ['email', 'e-mail', 'mail']:
                                    email = value
                                    break
                            if email and validate_email(email):
                                valid_count += 1
                except Exception as e:
                    self.logger.error(f"Error validating emails in {file_path}: {e}")
            return valid_count
        except Exception as e:
            self.logger.error(f"Error counting valid emails: {e}")
            return 0
    
    def count_lead_lists(self) -> int:
        """Count number of lead lists"""
        try:
            leads_dir = get_data_path('leads')
            return len(list(leads_dir.glob("*.csv")))
        except Exception as e:
            self.logger.error(f"Error counting lead lists: {e}")
            return 0
    
    def count_smtp_servers(self) -> int:
        """Count total SMTP servers"""
        try:
            smtp_dir = get_data_path('smtp')
            return len(list(smtp_dir.glob("*.json")))
        except Exception as e:
            self.logger.error(f"Error counting SMTP servers: {e}")
            return 0
    
    def count_active_smtps(self) -> int:
        """Count active SMTP servers"""
        try:
            smtp_dir = get_data_path('smtp')
            active_count = 0
            for file_path in smtp_dir.glob("*.json"):
                try:
                    smtp_data = load_json_file(file_path)
                    if smtp_data.get('status') == 'active':
                        active_count += 1
                except Exception as e:
                    self.logger.error(f"Error reading SMTP file {file_path}: {e}")
            return active_count
        except Exception as e:
            self.logger.error(f"Error counting active SMTPs: {e}")
            return 0
    
    def count_inactive_smtps(self) -> int:
        """Count inactive SMTP servers"""
        return self.count_smtp_servers() - self.count_active_smtps()
    
    def count_total_subjects(self) -> int:
        """Count total subjects across all lists"""
        try:
            subject_dir = get_data_path('subject')
            total = 0
            for file_path in subject_dir.glob("*.csv"):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        row_count = sum(1 for row in reader) - 1  # Exclude header
                        total += max(0, row_count)
                except Exception as e:
                    self.logger.error(f"Error counting subjects in {file_path}: {e}")
            return total
        except Exception as e:
            self.logger.error(f"Error counting total subjects: {e}")
            return 0
    
    def count_subject_lists(self) -> int:
        """Count number of subject lists"""
        try:
            subject_dir = get_data_path('subject')
            return len(list(subject_dir.glob("*.csv")))
        except Exception as e:
            self.logger.error(f"Error counting subject lists: {e}")
            return 0
    
    def count_message_templates(self) -> int:
        """Count message templates"""
        try:
            message_dir = get_data_path('message')
            return len([d for d in message_dir.iterdir() if d.is_dir()])
        except Exception as e:
            self.logger.error(f"Error counting message templates: {e}")
            return 0
    
    def count_templates_with_attachments(self) -> int:
        """Count templates with attachments"""
        try:
            message_dir = get_data_path('message')
            count = 0
            for template_dir in message_dir.iterdir():
                if template_dir.is_dir():
                    attachments_dir = template_dir / 'attachments'
                    if attachments_dir.exists() and any(attachments_dir.iterdir()):
                        count += 1
            return count
        except Exception as e:
            self.logger.error(f"Error counting templates with attachments: {e}")
            return 0
    
    def count_total_campaigns(self) -> int:
        """Count total campaigns"""
        try:
            campaigns_dir = get_data_path('campaigns')
            return len([d for d in campaigns_dir.iterdir() if d.is_dir()])
        except Exception as e:
            self.logger.error(f"Error counting total campaigns: {e}")
            return 0
    
    def count_active_campaigns(self) -> int:
        """Count active campaigns"""
        try:
            campaigns_dir = get_data_path('campaigns')
            active_count = 0
            for campaign_dir in campaigns_dir.iterdir():
                if campaign_dir.is_dir():
                    status_file = campaign_dir / 'status.json'
                    if status_file.exists():
                        try:
                            status_data = load_json_file(status_file)
                            if status_data.get('status') in ['running', 'active', 'sending']:
                                active_count += 1
                        except Exception as e:
                            self.logger.error(f"Error reading campaign status {status_file}: {e}")
            return active_count
        except Exception as e:
            self.logger.error(f"Error counting active campaigns: {e}")
            return 0
    
    def count_completed_campaigns(self) -> int:
        """Count completed campaigns"""
        try:
            campaigns_dir = get_data_path('campaigns')
            completed_count = 0
            for campaign_dir in campaigns_dir.iterdir():
                if campaign_dir.is_dir():
                    status_file = campaign_dir / 'status.json'
                    if status_file.exists():
                        try:
                            status_data = load_json_file(status_file)
                            if status_data.get('status') in ['completed', 'finished', 'done']:
                                completed_count += 1
                        except Exception as e:
                            self.logger.error(f"Error reading campaign status {status_file}: {e}")
            return completed_count
        except Exception as e:
            self.logger.error(f"Error counting completed campaigns: {e}")
            return 0
    
    def count_total_emails_sent(self) -> int:
        """Count total emails sent across all campaigns"""
        try:
            campaigns_dir = get_data_path('campaigns')
            total_sent = 0
            for campaign_dir in campaigns_dir.iterdir():
                if campaign_dir.is_dir():
                    stats_file = campaign_dir / 'stats.json'
                    if stats_file.exists():
                        try:
                            stats_data = load_json_file(stats_file)
                            total_sent += stats_data.get('emails_sent', 0)
                        except Exception as e:
                            self.logger.error(f"Error reading campaign stats {stats_file}: {e}")
            return total_sent
        except Exception as e:
            self.logger.error(f"Error counting total emails sent: {e}")
            return 0
    
    def count_total_emails_failed(self) -> int:
        """Count total emails failed across all campaigns"""
        try:
            campaigns_dir = get_data_path('campaigns')
            total_failed = 0
            for campaign_dir in campaigns_dir.iterdir():
                if campaign_dir.is_dir():
                    stats_file = campaign_dir / 'stats.json'
                    if stats_file.exists():
                        try:
                            stats_data = load_json_file(stats_file)
                            total_failed += stats_data.get('emails_failed', 0)
                        except Exception as e:
                            self.logger.error(f"Error reading campaign stats {stats_file}: {e}")
            return total_failed
        except Exception as e:
            self.logger.error(f"Error counting total emails failed: {e}")
            return 0
    
    # Data retrieval methods
    def get_lead_lists(self) -> List[Dict[str, Any]]:
        """Get all lead lists with metadata"""
        try:
            leads_dir = get_data_path('leads')
            lists = []
            
            for file_path in leads_dir.glob("*.csv"):
                try:
                    # Get file info
                    stats = file_path.stat()
                    
                    # Count rows
                    with open(file_path, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        row_count = sum(1 for row in reader) - 1  # Exclude header
                        
                    list_info = {
                        'name': file_path.stem,
                        'filename': file_path.name,
                        'path': str(file_path),
                        'row_count': max(0, row_count),
                        'created': datetime.fromtimestamp(stats.st_ctime).isoformat(),
                        'modified': datetime.fromtimestamp(stats.st_mtime).isoformat(),
                        'size': stats.st_size
                    }
                    lists.append(list_info)
                    
                except Exception as e:
                    self.logger.error(f"Error reading leads list {file_path}: {e}")
                    
            # Sort by modified date (newest first)
            lists.sort(key=lambda x: x['modified'], reverse=True)
            return lists
        except Exception as e:
            self.logger.error(f"Error getting lead lists: {e}")
            return []
    
    def get_leads(self, list_name: str, page: int = 1, per_page: int = 100, search: str = "") -> Dict[str, Any]:
        """Get leads from specific list with pagination"""
        try:
            leads_dir = get_data_path('leads')
            file_path = leads_dir / f"{list_name}.csv"
            
            if not file_path.exists():
                return {'leads': [], 'total': 0, 'page': page, 'per_page': per_page}
            
            leads = []
            headers = []
            
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                headers = reader.fieldnames or []
                
                for row in reader:
                    # Apply search filter
                    if search:
                        if not any(search.lower() in str(value).lower() for value in row.values()):
                            continue
                    leads.append(row)
            
            # Apply pagination
            total = len(leads)
            start = (page - 1) * per_page
            end = start + per_page
            paginated_leads = leads[start:end]
            
            return {
                'leads': paginated_leads,
                'headers': headers,
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': (total + per_page - 1) // per_page
            }
        except Exception as e:
            self.logger.error(f"Error getting leads from {list_name}: {e}")
            return {'leads': [], 'total': 0, 'page': page, 'per_page': per_page}
    
    def get_smtp_servers(self) -> List[Dict[str, Any]]:
        """Get all SMTP server configurations"""
        try:
            smtp_dir = get_data_path('smtp')
            servers = []
            
            for file_path in smtp_dir.glob("*.json"):
                try:
                    server_data = load_json_file(file_path)
                    servers.append(server_data)
                except Exception as e:
                    self.logger.error(f"Error reading SMTP file {file_path}: {e}")
            
            return servers
        except Exception as e:
            self.logger.error(f"Error getting SMTP servers: {e}")
            return []
    
    def get_subject_lists(self) -> List[Dict[str, Any]]:
        """Get all subject lists with metadata"""
        try:
            subject_dir = get_data_path('subject')
            lists = []
            
            for file_path in subject_dir.glob("*.csv"):
                try:
                    # Get file info
                    stats = file_path.stat()
                    
                    # Count rows
                    with open(file_path, 'r', encoding='utf-8') as f:
                        reader = csv.reader(f)
                        row_count = sum(1 for row in reader) - 1  # Exclude header
                        
                    list_info = {
                        'name': file_path.stem,
                        'filename': file_path.name,
                        'path': str(file_path),
                        'row_count': max(0, row_count),
                        'created': datetime.fromtimestamp(stats.st_ctime).isoformat(),
                        'modified': datetime.fromtimestamp(stats.st_mtime).isoformat(),
                        'size': stats.st_size
                    }
                    lists.append(list_info)
                    
                except Exception as e:
                    self.logger.error(f"Error reading subject list {file_path}: {e}")
                    
            # Sort by modified date (newest first)
            lists.sort(key=lambda x: x['modified'], reverse=True)
            return lists
        except Exception as e:
            self.logger.error(f"Error getting subject lists: {e}")
            return []
    
    def get_message_templates(self) -> List[Dict[str, Any]]:
        """Get all message templates"""
        try:
            message_dir = get_data_path('message')
            templates = []
            
            for template_dir in message_dir.iterdir():
                if template_dir.is_dir():
                    try:
                        metadata_file = template_dir / 'metadata.json'
                        if metadata_file.exists():
                            template_data = load_json_file(metadata_file)
                        else:
                            template_data = {'name': template_dir.name}
                        
                        # Check for files
                        html_file = template_dir / 'email.html'
                        plain_file = template_dir / 'plain.txt'
                        attachments_dir = template_dir / 'attachments'
                        
                        template_data.update({
                            'name': template_dir.name,
                            'has_html': html_file.exists(),
                            'has_plain': plain_file.exists(),
                            'has_attachments': attachments_dir.exists() and any(attachments_dir.iterdir()),
                            'path': str(template_dir)
                        })
                        
                        templates.append(template_data)
                        
                    except Exception as e:
                        self.logger.error(f"Error reading template {template_dir}: {e}")
            
            return templates
        except Exception as e:
            self.logger.error(f"Error getting message templates: {e}")
            return []
    
    def get_campaigns(self) -> List[Dict[str, Any]]:
        """Get all campaigns"""
        try:
            campaigns_dir = get_data_path('campaigns')
            campaigns = []
            
            for campaign_dir in campaigns_dir.iterdir():
                if campaign_dir.is_dir():
                    try:
                        config_file = campaign_dir / 'config.json'
                        status_file = campaign_dir / 'status.json'
                        stats_file = campaign_dir / 'stats.json'
                        
                        campaign_data = {'name': campaign_dir.name}
                        
                        if config_file.exists():
                            campaign_data.update(load_json_file(config_file))
                        
                        if status_file.exists():
                            campaign_data.update(load_json_file(status_file))
                        
                        if stats_file.exists():
                            campaign_data.update(load_json_file(stats_file))
                        
                        campaigns.append(campaign_data)
                        
                    except Exception as e:
                        self.logger.error(f"Error reading campaign {campaign_dir}: {e}")
            
            return campaigns
        except Exception as e:
            self.logger.error(f"Error getting campaigns: {e}")
            return []
    
    # Placeholder methods for saving data
    def import_leads_file(self, file, list_name: str, duplicate_handling: str) -> Dict[str, Any]:
        """Import leads from uploaded file"""
        # TODO: Implement file import logic
        return {'message': 'Import functionality to be implemented', 'imported': 0}
    
    def save_smtp_server(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Save SMTP server configuration"""
        # TODO: Implement SMTP save logic
        return {'message': 'SMTP save functionality to be implemented'}
    
    def test_smtp_connection(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Test SMTP server connection"""
        # TODO: Implement SMTP test logic
        return {'success': True, 'message': 'SMTP test functionality to be implemented'}
        
    # Leads Management
    def get_leads_lists(self) -> List[Dict[str, Any]]:
        """Get all leads lists with metadata"""
        cache_key = self._get_cache_key("leads_lists")
        cached = self._get_cache(cache_key)
        if cached is not None:
            return cached
            
        leads_dir = get_data_path('leads')
        lists = []
        
        for file_path in leads_dir.glob("*.csv"):
            try:
                # Get file info
                stats = file_path.stat()
                
                # Count rows
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    row_count = sum(1 for row in reader) - 1  # Exclude header
                    
                list_info = {
                    'name': file_path.stem,
                    'filename': file_path.name,
                    'path': str(file_path),
                    'row_count': max(0, row_count),
                    'created': datetime.fromtimestamp(stats.st_ctime),
                    'modified': datetime.fromtimestamp(stats.st_mtime),
                    'size': stats.st_size
                }
                lists.append(list_info)
                
            except Exception as e:
                self.logger.error(f"Error reading leads list {file_path}: {e}")
                
        # Sort by modified date (newest first)
        lists.sort(key=lambda x: x['modified'], reverse=True)
        
        self._set_cache(cache_key, lists)
        return lists
        
    def get_total_leads(self) -> int:
        """Get total number of leads across all lists"""
        cache_key = self._get_cache_key("total_leads")
        cached = self._get_cache(cache_key)
        if cached is not None:
            return cached
            
        total = 0
        lists = self.get_leads_lists()
        for list_info in lists:
            total += list_info['row_count']
            
        self._set_cache(cache_key, total)
        return total
        
    def load_leads_list(self, list_name: str) -> Tuple[List[str], List[List[str]]]:
        """Load a specific leads list"""
        cache_key = self._get_cache_key("leads_list", list_name)
        cached = self._get_cache(cache_key)
        if cached is not None:
            return cached
            
        leads_dir = get_data_path('leads')
        file_path = leads_dir / f"{safe_filename(list_name)}.csv"
        
        if not file_path.exists():
            return [], []
            
        try:
            with open(file_path, 'r', encoding='utf-8', newline='') as f:
                reader = csv.reader(f)
                rows = list(reader)
                
            if not rows:
                return [], []
                
            headers = rows[0]
            data = rows[1:] if len(rows) > 1 else []
            
            result = (headers, data)
            self._set_cache(cache_key, result)
            return result
            
        except Exception as e:
            self.logger.error(f"Error loading leads list {list_name}: {e}")
            return [], []
            
    def save_leads_list(self, list_name: str, headers: List[str], data: List[List[str]]) -> bool:
        """Save a leads list"""
        with self._lock:
            try:
                leads_dir = get_data_path('leads')
                file_path = leads_dir / f"{safe_filename(list_name)}.csv"
                
                with open(file_path, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)
                    writer.writerows(data)
                    
                # Clear cache
                self._cache.clear()
                
                self.logger.info(f"Saved leads list: {list_name}")
                return True
                
            except Exception as e:
                self.logger.error(f"Error saving leads list {list_name}: {e}")
                return False
                
    def import_leads_from_file(self, file_path: str, list_name: str) -> Tuple[bool, str, int]:
        """Import leads from a file (CSV, Excel, or Text)"""
        try:
            path = Path(file_path)
            if not path.exists():
                return False, "File not found", 0
                
            extension = path.suffix.lower()
            headers = []
            data = []
            
            if extension == '.csv':
                # CSV file
                with open(path, 'r', encoding='utf-8', newline='') as f:
                    # Try to detect delimiter
                    sample = f.read(1024)
                    f.seek(0)
                    
                    sniffer = csv.Sniffer()
                    delimiter = sniffer.sniff(sample).delimiter
                    
                    reader = csv.reader(f, delimiter=delimiter)
                    rows = list(reader)
                    
                if rows:
                    headers = rows[0]
                    data = rows[1:]
                    
            elif extension in ['.xlsx', '.xls']:
                # Excel file
                df = pd.read_excel(path)
                headers = df.columns.tolist()
                data = df.values.tolist()
                
            elif extension == '.txt':
                # Text file with colon separator
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                if lines:
                    headers = [h.strip() for h in lines[0].split(':')]
                    for line in lines[1:]:
                        row = [c.strip() for c in line.split(':')]
                        # Pad row to match headers length
                        while len(row) < len(headers):
                            row.append('')
                        data.append(row[:len(headers)])
                        
            else:
                return False, f"Unsupported file format: {extension}", 0
                
            if not headers or not data:
                return False, "No data found in file", 0
                
            # Validate email column exists
            email_col_found = False
            for header in headers:
                if header.lower() in ['email', 'e-mail', 'email_address']:
                    email_col_found = True
                    break
                    
            if not email_col_found:
                return False, "Email column not found (required)", 0
                
            # Save the imported data
            success = self.save_leads_list(list_name, headers, data)
            if success:
                return True, f"Successfully imported {len(data)} leads", len(data)
            else:
                return False, "Failed to save imported data", 0
                
        except Exception as e:
            self.logger.error(f"Error importing leads from {file_path}: {e}")
            return False, f"Import error: {str(e)}", 0
            
    def delete_leads_list(self, list_name: str) -> bool:
        """Delete a leads list"""
        with self._lock:
            try:
                leads_dir = get_data_path('leads')
                file_path = leads_dir / f"{safe_filename(list_name)}.csv"
                
                if file_path.exists():
                    file_path.unlink()
                    
                # Clear cache
                self._cache.clear()
                
                self.logger.info(f"Deleted leads list: {list_name}")
                return True
                
            except Exception as e:
                self.logger.error(f"Error deleting leads list {list_name}: {e}")
                return False
                
    # SMTP Management
    def get_smtp_servers(self) -> List[Dict[str, Any]]:
        """Get all SMTP servers"""
        cache_key = self._get_cache_key("smtp_servers")
        cached = self._get_cache(cache_key)
        if cached is not None:
            return cached
            
        smtp_dir = get_data_path('smtp')
        servers = []
        
        for file_path in smtp_dir.glob("*.json"):
            try:
                data = load_json_file(file_path)
                if data:
                    data['filename'] = file_path.name
                    servers.append(data)
                    
            except Exception as e:
                self.logger.error(f"Error loading SMTP config {file_path}: {e}")
                
        # Sort by name
        servers.sort(key=lambda x: x.get('server_name', ''))
        
        self._set_cache(cache_key, servers)
        return servers
        
    def get_total_smtp_servers(self) -> int:
        """Get total number of SMTP servers"""
        return len(self.get_smtp_servers())
        
    def save_smtp_server(self, server_data: Dict[str, Any]) -> bool:
        """Save SMTP server configuration"""
        with self._lock:
            try:
                smtp_dir = get_data_path('smtp')
                server_name = server_data.get('server_name', 'unnamed')
                file_path = smtp_dir / f"{safe_filename(server_name)}.json"
                
                # Add metadata
                server_data['created'] = server_data.get('created', datetime.now().isoformat())
                server_data['modified'] = datetime.now().isoformat()
                
                success = save_json_file(file_path, server_data)
                if success:
                    # Clear cache
                    self._cache.clear()
                    self.logger.info(f"Saved SMTP server: {server_name}")
                    
                return success
                
            except Exception as e:
                self.logger.error(f"Error saving SMTP server: {e}")
                return False
                
    def delete_smtp_server(self, server_name: str) -> bool:
        """Delete SMTP server"""
        with self._lock:
            try:
                smtp_dir = get_data_path('smtp')
                file_path = smtp_dir / f"{safe_filename(server_name)}.json"
                
                if file_path.exists():
                    file_path.unlink()
                    
                # Clear cache
                self._cache.clear()
                
                self.logger.info(f"Deleted SMTP server: {server_name}")
                return True
                
            except Exception as e:
                self.logger.error(f"Error deleting SMTP server {server_name}: {e}")
                return False
                
    # Subject Management
    def get_subject_lists(self) -> List[Dict[str, Any]]:
        """Get all subject lists"""
        cache_key = self._get_cache_key("subject_lists")
        cached = self._get_cache(cache_key)
        if cached is not None:
            return cached
            
        subject_dir = get_data_path('subject')
        lists = []
        
        for file_path in subject_dir.glob("*.csv"):
            try:
                stats = file_path.stat()
                
                # Count subjects
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    row_count = sum(1 for row in reader) - 1  # Exclude header
                    
                list_info = {
                    'name': file_path.stem,
                    'filename': file_path.name,
                    'path': str(file_path),
                    'subject_count': max(0, row_count),
                    'created': datetime.fromtimestamp(stats.st_ctime),
                    'modified': datetime.fromtimestamp(stats.st_mtime),
                    'size': stats.st_size
                }
                lists.append(list_info)
                
            except Exception as e:
                self.logger.error(f"Error reading subject list {file_path}: {e}")
                
        lists.sort(key=lambda x: x['modified'], reverse=True)
        
        self._set_cache(cache_key, lists)
        return lists
        
    def get_total_subjects(self) -> int:
        """Get total number of subjects across all lists"""
        cache_key = self._get_cache_key("total_subjects")
        cached = self._get_cache(cache_key)
        if cached is not None:
            return cached
            
        total = 0
        lists = self.get_subject_lists()
        for list_info in lists:
            total += list_info['subject_count']
            
        self._set_cache(cache_key, total)
        return total
        
    def get_total_smtp_servers(self) -> int:
        """Get total number of SMTP servers"""
        cache_key = self._get_cache_key("total_smtp")
        cached = self._get_cache(cache_key)
        if cached is not None:
            return cached
            
        smtp_dir = get_data_path('smtp')
        count = len(list(smtp_dir.glob("*.json")))
        
        self._set_cache(cache_key, count)
        return count
        
    def get_total_templates(self) -> int:
        """Get total number of message templates"""
        cache_key = self._get_cache_key("total_templates")
        cached = self._get_cache(cache_key)
        if cached is not None:
            return cached
            
        message_dir = get_data_path('message')
        count = len([d for d in message_dir.iterdir() if d.is_dir()])
        
        self._set_cache(cache_key, count)
        return count
        
    def get_total_campaigns(self) -> int:
        """Get total number of campaigns"""
        cache_key = self._get_cache_key("total_campaigns")
        cached = self._get_cache(cache_key)
        if cached is not None:
            return cached
            
        campaigns_dir = get_data_path('campaigns')
        count = len([d for d in campaigns_dir.iterdir() if d.is_dir()])
        
        self._set_cache(cache_key, count)
        return count
        
    def get_campaign_statistics(self) -> Dict[str, int]:
        """Get campaign statistics"""
        cache_key = self._get_cache_key("campaign_stats")
        cached = self._get_cache(cache_key)
        if cached is not None:
            return cached
            
        campaigns_dir = get_data_path('campaigns')
        stats = {
            'total': 0,
            'active': 0,
            'draft': 0,
            'completed': 0,
            'paused': 0,
            'failed': 0,
            'running': 0,
            'sent': 0,
            'failed_emails': 0,
            'remaining': 0
        }
        
        for campaign_dir in campaigns_dir.iterdir():
            if campaign_dir.is_dir():
                config_file = campaign_dir / 'config.json'
                if config_file.exists():
                    try:
                        with open(config_file, 'r', encoding='utf-8') as f:
                            campaign_data = json.load(f)
                            
                        stats['total'] += 1
                        status = campaign_data.get('status', 'draft')
                        if status in stats:
                            stats[status] += 1
                        else:
                            stats[status] = 1
                        
                        # Add sent/failed counts
                        stats['sent'] += campaign_data.get('sent_count', 0)
                        stats['failed_emails'] += campaign_data.get('failed_count', 0)
                        
                    except Exception as e:
                        self.logger.error(f"Error reading campaign {campaign_dir}: {e}")
                        
        self._set_cache(cache_key, stats)
        return stats
        
    def get_tracking_statistics(self) -> Dict[str, Any]:
        """Get tracking statistics"""
        # Placeholder for tracking stats
        return {
            'enabled': False,
            'opens': 0,
            'clicks': 0,
            'unique_opens': 0,
            'unique_clicks': 0
        }
        
    def get_system_statistics(self) -> Dict[str, Any]:
        """Get system statistics"""
        import threading
        
        try:
            # Try to get memory usage if psutil is available
            try:
                import psutil
                memory_percent = psutil.virtual_memory().percent
                memory_status = "Normal"
                if memory_percent > 80:
                    memory_status = "High"
                elif memory_percent > 90:
                    memory_status = "Critical"
            except ImportError:
                memory_status = "Unknown"
                memory_percent = 0
                
            # Get thread count
            thread_count = threading.active_count()
            
            # Get error count (would be from log files in real implementation)
            error_count = 0
            
            return {
                'memory': memory_status,
                'memory_percent': memory_percent,
                'threads': thread_count,
                'errors': error_count,
                'uptime': 'N/A'
            }
        except Exception as e:
            # Fallback for any errors
            return {
                'memory': 'Unknown',
                'memory_percent': 0,
                'threads': threading.active_count(),
                'errors': 0,
                'uptime': 'N/A'
            }
        
    # Template Management
    def get_templates(self) -> List[Dict[str, Any]]:
        """Get all message templates"""
        cache_key = self._get_cache_key("templates")
        cached = self._get_cache(cache_key)
        if cached is not None:
            return cached
            
        message_dir = get_data_path('message')
        templates = []
        
        for template_dir in message_dir.iterdir():
            if template_dir.is_dir():
                try:
                    metadata_file = template_dir / "metadata.json"
                    template_info = {
                        'name': template_dir.name,
                        'path': str(template_dir),
                        'created': datetime.fromtimestamp(template_dir.stat().st_ctime),
                        'modified': datetime.fromtimestamp(template_dir.stat().st_mtime),
                        'has_html': (template_dir / "email.html").exists(),
                        'has_text': (template_dir / "plain.txt").exists(),
                        'has_attachments': (template_dir / "attachments").exists()
                    }
                    
                    # Load metadata if available
                    if metadata_file.exists():
                        metadata = load_json_file(metadata_file)
                        if metadata:
                            template_info.update(metadata)
                            
                    templates.append(template_info)
                    
                except Exception as e:
                    self.logger.error(f"Error reading template {template_dir}: {e}")
                    
        templates.sort(key=lambda x: x['modified'], reverse=True)
        
        self._set_cache(cache_key, templates)
        return templates
        
    def get_total_templates(self) -> int:
        """Get total number of templates"""
        return len(self.get_templates())
        
    # Campaign Management
    def get_campaigns(self) -> List[Dict[str, Any]]:
        """Get all campaigns"""
        cache_key = self._get_cache_key("campaigns")
        cached = self._get_cache(cache_key)
        if cached is not None:
            return cached
            
        campaigns_dir = get_data_path('campaigns')
        campaigns = []
        
        for campaign_dir in campaigns_dir.iterdir():
            if campaign_dir.is_dir():
                try:
                    config_file = campaign_dir / "config.json"
                    if config_file.exists():
                        config = load_json_file(config_file)
                        if config:
                            config['name'] = campaign_dir.name
                            config['path'] = str(campaign_dir)
                            campaigns.append(config)
                            
                except Exception as e:
                    self.logger.error(f"Error reading campaign {campaign_dir}: {e}")
                    
        campaigns.sort(key=lambda x: x.get('created', ''), reverse=True)
        
        self._set_cache(cache_key, campaigns)
        return campaigns
        
    def get_campaign_statistics(self) -> Dict[str, int]:
        """Get campaign statistics"""
        cache_key = self._get_cache_key("campaign_stats")
        cached = self._get_cache(cache_key)
        if cached is not None:
            return cached
            
        campaigns = self.get_campaigns()
        stats = {
            'total': len(campaigns),
            'active': 0,
            'paused': 0,
            'completed': 0,
            'sent': 0,
            'failed': 0,
            'remaining': 0
        }
        
        for campaign in campaigns:
            status = campaign.get('status', 'draft')
            if status == 'running':
                stats['active'] += 1
            elif status == 'paused':
                stats['paused'] += 1
            elif status == 'completed':
                stats['completed'] += 1
                
            # Add email counts
            stats['sent'] += campaign.get('emails_sent', 0)
            stats['failed'] += campaign.get('emails_failed', 0)
            stats['remaining'] += campaign.get('emails_remaining', 0)
            
        self._set_cache(cache_key, stats)
        return stats
        
    def get_tracking_statistics(self) -> Dict[str, Any]:
        """Get tracking statistics"""
        # For now, return placeholder data
        # In a real implementation, this would query tracking database
        return {
            'enabled': False,
            'opens': 0,
            'clicks': 0,
            'unique_opens': 0,
            'unique_clicks': 0
        }
        
    def get_system_statistics(self) -> Dict[str, Any]:
        """Get system statistics"""
        import psutil
        import threading
        
        try:
            process = psutil.Process()
            memory_percent = process.memory_percent()
            
            # Determine memory status
            if memory_percent < 50:
                memory_status = "Normal"
            elif memory_percent < 80:
                memory_status = "High"
            else:
                memory_status = "Critical"
                
            return {
                'memory': memory_status,
                'memory_percent': memory_percent,
                'threads': threading.active_count(),
                'errors': 0  # TODO: Implement error counting
            }
        except Exception:
            return {
                'memory': 'Unknown',
                'memory_percent': 0,
                'threads': threading.active_count(),
                'errors': 0
            }
            
    def clear_cache(self):
        """Clear all cached data"""
        with self._lock:
            self._cache.clear()
            self.logger.debug("Data manager cache cleared")