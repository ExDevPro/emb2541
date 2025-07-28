# DeepMailer v1.0

## Project Overview

DeepMailer v1.0 is a comprehensive Windows-based email marketing and campaign management software designed for professional email marketing campaigns. Built with Python PyQt6 and featuring QSS-based theme customization, this desktop application provides advanced email sending capabilities with extensive personalization, automation, and anti-detection features.

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
- **UI Framework**: QSS-based theming system with switchable themes from settings
- **Architecture**: Multithreaded with separated core logic and GUI for future web version compatibility

### Key Technical Features
- **Compilation Compatibility**: Full support for Nuitka, Cython, and PyInstaller
- **No External Dependencies**: No database required - JSON-based data storage
- **Real-time Data Persistence**: Automatic saving prevents data loss
- **Professional Desktop UI**: QSS-styled interface with loading animations and responsive design
- **Resource Management**: Structured image, theme, and font organization with JSON path management

## 🏗️ Application Architecture & UI Layout

### Main Application Layout
**Left Panel Navigation:**
- **Dashboard** (default selection) - Overview and statistics
- **Leads** - Lead management and import/export
- **SMTPs** - SMTP server configuration and testing  
- **Subject** - Subject line management and rotation
- **Messages** - Email template creation and management
- **Campaigns** - Campaign setup and execution
- **Configurations** - Default placeholders and spintext settings
- **Settings** - Application settings and theme management

**Right Panel Content:**
- **Dynamic Content Area**: Changes based on left panel selection
- **Table Views**: Excel-style data presentation for leads, SMTPs, subjects
- **Configuration Forms**: Comprehensive setup interfaces
- **Real-time Statistics**: Live counters and progress indicators
- **Campaign Controls**: Start, stop, pause, resume functionality

### Dashboard Features
**Default Landing Page:**
- **Primary Interface**: Automatically selected when application opens
- **Comprehensive Overview**: Complete software status and statistics display

**Real-time Counters:**
- **Data Counters**:
  - Total Leads across all lists
  - Total Subjects across all lists  
  - Total SMTP servers configured
  - Total Message Templates created
- **Campaign Statistics**:
  - Active campaigns count
  - Total emails sent (success)
  - Total emails failed with error counts
  - Remaining emails in queue
- **Tracking Statistics** (when enabled):
  - Total Opens count
  - Total Clicks count
  - Tracking status indicators

**Visual Elements:**
- **Professional Layout**: Clean, commercial-grade interface without emojis
- **Progress Indicators**: Real-time progress bars for active campaigns
- **Status Badges**: Color-coded status indicators for SMTPs, campaigns
- **Live Updates**: All counters refresh automatically without page reload
- **Quick Navigation**: Direct access buttons to frequently used sections

**Performance Monitoring:**
- **System Status**: Application performance indicators
- **Memory Usage**: Resource utilization display
- **Thread Status**: Multi-campaign thread monitoring
- **Error Summary**: Recent error counts and quick access to logs

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

#### Faker Data Placeholders (80+ Available)
**Personal Data:**
- `{{FakerFirstName}}`, `{{FakerLastName}}`, `{{FakerFullName}}`
- `{{FakerGender}}`, `{{FakerEmail}}`, `{{FakerUsername}}`, `{{FakerPassword}}`

**Company & Professional:**
- `{{FakerCompany}}`, `{{FakerCompanySuffix}}`, `{{FakerJobTitle}}`

**Contact Information:**
- `{{FakerPhone}}`, `{{FakerPhoneNumber}}`

**Location Data:**
- `{{FakerCity}}`, `{{FakerState}}`, `{{FakerCountry}}`, `{{FakerCountryCode}}`
- `{{FakerAddress}}`, `{{FakerStreetName}}`, `{{FakerStreetAddress}}`
- `{{FakerBuildingNumber}}`, `{{FakerPostcode}}`
- `{{FakerLatitude}}`, `{{FakerLongitude}}`

**Date & Time:**
- `{{FakerDate}}`, `{{FakerTime}}`, `{{FakerDateTime}}`
- `{{FakerDayOfWeek}}`, `{{FakerMonthName}}`, `{{FakerYear}}`

**Internet & Technology:**
- `{{FakerUrl}}`, `{{FakerUUID}}`, `{{FakerUserAgent}}`
- `{{FakerIPv4}}`, `{{FakerIPv6}}`, `{{FakerMACAddress}}`

**Design & Content:**
- `{{FakerColor}}`, `{{FakerHexColor}}`, `{{FakerSlug}}`

**Localization:**
- `{{FakerLocale}}`, `{{FakerTimezone}}`, `{{FakerLanguageCode}}`

**Financial:**
- `{{FakerCurrencyCode}}`, `{{FakerIBAN}}`, `{{FakerBIC}}`

**Email Types:**
- `{{FakerAsciiSafeEmail}}`, `{{FakerFreeEmail}}`, `{{FakerSafeEmail}}`

**Data & Boolean:**
- `{{FakerBoolean}}`

**Text Generation:**
- `{{FakerWord}}`, `{{FakerWords}}`, `{{FakerSentence}}`
- `{{FakerParagraph}}`, `{{FakerText}}`

**Numbers:**
- `{{FakerRandomNumber}}`, `{{FakerDigit}}`, `{{FakerNumberBetween}}`

#### System Data Placeholders
- `{{timestamp}}` - Current time
- `{{date}}` - Current date  
- `{{year}}`, `{{month}}`, `{{day}}`, `{{hour}}`, `{{minute}}`, `{{second}}`
- `{{uuid}}` - System-generated unique ID for each recipient
- `{{token}}` - Unique token for each recipient/email/lead
- `{{counter}}` - Incrementing number for each email sent (user-configurable starting number)
- `{{sequence}}` - Sequential numbering
- `{{subject}}` - Current email subject being used
- `{{email}}` - Receiver email address
- `{{user_id}}` - Unique receiver user ID for each lead

#### Custom Data Placeholders
- `{{domain}}` - Rotates through user-defined domains (multiple domains, one per line)
- `{{campaign}}` - Campaign names (user-configurable, one per line)
- `{{batch}}` - Batch identifiers (user-configurable, one per line)
- `{{custom_string}}` - Custom text strings (user-configurable, one per line)
- `{{list_name}}` - List names (user-configurable, one per line)

#### Utility Placeholders
- `{{hash}}` - Customizable hash algorithms (MD5, SHA256, random - user selectable)
- `{{random}}` - Random numbers/words (user-configurable length and type)
- `{{random_alphanum}}` - Random alphanumeric strings (configurable min/max length)
- `{{ENCODED_URL}}` - Auto-generated tracking links based on template links
- `{{unsubscribe}}` - Auto-generated unsubscribe links with multiple format support

### Spintext System
- **Syntax**: `{{{word}}}`
- **Purpose**: Dynamic content variation for improved deliverability
- **Configuration**: Pipe-separated variations (`option1|option2|option3`)
- **Example**: `{{{struggling}}}` → randomly selects from "struggling|having trouble|facing challenges|finding it hard"

## 🎯 Campaign Setup & Execution

### Campaign Creation & Management
**Campaign List Interface:**
- **Campaign Overview**: Right panel displays all campaigns in organized list view
- **Campaign Selection**: Click any campaign to view detailed tab with progress, counters, and controls
- **Quick Actions**: Delete campaigns or create new ones with dedicated buttons  
- **Campaign Description**: Short description display area for selected campaign

