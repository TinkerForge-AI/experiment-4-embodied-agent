"""
db_insert.py

Functions to insert AgentObservation data from input_orchestrator into PostgreSQL/TimescaleDB.
"""

import psycopg2
import json
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
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO agent_observations (
                timestamp, video_frame, audio_chunk, keyboard_state, mouse_state, events
            ) VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                observation['timestamp'],
                observation.get('video_frame'),   # Should be bytes
                observation.get('audio_chunk').tobytes() if observation.get('audio_chunk') is not None else None,
                json.dumps(observation.get('keyboard_state')),
                json.dumps(observation.get('mouse_state')),
                json.dumps(observation.get('events'))
                # Store shape and dtype for reconstruction
                # You may want to add columns to your DB for audio_shape and audio_dtype
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
        obs = AgentObservation(
            timestamp=now,
            video_frame=b'test_image_bytes',
            audio_chunk=b'test_audio_bytes',
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