# Universal Agent Orchestrator · Agent-agnostic Skill Starter

This package converts the approved 30-decision Codex × Antigravity design into a **provider-neutral Skill interface**. It is a **starter / control-plane specification**, not a complete multi-agent orchestration service. The included scripts validate and route sample configurations without calling external agents.

## Why this is not limited to any named agent

- A role is *what a worker does* (`planner`, `developer`, `reviewer`, `tester`, `integrator`).
- A provider/agent is *who can do it*. Providers may offer CLI, API, MCP, or another approved transport.
- A capability is *what is verified*. Product marketing claims are not an execution guarantee.
- A trust tier sets *maximum permitted automation*, independent from task complexity and price.
- A routing policy chooses which verified agent to assign to which role and task.

Install `SKILL.md` in a host's supported Skill directory (for example Codex `~/.agents/skills/universal-agent-orchestrator/`, Claude Code `~/.claude/skills/universal-agent-orchestrator/`). Other hosts require their own verified Skill installation procedure. You may use the included installer for Codex/Claude; unknown hosts are intentionally manual.

## Quick local prototype

```bash
python3 scripts/doctor.py --registry config/agent-registry.example.json --policy config/policy.example.json
python3 scripts/route.py --registry config/agent-registry.example.json --task config/task.example.json
python3 -m unittest discover -s tests -v
```

All entries in the example registry are disabled. Set up a real adapter, verify its CLI/API and sandbox behavior, then mark it eligible via a verified probe. Do not enable a provider solely by editing its name.

## Installation

```bash
bash scripts/install.sh codex
# or
bash scripts/install.sh claude
```

Install from the extracted Skill directory. Installer refuses to overwrite an existing Skill. It installs the **Skill instructions and helper scripts**, not an `aio` orchestration daemon.

## Architecture source

The approved 30 decisions remain valid. See `references/architecture.md` for the provider-neutral amendments; see `references/adapter-contract.md` for adding any new agent, and `references/tiering.md` for multi-axis classification.

## Local visual console / 本地可视化控制台

The tested fixture under `orchestration-test/` includes a loopback-only GUI that shows Antigravity state, event progress, measured token usage, changed paths, deterministic tests and Codex review results. / `orchestration-test/` 中包含已验证的本地控制台，可显示 Antigravity 状态、事件进度、实测 token、变更文件、确定性测试和 Codex 审核结果。
