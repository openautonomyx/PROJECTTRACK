# PROJECTTRACK Context Checkpoint

Last updated: 2026-05-08

## Project

Repository: `openautonomyx/PROJECTTRACK`

PROJECTTRACK is an AI-native project tracking and delivery orchestration workspace.

Project Driver positioning:

> A composable, self-hostable, cloud-native project tracking platform with AI-driven software delivery orchestration.

## Agent Status

The reusable Project Driver Agent has been installed in PROJECTTRACK.

### Completed

1. GitHub issue automation
   - Workflow triggers on opened issues.
   - Agent calls OpenAI Responses API.
   - Agent posts comments back to GitHub issues.

2. Browser chat
   - FastAPI chat server added.
   - Browser UI added at `/`.
   - Chat endpoint added at `/chat`.
   - Uses `agents/project_driver/projects/projecttrack.yaml` as project context.

3. PR review automation
   - Workflow trigger added for pull requests.
   - Agent has `pr-review` operating mode.
   - PR-aware prompt evaluates architecture fit, implementation clarity, security risk, maintainability, missing tests/docs, and roadmap alignment.
   - Grounding PR still pending.

## Current Checkpoint

Stop point:

```text
PROJECTTRACK
├─ Step 1: GitHub issue automation — done
├─ Step 2: Browser chat — done
└─ Step 3: PR review automation — implemented, grounding PR pending
```

## Next Resume Command

Use this phrase to resume:

```text
resume PROJECTTRACK PR grounding
```

## Next Step

Create a branch from `main`, add a tiny README/doc change, open a PR into `main`, and verify the Project Driver posts a PR review-style comment.

Suggested branch:

```text
pr-review-grounding
```

Suggested change:

```md
## PR Review Grounding

Trigger Project Driver PR review automation.
```

## Files of Interest

```text
.github/workflows/project-driver.yml
agents/project_driver/agent.py
agents/project_driver/chat_server.py
agents/project_driver/projects/projecttrack.yaml
agents/project_driver/requirements.txt
```

## Required Secret

GitHub repository secret:

```text
OPENAI_API_KEY
```

Path:

```text
Settings → Secrets and variables → Actions
```

## Local Browser Chat

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

## Future Backlog

After PR grounding, continue one grounded step at a time:

1. Backlog generation automation
2. Persistent memory/state
3. Multi-agent orchestration
4. Slack/Discord adapters
5. MCP integration
6. Autonomous issue execution mode
