"""
System interaction module for automated clicking, typing, and UI control.
"""

import time
import platform
from typing import Tuple, Optional, List
import logging

try:
    import pyautogui
    # Configure pyautogui safety settings
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

try:
    from pynput import mouse, keyboard
    from pynput.mouse import Button
    from pynput.keyboard import Key
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False

logger = logging.getLogger(__name__)


class InteractionController:
    """Handles automated interactions with the UI."""
    
    def __init__(self, safety_mode: bool = True):
        self.safety_mode = safety_mode
        
        if not PYAUTOGUI_AVAILABLE:
            logger.warning("PyAutoGUI not available. Interaction features will be limited.")
            self.screen_width, self.screen_height = 1920, 1080  # Default
        else:
            # Get screen size for bounds checking
            self.screen_width, self.screen_height = pyautogui.size()
        
        if PYNPUT_AVAILABLE:
            self.mouse_controller = mouse.Controller()
            self.keyboard_controller = keyboard.Controller()
        else:
            logger.warning("Pynput not available. Some interaction features will be limited.")
            self.mouse_controller = None
            self.keyboard_controller = None
        
        logger.info(f"Initialized interaction controller for {platform.system()}")
        logger.info(f"Screen size: {self.screen_width}x{self.screen_height}")
    
    def click(self, x: int, y: int, button: str = 'left', clicks: int = 1, 
              interval: float = 0.1) -> bool:
        """
        Click at the specified coordinates.
        
        Args:
            x, y: Coordinates to click
            button: Mouse button ('left', 'right', 'middle')
            clicks: Number of clicks
            interval: Interval between clicks
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not PYAUTOGUI_AVAILABLE:
                logger.error("PyAutoGUI not available for clicking")
                return False
                
            if not self._validate_coordinates(x, y):
                logger.error(f"Invalid coordinates: ({x}, {y})")
                return False
            
            if self.safety_mode:
                logger.info(f"Clicking at ({x}, {y}) with {button} button, {clicks} times")
            
            # Map button string to pyautogui button
            button_map = {
                'left': 'left',
                'right': 'right', 
                'middle': 'middle'
            }
            
            if button not in button_map:
                logger.error(f"Invalid button: {button}")
                return False
            
            pyautogui.click(x, y, clicks=clicks, interval=interval, button=button_map[button])
            return True
            
        except Exception as e:
            logger.error(f"Error clicking at ({x}, {y}): {e}")
            return False
    
    def double_click(self, x: int, y: int) -> bool:
        """Double-click at the specified coordinates."""
        return self.click(x, y, clicks=2, interval=0.1)
    
    def right_click(self, x: int, y: int) -> bool:
        """Right-click at the specified coordinates."""
        return self.click(x, y, button='right')
    
    def drag(self, start_x: int, start_y: int, end_x: int, end_y: int, 
             duration: float = 1.0) -> bool:
        """
        Drag from start coordinates to end coordinates.
        
        Args:
            start_x, start_y: Starting coordinates
            end_x, end_y: Ending coordinates
            duration: Duration of the drag operation in seconds
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not PYAUTOGUI_AVAILABLE:
                logger.error("PyAutoGUI not available for dragging")
                return False
                
            if not (self._validate_coordinates(start_x, start_y) and 
                    self._validate_coordinates(end_x, end_y)):
                logger.error(f"Invalid coordinates for drag operation")
                return False
            
            if self.safety_mode:
                logger.info(f"Dragging from ({start_x}, {start_y}) to ({end_x}, {end_y})")
            
            pyautogui.drag(end_x - start_x, end_y - start_y, duration=duration)
            return True
            
        except Exception as e:
            logger.error(f"Error dragging: {e}")
            return False
    
    def scroll(self, x: int, y: int, clicks: int) -> bool:
        """
        Scroll at the specified coordinates.
        
        Args:
            x, y: Coordinates to scroll at
            clicks: Number of scroll clicks (positive = up, negative = down)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not PYAUTOGUI_AVAILABLE:
                logger.error("PyAutoGUI not available for scrolling")
                return False
                
            if not self._validate_coordinates(x, y):
                logger.error(f"Invalid coordinates for scroll: ({x}, {y})")
                return False
            
            # Move mouse to position first
            pyautogui.moveTo(x, y)
            pyautogui.scroll(clicks)
            return True
            
        except Exception as e:
            logger.error(f"Error scrolling at ({x}, {y}): {e}")
            return False
    
    def type_text(self, text: str, interval: float = 0.05) -> bool:
        """
        Type the specified text.
        
        Args:
            text: Text to type
            interval: Interval between keystrokes
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not PYAUTOGUI_AVAILABLE:
                logger.error("PyAutoGUI not available for typing")
                return False
                
            if self.safety_mode:
                logger.info(f"Typing text: '{text[:50]}{'...' if len(text) > 50 else ''}'")
            
            pyautogui.typewrite(text, interval=interval)
            return True
            
        except Exception as e:
            logger.error(f"Error typing text: {e}")
            return False
    
    def press_key(self, key: str) -> bool:
        """
        Press a single key.
        
        Args:
            key: Key to press (e.g., 'enter', 'tab', 'ctrl', 'alt')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not PYAUTOGUI_AVAILABLE:
                logger.error("PyAutoGUI not available for key press")
                return False
                
            if self.safety_mode:
                logger.info(f"Pressing key: {key}")
            
            pyautogui.press(key)
            return True
            
        except Exception as e:
            logger.error(f"Error pressing key '{key}': {e}")
            return False
    
    def key_combination(self, keys: List[str]) -> bool:
        """
        Press a combination of keys.
        
        Args:
            keys: List of keys to press simultaneously
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not PYAUTOGUI_AVAILABLE:
                logger.error("PyAutoGUI not available for key combination")
                return False
                
            if self.safety_mode:
                logger.info(f"Pressing key combination: {'+'.join(keys)}")
            
            pyautogui.hotkey(*keys)
            return True
            
        except Exception as e:
            logger.error(f"Error pressing key combination {keys}: {e}")
            return False
    
    def move_mouse(self, x: int, y: int, duration: float = 0.5) -> bool:
        """
        Move mouse to specified coordinates.
        
        Args:
            x, y: Target coordinates
            duration: Duration of movement in seconds
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not PYAUTOGUI_AVAILABLE:
                logger.error("PyAutoGUI not available for mouse movement")
                return False
                
            if not self._validate_coordinates(x, y):
                logger.error(f"Invalid coordinates for mouse move: ({x}, {y})")
                return False
            
            pyautogui.moveTo(x, y, duration=duration)
            return True
            
        except Exception as e:
            logger.error(f"Error moving mouse to ({x}, {y}): {e}")
            return False
    
    def get_mouse_position(self) -> Tuple[int, int]:
        """Get current mouse position."""
        if PYAUTOGUI_AVAILABLE:
            return pyautogui.position()
        else:
            logger.warning("PyAutoGUI not available for mouse position")
            return (0, 0)
    
    def wait(self, seconds: float) -> None:
        """Wait for specified number of seconds."""
        time.sleep(seconds)
    
    def _validate_coordinates(self, x: int, y: int) -> bool:
        """Validate that coordinates are within screen bounds."""
        return (0 <= x < self.screen_width and 0 <= y < self.screen_height)


class ActionSequence:
    """Manages sequences of automated actions."""
    
    def __init__(self, controller: InteractionController):
        self.controller = controller
        self.actions = []
        logger.info("Initialized action sequence")
    
    def add_click(self, x: int, y: int, button: str = 'left', delay: float = 0.5):
        """Add a click action to the sequence."""
        self.actions.append({
            'type': 'click',
            'x': x,
            'y': y,
            'button': button,
            'delay': delay
        })
        return self
    
    def add_type(self, text: str, delay: float = 0.5):
        """Add a type action to the sequence."""
        self.actions.append({
            'type': 'type',
            'text': text,
            'delay': delay
        })
        return self
    
    def add_key(self, key: str, delay: float = 0.3):
        """Add a key press action to the sequence."""
        self.actions.append({
            'type': 'key',
            'key': key,
            'delay': delay
        })
        return self
    
    def add_wait(self, seconds: float):
        """Add a wait action to the sequence."""
        self.actions.append({
            'type': 'wait',
            'seconds': seconds
        })
        return self
    
    def execute(self) -> bool:
        """Execute all actions in the sequence."""
        try:
            logger.info(f"Executing action sequence with {len(self.actions)} actions")
            
            for i, action in enumerate(self.actions):
                logger.debug(f"Executing action {i+1}/{len(self.actions)}: {action['type']}")
                
                if action['type'] == 'click':
                    success = self.controller.click(action['x'], action['y'], action['button'])
                elif action['type'] == 'type':
                    success = self.controller.type_text(action['text'])
                elif action['type'] == 'key':
                    success = self.controller.press_key(action['key'])
                elif action['type'] == 'wait':
                    self.controller.wait(action['seconds'])
                    success = True
                else:
                    logger.error(f"Unknown action type: {action['type']}")
                    success = False
                
                if not success:
                    logger.error(f"Action {i+1} failed: {action}")
                    return False
                
                # Add delay after action (except for wait actions)
                if action['type'] != 'wait' and 'delay' in action:
                    self.controller.wait(action['delay'])
            
            logger.info("Action sequence completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error executing action sequence: {e}")
            return False
    
    def clear(self):
        """Clear all actions from the sequence."""
        self.actions.clear()
        return self