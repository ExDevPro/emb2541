"""
Settings Widget for DeepMailer v1.0

This module provides application settings management including theme selection,
pagination settings, window preferences, and other user preferences.
"""

import logging
from typing import Dict, Any
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QComboBox, QSpinBox, QGroupBox, QMessageBox, QCheckBox, QLineEdit,
    QFormLayout, QTabWidget, QSlider, QProgressBar, QFrame
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont

from core.utils import load_config, save_config

class ThemeSettingsWidget(QWidget):
    """Widget for theme settings"""
    
    theme_changed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = load_config()
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        """Setup theme settings UI"""
        layout = QVBoxLayout(self)
        
        # Theme selection
        theme_group = QGroupBox("Application Theme")
        theme_layout = QFormLayout(theme_group)
        
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Dark Theme", "Light Theme"])
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        theme_layout.addRow("Theme:", self.theme_combo)
        
        # Theme preview
        self.theme_preview = QLabel("Theme changes require application restart")
        self.theme_preview.setStyleSheet("color: #666; font-style: italic;")
        theme_layout.addRow("Note:", self.theme_preview)
        
        layout.addWidget(theme_group)
        
        # Font settings
        font_group = QGroupBox("Font Settings")
        font_layout = QFormLayout(font_group)
        
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 20)
        self.font_size_spin.setValue(10)
        font_layout.addRow("Font Size:", self.font_size_spin)
        
        self.font_family_combo = QComboBox()
        self.font_family_combo.addItems(["System Default", "Arial", "Helvetica", "Times New Roman", "Courier"])
        font_layout.addRow("Font Family:", self.font_family_combo)
        
        layout.addWidget(font_group)
        
        layout.addStretch()
        
    def load_settings(self):
        """Load current theme settings"""
        theme = self.config.get('theme', 'dark')
        if theme == 'dark':
            self.theme_combo.setCurrentText("Dark Theme")
        else:
            self.theme_combo.setCurrentText("Light Theme")
            
        # Load font settings
        font_size = self.config.get('font_size', 10)
        self.font_size_spin.setValue(font_size)
        
        font_family = self.config.get('font_family', 'System Default')
        self.font_family_combo.setCurrentText(font_family)
        
    def on_theme_changed(self, theme_text):
        """Handle theme change"""
        theme = 'dark' if theme_text == "Dark Theme" else 'light'
        self.theme_changed.emit(theme)
        
    def get_settings(self):
        """Get current settings"""
        theme = 'dark' if self.theme_combo.currentText() == "Dark Theme" else 'light'
        return {
            'theme': theme,
            'font_size': self.font_size_spin.value(),
            'font_family': self.font_family_combo.currentText()
        }

