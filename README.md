
# Skills Agent (FastAPI Edition)

A lightweight Python AI Agent that dynamically loads and executes "Skills" as tools using the Anthropic Messages API. Now updated with a **FastAPI** web layer to serve the agent as a REST API.

## 🚀 Core Functionality

The agent operates on a **Discovery & Execution** pattern:

1. **Skill Discovery**: On startup, it scans the `skills/` directory for modular logic.
2. **Tool Mapping**: Markdown definitions in `SKILL.md` are converted into JSON schemas for Claude.
3. **Autonomous Loop**: Claude decides which tool to call; the agent executes local Python code and returns the result.
4. **Web API**: FastAPI exposes an `/ask` endpoint, making the agent accessible via HTTP.

## 📁 Project Structure

```text
.
├── main.py               # FastAPI entry point & routes
├── skills_agent.py       # Core Agent logic (Async enabled)
├── .env                  # API Keys
├── requirements.txt      # Project dependencies
└── skills/               # Custom capabilities folder
    └── weather_checker/
        ├── SKILL.md      
        └── weather_checker.py

```

## 🛠️ Setup & Usage

1. **Install Dependencies**:

```bash
pip install anthropic python-dotenv requests fastapi uvicorn

```

2. **Configure Environment**:
Create a `.env` file with your `ANTHROPIC_API_KEY`.
3. **Launch the API Server**:

```bash
uvicorn main:app --reload

```

4. **Interact via API**:
Send a POST request to `http://localhost:8000/ask`:

```json
{
  "text": "What is the weather in New Delhi?"
}

```

## 🧩 How to Add a New Skill

1. **Folder**: Create `skills/your_skill/`.
2. **Metadata**: Define name/params in `SKILL.md`.
3. **Logic**: Write your function in `your_skill.py`. The agent automatically registers the new tool upon restart.

---

### Why this approach works

* **Web-Ready**: Move from local scripts to a shareable API instantly.
* **Dynamic**: No need to hardcode new tools; just drop them into the directory.
* **Asynchronous**: Handles multiple requests efficiently using `async/await`.

---