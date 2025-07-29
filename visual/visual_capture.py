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
                t0 = time.time()
                img = sct.grab(self.region)
                timestamp = t0
                frame_path = os.path.join(self.output_dir, f"frame_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.png")
                mss.tools.to_png(img.rgb, img.size, output=frame_path)
                print(f"[DEBUG] Frame captured in {time.time() - t0:.4f}s at timestamp {timestamp}")
                time.sleep(1.0 / self.frame_rate)
                os.remove(frame_path)

    def stream_frames(self, callback, duration=None):
        """
        Continuously capture frames and call callback(frame, timestamp) for each.
        If duration is set, stream for that many seconds; else, run until interrupted.
        """
        import traceback
        import numpy as np
        with mss.mss() as sct:
            start_time = time.time()
            try:
                while True:
                    t0 = time.time()
                    img = sct.grab(self.region)
                    # Convert ScreenShot to numpy array (H, W, 3, uint8)
                    frame = np.array(img)
                    # mss returns BGRA; convert to BGR for OpenCV compatibility
                    if frame.shape[2] == 4:
                        frame = frame[:, :, :3]
                    timestamp = t0
                    print(f"[DEBUG] Frame captured in {time.time() - t0:.4f}s at timestamp {timestamp}")
                    callback(frame, timestamp)
                    if duration and (time.time() - start_time) > duration:
                        break
                    time.sleep(max(0, 1.0 / self.frame_rate - (time.time() - t0)))
            except KeyboardInterrupt:
                print("[VisualInputCapture] Visual streaming stopped by user.")
            except Exception as e:
                print(f"[ERROR] Exception in stream_frames: {e}\n{traceback.format_exc()}")

if __name__ == "__main__":
    # Example region: top-left corner, 1280x720
    region = {"top": 0, "left": 0, "width": 1280, "height": 720}
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "training_data", "frames"))
    capture = VisualInputCapture(region, output_dir, frame_rate=10)
    print("[INFO] Starting visual streaming test. Press Ctrl+C to stop.")
    def dummy_callback(frame, timestamp):
        print(f"[DEBUG] Frame at {timestamp}, shape: {getattr(frame, 'size', None)}")
    capture.stream_frames(dummy_callback, duration=5)
