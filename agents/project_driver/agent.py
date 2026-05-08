from openai import OpenAI
import yaml
import os
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
                'content': f'''You are the PROJECTTRACK Project Driver Agent.\n\nProject context:\n{project}'''
            },
            {
                'role': 'user',
                'content': task,
            },
        ],
    )

    return response.output_text


if __name__ == '__main__':
    task = os.environ.get(
        'PROJECT_DRIVER_TASK',
        'Plan the next implementation milestone for PROJECTTRACK.'
    )

    print(run(task))
