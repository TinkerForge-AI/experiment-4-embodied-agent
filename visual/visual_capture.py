    # Usage: orchestrator calls get_frame() each timestep to retrieve the latest frame
"""
visual_input_capture.py

Visual input capture for embodied agent using mss.
- Captures frames from a specified region (game window or screen).
- Saves frames to a training directory for agent processing.
- Removes frames after processing to manage storage.
"""

import mss
import mss.tools
import os
import time
from datetime import datetime

class VisualInputCapture:
    def __init__(self, region, output_dir, frame_rate=10):
        """
        region: dict with 'top', 'left', 'width', 'height' keys
        output_dir: directory to save frames
        frame_rate: frames per second
        """
        self.region = region
        self.output_dir = output_dir
        self.frame_rate = frame_rate
        os.makedirs(self.output_dir, exist_ok=True)
        self.paused = False

    def get_frame(self):
        """
        Capture and return a single frame from the specified region.
        Returns None if paused.
        """
        if self.paused:
            return None
        with mss.mss() as sct:
            img = sct.grab(self.region)
            return img  # You may convert to numpy array if needed
    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def capture_frames(self, duration=5):
        """
        Capture frames for a given duration (seconds).
        """
        with mss.mss() as sct:
            end_time = time.time() + duration
            while time.time() < end_time:
                img = sct.grab(self.region)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
                frame_path = os.path.join(self.output_dir, f"frame_{timestamp}.png")
                mss.tools.to_png(img.rgb, img.size, output=frame_path)
                # Here you would process the frame for training
                # For demo, we'll just remove it after a short delay
                time.sleep(1.0 / self.frame_rate)
                os.remove(frame_path)

if __name__ == "__main__":
    # Example region: top-left corner, 1280x720
    region = {"top": 0, "left": 0, "width": 1280, "height": 720}
    # Use absolute path for output_dir to avoid issues when running as module
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "training_data", "frames"))
    capture = VisualInputCapture(region, output_dir, frame_rate=10)
    capture.capture_frames(duration=5)
