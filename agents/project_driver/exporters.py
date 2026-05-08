from core_models import ProjectPlan
from pathlib import Path
import json


EXPORT_DIR = Path('.projecttrack/exports')
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def export_plan_json(plan: ProjectPlan, filename: str = 'latest-plan.json') -> Path:
    path = EXPORT_DIR / filename
    path.write_text(json.dumps(plan.model_dump(), indent=2))
    return path


def export_plan_markdown(plan: ProjectPlan, filename: str = 'latest-plan.md') -> Path:
    lines = []
    lines.append(f'# Project Plan')
    lines.append('')
    lines.append(plan.summary)
    lines.append('')

    lines.append('## Milestones')
    for milestone in plan.milestones:
        lines.append(f'### {milestone.title}')
        lines.append(f'Goal: {milestone.goal}')
        lines.append('')
        if milestone.success_criteria:
            lines.append('Success criteria:')
            for item in milestone.success_criteria:
                lines.append(f'- {item}')
        if milestone.tasks:
            lines.append('Tasks:')
            for task in milestone.tasks:
                lines.append(f'- [{task.status}] {task.title} ({task.priority})')
                if task.description:
                    lines.append(f'  - {task.description}')
                for criterion in task.acceptance_criteria:
                    lines.append(f'  - AC: {criterion}')
        lines.append('')

    lines.append('## Risks')
    for risk in plan.risks:
        lines.append(f'- **{risk.title}** ({risk.impact}): {risk.mitigation}')
    lines.append('')

    lines.append('## Decisions')
    for decision in plan.decisions:
        lines.append(f'### {decision.title}')
        lines.append(f'Context: {decision.context}')
        lines.append(f'Decision: {decision.decision}')
        for consequence in decision.consequences:
            lines.append(f'- {consequence}')
        lines.append('')

    lines.append('## Next Actions')
    for action in plan.next_actions:
        lines.append(f'- {action}')

    path = EXPORT_DIR / filename
    path.write_text('\n'.join(lines))
    return path
