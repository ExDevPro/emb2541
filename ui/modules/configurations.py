"""
Configurations Widget for DeepMailer v1.0

This module provides configuration management for placeholders, spintext,
unsubscribe formats, and other global application settings.
"""

import logging
from typing import Dict, List, Any
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QLineEdit,
    QSpinBox, QGroupBox, QMessageBox, QDialog, QDialogButtonBox,
    QTextEdit, QCheckBox, QProgressBar, QFrame, QSplitter, QListWidget,
    QListWidgetItem, QScrollArea, QTabWidget, QFormLayout, QPlainTextEdit
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QColor

from core.utils import load_config, save_config

class PlaceholderConfigWidget(QWidget):
    """Widget for configuring custom placeholders"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = load_config()
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        """Setup the placeholder configuration UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Custom Placeholders Configuration")
        title.setObjectName("section-title")
        layout.addWidget(title)
        
        # Tab widget for different placeholder types
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Domain placeholders
        self.setup_domains_tab()
        
        # Campaign names
        self.setup_campaigns_tab()
        
        # Batch names
        self.setup_batches_tab()
        
        # Custom strings
        self.setup_custom_strings_tab()
        
        # List names
        self.setup_list_names_tab()
        
        # Save button
        save_btn = QPushButton("Save Configuration")
        save_btn.clicked.connect(self.save_configuration)
        layout.addWidget(save_btn)
        
    def setup_domains_tab(self):
        """Setup domains configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        info_label = QLabel("Configure domains for {{domain}} placeholder rotation:")
        layout.addWidget(info_label)
        
        self.domains_edit = QPlainTextEdit()
        self.domains_edit.setPlaceholderText("Enter one domain per line:\nexample.com\nmydomain.com\ncompany.org")
        layout.addWidget(self.domains_edit)
        
        self.tab_widget.addTab(widget, "Domains")
        
    def setup_campaigns_tab(self):
        """Setup campaign names configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        info_label = QLabel("Configure campaign names for {{campaign}} placeholder:")
        layout.addWidget(info_label)
        
        self.campaigns_edit = QPlainTextEdit()
        self.campaigns_edit.setPlaceholderText("Enter one campaign name per line:\nSummerSale2025\nBlackFridayPromo\nWelcomeSeries")
        layout.addWidget(self.campaigns_edit)
        
        self.tab_widget.addTab(widget, "Campaign Names")
        
    def setup_batches_tab(self):
        """Setup batch names configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        info_label = QLabel("Configure batch names for {{batch}} placeholder:")
        layout.addWidget(info_label)
        
        self.batches_edit = QPlainTextEdit()
        self.batches_edit.setPlaceholderText("Enter one batch name per line:\nBatch1\nBatch2\nBatch3")
        layout.addWidget(self.batches_edit)
        
        self.tab_widget.addTab(widget, "Batch Names")
        
    def setup_custom_strings_tab(self):
        """Setup custom strings configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        info_label = QLabel("Configure custom strings for {{custom_string}} placeholder:")
        layout.addWidget(info_label)
        
        self.custom_strings_edit = QPlainTextEdit()
        self.custom_strings_edit.setPlaceholderText("Enter one custom string per line:\nCustom1\nCustom2\nCustom3")
        layout.addWidget(self.custom_strings_edit)
        
        self.tab_widget.addTab(widget, "Custom Strings")
        
    def setup_list_names_tab(self):
        """Setup list names configuration tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        info_label = QLabel("Configure list names for {{list_name}} placeholder:")
        layout.addWidget(info_label)
        
        self.list_names_edit = QPlainTextEdit()
        self.list_names_edit.setPlaceholderText("Enter one list name per line:\nList1\nList2\nList3")
        layout.addWidget(self.list_names_edit)
        
        self.tab_widget.addTab(widget, "List Names")
        
    def load_data(self):
        """Load current configuration data"""
        placeholders = self.config.get('placeholders', {})
        
        # Load domains
        domains = placeholders.get('domains', [])
        self.domains_edit.setPlainText('\n'.join(domains))
        
        # Load campaigns
        campaigns = placeholders.get('campaigns', [])
        self.campaigns_edit.setPlainText('\n'.join(campaigns))
        
        # Load batches
        batches = placeholders.get('batch_names', [])
        self.batches_edit.setPlainText('\n'.join(batches))
        
        # Load custom strings
        custom_strings = placeholders.get('custom_strings', [])
        self.custom_strings_edit.setPlainText('\n'.join(custom_strings))
        
        # Load list names
        list_names = placeholders.get('list_names', [])
        self.list_names_edit.setPlainText('\n'.join(list_names))
        
    def save_configuration(self):
        """Save the placeholder configuration"""
        try:
            # Get current config
            config = load_config()
            
            # Update placeholders
            if 'placeholders' not in config:
                config['placeholders'] = {}
                
            # Save domains
            domains_text = self.domains_edit.toPlainText().strip()
            config['placeholders']['domains'] = [line.strip() for line in domains_text.split('\n') if line.strip()]
            
            # Save campaigns
            campaigns_text = self.campaigns_edit.toPlainText().strip()
            config['placeholders']['campaigns'] = [line.strip() for line in campaigns_text.split('\n') if line.strip()]
            
            # Save batches
            batches_text = self.batches_edit.toPlainText().strip()
            config['placeholders']['batch_names'] = [line.strip() for line in batches_text.split('\n') if line.strip()]
            
            # Save custom strings
            custom_strings_text = self.custom_strings_edit.toPlainText().strip()
            config['placeholders']['custom_strings'] = [line.strip() for line in custom_strings_text.split('\n') if line.strip()]
            
            # Save list names
            list_names_text = self.list_names_edit.toPlainText().strip()
            config['placeholders']['list_names'] = [line.strip() for line in list_names_text.split('\n') if line.strip()]
            
            # Save configuration
            save_config(config)
            self.config = config
            
            QMessageBox.information(self, "Success", "Placeholder configuration saved successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save configuration: {str(e)}")

class SpintextConfigWidget(QWidget):
    """Widget for configuring spintext"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = load_config()
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        """Setup the spintext configuration UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Spintext Configuration")
        title.setObjectName("section-title")
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel("""
<b>Spintext Format:</b> {{{word}}} will be replaced with random variations<br>
<b>Configuration Format:</b> word = option1|option2|option3<br>
<b>Example:</b> amazing = amazing|fantastic|incredible|awesome
        """)
        instructions.setWordWrap(True)
        instructions.setObjectName("help-text")
        layout.addWidget(instructions)
        
        # Controls
        controls_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Spintext")
        add_btn.clicked.connect(self.add_spintext)
        controls_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("Edit Selected")
        edit_btn.clicked.connect(self.edit_spintext)
        controls_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self.delete_spintext)
        controls_layout.addWidget(delete_btn)
        
        controls_layout.addStretch()
        
        test_btn = QPushButton("Test Spintext")
        test_btn.clicked.connect(self.test_spintext)
        controls_layout.addWidget(test_btn)
        
        layout.addLayout(controls_layout)
        
        # Spintext table
        self.spintext_table = QTableWidget()
        self.spintext_table.setColumnCount(2)
        self.spintext_table.setHorizontalHeaderLabels(["Main Word", "Variations"])
        
        header = self.spintext_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        
        self.spintext_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        layout.addWidget(self.spintext_table)
        
        # Save button
        save_btn = QPushButton("Save Spintext Configuration")
        save_btn.clicked.connect(self.save_configuration)
        layout.addWidget(save_btn)
        
    def load_data(self):
        """Load spintext data"""
        spintext = self.config.get('spintext', {})
        
        self.spintext_table.setRowCount(len(spintext))
        
        for row, (word, variations) in enumerate(spintext.items()):
            self.spintext_table.setItem(row, 0, QTableWidgetItem(word))
            self.spintext_table.setItem(row, 1, QTableWidgetItem(variations))
            
    def add_spintext(self):
        """Add new spintext entry"""
        dialog = SpintextEditDialog(parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            word, variations = dialog.get_data()
            
            row = self.spintext_table.rowCount()
            self.spintext_table.insertRow(row)
            self.spintext_table.setItem(row, 0, QTableWidgetItem(word))
            self.spintext_table.setItem(row, 1, QTableWidgetItem(variations))
            
    def edit_spintext(self):
        """Edit selected spintext entry"""
        current_row = self.spintext_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a spintext entry to edit")
            return
            
        word_item = self.spintext_table.item(current_row, 0)
        variations_item = self.spintext_table.item(current_row, 1)
        
        if not word_item or not variations_item:
            return
            
        dialog = SpintextEditDialog(word_item.text(), variations_item.text(), parent=self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            word, variations = dialog.get_data()
            word_item.setText(word)
            variations_item.setText(variations)
            
    def delete_spintext(self):
        """Delete selected spintext entry"""
        current_row = self.spintext_table.currentRow()
        if current_row >= 0:
            self.spintext_table.removeRow(current_row)
            
    def test_spintext(self):
        """Test spintext replacement"""
        current_row = self.spintext_table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Warning", "Please select a spintext entry to test")
            return
            
        word_item = self.spintext_table.item(current_row, 0)
        variations_item = self.spintext_table.item(current_row, 1)
        
        if not word_item or not variations_item:
            return
            
        word = word_item.text()
        variations = variations_item.text().split('|')
        
        import random
        sample_text = f"This is a {{{{{word}}}}} example!"
        result_text = sample_text.replace(f"{{{{{word}}}}}", random.choice(variations))
        
        QMessageBox.information(self, "Spintext Test", 
                               f"Original: {sample_text}\n\nResult: {result_text}")
        
    def save_configuration(self):
        """Save spintext configuration"""
        try:
            config = load_config()
            
            # Build spintext dictionary
            spintext = {}
            for row in range(self.spintext_table.rowCount()):
                word_item = self.spintext_table.item(row, 0)
                variations_item = self.spintext_table.item(row, 1)
                
                if word_item and variations_item:
                    word = word_item.text().strip()
                    variations = variations_item.text().strip()
                    if word and variations:
                        spintext[word] = variations
                        
            config['spintext'] = spintext
            save_config(config)
            self.config = config
            
            QMessageBox.information(self, "Success", "Spintext configuration saved successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save spintext configuration: {str(e)}")

class SpintextEditDialog(QDialog):
    """Dialog for editing spintext entries"""
    
    def __init__(self, word: str = "", variations: str = "", parent=None):
        super().__init__(parent)
        self.word = word
        self.variations = variations
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the dialog UI"""
        self.setWindowTitle("Edit Spintext")
        self.setModal(True)
        self.resize(500, 300)
        
        layout = QVBoxLayout(self)
        
        # Word input
        layout.addWidget(QLabel("Main Word:"))
        self.word_input = QLineEdit()
        self.word_input.setText(self.word)
        self.word_input.setPlaceholderText("e.g., amazing")
        layout.addWidget(self.word_input)
        
        # Variations input
        layout.addWidget(QLabel("Variations (separated by |):"))
        self.variations_input = QPlainTextEdit()
        self.variations_input.setPlainText(self.variations)
        self.variations_input.setPlaceholderText("e.g., amazing|fantastic|incredible|awesome")
        self.variations_input.setMaximumHeight(100)
        layout.addWidget(self.variations_input)
        
        # Help text
        help_text = QLabel("Each variation will be randomly selected when {{{word}}} is used in templates")
        help_text.setObjectName("help-text")
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
        
    def get_data(self):
        """Get the entered data"""
        return self.word_input.text().strip(), self.variations_input.toPlainText().strip()

