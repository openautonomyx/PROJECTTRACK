from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from planning_engine import generate_plan
from publishers import ApprovalRequiredPublisher
from approval_workflow import ApprovalWorkflow
from status_reporter import StatusReporter


app = FastAPI(title='PROJECTTRACK Dashboard')
publisher = ApprovalRequiredPublisher()
approvals = ApprovalWorkflow()
reporter = StatusReporter()


class PlanRequest(BaseModel):
    task: str


class RejectRequest(BaseModel):
    reason: str | None = None


@app.get('/', response_class=HTMLResponse)
def dashboard():
    return '''<!doctype html>
<html>
<head>
  <title>PROJECTTRACK</title>
  <style>
    body { margin: 0; font-family: Inter, system-ui, sans-serif; background: #0b1020; color: #eef2ff; }
    .layout { display: grid; grid-template-columns: 250px 1fr; min-height: 100vh; }
    aside { background: #101827; padding: 24px; border-right: 1px solid #22304a; }
    main { padding: 28px; }
    h1 { margin: 0; font-size: 30px; }
    h2 { margin-top: 0; }
    .muted { color: #9aa7bd; }
    .nav { margin-top: 28px; display: grid; gap: 10px; }
    .nav button { text-align: left; background: transparent; color: #cbd5e1; border: 0; padding: 10px 12px; border-radius: 10px; cursor: pointer; }
    .nav button:hover, .nav button.active { background: #1d2a44; color: #fff; }
    .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 22px 0; }
    .card { background: #141d31; border: 1px solid #26324d; border-radius: 18px; padding: 18px; }
    .metric { font-size: 30px; font-weight: 800; margin-top: 8px; }
    textarea, input { width: 100%; box-sizing: border-box; background: #0f172a; color: #fff; border: 1px solid #2c3855; border-radius: 12px; padding: 12px; }
    textarea { min-height: 130px; }
    button.primary { background: #4f8cff; color: white; border: 0; padding: 12px 16px; border-radius: 10px; font-weight: 700; cursor: pointer; margin-top: 10px; }
    pre { white-space: pre-wrap; background: #0f172a; border: 1px solid #26324d; padding: 14px; border-radius: 12px; max-height: 380px; overflow: auto; }
    .section { display: none; }
    .section.active { display: block; }
    .row { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
  </style>
</head>
<body>
<div class="layout">
  <aside>
    <h1>PROJECTTRACK</h1>
    <div class="muted">AI-native project operating runtime</div>
    <div class="nav">
      <button class="active" onclick="show('overview', this)">Overview</button>
      <button onclick="show('plan', this)">Generate Plan</button>
      <button onclick="show('approvals', this); loadApprovals()">Approvals</button>
      <button onclick="show('snapshot', this); loadSnapshot()">Snapshot</button>
      <button onclick="show('chat', this)">Agent Chat</button>
    </div>
  </aside>
  <main>
    <section id="overview" class="section active">
      <h2>Overview</h2>
      <div class="muted">Provider-neutral project management runtime with approval-first execution.</div>
      <div class="grid">
        <div class="card"><div class="muted">Runtime</div><div class="metric">Active</div></div>
        <div class="card"><div class="muted">Core Model</div><div class="metric">Plan</div></div>
        <div class="card"><div class="muted">Approvals</div><div class="metric">Gated</div></div>
        <div class="card"><div class="muted">Adapters</div><div class="metric">Optional</div></div>
      </div>
      <div class="card">
        <h3>Architecture</h3>
        <pre>Planning Engine → ProjectPlan → State Store → Approval Workflow → Optional Provider Adapters</pre>
      </div>
    </section>

    <section id="plan" class="section">
      <h2>Generate Plan</h2>
      <textarea id="planTask" placeholder="Plan the next MVP sprint, define milestones, risks, decisions, and next actions..."></textarea>
      <button class="primary" onclick="generatePlan()">Generate Draft Plan</button>
      <pre id="planOutput"></pre>
    </section>

    <section id="approvals" class="section">
      <h2>Approval Queue</h2>
      <button class="primary" onclick="loadApprovals()">Refresh</button>
      <pre id="approvalOutput"></pre>
    </section>

    <section id="snapshot" class="section">
      <h2>Status Snapshot</h2>
      <button class="primary" onclick="loadSnapshot()">Refresh Snapshot</button>
      <button class="primary" onclick="exportSnapshot()">Export Markdown</button>
      <pre id="snapshotOutput"></pre>
    </section>

    <section id="chat" class="section">
      <h2>Agent Chat</h2>
      <textarea id="chatMessage" placeholder="Ask the project manager agent..."></textarea>
      <button class="primary" onclick="chat()">Send</button>
      <pre id="chatOutput"></pre>
    </section>
  </main>
</div>
<script>
function show(id, btn) {
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.getElementById(id).classList.add('active');
  document.querySelectorAll('.nav button').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
}
async function generatePlan() {
  const task = document.getElementById('planTask').value;
  const res = await fetch('/plan', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({task})});
  document.getElementById('planOutput').textContent = JSON.stringify(await res.json(), null, 2);
}
async function loadApprovals() {
  const res = await fetch('/approvals');
  document.getElementById('approvalOutput').textContent = JSON.stringify(await res.json(), null, 2);
}
async function loadSnapshot() {
  const res = await fetch('/snapshot');
  document.getElementById('snapshotOutput').textContent = JSON.stringify(await res.json(), null, 2);
}
async function exportSnapshot() {
  const res = await fetch('/snapshot/export', {method:'POST'});
  document.getElementById('snapshotOutput').textContent = JSON.stringify(await res.json(), null, 2);
}
async function chat() {
  const task = document.getElementById('chatMessage').value;
  const res = await fetch('/plan', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({task})});
  document.getElementById('chatOutput').textContent = JSON.stringify(await res.json(), null, 2);
}
</script>
</body>
</html>'''


@app.post('/plan')
def plan(req: PlanRequest):
    project_plan = generate_plan(req.task)
    publish_result = publisher.publish(project_plan)
    return {'plan': project_plan.model_dump(), 'publish': publish_result}


@app.get('/approvals')
def list_approvals():
    return {'approvals': approvals.list_drafts()}


@app.post('/approvals/{draft_id}/approve')
def approve_plan(draft_id: str):
    return approvals.approve(draft_id)


@app.post('/approvals/{draft_id}/reject')
def reject_plan(draft_id: str, req: RejectRequest):
    return approvals.reject(draft_id, reason=req.reason)


@app.get('/snapshot')
def snapshot():
    return reporter.generate_snapshot()


@app.post('/snapshot/export')
def export_snapshot():
    path = reporter.export_markdown()
    return {'status': 'exported', 'path': str(path)}


@app.get('/health')
def health():
    return {'status': 'ok'}
