    # Usage: orchestrator calls get_current_state() each timestep to retrieve held keys/buttons and mouse position
    # Usage: orchestrator calls get_events_since(start_time, end_time) to retrieve events for the current timestep
"""
input_capture.py

Keyboard and mouse input capture and injection for embodied agent using pynput.
- Captures keyboard and mouse events for agent observation.
- Simulates keyboard and mouse actions, including holding keys/buttons for specified durations.
- Supports clamping mouse movement (e.g., horizontal only).
"""

from pynput import keyboard, mouse
import time
import os
from datetime import datetime

class InputCapture:
    def pause(self):
        if hasattr(self, 'keyboard_listener') and self.keyboard_listener:
            self.keyboard_listener.stop()
        if hasattr(self, 'mouse_listener') and self.mouse_listener:
            self.mouse_listener.stop()
        print("[InputCapture] Paused keyboard and mouse listeners.")
    def __init__(self):
        self.keyboard_controller = keyboard.Controller()
        self.mouse_controller = mouse.Controller()
        self.events = []  # Store captured events
        self.key_down_time = {}
        self.button_down_time = {}
        self.current_keys = set()
        self.current_buttons = set()
        self.mouse_position = (0, 0)
        self.keyboard_controller = keyboard.Controller()
        self.mouse_controller = mouse.Controller()
        self.events = []  # Store captured events

    # Keyboard event capture
    def on_press(self, key):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        self.key_down_time[key] = time.time()
        self.current_keys.add(key)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        self.events.append((timestamp, 'key_press', str(key)))

    def on_release(self, key):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        if key in self.key_down_time:
            duration = time.time() - self.key_down_time[key]
            self.events.append((timestamp, 'key_hold', str(key), duration))
            self.key_down_time.pop(key, None)
        self.current_keys.discard(key)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        self.events.append((timestamp, 'key_release', str(key)))

    # Mouse event capture
    def on_move(self, x, y):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        self.mouse_position = (x, y)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        self.events.append((timestamp, 'mouse_move', (x, y)))

    def on_click(self, x, y, button, pressed):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        if pressed:
            self.button_down_time[button] = time.time()
            self.current_buttons.add(button)
        else:
            if button in self.button_down_time:
                duration = time.time() - self.button_down_time[button]
                self.events.append((timestamp, 'button_hold', (x, y, str(button)), duration))
                self.button_down_time.pop(button, None)
            self.current_buttons.discard(button)
    def get_current_state(self):
        # Returns dicts of currently held keys/buttons and their durations, plus mouse position
        now = time.time()
        keyboard_state = {str(key): now - self.key_down_time[key] for key in self.current_keys}
        mouse_state = {
            'buttons': {str(btn): now - self.button_down_time[btn] for btn in self.current_buttons},
            'position': self.mouse_position
        }
        return keyboard_state, mouse_state

    def get_events_since(self, start_time, end_time):
        # Returns events that occurred between start_time and end_time
        filtered_events = [e for e in self.events if start_time <= self._event_time_to_float(e[0]) < end_time]
        return filtered_events

    def _event_time_to_float(self, timestamp):
        # Helper to convert timestamp string to float
        dt = datetime.strptime(timestamp, '%Y%m%d_%H%M%S_%f')
        return dt.timestamp()
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        action = 'mouse_press' if pressed else 'mouse_release'
        self.events.append((timestamp, action, (x, y, str(button))))

    def on_scroll(self, x, y, dx, dy):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        self.events.append((timestamp, 'mouse_scroll', (x, y, dx, dy)))

    def start_listeners(self):
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.mouse_listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll)
        self.keyboard_listener.start()
        self.mouse_listener.start()

    # Keyboard action injection
    def press_key(self, key, duration=0.1):
        self.keyboard_controller.press(key)
        time.sleep(duration)
        self.keyboard_controller.release(key)

    # Mouse action injection
    def move_mouse_horizontal(self, x):
        _, current_y = self.mouse_controller.position
        self.mouse_controller.position = (x, current_y)

    def click_mouse(self, button=mouse.Button.left, duration=0.1):
        self.mouse_controller.press(button)
        time.sleep(duration)
        self.mouse_controller.release(button)

    def combined_action(self, key, button=mouse.Button.left, duration=0.5):
        self.keyboard_controller.press(key)
        self.mouse_controller.press(button)
        time.sleep(duration)
        self.mouse_controller.release(button)
        self.keyboard_controller.release(key)

if __name__ == "__main__":
    capture = InputCapture()
    capture.start_listeners()
    print("Keyboard and mouse listeners started. Capturing events...")
    # Example: Simulate holding 'ctrl' and left mouse button for 1 second
    time.sleep(2)
    capture.combined_action(keyboard.Key.ctrl, mouse.Button.left, duration=1)
    # Example: Move mouse horizontally
    capture.move_mouse_horizontal(500)
    # Print captured events
    time.sleep(2)
    print(capture.events)