**New Campaign Creation:**
- **Campaign Details**: Name and optional description input
- **Instant Setup**: Immediate campaign creation and list addition
- **Configuration Ready**: Direct access to comprehensive campaign setup options

### SMTP Selection & Configuration
**Multi-SMTP Support:**
- **SMTP Selection**: Dropdown with checkbox selection for multiple SMTP servers
- **Configuration Options**: Dedicated "Configuration" button for rotation settings
- **SMTP Rotation Modes**:
  - **Each Mail**: Automatic rotation through selected SMTPs for every email
  - **Custom Range**: Define rotation range (e.g., 10-15 emails per SMTP before rotating)
- **Limit Enforcement**: Automatic respect for individual SMTP sending limits and headers
- **Failure Handling**: Campaign stops with error message when all SMTP limits exceeded

### Lead Configuration & Sending Sequences
**Lead List Selection:**
- **List Dropdown**: Choose from all available lead lists
- **Sending Sequence Configuration**: Multiple ordering options via configuration button
- **Sequence Options**:
  - **First to Last**: Process leads from first entry to last (default)
  - **Last to First**: Reverse order processing from last to first entry
  - **Randomly**: Random lead selection for each email send
  - **Domain Based Send**: Extract and organize by email domains

**Domain-Based Sending Features:**
- **Domain Extraction**: Automatic extraction of unique email domains from selected leads
- **Domain Management Interface**: 
  - Right side shows extracted domains (e.g., outlook.com, yahoo.com, gmail.com)
  - Drag-and-drop interface to reorder domain priority
  - Visual domain list with reordering capabilities
- **Sequential Domain Processing**: Send to all leads of first domain, then second domain, etc.
- **Domain Rotation Option**: 
  - **Rotation Checkbox** (default: off): Enable rotation between domains
  - **When Enabled**: Send one email to each domain in sequence, then repeat cycle
  - **Example**: Send to outlook.com → yahoo.com → gmail.com → outlook.com (repeat)
  - **When Disabled**: Send to all leads in first domain, then all in second domain, etc.
- **Duplicate Prevention**: Guaranteed no duplicate emails to same recipient address
- **Domain Order Control**: Complete user control over domain sending priority

### Subject Line Configuration
**Subject Management:**
- **Enable/Disable Toggle**: Option to send emails without subjects
- **Multi-Subject Selection**: Checkbox interface for selecting multiple subject lines
- **Subject Rotation Configuration**:
  - **Each Time**: Automatic subject rotation with every email (default for multiple subjects)
  - **Custom Range**: Define rotation frequency (e.g., rotate every 1-5 emails)
- **Single Subject Mode**: Same subject for all emails when only one selected

### Template & Attachments Configuration
**Template Selection:**
- **Multi-Template Support**: Select multiple message templates with checkbox interface
- **Attachment Handling**: Support for templates with or without attachments
- **Template Rotation Settings**:
  - **Each Mail**: Rotate templates with every email send
  - **Custom Range**: Define template rotation frequency (X to Y emails per template)

### Custom Tracking Configuration
**Tracking System Setup:**
- **Tracking Toggle**: Disabled by default, optional enablement
- **Tracking Domain Configuration**:
  - Main tracking domain/subdomain input
  - API key for tracking database integration
  - Data submission timing: Before/After send dropdown
- **API Call Frequency**:
  - **Every**: Submit/read tracking data before every email
  - **Custom**: Batch processing with defined ranges (e.g., 1-5 emails per batch)

**Email Open Tracking:**
- **Custom URL Configuration**: Multiple tracking URL formats (one per line)
- **Placeholder Support**: Full integration with all placeholder types
- **Example Formats**:
  ```
  https://domain.com/open?{{uuid}}&{{campaign}}
  https://domain2.com/open?{{uuid}}&{email}
  https://domain3.com/open?{email}
  ```

**Email Click Tracking:**
- **Link Selection Options**:
  - **All**: Track all links in message (default)
  - **Custom**: Select specific links from template with checkbox interface
- **Click URL Configuration**: Customizable tracking URL formats (one per line)
- **Advanced Placeholder Support**: All default placeholders and lead columns
- **Example Click Formats**:
  ```
  https://domain.com/click?uid={{uuid}}&cid={{CAMPAIGN}}&redirect={{ENCODED_URL}}
  https://domain2.com/click?uid={{uuid}}&email={EMAIL}&redirect={{ENCODED_URL}}
  ```

### Custom Headers Configuration
**Header Management System:**
Comprehensive email header customization with individual configuration per header type. Each header includes Enable/Disable dropdown (default: disabled) with Configure button:

**Message-ID Headers:**
- **Enable/Disable**: Individual control with configuration button
- **Format Options**: Multiple Message-ID formats (one per line):
  ```
  <{{uuid}}@{{domain}}>
  <{{timestamp}}.{{random}}@{{domain}}>
  <{{timestamp}}-{{user_id}}@{{domain}}>
  <{{campaign}}-{{batch}}-{{uuid}}@{{domain}}>
  <{{random_alphanum}}@{{domain}}>
  <{{custom_string}}@{{domain}}>
  <{{date}}-{{sequence}}@{{domain}}>
  <{{hash}}@{{domain}}>
  <{{email}}-{{uuid}}@{{domain}}>
  <{{FakerFullName}}-{{sequence}}@{{domain}}>
  <{{email}}.{{random_alphanum}}@{{domain}}>
  <{{FakerCompany}}-{{uuid}}@{{domain}}>
  <{{email}}-{{list_name}}-{{counter}}@{{domain}}>
  <{{ColumnName}}-{{uuid}}@{{domain}}>
  <{{FakerWord}}-{{uuid}}@{{domain}}>
  ```
- **Format Rotation**: Each Mail / Custom range options
- **Header Use Policy**: Must use each time / Optional application

**X-Tracking-ID Headers:**
- **Enable/Disable**: Individual control with configuration button
- **Format Options**: Custom tracking identifier formats (one per line):
  ```
  {{uuid}}
  {{hash}}
  {{random}}
  {{random_alphanum}}
  {{FakerUUID}}
  {{FakerRandomNumber}}
  {{timestamp}}
  {{date}}-{{sequence}}
  {{timestamp}}-{{counter}}
  {{year}}{{month}}{{day}}-{{hour}}{{minute}}{{second}}
  {{email}}-{{uuid}}
  {{email}}-{{timestamp}}
  {{FakerFirstName}}-{{FakerLastName}}-{{uuid}}
  {{campaign}}-{{batch}}-{{uuid}}
  {{campaign}}-{{timestamp}}
  {{campaign}}-{{email}}
  {{campaign}}-{{batch}}-{{email}}-{{uuid}}
  {{hash}}-{{counter}}
  {{user_id}}-{{uuid}}
  {{list_name}}-{{counter}}
  {{column1}}-{{column2}}-{{uuid}}
  ```
- **Format Rotation**: Each Mail / Custom range options
- **Header Use Policy**: Must use each time / Optional application

