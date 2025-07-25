"""
input_orchestrator.py

Orchestrates synchronized multi-modal input (visual, audio, keyboard, mouse) for embodied agent.
- Aggregates all inputs at a fixed timestep (e.g., 1/60th second).
- Packages data into unified AgentObservation objects for downstream processing or database insertion.
"""

import time
import os
import mss
from datetime import datetime

class AgentObservation:
    def __init__(self, timestamp, video_frame, audio_chunk, keyboard_state, mouse_state, events):
        self.timestamp = timestamp
        self.video_frame = video_frame
        self.audio_chunk = audio_chunk
        self.keyboard_state = keyboard_state  # dict: key -> duration held
        self.mouse_state = mouse_state        # dict: button -> duration held, position
        self.events = events                  # list of raw events in this timestep

class InputOrchestrator:
    def pause(self):
        """Pause all input capture systems."""
        if hasattr(self.video_capture, 'pause'):
            self.video_capture.pause()
        if hasattr(self.audio_capture, 'pause'):
            self.audio_capture.pause()
        if hasattr(self.input_capture, 'pause'):
            self.input_capture.pause()
        print("[InputOrchestrator] Paused all input capture systems.")
    def __init__(self, video_capture, audio_capture, input_capture, timestep=1/60):
        self.video_capture = video_capture      # e.g., VisualInputCapture instance
        self.audio_capture = audio_capture      # e.g., AudioInputCapture instance
        self.input_capture = input_capture      # e.g., InputCapture instance
        self.timestep = timestep
        self.last_time = time.time()

    def get_observation(self):
        now = time.time()
        timestamp = datetime.now().isoformat(sep=' ', timespec='microseconds')
        video_frame = None
        if self.video_capture:
            video_frame = self.video_capture.get_frame()
            if video_frame is not None:
                try:
                    frame_bytes = video_frame.rgb if hasattr(video_frame, 'rgb') else None
                except Exception as e:
                    print(f"[ERROR] Could not access video_frame.rgb: {e}")
            else:
                print("[WARN] video_frame is None!")
        audio_chunk = self.audio_capture.get_chunk(int(44100 * self.timestep))
        keyboard_state, mouse_state = self.input_capture.get_current_state()
        events = self.input_capture.get_events_since(self.last_time, now)
        self.last_time = now
        obs = {}
        # Visual
        if self.video_capture and video_frame is not None:
            frame_path = os.path.join(self.video_capture.output_dir, f"frame_{timestamp}.png")
            try:
                mss.tools.to_png(video_frame.rgb, video_frame.size, output=frame_path)
                obs['visual_frame_path'] = frame_path
                obs['video_frame'] = video_frame.rgb  # Add raw bytes for DB
            except Exception as e:
                print(f"[ERROR] Could not save frame or extract bytes: {e}")
                obs['video_frame'] = None
        else:
            obs['video_frame'] = None
        obs['timestamp'] = timestamp
        # Store audio as numpy array in memory, serialize for DB
        obs['audio_chunk'] = audio_chunk
        obs['audio_shape'] = audio_chunk.shape
        obs['audio_dtype'] = str(audio_chunk.dtype)
        obs['keyboard_state'] = keyboard_state
        obs['mouse_state'] = mouse_state
        obs['events'] = events
        print(f"[DEBUG] Final obs['video_frame'] type: {type(obs['video_frame'])}, length: {len(obs['video_frame']) if obs['video_frame'] is not None else 'NULL'}")
        return obs

    def stream_observations(self, duration=1.0):
        end_time = time.time() + duration
        observations = []
        while time.time() < end_time:
            obs = self.get_observation()
            observations.append(obs)
            time.sleep(self.timestep)
        return observations

# Note: Implement get_frame(), get_chunk(), get_current_state(), and get_events_since() in your respective input modules.
# This orchestrator can be extended to insert observations into a database or pass them to the agent core.
