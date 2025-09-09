"""
Example usage scripts for AMIYA AI Assistant.
"""

from amiya import AmiyaAssistant
import time


def example_basic_usage():
    """Basic usage example."""
    print("=== Basic AMIYA Usage Example ===")
    
    # Initialize assistant
    assistant = AmiyaAssistant(safety_mode=True)
    print("✓ Assistant initialized")
    
    # Capture and analyze screen
    print("\n1. Capturing and analyzing screen...")
    analysis = assistant.capture_and_analyze()
    
    ui_count = len(analysis.get('ui_elements', []))
    text_count = len(analysis.get('text_regions', []))
    context = analysis.get('context', 'unknown')
    
    print(f"   - UI elements found: {ui_count}")
    print(f"   - Text regions found: {text_count}")
    print(f"   - Detected context: {context}")
    
    # Get suggestions
    print("\n2. Getting assistance suggestions...")
    suggestions = assistant.get_assistance_suggestions()
    for i, suggestion in enumerate(suggestions, 1):
        print(f"   {i}. {suggestion}")
    
    # Show status
    print("\n3. Assistant status:")
    status = assistant.get_status()
    for key, value in status.items():
        print(f"   {key}: {value}")


def example_task_assistance():
    """Example of task-based assistance."""
    print("\n=== Task Assistance Example ===")
    
    assistant = AmiyaAssistant()
    
    # Example tasks
    tasks = [
        "click the save button",
        "type hello world",
        "copy selected text",
        "open new file"
    ]
    
    for task in tasks:
        print(f"\nAssisting with: '{task}'")
        success = assistant.assist_with_task(task)
        status = "✓ Success" if success else "✗ Failed"
        print(f"Result: {status}")


def example_element_detection():
    """Example of UI element detection and interaction."""
    print("\n=== Element Detection Example ===")
    
    assistant = AmiyaAssistant()
    
    # Analyze screen first
    print("Analyzing screen for UI elements...")
    assistant.capture_and_analyze()
    
    # Try to find different types of elements
    element_types = ['button', 'text', 'menu', 'icon']
    
    for element_type in element_types:
        print(f"\nLooking for {element_type} elements...")
        element = assistant.find_element(element_type)
        
        if element:
            print(f"✓ Found {element_type} at {element.center} (confidence: {element.confidence:.2f})")
            
            # Simulate clicking (in safe mode, this won't actually click)
            print(f"  Simulating click on {element_type}...")
            success = assistant.click_element(element)
            print(f"  Click result: {'✓ Success' if success else '✗ Failed'}")
        else:
            print(f"✗ No {element_type} found")


def example_automation_sequence():
    """Example of automated action sequence."""
    print("\n=== Automation Sequence Example ===")
    
    assistant = AmiyaAssistant()
    
    # Define a sequence of actions
    actions = [
        {"type": "click", "x": 100, "y": 100},
        {"type": "wait", "seconds": 1.0},
        {"type": "type", "text": "Hello, AMIYA!"},
        {"type": "key", "key": "enter"},
        {"type": "wait", "seconds": 0.5},
        {"type": "click", "x": 200, "y": 150}
    ]
    
    print(f"Executing sequence of {len(actions)} actions...")
    success = assistant.automate_sequence(actions)
    
    print(f"Sequence result: {'✓ Success' if success else '✗ Failed'}")


if __name__ == "__main__":
    print("AMIYA AI Assistant - Usage Examples")
    print("=" * 40)
    
    try:
        example_basic_usage()
        example_task_assistance()
        example_element_detection()
        example_automation_sequence()
        
        print("\n" + "=" * 40)
        print("All examples completed successfully!")
        
    except Exception as e:
        print(f"\nError running examples: {e}")
        import traceback
        traceback.print_exc()