"""
SMTP Management Widget for DeepMailer v1.0

This module provides comprehensive SMTP server management functionality including
configuration, testing, proxy support, rate limiting, and rotation settings.
"""

import logging
import smtplib
import socket
from datetime import datetime, timedelta
from typing import Dict, List, Any, Tuple, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QLineEdit,
    QSpinBox, QGroupBox, QMessageBox, QDialog, QDialogButtonBox,
    QTextEdit, QCheckBox, QProgressBar, QFrame, QSplitter, QListWidget,
    QListWidgetItem, QScrollArea, QTabWidget, QFormLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor

from modules.data_manager import DataManager
from core.utils import format_number, safe_filename

class SMTPTestWorker(QThread):
    """Worker thread for testing SMTP connections"""
    
    progress = pyqtSignal(str)
    finished = pyqtSignal(bool, str)
    
    def __init__(self, smtp_config: Dict[str, Any]):
        super().__init__()
        self.smtp_config = smtp_config
        
    def run(self):
        """Test SMTP connection in background thread"""
        try:
            self.progress.emit("Connecting to SMTP server...")
            
            host = self.smtp_config.get('host', '')
            port = int(self.smtp_config.get('port', 587))
            username = self.smtp_config.get('username', '')
            password = self.smtp_config.get('password', '')
            security = self.smtp_config.get('security', 'auto')
            
            # Determine security type
            if security == 'ssl' or port == 465:
                self.progress.emit("Establishing SSL connection...")
                server = smtplib.SMTP_SSL(host, port, timeout=30)
            else:
                self.progress.emit("Establishing connection...")
                server = smtplib.SMTP(host, port, timeout=30)
                
                if security == 'tls' or port == 587:
                    self.progress.emit("Starting TLS...")
                    server.starttls()
                    
            self.progress.emit("Authenticating...")
            server.login(username, password)
            
            self.progress.emit("Testing successful!")
            server.quit()
            
            self.finished.emit(True, "SMTP connection test successful!")
            
        except smtplib.SMTPAuthenticationError:
            self.finished.emit(False, "Authentication failed. Check username and password.")
        except smtplib.SMTPConnectError:
            self.finished.emit(False, "Cannot connect to SMTP server. Check host and port.")
        except smtplib.SMTPServerDisconnected:
            self.finished.emit(False, "Server disconnected unexpectedly.")
        except socket.timeout:
            self.finished.emit(False, "Connection timeout. Check host and port.")
        except Exception as e:
            self.finished.emit(False, f"Test failed: {str(e)}")

