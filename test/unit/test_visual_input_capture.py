import os
import tempfile
from visual.visual_capture import VisualInputCapture

def test_visual_input_capture_pause_resume():
    region = {"top": 0, "left": 0, "width": 100, "height": 100}
    with tempfile.TemporaryDirectory() as tmpdir:
        capture = VisualInputCapture(region, tmpdir, frame_rate=1)
        # Should not be paused initially
        assert not capture.paused
        # Pause and check
        capture.pause()
        assert capture.paused
        assert capture.get_frame() is None
        # Resume and check
        capture.resume()
        assert not capture.paused
        frame = capture.get_frame()
        assert frame is not None

if __name__ == "__main__":
    test_visual_input_capture_pause_resume()
    print("VisualInputCapture pause/resume test passed.")
