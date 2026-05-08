from core_models import ProjectPlan
from exporters import export_plan_json, export_plan_markdown


class ApprovalRequiredPublisher:
    """
    Provider-neutral publisher.

    This intentionally does NOT write directly into GitHub/Jira/etc.
    until a human approves the generated plan.
    """

    def publish(self, plan: ProjectPlan):
        json_path = export_plan_json(plan)
        markdown_path = export_plan_markdown(plan)

        return {
            'status': 'awaiting_approval',
            'json_export': str(json_path),
            'markdown_export': str(markdown_path),
        }