class SMTPConfigDialog(QDialog):
    """Dialog for configuring SMTP servers"""
    
    def __init__(self, smtp_data: Dict[str, Any] = None, parent=None):
        super().__init__(parent)
        self.smtp_data = smtp_data or {}
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        """Setup the SMTP configuration dialog"""
        self.setWindowTitle("SMTP Server Configuration")
        self.setModal(True)
        self.resize(600, 700)
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("SMTP Server Configuration")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Create tab widget
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)
        
        # Basic settings tab
        self.setup_basic_tab()
        
        # Advanced settings tab
        self.setup_advanced_tab()
        
        # Rate limiting tab
        self.setup_rate_limiting_tab()
        
        # Proxy settings tab
        self.setup_proxy_tab()
        
        # Test button
        self.test_btn = QPushButton("🧪 Test Connection")
        self.test_btn.clicked.connect(self.test_connection)
        layout.addWidget(self.test_btn)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
    def setup_basic_tab(self):
        """Setup basic settings tab"""
        basic_widget = QWidget()
        layout = QFormLayout(basic_widget)
        
        # Server name
        self.server_name_field = QLineEdit()
        self.server_name_field.setPlaceholderText("Enter server name")
        layout.addRow("Server Name*:", self.server_name_field)
        
        # Description
        self.description_field = QLineEdit()
        self.description_field.setPlaceholderText("Optional description")
        layout.addRow("Description:", self.description_field)
        
        # Host
        self.host_field = QLineEdit()
        self.host_field.setPlaceholderText("smtp.gmail.com")
        layout.addRow("Host*:", self.host_field)
        
        # Port
        self.port_field = QSpinBox()
        self.port_field.setRange(1, 65535)
        self.port_field.setValue(587)
        layout.addRow("Port*:", self.port_field)
        
        # Security
        self.security_combo = QComboBox()
        self.security_combo.addItems(["Auto", "None", "SSL", "TLS"])
        layout.addRow("Security:", self.security_combo)
        
        # Authentication
        self.auth_combo = QComboBox()
        self.auth_combo.addItems(["Auto", "PLAIN", "LOGIN", "CRAM-MD5"])
        layout.addRow("Authentication:", self.auth_combo)
        
        # Username
        self.username_field = QLineEdit()
        self.username_field.setPlaceholderText("your.email@gmail.com")
        layout.addRow("Username*:", self.username_field)
        
        # Password
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_field.setPlaceholderText("Enter password")
        layout.addRow("Password*:", self.password_field)
        
        # From email
        self.from_email_field = QLineEdit()
        self.from_email_field.setPlaceholderText("sender@gmail.com")
        layout.addRow("From Email*:", self.from_email_field)
        
        self.tabs.addTab(basic_widget, "Basic Settings")
        
    def setup_advanced_tab(self):
        """Setup advanced settings tab"""
        advanced_widget = QWidget()
        layout = QVBoxLayout(advanced_widget)
        
        # From Name Header
        from_name_group = QGroupBox("From Name Header")
        from_name_layout = QVBoxLayout(from_name_group)
        
        self.from_name_enabled = QCheckBox("Enable From Name Header")
        from_name_layout.addWidget(self.from_name_enabled)
        
        # From name mode
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Mode:"))
        self.from_name_mode = QComboBox()
        self.from_name_mode.addItems(["Custom", "Faker"])
        mode_layout.addWidget(self.from_name_mode)
        mode_layout.addStretch()
        from_name_layout.addLayout(mode_layout)
        
        # From names
        self.from_names_field = QTextEdit()
        self.from_names_field.setMaximumHeight(80)
        self.from_names_field.setPlaceholderText("Enter from names (one per line)")
        from_name_layout.addWidget(QLabel("From Names:"))
        from_name_layout.addWidget(self.from_names_field)
        
        # Rotation
        rotation_layout = QHBoxLayout()
        rotation_layout.addWidget(QLabel("Rotation:"))
        self.from_name_rotation = QComboBox()
        self.from_name_rotation.addItems(["Each time", "Custom range"])
        rotation_layout.addWidget(self.from_name_rotation)
        rotation_layout.addStretch()
        from_name_layout.addLayout(rotation_layout)
        
        layout.addWidget(from_name_group)
        
        # Reply-To Header
        reply_to_group = QGroupBox("Reply-To Header")
        reply_to_layout = QVBoxLayout(reply_to_group)
        
        self.reply_to_enabled = QCheckBox("Enable Reply-To Header")
        reply_to_layout.addWidget(self.reply_to_enabled)
        
        # Reply-to mode
        reply_mode_layout = QHBoxLayout()
        reply_mode_layout.addWidget(QLabel("Mode:"))
        self.reply_to_mode = QComboBox()
        self.reply_to_mode.addItems(["Custom", "Faker"])
        reply_mode_layout.addWidget(self.reply_to_mode)
        reply_mode_layout.addStretch()
        reply_to_layout.addLayout(reply_mode_layout)
        
        # Reply-to addresses
        self.reply_to_field = QTextEdit()
        self.reply_to_field.setMaximumHeight(80)
        self.reply_to_field.setPlaceholderText("Enter reply-to addresses (one per line)")
        reply_to_layout.addWidget(QLabel("Reply-To Addresses:"))
        reply_to_layout.addWidget(self.reply_to_field)
        
        layout.addWidget(reply_to_group)
        layout.addStretch()
        
        self.tabs.addTab(advanced_widget, "Advanced")
        
    def setup_rate_limiting_tab(self):
        """Setup rate limiting tab"""
        rate_widget = QWidget()
        layout = QVBoxLayout(rate_widget)
        
        # Enable rate limiting
        self.rate_limiting_enabled = QCheckBox("Enable Rate Limiting")
        layout.addWidget(self.rate_limiting_enabled)
        
        # Rate limits
        limits_group = QGroupBox("Rate Limits")
        limits_layout = QFormLayout(limits_group)
        
        # Per minute
        self.per_minute_field = QSpinBox()
        self.per_minute_field.setRange(0, 9999)
        self.per_minute_field.setValue(60)
        self.per_minute_field.setSuffix(" emails/minute")
        limits_layout.addRow("Per Minute:", self.per_minute_field)
        
        # Hourly
        self.hourly_field = QSpinBox()
        self.hourly_field.setRange(0, 999999)
        self.hourly_field.setValue(1000)
        self.hourly_field.setSuffix(" emails/hour")
        limits_layout.addRow("Hourly:", self.hourly_field)
        
        # Daily
        self.daily_field = QSpinBox()
        self.daily_field.setRange(0, 999999)
        self.daily_field.setValue(10000)
        self.daily_field.setSuffix(" emails/day")
        limits_layout.addRow("Daily:", self.daily_field)
        
        # Total limit
        self.total_limit_field = QSpinBox()
        self.total_limit_field.setRange(0, 9999999)
        self.total_limit_field.setValue(0)
        self.total_limit_field.setSuffix(" emails (0 = unlimited)")
        limits_layout.addRow("Total Limit:", self.total_limit_field)
        
        layout.addWidget(limits_group)
        
        # Reset button
        self.reset_limits_btn = QPushButton("🔄 Reset Usage Counters")
        self.reset_limits_btn.clicked.connect(self.reset_usage_counters)
        layout.addWidget(self.reset_limits_btn)
        
        layout.addStretch()
        self.tabs.addTab(rate_widget, "Rate Limiting")
        
    def setup_proxy_tab(self):
        """Setup proxy settings tab"""
        proxy_widget = QWidget()
        layout = QVBoxLayout(proxy_widget)
        
        # Enable proxy
        self.proxy_enabled = QCheckBox("Enable Proxy")
        layout.addWidget(self.proxy_enabled)
        
        # Proxy settings
        proxy_group = QGroupBox("Proxy Configuration")
        proxy_layout = QFormLayout(proxy_group)
        
        # Type
        self.proxy_type = QComboBox()
        self.proxy_type.addItems(["HTTP", "HTTPS", "SOCKS5"])
        proxy_layout.addRow("Type:", self.proxy_type)
        
        # Host
        self.proxy_host = QLineEdit()
        self.proxy_host.setPlaceholderText("proxy.example.com")
        proxy_layout.addRow("Host:", self.proxy_host)
        
        # Port
        self.proxy_port = QSpinBox()
        self.proxy_port.setRange(1, 65535)
        self.proxy_port.setValue(8080)
        proxy_layout.addRow("Port:", self.proxy_port)
        
        # Authentication
        self.proxy_auth = QCheckBox("Requires Authentication")
        proxy_layout.addRow(self.proxy_auth)
        
        # Username
        self.proxy_username = QLineEdit()
        self.proxy_username.setPlaceholderText("Proxy username")
        proxy_layout.addRow("Username:", self.proxy_username)
        
        # Password
        self.proxy_password = QLineEdit()
        self.proxy_password.setEchoMode(QLineEdit.EchoMode.Password)
        self.proxy_password.setPlaceholderText("Proxy password")
        proxy_layout.addRow("Password:", self.proxy_password)
        
        layout.addWidget(proxy_group)
        layout.addStretch()
        
        self.tabs.addTab(proxy_widget, "Proxy")
        
    def load_data(self):
        """Load existing data into fields"""
        if not self.smtp_data:
            return
            
        # Basic settings
        self.server_name_field.setText(self.smtp_data.get('server_name', ''))
        self.description_field.setText(self.smtp_data.get('description', ''))
        self.host_field.setText(self.smtp_data.get('host', ''))
        self.port_field.setValue(self.smtp_data.get('port', 587))
        
        security = self.smtp_data.get('security', 'auto')
        self.security_combo.setCurrentText(security.title())
        
        auth = self.smtp_data.get('authentication', 'auto')
        self.auth_combo.setCurrentText(auth.title())
        
        self.username_field.setText(self.smtp_data.get('username', ''))
        self.password_field.setText(self.smtp_data.get('password', ''))
        self.from_email_field.setText(self.smtp_data.get('from_email', ''))
        
        # Advanced settings
        from_name_config = self.smtp_data.get('from_name', {})
        self.from_name_enabled.setChecked(from_name_config.get('enabled', False))
        self.from_name_mode.setCurrentText(from_name_config.get('mode', 'Custom'))
        self.from_names_field.setPlainText('\n'.join(from_name_config.get('values', [])))
        
        reply_to_config = self.smtp_data.get('reply_to', {})
        self.reply_to_enabled.setChecked(reply_to_config.get('enabled', False))
        self.reply_to_mode.setCurrentText(reply_to_config.get('mode', 'Custom'))
        self.reply_to_field.setPlainText('\n'.join(reply_to_config.get('values', [])))
        
        # Rate limiting
        rate_config = self.smtp_data.get('rate_limiting', {})
        self.rate_limiting_enabled.setChecked(rate_config.get('enabled', False))
        self.per_minute_field.setValue(rate_config.get('per_minute', 60))
        self.hourly_field.setValue(rate_config.get('hourly', 1000))
        self.daily_field.setValue(rate_config.get('daily', 10000))
        self.total_limit_field.setValue(rate_config.get('total_limit', 0))
        
        # Proxy
        proxy_config = self.smtp_data.get('proxy', {})
        self.proxy_enabled.setChecked(proxy_config.get('enabled', False))
        self.proxy_type.setCurrentText(proxy_config.get('type', 'HTTP'))
        self.proxy_host.setText(proxy_config.get('host', ''))
        self.proxy_port.setValue(proxy_config.get('port', 8080))
        self.proxy_auth.setChecked(proxy_config.get('auth_enabled', False))
        self.proxy_username.setText(proxy_config.get('username', ''))
        self.proxy_password.setText(proxy_config.get('password', ''))
        
    def get_data(self) -> Dict[str, Any]:
        """Get the configured data"""
        return {
            'server_name': self.server_name_field.text().strip(),
            'description': self.description_field.text().strip(),
            'host': self.host_field.text().strip(),
            'port': self.port_field.value(),
            'security': self.security_combo.currentText().lower(),
            'authentication': self.auth_combo.currentText().lower(),
            'username': self.username_field.text().strip(),
            'password': self.password_field.text(),
            'from_email': self.from_email_field.text().strip(),
            'from_name': {
                'enabled': self.from_name_enabled.isChecked(),
                'mode': self.from_name_mode.currentText(),
                'values': [line.strip() for line in self.from_names_field.toPlainText().split('\n') if line.strip()],
                'rotation': self.from_name_rotation.currentText()
            },
            'reply_to': {
                'enabled': self.reply_to_enabled.isChecked(),
                'mode': self.reply_to_mode.currentText(),
                'values': [line.strip() for line in self.reply_to_field.toPlainText().split('\n') if line.strip()]
            },
            'rate_limiting': {
                'enabled': self.rate_limiting_enabled.isChecked(),
                'per_minute': self.per_minute_field.value(),
                'hourly': self.hourly_field.value(),
                'daily': self.daily_field.value(),
                'total_limit': self.total_limit_field.value(),
                'usage': self.smtp_data.get('rate_limiting', {}).get('usage', {
                    'current_minute': 0,
                    'current_hour': 0,
                    'current_day': 0,
                    'total_sent': 0,
                    'last_reset': datetime.now().isoformat()
                })
            },
            'proxy': {
                'enabled': self.proxy_enabled.isChecked(),
                'type': self.proxy_type.currentText(),
                'host': self.proxy_host.text().strip(),
                'port': self.proxy_port.value(),
                'auth_enabled': self.proxy_auth.isChecked(),
                'username': self.proxy_username.text().strip(),
                'password': self.proxy_password.text()
            },
            'status': self.smtp_data.get('status', 'active'),
            'created': self.smtp_data.get('created', datetime.now().isoformat()),
            'modified': datetime.now().isoformat()
        }
        
    def validate_input(self) -> Tuple[bool, str]:
        """Validate input fields"""
        if not self.server_name_field.text().strip():
            return False, "Server name is required"
        if not self.host_field.text().strip():
            return False, "Host is required"
        if not self.username_field.text().strip():
            return False, "Username is required"
        if not self.password_field.text():
            return False, "Password is required"
        if not self.from_email_field.text().strip():
            return False, "From email is required"
        return True, ""
        
    def test_connection(self):
        """Test SMTP connection"""
        valid, message = self.validate_input()
        if not valid:
            QMessageBox.warning(self, "Validation Error", message)
            return
            
        # Get current configuration
        config = self.get_data()
        
        # Start test worker
        self.test_worker = SMTPTestWorker(config)
        self.test_worker.progress.connect(self.on_test_progress)
        self.test_worker.finished.connect(self.on_test_finished)
        
        # Disable test button
        self.test_btn.setEnabled(False)
        self.test_btn.setText("🔄 Testing...")
        
        self.test_worker.start()
        
    def on_test_progress(self, message):
        """Handle test progress"""
        self.test_btn.setText(f"🔄 {message}")
        
    def on_test_finished(self, success, message):
        """Handle test completion"""
        self.test_btn.setEnabled(True)
        self.test_btn.setText("🧪 Test Connection")
        
        if success:
            QMessageBox.information(self, "Test Successful", message)
        else:
            QMessageBox.critical(self, "Test Failed", message)
            
    def reset_usage_counters(self):
        """Reset usage counters"""
        reply = QMessageBox.question(
            self,
            "Reset Counters",
            "Are you sure you want to reset all usage counters?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            # This will be handled when saving the data
            QMessageBox.information(self, "Reset", "Usage counters will be reset when you save the configuration.")
            
    def accept(self):
        """Accept dialog with validation"""
        valid, message = self.validate_input()
        if not valid:
            QMessageBox.warning(self, "Validation Error", message)
            return
            
        super().accept()

class SMTPWidget(QWidget):
    """SMTP management widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.logger = logging.getLogger(__name__)
        self.data_manager = DataManager()
        
        # Current state
        self.current_page = 0
        self.items_per_page = 25
        self.smtp_servers = []
        self.filtered_servers = []
        
        self.setup_ui()
        self.refresh_servers()
        
        self.logger.info("SMTP widget initialized")
        
    def setup_ui(self):
        """Setup the SMTP UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Page title
        title_label = QLabel("📧 SMTP Server Management")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        """)
        main_layout.addWidget(title_label)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        # Search
        controls_layout.addWidget(QLabel("Search:"))
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Search servers...")
        self.search_field.textChanged.connect(self.filter_servers)
        controls_layout.addWidget(self.search_field)
        
        controls_layout.addStretch()
        
        # Server controls
        self.add_server_btn = QPushButton("➕ Add Server")
        self.add_server_btn.clicked.connect(self.add_server)
        controls_layout.addWidget(self.add_server_btn)
        
        self.edit_server_btn = QPushButton("✏️ Edit Server")
        self.edit_server_btn.clicked.connect(self.edit_server)
        self.edit_server_btn.setEnabled(False)
        controls_layout.addWidget(self.edit_server_btn)
        
        self.test_server_btn = QPushButton("🧪 Test Server")
        self.test_server_btn.clicked.connect(self.test_server)
        self.test_server_btn.setEnabled(False)
        controls_layout.addWidget(self.test_server_btn)
        
        self.delete_server_btn = QPushButton("🗑️ Delete Server")
        self.delete_server_btn.clicked.connect(self.delete_server)
        self.delete_server_btn.setEnabled(False)
        controls_layout.addWidget(self.delete_server_btn)
        
        main_layout.addLayout(controls_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        self.table.itemDoubleClicked.connect(self.edit_server)
        self.setup_table()
        main_layout.addWidget(self.table)
        
        # Statistics and pagination
        bottom_layout = QHBoxLayout()
        
        # Stats
        self.stats_label = QLabel("No servers")
        bottom_layout.addWidget(self.stats_label)
        
        bottom_layout.addStretch()
        
        # Pagination
        bottom_layout.addWidget(QLabel("Servers per page:"))
        self.items_per_page_combo = QComboBox()
        self.items_per_page_combo.addItems(["10", "25", "50", "100"])
        self.items_per_page_combo.setCurrentText("25")
        self.items_per_page_combo.currentTextChanged.connect(self.change_page_size)
        bottom_layout.addWidget(self.items_per_page_combo)
        
        self.prev_page_btn = QPushButton("◀ Previous")
        self.prev_page_btn.clicked.connect(self.previous_page)
        self.prev_page_btn.setEnabled(False)
        bottom_layout.addWidget(self.prev_page_btn)
        
        self.page_label = QLabel("Page 1 of 1")
        bottom_layout.addWidget(self.page_label)
        
        self.next_page_btn = QPushButton("Next ▶")
        self.next_page_btn.clicked.connect(self.next_page)
        self.next_page_btn.setEnabled(False)
        bottom_layout.addWidget(self.next_page_btn)
        
        main_layout.addLayout(bottom_layout)
        
    def setup_table(self):
        """Setup table structure"""
        headers = [
            "Server Name", "Description", "Host", "Port", "Username", 
            "From Email", "Status", "Added", "Last Modified"
        ]
        
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        
        # Resize columns
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(0, 150)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(1, 200)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(2, 150)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(3, 60)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(4, 150)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(5, 150)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.Fixed)
        header.resizeSection(6, 80)
        
    def refresh_servers(self):
        """Refresh SMTP servers list"""
        self.smtp_servers = self.data_manager.get_smtp_servers()
        self.filter_servers()
        
    def filter_servers(self):
        """Filter servers based on search text"""
        search_text = self.search_field.text().lower()
        
        if not search_text:
            self.filtered_servers = self.smtp_servers.copy()
        else:
            self.filtered_servers = []
            for server in self.smtp_servers:
                if (search_text in server.get('server_name', '').lower() or
                    search_text in server.get('host', '').lower() or
                    search_text in server.get('description', '').lower()):
                    self.filtered_servers.append(server)
                    
        self.current_page = 0
        self.update_table()
        self.update_pagination()
        self.update_stats()
        
    def update_table(self):
        """Update table with current page data"""
        if not self.filtered_servers:
            self.table.setRowCount(0)
            return
            
        # Calculate page bounds
        start_idx = self.current_page * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, len(self.filtered_servers))
        page_servers = self.filtered_servers[start_idx:end_idx]
        
        # Set table rows
        self.table.setRowCount(len(page_servers))
        
        # Populate table
        for row, server in enumerate(page_servers):
            self.table.setItem(row, 0, QTableWidgetItem(server.get('server_name', '')))
            self.table.setItem(row, 1, QTableWidgetItem(server.get('description', '')))
            self.table.setItem(row, 2, QTableWidgetItem(server.get('host', '')))
            self.table.setItem(row, 3, QTableWidgetItem(str(server.get('port', ''))))
            self.table.setItem(row, 4, QTableWidgetItem(server.get('username', '')))
            self.table.setItem(row, 5, QTableWidgetItem(server.get('from_email', '')))
            
            # Status with color
            status = server.get('status', 'active')
            status_item = QTableWidgetItem(status.title())
            if status == 'active':
                status_item.setBackground(QColor(200, 255, 200))  # Light green
            else:
                status_item.setBackground(QColor(255, 200, 200))  # Light red
            self.table.setItem(row, 6, status_item)
            
            # Dates
            created = server.get('created', '')
            if created:
                try:
                    created_dt = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    created_str = created_dt.strftime('%Y-%m-%d')
                except:
                    created_str = created[:10] if len(created) >= 10 else created
            else:
                created_str = 'Unknown'
            self.table.setItem(row, 7, QTableWidgetItem(created_str))
            
            modified = server.get('modified', '')
            if modified:
                try:
                    modified_dt = datetime.fromisoformat(modified.replace('Z', '+00:00'))
                    modified_str = modified_dt.strftime('%Y-%m-%d')
                except:
                    modified_str = modified[:10] if len(modified) >= 10 else modified
            else:
                modified_str = 'Unknown'
            self.table.setItem(row, 8, QTableWidgetItem(modified_str))
            
    def update_stats(self):
        """Update statistics display"""
        total = len(self.filtered_servers)
        active = sum(1 for s in self.filtered_servers if s.get('status') == 'active')
        inactive = total - active
        
        if self.search_field.text():
            stats_text = f"Showing: {format_number(total)} servers (filtered)"
        else:
            stats_text = f"Total: {format_number(total)} servers"
            
        stats_text += f" | Active: {format_number(active)} | Inactive: {format_number(inactive)}"
        self.stats_label.setText(stats_text)
        
    def update_pagination(self):
        """Update pagination controls"""
        if not self.filtered_servers:
            self.page_label.setText("Page 1 of 1")
            self.prev_page_btn.setEnabled(False)
            self.next_page_btn.setEnabled(False)
            return
            
        total_pages = max(1, (len(self.filtered_servers) + self.items_per_page - 1) // self.items_per_page)
        current_page_num = self.current_page + 1
        
        self.page_label.setText(f"Page {current_page_num} of {total_pages}")
        self.prev_page_btn.setEnabled(self.current_page > 0)
        self.next_page_btn.setEnabled(self.current_page < total_pages - 1)
        
    def previous_page(self):
        """Go to previous page"""
        if self.current_page > 0:
            self.current_page -= 1
            self.update_table()
            self.update_pagination()
            
    def next_page(self):
        """Go to next page"""
        total_pages = (len(self.filtered_servers) + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.update_table()
            self.update_pagination()
            
    def change_page_size(self, size_text):
        """Change items per page"""
        self.items_per_page = int(size_text)
        self.current_page = 0
        self.update_table()
        self.update_pagination()
        
    def on_selection_changed(self):
        """Handle table selection change"""
        selected = len(self.table.selectedItems()) > 0
        self.edit_server_btn.setEnabled(selected)
        self.test_server_btn.setEnabled(selected)
        self.delete_server_btn.setEnabled(selected)
        
    def get_selected_server(self) -> Optional[Dict[str, Any]]:
        """Get the currently selected server"""
        row = self.table.currentRow()
        if row < 0:
            return None
            
        global_row = self.current_page * self.items_per_page + row
        if global_row >= len(self.filtered_servers):
            return None
            
        return self.filtered_servers[global_row]
        
    def add_server(self):
        """Add a new SMTP server"""
        dialog = SMTPConfigDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            server_data = dialog.get_data()
            
            # Check if server name already exists
            existing_names = [s.get('server_name', '') for s in self.smtp_servers]
            if server_data['server_name'] in existing_names:
                QMessageBox.warning(self, "Error", f"Server '{server_data['server_name']}' already exists.")
                return
                
            # Save server
            success = self.data_manager.save_smtp_server(server_data)
            
            if success:
                self.refresh_servers()
                QMessageBox.information(self, "Success", f"Server '{server_data['server_name']}' added successfully.")
            else:
                QMessageBox.critical(self, "Error", "Failed to save SMTP server.")
                
    def edit_server(self):
        """Edit selected SMTP server"""
        server = self.get_selected_server()
        if not server:
            return
            
        dialog = SMTPConfigDialog(server, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            server_data = dialog.get_data()
            
            # Save server
            success = self.data_manager.save_smtp_server(server_data)
            
            if success:
                self.refresh_servers()
                QMessageBox.information(self, "Success", f"Server '{server_data['server_name']}' updated successfully.")
            else:
                QMessageBox.critical(self, "Error", "Failed to save SMTP server.")
                
    def test_server(self):
        """Test selected SMTP server"""
        server = self.get_selected_server()
        if not server:
            return
            
        # Start test worker
        self.test_worker = SMTPTestWorker(server)
        self.test_worker.progress.connect(self.on_test_progress)
        self.test_worker.finished.connect(self.on_test_finished)
        
        # Disable test button
        self.test_server_btn.setEnabled(False)
        self.test_server_btn.setText("🔄 Testing...")
        
        self.test_worker.start()
        
    def on_test_progress(self, message):
        """Handle test progress"""
        self.test_server_btn.setText(f"🔄 {message}")
        
    def on_test_finished(self, success, message):
        """Handle test completion"""
        self.test_server_btn.setEnabled(True)
        self.test_server_btn.setText("🧪 Test Server")
        
        if success:
            QMessageBox.information(self, "Test Successful", message)
        else:
            QMessageBox.critical(self, "Test Failed", message)
            
    def delete_server(self):
        """Delete selected SMTP server"""
        server = self.get_selected_server()
        if not server:
            return
            
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete the server '{server.get('server_name', '')}'?\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success = self.data_manager.delete_smtp_server(server.get('server_name', ''))
            
            if success:
                self.refresh_servers()
                QMessageBox.information(self, "Success", "SMTP server deleted successfully.")
            else:
                QMessageBox.critical(self, "Error", "Failed to delete SMTP server.")
        
    def refresh(self):
        """Refresh the module"""
        self.refresh_servers()
        
    def get_status_info(self):
        """Get status info"""
        total = len(self.smtp_servers)
        active = sum(1 for s in self.smtp_servers if s.get('status') == 'active')
        return f"SMTP - {format_number(total)} servers ({format_number(active)} active)"
        
    def cleanup(self):
        """Cleanup resources"""
        if hasattr(self, 'test_worker') and self.test_worker.isRunning():
            self.test_worker.terminate()
        self.logger.info("SMTP widget cleaned up")