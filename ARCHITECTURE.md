# AMIYA AI Assistant Architecture

## Overview

AMIYA (Autonomous Machine learning Image recognition Yolo Assistance) is designed as a modular, cross-platform AI assistant that uses computer vision to interact with any software interface. The architecture follows clean separation of concerns with well-defined interfaces between components.

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        AMIYA AI Assistant                      │
├─────────────────────────────────────────────────────────────────┤
│                          CLI Interface                         │
│                        (amiya.cli)                            │
├─────────────────────────────────────────────────────────────────┤
│                      Core Assistant                            │
│                   (amiya.core.assistant)                      │
├───────────────────┬───────────────────┬───────────────────────┤
│   Screen Capture  │  Vision Processor │  Interaction Controller│
│   (core.screen_   │   (vision.        │   (interaction.       │
│    capture)       │    detector)      │    controller)        │
├───────────────────┼───────────────────┼───────────────────────┤
│      PIL/         │    OpenCV/        │    PyAutoGUI/         │
│   Platform APIs   │     YOLO          │     Pynput           │
└───────────────────┴───────────────────┴───────────────────────┘
```

## Core Components

### 1. Core Assistant (`amiya.core.assistant.AmiyaAssistant`)

**Purpose**: Central orchestrator that coordinates all other components

**Key Responsibilities**:
- Manages overall assistant state and context
- Coordinates screen capture, analysis, and interaction
- Provides high-level task assistance interface
- Implements context-aware behavior

**Key Methods**:
- `capture_and_analyze()`: Captures screen and detects UI elements
- `assist_with_task()`: Provides task-based assistance
- `find_element()`: Locates specific UI elements
- `automate_sequence()`: Executes action sequences

### 2. Screen Capture (`amiya.core.screen_capture.ScreenCapture`)

**Purpose**: Cross-platform screen capture functionality

**Key Responsibilities**:
- Captures full screen or specific regions
- Handles platform-specific implementations
- Provides fallback for headless environments
- Manages window detection and capture

**Key Methods**:
- `capture_screen()`: Main screen capture function
- `get_screen_size()`: Returns display dimensions
- `capture_window()`: Captures specific windows
- `get_window_list()`: Lists available windows

**Platform Support**:
- Windows: Uses PIL.ImageGrab and pygetwindow
- macOS: Uses PIL.ImageGrab with platform-specific optimizations
- Linux: Uses PIL.ImageGrab with X11/Wayland support
- Headless: Mock image generation for testing

### 3. Vision Processor (`amiya.vision.detector.VisionProcessor`)

**Purpose**: Computer vision for UI element detection

**Key Responsibilities**:
- Detects UI elements (buttons, text fields, menus)
- Performs text recognition
- Integrates YOLO object detection (optional)
- Provides template matching fallback

**Key Methods**:
- `detect_ui_elements()`: Main detection function
- `detect_text()`: Text region detection
- Template-based detection for common elements

**Detection Strategies**:
1. **YOLO Detection**: Uses pre-trained or custom YOLO models
2. **Template Matching**: Fallback for basic UI elements
3. **Morphological Operations**: For text and shape detection
4. **Contour Analysis**: For button and widget detection

### 4. Interaction Controller (`amiya.interaction.controller.InteractionController`)

**Purpose**: Automated user interface interactions

**Key Responsibilities**:
- Simulates mouse clicks, movements, and scrolling
- Handles keyboard input and key combinations
- Provides action sequencing capabilities
- Implements safety features and validation

**Key Methods**:
- `click()`: Mouse click operations
- `type_text()`: Keyboard text input
- `press_key()`: Single key presses
- `key_combination()`: Multi-key combinations
- `drag()`: Mouse drag operations

**Safety Features**:
- Coordinate validation
- Screen boundary checking
- Rate limiting and delays
- Emergency failsafe mechanisms

### 5. CLI Interface (`amiya.cli`)

**Purpose**: Command-line interface for all functionality

**Key Responsibilities**:
- Provides user-friendly command interface
- Handles argument parsing and validation
- Formats output for human consumption
- Supports batch operations and scripting

**Available Commands**:
- `analyze`: Screen analysis and element detection
- `assist`: Task-based assistance
- `click-at`: Direct coordinate clicking
- `type-text`: Text input
- `find-and-click`: Element-based interaction
- `status`: System status and diagnostics
- `demo`: Interactive demonstration

## Data Flow

### 1. Screen Analysis Flow

```
Screen Capture → Image Processing → Element Detection → Result Aggregation
      ↓                ↓                  ↓                 ↓
  PIL.ImageGrab → OpenCV Processing → YOLO/Template → UIElement Objects
