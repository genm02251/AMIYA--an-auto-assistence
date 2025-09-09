# AMIYA AI Assistant Usage Guide

## Quick Start

### Command Line Interface

The easiest way to get started with AMIYA is through the command line interface:

```bash
# Analyze current screen
amiya analyze

# Get assistance with a task
amiya assist "click the save button"

# Show current status
amiya status

# Run interactive demo
amiya demo
```

### Python API

For more advanced usage, you can use the Python API:

```python
from amiya import AmiyaAssistant

# Initialize assistant
assistant = AmiyaAssistant(safety_mode=True)

# Basic screen analysis
analysis = assistant.capture_and_analyze()
print(f"Found {len(analysis['ui_elements'])} UI elements")

# Task-based assistance
assistant.assist_with_task("save the document")
```

## Core Concepts

### 1. Context Awareness

AMIYA adapts its assistance based on the current context:

- **Learning**: Educational content, tutorials, study materials
- **Working**: Productivity apps, documents, workflows  
- **Playing**: Entertainment, games, media

```python
# Context is automatically detected
analysis = assistant.capture_and_analyze()
context = analysis['context']  # 'learning', 'working', 'playing', or 'general'
```

### 2. UI Element Detection

AMIYA can detect various UI elements:

```python
# Find specific elements
button = assistant.find_element("button", confidence_threshold=0.7)
if button:
    assistant.click_element(button)

# Get all detected elements
assistant.capture_and_analyze()
for element in assistant.detected_elements:
    print(f"{element.element_type} at {element.center}")
```

### 3. Automated Interactions

AMIYA can perform various automated actions:

```python
# Click at coordinates
assistant.interaction_controller.click(100, 200)

# Type text
assistant.interaction_controller.type_text("Hello, World!")

# Press keys
assistant.interaction_controller.press_key("enter")
assistant.interaction_controller.key_combination(["ctrl", "s"])
```

## Common Use Cases

### 1. Automating Repetitive Tasks

```python
# Define a sequence of actions
actions = [
    {"type": "click", "x": 100, "y": 100},
    {"type": "type", "text": "automation test"},
    {"type": "key", "key": "enter"},
    {"type": "wait", "seconds": 1.0}
]

# Execute the sequence
assistant.automate_sequence(actions)
```

### 2. Screen Monitoring

```python
import time

# Monitor screen changes
while True:
    analysis = assistant.capture_and_analyze()
    ui_count = len(analysis['ui_elements'])
    
    if ui_count > 5:  # Many UI elements detected
        print("Complex interface detected")
        # Take action...
        
    time.sleep(2)  # Check every 2 seconds
```

### 3. Context-Specific Assistance

```python
# Get suggestions based on current context
suggestions = assistant.get_assistance_suggestions()
for suggestion in suggestions:
    print(f"Suggestion: {suggestion}")

# Context-aware task execution
if assistant.current_context == "working":
    assistant.assist_with_task("save document")
elif assistant.current_context == "learning":
    assistant.assist_with_task("highlight important text")
```

## CLI Commands Reference

### Analysis Commands

```bash
# Analyze entire screen
amiya analyze

# Analyze specific region
amiya analyze --region "100,100,800,600"

# Save analysis to file
amiya analyze --output analysis.json
```

### Interaction Commands

```bash
# Click at coordinates
amiya click-at 100 200

# Right-click
amiya click-at 100 200 --button right

# Type text
amiya type-text "Hello, World!"

# Find and click element
amiya find-and-click button --confidence 0.7
```

### Assistance Commands

```bash
# Task-based assistance
amiya assist "click the save button"
amiya assist "copy selected text"
amiya assist "open new file"
```

### Information Commands

```bash
# Show status
amiya status

# Show status in JSON format
amiya status --format json

# Run demonstration
amiya demo
```

## Advanced Features

### 1. Custom YOLO Models

```bash
# Use custom trained model
amiya analyze --model-path /path/to/custom_model.pt
```

```python
# In Python
assistant = AmiyaAssistant(model_path="/path/to/custom_model.pt")
```

### 2. Safety Features

AMIYA includes several safety features:

- **Coordinate validation**: Ensures clicks stay within screen bounds
- **Safety mode**: Logs all actions before execution
- **Confidence thresholds**: Only acts on high-confidence detections

```python
# Initialize with safety mode
assistant = AmiyaAssistant(safety_mode=True)

# Validate coordinates
controller = assistant.interaction_controller
valid = controller._validate_coordinates(x, y)
```

### 3. Error Handling

```python
try:
    success = assistant.assist_with_task("complex task")
    if not success:
        print("Task failed, trying alternative approach...")
        # Implement fallback logic
except Exception as e:
    print(f"Error: {e}")
    # Handle error gracefully
```

## Best Practices

### 1. Always Use Safety Mode

```python
# Recommended: Enable safety mode for testing
assistant = AmiyaAssistant(safety_mode=True)
```

### 2. Handle Failures Gracefully

```python
# Check for success and provide alternatives
if not assistant.assist_with_task("primary task"):
    # Try alternative approach
    assistant.assist_with_task("alternative task")
```

### 3. Use Appropriate Confidence Thresholds

```python
# Adjust confidence based on accuracy needs
high_precision = assistant.find_element("button", confidence_threshold=0.9)
general_use = assistant.find_element("button", confidence_threshold=0.6)
```

### 4. Regular Screen Analysis

```python
# Update analysis before major actions
assistant.capture_and_analyze()
# Now use detected elements...
```

## Limitations and Considerations

1. **Performance**: Screen analysis can be CPU-intensive
2. **Accuracy**: Detection accuracy depends on screen content and quality
3. **Platform**: Some features may be limited in headless environments
4. **Security**: Be mindful of sensitive information on screen during capture

## Troubleshooting

### Common Issues

**Issue**: No UI elements detected
**Solution**: Try adjusting confidence thresholds or ensure clear UI visibility

**Issue**: Clicks not registering
**Solution**: Verify coordinates are correct and within screen bounds

**Issue**: Slow performance
**Solution**: Reduce analysis frequency or use region-specific capture

**Issue**: Context not detected correctly
**Solution**: The context detection is basic; consider manual context setting