# Skills Agent (FastAPI + Docker + Nginx + CI/CD Edition)

A lightweight Python AI Agent that dynamically loads and executes "Skills" as tools using the Anthropic Messages API. This version is production-hardened with a **FastAPI** backend, **Nginx** reverse proxy, **Docker** orchestration, and **GitHub Actions** for CI/CD.

## 🚀 Core Functionality

The agent operates on a **Discovery & Execution** pattern:

1. **Skill Discovery**: On startup, it scans the `skills/` directory for modular logic.
2. **Tool Mapping**: Markdown definitions in `SKILL.md` are converted into JSON schemas for Claude.
3. **Autonomous Loop**: Claude decides which tool to call; the agent executes local Python code and returns the result.
4. **Web API**: FastAPI exposes a production-ready `/ask` endpoint.
5. **Reverse Proxy & Rate Limiting**: **Nginx** handles incoming traffic on port 80, providing security and protecting the AI backend from abuse with a **Leaky Bucket** rate limiter.
6. **Containerized**: Fully Dockerized with multi-stage builds and non-root security.
7. **CI/CD**: Automatically builds and pushes images to **Docker Hub** on every push to `main`.

## 📁 Project Structure

```text
.
├── .github/workflows/    # CI/CD Pipeline (Docker Hub Push)
├── nginx/
│   └── default.conf      # Nginx Reverse Proxy & Rate Limit Config
├── main.py               # FastAPI entry point & Proxy Middleware
├── skills_agent.py       # Core Agent logic (AsyncAnthropic enabled)
├── Dockerfile            # Multi-stage, non-root production image
├── docker-compose.yml    # Full stack orchestration (App + Proxy)
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

### Option B: Docker Production (Recommended)

1. **Configure Environment**: Add your `ANTHROPIC_API_KEY` to the `.env` file.
2. **Build and Run**:
```bash
docker-compose up --build -d

```


*The API is now accessible on port **80** (via Nginx).*

## 🛡️ Traffic Management (Rate Limiting)

The system is pre-configured with Nginx rate limiting to prevent API key exhaustion:

* **Rate**: 2 requests per second (`2r/s`).
* **Burst**: 5 requests allowed in a quick surge (`burst=5`).
* **Behavior**: Excessive requests return an **HTTP 429 (Too Many Requests)** status code.

## 🤖 CI/CD Deployment

Automated image publishing via GitHub Actions:

* **Target**: `dhiraj918106/claude-skills:latest`
* **Trigger**: Every push to the `main` branch.

## 🧪 Interact via API

Send a POST request to `http://localhost/ask`:

```json
{
  "text": "What is the weather in New Delhi?"
}

```

*Access API Documentation at `http://localhost/docs`.*

---

### Why this approach works

* **Production Secure**: Uses Nginx as a buffer and runs the Python app as a non-privileged user.
* **Non-Blocking**: Implements `AsyncAnthropic` to ensure high performance under load.
* **Abuse Prevention**: Integrated `limit_req` ensures one user cannot monopolize your AI model credits.
* **Swagger Friendly**: Configured with Proxy Header Middleware to ensure `/docs` load correctly behind Nginx.

---