**X-Campaign-ID Headers:**
- **Enable/Disable**: Individual control with configuration button
- **Static Campaign Names**: Multiple campaign names/IDs (one per line) with placeholder support
- **Custom Override**: Option to override {{campaign}} and {{batch}} default values
- **Format Rotation**: Each Mail / Custom range options
- **Header Use Policy**: Must use each time / Optional application

**X-UID Headers:**
- **Enable/Disable**: Individual control with configuration button
- **Format Options**: Custom UID formats (one per line) using any placeholders
- **Format Rotation**: Each Mail / Custom range options
- **Header Use Policy**: Must use each time / Optional application

**Email Client Simulation (X-Mailer):**
- **Enable/Disable**: Individual control with configuration button
- **80+ Predefined X-Mailer Values** (one per line):
  ```
  Microsoft Outlook 16.0
  Microsoft Outlook 15.0
  Microsoft Outlook 14.0
  Microsoft Outlook Express 6.00.2900.2869
  Microsoft Windows Live Mail 16.4.3528.0331
  Microsoft Exchange Server 2016
  Microsoft Exchange Server 2013
  Microsoft-MacOutlook/16.81.0.24062400
  Apple Mail (2.3696.100.31)
  Apple Mail (2.3654.120.0.1.13)
  iPhone Mail (17G68)
  iPhone Mail (20A5358e)
  iPad Mail (15E148)
  Mozilla Thunderbird 115.3.1
  Mozilla Thunderbird 102.10.0
  Mozilla Thunderbird 91.13.1
  Android Mail 9.0.0.20702
  Samsung Email 6.1.00.16
  Gmail Web
  YahooMailWebService/0.8.111_71
  Airmail 3.6.70 (527)
  The Bat! (v9.5.1)
  The Bat! (v7.4.16)
  Lotus Notes Release 8.5
  Lotus Notes Release 9.0
  Zimbra 8.8.15_GA_3869
  Roundcube Webmail/1.6.2
  Roundcube Webmail/1.4.13
  Alpine 2.23 (LNX 1166 2018-08-05)
  Postbox 7.0.42
  Claws Mail 3.18.0 (GTK+ 2.24.32; x86_64-pc-linux-gnu)
  Evolution 3.46.4-1
  KMail/5.21.3 (20.12.3)
  Mutt/1.14.7 (2020-09-21)
  MailMate (5878)
  PHPMailer 6.7.1 (https://github.com/PHPMailer/PHPMailer)
  PHPMailer 5.2.27 (https://github.com/PHPMailer/PHPMailer)
  SwiftMailer 6.3.0
  SwiftMailer 5.4.12
  Mailgun PHP 4.0.0
  SendGrid Mailer
  Amazon Simple Email Service (SES)
  MailChimp Mailer
  Mailgun Mailer
  Sendmail 8.16.1
  Sendmail 8.15.2
  Exim 4.96
  Exim 4.94
  Postfix 3.6.4
  Postfix 3.4.13
  Sympa 6.2.60
  MailEnable Standard 10.36
  ```
- **X-Mailer Rotation**: Each Mail / Custom range options
- **Header Use Policy**: Must use each time / Optional application

**X-Origin Headers:**
- **Enable/Disable**: Individual control with configuration button
- **Origin Values**: Custom origin servers (one per line):
  ```
  webmail.google.com
  outbound-mail.company.com
  app-server-01.internal
  relay01.hostingprovider.net
  {{FakerIPv4}}
  (Any custom text or placeholders allowed)
  ```
- **Format Rotation**: Each Mail / Custom range options
- **Header Use Policy**: Must use each time / Optional application

**X-Email-Type Headers:**
- **Enable/Disable**: Individual control with configuration button
- **Email Types**: Classification values (one per line):
  ```
  Transactional
  Marketing
  Notification
  Alert
  Reminder
  Welcome
  PasswordReset
  AccountActivation
  Receipt
  Invoice
  Newsletter
  Survey
  Invitation
  System
  Support
  Promotion
  (Plus placeholder support like {{FakerWord}})
  ```
- **Format Rotation**: Each Mail / Custom range options
- **Header Use Policy**: Must use each time / Optional application

**X-Campaign-Name Headers:**
- **Enable/Disable**: Individual control with configuration button
- **Campaign Names**: Custom campaign names (one per line):
  ```
  SummerSale2025
  BlackFridayPromo
  WelcomeSeries
  JulyNewsletter
  BlackFridayPromo-{{uuid}}
  {{campaign}}
  {{FakerWord}}
  {{FakerCompany}}-{{campaign}}
  {{campaign}}-{{batch}}
  ```
- **Custom Override**: Option to override {{campaign}} and {{batch}} values
- **Format Rotation**: Each Mail / Custom range options
- **Header Use Policy**: Must use each time / Optional application

**Auto-Submitted Headers:**
- **Enable/Disable**: Individual control with configuration button
- **Options**: Dropdown with choices:
  - auto-generated
  - auto-replied
  - no
  - random (with From/To range specification for random selection)
- **Header Use Policy**: Must use each time / Optional application

**Precedence Headers:**
- **Enable/Disable**: Individual control with configuration button
- **Options**: Dropdown with choices:
  - bulk
  - list
  - junk
  - normal
  - random (with From/To range for rotating among all options)
- **Header Use Policy**: Must use each time / Optional application

**Priority Headers:**
- **Enable/Disable**: Individual control with configuration button
- **Options**: Dropdown with choices:
  - high
  - normal
  - low
  - random (with From/To range for rotation)
- **Header Use Policy**: Must use each time / Optional application

**X-Priority Headers:**
- **Enable/Disable**: Individual control with configuration button
- **Options**: Dropdown with choices:
  - 1 (Highest)
  - 2 (High)
  - 3 (Normal)
  - 4 (Low)
  - 5 (Lowest)
  - random (with From/To range for rotation among 1-5)
- **Header Use Policy**: Must use each time / Optional application

**Importance Headers:**
- **Enable/Disable**: Individual control with configuration button
- **Options**: Dropdown with choices:
  - high
  - normal
  - low
  - random (with From/To range for rotation)
- **Header Use Policy**: Must use each time / Optional application

**X-Auto-Response-Suppress Headers:**
- **Enable/Disable**: Individual control with configuration button
- **Options**: Dropdown with choices:
  - All (suppress all automatic responses)
  - OOF (suppress Out of Office replies)
  - AutoReply (suppress automatic replies)
  - AutoForward (suppress auto-forwarding)
  - DR (suppress Delivery Receipts)
  - RN (suppress Read Notifications)
  - NRN (suppress Non-Read Notifications)
  - Random (randomly pick one option)
- **Type Rotation**: Each Time / Custom range for rotation frequency
- **Header Use Policy**: Must use each time / Optional application

**Unsubscribe Headers:**
- **List-Unsubscribe**: Enable/Disable with configuration
- **Format Options**: Multiple unsubscribe formats (one per line):
  ```
  <mailto:unsubscribe@yourdomain.com>
  <mailto:unsubscribe@{{domain}}>
  <mailto:{{FakerFullName}}@yourdomain.com>
  <mailto:{{FakerFullName}}@{{domain}}>
  <mailto:{{campaign}}@yourdomain.com>
  <mailto:{{campaign}}@{{domain}}>
  <mailto:unsubscribe@yourdomain.com?{{subject}}=unsubscribe>
  <https://yourdomain.com/unsubscribe?email={email}>
  <https://yourdomain.com/unsubscribe/{{token}}>
  <mailto:unsubscribe@yourdomain.com>, <https://yourdomain.com/unsubscribe/{{token}}>
  ```
