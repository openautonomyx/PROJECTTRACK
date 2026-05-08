from openai import OpenAI
import os
import yaml
from pathlib import Path


base = Path(__file__).resolve().parent
config_path = base / 'projects' / 'projecttrack.yaml'

with open(config_path, 'r') as f:
    project = yaml.safe_load(f)


client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


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

    return response.output_text
