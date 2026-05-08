# PROJECTTRACK Project Driver

AI-native provider-neutral project orchestration runtime.

## Features

- provider-neutral planning engine
- structured ProjectPlan generation
- local project state persistence
- approval-first publishing
- browser chat interface
- generic project-manager API
- CLI runtime
- GitHub automation adapter

## Architecture

```text
Planning Engine
        ↓
Structured ProjectPlan
        ↓
State Store
        ↓
Approval-first Publisher
        ↓
Optional Adapters
```

## Setup

Add:

```text
OPENAI_API_KEY
```

## Run Browser Chat

```bash
cd agents/project_driver
pip install -r requirements.txt
export OPENAI_API_KEY=YOUR_KEY
uvicorn chat_server:app --host 0.0.0.0 --port 8080 --reload
```

Open:

```text
http://localhost:8080
```

## Run Project Manager API

```bash
cd agents/project_driver
pip install -r requirements.txt
export OPENAI_API_KEY=YOUR_KEY
uvicorn api_server:app --host 0.0.0.0 --port 8090 --reload
```

API base:

```text
http://localhost:8090
```

## Run CLI

```bash
cd agents/project_driver
export OPENAI_API_KEY=YOUR_KEY
python cli.py "Plan the next MVP sprint"
```

### JSON output

```bash
python cli.py "Plan the next MVP sprint" --json
```

### Publish artifacts

```bash
python cli.py "Plan the next MVP sprint" --publish
```

## API Endpoints

### Health

```text
GET /health
```

### Generate Project Plan

```text
POST /plan
```

### Runtime Status

```text
GET /status
```