- **List-Unsubscribe-Post**: Dropdown with Disable/Enable/Random for one-click unsubscribe
- **Format Rotation**: Each Time / Custom range options
- **Header Use Policy**: Must use each time / Optional application

**Add More Headers:**
- **Custom Header Addition**: "Add more header" button for unlimited custom headers
- **Custom Configuration**: User-defined header names (e.g., "X-Custom-Header")
- **Remove Option**: (-) button to delete custom headers
- **Value Configuration**: Custom values (one per line) with full placeholder support
- **Rotation Options**: Each Mail / Custom range for custom headers
- **Header Use Policy**: Must use each time / Optional application

**Advanced Header Policies:**
- **Header Use Limit**: 
  - **All**: Use all enabled headers for each email
  - **Custom**: Minimum/maximum header count per email
    - Minimum automatically set to number of "Must use" headers
    - Maximum can be any number up to total headers
    - Optional headers rotate up to maximum limit
- **Disable Sometimes**: Optional checkbox (default: off)
  - When enabled: Even "Must use" headers may be omitted sometimes
  - Completely randomizes header usage for detection avoidance
  - Some emails sent with no custom headers at all
- **Rotation Patterns**: Each Mail / Custom range rotation for all headers
- **Policy Options**: Must use / Optional application for each header type

### Sending Modes
**Mode Selection**: Dropdown with four exclusive choices (only one can be selected):

**Single Mode (One-by-One):**
- **Sequential Sending**: Email sent individually with configurable delays
- **Delay Configuration**: From/To delay ranges with unit selection (seconds/minutes/hours)
- **Example**: Delay from 10 seconds to 20 seconds between each email
- **Precision Control**: Exact timing control for careful delivery patterns
- **Process**: Send one email → wait random delay in range → send next email → repeat

**Batch Mode (Group Sending):**
- **Batch Size Configuration**: Minimum and maximum batch sizes (e.g., 10-20 emails per batch)
- **Dynamic Batching**: Random batch sizes within defined ranges
- **Batch Delays**: Configurable delays between batches with unit selection (sec/min/hour)
- **Example**: Send 15 emails at once → wait 5-10 minutes → send next batch of 12 emails
- **Efficient Processing**: Optimized for high-volume sending

**Date & Time Mode (Scheduled Sending):**
- **Time Window Definition**: From Date/Time and To Date/Time selection with calendars
- **Current Date/Time Display**: Shows current system date and time for reference
- **Send Limit Configuration**: Maximum emails per time window (e.g., 100 emails)
- **Automatic Calculation**: Tool calculates optimal delays to meet schedule
- **Multiple Ranges**: "Add more" button to add multiple date/time ranges with individual limits
- **Coverage Analysis**: 
  - Shows total leads vs. configured limits
  - Displays remaining leads after all configured ranges
  - Warning if configuration won't cover all leads
- **Example**: Send 100 emails between Jan 1 8:00 AM and Jan 1 6:00 PM

**Spike Mode (Day-by-Day Planning):**
- **Daily Limit Planning**: Specify exact email count per day
- **Day Configuration**: Add Day 1, Day 2, Day 3, etc. with individual email limits
- **Progressive Sending**: Gradually increase daily limits over time (optional)
- **Multi-Day Configuration**: "Add more" button for unlimited days
- **Automatic Scheduling**: Tool manages 24-hour distribution for each day's limit
- **Remaining Tracking**: Real-time display of remaining leads after each day's plan
- **Example**: Day 1: 100 emails, Day 2: 150 emails, Day 3: 200 emails
- **Coverage Analysis**: Shows total leads vs. total planned sends across all days

### Campaign Scheduling
**Schedule Configuration:**
- **Scheduling Toggle**: Disable/Enable with default disabled state
- **Date/Time Selection**: Precise scheduling with hours/minutes and AM/PM
- **Countdown Display**: Real-time countdown to scheduled start time
- **Immediate Start**: Instant campaign start when scheduling disabled

### Live Status & Controls
**Real-time Monitoring:**
- **Live Counters**: 
  - Total Leads, Subjects, SMTPs, Message Templates
  - Sent Success/Failed counts with real-time updates
  - Remaining emails counter
  - Total Opens/Clicks (when tracking enabled, "Off" when disabled)
- **Progress Visualization**: Real-time progress bar with completion percentage
- **Dynamic Updates**: All counters update instantly during campaign execution

**Campaign Controls:**
- **Start**: Begin campaign execution (respects scheduling if enabled)
- **Stop**: Complete campaign termination (enabled only after starting)
- **Pause**: Pause sending without losing progress (enabled only while sending)
- **Resume**: Continue from exact pause point (enabled only when paused)
- **Save as Draft**: Preserve configuration and progress for later continuation

**Data Persistence:**
- **Automatic Saving**: Real-time campaign data and progress preservation
- **JSON Storage**: All configuration, settings, reports, and status saved as JSON files
- **Crash Recovery**: Resume campaigns exactly where left off after unexpected closure
- **Progress Integrity**: Complete counter and data preservation across sessions

### Campaign Reports
**Comprehensive Reporting:**
- **Detailed Send Log**: Complete table of all send attempts including:
  - Send status (success/failed) with error details
  - SMTP server used for each email
  - Subject line applied
  - Headers included
  - Message template used
  - Complete lead data for each recipient
  - Precise date/time stamps
- **Export Options**: Excel and CSV format exports
- **Live CSV Reports**: Automatic CSV generation and real-time updates in campaign folder
- **Data Completeness**: All lead file columns preserved in reports for complete traceability

## 🔧 Core Modules

### 1. Lead Management
**Core Operations:**
- **Import/Export**: CSV, Excel, Text file support with automatic format conversion
- **Smart Duplicate Detection**: Automatic duplicate removal with user options:
  - Keep all duplicates
  - Remove duplicates completely  
  - Merge rows (if extra fields differ)
  - Preview duplicate count before confirmation
- **File Format Support**: 
  - CSV files with automatic delimiter detection
  - Excel files with sheet selection
  - Text files using colon (:) separator with first line as headers

**Advanced Table Features:**
- **Inline Cell Editing**: Double-click any cell to edit and auto-save instantly
- **Bulk Operations**: 
  - Select multiple rows for bulk delete
  - Bulk export of selected data
  - Copy/paste functionality between rows
- **Column Management**: 
  - Add/remove columns dynamically with "+Header" button
  - Automatic column type detection with visual icons
  - Resize columns and customize display
- **Right-click Context Menu**:
  - Delete Row
  - Insert New Row Below/Above
  - Copy Row Data
  - Professional table operations

**Data Management:**
- **Manual Entry**: "+Manually" button opens form with:
  - Dropdown showing current headers
  - Input boxes for each column
  - Fill any/all fields, leave blanks as needed
  - One-click row addition with validation
- **Merge Functionality**: "+Merge" button provides:
  - Import additional leads file
  - Column mapping interface (drag-and-drop or dropdown)
  - Match columns like "Email to email", "Name to First Name"
  - Preview merge results before confirmation
  - Automatic duplicate handling during merge

