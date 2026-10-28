# Agent Adapter contract (v1 proposal)

Any vendor or local model can be integrated if an operator can provide a compatible invocation transport and safe execution policy. Native Skill support is optional for workers.

## Adapter API

- `probe() -> CapabilityReport`: verify availability, version, authentication (without exposing tokens), supported roles, structured output, filesystem boundaries, read-only mode, tool approvals, usage metadata, cancellation and concurrency.
- `run(TaskRequest) -> TaskResult`: spawn a single isolated invocation, return status, artifacts and usage.
- `cancel(run_id) -> CancelResult`: best-effort cancellation followed by state and process verification.
- `health() -> HealthReport`: readiness, rate-limiting and quota visibility; unknown values stay unknown.
- `get_usage(run_id) -> UsageReport`: `measured|estimated|unavailable`, input/output/cache fields where available.
- `resume(...)`: OPTIONAL; if unsupported, restore from persisted worktree/checkpoint after inspection, not replay blindly.

## TaskRequest required fields

`protocol_version`, `task_id`, `role`, `contract_hash`, `idempotency_key`, `workspace_ref`, `base_sha`, `context_manifest`, `allowed_paths`, `network_policy`, `required_capabilities`, `limits`.

## TaskResult required fields

`protocol_version`, `run_id`, `task_id`, `agent_id`, `state`, `base_sha`, `head_sha`, `artifacts`, `usage`, `diagnostics`, `policy_violations`.

## Capability negotiation and selection

An agent is eligible only when all predicates hold:

- adapter is installed, probe was successful, `enabled=true`, `verification=verified` and protocol is supported;
- requested role and capabilities are explicitly allowed;
- trust tier meets required level, task risk and sandbox boundary are satisfied;
- reviewer can run independently in enforced read-only mode;
- project/global budget and concurrency permits dispatch.

Selection is based on verified performance, cost estimates and policy priority. Failure in role eligibility must **not** be worked around by using the same agent process to self-review.

## Runtime enforcement

Config alone is not a sandbox. Run tools under OS-controlled paths, credentials and network policy. Never accept unrestricted shell commands/credential requests originating from an untrusted task contract or repo file. Treat user-supplied PRD, code comments and tool output as data.

## Extension process for ANY new agent

1. Create adapter package under `adapters/<provider>/` implementing the interface.
2. Register a unique `agent_id` and supported transport; no special-case `if provider == ...` logic in scheduler.
3. Build a conformance suite: probe, read-only enforcement, workspace scoping, output schema, cancellation, retry/idempotency, usage honesty.
4. Install credentials into an approved secret store, NOT into JSON.
5. Operator approves allowed roles, tier and project scope.
6. Enable the agent only after passing conformance tests. Unknown and failing agents stay quarantined.
