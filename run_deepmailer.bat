@echo off
title DeepMailer v1.0 - Professional Email Marketing Software
echo ==========================================================
echo DeepMailer v1.0 - Professional Email Marketing Software
echo ==========================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    echo.
    pause
    exit /b 1
)

:: Check Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set pyver=%%i
echo Python version: %pyver%

:: Check if requirements.txt exists
if not exist "requirements.txt" (
    echo ERROR: requirements.txt not found
    echo Please ensure you're running this from the DeepMailer directory
    pause
    exit /b 1
)

:: Check if dependencies are installed
echo Checking dependencies...
python -c "import PyQt6, faker, pandas, openpyxl, psutil" >nul 2>&1
if errorlevel 1 (
    echo Missing dependencies detected
    set /p install="Install missing dependencies? (y/n): "
    if /i "%install%"=="y" (
        echo Installing dependencies...
        python -m pip install -r requirements.txt
        if errorlevel 1 (
            echo Failed to install dependencies
            pause
            exit /b 1
        )
    ) else (
        echo Cannot continue without dependencies
        pause
        exit /b 1
    )
) else (
    echo All dependencies are installed
)

echo.
echo Starting DeepMailer...
echo.

:: Start the application
python main.py

echo.
echo DeepMailer has exited
pause