**Performance Features:**
- **Pagination**: Handle millions of records efficiently
  - Configurable page sizes (100/500/1000 per page)
  - User-adjustable from Configuration panel
  - Smooth navigation between pages
- **Search/Filter Bar**: 
  - Real-time search across all columns
  - Filter by Email, Name, or any custom column
  - Advanced filtering options
- **Real-time Statistics**:
  - Total Rows count (e.g., "Total: 150")
  - Valid Email count (e.g., "Valid Emails: 140") 
  - Invalid Email count (e.g., "Invalid Emails: 10")
  - Live validation with inline error badges

**Column Type Detection:**
- **Automatic Recognition**: Smart detection of data types
- **Visual Indicators**: Icons next to headers for recognized types
  - Phone numbers, dates, countries, emails
  - Enhanced visual organization
- **Validation**: Real-time email format validation during import

**File Structure Management:**
- **List Creation**: Create named lead lists with optional descriptions
- **CSV Storage**: Each list stored as separate CSV file in `Data/Leads/`
- **Case-insensitive Columns**: Automatic detection of "email", "Email", or "EMAIL"
- **Required Fields**: Email column mandatory for all lists
- **Custom Columns**: Add unlimited custom columns for additional data

### 2. SMTP Management
**Server Configuration:**
- **Basic Settings**:
  - Server Name (used as filename for JSON storage)
  - Short Description (optional)
  - SMTP Host and Port (supports all standard ports: 465, 587, 25, 2525, etc.)
  - Authentication Method: Auto, PLAIN, LOGIN, CRAM-MD5
  - Security Type: Auto, None, SSL, TLS
  - Username/Email and Password credentials
  - From Email address configuration

**From Name Header Management:**
- **Header Option**: Enable/Disable dropdown (default: Disable) with edit icon for reconfiguration
- **Header Mode Selection**:
  - **Custom**: User-defined From Names (one or multiple, one per line)
  - **Faker**: Auto-generated unique names using Faker library
- **Rotation Settings**:
  - **Each time**: Rotate From Name with every email send
  - **After X to Y sends**: Define range (e.g., use same name for 10-25 emails, then rotate)
- **Header Use Policy**:
  - **Must Use** (default): Always apply configured From Name
  - **Random**: Define usage pattern with From/To ranges
    - Use header for X emails, skip for Y emails, repeat cycle
    - Example: Use header for 12 emails, skip for 20 emails, repeat
    - Improves inbox placement through unpredictable patterns

**Reply-To Header Management:**
- **Header Option**: Enable/Disable dropdown (default: Disable) with edit icon for reconfiguration
- **Header Mode Selection**:
  - **Custom**: User-defined Reply-To emails (one or multiple, one per line)
  - **Faker**: Auto-generated emails using provided domains (one domain per line)
- **Rotation Settings**:
  - **Each time**: Rotate Reply-To with every email send
  - **After X to Y emails**: Define rotation range for Reply-To addresses
    - Example: Use same Reply-To for 10-20 emails, then rotate to next
- **Header Use Policy**:
  - **Must Use** (default): Always apply configured Reply-To
  - **Random**: Random application pattern
    - Use Reply-To for X emails, use SMTP default for Y emails
    - Example: Use Reply-To for 10-15 emails, skip for next 15 emails
    - Creates natural variation to avoid detection

**Proxy Integration:**
- **Proxy Enable/Disable**: Optional proxy usage per SMTP with edit icon
- **Multiple Proxy Support**: Add unlimited proxies with automatic rotation
- **Add Proxy Configuration**:
  - IP/Host and Port settings
  - Proxy Type: HTTP, HTTPS, SOCKS5
  - Authentication: Optional username/password checkbox
  - SMTP Host for proxy testing
- **Proxy Testing**: Built-in connectivity testing for each proxy
- **Fallback Options**:
  - Stop using SMTP if proxy fails
  - Fallback to system default (no proxy)
- **Mandatory Proxy Use**: When enabled, proxy must be used every time
- **Rotation**: If multiple proxies added, automatic rotation between them

**Rate Limiting System:**
- **Limit Control**: Enable/Disable with edit icon and Reset Limit button
- **Time-based Limits**:
  - **Per Minute**: X emails per minute
  - **Hourly**: X emails per hour (60 minutes)
  - **Daily**: X emails per day (24 hours)  
  - **Weekly**: X emails per week (7 days)
  - **Monthly**: X emails per month (30 days)
- **Total Usage Limits**:
  - Set maximum total emails (0 = unlimited)
  - Automatic SMTP deactivation when limit reached
  - Status update: "Inactive - Reason: Limit Reached"
  - Reset functionality to clear usage counters (enabled only when limits used)
- **Usage Tracking**:
  - Real-time usage monitoring
  - Automatic status updates (Active/Inactive)
  - Detailed usage statistics and timestamps
  - Precise timing calculations for limit enforcement

**SMTP Table Management:**
- **Pagination**: 10/25/50 per page (configurable from Configuration panel)
- **Table View Columns**:
  - Server Name, Description, Host, Port
  - Username/Email, From Email
  - Added Date, Last Update Date, Status
- **Search/Filter**: Filter by Server Name, Host, or Status
- **Quick Actions**:
  - **Test SMTP**: Individual or bulk testing
    - Single SMTP testing with detailed results
    - Bulk testing of multiple SMTPs
    - Failed SMTPs highlighted in red with error reasons
    - Success indicators for passed tests
  - **Details**: Full configuration popup with horizontal scroll
    - Professional table format showing all configuration fields
    - Horizontal scroll for long data content
  - **Edit**: Modify any SMTP configuration
  - **Delete**: Remove SMTP and associated JSON file
- **Optional Features**:
  - Tag/Category field for grouping SMTPs by provider
  - Advanced sorting and filtering options

**JSON Storage**: Each SMTP stored as individual JSON file in `Data/SMTP/ServerName.json`
**Complete Configuration Fields Stored**:
- Server Name, Description, Host, Port, Authentication, Security
- Username, Password, From Email
- From Name settings (Enable/Disable, Mode, Custom/Faker, Rotation)
- Reply-To settings (Enable/Disable, Mode, Custom/Faker, Rotation)
- Proxy settings (Enable/Disable, IP/Host, Port, Type, Auth, Fallback)
- Limit settings (Enable/Disable, Type, Values, Usage tracking)
- Added timestamp, Last update, Status, Test results

### 3. Subject Line Management
**List Management:**
- **Multiple Subject Lists**: Create unlimited subject line lists
- **List Creation**: Name and optional description for each list
- **CSV Storage**: Each list stored as separate CSV file in `Data/Subject/`
- **Import/Export**: Full support for CSV, Excel, Text with auto-conversion

**Content Features:**
- **Personalization Support**: 
  - Lead column references: `{ColumnName}` (case-insensitive)
  - Default placeholders: `{{placeholder}}` (all 80+ placeholders)
  - Spintext integration: `{{{spinword}}}` format
- **Emoji Support**: Full Unicode emoji compatibility in subject lines
- **Duplicate Management**: Automatic duplicate detection and removal
- **Manual Addition**: "Add Manually" button with multi-line input support

**Advanced Functionality:**
- **Real-time Preview**: Preview button shows final subject after applying:
  - `{ColumnName}` values displayed in blue
  - `{{placeholders}}` values displayed in green  
  - `{{{spintext}}}` values displayed in orange
  - Helps validate personalization before sending
