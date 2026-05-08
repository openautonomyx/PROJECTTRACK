# PROJECTTRACK Project Driver

AI-native provider-neutral project orchestration runtime.

## Features

- provider-neutral planning engine
- structured ProjectPlan generation
- local project state persistence
- approval-first publishing
- dashboard UI
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

## Run Dashboard

```bash
cd agents/project_driver
pip install -r requirements.txt
export OPENAI_API_KEY=YOUR_KEY
uvicorn dashboard_server:app --host 0.0.0.0 --port 8081 --reload
```

Open:

```text
http://localhost:8081
```

## Dashboard Features

- Overview dashboard
- Generate plans
- Approval queue
- Project snapshots
- Agent chat
- Runtime visibility

## Run Browser Chat

```bash
uvicorn chat_server:app --host 0.0.0.0 --port 8080 --reload
```

## Run API

```bash
uvicorn api_server:app --host 0.0.0.0 --port 8090 --reload
```

## Run CLI

```bash
python cli.py "Plan the next MVP sprint"
```
