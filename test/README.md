# Test Suite Documentation

This folder contains integration and unit tests for the embodied agent framework.

## Tests

- **test_agent_env_interface.py**  
  Verifies multi-modal input capture, orchestrator synchronization, window manager, and agent-environment action dispatch.

- **test_simple_agent.py**  
  Runs the `SimpleAgent` for several steps, prints actions for debugging, and checks output structure. Useful for validating agent action generation and debugging agent logic.

- **test_full_capture.py**  
  Runs a full integration test of the input capture modules (visual, audio, keyboard, mouse) and orchestrator. Ensures all modalities are captured, synchronized, and logged correctly. Useful for validating end-to-end data flow and multi-modal input handling.

---

Add new tests here as the project grows!
