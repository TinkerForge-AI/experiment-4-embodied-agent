"""
test_perception.py (visual, streaming)

Test script to stream live visual frames through the visual perception pipeline and print results in real time.
"""

import time
from visual_capture import VisualInputCapture
from perception import VisualPerception

def perception_callback(frame, timestamp):
    vp = VisualPerception()
    obs = vp.process_frame(frame, frame_timestamp=timestamp)
    print("\n[RESULT] Visual perception output:")
    for k, v in obs.items():
        if isinstance(v, dict) and 'lag' in v:
            print(f"  {k}: value={v['value']}, lag={v['lag']:.4f}s")
        else:
            print(f"  {k}: {v}")

if __name__ == "__main__":
    region = {"top": 0, "left": 0, "width": 1280, "height": 720}
    output_dir = "training_data/frames"
    capture = VisualInputCapture(region, output_dir, frame_rate=5)
    print("[INFO] Starting visual streaming test. Press Ctrl+C to stop.")
    capture.stream_frames(perception_callback)