class UnsubscribeConfigWidget(QWidget):
    """Widget for configuring unsubscribe formats"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = load_config()
        self.setup_ui()
        self.load_data()
        
    def setup_ui(self):
        """Setup the unsubscribe configuration UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Unsubscribe Link Configuration")
        title.setObjectName("section-title")
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel("""
Configure multiple unsubscribe link formats. When using {{unsubscribe}} placeholder,
a random format will be selected from the list below.
        """)
        instructions.setWordWrap(True)
        instructions.setObjectName("help-text")
        layout.addWidget(instructions)
        
        # Formats editor
        layout.addWidget(QLabel("Unsubscribe Formats (one per line):"))
        self.formats_edit = QPlainTextEdit()
        self.formats_edit.setPlaceholderText("""<mailto:unsubscribe@{{domain}}>
<https://{{domain}}/unsubscribe?email={email}>
<https://{{domain}}/unsubscribe/{{token}}>
<mailto:unsubscribe@yourdomain.com>
<mailto:{{FakerFullName}}@{{domain}}>""")
        layout.addWidget(self.formats_edit)
        
        # Examples
        examples = QLabel("""
<b>Examples:</b><br>
• <code>&lt;mailto:unsubscribe@{{domain}}&gt;</code> - Simple mailto link<br>
• <code>&lt;https://{{domain}}/unsubscribe?email={email}&gt;</code> - Web link with email<br>
• <code>&lt;https://{{domain}}/unsubscribe/{{token}}&gt;</code> - Web link with token<br>
• <code>&lt;mailto:{{campaign}}@{{domain}}&gt;</code> - Campaign-specific mailto
        """)
        examples.setWordWrap(True)
        examples.setObjectName("help-text")
        layout.addWidget(examples)
        
        # Save button
        save_btn = QPushButton("Save Unsubscribe Configuration")
        save_btn.clicked.connect(self.save_configuration)
        layout.addWidget(save_btn)
        
    def load_data(self):
        """Load unsubscribe formats"""
        formats = self.config.get('unsubscribe_formats', [])
        self.formats_edit.setPlainText('\n'.join(formats))
        
    def save_configuration(self):
        """Save unsubscribe configuration"""
        try:
            config = load_config()
            
            formats_text = self.formats_edit.toPlainText().strip()
            formats = [line.strip() for line in formats_text.split('\n') if line.strip()]
            
            config['unsubscribe_formats'] = formats
            save_config(config)
            self.config = config
            
            QMessageBox.information(self, "Success", "Unsubscribe configuration saved successfully!")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save unsubscribe configuration: {str(e)}")

