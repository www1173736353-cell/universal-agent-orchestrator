---
name: universal-agent-orchestrator
description: Orchestrate software development with interchangeable AI agents, capability-based routing, isolated Git worktrees, independent review, budget gates, and human approval. Use for planning, dispatching, reviewing, resuming, or auditing multi-agent development tasks across any provider.
---

# Universal Agent Orchestrator

This is a provider-neutral **control skill**. The current host may be Codex, Claude Code, or another Agent Skills-compatible environment. **Never assume** the host is also the developer or reviewer. Agent product names are labels, not roles or routing requirements.

## Start safely

1. Locate the repository, authoritative requirements and user-approved plan. Do not start editing without a plan approval or the explicit user-approved scope.
2. Read `references/architecture.md` and `references/adapter-contract.md` only when needed. Read `references/tiering.md` before choosing agents.
3. Check `config/agent-registry.example.json` and `config/policy.example.json` as templates only. These examples are **not** real agent connections or grants of permissions.
4. If the production `aio` CLI is available, use `aio doctor --json` before dispatch. Otherwise report the missing backend; do not invent success or silently simulate production work. This package contains only a router/probe prototype, not the completed scheduler.
5. Run `python3 scripts/doctor.py --registry <registry.json> --policy <policy.json>` to validate a registry. The tool does not contact providers.
6. For routing dry runs, use `python3 scripts/route.py --registry <registry.json> --task <task.json>`. This chooses a candidate but **does not execute** any Agent.

## When the requested chain cannot run

Return the blocker immediately when any required prerequisite is missing or unverified. Do not continue with a simulated dispatch, do not present a dry run as execution, and do not claim that a review or integration happened.

The response must include:

1. **Blocker**: the exact missing or failed capability, such as `aio` unavailable, adapter probe failed, no eligible agent, missing isolated worktree, or review gate unavailable.
2. **Evidence**: the command, probe result, registry decision, error, or SHA that proves the blocker. Mark each item as `measured`, `estimated`, or `unavailable` where applicable.
3. **Impact**: the first control-protocol step that cannot be completed and the work that was not performed.
4. **Resolution**: the concrete setup or approval required, including the adapter/transport, permission boundary, configuration change, or human action needed.
5. **Resume condition**: the exact verification to run before retrying. Do not retry an uncertain task blindly; recover and verify persisted state first.

Use an explicit status such as `blocked`, `partial`, or `dry_run_only`. A successful static validation only proves configuration syntax and policy checks; it does not prove provider availability, execution, sandboxing, review independence, or integration.

## Control protocol

- Parse requirements into versioned, task-specific contracts: goal, dependencies, interface versions, allowlisted file scope, quality gates and acceptance criteria.
- Keep `role` independent of `provider` and of `trust_tier`. Roles include `planner`, `developer`, `reviewer`, `tester`, `integrator`, and `analyst`.
- Select agents via **capability probe + execution eligibility + privilege tier + task risk + resource budget**, not via a hardcoded vendor switch.
- A new provider enters through an `AgentAdapter` implementing the common protocol; see `references/adapter-contract.md`. Unknown agents remain ineligible until probed and authorized.
- Where possible, run at most two development tasks concurrently, each in its own Git Worktree. Limit is configured, not presumed.
- Run deterministic checks before model-based review. The reviewer must be a separate read-only invocation and must not approve its own generated changes.
- Route review findings to a write-capable developer in the matching isolated Worktree. At most three repair rounds; do not conflate repair retries with transient network retries.
- Permit local task commits and integration branch merges only when approved by the project policy. Never auto-merge the protected branch, push remote, or deploy.
- Treat Ponytail/minimal-implementation guidance as **optional provider policy**, not a dependency or permission elevation. Never compromise mandatory security or acceptance tests.
- Track usage as `measured`, `estimated`, or `unavailable`. Enforce project-level caps to the extent observable; pause before additional calls at a hard limit. Never claim perfect prediction of in-flight usage.
- Save status transitions, plan approvals, checksums, code SHA, review evidence and usage to durable storage through the backend. For uncertain state after interruption, require recovery verification before replay.

## On any unsafe or missing capability

Fail closed. State which adapter/capability is unavailable and what verified setup is required. No provider receives filesystem/network/secrets access merely by appearing in the registry. Executable permissions are enforced by the backend/OS, not by instructions in this Skill.

## User-facing response

Report: plan version, current task, chosen agent and role, selection rationale, relevant base/head SHAs, test gate status, review findings, actual-vs-estimated usage, blockers, and what needs approval. In the Codex Desktop host, show branch comparisons against `integration/<run_id>` for committed changes; uncommitted changes appear in the working tree Diff.
