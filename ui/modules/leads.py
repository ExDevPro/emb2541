"""
Leads Management Widget for DeepMailer v1.0

This module provides comprehensive lead management functionality including
import/export, table view, pagination, duplicate detection, and editing.
"""

import logging
import csv
from pathlib import Path
from typing import List, Dict, Any, Tuple
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QLineEdit,
    QSpinBox, QGroupBox, QFileDialog, QMessageBox, QDialog, QDialogButtonBox,
    QTextEdit, QCheckBox, QProgressBar, QFrame, QSplitter, QListWidget,
    QListWidgetItem, QScrollArea
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor

from modules.data_manager import DataManager
from core.utils import format_number, validate_email

class ImportWorker(QThread):
    """Worker thread for importing leads"""
    
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished = pyqtSignal(bool, str, int)
    
    def __init__(self, file_path: str, list_name: str, data_manager: DataManager):
        super().__init__()
        self.file_path = file_path
        self.list_name = list_name
        self.data_manager = data_manager
        
    def run(self):
        """Import leads in background thread"""
        try:
            self.status.emit("Starting import...")
            success, message, count = self.data_manager.import_leads_from_file(
                self.file_path, self.list_name
            )
            self.finished.emit(success, message, count)
        except Exception as e:
            self.finished.emit(False, f"Import error: {str(e)}", 0)

class LeadEditDialog(QDialog):
    """Dialog for editing a single lead"""
    
    def __init__(self, headers: List[str], data: List[str] = None, parent=None):
        super().__init__(parent)
        self.headers = headers
        self.data = data or [''] * len(headers)
        self.fields = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the edit dialog UI"""
        self.setWindowTitle("Edit Lead")
        self.setModal(True)
        self.resize(400, 500)
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Edit Lead Information")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # Scroll area for fields
        scroll = QScrollArea()
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # Create input fields for each header
        for i, header in enumerate(self.headers):
            field_layout = QVBoxLayout()
            
            label = QLabel(header)
            label.setStyleSheet("font-weight: bold;")
            field_layout.addWidget(label)
            
            if header.lower() in ['email', 'e-mail', 'email_address']:
                # Email field with validation
                field = QLineEdit(self.data[i] if i < len(self.data) else '')
                field.setPlaceholderText("Enter email address")
                field.textChanged.connect(self.validate_email_field)
            else:
                field = QLineEdit(self.data[i] if i < len(self.data) else '')
                field.setPlaceholderText(f"Enter {header}")
                
            self.fields[header] = field
            field_layout.addWidget(field)
            
            scroll_layout.addLayout(field_layout)
            
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
    def validate_email_field(self):
        """Validate email field"""
        sender = self.sender()
        email = sender.text()
        
        if email and not validate_email(email):
            sender.setStyleSheet("border: 2px solid red;")
        else:
            sender.setStyleSheet("")
            
    def get_data(self) -> List[str]:
        """Get the edited data"""
        result = []
        for header in self.headers:
            field = self.fields.get(header)
            result.append(field.text() if field else '')
        return result

class CreateListDialog(QDialog):
    """Dialog for creating a new leads list"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the create list dialog UI"""
        self.setWindowTitle("Create New Leads List")
        self.setModal(True)
        self.resize(400, 200)
        
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Create New Leads List")
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        # List name
        layout.addWidget(QLabel("List Name:"))
        self.name_field = QLineEdit()
        self.name_field.setPlaceholderText("Enter list name")
        layout.addWidget(self.name_field)
        
        # Description
        layout.addWidget(QLabel("Description (optional):"))
        self.description_field = QTextEdit()
        self.description_field.setMaximumHeight(80)
        self.description_field.setPlaceholderText("Enter description")
        layout.addWidget(self.description_field)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
        # Validation
        self.name_field.textChanged.connect(self.validate_input)
        self.validate_input()
        
    def validate_input(self):
        """Validate input fields"""
        ok_button = self.findChild(QDialogButtonBox).button(QDialogButtonBox.StandardButton.Ok)
        ok_button.setEnabled(bool(self.name_field.text().strip()))
        
    def get_list_name(self) -> str:
        """Get the list name"""
        return self.name_field.text().strip()
        
    def get_description(self) -> str:
        """Get the description"""
        return self.description_field.toPlainText().strip()

