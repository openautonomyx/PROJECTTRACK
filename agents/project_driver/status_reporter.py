import json
from pathlib import Path
from datetime import datetime


BASE = Path('.projecttrack')
PLANS_FILE = BASE / 'plans.json'
APPROVAL_DIR = BASE / 'approvals'
REPORTS_DIR = BASE / 'reports'
REPORTS_DIR.mkdir(parents=True, exist_ok=True)


class StatusReporter:
    def load_plans(self):
        if not PLANS_FILE.exists():
            return []
        return json.loads(PLANS_FILE.read_text())

    def load_approvals(self):
        if not APPROVAL_DIR.exists():
            return []
        return [json.loads(path.read_text()) for path in APPROVAL_DIR.glob('*.json')]

    def generate_snapshot(self):
        plans = self.load_plans()
        approvals = self.load_approvals()

        pending = [a for a in approvals if a.get('status') == 'pending']
        approved = [a for a in approvals if a.get('status') == 'approved']
        rejected = [a for a in approvals if a.get('status') == 'rejected']

        latest_plan = plans[-1]['plan'] if plans else None

        return {
            'generated_at': datetime.utcnow().isoformat(),
            'plan_count': len(plans),
            'approval_count': len(approvals),
            'pending_approval_count': len(pending),
            'approved_count': len(approved),
            'rejected_count': len(rejected),
            'latest_summary': latest_plan.get('summary') if latest_plan else None,
            'latest_next_actions': latest_plan.get('next_actions', []) if latest_plan else [],
        }

    def export_markdown(self):
        snapshot = self.generate_snapshot()
        path = REPORTS_DIR / 'latest-status.md'

        lines = [
            '# PROJECTTRACK Status Snapshot',
            '',
            f"Generated at: {snapshot['generated_at']}",
            '',
            '## Counts',
            f"- Plans: {snapshot['plan_count']}",
            f"- Approvals: {snapshot['approval_count']}",
            f"- Pending approvals: {snapshot['pending_approval_count']}",
            f"- Approved: {snapshot['approved_count']}",
            f"- Rejected: {snapshot['rejected_count']}",
            '',
            '## Latest Summary',
            snapshot['latest_summary'] or 'No plan generated yet.',
            '',
            '## Latest Next Actions',
        ]

        for action in snapshot['latest_next_actions']:
            lines.append(f'- {action}')

        path.write_text('\n'.join(lines))
        return path
