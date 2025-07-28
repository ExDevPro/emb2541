# DeepMailer v1.0

## Project Overview

DeepMailer v1.0 is a comprehensive Windows-based email marketing and campaign management software designed for professional email marketing campaigns. Built with Python PyQt6 and featuring a modern, customizable interface, this software provides advanced email sending capabilities with extensive personalization, automation, and anti-detection features.

## 🎯 Key Features

### ✨ Core Functionality
- **Multi-Campaign Management**: Run multiple email campaigns simultaneously with independent threading
- **Advanced SMTP Management**: Support for unlimited SMTP servers with rotation, limits, and proxy support
- **Lead Management**: Import, edit, and manage unlimited email leads with CSV/Excel/Text support
- **Template Engine**: WYSIWYG HTML email editor with full customization capabilities
- **Subject Line Management**: Advanced subject line rotation and personalization
- **Real-time Analytics**: Live campaign tracking and detailed reporting

### 🔧 Advanced Features
- **Smart Placeholders**: 80+ built-in placeholders including Faker data generation
- **Spintext Support**: Dynamic content variation for improved deliverability
- **Custom Headers**: Extensive email header customization for better inbox placement
- **Fingerprint Obfuscation**: Anti-detection technology to bypass spam filters
- **Flexible Sending Modes**: Single, Batch, Scheduled, and Spike sending modes
- **Proxy Support**: Full proxy integration for enhanced anonymity

## 📋 Technical Requirements

### System Requirements
- **Operating System**: Windows 10/11 only
- **Programming Language**: Python with PyQt6
- **UI Framework**: QSS-based theming system
- **Architecture**: Multithreaded with separated core logic and GUI

### Key Technical Features
- **Compilation Compatibility**: Full support for Nuitka, Cython, and PyInstaller
- **No External Dependencies**: No database required - JSON-based data storage
- **Real-time Data Persistence**: Automatic saving prevents data loss
- **Professional UI**: Embedded browser components, loading animations, responsive design
- **Resource Management**: Structured image, theme, and font organization

## 🏗️ Architecture

### File Structure
```
ProjectDirectory/
├── Data/
│   ├── Leads/                      # Lead data storage
│   ├── SMTP/                       # SMTP server configurations
│   ├── Subject/                    # Subject line collections
│   ├── Message/TemplateName/       # Email templates and attachments
│   ├── Campaigns/CampaignName/     # Campaign data and reports
│   ├── Settings/                   # Application settings
│   └── Logs/                       # Error and runtime logs
└── Resource/
    ├── Images/                     # Icons and images
    ├── Theme/                      # QSS theme files
    └── Fonts/                      # Custom fonts
```

## 📧 Placeholder System

### Lead Column Placeholders
- **Syntax**: `{column_name}`
- **Purpose**: References columns from uploaded leads files
- **Example**: `{email}`, `{first_name}`, `{company}`
- **Case Insensitive**: Automatically detects `{EMAIL}`, `{Email}`, or `{email}`

### Default System Placeholders
- **Syntax**: `{{placeholder}}`
- **80+ Built-in Placeholders** including:

#### Faker Data Placeholders
- `{{FakerFirstName}}`, `{{FakerLastName}}`, `{{FakerFullName}}`
- `{{FakerEmail}}`, `{{FakerCompany}}`, `{{FakerJobTitle}}`
- `{{FakerPhone}}`, `{{FakerAddress}}`, `{{FakerCity}}`, `{{FakerCountry}}`
- `{{FakerUUID}}`, `{{FakerIPv4}}`, `{{FakerUserAgent}}`
- `{{FakerDate}}`, `{{FakerTime}}`, `{{FakerUrl}}`

#### System Data Placeholders
- `{{timestamp}}` - Current time
- `{{date}}` - Current date
- `{{year}}`, `{{month}}`, `{{day}}`, `{{hour}}`, `{{minute}}`, `{{second}}`
- `{{uuid}}` - System-generated unique ID for each recipient
- `{{token}}` - Unique token for each recipient/email/lead
- `{{counter}}` - Incrementing number for each email sent
- `{{sequence}}` - Sequential numbering

