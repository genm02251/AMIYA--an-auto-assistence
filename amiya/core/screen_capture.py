"""
Cross-platform screen capture functionality for AMIYA AI Assistant.
"""

import platform
import numpy as np
from PIL import Image
import cv2
from typing import Tuple, Optional, List
import logging

# Platform-specific imports
if platform.system() == "Windows":
    import pygetwindow as gw
elif platform.system() == "Darwin":  # macOS
    try:
        import pygetwindow as gw
    except ImportError:
        gw = None
elif platform.system() == "Linux":
    try:
        import pygetwindow as gw
    except ImportError:
        gw = None

logger = logging.getLogger(__name__)


class ScreenCapture:
    """Cross-platform screen capture utility."""
    
    def __init__(self):
        self.system = platform.system()
        logger.info(f"Initialized screen capture for {self.system}")
    
    def capture_screen(self, region: Optional[Tuple[int, int, int, int]] = None) -> np.ndarray:
        """
        Capture the screen or a specific region.
        
        Args:
            region: Optional tuple (x, y, width, height) for specific region capture
            
        Returns:
            numpy array of the captured image in BGR format
        """
        try:
            # Check if PIL.Image.grab is available (not available in headless environments)
            if not hasattr(Image, 'grab'):
                logger.warning("PIL Image.grab not available (headless environment). Creating mock image.")
                # Create a mock image for testing
                width, height = (1920, 1080) if not region else (region[2], region[3])
                mock_image = np.zeros((height, width, 3), dtype=np.uint8)
                # Add some test pattern
                mock_image[height//4:3*height//4, width//4:3*width//4] = [100, 150, 200]
                return mock_image
            
            # Use PIL for cross-platform screenshot
            if region:
                x, y, width, height = region
                screenshot = Image.grab(bbox=(x, y, x + width, y + height))
            else:
                screenshot = Image.grab()
            
            # Convert PIL image to OpenCV format (BGR)
            screenshot_cv = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            return screenshot_cv
            
        except Exception as e:
            logger.error(f"Error capturing screen: {e}")
            raise
    
    def get_screen_size(self) -> Tuple[int, int]:
        """Get the screen resolution."""
        try:
            if not hasattr(Image, 'grab'):
                logger.warning("PIL Image.grab not available. Using default screen size.")
                return (1920, 1080)  # Default screen size for headless environment
            
            screenshot = Image.grab()
            return screenshot.size
        except Exception as e:
            logger.error(f"Error getting screen size: {e}")
            return (1920, 1080)  # Fallback default
    
    def get_window_list(self) -> List[str]:
        """Get list of open windows (platform dependent)."""
        try:
            if gw is not None:
                windows = gw.getAllWindows()
                return [w.title for w in windows if w.title.strip()]
            else:
                logger.warning("Window management not available on this platform")
                return []
        except Exception as e:
            logger.error(f"Error getting window list: {e}")
            return []
    
    def capture_window(self, window_title: str) -> Optional[np.ndarray]:
        """
        Capture a specific window by title.
        
        Args:
            window_title: Title of the window to capture
            
        Returns:
            numpy array of the captured window image or None if not found
        """
        try:
            if gw is not None:
                windows = gw.getWindowsWithTitle(window_title)
                if windows:
                    window = windows[0]
                    x, y, width, height = window.left, window.top, window.width, window.height
                    return self.capture_screen((x, y, width, height))
            
            logger.warning(f"Window '{window_title}' not found or window management not available")
            return None
            
        except Exception as e:
            logger.error(f"Error capturing window '{window_title}': {e}")
            return None