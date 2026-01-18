
# Skills Agent (FastAPI + Docker + Nginx + CI/CD Edition)

A lightweight Python AI Agent that dynamically loads and executes "Skills" as tools using the Anthropic Messages API. This version is production-hardened with a **FastAPI** backend, **Nginx** reverse proxy, **Docker** orchestration, and **GitHub Actions** for CI/CD.

## 🚀 Core Functionality

The agent operates on a **Discovery & Execution** pattern:

1. **Skill Discovery**: On startup, it scans the `skills/` directory for modular logic.
2. **Tool Mapping**: Markdown definitions in `SKILL.md` are converted into JSON schemas for Claude.
3. **Autonomous Loop**: Claude decides which tool to call; the agent executes local Python code and returns the result.
4. **Web API**: FastAPI exposes a production-ready `/ask` endpoint.
5. **Reverse Proxy & SSL**: **Nginx** handles incoming traffic on port 80 (Redirect) and 443 (SSL), securing the AI backend.
6. **Rate Limiting**: Integrated **Leaky Bucket** limiter to prevent API abuse.
7. **CI/CD**: Automatically builds and pushes images to **Docker Hub** on every push to `main`.

## 📁 Project Structure

```text
.
├── .github/workflows/    # CI/CD Pipeline (Docker Hub Push)
├── nginx/
│   ├── default.conf      # Nginx SSL & Rate Limit Config
│   └── certs/            # [Untracked] SSL .crt and .key files
├── main.py               # FastAPI entry point & Proxy Middleware
├── skills_agent.py       # Core Agent logic (AsyncAnthropic enabled)
├── Dockerfile            # Multi-stage, non-root production image
├── docker-compose.yml    # Full stack orchestration (App + Proxy)
└── skills/               # Custom capabilities folder

```

## 🛠️ Setup & Usage

### 🔒 SSL Certificate Generation

Before running the stack, generate your self-signed certificates locally (these are ignored by Git for security):

```bash
mkdir -p nginx/certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/certs/nginx.key -out nginx/certs/nginx.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

```

### 🐳 Docker Production (Recommended)

1. **Configure Environment**: Add your `ANTHROPIC_API_KEY` to the `.env` file.
2. **Build and Run**:

```bash
docker-compose up --build -d

```

*The API is now accessible via **HTTPS** on port **443**.*

## 🛡️ Security & Traffic Management

* **HTTPS Enforcement**: All HTTP traffic on port 80 is automatically redirected to port 443.
* **Rate Limiting**: 2 requests per second (`2r/s`) with a `burst=5` queue.
* **Git Security**: SSL certificates and keys are untracked and managed locally to prevent credential leaks.

## 🧪 Interact via API

Because the certificate is self-signed, use the `-k` (insecure) flag:

```bash
curl -k -X POST https://localhost/ask \
     -H "Content-Type: application/json" \
     -d '{"text": "What is the weather in New Delhi?"}'

```

---

### Why this approach works

* **End-to-End Encryption**: SSL ensures data between the client and proxy is encrypted.
* **Secret Management**: By untracking `nginx/certs/`, we ensure sensitive keys never touch the remote repository.
* **Non-Blocking**: Implements `AsyncAnthropic` to ensure high performance under load.

---
