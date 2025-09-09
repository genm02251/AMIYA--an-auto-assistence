# AMIYA AI Assistant

**Autonomous Machine learning Image recognition Yolo Assistance**

An AI assistant that uses computer vision to interact with any software across all platforms. AMIYA provides universal compatibility by analyzing the visual interface rather than relying on specific APIs or integrations.

## 🌟 Features

- **Universal Compatibility**: Works with any software on any operating system
- **Computer Vision Based**: Uses YOLO and OpenCV for UI element detection
- **Cross-Platform**: Supports Windows, macOS, and Linux
- **Context-Aware**: Adapts assistance based on current activity (learning, working, playing)
- **Automated Interactions**: Click, type, scroll, and navigate automatically
- **Safety Features**: Built-in safety modes to prevent unwanted actions

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/genm02251/AMIYA--an-auto-assistence.git
cd AMIYA--an-auto-assistence

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Basic Usage

```bash
# Analyze current screen
amiya analyze

# Get assistance with a task
amiya assist "click the save button"

# Find and click a specific element
amiya find-and-click button

# Type text
amiya type-text "Hello, World!"

# Click at specific coordinates
amiya click-at 100 200

# Show status
amiya status

# Run demo
amiya demo
```

### Python API

```python
from amiya import AmiyaAssistant

# Initialize the assistant
assistant = AmiyaAssistant(safety_mode=True)

# Analyze current screen
analysis = assistant.capture_and_analyze()
print(f"Found {len(analysis['ui_elements'])} UI elements")

# Assist with a task
success = assistant.assist_with_task("save the document")

# Find and click a button
assistant.capture_and_analyze()
button = assistant.find_element("button")
if button:
    assistant.click_element(button)

# Get suggestions
suggestions = assistant.get_assistance_suggestions()
for suggestion in suggestions:
    print(f"- {suggestion}")
```

## 🔧 Components

### Core Modules

- **Screen Capture**: Cross-platform screenshot functionality
- **Vision Processor**: YOLO-based UI element detection and text recognition
- **Interaction Controller**: Automated mouse and keyboard interactions
- **Assistant**: Main orchestration and AI logic

### Supported Contexts

- **Learning**: Assists with educational content, tutorials, and study materials
- **Working**: Helps with productivity applications, documents, and workflows
- **Playing**: Supports entertainment applications, games, and media

## 🛡️ Safety Features

- **Coordinate Validation**: Ensures interactions stay within screen bounds
- **Safety Mode**: Logs all actions before execution
- **Failsafe**: Built-in emergency stop mechanisms
- **Confidence Thresholds**: Only acts on high-confidence detections

## 📋 Requirements

- Python 3.8+
- OpenCV
- PyAutoGUI
- Ultralytics YOLO
- PIL/Pillow
- Platform-specific GUI libraries

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔮 Future Enhancements

- [ ] Custom YOLO model training for UI elements
- [ ] Natural language task interpretation
- [ ] Machine learning-based action prediction
- [ ] Plugin system for application-specific assistance
- [ ] Voice control integration
- [ ] Multi-monitor support
- [ ] Gesture recognition

## ⚠️ Disclaimer

This tool is designed for legitimate automation and assistance purposes. Users are responsible for ensuring compliance with software terms of service and applicable laws. The authors are not responsible for any misuse of this software.
