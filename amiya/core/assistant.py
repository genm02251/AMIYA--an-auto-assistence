"""
Main AMIYA AI Assistant class that coordinates all components.
"""

import logging
import time
from typing import Dict, List, Optional, Tuple, Any
import numpy as np

from ..core.screen_capture import ScreenCapture
from ..vision.detector import VisionProcessor, UIElement
from ..interaction.controller import InteractionController, ActionSequence

logger = logging.getLogger(__name__)


class AmiyaAssistant:
    """
    Main AI Assistant class that uses computer vision for universal software interaction.
    """
    
    def __init__(self, safety_mode: bool = True, model_path: Optional[str] = None):
        """
        Initialize AMIYA AI Assistant.
        
        Args:
            safety_mode: Enable safety features and logging
            model_path: Optional path to custom YOLO model
        """
        self.safety_mode = safety_mode
        
        # Initialize components
        self.screen_capture = ScreenCapture()
        self.vision_processor = VisionProcessor(model_path)
        self.interaction_controller = InteractionController(safety_mode)
        
        # Assistant state
        self.last_screenshot = None
        self.detected_elements = []
        self.current_context = "general"
        
        # Activity contexts for different assistance modes
        self.contexts = {
            "learning": {
                "keywords": ["tutorial", "course", "study", "learn", "education"],
                "actions": ["highlight_text", "take_notes", "bookmark"]
            },
            "working": {
                "keywords": ["document", "spreadsheet", "email", "presentation"],
                "actions": ["copy_paste", "format_text", "save_file"]
            },
            "playing": {
                "keywords": ["game", "entertainment", "video", "music"],
                "actions": ["click_play", "adjust_volume", "fullscreen"]
            }
        }
        
        logger.info("AMIYA AI Assistant initialized successfully")
    
    def capture_and_analyze(self, region: Optional[Tuple[int, int, int, int]] = None) -> Dict[str, Any]:
        """
        Capture screen and analyze for UI elements.
        
        Args:
            region: Optional region to capture (x, y, width, height)
            
        Returns:
            Dictionary containing analysis results
        """
        try:
            # Capture screen
            screenshot = self.screen_capture.capture_screen(region)
            self.last_screenshot = screenshot
            
            # Detect UI elements
            ui_elements = self.vision_processor.detect_ui_elements(screenshot)
            self.detected_elements = ui_elements
            
            # Detect text regions
            text_regions = self.vision_processor.detect_text(screenshot)
            
            # Analyze context based on detected elements
            context = self._analyze_context(ui_elements, text_regions)
            
            analysis_result = {
                "timestamp": time.time(),
                "ui_elements": ui_elements,
                "text_regions": text_regions,
                "context": context,
                "screen_size": screenshot.shape[:2]
            }
            
            logger.info(f"Analysis complete: {len(ui_elements)} UI elements, {len(text_regions)} text regions")
            return analysis_result
            
        except Exception as e:
            logger.error(f"Error in capture and analysis: {e}")
            return {}
    
    def find_element(self, element_type: str, confidence_threshold: float = 0.5) -> Optional[UIElement]:
        """
        Find a specific type of UI element.
        
        Args:
            element_type: Type of element to find (e.g., 'button', 'text', 'menu')
            confidence_threshold: Minimum confidence threshold
            
        Returns:
            UIElement if found, None otherwise
        """
        try:
            for element in self.detected_elements:
                if (element.element_type.lower() == element_type.lower() and 
                    element.confidence >= confidence_threshold):
                    return element
            
            logger.info(f"Element type '{element_type}' not found")
            return None
            
        except Exception as e:
            logger.error(f"Error finding element: {e}")
            return None
    
    def click_element(self, element: UIElement, offset: Tuple[int, int] = (0, 0)) -> bool:
        """
        Click on a detected UI element.
        
        Args:
            element: UIElement to click on
            offset: Optional offset from element center
            
        Returns:
            True if successful, False otherwise
        """
        try:
            x = element.center[0] + offset[0]
            y = element.center[1] + offset[1]
            
            return self.interaction_controller.click(x, y)
            
        except Exception as e:
            logger.error(f"Error clicking element: {e}")
            return False
    
    def assist_with_task(self, task_description: str) -> bool:
        """
        Provide assistance with a specific task based on current screen context.
        
        Args:
            task_description: Description of the task to assist with
            
        Returns:
            True if assistance was provided, False otherwise
        """
        try:
            # Analyze current screen
            analysis = self.capture_and_analyze()
            if not analysis:
                return False
            
            # Determine context and appropriate actions
            context = analysis.get("context", "general")
            self.current_context = context
            
            logger.info(f"Assisting with task: '{task_description}' in context: '{context}'")
            
            # Execute context-specific assistance
            success = self._execute_context_assistance(task_description, analysis)
            
            return success
            
        except Exception as e:
            logger.error(f"Error providing assistance: {e}")
            return False
    
    def automate_sequence(self, actions: List[Dict[str, Any]]) -> bool:
        """
        Execute a sequence of automated actions.
        
        Args:
            actions: List of action dictionaries
            
        Returns:
            True if all actions completed successfully, False otherwise
        """
        try:
            sequence = ActionSequence(self.interaction_controller)
            
            for action in actions:
                action_type = action.get("type")
                
                if action_type == "click":
                    sequence.add_click(action["x"], action["y"], 
                                     action.get("button", "left"))
                elif action_type == "type":
                    sequence.add_type(action["text"])
                elif action_type == "key":
                    sequence.add_key(action["key"])
                elif action_type == "wait":
                    sequence.add_wait(action["seconds"])
                else:
                    logger.warning(f"Unknown action type: {action_type}")
            
            return sequence.execute()
            
        except Exception as e:
            logger.error(f"Error executing automation sequence: {e}")
            return False
    
    def get_assistance_suggestions(self) -> List[str]:
        """
        Get suggestions for assistance based on current screen context.
        
        Returns:
            List of suggested assistance actions
        """
        try:
            if not self.detected_elements:
                return ["Take screenshot and analyze screen"]
            
            suggestions = []
            context = self.current_context
            
            # Context-specific suggestions
            if context == "learning":
                suggestions.extend([
                    "Highlight important text",
                    "Take screenshot for notes",
                    "Navigate to next section"
                ])
            elif context == "working":
                suggestions.extend([
                    "Copy selected text",
                    "Save current document",
                    "Open new file"
                ])
            elif context == "playing":
                suggestions.extend([
                    "Pause/resume media",
                    "Adjust volume",
                    "Enter fullscreen mode"
                ])
            
            # General suggestions based on detected elements
            button_count = len([e for e in self.detected_elements if e.element_type == "button"])
            if button_count > 0:
                suggestions.append(f"Click one of {button_count} detected buttons")
            
            return suggestions[:5]  # Limit to top 5 suggestions
            
        except Exception as e:
            logger.error(f"Error generating suggestions: {e}")
            return []
    
    def _analyze_context(self, ui_elements: List[UIElement], text_regions: List[Dict]) -> str:
        """Analyze the current context based on detected elements."""
        try:
            # Simple context detection based on element patterns
            # In a real implementation, this would be more sophisticated
            
            element_types = [e.element_type for e in ui_elements]
            
            # Check for learning context indicators
            if len(text_regions) > 10:  # Lots of text = learning/reading
                return "learning"
            
            # Check for working context indicators
            button_count = element_types.count("button")
            if button_count > 5:  # Many buttons = work application
                return "working"
            
            # Default to general context
            return "general"
            
        except Exception as e:
            logger.error(f"Error analyzing context: {e}")
            return "general"
    
    def _execute_context_assistance(self, task_description: str, analysis: Dict[str, Any]) -> bool:
        """Execute assistance based on current context."""
        try:
            context = analysis.get("context", "general")
            ui_elements = analysis.get("ui_elements", [])
            
            # Simple task execution based on keywords
            task_lower = task_description.lower()
            
            if "click" in task_lower and "button" in task_lower:
                # Find and click a button
                button = self.find_element("button")
                if button:
                    return self.click_element(button)
            
            elif "type" in task_lower or "enter" in task_lower:
                # Extract text to type (simplified)
                text_start = task_lower.find("type") + 4
                text_to_type = task_description[text_start:].strip().strip('"\'')
                if text_to_type:
                    return self.interaction_controller.type_text(text_to_type)
            
            elif "save" in task_lower:
                # Execute save command
                return self.interaction_controller.key_combination(["ctrl", "s"])
            
            elif "copy" in task_lower:
                # Execute copy command
                return self.interaction_controller.key_combination(["ctrl", "c"])
            
            elif "paste" in task_lower:
                # Execute paste command
                return self.interaction_controller.key_combination(["ctrl", "v"])
            
            logger.info(f"No specific assistance action found for: {task_description}")
            return False
            
        except Exception as e:
            logger.error(f"Error executing context assistance: {e}")
            return False
    
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the assistant."""
        return {
            "initialized": True,
            "safety_mode": self.safety_mode,
            "current_context": self.current_context,
            "detected_elements_count": len(self.detected_elements),
            "last_analysis_time": getattr(self, '_last_analysis_time', None),
            "screen_size": self.screen_capture.get_screen_size()
        }