"""
input_orchestrator.py

Orchestrates synchronized multi-modal input (visual, audio, keyboard, mouse) for embodied agent.
- Aggregates all inputs at a fixed timestep (e.g., 1/60th second).
- Packages data into unified AgentObservation objects for downstream processing or database insertion.
"""

import time
import os
import numpy as np
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
        audio_chunk = self.audio_capture.get_one_second_chunk()
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
                # Convert bytes to numpy array with correct shape (height, width, 3)
                width, height = video_frame.size
                arr = np.frombuffer(video_frame.rgb, dtype=np.uint8).reshape((height, width, 3))
                obs['video_frame'] = arr
            except Exception as e:
                print(f"[ERROR] Could not save frame or extract bytes: {e}")
                obs['video_frame'] = None
        else:
            obs['video_frame'] = None
        # Add shape and dtype for video_frame if present
        if obs['video_frame'] is not None and isinstance(obs['video_frame'], np.ndarray):
            obs['video_frame_shape'] = obs['video_frame'].shape
            obs['video_frame_dtype'] = str(obs['video_frame'].dtype)
        else:
            obs['video_frame_shape'] = None
            obs['video_frame_dtype'] = None
        obs['timestamp'] = timestamp
        # Store audio as numpy array in memory, serialize for DB
        obs['audio_chunk'] = audio_chunk
        if audio_chunk is not None and isinstance(audio_chunk, np.ndarray):
            obs['audio_shape'] = audio_chunk.shape
            obs['audio_dtype'] = str(audio_chunk.dtype)
        else:
            obs['audio_shape'] = None
            obs['audio_dtype'] = None
        obs['keyboard_state'] = keyboard_state
        obs['mouse_state'] = mouse_state
        obs['events'] = events
        print(f"[DEBUG] Final obs['video_frame'] type: {type(obs['video_frame'])}, length: {len(obs['video_frame']) if obs['video_frame'] is not None else 'NULL'}")
        print(f"[DEBUG] Final obs['video_frame_shape']: {obs['video_frame_shape']}, obs['video_frame_dtype']: {obs['video_frame_dtype']}")
        print(f"[DEBUG] Final obs['audio_shape']: {obs['audio_shape']}, obs['audio_dtype']: {obs['audio_dtype']}")
        return obs

    def stream_observations(self, duration=1.0):
        end_time = time.time() + duration
        observations = []
        while time.time() < end_time:
            obs = self.get_observation()
            observations.append(obs)
            time.sleep(self.timestep)
        return observations


# --- Streaming Perception and Learning Loop ---
import collections
import threading
import cv2  # For video writing
import soundfile as sf  # For audio writing

class OnlineAgentRunner:
    def __init__(self, orchestrator, perception_pipeline, agent, buffer_size=60, record_video=False, record_audio=False, video_path='session_video.avi', audio_path='session_audio.wav'):
        self.orchestrator = orchestrator
        self.perception_pipeline = perception_pipeline  # Callable: obs -> features
        self.agent = agent  # Must have observe(features) method
        self.buffer = collections.deque(maxlen=buffer_size)  # Short-term buffer
        self.episodic_memory = []  # For salient episodes/events
        self.record_video = record_video
        self.record_audio = record_audio
        self.video_writer = None
        self.audio_frames = []
        self.video_path = video_path
        self.audio_path = audio_path
        self._init_video_writer = False

    def run(self, duration=10.0):
        start_time = time.time()
        while time.time() - start_time < duration:
            obs = self.orchestrator.get_observation()
            # --- Optional: Raw Data Storage ---
            if self.record_video and obs.get('video_frame') is not None:
                frame = obs['video_frame']
                if not self._init_video_writer:
                    height, width, _ = frame.shape
                    self.video_writer = cv2.VideoWriter(self.video_path, cv2.VideoWriter_fourcc(*'XVID'), 1/self.orchestrator.timestep, (width, height))
                    self._init_video_writer = True
                self.video_writer.write(frame)
            if self.record_audio and obs.get('audio_chunk') is not None:
                self.audio_frames.append(obs['audio_chunk'])
            # --- Perception and Agent ---
            features = self.perception_pipeline(obs)
            self.buffer.append({'timestamp': obs['timestamp'], 'features': features})
            self.agent.observe(features, buffer=list(self.buffer))
            # --- Episodic Memory (example: store salient events) ---
            if hasattr(self.agent, 'is_salient') and self.agent.is_salient(features):
                self.episodic_memory.append({'timestamp': obs['timestamp'], 'features': features})
        # --- Finalize video/audio writing ---
        if self.record_video and self.video_writer is not None:
            self.video_writer.release()
        if self.record_audio and self.audio_frames:
            # Concatenate and save audio
            audio_data = np.concatenate(self.audio_frames, axis=0)
            sf.write(self.audio_path, audio_data, self.orchestrator.audio_capture.samplerate)

# --- Example Usage ---
# from input_orchestrator import InputOrchestrator
# from agent import MyAgent
# from perception import perception_pipeline
# orchestrator = InputOrchestrator(...)
# agent = MyAgent(...)
# runner = OnlineAgentRunner(orchestrator, perception_pipeline, agent, buffer_size=60, record_video=True, record_audio=True)
# runner.run(duration=60.0)

# Documentation:
# - OnlineAgentRunner streams observations, processes them through perception, and feeds them to the agent in real time.
# - A short-term buffer (deque) is maintained for temporal context.
# - Optionally records raw video/audio for later review, with timestamps for alignment.
# - Episodic memory stores only salient events (if agent provides is_salient()).
# - No database insertion of raw observations; only features/episodes are stored as needed.
