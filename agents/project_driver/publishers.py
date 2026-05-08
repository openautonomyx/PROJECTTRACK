from core_models import ProjectPlan
from exporters import export_plan_json, export_plan_markdown
from approval_workflow import ApprovalWorkflow


class ApprovalRequiredPublisher:
    """
    Provider-neutral publisher.

    Plans become drafts first.
    Human approval is required before adapters publish externally.
    """

    def __init__(self):
        self.workflow = ApprovalWorkflow()

    def publish(self, plan: ProjectPlan):
        draft = self.workflow.create_draft(plan)

        json_path = export_plan_json(plan)
        markdown_path = export_plan_markdown(plan)

        return {
            'status': 'awaiting_approval',
            'draft_id': draft['id'],
            'json_export': str(json_path),
            'markdown_export': str(markdown_path),
        }
