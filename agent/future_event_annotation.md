# Future Consideration: Hybrid Event Annotation for Embodied Agent

## Overview
As the embodied agent framework evolves, we will need to interpret raw multi-modal observations into meaningful, symbolic events. This hybrid approach combines agent self-reporting and human annotation to maximize insight and flexibility.

## Motivation
- Enable both agent-centric and human-centric analysis of agent experiences.
- Facilitate debugging, curriculum design, and collaborative research.
- Support richer visualization and understanding of agent behavior.

## Planned Workflow
1. **Raw Data Storage**
   - Continue storing all raw observations (visual, audio, keyboard, mouse) in the database.
2. **Agent Self-Reporting**
   - As the agent develops, add logic for it to signal meaningful events (e.g., outputting labels, flags, or scores per observation).
   - Store these signals in the `symbolic_events` column.
3. **Human Annotation & Event Extraction**
   - Build tools/scripts to let humans annotate or extract symbolic events from raw data (e.g., tagging frames, audio, or input sequences).
   - Store these annotations in the same `symbolic_events` column or a related table.
4. **Visualization & Analysis**
   - Develop scripts/notebooks to visualize and analyze both raw and symbolic data for curriculum refinement and research.

## Implementation Notes
- The `symbolic_events` column (JSONB) is now present in the database schema.
- Annotation tools and event extraction scripts will be developed once the agent is interacting with Eastshade and generating meaningful experiences.
- This document should be revisited and expanded as the agent's capabilities and research goals evolve.

## Next Steps
- Focus on core agent development and integration with Eastshade.
- Revisit this plan once the agent is generating and responding to real game data.
- Collaborate with team members to design annotation and visualization workflows.

---
*This document is a placeholder for future work. For questions or suggestions, please contact the project maintainers.*
