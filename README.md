# experiment-4-embodied-agent
Experiment 4, the embodied agent
# Embodied Agent Framework: Eastshade Experiment

## Project Overview
This repository documents the design and development of an embodied agent framework, with a focus on training agents in gentle, story-driven environments. Our initial experiment centers on the game **Eastshade**, chosen for its emphasis on exploration, beauty, and positive social interaction.

## Vision & Philosophy
- Develop agents that learn through experience, not just language.
- Foster values such as curiosity, empathy, appreciation of nature, and kindness.
- Use curriculum design to align agent behavior with human-centric values.

## Technical Approach
- Modular architecture: input orchestration, environment interface, agent core, curriculum management, logging, and evaluation.
- Multi-modal perception: synchronize screen, audio, keyboard, and mouse inputs for unified agent observations.
- Intrinsic motivation: reward curiosity, exploration, social engagement, and aesthetic appreciation rather than competition or combat.
- Safety and intervention: detect and respond to human input or unexpected game states to maintain data integrity.

## Initial Environment: Eastshade
- Agent will learn to navigate, explore, interact with NPCs, and appreciate the world of Eastshade.
- Success metrics include exploration coverage, novelty seeking, social interaction, task completion, and behavioral diversity.
- Theoretical outcomes: agent develops positive associations with beauty, kindness, and helping others.

## Integration Workflow
- Install Eastshade via Steam and configure for agent interaction.
- Capture and inject inputs using OS-level APIs and libraries (OpenCV, PyAudio, pynput, etc.).
- Synchronize and buffer multi-modal data for agent training.
- Log all actions, states, and events for analysis and curriculum refinement.


## Recent Progress
- Input capture modules for visual, audio, keyboard, and mouse are implemented and tested.
- Input orchestrator synchronizes multi-modal data into unified agent observations.
- PostgreSQL + TimescaleDB integration for high-throughput, time-series data storage.
- Database credentials and configuration now loaded securely from a `.env` file (see template in repo).
- `.gitignore` updated to exclude sensitive files and unnecessary artifacts.
- All code refactored for modularity and security, ready for collaborative development and safe repository sharing.

## Next Steps
- Expand agent-environment interface and begin initial scripted testing.
- Refine curriculum and success metrics as agent begins to learn.
- Develop data retrieval and visualization tools for analysis and training.

---
*This README is a living document and will evolve as the project progresses. For questions or collaboration, please contact the project maintainers.*