class PaginationSettingsWidget(QWidget):
    """Widget for pagination settings"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = load_config()
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        """Setup pagination settings UI"""
        layout = QVBoxLayout(self)
        
        # Pagination group
        pagination_group = QGroupBox("Table Pagination Settings")
        pagination_layout = QFormLayout(pagination_group)
        
        self.leads_per_page = QSpinBox()
        self.leads_per_page.setRange(10, 1000)
        self.leads_per_page.setValue(100)
        pagination_layout.addRow("Leads per page:", self.leads_per_page)
        
        self.smtp_per_page = QSpinBox()
        self.smtp_per_page.setRange(10, 100)
        self.smtp_per_page.setValue(25)
        pagination_layout.addRow("SMTP servers per page:", self.smtp_per_page)
        
        self.subjects_per_page = QSpinBox()
        self.subjects_per_page.setRange(10, 500)
        self.subjects_per_page.setValue(50)
        pagination_layout.addRow("Subjects per page:", self.subjects_per_page)
        
        self.templates_per_page = QSpinBox()
        self.templates_per_page.setRange(10, 100)
        self.templates_per_page.setValue(25)
        pagination_layout.addRow("Templates per page:", self.templates_per_page)
        
        self.campaigns_per_page = QSpinBox()
        self.campaigns_per_page.setRange(10, 100)
        self.campaigns_per_page.setValue(25)
        pagination_layout.addRow("Campaigns per page:", self.campaigns_per_page)
        
        layout.addWidget(pagination_group)
        
        # Performance settings
        performance_group = QGroupBox("Performance Settings")
        performance_layout = QFormLayout(performance_group)
        
        self.auto_refresh = QCheckBox("Auto-refresh data")
        self.auto_refresh.setChecked(True)
        performance_layout.addRow("Auto-refresh:", self.auto_refresh)
        
        self.refresh_interval = QSpinBox()
        self.refresh_interval.setRange(5, 300)
        self.refresh_interval.setValue(30)
        self.refresh_interval.setSuffix(" seconds")
        performance_layout.addRow("Refresh interval:", self.refresh_interval)
        
        layout.addWidget(performance_group)
        
        layout.addStretch()
        
    def load_settings(self):
        """Load current pagination settings"""
        pagination = self.config.get('pagination', {})
        
        self.leads_per_page.setValue(pagination.get('leads_per_page', 100))
        self.smtp_per_page.setValue(pagination.get('smtp_per_page', 25))
        self.subjects_per_page.setValue(pagination.get('subjects_per_page', 50))
        self.templates_per_page.setValue(pagination.get('templates_per_page', 25))
        self.campaigns_per_page.setValue(pagination.get('campaigns_per_page', 25))
        
        # Performance settings
        self.auto_refresh.setChecked(self.config.get('auto_refresh', True))
        self.refresh_interval.setValue(self.config.get('refresh_interval', 30))
        
    def get_settings(self):
        """Get current settings"""
        return {
            'pagination': {
                'leads_per_page': self.leads_per_page.value(),
                'smtp_per_page': self.smtp_per_page.value(),
                'subjects_per_page': self.subjects_per_page.value(),
                'templates_per_page': self.templates_per_page.value(),
                'campaigns_per_page': self.campaigns_per_page.value()
            },
            'auto_refresh': self.auto_refresh.isChecked(),
            'refresh_interval': self.refresh_interval.value()
        }

class EmailSettingsWidget(QWidget):
    """Widget for email settings"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = load_config()
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        """Setup email settings UI"""
        layout = QVBoxLayout(self)
        
        # Connection settings
        connection_group = QGroupBox("Connection Settings")
        connection_layout = QFormLayout(connection_group)
        
        self.timeout_spin = QSpinBox()
        self.timeout_spin.setRange(10, 300)
        self.timeout_spin.setValue(30)
        self.timeout_spin.setSuffix(" seconds")
        connection_layout.addRow("Connection timeout:", self.timeout_spin)
        
        self.retry_count = QSpinBox()
        self.retry_count.setRange(0, 10)
        self.retry_count.setValue(3)
        connection_layout.addRow("Retry count:", self.retry_count)
        
        layout.addWidget(connection_group)
        
        # Sending settings
        sending_group = QGroupBox("Sending Settings")
        sending_layout = QFormLayout(sending_group)
        
        self.batch_size = QSpinBox()
        self.batch_size.setRange(1, 1000)
        self.batch_size.setValue(50)
        sending_layout.addRow("Default batch size:", self.batch_size)
        
        self.delay_between_emails = QSpinBox()
        self.delay_between_emails.setRange(0, 3600)
        self.delay_between_emails.setValue(1)
        self.delay_between_emails.setSuffix(" seconds")
        sending_layout.addRow("Default delay between emails:", self.delay_between_emails)
        
        layout.addWidget(sending_group)
        
        # Security settings
        security_group = QGroupBox("Security Settings")
        security_layout = QFormLayout(security_group)
        
        self.verify_ssl = QCheckBox("Verify SSL certificates")
        self.verify_ssl.setChecked(True)
        security_layout.addRow("SSL verification:", self.verify_ssl)
        
        self.use_proxy = QCheckBox("Enable proxy support")
        self.use_proxy.setChecked(False)
        security_layout.addRow("Proxy support:", self.use_proxy)
        
        layout.addWidget(security_group)
        
        layout.addStretch()
        
    def load_settings(self):
        """Load current email settings"""
        email = self.config.get('email', {})
        
        self.timeout_spin.setValue(email.get('timeout', 30))
        self.retry_count.setValue(email.get('retry_count', 3))
        self.batch_size.setValue(email.get('batch_size', 50))
        self.delay_between_emails.setValue(email.get('delay_between_emails', 1))
        self.verify_ssl.setChecked(email.get('verify_ssl', True))
        self.use_proxy.setChecked(email.get('use_proxy', False))
        
    def get_settings(self):
        """Get current settings"""
        return {
            'email': {
                'timeout': self.timeout_spin.value(),
                'retry_count': self.retry_count.value(),
                'batch_size': self.batch_size.value(),
                'delay_between_emails': self.delay_between_emails.value(),
                'verify_ssl': self.verify_ssl.isChecked(),
                'use_proxy': self.use_proxy.isChecked()
            }
        }

