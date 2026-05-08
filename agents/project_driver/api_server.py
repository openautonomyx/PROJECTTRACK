from fastapi import FastAPI
from pydantic import BaseModel

from planning_engine import generate_plan
from publishers import ApprovalRequiredPublisher
from approval_workflow import ApprovalWorkflow


app = FastAPI(title='PROJECTTRACK Project Manager API')
publisher = ApprovalRequiredPublisher()
approvals = ApprovalWorkflow()


class PlanRequest(BaseModel):
    task: str


class RejectRequest(BaseModel):
    reason: str | None = None


@app.get('/health')
def health():
    return {'status': 'ok'}


@app.post('/plan')
def plan(req: PlanRequest):
    project_plan = generate_plan(req.task)
    publish_result = publisher.publish(project_plan)

    return {
        'plan': project_plan.model_dump(),
        'publish': publish_result,
    }


@app.get('/approvals')
def list_approvals():
    return {
        'approvals': approvals.list_drafts(),
    }


@app.post('/approvals/{draft_id}/approve')
def approve_plan(draft_id: str):
    return approvals.approve(draft_id)


@app.post('/approvals/{draft_id}/reject')
def reject_plan(draft_id: str, req: RejectRequest):
    return approvals.reject(draft_id, reason=req.reason)


@app.get('/status')
def status():
    return {
        'status': 'active',
        'mode': 'provider-neutral',
        'core_model': 'ProjectPlan',
        'approval_workflow': 'enabled',
    }