```

### 2. Task Assistance Flow

```
User Task → Context Analysis → Screen Analysis → Action Planning → Execution
    ↓            ↓                ↓               ↓              ↓
Task String → Context Detection → UI Elements → Action Sequence → Interactions
```

### 3. Interaction Flow

```
High-Level Action → Validation → Platform Translation → Execution → Feedback
       ↓              ↓              ↓                 ↓           ↓
   Click Element → Bounds Check → PyAutoGUI Call → System Action → Success/Fail
```

## Context System

### Context Detection

AMIYA automatically detects the current usage context:

- **Learning**: Educational interfaces, tutorials, documentation
- **Working**: Productivity applications, office suites, development tools
- **Playing**: Games, entertainment applications, media players
- **General**: Default context for unrecognized interfaces

### Context-Aware Assistance

Each context provides specialized assistance:

```python
contexts = {
    "learning": {
        "keywords": ["tutorial", "course", "study"],
        "actions": ["highlight_text", "take_notes", "bookmark"]
    },
    "working": {
        "keywords": ["document", "spreadsheet", "email"],
        "actions": ["copy_paste", "format_text", "save_file"]
    },
    "playing": {
        "keywords": ["game", "entertainment", "video"],
        "actions": ["click_play", "adjust_volume", "fullscreen"]
    }
}
```

## Error Handling and Resilience

### Graceful Degradation

AMIYA is designed to work even when optional components are unavailable:

- **No YOLO**: Falls back to template matching and morphological detection
- **No PyAutoGUI**: Disables interaction but maintains analysis capabilities
- **Headless Environment**: Uses mock images for testing and validation
- **No GUI Libraries**: Provides console-only interface

### Error Recovery

- **Failed Detections**: Retry with different parameters or methods
- **Interaction Failures**: Validate coordinates and retry
- **Context Confusion**: Fall back to general assistance mode
- **Resource Constraints**: Reduce analysis frequency or quality

## Security and Safety

### Safety Mechanisms

1. **Coordinate Validation**: All interactions validate screen boundaries
2. **Safety Mode**: Logs all actions before execution in development
3. **Confidence Thresholds**: Only acts on high-confidence detections
4. **Rate Limiting**: Prevents rapid-fire actions that could cause issues

### Privacy Considerations

- **Local Processing**: All analysis happens locally by default
- **No Network Communication**: Core functionality doesn't require internet
- **Temporary Storage**: Screen captures can be automatically deleted
- **User Control**: All actions require explicit user initiation

## Extensibility

### Plugin Architecture

The modular design supports easy extension:

```python
# Custom vision processor
class CustomVisionProcessor(VisionProcessor):
    def detect_ui_elements(self, image):
        # Custom detection logic
        return custom_elements

# Custom interaction controller  
class CustomController(InteractionController):
    def custom_interaction(self, params):
        # Platform-specific interactions
        pass
```

### Custom Models

AMIYA supports custom YOLO models for specialized detection:

```python
assistant = AmiyaAssistant(model_path="/path/to/custom_model.pt")
```

## Performance Considerations

### Optimization Strategies

1. **Region-Based Capture**: Capture only relevant screen areas
2. **Confidence Thresholds**: Balance accuracy vs. speed
3. **Caching**: Cache detection results for stable interfaces
4. **Threading**: Parallel processing for analysis and interaction

### Resource Management

- **Memory**: Efficient image processing and cleanup
- **CPU**: Configurable analysis frequency
- **GPU**: Optional GPU acceleration for YOLO models
- **Network**: Minimal network usage for model downloads only

## Future Architecture Enhancements

### Planned Improvements

1. **Multi-Agent System**: Specialized agents for different contexts
2. **Learning Pipeline**: Adaptive behavior based on user patterns
3. **Cloud Integration**: Optional cloud-based model updates
4. **Real-Time Processing**: Streaming analysis for dynamic interfaces
5. **Natural Language**: Enhanced task interpretation using NLP

### Scalability Considerations

- **Distributed Processing**: Support for remote analysis servers
- **Model Registry**: Centralized model management and updates
- **Configuration Management**: Environment-specific configurations
- **Monitoring**: Performance and usage analytics