- **Color-coded Editing**: Visual highlighting of different placeholder types
- **Import Summary**: Post-import popup showing:
  - Total imported count
  - Duplicates skipped count
  - Error details (if any)

**Table Operations:**
- **Inline Editing**: Edit subject lines directly in table view
- **Bulk Operations**: Select multiple subjects for:
  - Mass delete operations
  - Bulk export to various formats
  - Copy/paste between lists
- **Search & Filter**: Real-time search bar above subject table
  - Filter by content, placeholders, or keywords
  - Essential for managing large subject lists
- **Pagination**: Configurable from Configuration panel
  - Handle unlimited subjects per list efficiently
  - User-adjustable page sizes

**File Format Handling:**
- **Text File Import**: Each line becomes one subject line
- **CSV/Excel Import**: Automatic format detection and conversion
- **Merge Support**: Import additional subjects to existing lists
  - Automatic duplicate removal during merge
  - Preserve existing subjects while adding new ones
- **Export Options**: Export to CSV, Excel, or Text formats
  - Text export uses one subject per line format

**Organization Features:**
- **Unlimited Storage**: Support for unlimited subjects per list
- **Unlimited Lists**: No restriction on number of subject lists
- **Auto-save**: Instant saving of all changes to CSV files
- **Real-time Updates**: All edits immediately reflected in storage

### 4. Message Templates
**Template Creation & Management:**
- **WYSIWYG HTML Editor**: Full-featured email editor with live preview
- **Content Types**: Support for HTML, Plain Text, Attachments-only, or combinations
- **Template Storage**: Organized in dedicated folders (`Data/Message/TemplateName/`)
- **Flexible Content**: 
  - "Enable Content" checkbox (default: checked)
  - Can create attachment-only templates without content
  - Combine HTML, plain text, and attachments in single template

**Advanced Editor Features:**
- **Image Support**: 
  - Direct file upload within email design
  - External image source links with automatic loading
  - Size/alt text specification and professional controls
- **Content Controls**:
  - Full HTML design capabilities
  - Plain text alternative creation
  - Mixed content type support
- **Personalization Integration**:
  - Lead column placeholders: `{column_name}`
  - Default placeholders: `{{placeholder}}` (all 80+ available)
  - Spintext support: `{{{spinword}}}` format

**Unsubscribe Link Integration:**
Direct insertion of unsubscribe links with multiple format options:
- `<mailto:unsubscribe@domain.com>` - Direct domain links
- `<mailto:unsubscribe@{{domain}}>` - Domain placeholder rotation
- `<mailto:{{FakerFullName}}@domain.com>` - Faker name integration
- `<mailto:{{FakerFullName}}@{{domain}}>` - Combined Faker and domain rotation
- `<mailto:{{campaign}}@domain.com>` - Campaign-based unsubscribe
- `<mailto:{{campaign}}@{{domain}}>` - Campaign with domain rotation
- `<mailto:unsubscribe@domain.com?{{subject}}=unsubscribe>` - Subject-based
- `<https://domain.com/unsubscribe?email={email}>` - Web-based with email
- `<https://domain.com/unsubscribe/{{token}}>` - Token-based links

**Fingerprint Obfuscation System:**
- **Purpose**: Bypass spam filters by creating unique HTML fingerprints
- **Default State**: Disabled by default, user-enabled per template
- **Obfuscation Techniques**:
  - `<div style="display:none">random string</div>` - Invisible content
  - `<span style="font-size:0">invisible</span>` - Zero-size elements
  - `<!-- abc123 -->` - Random HTML comments
  - Rotating inline CSS styles (random padding, margin values)
- **Rotation Policy Configuration**:
  - **Each time**: New fingerprint for every email send
  - **Custom**: User-defined range (e.g., "From 10 to 25 sends")
  - **Skip Sometimes**: Optional checkbox to occasionally skip fingerprinting
- **Result**: Every email has unique HTML fingerprint while looking identical to recipients

**Emoji Rotation System:**
- **Automatic Detection**: System detects emojis in template automatically
- **Enable/Disable**: "Emoji Rotation" option appears with dropdown (default: disabled)
- **Configuration Window**:
  - **Left Panel**: Table showing all detected emojis in template
  - **Right Panel**: Define alternative emojis for rotation (comma-separated)
- **Example Configuration**:
  ```
  Current Emoji | Rotate With
  😊           | 🙂, 😁, 😃
  🚀           | ✈️, 🛸, 🛫
  ```
- **Rotation Settings**:
  - **Each time**: Random emoji rotation on every email
  - **Custom**: Define rotation frequency (e.g., every 5-15 emails)
  - **Skip Sometimes**: Occasionally use original emoji for natural variation

**Preview Functionality:**
- **Real-time Preview**: See exactly how message will appear after processing
- **Color-coded Placeholders**:
  - `{lead_column}` values appear in **blue**
  - `{{default placeholders}}` appear in **green**
  - `{{{spintext}}}` appear in **orange**
- **Validation**: Confirm all placeholders and formatting before sending
- **Live Updates**: Preview updates as template is edited

**Attachment Management:**
- **Multiple Attachments**: Support for unlimited attachments per template
- **Flexible Usage**:
  - Content with attachments
  - Attachments only (no content)
  - Any combination as needed
- **Storage**: Attachments stored in template's dedicated folder
- **File Management**: Add, remove, replace attachments easily

**Template Organization:**
- **Folder Structure**: Each template gets dedicated directory
  ```
  ProjectDirectory/Data/Message/TemplateName/
  ├── email.html          # HTML version
  ├── plain.txt           # Plain text version  
  ├── attachments/        # Attachment storage
  └── metadata.json       # Template settings
  ```
- **Search & Pagination**: 
  - Search templates by name or content
  - Pagination for large template collections (10/25/50 per page)
- **Metadata Storage**: All configurations and settings preserved

**Advanced Template Features:**
- **Template Duplication**: Clone existing templates for variations
- **Import/Export**: Share templates between installations
- **Version History**: Track template modifications
- **Performance**: Optimized loading for large template libraries

### 5. Campaign Management
**Multi-Campaign Support:**
- **Independent Campaigns**: Run multiple campaigns simultaneously
- **Dedicated Threading**: Each campaign runs on separate background thread
- **Non-interference**: Start, stop, pause, resume any campaign without affecting others
- **Campaign Isolation**: Complete independence between campaign operations

**SMTP Configuration:**
- **Multi-SMTP Selection**: Choose multiple SMTP servers per campaign
- **Rotation Modes**:
  - **Each mail**: Rotate SMTP with every email send
  - **Custom ranges**: Rotate after X to Y emails sent
- **Automatic Limit Management**: 
  - Respect individual SMTP rate limits
  - Skip SMTPs that have reached limits
  - Automatic re-enable when limits reset
- **Fallback Handling**: Continue with available SMTPs if others fail

**Lead Configuration:**
- **Sending Sequences**: Multiple ordering options:
  - **First-to-Last**: Process leads in original order
  - **Last-to-First**: Reverse order processing
  - **Random**: Completely random lead selection
  - **Domain-based**: Group and reorder by email domain
- **Domain-based Sending**: 
  - Automatically reorder leads by domain
  - Distribute sending across different domains
  - Avoid concentrated sending to single domain
