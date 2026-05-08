import json
from pathlib import Path
from datetime import datetime


BASE = Path('.projecttrack')
BASE.mkdir(exist_ok=True)


PLANS_FILE = BASE / 'plans.json'
TASKS_FILE = BASE / 'tasks.json'
RISKS_FILE = BASE / 'risks.json'
DECISIONS_FILE = BASE / 'decisions.json'
STATUS_FILE = BASE / 'status.json'


class StateStore:
    def __init__(self):
        self.ensure_files()

    def ensure_files(self):
        for file in [
            PLANS_FILE,
            TASKS_FILE,
            RISKS_FILE,
            DECISIONS_FILE,
            STATUS_FILE,
        ]:
            if not file.exists():
                file.write_text('[]')

    def save_plan(self, plan: dict):
        existing = json.loads(PLANS_FILE.read_text())

        existing.append({
            'created_at': datetime.utcnow().isoformat(),
            'plan': plan,
        })

        PLANS_FILE.write_text(json.dumps(existing, indent=2))
