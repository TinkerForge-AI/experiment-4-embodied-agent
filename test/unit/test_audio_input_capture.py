import numpy as np
from audio.audio_capture import AudioInputCapture

def test_audio_input_capture_pause_resume():
    capture = AudioInputCapture("/tmp", samplerate=8000, channels=1, segment_duration=1)
    capture.pause()
    chunk = capture.get_one_second_chunk()
    assert np.all(chunk == 0)
    capture.resume()
    chunk = capture.get_one_second_chunk()
    assert chunk.shape == (100, 1)

if __name__ == "__main__":
    test_audio_input_capture_pause_resume()
    print("AudioInputCapture pause/resume test passed.")
