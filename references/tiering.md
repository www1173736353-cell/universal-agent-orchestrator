# Multi-dimensional classification: do not mix levels

## Axis 1: Agent assurance tier (authorization maturity)

| Tier | Meaning | Eligible for |
|---|---|---|
| E0 | Discovered, unverified | No automatic execution |
| E1 | Verified read-only & structured output | Read-only inspection/planning in permitted scope |
| E2 | Verified isolated workspace writes and safe execution | Development/testing inside approved worktree |
| E3 | Proven reliability on complex tasks; enhanced testing/review evidence | High-complexity assigned tasks *within the same OS permission limits* |

A high assurance tier does not confer access to protected branches, production systems or secrets. Access requires a separate operation-level approval.

## Axis 2: Task complexity (cost/risk planning)

`C1`: small change; `C2`: ordinary module; `C3`: cross-module or complex algorithms; `C4`: high-risk security, payment, data migration, or architecture. This is independent of model price and agent trust.

## Axis 3: Role

`planner` / `developer` / `reviewer` / `tester` / `integrator` / `analyst`. Agent may hold multiple verified roles but cannot approve its own work in the same execution context.

## Axis 4: Cost and quality

Use **observed** success/defect metrics and actual billing when supplied; record estimates otherwise. Compare total cost per accepted task, not merely cost per request. A cheaper model may be worse after retries. Route only to models available to the user's real account and adapter.

## Axis 5: Data sensitivity

`public` / `internal` / `restricted`. Each adapter lists allowable data scope and where processing occurs. Never send restricted project context to an unapproved remote provider.

## Default routing idea

`C1` => low-cost eligible E2 developer; `C2` => balanced E2; `C3` => E2/E3 with validated contracts; `C4` => E3 + enforced independent review + required human approval for architectural/security scope changes. All categories retain mandatory gate policies.