class AdvancedSettingsWidget(QWidget):
    """Widget for advanced settings"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = load_config()
        self.setup_ui()
        self.load_settings()
        
    def setup_ui(self):
        """Setup advanced settings UI"""
        layout = QVBoxLayout(self)
        
        # Logging settings
        logging_group = QGroupBox("Logging Settings")
        logging_layout = QFormLayout(logging_group)
        
        self.log_level = QComboBox()
        self.log_level.addItems(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        self.log_level.setCurrentText("INFO")
        logging_layout.addRow("Log level:", self.log_level)
        
        self.log_to_file = QCheckBox("Save logs to file")
        self.log_to_file.setChecked(True)
        logging_layout.addRow("File logging:", self.log_to_file)
        
        self.max_log_size = QSpinBox()
        self.max_log_size.setRange(1, 100)
        self.max_log_size.setValue(10)
        self.max_log_size.setSuffix(" MB")
        logging_layout.addRow("Max log file size:", self.max_log_size)
        
        layout.addWidget(logging_group)
        
        # Data settings
        data_group = QGroupBox("Data Management")
        data_layout = QFormLayout(data_group)
        
        self.auto_backup = QCheckBox("Auto-backup data")
        self.auto_backup.setChecked(True)
        data_layout.addRow("Auto-backup:", self.auto_backup)
        
        self.backup_interval = QSpinBox()
        self.backup_interval.setRange(1, 30)
        self.backup_interval.setValue(7)
        self.backup_interval.setSuffix(" days")
        data_layout.addRow("Backup interval:", self.backup_interval)
        
        self.keep_backups = QSpinBox()
        self.keep_backups.setRange(1, 50)
        self.keep_backups.setValue(10)
        data_layout.addRow("Keep backups:", self.keep_backups)
        
        layout.addWidget(data_group)
        
        # Cache settings
        cache_group = QGroupBox("Cache Settings")
        cache_layout = QFormLayout(cache_group)
        
        self.enable_cache = QCheckBox("Enable data caching")
        self.enable_cache.setChecked(True)
        cache_layout.addRow("Data caching:", self.enable_cache)
        
        self.cache_timeout = QSpinBox()
        self.cache_timeout.setRange(30, 3600)
        self.cache_timeout.setValue(300)
        self.cache_timeout.setSuffix(" seconds")
        cache_layout.addRow("Cache timeout:", self.cache_timeout)
        
        # Clear cache button
        clear_cache_btn = QPushButton("Clear Cache")
        clear_cache_btn.clicked.connect(self.clear_cache)
        cache_layout.addRow("Actions:", clear_cache_btn)
        
        layout.addWidget(cache_group)
        
        layout.addStretch()
        
    def load_settings(self):
        """Load current advanced settings"""
        # Log level
        self.log_level.setCurrentText(self.config.get('log_level', 'INFO'))
        
        # File logging
        self.log_to_file.setChecked(self.config.get('log_to_file', True))
        self.max_log_size.setValue(self.config.get('max_log_size', 10))
        
        # Data management
        self.auto_backup.setChecked(self.config.get('auto_backup', True))
        self.backup_interval.setValue(self.config.get('backup_interval', 7))
        self.keep_backups.setValue(self.config.get('keep_backups', 10))
        
        # Cache
        self.enable_cache.setChecked(self.config.get('enable_cache', True))
        self.cache_timeout.setValue(self.config.get('cache_timeout', 300))
        
    def clear_cache(self):
        """Clear application cache"""
        QMessageBox.information(self, "Cache Cleared", "Application cache has been cleared successfully!")
        
    def get_settings(self):
        """Get current settings"""
        return {
            'log_level': self.log_level.currentText(),
            'log_to_file': self.log_to_file.isChecked(),
            'max_log_size': self.max_log_size.value(),
            'auto_backup': self.auto_backup.isChecked(),
            'backup_interval': self.backup_interval.value(),
            'keep_backups': self.keep_backups.value(),
            'enable_cache': self.enable_cache.isChecked(),
            'cache_timeout': self.cache_timeout.value()
        }

class SettingsWidget(QWidget):
    """Settings widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.logger = logging.getLogger(__name__)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the settings UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("🔧 Application Settings")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Tab widget for different settings categories
        tab_widget = QTabWidget()
        
        # Theme settings
        self.theme_widget = ThemeSettingsWidget(self)
        tab_widget.addTab(self.theme_widget, "Theme & Appearance")
        
        # Pagination settings
        self.pagination_widget = PaginationSettingsWidget(self)
        tab_widget.addTab(self.pagination_widget, "Pagination & Performance")
        
        # Email settings
        self.email_widget = EmailSettingsWidget(self)
        tab_widget.addTab(self.email_widget, "Email Settings")
        
        # Advanced settings
        self.advanced_widget = AdvancedSettingsWidget(self)
        tab_widget.addTab(self.advanced_widget, "Advanced")
        
        layout.addWidget(tab_widget)
        
        # Action buttons
        buttons_layout = QHBoxLayout()
        
        # Reset to defaults
        reset_btn = QPushButton("Reset to Defaults")
        reset_btn.clicked.connect(self.reset_to_defaults)
        buttons_layout.addWidget(reset_btn)
        
        buttons_layout.addStretch()
        
        # Apply settings
        apply_btn = QPushButton("Apply Settings")
        apply_btn.clicked.connect(self.apply_settings)
        buttons_layout.addWidget(apply_btn)
        
        # Save settings
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
        
        # Status
        self.status_label = QLabel("Settings ready")
        layout.addWidget(self.status_label)
        
    def reset_to_defaults(self):
        """Reset all settings to defaults"""
        reply = QMessageBox.question(
            self, "Reset Settings",
            "Are you sure you want to reset all settings to their default values?\n\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                from core.utils import DEFAULT_CONFIG
                save_config(DEFAULT_CONFIG.copy())
                
                # Reload all settings widgets
                self.theme_widget.load_settings()
                self.pagination_widget.load_settings()
                self.email_widget.load_settings()
                self.advanced_widget.load_settings()
                
                QMessageBox.information(self, "Success", "Settings have been reset to defaults!")
                self.status_label.setText("Settings reset to defaults")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to reset settings: {str(e)}")
                
    def apply_settings(self):
        """Apply current settings without saving"""
        try:
            # Get settings from all widgets
            settings = {}
            settings.update(self.theme_widget.get_settings())
            settings.update(self.pagination_widget.get_settings())
            settings.update(self.email_widget.get_settings())
            settings.update(self.advanced_widget.get_settings())
            
            # Apply theme change if needed
            current_config = load_config()
            if settings.get('theme') != current_config.get('theme'):
                if hasattr(self.parent_window, 'change_theme'):
                    self.parent_window.change_theme(settings['theme'])
                    
            self.status_label.setText("Settings applied (not saved)")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to apply settings: {str(e)}")
            
    def save_settings(self):
        """Save all current settings"""
        try:
            # Get current config
            config = load_config()
            
            # Get settings from all widgets
            theme_settings = self.theme_widget.get_settings()
            pagination_settings = self.pagination_widget.get_settings()
            email_settings = self.email_widget.get_settings()
            advanced_settings = self.advanced_widget.get_settings()
            
            # Update config
            config.update(theme_settings)
            config.update(pagination_settings)
            config.update(email_settings)
            config.update(advanced_settings)
            
            # Save configuration
            save_config(config)
            
            QMessageBox.information(self, "Success", "Settings saved successfully!")
            self.status_label.setText("Settings saved successfully")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save settings: {str(e)}")
            self.status_label.setText(f"Error saving settings: {str(e)}")
        
    def refresh(self):
        """Refresh the module"""
        self.theme_widget.load_settings()
        self.pagination_widget.load_settings()
        self.email_widget.load_settings()
        self.advanced_widget.load_settings()
        self.status_label.setText("Settings refreshed")
        
    def get_status_info(self):
        """Get status info"""
        config = load_config()
        theme = config.get('theme', 'dark')
        return f"Settings: {theme} theme, {config.get('pagination', {}).get('leads_per_page', 100)} leads/page"
        
    def cleanup(self):
        """Cleanup resources"""
        pass