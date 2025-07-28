"""
Campaign Management Widget for DeepMailer v1.0

This module provides comprehensive campaign management functionality including
multi-threading, real-time tracking, and advanced sending configurations.
"""

import logging
import json
import uuid
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QLineEdit,
    QSpinBox, QGroupBox, QMessageBox, QDialog, QDialogButtonBox,
    QTextEdit, QCheckBox, QProgressBar, QFrame, QSplitter, QListWidget,
    QListWidgetItem, QScrollArea, QTabWidget, QFormLayout, QPlainTextEdit,
    QDateTimeEdit, QSlider
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer, QDateTime
from PyQt6.QtGui import QFont, QColor

from modules.data_manager import DataManager
from core.utils import get_data_path, safe_filename, format_number

class CampaignConfigDialog(QDialog):
    """Dialog for configuring campaigns"""
    
    def __init__(self, campaign_data: Dict[str, Any] = None, parent=None):
        super().__init__(parent)
        self.campaign_data = campaign_data or {}
        self.data_manager = DataManager()
        self.setup_ui()
        if campaign_data:
            self.load_campaign_data()
            
    def setup_ui(self):
        """Setup the campaign configuration dialog"""
        self.setWindowTitle("Campaign Configuration")
        self.setModal(True)
        self.resize(900, 700)
        
        layout = QVBoxLayout(self)
        
        # Campaign name and description
        basic_layout = QHBoxLayout()
        basic_layout.addWidget(QLabel("Campaign Name:"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter campaign name")
        basic_layout.addWidget(self.name_input)
        layout.addLayout(basic_layout)
        
        desc_layout = QHBoxLayout()
        desc_layout.addWidget(QLabel("Description:"))
        self.description_input = QLineEdit()
        self.description_input.setPlaceholderText("Optional campaign description")
        desc_layout.addWidget(self.description_input)
        layout.addLayout(desc_layout)
        
        # Tab widget for configuration sections
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Setup tabs
        self.setup_leads_tab()
        self.setup_smtp_tab()
        self.setup_subjects_tab()
        self.setup_templates_tab()
        self.setup_sending_tab()
        self.setup_tracking_tab()
        
        # Buttons
        button_layout = QHBoxLayout()
        
        test_btn = QPushButton("Test Configuration")
        test_btn.clicked.connect(self.test_configuration)
        button_layout.addWidget(test_btn)
        
        button_layout.addStretch()
        
        save_btn = QPushButton("Save Campaign")
        save_btn.clicked.connect(self.save_campaign)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
    def setup_leads_tab(self):
        """Setup leads selection tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Lead list selection
        leads_group = QGroupBox("Lead List Selection")
        leads_layout = QVBoxLayout(leads_group)
        
        # Get available lead lists
        self.leads_combo = QComboBox()
        self.refresh_leads_list()
        leads_layout.addWidget(QLabel("Select Lead List:"))
        leads_layout.addWidget(self.leads_combo)
        
        # Sending sequence options
        sequence_group = QGroupBox("Sending Sequence")
        sequence_layout = QVBoxLayout(sequence_group)
        
        self.sequence_combo = QComboBox()
        self.sequence_combo.addItems([
            "First to Last",
            "Last to First", 
            "Random",
            "Domain Based"
        ])
        sequence_layout.addWidget(self.sequence_combo)
        
        # Domain settings (when domain based is selected)
        self.domain_settings = QWidget()
        domain_layout = QVBoxLayout(self.domain_settings)
        
        self.domain_rotation = QCheckBox("Enable Domain Rotation")
        domain_layout.addWidget(self.domain_rotation)
        
        self.domain_settings.setVisible(False)
        sequence_layout.addWidget(self.domain_settings)
        
        self.sequence_combo.currentTextChanged.connect(self.on_sequence_changed)
        
        layout.addWidget(leads_group)
        layout.addWidget(sequence_group)
        layout.addStretch()
        
        self.tab_widget.addTab(widget, "Leads")
        
    def setup_smtp_tab(self):
        """Setup SMTP configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # SMTP selection
        smtp_group = QGroupBox("SMTP Server Selection")
        smtp_layout = QVBoxLayout(smtp_group)
        
        # Get available SMTP servers
        self.smtp_list = QListWidget()
        self.smtp_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.refresh_smtp_list()
        smtp_layout.addWidget(QLabel("Select SMTP Servers (hold Ctrl for multiple):"))
        smtp_layout.addWidget(self.smtp_list)
        
        # SMTP rotation settings
        rotation_group = QGroupBox("SMTP Rotation")
        rotation_layout = QFormLayout(rotation_group)
        
        self.smtp_rotation = QComboBox()
        self.smtp_rotation.addItems(["Each Mail", "Custom Range"])
        rotation_layout.addRow("Rotation Mode:", self.smtp_rotation)
        
        self.smtp_range_min = QSpinBox()
        self.smtp_range_min.setRange(1, 1000)
        self.smtp_range_min.setValue(10)
        rotation_layout.addRow("Range Min:", self.smtp_range_min)
        
        self.smtp_range_max = QSpinBox()
        self.smtp_range_max.setRange(1, 1000)
        self.smtp_range_max.setValue(25)
        rotation_layout.addRow("Range Max:", self.smtp_range_max)
        
        layout.addWidget(smtp_group)
        layout.addWidget(rotation_group)
        layout.addStretch()
        
        self.tab_widget.addTab(widget, "SMTP")
        
    def setup_subjects_tab(self):
        """Setup subject lines configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Subject enable/disable
        self.subjects_enabled = QCheckBox("Enable Subject Lines")
        self.subjects_enabled.setChecked(True)
        layout.addWidget(self.subjects_enabled)
        
        # Subject selection
        subject_group = QGroupBox("Subject Lists Selection")
        subject_layout = QVBoxLayout(subject_group)
        
        self.subjects_list = QListWidget()
        self.subjects_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.refresh_subjects_list()
        subject_layout.addWidget(QLabel("Select Subject Lists (hold Ctrl for multiple):"))
        subject_layout.addWidget(self.subjects_list)
        
        # Subject rotation
        rotation_group = QGroupBox("Subject Rotation")
        rotation_layout = QFormLayout(rotation_group)
        
        self.subject_rotation = QComboBox()
        self.subject_rotation.addItems(["Each Time", "Custom Range"])
        rotation_layout.addRow("Rotation Mode:", self.subject_rotation)
        
        self.subject_range_min = QSpinBox()
        self.subject_range_min.setRange(1, 1000)
        self.subject_range_min.setValue(1)
        rotation_layout.addRow("Range Min:", self.subject_range_min)
        
        self.subject_range_max = QSpinBox()
        self.subject_range_max.setRange(1, 1000)
        self.subject_range_max.setValue(5)
        rotation_layout.addRow("Range Max:", self.subject_range_max)
        
        layout.addWidget(subject_group)
        layout.addWidget(rotation_group)
        layout.addStretch()
        
        self.tab_widget.addTab(widget, "Subjects")
        
    def setup_templates_tab(self):
        """Setup message templates configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Template selection
        template_group = QGroupBox("Message Templates Selection")
        template_layout = QVBoxLayout(template_group)
        
        self.templates_list = QListWidget()
        self.templates_list.setSelectionMode(QListWidget.SelectionMode.MultiSelection)
        self.refresh_templates_list()
        template_layout.addWidget(QLabel("Select Message Templates (hold Ctrl for multiple):"))
        template_layout.addWidget(self.templates_list)
        
        # Template rotation
        rotation_group = QGroupBox("Template Rotation")
        rotation_layout = QFormLayout(rotation_group)
        
        self.template_rotation = QComboBox()
        self.template_rotation.addItems(["Each Mail", "Custom Range"])
        rotation_layout.addRow("Rotation Mode:", self.template_rotation)
        
        self.template_range_min = QSpinBox()
        self.template_range_min.setRange(1, 1000)
        self.template_range_min.setValue(1)
        rotation_layout.addRow("Range Min:", self.template_range_min)
        
        self.template_range_max = QSpinBox()
        self.template_range_max.setRange(1, 1000)
        self.template_range_max.setValue(10)
        rotation_layout.addRow("Range Max:", self.template_range_max)
        
        layout.addWidget(template_group)
        layout.addWidget(rotation_group)
        layout.addStretch()
        
        self.tab_widget.addTab(widget, "Templates")
        
    def setup_sending_tab(self):
        """Setup sending mode configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Sending mode selection
        mode_group = QGroupBox("Sending Mode")
        mode_layout = QVBoxLayout(mode_group)
        
        self.sending_mode = QComboBox()
        self.sending_mode.addItems([
            "Single Mode (One-by-One)",
            "Batch Mode (Group Sending)",
            "Date & Time Mode (Scheduled)",
            "Spike Mode (Day-by-Day)"
        ])
        self.sending_mode.currentTextChanged.connect(self.on_sending_mode_changed)
        mode_layout.addWidget(self.sending_mode)
        
        # Mode-specific settings
        self.mode_settings = QWidget()
        self.mode_settings_layout = QVBoxLayout(self.mode_settings)
        mode_layout.addWidget(self.mode_settings)
        
        # Initialize with single mode
        self.setup_single_mode()
        
        # Scheduling
        schedule_group = QGroupBox("Campaign Scheduling")
        schedule_layout = QFormLayout(schedule_group)
        
        self.scheduling_enabled = QCheckBox("Enable Scheduling")
        schedule_layout.addRow("Scheduling:", self.scheduling_enabled)
        
        self.start_datetime = QDateTimeEdit()
        self.start_datetime.setDateTime(QDateTime.currentDateTime())
        schedule_layout.addRow("Start Date/Time:", self.start_datetime)
        
        layout.addWidget(mode_group)
        layout.addWidget(schedule_group)
        layout.addStretch()
        
        self.tab_widget.addTab(widget, "Sending")
        
    def setup_tracking_tab(self):
        """Setup tracking configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Tracking enable/disable
        self.tracking_enabled = QCheckBox("Enable Custom Tracking")
        layout.addWidget(self.tracking_enabled)
        
        # Tracking settings
        tracking_group = QGroupBox("Tracking Configuration")
        tracking_layout = QFormLayout(tracking_group)
        
        self.tracking_domain = QLineEdit()
        self.tracking_domain.setPlaceholderText("tracking.yourdomain.com")
        tracking_layout.addRow("Tracking Domain:", self.tracking_domain)
        
        self.tracking_api_key = QLineEdit()
        self.tracking_api_key.setPlaceholderText("API key for tracking database")
        tracking_layout.addRow("API Key:", self.tracking_api_key)
        
        # Open tracking
        open_group = QGroupBox("Email Open Tracking")
        open_layout = QVBoxLayout(open_group)
        
        self.open_tracking = QCheckBox("Track Email Opens")
        open_layout.addWidget(self.open_tracking)
        
        self.open_urls = QPlainTextEdit()
        self.open_urls.setPlaceholderText("https://domain.com/open?{{uuid}}&{{campaign}}\nhttps://domain2.com/open?{{uuid}}&{email}")
        self.open_urls.setMaximumHeight(100)
        open_layout.addWidget(QLabel("Open Tracking URLs (one per line):"))
        open_layout.addWidget(self.open_urls)
        
        # Click tracking
        click_group = QGroupBox("Email Click Tracking")
        click_layout = QVBoxLayout(click_group)
        
        self.click_tracking = QCheckBox("Track Email Clicks")
        click_layout.addWidget(self.click_tracking)
        
        self.click_mode = QComboBox()
        self.click_mode.addItems(["All Links", "Custom Selection"])
        click_layout.addWidget(QLabel("Track:"))
        click_layout.addWidget(self.click_mode)
        
        self.click_urls = QPlainTextEdit()
        self.click_urls.setPlaceholderText("https://domain.com/click?uid={{uuid}}&redirect={{ENCODED_URL}}\nhttps://domain2.com/click?uid={{uuid}}&email={EMAIL}&redirect={{ENCODED_URL}}")
        self.click_urls.setMaximumHeight(100)
        click_layout.addWidget(QLabel("Click Tracking URLs (one per line):"))
        click_layout.addWidget(self.click_urls)
        
        layout.addWidget(tracking_group)
        layout.addWidget(open_group)
        layout.addWidget(click_group)
        layout.addStretch()
        
        self.tab_widget.addTab(widget, "Tracking")
        
    def on_sequence_changed(self, sequence_type):
        """Handle sending sequence change"""
        self.domain_settings.setVisible(sequence_type == "Domain Based")
        
    def on_sending_mode_changed(self, mode):
        """Handle sending mode change"""
        # Clear current mode settings
        for i in reversed(range(self.mode_settings_layout.count())):
            child = self.mode_settings_layout.takeAt(i).widget()
            if child:
                child.deleteLater()
                
        # Setup new mode settings
        if mode.startswith("Single"):
            self.setup_single_mode()
        elif mode.startswith("Batch"):
            self.setup_batch_mode()
        elif mode.startswith("Date"):
            self.setup_datetime_mode()
        elif mode.startswith("Spike"):
            self.setup_spike_mode()
            
    def setup_single_mode(self):
        """Setup single mode settings"""
        group = QGroupBox("Single Mode Settings")
        layout = QFormLayout(group)
        
        self.single_delay_min = QSpinBox()
        self.single_delay_min.setRange(1, 3600)
        self.single_delay_min.setValue(10)
        layout.addRow("Min Delay (seconds):", self.single_delay_min)
        
        self.single_delay_max = QSpinBox()
        self.single_delay_max.setRange(1, 3600)
        self.single_delay_max.setValue(20)
        layout.addRow("Max Delay (seconds):", self.single_delay_max)
        
        self.mode_settings_layout.addWidget(group)
        
    def setup_batch_mode(self):
        """Setup batch mode settings"""
        group = QGroupBox("Batch Mode Settings")
        layout = QFormLayout(group)
        
        self.batch_size_min = QSpinBox()
        self.batch_size_min.setRange(1, 1000)
        self.batch_size_min.setValue(10)
        layout.addRow("Min Batch Size:", self.batch_size_min)
        
        self.batch_size_max = QSpinBox()
        self.batch_size_max.setRange(1, 1000)
        self.batch_size_max.setValue(20)
        layout.addRow("Max Batch Size:", self.batch_size_max)
        
        self.batch_delay_min = QSpinBox()
        self.batch_delay_min.setRange(1, 3600)
        self.batch_delay_min.setValue(300)
        layout.addRow("Min Batch Delay (seconds):", self.batch_delay_min)
        
        self.batch_delay_max = QSpinBox()
        self.batch_delay_max.setRange(1, 3600)
        self.batch_delay_max.setValue(600)
        layout.addRow("Max Batch Delay (seconds):", self.batch_delay_max)
        
        self.mode_settings_layout.addWidget(group)
        
    def setup_datetime_mode(self):
        """Setup date/time mode settings"""
        group = QGroupBox("Date & Time Mode Settings")
        layout = QFormLayout(group)
        
        self.dt_start = QDateTimeEdit()
        self.dt_start.setDateTime(QDateTime.currentDateTime())
        layout.addRow("Start Date/Time:", self.dt_start)
        
        self.dt_end = QDateTimeEdit()
        self.dt_end.setDateTime(QDateTime.currentDateTime().addDays(1))
        layout.addRow("End Date/Time:", self.dt_end)
        
        self.dt_limit = QSpinBox()
        self.dt_limit.setRange(1, 10000)
        self.dt_limit.setValue(100)
        layout.addRow("Email Limit:", self.dt_limit)
        
        self.mode_settings_layout.addWidget(group)
        
    def setup_spike_mode(self):
        """Setup spike mode settings"""
        group = QGroupBox("Spike Mode Settings")
        layout = QVBoxLayout(group)
        
        # Day planning
        days_layout = QHBoxLayout()
        
        self.spike_days = QSpinBox()
        self.spike_days.setRange(1, 30)
        self.spike_days.setValue(3)
        days_layout.addWidget(QLabel("Number of Days:"))
        days_layout.addWidget(self.spike_days)
        
        days_layout.addStretch()
        layout.addLayout(days_layout)
        
        # Daily limits
        self.daily_limits = QPlainTextEdit()
        self.daily_limits.setPlaceholderText("Day 1: 100 emails\nDay 2: 150 emails\nDay 3: 200 emails")
        self.daily_limits.setMaximumHeight(100)
        layout.addWidget(QLabel("Daily Email Limits:"))
        layout.addWidget(self.daily_limits)
        
        self.mode_settings_layout.addWidget(group)
        
    def refresh_leads_list(self):
        """Refresh the leads list dropdown"""
        try:
            leads_lists = self.data_manager.get_leads_lists()
            self.leads_combo.clear()
            for leads_list in leads_lists:
                self.leads_combo.addItem(f"{leads_list['name']} ({leads_list['row_count']} leads)")
        except Exception as e:
            logging.error(f"Failed to refresh leads lists: {e}")
            
    def refresh_smtp_list(self):
        """Refresh the SMTP servers list"""
        try:
            # Would get SMTP servers from data manager
            self.smtp_list.clear()
            smtp_servers = ["SMTP Server 1", "SMTP Server 2", "SMTP Server 3"]  # Placeholder
            for smtp in smtp_servers:
                self.smtp_list.addItem(smtp)
        except Exception as e:
            logging.error(f"Failed to refresh SMTP list: {e}")
            
    def refresh_subjects_list(self):
        """Refresh the subject lists"""
        try:
            # Would get subject lists from data manager
            self.subjects_list.clear()
            subject_lists = ["Subject List 1", "Subject List 2", "Subject List 3"]  # Placeholder
            for subject_list in subject_lists:
                self.subjects_list.addItem(subject_list)
        except Exception as e:
            logging.error(f"Failed to refresh subjects list: {e}")
            
    def refresh_templates_list(self):
        """Refresh the templates list"""
        try:
            # Would get templates from data manager
            self.templates_list.clear()
            templates = ["Template 1", "Template 2", "Template 3"]  # Placeholder
            for template in templates:
                self.templates_list.addItem(template)
        except Exception as e:
            logging.error(f"Failed to refresh templates list: {e}")
            
    def test_configuration(self):
        """Test the campaign configuration"""
        # Validate configuration
        errors = []
        
        if not self.name_input.text().strip():
            errors.append("Campaign name is required")
            
        if self.leads_combo.currentIndex() < 0:
            errors.append("Please select a lead list")
            
        if not self.smtp_list.selectedItems():
            errors.append("Please select at least one SMTP server")
            
        if self.subjects_enabled.isChecked() and not self.subjects_list.selectedItems():
            errors.append("Please select at least one subject list")
            
        if not self.templates_list.selectedItems():
            errors.append("Please select at least one message template")
            
        if errors:
            QMessageBox.warning(self, "Configuration Errors", 
                               "Please fix the following errors:\n\n" + "\n".join(f"• {error}" for error in errors))
        else:
            QMessageBox.information(self, "Configuration Test", "Campaign configuration is valid!")
            
    def save_campaign(self):
        """Save the campaign configuration"""
        campaign_name = self.name_input.text().strip()
        if not campaign_name:
            QMessageBox.warning(self, "Error", "Please enter a campaign name")
            return
            
        # Test configuration first
        self.test_configuration()
        
        # Create campaign data
        campaign_data = {
            'id': str(uuid.uuid4()),
            'name': campaign_name,
            'description': self.description_input.text().strip(),
            'created': datetime.now().isoformat(),
            'modified': datetime.now().isoformat(),
            'status': 'draft',
            'configuration': self.get_configuration()
        }
        
        # Save to file
        try:
            campaign_dir = get_data_path('campaigns') / safe_filename(campaign_name)
            campaign_dir.mkdir(exist_ok=True)
            
            config_file = campaign_dir / 'config.json'
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(campaign_data, f, indent=2)
                
            QMessageBox.information(self, "Success", f"Campaign '{campaign_name}' saved successfully!")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save campaign: {str(e)}")
            
    def get_configuration(self):
        """Get current configuration"""
        config = {
            'leads': {
                'list': self.leads_combo.currentText(),
                'sequence': self.sequence_combo.currentText(),
                'domain_rotation': self.domain_rotation.isChecked() if hasattr(self, 'domain_rotation') else False
            },
            'smtp': {
                'servers': [item.text() for item in self.smtp_list.selectedItems()],
                'rotation': self.smtp_rotation.currentText(),
                'range_min': self.smtp_range_min.value(),
                'range_max': self.smtp_range_max.value()
            },
            'subjects': {
                'enabled': self.subjects_enabled.isChecked(),
                'lists': [item.text() for item in self.subjects_list.selectedItems()],
                'rotation': self.subject_rotation.currentText(),
                'range_min': self.subject_range_min.value(),
                'range_max': self.subject_range_max.value()
            },
            'templates': {
                'lists': [item.text() for item in self.templates_list.selectedItems()],
                'rotation': self.template_rotation.currentText(),
                'range_min': self.template_range_min.value(),
                'range_max': self.template_range_max.value()
            },
            'sending': {
                'mode': self.sending_mode.currentText(),
                'scheduling_enabled': self.scheduling_enabled.isChecked(),
                'start_datetime': self.start_datetime.dateTime().toString()
            },
            'tracking': {
                'enabled': self.tracking_enabled.isChecked(),
                'domain': self.tracking_domain.text(),
                'api_key': self.tracking_api_key.text(),
                'open_tracking': self.open_tracking.isChecked(),
                'click_tracking': self.click_tracking.isChecked()
            }
        }
        
        return config
        
    def load_campaign_data(self):
        """Load existing campaign data"""
        # Implementation for loading existing campaign data
        pass

class CampaignsWidget(QWidget):
    """Campaign management widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.logger = logging.getLogger(__name__)
        self.data_manager = DataManager()
        self.campaigns = []
        self.setup_ui()
        self.refresh_campaigns()
        
    def setup_ui(self):
        """Setup the campaigns UI"""
        layout = QVBoxLayout(self)
        
        # Title and controls
        header_layout = QHBoxLayout()
        
        title = QLabel("🚀 Campaign Management")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Action buttons
        new_btn = QPushButton("New Campaign")
        new_btn.clicked.connect(self.create_campaign)
        header_layout.addWidget(new_btn)
        
        layout.addLayout(header_layout)
        
        # Campaigns table
        self.campaigns_table = QTableWidget()
        self.campaigns_table.setColumnCount(7)
        self.campaigns_table.setHorizontalHeaderLabels([
            "Campaign Name", "Status", "Progress", "Sent", "Failed", "Created", "Actions"
        ])
        
        # Configure table
        header = self.campaigns_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        
        self.campaigns_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.campaigns_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.campaigns_table)
        
        # Status bar
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
    def refresh_campaigns(self):
        """Refresh the campaigns list"""
        try:
            self.campaigns = self.get_campaigns()
            self.update_table()
            self.status_label.setText(f"Found {len(self.campaigns)} campaigns")
        except Exception as e:
            self.logger.error(f"Failed to refresh campaigns: {e}")
            self.status_label.setText("Error loading campaigns")
            
    def get_campaigns(self) -> List[Dict[str, Any]]:
        """Get all campaigns"""
        campaigns = []
        campaigns_dir = get_data_path('campaigns')
        
        if not campaigns_dir.exists():
            return campaigns
            
        for campaign_dir in campaigns_dir.iterdir():
            if campaign_dir.is_dir():
                config_file = campaign_dir / 'config.json'
                if config_file.exists():
                    try:
                        with open(config_file, 'r', encoding='utf-8') as f:
                            campaign_data = json.load(f)
                        campaigns.append(campaign_data)
                    except Exception as e:
                        self.logger.error(f"Failed to load campaign {campaign_dir}: {e}")
                        
        return campaigns
        
    def update_table(self):
        """Update the campaigns table"""
        self.campaigns_table.setRowCount(len(self.campaigns))
        
        for row, campaign in enumerate(self.campaigns):
            # Campaign name
            self.campaigns_table.setItem(row, 0, QTableWidgetItem(campaign.get('name', 'Unknown')))
            
            # Status
            status = campaign.get('status', 'draft')
            status_item = QTableWidgetItem(status.title())
            if status == 'running':
                status_item.setBackground(QColor(144, 238, 144))
            elif status == 'completed':
                status_item.setBackground(QColor(173, 216, 230))
            elif status == 'failed':
                status_item.setBackground(QColor(255, 182, 193))
            self.campaigns_table.setItem(row, 1, status_item)
            
            # Progress
            progress = campaign.get('progress', 0)
            self.campaigns_table.setItem(row, 2, QTableWidgetItem(f"{progress}%"))
            
            # Sent count
            sent = campaign.get('sent_count', 0)
            self.campaigns_table.setItem(row, 3, QTableWidgetItem(str(sent)))
            
            # Failed count
            failed = campaign.get('failed_count', 0)
            self.campaigns_table.setItem(row, 4, QTableWidgetItem(str(failed)))
            
            # Created date
            created = campaign.get('created', '')
            if 'T' in created:
                created = created.split('T')[0]
            self.campaigns_table.setItem(row, 5, QTableWidgetItem(created))
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 2, 5, 2)
            
            if status == 'draft':
                start_btn = QPushButton("Start")
                start_btn.clicked.connect(lambda checked, c=campaign: self.start_campaign(c))
                actions_layout.addWidget(start_btn)
            elif status == 'running':
                pause_btn = QPushButton("Pause")
                pause_btn.clicked.connect(lambda checked, c=campaign: self.pause_campaign(c))
                actions_layout.addWidget(pause_btn)
                
                stop_btn = QPushButton("Stop")
                stop_btn.clicked.connect(lambda checked, c=campaign: self.stop_campaign(c))
                actions_layout.addWidget(stop_btn)
            elif status == 'paused':
                resume_btn = QPushButton("Resume")
                resume_btn.clicked.connect(lambda checked, c=campaign: self.resume_campaign(c))
                actions_layout.addWidget(resume_btn)
                
                stop_btn = QPushButton("Stop")
                stop_btn.clicked.connect(lambda checked, c=campaign: self.stop_campaign(c))
                actions_layout.addWidget(stop_btn)
            
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, c=campaign: self.edit_campaign(c))
            actions_layout.addWidget(edit_btn)
            
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, c=campaign: self.delete_campaign(c))
            actions_layout.addWidget(delete_btn)
            
            self.campaigns_table.setCellWidget(row, 6, actions_widget)
            
    def create_campaign(self):
        """Create a new campaign"""
        dialog = CampaignConfigDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_campaigns()
            
    def edit_campaign(self, campaign: Dict[str, Any]):
        """Edit an existing campaign"""
        dialog = CampaignConfigDialog(campaign, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_campaigns()
            
    def start_campaign(self, campaign: Dict[str, Any]):
        """Start a campaign"""
        QMessageBox.information(self, "Start Campaign", 
                               f"Campaign '{campaign['name']}' will be started.\n\nThis feature will be fully implemented in the campaign engine.")
        
    def pause_campaign(self, campaign: Dict[str, Any]):
        """Pause a running campaign"""
        QMessageBox.information(self, "Pause Campaign", 
                               f"Campaign '{campaign['name']}' will be paused.")
        
    def resume_campaign(self, campaign: Dict[str, Any]):
        """Resume a paused campaign"""
        QMessageBox.information(self, "Resume Campaign", 
                               f"Campaign '{campaign['name']}' will be resumed.")
        
    def stop_campaign(self, campaign: Dict[str, Any]):
        """Stop a campaign"""
        reply = QMessageBox.question(
            self, "Stop Campaign",
            f"Are you sure you want to stop campaign '{campaign['name']}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            QMessageBox.information(self, "Stop Campaign", 
                                   f"Campaign '{campaign['name']}' will be stopped.")
        
    def delete_campaign(self, campaign: Dict[str, Any]):
        """Delete a campaign"""
        reply = QMessageBox.question(
            self, "Delete Campaign",
            f"Are you sure you want to delete campaign '{campaign['name']}'?\n\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                campaign_dir = get_data_path('campaigns') / safe_filename(campaign['name'])
                if campaign_dir.exists():
                    import shutil
                    shutil.rmtree(campaign_dir)
                    
                self.refresh_campaigns()
                QMessageBox.information(self, "Success", "Campaign deleted successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete campaign: {str(e)}")
        
    def refresh(self):
        """Refresh the module"""
        self.refresh_campaigns()
        
    def get_status_info(self):
        """Get status info"""
        running_count = sum(1 for c in self.campaigns if c.get('status') == 'running')
        return f"Campaigns: {len(self.campaigns)} total, {running_count} running"
        
    def cleanup(self):
        """Cleanup resources"""
        pass