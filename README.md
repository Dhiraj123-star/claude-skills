
# Skills Agent (FastAPI + Docker Edition)

A lightweight Python AI Agent that dynamically loads and executes "Skills" as tools using the Anthropic Messages API. This version is production-ready, featuring a **FastAPI** web layer and **Docker** containerization.

## 🚀 Core Functionality

The agent operates on a **Discovery & Execution** pattern:

1. **Skill Discovery**: On startup, it scans the `skills/` directory for modular logic.
2. **Tool Mapping**: Markdown definitions in `SKILL.md` are converted into JSON schemas for Claude.
3. **Autonomous Loop**: Claude decides which tool to call; the agent executes local Python code and returns the result.
4. **Web API**: FastAPI exposes an `/ask` endpoint for remote interaction.
5. **Containerized**: Fully Dockerized with multi-stage builds and non-root security.

## 📁 Project Structure

```text
.
├── main.py               # FastAPI entry point
├── skills_agent.py       # Core Agent logic (Async)
├── Dockerfile            # Multi-stage, non-root production image
├── docker-compose.yml    # Service orchestration
├── .dockerignore         # Build optimization
├── .env                  # API Keys (Excluded from Docker image)
└── skills/               # Custom capabilities folder
    └── weather_checker/
        ├── SKILL.md      
        └── weather_checker.py

```

## 🛠️ Setup & Usage

### Option A: Local Development

1. **Install Dependencies**: `pip install -r requirements.txt`
2. **Launch**: `uvicorn main:app --reload`

### Option B: Docker (Recommended)

1. **Configure Environment**: Add your `ANTHROPIC_API_KEY` to the `.env` file.
2. **Build and Run**:
```bash
docker-compose up --build -d

```


3. **Check Logs**: `docker-compose logs -f`

## 🧪 Interact via API

Send a POST request to `http://localhost:8000/ask`:

```json
{
  "text": "What is the weather in New Delhi?"
}

```

## 🧩 How to Add a New Skill

1. **Folder**: Create `skills/your_skill/`.
2. **Metadata**: Define name/params in `SKILL.md`.
3. **Logic**: Write your function in `your_skill.py`.
4. **Hot Reload**: If using Docker Compose with volumes, the agent can pick up new skills on container restart.

---

### Why this approach works

* **Production Secure**: Runs as a non-privileged `appuser` inside the container.
* **Optimized**: Multi-stage Docker builds keep the final image size minimal.
* **Modular**: Skills remain decoupled from the core API logic.

---
