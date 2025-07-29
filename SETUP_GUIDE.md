# DeepMailer v1.0 - Setup and Installation Guide

## Quick Start

### Windows Users
1. Double-click `run_deepmailer.bat` to start the application
2. If prompted, allow dependency installation
3. The application will start automatically

### Linux/Mac Users
1. Run `python run_deepmailer.py` or `./run_deepmailer.py`
2. If prompted, allow dependency installation
3. The application will start automatically

### Manual Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## System Requirements

- **Python 3.8 or higher**
- **Operating System:** Windows 10/11, Linux (Ubuntu 18.04+), macOS 10.15+
- **Memory:** 2GB RAM minimum, 4GB recommended
- **Storage:** 500MB free space

## Dependencies

The application requires the following Python packages:
- PyQt6 >= 6.6.0
- Faker >= 20.1.0
- requests >= 2.31.0
- openpyxl >= 3.1.2
- pandas >= 2.1.0
- psutil >= 5.9.0

## Troubleshooting

### Common Issues

#### 1. PyQt6 Import Errors (Linux)
If you get errors like `libEGL.so.1: cannot open shared object file`:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install libgl1 libxkbcommon-x11-0 libxcb-cursor0
sudo apt-get install libfontconfig1 libx11-xcb1 libegl1

# CentOS/RHEL/Fedora
sudo yum install mesa-libGL libxkbcommon-x11 libxcb-cursor
sudo yum install fontconfig libX11-xcb mesa-libEGL
```

#### 2. Display Issues (Headless Servers)
If running on a server without a display:
```bash
export QT_QPA_PLATFORM=offscreen
python main.py
```

#### 3. Permission Errors
If you get permission errors:
```bash
# Linux/Mac
chmod +x run_deepmailer.py

# Windows: Run as Administrator
```

#### 4. Python Version Issues
Ensure you're using Python 3.8+:
```bash
python --version
# If using Python 3: try python3 instead of python
python3 main.py
```

#### 5. Missing Dependencies
Install missing packages manually:
```bash
pip install PyQt6 Faker requests openpyxl pandas psutil
```

### Platform-Specific Issues

#### Windows
- **Visual C++ Redistributable Required:** Install from Microsoft website
- **Antivirus Interference:** Add DeepMailer folder to exclusions
- **Firewall Blocking:** Allow Python through Windows Firewall

#### Linux
- **Display Server Required:** Ensure X11 or Wayland is running
- **Font Issues:** Install additional fonts if UI appears broken
```bash
sudo apt-get install fonts-liberation fonts-dejavu
```

#### macOS
- **Security Permissions:** Allow Python in System Preferences > Security & Privacy
- **Homebrew Installation:** Use brew if pip fails
```bash
brew install python-tk
```

### Advanced Troubleshooting

#### Enable Debug Logging
Set environment variable for detailed logs:
```bash
export DEEPMAILER_DEBUG=1
python main.py
```

#### Check System Compatibility
```bash
python -c "
import sys, platform
print(f'Python: {sys.version}')
print(f'Platform: {platform.platform()}')
print(f'Architecture: {platform.architecture()}')
"
```

#### Test PyQt6 Installation
```bash
python -c "
from PyQt6.QtWidgets import QApplication
app = QApplication([])
print('PyQt6 works!')
"
```

## Environment Variables

- `QT_QPA_PLATFORM`: Set to 'offscreen' for headless operation
- `DISPLAY`: Required for X11 forwarding (Linux)
- `DEEPMAILER_DEBUG`: Enable debug mode
- `DEEPMAILER_CONFIG`: Custom config directory path

## File Structure

```
DeepMailer/
├── main.py                 # Main application entry point
├── run_deepmailer.py       # Cross-platform startup script
├── run_deepmailer.bat      # Windows batch file
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── SETUP_GUIDE.md         # This setup guide
├── core/                  # Core application modules
├── ui/                    # User interface modules
├── modules/               # Business logic modules
├── Data/                  # Application data (auto-created)
│   ├── Leads/            # Lead data storage
│   ├── SMTP/             # SMTP configurations
│   ├── Subject/          # Subject line collections
│   ├── Message/          # Email templates
│   ├── Campaigns/        # Campaign data
│   ├── Settings/         # Application settings
│   └── Logs/             # Application logs
└── Resource/             # Application resources
    ├── Images/           # Icons and images
    ├── Theme/           # QSS theme files
    └── Fonts/           # Custom fonts
```

## Support

If you continue to experience issues:

1. Check the logs in `Data/Logs/` for detailed error messages
2. Ensure all system requirements are met
3. Try running with debug mode enabled
4. Check for updates to Python and dependencies

## Performance Tips

- **Large Lead Lists:** Use pagination settings in Configuration
- **Multiple Campaigns:** Monitor system resources
- **Theme Loading:** Clear browser cache if themes don't load
- **Memory Usage:** Restart application periodically for large operations

## Security Notes

- Keep your SMTP credentials secure
- Regularly backup your `Data/` directory
- Use strong passwords for email accounts
- Monitor sending limits to avoid blacklisting