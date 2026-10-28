# Vendor-neutral amendment to the approved 30-decision architecture

## Scope change

Original default: Codex Desktop = user entry; Codex = planner/reviewer; Antigravity = developer. This remains the **default profile**, not a hardcoded restriction. The user now requires any future AI agent to be eligible through a plug-in adapter, provided its capabilities can be verified and approved.

## Three separate layers

1. **Skill surface**: portable `SKILL.md` for human/AI instructions; host-specific thin installation if needed.
2. **Deterministic orchestration**: Python `aio` engine (DAG, policy, budget, SQLite, worktree, execution/leases), independent of the chosen AI model/provider.
3. **Adapter registry**: dynamically discover/call arbitrary agents via CLI/API/MCP/remote worker/custom connector, with versioned capability and security checks. Unsupported hosts can still be workers via their supported transport, even if they do not read Skills.

## Non-negotiable invariants inherited from decisions

- Plan approved once; scope/architecture/permissions/budget changes trigger human approval.
- Independent review, deterministic test gates and up to 3 repairs.
- Two initial concurrent developer workers, isolated worktrees and ordered integration.
- Automatic local integration only; no automatic push, protected branch merge, or deployment.
- Project-specific budgets and SQLite; global scheduler resource limit.
- Crash-safe checkpoints, no duplicate execution of an uncertain task.
- Capabilities and usage must be verified, never guessed.

## Provider-independent control flow

```text
Human -> Host (Codex today, replaceable tomorrow)
          -> universal-agent-orchestrator Skill
          -> aio engine and policy gate
          -> adapter registry/capability probes
             -> selected planner / developer / reviewer / tester agents
          -> isolated Git worktrees + SQLite evidence
          -> integration branch + final human acceptance
```

The Skill **does not itself guarantee** background execution or cross-agent IPC. Those belong to the `aio` daemon and adapter implementations, which must be built and independently tested in four phases from the original architecture.

## Phasing impact

P0: inventory installed agents and their supported invocation/permission modes; ensure no permission bypass.
Phase 1: implement single developer/reviewer loop using generic adapter protocol (not vendor hardcoding).
Phase 2: DAG routing, 2 independent developer worktrees, role constraints and integration.
Phase 3: budget routing, Ponytail optional policy, checkpoint persistence, model selection.
Phase 4: launchd, multiple projects, Skill host bridges, reporting, audit and upgrade.