#### Custom Data Placeholders
- `{{domain}}` - Rotates through user-defined domains
- `{{campaign}}` - Campaign names (user-configurable)
- `{{batch}}` - Batch identifiers (user-configurable)
- `{{custom_string}}` - Custom text strings (user-configurable)
- `{{list_name}}` - List names (user-configurable)

#### Utility Placeholders
- `{{hash}}` - Customizable hash (MD5, SHA256, random)
- `{{random}}` - Random numbers/words (configurable length)
- `{{random_alphanum}}` - Random alphanumeric (min/max length)
- `{{ENCODED_URL}}` - Auto-generated tracking links
- `{{subject}}` - Current email subject
- `{{email}}` - Receiver email address
- `{{user_id}}` - Unique receiver user ID
- `{{unsubscribe}}` - Auto-generated unsubscribe links

### Spintext System
- **Syntax**: `{{{word}}}`
- **Purpose**: Dynamic content variation for improved deliverability
- **Configuration**: Pipe-separated variations (`option1|option2|option3`)
- **Example**: `{{{struggling}}}` → randomly selects from "struggling|having trouble|facing challenges|finding it hard"

## 🔧 Core Modules

### 1. Lead Management
- **Import/Export**: CSV, Excel, Text file support
- **Smart Duplicate Detection**: Automatic duplicate removal with user options
- **Inline Editing**: Direct table editing with real-time saving
- **Bulk Operations**: Mass edit, delete, and export capabilities
- **Pagination**: Optimized for handling millions of records
- **Search/Filter**: Advanced filtering and search capabilities
- **Column Management**: Add/remove columns, type detection
- **Real-time Validation**: Email format validation and statistics

### 2. SMTP Management
- **Multi-Server Support**: Unlimited SMTP servers with individual configurations
- **Authentication Methods**: Auto, PLAIN, LOGIN, CRAM-MD5
- **Security Types**: Auto, None, SSL, TLS
- **Header Customization**: 
  - From Name with rotation (Custom/Faker options)
  - Reply-To with rotation (Custom/Faker options)
  - Rotation policies: Each time, After X-Y sends, Random usage
- **Proxy Integration**: 
  - Support for HTTP, HTTPS, SOCKS5 proxies
  - Authentication support
  - Multiple proxy rotation
  - Fallback options
- **Rate Limiting**: 
  - Per minute, hourly, daily, weekly, monthly limits
  - Total usage limits
  - Automatic status management
- **Connection Testing**: Built-in SMTP testing and validation

### 3. Subject Line Management
- **Multiple Lists**: Unlimited subject line lists
- **Import/Export**: CSV, Excel, Text support with auto-conversion
- **Personalization**: Full placeholder and spintext support
- **Emoji Support**: Unicode emoji compatibility
- **Duplicate Management**: Automatic duplicate removal
- **Preview Functionality**: Real-time preview with placeholder rendering
- **Bulk Operations**: Mass edit, delete, import capabilities
- **Search/Filter**: Advanced subject line filtering

### 4. Message Templates
- **WYSIWYG Editor**: Full-featured HTML email editor with live preview
- **Content Types**: HTML, Plain Text, Attachments-only, or combinations
- **Attachment Support**: Multiple file attachments per template
- **Personalization**: Full placeholder and spintext integration
- **Unsubscribe Integration**: Built-in unsubscribe link management
- **Advanced Features**:
  - Fingerprint Obfuscation for anti-detection
  - Emoji Rotation for natural variation
  - Template organization in dedicated folders
  - Metadata storage for configurations

### 5. Campaign Management
- **Multi-Campaign Support**: Run multiple independent campaigns
- **SMTP Configuration**: 
  - Multi-SMTP selection and rotation
  - Rotation modes: Each mail, Custom ranges
  - Automatic limit respect
