from fastapi import FastAPI
from pydantic import BaseModel

from planning_engine import generate_plan
from publishers import ApprovalRequiredPublisher


app = FastAPI(title='PROJECTTRACK Project Manager API')
publisher = ApprovalRequiredPublisher()


class PlanRequest(BaseModel):
    task: str


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


@app.get('/status')
def status():
    return {
        'status': 'active',
        'mode': 'provider-neutral',
        'core_model': 'ProjectPlan',
    }
