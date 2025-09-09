# Configuration Guide

## Overview

AMIYA AI Assistant can be configured through various methods to customize its behavior for different use cases and environments.

## Configuration Methods

### 1. Environment Variables

Set these environment variables to configure AMIYA:

```bash
# Enable debug logging
export AMIYA_DEBUG=1

# Set custom model path
export AMIYA_MODEL_PATH=/path/to/custom/model.pt

# Set screen capture interval (seconds)
export AMIYA_CAPTURE_INTERVAL=1.0

# Set confidence thresholds
export AMIYA_CONFIDENCE_THRESHOLD=0.7
export AMIYA_TEXT_CONFIDENCE_THRESHOLD=0.6

# Safety settings
export AMIYA_SAFETY_MODE=1
export AMIYA_DRY_RUN=1  # Simulate actions without executing them
```

### 2. Configuration File

Create a `config.yaml` file in your project directory:

```yaml
# AMIYA AI Assistant Configuration

# Core settings
assistant:
  safety_mode: true
  debug: false
  model_path: null

# Vision processing
vision:
  confidence_threshold: 0.7
  text_confidence_threshold: 0.6
  enable_yolo: true
  yolo_model: "yolov8n.pt"

# Screen capture
screen:
  capture_interval: 1.0
  default_region: null  # [x, y, width, height]
  mock_mode: false  # Use mock images for testing

# Interaction
interaction:
  click_delay: 0.1
  type_interval: 0.05
  safety_boundary: 10  # Pixels from screen edge
  enable_failsafe: true

# Context detection
context:
  learning_keywords: ["tutorial", "course", "study", "learn", "education"]
  working_keywords: ["document", "spreadsheet", "email", "presentation"]
  playing_keywords: ["game", "entertainment", "video", "music"]
  
# Logging
logging:
  level: "INFO"  # DEBUG, INFO, WARNING, ERROR
  file: null  # Log file path, null for console only
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
```

### 3. Runtime Configuration

Configure AMIYA programmatically:

```python
from amiya import AmiyaAssistant
from amiya.core.assistant import AmiyaConfig

# Create custom configuration
config = AmiyaConfig(
    safety_mode=True,
    confidence_threshold=0.8,
    debug=True
)

# Initialize with configuration
assistant = AmiyaAssistant(config=config)
```

## Configuration Options

### Core Settings

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `safety_mode` | bool | `True` | Enable safety features and logging |
| `debug` | bool | `False` | Enable debug logging |
| `model_path` | str | `None` | Path to custom YOLO model |

### Vision Processing

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `confidence_threshold` | float | `0.7` | Minimum confidence for UI elements |
| `text_confidence_threshold` | float | `0.6` | Minimum confidence for text detection |
| `enable_yolo` | bool | `True` | Use YOLO for object detection |
| `yolo_model` | str | `"yolov8n.pt"` | YOLO model to use |

### Screen Capture

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `capture_interval` | float | `1.0` | Seconds between captures |
| `default_region` | list | `None` | Default capture region [x,y,w,h] |
| `mock_mode` | bool | `False` | Use mock images for testing |

### Interaction

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `click_delay` | float | `0.1` | Delay after clicks (seconds) |
| `type_interval` | float | `0.05` | Interval between keystrokes |
| `safety_boundary` | int | `10` | Pixels from screen edge to avoid |
| `enable_failsafe` | bool | `True` | Enable PyAutoGUI failsafe |

## Platform-Specific Configuration

### Windows Configuration

```yaml
# Windows-specific settings
platform:
  windows:
    use_win32: true
    window_detection: true
    dpi_awareness: true
```

### macOS Configuration

```yaml
# macOS-specific settings
platform:
  macos:
    accessibility_permissions: true
    use_quartz: true
```

### Linux Configuration

```yaml
# Linux-specific settings
platform:
  linux:
    display_server: "auto"  # auto, x11, wayland
    use_xlib: true
```

## Performance Tuning

### High Performance Configuration

```yaml
# Optimized for speed
performance:
  fast_mode: true
  reduce_analysis_frequency: true
  skip_detailed_text_detection: true
  use_threading: true
```

### High Accuracy Configuration

```yaml
# Optimized for accuracy
performance:
  detailed_analysis: true
  multiple_detection_passes: true
  enhanced_text_detection: true
  confidence_threshold: 0.9
```

## Security Configuration

### Secure Mode

```yaml
# Security-focused settings
security:
  no_screen_recording: true
  encrypt_captured_data: true
  auto_delete_captures: true
  require_confirmation: true
  restricted_interaction_zones: 
    - [0, 0, 100, 50]  # Top-left corner (taskbar)
```

## Development Configuration

### Debug Configuration

```yaml
# Development and debugging
development:
  verbose_logging: true
  save_debug_images: true
  debug_output_dir: "./debug/"
  mock_interactions: true
  performance_metrics: true
```

### Testing Configuration

```yaml
# Testing configuration
testing:
  mock_mode: true
  deterministic_behavior: true
  test_data_path: "./test_data/"
  disable_actual_interactions: true
  use_test_images: true
```

## Example Configurations

### Basic Desktop Automation

```yaml
assistant:
  safety_mode: true
vision:
  confidence_threshold: 0.8
interaction:
  click_delay: 0.2
  type_interval: 0.1
```

### Learning Assistant

```yaml
assistant:
  safety_mode: true
context:
  default_context: "learning"
  learning_keywords: ["tutorial", "lesson", "course", "study"]
interaction:
  gentle_mode: true
  confirmation_required: true
```

### Gaming Assistant

```yaml
assistant:
  safety_mode: false  # For faster response
vision:
  confidence_threshold: 0.6
  fast_detection: true
interaction:
  click_delay: 0.05
  rapid_mode: true
context:
  default_context: "playing"
```

## Loading Configuration

### From File

```python
from amiya import AmiyaAssistant
import yaml

# Load configuration from file
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

assistant = AmiyaAssistant.from_config(config)
```

### From Environment

```python
import os
from amiya import AmiyaAssistant

# Configuration from environment variables
config = {
    'safety_mode': os.getenv('AMIYA_SAFETY_MODE', 'true').lower() == 'true',
    'debug': os.getenv('AMIYA_DEBUG', 'false').lower() == 'true',
    'model_path': os.getenv('AMIYA_MODEL_PATH'),
}

assistant = AmiyaAssistant(**config)
```

### Command Line Override

```bash
# Override configuration via CLI
amiya analyze --debug --confidence-threshold 0.9
amiya assist "task" --safety-mode --model-path /custom/model.pt
```

## Configuration Validation

AMIYA validates configuration settings and provides helpful error messages:

```python
try:
    assistant = AmiyaAssistant(confidence_threshold=1.5)  # Invalid: > 1.0
except ValueError as e:
    print(f"Configuration error: {e}")
```

## Best Practices

1. **Start with defaults**: Use default configuration initially
2. **Gradual customization**: Adjust one setting at a time
3. **Test thoroughly**: Validate configuration changes
4. **Version control**: Keep configuration files in version control
5. **Environment-specific**: Use different configs for dev/test/prod
6. **Documentation**: Document custom configuration choices