"""
Computer vision module for UI element detection using YOLO and OpenCV.
"""

import cv2
import numpy as np
from typing import List, Tuple, Dict, Optional
import logging
import os

try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except ImportError:
    YOLO_AVAILABLE = False

logger = logging.getLogger(__name__)


class UIElement:
    """Represents a detected UI element."""
    
    def __init__(self, element_type: str, confidence: float, bbox: Tuple[int, int, int, int], 
                 center: Tuple[int, int] = None):
        self.element_type = element_type
        self.confidence = confidence
        self.bbox = bbox  # (x, y, width, height)
        self.center = center or (bbox[0] + bbox[2] // 2, bbox[1] + bbox[3] // 2)
    
    def __repr__(self):
        return f"UIElement(type='{self.element_type}', confidence={self.confidence:.2f}, center={self.center})"


class VisionProcessor:
    """Computer vision processor for detecting UI elements."""
    
    def __init__(self, model_path: Optional[str] = None):
        self.model = None
        self.template_matcher = TemplateManager()
        
        # Try to load YOLO model if available
        try:
            if not YOLO_AVAILABLE:
                logger.info("YOLO not available. Using template matching only.")
                return
                
            if model_path and os.path.exists(model_path):
                self.model = YOLO(model_path)
                logger.info(f"Loaded custom YOLO model from {model_path}")
            else:
                # Use pre-trained model for general object detection
                self.model = YOLO('yolov8n.pt')
                logger.info("Loaded pre-trained YOLOv8 model")
        except ImportError:
            logger.warning("Ultralytics not available. Using template matching only.")
        except Exception as e:
            logger.warning(f"Could not load YOLO model: {e}. Falling back to template matching.")
    
    def detect_ui_elements(self, image: np.ndarray) -> List[UIElement]:
        """
        Detect UI elements in the given image.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            List of detected UI elements
        """
        elements = []
        
        # Try YOLO detection first
        if self.model:
            try:
                results = self.model(image)
                for result in results:
                    boxes = result.boxes
                    if boxes is not None:
                        for box in boxes:
                            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                            conf = box.conf[0].cpu().numpy()
                            cls = int(box.cls[0].cpu().numpy())
                            
                            # Convert to our format
                            width = int(x2 - x1)
                            height = int(y2 - y1)
                            bbox = (int(x1), int(y1), width, height)
                            
                            # Map class to UI element type (simplified)
                            element_type = self._map_class_to_ui_element(cls)
                            
                            elements.append(UIElement(element_type, float(conf), bbox))
            except Exception as e:
                logger.error(f"Error in YOLO detection: {e}")
        
        # Add template-based detection for common UI elements
        template_elements = self.template_matcher.detect_common_elements(image)
        elements.extend(template_elements)
        
        return elements
    
    def detect_text(self, image: np.ndarray) -> List[Dict]:
        """
        Detect text regions in the image using OpenCV.
        
        Args:
            image: Input image as numpy array
            
        Returns:
            List of text regions with bounding boxes
        """
        text_regions = []
        
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply EAST text detector if available, otherwise use simple contour detection
            text_regions = self._detect_text_simple(gray)
            
        except Exception as e:
            logger.error(f"Error in text detection: {e}")
        
        return text_regions
    
    def _detect_text_simple(self, gray_image: np.ndarray) -> List[Dict]:
        """Simple text detection using morphological operations."""
        text_regions = []
        
        try:
            # Apply threshold
            _, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
            
            # Create kernel for morphological operations
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
            connected = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            
            # Find contours
            contours, _ = cv2.findContours(connected, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                x, y, w, h = cv2.boundingRect(contour)
                # Filter by size
                if w > 20 and h > 10 and w < 800 and h < 100:
                    text_regions.append({
                        'bbox': (x, y, w, h),
                        'center': (x + w // 2, y + h // 2),
                        'confidence': 0.7  # Simple heuristic
                    })
        
        except Exception as e:
            logger.error(f"Error in simple text detection: {e}")
        
        return text_regions
    
    def _map_class_to_ui_element(self, class_id: int) -> str:
        """Map YOLO class ID to UI element type."""
        # This is a simplified mapping - in practice, you'd train a custom model
        # for UI elements like buttons, text fields, etc.
        class_map = {
            0: 'object',  # person -> general UI element
            67: 'phone',  # cell phone
            73: 'laptop',  # laptop
            76: 'remote'  # remote -> button-like
        }
        return class_map.get(class_id, 'unknown')


class TemplateManager:
    """Manages template matching for common UI elements."""
    
    def __init__(self):
        self.templates = {}
        self._load_default_templates()
    
    def _load_default_templates(self):
        """Load default templates for common UI elements."""
        # In a real implementation, you'd load actual template images
        # For now, we'll use shape-based detection
        pass
    
    def detect_common_elements(self, image: np.ndarray) -> List[UIElement]:
        """Detect common UI elements using template matching and shape detection."""
        elements = []
        
        try:
            # Detect button-like rectangles
            button_elements = self._detect_buttons(image)
            elements.extend(button_elements)
            
        except Exception as e:
            logger.error(f"Error in template detection: {e}")
        
        return elements
    
    def _detect_buttons(self, image: np.ndarray) -> List[UIElement]:
        """Detect button-like rectangular elements."""
        buttons = []
        
        try:
            # Convert to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # Apply edge detection
            edges = cv2.Canny(gray, 50, 150, apertureSize=3)
            
            # Find contours
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            for contour in contours:
                # Approximate contour
                epsilon = 0.02 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)
                
                # Check if it's roughly rectangular (4 corners)
                if len(approx) >= 4:
                    x, y, w, h = cv2.boundingRect(contour)
                    
                    # Filter by size and aspect ratio (typical button characteristics)
                    if (30 < w < 300 and 20 < h < 80 and 
                        0.2 < h/w < 2.0):  # Reasonable button proportions
                        
                        bbox = (x, y, w, h)
                        confidence = 0.6  # Heuristic confidence
                        
                        buttons.append(UIElement('button', confidence, bbox))
        
        except Exception as e:
            logger.error(f"Error detecting buttons: {e}")
        
        return buttons