# Initial Thoughts: Embodied Agent Framework

## Project Vision
- Develop a framework for training embodied agents to navigate real-world scenarios using experience from simulated environments.
- Curriculum design is crucial; the agent's generalization ability depends on the diversity and realism of training scenarios.
- Input orchestration: Route all sensory inputs (audio, video, keyboard, mouse) to the agent in a synchronized, temporal fashion for immediate processing.
- Consider future concepts like long-term/short-term memory and conscious/subconscious thought.

## Technical Considerations
- High resource usage (CPU/GPU/RAM) when running complex games (e.g., Skyrim) and ML training simultaneously; expect performance trade-offs.
- Start with simpler environments before scaling up to AAA games.
- Monitor system performance and synchronize all input streams.
- Use buffers and timestamps to handle minor lag, but avoid significant delays.
- Hardware upgrades (more RAM, better GPU) or cloud resources may be needed for scaling.

## Intervention & Data Integrity

## Next Steps
 Human intervention (e.g., opening game menus) during training can confuse the agent and lead to undesirable behaviors.
 Always pause or stop training before intervening in the environment.
 Log and exclude data from interrupted sessions to maintain clean training data.
 Detect screen changes (such as game menus, window focus loss, or the game window closing) and immediately shut down training and the agent. This prevents the agent from learning from unintended states and keeps training data clean. Log these events for later analysis.
- Draft a modular architecture and list required components.
- Prototype input orchestration and agent-environment interaction.
- Consider sample code for system monitoring and input synchronization.

---

## Language Learning Integration (Future Consideration)

- The framework should support optional modules for language-based learning, including:
  - Traditional LLM training (text corpus ingestion, supervised/unsupervised learning).
  - Interactive language experiences (chatting with an LLM, in-game dialogue, multi-modal communication).
- The agent’s openness and adaptability to language learning should be measured through defined evaluation metrics (e.g., task performance, behavioral change, retention).
- The system must support safe experimentation:
  - Ability to snapshot and restore agent weights/states before and after language learning interventions.
  - Logging and analysis tools to compare agent performance and traits pre- and post-language exposure.
- Research teams should carefully monitor for adverse effects (e.g., reduced generalization, confusion, behavioral drift) and be able to revert to previous agent states if needed.

*These considerations ensure that language learning can be introduced thoughtfully, with robust measurement and recovery mechanisms to protect agent development and research integrity.*

1. Requirements & Architecture
Define core requirements (inputs, outputs, supported environments, agent API).
Draft a modular architecture diagram (input modules, agent core, environment interface, logging, etc.).

2. Input Orchestration
Implement modules to capture and synchronize audio, video, keyboard, and mouse inputs.
Ensure inputs are timestamped and routed only to the agent.

3. Environment Integration
Choose initial simulation/game environments (start simple, e.g., 2D games or custom sandbox).
Develop wrappers to interface with these environments and manage window focus.

4. Agent Core
Define agent API (observation, action, reward, memory).
Implement a basic agent loop for real-time training and feedback.

5. Intervention & Data Integrity
Add detection for screen changes, window focus loss, and game closure.
Implement immediate shutdown and logging for interventions.

6. System Monitoring
Add resource usage monitoring (CPU/GPU/RAM).
Log performance metrics and lag events.

7. Curriculum & Training
Design curriculum management (scenario creation, replay, evaluation).
Prototype training loop and data logging.

8. Evaluation & Extensibility
Develop evaluation metrics for agent performance and generalization.
Plan for future features (memory systems, multi-agent, new input types).

---
*Document created July 22, 2025*