class LeadsWidget(QWidget):
    """Leads management widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.logger = logging.getLogger(__name__)
        self.data_manager = DataManager()
        
        # Current state
        self.current_list = None
        self.current_headers = []
        self.current_data = []
        self.current_page = 0
        self.items_per_page = 100
        self.total_items = 0
        
        self.setup_ui()
        self.refresh_lists()
        
        self.logger.info("Leads widget initialized")
        
    def setup_ui(self):
        """Setup the leads UI"""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Page title
        title_label = QLabel("👥 Leads Management")
        title_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
        """)
        main_layout.addWidget(title_label)
        
        # Create horizontal splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel - Lists
        self.setup_left_panel(splitter)
        
        # Right panel - Table
        self.setup_right_panel(splitter)
        
        # Set splitter proportions
        splitter.setSizes([300, 700])
        
    def setup_left_panel(self, parent):
        """Setup the left panel with list management"""
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        
        # Lists section
        lists_group = QGroupBox("Leads Lists")
        lists_layout = QVBoxLayout(lists_group)
        
        # List controls
        list_controls = QHBoxLayout()
        
        self.create_list_btn = QPushButton("📝 Create List")
        self.create_list_btn.clicked.connect(self.create_new_list)
        list_controls.addWidget(self.create_list_btn)
        
        self.import_btn = QPushButton("📥 Import")
        self.import_btn.clicked.connect(self.import_leads)
        list_controls.addWidget(self.import_btn)
        
        lists_layout.addLayout(list_controls)
        
        # Lists widget
        self.lists_widget = QListWidget()
        self.lists_widget.currentItemChanged.connect(self.on_list_selected)
        lists_layout.addWidget(self.lists_widget)
        
        # List info
        self.list_info_label = QLabel("No list selected")
        self.list_info_label.setStyleSheet("""
            background-color: #f0f0f0;
            border: 1px solid #ddd;
            border-radius: 3px;
            padding: 8px;
            font-size: 11px;
        """)
        lists_layout.addWidget(self.list_info_label)
        
        # List actions
        list_actions = QVBoxLayout()
        
        self.delete_list_btn = QPushButton("🗑️ Delete List")
        self.delete_list_btn.clicked.connect(self.delete_current_list)
        self.delete_list_btn.setEnabled(False)
        list_actions.addWidget(self.delete_list_btn)
        
        self.export_btn = QPushButton("📤 Export")
        self.export_btn.clicked.connect(self.export_leads)
        self.export_btn.setEnabled(False)
        list_actions.addWidget(self.export_btn)
        
        lists_layout.addLayout(list_actions)
        
        left_layout.addWidget(lists_group)
        left_layout.addStretch()
        
        parent.addWidget(left_widget)
        
    def setup_right_panel(self, parent):
        """Setup the right panel with table view"""
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        
        # Table controls
        controls_layout = QHBoxLayout()
        
        # Search
        controls_layout.addWidget(QLabel("Search:"))
        self.search_field = QLineEdit()
        self.search_field.setPlaceholderText("Search in all columns...")
        self.search_field.textChanged.connect(self.filter_table)
        controls_layout.addWidget(self.search_field)
        
        controls_layout.addStretch()
        
        # Add/Edit controls
        self.add_lead_btn = QPushButton("➕ Add Lead")
        self.add_lead_btn.clicked.connect(self.add_lead)
        self.add_lead_btn.setEnabled(False)
        controls_layout.addWidget(self.add_lead_btn)
        
        self.edit_lead_btn = QPushButton("✏️ Edit Lead")
        self.edit_lead_btn.clicked.connect(self.edit_lead)
        self.edit_lead_btn.setEnabled(False)
        controls_layout.addWidget(self.edit_lead_btn)
        
        self.delete_lead_btn = QPushButton("🗑️ Delete Lead")
        self.delete_lead_btn.clicked.connect(self.delete_lead)
        self.delete_lead_btn.setEnabled(False)
        controls_layout.addWidget(self.delete_lead_btn)
        
        right_layout.addLayout(controls_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setAlternatingRowColors(True)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.itemSelectionChanged.connect(self.on_selection_changed)
        self.table.itemDoubleClicked.connect(self.edit_lead)
        right_layout.addWidget(self.table)
        
        # Pagination and stats
        bottom_layout = QHBoxLayout()
        
        # Stats
        self.stats_label = QLabel("No data")
        bottom_layout.addWidget(self.stats_label)
        
        bottom_layout.addStretch()
        
        # Pagination
        bottom_layout.addWidget(QLabel("Items per page:"))
        self.items_per_page_combo = QComboBox()
        self.items_per_page_combo.addItems(["50", "100", "200", "500"])
        self.items_per_page_combo.setCurrentText("100")
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
        
        right_layout.addLayout(bottom_layout)
        
        parent.addWidget(right_widget)
        
    def refresh_lists(self):
        """Refresh the lists widget"""
        self.lists_widget.clear()
        lists = self.data_manager.get_leads_lists()
        
        for list_info in lists:
            item = QListWidgetItem()
            item.setText(f"{list_info['name']} ({list_info['row_count']} leads)")
            item.setData(Qt.ItemDataRole.UserRole, list_info)
            self.lists_widget.addItem(item)
            
        # Update list info
        if not lists:
            self.list_info_label.setText("No lists found")
        else:
            total_leads = sum(lst['row_count'] for lst in lists)
            self.list_info_label.setText(f"Total: {len(lists)} lists, {format_number(total_leads)} leads")
            
    def on_list_selected(self, current, previous):
        """Handle list selection"""
        if current:
            list_info = current.data(Qt.ItemDataRole.UserRole)
            self.current_list = list_info['name']
            
            # Load list data
            self.load_list_data()
            
            # Enable controls
            self.delete_list_btn.setEnabled(True)
            self.export_btn.setEnabled(True)
            self.add_lead_btn.setEnabled(True)
            
            self.logger.info(f"Selected list: {self.current_list}")
        else:
            self.current_list = None
            self.clear_table()
            
            # Disable controls
            self.delete_list_btn.setEnabled(False)
            self.export_btn.setEnabled(False)
            self.add_lead_btn.setEnabled(False)
            self.edit_lead_btn.setEnabled(False)
            self.delete_lead_btn.setEnabled(False)
            
    def load_list_data(self):
        """Load data for the current list"""
        if not self.current_list:
            return
            
        headers, data = self.data_manager.load_leads_list(self.current_list)
        self.current_headers = headers
        self.current_data = data
        self.current_page = 0
        self.total_items = len(data)
        
        self.setup_table()
        self.update_table()
        self.update_pagination()
        self.update_stats()
        
    def setup_table(self):
        """Setup table structure"""
        if not self.current_headers:
            self.clear_table()
            return
            
        self.table.setColumnCount(len(self.current_headers))
        self.table.setHorizontalHeaderLabels(self.current_headers)
        
        # Resize columns to content
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        
    def update_table(self):
        """Update table with current page data"""
        if not self.current_data:
            self.table.setRowCount(0)
            return
            
        # Calculate page bounds
        start_idx = self.current_page * self.items_per_page
        end_idx = min(start_idx + self.items_per_page, len(self.current_data))
        page_data = self.current_data[start_idx:end_idx]
        
        # Set table rows
        self.table.setRowCount(len(page_data))
        
        # Populate table
        for row, data_row in enumerate(page_data):
            for col, value in enumerate(data_row):
                item = QTableWidgetItem(str(value) if value else '')
                
                # Validate email columns
                if (col < len(self.current_headers) and 
                    self.current_headers[col].lower() in ['email', 'e-mail', 'email_address']):
                    if value and not validate_email(value):
                        item.setBackground(QColor(255, 200, 200))  # Light red for invalid emails
                        
                self.table.setItem(row, col, item)
                
    def clear_table(self):
        """Clear the table"""
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        self.stats_label.setText("No data")
        self.page_label.setText("Page 1 of 1")
        
    def update_stats(self):
        """Update statistics display"""
        if not self.current_data:
            self.stats_label.setText("No data")
            return
            
        total = len(self.current_data)
        valid_emails = 0
        invalid_emails = 0
        
        # Find email column
        email_col = -1
        for i, header in enumerate(self.current_headers):
            if header.lower() in ['email', 'e-mail', 'email_address']:
                email_col = i
                break
                
        if email_col >= 0:
            for row in self.current_data:
                if email_col < len(row) and row[email_col]:
                    if validate_email(row[email_col]):
                        valid_emails += 1
                    else:
                        invalid_emails += 1
                        
        stats_text = f"Total: {format_number(total)} leads"
        if email_col >= 0:
            stats_text += f" | Valid emails: {format_number(valid_emails)} | Invalid: {format_number(invalid_emails)}"
            
        self.stats_label.setText(stats_text)
        
    def update_pagination(self):
        """Update pagination controls"""
        if not self.current_data:
            self.page_label.setText("Page 1 of 1")
            self.prev_page_btn.setEnabled(False)
            self.next_page_btn.setEnabled(False)
            return
            
        total_pages = max(1, (len(self.current_data) + self.items_per_page - 1) // self.items_per_page)
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
        total_pages = (len(self.current_data) + self.items_per_page - 1) // self.items_per_page
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
        
    def filter_table(self, text):
        """Filter table based on search text"""
        # TODO: Implement filtering
        pass
        
    def on_selection_changed(self):
        """Handle table selection change"""
        selected = len(self.table.selectedItems()) > 0
        self.edit_lead_btn.setEnabled(selected)
        self.delete_lead_btn.setEnabled(selected)
        
    def create_new_list(self):
        """Create a new leads list"""
        dialog = CreateListDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            list_name = dialog.get_list_name()
            
            # Check if list already exists
            existing_lists = [lst['name'] for lst in self.data_manager.get_leads_lists()]
            if list_name in existing_lists:
                QMessageBox.warning(self, "Error", f"List '{list_name}' already exists.")
                return
                
            # Create empty list with basic headers
            headers = ['email', 'first_name', 'last_name', 'company']
            success = self.data_manager.save_leads_list(list_name, headers, [])
            
            if success:
                self.refresh_lists()
                QMessageBox.information(self, "Success", f"List '{list_name}' created successfully.")
            else:
                QMessageBox.critical(self, "Error", "Failed to create list.")
                
    def import_leads(self):
        """Import leads from file"""
        if not self.current_list:
            QMessageBox.warning(self, "Error", "Please select a list first.")
            return
            
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Import Leads", 
            "", 
            "CSV Files (*.csv);;Excel Files (*.xlsx *.xls);;Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            # Start import in background thread
            self.import_worker = ImportWorker(file_path, self.current_list, self.data_manager)
            self.import_worker.finished.connect(self.on_import_finished)
            self.import_worker.start()
            
            # Show progress (simplified - no actual progress bar for now)
            QMessageBox.information(self, "Import", "Import started. Please wait...")
            
    def on_import_finished(self, success, message, count):
        """Handle import completion"""
        if success:
            QMessageBox.information(self, "Success", message)
            self.load_list_data()  # Refresh current list
            self.refresh_lists()   # Refresh list stats
        else:
            QMessageBox.critical(self, "Error", message)
            
    def export_leads(self):
        """Export current list"""
        if not self.current_list or not self.current_data:
            QMessageBox.warning(self, "Error", "No data to export.")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Leads",
            f"{self.current_list}.csv",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(self.current_headers)
                    writer.writerows(self.current_data)
                    
                QMessageBox.information(self, "Success", f"Exported {len(self.current_data)} leads.")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Export failed: {str(e)}")
                
    def add_lead(self):
        """Add a new lead"""
        if not self.current_headers:
            return
            
        dialog = LeadEditDialog(self.current_headers, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_data()
            
            # Add to current data
            self.current_data.append(new_data)
            
            # Save to file
            success = self.data_manager.save_leads_list(
                self.current_list, self.current_headers, self.current_data
            )
            
            if success:
                self.update_table()
                self.update_stats()
                self.update_pagination()
                self.refresh_lists()  # Update counts
            else:
                # Remove from current data if save failed
                self.current_data.pop()
                QMessageBox.critical(self, "Error", "Failed to save lead.")
                
    def edit_lead(self):
        """Edit selected lead"""
        if not self.table.currentRow() >= 0:
            return
            
        # Get current row data
        row = self.table.currentRow()
        global_row = self.current_page * self.items_per_page + row
        
        if global_row >= len(self.current_data):
            return
            
        current_data = self.current_data[global_row]
        
        dialog = LeadEditDialog(self.current_headers, current_data, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_data = dialog.get_data()
            
            # Update current data
            self.current_data[global_row] = new_data
            
            # Save to file
            success = self.data_manager.save_leads_list(
                self.current_list, self.current_headers, self.current_data
            )
            
            if success:
                self.update_table()
                self.update_stats()
            else:
                # Revert changes if save failed
                self.current_data[global_row] = current_data
                QMessageBox.critical(self, "Error", "Failed to save changes.")
                
    def delete_lead(self):
        """Delete selected lead"""
        if not self.table.currentRow() >= 0:
            return
            
        reply = QMessageBox.question(
            self, 
            "Confirm Delete", 
            "Are you sure you want to delete this lead?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            row = self.table.currentRow()
            global_row = self.current_page * self.items_per_page + row
            
            if global_row >= len(self.current_data):
                return
                
            # Remove from current data
            removed_data = self.current_data.pop(global_row)
            
            # Save to file
            success = self.data_manager.save_leads_list(
                self.current_list, self.current_headers, self.current_data
            )
            
            if success:
                self.update_table()
                self.update_stats()
                self.update_pagination()
                self.refresh_lists()  # Update counts
            else:
                # Restore data if save failed
                self.current_data.insert(global_row, removed_data)
                QMessageBox.critical(self, "Error", "Failed to delete lead.")
                
    def delete_current_list(self):
        """Delete the current list"""
        if not self.current_list:
            return
            
        reply = QMessageBox.question(
            self,
            "Confirm Delete",
            f"Are you sure you want to delete the list '{self.current_list}'?\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            success = self.data_manager.delete_leads_list(self.current_list)
            
            if success:
                self.current_list = None
                self.clear_table()
                self.refresh_lists()
                QMessageBox.information(self, "Success", "List deleted successfully.")
            else:
                QMessageBox.critical(self, "Error", "Failed to delete list.")
        
    def refresh(self):
        """Refresh the module"""
        self.refresh_lists()
        if self.current_list:
            self.load_list_data()
        
    def get_status_info(self):
        """Get status info"""
        if self.current_list:
            return f"Leads - {self.current_list} ({format_number(len(self.current_data))} leads)"
        return "Leads - No list selected"
        
    def cleanup(self):
        """Cleanup resources"""
        if hasattr(self, 'import_worker') and self.import_worker.isRunning():
            self.import_worker.terminate()
        self.logger.info("Leads widget cleaned up")