- **Lead Configuration**:
  - Sending sequences: First-to-Last, Last-to-First, Random, Domain-based
  - Domain-based sending with reordering
  - No duplicate sending guarantee
- **Subject Configuration**:
  - Multiple subject selection and rotation
  - Custom rotation patterns
- **Template Configuration**:
  - Multiple template rotation
  - Attachment handling
- **Tracking Integration**:
  - Custom tracking domain support
  - Open/Click tracking configuration
  - API integration for tracking data

### 6. Sending Modes
- **Single Mode**: One-by-one sending with configurable delays (seconds/minutes/hours)
- **Batch Mode**: Group sending with batch size ranges and delays
- **Date & Time Mode**: Scheduled sending within specific time windows
- **Spike Mode**: Day-by-day sending plans with daily email limits

### 7. Advanced Headers
Comprehensive email header management including:
- **Message-ID**: Multiple format options with domain rotation
- **X-Tracking-ID**: Custom tracking identifiers
- **X-Campaign-ID**: Campaign identification headers
- **X-UID**: Unique identifier headers
- **X-Mailer**: Email client simulation (80+ options)
- **X-Origin**: Origin server identification
- **X-Email-Type**: Email type classification
- **X-Campaign-Name**: Campaign naming headers
- **Auto-Submitted**: Automatic submission flags
- **Precedence**: Email precedence levels
- **Priority/X-Priority**: Email priority settings
- **Importance**: Message importance levels
- **X-Auto-Response-Suppress**: Auto-response suppression
- **List-Unsubscribe**: RFC-compliant unsubscribe headers with one-click support
- **Custom Headers**: User-defined header addition

Each header includes:
- Enable/Disable options
- Format rotation (Each mail/Custom ranges)
- Header use policy (Must use/Optional with random application)

## 📊 Reporting & Analytics

### Real-time Dashboard
- **Live Counters**: 
  - Total Leads, Subjects, SMTPs, Templates
  - Sent Success/Failed counts
  - Remaining emails
  - Open/Click tracking (when enabled)
- **Progress Visualization**: Real-time progress bars and percentages
- **Campaign Status**: Live status updates for all running campaigns

### Detailed Reports
- **Export Formats**: Excel, CSV with customizable columns
- **Data Included**: 
  - SMTP server used
  - Headers applied
  - Templates used
  - Complete lead data
  - Timestamps and status
- **Auto-saving**: Continuous CSV report updates during campaigns
- **Campaign History**: Complete sending logs and historical statistics

## ⚙️ Configuration System

### Default Placeholders Configuration
- **Case-insensitive Detection**: Automatic placeholder recognition
- **User-configurable Values**: Custom placeholder definitions
- **Rotation Settings**: Configurable rotation for dynamic content
- **Domain Management**: Multiple domain rotation system
- **Hash Algorithms**: User-selectable hash algorithms (MD5, SHA256, random)

### Spintext Configuration
- **Unlimited Entries**: No limit on spintext definitions
- **Pipe-separated Variations**: Easy format for multiple options
- **Main Word Mapping**: Clear word-to-variations relationship
- **Global Library**: Centralized spintext management
- **Add More Functionality**: Dynamic spintext addition

### Unsubscribe Configuration
Multiple format support including:
- `<mailto:unsubscribe@domain.com>`
- `<mailto:{{FakerFullName}}@{{domain}}>`
- `<https://domain.com/unsubscribe?email={email}>`
- `<https://domain.com/unsubscribe/{{token}}>`
- Combined formats for multiple options

### Theme System
- **QSS-based Styling**: Professional theme management
- **Switchable Themes**: Runtime theme switching
- **Custom Theme Support**: User-created theme import
- **Resource Management**: JSON-based resource path management

## 🔒 Security & Compliance

### Anti-Detection Features
- **Fingerprint Obfuscation**: 
  - Invisible HTML modifications
  - Random CSS styles
  - HTML comments insertion
  - Unique fingerprint per email
