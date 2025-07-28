"""
Main Window for DeepMailer v1.0

This module contains the main application window with left panel navigation
and dynamic right panel content. The window manages all major application
components and provides the primary user interface.
"""

import logging
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QSplitter,
    QListWidget, QListWidgetItem, QStackedWidget, QLabel, QFrame,
    QStatusBar, QMenuBar, QMessageBox, QApplication
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QIcon, QFont, QPixmap, QAction

from core.utils import load_config, save_config, get_resource_path
from ui.modules.dashboard import DashboardWidget
from ui.modules.leads import LeadsWidget  
from ui.modules.smtp import SMTPWidget
from ui.modules.subjects import SubjectsWidget
from ui.modules.messages import MessagesWidget
from ui.modules.campaigns import CampaignsWidget
from ui.modules.configurations import ConfigurationsWidget
from ui.modules.settings import SettingsWidget

class MainWindow(QMainWindow):
    """Main application window"""
    
    # Signals
    theme_changed = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.config = load_config()
        self.modules = {}
        self.logger = logging.getLogger(__name__)
        
        self.init_ui()
        self.setup_window()
        self.setup_connections()
        self.setup_status_updates()
        
        # Select dashboard by default
        self.navigation_list.setCurrentRow(0)
        self.on_navigation_changed(0)
        
        self.logger.info("Main window initialized successfully")
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("DeepMailer v1.0 - Professional Email Marketing Software")
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Create left panel (navigation)
        self.setup_left_panel(splitter)
        
        # Create right panel (content)
        self.setup_right_panel(splitter)
        
        # Set splitter proportions (20% left, 80% right)
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setSizes([250, 950])
        
        # Setup menu bar
        self.setup_menu_bar()
        
        # Setup status bar
        self.setup_status_bar()
        
    def setup_left_panel(self, parent):
        """Setup the left navigation panel"""
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(5, 5, 5, 5)
        
        # Application title/logo
        title_label = QLabel("DeepMailer v1.0")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("""
            QLabel {
                font-size: 16px;
                font-weight: bold;
                color: #2196F3;
                padding: 10px;
                border-bottom: 2px solid #2196F3;
                margin-bottom: 10px;
            }
        """)
        left_layout.addWidget(title_label)
        
        # Navigation list
        self.navigation_list = QListWidget()
        self.navigation_list.setMaximumWidth(240)
        self.navigation_list.setMinimumWidth(200)
        
        # Add navigation items
        nav_items = [
            ("Dashboard", "📊"),
            ("Leads", "👥"),
            ("SMTPs", "📧"),
            ("Subjects", "📝"),
            ("Messages", "💬"),
            ("Campaigns", "🚀"),
            ("Configurations", "⚙️"),
            ("Settings", "🔧")
        ]
        
        for name, icon in nav_items:
            item = QListWidgetItem(f"{icon} {name}")
            item.setData(Qt.ItemDataRole.UserRole, name.lower())
            self.navigation_list.addItem(item)
        
        # Style the navigation list
        self.navigation_list.setStyleSheet("""
            QListWidget {
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f8f9fa;
                selection-background-color: #2196F3;
                selection-color: white;
                font-size: 14px;
            }
            QListWidget::item {
                padding: 12px;
                border-bottom: 1px solid #eee;
            }
            QListWidget::item:selected {
                background-color: #2196F3;
                color: white;
                font-weight: bold;
            }
            QListWidget::item:hover {
                background-color: #e3f2fd;
            }
        """)
        
        left_layout.addWidget(self.navigation_list)
        left_layout.addStretch()
        
        parent.addWidget(left_widget)
        
    def setup_right_panel(self, parent):
        """Setup the right content panel"""
        # Create stacked widget for different modules
        self.content_stack = QStackedWidget()
        
        # Initialize all modules
        self.init_modules()
        
        parent.addWidget(self.content_stack)
        
    def init_modules(self):
        """Initialize all application modules"""
        module_classes = {
            'dashboard': DashboardWidget,
            'leads': LeadsWidget,
            'smtps': SMTPWidget,
            'subjects': SubjectsWidget, 
            'messages': MessagesWidget,
            'campaigns': CampaignsWidget,
            'configurations': ConfigurationsWidget,
            'settings': SettingsWidget
        }
        
        for module_name, module_class in module_classes.items():
            try:
                widget = module_class(self)
                self.modules[module_name] = widget
                self.content_stack.addWidget(widget)
                self.logger.debug(f"Initialized {module_name} module")
            except Exception as e:
                self.logger.error(f"Failed to initialize {module_name} module: {e}")
                # Create placeholder widget
                placeholder = QLabel(f"Module '{module_name}' not available")
                placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
                self.modules[module_name] = placeholder
                self.content_stack.addWidget(placeholder)
        
    def setup_menu_bar(self):
        """Setup the application menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # View menu
        view_menu = menubar.addMenu('View')
        
        # Theme submenu
        theme_menu = view_menu.addMenu('Theme')
        
        dark_theme = QAction('Dark Theme', self)
        dark_theme.triggered.connect(lambda: self.change_theme('dark'))
        theme_menu.addAction(dark_theme)
        
        light_theme = QAction('Light Theme', self)
        light_theme.triggered.connect(lambda: self.change_theme('light'))
        theme_menu.addAction(light_theme)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def setup_status_bar(self):
        """Setup the application status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Status labels
        self.status_label = QLabel("Ready")
        self.status_bar.addWidget(self.status_label)
        
        self.status_bar.addPermanentWidget(QLabel("DeepMailer v1.0"))
        
    def setup_window(self):
        """Setup window properties"""
        # Set window size and position
        width = self.config.get('window', {}).get('width', 1200)
        height = self.config.get('window', {}).get('height', 800)
        self.resize(width, height)
        
        # Center window on screen
        screen = QApplication.primaryScreen().geometry()
        window_rect = self.geometry()
        x = (screen.width() - window_rect.width()) // 2
        y = (screen.height() - window_rect.height()) // 2
        self.move(x, y)
        
        # Set minimum size
        self.setMinimumSize(800, 600)
        
    def setup_connections(self):
        """Setup signal connections"""
        self.navigation_list.currentRowChanged.connect(self.on_navigation_changed)
        
    def setup_status_updates(self):
        """Setup periodic status updates"""
        self.status_timer = QTimer()
        self.status_timer.timeout.connect(self.update_status)
        self.status_timer.start(5000)  # Update every 5 seconds
        
    def on_navigation_changed(self, index):
        """Handle navigation list selection change"""
        if index < 0:
            return
            
        item = self.navigation_list.item(index)
        if not item:
            return
            
        module_name = item.data(Qt.ItemDataRole.UserRole)
        
        if module_name in self.modules:
            widget = self.modules[module_name]
            self.content_stack.setCurrentWidget(widget)
            
            # Update status
            self.status_label.setText(f"Viewing: {module_name.title()}")
            
            # Refresh module if it has a refresh method
            if hasattr(widget, 'refresh'):
                widget.refresh()
                
            self.logger.debug(f"Switched to {module_name} module")
        
    def change_theme(self, theme_name):
        """Change the application theme"""
        self.config['theme'] = theme_name
        save_config(self.config)
        
        # Emit signal for theme change
        self.theme_changed.emit(theme_name)
        
        # Show message that restart is required
        QMessageBox.information(
            self, 
            "Theme Changed",
            f"Theme changed to {theme_name}. Please restart the application to apply the new theme."
        )
        
    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About DeepMailer v1.0",
            """
            <h2>DeepMailer v1.0</h2>
            <p>Professional Email Marketing Software</p>
            <p>A comprehensive Windows-based email marketing and campaign management software 
            built with Python PyQt6 and featuring QSS-based theme customization.</p>
            <p><b>Features:</b></p>
            <ul>
            <li>Multi-Campaign Management</li>
            <li>Advanced SMTP Management</li> 
            <li>Lead Management</li>
            <li>Template Engine</li>
            <li>Real-time Analytics</li>
            <li>80+ Built-in Placeholders</li>
            <li>Anti-detection Technology</li>
            </ul>
            <p><b>Version:</b> 1.0<br>
            <b>License:</b> Commercial</p>
            """
        )
        
    def update_status(self):
        """Update status information"""
        try:
            # Get current module
            current_widget = self.content_stack.currentWidget()
            
            if hasattr(current_widget, 'get_status_info'):
                status_info = current_widget.get_status_info()
                if status_info:
                    self.status_label.setText(status_info)
        except Exception as e:
            self.logger.error(f"Error updating status: {e}")
            
    def closeEvent(self, event):
        """Handle application close event"""
        # Save window geometry
        self.config['window'] = {
            'width': self.width(),
            'height': self.height(),
            'maximized': self.isMaximized()
        }
        save_config(self.config)
        
        # Cleanup all modules
        self.cleanup()
        
        self.logger.info("Application closing")
        event.accept()
        
    def cleanup(self):
        """Cleanup resources before closing"""
        # Stop status timer
        if hasattr(self, 'status_timer'):
            self.status_timer.stop()
            
        # Cleanup all modules
        for module_name, module in self.modules.items():
            if hasattr(module, 'cleanup'):
                try:
                    module.cleanup()
                    self.logger.debug(f"Cleaned up {module_name} module")
                except Exception as e:
                    self.logger.error(f"Error cleaning up {module_name}: {e}")
                    
        self.logger.info("Main window cleanup completed")