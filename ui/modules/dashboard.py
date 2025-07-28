"""
Dashboard Widget for DeepMailer v1.0

This module provides the main dashboard interface with real-time statistics,
counters, and overview information for the email marketing application.
Default landing page automatically selected when application opens.
"""

import logging
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QFrame,
    QProgressBar, QPushButton, QGroupBox, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QFont, QPalette

from core.utils import get_data_path, format_number
from modules.data_manager import DataManager

class StatCard(QFrame):
    """Statistics card widget for displaying counters"""
    
    def __init__(self, title: str, value: str = "0", icon: str = "📊"):
        super().__init__()
        self.title = title
        self.icon = icon
        self.setup_ui()
        self.set_value(value)
        
    def setup_ui(self):
        """Setup the card UI"""
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        self.setObjectName("stat-card")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Icon and title
        title_layout = QHBoxLayout()
        
        icon_label = QLabel(self.icon)
        icon_label.setObjectName("stat-icon")
        title_layout.addWidget(icon_label)
        
        title_label = QLabel(self.title)
        title_label.setObjectName("stat-title")
        title_layout.addWidget(title_label)
        title_layout.addStretch()
        
        layout.addLayout(title_layout)
        
        # Value
        self.value_label = QLabel("0")
        self.value_label.setObjectName("stat-value")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.value_label)
        
    def set_value(self, value: str):
        """Set the card value"""
        self.value_label.setText(str(value))

