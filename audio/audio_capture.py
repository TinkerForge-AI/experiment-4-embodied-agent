    # Usage: orchestrator calls get_chunk(num_samples) each timestep to retrieve the latest audio segment
"""
audio_capture.py

Audio input capture for embodied agent using sounddevice.
- Captures stereo, high-quality audio from the default input/output device.
- Saves audio segments to a training directory for agent processing.
- Removes audio files after processing to manage storage.
"""

import sounddevice as sd
import numpy as np
import os
import time
from scipy.io.wavfile import write
from datetime import datetime

class AudioInputCapture:
    def __init__(self, output_dir, samplerate=44100, channels=2, segment_duration=2):
        """
        output_dir: directory to save audio segments
        samplerate: audio sample rate (Hz)
        channels: number of audio channels (2 for stereo)
        segment_duration: duration of each audio segment (seconds)
        """
        self.output_dir = output_dir
        self.samplerate = samplerate
        self.channels = channels
        self.segment_duration = segment_duration
        os.makedirs(self.output_dir, exist_ok=True)

    def get_chunk(self, num_samples):
        """
        Capture and return a chunk of audio samples.
        """
        audio = sd.rec(num_samples, samplerate=self.samplerate, channels=self.channels, dtype='int16')
        sd.wait()
        return audio

    def capture_segments(self, total_duration=10):
        """
        Capture audio segments for a given total duration (seconds).
        """
        num_segments = int(total_duration / self.segment_duration)
        for _ in range(num_segments):
            print(f"Recording {self.segment_duration}s segment...")
            audio = sd.rec(int(self.segment_duration * self.samplerate), samplerate=self.samplerate, channels=self.channels, dtype='int16')
            sd.wait()
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
            segment_path = os.path.join(self.output_dir, f"audio_{timestamp}.wav")
            write(segment_path, self.samplerate, audio)
            # Here you would process the audio for training
            # For demo, we'll just remove it after a short delay
            time.sleep(0.5)
            os.remove(segment_path)

if __name__ == "__main__":
    output_dir = "training_data/audio"
    capture = AudioInputCapture(output_dir, samplerate=44100, channels=2, segment_duration=2)
    capture.capture_segments(total_duration=10)
