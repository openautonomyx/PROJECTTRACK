# PROJECTTRACK

A Python-based project tracking workspace with reusable Project Driver Agent automation.

## Production Deployment

This repository is now wired to the shared LangGraph deployment orchestration agent:

- Pre-production validation
- Docker build validation
- Production hardening checks
- Deployment orchestration
- Post-production validation
- Deployment reporting
- Parallel deployment support
- Time and cost budget enforcement

Deployment flow:

```text
main branch merge
→ deployment agent validation
→ provider deployment
→ live validation
→ deployment report generation
```

Shared deployment agent:

- `AGenNext/code-deploy`

## Where This Agent Deploys

Current deployment mode:

| Field | Value |
|---|---|
| Provider | `webhook` |
| Runtime target | Coolify, Dokploy, Cloud Run trigger, AWS trigger, or any deployment webhook target |
| Deploy trigger | `DEPLOY_WEBHOOK_URL` GitHub secret |
| Production URL | `DEPLOYED_BASE_URL` GitHub secret |
| Compose file | `docker-compose.deploy.yml` |
| Dockerfile | `Dockerfile` |
| Runtime API | `projecttrack.api:app` |
| Health endpoint | `/health` |

To deploy through Coolify:

```text
DEPLOY_WEBHOOK_URL=<coolify deploy webhook>
DEPLOYED_BASE_URL=<public deployed URL>
```

## Required GitHub Secrets

| Secret | Description |
|---|---|
| `DEPLOY_WEBHOOK_URL` | Deployment webhook URL |
| `DEPLOYED_BASE_URL` | Public deployment URL used for validation |

## Runtime

A lightweight FastAPI runtime surface is included for deployment validation.

Run locally:

```bash
uvicorn projecttrack.api:app --host 0.0.0.0 --port 8000
```

Health endpoint:

```text
GET /health
```

## Installation

```bash
git clone https://github.com/openautonomyx/PROJECTTRACK.git
cd PROJECTTRACK
pip install -r requirements.txt
```

## Usage

### Project Driver

```bash
python scripts/run_project.py
```

### API Runtime

```bash
uvicorn projecttrack.api:app --host 0.0.0.0 --port 8000
```

## Production Files

| File | Purpose |
|---|---|
| `Dockerfile` | Production container runtime |
| `docker-compose.deploy.yml` | Production deployment compose |
| `.env.production.example` | Production environment template |
| `.github/workflows/deploy.yml` | Shared deployment-agent workflow |

## Contributing
1. Fork the repo
2. Create a feature branch
3. Submit a pull request

## License
MIT License
