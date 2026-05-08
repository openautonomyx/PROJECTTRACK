import json
from pathlib import Path
from datetime import datetime
from uuid import uuid4

from core_models import ProjectPlan


APPROVAL_DIR = Path('.projecttrack/approvals')
APPROVAL_DIR.mkdir(parents=True, exist_ok=True)


class ApprovalWorkflow:
    def create_draft(self, plan: ProjectPlan) -> dict:
        draft_id = str(uuid4())
        path = APPROVAL_DIR / f'{draft_id}.json'

        payload = {
            'id': draft_id,
            'status': 'pending',
            'created_at': datetime.utcnow().isoformat(),
            'reviewed_at': None,
            'plan': plan.model_dump(),
        }

        path.write_text(json.dumps(payload, indent=2))
        return payload

    def approve(self, draft_id: str) -> dict:
        path = APPROVAL_DIR / f'{draft_id}.json'
        payload = json.loads(path.read_text())
        payload['status'] = 'approved'
        payload['reviewed_at'] = datetime.utcnow().isoformat()
        path.write_text(json.dumps(payload, indent=2))
        return payload

    def reject(self, draft_id: str, reason: str | None = None) -> dict:
        path = APPROVAL_DIR / f'{draft_id}.json'
        payload = json.loads(path.read_text())
        payload['status'] = 'rejected'
        payload['reviewed_at'] = datetime.utcnow().isoformat()
        payload['rejection_reason'] = reason
        path.write_text(json.dumps(payload, indent=2))
        return payload

    def list_drafts(self) -> list[dict]:
        drafts = []
        for path in APPROVAL_DIR.glob('*.json'):
            drafts.append(json.loads(path.read_text()))
        return drafts
