
# 🧑‍💻 experiment-4-embodied-agent
*Experiment 4: The Embodied Agent Framework*

## 🌱 Project Overview
This repository documents the design and development of an embodied agent framework, with a focus on training agents in gentle, story-driven environments. Our initial experiment centers on the game **Eastshade**, chosen for its emphasis on exploration, beauty, and positive social interaction.

## 💡 Vision & Philosophy
- Develop agents that learn through experience, not just language.
- Foster values such as curiosity, empathy, appreciation of nature, and kindness.
- Use curriculum design to align agent behavior with human-centric values.

## 🛠️ Technical Approach
- **Modular architecture:** Input orchestration, environment interface, agent core, curriculum management, logging, and evaluation.
- **Multi-modal perception:** Synchronize screen, audio, keyboard, and mouse inputs for unified agent observations.
- **Intrinsic motivation:** Reward curiosity, exploration, social engagement, and aesthetic appreciation rather than competition or combat.
- **Safety and intervention:** Detect and respond to human input or unexpected game states to maintain data integrity.

## 🌍 Initial Environment: Eastshade
- Agent will learn to navigate, explore, interact with NPCs, and appreciate the world of Eastshade.
- Success metrics include exploration coverage, novelty seeking, social interaction, task completion, and behavioral diversity.
- Theoretical outcomes: agent develops positive associations with beauty, kindness, and helping others.

---



## 🪟 Window Manager: Automatic Game Window Detection


By default, the agent-environment interface uses a window manager to interact with the game window. For Eastshade, the window manager can automatically detect the correct window by searching for its title (e.g., "Eastshade").

**Automatic detection:**
- The system scans all open windows and matches the title to "Eastshade".
- This avoids manual configuration and ensures reproducibility for training runs.

**Manual override:**
- If automatic detection fails, you can manually specify the window ID in your configuration or test script.

**Example usage:**
```python
window_manager = RealWindowManager(target_name="Eastshade")
window_id = window_manager.find_window_by_title("Eastshade")
if window_id:
    window_manager.target_id = window_id
else:
    print("Eastshade window not found. Please start the game or set the window ID manually.")
```


Document this step for anyone running training or integration tests to ensure the agent interacts with the correct game window.

---

## 🚀 Getting Started: Environment Setup


### 1. Install System Dependencies

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3 python3-pip postgresql postgresql-contrib libportaudio2 portaudio19-dev
```


### 2. Install TimescaleDB (for time-series data)
```bash
sudo apt-get install timescaledb-postgresql-14
sudo systemctl restart postgresql
```
*(Replace `14` with your PostgreSQL version if needed)*


### 3. Create Database and User
```bash
sudo -u postgres psql
CREATE DATABASE embodied_agent;
CREATE USER [desired_agent_user] WITH PASSWORD '[desired_agent_password]';
GRANT ALL PRIVILEGES ON DATABASE embodied_agent TO [desired_agent_user];
CREATE EXTENSION IF NOT EXISTS timescaledb;
\q
```


### 4. Apply Database Schema
```bash
psql -U agent -d embodied_agent -h localhost -f schema.sql
```


### 5. Install Python Dependencies
```bash
pip install -r requirements.txt
```


### 6. (Optional) Install DBeaver for GUI Database Management
```bash
sudo apt-get install dbeaver-ce
```
Or download from [dbeaver.io](https://dbeaver.io/download/).

---


---

## 🧪 Running Tests

To run all unit and integration tests:
```bash
python test/test.py
```
This will execute all tests in `test/unit/` and `test/e2e/` with detailed debugging output.

---


---

## 🛟 Troubleshooting

- **TimescaleDB errors:** Ensure TimescaleDB is installed and enabled in your database.
- **PortAudio errors:** Install `libportaudio2` and `portaudio19-dev`.
- **Import errors:** Make sure you run scripts from the project root or use the provided `test.py` runner.

---


---


## 🚧 Project Status & What’s Missing

This project is a work in progress! Here’s what you can (and can’t) expect right now:

### ✅ What’s Working
- Modular codebase for agent, input, and environment interface
- Basic agent can launch, observe, and interact with Eastshade (screen, audio, keyboard, mouse)
- Logging, window management, and test harnesses
- Example curriculum and success metrics

### ❌ Not Yet Implemented / Incomplete
- Full curriculum management and scenario switching
- Advanced agent learning algorithms (currently rule-based or random policies)
- Robust evaluation, visualization, and analysis tools
- Automated Docker setup and deployment
- Community-contributed modules and documentation

We’re sharing this early so others can experiment, replicate, and help build out the vision! If you run into issues or want to add features, please open an issue or pull request.

---

## 🔭 Next Steps

- Develop and test new agent logic and curriculum scenarios.
- Expand logging, visualization, and evaluation tools.
- Consider Docker for easier reproducibility in future versions.

---


---

## 🧑‍🔬 How to Experiment & Contribute

Ready to try your own ideas or help expand the project? Here’s how you can get started:

### 🏃‍♂️ Quickstart: Run the Agent
1. Follow the setup instructions above to install dependencies and set up the database.
2. Launch the agent and environment interface:
   ```bash
   python agent/simple_agent.py
   ```
3. Run tests to verify your setup:
   ```bash
   python test/test.py
   ```

### 🧩 Expand or Build Your Own Modules
- Add new input modalities, agent logic, or curriculum scenarios by editing or creating modules in the `agent/`, `input/`, `audio/`, `visual/`, or `test/` directories.
- Use the modular architecture to plug in your own experiments or evaluation tools.

### 🤝 Contributing
We welcome issues, feature requests, and pull requests! Please:
- Fork the repo and create a branch for your changes.
- Add or update documentation as needed.
- Run all tests before submitting a pull request.

### 💬 Community & Support
- Open a discussion or issue for questions, ideas, or troubleshooting.
- Share your results and feedback to help us improve the framework!

---

## 🌐 Project Links

- [GitHub Repository](https://github.com/dchisholm125/experiment-4-embodied-agent)

---

Thanks for checking out the project! We can’t wait to see what you build. 🚀