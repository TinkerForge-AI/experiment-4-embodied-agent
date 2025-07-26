import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import time
from agent_env_interface.agent_env_interface import AgentEnvInterface
from input.input_orchestrator import InputOrchestrator
from visual.visual_capture import VisualInputCapture
from audio.audio_capture import AudioInputCapture
from input.input_capture import InputCapture
from agent.simple_agent import SimpleAgent


def run_full_system_e2e(duration=3.0, timestep=1/10):
    region = {"top": 0, "left": 0, "width": 100, "height": 100}
    video_capture = VisualInputCapture(region, "/tmp/frames", frame_rate=int(1/timestep))
    audio_capture = AudioInputCapture("/tmp/audio", samplerate=8000, channels=1, segment_duration=timestep)
    input_capture = InputCapture()
    orchestrator = InputOrchestrator(video_capture, audio_capture, input_capture, timestep=timestep)
    # Dummy window manager for test
    class DummyWindowManager:
        def is_focused(self): return True
    interface = AgentEnvInterface(orchestrator, DummyWindowManager())
    agent = SimpleAgent()
    print("Starting full system E2E test...")
    start_time = time.time()
    step = 0
    while time.time() - start_time < duration:
        obs = interface.get_observation()
        actions = agent.act(obs)
        for action in actions:
            # Only print keyboard and mouse actions
            if action.get('type') in ('keyboard', 'mouse'):
                print(f"Step {step}: Sending {action['type'].capitalize()} Action: {action}")
            interface.send_action(action)
        step += 1
        time.sleep(timestep)
    print("Full system E2E test completed.")

if __name__ == "__main__":
    run_full_system_e2e()
