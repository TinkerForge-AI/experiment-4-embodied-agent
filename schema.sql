-- PostgreSQL schema for agent observations with TimescaleDB

CREATE TABLE agent_observations (
    id SERIAL,
    timestamp TIMESTAMPTZ NOT NULL,
    video_frame BYTEA,
    audio_chunk BYTEA,
    keyboard_state JSONB,
    mouse_state JSONB,
    events JSONB,
    -- Visual perception features
    edges TEXT,
    dominant_color TEXT,
    motion_detected BOOLEAN,
    change_detected BOOLEAN,
    light_dark TEXT,
    visual_attention TEXT,
    text TEXT,
    npc_detected BOOLEAN,
    objects JSONB,
    PRIMARY KEY (id, timestamp)
);

-- Convert to TimescaleDB hypertable
SELECT create_hypertable('agent_observations', 'timestamp');