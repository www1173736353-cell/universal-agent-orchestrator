# Codex supervisor / Antigravity employee test

This is a safe fixture for validating the control protocol. The intended flow is:

1. Codex approves the task contract and dispatches a verified Antigravity developer adapter.
2. Antigravity changes only `employee-repo/src/calculator.py` in an isolated worktree.
3. Deterministic tests run before review.
4. Codex performs an independent read-only review.
5. Human approval is required before integration or any push/deploy.

Current status: fixture only. No `aio` backend or verified Antigravity adapter is installed in this environment, so no employee task is dispatched.

## Local GUI console

Start the console from this directory:

```bash
python3 dashboard.py
```

Open http://127.0.0.1:8765 and press **Run task**. The page polls `/api/status` and shows Antigravity's provider session, current phase, event timeline, measured token usage, changed paths, deterministic test results and the Codex read-only review result. The server binds to loopback only.
