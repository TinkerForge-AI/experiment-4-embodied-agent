"""
test/test_full_capture.py

Comprehensive test: Runs all input capture systems, synchronizes data for 5 seconds, and inserts observations into the database.
"""

import time
import psycopg2
from db.db_insert import insert_observation
from input.input_orchestrator import InputOrchestrator
from visual.visual_capture import VisualInputCapture
from audio.audio_capture import AudioInputCapture
from input.input_capture import InputCapture
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')

def run_full_capture_test(dbname='embodied_agent', user='agent', password='agent', host='localhost', duration=5.0, timestep=1/60):
    # Example region for visual input (customize as needed)
    region = {"top": 0, "left": 0, "width": 1280, "height": 720}
    video_capture = VisualInputCapture(region, output_dir="/tmp/frames", frame_rate=int(1/timestep))
    audio_capture = AudioInputCapture(output_dir="/tmp/audio", samplerate=44100, channels=2, segment_duration=timestep)
    input_capture = InputCapture()
    orchestrator = InputOrchestrator(video_capture, audio_capture, input_capture, timestep=timestep)

    # Connect to database
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    print("Database connection successful!")

    # Start listeners for keyboard/mouse
    input_capture.start_listeners()

    print(f"Starting synchronized capture for {duration} seconds...")
    start_time = time.time()
    obs_count = 0
    while time.time() - start_time < duration:
        obs = orchestrator.get_observation()
        insert_observation(conn, obs)
        obs_count += 1
        time.sleep(timestep)
    conn.close()
    print(f"Capture complete. {obs_count} observations inserted.")

if __name__ == "__main__":
    run_full_capture_test()
