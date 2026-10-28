#!/usr/bin/env python3
"""Static registry/policy validator. Does NOT contact providers or execute agents."""
import argparse
import json
from pathlib import Path

ROLES = {"planner", "developer", "reviewer", "tester", "integrator", "analyst"}
TRANSPORTS = {"cli", "api", "mcp", "remote-worker", "custom"}

def load(path):
    with Path(path).open(encoding="utf-8") as f:
        return json.load(f)

def validate(registry, policy):
    errors, warnings = [], []
    agents = registry.get("agents")
    if registry.get("protocol_version") != "1" or policy.get("protocol_version") != "1":
        errors.append("Only protocol_version=1 is supported by this starter")
    if not isinstance(agents, list):
        return ["registry.agents must be a list"], []
    ids = set()
    for agent in agents:
        if not isinstance(agent, dict):
            errors.append("Each agent must be an object")
            continue
        ident = agent.get("id")
        if not isinstance(ident, str) or not ident:
            errors.append("Every agent needs a nonempty id")
            continue
        if ident in ids:
            errors.append(f"Duplicate agent id: {ident}")
        ids.add(ident)
        if agent.get("transport") not in TRANSPORTS:
            errors.append(f"{ident}: unknown transport")
        if not set(agent.get("roles", [])).issubset(ROLES):
            errors.append(f"{ident}: invalid roles")
        tier = agent.get("assurance_tier")
        if type(tier) is not int or tier not in range(4):
            errors.append(f"{ident}: assurance_tier must be integer 0-3")
        if agent.get("enabled"):
            if agent.get("verification") != "verified":
                errors.append(f"{ident}: enabled without verified capability probe")
            if not agent.get("adapter"):
                errors.append(f"{ident}: enabled without adapter")
            if "reviewer" in agent.get("roles", []) and not agent.get("read_only_enforced"):
                errors.append(f"{ident}: reviewer lacks enforced read-only capability")
            if agent.get("assurance_tier", 0) == 0:
                errors.append(f"{ident}: enabled at E0")
            warnings.append(f"{ident}: declaration is NOT proof of real OS sandboxing; run a live conformance probe")
        if not agent.get("enabled"):
            warnings.append(f"{ident}: disabled (not dispatchable)")
    for key in ("allow_automatic_push", "allow_automatic_deploy", "allow_automatic_protected_merge"):
        if policy.get(key) is not False:
            errors.append(f"{key} must be false under the approved 30 decisions")
    if not policy.get("require_independent_read_only_review"):
        errors.append("independent read-only review is required")
    max_dev = policy.get("global_max_concurrent_developers")
    if type(max_dev) is not int or max_dev < 1:
        errors.append("global_max_concurrent_developers must be positive integer")
    return errors, warnings

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", required=True)
    ap.add_argument("--policy", required=True)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    try:
        reg, pol = load(args.registry), load(args.policy)
        errors, warnings = validate(reg, pol)
    except (ValueError, OSError) as exc:
        errors, warnings = [str(exc)], []
    result = {"ok": not errors, "errors": errors, "warnings": warnings, "real_provider_probes_performed": False}
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("STATIC VALIDATION:", "PASS" if result["ok"] else "FAIL")
        for msg in errors:
            print("ERROR:", msg)
        for msg in warnings:
            print("NOTE:", msg)
        print("Real provider probes: NOT PERFORMED")
    raise SystemExit(0 if not errors else 1)

if __name__ == "__main__":
    main()
