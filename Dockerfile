# Dockerfile for TallyAI Full-Stack (Backend API + Frontend Dashboard)
FROM node:20-alpine AS frontend-builder
WORKDIR /app/frontend
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ ./
RUN npm run build

FROM python:3.11-slim
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python backend dependencies
COPY backend/app/ ./backend/app/
COPY tally-agent/tally_client.py ./tally-agent/
COPY tally-agent/tally_xml_templates.py ./tally-agent/
COPY tally-agent/tally_parser.py ./tally-agent/

RUN pip install --no-cache-dir \
    fastapi \
    uvicorn \
    sqlalchemy \
    pydantic \
    requests \
    xmltodict \
    python-dotenv \
    apscheduler

# Copy built frontend assets to serve statically
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

EXPOSE 8000

ENV PYTHONPATH=/app/backend:/app/tally-agent

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
