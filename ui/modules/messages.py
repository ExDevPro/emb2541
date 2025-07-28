"""
Message Templates Widget for DeepMailer v1.0

This module provides comprehensive email template management functionality including
WYSIWYG editor, attachments, personalization, and advanced obfuscation features.
"""

import logging
import os
import shutil
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
from PyQt6.QtGui import QFont, QColor, QTextCharFormat, QTextCursor

from modules.data_manager import DataManager
from core.utils import get_data_path, safe_filename, format_number

class TemplateEditDialog(QDialog):
    """Dialog for creating/editing email templates"""
    
    def __init__(self, template_name: str = None, parent=None):
        super().__init__(parent)
        self.template_name = template_name
        self.template_dir = None
        self.attachments = []
        self.setup_ui()
        if template_name:
            self.load_template()
        
    def setup_ui(self):
        """Setup the template editor dialog"""
        self.setWindowTitle("Email Template Editor")
        self.setModal(True)
        self.resize(1000, 700)
        
        layout = QVBoxLayout(self)
        
        # Template name input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("Template Name:"))
        self.name_input = QLineEdit()
        if self.template_name:
            self.name_input.setText(self.template_name)
        name_layout.addWidget(self.name_input)
        layout.addWidget(QFrame())  # separator
        layout.addLayout(name_layout)
        
        # Tab widget for different content types
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # HTML Content tab
        self.setup_html_tab()
        
        # Plain Text tab
        self.setup_text_tab()
        
        # Attachments tab
        self.setup_attachments_tab()
        
        # Advanced Settings tab
        self.setup_advanced_tab()
        
        # Buttons
        button_layout = QHBoxLayout()
        
        preview_btn = QPushButton("Preview")
        preview_btn.clicked.connect(self.preview_template)
        button_layout.addWidget(preview_btn)
        
        test_placeholders_btn = QPushButton("Test Placeholders")
        test_placeholders_btn.clicked.connect(self.test_placeholders)
        button_layout.addWidget(test_placeholders_btn)
        
        button_layout.addStretch()
        
        save_btn = QPushButton("Save Template")
        save_btn.clicked.connect(self.save_template)
        button_layout.addWidget(save_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
        
    def setup_html_tab(self):
        """Setup HTML content editing tab"""
        html_widget = QWidget()
        layout = QVBoxLayout(html_widget)
        
        # Enable content checkbox
        self.html_enabled = QCheckBox("Enable HTML Content")
        self.html_enabled.setChecked(True)
        layout.addWidget(self.html_enabled)
        
        # Toolbar for HTML editing
        toolbar = QHBoxLayout()
        
        bold_btn = QPushButton("B")
        bold_btn.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        bold_btn.clicked.connect(lambda: self.format_text("bold"))
        toolbar.addWidget(bold_btn)
        
        italic_btn = QPushButton("I")
        italic_btn.setFont(QFont("Arial", 10, QFont.Weight.Normal))
        italic_btn.setStyleSheet("font-style: italic;")
        italic_btn.clicked.connect(lambda: self.format_text("italic"))
        toolbar.addWidget(italic_btn)
        
        link_btn = QPushButton("Link")
        link_btn.clicked.connect(self.insert_link)
        toolbar.addWidget(link_btn)
        
        image_btn = QPushButton("Image")
        image_btn.clicked.connect(self.insert_image)
        toolbar.addWidget(image_btn)
        
        toolbar.addStretch()
        
        placeholder_btn = QPushButton("Insert Placeholder")
        placeholder_btn.clicked.connect(self.show_placeholder_menu)
        toolbar.addWidget(placeholder_btn)
        
        unsubscribe_btn = QPushButton("Unsubscribe Link")
        unsubscribe_btn.clicked.connect(self.insert_unsubscribe)
        toolbar.addWidget(unsubscribe_btn)
        
        layout.addLayout(toolbar)
        
        # HTML editor
        self.html_editor = QTextEdit()
        self.html_editor.setPlaceholderText("Enter your HTML email content here...")
        self.html_editor.setAcceptRichText(True)
        layout.addWidget(self.html_editor)
        
        self.tab_widget.addTab(html_widget, "HTML Content")
        
    def setup_text_tab(self):
        """Setup plain text editing tab"""
        text_widget = QWidget()
        layout = QVBoxLayout(text_widget)
        
        # Enable content checkbox
        self.text_enabled = QCheckBox("Enable Plain Text Content")
        self.text_enabled.setChecked(True)
        layout.addWidget(self.text_enabled)
        
        # Toolbar
        toolbar = QHBoxLayout()
        
        placeholder_btn = QPushButton("Insert Placeholder")
        placeholder_btn.clicked.connect(self.show_placeholder_menu_text)
        toolbar.addWidget(placeholder_btn)
        
        unsubscribe_btn = QPushButton("Unsubscribe Link")
        unsubscribe_btn.clicked.connect(self.insert_unsubscribe_text)
        toolbar.addWidget(unsubscribe_btn)
        
        toolbar.addStretch()
        layout.addLayout(toolbar)
        
        # Plain text editor
        self.text_editor = QPlainTextEdit()
        self.text_editor.setPlaceholderText("Enter your plain text email content here...")
        layout.addWidget(self.text_editor)
        
        self.tab_widget.addTab(text_widget, "Plain Text")
        
    def setup_attachments_tab(self):
        """Setup attachments management tab"""
        attachments_widget = QWidget()
        layout = QVBoxLayout(attachments_widget)
        
        # Attachments list
        list_layout = QHBoxLayout()
        
        self.attachments_list = QListWidget()
        list_layout.addWidget(self.attachments_list)
        
        # Attachment controls
        controls_layout = QVBoxLayout()
        
        add_btn = QPushButton("Add File")
        add_btn.clicked.connect(self.add_attachment)
        controls_layout.addWidget(add_btn)
        
        remove_btn = QPushButton("Remove")
        remove_btn.clicked.connect(self.remove_attachment)
        controls_layout.addWidget(remove_btn)
        
        controls_layout.addStretch()
        list_layout.addLayout(controls_layout)
        
        layout.addLayout(list_layout)
        
        # Attachment info
        info_label = QLabel("Supported file types: PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX, TXT, CSV, ZIP, RAR, JPG, PNG, GIF")
        info_label.setStyleSheet("color: #666; font-size: 12px;")
        layout.addWidget(info_label)
        
        self.tab_widget.addTab(attachments_widget, "Attachments")
        
    def setup_advanced_tab(self):
        """Setup advanced settings tab"""
        advanced_widget = QWidget()
        layout = QVBoxLayout(advanced_widget)
        
        # Fingerprint obfuscation
        obfuscation_group = QGroupBox("Fingerprint Obfuscation")
        obfuscation_layout = QVBoxLayout(obfuscation_group)
        
        self.obfuscation_enabled = QCheckBox("Enable Fingerprint Obfuscation")
        obfuscation_layout.addWidget(self.obfuscation_enabled)
        
        obf_info = QLabel("Adds invisible HTML elements to create unique fingerprints for each email")
        obf_info.setStyleSheet("color: #666; font-size: 12px;")
        obfuscation_layout.addWidget(obf_info)
        
        # Rotation settings
        rotation_layout = QHBoxLayout()
        rotation_layout.addWidget(QLabel("Rotation:"))
        
        self.obfuscation_rotation = QComboBox()
        self.obfuscation_rotation.addItems(["Each Time", "Custom Range"])
        rotation_layout.addWidget(self.obfuscation_rotation)
        
        self.obfuscation_range_min = QSpinBox()
        self.obfuscation_range_min.setRange(1, 1000)
        self.obfuscation_range_min.setValue(10)
        rotation_layout.addWidget(self.obfuscation_range_min)
        
        rotation_layout.addWidget(QLabel("to"))
        
        self.obfuscation_range_max = QSpinBox()
        self.obfuscation_range_max.setRange(1, 1000)
        self.obfuscation_range_max.setValue(25)
        rotation_layout.addWidget(self.obfuscation_range_max)
        
        rotation_layout.addStretch()
        obfuscation_layout.addLayout(rotation_layout)
        
        layout.addWidget(obfuscation_group)
        
        # Emoji rotation
        emoji_group = QGroupBox("Emoji Rotation")
        emoji_layout = QVBoxLayout(emoji_group)
        
        self.emoji_rotation_enabled = QCheckBox("Enable Emoji Rotation")
        emoji_layout.addWidget(self.emoji_rotation_enabled)
        
        emoji_info = QLabel("Automatically detects and rotates emojis in the template")
        emoji_info.setStyleSheet("color: #666; font-size: 12px;")
        emoji_layout.addWidget(emoji_info)
        
        layout.addWidget(emoji_group)
        
        layout.addStretch()
        
        self.tab_widget.addTab(advanced_widget, "Advanced")
        
    def format_text(self, format_type):
        """Apply text formatting"""
        cursor = self.html_editor.textCursor()
        format = QTextCharFormat()
        
        if format_type == "bold":
            format.setFontWeight(QFont.Weight.Bold if not cursor.charFormat().font().bold() else QFont.Weight.Normal)
        elif format_type == "italic":
            format.setFontItalic(not cursor.charFormat().font().italic())
            
        cursor.mergeCharFormat(format)
        
    def insert_link(self):
        """Insert a hyperlink"""
        from PyQt6.QtWidgets import QInputDialog
        url, ok = QInputDialog.getText(self, "Insert Link", "Enter URL:")
        if ok and url:
            cursor = self.html_editor.textCursor()
            cursor.insertHtml(f'<a href="{url}">{url}</a>')
            
    def insert_image(self):
        """Insert an image"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Image", "", 
            "Image files (*.png *.jpg *.jpeg *.gif *.bmp)"
        )
        if file_path:
            cursor = self.html_editor.textCursor()
            cursor.insertHtml(f'<img src="{file_path}" alt="Image" style="max-width: 100%;">')
            
    def show_placeholder_menu(self):
        """Show placeholder insertion menu"""
        # Common placeholders
        placeholders = [
            "{email}", "{first_name}", "{last_name}", "{company}",
            "{{FakerFirstName}}", "{{FakerLastName}}", "{{FakerCompany}}",
            "{{timestamp}}", "{{date}}", "{{uuid}}", "{{campaign}}"
        ]
        
        from PyQt6.QtWidgets import QMenu
        menu = QMenu(self)
        
        for placeholder in placeholders:
            action = menu.addAction(placeholder)
            action.triggered.connect(lambda checked, p=placeholder: self.insert_placeholder_html(p))
            
        menu.exec(self.sender().mapToGlobal(self.sender().rect().bottomLeft()))
        
    def show_placeholder_menu_text(self):
        """Show placeholder insertion menu for text editor"""
        placeholders = [
            "{email}", "{first_name}", "{last_name}", "{company}",
            "{{FakerFirstName}}", "{{FakerLastName}}", "{{FakerCompany}}",
            "{{timestamp}}", "{{date}}", "{{uuid}}", "{{campaign}}"
        ]
        
        from PyQt6.QtWidgets import QMenu
        menu = QMenu(self)
        
        for placeholder in placeholders:
            action = menu.addAction(placeholder)
            action.triggered.connect(lambda checked, p=placeholder: self.insert_placeholder_text(p))
            
        menu.exec(self.sender().mapToGlobal(self.sender().rect().bottomLeft()))
        
    def insert_placeholder_html(self, placeholder):
        """Insert placeholder in HTML editor"""
        cursor = self.html_editor.textCursor()
        cursor.insertText(placeholder)
        
    def insert_placeholder_text(self, placeholder):
        """Insert placeholder in text editor"""
        cursor = self.text_editor.textCursor()
        cursor.insertText(placeholder)
        
    def insert_unsubscribe(self):
        """Insert unsubscribe link in HTML"""
        cursor = self.html_editor.textCursor()
        cursor.insertHtml('<a href="{{unsubscribe}}">Unsubscribe</a>')
        
    def insert_unsubscribe_text(self):
        """Insert unsubscribe link in text"""
        cursor = self.text_editor.textCursor()
        cursor.insertText("{{unsubscribe}}")
        
    def add_attachment(self):
        """Add an attachment file"""
        file_paths, _ = QFileDialog.getOpenFileNames(
            self, "Select Files to Attach", "",
            "All files (*.*)"
        )
        
        for file_path in file_paths:
            if file_path not in self.attachments:
                self.attachments.append(file_path)
                self.attachments_list.addItem(Path(file_path).name)
                
    def remove_attachment(self):
        """Remove selected attachment"""
        current_row = self.attachments_list.currentRow()
        if current_row >= 0:
            self.attachments.pop(current_row)
            self.attachments_list.takeItem(current_row)
            
    def preview_template(self):
        """Preview the template"""
        QMessageBox.information(self, "Preview", "Template preview functionality will be implemented")
        
    def test_placeholders(self):
        """Test placeholder replacement"""
        QMessageBox.information(self, "Test Placeholders", "Placeholder testing functionality will be implemented")
        
    def save_template(self):
        """Save the template"""
        template_name = self.name_input.text().strip()
        if not template_name:
            QMessageBox.warning(self, "Error", "Please enter a template name")
            return
            
        # Create template directory
        template_dir = get_data_path('message') / safe_filename(template_name)
        template_dir.mkdir(exist_ok=True)
        
        # Save template metadata
        from datetime import datetime
        metadata = {
            'name': template_name,
            'created': datetime.now().isoformat(),
            'modified': datetime.now().isoformat(),
            'html_enabled': self.html_enabled.isChecked(),
            'text_enabled': self.text_enabled.isChecked(),
            'obfuscation_enabled': self.obfuscation_enabled.isChecked(),
            'emoji_rotation_enabled': self.emoji_rotation_enabled.isChecked(),
            'attachments': []
        }
        
        # Save HTML content
        if self.html_enabled.isChecked():
            html_content = self.html_editor.toHtml()
            with open(template_dir / 'email.html', 'w', encoding='utf-8') as f:
                f.write(html_content)
                
        # Save plain text content
        if self.text_enabled.isChecked():
            text_content = self.text_editor.toPlainText()
            with open(template_dir / 'plain.txt', 'w', encoding='utf-8') as f:
                f.write(text_content)
                
        # Copy attachments
        if self.attachments:
            attachments_dir = template_dir / 'attachments'
            attachments_dir.mkdir(exist_ok=True)
            
            for file_path in self.attachments:
                file_name = Path(file_path).name
                shutil.copy2(file_path, attachments_dir / file_name)
                metadata['attachments'].append(file_name)
                
        # Save metadata
        with open(template_dir / 'metadata.json', 'w', encoding='utf-8') as f:
            import json
            json.dump(metadata, f, indent=2)
            
        QMessageBox.information(self, "Success", f"Template '{template_name}' saved successfully!")
        self.accept()
        
    def load_template(self):
        """Load existing template"""
        if not self.template_name:
            return
            
        template_dir = get_data_path('message') / safe_filename(self.template_name)
        if not template_dir.exists():
            return
            
        # Load metadata
        metadata_file = template_dir / 'metadata.json'
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    import json
                    metadata = json.load(f)
                    
                self.html_enabled.setChecked(metadata.get('html_enabled', True))
                self.text_enabled.setChecked(metadata.get('text_enabled', True))
                self.obfuscation_enabled.setChecked(metadata.get('obfuscation_enabled', False))
                self.emoji_rotation_enabled.setChecked(metadata.get('emoji_rotation_enabled', False))
                
            except Exception as e:
                logging.error(f"Failed to load template metadata: {e}")
                
        # Load HTML content
        html_file = template_dir / 'email.html'
        if html_file.exists():
            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    self.html_editor.setHtml(f.read())
            except Exception as e:
                logging.error(f"Failed to load HTML content: {e}")
                
        # Load plain text content
        text_file = template_dir / 'plain.txt'
        if text_file.exists():
            try:
                with open(text_file, 'r', encoding='utf-8') as f:
                    self.text_editor.setPlainText(f.read())
            except Exception as e:
                logging.error(f"Failed to load text content: {e}")

class MessagesWidget(QWidget):
    """Message templates widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.logger = logging.getLogger(__name__)
        self.data_manager = DataManager()
        self.templates = []
        self.setup_ui()
        self.refresh_templates()
        
    def setup_ui(self):
        """Setup the messages UI"""
        layout = QVBoxLayout(self)
        
        # Title and controls
        header_layout = QHBoxLayout()
        
        title = QLabel("💬 Message Templates")
        title.setStyleSheet("font-size: 20px; font-weight: bold; margin: 10px;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Action buttons
        new_btn = QPushButton("New Template")
        new_btn.clicked.connect(self.create_template)
        header_layout.addWidget(new_btn)
        
        import_btn = QPushButton("Import Template")
        import_btn.clicked.connect(self.import_template)
        header_layout.addWidget(import_btn)
        
        layout.addLayout(header_layout)
        
        # Templates table
        self.templates_table = QTableWidget()
        self.templates_table.setColumnCount(6)
        self.templates_table.setHorizontalHeaderLabels([
            "Template Name", "Type", "Attachments", "Created", "Modified", "Actions"
        ])
        
        # Configure table
        header = self.templates_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        
        self.templates_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.templates_table.setAlternatingRowColors(True)
        
        layout.addWidget(self.templates_table)
        
        # Status bar
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
    def refresh_templates(self):
        """Refresh the templates list"""
        try:
            self.templates = self.get_templates()
            self.update_table()
            self.status_label.setText(f"Found {len(self.templates)} templates")
        except Exception as e:
            self.logger.error(f"Failed to refresh templates: {e}")
            self.status_label.setText("Error loading templates")
            
    def get_templates(self) -> List[Dict[str, Any]]:
        """Get all message templates"""
        templates = []
        messages_dir = get_data_path('message')
        
        if not messages_dir.exists():
            return templates
            
        for template_dir in messages_dir.iterdir():
            if template_dir.is_dir():
                template_info = self.get_template_info(template_dir)
                if template_info:
                    templates.append(template_info)
                    
        return templates
        
    def get_template_info(self, template_dir: Path) -> Optional[Dict[str, Any]]:
        """Get template information"""
        try:
            metadata_file = template_dir / 'metadata.json'
            if metadata_file.exists():
                import json
                with open(metadata_file, 'r', encoding='utf-8') as f:
                    metadata = json.load(f)
                    
                # Determine template type
                template_type = []
                if metadata.get('html_enabled', False):
                    template_type.append("HTML")
                if metadata.get('text_enabled', False):
                    template_type.append("Text")
                    
                return {
                    'name': metadata.get('name', template_dir.name),
                    'path': str(template_dir),
                    'type': " + ".join(template_type) if template_type else "Unknown",
                    'attachments': len(metadata.get('attachments', [])),
                    'created': metadata.get('created', 'Unknown'),
                    'modified': metadata.get('modified', 'Unknown')
                }
        except Exception as e:
            self.logger.error(f"Failed to get template info for {template_dir}: {e}")
            
        return None
        
    def update_table(self):
        """Update the templates table"""
        self.templates_table.setRowCount(len(self.templates))
        
        for row, template in enumerate(self.templates):
            # Template name
            self.templates_table.setItem(row, 0, QTableWidgetItem(template['name']))
            
            # Type
            self.templates_table.setItem(row, 1, QTableWidgetItem(template['type']))
            
            # Attachments
            self.templates_table.setItem(row, 2, QTableWidgetItem(str(template['attachments'])))
            
            # Created
            created_date = template['created']
            if 'T' in created_date:
                created_date = created_date.split('T')[0]
            self.templates_table.setItem(row, 3, QTableWidgetItem(created_date))
            
            # Modified
            modified_date = template['modified']
            if 'T' in modified_date:
                modified_date = modified_date.split('T')[0]
            self.templates_table.setItem(row, 4, QTableWidgetItem(modified_date))
            
            # Actions
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(5, 2, 5, 2)
            
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, t=template: self.edit_template(t))
            actions_layout.addWidget(edit_btn)
            
            copy_btn = QPushButton("Copy")
            copy_btn.clicked.connect(lambda checked, t=template: self.copy_template(t))
            actions_layout.addWidget(copy_btn)
            
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, t=template: self.delete_template(t))
            actions_layout.addWidget(delete_btn)
            
            self.templates_table.setCellWidget(row, 5, actions_widget)
            
    def create_template(self):
        """Create a new template"""
        dialog = TemplateEditDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_templates()
            
    def edit_template(self, template: Dict[str, Any]):
        """Edit an existing template"""
        dialog = TemplateEditDialog(template['name'], parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.refresh_templates()
            
    def copy_template(self, template: Dict[str, Any]):
        """Copy a template"""
        from PyQt6.QtWidgets import QInputDialog
        new_name, ok = QInputDialog.getText(
            self, "Copy Template", 
            f"Enter name for copy of '{template['name']}':",
            text=f"{template['name']}_copy"
        )
        
        if ok and new_name.strip():
            try:
                source_dir = Path(template['path'])
                dest_dir = get_data_path('message') / safe_filename(new_name.strip())
                
                if dest_dir.exists():
                    QMessageBox.warning(self, "Error", "A template with that name already exists")
                    return
                    
                shutil.copytree(source_dir, dest_dir)
                
                # Update metadata
                metadata_file = dest_dir / 'metadata.json'
                if metadata_file.exists():
                    import json
                    with open(metadata_file, 'r', encoding='utf-8') as f:
                        metadata = json.load(f)
                    
                    from datetime import datetime
                    metadata['name'] = new_name.strip()
                    metadata['created'] = datetime.now().isoformat()
                    metadata['modified'] = datetime.now().isoformat()
                    
                    with open(metadata_file, 'w', encoding='utf-8') as f:
                        json.dump(metadata, f, indent=2)
                        
                self.refresh_templates()
                QMessageBox.information(self, "Success", f"Template copied as '{new_name}'")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to copy template: {str(e)}")
                
    def delete_template(self, template: Dict[str, Any]):
        """Delete a template"""
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete template '{template['name']}'?\n\nThis action cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                template_dir = Path(template['path'])
                shutil.rmtree(template_dir)
                self.refresh_templates()
                QMessageBox.information(self, "Success", "Template deleted successfully")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete template: {str(e)}")
                
    def import_template(self):
        """Import a template from file"""
        QMessageBox.information(self, "Import Template", "Template import functionality will be implemented")
        
    def refresh(self):
        """Refresh the module"""
        self.refresh_templates()
        
    def get_status_info(self):
        """Get status info"""
        return f"Templates: {len(self.templates)} available"
        
    def cleanup(self):
        """Cleanup resources"""
        pass