- **Duplicate Prevention**: Guarantee no duplicate sending to same lead

**Subject Configuration:**
- **Multiple Subject Selection**: Choose multiple subject lists per campaign
- **Rotation Patterns**:
  - Sequential rotation through selected subjects
  - Random subject selection
  - Custom rotation patterns
- **Subject Personalization**: All placeholders and spintext supported

**Template Configuration:**
- **Multiple Template Support**: Use multiple templates in single campaign
- **Template Rotation**: Automatic rotation between selected templates
- **Attachment Handling**: Support for templates with/without attachments
- **Content Variation**: Combine different template types for natural variation

**Tracking Integration:**
- **Custom Tracking Domain**: Optional tracking domain configuration
- **Open/Click Tracking**: Configurable tracking options (future feature)
- **API Integration**: Tracking data API support (future feature)
- **Campaign Analytics**: Real-time campaign performance data

### 6. Sending Modes
**Single Mode:**
- **One-by-one Sending**: Sequential email sending with configurable delays
- **Delay Options**: 
  - Seconds: 1-999 seconds between emails
  - Minutes: 1-999 minutes between emails  
  - Hours: 1-24 hours between emails
- **Precision Control**: Exact timing control for careful sending patterns

**Batch Mode:**
- **Group Sending**: Send emails in configured batch sizes
- **Batch Size Ranges**: Define minimum and maximum batch sizes (e.g., 50-100 emails per batch)
- **Batch Delays**: Configurable delays between batches
- **Dynamic Batching**: Random batch sizes within defined ranges for natural patterns

**Date & Time Mode (Scheduled Sending):**
- **Time Window Scheduling**: Define specific time windows for sending
- **Daily Schedule**: Set start and end times for each day
- **Day Selection**: Choose specific days of week for sending
- **Timezone Support**: Configure sending based on recipient or sender timezone
- **Automatic Queuing**: Emails queue when outside scheduled time windows

**Spike Mode (Day-by-Day Planning):**
- **Daily Email Limits**: Set maximum emails per day
- **Progressive Sending**: Gradually increase daily limits over time
- **Custom Daily Plans**: Define different limits for each day
- **Weekly/Monthly Planning**: Long-term sending schedule planning
- **Limit Monitoring**: Real-time tracking of daily limits and usage

**Advanced Sending Features:**
- **Mode Switching**: Change sending modes during campaign execution
- **Pause/Resume**: Pause any mode and resume from exact stopping point
- **Override Controls**: Manual override for urgent sends
- **Scheduling Conflicts**: Automatic handling of scheduling conflicts
- **Mode Persistence**: Save and reload sending mode configurations

### 7. Advanced Headers
**Comprehensive Header Management:**
Extensive email header customization with rotation and policy controls for each header type:

**Message Identification Headers:**
- **Message-ID**: Multiple format options with automatic domain rotation
- **X-Tracking-ID**: Custom tracking identifiers for campaign monitoring
- **X-Campaign-ID**: Campaign identification headers
- **X-UID**: Unique identifier headers for each email
- **X-Origin**: Origin server identification

**Email Client Simulation:**
- **X-Mailer**: Email client simulation with 80+ options including:
  - Outlook versions, Thunderbird, Apple Mail, Gmail, Yahoo
  - Mobile clients, webmail interfaces
  - Custom mailer strings
- **User-Agent**: Browser/client identification headers

**Email Classification Headers:**
- **X-Email-Type**: Email type classification (promotional, transactional, etc.)
- **X-Campaign-Name**: Campaign naming headers with placeholder support
- **Auto-Submitted**: Automatic submission flags (auto-generated, auto-replied)

**Priority & Importance Headers:**
- **Precedence**: Email precedence levels (bulk, list, junk, first-class)
- **Priority/X-Priority**: Email priority settings (1-5 scale)
- **Importance**: Message importance levels (high, normal, low)

**List Management Headers:**
- **List-Unsubscribe**: RFC-compliant unsubscribe headers with:
  - One-click unsubscribe support  
  - Multiple unsubscribe method options
  - Automatic generation based on template configuration
- **X-Auto-Response-Suppress**: Auto-response suppression controls

**Custom Headers:**
- **User-defined Headers**: Add unlimited custom headers
- **Dynamic Values**: Support for all placeholder types in header values
- **Header Validation**: Automatic validation of header formats

**Header Rotation & Policies:**
Each header includes comprehensive rotation controls:

**Enable/Disable Options:**
- Individual control for each header type
- Quick enable/disable toggles
- Bulk header management

**Format Rotation Settings:**
- **Each mail**: Rotate header format/value with every email
- **Custom ranges**: Rotate after X to Y emails (e.g., use same header for 10-25 emails)
- **Random selection**: Pick random format from available options

**Header Use Policies:**
- **Must Use** (default): Always include header when enabled
- **Optional with Random Application**: 
  - Define usage percentage (e.g., use header 70% of the time)
  - Random application patterns to avoid detection
  - Custom frequency ranges

**Advanced Policy Options:**
- **Skip Patterns**: Define when to skip header application
- **Frequency Control**: Control how often headers change
- **Detection Avoidance**: Random patterns to prevent spam filter detection
- **Header Combinations**: Smart combination of headers for authenticity

**Header Value Generation:**
- **Static Values**: Fixed header values
- **Dynamic Values**: Placeholder-based header generation
- **Faker Integration**: Auto-generated realistic header values
- **Domain Rotation**: Automatic domain rotation in applicable headers
- **Template Variables**: Use campaign, lead, and system data in headers

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
**Case-insensitive Detection:**
- Automatic placeholder recognition regardless of case
- `{{campaign}}`, `{{CAMPAIGN}}`, and `{{Campaign}}` all detect as `{{campaign}}`
- Applies to both default placeholders and uploaded lead column names
- No need for exact case matching

**Add More Functionality:**
- "Add More" button to create custom placeholders
- Define placeholder name and content
- One entry per line for multiple values
- Configurable rotation settings for each placeholder
- User-editable placeholder definitions

**Rotation Settings:**
- Each placeholder can have individual rotation policies
- Support for sequential, random, and custom rotation patterns
- Configurable rotation frequency (each use, after X emails, etc.)

**Domain Management:**
- Multiple domain rotation system with one domain per line
- Default example domains provided
- User-configurable domain lists for placeholder rotation

**Hash Algorithms:**
- User-selectable hash algorithms (MD5, SHA256, random)
- Custom hash configuration options
- Algorithm selection per placeholder use

**Custom String Management:**
- `{{batch}}` - Custom batch identifiers (one per line)
- `{{campaign}}` - Campaign names (one per line)  
- `{{custom_string}}` - Custom text strings (one per line)
- `{{list_name}}` - List names (one per line)
- All support unlimited entries and rotation

### Spintext Configuration
**Core Features:**
- **Unlimited Entries**: No limit on spintext definitions
- **Pipe-separated Variations**: Easy format using `|` separator (e.g., `option1|option2|option3`)
- **Main Word Mapping**: Clear word-to-variations relationship
- **Global Library**: Centralized spintext management across all templates
- **Add More Functionality**: Dynamic spintext addition with "Add More" button

