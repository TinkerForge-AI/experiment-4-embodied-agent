import random

class SimpleAgent:
    """
    A simple agent for the embodied agent framework.
    - Action space: keyboard (w, a, s, d, e, space), mouse movement (left/right/up/down), mouse click (left/right), and noop (do nothing).
    - At each step, selects a random combination of actions or chooses to do nothing.
    """
    def __init__(self):
        self.keyboard_keys = ['w', 'a', 's', 'd', 'e', 'space']
        self.mouse_moves = [(10,0), (-10,0), (0,10), (0,-10)]  # dx, dy
        self.mouse_clicks = ['left', 'right']

    def act(self, observation=None):
        actions = []
        # Randomly choose to do nothing
        if random.random() < 0.2:
            actions.append({'type': 'noop'})
            return actions
        # Randomly choose to press a key
        if random.random() < 0.5:
            key = random.choice(self.keyboard_keys)
            actions.append({'type': 'keyboard', 'key': key, 'press': True})
        # Randomly choose to move mouse
        if random.random() < 0.5:
            move = random.choice(self.mouse_moves)
            actions.append({'type': 'mouse', 'move': move})
        # Randomly choose to click mouse
        if random.random() < 0.3:
            click = random.choice(self.mouse_clicks)
            actions.append({'type': 'mouse', 'click': click})
        return actions