class DashboardWidget(QWidget):
    """Main dashboard widget"""
    
    # Signals
    navigation_requested = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.logger = logging.getLogger(__name__)
        self.data_manager = DataManager()
        
        self.setup_ui()
        self.setup_timer()
        self.refresh_data()
        
        self.logger.info("Dashboard widget initialized")
        
    def setup_ui(self):
        """Setup the dashboard UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Page title
        title_label = QLabel("Dashboard - Overview & Statistics")
        title_label.setObjectName("page-title")
        main_layout.addWidget(title_label)
        
        # Create scroll area for content
        scroll_area = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Data counters section
        self.setup_data_counters(scroll_layout)
        
        # Campaign statistics section
        self.setup_campaign_stats(scroll_layout)
        
        # System status section
        self.setup_system_status(scroll_layout)
        
        # Quick navigation section
        self.setup_quick_navigation(scroll_layout)
        
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)
        
    def setup_data_counters(self, layout):
        """Setup data counters section"""
        group = QGroupBox("Data Overview")
        
        grid_layout = QGridLayout(group)
        grid_layout.setSpacing(15)
        
        # Create stat cards
        self.leads_card = StatCard("Total Leads", "0", "👥")
        self.subjects_card = StatCard("Total Subjects", "0", "📝") 
        self.smtp_card = StatCard("SMTP Servers", "0", "📧")
        self.templates_card = StatCard("Message Templates", "0", "💬")
        
        # Add cards to grid
        grid_layout.addWidget(self.leads_card, 0, 0)
        grid_layout.addWidget(self.subjects_card, 0, 1)
        grid_layout.addWidget(self.smtp_card, 1, 0)
        grid_layout.addWidget(self.templates_card, 1, 1)
        
        layout.addWidget(group)
        
    def setup_campaign_stats(self, layout):
        """Setup campaign statistics section"""
        group = QGroupBox("Campaign Statistics")
        
        grid_layout = QGridLayout(group)
        grid_layout.setSpacing(15)
        
        # Campaign stat cards
        self.active_campaigns_card = StatCard("Active Campaigns", "0", "🚀")
        self.emails_sent_card = StatCard("Emails Sent", "0", "✅")
        self.emails_failed_card = StatCard("Failed Emails", "0", "❌")
        self.emails_remaining_card = StatCard("Remaining Queue", "0", "⏳")
        
        # Tracking stats (when enabled)
        self.opens_card = StatCard("Total Opens", "Off", "👁️")
        self.clicks_card = StatCard("Total Clicks", "Off", "🖱️")
        
        # Add to grid
        grid_layout.addWidget(self.active_campaigns_card, 0, 0)
        grid_layout.addWidget(self.emails_sent_card, 0, 1)
        grid_layout.addWidget(self.emails_failed_card, 0, 2)
        grid_layout.addWidget(self.emails_remaining_card, 1, 0)
        grid_layout.addWidget(self.opens_card, 1, 1)
        grid_layout.addWidget(self.clicks_card, 1, 2)
        
        layout.addWidget(group)
        
    def setup_system_status(self, layout):
        """Setup system status section"""
        group = QGroupBox("System Status")
        group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                left: 10px;
                top: -10px;
            }
        """)
        
        grid_layout = QGridLayout(group)
        grid_layout.setSpacing(15)
        
        # System status cards
        self.app_status_card = StatCard("Application Status", "Running", "⚡")
        self.memory_card = StatCard("Memory Usage", "Normal", "💾")
        self.threads_card = StatCard("Active Threads", "0", "⚙️")
        self.errors_card = StatCard("Recent Errors", "0", "⚠️")
        
        # Add to grid
        grid_layout.addWidget(self.app_status_card, 0, 0)
        grid_layout.addWidget(self.memory_card, 0, 1)
        grid_layout.addWidget(self.threads_card, 1, 0)
        grid_layout.addWidget(self.errors_card, 1, 1)
        
        layout.addWidget(group)
        
    def setup_quick_navigation(self, layout):
        """Setup quick navigation section"""
        group = QGroupBox("Quick Actions")
        group.setStyleSheet("""
            QGroupBox {
                font-size: 16px;
                font-weight: bold;
                color: #333;
                margin-top: 10px;
                padding-top: 10px;
            }
            QGroupBox::title {
                left: 10px;
                top: -10px;
            }
        """)
        
        button_layout = QHBoxLayout(group)
        button_layout.setSpacing(15)
        
        # Quick action buttons
        buttons = [
            ("Import Leads", "leads", "👥"),
            ("Add SMTP", "smtps", "📧"),
            ("Create Template", "messages", "💬"),
            ("New Campaign", "campaigns", "🚀"),
            ("View Settings", "settings", "⚙️")
        ]
        
        for text, module, icon in buttons:
            btn = QPushButton(f"{icon} {text}")
            btn.setStyleSheet("""
                QPushButton {
                    padding: 10px 20px;
                    font-size: 14px;
                    border: 2px solid #2196F3;
                    border-radius: 5px;
                    background-color: white;
                    color: #2196F3;
                }
                QPushButton:hover {
                    background-color: #2196F3;
                    color: white;
                }
                QPushButton:pressed {
                    background-color: #1976D2;
                }
            """)
            btn.clicked.connect(lambda checked, m=module: self.navigate_to_module(m))
            button_layout.addWidget(btn)
            
        button_layout.addStretch()
        layout.addWidget(group)
        
    def setup_timer(self):
        """Setup refresh timer"""
        self.refresh_timer = QTimer()
        self.refresh_timer.timeout.connect(self.refresh_data)
        self.refresh_timer.start(5000)  # Refresh every 5 seconds
        
    def refresh_data(self):
        """Refresh dashboard data"""
        try:
            # Get data counts
            leads_count = self.data_manager.get_total_leads()
            subjects_count = self.data_manager.get_total_subjects()
            smtp_count = self.data_manager.get_total_smtp_servers()
            templates_count = self.data_manager.get_total_templates()
            
            # Update data counter cards
            self.leads_card.set_value(format_number(leads_count))
            self.subjects_card.set_value(format_number(subjects_count))
            self.smtp_card.set_value(format_number(smtp_count))
            self.templates_card.set_value(format_number(templates_count))
            
            # Get campaign statistics
            campaign_stats = self.data_manager.get_campaign_statistics()
            
            self.active_campaigns_card.set_value(format_number(campaign_stats.get('active', 0)))
            self.emails_sent_card.set_value(format_number(campaign_stats.get('sent', 0)))
            self.emails_failed_card.set_value(format_number(campaign_stats.get('failed', 0)))
            self.emails_remaining_card.set_value(format_number(campaign_stats.get('remaining', 0)))
            
            # Update tracking stats if enabled
            tracking_stats = self.data_manager.get_tracking_statistics()
            if tracking_stats.get('enabled', False):
                self.opens_card.set_value(format_number(tracking_stats.get('opens', 0)))
                self.clicks_card.set_value(format_number(tracking_stats.get('clicks', 0)))
            else:
                self.opens_card.set_value("Off")
                self.clicks_card.set_value("Off")
                
            # Update system status
            system_stats = self.data_manager.get_system_statistics()
            self.memory_card.set_value(system_stats.get('memory', 'Normal'))
            self.threads_card.set_value(format_number(system_stats.get('threads', 0)))
            self.errors_card.set_value(format_number(system_stats.get('errors', 0)))
            
            self.logger.debug("Dashboard data refreshed")
            
        except Exception as e:
            self.logger.error(f"Error refreshing dashboard data: {e}")
            
    def navigate_to_module(self, module_name):
        """Navigate to a specific module"""
        if self.parent_window:
            # Find the navigation item and select it
            nav_list = self.parent_window.navigation_list
            for i in range(nav_list.count()):
                item = nav_list.item(i)
                if item.data(Qt.ItemDataRole.UserRole) == module_name:
                    nav_list.setCurrentRow(i)
                    break
                    
    def get_status_info(self):
        """Get status information for the status bar"""
        try:
            leads_count = self.data_manager.get_total_leads()
            active_campaigns = self.data_manager.get_campaign_statistics().get('active', 0)
            return f"Dashboard - {format_number(leads_count)} leads, {active_campaigns} active campaigns"
        except Exception:
            return "Dashboard - Ready"
            
    def refresh(self):
        """Refresh the dashboard (called when module is activated)"""
        self.refresh_data()
        
    def cleanup(self):
        """Cleanup resources"""
        if hasattr(self, 'refresh_timer'):
            self.refresh_timer.stop()
        self.logger.info("Dashboard widget cleaned up")