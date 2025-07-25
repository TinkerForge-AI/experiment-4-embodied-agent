"""
test/test_agent_env_interface.py

Integration test: Runs the full agent-environment interface loop, capturing multi-modal observations and sending dummy actions to the game (via pynput). Verifies orchestrator control, window focus logic, and action dispatch.
"""

import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from agent_env_interface.agent_env_interface import AgentEnvInterface
from input.input_orchestrator import InputOrchestrator
from visual.visual_capture import VisualInputCapture
from audio.audio_capture import AudioInputCapture
from input.input_capture import InputCapture


# Real window manager using wmctrl
import subprocess
class RealWindowManager:
    def print_current_focus(self):
        import re, os
        if not os.environ.get('DISPLAY'):
            os.environ['DISPLAY'] = ':0'
        result = subprocess.run(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE, text=True)
        line = result.stdout.strip()
        match = re.search(r'window id # (0x[0-9a-fA-F]+)', line)
        if match:
            focused_id_hex = match.group(1).lower()
            focused_id_dec = int(focused_id_hex, 16)
            def normalize_id(win_id):
                return win_id.lower().replace('0x', '').zfill(8)
            # Print normalized IDs for all open windows
            for win in self.list_windows():
                print(f"  ID: {win['id']} | Normalized: {normalize_id(win['id'])} | Title: {win['title']}")
    def __init__(self, target_id=None, target_name=None):
        self.target_id = target_id
        self.target_name = target_name

    def list_windows(self):
        result = subprocess.run(['wmctrl', '-l'], stdout=subprocess.PIPE, text=True)
        windows = []
        for line in result.stdout.splitlines():
            parts = line.split(None, 3)
            if len(parts) == 4:
                win_id, desktop, host, title = parts
                windows.append({'id': win_id, 'title': title})
        return windows

    def is_focused(self):
        import re, os
        if not os.environ.get('DISPLAY'):
            os.environ['DISPLAY'] = ':0'
        def normalize_id(win_id):
            return win_id.lower().replace('0x', '').zfill(8)
        result = subprocess.run(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE, text=True)
        line = result.stdout.strip()
        match = re.search(r'window id # (0x[0-9a-fA-F]+)', line)
        if match:
            focused_id_hex = match.group(1).lower()
            focused_id_dec = int(focused_id_hex, 16)
            def normalize_id(win_id):
                return win_id.lower().replace('0x', '').zfill(8)
            if self.target_id and normalize_id(focused_id_hex) == normalize_id(self.target_id):
                return True
        return False

# Dummy agent for testing (random actions)
import random
from pynput.keyboard import Key
from pynput.mouse import Button

def random_action():
    if random.random() < 0.5:
        return {'type': 'keyboard', 'key': 'w', 'press': True}
    else:
        return {'type': 'mouse', 'move': (random.randint(-5,5), random.randint(-5,5)), 'click': Button.left}

def run_agent_env_interface_test(duration=5.0, timestep=1/10):
    region = {"top": 0, "left": 0, "width": 1280, "height": 720}
    video_capture = VisualInputCapture(region, output_dir="/tmp/frames", frame_rate=int(1/timestep))
    audio_capture = AudioInputCapture(output_dir="/tmp/audio", samplerate=44100, channels=2, segment_duration=timestep)
    input_capture = InputCapture()
    orchestrator = InputOrchestrator(video_capture, audio_capture, input_capture, timestep=timestep)
    # Use the window ID for derek@derek-Precision-3520: ~
    window_manager = RealWindowManager(target_id="0x3e00004")
    interface = AgentEnvInterface(orchestrator, window_manager)

    print(f"Starting agent-environment interface test for {duration} seconds...")
    start_time = time.time()
    step_count = 0
    while time.time() - start_time < duration:
        obs = interface.get_observation()
        action = random_action()
        interface.send_action(action)
        step_count += 1
        time.sleep(timestep)
    print(f"Test complete. {step_count} steps executed.")

if __name__ == "__main__":
    # Instantiate wm before using it
    wm = RealWindowManager()
    # Print the currently focused window for debugging
    wm.print_current_focus()
    # List all open windows
    windows = wm.list_windows()
    print("Open windows detected:")
    for win in windows:
        print(f"ID: {win['id']} | Title: {win['title']}")

    # Quick focus test loop
    test_wm = RealWindowManager(target_id="0x2c00004")
    print("Starting window focus test. Press Ctrl+C to exit.")
    last_status = None
    try:
        while True:
            focused = test_wm.is_focused()
            if focused != last_status:
                last_status = focused
                status_str = "focused" if focused else "lost focus"
                print(f"Window {status_str} ({test_wm.target_id})")
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Exiting focus test.")

    # Run the agent-environment integration test
    print("\nRunning agent-environment interface integration test...")
    run_agent_env_interface_test()
