# Installation Guide

## System Requirements

- Python 3.8 or higher
- Operating System: Windows 10+, macOS 10.15+, or Linux
- Display server (for full functionality)

## Installation Methods

### Method 1: Basic Installation (Recommended for testing)

```bash
# Clone the repository
git clone https://github.com/genm02251/AMIYA--an-auto-assistence.git
cd AMIYA--an-auto-assistence

# Install minimal dependencies
pip install -r requirements-minimal.txt

# Install in development mode
pip install -e .
```

### Method 2: Full Installation (For production use)

```bash
# Clone the repository
git clone https://github.com/genm02251/AMIYA--an-auto-assistence.git
cd AMIYA--an-auto-assistence

# Install all dependencies including YOLO
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Method 3: Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv amiya-env

# Activate virtual environment
# On Windows:
amiya-env\Scripts\activate
# On macOS/Linux:
source amiya-env/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e .
```

## Platform-Specific Setup

### Windows
```bash
# Additional Windows-specific dependencies
pip install pywin32
```

### macOS
```bash
# Additional macOS-specific dependencies
pip install pyobjc
```

### Linux
```bash
# Additional Linux-specific dependencies
pip install python-xlib

# For Ubuntu/Debian, you may also need:
sudo apt-get install python3-tk python3-dev
```

## Verification

Test your installation:

```bash
# Test basic functionality
python -c "from amiya import AmiyaAssistant; print('✓ Installation successful')"

# Test CLI
amiya --help

# Run demo
amiya demo
```

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'amiya'`
**Solution**: Run `pip install -e .` in the project directory

**Issue**: Screen capture not working
**Solution**: Ensure you're not in a headless environment, or use the mock mode for testing

**Issue**: PyAutoGUI not working
**Solution**: Install GUI dependencies for your platform and ensure you have a display server

**Issue**: YOLO model download fails
**Solution**: Check internet connection or use minimal installation without YOLO

### Getting Help

1. Check the [Examples](examples.py) file for usage patterns
2. Run `amiya --help` for command reference
3. Enable debug mode: `amiya --debug <command>`
4. Check the logs for detailed error messages