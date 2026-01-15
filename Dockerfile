# ----- Stage 1: Build Stage -----
FROM  python:3.11-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies into local folder
COPY requirements.txt .
RUN pip install --upgrade pip \ 
    && pip install --user --no-cache-dir -r requirements.txt

# ----- Stage 2: Final Stage -----
FROM python:3.11-slim

# Create a non-root user
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Copy only the necessary files from the builder stage
COPY --from=builder /root/.local /home/appuser/.local
COPY . .

# Ensure the appuser owns the application files
RUN chown -R appuser:appuser /app

# Set environment variables
ENV PATH="/home/appuser/.local/bin:${PATH}"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

USER appuser

EXPOSE 8000

CMD ["uvicorn","main:app","--host","0.0.0.0","--port","8000"]


