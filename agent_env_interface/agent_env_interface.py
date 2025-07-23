"""
agent_env_interface.py

Agent-Environment Interface for Eastshade Experiment
--------------------------------------------------
This module provides a standardized interface between the agent and the game environment.
It manages orchestrator control, window focus, and action dispatch via keyboard/mouse (pynput).
Advanced features (state detection, reset/init, safety/intervention) are deferred for future development.
"""

import time
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Controller as MouseController

class AgentEnvInterface:
    def __init__(self, orchestrator, window_manager):
        self.orchestrator = orchestrator
        self.window_manager = window_manager  # Should provide is_focused() for Eastshade
        self.keyboard = KeyboardController()
        self.mouse = MouseController()
        self.paused = False

    def check_focus(self):
        """Check if Eastshade window is focused. Pause orchestrator if not."""
        if not self.window_manager.is_focused():
            if not self.paused:
                self.orchestrator.pause()
                self.paused = True
                print("[INFO] Eastshade not focused. Orchestrator paused.")
        else:
            if self.paused:
                self.orchestrator.resume()
                self.paused = False
                print("[INFO] Eastshade focused. Orchestrator resumed.")

    def send_action(self, action):
        """Send keyboard/mouse actions to the game via pynput."""
        self.check_focus()
        if self.paused:
            print("[WARN] Action not sent: Eastshade not focused.")
            return
        # Example action format: {'type': 'keyboard', 'key': 'w', 'press': True}
        if action['type'] == 'keyboard':
            key = action['key']
            if action.get('press', True):
                self.keyboard.press(key)
            else:
                self.keyboard.release(key)
        elif action['type'] == 'mouse':
            # Example: {'type': 'mouse', 'move': (dx, dy), 'click': 'left'}
            if 'move' in action:
                dx, dy = action['move']
                self.mouse.move(dx, dy)
            if 'click' in action:
                button = action['click']
                self.mouse.click(button)

    def get_observation(self):
        """Retrieve the latest synchronized observation from the orchestrator."""
        return self.orchestrator.get_observation()

    def run_session(self):
        """Main loop for agent-environment interaction."""
        while True:
            self.check_focus()
            if not self.paused:
                obs = self.get_observation()
                # Here, agent logic would decide on an action
                # action = agent.act(obs)
                # self.send_action(action)
            time.sleep(0.05)  # Adjust loop rate as needed

    # Advanced features (reset/init, state detection, safety/intervention) can be added later
