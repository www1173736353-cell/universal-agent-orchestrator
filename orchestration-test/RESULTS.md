# Test result: Codex supervisor / Antigravity employee

Date: 2026-10-28

## Verified

- The fixture repository exists at `employee-repo/` with initial commit `ad86632`.
- The deterministic fixture test passes: 1 test, 0 failures.
- Static policy validation passes.
- Static routing fails closed with `selected_agent: null`.
- The registry marks both `codex` and `antigravity` as disabled and unverified.
- No `aio` executable is installed, so no production scheduler or durable execution backend is available.
- No `antigravity`, `ag`, or `gemini` CLI executable is available.
- No adapter implementation is present in this project.
- The local `127.0.0.1:8317/v1/models` provider endpoint is not running.

## Current conclusion

The requested chain cannot be claimed as working yet:

`Codex supervisor -> verified Antigravity developer adapter -> isolated worktree -> deterministic tests -> independent Codex read-only review -> human-approved integration`

The current Skill package can describe and statically validate this chain, but it cannot execute it in this environment.

This test intentionally does not use Computer Use to operate the Antigravity desktop application. The required integration is an approved machine-callable adapter.

## Required prerequisites

1. A production `aio` backend or an equivalent scheduler that persists task state, leases, checksums, worktree state and review evidence.
2. An Antigravity adapter implementing `probe()` and `run()` through an approved CLI, API, MCP or remote-worker transport.
3. A successful live probe proving version, authentication without token exposure, structured output, workspace boundary, write scope, cancellation and usage reporting.
4. A Codex adapter or host bridge with a separate read-only review invocation. The reviewer must not share the employee's write context.
5. OS-enforced sandbox and network/credential policy for the employee worktree.
6. Human approval for the plan and final integration; automatic push, protected merge and deployment remain disabled.

Only after these prerequisites pass may the registry change to `enabled: true` and `verification: "verified"`. Editing those fields manually would not be evidence of a working integration.

## Real Antigravity CLI rerun

- Skill was reinstalled from the project source; installed and source SHA-256 match.
- Antigravity CLI: `/Users/shanguikui/.local/bin/agy`, version `1.4.9`.
- Read-only probe: `PROBE_OK`; conversation `ab48866a-4a38-4f5e-b8b1-ea8d46d95548`.
- Initial headless coding attempt was blocked because `RunCommand` had no allow-rule; no files changed in that attempt.
- A write-only, two-path retry succeeded. Antigravity changed only `src/calculator.py` and `tests/test_calculator.py`.
- Codex deterministic gate: 2 tests passed and `git diff --check` passed after one formatting repair round.
- Final employee work remains uncommitted for Codex review and human-approved integration.

## Local GUI verification

- Console: `dashboard.py`, loopback URL `http://127.0.0.1:8765`.
- Browser verification showed state `reviewing`, current action `Waiting for Codex read-only review`, Antigravity session `7730d655-5bdf-4cd9-a165-5e792c80feaf`, and measured total usage `82035` tokens.
- Timeline showed dispatch, employee completion, deterministic tests and review readiness.
- Codex review displayed `changes_requested`, with tests passing and the formatting gate failing.
