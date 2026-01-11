
# Skills Agent 

A lightweight Python AI Agent that dynamically loads and executes "Skills" as tools using the Anthropic Messages API. The agent can automatically discover Python functions in a directory and use them to solve user queries.

## 🚀 Core Functionality

The agent operates on a **Discovery & Execution** pattern:

1. **Skill Discovery**: On startup, it scans the `skills/` directory for folders containing a `SKILL.md` (metadata) and a `.py` file (logic).
2. **Tool Mapping**: It converts the markdown definitions into JSON schemas that Claude understands.
3. **Autonomous Loop**: Claude decides which tool to call. The agent executes the local Python code and feeds the result back to Claude to generate a final answer.

## 📁 Project Structure

```text
.
├── skills_agent.py       # Main Agent logic & Chat loop
├── .env                  # API Keys (ANTHROPIC_API_KEY)
└── skills/               # Directory for custom capabilities
    └── weather_checker/
        ├── SKILL.md      # Metadata & Parameter definitions
        └── weather_checker.py  # Python execution logic

```

## 🛠️ Setup & Usage

1. **Install Dependencies**:
```bash
pip install anthropic python-dotenv requests

```


2. **Configure Environment**:
Create a `.env` file and add your key:
```text
ANTHROPIC_API_KEY=your_actual_key_here

```


3. **Run the Agent**:
```python
from skills_agent import SkillsAgent

agent = SkillsAgent()
agent.chat("What's the weather in New Delhi?")

```



## 🧩 How to Add a New Skill

To give the agent a new capability, create a new folder in `skills/`:

1. **Define the Metadata (`SKILL.md`)**:
```yaml
name: weather_checker
description: Retrieves current weather for a given location.
parameters:
  - name: location
    type: string
    description: City name (e.g., London)

```


2. **Write the Logic (`your_skill_name.py`)**:
Create a function that returns a dictionary. The agent will automatically pick the first function it finds in the file.

---

### Why this approach works

* **Decoupled Logic**: You can update your weather API or logic without touching the main AI code.
* **No API Keys for Tools**: By using Open-Meteo in your skill logic, you provide high-value data to the AI for free.
* **Scalable**: Just drop a new folder into `skills/` to teach the agent a new trick.
