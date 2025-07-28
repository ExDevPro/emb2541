"""
Subject Lines Management Widget for DeepMailer v1.0

This module provides comprehensive subject line management functionality including
multiple lists, personalization, spintext support, and rotation settings.
"""

import logging
import csv
from pathlib import Path
from typing import Dict, List, Any, Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QLineEdit,
    QSpinBox, QGroupBox, QFileDialog, QMessageBox, QDialog, QDialogButtonBox,
    QTextEdit, QCheckBox, QProgressBar, QFrame, QSplitter, QListWidget,
    QListWidgetItem, QScrollArea, QTabWidget, QFormLayout, QPlainTextEdit
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QColor

from modules.data_manager import DataManager
from modules.placeholders import PlaceholderEngine
from core.utils import get_data_path, safe_filename, format_number

class SubjectEditDialog(QDialog):
    """Dialog for editing subject lines"""
    
    def __init__(self, subject_text: str = "", parent=None):
        super().__init__(parent)
        self.subject_text = subject_text
        self.placeholder_engine = PlaceholderEngine()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the subject edit dialog"""
        self.setWindowTitle("Edit Subject Line")
        self.setModal(True)
        self.resize(600, 400)
        
        layout = QVBoxLayout(self)
        
        # Subject input
        layout.addWidget(QLabel("Subject Line:"))
        self.subject_input = QTextEdit()
        self.subject_input.setMaximumHeight(100)
        self.subject_input.setPlainText(self.subject_text)
        layout.addWidget(self.subject_input)
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        placeholder_btn = QPushButton("Insert Placeholder")
        placeholder_btn.clicked.connect(self.show_placeholder_menu)
        toolbar.addWidget(placeholder_btn)
        
        spintext_btn = QPushButton("Insert Spintext")
        spintext_btn.clicked.connect(self.show_spintext_menu)
        toolbar.addWidget(spintext_btn)
        
        preview_btn = QPushButton("Preview")
        preview_btn.clicked.connect(self.preview_subject)
        toolbar.addWidget(preview_btn)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # Help text
        help_text = QLabel("""
