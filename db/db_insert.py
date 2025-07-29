"""
db_insert.py

Functions to insert AgentObservation data from input_orchestrator into PostgreSQL/TimescaleDB.
"""

import psycopg2
import json
import numpy as np
import datetime
import os
from dotenv import load_dotenv
def get_db_connection():
    load_dotenv()
    conn = psycopg2.connect(
        dbname=os.environ.get('DB_NAME'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT')
    )
    return conn

def insert_observation(conn, observation):
    """
    Insert a single AgentObservation into the database.
    observation: AgentObservation object
    conn: psycopg2 connection
    """
    video_frame = observation.get('video_frame')
    audio_chunk = observation.get('audio_chunk')
    # Track shape and dtype for video_frame if it's a numpy array
    video_frame_shape = None
    video_frame_dtype = None
    if isinstance(video_frame, np.ndarray):
        video_frame_shape = video_frame.shape
        video_frame_dtype = str(video_frame.dtype)
        video_frame_bytes = video_frame.tobytes()
    else:
        video_frame_bytes = video_frame
    print(f"[DB DEBUG] Inserting observation:")
    print(f"  timestamp: {observation['timestamp']}")
    print(f"  video_frame type: {type(video_frame)}, length: {len(video_frame) if video_frame is not None else 'NULL'}")
    print(f"  audio_chunk type: {type(audio_chunk)}, shape: {audio_chunk.shape if hasattr(audio_chunk, 'shape') else 'N/A'}")
    print(f"  keyboard_state: {observation.get('keyboard_state')}")
    print(f"  mouse_state: {observation.get('mouse_state')}")
    print(f"  events: {observation.get('events')}")
    audio_shape = observation.get('audio_shape')
    audio_dtype = observation.get('audio_dtype')
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO agent_observations (
                timestamp, video_frame, video_frame_shape, video_frame_dtype, audio_chunk, audio_shape, audio_dtype, keyboard_state, mouse_state, events
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                observation['timestamp'],
                psycopg2.Binary(video_frame_bytes) if video_frame_bytes is not None else None,
                json.dumps(video_frame_shape) if video_frame_shape is not None else None,
                video_frame_dtype,
                audio_chunk.tobytes() if audio_chunk is not None else None,
                json.dumps(audio_shape) if audio_shape is not None else None,
                audio_dtype,
                json.dumps(observation.get('keyboard_state')),
                json.dumps(observation.get('mouse_state')),
                json.dumps(observation.get('events'))
            )
        )
    conn.commit()

def test_db_insert_and_retrieve():
    try:
        conn = get_db_connection()
        print("Connection successful!")
        # Create a sample observation
        class AgentObservation:
            def __init__(self, timestamp, video_frame, audio_chunk, keyboard_state, mouse_state, events):
                self.timestamp = timestamp
                self.video_frame = video_frame
                self.audio_chunk = audio_chunk
                self.keyboard_state = keyboard_state
                self.mouse_state = mouse_state
                self.events = events

        now = datetime.datetime.utcnow()
        # Use a real numpy array for video_frame to test shape/dtype tracking
        video_frame = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        audio_chunk = np.random.randint(-32768, 32767, (48000, 2), dtype=np.int16)  # 1 sec stereo audio at 48kHz
        obs = AgentObservation(
            timestamp=now,
            video_frame=video_frame,
            audio_chunk=audio_chunk,
            keyboard_state={'W': 1.0},
            mouse_state={'buttons': {'left': 0.5}, 'position': (100, 200)},
            events=[('20250723_120000_000000', 'key_press', 'W')]
        )
        insert_observation(conn, obs)
        print("Inserted test observation.")

        # Retrieve the latest observation
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM agent_observations ORDER BY timestamp DESC LIMIT 1;")
            row = cur.fetchone()
            print("Latest observation:", row)
        conn.close()
    except Exception as e:
        print("Test failed:", e)

if __name__ == "__main__":
    test_db_insert_and_retrieve()