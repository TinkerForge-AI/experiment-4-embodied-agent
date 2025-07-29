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
    def __init__(self, output_dir, samplerate=44100, channels=2, segment_duration=0.02):
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
        self.paused = False

    def get_chunk(self, num_samples):
        """
        Capture and return a chunk of audio samples of length num_samples.
        Returns zeros if paused.
        """
        if self.paused:
            return np.zeros((num_samples, self.channels), dtype='int16')
        audio = sd.rec(num_samples, samplerate=self.samplerate, channels=self.channels, dtype='int16')
        sd.wait()
        return audio

    def get_one_second_chunk(self):
        """
        Capture and return exactly 1 second of audio (44100 samples per channel at 44.1kHz).
        Returns zeros if paused.
        """
        return self.get_chunk(self.samplerate)
    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stream_audio(self, callback, segment_duration=None, parallel=False, max_workers=4):
        """
        Continuously stream audio segments and process them with a callback.
        Args:
            callback: function to call with (audio_chunk, timestamp) for each segment
            segment_duration: duration of each audio segment (seconds), defaults to self.segment_duration
            parallel: if True, use ThreadPoolExecutor for parallel processing
            max_workers: number of parallel workers if parallel=True
        """
        import concurrent.futures
        if segment_duration is None:
            segment_duration = self.segment_duration
        print(f"[AudioInputCapture] Starting audio stream with segment_duration={segment_duration}s, parallel={parallel}...")
        executor = None
        if parallel:
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)
        try:
            while True:
                if self.paused:
                    time.sleep(0.1)
                    continue
                t_capture_start = time.time()
                print(f"[AudioInputCapture] Recording {segment_duration}s segment...")
                audio = sd.rec(int(segment_duration * self.samplerate), samplerate=self.samplerate, channels=self.channels, dtype='int16')
                sd.wait()
                timestamp = datetime.now().timestamp()
                t_capture_end = time.time()
                capture_lag = t_capture_end - t_capture_start
                print(f"[DEBUG] Audio segment captured in {capture_lag:.4f}s at timestamp {timestamp}")
                def process_and_log(audio, timestamp):
                    t_proc_start = time.time()
                    callback(audio, timestamp)
                    t_proc_end = time.time()
                    proc_lag = t_proc_end - t_proc_start
                    print(f"[DEBUG] Perception processing time: {proc_lag:.4f}s (segment timestamp: {timestamp})")
                if parallel:
                    executor.submit(process_and_log, audio, timestamp)
                else:
                    process_and_log(audio, timestamp)
        except KeyboardInterrupt:
            print("[AudioInputCapture] Audio streaming stopped by user.")
        finally:
            if executor:
                executor.shutdown(wait=True)

if __name__ == "__main__":
    output_dir = "training_data/audio"
    capture = AudioInputCapture(output_dir, samplerate=44100, channels=2, segment_duration=2)
    capture.capture_segments(total_duration=10)
