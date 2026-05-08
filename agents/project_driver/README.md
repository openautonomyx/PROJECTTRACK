# PROJECTTRACK Project Driver

AI-native project orchestration agent for PROJECTTRACK.

## Features

- GitHub issue automation
- roadmap planning
- sprint planning
- implementation decomposition
- architecture guidance
- browser chat interface

## Setup

Add:

```text
OPENAI_API_KEY
```

to:

```text
GitHub → Settings → Secrets and variables → Actions
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

## Example prompts

- Plan the next sprint
- Review the architecture
- Break the MVP into milestones
- Recommend GitHub issues
- Design the governance model
- Review open-core boundaries
