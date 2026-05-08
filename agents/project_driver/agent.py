from openai import OpenAI
import yaml
import os
import json
import urllib.request
from pathlib import Path


base = Path(__file__).resolve().parent
config_path = base / 'projects' / 'projecttrack.yaml'

with open(config_path, 'r') as f:
    project = yaml.safe_load(f)


client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])


def run(task: str):
    response = client.responses.create(
        model=os.environ.get('OPENAI_MODEL', 'gpt-5.1'),
        input=[
            {
                'role': 'system',
                'content': f'''You are the PROJECTTRACK Project Driver Agent.\n\nProject context:\n{project}\n\nBe concise, structured, and actionable.'''
            },
            {
                'role': 'user',
                'content': task,
            },
        ],
    )

    return response.output_text


def post_issue_comment(body: str):
    token = os.environ.get('GITHUB_TOKEN')
    repo = os.environ.get('GITHUB_REPOSITORY')
    issue_number = os.environ.get('GITHUB_ISSUE_NUMBER')

    if not token or not repo or not issue_number:
        return

    url = f'https://api.github.com/repos/{repo}/issues/{issue_number}/comments'
    payload = json.dumps({'body': body}).encode('utf-8')
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            'Authorization': f'Bearer {token}',
            'Accept': 'application/vnd.github+json',
            'X-GitHub-Api-Version': '2022-11-28',
            'Content-Type': 'application/json',
        },
        method='POST',
    )

    with urllib.request.urlopen(req) as res:
        res.read()


if __name__ == '__main__':
    task = os.environ.get(
        'PROJECT_DRIVER_TASK',
        'Plan the next implementation milestone for PROJECTTRACK.'
    )

    output = run(task)
    print(output)

    post_issue_comment(
        f'''## PROJECTTRACK Project Driver Agent\n\n{output}\n\n---\n_Automated by Project Driver._'''
    )