- **Header Randomization**: Dynamic header generation and rotation
- **Content Variation**: Spintext and emoji rotation for natural appearance
- **Sending Pattern Obfuscation**: Random delays and SMTP rotation

### Code Protection
- **Compilation Ready**: Full compatibility with Nuitka, Cython, PyInstaller
- **Resource Protection**: Secure bundling of assets and configurations
- **No External Dependencies**: Self-contained execution environment
- **Clean Architecture**: Separated core logic for future web version

## 🎨 User Interface

### Design Principles
- **Professional Appearance**: Commercial-grade UI without emojis
- **Responsive Design**: Automatic adaptation to different screen sizes
- **Resource Management**: External SVG/PNG icons with JSON path management
- **Loading Animations**: Professional loading indicators for all operations
- **Embedded Browser**: Internal browser component (CEF/Chromium)

### Layout Structure
- **Left Panel Navigation**:
  - Dashboard (default)
  - Leads Management
  - SMTP Configuration
  - Subject Management
  - Message Templates
  - Campaign Management
  - Configuration Settings
  - Application Settings

- **Right Panel Content**: Dynamic content area showing:
  - Table views (Excel-style)
  - Configuration forms
  - Real-time statistics
  - Campaign controls

### User Experience Features
- **Real-time Updates**: Instant data persistence
- **Non-blocking Operations**: Background threads for all tasks
- **Multi-campaign Support**: Independent campaign management
- **Professional Controls**: Start, Stop, Pause, Resume functionality
- **Draft Saving**: Campaign configuration preservation

## 📚 Documentation Requirements

### Technical Documentation
Upon completion, two comprehensive documentation sets will be provided:

#### 1. Compilation Guide
- **Complete .exe Creation Instructions**: Step-by-step compilation process
- **Environment Setup**: Dependency and configuration management
- **Compilation Commands**: Nuitka, PyInstaller, Cython specific instructions
- **Resource Handling**: Proper bundling of images, themes, and JSON files
- **Troubleshooting Guide**: Common compilation issues and solutions
- **Testing Procedures**: Verification of compiled executable functionality

#### 2. User Manual
- **Comprehensive Feature Guide**: Human-readable explanations of all features
- **Step-by-step Instructions**: Detailed usage procedures
- **Configuration Examples**: Practical implementation scenarios
- **Setting Interactions**: How different options affect each other
- **Best Practices**: Optimal usage recommendations
- **Troubleshooting**: Common user issues and solutions

## 🚀 Installation & Development

### Development Environment
- **Python 3.8+** with PyQt6 framework
- **Faker Library** for realistic data generation
- **QSS Styling** for professional UI theming
- **Threading Libraries** for concurrent operations
- **JSON Processing** for configuration management

### Compilation Requirements
- **Nuitka/PyInstaller/Cython** compatibility
- **Resource Bundling** configuration for assets
- **Icon Management** for executable branding
- **Optimization Settings** for performance

### File Permissions & Storage
- **Same Directory Storage**: All data files in executable directory
- **Auto-creation**: Automatic folder/file creation on first run
- **Real-time Persistence**: Immediate data saving
- **Backup-friendly Structure**: Organized file hierarchy

## 📋 Technical Clarifications

### Architecture Decisions
- **Individual SMTP Storage**: Each SMTP as separate JSON file
- **Embedded Browser**: CEF/Chromium integration within application
- **Threading Model**: Individual threads per campaign for isolation
- **Configuration Management**: Both file-based and GUI-editable settings
- **Data Persistence**: Auto-save and manual save options

### Email Handling
- **Direct SMTP Implementation**: Native SMTP protocol handling
- **Error Management**: Comprehensive logging, notifications, retry mechanisms
- **Queue Optimization**: Efficient handling of high-volume sending
- **Limit Enforcement**: Automatic SMTP limit monitoring and enforcement

This specification ensures DeepMailer v1.0 will be a professional-grade email marketing solution with enterprise-level features, security, and reliability suitable for commercial use.