from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from openai import OpenAI
import yaml
import os
from pathlib import Path


base = Path(__file__).resolve().parent
config_path = base / 'projects' / 'projecttrack.yaml'

with open(config_path, 'r') as f:
    project = yaml.safe_load(f)

client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
app = FastAPI(title='PROJECTTRACK Project Driver Chat')


class ChatRequest(BaseModel):
    message: str


@app.get('/', response_class=HTMLResponse)
async def home():
    return '''<!doctype html>
<html>
<head>
  <title>PROJECTTRACK Agent Chat</title>
  <style>
    body { font-family: Inter, system-ui, sans-serif; background: #0b1020; color: #fff; margin: 0; }
    .wrap { max-width: 920px; margin: 40px auto; padding: 24px; }
    h1 { margin: 0 0 8px; font-size: 34px; }
    p { color: #a7b0c0; }
    #chat { background: #141b2d; border: 1px solid #263149; border-radius: 18px; padding: 18px; min-height: 420px; overflow-y: auto; }
    .msg { padding: 12px 14px; border-radius: 12px; margin: 12px 0; line-height: 1.45; }
    .user { background: #24314f; }
    .agent { background: #182338; }
    textarea { width: 100%; min-height: 110px; margin-top: 16px; padding: 14px; border: 0; border-radius: 12px; background: #101827; color: #fff; font-size: 14px; }
    button { margin-top: 12px; padding: 12px 18px; border: 0; border-radius: 10px; background: #4f8cff; color: #fff; font-weight: 700; cursor: pointer; }
  </style>
</head>
<body>
  <div class="wrap">
    <h1>PROJECTTRACK Project Driver</h1>
    <p>Chat with the AI project driver for roadmap, sprint, architecture, and delivery planning.</p>
    <div id="chat"></div>
    <textarea id="message" placeholder="Ask: Plan the next sprint, review architecture, decompose the MVP..."></textarea>
    <button onclick="sendMessage()">Send</button>
  </div>
<script>
async function sendMessage() {
  const input = document.getElementById('message');
  const chat = document.getElementById('chat');
  const message = input.value.trim();
  if (!message) return;
  chat.innerHTML += `<div class="msg user"><b>You</b><br>${message}</div>`;
  input.value = '';
  const res = await fetch('/chat', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({message}) });
  const data = await res.json();
  chat.innerHTML += `<div class="msg agent"><b>Agent</b><br>${data.response.replace(/\n/g, '<br>')}</div>`;
  chat.scrollTop = chat.scrollHeight;
}
</script>
</body>
</html>'''


@app.post('/chat')
async def chat(req: ChatRequest):
    response = client.responses.create(
        model=os.environ.get('OPENAI_MODEL', 'gpt-5.1'),
        input=[
            {
                'role': 'system',
                'content': f'''You are the PROJECTTRACK Project Driver Agent.\n\nProject context:\n{project}\n\nBe concise, structured, and actionable.''',
            },
            {'role': 'user', 'content': req.message},
        ],
    )
    return {'response': response.output_text}
