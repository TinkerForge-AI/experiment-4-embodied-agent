import sys
import os
import time

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from agent.simple_agent import SimpleAgent

def debug_print(step, actions):
    print(f"[DEBUG] Step {step}:")
    for action in actions:
        print(f"  Action: {action}")

def test_simple_agent(num_steps=10):
    agent = SimpleAgent()
    for step in range(num_steps):
        actions = agent.act()
        debug_print(step, actions)
        # Basic checks
        assert isinstance(actions, list), "Actions should be a list"
        for action in actions:
            assert 'type' in action, "Each action should have a 'type' key"
        time.sleep(0.1)  # Simulate step delay

if __name__ == "__main__":
    print("Running SimpleAgent test...")
    test_simple_agent()
    print("Test completed.")