**Configuration Interface:**
- **Main Word Input**: Define the base word or sentence (e.g., "struggling")
- **Spintext Options Input**: Define variations separated by pipes (e.g., "struggling|having trouble|facing challenges|finding it hard")
- **Add/Edit/Delete**: Full management of spintext entries
- **Preview Functionality**: Test spintext replacements before use

**Usage Syntax:**
- **Template Usage**: `{{{word}}}` format (e.g., `{{{struggling}}}`)
- **Random Selection**: Tool automatically picks random variation on each use
- **Universal Support**: Works in subjects, message body, and headers

**Example Configuration:**
```
Main Word: offer
Spintext Options: offer|deal|promotion|special|discount

Main Word: struggling  
Spintext Options: struggling|having trouble|facing challenges|finding it hard

Main Word: business
Spintext Options: business|company|organization|enterprise|firm
```

**Advanced Features:**
- **Rotation Policies**: Configure how variations are selected
- **Usage Statistics**: Track which variations are used most
- **Import/Export**: Backup and share spintext libraries
- **Nested Support**: Use placeholders within spintext variations

### Unsubscribe Configuration
Multiple format support including:
- `<mailto:unsubscribe@domain.com>` - Direct user-specific domain
- `<mailto:unsubscribe@{{domain}}>` - Using placeholder domain rotation
- `<mailto:{{FakerFullName}}@domain.com>` - Faker-generated names with specific domain
- `<mailto:{{FakerFullName}}@{{domain}}>` - Faker names with domain rotation
- `<mailto:{{campaign}}@domain.com>` - Campaign name with specific domain
- `<mailto:{{campaign}}@{{domain}}>` - Campaign name with domain rotation  
- `<mailto:unsubscribe@domain.com?{{subject}}=unsubscribe>` - Subject-based unsubscribe
- `<https://domain.com/unsubscribe?email={email}>` - Web-based with email parameter
- `<https://domain.com/unsubscribe/{{token}}>` - Token-based unsubscribe links
- `<mailto:unsubscribe@domain.com>, <https://domain.com/unsubscribe/{{token}}>` - Combined formats

**Configuration Features:**
- Add/edit/delete custom unsubscribe formats
- One format per line input
- Automatic rotation through defined formats
- Support for all placeholder types
- When using `{{unsubscribe}}` placeholder, tool automatically selects random format

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
- **QSS Theming**: Switchable themes with QSS styling system

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

#### 1. Compilation Guide (Technical)
**Complete .exe Creation Instructions:**
- **Step-by-step Compilation Process**: Detailed instructions for creating standalone executable
- **Environment Setup**: Complete dependency and configuration management
- **Tool-specific Instructions**: Separate guides for Nuitka, PyInstaller, and Cython compilation
- **Resource Handling**: Proper bundling of images, themes, JSON files, and fonts
- **Directory Structure**: Exact folder organization requirements for compilation
- **Compilation Commands**: Complete command-line instructions with parameters
- **Troubleshooting Guide**: Common compilation issues and proven solutions
- **Testing Procedures**: Verification methods for compiled executable functionality
- **Compatibility Assurance**: Ensuring identical functionality between .py and .exe versions
- **Resource Path Management**: Handling of external resources in compiled version

**Critical Requirements:**
- Ensure no broken buttons, input fields, or functionality after compilation
- Prevent random closing, freezing, or crashing in compiled version
- Maintain all GUI responsiveness and thread functionality
- Preserve all file read/write operations in packaged executable

#### 2. User Manual (Comprehensive)
**Human-readable Documentation:**
- **Natural Language Explanations**: Written in conversational, accessible tone
- **Complete Feature Coverage**: Documentation for every single feature and option
- **Step-by-step Instructions**: Detailed procedures for all software operations
- **Practical Examples**: Real-world usage scenarios and implementation guides
- **Setting Interactions**: Clear explanation of how different options affect each other
- **Unlock Behavior**: Description of when enabling settings reveals additional options

**Content Organization:**
- **Feature Accessibility**: Clear instructions on how to access each feature
- **Click-by-Click Guidance**: Exact UI navigation instructions
- **Option Explanations**: What happens when specific settings are selected
- **Configuration Examples**: Practical implementation scenarios for all features
- **Best Practices**: Optimal usage recommendations for different use cases
- **Troubleshooting**: Common user issues and step-by-step solutions

**User Experience Focus:**
- **Non-technical Language**: Avoiding robotic or overly technical explanations
- **Visual Learning**: Clear descriptions that help users understand interface elements
- **Workflow Guidance**: Logical progression through software features
- **Scenario-based Examples**: Practical applications for different email marketing needs
- **Error Prevention**: Guidance to avoid common mistakes and configuration errors

**Documentation Goals:**
- Make software fully understandable to non-technical users
- Provide complete accessibility to all features and capabilities
- Enable independent operation without additional support
- Serve as comprehensive reference for all software functionality

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

## 📋 Technical Clarifications

### Architecture Decisions
- **Individual SMTP Storage**: Each SMTP as separate JSON file with complete configuration
- **Desktop Application**: Pure PyQt6 desktop application with QSS styling (no browser components)
- **Threading Model**: Individual threads per campaign for complete isolation
- **Configuration Management**: Both file-based storage and GUI-editable settings with auto-sync
- **Data Persistence**: Real-time auto-save and manual save options for all user actions

### Email Handling
- **Direct SMTP Implementation**: Native SMTP protocol handling without external dependencies
- **Error Management**: Comprehensive logging, user notifications, and customizable retry mechanisms
- **Queue Optimization**: Efficient handling of high-volume sending with background processing
- **Limit Enforcement**: Automatic SMTP limit monitoring and enforcement with status management

### File & Storage Management
- **Storage Location**: All data files stored in same directory as executable
- **Auto-creation**: Automatic folder/file creation on first run
- **File Structure**: Organized hierarchy for leads, SMTPs, subjects, templates, campaigns
- **JSON Configuration**: All settings stored in JSON format for portability and editing

### UI Framework Specifications
- **PyQt6 Implementation**: Complete desktop application built with PyQt6 framework
- **QSS Styling**: External QSS files for theme management and customization
- **Theme Switching**: Runtime theme switching capability from settings
- **Professional Design**: Commercial-grade interface without emojis
- **External Icons**: SVG/PNG images with JSON path management system
- **Loading Animations**: Professional loading indicators for all operations

### Threading Architecture
- **Multi-Campaign Support**: Each campaign runs in dedicated thread
- **Non-blocking UI**: All operations on background threads to prevent UI freezing
- **Campaign Isolation**: Complete independence between campaign operations
- **Resource Management**: Proper thread management and cleanup

### Error Handling & Reliability
- **Detailed Logging**: Comprehensive error logging with user-friendly notifications
- **Retry Mechanisms**: Customizable retry counts and limits configurable via UI
- **User Notifications**: Clear error messages and status updates within application
- **Graceful Degradation**: Continue operation when individual components fail

### Compilation Compatibility
- **Multi-tool Support**: Full compatibility with Nuitka, Cython, and PyInstaller
- **Resource Bundling**: Proper handling of all external resources in compiled version
- **Functionality Preservation**: Identical behavior between .py source and compiled .exe
- **Cross-environment Testing**: Verification across different Windows versions and configurations

This specification ensures DeepMailer v1.0 will be a professional-grade email marketing solution with enterprise-level features, security, and reliability suitable for commercial use.