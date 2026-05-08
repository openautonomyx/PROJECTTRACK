from openai import OpenAI
import os
import yaml
import json
from pathlib import Path

from core_models import ProjectPlan
from state_store import StateStore


base = Path(__file__).resolve().parent
config_path = base / 'projects' / 'projecttrack.yaml'

with open(config_path, 'r') as f:
    project = yaml.safe_load(f)


client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
store = StateStore()


SYSTEM_PROMPT = f'''
You are a provider-neutral Project Manager Agent.

Project:
{project}

Your responsibilities:
- create milestones
- define tasks
- identify risks
- capture architectural decisions
- propose next actions
- maintain execution momentum

You are NOT tied to GitHub, GitLab, Jira, Linear, or any specific provider.

You operate on generic project-management primitives.

Always return valid structured JSON matching this schema:

{{
  "summary": "string",
  "milestones": [],
  "risks": [],
  "decisions": [],
  "next_actions": []
}}
'''


def generate_plan(task: str):
    response = client.responses.create(
        model=os.environ.get('OPENAI_MODEL', 'gpt-5.1'),
        input=[
            {
                'role': 'system',
                'content': SYSTEM_PROMPT,
            },
            {
                'role': 'user',
                'content': task,
            },
        ],
    )

    raw = response.output_text

    try:
        parsed = json.loads(raw)
        plan = ProjectPlan(**parsed)

        store.save_plan(plan.model_dump())

        return plan

    except Exception:
        fallback = ProjectPlan(
            summary=raw,
            milestones=[],
            risks=[],
            decisions=[],
            next_actions=[],
        )

        store.save_plan(fallback.model_dump())

        return fallback
