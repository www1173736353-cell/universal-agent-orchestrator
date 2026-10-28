#!/usr/bin/env python3
"""Local control console for the Codex/Antigravity test fixture."""
from __future__ import annotations
import json, os, subprocess, threading, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
REPO = ROOT / "employee-repo"
AGY = Path("/Users/shanguikui/.local/bin/agy")
TASK_ID = "antigravity-calculator-001"
state_lock = threading.Lock()
state = {
    "task_id": TASK_ID, "state": "idle", "current_phase": "waiting",
    "current_action": "Start the demo to dispatch Antigravity",
    "employee": "antigravity", "reviewer": "codex", "events": [],
    "changed_paths": [], "usage": {}, "usage_quality": "unavailable",
    "review": None, "blocker": None, "started_at": None, "updated_at": None,
}

def event(kind, message, **extra):
    with state_lock:
        item = {"at": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "kind": kind, "message": message, **extra}
        state["events"].append(item)
        state["events"] = state["events"][-80:]
        state["updated_at"] = item["at"]

def set_state(**kwargs):
    with state_lock:
        state.update(kwargs)
        state["updated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")

def snapshot():
    with state_lock:
        return json.loads(json.dumps(state))

def run_demo():
    set_state(state="dispatched", current_phase="dispatch", current_action="Starting Antigravity CLI", started_at=time.strftime("%Y-%m-%dT%H:%M:%S%z"), blocker=None, review=None, events=[])
    event("dispatch", "Antigravity CLI process started", adapter=str(AGY))
    prompt = ("Edit only src/calculator.py and tests/test_calculator.py. "
              "Implement multiply(a, b) and add focused tests. Do not run commands, "
              "do not commit, do not access network, and do not modify other files. "
              "Reply with the changed paths.")
    try:
        proc = subprocess.run([str(AGY), f"--print={prompt}", "--output-format", "json",
                               "--mode", "accept-edits", "--sandbox", "--add-dir", str(REPO)],
                              cwd=REPO, text=True, capture_output=True, timeout=180)
        raw = proc.stdout.strip()
        result = json.loads(raw) if raw.startswith("{") else {"response": raw}
        usage = result.get("usage") or {}
        set_state(state="testing", current_phase="testing", current_action="Running deterministic tests",
                  usage=usage, usage_quality="measured" if usage else "unavailable")
        event("employee_complete", "Antigravity returned", conversation_id=result.get("conversation_id"), status=result.get("status"), usage=usage)
        changed = subprocess.run(["git", "diff", "--name-only"], cwd=REPO, text=True, capture_output=True, check=True).stdout.splitlines()
        set_state(changed_paths=changed)
        test = subprocess.run(["python3", "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=REPO, text=True, capture_output=True)
        check = subprocess.run(["git", "diff", "--check"], cwd=REPO, text=True, capture_output=True)
        event("tests", "Deterministic test gate finished", passed=test.returncode == 0, output=(test.stdout + test.stderr)[-3000:])
        set_state(state="reviewing", current_phase="reviewing", current_action="Waiting for Codex read-only review")
        review = {"reviewer": "codex", "mode": "read_only", "status": "passed" if test.returncode == 0 and check.returncode == 0 else "changes_requested", "test_passed": test.returncode == 0, "diff_check_passed": check.returncode == 0, "changed_paths": changed, "findings": [] if check.returncode == 0 else ["git diff --check reported a formatting issue; repair before integration"]}
        set_state(review=review)
        event("review_ready", "Codex can review the isolated diff", review=review)
    except Exception as exc:
        set_state(state="blocked", current_phase="blocked", current_action="Execution stopped", blocker=str(exc))
        event("blocker", str(exc))

HTML = '''<!doctype html><meta charset="utf-8"><title>Agent Orchestrator Console</title>
<style>body{font:14px system-ui;margin:0;background:#10141c;color:#e8edf5}main{max-width:1100px;margin:30px auto;padding:0 20px}h1{font-size:28px}.grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}.card{background:#1a2130;border:1px solid #2d384c;border-radius:10px;padding:14px}.wide{grid-column:span 2}.muted{color:#94a3b8}.pill{display:inline-block;background:#244a3c;color:#9ff0bf;border-radius:999px;padding:4px 10px}.danger{color:#ff9a9a}button{background:#6ee7b7;border:0;border-radius:7px;padding:9px 15px;font-weight:700;cursor:pointer}pre{white-space:pre-wrap;max-height:260px;overflow:auto;background:#0b0f16;padding:10px;border-radius:7px}table{width:100%;border-collapse:collapse}td,th{padding:7px;border-bottom:1px solid #2d384c;text-align:left}.bar{height:8px;background:#263244;border-radius:10px}.fill{height:8px;background:#6ee7b7;border-radius:10px;width:100%}</style>
<main><h1>Universal Agent Orchestrator</h1><p class="muted">Local-only Codex supervisor · Antigravity employee · Codex read-only review</p><button onclick="run()">Run task</button> <span id="stamp" class="muted"></span><div class="grid" style="margin-top:18px"><div class="card"><div class="muted">状态</div><h2 id="state">idle</h2><div id="phase">waiting</div></div><div class="card"><div class="muted">当前动作</div><div id="action">—</div></div><div class="card"><div class="muted">员工</div><h3>antigravity</h3><div id="session" class="muted">session pending</div></div><div class="card"><div class="muted">Token</div><h3 id="tokens">unavailable</h3><div id="quality" class="muted">quality: unavailable</div></div><div class="card wide"><h3>进度时间线</h3><div id="events"></div></div><div class="card wide"><h3>Codex 审核</h3><div id="review">pending</div><pre id="blocker"></pre></div><div class="card wide"><h3>Changed paths</h3><pre id="paths">—</pre></div></div></main>
<script>let busy=false;async function run(){if(busy)return;busy=true;await fetch('/api/run',{method:'POST'});busy=false}function esc(s){return String(s??'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}async function refresh(){let s=await (await fetch('/api/status')).json();document.querySelector('#state').textContent=s.state;document.querySelector('#phase').textContent=s.current_phase;document.querySelector('#action').textContent=s.current_action;document.querySelector('#stamp').textContent='updated '+(s.updated_at||'—');let u=s.usage||{};document.querySelector('#tokens').textContent=u.total_tokens??'unavailable';document.querySelector('#quality').textContent='quality: '+s.usage_quality;document.querySelector('#session').textContent=(s.events.find(e=>e.conversation_id)?.conversation_id)||'session pending';document.querySelector('#events').innerHTML=s.events.slice(-12).reverse().map(e=>`<p><span class="muted">${esc(e.at)}</span> <b>${esc(e.kind)}</b> ${esc(e.message)}</p>`).join('');document.querySelector('#review').innerHTML=esc(JSON.stringify(s.review,null,2));document.querySelector('#blocker').textContent=s.blocker||'';document.querySelector('#paths').textContent=(s.changed_paths||[]).join('\\n')||'—'}setInterval(refresh,1000);refresh();</script>'''

class Handler(BaseHTTPRequestHandler):
    def send_json(self, obj, code=200):
        data=json.dumps(obj, ensure_ascii=False).encode(); self.send_response(code); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_GET(self):
        if urlparse(self.path).path == "/api/status": self.send_json(snapshot()); return
        data=HTML.encode(); self.send_response(200); self.send_header("Content-Type","text/html; charset=utf-8"); self.send_header("Content-Length",str(len(data))); self.end_headers(); self.wfile.write(data)
    def do_POST(self):
        if self.path == "/api/run":
            threading.Thread(target=run_demo, daemon=True).start(); self.send_json({"started": True}); return
        self.send_json({"error":"not found"},404)
    def log_message(self, *_): pass

if __name__ == "__main__":
    server=ThreadingHTTPServer(("127.0.0.1",8765),Handler)
    print("GUI: http://127.0.0.1:8765", flush=True)
    server.serve_forever()