class ConfigurationsWidget(QWidget):
    """Configurations widget"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent_window = parent
        self.logger = logging.getLogger(__name__)
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the configurations UI"""
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("⚙️ Configurations")
        title.setObjectName("page-title")
        layout.addWidget(title)
        
        # Tab widget for different configuration sections
        tab_widget = QTabWidget()
        
        # Placeholders tab
        placeholder_widget = PlaceholderConfigWidget(self)
        tab_widget.addTab(placeholder_widget, "Placeholders")
        
        # Spintext tab
        spintext_widget = SpintextConfigWidget(self)
        tab_widget.addTab(spintext_widget, "Spintext")
        
        # Unsubscribe tab
        unsubscribe_widget = UnsubscribeConfigWidget(self)
        tab_widget.addTab(unsubscribe_widget, "Unsubscribe")
        
        layout.addWidget(tab_widget)
        
        # Status
        self.status_label = QLabel("Configuration ready")
        layout.addWidget(self.status_label)
        
    def refresh(self):
        """Refresh the module"""
        self.status_label.setText("Configuration refreshed")
        
    def get_status_info(self):
        """Get status info"""
        config = load_config()
        placeholder_count = len(config.get('placeholders', {}).get('domains', []))
        spintext_count = len(config.get('spintext', {}))
        unsubscribe_count = len(config.get('unsubscribe_formats', []))
        
        return f"Config: {placeholder_count} domains, {spintext_count} spintexts, {unsubscribe_count} unsubscribe formats"
        
    def cleanup(self):
        """Cleanup resources"""
        pass