<b>Placeholder Types:</b><br>
• <span style="color: blue;">{column_name}</span> - Lead column data<br>
• <span style="color: green;">{{placeholder}}</span> - System placeholders<br>
• <span style="color: orange;">{{{spintext}}}</span> - Spintext variations<br><br>
<b>Examples:</b><br>
• "Hi {first_name}, check out our {{FakerWord}} deal!"<br>
• "Don't miss this {{{amazing|fantastic|incredible}}} offer!"
        """)
        help_text.setWordWrap(True)
        help_text.setStyleSheet("font-size: 12px; padding: 10px; background: #f0f0f0; border-radius: 5px;")
        layout.addWidget(help_text)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
    def show_placeholder_menu(self):
        """Show placeholder insertion menu"""
        placeholders = [
            "{email}", "{first_name}", "{last_name}", "{company}",
            "{{FakerFirstName}}", "{{FakerLastName}}", "{{FakerCompany}}",
            "{{timestamp}}", "{{date}}", "{{uuid}}", "{{campaign}}",
            "{{FakerWord}}", "{{FakerCity}}", "{{FakerJobTitle}}"
        ]
        
        from PyQt6.QtWidgets import QMenu
        menu = QMenu(self)
        
        for placeholder in placeholders:
            action = menu.addAction(placeholder)
            action.triggered.connect(lambda checked, p=placeholder: self.insert_text(p))
            
        menu.exec(self.sender().mapToGlobal(self.sender().rect().bottomLeft()))
        
    def show_spintext_menu(self):
        """Show spintext insertion menu"""
        spintexts = [
            "{{{amazing|fantastic|incredible|awesome}}}",
            "{{{deal|offer|promotion|special}}}",
            "{{{today|now|this week|limited time}}}",
            "{{{save|discount|off|reduced}}}",
            "{{{free|complimentary|no cost|bonus}}}"
        ]
        
        from PyQt6.QtWidgets import QMenu
        menu = QMenu(self)
        
        for spintext in spintexts:
            action = menu.addAction(spintext)
            action.triggered.connect(lambda checked, s=spintext: self.insert_text(s))
            
        menu.exec(self.sender().mapToGlobal(self.sender().rect().bottomLeft()))
        
    def insert_text(self, text):
        """Insert text at cursor position"""
        cursor = self.subject_input.textCursor()
        cursor.insertText(text)
        
    def preview_subject(self):
        """Preview the subject line with placeholder replacement"""
        subject_text = self.subject_input.toPlainText()
        
        # Simple preview (would use actual placeholder engine in real implementation)
        preview_text = subject_text
        
        # Preview placeholders with sample data
        sample_replacements = {
            '{first_name}': 'John',
            '{last_name}': 'Doe',
            '{email}': 'john.doe@example.com',
            '{company}': 'Acme Corp',
            '{{FakerFirstName}}': self.placeholder_engine.faker.first_name(),
            '{{FakerLastName}}': self.placeholder_engine.faker.last_name(),
            '{{FakerCompany}}': self.placeholder_engine.faker.company(),
            '{{timestamp}}': '1234567890',
            '{{date}}': '2025-01-01',
            '{{uuid}}': '12345678-1234-1234-1234-123456789012'
        }
        
        for placeholder, value in sample_replacements.items():
            preview_text = preview_text.replace(placeholder, str(value))
            
        # Handle spintext (simple version)
        import re
        spintext_pattern = r'\{\{\{([^}]+)\}\}\}'
        def replace_spintext(match):
            options = match.group(1).split('|')
            return options[0] if options else match.group(0)
        
        preview_text = re.sub(spintext_pattern, replace_spintext, preview_text)
        
        QMessageBox.information(self, "Subject Preview", f"Preview:\n\n{preview_text}")
        
    def get_subject_text(self):
        """Get the subject text"""
        return self.subject_input.toPlainText()

class SubjectListDialog(QDialog):
    """Dialog for creating/editing subject lists"""
    
    def __init__(self, list_name: str = "", parent=None):
        super().__init__(parent)
        self.list_name = list_name
        self.subjects = []
        self.setup_ui()
        if list_name:
            self.load_list()
            
    def setup_ui(self):
        """Setup the subject list dialog"""
        self.setWindowTitle("Subject List Manager")
        self.setModal(True)
        self.resize(800, 600)
        
        layout = QVBoxLayout(self)
        
        # List name input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("List Name:"))
        self.name_input = QLineEdit()
        if self.list_name:
            self.name_input.setText(self.list_name)
        name_layout.addWidget(self.name_input)
        layout.addLayout(name_layout)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Subject")
        add_btn.clicked.connect(self.add_subject)
        controls_layout.addWidget(add_btn)
        
        import_btn = QPushButton("Import from File")
        import_btn.clicked.connect(self.import_subjects)
        controls_layout.addWidget(import_btn)
        
        export_btn = QPushButton("Export to File")
        export_btn.clicked.connect(self.export_subjects)
        controls_layout.addWidget(export_btn)
        
        controls_layout.addStretch()
        
        edit_btn = QPushButton("Edit Selected")
        edit_btn.clicked.connect(self.edit_subject)
        controls_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self.delete_subject)
        controls_layout.addWidget(delete_btn)
        
        layout.addLayout(controls_layout)
        
        # Subjects list
        self.subjects_list = QListWidget()
        self.subjects_list.itemDoubleClicked.connect(self.edit_subject)
        layout.addWidget(self.subjects_list)
        
        # Stats
        self.stats_label = QLabel("0 subjects")
        layout.addWidget(self.stats_label)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_btn = QPushButton("Save List")
        save_btn.clicked.connect(self.save_list)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
        self.update_stats()
        
    def load_list(self):
        """Load existing subject list"""
        if not self.list_name:
            return
            
        file_path = get_data_path('subject') / f"{safe_filename(self.list_name)}.csv"
        if not file_path.exists():
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                headers = next(reader, None)
                
                for row in reader:
                    if row:  # Skip empty rows
                        self.subjects.append(row[0])
                        
            self.update_subjects_list()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load subject list: {str(e)}")
            
    def update_subjects_list(self):
        """Update the subjects list widget"""
        self.subjects_list.clear()
        for subject in self.subjects:
            self.subjects_list.addItem(subject)
        self.update_stats()
        
    def update_stats(self):
        """Update statistics label"""
        self.stats_label.setText(f"{len(self.subjects)} subjects")
        
    def add_subject(self):
        """Add a new subject"""
        dialog = SubjectEditDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            subject_text = dialog.get_subject_text().strip()
            if subject_text and subject_text not in self.subjects:
                self.subjects.append(subject_text)
                self.update_subjects_list()
                
    def edit_subject(self):
        """Edit selected subject"""
        current_item = self.subjects_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Warning", "Please select a subject to edit")
            return
            
        current_row = self.subjects_list.currentRow()
        current_text = self.subjects[current_row]
        
        dialog = SubjectEditDialog(current_text, parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_text = dialog.get_subject_text().strip()
            if new_text:
                self.subjects[current_row] = new_text
                self.update_subjects_list()
                
    def delete_subject(self):
        """Delete selected subject"""
        current_row = self.subjects_list.currentRow()
        if current_row >= 0:
            self.subjects.pop(current_row)
            self.update_subjects_list()
            
    def import_subjects(self):
        """Import subjects from file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Import Subjects", "",
            "Text files (*.txt);;CSV files (*.csv);;All files (*.*)"
        )
        
        if not file_path:
            return
            
        try:
            imported_count = 0
            duplicates_count = 0
            
            if file_path.endswith('.csv'):
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        if row:
                            subject = row[0].strip()
                            if subject:
                                if subject not in self.subjects:
                                    self.subjects.append(subject)
                                    imported_count += 1
                                else:
                                    duplicates_count += 1
            else:
                # Text file - one subject per line
                with open(file_path, 'r', encoding='utf-8') as f:
                    for line in f:
                        subject = line.strip()
                        if subject:
                            if subject not in self.subjects:
                                self.subjects.append(subject)
                                imported_count += 1
                            else:
                                duplicates_count += 1
                                
            self.update_subjects_list()
            
            message = f"Import completed:\n• {imported_count} subjects imported"
            if duplicates_count > 0:
                message += f"\n• {duplicates_count} duplicates skipped"
                
            QMessageBox.information(self, "Import Complete", message)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to import subjects: {str(e)}")
            
    def export_subjects(self):
        """Export subjects to file"""
        if not self.subjects:
            QMessageBox.warning(self, "Warning", "No subjects to export")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Subjects", "",
            "Text files (*.txt);;CSV files (*.csv);;All files (*.*)"
        )
        
        if not file_path:
            return
            
        try:
            if file_path.endswith('.csv'):
                with open(file_path, 'w', encoding='utf-8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['Subject'])
                    for subject in self.subjects:
                        writer.writerow([subject])
            else:
                # Text file - one subject per line
                with open(file_path, 'w', encoding='utf-8') as f:
                    for subject in self.subjects:
                        f.write(subject + '\n')
                        
            QMessageBox.information(self, "Success", f"Subjects exported to {file_path}")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to export subjects: {str(e)}")
            
    def save_list(self):
        """Save the subject list"""
        list_name = self.name_input.text().strip()
        if not list_name:
            QMessageBox.warning(self, "Error", "Please enter a list name")
            return
            
        if not self.subjects:
            QMessageBox.warning(self, "Error", "Please add at least one subject")
            return
            
        try:
            file_path = get_data_path('subject') / f"{safe_filename(list_name)}.csv"
            
            with open(file_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Subject'])
                for subject in self.subjects:
                    writer.writerow([subject])
                    
            QMessageBox.information(self, "Success", f"Subject list '{list_name}' saved successfully!")
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save subject list: {str(e)}")

class SubjectsWidget(QWidget):
    """Subject lines management widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.logger = logging.getLogger(__name__)
        self.data_manager = DataManager()
        self.subject_lists = []
        self.setup_ui()
        self.refresh_lists()
        
    def setup_ui(self):
        """Setup the subjects UI"""
        layout = QVBoxLayout(self)
        
        # Title and controls
        header_layout = QHBoxLayout()
        
        title = QLabel("📝 Subject Lines Management")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Action buttons
        new_list_btn = QPushButton("New Subject List")
        new_list_btn.clicked.connect(self.create_list)
        header_layout.addWidget(new_list_btn)
        
        layout.addLayout(header_layout)
        
        # Subject lists table
        self.lists_table = QTableWidget()
        self.lists_table.setColumnCount(5)
        self.lists_table.setHorizontalHeaderLabels([
            "List Name", "Subjects Count", "Created", "File Size", "Actions"
        ])
        
        # Configure table
        header = self.lists_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        
        self.lists_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.lists_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.lists_table)
        
        # Status bar
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
    def refresh_lists(self):
        """Refresh the subject lists"""
        try:
            self.subject_lists = self.get_subject_lists()
            self.update_table()
            self.status_label.setText(f"Found {len(self.subject_lists)} subject lists")
        except Exception as e:
            self.logger.error(f"Failed to refresh subject lists: {e}")
            self.status_label.setText("Error loading subject lists")
            
    def get_subject_lists(self) -> List[Dict[str, Any]]:
        """Get all subject lists"""
        lists = []
        subjects_dir = get_data_path('subject')
        
        if not subjects_dir.exists():
            return lists
            
        for file_path in subjects_dir.glob("*.csv"):
            try:
                # Count subjects
                with open(file_path, 'r', encoding='utf-8') as f:
                    reader = csv.reader(f)
                    next(reader, None)  # Skip header
                    subject_count = sum(1 for row in reader if row)
                    
                # Get file stats
                stats = file_path.stat()
                
                lists.append({
                    'name': file_path.stem,
                    'path': str(file_path),
                    'subject_count': subject_count,
                    'file_size': f"{stats.st_size / 1024:.1f} KB",
                    'created': stats.st_ctime
                })
                
            except Exception as e:
                self.logger.error(f"Failed to read subject list {file_path}: {e}")
                
        return lists
        
    def update_table(self):
        """Update the subject lists table"""
        self.lists_table.setRowCount(len(self.subject_lists))
        
        for row, subject_list in enumerate(self.subject_lists):
            # List name
            self.lists_table.setItem(row, 0, QTableWidgetItem(subject_list['name']))
            
            # Subject count
            self.lists_table.setItem(row, 1, QTableWidgetItem(str(subject_list['subject_count'])))
            
            # Created date
            from datetime import datetime
            created_date = datetime.fromtimestamp(subject_list['created']).strftime('%Y-%m-%d')
            self.lists_table.setItem(row, 2, QTableWidgetItem(created_date))
            
            # File size
            self.lists_table.setItem(row, 3, QTableWidgetItem(subject_list['file_size']))
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 2, 5, 2)
            
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, sl=subject_list: self.edit_list(sl))
            actions_layout.addWidget(edit_btn)
            
            copy_btn = QPushButton("Copy")
            copy_btn.clicked.connect(lambda checked, sl=subject_list: self.copy_list(sl))
            actions_layout.addWidget(copy_btn)
            
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, sl=subject_list: self.delete_list(sl))
            actions_layout.addWidget(delete_btn)
            
            self.lists_table.setCellWidget(row, 4, actions_widget)
            
    def create_list(self):
        """Create a new subject list"""
        dialog = SubjectListDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_lists()
            
    def edit_list(self, subject_list: Dict[str, Any]):
        """Edit an existing subject list"""
        dialog = SubjectListDialog(subject_list['name'], parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_lists()
            
    def copy_list(self, subject_list: Dict[str, Any]):
        """Copy a subject list"""
        from PyQt6.QtWidgets import QInputDialog
        new_name, ok = QInputDialog.getText(
            self, "Copy Subject List", 
            f"Enter name for copy of '{subject_list['name']}':",
            text=f"{subject_list['name']}_copy"
        )
        
        if ok and new_name.strip():
            try:
                source_file = Path(subject_list['path'])
                dest_file = get_data_path('subject') / f"{safe_filename(new_name.strip())}.csv"
                
                if dest_file.exists():
                    QMessageBox.warning(self, "Error", "A subject list with that name already exists")
                    return
                    
                import shutil
                shutil.copy2(source_file, dest_file)
                
                self.refresh_lists()
                QMessageBox.information(self, "Success", f"Subject list copied as '{new_name}'")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to copy subject list: {str(e)}")
                
    def delete_list(self, subject_list: Dict[str, Any]):
        """Delete a subject list"""
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete subject list '{subject_list['name']}'?\n\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                file_path = Path(subject_list['path'])
                file_path.unlink()
                self.refresh_lists()
                QMessageBox.information(self, "Success", "Subject list deleted successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete subject list: {str(e)}")
                
    def refresh(self):
        """Refresh the module"""
        self.refresh_lists()
        
    def get_status_info(self):
        """Get status info"""
        total_subjects = sum(sl['subject_count'] for sl in self.subject_lists)
        return f"Subject lists: {len(self.subject_lists)} lists, {total_subjects} subjects total"
        
    def cleanup(self):
        """Cleanup resources"""
        pass